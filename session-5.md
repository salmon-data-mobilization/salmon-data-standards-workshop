---
title: 'From Concepts to Semantics — Introducing Simple Knowledge Organization System (SKOS)'
teaching: 75
exercises: 5
---

:::::::::::::::::::::::::::::::::: questions

-   How do we move from lists of terms and definitions to formal, machine-readable vocabularies?
-   What does it mean to give a term a URI and define its relationships to others?
-   How can SKOS help represent our concepts and mappings in a structured, shareable way?
-   How do hierarchical relationships (“broader”, “narrower”, “related”) clarify meaning and enable interoperability?

::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::: objectives

-   Explain the purpose of SKOS in representing controlled vocabularies.
-   Map existing terms and definitions from a data dictionary into basic SKOS structure (Concept, prefLabel, definition, broader, narrower, related).
-   Understand how SKOS differs from an ontology but connects to it (conceptual bridge).
-   Create a simple schema diagram showing relationships among terms, using SKOS-like semantics.

::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::: instructor

Key Takeaways for the Instructor to Reinforce

SKOS is about organizing concepts, not building full ontologies yet.

It’s okay if learners don’t fully “get” RDF — focus on relationships and hierarchy.

Encourage conversation about meaning, consistency, and relationships between concepts.

Diagrams help demystify formal semantics — it’s okay to stay visual!

Facilitator Prompt:

“You’ve all worked on documenting your data terms and even aligning them across datasets. But how do we represent those relationships formally, so others can understand or reuse them — including computers? That’s where SKOS comes in.”

Questions to ask the room:

“What happens if two groups both define ‘condition factor’ slightly differently?”

“How do you think we could show that one term is broader or narrower than another?”

“Why might this matter when sharing data or integrating across studies?”

Instructor Tip:

Keep it conversational — the goal is to surface the problem space that SKOS solves. Don’t introduce jargon yet.

Teaching Flow

1. Define SKOS in plain language:

“SKOS stands for Simple Knowledge Organization System. It’s a way to represent vocabularies — lists of terms and their relationships — in a structured way computers and humans can understand.”

2. Relate it to what they already know:

“You already have terms, definitions, and mappings. SKOS gives those structure — think of it as putting your dictionary into a well-organized tree.”

3. Show an example. 

4. Make the bridge to ontology:

“SKOS is not an ontology — it doesn’t describe processes or logic. But it helps us get there by establishing consistent language.”

Instructor Notes:

If learners seem intimidated, reassure them:
“You don’t need to write code today — we’re just organizing concepts visually.”

Have a slide or printed SKOS term table for reference:
Concept, prefLabel, definition, broader, narrower, related, exactMatch, closeMatch.

:::::::::::::::::::::::::::::::::::::::::

## Introduction

Learners have already identified and documented terms (Modules 1–3), and developed competency questions (Module 4). This module introduces semantic structure: how to move from “terms and mappings” to “concepts and relationships” that can be shared, reused, and machine-readable.

This is the first dip into ontology thinking, using SKOS because it’s lightweight, visual, and flexible.

SKOS (Simple Knowledge Organization System) provides a lightweight, flexible way to express controlled vocabularies and their relationships using the Semantic Web.

| SKOS Term | Meaning | Example (Salmon Context) |
|------------------|-------------------------|-----------------------------|
| skos:Concept | A unique concept or term | “Smolt condition factor” |
| skos:prefLabel | The preferred human-readable label | “Condition factor” |
| skos:definition | Text definition of the concept | “A measure of body condition calculated as weight/length³” |
| skos:broader | More general concept | “Smolt condition factor” broader: “Condition metric” |
| skos:narrower | More specific concept | “Smolt condition factor” narrower: “Fork length condition factor” |
| skos:related | Related but not hierarchical concept | “Condition factor” related to: “Smolt age” |
| skos:exactMatch, skos:closeMatch | Crosswalk to another vocabulary | “Condition factor” exactMatch: <https://vocab.nerc.ac.uk/condition_factor/> |

SKOS helps structure your data terms before you build an ontology — it’s a bridge between documentation and formal reasoning.

:::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: From Data Dictionary to SKOS (25 min)

Purpose: Practice turning natural-language data terms into formal SKOS concepts.

Instructions:

1.  Take 3–5 terms from your data dictionary (Modules 1–3).
2.  For each term, fill in:

-   Preferred label
-   Definition (or short description)
-   Broader / narrower / related concepts (if applicable)
-   Equivalent or similar terms in another dataset or vocabulary

3.  Assign a temporary URI (e.g., <https://example.org/salmon/condition_factor>).

4.  Note which relationships are uncertain or need discussion.

🧠 Tip: You don’t need RDF syntax yet — the goal is concept structure, not code.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::: spoiler

| Concept | PrefLabel | Definition | Broader | Related URI |
|----------------|----------------|----------------|----------------|----------------|
|Smolt condition factor | Condition factor | Weight/length³, used as an indicator of fish health Condition metric | Smolt length | <https://vocab.salmon.org/SmoltConditionFactor> |

:::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Build a Simple Schema Diagram (20 min)

Purpose: Visualize how your SKOS concepts relate to one another.

Instructions:

1. On a whiteboard or digital diagram tool (e.g., MS PowerPoint, Google Slides, MS Paint, paper):

- Draw boxes for each concept.
- Connect them with arrows labeled broader, narrower, or related.

2. Check:

- Is the hierarchy logical (no circular relationships)?
- Are broader/narrower concepts consistent in scope?
- Where could you reuse existing concepts from other vocabularies?

3. Optional: Add color or icons to distinguish reused vs. new concepts.

::::::::::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::: instructor

💬 Reflection (10 min)

Discuss as a group:

- What patterns or redundancies did you notice in your terms?
- Which concepts could be reused from an existing vocabulary?
- How does formalizing these relationships help you answer your Competency Questions from Module 4?

End by connecting this back to Competency Questions (Module 4):

“Your CQs ask big research questions. The SKOS structure helps ensure your vocabulary supports answering those questions consistently.”

:::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::: keypoints

- SKOS helps bridge informal definitions and formal semantics.
- It supports controlled vocabularies that can later evolve into ontologies.
- Creating a schema diagram helps visualize and communicate conceptual structure.
- Reusing terms and clearly defining relationships builds semantic interoperability.

:::::::::::::::::::::::::::::::::::::::::
