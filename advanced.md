---
title: "Day 2: Build and Connect Vocabularies and Ontologies"
---

Day 2 is **Part 2 of the workshop: six hours of teaching and activities**, excluding breaks. It follows the six-hour beginner route to publication in Chapters 1–7. Five chapters use the same **173-row, 14-column Fraser Coho NuSEDS dataset** to develop vocabulary, ontology, bridge and contribution drafts.

## Bring the human model forward

Start with your dataset graph, interpretation dictionary, measurement decomposition, and peer review from Day 1. Keep the questions that remain unresolved. Returning participants can prepare by completing the diagram, dictionary and peer-review activities in Chapters 2–3 using this same source.

The activities use local files and can be completed offline with the supplied source material and RDF tools from Setup.

## The six-hour route

| Chapter | Question | Artifact | Minutes |
| --- | --- | --- | ---: |
| [8. Choose the right route](session-8.html) | Reuse, describe locally, model, or request a shared term? | Evidence-backed routing decisions | 60 |
| [9. Build a controlled vocabulary](session-9.html) | How do source codes become maintained concepts? | Draft SKOS scheme and stewardship record | 75 |
| [10. Formalize the graph](session-10.html) | What does a logical statement commit us to? | Small RDF/OWL model, real-row examples, and checks | 90 |
| [11. Build bridges](session-11.html) | Which local and shared meanings can be connected? | Separate mappings, rationale, and consequence checks | 75 |
| [12. Prepare contributions](session-12.html) | What should maintainers review, and what happens next? | Term-request or clarification draft and review plan | 60 |
| | | **Total** | **360** |

The [semantic lab guide](files/fraser-coho-workshop/semantic-lab/README.html) lists the files and commands. Use a plain-text editor for Turtle (`.ttl`), or work in the worksheets with a partner who runs the checks. A specialist ontology editor is optional. [Setup](setup.html) describes the small additional Python environment for the offline checks.

## What the artifacts mean

The teaching namespace `https://example.org/fraser-coho-workshop/terms/` identifies **draft classroom terms**. It is not an organization-owned production namespace and does not resolve to maintained term pages. Source codes remain unchanged. Learners do not mint official `smn:` or `gcdfo:` terms, alter their definitions, or publish an organization's vocabulary during the class.

The [Salmon Domain Ontology conventions][sdo-conventions] govern its modelling choices. The [metamodel view](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/main/ontology/views/README.md) is a non-normative teaching aid. [SKOS](glossary.html#skos), [OWL](glossary.html#owl), and [SHACL](glossary.html#shacl) serve different purposes: concept schemes, logical assertions, and checks on a supplied graph. You will pair these technical checks with source review and a plan for maintaining the meanings.

## Review and future practice

By the end, another group should be able to trace a source value to its description, local concept, proposed mapping, and unresolved decision. They should also be able to explain one claim the graph supports and one it does not establish. Use the [reference page](reference.html#teaching-record) to check the supplied examples' current review status.

Future practice can extend the small model, check its complete OWL DL import closure, arrange vocabulary hosting and persistent identifiers, and test integration with operational systems. The chapters identify the evidence and stewardship decisions each step needs.
