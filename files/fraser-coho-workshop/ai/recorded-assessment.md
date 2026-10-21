# Recorded AI assessment: adult-spawner meaning in the Fraser Coho slice

Recording kind: actual Codex workshop-authoring assistant assessment.
Original recording started at: 2026-09-08 17:04:31 UTC.
Assessment revision: 2, reassessed at 2026-09-08 17:22:03 UTC.
Author: the Codex assistant preparing these workshop materials in this task.
Provider/model metadata: no verified underlying model identifier is recorded.
Native metasalmon/metasalmonpy request: not performed for this recording.
Human scientific approval: pending; none is claimed.

This document is my assessment of the source and draft working artifacts listed
below. It was written in the workshop-authoring conversation. It is **not** a
response from OpenRouter, a native metasalmon assessment table, or evidence of a
successful live API rehearsal. It contains AI-authored recommendations for
learners to evaluate after completing their own human baseline.

## Revision 2 scope

I reread the revised learner and working dictionaries, the starter unit evidence
and all 22 entries in `reference/code-definitions-working.csv`. The dictionaries
now make units and code meanings explicit. The adult-spawner unit is supported
by the starter's `Individual` unit label, while its estimate interpretation
across methods and classifications still needs confirmation. The other fields
are not measurement fields; their year/date formats and identifier structure
remain documented separately from measurement units.

The code list improves the account of supported meanings without filling gaps
with guesses. In particular, numeric run code `1` must not silently become
`FALL`; `Fence` lacks a separate estimate-method definition in the retrieved
source; and the Type-1/3/4/5 labels still need their operational criteria. I retain
the original 13 recommended dispositions after this reassessment. The learner's
six focus definitions and every human comparison decision remain blank.

This is a new authoring-assistant assessment revision, not a new provider API
response. The evidence hashes below identify revision 2. The previous working
dictionary hash was
`d71e670b818a71db6ec51b5ce9ca89dd1ec1923fd6f744a77b54222f5142a614`;
it described the version without the new units and code-meanings columns and
must not be used to identify the current dictionary.

## Assessment

The draft decomposition makes a useful distinction between the reported
adult-spawner variable and abundance as its reusable property. The population
or group, mature-adult scope, reported value, unit, method and row context still
need to remain visible. A single abundance label cannot replace that explanation.

The strongest source reconciliation is the adult definition. The current DFO
dictionary describes mature fish excluding jacks. The starter dictionary adds
natural-origin wording that the official definition does not establish. I would
retain the supported mature-adult/jack distinction, preserve the conflicting
starter statement as evidence and keep the meaning of natural open. I would
reject an automatic NaturalOrigin constraint. This does not prove the opposite
origin interpretation; it records that the proposed restriction lacks support.

I would keep the measurement or estimation activity distinct from its result.
The first record's 758 is a reported numerical value. The activity uses a
procedure and can yield that result; the complete variable states what the
result concerns. The draft graph correctly leaves the exact activity/record
grain subject to review. It must not imply that every row is one field visit.

The official ANALYSIS_YR definition supplies the year the estimate is for;
inspections may continue into the next calendar year. I would reject a brood-year
mapping without additional evidence. The row's year and waterbody are varying
coordinates/context, not fixed qualifiers attached to the entire column.

The method field should stay linked to how the estimate was produced. Its nine
source labels need individual meanings; some official entries provide little
or no definition. Different methods or classifications cannot be declared
comparable simply because a package stores them under the same column.

I would preserve all 13 missing estimates and all reported decimals. A blank
is not a zero, and an estimated number of individuals need not be an observed
integer count. I would also retain all 173 records. The 164 distinct
population–analysis-year pairs show that the proposed two-field key is not
unique; repeated pairs do not authorize deletion, summation or an inference of
population-to-CU membership.

The draft working dictionary's AREA correction is warranted by the current
official source: this is a NuSEDS subdistrict, which may differ from a statistical
area in the Fraser. Source FINAL status belongs to the estimate's stage, not to
this new dictionary, conceptual graph or publication decision.

