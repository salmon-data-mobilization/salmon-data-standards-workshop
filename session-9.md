---
title: "Build and Steward a Small SKOS Vocabulary"
teaching: 30
exercises: 45
---

:::::::::::::::::::::::::::::::::::::: questions

- What turns a list of source labels into a reviewable vocabulary?
- How can we represent a category whose definition is missing?
- What must be decided before a teaching vocabulary becomes a maintained resource?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Write four concept records grounded in observed Fraser Coho method values.
- Build a small Turtle file containing a SKOS concept scheme and its concepts.
- Preserve a definition gap without inventing a method description or synonym.
- Record stewardship, versioning, review and release questions separately from technical checks.

::::::::::::::::::::::::::::::::::::::::::::::::

## Build from source meanings, not labels alone

Chapter 8 selected a local/profile teaching draft for a small set of estimate-method categories. Continue with your human dictionary and the same 173-row, 14-column source. The four values below all occur in `ESTIMATE_METHOD`; they are a **selection from its nine values**, not a complete NuSEDS method vocabulary.

| Exact stored value | Source evidence available | What remains open |
| --- | --- | --- |
| `Area Under the Curve` | Abundance over time is integrated and divided by survey life to estimate annual abundance | Which observations, survey-life assumption and coverage apply to a particular record? |
| `Combined Methods` | A final estimate combines two or more estimate methods after estimates are calculated from multiple survey methods | Which methods and combination rule apply? |
| `Fixed Site Census` | Raw observations are combined into one estimate; the source gives daily fence observations combined into an annual estimate as an example | What site, period and combination rule apply? |
| `Resistivity Counter` | The code exists, but its official dictionary entry is `N/A` | Which counter observations and estimation procedure generated the result? |

These are paraphrases of the kit's `raw_data/official-nuseds-dictionary.csv`, retrieved on **8 September 2026**. Its wording may postdate the 2025 source workbook. Consult the preserved file and [code evidence table](files/fraser-coho-workshop/reference/code-definitions-working.csv), including their questions and retrieval caveat. A broader method reference may help later, but its existence does not prove that a particular procedure produced these records.

## Give each concept a record

Open [vocabulary-concepts.csv](files/fraser-coho-workshop/semantic-lab/worksheets/vocabulary-concepts.csv). It supplies the exact source values, teaching IRIs and source references; write the definition, definition status, scope and remaining question. The source key is the pair `source_column` + `code_value`. The IRI identifies your local concept, while the preferred label is its human-readable name.

| Record field | What to establish |
| --- | --- |
| `concept_iri`, `scheme_iri` | Which concept is described and which scheme includes it |
| `source_column`, `code_value` | The exact source binding; never silently recode the CSV |
| `pref_label`, `language` | The label used in this scheme and its language |
| `definition`, `definition_status` | A sourced description, or an explicitly recorded absence |
| `scope_note`, `open_question` | Limits of applicability and evidence still needed |
| `source_reference`, source date and caveat | Where the wording came from and its temporal limits |
| `broader_iri`, `alternative_label` | Relationships or synonyms only when evidence supports them |
| `steward`, `status` | The actual responsible person if agreed, and the real review state |

For `Resistivity Counter`, leave the operational definition empty and explain why in `definition_status` and `open_question`. Do not use the word `N/A` as though it defined the procedure. A known source category can be documented as an incomplete draft while its meaning remains unresolved.

`Combined Methods` is not automatically a broader concept than every method that might be combined. The source also does not establish that `Fence` is a synonym of `Fixed Site Census`. The worked vocabulary leaves these relationships open for investigation.

## Read and write a small SKOS file

