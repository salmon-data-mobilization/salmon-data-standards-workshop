#!/usr/bin/env python3
"""Refresh pinned teaching sources and render the worked example figures.

Run from the lesson repository. Source data is copied from the released R
package, never from mutable generated checkpoints. No inference or deposit.
"""
from pathlib import Path
import csv
import hashlib
import html
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "episodes/files/fraser-coho-workshop"
UPSTREAM = ROOT.parent / "metasalmon"
TAG = "v0.5.0"


def released(path):
    return subprocess.check_output(["git", "show", f"{TAG}:{path}"], cwd=UPSTREAM)


def render_record_preview(figures):
    """Export the Chapter 1 worked preview, taking example values from row 1.

    This compact graph shows source-record relationships. The full conceptual
    graph, including activity/variable/result distinctions, remains in the kit.
    SVG coordinates are presentation only; the lesson provides a text version.
    """
    with (KIT / "raw_data/nuseds-fraser-coho-2023-2024.csv").open(newline="") as source:
        row = next(csv.DictReader(source))

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="856" '
        'viewBox="0 0 760 856" role="img" aria-labelledby="title desc">',
        '<title id="title">One estimate: from source relationships to reusable data and terms</title>',
        '<desc id="desc">The first source record refers to a population, names a waterbody '
        'and reports an estimate. Write and decompose its dictionary, then peer review it '
        'before building the package or evaluating term and AI suggestions. Day 1 previews '
        'catalog publication. Day 2 prepares local vocabulary or ontology drafts and shared '
        'term requests. Following steward review and release, term identifiers can be linked '
        'in a later version of the metadata. The source meaning of natural remains a question.</desc>',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#334755"/></marker></defs>',
        '<rect width="760" height="856" rx="8" fill="#ffffff"/>',
    ]

    def text(x, y, value, size=18, bold=False, anchor="start"):
        parts.append(
            f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" '
            f'font-weight="{"bold" if bold else "normal"}" text-anchor="{anchor}" '
            f'fill="#172b3a">{html.escape(value)}</text>'
        )

    def box(x, y, width, height, fill="#f4f5f6"):
        parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
                     f'rx="7" fill="{fill}" stroke="#687582"/>')

    def arrow(path, dashed=False):
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        parts.append(f'<path d="{path}" fill="none" stroke="#334755" '
                     f'stroke-width="2"{dash} marker-end="url(#arrow)"/>')

    text(24, 32, "1. Draw the source relationships", size=22, bold=True)
    box(264, 54, 232, 48)
    text(380, 84, "First source record", bold=True, anchor="middle")
    arrow("M 286 102 V 132 H 129 V 163")
    arrow("M 380 102 V 163")
    arrow("M 474 102 V 132 H 629 V 163")
    text(179, 125, "refers to", size=16)
    text(389, 142, "names", size=16)
    text(527, 125, "reports", size=16)
    for x, heading, example in [
        (20, "Source population", f'POP_ID {row["POP_ID"]}'),
        (270, "Waterbody", row["WATERBODY"]),
        (520, "Reported estimate", row["NATURAL_ADULT_SPAWNERS"]),
    ]:
        box(x, 164, 218, 62)
        text(x + 109, 189, heading, size=17, bold=True, anchor="middle")
        text(x + 109, 213, example, size=17, anchor="middle")
    text(380, 252,
         f'Year: {row["ANALYSIS_YR"]} · Species: {row["SPECIES"]} · '
         f'Source method: {row["ESTIMATE_METHOD"]}', size=17, anchor="middle")

    arrow("M 380 270 V 293")
    box(20, 296, 720, 114)
    text(40, 324, "2. Write the dictionary and decompose the meaning", size=21, bold=True)
    text(40, 351, "NATURAL_ADULT_SPAWNERS: reported adult-spawner estimate", size=18)
    text(40, 377,
         f'Entity: source population · Property: abundance · Result: {row["NATURAL_ADULT_SPAWNERS"]}',
         size=18)
    text(40, 399, 'Open question: what does “natural” mean in this source?', size=17)

    arrow("M 380 411 V 435")
    box(20, 438, 720, 58, fill="#e2f0eb")
    text(40, 463, "3. Peer-review the graph and dictionary", size=21, bold=True)
    text(40, 486, "Revise the explanation; keep evidence and unanswered questions.", size=17)

    arrow("M 380 497 V 521")
    box(20, 524, 720, 82)
    text(40, 551, "4. Build the package; review term and AI suggestions", size=21, bold=True)
    text(40, 578, "Compare the abundance property with the existing smn:Abundance term.", size=18)
    text(40, 599, "Keep the full variable definition, method context and questions.", size=17)

    arrow("M 200 607 V 633")
    arrow("M 560 607 V 633")
    box(20, 636, 350, 132, fill="#e2f0eb")
    text(38, 664, "Day 1: Make data discoverable", size=19, bold=True)
    text(38, 694, "Validate package → export metadata", size=17)
    text(38, 719, "→ KNB test publication preview", size=17)
    text(38, 747, "Data + descriptions + term links", size=17)
    box(390, 636, 350, 132)
    text(408, 664, "Day 2: Develop missing meanings", size=19, bold=True)
    text(408, 694, "Draft a local vocabulary or ontology,", size=17)
    text(408, 719, "or prepare a shared-term request.", size=17)
    text(408, 747, "Steward review → term publication", size=17)
    arrow("M 560 769 V 797 H 380 V 808", dashed=True)
    text(380, 836, "Released term IRIs can be linked in later versions of the metadata.",
         size=18, anchor="middle")
    parts.append("</svg>")
    (figures / "record-to-reuse.svg").write_text("\n".join(parts) + "\n")

    # An alternate editable graph source carries the same workflow and values.
    mermaid = f'''flowchart TB
  subgraph draw["1. Draw the source relationships"]
    record["First source record"]
    population["Source population identified by POP_ID {row['POP_ID']}"]
    waterbody["Waterbody: {row['WATERBODY']}"]
    result["Reported estimate: {row['NATURAL_ADULT_SPAWNERS']}"]
    record -->|refers to| population
    record -->|names| waterbody
    record -->|reports| result
  end
  dictionary["2. Dictionary and decomposition: entity = source population; property = abundance; natural scope unresolved"]
  review["3. Peer-review the graph and dictionary"]
  package["4. Build SDP; review terms and AI suggestions; compare smn:Abundance"]
  catalog["Day 1: validate, export metadata, preview KNB test publication"]
  terms["Day 2: draft a local vocabulary or ontology, or prepare a shared-term request"]
  release["Steward review and term publication"]
  draw --> dictionary --> review --> package
  package --> catalog
  package --> terms --> release
  release -.->|link released IRIs in later metadata versions| package
'''
    (figures / "record-to-reuse.mmd").write_text(mermaid)


