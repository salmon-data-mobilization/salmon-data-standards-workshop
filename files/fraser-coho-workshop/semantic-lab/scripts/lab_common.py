"""Local-only teaching utilities, not MetaSalmon APIs or scientific validators."""
import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys

from rdflib import Graph, Namespace
from rdflib.namespace import OWL, RDF, SKOS
from owlrl import DeductiveClosure, OWLRL_Semantics

KIT = Path(__file__).resolve().parents[2]
LAB = KIT / "semantic-lab"
EX = Namespace("https://example.org/fraser-coho-workshop/terms/")
INSTANCE = Namespace("https://example.org/fraser-coho-workshop/instances/")
SMN = Namespace("https://w3id.org/smn/")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def environment():
    require(Path.cwd().resolve() == KIT, "Run from the extracted fraser-coho-workshop directory.")
    expected = {"rdflib": "7.1.4", "owlrl": "7.1.4", "pyshacl": "0.30.1"}
    for name, version in expected.items():
        require(importlib.metadata.version(name) == version,
                f"Use {name}=={version}, from semantic-lab/scripts/requirements.txt.")
    return expected


def prepare():
    expected = environment()
    # Reuse the canonical workshop preparation check. It checks the human files,
    # but cannot establish that the recorded review was scientifically adequate.
    sys.path.insert(0, str(KIT / "scripts"))
    from workshop import check_preparation
    check_preparation()
    review = (KIT / "worksheets/peer-review.md").read_text()
    context = "automated disposable fixture; NOT human review" if "AUTOMATED" in review else "existing human preparation record checked; quality not assessed"
    return {"dependencies": expected, "preparation_context": context,
            "scope": "Selected local parsing, entailment, conformance and regression examples; no full OWL DL or scientific approval.",
            "network_requests": 0}


def reference_inspection():
    """Maintainer/CI inspection of supplied drafts; never records peer review."""
    expected = environment()
    require("Completion: pending" in (KIT / "worksheets/peer-review.md").read_text(),
            "The distribution should ship a pending human-review worksheet.")
    return {"dependencies": expected,
            "preparation_context": "not completed or claimed: technical inspection of shipped reference files only",
            "scope": "Reference artifact regression check; does not satisfy the learner preparation requirement, establish full OWL DL validity, or approve domain meaning.",
            "network_requests": 0}


def read_rows(path):
    with Path(path).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def source_trace():
    trace = json.loads((LAB / "model/source-trace.json").read_text())
    source = KIT / trace["source_path"]
    require(hashlib.sha256(source.read_bytes()).hexdigest() == trace["sha256"], "Source hash differs from the teaching trace.")
    rows = read_rows(source)
    require(len(rows) == 173 and len(rows[0]) == 14, "Expected all 173 rows and 14 columns.")
    require(list(rows[0]) == trace["columns"], "Source column order changed.")
    for selected in trace["selected_rows"]:
        require(rows[selected["data_row_number"] - 1] == selected["values"], "Selected row no longer matches all source values.")
    return rows, trace


def load_graph(*paths):
    graph = Graph()
    for path in paths:
        path = Path(path)
        require(path.is_file(), "Missing local Turtle file: " + str(path))
        graph.parse(path, format="turtle")
    require(not list(graph.triples((None, OWL.imports, None))),
            "This bounded offline exercise does not load ontology imports; review an explicit local closure separately.")
    return graph


def clone(graph):
    duplicate = Graph()
    for triple in graph:
        duplicate.add(triple)
    return duplicate


def closure(graph):
    result = clone(graph)
    DeductiveClosure(OWLRL_Semantics, axiomatic_triples=False, datatype_axioms=False).expand(result)
    return result


def check_class_concept_collision(graph):
    classes = set(graph.subjects(RDF.type, OWL.Class))
    concepts = set(graph.subjects(RDF.type, SKOS.Concept))
    require(not classes.intersection(concepts),
            "Workshop policy forbids using one IRI as both owl:Class and skos:Concept.")


def file_evidence(paths):
    return [{"path": Path(p).resolve().relative_to(KIT).as_posix(),
             "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()} for p in paths]


def finish(report, report_path=None):
    rendered = json.dumps(report, indent=2) + "\n"
    if report_path:
        path = Path(report_path).resolve()
        require(path.is_relative_to((KIT / "output/semantic-lab").resolve()), "Write reports only to a new output/semantic-lab/ path.")
        require(not path.exists(), "Report exists; choose a new name rather than overwrite it.")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x") as stream:
            stream.write(rendered)
    print(rendered, end="")
