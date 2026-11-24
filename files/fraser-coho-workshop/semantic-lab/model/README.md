# Draft source-record model

Use after the actual human graph, dictionary, decomposition and peer review. The
learner command checks that preparation record. These files do not approve a
biological interpretation or define an official NuSEDS/SDO ontology.

- `model.ttl`: local OWL classes and properties for records, reported values,
  source population references, variable descriptions, and method documentation.
- `instances.ttl`: data rows 1 and 2 from the unchanged 173×14 source, plus a
  documentation item for the official AUC method explanation.
- `source-trace.json`: full values and the source hash for model rows 1–2 and
  bridge examples 5 and 39. Positions count data rows, excluding the header.
- `record-shapes.ttl`: small local SHACL requirements, separate from OWL meaning.
- `record-model.mmd` and `record-model.svg`: editable diagram and reading view.

The model treats `numericValue` as decimal, preserving the possibility of
fractional estimates. It does not create an observation-activity identity from a
source row, assert a natural-origin qualifier, or treat a population reference as
a biological group. Unit and richer I-ADOPT alignments remain human review work.

From the kit root, activate the environment containing the versions in
`semantic-lab/scripts/requirements.txt`, then run:

```bash
python semantic-lab/scripts/check_model.py --report output/semantic-lab/model-check-01.json
```

The command checks preparation, parses local files, checks the source trace,
computes selected OWL RL consequences, and runs the local SHACL shapes. It also
tests three in-memory changes: a missing year, a mistaken edge, and a forbidden
class/concept IRI collision. Those mutated examples are never saved to the model.
Use a new report filename; existing reports are not overwritten.

For an edited model copy, pass `--model output/semantic-lab/model.ttl` and
`--instances output/semantic-lab/instances.ttl`. Checks retain the documented
reference expectations; a changed meaning may require an explicitly reviewed
change to those expectations, not merely an error suppression.

The separate maintainer command `python semantic-lab/scripts/check_reference.py`
inspects the distributed drafts while the distributed peer-review sheet remains
pending. It does not complete or simulate human review and is not the learner
preparation route.

“Absent from this closure” is a limited check. A counterexample interpretation
helps explain the subclass boundary: a record from another source can be a
`SourceRecord` without being a `NuSEDSEstimateRecord`. The supplied subclass axiom
permits that interpretation, so reverse inclusion is not justified. No full OWL
DL proof or complete imported-ontology classification is claimed.

Sources: [SDO conventions](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/d45f8f7cc857d92af8bbe54a7c89b2a4a14784b2/CONVENTIONS.md),
[SDO metamodel](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/d45f8f7cc857d92af8bbe54a7c89b2a4a14784b2/ontology/views/salmon-data-metamodel.ttl),
[OWL primer](https://www.w3.org/TR/owl2-primer/),
[RDF Schema](https://www.w3.org/TR/rdf-schema/), and
[SHACL](https://www.w3.org/TR/shacl/).
