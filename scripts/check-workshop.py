#!/usr/bin/env python3
"""Check fixed-source integrity, stage artifacts, navigation and download bytes.

This checks the workshop distribution, not scientific approval or the separate
SDP specification validator. Its known failure is recorded in validation/.
Run after build-workshop-kit.py; optionally pass --site site/docs after rendering.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "episodes/files/fraser-coho-workshop"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--site", type=Path)
args = parser.parse_args()


def rows(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def check(condition, message):
    if not condition:
        raise AssertionError(message)


source = KIT / "raw_data/nuseds-fraser-coho-2023-2024.csv"
data = rows(source)
check(len(data) == 173 and len(data[0]) == 14, "Source shape changed")
check(len({(r["POP_ID"], r["ANALYSIS_YR"]) for r in data}) == 164, "Population-year counts changed")
check(sum(r["NATURAL_ADULT_SPAWNERS"] == "" for r in data) == 13, "Missingness changed")
for item in json.loads((KIT / "raw_data/source-manifest.json").read_text())["files"]:
    check(hashlib.sha256((KIT / item["path"]).read_bytes()).hexdigest() == item["sha256"],
          "Pinned source changed: " + item["path"])
for stage in ("draft-sdp", "seeded-sdp", "reference-sdp"):
    package = KIT / "checkpoints" / stage
    check((package / "data/escapement.csv").read_bytes() == source.read_bytes(), f"{stage} changed source bytes")
    dictionary = rows(package / "metadata/column_dictionary.csv")
    check([r["column_name"] for r in dictionary] == list(data[0]), f"{stage} dictionary fields differ")
    if stage != "reference-sdp":
        for collection in (dictionary, rows(package / "metadata/codes.csv")):
            check(not any(v for r in collection for k, v in r.items() if k.endswith("_iri")),
                  f"{stage} contains an unreviewed assigned IRI")

nodes = rows(KIT / "reference/dataset-nodes-working.csv")
ids = {r["node_id"] for r in nodes}
check(len(ids) == len(nodes), "Graph node IDs are duplicated")
for edge in rows(KIT / "reference/dataset-edges-working.csv"):
    check(edge["subject_id"] in ids and edge["object_id"] in ids and edge["relationship"], "Graph edge incomplete")
check("Completion: pending" in (KIT / "worksheets/peer-review.md").read_text(), "Shipped learner review is not pending")
check(len(rows(KIT / "ai/recorded-suggestions.csv")) == 13, "Recorded comparison proposals missing")
check(all(not r["human_decision"] and not r["reviewer"] for r in rows(KIT / "ai/comparison-worksheet.csv")), "Shipped AI worksheet claims human decisions")
for path in [*KIT.glob("reference/*.svg"), *ROOT.glob("episodes/fig/*.svg")]:
    ET.parse(path)

durations = []
for n in range(1, 13):
    page = (ROOT / f"episodes/session-{n}.Rmd").read_text()
    durations.append(sum(int(re.search(rf"^{key}: (\d+)$", page, re.M)[1]) for key in ("teaching", "exercises")))
    check("../glossary.html" not in page and "../reference.html" not in page, "Link escapes deployment root")
    if n < 4:
        check(not re.search(r"```(?:\{r|python)|create_sdp\(", page), "Early chapter contains an ingestion code example")
check(durations[:7] == [55, 55, 65, 40, 70, 30, 45] and sum(durations[:7]) == 360,
      "Day 1 beginner route is not six hours")
check(durations[7:] == [60, 75, 90, 75, 60] and sum(durations[7:]) == 360,
      "Day 2 semantic authoring route is not six hours")
check(sum(durations) == 720, "Full teaching route is not twelve hours")
configured = re.findall(r"^- (session-\d+\.Rmd)$", (ROOT / "config.yaml").read_text(), re.M)
check(configured == [f"session-{n}.Rmd" for n in range(1, 13)], "Chapter navigation differs from the two-day sequence")

for required in ("README.md", "vocabulary/estimate-methods.ttl", "vocabulary/concepts-working.csv",
                 "model/model.ttl", "model/instances.ttl", "model/record-shapes.ttl",
                 "bridge/bridge.ttl", "bridge/mapping-decisions-working.csv",
                 "worksheets/term-request.md", "contributions/source-clarification-example.md",
                 "scripts/check_reference.py", "scripts/requirements.txt"):
    check((KIT / "semantic-lab" / required).is_file(), "Missing Day 2 artifact: " + required)
day2_receipt = json.loads((KIT / "validation/day2-reference-checks.json").read_text())
check(day2_receipt["status"] == "pass", "Day 2 reference checks have not passed")
for item in day2_receipt["checked_files"]:
    check(hashlib.sha256((KIT / item["path"]).read_bytes()).hexdigest() == item["sha256"],
          "Stale Day 2 reference evidence: " + item["path"])

reference = KIT / "checkpoints/reference-sdp"
manifest = json.loads((reference / "publication/test/knb-manifest.json").read_text())
check(manifest["knb_environment"] == "test" and manifest["public"] and manifest["representation"] == "expanded", "Wrong publication plan")
check(manifest["status"] == "dry_run", "Update verification status deliberately when a real deposit is made")
for obj in manifest["objects"]:
    body = (reference / obj["path"]).read_bytes()
    check(len(body) == obj["size"] and hashlib.sha256(body).hexdigest() == obj["sha256"], "Stale planned object: " + obj["path"])
def included(path):
    # Match build-workshop-kit.py's distribution rule. A complete inventory is
    # necessary: checking only listed entries cannot detect a missing member.
    rel = path.relative_to(KIT)
    return (path.is_file() and not any(part.startswith(".") for part in rel.parts)
            and "__pycache__" not in rel.parts and "output" not in rel.parts
            and path.suffix != ".pyc")


inventory_path = KIT / "validation/kit-files.json"
included_files = {p.relative_to(KIT).as_posix() for p in KIT.rglob("*") if included(p)}
inventory = json.loads(inventory_path.read_text())["files"]
inventory_names = [item["path"] for item in inventory]
check(len(inventory_names) == len(set(inventory_names)), "Duplicate kit inventory entries")
check(set(inventory_names) == included_files - {"validation/kit-files.json"}, "Kit inventory membership differs from distribution files")
for item in inventory:
    body = (KIT / item["path"]).read_bytes()
    check(len(body) == item["bytes"] and hashlib.sha256(body).hexdigest() == item["sha256"], "Stale kit inventory: " + item["path"])
with zipfile.ZipFile(KIT.with_suffix(".zip")) as archive:
    check(archive.testzip() is None, "Corrupt ZIP")
    names = archive.namelist()
    check(len(names) == len(set(names)), "Duplicate ZIP members")
    check(set(names) == {"fraser-coho-workshop/" + name for name in included_files}, "ZIP membership differs from distribution files")
    for name in archive.namelist():
        rel = Path(name).relative_to("fraser-coho-workshop")
        check(archive.read(name) == (KIT / rel).read_bytes(), "Stale download: " + name)

if args.site:
    class Links(HTMLParser):
        def __init__(self):
            super().__init__(); self.links = []; self.ids = set()
        def handle_starttag(self, tag, attributes):
            attrs = dict(attributes)
            if "id" in attrs: self.ids.add(attrs["id"])
            if tag in {"a", "img", "script", "link"}:
                link = attrs.get("href", attrs.get("src"))
                if link: self.links.append((link, tag, attrs.get("rel", "")))
    site = args.site.resolve()
    check(site.is_dir(), "Rendered site directory does not exist")
    deployed_kit = site / "files/fraser-coho-workshop"
    deployed_zip = site / "files/fraser-coho-workshop.zip"
    check(deployed_zip.is_file() and deployed_zip.read_bytes() == KIT.with_suffix(".zip").read_bytes(),
          "Rendered workshop ZIP is absent or stale; rebuild the site after the kit")
    for name in sorted(included_files):
        deployed_file = deployed_kit / name
        check(deployed_file.is_file() and deployed_file.read_bytes() == (KIT / name).read_bytes(),
              "Rendered kit file is absent or stale: " + name)
    for source_figure in ROOT.glob("episodes/fig/*.svg"):
        deployed_figure = site / "fig" / source_figure.name
        check(deployed_figure.is_file() and deployed_figure.read_bytes() == source_figure.read_bytes(),
              f"Rendered {source_figure.name} is absent or stale")
    pages = {p.resolve(): Links() for p in site.rglob("*.html")}
    check(bool(pages), "Rendered site contains no HTML pages")
    for path, parsed in pages.items(): parsed.feed(path.read_text())
    errors = set()
    theme_warnings = set()
    # Bundled Varnish currently references five absent incubator favicon assets.
    # Retire this exact, visible warning exception when Varnish ships them.
    # Navigation, images, scripts, stylesheets and other missing assets still fail.
    missing_theme_icons = {
        "favicons/incubator/apple-touch-icon.png": "apple-touch-icon",
        "favicons/incubator/favicon-32x32.png": "icon",
        "favicons/incubator/favicon-16x16.png": "icon",
        "favicons/incubator/site.webmanifest": "manifest",
        "favicons/incubator/safari-pinned-tab.svg": "mask-icon",
    }
    for path, parsed in pages.items():
        for link, tag, rel in parsed.links:
            url = urlsplit(link)
            if url.scheme or url.netloc or not url.path and not url.fragment: continue
            # Site-root host routes (e.g. favicon) are outside relative lesson links.
            if url.path.startswith("/"): continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir(): target = target / "index.html"
            if not target.is_relative_to(site): errors.add(f"{path.relative_to(site)}: escapes rendered site: {link}")
            elif not target.exists():
                target_name = target.relative_to(site).as_posix()
                if tag == "link" and missing_theme_icons.get(target_name) == rel:
                    theme_warnings.add(target_name)
                else:
                    errors.add(f"{path.relative_to(site)}: missing {link}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.add(f"{path.relative_to(site)}: missing anchor {link}")
    for warning in sorted(theme_warnings):
        print("WARNING: bundled Varnish theme asset is missing: " + warning)
    check(not errors, "Rendered links failed:\n" + "\n".join(sorted(errors)))
print("PASS: workshop source, checkpoints, human artifacts, two 360-minute routes (720 total), test plan, ZIP" + (" and rendered links" if args.site else ""))
print("Separate acceptance remains pending: scientific review, independent SDP validator fix, free API rehearsal and anonymous live test-catalog verification.")
