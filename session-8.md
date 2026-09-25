---
title: "Choose What to Reuse, Define Locally, or Propose Together"
teaching: 30
exercises: 30
---

:::::::::::::::::::::::::::::::::::::: questions

- Does this problem need a shared term, a local definition, a data check, or a source question?
- When should a meaning be represented with SKOS or OWL?
- What evidence would justify a contribution to the Salmon Domain Ontology?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Separate the source of a definition from the scope of its meaning and its steward.
- Choose a representation for seven questions from the Fraser Coho dataset.
- Document reuse, local/profile and shared-contribution decisions without inventing missing meanings.
- Explain why a source code, a SKOS concept and an OWL class have different roles.

::::::::::::::::::::::::::::::::::::::::::::::::

## Start with the human work already completed

Day 1 followed all **173 rows and 14 columns** of the Fraser Coho NuSEDS slice through interpretation, packaging and review. Day 2 develops small vocabulary, model and bridge artifacts from those same records. Keep the completed graph, dictionary, decomposition and actual peer-review record beside you. A supplied example does not replace that baseline.

Open `semantic-lab/worksheets/routing-decisions.csv` in the extracted kit. Its seven cases refer to real source fields or to components of your existing graph. You will choose an action and record why. The raw data, dataset ID `fraser-coho-workshop` and table ID `escapement` remain unchanged.

The purpose of a new term is to solve a demonstrated communication or integration problem. Finding a plausible name is only the beginning. A missing definition, a failed lookup and a missing ontology concept are different findings.

## Ask five questions before choosing a home

1. **What is the intended use?** Explain a stored category, annotate a measurement, express a relationship, or check data values?
2. **What does the source establish?** Compare the actual rows, dictionary and method documentation. Separate a definition from an inference.
3. **What already exists?** Check a candidate's definition, type and scope before proposing another identifier. Keep the search source and version.
4. **How broadly does the meaning hold?** A DFO document can describe a broadly shared scientific concept; its publisher alone does not decide the concept's home.
5. **Who can maintain and approve it?** A team can prepare a draft while the appropriate scientific or vocabulary steward retains the adoption decision.

The [Salmon Domain Ontology conventions at the inspected commit](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/d45f8f7cc857d92af8bbe54a7c89b2a4a14784b2/CONVENTIONS.md) distinguish shared OWL, a small shared SKOS layer, organization/profile resources and separate bridges. Their default is local/profile when reuse is uncertain; shared promotion needs stable, policy-neutral meaning and cross-organization reuse. A local resource can still be carefully governed and machine-readable.

## Choose the representation that answers the question

