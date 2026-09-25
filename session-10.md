---
title: "Turn the Human Graph into a Small OWL Model"
teaching: 35
exercises: 55
---

:::::::::::::::::::::::::::::::::::::: questions

- Which parts of our human diagram are classes, relationships, individual objects, or literal values?
- What new information follows from an OWL statement?
- How can a graph pass a reasoning check and still lack required information?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Translate a small part of the reviewed Fraser Coho diagram into local OWL classes and properties.
- Trace individual objects and literal values to actual records in the unchanged source.
- Predict and inspect subclass, domain, and range inferences.
- Contrast open-world reasoning, SHACL conformance, and scientific review.
- Keep source records, result values, population references, and method concepts distinct.

::::::::::::::::::::::::::::::::::::::::::::::::

## Start with a question the model should answer

We have already described the data and built a small vocabulary. Now we want another system to recognize relationships that a person can see in the diagram. For example: **if a NuSEDS record has a reported result, what kind of object is that result?** A second question is just as useful: **does a missing result tell us that zero fish were reported?**

Return to your actual Chapter 2 diagram, Chapter 3 dictionary and decomposition, and named, dated peer review. Complete those before running the graph tools. Compare the proposed statements in `semantic-lab/worksheets/model-statements.csv` with your own diagram. The supplied N1–N11 references point to the facilitator's working diagram; substitute your own node identifiers when they differ. Record a decision, reason, and remaining question for each statement you examine.

The model in this chapter is deliberately about what the source records. We do not know the identities of the field visits behind every estimate, the exact population boundaries, or every calculation used. A diagram can show those questions before a formal ontology has enough evidence to assert the answers.

## Read two real records carefully

Open the full `raw_data/nuseds-fraser-coho-2023-2024.csv`. Count data rows from one, excluding the header:

| Data row | Source population | Analysis year | Adult-spawner cell | Method label |
| --- | --- | --- | --- | --- |
| 1 | `46200`, Bonaparte River (Lillooet) Coho | 2023 | 758 | Resistivity Counter |
| 2 | `44965`, Clapperton Creek (Lillooet) Coho | 2023 | blank | Not Applicable |

These are two illustrations within the same **173-row, 14-column table**. `semantic-lab/model/source-trace.json` retains their complete source values and the CSV checksum. A row position locates a record only in that exact file version; it is not a permanent NuSEDS identifier. `POP_ID` plus `ANALYSIS_YR` is still not a demonstrated unique key for the full file.

Row 1 gives us a record, a reported numeric result, a population reference, and a year. The official dictionary describes the adult-spawner field as mature salmon excluding jacks. It does not establish natural-origin scope. The method label tells us which category was stored; the current dictionary's `N/A` entry for Resistivity Counter leaves its operational definition unresolved. Row 2 supplies no numeric estimate. Preserve both limits.

![Two actual source records represented as distinct records, results, references, and literals.](files/fraser-coho-workshop/semantic-lab/model/record-model.svg)

The editable diagram is `semantic-lab/model/record-model.mmd`. The model and instance files make the distinction between the kinds of objects and the particular objects explicit.

## Decide what each box and arrow represents

