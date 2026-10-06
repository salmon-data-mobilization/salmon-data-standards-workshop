---
title: "Build and Test Bridges to Shared Salmon Meanings"
teaching: 30
exercises: 45
---

:::::::::::::::::::::::::::::::::::::: questions

- When should a local term reuse a shared identifier, remain local, or become a proposed shared contribution?
- What does each mapping predicate actually claim, and in which direction?
- How can we test what a bridge implies while preserving the source meaning?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Keep local vocabulary, local OWL model, shared anchors, and bridge assertions in separate files.
- Select mapping predicates by the types and meanings of both endpoints.
- Record evidence, direction, counterexamples, and a human decision for each proposal.
- Test a SKOS mapping and an OWL subclass bridge against real source context.
- Distinguish a mapping's meaning from its serialization or review status.

::::::::::::::::::::::::::::::::::::::::::::::::

## Preserve local meaning while making it discoverable

A collaborator wants to find salmon enumeration information across programs. Our source uses `Area Under the Curve`, `Combined Methods`, `Fixed Site Census`, and other NuSEDS categories. The shared Salmon Domain Ontology contains reusable terms, but a shared label need not capture every local distinction.

A [bridge](glossary.html#bridge) is a set of explicit relationships between those meanings. It can support discovery or integration while the source retains its own labels, definitions, and authority. The first question is not “which shared IRI looks closest?” It is “what claim can these two definitions support?”

Complete the human graph, dictionary, and peer review before this exercise. Use your Chapter 9 vocabulary and Chapter 10 statement decisions. If you disagree with a supplied definition, record that disagreement before comparing mappings. A formatted mapping cannot repair an unsupported local meaning.

## Keep four pieces separate

| Artifact | What it owns in this lab |
| --- | --- |
| `semantic-lab/vocabulary/estimate-methods.ttl` | Local SKOS concepts for four actual method labels. |
| `semantic-lab/model/model.ttl` and `instances.ttl` | Local OWL classes, relationships, and the illustrated source objects. |
| `semantic-lab/bridge/shared-anchors.ttl` | A small, attributed excerpt of existing SDO definitions and types. |
| `semantic-lab/bridge/bridge.ttl` | Two explicit draft relationships between local and shared meanings. |

The bridge does not rename source codes, move local definitions into the shared namespace, or edit the shared ontology. The `example.org` terms remain teaching identifiers. `shared-anchor-sources.json` identifies SDO commit `d45f8f7cc857d92af8bbe54a7c89b2a4a14784b2`, the source modules, and their checksums. The excerpt contains outgoing triples for six selected subjects; it is not the full ontology or its import closure.

This arrangement follows the [SDO conventions](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/d45f8f7cc857d92af8bbe54a7c89b2a4a14784b2/CONVENTIONS.md): retain local or program meanings when shared reuse is uncertain, document bridge provenance, and promote shared terms through stewardship. The [modules and bridges guide](https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/d45f8f7cc857d92af8bbe54a7c89b2a4a14784b2/docs/guides/modules-and-bridges-for-biologists.md) provides the broader workflow. Check a target's current definition and type before applying an example pattern from any guide.

## Read the endpoint types before choosing a predicate

The selected source declarations include:

| Shared IRI | Declared representation | Consequence for this exercise |
| --- | --- | --- |
| `smn:EnumerationMethod` | `skos:Concept` and `sosa:Procedure` | It can be compared with a local method concept; it is not an OWL class. |
| `smn:MethodDocumentation` | `owl:Class` | It can be compared with a class of local documentation items. |
| `smn:EscapementEstimate` | `owl:Class` | Its definition describes a datum tied to a stock and survey event, not a source table row. |
| `smn:Population` | `owl:Class` | It describes a biological grouping, not the information object holding `POP_ID`. |

A SKOS concept can also be an instance of a class such as `sosa:Procedure`. That does not make the concept itself an OWL class. The SDO dual-representation policy uses separate IRIs when class and concept representations are both needed. The lab includes an explicit collision check because legal OWL punning alone does not enforce this editorial policy.

Keep these predicate families distinct:

| Statement | What it claims | What it does not claim |
| --- | --- | --- |
| `localClass rdfs:subClassOf sharedClass` | Every local-class instance is a shared-class instance. | The reverse inclusion. |
| `localClass owl:equivalentClass sharedClass` | The classes have the same members. | That similar labels are sufficient evidence. |
| `individualA owl:sameAs individualB` | The names identify the same individual. | Merely related records, matching labels, or matching numeric identifiers from different systems. |
| `localConcept skos:exactMatch sharedConcept` | Strong interchangeability across a wide range of information-retrieval applications. | OWL individual identity or class equivalence. |
| `localConcept skos:closeMatch sharedConcept` | Sufficient similarity for some information-retrieval applications. | Universal interchangeability. |
| `localConcept skos:broadMatch sharedConcept` | The shared concept is broader than the local concept. | That the same predicate holds in reverse. |
| `localConcept skos:relatedMatch sharedConcept` | An associative relationship between the concepts. | A hierarchy or permission to replace one with the other. |

OWL class equivalence concerns class membership; `owl:sameAs` concerns individuals. [OWL semantics](https://www.w3.org/TR/owl2-direct-semantics/). SKOS exact/close mappings have information-retrieval meanings; they do not entail those OWL equivalences. `broadMatch` reverses to `narrowMatch`, while `relatedMatch`, `closeMatch`, and `exactMatch` are symmetric. [SKOS mapping properties](https://www.w3.org/TR/skos-reference/#mapping).

Choosing a weaker predicate is not a substitute for evidence. If you cannot explain why two concepts are related, defer the mapping. Similarly, `closeMatch` means scoped retrieval similarity; it is not a generic spelling for “we are unsure.”

## Work through an actual method example

Find data row **5** in the unchanged source: Gates River (Lillooet) Coho, `POP_ID` `47213`, analysis year `2023`, reported value `3032`, method `Area Under the Curve`, classification `RELATIVE ABUNDANCE (TYPE-3)`.

The official dictionary describes AUC as combining abundance point estimates using the area under an abundance-time curve and a survey-life assumption. The shared `EnumerationMethod` definition concerns enumerating or counting salmon in the field. These descriptions support a relationship worth reviewing, but they do not establish interchangeable procedures or comparable numerical results.

The supplied **draft** proposes:

```turtle
ex:area-under-the-curve skos:relatedMatch smn:EnumerationMethod .
```

Its counterexample is concrete: an annual estimate calculated from a time series and survey-life assumption is not simply a direct field count. Replacing `Area Under the Curve` with `Enumeration method` would remove information a reader needs to interpret row 5. A discovery interface may show this record under a reviewed “related methods” expansion while still displaying the original method and classification. Whether its value can be combined with other estimates still depends on the methods and coverage of those estimates.

Compare data row **39**, Dunn Creek (Clearwater) Coho, which stores `Fixed Site Census`. The official source describes combining raw observations into an estimate. The label alone might make you imagine a single direct field census. Use that tension to test your proposed category boundaries, not to infer undocumented equivalence between the two local methods.

`mapping-decisions-working.csv` records six proposals and alternatives. B01 is the draft related link above; B02 rejects an exact link between the same endpoints. B05 defers a Resistivity Counter mapping because the current dictionary lacks an operational definition. A rejected or deferred row stays in the decision record without becoming a mapping triple.

## Work through a bridge between record classes

Chapter 10 includes a documentation item, `method-description-auc`, representing the captured NuSEDS explanation of the AUC method. It is an instance of local class `NuSEDSMethodDescription`. This is distinct from the method concept and from an actual execution of that method.

The local class is scoped to documentation that explains how a NuSEDS estimate method works. The shared `MethodDocumentation` class covers documented method descriptions linked to the production of a salmon metric or estimate. The second draft bridge therefore proposes:

```turtle
ex:NuSEDSMethodDescription rdfs:subClassOf smn:MethodDocumentation .
```

With this bridge loaded, the local documentation item receives the shared documentation type. That is useful for a query seeking method documentation across programs. It does not make every shared method document a NuSEDS document. Documentation from another program provides a possible counterexample to the reverse inclusion. The supplied model does not assert `owl:equivalentClass`.

By contrast, B03 rejects equating the local source-record class with `smn:EscapementEstimate`: the record and datum are different objects, and some records have no numeric result. B04 rejects making a population **reference** a subclass of biological `smn:Population`. Both mistakes can look plausible in a table of labels. Reading the endpoint definitions exposes the category mismatch.

## Make the decision record carry the reasoning

Use `semantic-lab/worksheets/bridge-decisions.csv`. It starts with candidate statements and source questions; human decision, reason, reviewer, and date fields are blank. For each mapping you review, record:

1. The exact subject, predicate, and object, including direction.
2. The meaning and representation type of both endpoints.
3. The source definition and an actual record showing the local use.
4. A counterexample, boundary case, or unresolved question.
5. Your disposition, intended use, reason, reviewer, and date.

Keep local definitions and source labels intact. Retain one proposed predicate per pair in the assertion file; keep rejected alternatives in the table. If a future review strengthens a mapping, record the change and recheck its consequences rather than leaving contradictory alternatives active together.

**A draft annotation does not switch off a triple.** Loading `bridge.ttl` asserts its two mapping statements. Its review annotations tell a person how to treat the file; a reasoner still uses the logical assertions. The workshop therefore loads it only into the isolated exercise. Passing the check does not approve its use in production integration.

[SSSOM](glossary.html#sssom) is a format for sharing mappings and their metadata. It carries a mapping predicate; it does not choose the predicate's semantics or make an uncertain relationship exact. To export the lab's decision worksheet as SSSOM, use the required format fields, preserve the predicate, provenance and review decision, and validate against the chosen SSSOM version. [SSSOM documentation](https://mapping-commons.github.io/sssom/dev/).

## Test the bridge, then inspect what the test leaves open

With the semantic-lab environment active, run from the workshop project root:

```bash
python semantic-lab/scripts/check_bridge.py --report output/semantic-lab/bridge-check-01.json
```

The script requires the completed human preparation record. It loads the local model, instances, vocabulary, shared-anchor excerpt, draft bridge, and a small excerpt of the W3C SKOS rules. It reads no remote ontology and makes no API call. The limited SKOS rule file is named in the report; importing a namespace name alone would not supply its inference rules.

The expected report contains ten named checks. Inspect at least these:

- The AUC example still matches actual row 5.
- The related mapping yields the reverse related mapping, but no identity between the two concepts.
- The local documentation item gains `smn:MethodDocumentation` type.
- The reverse subclass and class equivalence are absent from the selected closure.
- A **counterfactual in-memory** `broadMatch` produces an inverse `narrowMatch`, not a reverse `broadMatch`. This demonstrates direction without promoting the unsupported stronger mapping into the saved bridge.
- Adding an exact mapping alongside the related mapping fails the lab's per-pair policy.

The supplied checks test these particular examples and their stated expectations. They do not prove that every possible bridge is sound, run a full OWL DL classifier, or establish scientific agreement. If an edited proposal changes an expected outcome, a failing check is a prompt to inspect the new claim and revise its documented test deliberately.

## Decide whether to reuse, keep local, or request a shared term

| Finding after review | Next action |
| --- | --- |
| A shared term already captures the intended meaning and type | Reuse it directly where the application supports that role. |
| A useful local distinction needs to survive | Keep the local identifier and definition; propose a bridge with evidence and a stated use. |
| A policy-neutral concept has credible use across organizations | Prepare a shared-term request, including the local examples and reuse case. |
| The meaning or source authority remains unclear | Ask for clarification and defer the assertion. |

Building a governed vocabulary also requires named stewards, a review process, versioning, stable publication, and maintenance. A successful reasoner run does not create those arrangements. Chapter 12 turns a justified unresolved need into a reviewable request rather than automatically minting a shared identifier.

::::::::::::::::::::::::::::::::::::: challenge

## Activity: defend one bridge and one withheld mapping

Work in pairs for 45 minutes:

1. **Compare endpoints, 10 minutes.** Choose B01 or B06. Read both definitions and types in the local files; trace the source context. Explain why the proposed predicate is a SKOS relationship or an OWL class relationship.
2. **Record your decision, 10 minutes.** Complete the human fields for that proposal and one rejected or deferred alternative. Include a counterexample and the intended use. You may disagree with the supplied draft; record the specific change required.
3. **Test a separate copy, 10 minutes.** Copy `semantic-lab/bridge/bridge.ttl` to a new `output/semantic-lab/bridge.ttl`. Run `python semantic-lab/scripts/check_bridge.py --bridge output/semantic-lab/bridge.ttl --report output/semantic-lab/bridge-check-02.json`, choosing an unused report name. Inspect the reverse mapping, subclass inference, and counterfactual direction checks. Preserve the reference files.
4. **Peer challenge and handoff, 15 minutes.** Ask another pair what information would be lost by canonicalizing the source through your bridge. Revise your rationale or defer the mapping. Prepare either a local stewardship action or the evidence needed for a shared-term request.

Your output is a small bridge file, a completed decision table, and a test report whose scope you can explain. The full source table and original method labels remain intact.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Local meanings, shared anchors, and bridge assertions have separate responsibilities.
- Predicate direction and endpoint type are part of the mapping claim.
- SKOS similarity is different from OWL class equivalence or individual identity.
- Counterexamples help distinguish a useful bridge from a destructive replacement.
- Draft statements still have effects when loaded; a test result and a stewardship decision remain separate.

::::::::::::::::::::::::::::::::::::::::::::::::