| Need | Representation | Fraser Coho example |
| --- | --- | --- |
| Explain categories with labels, definitions and scope | [SKOS](glossary.html#controlled-vocabulary) concepts in a scheme | The `ESTIMATE_METHOD` category `Area Under the Curve` |
| State formal relationships among types of things or describe individuals using those types | An [OWL](glossary.html#ontology) model with RDF assertions | Separate an estimation activity, its reported result and the population it concerns |
| Check the form or completeness of stored data | A schema or explicit data check | Date representation; whether a proposed population/year key is unique |
| Resolve insufficient or conflicting evidence | A source question with a next step | Whether “natural” establishes a natural-origin restriction |
| Express a complete measurement variable | A local/profile variable description with decomposed components | Adult-spawner estimate, abundance property, unit, qualifiers and row context |

SKOS organizes concepts and their documentation; OWL supports formal classes, properties and logical statements. Neither a vocabulary label nor an OWL axiom makes a table pass a completeness check. These tools can work together, but the choice starts with the intended use. See the [W3C SKOS Primer](https://www.w3.org/TR/2009/NOTE-skos-primer-20090818/) and [OWL 2 overview](https://www.w3.org/TR/2012/REC-owl2-overview-20121211/).

Consider three distinct things:

- `Area Under the Curve` in a CSV cell is a **stored string**.
- A workshop SKOS concept documents the **meaning of that category** with its own identifier.
- An OWL class describes a **type of thing** in a formal model. An individual activity may be described using a class and linked to a procedure.

Do not turn each code into an OWL class merely because it has an IRI. Under the SDO conventions, a SKOS concept and an OWL class use separate IRIs. A method concept may also be typed as an *instance* of `sosa:Procedure` when supported; that is different from declaring the same IRI an `owl:Class`. Chapters 9–10 make the distinction concrete.

## Choose the scope and the next action

| Finding | Action now | Evidence that could change the decision |
| --- | --- | --- |
| An existing term fits the supported meaning | Reuse it and retain the local source binding | A mismatch in definition, inclusions, grain or use |
| A local category has a source-backed definition | Document it in a local/profile draft; check maintained resources before production reuse | Demonstrated equivalent meaning and use by other organizations |
| A stable concept is missing and multiple organizations need it | Prepare a shared-term proposal with examples and a search record | Steward review confirms scope, representation and duplication checks |
| Meaning depends on a program or operational rule | Keep that scope explicit and route to the appropriate program/profile steward | Evidence that the meaning is policy-neutral and shared |
| The source does not establish the meaning | Ask a source question and keep the uncertainty visible | A dated definition or method source answers it |

For this dataset, the abundance property already has the shared anchor `https://w3id.org/smn/Abundance`. The [pinned definition](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/d45f8f7cc857d92af8bbe54a7c89b2a4a14784b2/ontology/modules/02-observation-measurement.ttl) concerns a reusable characteristic. The complete adult-spawner variable still needs its population, qualifiers, units and method context before you can assess whether estimates are comparable.

The current SDO conventions keep estimate-method and estimate-type schemes in the profile layer. Chapter 9 therefore builds a **teaching draft of selected source categories**, without claiming that NuSEDS needs a new official vocabulary. All newly introduced example identifiers begin `https://example.org/fraser-coho-workshop/terms/`. They identify classroom artifacts, not production resources or resolving vocabulary pages. No labels or definitions are added to terms owned by another namespace.

## Worked route: a repeated population/year pair

The source has 173 records and 164 distinct `POP_ID`–`ANALYSIS_YR` pairs. A proposal that those two fields uniquely identify a record fails against this slice. The immediate outputs are a failed key check and a question about record identity. Creating a class called “unique population-year” would not resolve the data question.

Record the intended use, observed evidence, rejected uniqueness claim and next source question. Keep every original row. A source question is a complete routing decision when the missing evidence is identified.

::::::::::::::::::::::::::::::::::::: challenge

## Activity: route seven real questions

1. **Decide for 15 minutes.** Complete the seven rows in the [routing worksheet](files/fraser-coho-workshop/semantic-lab/worksheets/routing-decisions.csv). Work through abundance, an AUC method category, `NO SURVEY THIS YEAR`, the proposed key, natural origin, date representation and activity/result relationships. Specify the representation separately from the local/shared route.
2. **Challenge for 10 minutes.** Exchange decisions. For one apparent shared-term proposal, ask whether an existing term, better source definition or data check would solve the problem. For one local decision, name the evidence that would warrant wider reuse. No new shared term needs to be proposed if none is justified.
3. **Record for 5 minutes.** Save reasons, sources and next actions. Record only a reviewer's actual participation; leave unperformed review fields blank. Carry the method-category decision into Chapter 9.

:::::::::::::::::::::::: solution

## What a defensible result contains

Compare your proposed routes and reasons with the [worked routing decisions](files/fraser-coho-workshop/semantic-lab/vocabulary/routing-decisions-working.csv) after your attempt.

- Abundance can reuse an existing shared characteristic while the full compound variable remains separately described.
- Method categories and the `NO SURVEY THIS YEAR` classification need different schemes and scope. The classification is not a procedure.
- The proposed key and date representation belong in data checks; uncertainty about source grain or missing dates remains a source question.
- The unsupported natural-origin interpretation remains open.
- Activity/result relationships belong in a model whose assertions are justified by evidence.

An acceptable answer identifies what would change its recommendation. Neither the frequency of a label nor the organization that published it proves that its meaning should enter the shared core.

::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Separate intended use, evidence, representation, semantic scope and stewardship.
- Reuse a fitting term before proposing a new one.
- A code string, a SKOS concept and an OWL class have different roles.
- Schemas check data shape; source questions address missing evidence.
- Local/profile drafting preserves meaning while shared adoption remains a steward decision.

::::::::::::::::::::::::::::::::::::::::::::::::
