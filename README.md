# Salmon Data Integration Workshop

This **two-day, 12-hour workshop** follows one NuSEDS Fraser Coho 2023–2024 dataset from human interpretation through data publication and semantic stewardship. Day 1 is a six-hour beginner route to a Salmon Data Package and a KNB Test Node publication exercise. Day 2 is six hours of controlled-vocabulary construction, ontology modelling, bridge review, and shared-term contribution. Everyone uses the included `nuseds-fraser-coho-2023-2024.csv`: **173 rows and 14 columns**. No personal dataset is needed.

Participants first draw how observations, results, populations, methods, and units relate. They write and peer-review a data dictionary before asking software to suggest mappings. They then compare human decisions with recorded AI outputs, document code meanings and gaps, and inspect validation, EML, and a test catalog record. The reference package is a technical draft pending Bruno and Tom's domain review; a passing software check does not supply that review.

Day 2 returns to the human model and produces actual draft SKOS, OWL, mapping, and request artifacts. Organization-owned meanings and shared concepts remain distinct; a teaching namespace does not establish authority or a public vocabulary release. The curriculum supports three related outcomes: reusable data publication, contributions to shared terminology, and local terminology connected through explicit bridges.

## Part 1 — beginner route to publication (Day 1)

| Chapter | Activity | Minutes |
| --- | --- | ---: |
| 1 | See the complete workflow and the shared data | 55 |
| 2 | Draw a human concept graph | 55 |
| 3 | Write a dictionary, decompose a measurement, and peer-review | 65 |
| 4 | Build the Salmon Data Package | 40 |
| 5 | Review mappings and compare human and AI reasoning | 70 |
| 6 | Describe codes and record term gaps | 30 |
| 7 | Validate, export EML, and inspect test publication | 45 |
| | **Teaching and activities; add breaks and lunch** | **360** |

## Part 2 — build and connect meanings (Day 2)

| Chapter | Activity | Minutes |
| --- | --- | ---: |
| 8 | Choose reuse, local representation, or a shared contribution | 60 |
| 9 | Build and steward a small SKOS controlled vocabulary | 75 |
| 10 | Formalize the human graph with RDF and OWL | 90 |
| 11 | Build and test bridges to shared ontology terms | 75 |
| 12 | Prepare term requests and plan review and release | 60 |
| | **Teaching and activities; add breaks and lunch** | **360** |

Both parts total **720 minutes**. Chapter 1 is also a standalone 55-minute overview. Day 2 requires the Day 1 graph, dictionary, and peer review, or an equivalent preparation session on this same dataset; possessing a downloaded checkpoint alone does not meet that prerequisite.

## Start here

- [Training interest](learners/training-interest.md): ask Brett for future workshop information by email.
- [Setup](learners/setup.md): download the workshop kit and choose spreadsheet, R, or Python tools.
- [Glossary](learners/glossary.md): plain-language terms linked from their first use in the lesson.
- [Field reference](learners/field-reference.md): package files, required fields, and links to the canonical SDP specification.
- [Reference and teaching record](learners/reference.md#teaching-record): checkpoints, software boundaries, and test catalog status.
- [Instructor notes](instructors/instructor-notes.md): timing, preparation, and review criteria.
- [Extended practice](learners/extended-practice.md): five optional labs using the same source, after the human graph and dictionary checkpoints.
- [Day 2 guide](learners/advanced.md): prerequisites, substantive authoring chapters, and draft artifact boundaries.

Extended practice is outside the 720-minute schedule. The labs investigate repeated population–year records, missingness and method context, code sources, a reviewed metadata edit across R and Python, and validation/EML/manifest evidence. They use the included data and local artifacts without requiring live AI or a deposit. The Day 2 authoring files are under `semantic-lab/` in the same kit and remain separate from the canonical SDP metadata.

The project is `fraser-coho-workshop/`. Keep the source at `raw_data/nuseds-fraser-coho-2023-2024.csv`, the build at `scripts/build_sdp.R` or `scripts/build_sdp.py`, and the working package at `output/fraser-coho-workshop-sdp`. Dataset ID `fraser-coho-workshop` and table ID `escapement` remain consistent throughout. The kit contains `draft-sdp`, `seeded-sdp`, and `reference-sdp` checkpoints from the same data.

## Tools and access

The lesson pins R `metasalmon` to **v0.5.0** and Python `metasalmonpy` to **v0.4.0**. The Python release does not yet provide the R-native review and metadata setters; its lane uses the documented alternatives and supplied evidence. Spreadsheet participants review the same files and decisions.

The human–AI comparison is required, using supplied recorded outputs. Live AI calls are optional. Participants need no AI account, API key, purchased credits, or catalog account to complete the workshop. Optional OpenRouter practice uses a free model with no paid fallback; optional Ollama practice can use a local model.

Catalog work uses a separately authorized **KNB Test Node** teaching record under Brett's identity. It does not authorize a production deposit or imply Bruno and Tom have reviewed the scientific meanings. See the [teaching-record status](learners/reference.md#teaching-record) before presenting a live result.

## Repository maintenance

Edit lesson sources under `episodes/` and `learners/`; do not edit generated `site/` output. Kit source files are under `episodes/files/fraser-coho-workshop/`, and the downloadable ZIP is `episodes/files/fraser-coho-workshop.zip`. [Entrypoints](docs/entrypoints.md) records the source map, build commands, and checks.

The [Salmon Data Package specification](https://github.com/salmon-data-mobilization/smn-data-pkg/blob/main/SPECIFICATION.md), [metasalmon](https://github.com/salmon-data-mobilization/metasalmon), and [metasalmonpy](https://github.com/salmon-data-mobilization/metasalmonpy) own the underlying formats and software contracts.
