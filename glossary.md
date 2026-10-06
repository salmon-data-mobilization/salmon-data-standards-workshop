---
title: Glossary
---

Use these short explanations while drawing the human graph and reviewing metadata. They explain the workshop's usage; the linked standards and source documentation remain the authorities for formal definitions. For CSV field names and requirements, use the [Field reference](field-reference.html).

## Dataset {#dataset}

The collection being documented. Here it is the 173-row, 14-column Fraser Coho 2023–2024 extract, packaged with dataset ID `fraser-coho-workshop`. A dataset can contain more than one table, though this workshop keeps one source table.

## Table {#table}

A rectangular collection of records: columns hold fields and rows hold records. Our table ID is `escapement`; its exact row meaning is something we document and test against the source.

## Row grain {#row-grain}

What one record represents, including the dimensions needed to distinguish it from another record. Investigate population, analysis year, and method context before claiming that a row is uniquely identified by any combination. A plausible description is not a demonstrated primary key.

## Data dictionary {#data-dictionary}

A description of each data field: its meaning, expected values, units, and caveats. The human worksheet comes first; `metadata/column_dictionary.csv` later records the accepted descriptions in the package's required structure.

## Metadata {#metadata}

Information needed to find, interpret, or reuse the data: descriptions, provenance, contacts, units, code meanings, and rights. Metadata includes the evidence behind an interpretation, not just a list of column names.

## FAIR {#fair}

Findable, Accessible, Interoperable, and Reusable: principles for making data and metadata easier for people and machines to discover and use. FAIR does not mean that access is unrestricted or that every interpretation has been scientifically approved. [FAIR principles][fair-principles].

## Salmon Data Package {#salmon-data-package}

An SDP keeps data CSVs, structured metadata CSVs, a generated package descriptor, and human context together. Its files must agree about IDs, columns, and meanings. The [SDP specification][sdp-specification] defines the validity rules.

## Observation {#observation}

An activity that establishes a value for a property of something. In the human graph, distinguish that activity from the thing studied and the result recorded. A source row may summarize evidence from several activities; do not assume it is one field visit. This distinction follows [SOSA/SSN][sosa-ssn].

## Result {#result}

The output of an observation or estimation activity. A populated `NATURAL_ADULT_SPAWNERS` cell holds a reported value; the number alone does not tell us its scope, method, or completeness. A blank remains missing, not zero. See [SOSA results][sosa-ssn].

## Measurement {#measurement}

A recorded or computed quantity, interpreted with its property, entity, unit, and context. The workshop focuses on `NATURAL_ADULT_SPAWNERS`; the field name is the starting point for reviewing its meaning, not a complete definition.

## Variable {#variable}

The reusable description of what is measured or represented. A variable is distinct from a particular result: the definition can apply to many observations whose values differ. In the SDP dictionary, `term_iri` can identify the whole measurement variable.

## Entity {#entity}

The thing a measurement is about. Identify its scope from the source: a particular population, a group of organisms, or another defined object may be relevant. In [I-ADOPT][iadopt], an entity participates in the definition of a variable.

## Property {#property}

The characteristic being measured, such as abundance, length, or mass. It is distinct from the entity that has the characteristic and the result that records its value. See [I-ADOPT][iadopt].

## Unit {#unit}

The scale used to express a numeric result, such as a length unit or a count unit. Store a readable label and, when required, a reviewed unit IRI. Read the unit definition; a label that sounds familiar can still be wrong. [QUDT][qudt] is one unit vocabulary.

## Constraint {#constraint}

A qualifier that narrows a variable's meaning, such as a documented life stage or origin. Add it only when the evidence establishes the restriction. A qualifier in the column name still needs interpretation. See [I-ADOPT][iadopt].

## Statistical modifier {#statistical-modifier}

The form of a reported summary, such as a mean, maximum, or total. It changes what the value represents. Do not add one merely because multiple observations or a method were involved; record the documented summary meaning. See the [SDP field reference][sdp-field-reference].

## Method {#method}

How an observation or estimate was produced. It is different from the variable being measured. `ESTIMATE_METHOD` varies between source records, so its stored values need code-level descriptions. A table-wide method is appropriate only if it actually applies uniformly. See [SOSA procedures][sosa-ssn].

## I-ADOPT {#i-adopt}

A framework for describing variable meaning through components such as property, entity, and constraints. The workshop uses this decomposition to expose assumptions before selecting identifiers. A complete-looking diagram is still a proposal until its components are supported. [I-ADOPT ontology][iadopt].

## Controlled vocabulary {#controlled-vocabulary}

A maintained set of terms or codes with documented meanings and identifiers. It can help people use a label consistently without requiring a detailed formal model of every relationship. [SKOS][skos-reference] supports concepts, labels, definitions, and links between concepts.

## Ontology {#ontology}

An explicit model of concepts and their relationships, often including rules about how they may be used together. Our hand-drawn graph makes those relationships discussable before we consider formal ontology terms. [OWL][owl-overview] is one language used to express ontologies.

## SKOS {#skos}

