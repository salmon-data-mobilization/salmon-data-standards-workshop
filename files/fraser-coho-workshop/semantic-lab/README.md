# Day 2 semantic lab

Use this lab from the extracted `fraser-coho-workshop/` project root after the actual human graph, dictionary, decomposition and peer review from Day 1. It supplies the five chapters of Part 2: **60 + 75 + 90 + 75 + 60 = 360 minutes**. Both days together contain 720 minutes of teaching and activities, excluding breaks.

The source remains `raw_data/nuseds-fraser-coho-2023-2024.csv`, all 173 rows and 14 columns. The model illustrates selected actual rows with a source hash and row-position trace; it does not replace the full source table or declare a population/year key. No source data are renamed, synthesized, deduplicated or aggregated.

## What you will make

| Chapter | Start with | Create or review |
| --- | --- | --- |
| 8 — choose a route | `worksheets/routing-decisions.csv` | Evidence-backed choices about reuse, representation and stewardship |
| 9 — build a vocabulary | `worksheets/vocabulary-concepts.csv` and [vocabulary guide](vocabulary/README.html) | Four draft concepts in a SKOS scheme, with three sourced definitions and one explicit gap; stewardship record |
| 10 — formalize the graph | `worksheets/model-statements.csv`, `model/model.ttl`, `model/instances.ttl`, `model/record-shapes.ttl` | Small local RDF/OWL model and checks of selected consequences and required data |
| 11 — build bridges | `worksheets/bridge-decisions.csv`, `bridge/mapping-decisions-working.csv`, `bridge/bridge.ttl` | A proposed mapping with evidence, rejected alternatives and consequence checks |
| 12 — prepare a contribution | [contribution guide](contributions/README.html) and [request worksheet](worksheets/term-request.html) | A complete unsubmitted term request or source-clarification draft and next review step |

Paths in this table are relative to `semantic-lab/`. In the terminal, stay at the **kit root** and include that prefix. Preserve the supplied working examples; save your own generated Turtle and check reports under `output/semantic-lab/`. Edit the blank worksheets as the chapters direct. Candidate request previews use their separate, explicitly named folders under `output/`.

## Install checking tools before the class

```bash
python3 -m venv .venv-semantic
. .venv-semantic/bin/activate
python -m pip install -r semantic-lab/scripts/requirements.txt
```

On Windows activate `.venv-semantic/Scripts/Activate.ps1` in PowerShell. The requirements pin rdflib 7.1.4, owlrl 7.1.4 and pyshacl 0.30.1. Installation downloads software; the subsequent lab checks read local files without retrieval, ontology imports or AI requests. R and spreadsheet users can author and review the same artifacts with a partner running Python checks. The optional Chapter 12 R/Python request preview uses the Day 1 package environment, not this small RDF-only environment.

After completing the chapter's actual preparation and authoring:

```bash
python semantic-lab/vocabulary/check_vocabulary.py --vocabulary output/semantic-lab/estimate-methods.ttl
python semantic-lab/scripts/check_model.py
python semantic-lab/scripts/check_bridge.py
```

The vocabulary command reads your four completed concept rows. The model and bridge commands default to the supplied reference artifacts; use the `--model`, `--instances`, `--shapes` or `--bridge` options shown in Chapters 10–11 to inspect your copies. Reference checks have deliberately bounded expectations. A changed example can fail because it no longer makes the taught claims; investigate and document the difference rather than weakening the check to obtain a pass. Preserve reports with `--report output/semantic-lab/new-report-name.json` where supported.

## Understand the technical evidence

The supplied [Day 2 validation receipt](../validation/day2-reference-checks.json) records maintainer checks of the shipped draft artifacts. It does **not** complete a learner's human review. The learner commands require the existing Day 1 preparation record. The separate maintainer command `python semantic-lab/scripts/check_reference.py` explicitly inspects model/bridge references with a still-pending distributed worksheet; it creates no learner answer or approval.

The exercises include Turtle parsing, selected OWL RL inferences, concrete SHACL conditions, source-value traces, and checks against mixing SKOS concept and OWL class IRIs. Some deliberately changed assertions are examined only in memory to demonstrate errors. The original table and shipped examples remain unchanged. A statement absent from this bounded rule closure is not automatically false. These checks do not constitute a full OWL DL consistency assessment of the SDO and all its imports.

## Keep identity, evidence and authority separate

Every newly defined teaching term uses `https://example.org/fraser-coho-workshop/terms/`; source-record illustration instances have their own `https://example.org/fraser-coho-workshop/instances/` identifiers. These are classroom identifiers, not production vocabulary pages or official DFO/SDO terms. Each new resource remains draft. The shared-anchor excerpt records its original namespace and source commit; it does not give us authority to rename or redefine those terms.

Source wording, working interpretation, a proposed bridge, and a steward's decision are different evidence. Draft annotations do not turn off RDF or OWL inference when the file is loaded, so keep experimental bridges out of production imports. Do not copy these lab files into canonical SDP metadata or update the Day 1 package mappings without the applicable review and rebuild.

The supplied scientific interpretations remain pending Bruno and Tom's review through Brett. No live AI, issue submission, ontology release, production deposit or DOI request is required. A justified source question or local-retention decision is a useful outcome; this dataset need not contain a previously unknown shared concept.
