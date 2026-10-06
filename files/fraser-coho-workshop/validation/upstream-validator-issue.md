# Draft issue: permit schema-derived semantic annotations in descriptor fields

Prepared for Brett to review and post at <https://github.com/salmon-data-mobilization/smn-data-pkg/issues/new>. **This draft has not been posted.**

## Problem

The workshop reference passes metasalmon's strict package check and EML schema validation, but the separate `smn-data-pkg` publication validator rejects its semantically annotated measurement field. These are different checks; the workshop does not claim the independent validator passed.

This reproduces **item #90 in metasalmon's local backlog**, not necessarily GitHub issue 90: [backlog entry](https://github.com/salmon-data-mobilization/metasalmon/blob/main/knowledge/backlog.md). The entry records Brett's 24 August 2026 decision to permit these annotations, deriving the permitted keys from the canonical column-dictionary schema. The writers should continue projecting the annotations.

## Reproduction and exact versions

Observed 8 September 2026:

- `smn-data-pkg` local checkout: `1ec6cf54f9962faf13093f974592780665e9c427`.
- Its tracked `origin/main`: `47f0e81ac58a988be82a84df41d0cffec38a8999`, two commits ahead of that local checkout.
- `scripts/validate_package.py` has the identical Git blob at both revisions: `b4880b2687a42f3f309b1f07422acaf0bea17d3f`.
- The reference was generated with R `metasalmon` v0.5.0 from the unchanged 173-row, 14-column Fraser Coho 2023–2024 teaching source. Dataset ID: `fraser-coho-workshop`; table ID: `escapement`.

With the kit extracted and the spec validator's dependencies installed, run from the `smn-data-pkg` repository:

```sh
python scripts/validate_package.py /path/to/fraser-coho-workshop/checkpoints/reference-sdp
```

The validator reports exactly this error:

```text
datapackage.json resource data/escapement.csv schema.fields must match metadata/column_dictionary.csv-derived fields.
```

## Actual and expected behavior

All 14 generated base-field projections agree with `descriptor_field_from_column()`. Only the `NATURAL_ADULT_SPAWNERS` field differs: the writer also projects five populated semantic keys from that same dictionary row:

```json
{
  "unit_iri": "http://qudt.org/vocab/unit/INDIV",
  "term_iri": "https://w3id.org/gcdfo/salmon#SpawnerAbundance",
  "term_type": "owl_class",
  "property_iri": "https://w3id.org/smn/Abundance",
  "entity_iri": "https://w3id.org/smn/Population"
}
```

There are no missing keys or unequal common values. An in-memory diagnostic comparison that ignores only those five extra keys gives exact equality. No package file was modified to obtain that result. The illustrated IRIs are agent-selected technical draft annotations pending domain review; this issue concerns their faithful descriptor projection, not scientific approval of the selections.

Expected: permit schema-defined semantic annotations that agree with `metadata/column_dictionary.csv`, while still rejecting unknown properties and annotation values that disagree with the canonical dictionary.

## Proposed change and validation

Derive the permitted semantic projection keys from the column-dictionary schema, update `descriptor_field_from_column()`, and document the permitted descriptor extensions. Keep the canonical CSV header contract unchanged.

Add cases covering a populated measurement annotation set, optional blank annotations, an unknown descriptor property, and a descriptor annotation that differs from its dictionary value. Confirm that the current minimal examples still pass and the unchanged workshop reference passes this independent validator after the fix.

Do not strip accurate descriptor annotations from the workshop package to conceal this disagreement. Until the upstream fix lands, retain the failing result alongside the separate package and EML validation results. The workaround note retires when the unchanged annotated reference passes the corrected independent validator.