Simple Knowledge Organization System: an RDF vocabulary for representing concept schemes with identifiers, labels, definitions, notes, and relationships. A code in a source table can be associated with a SKOS concept; the code, label, and concept have different roles. [Chapter 9](session-9.html) builds a small scheme. [W3C SKOS Primer][skos-primer].

## OWL {#owl}

Web Ontology Language: a language for logical statements about classes, properties, and individuals. Its statements can imply further facts. A missing value is not automatically false under its open-world interpretation. [Chapter 10](session-10.html) demonstrates selected consequences and their limits. [W3C OWL Primer][owl-primer].

## RDF and Turtle {#rdf}

RDF expresses a graph as subject–predicate–object statements. Turtle is a readable text syntax for writing those statements. Turtle files can describe data, vocabulary concepts, ontology axioms, or mappings; the file extension alone does not establish which kind of claim is inside. [RDF Primer][rdf-primer].

## Class and individual {#class-and-individual}

A class describes a category; an individual is something a statement is about. In the teaching model, a source-record class and the individual representing a particular source row are distinct. A SKOS concept is not automatically an OWL class. SDO requires separate identifiers when both representations are needed; instance-typing a concept as a procedure is a different operation. [SDO conventions][sdo-conventions].

## Namespace {#namespace}

An IRI prefix used to organize identifiers. The classroom uses `https://example.org/fraser-coho-workshop/terms/` for explicitly draft terms. A real organization needs an identifier and maintenance policy for its own namespace; an IRI's appearance does not establish authority or web availability.

## Bridge {#bridge}

A separate set of statements connecting local meanings to shared meanings. Each mapping needs an appropriate relationship, direction, evidence, and review record. A bridge can preserve useful differences rather than replacing local identifiers. [Chapter 11](session-11.html) constructs and assesses one. [SDO bridge guide][sdo-bridge-guide].

## Entailment {#entailment}

A statement that follows logically from specified assertions and rules. Which files and rules were loaded matters. A limited classroom reasoner demonstration does not establish every consequence of a full ontology import closure or independently verify the science. [OWL Primer][owl-primer].

## SHACL {#shacl}

Shapes Constraint Language: a way to test an RDF graph against explicit conditions, such as requiring a value or limiting its count. It addresses conformance of supplied data. OWL domain and range statements instead support logical inferences about types. The workshop runs selected SHACL shapes and bounded OWL RL reasoning; these checks do not establish full SDO conformance or complete OWL DL consistency. [W3C SHACL Recommendation][shacl-reference].

## SSSOM {#sssom}

Simple Standard for Sharing Ontological Mappings: a format for exchanging mappings and their metadata. The mapping predicate determines the relationship being claimed. A mapping table and a Turtle file can express the same proposed relationship; a format change does not strengthen its evidence. [SSSOM specification][sssom-spec].

## Competency question {#competency-question}

A concrete question the model should help answer. For this source, “which record carries this result and analysis year?” is different from “which field survey produced it?” The latter may remain unanswered when source evidence is missing. Use these questions to decide what to model and what to test.

## Term request {#term-request}

A proposal asking a vocabulary or ontology's stewards to review a missing concept or change. It records the supported meaning, existing candidates, evidence, intended scope, and unresolved decisions. A request, local draft, or passing check is not a term's admission into a shared resource. [Chapter 12](session-12.html) prepares a request or source-clarification draft.

## IRI {#iri}

An Internationalized Resource Identifier names a resource, such as a concept in a vocabulary. Many look like web addresses. In this workshop, an IRI links a local field or code to a term whose definition must fit. A resolving link alone does not prove that fit. See the [RDF primer][rdf-primer].

## Persistent identifier {#persistent-identifier}

An identifier managed so a resource can remain identifiable over time, often across versions or storage changes. A DOI is a common example. A test catalog's identifier is useful for a rehearsal, but does not carry a production archive's durability commitment. The publication receipt records exactly which object and environment were used.

## Semantic mapping {#semantic-mapping}

A documented relationship between a local meaning and a shared term. Record what was compared, the relationship claimed, the evidence, and the review decision. Similar wording does not establish equivalence. [SKOS mapping relations][skos-reference] distinguish several strengths of relationship.

## Provenance {#provenance}

The record of where data or a claim came from and what happened to it. Keep the NuSEDS source, extraction steps, source date, package version, and subsequent metadata decisions distinguishable. A teaching adaptation should remain traceable to its source. See the [bundled example notes][metasalmon-example-data].

## AI {#ai}

Artificial intelligence. Here, a language model generates proposed descriptions or mappings from supplied material. Its output is evidence to examine, not source authority. Everyone compares recorded outputs with their own dictionary; optional live calls do not replace that review.

## EML {#eml}

Ecological Metadata Language: a structured XML format for describing ecological data. The package exporter translates reviewed information into EML and checks its structure. Schema validation cannot determine whether a biological definition or licence claim is true. [EML documentation][eml-specification].

## KNB {#knb}

The Knowledge Network for Biocomplexity provides a catalog and data repository. This workshop uses the **KNB Test Node** to rehearse publication. A local dry run, a test upload, and a production deposit are different outcomes; the [teaching record](reference.html#teaching-record) reports which one was verified. [KNB][knb].
