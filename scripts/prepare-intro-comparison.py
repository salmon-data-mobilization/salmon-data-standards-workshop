#!/usr/bin/env python3
"""Render Chapter 1's comparison; optionally refresh its pinned source excerpts.

Ordinary runs read local files and do not make requests. --refresh-sources
retrieves the two declared Git revisions, preserves original fields and values,
and records the full source and excerpt checksums. It does not map, combine,
infer, publish, or replace the NuSEDS teaching dataset.
"""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import html
import io
import json
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
EXCERPTS = ROOT / "episodes/files/intro-comparison"
FIGURES = ROOT / "episodes/fig"
SOURCES = [
    {
        "id": "yukon",
        "repository": "Pacific-salmon-assess/Yukon-Chinook-CU-reconstructions",
        "revision": "3390d4f2a706e1923785aef24e96eba17a7002c0",
        "path": "data/generated/2025/esc-data.csv",
        "selection": {"stock": "NorthernYukonR.andtribs.", "year": ["2022", "2023"]},
        "repository_license": "MIT",
    },
    {
        "id": "fraser",
        "repository": "sos-program/Approved-WSP-Statuses",
        "revision": "05643cf7474e2c468e21e30edbf1da0ef9a060a8",
        "path": "OUTPUT/Retrospective_RapidStatus_Results_Approved.csv",
        "selection": {"CU_ID": "CK-03", "Year": ["2022", "2023"]},
        "repository_license": "GPL-3.0",
    },
]


def refresh_sources():
    EXCERPTS.mkdir(parents=True, exist_ok=True)
    manifest = {"retrieved": datetime.now(timezone.utc).date().isoformat(), "purpose": "Chapter 1 source excerpts; not an integrated dataset or reviewed mapping", "sources": []}
    for source in SOURCES:
        url = (f"https://raw.githubusercontent.com/{source['repository']}/"
               f"{source['revision']}/{source['path']}")
        with urlopen(url, timeout=30) as response:
            body = response.read()
        table = csv.DictReader(io.StringIO(body.decode("utf-8-sig")))
        fields = table.fieldnames
        records = list(table)
        selection = source["selection"]
        selected = [row for row in records if all(
            row[field] in expected if isinstance(expected, list) else row[field] == expected
            for field, expected in selection.items()
        )]
        if len(selected) != 2:
            raise ValueError(f"Expected two {source['id']} rows; found {len(selected)}")
        path = EXCERPTS / f"{source['id']}-excerpt.csv"
        with path.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(selected)
        # CSV serialization is local; source field names and parsed values are
        # unchanged. Retain the original full-source hash separately.
        manifest["sources"].append({
            **source, "source_url": url,
            "source_sha256": hashlib.sha256(body).hexdigest(),
            "source_rows": len(records), "source_columns": len(fields),
            "excerpt": path.name, "excerpt_rows": len(selected),
            "excerpt_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "license_url": f"https://github.com/{source['repository']}/blob/{source['revision']}/LICENSE",
        })
    (EXCERPTS / "source-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def check_excerpts():
    manifest = json.loads((EXCERPTS / "source-manifest.json").read_text())
    for item in manifest["sources"]:
        path = EXCERPTS / item["excerpt"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != item["excerpt_sha256"]:
            raise ValueError(f"Excerpt changed: {path.name}")
        with path.open(newline="") as stream:
            records = list(csv.DictReader(stream))
        if len(records) != item["excerpt_rows"]:
            raise ValueError(f"Excerpt row count changed: {path.name}")


def render():
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="510" viewBox="0 0 760 510" role="img" aria-labelledby="title desc">',
        '<title id="title">Two routes to deciding whether data fit a question</title>',
        '<desc id="desc">With source files alone, interpretation moves back and forth between columns, documentation and authors. Source-backed descriptions and shared-term links can preserve that work in a reviewed package. Both routes still need a human decision about quantity, scope, scale, methods and uncertainty.</desc>',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#334755"/></marker></defs>',
        '<rect width="760" height="510" rx="8" fill="#fff"/>',
    ]

    def text(x, y, value, size=17, bold=False, anchor="start"):
        parts.append(f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" text-anchor="{anchor}" fill="#172b3a">{html.escape(value)}</text>')

    def box(x, y, w, h, lines, fill="#f4f5f6"):
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="#687582"/>')
        for i, line in enumerate(lines):
            text(x + w / 2, y + 26 + i * 23, line, anchor="middle")

    def arrow(path):
        parts.append(f'<path d="{path}" fill="none" stroke="#334755" stroke-width="2" marker-end="url(#arrow)"/>')

    text(24, 34, "Starting with source files", 22, True)
    for x, lines in [(20, ["Find fields", "in each file"]),
                     (280, ["Read dictionaries", "and methods"]),
                     (540, ["Ask authors", "about the gaps"])]:
        box(x, 58, 200, 72, lines)
    arrow("M 220 94 H 280")
    arrow("M 480 94 H 540")
    arrow("M 640 131 V 153 H 120 V 131")
    text(380, 178, "New evidence can send us back to the columns.", 17, anchor="middle")

    text(24, 225, "Starting with a reviewed Salmon Data Package", 22, True)
    text(24, 250, "A provider has drawn, described and peer-reviewed the meanings.", 17)
    for x, lines in [(20, ["Read recorded", "meanings + evidence"]),
                     (280, ["Follow shared", "definition links"]),
                     (540, ["Check the differences", "against our question"])]:
        box(x, 273, 200, 72, lines, "#e2f0eb")
    arrow("M 220 309 H 280")
    arrow("M 480 309 H 540")
    text(380, 373, "Definitions preserve interpretation; methods and scope still matter.", 17, anchor="middle")

    arrow("M 740 94 H 750 V 444 H 740")
    arrow("M 640 346 V 400")
    box(20, 403, 720, 82, [
        "Human decision: which estimates fit this purpose?",
        "Check quantity, CU, year, scope, scale, method and uncertainty.",
    ])
    parts.append("</svg>")
    (FIGURES / "comparison-workflows.svg").write_text("\n".join(parts) + "\n")
    (FIGURES / "comparison-workflows.mmd").write_text('''flowchart TB
  subgraph source["Starting with source files"]
    columns["Find fields in each file"] --> docs["Read dictionaries and methods"]
    docs --> authors["Ask authors about the gaps"]
    authors --> columns
  end
  preparation["Provider: draw, describe and peer-review the meanings"]
  subgraph package["Starting with a reviewed Salmon Data Package"]
    meanings["Read recorded meanings and evidence"] --> terms["Follow shared definition links"]
    terms --> checks["Check differences against the question"]
  end
  preparation --> meanings
  decision["Human decision: quantity, CU, year, scope, scale, method and uncertainty"]
  source --> decision
  checks --> decision
''')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-sources", action="store_true")
    args = parser.parse_args()
    if args.refresh_sources:
        refresh_sources()
    check_excerpts()
    render()
    print("Checked the pinned intro excerpts and rendered the workflow SVG/Mermaid.")
