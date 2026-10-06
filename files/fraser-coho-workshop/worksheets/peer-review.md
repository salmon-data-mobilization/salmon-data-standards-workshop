# Human review before packaging or AI

Completion: pending
Reviewer:
Review date:
Author/team:

Complete this record only after a person has reviewed the actual artifacts.
Change `Completion: pending` to `Completion: complete` when the review and
required revisions below have happened. Enter the actual reviewer and date;
write the review date as `YYYY-MM-DD` so the preparation check can read it.
Do not use a supplied working example or an AI response as a fictional review.

This is a workshop readiness review, not scientific approval or publication
authorization. An explicit unresolved scientific question can remain in a draft.

## Artifacts reviewed

- Editable diagram or paper capture filename:
- `worksheets/dataset-nodes.csv`
- `worksheets/dataset-edges.csv`
- `worksheets/data-dictionary.csv`
- `worksheets/variable-decomposition.csv`
- Unchanged source: `raw_data/nuseds-fraser-coho-2023-2024.csv`

## Checks performed

- [ ] The diagram has labelled directed edges, distinct node IDs and a text-based node/edge companion.
- [ ] Every edge endpoint exists in the node table; examples and broad concepts are distinguished.
- [ ] The source is 173 rows and 14 columns, with 164 distinct population–analysis-year pairs; population/year is not asserted to be a unique row key.
- [ ] Population, identifier, waterbody, species and Conservation Unit are distinct; no unsupported CU assignment is asserted.
- [ ] The six focus fields have human-written definitions: POP_ID, WATERBODY, ANALYSIS_YR, SPECIES, NATURAL_ADULT_SPAWNERS and ESTIMATE_METHOD.
- [ ] All eight remaining field descriptions have been read, so all 14 fields have been reviewed.
- [ ] Source wording remains separate from working definitions, and the official dictionary's retrieval date is recorded.
- [ ] AREA is described as NuSEDS subdistrict; ANALYSIS_YR is the year the estimate is for, not an inferred brood year.
- [ ] The adult-spawner decomposition separates entity, property, variable, activity, result, unit, method, qualifiers and dimensions.
- [ ] Mature adults excluding jacks is supported by the current official definition; an unsupported natural-origin restriction has not been added.
- [ ] Blank and decimal estimates are preserved; neither deletion of repeated pairs nor aggregation is implied.
- [ ] The graph and dictionary agree, or any remaining disagreement is explicitly recorded below.
- [ ] The first human draft and this review precede metasalmon and AI ingestion.

## Reviewer observations

Write what you checked and which source row(s) you traced through the diagram
and dictionary. A checkbox alone does not describe the review.

## Required revisions and what changed

Record the revision and the artifact affected. If none were required, say so.

## Questions carried forward

| Question | Affected fields/relationships | Evidence needed | Person or source to consult | Next step |
| --- | --- | --- | --- | --- |
| | | | | |

Do not turn an unanswered question into an accepted ontology mapping.

## Readiness decision

State whether the human baseline is ready for draft packaging and why.
Retain any limits on that decision. Fill the completion marker, reviewer and
date at the top only after the review is complete.
