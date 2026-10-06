---
title: Instructor Notes
---

## The teaching contract

Use the same **173-row, 14-column NuSEDS Fraser Coho 2023–2024 dataset** for the whole workshop. The source is `nuseds-fraser-coho-2023-2024.csv`, the dataset ID is `fraser-coho-workshop`, and the table ID is `escapement`. The measurement is `NATURAL_ADULT_SPAWNERS`. Begin with human interpretation; introduce packaging software only after the graph, dictionary, and peer review.

Show the three outcomes in Chapter 1: reusable data publication, shared-term contributions, and local semantic stewardship through vocabularies, ontologies, and bridges. Then return to the raw data. Participants should understand why definitions, context, and relationships matter before they encounter identifiers or automated suggestions. The kit supplies the dataset for everyone.

The supplied reference package is a **technical draft pending Bruno and Tom's domain review**. Label it that way in handouts and demonstrations. Structural validation and a successful test upload are useful technical evidence; neither is an expert ruling about biological meanings.

## Day 1 — six-hour beginner route to publication

| Elapsed time | Chapter | Minutes | Learner result |
| --- | --- | ---: | --- |
| 0:00–0:55 | 1. Overview and endpoint tour | 55 | Explain how source data, metadata, and the test record connect. |
| 0:55–1:50 | 2. Human concept graph | 55 | Draw entities, properties, observations, results, units, and methods with named relationships. |
| 1:50–2:55 | 3. Human dictionary and peer review | 65 | Define fields, decompose the measurement, and record review questions. |
| 2:55–3:35 | 4. Build the SDP | 40 | Create or inspect the same-data draft and locate the metadata files. |
| 3:35–4:45 | 5. Mapping and AI comparison | 70 | Compare human and recorded AI proposals and record supported decisions. |
| 4:45–5:15 | 6. Codes and term gaps | 30 | Describe a code meaning and draft an unresolved-term question. |
| 5:15–6:00 | 7. Validation and test publication | 45 | Interpret validation, EML, a manifest, and the teaching-record outcome. |
| | **Total** | **360** | |

Add breaks and lunch outside these six hours. Preserve the human graph, dictionary, and required AI comparison if discussion runs long; shorten optional live tool demonstrations first. Do not use installation or account creation time as a substitute for the review exercises.

The [extended practice labs](extended-practice.html) are optional follow-up work outside the two-day, 720-minute schedule. They investigate repeated population–year records, missingness and method context, code sources, a reviewed metadata edit across R and Python, and validation/EML/manifest evidence using the same included dataset. Require the actual Chapter 2–3 human work and peer review before any lab; do not use supplied reference answers to bypass that checkpoint. Pair across tools where useful and assess the stated output and self-check for each lab.

## Day 2 — six hours of vocabulary, ontology and contribution work

| Elapsed time | Chapter | Minutes | Learner result |
| --- | --- | ---: | --- |
| 0:00–1:00 | 8. Choose reuse, local or shared | 60 | Separate evidence, representation and stewardship decisions. |
| 1:00–2:15 | 9. Build a controlled vocabulary | 75 | Draft a small SKOS scheme and its stewardship record. |
| 2:15–3:45 | 10. Formalize the graph | 90 | Read and edit a small OWL model and test selected consequences. |
| 3:45–5:00 | 11. Build bridges | 75 | Assess and express mappings with direction, evidence and limits. |
| 5:00–6:00 | 12. Prepare contributions | 60 | Produce a request or source-clarification draft and a review plan. |
| | **Total** | **360** | |

Both days total 12 hours excluding breaks. Day 1 can be delivered independently. For participants joining only Day 2, arrange the same-source human preparation and peer review before the six-hour session; do not consume the authoring time with an unplanned catch-up. No live publication is a prerequisite for Day 2.

