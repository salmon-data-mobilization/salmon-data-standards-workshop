"""Chapter 11: inspect the draft bridge and selected inference consequences.

No remote ontology imports, API requests, source edits or publication actions.
The broadMatch counterfactual runs in memory, not in the saved bridge.
"""
import argparse
import hashlib
import json
import sys

from rdflib import URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS

from lab_common import (LAB, EX, INSTANCE, SMN, prepare, source_trace,
                        read_rows, load_graph, clone, closure,
                        check_class_concept_collision, require, file_evidence, finish,
                        reference_inspection)

MAPPING_PREDICATES = {RDFS.subClassOf, OWL.equivalentClass, OWL.sameAs,
                      SKOS.exactMatch, SKOS.closeMatch, SKOS.relatedMatch,
                      SKOS.broadMatch, SKOS.narrowMatch}


def bridge_pairs(graph):
    return {(s, p, o) for s, p, o in graph if p in MAPPING_PREDICATES
            and str(s).startswith(str(EX)) and str(o).startswith(str(SMN))}


def policy(graph):
    check_class_concept_collision(graph)
    pairs = {}
    for subject, predicate, obj in bridge_pairs(graph):
        key = (subject, obj)
        pairs.setdefault(key, set()).add(predicate)
        if predicate in {RDFS.subClassOf, OWL.equivalentClass}:
            require((subject, RDF.type, OWL.Class) in graph and (obj, RDF.type, OWL.Class) in graph,
                    "Class mapping needs two declared OWL classes.")
        elif predicate == OWL.sameAs:
            raise AssertionError("No individual identity bridge is supported in this teaching record.")
        else:
            require((subject, RDF.type, SKOS.Concept) in graph and (obj, RDF.type, SKOS.Concept) in graph,
                    "This lab's SKOS mappings must connect declared concepts, not class IRIs.")
    require(all(len(predicates) == 1 for predicates in pairs.values()),
            "Retain one proposed mapping predicate per pair in the draft assertion file; put rejected alternatives in the decision table.")


def check(bridge_path, *, reference_only=False):
    report = reference_inspection() if reference_only else prepare()
    rows, trace = source_trace()
    anchor_path = LAB / "bridge/shared-anchors.ttl"
    anchor_sources = json.loads((LAB / "bridge/shared-anchor-sources.json").read_text())
    require(hashlib.sha256(anchor_path.read_bytes()).hexdigest() == anchor_sources["excerpt_sha256"], "Shared-anchor excerpt changed without its provenance record.")
    paths = [LAB / "model/model.ttl", LAB / "model/instances.ttl",
             LAB / "vocabulary/estimate-methods.ttl", anchor_path,
             LAB / "bridge/skos-rules-excerpt.ttl", bridge_path]
    graph = load_graph(*paths)
    bridge = load_graph(bridge_path)
    policy(graph)
    decisions = read_rows(LAB / "bridge/mapping-decisions-working.csv")
    expected = {(URIRef(r["subject_id"]), URIRef(r["predicate_id"]), URIRef(r["object_id"]))
                for r in decisions if r["asserted_in_draft_bridge"] == "true"}
    require(bridge_pairs(bridge) == expected, "Draft assertions differ from the supplied proposal table; inspect the changed mapping and revise the documented test expectations deliberately.")
    checks = []

    def expect(name, condition):
        require(condition, name)
        checks.append({"check": name, "passed": True})

    expect("AUC mapping example traces to actual row 5",
           rows[4]["POP_ID"] == "47213" and rows[4]["ESTIMATE_METHOD"] == "Area Under the Curve" and
           rows[4]["NATURAL_ADULT_SPAWNERS"] == "3032")
    expect("shared enumeration anchor is a concept, not an OWL class",
           (SMN.EnumerationMethod, RDF.type, SKOS.Concept) in graph and
           (SMN.EnumerationMethod, RDF.type, OWL.Class) not in graph)
    expect("shared documentation anchor is an OWL class",
           (SMN.MethodDocumentation, RDF.type, OWL.Class) in graph)
    expanded = closure(graph)
    check_class_concept_collision(expanded)
    expect("relatedMatch has a reverse relatedMatch",
           (SMN.EnumerationMethod, SKOS.relatedMatch, EX["area-under-the-curve"]) in expanded)
    expect("relatedMatch does not create sameAs between the two concepts",
           (EX["area-under-the-curve"], OWL.sameAs, SMN.EnumerationMethod) not in expanded)
    expect("local method document gains the shared documentation class",
           (INSTANCE["method-description-auc"], RDF.type, SMN.MethodDocumentation) in expanded)
    expect("reverse subclass and equivalentClass are absent from the selected closure",
           (SMN.MethodDocumentation, RDFS.subClassOf, EX.NuSEDSMethodDescription) not in expanded and
           (EX.NuSEDSMethodDescription, OWL.equivalentClass, SMN.MethodDocumentation) not in expanded)
    expect("record/result and population-reference/organism conflations remain absent",
           (EX.NuSEDSEstimateRecord, OWL.equivalentClass, SMN.EscapementEstimate) not in expanded and
           (INSTANCE["population-reference-46200"], RDF.type, SMN.Population) not in expanded)

    # A hypothesis about direction only, not an endorsed stronger method mapping.
    hypothetical = clone(graph)
    hypothetical.remove((EX["area-under-the-curve"], SKOS.relatedMatch, SMN.EnumerationMethod))
    hypothetical.add((EX["area-under-the-curve"], SKOS.broadMatch, SMN.EnumerationMethod))
    imagined = closure(hypothetical)
    expect("counterfactual broadMatch yields inverse narrowMatch, not reverse broadMatch",
           (SMN.EnumerationMethod, SKOS.narrowMatch, EX["area-under-the-curve"]) in imagined and
           (SMN.EnumerationMethod, SKOS.broadMatch, EX["area-under-the-curve"]) not in imagined)
    conflicting = clone(graph)
    conflicting.add((EX["area-under-the-curve"], SKOS.exactMatch, SMN.EnumerationMethod))
    rejected = False
    try:
        policy(conflicting)
    except AssertionError:
        rejected = True
    expect("adding an unreviewed stronger alternative fails the per-pair policy", rejected)
    report.update(status="passed-bounded-teaching-checks", source_sha256=trace["sha256"],
                  source_shape=[173, 14], shared_anchor_commit=anchor_sources["commit"],
                  asserted_mapping_count=len(expected), human_mapping_approval="not established",
                  checks=checks, files=file_evidence(paths),
                  interpretation="Selected rule consequences and policy checks only. The draft triples take effect when loaded; their annotations do not disable reasoning. No full DL classification or SSSOM validation was run.")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bridge", default=LAB / "bridge/bridge.ttl")
    parser.add_argument("--report", help="Optional new file beneath output/semantic-lab/.")
    args = parser.parse_args()
    try:
        finish(check(args.bridge), args.report)
    except Exception as error:
        print(f"FAILED: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
