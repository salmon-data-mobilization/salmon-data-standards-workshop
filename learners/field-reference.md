---
title: Field Reference
---

This is a workshop reading aid for **SDP 0.3.0**, not a second specification. The [canonical SDP field reference][sdp-field-reference] gives the full field inventory, and the [SDP specification][sdp-specification] defines validity. Preserve canonical CSV headers; put exercise notes and questions in the supplied worksheets or context files.

The source data have 173 rows and 14 columns. Metadata have a different structure: one dataset row, one `escapement` table row, one dictionary row for each source column, and code entries for categorical values.

## Dataset fields {#dataset-fields}

`metadata/dataset.csv` describes the collection as a whole.

| Field or group | How to use it in the workshop |
| --- | --- |
| `dataset_id` | Keep `fraser-coho-workshop`; it joins the metadata files. |
| `title`, `description` | Say this is the Fraser Coho 2023–2024 workshop derivative and explain its purpose and limits. |
| `creator` | Credit the documented source creators; distinguish the workshop compiler's role. |
| `contact_name`, `contact_email` | Use confirmed contact facts appropriate to this package. |
| `license` | Record the applicable source-backed licence; a public source is not itself a licence. |
| `temporal_start`, `temporal_end` | Describe the documented time coverage. |
| `source_citation`, `provenance_note` | Connect the extract, source documentation, and processing history. |

The identifier, title, description, creator, contact name, contact email, and licence are required dataset fields. Coverage and provenance fields are useful evidence even where the schema does not require them. Use the dataset's documented creators, contact and licence when completing these fields. [Canonical dataset fields][sdp-field-reference].

## Table fields {#table-fields}

`metadata/tables.csv` describes what a row represents and how to locate its data.

| Field | Workshop use |
| --- | --- |
| `dataset_id`, `table_id` | `fraser-coho-workshop`, `escapement`. |
| `file_name` | `data/escapement.csv`, relative to the package root. |
| `table_label`, `description` | A readable name and an evidence-backed statement of row meaning. |
| `observation_unit`, `observation_unit_iri` | Describe the thing each record concerns; review the IRI separately. |
| `primary_key` | Optional; declare only a demonstrated unique, nonmissing column combination. |
| `protocol_iri`, `protocol_citation` | Link a documented protocol that applies to the table. |
| `method_iri` | Use only when a single method applies to the whole table and the protocol route does not apply. |

The source `ESTIMATE_METHOD` varies by row. Describe those stored values in the code metadata rather than imposing one table-wide method. [Canonical table fields][sdp-field-reference].

## Column fields {#column-fields}

`metadata/column_dictionary.csv` contains one row for each of the 14 source columns. Keep `column_name` an exact, case-sensitive match to the source.

| Field or group | Meaning |
| --- | --- |
| `dataset_id`, `table_id`, `column_name` | Identify the exact field being described. |
| `column_label`, `column_description` | Human wording and a definition supported by evidence. |
| `column_role` | `identifier`, `attribute`, `temporal`, `categorical`, or `measurement`. |
| `value_type` | `integer`, `number`, `string`, `boolean`, `date`, or `datetime`. |
| `required` | Whether each data row must contain a value in this field; `TRUE`, `FALSE`, or blank. |
| `unit_label`, `unit_iri` | Human-readable unit and reviewed unit identifier. |
| `term_iri` | The term for the whole variable or field meaning. |
| `property_iri`, `entity_iri` | The characteristic measured and what it is about. |
| `constraint_iri` | Supported qualifiers; multiple IRIs are separated by semicolons. |
| `statistical_modifier_iri` | A supported summary meaning, such as mean or maximum. |
| `term_type` | `owl_class`, `owl_object_property`, or `skos_concept` for dictionary terms. |

For measurement rows, strict SDP validation requires `term_iri`, `property_iri`, `entity_iri`, and `unit_iri`. Constraint and statistical-modifier fields remain optional: do not invent qualifiers to fill empty cells. The dictionary's `required` flag concerns missing **data values**, not whether a metadata field is mandatory. [Canonical column fields][sdp-field-reference].

Use the human dictionary to review all source fields:

```text
POP_ID, POPULATION, AREA, WATERBODY, ANALYSIS_YR, SPECIES, RUN_TYPE,
NATURAL_ADULT_SPAWNERS, ESTIMATE_METHOD, ESTIMATE_CLASSIFICATION,
ESTIMATE_STAGE, START_DTT, END_DTT, WATERSHED_CDE
```

The [Glossary](glossary.html#i-adopt) explains the measurement components. A `REVIEW:` prefix marks a candidate that still needs a decision; it is not part of an accepted IRI.

## Code fields {#code-fields}

`metadata/codes.csv` describes stored categorical values. It is required when the dictionary marks a column as categorical.

| Field | Meaning |
| --- | --- |
| `dataset_id`, `table_id`, `column_name` | Identify the categorical source field. |
| `code_value` | Preserve the actual stored value. |
| `code_label`, `code_description` | Explain the value and any interpretation limits. |
| `vocabulary_iri` | Identify the vocabulary defining the code set, when one fits. |
| `term_iri` | Identify the particular term, when its definition fits. |
| `term_type` | The kind of term; follow the code schema, whose allowed values differ from the dictionary's. |

Start with `ESTIMATE_METHOD` and `ESTIMATE_CLASSIFICATION`. A missing source value and a named category such as “Unknown” must not be merged without evidence. For complete rules, including externally defined code lists, use the [canonical code fields][sdp-field-reference].

## Review and validation {#review-and-validation}

| Evidence or artifact | What it establishes |
| --- | --- |
| Human worksheet and peer review | A recorded interpretation, its evidence, and unresolved questions. |
| `semantic_suggestions.csv` | Candidate retrieval evidence; scores and ranks do not establish correctness. |
| Recorded AI outputs | Proposals to compare with the human graph, dictionary and source evidence. |
| Review-state validation | Structural checks that allow specified semantic work to remain unfinished. |
| Strict validation | Whether the checked package meets the implemented publication rules. |
| Schema-valid EML | Whether the exported metadata conforms to the EML schema. |
| Test publication receipt | The exact environment, identifiers, and upload outcome recorded by the rehearsal. |

The [teaching record](reference.html#teaching-record) records which technical checks, domain reviews and publication steps are complete for the supplied example.