def render_measurement_sketch():
    """Export the small Chapter 2 graph and its editable evidence tables."""
    with (KIT / "raw_data/nuseds-fraser-coho-2023-2024.csv").open(newline="") as source:
        row = next(csv.DictReader(source))
    folder = KIT / "reference"
    field = "NATURAL_ADULT_SPAWNERS"
    official = "Official NuSEDS dictionary retrieved 2026-09-08; may postdate the 2025 workbook"
    sdo = ("https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/"
           "d45f8f7cc857d92af8bbe54a7c89b2a4a14784b2/ontology/")
    node_columns = ["node_id", "label", "node_kind", "source_fields", "evidence", "status", "question"]
    nodes = [
        ["N6", "Reported adult-spawner estimate", "variable", field, official,
         "working interpretation", "Confirm the source meaning of natural and estimation extent."],
        ["N2", f'Source population identified by POP_ID {row["POP_ID"]}', "entity", "POP_ID",
         "First source record; official Population ID definition", "working interpretation",
         "Which population or group of fish does this source identifier cover?"],
        ["N7", "Abundance", "property", field, sdo + "modules/02-observation-measurement.ttl",
         "working interpretation", "Confirm applicability to the defined population and estimate."],
        ["N13", "Mature adults excluding jacks", "scope", field, official,
         "working interpretation", "Confirm applicability of the current definition to the source workbook."],
        ["Q1", "Natural origin?", "unresolved constraint", field,
         "Starter and official dictionary comparison; " + sdo + "modules/07-controlled-vocabularies.ttl",
         "question", "Does this source field restrict the estimate to fish born and reared in the wild?"],
        ["N8", "Observation or estimation activity", "activity", "ESTIMATE_METHOD; START_DTT; END_DTT",
         "Source method and inspection context; " + sdo + "views/README.md",
         "working interpretation", "How were observations collected and the estimate calculated? A row may summarize several activities."],
        ["N11", row["ESTIMATE_METHOD"], "source method label", "ESTIMATE_METHOD",
         "First source record; official method definition is N/A", "observed in file",
         "Which collection and calculation procedures apply to this record?"],
        ["N9", f'Reported result {row[field]}', "example result", field,
         "First source record; starter dictionary supplies unit Individual", "observed in file",
         "Confirm the unit and interpretation across estimate classifications."],
    ]
    edge_columns = ["subject_id", "relationship", "object_id", "source_fields", "evidence", "status", "question"]
    edges = [
        ["N6", "concerns", "N2", "POP_ID; " + field, "Source record and working variable decomposition",
         "working interpretation", "Confirm the estimation extent."],
        ["N6", "represents property", "N7", field, sdo + "modules/02-observation-measurement.ttl",
         "working interpretation", "Review the property definition against the complete variable."],
        ["N6", "has scope", "N13", field, official, "working interpretation",
         "Check the definition against the source workbook's documentation."],
        ["N6", "has constraint?", "Q1", field, "Starter and official dictionary wording differ",
         "question", "Natural-origin applicability is unresolved; this is not an asserted constraint."],
        ["N8", "applies variable", "N6", field, sdo + "views/README.md", "working interpretation",
         "Confirm the relationship between source records and observation/estimation activities."],
        ["N8", "uses source method", "N11", "ESTIMATE_METHOD", "First source record",
         "working interpretation", "The label alone does not define the full procedure."],
        ["N8", "generates result", "N9", field, "Source result and metamodel activity/result distinction",
         "working interpretation", "Confirm which activities contributed to the result."],
    ]
    for name, columns, records in [
        ("measurement-sketch-nodes.csv", node_columns, nodes),
        ("measurement-sketch-edges.csv", edge_columns, edges),
    ]:
        with (folder / name).open("w", newline="") as output:
            writer = csv.writer(output, lineterminator="\n")
            writer.writerow(columns)
            writer.writerows(records)

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="762" '
        'viewBox="0 0 760 762" role="img" aria-labelledby="title desc">',
        '<title id="title">A small measurement sketch for the first NuSEDS record</title>',
        '<desc id="desc">A variable concerns a population, represents abundance and has adult scope. '
        'A dashed arrow asks whether natural origin applies. An observation or estimation activity '
        'applies the variable, uses the source method label Resistivity Counter and generates result 758. '
        'Method details, source scope and unit applicability remain questions. Node and edge tables '
        'record the evidence for these working statements.</desc>',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#334755"/></marker></defs>',
        '<rect width="760" height="762" rx="8" fill="#ffffff"/>',
    ]

    def text(x, y, value, size=17, bold=False, anchor="start"):
        parts.append(f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" '
                     f'font-weight="{"bold" if bold else "normal"}" text-anchor="{anchor}" '
                     f'fill="#172b3a">{html.escape(value)}</text>')

    def box(x, y, width, height, lines, question=False):
        dash = ' stroke-dasharray="6 4"' if question else ""
        parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="7" '
                     f'fill="#f4f5f6" stroke="#687582"{dash}/>')
        for i, line in enumerate(lines):
            text(x + width / 2, y + 23 + i * 22, line, size=16,
                 bold=i == 0, anchor="middle")

    def arrow(path, question=False):
        dash = ' stroke-dasharray="6 4"' if question else ""
        parts.append(f'<path d="{path}" fill="none" stroke="#334755" stroke-width="2" '
                     f'{dash} marker-end="url(#arrow)"/>')

    text(24, 32, "One estimate, unpacked", size=23, bold=True)
    box(20, 66, 220, 84, ["N2 · ENTITY", "Source population", f'POP_ID {row["POP_ID"]}'])
    box(270, 66, 220, 84, ["N7 · PROPERTY", "Abundance"])
    box(520, 66, 220, 84, ["N13 · SCOPE", "Mature adults;", "exclude jacks"])
    box(220, 248, 320, 90, ["N6 · VARIABLE", "Adult-spawner estimate", field])
    box(520, 356, 220, 92, ["Q1 · QUESTION", "Natural origin?", "Source evidence needed"], question=True)
    box(20, 515, 220, 112, ["N11 · METHOD LABEL", row["ESTIMATE_METHOD"], "How collected?", "How calculated?"])
    box(270, 515, 220, 112, ["N8 · ACTIVITY", "Observation / estimation", "Details to investigate"])
    box(520, 515, 220, 112, ["N9 · RESULT", row[field], "Individuals? (starter unit)"])
    arrow("M 270 248 V 199 H 130 V 151")
    text(145, 185, "concerns", size=16)
    arrow("M 380 248 V 151")
    text(391, 213, "represents", size=16)
    text(391, 233, "property", size=16)
    arrow("M 500 248 V 199 H 630 V 151")
    text(550, 189, "has scope", size=16)
    arrow("M 540 293 H 630 V 355", question=True)
    text(545, 322, "has", size=16)
    text(545, 342, "constraint?", size=16)
    arrow("M 380 515 V 339")
    text(391, 425, "applies variable", size=16)
    arrow("M 270 563 H 256 V 483 H 130 V 514")
    text(55, 474, "uses source method", size=16)
    arrow("M 490 563 H 506 V 483 H 630 V 514")
    text(543, 474, "generates result", size=16)
    text(380, 665,
         f'Record context: {row["WATERBODY"]} · {row["ANALYSIS_YR"]} · {row["SPECIES"]}',
         anchor="middle")
    arrow("M 24 701 H 79")
    text(94, 707, "Working statement: follow its evidence in the tables.", size=16)
    arrow("M 24 735 H 79", question=True)
    text(94, 741, "Question: a possible relationship to investigate.", size=16)
    parts.append("</svg>")
    (folder / "measurement-sketch-working.svg").write_text("\n".join(parts) + "\n")

    mermaid = ["flowchart TB"]
    for node_id, label, kind, *_ in nodes:
        mermaid.append(f'  {node_id}["{node_id}: {kind}<br/>{label}"]')
    for start, relation, end, _, _, status, _ in edges:
        connector = "-.->" if status == "question" else "-->"
        mermaid.append(f"  {start} {connector}|{relation}| {end}")
    (folder / "measurement-sketch-working.mmd").write_text("\n".join(mermaid) + "\n")


