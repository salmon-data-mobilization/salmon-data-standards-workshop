---
title: "Build the Package from Your Human Description"
teaching: 20
exercises: 20
---

:::::::::::::::::::::::::::::::::::::: questions

- How does our diagram and dictionary become a Salmon Data Package?
- Which facts can software infer, and which decisions must we supply?
- How can we rebuild a draft without losing our review work?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Confirm the human diagram, dictionary, and peer review are complete before using packaging tools.
- Build or inspect an SDP containing the same 173-row, 14-column Fraser Coho source.
- Trace a human-written description into its canonical metadata field.
- Distinguish draft validation from scientific review and publication readiness.

::::::::::::::::::::::::::::::::::::::::::::::::

## The problem: useful descriptions need to travel with the data

Your diagram explains the relationships. Your dictionary explains the columns. A [Salmon Data Package](glossary.html#salmon-data-package) organizes data and standardized metadata for another person and their software to inspect. This chapter transfers selected human descriptions into that structure while retaining the richer diagram and reasoning in the workshop project.

**Before opening metasalmon or supplying anything to AI**, complete `worksheets/dataset-nodes.csv`, `worksheets/dataset-edges.csv`, `worksheets/data-dictionary.csv`, and `worksheets/variable-decomposition.csv`. Record the peer reviewer, date, decision, and remaining questions in `worksheets/peer-review.md`. Revise any relationship or definition the reviewer cannot explain, and identify questions that need further evidence.

Use the `reference/*-working.csv` files to compare interpretations with your own reviewed worksheets. Keep the reasons for your decisions alongside them.

## Open the common workshop project

Download and extract the [workshop kit](files/fraser-coho-workshop.zip), as described in [Setup](setup.html). Work from its `fraser-coho-workshop/` directory. Keep the source file unchanged throughout:

```text
fraser-coho-workshop/
  raw_data/nuseds-fraser-coho-2023-2024.csv
  worksheets/                 # your diagram, dictionary, and peer review
  reference/                  # facilitator comparison drafts and source notes
  scripts/build_sdp.R         # or build_sdp.py
  checkpoints/                # supplied, labelled comparison stages
  output/fraser-coho-workshop-sdp/
```

The early column view was a way to focus attention. The package still contains **all 173 rows and 14 columns**, with dataset ID `fraser-coho-workshop` and table ID `escapement`. `POP_ID` plus `ANALYSIS_YR` is not guaranteed to identify one row: the source includes repeated population-year combinations, including different waterbody records. Preserve those distinctions.

## Generate or inspect the draft

The kit build script checks the peer-review record before reading the data into the packaging workflow. It starts with semantic seeding and AI disabled, imports each column's `working_definition`, and refuses to overwrite an existing output. Read its comments so you can trace the inputs and outputs.

**Compare the supplied technical bindings with your human worksheet before building.** Roles, value types, and the individual-count unit are supplied choices in the helper script; they are not automatically translated from your diagram or decomposition. Record any mismatch or open question. If a binding needs changing, review and edit the script before building. The source definitions and human reasoning remain your baseline for evaluating these choices.

::::::::::::::::::::::::::::::::::::: group-tab

### R

Run from the workshop project root:


``` r
# The script checks the preparation and imports reviewed working definitions.
# Compare its supplied roles, value types, and units with your worksheets first.
# Its create_sdp() step uses seed_semantics = FALSE and llm_assess = FALSE.
source("scripts/build_sdp.R")

pkg_path <- file.path("output", "fraser-coho-workshop-sdp")
pkg <- metasalmon::read_salmon_datapackage(pkg_path)
pkg$dataset
pkg$tables
pkg$dictionary
```

The workshop uses `metasalmon` **v0.5.0**. The script is the reproducible record of metadata changes. Keep reviewed text edits in the working worksheets or explicit script calls, then preserve the current output before making a new build.

### Python

Run from the workshop project root:

```bash
python scripts/build_sdp.py
```

Then inspect the written files in Python:

```python
from pathlib import Path
from metasalmonpy import read_salmon_datapackage

pkg_path = Path("output") / "fraser-coho-workshop-sdp"
pkg = read_salmon_datapackage(str(pkg_path))
print(pkg["dataset"])
print(pkg["tables"])
print(pkg["dictionary"])
```

The workshop uses `metasalmonpy` **v0.4.0**. It can create and inspect the package; its native semantic-review functions differ from the R lane, as Chapter 5 explains. Seeding remains off here so that candidate search follows the human-description stage.

### Spreadsheet

After peer review, copy `checkpoints/draft-sdp/` into `output/fraser-coho-workshop-sdp/` only if that destination does not already exist. Open the metadata CSVs and compare them against your own worksheets. Transfer your supported descriptions into the appropriate existing fields, retaining your source and decision notes separately.

Open CSVs through your spreadsheet application's import dialog. Preserve identifiers and codes as text, date spellings, blank values, and all source rows. Avoid an automatic save over the supplied source. An R or Python collaborator can later rebuild the package descriptor and run its validator.

::::::::::::::::::::::::::::::::::::::::::::::::

## Follow one description into the package

The [field reference](field-reference.html) explains each metadata column and its allowed values. Use it while editing; you do not need to memorize the entire format.

| Human preparation | Package destination | What to check |
| --- | --- | --- |
| Dataset purpose, source, and caveats | `metadata/dataset.csv` and accompanying notes | Credit the source and distinguish the teaching derivative. |
| What one row represents | `metadata/tables.csv` | State the row meaning; do not declare a key without checking it. |
| Exact column name and working definition | `metadata/column_dictionary.csv` | Definitions are imported by exact source column name. Compare the supplied role, type, and unit bindings with the worksheet before building. |
| Meaning of a stored category | `metadata/codes.csv` | Preserve the stored value and describe its scope. |
| Human graph, decomposition, evidence, and questions | Working worksheets and reference notes in the project | Retain these for the later mapping review; the build copies only the peer-review record into the SDP as `preparation-review.md`. |

Software can suggest that `NATURAL_ADULT_SPAWNERS` holds numeric values. The official NuSEDS dictionary describes mature salmon excluding jacks; it does not establish a natural-origin restriction. The header alone cannot resolve that distinction. Your source-based definition and unresolved question must survive the build. The dictionary's measurement IRI fields are filled in Chapter 5 only when their meanings are supported.

Do not append worksheet-only columns to the canonical metadata CSVs. Methods that vary by row remain associated with the `ESTIMATE_METHOD` code column; the SDP dictionary has no general-purpose `method_iri` column.

## Check the package structure

Run the prepared validation script for your lane, or inspect the facilitator's validation result:

::::::::::::::::::::::::::::::::::::: group-tab

### R


``` r
source("scripts/validate_sdp.R")
```

This stage uses `require_iris = FALSE`. Inspect all messages and connect them to the relevant metadata field.

### Python

```bash
python scripts/validate_sdp.py
```

This stage uses `require_iris=False`. Inspect all messages and connect them to the relevant metadata field.

### Spreadsheet

Use the [metadata field reference](field-reference.html#review-and-validation) to inspect required fields and allowed values. Ask your collaborator to run the validator against your edited files. Record your inspection notes and the validator's results so you can compare them.

::::::::::::::::::::::::::::::::::::::::::::::::

Draft validation checks the package's structure. Reviewing the source definitions, biological interpretation and licence requires separate evidence; carry those questions into the next chapters.

::::::::::::::::::::::::::::::::::::: challenge

## Activity: trace and explain one field

Work in pairs for 20 minutes:

1. Confirm the graph, dictionary, and peer-review record were completed before this build.
2. Build or open the draft, then find one definition you wrote in Chapter 3.
3. Check that the package contains the full source table and keeps blanks distinct from recorded zeroes.
4. Explain one validation message and one scientific question validation cannot answer.
5. Save your evidence and current draft. If you need to rebuild, preserve this output and deliberately choose a new versioned destination; do not overwrite another person's edits.

Your output is a traceable **draft package**, with its human preparation intact.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Human diagramming, dictionary work, and peer review precede packaging tools and AI.
- The same full Fraser Coho source is used in every chapter.
- Canonical metadata fields have defined roles; the working worksheets preserve richer reasoning.
- Validation checks structure; source review checks whether the descriptions fit the data.

::::::::::::::::::::::::::::::::::::::::::::::::