An [OWL](glossary.html#owl) [class](glossary.html#class-and-individual) describes a kind of thing. An **individual** is a particular thing. An **object property** connects individuals, while a **datatype property** connects an individual to a literal, such as the number `758`. An IRI names a resource; a label helps a person read it. These are separate roles. [OWL basic modelling](https://www.w3.org/TR/owl2-primer/#Classes.2C_Properties.2C_and_Individuals_.E2.80.93_And_Basic_Modeling_With_Them).

| Part of the human explanation | Representation in this exercise | Question that remains |
| --- | --- | --- |
| A kind of source record | Class `NuSEDSEstimateRecord` | Which source record identifiers would support a durable identity? |
| This particular first record | Individual `record-1` | Does a later source version retain the same record? |
| Its reported estimate | Individual `result-1`, with decimal literal `758` | Which procedure and assumptions produced this value? |
| Its population identifier and label | Individual `population-reference-46200` | What biological or operational population does the reference identify? |
| The adult-spawner field description | Individual `adult-spawner-field` | Which reviewed variable, entity, property, and unit links apply? |
| “Has reported result” | Object property `hasReportedResult` | Are we connecting the record to its datum rather than to an activity? |
| The recorded analysis year | Datatype property with a `gYear` literal | What biological year basis would a later analysis require? |
| The estimate-method category | The Chapter 9 SKOS concept, when supported | Is a category enough, or do we need a detailed protocol? |

The [Salmon Domain Ontology metamodel](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/d45f8f7cc857d92af8bbe54a7c89b2a4a14784b2/ontology/views/salmon-data-metamodel.ttl) helps distinguish entity, characteristic, variable, method, activity, and result. It is an optional teaching view, separate from the shared core. Use it to ask sharper questions; do not mechanically turn every box into an OWL class.

Pay particular attention to the word **property**. The measured characteristic, such as abundance, is a role in the human/I-ADOPT decomposition. An OWL object property, such as `hasReportedResult`, is a relationship predicate. The reusable `smn:Abundance` anchor is an OWL class in the pinned SDO source. It is not interchangeable with an arrow merely because both discussions use the word “property.”

## Read the small model before running it

Open `semantic-lab/model/model.ttl`. The prefix `ex:` expands to the teaching namespace `https://example.org/fraser-coho-workshop/terms/`. These local IRIs are classroom names, not identifiers minted by DFO or the Salmon Domain Ontology. Particular objects use the separate `/instances/` namespace.

```turtle
ex:SourceRecord a owl:Class .

ex:NuSEDSEstimateRecord a owl:Class ;
    rdfs:subClassOf ex:SourceRecord .

ex:hasReportedResult a owl:ObjectProperty ;
    rdfs:domain ex:NuSEDSEstimateRecord ;
    rdfs:range ex:RecordedNumericResult .
```

Read the subclass statement as “every NuSEDS estimate record is a source record.” It does not say that every source record is a NuSEDS estimate record. **Subclass is not equivalence.** A source record from another kind of table can belong to the broader class without belonging to the narrower one. [RDF Schema subclass semantics](https://www.w3.org/TR/rdf-schema/#ch_subclassof).

Now open `semantic-lab/model/instances.ttl`:

```turtle
row:record-1 a ex:NuSEDSEstimateRecord ;
    ex:hasReportedResult row:result-1 .

row:result-1 ex:numericValue "758"^^xsd:decimal .
```

The complete file also retains the source row locator, population reference, year, and field description. Decimal values allow for fractional estimates elsewhere in this source; do not impose whole-fish integers on every estimate. The result's type is intentionally not written next to it: the range rule lets us infer it. Before running anything, predict these three outcomes:

1. `record-1` will also be a `SourceRecord` through the subclass rule.
2. `result-1` will be a `RecordedNumericResult` through the range rule.
3. If we remove the explicit record type from a scratch graph but keep `hasReportedResult`, the domain rule will infer the record type again.

Domain and range describe the types inferred from a property's use. They are not dropdown restrictions that stop an inappropriate edge from being entered. Multiple domains normally imply membership in every stated domain; they do not mean “choose any one.” [RDF Schema domain and range](https://www.w3.org/TR/rdf-schema/#ch_domain).

## Compare reasoning with required information

Suppose someone mistakenly connects `population-reference-46200` directly to `result-1` using `hasReportedResult`. The domain rule now classifies that reference as a NuSEDS estimate record too. Without additional incompatible axioms, the type inference itself does not reject the mistaken edge. We need a source interpretation and an appropriate checking rule to recognize the error.

OWL uses an **open-world** approach: information missing from the graph may simply be unknown. The absence of a result triple for row 2 does not assert zero, prove that no estimate could exist elsewhere, or provide a reason for the blank. Likewise, an OWL model is not a requirement that a document explicitly contain a year value. [OWL's information and schema distinction](https://www.w3.org/TR/owl2-primer/#What_is_OWL_2.3F).

`semantic-lab/model/record-shapes.ttl` adds separate classroom conformance requirements using [SHACL](glossary.html#shacl):

```turtle
ex:RecordShape a sh:NodeShape ;
    sh:targetClass ex:NuSEDSEstimateRecord ;
    sh:property [
        sh:path ex:analysisYear ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:gYear
    ] .
```

This SHACL shape requires one year value on each targeted record. The full supplied shape permits a missing numeric result because blanks occur in the source. It is a local exercise contract, not the complete NuSEDS or SDP schema. The checker applies RDFS inference for its SHACL run and reports that choice. [SHACL validation and shapes](https://www.w3.org/TR/shacl/#introduction).

| Check | What it answers here |
| --- | --- |
| Turtle parsing | Can the software read the graph's syntax? |
| Selected OWL/RDFS rule inferences | Which additional triples follow through the tested rules? |
| SHACL | Does this data graph meet the supplied shape requirements? |
| Source-trace regression check | Do the illustrated objects still match the pinned CSV records? |
| Human review | Does the model represent the intended scientific and operational meaning? |

Passing one row does not answer all five questions.

## Run the offline checks

Use the semantic-lab environment from [Setup](setup.html). Its requirements file pins `rdflib==7.1.4`, `owlrl==7.1.4`, and `pyshacl==0.30.1`. From the workshop project root, with that Python environment active:

```bash
python semantic-lab/scripts/check_model.py --report output/semantic-lab/model-check-01.json
```

Run this utility in the separate Python RDF environment from Setup, whichever SDP lane you chose. Spreadsheet participants can make the statement table and predictions, then inspect a partner's or facilitator's run. Record whether you executed or inspected the result.

The learner command checks the Chapter 2–3 preparation record before loading the model. It reads local Turtle files, resolves no ontology imports, makes no API calls, preserves the source, and refuses to overwrite a report. Use a new report name on the next run.

The supplied example reports 15 named checks, including deliberately broken **in-memory** cases. Removing a required year must fail SHACL; adding the mistaken edge must infer the extra type; a deliberate class/SKOS-concept IRI collision must be rejected by the targeted workshop policy check. A passing report means those expected contrasts occurred. It does not mean the deliberately broken graph was accepted as correct.

The inference library implements rule-based OWL RL reasoning. This exercise is not a full OWL DL consistency or completeness assessment of the Salmon Domain Ontology and its imports. In particular, “not present in this selected closure” is a bounded observation, not a general proof that a statement cannot follow under some larger ontology. [OWL profiles](https://www.w3.org/TR/owl2-profiles/#OWL_2_RL), [OWL-RL implementation](https://owl-rl.readthedocs.io/en/latest/).

::::::::::::::::::::::::::::::::::::: challenge

## Activity: formalize, predict, and challenge

Work in pairs for 55 minutes:

1. **Read and decide, 15 minutes.** Compare at least four proposed model statements with your human diagram and dictionary. Include the record/result distinction and the blank estimate. Fill your decision, reason, and reviewer fields in `semantic-lab/worksheets/model-statements.csv`.
2. **Make a local model copy, 15 minutes.** Create `output/semantic-lab/` if needed. Copy `model.ttl` to `output/semantic-lab/model.ttl` and `instances.ttl` to `output/semantic-lab/instances.ttl`, without overwriting an earlier copy. Improve one local class description so another pair can distinguish its instances from nearby objects. Keep source values and the shared namespace unchanged.
3. **Predict before running, 10 minutes.** Write the expected subclass, domain, and range results. Run the checker against the copies with `--model output/semantic-lab/model.ttl --instances output/semantic-lab/instances.ttl`, choosing a new report filename. Explain any difference from your prediction.
4. **Challenge the interpretation, 15 minutes.** Read the two in-memory mutation tests in the report. Explain why the missing year is a conformance failure and why the mistaken edge produces an inference. Propose one additional test for a question in your own graph, including a counterexample. Mark any unimplemented proposal clearly.

Your output is an edited local model, a source trace, explicit predictions, and a reviewed statement table. Keep the uncertain survey, population, origin, and unit questions visible. Chapter 11 adds bridges only after comparing the types and definitions on both sides.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Formal statements begin with reviewed human meanings and questions.
- Classes, individual objects, relationship predicates, and literal values play different roles.
- Subclass, domain, and range can add type information; they do not replace conformance checks.
- A blank source cell does not become zero or an OWL negation.
- Parsing, selected inference, SHACL, source fidelity, and scientific review establish different things.

::::::::::::::::::::::::::::::::::::::::::::::::