The current official dictionary was retrieved on 2026-09-08 and may postdate
the 2025 workbook used for the slice. Its wording is useful evidence, but review
should preserve that timing and seek historical/source-specific clarification
where it affects the intended interpretation. Bruno and Tom have not yet
approved this teaching model in the supplied records.

## Candidate propositions for learners

[recorded-suggestions.csv](recorded-suggestions.csv) contains 13 identifiable
propositions and my recommended dispositions. Some are **explicitly rejected
alternatives**, included so learners can identify the tempting inference and
explain why it fails. They are not endorsed mappings, hidden ground truth or
examples of successful automated acceptance.

Use [comparison-worksheet.csv](comparison-worksheet.csv) to accept, revise or
reject each proposition against your own human baseline. Record a reason and
the evidence checked. My accept recommendation means the plain-language
statement is a defensible working interpretation; it does not grant permission
to apply an ontology IRI or publish the dataset.

## Evidence used and recording identity

Paths are relative to the extracted workshop-kit root. SHA-256 hashes identify
the exact bytes read for this assessment revision; they do not certify scientific truth.
If an artifact changes, keep this recording with its original evidence or make
a new labelled recording rather than silently presenting it as a fresh response.

| Evidence path | SHA-256 at assessment revision 2 |
| --- | --- |
| `raw_data/nuseds-fraser-coho-2023-2024.csv` | `ae7cd8f9f4facee1b1c8a75b2f9ead046e3eca0d3545cec7ef223c0f816d47b1` |
| `raw_data/source-column-dictionary.csv` | `ea4f5bbd703374f16d52be2706946b400a2a753e1a94ac8b9a5753134f198c78` |
| `raw_data/official-nuseds-dictionary.csv` | `195a164956d6c748f70856111d48ba9ca6c7d6ae2080736411b89c975bda08f0` |
| `raw_data/official-dictionary-source.json` | `393da6de4caacb101764796f42186f8fcf6a77f44be60b0ca0aa18705b1f39d7` |
| `raw_data/open-canada-record.json` | `0a39d29113b2caccb103f1851dce4bd176ecf11a9b91403e88deb1a121b1ed61` |
| `reference/dataset-nodes-working.csv` | `edacef3e2b46b2baabc76d550c58ba51948968545770d8e91fb6bdd5cb934d5d` |
| `reference/dataset-edges-working.csv` | `2c5f12a039c0c5c520d0f59a7d8e9913e775d7b8a17b7aa26f407f26af7653ae` |
| `reference/data-dictionary-working.csv` | `f93f0f5898fd4209de10a6313797d7cb888b5943da34bc71e5268d5bd800aac9` |
| `reference/variable-decomposition-working.csv` | `c937acb04916b398b790bc33c12d5859d1e53a7b0663601eac2ecb02f081b3e3` |
| `reference/metamodel-source-notes.md` | `2542196eadedf1abf65a06729339aca2b47c0f9a01a52ae9440e3b4a0ea1fc6f` |
| `worksheets/data-dictionary.csv` | `fea0d45cf6a7e04db86b12e1386bc6444f90877f0993cc11a318d3d216c525fa` |
| `reference/code-definitions-working.csv` | `3dbb824fedbf73e100dd81858a358d7570a2ba45991a1c77821b92eef08479c0` |

Ontology guidance used: the locally inspected Salmon Domain Ontology at commit
`d45f8f7`, especially `ontology/modules/02-observation-measurement.ttl`,
`ontology/views/` and `CONVENTIONS.md` section 12. An offline summary of that source guidance is
in `reference/metamodel-source-notes.md`. The metamodel views are
non-normative orientation material; no ontology query or mapping approval was
performed for this recording.

No provider-generated confidence scores, token usage, API request IDs or native
assessment metadata are claimed. The separate live-provider rehearsal receipt
records its own outcome; this authoring assessment does not convert a failed
rehearsal into a successful provider call.