def main():
    destinations = {
        "inst/extdata/nuseds-fraser-coho-2023-2024.csv": "raw_data/nuseds-fraser-coho-2023-2024.csv",
        "inst/extdata/nuseds-fraser-coho-2023-2024-column_dictionary.csv": "raw_data/source-column-dictionary.csv",
        "inst/extdata/example-data-README.md": "raw_data/upstream-example-data-README.md",
        "data-raw/nuseds_fraser_coho_examples.R": "raw_data/upstream-derivation.R",
    }
    records = []
    commit = subprocess.check_output(["git", "rev-parse", f"{TAG}^{{commit}}"], cwd=UPSTREAM, text=True).strip()
    for source, target in destinations.items():
        content = released(source)
        path = KIT / target
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        records.append({"path": target, "sha256": hashlib.sha256(content).hexdigest(),
                        "source_url": f"https://raw.githubusercontent.com/salmon-data-mobilization/metasalmon/{commit}/{source}"})
    (KIT / "raw_data/source-manifest.json").write_text(json.dumps({
        "package": "metasalmon", "version": TAG, "commit": commit,
        "original_catalog": "https://open.canada.ca/data/en/dataset/c48669a3-045b-400d-b730-48aafe8c5ee6",
        "files": records,
    }, indent=2) + "\n")

    figures = ROOT / "episodes/fig"
    figures.mkdir(exist_ok=True)
    render_record_preview(figures)
    render_measurement_sketch()
    print("Pinned source files and worked example figures prepared.")


if __name__ == "__main__":
    main()
