---
title: Instructor Notes
---

## The teaching contract

Use the same **173-row, 14-column NuSEDS Fraser Coho 2023–2024 dataset** for the hands-on chapters. Chapter 1 frames the reuse problem with separate Yukon and Fraser excerpts and a conceptual Central Coast illustration. The source is `nuseds-fraser-coho-2023-2024.csv`, the dataset ID is `fraser-coho-workshop`, and the table ID is `escapement`. The measurement is `NATURAL_ADULT_SPAWNERS`. Begin with human interpretation; introduce packaging software only after the graph, dictionary, and peer review.

After the Chapter 1 comparison, show the three outcomes: reusable data publication, shared-term contributions, and local semantic stewardship through vocabularies, ontologies, and bridges. Then return to the raw data. Participants should understand why definitions, context, and relationships matter before they encounter identifiers or automated suggestions. The kit supplies the dataset for everyone.

The supplied reference package is a **technical draft pending Bruno and Tom's domain review**. Label it that way in handouts and demonstrations. Structural validation and a successful test upload are useful technical evidence; neither is an expert ruling about biological meanings.

## Delivery formats

Every format uses the same chapters and the same Fraser Coho dataset.

| Format | What it covers |
| --- | --- |
| 1-hour primer | The whole journey without detail: Chapter 1 on its own, run as the [standalone 55-minute overview](#standalone-55-minute-overview). |
| 1-day workshop | Day 1, Chapters 1–7. |
| 2-day workshop | Day 1 and Day 2, Chapters 1–12. |
| Webinar series | Three or four weekly sessions of about two hours each. That is six to eight hours against the two-day workshop's twelve, so a series covers part of the curriculum: three sessions fit Day 1, Chapters 1–7. Which Day 2 chapters a fourth session takes is for the lesson maintainer to choose. Record every session so a learner who misses a week can catch up before the next one. |

Learners who bring their own data work with it in a separate solo hour after the group walkthrough, never during a group exercise. The chapter timings below do not include that hour.

## Day 1 — six-hour beginner route to publication

| Elapsed time | Chapter | Minutes | Learner result |
| --- | --- | ---: | --- |
| 0:00–0:55 | 1. Comparison and workshop overview | 55 | Explain candidate field matches, context needed for reuse, and the connected data/term outcomes. |
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

Chapter 1 retains 30 teaching minutes and 25 exercise minutes. The comparison replaces the generic opening reuse scenario and detailed catalog tour. The three outcomes are a short list after the practical example; both existing overview illustrations remain linked for optional reading. The former values-versus-descriptions section and dense journey recap are removed.

| Elapsed time | Minutes | Focus |
| --- | ---: | --- |
| 0:00–0:05 | 5 teaching | State the CU–year question and show the Yukon and Fraser excerpts. |
| 0:05–0:15 | 10 exercise | Pairs choose candidate fields and identify evidence they need. |
| 0:15–0:25 | 10 teaching | Follow source definitions, compare the prepared descriptions and the two workflow routes, then introduce the Central Coast scale problem. |
| 0:25–0:35 | 10 teaching | Switch explicitly to the Fraser Coho teaching slice; inspect its first records, blank and interpretation questions. |
| 0:35–0:40 | 5 teaching | Connect the workflow to the three outcomes and the two days. |
| 0:40–0:55 | 15 exercise | Pairs record what the next user would need, then share and recap. |

This is an awareness session, not completion of either day's hands-on outcomes. It uses a prepared description example; no live integration, package creation or AI call is needed.

## Facilitate Chapter 1

Begin with the question about assembling the best available estimates by CU and year, with differences documented, before introducing the delivery schedule or the ontology vocabulary. Explain that the two excerpts concern different CUs: this is a candidate-field comparison, not a row join or a claim that the populations are interchangeable. The selected records are illustrative choices for this draft, pending Bruno and Tom's review.

The Rapid Status repository has a dictionary and CU narratives. Use the published lookup to show how interpretation works. Keep an author's correspondence out of the story until the person who performed that exchange supplies and checks the account. Do not convert the meeting's anecdotal wrangling-time estimate into a measured benefit.

The prepared comparison table is a teaching description, not an approved mapping or a canonical SDP dictionary. Explain the source of the descriptions and what remains to be confirmed. A shared abundance property does not resolve total versus wild scope, a relative index versus absolute abundance, year basis, CU identity, method or uncertainty. In particular, `ConfidenceRating` describes assessment status confidence, not an interval around an abundance estimate. The script demonstrates no universal metasalmon integration API.

The Central Coast section introduces a real estimation pathway but does not supply a newly reviewed extract, crosswalk or expansion calculation. Link to the source report, then say explicitly that the practical exercises use a Fraser Coho slice. Keep those regional sources and their provenance distinct. If the group later selects a Central Coast extract, review its source and relationship evidence before adding actual rows.

The intro source excerpts are outside the teaching kit in `episodes/files/intro-comparison/`. Their manifest records revisions, row selection and checksums; all source columns are retained. `scripts/prepare-intro-comparison.py` renders the diagram and checks the local excerpts offline. Its explicit `--refresh-sources` option retrieves only the pinned sources. Retain those source versions and original field names when discussing a different mapping.

Use the three-record NuSEDS excerpt to make the next activity tangible. Keep the blank visible and have participants distinguish the population identifier, place, year and estimate. Learners draw their own graph, write and decompose the dictionary, and complete peer review in Chapters 2–3, before package creation in Chapter 4 and AI comparison in Chapter 5.

The [worked publication example](reference.html#teaching-record) remains available for the later workflow preview. Check its actual status before teaching. If the public test record is unavailable, show the supplied local preview and describe it as a preview. Use the short outcome list, optional outcome figure and `semantic-lab/` files to connect data publication to local stewardship, bridges and shared-term contributions, linking back to [setup](index.html#download-and-open-the-workshop-kit) as needed.

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

In Chapter 2, ask what each arrow claims. Keep the observation activity separate from its result, the property from the entity, and the method from the variable meaning. A sketch can contain useful open questions. It need not become a formal ontology during the exercise. Offer the drawing skeleton to anyone stuck on a blank page, and keep the answer key closed until each pair has drawn and explained its own variable.

In Chapter 3, ask another pair to explain a field using only the draft definition and cited context. Record where their interpretation differs. Check proposed row grain and keys against the source records, and preserve missing estimates as missing. Do not silently resolve uncertainty because the reference worksheet supplies a plausible answer.

## Facilitate the AI comparison

Comparing human reasoning with the supplied recorded AI outputs is a required activity for every lane. Have learners identify one agreement, one disputed or unsupported claim, the evidence that would resolve it, and a decision or open question. Their own dictionary must be available before they see the AI response.

Live requests are optional. OpenRouter practice uses an explicitly free model and no paid fallback; no credit purchase is required or requested. Free endpoints may be unavailable or rate-limited, so the recorded comparison is always available. Ollama is an optional local route for participants who have prepared it. Do not spend the group session troubleshooting an individual installation.

A fluent response, retrieval rank, or numerical score is not approval. Keep source excerpts, human interpretations, retrieval candidates, and AI proposals visibly distinguishable.

## Checks at each handoff

| After chapter | Check before continuing |
| --- | --- |
| 1 | Participants can name candidate comparison fields, an unresolved compatibility question, and the separate NuSEDS hands-on dataset. |
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
