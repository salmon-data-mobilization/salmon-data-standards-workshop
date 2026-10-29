---
title: Extended Practice With the Fraser Coho Dataset
---

These five optional labs are **outside the 720-minute, two-day workshop**. Each deepens work on the same 173-row, 14-column `raw_data/nuseds-fraser-coho-2023-2024.csv`; no additional dataset, live AI call, or catalog deposit is needed. Choose a lab after completing its prerequisites. Vocabulary and ontology authoring now have a full [Day 2 route](advanced.html), Chapters 8–12.

## Before any lab

Complete the actual [Chapter 2 graph](session-2.html) and [Chapter 3 dictionary, decomposition, and peer review](session-3.html). Retain your named relationships, source evidence, questions, and the real reviewer/date in `worksheets/peer-review.md`. Supplied reference answers and a passing preparation check do not replace that work. Later labs also name the technical chapters they require.

Work in a separate practice folder and preserve the raw CSV, completed worksheets, and existing package. A scratch row number can help trace a record in this particular file; it is not a persistent source identifier. Keep new notes and comparison tables separate from the source. Use spreadsheet filters, R, or Python as you prefer; report what you inspected or executed and what remains unresolved.

## Lab 1: investigate repeated population–year records

**Problem.** A colleague proposes `POP_ID` plus `ANALYSIS_YR` as a unique key. Determine what the repeated records actually show before suggesting a key or changing the [row-grain](glossary.html#row-grain) definition. Allow 35–45 minutes.

1. Count records for each `POP_ID`–`ANALYSIS_YR` combination without deleting or combining rows. Identify every combination with more than one record.
2. Select two repeated combinations. Lay their complete records side by side, including `POPULATION`, `WATERBODY`, `AREA`, `WATERSHED_CDE`, estimate, method, classification, and dates. Mark fields that agree and fields that differ.
3. Compare one selected population across 2023 and 2024. Decide which relationships the file demonstrates and which would need an authoritative location or population crosswalk.
4. Return to your human graph and table definition. Propose one more precise sentence about what a row represents and one source question that prevents a stronger identity claim. Ask a peer to challenge both.

**Output.** A record comparison with source-row references, a revised row-grain sentence, and a short key assessment explaining why the proposed pair succeeds or fails. Preserve every source record.

**Self-check.** You should recover 173 records and 164 distinct population–year combinations. That difference counts additional records, not necessarily the number of repeated groups. A key that happens to be unique in this slice is not automatically a stable source key. No records were discarded as “duplicates” merely because the pair repeats.

## Lab 2: compare missingness, methods, and classifications

**Problem.** A reader treats a blank estimate as zero and assumes a method label explains every missing value. Test those assumptions at the record level, without producing abundance totals or averages. Allow 30–40 minutes.

1. In a scratch table, classify `NATURAL_ADULT_SPAWNERS` as blank, recorded zero, or other recorded value. Keep the original cell alongside this inspection category.
2. Select examples from each category and inspect `ESTIMATE_METHOD`, `ESTIMATE_CLASSIFICATION`, `ESTIMATE_STAGE`, `START_DTT`, and `END_DTT`. Include contrasting records with `Not Applicable` and `NO SURVEY THIS YEAR` where present.
3. Find a record that challenges an initial assumption. Compare its source labels with `raw_data/official-nuseds-dictionary.csv` and your Chapter 3 notes. Separate the documented definition from a pattern you observed in this slice.
4. Write a missing-value explanation that states what the file records and what it does not explain. Ask whether each method/classification combination supports comparing estimates, and retain unanswered questions.

**Output.** A table of at least six individually traceable examples, two supported statements, one counterexample or unresolved exception, and proposed dictionary wording. Do not aggregate spawner values or infer trends.

**Self-check.** The source contains 13 blank estimates and 14 recorded zeroes. These remain distinct. `FINAL` describes source estimate stage; it does not certify your interpretation. A relationship observed among labels does not by itself establish the cause of missingness or comparability between estimates.

## Lab 3: audit code meanings against their sources

**Problem.** A plausible label or starter dictionary may not match the documented operational meaning. Build a small, auditable code review after [Chapter 6](session-6.html). Allow 40–50 minutes.

1. Inventory the distinct stored values, including blanks, for `AREA`, `RUN_TYPE`, `ESTIMATE_METHOD`, and `ESTIMATE_CLASSIFICATION`. Preserve spelling and distinguish a missing cell from a literal code.
2. Select at least four values spanning three fields. Compare the starter descriptions in `raw_data/source-column-dictionary.csv`, the official dictionary, and `reference/code-definitions-working.csv`. Read `reference/scientific-review-packet.md` for conflicts and limitations.
3. For each value, record the field, exact stored value, proposed meaning, source file and definition location, source/retrieval date where available, and whether the claim is documented, inferred, conflicting, or unresolved. The current official dictionary may postdate the source workbook; retain that distinction.
4. Explain whether any apparent synonyms can safely be treated as equivalent. Pay particular attention to `AREA` being described as a subdistrict and to the mixture of code `1`, label `FALL`, and blanks in `RUN_TYPE`.
5. Use the Chapter 6 term-gap process for one unresolved meaning. Draft the evidence question locally; do not assign an invented IRI or submit an issue as part of this lab.

**Output.** A four-or-more-row code audit, one justified correction or retained disagreement, and one draft source or vocabulary question.

**Self-check.** Every meaning has a traceable source or an explicit question. Raw codes are unchanged. Compare full definitions when assessing a mapping, including any differences in scope hidden by similar labels.

## Lab 4: carry one reviewed definition through R and Python

**Problem.** A reviewed dictionary correction must reach both the metadata CSV and the package descriptor. Reproduce one descriptive edit using the Chapter 4 build paths, after completing [Chapter 4](session-4.html). Allow 40–50 minutes; pair across languages if useful.

1. Choose one `working_definition` from your completed `worksheets/data-dictionary.csv` that a real peer has agreed needs a clearer explanation. Save the old text, proposed text, supporting evidence, and actual review decision. This lab changes a description only; semantic acceptance remains the Chapter 5 process.
2. Make a separate practice copy of the project inputs, scripts, and completed human worksheets. Before running each build, choose a new output directory beneath `output/`: set `workshop_path` in the copied `scripts/workshop.R` for R, or `PACKAGE` in the copied `scripts/workshop.py` for Python. Keep dataset ID `fraser-coho-workshop` and table ID `escapement` unchanged. Never reuse an existing output directory.
3. Run the copied `scripts/build_sdp.R` or `scripts/build_sdp.py` once with the old wording to create a baseline draft. Change only the reviewed worksheet definition, select another new output directory, and run the build again. Retain the script/helper settings used for each run. These are fresh unseeded drafts; the exercise does not recreate a later package's semantic review evidence.
4. Locate the selected row in each draft's `metadata/column_dictionary.csv`. Then find the `escapement` resource in `datapackage.json`, its `schema.fields` entry with the same column name, and its `description`. Compare both representations with the worksheet.
5. Repeat with the other language or review a partner's result. Explain how `fill_workshop_metadata()` and `write_workshop_package()` in the supplied R helper correspond to `fill_metadata()` and `write_package()` in the supplied Python helper. These are workshop helpers, not new package APIs. Python 0.4.0 does not supply the R-native metadata setters.

**Output.** An old/new wording record, the real review decision, saved build settings, and a comparison of the worksheet, CSV description, and descriptor description in both lanes. Spreadsheet participants can supply the reviewed edit and inspect a partner's builds.

**Self-check.** The revised wording agrees in the worksheet, metadata CSV, and descriptor. Both outputs retain the 173×14 source values and fixed identifiers. Compare parsed values across languages, not CSV byte formatting. The writer regenerated the descriptor; you did not edit one generated representation alone. Expected missing semantic mappings in these drafts are still visible.

## Lab 5: trace a validation claim into EML and a manifest

**Problem.** A package validation result, an EML schema result, and a planned catalog object answer different questions. Trace their evidence after [Chapter 7](session-7.html) without making a deposit. Allow 35–45 minutes.

1. Read the stage/review notes in `checkpoints/reference-sdp/`, `validation/README.md`, and `validation/reference-validation.json`. Make separate entries for the pinned MetaSalmon check, the independent SDP specification validator, EML validation, human scientific review, and live test-record status. Copy each actual outcome and its evidence location.
2. Select one source field. Trace its definition from your human dictionary into `metadata/column_dictionary.csv` and the descriptor in the reference checkpoint. Note any disagreements and identify evidence that could resolve them.
3. Inspect the reference checkpoint's `metadata/eml-mapping.yml` and `publication/test/eml.xml`. Find the corresponding EML attribute and identify which description, unit/domain, and missing-value information came from the dictionary or the mapping sidecar. Record anything you cannot trace.
4. Open `publication/test/knb-manifest.json` in that checkpoint. Trace the data table, one metadata CSV, EML, and the resource map to their local files and planned identifiers. Record a checksum and its declared algorithm for one object; optionally recompute it locally using that algorithm.
5. Compare the manifest with the current [teaching-record status](reference.html#teaching-record). Explain what additional evidence would establish anonymous catalog access and what evidence would still be needed for scientific approval.

**Output.** A five-claim evidence table plus a source-to-metadata-to-EML-to-manifest trace. Mark each check as executed, inspected, or unavailable and include any unresolved mismatch.

**Self-check.** Your notes distinguish planned objects from available catalog files and identify which validation checks passed or failed, including the known independent-validator failure. Use the [reference page](reference.html#teaching-record) to compare these technical results with the example's domain-review and publication status.
