---
title: "Help Your Salmon Data Travel Further"
teaching: 40
exercises: 15
---

:::::::::::::::::::::::::::::::::::::: questions

- Why does preparing and sharing salmon data take so much work?
- How can common formats and shared meanings make reuse easier?
- What will we create over the two days, and how will it help our colleagues?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Relate the workshop's reuse and publication problems to your own work with salmon data.
- Explain how packaging data, sharing definitions and recording relationships support reuse.
- Describe what you can publish after Day 1 and what you can develop or contribute on Day 2.
- Recognize how drawing and describing a dataset helps someone else understand it.

::::::::::::::::::::::::::::::::::::::::::::::::

## I've got data. Why is reuse still so hard? {#framing-the-challenge}

### A typical research project: reuse data to answer a question

You start with a biological question, some promising files from other studies and a deadline. Before you can analyse anything, you need to find the right columns, connect them to the methods and work out what can be compared. The answers may be scattered across papers, appendices and emails. New questions appear when you combine the tables.

### Publish what the next researcher will need

Later, you may be asked to publish the data behind your paper or make them [FAIR](glossary.html#fair): **findable, accessible, interoperable and reusable**. Here, interoperable means that different systems can exchange and use the data. Reconstructing explanations at the end takes more work, and the next user may still need to email you. Capturing answers as you go can help both of you.

### Our example: annual spawner abundance by Conservation Unit

Our task is to **assemble the best available annual estimates of salmon spawner abundance by Conservation Unit (CU)** across several regions. A CU groups salmon populations for conservation and assessment. We want records for each CU and year, with differences in which fish were included, estimation methods and uncertainty kept visible.

## The archetypical data problem

Two files look promising. Here is one 2023 record from each, showing selected columns with their original names and values. These records concern different CUs; our aim is to retain their separate identities in a combined table.

### Yukon Chinook: which quantity does `mean` describe?

The [Yukon project][yukon-methods] uses **run reconstruction**: combining river-border passage estimates, genetic information and estimates of fishery harvest to reconstruct salmon abundance for CUs. Its output contains a column called `mean`.

| stock | year | mean |
| --- | --- | ---: |
| NorthernYukonR.andtribs. | 2023 | 2009.4529003227 |

The [Yukon excerpt](files/intro-comparison/yukon-excerpt.csv) also contains `lower` and `upper`, which describe uncertainty around the estimate. We need the methods to establish exactly what the estimate and those limits represent.

### Fraser Rapid Status Assessment: which column contains abundance?

The [Rapid Status Assessment output][fraser-dictionary] reports assessments of the conservation status of salmon CUs. It includes abundance estimates alongside the measures used to assess status. This record concerns a Lower Fraser **Chinook** CU.

| CU_ID | Stock | Year | SpnForAbd_Total |
| --- | --- | --- | ---: |
| CK-03 | Lower Fraser River_FA_0.3 | 2023 | 146371 |

The [Fraser excerpt](files/intro-comparison/fraser-excerpt.csv) also contains `SpnForAbd_Wild`, `DataType` and `ConfidenceRating`. Which columns answer our abundance question, and what do we need to know before using them together?

The downloads retain all source columns for the selected 2022–2023 records. [Source notes](files/intro-comparison/PROVENANCE.txt) record where they came from; the [file-check manifest](files/intro-comparison/source-manifest.json) contains checksums, digital fingerprints used to detect changes to the files.

## Follow these records through two research workflows

The left timeline starts with those Yukon and Fraser files and the work of finding their explanations. The right imagines receiving the same sources as reviewed [Salmon Data Packages](glossary.html#salmon-data-package): **data and their descriptions kept together in a common file structure**.

Those descriptions are [metadata](glossary.html#metadata), information that helps people find, interpret and reuse data. One part is a [data dictionary](glossary.html#data-dictionary), which explains each column's meaning, units and possible values. A package also keeps methods and source information with the table.

**Next** adds a phase to both timelines. Select a step to open its details inside the diagram. The comparison asks what changes when the explanations we work out once are available to the next user.

<section id="salmon-workflow-guided" aria-label="Interactive workflow comparison">
<p>The interactive comparison requires JavaScript. The text version below follows the same four phases.</p>
</section>

[Open the diagram on its own](files/workflow-explorer/index.html).

<details class="workflow-text" id="workflow-text">
<summary>Read the workflow as text</summary>

1. **Find and understand the data.** We look for explanations of Yukon `mean` and Fraser `SpnForAbd_Total` in methods, dictionaries and correspondence. A reviewed package preserves those explanations with the original fields and values.
2. **Check and combine the estimates.** Both fields are candidates for an abundance comparison. Linking their descriptions to a shared abundance definition helps software find them despite different column names. We still check each population, year, included fish, method and uncertainty. The prepared example below shows this link and the remaining questions.
3. **Keep the estimates and their limits visible.** Retain each CU's estimates with their methods and uncertainty. As a supporting example, Fraser `ConfidenceRating` concerns assessment status; treating it as abundance precision would produce an unsupported claim. The green check marks the interpretation checked against that field's definition.
4. **Publish once, help the next project.** Preserve the source descriptions and the decisions behind the combined table. Reviewed source and derived packages, with appropriate credit and permission, give the next user more of the preparation work already done.

[Static overview of the interpretation loop](fig/comparison-workflows.svg).

</details>

## My life would have been easier if the meanings came with the data

### Different column names, a shared characteristic

A [controlled vocabulary](glossary.html#controlled-vocabulary) is a maintained set of terms with definitions and identifiers. It gives us shared meanings to use when describing data. An [ontology](glossary.html#ontology) is an explicit model of concepts and their relationships that software can interpret. For example, it can distinguish a population, an estimation activity and the result that activity produced.

The **Salmon Domain Ontology** provides shared concepts and relationships for salmon data. Its [Abundance term][abundance-definition] describes a quantity associated with a specified group, place and time. This is a **property**—the characteristic represented by a measurement or estimate. The complete description still needs to say whose abundance, when, which fish and how it was estimated.

Here is a small **teaching draft of the descriptions** that could accompany our two records. It illustrates Phase 2's shared-meaning link; the proposed descriptions still need source and domain review.

| Description to retain | Yukon record | Fraser record |
| --- | --- | --- |
| Source field and reported value | `mean`: `2009.4529003227` | `SpnForAbd_Total`: `146371` |
| Population and year | `NorthernYukonR.andtribs.`, `2023`; confirm its CU identifier and year definition | `CK-03`, `2023`; the source defines `Year` as the year fish return to spawn |
| Proposed property link | [Abundance][abundance-definition] | [Abundance][abundance-definition] |
| Context and questions | Reconstruction method; included fish; meaning of `lower` and `upper` | Total versus wild fish; abundance versus an index; estimation method; status confidence kept separate |

Both proposed property links use the identifier `https://w3id.org/smn/Abundance`. A term identifier of this kind is called an **Internationalized Resource Identifier ([IRI](glossary.html#iri))**. It names a concept independently of the words used for a column.

This makes a practical difference: software could find fields described with that abundance identifier even when their names differ. The ontology provides a way to state which population an estimate concerns, which characteristic it represents and which result was produced. Our descriptions and explicit mappings—recorded connections between source fields and meanings—supply those relationships. People check whether the resulting estimates fit the research question.

### Keep the differences that matter

The [Fraser dictionary][fraser-dictionary] describes `SpnForAbd_Total` as total spawner abundance used in abundance-based assessment measures. It distinguishes this from wild spawner abundance and from a **relative index**, a measure of change on a scale that need not be a count of all fish. The selected record's `DataType` is `Abs_Abd`, indicating absolute abundance.

For the Yukon estimate, retain the [reconstruction methods][yukon-methods] and check which fish, years and uncertainty limits it covers. Sharing an abundance term helps us locate candidate fields; these additional descriptions support the decision about using the estimates together.

Our intended output is **a set of CU–year estimates with their methods, scope and uncertainty visible**. Here, scope means which fish and places an estimate covers. Different methods may be acceptable for assembling the best available estimates. A study comparing one particular estimation method would need a different selection.

### Catch a plausible mistake along the way

In the Fraser record, `ConfidenceRating` is `High`. The source dictionary defines it as confidence in the **assessment status**. Reading it as evidence that the abundance estimate is more precise would be a mistake. Keep it separate from the Yukon estimate's `lower` and `upper` limits.

This is the caution/check example in Phase 3. It is an invented misreading of real fields, not an error attributed to the source authors. Checking the definition prevents this particular unsupported conclusion; the other questions about using the estimates together still need review.

### Save the work for the next project

The R software package **metasalmon**, and its Python counterpart, help create, review and validate Salmon Data Packages. Validation checks whether the files follow the required structure and agree with one another. Study-specific code uses the recorded mappings to combine data; people supply the evidence and decide which differences matter.

When we prepare publication, the package already carries the descriptions and source history. We can credit the original data providers and the people who prepared the package, and preserve how a combined dataset was produced. Later projects can reuse both the data packages and the maintained definitions they reference.

## And now someone sends you a third dataset

**NuSEDS** is the **New Salmon Escapement Database System**, maintained by Fisheries and Oceans Canada (DFO). It records salmon **escapement**: fish returning to fresh water to spawn after passing through fisheries. Its [Open Government Portal record][nuseds-source] provides data and supporting documentation.

The [Central Coast example](https://salmonwatersheds.ca/document/lib_451/) starts with stream records and uses additional information and expansion factors—multipliers used to account for fish beyond the observed counts—to produce estimates for CUs. A stream record and a whole-CU estimate can both describe abundance while covering different groups and places.

This adds a question to Phase 2: how do stream observations support the CU estimate? We need the population relationships, coverage and estimation method as well as the shared abundance term. The next chapters practise recording those relationships.

## Let's make one dataset easier for the next person

For the exercises, we switch to a **Fraser Coho NuSEDS teaching dataset**. It is separate from both the Fraser **Chinook** Rapid Status Assessment records above and the Central Coast illustration.

Download and extract the [Fraser Coho workshop kit](files/fraser-coho-workshop.zip). The exercises use its **173-row, 14-column subset for 2023–2024**, in `raw_data/nuseds-fraser-coho-2023-2024.csv`. CSV means comma-separated values, a plain-text table format that spreadsheet software can open. Work with a copy, keeping the source unchanged.

The subset comes from DFO's Fraser and BC Interior NuSEDS workbook. The kit includes its **provenance**—the record of the source and extraction steps—and the [official DFO dictionary](files/fraser-coho-workshop/raw_data/official-nuseds-dictionary.csv). That dictionary was retrieved on 8 September 2026 and may postdate the source workbook.

Here are the first three records, showing our six focus columns. The blank estimate is also blank in the source.

| POP_<wbr>ID | WATERBODY | ANALYSIS_<wbr>YR | SPECIES | NATURAL_<wbr>ADULT_<wbr>SPAWNERS | ESTIMATE_<wbr>METHOD |
| --- | --- | --- | --- | --- | --- |
| 46200 | BONAPARTE RIVER | 2023 | Coho | 758 | Resistivity Counter |
| 44965 | CLAPPERTON CREEK | 2023 | Coho |  | Not Applicable |
| 46190 | COLDWATER RIVER | 2023 | Coho | 7943 | Combined Methods |

We will describe these six fields and review supplied descriptions for the other eight, asking which fish were included and how each method produced its result.

There are **164 distinct population–analysis-year pairs across 173 rows**, so population plus year does not uniquely identify a row. The table also has no CU field. Connecting these population records to CUs would require additional evidence.

The compound column name `NATURAL_ADULT_SPAWNERS` gives us a place to begin. The [entity](glossary.html#entity) is the thing the estimate concerns, such as a defined group of fish. The property is the characteristic being estimated, such as abundance. The full [variable](glossary.html#variable) describes what is being measured, including its scope and context. We will investigate “adult” and “natural”, the year, unit and method, keeping unsupported interpretations as questions.

## Give the next user a better starting point

Someone has to prepare the explanations that make the diagram's shorter route possible. We will do that work together, starting with the estimate `758`:

**Draw the relationships → write the dictionary and separate its meanings → peer review → build the package → assess suggestions → validate and prepare publication.**

[Chapter 2](session-2.html) starts with a drawing of the things the data describes and their relationships. [Chapter 3](session-3.html) turns it into a dictionary and **decomposes** a compound description: separating its entity, property, result, unit, method and other context. A peer reviews whether the drawing and dictionary agree before we use software.

In [Chapters 4–7](session-4.html), we build the package, compare term suggestions and **artificial intelligence (AI)** suggestions against our own descriptions, and prepare a publication preview. The [teaching-record page](reference.html#teaching-record) records the actual status of the example catalog record.

## What you'll take away from the two days

**Day 1: prepare data others can understand and reuse.** The six-hour beginner route takes you to a described package and a publication demonstration on the test server of the **Knowledge Network for Biocomplexity (KNB)**, a data catalog where people can discover and access research datasets.

**Day 2: develop and connect the meanings behind the data.** Over another six hours, we practise reusing existing terms, maintaining a local controlled vocabulary or ontology, and proposing missing concepts for shared use. A **bridge** records how meanings in different resources relate. A **term request** asks the people maintaining a shared resource to review a proposed definition and its evidence.

We will introduce **SKOS (Simple Knowledge Organization System)**, a standard for publishing vocabulary concepts and their relationships, and **OWL (Web Ontology Language)**, a language for expressing formal statements about types of things and how they relate. The [Day 2 guide](advanced.html) explains the exercises; [setup](index.html#download-and-open-the-workshop-kit) identifies their `semantic-lab/` folder in the kit.

Publishing a dataset and publishing a shared term are separate contributions. A reviewed and released term or bridge can be reused by many later packages, so the benefit extends beyond one catalog record.

::::::::::::::::::::::::::::::::::::: challenge

## Activity: Describe what the next user would need

Return to the Fraser Coho table with a partner. Spend 15 minutes, including sharing your example, identifying one question you could answer from the table and one that needs more evidence.

Write three short notes:

- The field or value that raises your question.
- The description, relationship or source evidence that would help someone else interpret it.
- The workshop stage where you expect to prepare or review that information.

Keep these notes for the diagram and dictionary exercises. Consider how publishing a clear explanation now would change the work of someone who finds the data later.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Yukon `mean` and Fraser `SpnForAbd_Total` illustrate why column names alone cannot establish which estimates fit an analysis.
- A shared abundance identifier helps locate candidate fields. Population, year, included fish, method and uncertainty still matter.
- A Salmon Data Package preserves descriptions and evidence; a controlled vocabulary supplies maintained meanings, and an ontology expresses concepts and relationships.
- We draw, describe and peer-review the 173-row, 14-column Fraser Coho dataset before using metasalmon or AI.
- Publishing data and contributing reusable terms or relationships both give later projects a better starting point.

::::::::::::::::::::::::::::::::::::::::::::::::

[yukon-methods]: https://github.com/Pacific-salmon-assess/Yukon-Chinook-CU-reconstructions/blob/3390d4f2a706e1923785aef24e96eba17a7002c0/README.md
[fraser-dictionary]: https://github.com/sos-program/Approved-WSP-Statuses/blob/05643cf7474e2c468e21e30edbf1da0ef9a060a8/OUTPUT/README.md
[abundance-definition]: https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/d45f8f7cc857d92af8bbe54a7c89b2a4a14784b2/ontology/modules/02-observation-measurement.ttl#L27-L33
[nuseds-source]: https://open.canada.ca/data/en/dataset/c48669a3-045b-400d-b730-48aafe8c5ee6
