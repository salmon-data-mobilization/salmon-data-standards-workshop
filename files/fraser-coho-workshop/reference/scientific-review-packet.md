# Fraser Coho workshop model — scientific-review packet

Status: draft prepared for Brett to share; not sent and not scientifically approved.
Prepared for: Bruno and Tom, with Brett coordinating the workshop revision.
Requested review: when the co-authors can assess the complete draft; no fixed deadline.
Reviewer:
Review date:
Review outcome:

## The proposed teaching case

Every chapter uses the same 173-row, 14-column Fraser Coho 2023–2024 NuSEDS
slice. Chapter 1 tours the intended source-to-publication outcome. Chapters
2–3 ask learners to draw a node-and-edge model, write a dictionary and decompose
a compound variable before loading data into metasalmon or AI. Another person
reviews that human baseline before the tool-assisted stages.

The six writing exercises are `POP_ID`, `WATERBODY`, `ANALYSIS_YR`, `SPECIES`,
`NATURAL_ADULT_SPAWNERS` and `ESTIMATE_METHOD`. All 14 fields remain in the
table and dictionary; the eight remaining descriptions are supplied drafts
that learners read and review. No participant-owned dataset is required.

## Artifacts to review together

- [Conceptual diagram and limits](dataset-graph-working.md), with its [SVG view](dataset-graph-working.svg).
- [Node table](dataset-nodes-working.csv) and [edge table](dataset-edges-working.csv).
- [All-field working dictionary](data-dictionary-working.csv), retaining starter descriptions separately.
- [Adult-spawner decomposition](variable-decomposition-working.csv).
- [All observed code meanings](code-definitions-working.csv), separating supported official-source paraphrases from remaining operational questions.
- [Offline metamodel source notes](metamodel-source-notes.md).
- The unchanged source CSV and source records under `../raw_data/`.

These artifacts are draft teaching interpretations. Their preparation, schema
checks or successful package builds must not be represented as your approval.

## Evidence ledger

| Source | What it supports | Limit |
| --- | --- | --- |
| `../raw_data/nuseds-fraser-coho-2023-2024.csv` | Values, field names, record counts, missingness and repeated identifier/year pairs | Does not itself establish every biological definition or observation grain |
| metasalmon's `inst/extdata/nuseds-fraser-coho-2023-2024-column_dictionary.csv` | Starter wording and candidate semantic interpretation | Contains natural-origin and PFMA wording that require correction/reconciliation with the official source |
| `../raw_data/official-nuseds-dictionary.csv` | Current DFO definitions of the source fields | Retrieved 2026-09-08; may postdate the workbook used for this teaching slice |
| `../raw_data/official-dictionary-source.json` | Retrieval URL, timestamp and SHA-256 for the preserved official dictionary bytes | Provenance for retrieval, not independent scientific review |
| `../raw_data/open-canada-record.json` | Current catalog description and source-resource context | A current catalog record is not a historical definition snapshot |
| Salmon Domain Ontology metamodel and core conventions | Distinction between entity, property, variable, activity, result, method, unit, qualifiers and row-varying dimensions | Orientation view is non-normative; workshop diagram does not assert OWL or approved mappings |

Primary source links: [Open Government NuSEDS record](https://open.canada.ca/data/en/dataset/c48669a3-045b-400d-b730-48aafe8c5ee6), [DFO data dictionary](https://api-proxy.edh-cde.dfo-mpo.gc.ca/catalogue/records/c48669a3-045b-400d-b730-48aafe8c5ee6/attachments/Data_Dictionary_NuSEDS_EN.csv), [metasalmon example derivation notes](https://github.com/salmon-data-mobilization/metasalmon/blob/v0.5.0/inst/extdata/example-data-README.md), [SDO metamodel](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/main/ontology/views/README.md) and [SDO composition rules](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/main/CONVENTIONS.md#12-year-age-abundance-and-method-composition).

## Checks from the actual table

- 173 rows, 14 columns, years 2023 and 2024, all species labels `Coho`.
- 87 distinct population IDs; 164 distinct population–analysis-year pairs.
- Repeated pairs: `46170/2023` twice; `46602/2023` and `46602/2024` twice each;
  `46582/2023` and `46582/2024` four times each. They are retained as source records.
- 13 blank adult-spawner estimates; nonblank estimates can have decimals.
- `RUN_TYPE` has `1`, `FALL` and 15 blanks; start and end dates each have 16 blanks.
- No Conservation Unit field or population-to-CU crosswalk occurs in the slice.
- Nine estimate-method labels: Area Under the Curve (84), Peak Live * Expansion
  (39), Not Applicable (27), Combined Methods (12), Resistivity Counter (4),
  Sonar-ARIS (4), Sonar-DIDSON (1), Fixed Site Census (1), Fence (1).

These are file observations, not an assessment of scientific completeness or
comparability. No rows are dropped or aggregated and no blank is changed to zero.

## Proposed interpretations and questions

| Review item | Current working position | Requested scientific input |
| --- | --- | --- |
| Population and record grain | A record refers to the source population; population/year is not a unique key | What differentiates repeated pairs? Which source identifier or dimensions distinguish an annual estimate/SEN record, and are any records nested or overlapping? |
| Waterbody relationship | Use the official wording: waterbody or portion bounding the population on a SEN | Confirm the diagram's direction and label; clarify locations such as Nicola River DAM/DOT without implying exclusive ecological membership |
| Species / population / CU | Keep distinct nodes; no CU assignment is asserted | Supply a dated authoritative crosswalk if a worked CU relationship should be added; do not infer a simple species–CU–stream–population hierarchy |
| Analysis year | Year the estimate is for; inspections may extend into the next calendar year | Confirm applicability to the 2025 workbook and whether further biological-year distinctions need teaching; no brood-year substitution is proposed |
| Adult spawner scope | Mature fish excluding jacks is supported by the current official definition | What exactly does natural qualify here? Does any source support or rule out an origin restriction? Correct the starter's natural-origin claim before it is used as an accepted mapping |
| Unit / estimate interpretation | Preserve numerical values and the starter's Individuals unit as a working interpretation | Confirm interpretation across true/relative abundance classifications and decimal estimates; identify any limits on comparison or aggregation |
| AREA | Describe as subdistrict, not automatically PFMA/statistical area | Confirm the Fraser subdistrict reference and intended learner explanation |
| Method and classification | Keep row-specific method values and source definitions; do not treat every label as interchangeable | Confirm definitions for labels with N/A or absent entries and the most useful comparison pair for learners |
| Missingness | Preserve blanks and use classification/context to investigate | Confirm what can safely be concluded about the 13 missing estimates and date blanks |
| Six-field exercise | Write six; read/review all 14 | Are these the most useful introductory fields, and do the draft graph and decomposition communicate the intended distinctions? |

## Record the actual review

For each decision, record the exact artifact or statement, source/evidence,
accepted wording or required revision, reviewer and date. A response may leave
questions unresolved. Populate the fields below only after the review occurs.

| Artifact/statement | Reviewer feedback | Evidence | Required change or retained question | Reviewer | Date |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Before treating this as an answer key, incorporate the actual review, keep the
source and retrieval history, and identify which decisions were approved and
which remain draft. Software validation cannot supply this scientific review.
