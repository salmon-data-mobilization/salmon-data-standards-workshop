# Metamodel guidance included for offline comparison

Status: source-grounded teaching summary; not an approved Fraser Coho mapping.

These notes summarize the Salmon Domain Ontology checkout inspected at commit
`d45f8f7`. The references below identify its canonical files. They let learners
evaluate the recorded AI propositions offline without treating the recording
itself as the authority for every modeling distinction.

| Distinction | Source guidance | Consequence for the workshop |
| --- | --- | --- |
| Entity / property / variable | `ontology/views/salmon-data-metamodel-variable.ttl` describes a variable as an observed property of an entity, with optional constraints and statistical modifiers | Preserve the complete variable and its components separately |
| Activity / result | `ontology/modules/02-observation-measurement.ttl` makes `smn:Measurement` a subclass of `smn:Observation`; `smn:EscapementEstimate` is an IAO measurement datum | A numerical cell is a result value, not an observation activity |
| Abundance and qualifiers | The same module defines `smn:Abundance` as a reusable characteristic and distinguishes units, statistical modifiers, context and procedures | Using abundance as a property does not resolve the full adult-spawner meaning |
| Row coordinates / fixed constraint | `CONVENTIONS.md` section 12 separates year basis, dimension property and coordinate value; row-varying year/age coordinates are dimensions | Do not make 2023 a fixed constraint on the full two-year column |
| Method / result | `ontology/views/salmon-data-metamodel-method-protocol.ttl` links an observation to the procedure it used | Keep the row's estimate method connected to the activity producing the result |
| Metamodel status | `ontology/views/README.md` calls the view optional and non-normative, outside the shared-core imports | A teaching diagram does not by itself establish normative OWL or approved mappings |

No source in these notes establishes that `NATURAL_ADULT_SPAWNERS` means
natural-origin fish, assigns a CU to a source population, or authorizes
aggregation of repeated records. Those are dataset/source questions, not facts
that a general metamodel can supply.

For online source inspection, use the [ontology repository at the recorded
commit](https://github.com/salmon-data-mobilization/salmon-domain-ontology/tree/d45f8f7).
The preserved official NuSEDS dictionary and source table under `../raw_data/`
supply the complementary dataset evidence.
