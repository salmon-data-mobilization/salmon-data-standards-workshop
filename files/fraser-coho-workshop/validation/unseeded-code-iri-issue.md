# Draft issue: keep code mappings visibly unreviewed during unseeded creation

Prepared for Brett to review and post at <https://github.com/salmon-data-mobilization/metasalmon/issues/new>. The mirrored Python result can be reported at <https://github.com/salmon-data-mobilization/metasalmonpy/issues/new>. **Neither draft has been posted.**

## Observed behavior

On 8 September 2026, R `metasalmon` v0.5.0 and exact tagged Python `metasalmonpy` v0.4.0 both wrote 11 populated `metadata/codes.csv$term_iri` values when creating the same 173-row Fraser Coho example with semantic seeding and LLM assessment explicitly disabled. This was reproduced in isolated temporary test packages with no live vocabulary or AI requests.

Seven affected rows belong to `ESTIMATE_METHOD`; four belong to `ESTIMATE_CLASSIFICATION`. Examples include:

| Source code | Automatically written IRI |
| --- | --- |
| `Resistivity Counter` | `https://w3id.org/gcdfo/salmon#FixedStationTally` |
| `Combined Methods` | `https://w3id.org/gcdfo/salmon#EstimateMethod` |
| `TRUE ABUNDANCE (TYPE-1)` | `https://w3id.org/gcdfo/salmon#Type1` |

The IRIs lack a `REVIEW:` prefix. Their presence does not record a human decision or establish that each mapping fits the source's current definition. This is related to the auto-application concerns recorded in the metasalmon backlog; do not assume a backlog number is a GitHub issue number.

## Reproduce

Read `raw_data/nuseds-fraser-coho-2023-2024.csv` as character values. Create a new, otherwise absent output directory through either pinned package:

```r
metasalmon::create_sdp(
  list(escapement = raw), path = "output/unseeded-probe-sdp",
  dataset_id = "fraser-coho-workshop", table_id = "escapement",
  seed_semantics = FALSE, llm_assess = FALSE,
  check_updates = FALSE, overwrite = FALSE
)
```

```python
metasalmonpy.create_sdp(
    {"escapement": raw}, path="output/unseeded-probe-sdp",
    dataset_id="fraser-coho-workshop", table_id="escapement",
    seed_semantics=False, llm_assess=False,
    check_updates=False, overwrite=False,
)
```

Inspect non-empty `term_iri` values in `metadata/codes.csv`. The sanitized `lane-smoke.json` receipt records all 11 observed rows for both implementations.

## Expected behavior and follow-up

Define an explicit contract for bundled code mappings during unseeded creation: leave semantic targets empty or retain them as clearly unreviewed candidate evidence, unless the caller deliberately supplies reviewed mappings with their provenance. Implement the same behavior in both languages and test that seeding/LLM opt-outs cannot silently produce accepted-looking defaults.

The workshop helper currently clears inherited code IRIs and writes honest descriptions before presenting the draft. Its isolated R and Python smoke tests confirm that the workshop draft preserves all source rows and values, contains only code rows for categorical fields, and has no populated code IRIs. This workaround retires when a released, pinned pair preserves the human-review boundary without the workshop clearing those defaults.
