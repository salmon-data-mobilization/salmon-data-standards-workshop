# Draft bridge experiments

The separate `bridge.ttl` asserts two classroom proposals:

1. Local AUC method concept `skos:relatedMatch smn:EnumerationMethod`.
2. Local `NuSEDSMethodDescription rdfs:subClassOf smn:MethodDocumentation`.

They are not approved source annotations or production integration rules. A
draft annotation does not disable the logical effect of a loaded triple.

`mapping-decisions-working.csv` includes these and four rejected/deferred
alternatives, with evidence and counterexamples. Its human decision fields are
blank. Complete your own `semantic-lab/worksheets/bridge-decisions.csv` after
reading both endpoint definitions and your human baseline. Preserve the original
source codes and use `output/semantic-lab/` for learner copies and reports.

`shared-anchors.ttl` is an exact selected-subject excerpt from SDO commit
`d45f8f7cc857d92af8bbe54a7c89b2a4a14784b2`.
`shared-anchor-sources.json` gives the source module paths and checksums. It is not
the whole SDO or its imports. The `EnumerationMethod` anchor is a SKOS concept and
an instance of `sosa:Procedure`; the documentation, population, abundance, and
escapement-estimate anchors are OWL classes.

From the kit root with the pinned semantic environment active:

```bash
python semantic-lab/scripts/check_bridge.py --report output/semantic-lab/bridge-check-01.json
```

The learner command requires the existing human preparation record. It parses
only local files, checks actual row 5 and pinned anchor bytes, tests endpoint
types, compares the draft with its proposal table, and computes selected
consequences. It also tests an in-memory broad/narrow direction hypothesis and a
conflicting stronger mapping. No API request, source edit, or upload occurs.

The SKOS rule excerpt preserves the W3C mapping-rule predicates and directions;
it is deliberately labelled as an excerpt. Loading an IRI does not by itself
load its schema. Absence from this selected rule closure is not a general
non-entailment proof for an arbitrary imported graph. No full OWL DL classifier,
SKOS validation suite, or SSSOM validator is run.

The class bridge has a straightforward counterexample to reverse inclusion:
documentation of a method in another salmon program can be shared
`MethodDocumentation` without being a NuSEDS method description. The subclass
statement permits that situation; equivalence would remove the distinction.

The worksheet is not an SSSOM serialization claim. SSSOM can carry mappings and
their metadata, but the mapping predicate still determines whether the relation
is identity, subclass, or a SKOS relationship. Formatting does not approve a
meaning or strengthen a predicate.

Sources: [SDO mapping policy](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/d45f8f7cc857d92af8bbe54a7c89b2a4a14784b2/CONVENTIONS.md),
[W3C SKOS mappings](https://www.w3.org/TR/skos-reference/#mapping),
[OWL semantics](https://www.w3.org/TR/owl2-direct-semantics/), and
[SSSOM documentation](https://mapping-commons.github.io/sssom/dev/).
