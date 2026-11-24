---
title: "Write the Dictionary, Decompose Meanings and Review Together"
teaching: 20
exercises: 45
---

:::::::::::::::::::::::::::::::::::::: questions

- What must a dictionary explain beyond column names and data types?
- How do we separate the parts of a compound measurement term?
- What evidence and peer review are needed before packaging or AI-assisted interpretation?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Write working definitions for six focus fields and review all 14 source columns.
- Decompose `NATURAL_ADULT_SPAWNERS` into distinct semantic roles without inventing unsupported qualifiers.
- Reconcile the dictionary with the dataset graph and preserve source wording separately.
- Record an actual peer review, including unresolved questions, before moving to metasalmon or AI.

::::::::::::::::::::::::::::::::::::::::::::::::

## Turn the diagram into a usable explanation

Continue with the unchanged 173-row Fraser Coho table and your Chapter 2 diagram. Open `worksheets/data-dictionary.csv` and `worksheets/variable-decomposition.csv` from the kit in a spreadsheet or text editor. **Write and peer-review your interpretation before using metasalmon or AI.**

A [data dictionary](glossary.html#data-dictionary) explains each field: what it means, how values are represented, which values or codes are allowed, what missing values may mean, and which sources support the explanation. It should help someone identify both appropriate uses and unresolved questions.

The [dictionary worksheet](files/fraser-coho-workshop/worksheets/data-dictionary.csv) includes all 14 source fields. Six rows are marked for you to write: `POP_ID`, `WATERBODY`, `ANALYSIS_YR`, `SPECIES`, `NATURAL_ADULT_SPAWNERS` and `ESTIMATE_METHOD`. The other eight have draft working descriptions to read and amend. Keep the original source description in its own column even when you question it.

### What to record

| Worksheet field | Purpose |
| --- | --- |
| `column_name`, `exercise_focus` | Preserve the exact source name and identify the six writing exercises. |
| `source_description`, `working_definition` | Separate supplied wording from your own evidence-based account. |
| `field_role`, `value_format`, `example_values` | Explain the field's job and representation. A number-shaped identifier is still an identifier. |
| `units`, `code_meanings` | Record the measurement unit or N/A; retain exact category values and cite their definitions or explicit questions. The linked working code list gives source evidence and its limits. |
| `missingness`, `related_fields` | Explain missing-value handling and the context needed to interpret a value. |
| `evidence`, `status`, `open_question` | Make support, review state and uncertainty visible. |

These are **workshop interpretation fields**. They are not a replacement schema for an SDP metadata CSV. Chapter 4 will show how reviewed descriptions map into the package's own metadata fields, while the full worksheets remain supporting context.

## Read the data and source together

Compare the supplied starter dictionary with the [official DFO dictionary](files/fraser-coho-workshop/raw_data/official-nuseds-dictionary.csv) and its [retrieval record](files/fraser-coho-workshop/raw_data/official-dictionary-source.json). The official dictionary was retrieved on 8 September 2026 and may postdate the 2025 workbook used for this slice. Its current definitions support useful corrections to the starter. The <a href="files/fraser-coho-workshop/reference/scientific-review-packet.md" download>scientific-review packet</a> records source questions that still need investigation.

Keep these checks beside the six writing tasks:

| Field | Supported observation | Boundary to preserve |
| --- | --- | --- |
| `POP_ID` | No blanks; 87 distinct IDs in this slice | `POP_ID` plus year does not uniquely identify all 173 rows. Do not equate the source unit with a CU. |
| `WATERBODY` | Names include distinct Nicola River locations | A name in a record does not establish an exclusive population-to-stream relationship. |
| `ANALYSIS_YR` | Officially the year the estimate is for; surveys may continue into the next calendar year | Do not rename it brood year or equate it with every inspection date. |
| `SPECIES` | All rows say `Coho` | Preserve the source label; formal taxon mapping is a later review decision. |
| `NATURAL_ADULT_SPAWNERS` | 13 blanks; some nonblank values have decimals | Preserve blanks and decimals. A source estimate is not necessarily an observed integer count. |
| `ESTIMATE_METHOD` | Nine distinct labels | Describe code meanings; do not assume all labels are interchangeable analytical procedures. |

The other fields supply population naming, area, run type, estimate classification, estimate stage, survey-window dates and watershed code. **Correct `AREA` to NuSEDS subdistrict**: the official dictionary says subdistricts may differ from statistical areas, particularly for Fraser streams. The starter's PFMA wording should not be copied as an accepted definition. For example, `RUN_TYPE` contains `1`, `FALL` and blanks, and `ESTIMATE_CLASSIFICATION` includes `NO SURVEY THIS YEAR`. That context can matter for an estimate, but the classification alone does not explain every missing value.

## Decompose a compound variable

The [Salmon Domain Ontology metamodel](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/main/ontology/views/README.md) separates the thing being described, its characteristic, the complete variable, the activity, its result and its context. This optional teaching view is aligned with the ontology's core; it is not a requirement to turn every phrase into an OWL class.

Use the [decomposition worksheet](files/fraser-coho-workshop/worksheets/variable-decomposition.csv) to unpack `NATURAL_ADULT_SPAWNERS`:

| Part | Working interpretation or question |
| --- | --- |
| Variable | The reported estimate of mature spawners excluding jacks; the field's exact “natural” scope needs confirmation. |
| Entity | The population/group represented by the source record; the precise biological unit needs review. |
| Property | Abundance: the characteristic being represented. |
| Result value | A reported numerical estimate, such as `758`; preserve decimals and missing values. |
| Unit | Individuals is the supplied dictionary's unit; retain that source and seek confirmation of the estimate's interpretation. |
| Context or constraints | Coho in this slice; the current official adult definition excludes jacks. A natural-origin restriction is not established. Row-varying place and year are recorded separately. |
| Statistical modifier | Record only what the source establishes. Do not infer “count”, “total” or “mean” simply from the presence of a number. |
| Method | Refer to the row's `ESTIMATE_METHOD`; its meaning belongs with the procedure that produced the result. |
| Observation context and dimensions | Source population, waterbody, analysis year, survey-window dates, estimate classification and any other demonstrated context. |

The starter dictionary says “natural-origin adult spawners”; the current official DFO definition describes maturity and excludes jacks, without establishing natural origin. Our worksheet retains the starter phrase as **source wording requiring review**, alongside the more cautious working definition. Finding a vocabulary term with the same wording would still leave this source question unanswered. Likewise, a year value varies between rows; it is not a fixed constraint on the entire measurement column. The official definition identifies the estimate year; a claim that it is a brood year or another biological-year basis requires further evidence.

The ontology's [composition rules](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/main/CONVENTIONS.md#12-year-age-abundance-and-method-composition) keep reusable abundance, unit, procedure, qualifiers and dimensions distinct. Your dictionary should do the same in plain language. Specific ontology identifiers and mapping strengths come later.

## Peer review is the handoff to tools

Exchange the diagram, node/edge tables, dictionary and decomposition with another person. Check whether the explanation is understandable, internally consistent and supported by the cited evidence. Identify any questions that need further source information or specialist review.

Use `worksheets/peer-review.md` to record the reviewer, review date, observations, revisions and unresolved questions. The supplied form starts with `Completion: pending` and a blank reviewer. After the reviewer has checked the artifacts and required revisions are complete, record their name and date (as `YYYY-MM-DD`) and change that marker to `Completion: complete`. Give each unresolved scientific question a next step.

A peer-reviewed draft can include open scientific questions. The handoff requires a working interpretation or explicit question for every field, agreement between the graph and dictionary, and a completed peer-review record. Chapter 4's build checks that record before creating the package.

::::::::::::::::::::::::::::::::::::: challenge

## Activity: Write, reconcile and peer review

1. **Write for 20 minutes.** Complete the six focus dictionary rows and the adult-spawner decomposition. Read all eight remaining rows and flag anything unclear. Check the units and code meanings against their cited sources; record questions where a definition is missing. Use examples from the unchanged source table.
2. **Review for 15 minutes.** Your partner traces a source row through the graph and dictionary. Check the six focus fields, the other eight descriptions, blank handling, decimal estimates, the non-unique population/year pair, the unsupported natural-origin restriction, the supported estimate-year definition and any further year-basis claims.
3. **Revise for 10 minutes.** Reconcile conflicting labels or relationships and record what changed. Complete the peer-review record only when the described review has actually occurred.

Compare your results with the [draft dictionary](files/fraser-coho-workshop/reference/data-dictionary-working.csv) and [draft decomposition](files/fraser-coho-workshop/reference/variable-decomposition-working.csv) after your first attempt. Discuss differences in the interpretations, their evidence and their remaining questions.

**Ready for Chapter 4:** the diagram and node/edge tables agree; all 14 dictionary fields have been read; the six writing tasks and one decomposition are complete; a real reviewer and date are recorded; unresolved questions remain explicit. Keep these human-created artifacts as the baseline against which you will later compare software and AI suggestions.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Preserve source descriptions separately from your working interpretation.
- A dictionary explains value meaning, context, representation, missingness and evidence.
- Decomposition separates entity, property, variable, activity, result, unit, method and qualifiers.
- Use the current source definitions for estimate year, adults excluding jacks and subdistrict; retain the unsupported natural-origin restriction as a question.
- Complete a real human peer review before metasalmon or AI ingestion; save the baseline for later comparison.

::::::::::::::::::::::::::::::::::::::::::::::::