The [W3C SKOS Primer](https://www.w3.org/TR/2009/NOTE-skos-primer-20090818/) describes concepts with identifiers, labels, documentation and scheme membership. Turtle is a text syntax for recording RDF statements. In the example below, `a` states a type, semicolons continue statements about the same subject, and a period ends them. `@en` identifies English text.

```turtle
@prefix ex: <https://example.org/fraser-coho-workshop/terms/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

ex:estimate-method-scheme a skos:ConceptScheme ;
    skos:prefLabel "Fraser Coho workshop estimate-method selection"@en .

ex:combined-methods a skos:Concept ;
    skos:inScheme ex:estimate-method-scheme ;
    skos:prefLabel "Combined Methods"@en ;
    skos:definition "An estimate method in which separate estimates are calculated from multiple survey methods and the final estimate combines two or more estimate methods."@en .
```

This short excerpt illustrates the structure. The supplied [estimate-methods.ttl](files/fraser-coho-workshop/semantic-lab/vocabulary/estimate-methods.ttl) additionally records source links, scope, questions and draft status. Read those statements as part of each concept; they are not optional background to the definition.

Create `output/semantic-lab/` and save your own edited file there as `estimate-methods.ttl`. Keep the reference unchanged. Use its prefix and scheme declarations, then build the four concept blocks from your completed worksheet. Each supported definition becomes `skos:definition`; scope belongs in `skos:scopeNote`, the outstanding question and draft state in `skos:editorialNote`, and the source in `dcterms:source`. Omit a `skos:definition` statement for the unresolved counter method rather than copying a guess into it.

All new subject IRIs are in the teaching namespace `https://example.org/fraser-coho-workshop/terms/`. Keeping local identifiers separate from existing shared identifiers makes it clear which resource defines each concept. The complete source and convention pins are in [provenance.json](files/fraser-coho-workshop/semantic-lab/vocabulary/provenance.json).

## Check the artifact and its limits

A syntax check determines whether Turtle can be read. A vocabulary check examines selected expectations such as concept types, labels and scheme membership. A domain reviewer assesses whether the definitions accurately describe the methods.

After preparing the Day 2 Python environment in Setup, run the same small utility from any software lane. Start in the extracted workshop-kit root:

```sh
python semantic-lab/vocabulary/check_vocabulary.py
```

It checks your copied Turtle against `semantic-lab/worksheets/vocabulary-concepts.csv` and the unchanged source, after checking the existing Day 1 human-preparation record. It reads local files without fetching vocabulary URLs or imports. A collaborator can run it for a spreadsheet participant. Chapter 10 checks the formal model separately, and Chapter 12 assembles the review handoff.

Use this human checklist alongside that bounded check:

- One resource is the scheme; four distinct resources are concepts in it.
- The four preferred labels match the exact source values and have language `en`.
- There is one preferred label per language on each concept, and no identical literal used as both preferred and alternative label.
- Three concepts have source-backed definitions; the counter concept explicitly records its missing operational definition.
- Every concept retains evidence, scope and a pending-review note; no concept IRI is also declared an OWL class.
- Each proposed hierarchy or cross-vocabulary relationship has supporting evidence.

The label and scheme distinctions follow the [SKOS Reference](https://www.w3.org/TR/2009/REC-skos-reference-20090818/). Our exact four-concept inventory is a workshop check. SKOS scheme membership alone does not impose a closed list of permitted values on the source column; the dataset's schema and code inventory do that job.

## Steward the meaning as well as the file

Complete `semantic-lab/worksheets/stewardship.md`. Propose who would maintain the vocabulary, who would use it, and how identifiers, evidence review, versioning, corrections and release would work. Record which responsibilities still need agreement with the proposed owner.

In the draft, distinguish a wording correction from a changed meaning. Record the former in a change log; a substantive change may need a new concept and an explicit replacement decision so old data can still be interpreted. Preserve versions and review evidence. Before publication, the responsible steward must decide the production namespace, adoption scope, hosting and maintenance. These example.org IRIs remain teaching identifiers.

The [pinned SDO conventions](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/d45f8f7cc857d92af8bbe54a7c89b2a4a14784b2/CONVENTIONS.md) keep estimate-method schemes in the profile layer and require distinct IRIs for SKOS concepts and OWL classes. Chapter 10 creates the formal model; Chapter 11 reviews bridges without collapsing local definitions into shared ones.

::::::::::::::::::::::::::::::::::::: challenge

## Activity: create a vocabulary and its stewardship record

1. **Write for 15 minutes.** Complete all four concept records against the source. Keep the missing definition and unsupported relationships as open questions.
2. **Build for 15 minutes.** Create your own Turtle file from those records. Work in pairs if a text editor is unfamiliar. Trace each statement back to a worksheet cell or cited source.
3. **Review for 10 minutes.** Exchange the worksheet and Turtle file. Use the checklist above to find missing source links, changed source values, unsupported hierarchy or lost questions. Record only the review that actually occurred.
4. **Plan for 5 minutes.** Complete the stewardship form's proposed roles, release conditions and one change scenario. Keep names or decisions blank where no agreement exists.

:::::::::::::::::::::::: solution

## Worked output and answer criteria

Compare [concepts-working.csv](files/fraser-coho-workshop/semantic-lab/vocabulary/concepts-working.csv) and [estimate-methods.ttl](files/fraser-coho-workshop/semantic-lab/vocabulary/estimate-methods.ttl) with your output. Trace their definitions and questions to the cited evidence. Use `semantic-lab/vocabulary/stewardship-working.md` to compare the proposed responsibilities and decisions still needed for release.

Success means another person can recover all four exact source bindings, distinguish three supported paraphrases from one definition gap, and identify what must happen before adoption. Documenting the gap gives a future reviewer a concrete question to resolve.

::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- A vocabulary connects concept identity, source meaning, evidence and stewardship.
- Preserve exact code values separately from the concepts that explain them.
- Missing definitions and unsupported relationships remain visible.
- SKOS scheme membership does not replace a data schema's allowed-value checks.
- A technical pass, peer review and authorization to publish are distinct outcomes.

::::::::::::::::::::::::::::::::::::::::::::::::
