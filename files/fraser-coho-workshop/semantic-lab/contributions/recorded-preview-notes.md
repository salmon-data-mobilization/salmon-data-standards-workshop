# Recorded request-preview evidence

Observed 2026-09-08 using installed metasalmon 0.5.0 and exact metasalmonpy v0.4.0 tagged source (`3b587e6be20d5feaf12c3640d48e449681271d23`). The input is the supplied `checkpoints/seeded-sdp/semantic_suggestions.csv`; its checksum and compared columns are in `preview-receipt.json`.

Both implementations executed `detect_semantic_term_gaps(suggestions=...)` and `render_ontology_term_request(..., scope="auto", ask=FALSE/False, profile_name="fraser-coho-workshop-draft")`. Both returned two rows, one for the `property` role and one for the `variable` role of `NATURAL_ADULT_SPAWNERS`. The selected columns in `recorded-gap-preview.csv` agree after sorting by role. Original row order differs between implementations; no general byte-parity claim is made.

Both automatic titles request a new shared SMN term named after the column. These are provisional renderer outputs, not evidence that a new term is warranted. Inspect existing `smn:Abundance`, the source definition and variable scope, and your human review before drafting the actual question. A targeted retrieval result does not prove absence from the vocabulary, and a saved shortlist may omit later human rejections or targets with no candidates.

The API recording does not claim that a learner or domain expert completed the preparation gate. The runnable learner scripts require the actual Chapter 2–3 preparation and refuse the blank supplied review form. Their resulting preview text is written only into a new local output folder.

No source data were changed, no new term was declared missing by a human review, no AI request was made, and no issue was posted. The filled source-clarification example is a separately authored teaching draft rather than one of these generated requests.
