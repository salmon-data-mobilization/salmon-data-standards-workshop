# Filled illustration: clarify the NuSEDS Resistivity Counter label

Status: teaching draft, unsubmitted; no human approval claimed
Prepared: 2026-09-08 by the workshop authoring assistant
Actual peer reviewer and maintainer decision: pending

## Problem and requested outcome

Request kind: source clarification and mapping review, not a claim that a new shared term is missing.

Proposed title: **Clarify the procedure represented by NuSEDS ESTIMATE_METHOD “Resistivity Counter”**

In the workshop's unchanged Fraser Coho 2023–2024 slice, four records carry this label. One is the Bonaparte River record with `POP_ID = 46200`, `ANALYSIS_YR = 2023`, `WATERBODY = BONAPARTE RIVER`, and reported estimate `758`. These locate a record in this supplied file; population-year alone is not asserted as a universal key.

The source dictionary lists “Resistivity Counter - N/A”. It does not supply the operational procedure needed to justify a more detailed method mapping. Please identify the applicable source definition or procedure documentation and clarify which aspects are common to these records versus determined locally.

## Evidence inspected and limits

| Evidence | Location/version | What it supports or leaves open |
| --- | --- | --- |
| Source CSV | `raw_data/nuseds-fraser-coho-2023-2024.csv`; provenance in `raw_data/source-manifest.json` | Four stored occurrences and their record context; no inferred procedure details. |
| Official NuSEDS dictionary snapshot | `raw_data/official-nuseds-dictionary.csv`, ESTIMATE_METHOD entry; retrieval metadata in `raw_data/official-dictionary-source.json` | The label is listed with `N/A`; this snapshot may postdate the 2025 source workbook. |
| DFO candidate | `https://w3id.org/gcdfo/salmon#FixedSiteCensusElectronic`; source commit `26d7c388a2c97b4098cf267eddca44857f81b36b`, `ontology/dfo-salmon.ttl` | Definition covers automated counting at a constrained opening using several technologies and describes QA/coverage context. A legacy note includes Resistivity Counter. |
| Shared method anchor | `https://w3id.org/smn/EnumerationMethod`; DFO source uses it above local narrower methods | A broader field-enumeration concept to inspect; it does not settle the detailed NuSEDS label meaning. |

Search boundary: targeted inspection of these source files and candidates only. This is not an exhaustive vocabulary search and does not establish the absence of another fitting term.

## Proposed disposition

- Keep the exact stored code and its current uncertainty visible.
- Ask the NuSEDS source steward for the definition/procedure evidence first; the specific contact remains to be identified by the facilitator.
- Treat `FixedSiteCensusElectronic` as a candidate to compare. Do not assert `skos:exactMatch` solely from the legacy-label note. A broader relationship may be suitable after evidence review; no predicate is approved here.
- Keep any interim project concept in a clearly labelled local draft. New shared-term admission is not requested by this illustration.
- If the question instead concerns the existing DFO term's scope, prepare a definition/boundary issue using DFO CONTRIBUTING. Do not imply that authoring this example contacted a steward.

## Draft request body

We are documenting the method context of the four NuSEDS Fraser Coho 2023–2024 records labelled `Resistivity Counter`. The included official dictionary lists the label with `N/A`. Which definition or procedure document should we cite, and does it describe the enumeration procedure, the device, an estimate derivation method, or a combination? Are the constrained-opening, QA, and coverage details in `gcdfo:FixedSiteCensusElectronic` established for these source records, or should they remain separate questions? We will retain the original code and defer a strong mapping until this is resolved.

## Handoff and completion evidence

Next action: a human contributor reviews the question, identifies the source steward, and chooses an authorized submission/contact route if appropriate. The workshop itself stops at the saved draft.

Peer feedback: pending. Steward response: pending. Mapping decision: pending. Issue URL, released term, and release version: none. A useful answer might simply provide existing documentation; it need not create any new term.