Use `semantic-lab/` for the worked examples, worksheets, Turtle and local checks. Keep one facilitator who can run the pinned Python RDF tools, while all participants make the same conceptual and review decisions. Inspecting a supplied result is a valid lane, but record it as inspection. The lesson checks are scoped technical evidence, not complete OWL DL verification or independent scientific approval.

The practical progression is a source value → documented local meaning → representation choice → explicit mapping → contribution decision. Have groups show their files and explain one rejected or deferred claim. A larger artifact is not automatically better. In particular, no new shared term should be invented just to give every group a term request.

## Standalone 55-minute overview

Use Chapter 1 without package creation or AI calls. Allocate 10 minutes to the three outcomes and raw/finished comparison, 10 to the six source columns and their interpretation problems, 15 to the human-preparation and Day 1 workflow, 10 to a preview of Day 2's vocabulary/model/bridge/request files, and 10 to the chapter's pair discussion and recap. This is an awareness session, not completion of either day's hands-on outcomes.

## Facilitate Chapter 1

Begin with a reuse problem familiar to biologists: comparing spawner estimates across rivers or years when another team's definitions and methods are unclear. Invite participants to identify the context they would need before combining the values.

Open the [worked publication example](reference.html#teaching-record) beside the source CSV. Check the reference page for the actual catalog status before teaching. If the public test record is still unavailable, show the supplied local publication preview and explain that it is a preview. A draft, test upload, and production deposit have different outcomes; describe the one actually being shown.

Keep this chapter as a tour and discussion. Learners first draw their own diagram, write the dictionary and decomposition, and complete peer review in Chapters 2–3. Package creation begins in Chapter 4; AI comparison follows in Chapter 5.

Briefly preview the Day 2 files in `semantic-lab/` inside the extracted workshop ZIP, linking back to the [setup instructions](index.html#download-and-open-the-workshop-kit) for anyone who has not located it. Return to the source table after showing what the later vocabulary, model, bridge and contribution activities will produce.

Use the three-record excerpt to distinguish stored values from descriptions. Keep the blank estimate visible and invite participants to ask what they would need to compare the different methods. The full CSV and later exercises retain all 173 rows and 14 columns.

Walk through the first record using the worked flow. The abundance property illustrates reusing an existing term; the unresolved source-method definition illustrates why clarification may come before a new-term request. Show the two publication outcomes and the return path from a released term's IRI to a later metadata version. Day 1 reaches the catalog preview, while Day 2 prepares semantic drafts for later review and release.

## Prepare the kit and endpoint tour

1. Download and open the [workshop kit][workshop-kit]. Confirm that the source has 173 rows and 14 columns and that its README explains the source, extraction, and limitations.
2. Check the worksheets, blank human dictionary, context notes, recorded AI outputs, and `draft-sdp`, `seeded-sdp`, and `reference-sdp` checkpoints. Confirm that checkpoint data retain the same rows and values. Preserve the raw CSV byte-for-byte; do not require separate language writers to produce identical CSV formatting.
3. Run the relevant R/Python scripts in a fresh project and verify their documented outputs. R is pinned to metasalmon 0.5.0 and Python to metasalmonpy 0.4.0; use supplied candidate evidence for the documented Python review alternatives. Do not imply the missing R-native APIs exist in Python.
4. Open the [Glossary](glossary.html), [Field reference](field-reference.html), and [teaching-record section](reference.html#teaching-record) in the browser. Verify the public Test Node link and its recorded status before using it in the opening tour. If the record is unavailable, show the supplied local artifacts and state the actual status.
5. Prepare one example where a plausible label or AI explanation requires source evidence. Do not present a synthetic teaching response as though it were a captured provider output; the kit must identify what was recorded, when, and from which model or process.
6. Retain evidence for creator, contact, licence, provenance, and export decisions. Separate the source dataset's creators from the workshop compiler and the authorized test publisher.
7. Before Day 2, run the semantic lab checks on a fresh extracted kit. Read the source-pinned vocabulary, model and bridge notes; check that draft mappings remain draft and that missing source definitions remain visible. Review the contribution examples before showing request-generation code. There is no automatic issue submission or vocabulary release.

The test deposit is authorized under Brett's identity and scoped to the KNB Test Node. Learners do not need credentials and must not copy a token from a demonstration. No production deposit is included in this workshop. Update the teaching-record section only from an actual observed outcome and receipt.

## Facilitate the human work

For mixed groups, rotate four roles: source reader, graph or dictionary editor, skeptical reviewer, and recorder. Spreadsheet users can lead source interpretation and peer review; R and Python users should complete those activities before automating them.

In Chapter 2, ask what each arrow claims. Keep the observation activity separate from its result, the property from the entity, and the method from the variable meaning. A sketch can contain useful open questions. It need not become a formal ontology during the exercise.

In Chapter 3, ask another pair to explain a field using only the draft definition and cited context. Record where their interpretation differs. Check proposed row grain and keys against the source records, and preserve missing estimates as missing. Do not silently resolve uncertainty because the reference worksheet supplies a plausible answer.

## Facilitate the AI comparison

Comparing human reasoning with the supplied recorded AI outputs is a required activity for every lane. Have learners identify one agreement, one disputed or unsupported claim, the evidence that would resolve it, and a decision or open question. Their own dictionary must be available before they see the AI response.

Live requests are optional. OpenRouter practice uses an explicitly free model and no paid fallback; no credit purchase is required or requested. Free endpoints may be unavailable or rate-limited, so the recorded comparison is always available. Ollama is an optional local route for participants who have prepared it. Do not spend the group session troubleshooting an individual installation.

A fluent response, retrieval rank, or numerical score is not approval. Keep source excerpts, human interpretations, retrieval candidates, and AI proposals visibly distinguishable.

## Checks at each handoff

| After chapter | Check before continuing |
| --- | --- |
| 1 | Participants can name the shared dataset and distinguish a test record from production publication. |
| 2 | The graph names relationships and leaves unsupported claims as questions. |
| 3 | The dictionary covers the fields, includes a measurement decomposition, and records peer-review feedback. |
| 4 | Dataset/table IDs and 173×14 source values remain unchanged in the package. |
| 5 | Each comparison records evidence and a human decision or question; AI output is not silently accepted. |
| 6 | A stored code has a source-backed description, and any gap is a draft request rather than an unapproved submission. |
| 7 | Participants distinguish review validation, strict validation, EML validity, domain review, and the actual test upload outcome. |
| 8 | Representation and ownership decisions have separate reasons; a missing search hit is not treated as proof of a missing term. |
| 9 | Source codes, concept IRIs, labels and definitions remain distinct; missing definitions and stewards are explicit. |
| 10 | Learners can explain an inferred statement and why a missing statement is not automatically false. |
| 11 | Mapping direction, term types, evidence and review status agree; a candidate link is not silently applied. |
| 12 | The draft has a source, scope, candidate search and a competent reviewer or open reviewer question. Nothing has been submitted automatically. |

## Common corrections

- A blank estimate is not zero; an analysis year is not automatically a survey date.
- A row is not automatically one field observation; document what this source record represents.
- A method describes how a value was obtained. A statistical modifier describes what a reported summary means.
- One first-ranked candidate may be the only candidate. Read its definition and scope.
- An empty review queue does not prove that all required metadata are filled.
- Rerunning a build may replace generated edits. Preserve the worksheet and record accepted decisions in the script or review log.
- A public Test Node object is a test publication, and the reference remains pending Bruno and Tom's review.

## Maintaining the lesson

Keep the kit, literal episode code, package pins, and field references aligned. When a released Python version closes a documented gap, verify the complete workshop path before removing the alternative. Run the checks in [Entrypoints](https://github.com/salmon-data-mobilization/salmon-data-standards-workshop/blob/main/docs/entrypoints.md) and inspect rendered pages after changing headings, tables, or links.
