"""Chapter 10: check selected source-record entailments and SHACL contrasts.

Runs without network access after dependencies are installed. Mutated examples
exist only in memory. Passing is not full OWL DL validation or domain approval.
"""
import argparse
import sys

from pyshacl import validate
from rdflib import Literal
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD

from lab_common import (KIT, LAB, EX, INSTANCE, SMN, prepare, source_trace,
                        load_graph, clone, closure, check_class_concept_collision,
                        require, file_evidence, finish, reference_inspection)


def check(model_path, instances_path, shapes_path, *, reference_only=False):
    report = reference_inspection() if reference_only else prepare()
    rows, trace = source_trace()
    model = load_graph(model_path)
    instances = load_graph(instances_path)
    shapes = load_graph(shapes_path)
    asserted = model + instances
    vocabulary_path = LAB / "vocabulary/estimate-methods.ttl"
    vocabulary = load_graph(vocabulary_path)
    check_class_concept_collision(asserted + vocabulary)
    inferred = closure(asserted)
    check_class_concept_collision(inferred + vocabulary)
    checks = []

    def expect(name, condition):
        require(condition, name)
        checks.append({"check": name, "passed": True})

    for n in (1, 2):
        record = INSTANCE[f"record-{n}"]
        population = INSTANCE[f"population-reference-{rows[n - 1]['POP_ID']}"]
        expect(f"row {n} position and source identity",
               (record, EX.sourceRowNumber, Literal(n)) in instances and
               (record, EX.sourceFile, Literal(trace["source_path"])) in instances and
               (record, EX.concernsPopulationReference, population) in instances and
               (population, EX.sourcePopulationID, Literal(rows[n - 1]["POP_ID"])) in instances and
               (population, EX.sourcePopulationLabel, Literal(rows[n - 1]["POPULATION"])) in instances and
               (record, EX.analysisYear, Literal(rows[n - 1]["ANALYSIS_YR"], datatype=XSD.gYear)) in instances and
               (record, EX.sourceMethodLabel, Literal(rows[n - 1]["ESTIMATE_METHOD"])) in instances)
    expect("reported numeric value remains 758",
           (INSTANCE["result-1"], EX.numericValue, Literal(rows[0]["NATURAL_ADULT_SPAWNERS"], datatype=XSD.decimal)) in instances)
    expect("subclass entails source-record type",
           (INSTANCE["record-1"], RDF.type, EX.SourceRecord) not in asserted and
           (INSTANCE["record-1"], RDF.type, EX.SourceRecord) in inferred)
    expect("range entails result type",
           (INSTANCE["result-1"], RDF.type, EX.RecordedNumericResult) not in asserted and
           (INSTANCE["result-1"], RDF.type, EX.RecordedNumericResult) in inferred)
    untyped = clone(asserted)
    untyped.remove((INSTANCE["record-1"], RDF.type, None))
    expect("domain restores record type when its explicit type is removed",
           (INSTANCE["record-1"], RDF.type, EX.NuSEDSEstimateRecord) in closure(untyped))
    expect("blank estimate creates neither result node nor zero",
           rows[1]["NATURAL_ADULT_SPAWNERS"] == "" and
           not list(inferred.objects(INSTANCE["record-2"], EX.hasReportedResult)))
    expect("reverse subclass is not in the selected closure",
           (EX.SourceRecord, RDFS.subClassOf, EX.NuSEDSEstimateRecord) not in inferred)
    expect("source population reference is not inferred to be a biological population",
           (INSTANCE["population-reference-46200"], RDF.type, SMN.Population) not in inferred)

    def conforms(data):
        result, _, _ = validate(data_graph=data, shacl_graph=shapes,
                                ont_graph=model, inference="rdfs", advanced=False,
                                do_owl_imports=False, js=False)
        return bool(result)

    expect("reference records conform to the local teaching shapes", conforms(instances))
    missing_year = clone(instances)
    missing_year.remove((INSTANCE["record-1"], EX.analysisYear, None))
    expect("removing an explicit year fails the SHACL minCount requirement", not conforms(missing_year))
    expect("OWL still infers the record type without the required explicit year",
           (INSTANCE["record-1"], RDF.type, EX.SourceRecord) in closure(model + missing_year))
    mistaken_edge = clone(instances)
    mistaken_edge.add((INSTANCE["population-reference-46200"], EX.hasReportedResult, INSTANCE["result-1"]))
    expect("a mistaken edge infers an extra record type rather than rejecting the edge",
           (INSTANCE["population-reference-46200"], RDF.type, EX.NuSEDSEstimateRecord) in closure(model + mistaken_edge))
    expect("SHACL detects missing record fields on the mistakenly typed reference", not conforms(mistaken_edge))
    collision = clone(asserted + vocabulary)
    collision.add((EX["area-under-the-curve"], RDF.type, OWL.Class))
    rejected = False
    try:
        check_class_concept_collision(collision)
    except AssertionError:
        rejected = True
    expect("the targeted class/concept collision check rejects a deliberate collision", rejected)
    report.update(status="passed-bounded-teaching-checks", source_sha256=trace["sha256"],
                  source_shape=[173, 14], checks=checks,
                  interpretation="Absence checks concern this selected rule closure. They are not general proofs of non-entailment or proof that missing source facts are false.",
                  files=file_evidence([model_path, instances_path, shapes_path, vocabulary_path]))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=LAB / "model/model.ttl")
    parser.add_argument("--instances", default=LAB / "model/instances.ttl")
    parser.add_argument("--shapes", default=LAB / "model/record-shapes.ttl")
    parser.add_argument("--report", help="Optional new file beneath output/semantic-lab/.")
    args = parser.parse_args()
    try:
        finish(check(args.model, args.instances, args.shapes), args.report)
    except Exception as error:
        print(f"FAILED: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
