# Source and interpretation provenance

Original publisher: Fisheries and Oceans Canada (DFO).
Original publication: [NuSEDS—New Salmon Escapement Database System](https://open.canada.ca/data/en/dataset/c48669a3-045b-400d-b730-48aafe8c5ee6).
Licence: [Open Government Licence – Canada](https://open.canada.ca/en/open-government-licence-canada).

Contains information licensed under the Open Government Licence – Canada.
This teaching derivative does not imply DFO endorsement. The source licence
permits copying, modification and redistribution with attribution; source
licensing is distinct from approval of these workshop interpretations.

## Exact selected table

`nuseds-fraser-coho-2023-2024.csv` is copied unchanged from metasalmon v0.5.0,
commit `af84689df5d6365c1abaa49f8cd9012cbe8494c5`. It derives from the
**Fraser and BC Interior NuSEDS_20251014** workbook, selecting Coho in analysis
years 2023 and 2024, retaining 14 fields and formatting survey dates as ISO
dates. The original derivation and notes are preserved in
`upstream-derivation.R` and `upstream-example-data-README.md`.

Do not rerun that upstream script during the workshop: it downloads other
source inputs and produces examples beyond this fixed selection. The workshop
uses the included CSV throughout. `source-manifest.json` pins its bytes and the
supporting metasalmon files with SHA-256 hashes and source URLs.

Measured from the selected table:

- 173 rows, 14 columns and 164 distinct `POP_ID`–`ANALYSIS_YR` pairs.
- Every full row is distinct; repeated population–year pairs must be retained.
- 13 missing `NATURAL_ADULT_SPAWNERS` values; blank is not zero.
- Decimal estimates, source code spelling and dates are preserved.
- CU assignments are absent from these 14 fields.

The worksheet introduces only six columns first; this is a view of the same
table, not a smaller substituted dataset. A package checkpoint's source table
must match the pinned CSV byte for byte.

## Three distinct description layers

| File | What it records |
| --- | --- |
| `source-column-dictionary.csv` | Original metasalmon starter descriptions, preserved without correction. Some interpretations require correction or qualification. |
| `official-nuseds-dictionary.csv` | Original bytes of the current DFO dictionary retrieved on 2026-09-08. It uses a legacy text encoding; import as Windows-1252 if your editor shows broken characters. |
| `../reference/data-dictionary-working.csv` | Draft human interpretation, with original wording, evidence, corrections and unresolved questions kept separate. |

`open-canada-record.json` records selected public catalog metadata and resource
links observed on 2026-09-08. `official-dictionary-source.json` records the
official dictionary URL, retrieval time and hash. That current dictionary may
postdate the 2025 workbook; preserve this limitation in historical interpretation.

The current official wording identifies AREA as a NuSEDS subdistrict,
ANALYSIS_YR as the year the estimate is for, and the adult-spawner field as
mature salmon excluding jacks. It does not establish natural-origin-only fish.
These findings guide the working draft; Bruno and Tom's review is still needed
for the source-specific questions in the scientific review packet.

The ontology's metamodel view is an organizing aid, not a normative definition
source. Use its linked core definitions to interpret entity, property,
variable, measurement activity and result; leave unsupported OWL relations out.
