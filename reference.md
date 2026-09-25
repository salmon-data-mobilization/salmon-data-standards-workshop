---
title: Reference
---

## One dataset and one workflow

The entire workshop uses **173 rows and 14 columns** from `nuseds-fraser-coho-2023-2024.csv`. The source covers selected Fraser Coho records for 2023 and 2024. Describe the selection and missing values from the supplied source notes; do not infer completeness from the filename.

| Item | Workshop value |
| --- | --- |
| Project root | `fraser-coho-workshop/` |
| Unchanged input | `raw_data/nuseds-fraser-coho-2023-2024.csv` |
| Build script | `scripts/build_sdp.R` or `scripts/build_sdp.py` |
| Working package | `output/fraser-coho-workshop-sdp/` |
| Dataset ID | `fraser-coho-workshop` |
| Table ID | `escapement` |
| Measurement field | `NATURAL_ADULT_SPAWNERS` |

Start with the human graph and dictionary, then build a package, review mappings and AI suggestions, describe codes and term gaps, and inspect validation, EML, and test publication. The [Glossary](glossary.html) explains the concepts; the [Field reference](field-reference.html) connects them to package fields.

That is **Part 1, Chapters 1–7 (six hours)**. [Part 2, Chapters 8–12](advanced.html) adds six hours to create and review vocabulary, ontology, bridge, and contribution artifacts from the same source. The downloadable `semantic-lab/` directory holds the Day 2 files, separately from canonical SDP metadata and the unchanged publication checkpoints.

## Glossary {#glossary}

Use the [workshop glossary](glossary.html) for short definitions of the concepts linked throughout the lesson, and the [field reference](field-reference.html) for their package fields.

## Download and checkpoints

Get the [complete workshop kit][workshop-kit]. Its README locates the source notes, worksheets, scripts, recorded AI outputs, and checkpoints.

| Checkpoint | What it is for | What it does not establish |
| --- | --- | --- |
| `draft-sdp` | Inspect the package structure and initial metadata. | Complete descriptions or accepted mappings. |
| `seeded-sdp` | Inspect candidate evidence and practise review. | That the first-ranked suggestion is correct. |
| `reference-sdp` | Compare a documented technical draft and follow the validation/export workflow. | Domain approval from Bruno or Tom. |

All three checkpoints describe the same source rows and values. Preserve your own worksheet and review decisions before opening a supplied checkpoint. Keep candidate retrieval, human decisions, and technical validation as separate evidence.

## Teaching record {#teaching-record}

**Status: a live KNB Test Node record has not yet been verified for this workshop revision.** The supplied local reference package and Chapter 7's test publication artifacts are available for inspection. A verified catalog link and publication receipt are still pending.

The planned teaching deposit uses the **KNB Test Node** to demonstrate discovery, downloads and metadata. Test services are independent of production services and do not provide the same durability commitment as a production archive.

The reference package remains a **technical draft pending Bruno and Tom's domain review**. A resolvable catalog link, schema-valid EML, or passing package check does not change that status. Consult the supplied provenance and review notes before reusing its interpretations.

## Software functions and lane boundaries

| Task | R 0.5.0 | Python 0.4.0 |
| --- | --- | --- |
| Create and read a package | `create_sdp()`, `read_salmon_datapackage()` | Same function names. |
| Inspect semantic candidates | `review_semantics()` | Supplied candidate CSV and Python inspection. |
| Record native review decisions | `accept_suggestion()`, `reject_suggestion()`, `apply_sdp_semantics()` | Follow the documented target-cell and review-log alternative. |
| Update free-text metadata | `set_sdp_dataset()`, `set_sdp_table()`, `set_sdp_column()`, `set_sdp_code()` | Read, edit copies, and write through `write_salmon_datapackage()`. |
| Validate | `validate_salmon_datapackage()` | Same function name. |
| Export EML | `write_eml_from_sdp()` | Same function name; EML dependencies required. |
| Plan a catalog deposit | `publish_sdp_to_knb()` | Same function name; KNB dependencies required. |

Use the literal code for your lane rather than translating argument names by eye. The [Setup page](setup.html) pins the releases and explains the current [parity gap][metasalmonpy-parity]. Spreadsheet participants inspect the same evidence and record decisions; an R or Python collaborator runs automated checks.

## Review reminders

- Keep an identifier separate from a description: an [IRI](glossary.html#iri) names a term, while its definition and evidence determine whether it fits.
- Treat [row grain](glossary.html#row-grain) as a claim to check against the actual records. Do not declare a primary key merely because a combination sounds plausible.
- A missing spawner estimate is not a zero. Preserve the source value and document what is known about its absence.
- A candidate's rank or score is retrieval evidence, not scientific confidence or approval.
- For row-varying `ESTIMATE_METHOD`, review the code values and their meanings. Do not claim one table-wide method unless the evidence supports it.
- Review-state validation can leave links unresolved. Strict validation applies the publication rules, but passing it still does not establish domain review or permission to publish.
- Keep recorded AI outputs available for the required comparison. A live AI account or paid service is never a prerequisite.

## Source standards

Use the [SDP specification][sdp-specification] for validity rules and the [canonical field reference][sdp-field-reference] for the full field inventory. Measurement decomposition draws on [I-ADOPT][iadopt], concept labels and mappings on [SKOS][skos-reference], observation relationships on [SOSA/SSN][sosa-ssn], and the export on [EML][eml-specification]. The workshop's short explanations support those sources; they do not replace them.
