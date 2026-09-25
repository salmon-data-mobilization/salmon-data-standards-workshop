"""Check the bounded teaching vocabulary locally; never approve its meanings."""
import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

from rdflib import DCTERMS, OWL, RDF, SKOS, Graph, Literal, Namespace, URIRef


TERMS = Namespace("https://example.org/fraser-coho-workshop/terms/")
EXPECTED = {
    "area-under-the-curve": "Area Under the Curve",
    "combined-methods": "Combined Methods",
    "fixed-site-census": "Fixed Site Census",
    "resistivity-counter": "Resistivity Counter",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_vocabulary(vocabulary, concepts, kit_root):
    """Inspect source bindings and representation without inventing human review."""
    vocabulary, concepts, kit_root = map(Path, (vocabulary, concepts, kit_root))
    source = kit_root / "raw_data/nuseds-fraser-coho-2023-2024.csv"
    provenance = json.loads((kit_root / "semantic-lab/vocabulary/provenance.json").read_text())
    expected_hash = next(item["sha256"] for item in provenance["evidence"]
                         if item["path"] == "raw_data/nuseds-fraser-coho-2023-2024.csv")
    require(hashlib.sha256(source.read_bytes()).hexdigest() == expected_hash,
            "The source bytes changed; restore the unchanged workshop source.")
    with source.open(newline="") as stream:
        source_rows = list(csv.DictReader(stream))
    with concepts.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 4, "This exercise requires four concept records.")
    by_iri = {row["concept_iri"]: row for row in rows}
    expected_iris = {str(TERMS[slug]) for slug in EXPECTED}
    require(set(by_iri) == expected_iris, "Use the four distinct teaching concept IRIs.")

    # format='turtle' reads this local file only. No URL or owl:imports is fetched.
    graph = Graph().parse(vocabulary, format="turtle")
    require(set(graph.subjects(RDF.type, SKOS.Concept)) == {URIRef(x) for x in expected_iris},
            "The Turtle must contain exactly the four teaching SKOS concepts.")
    require(set(graph.subjects(RDF.type, SKOS.ConceptScheme)) == {TERMS["estimate-method-scheme"]},
            "Use one separate estimate-method scheme.")
    require(all(isinstance(subject, URIRef) and str(subject).startswith(str(TERMS))
                for subject in graph.subjects()),
            "Do not add assertions or labels to foreign-namespace subjects in this local vocabulary.")
    require(not list(graph.triples((None, OWL.imports, None))),
            "This vocabulary exercise does not use ontology imports.")
    unsupported_relations = {SKOS.broader, SKOS.narrower, SKOS.related, SKOS.exactMatch,
                             SKOS.closeMatch, SKOS.broadMatch, SKOS.narrowMatch, SKOS.relatedMatch}
    require(not any(predicate in unsupported_relations for _, predicate, _ in graph),
            "This source-bounded selection has no supported hierarchy or mappings; bridges are reviewed separately.")
    for slug, code in EXPECTED.items():
        iri = TERMS[slug]
        row = by_iri[str(iri)]
        require(row["source_column"] == "ESTIMATE_METHOD" and row["code_value"] == code,
                f"Preserve the exact source binding for {slug}.")
        require(any(record["ESTIMATE_METHOD"] == code for record in source_rows),
                f"The code {code} is not observed in the source.")
        require(row["pref_label"] == code and row["language"] == "en",
                f"Keep the source label and English language for {slug}.")
        require(not row["broader_iri"].strip() and not row["alternative_label"].strip(),
                f"No parent or alternative label is established by this exercise's sources for {slug}.")
        require(set(graph.objects(iri, SKOS.prefLabel)) == {Literal(code, lang="en")},
                f"Use one exact English preferred label for {slug}.")
        require(set(graph.objects(iri, SKOS.inScheme)) == {TERMS["estimate-method-scheme"]}
                and row["scheme_iri"] == str(TERMS["estimate-method-scheme"]),
                f"Scheme membership does not match the worksheet for {slug}.")
        require((iri, RDF.type, OWL.Class) not in graph,
                f"A teaching concept must not also be an OWL class: {slug}.")
        require(all(row[key].strip() for key in ("definition_status", "scope_note",
                    "source_reference", "source_caveat", "status", "open_question")),
                f"Complete evidence, scope, status and questions for {slug}.")
        definitions = set(graph.objects(iri, SKOS.definition))
        if slug == "resistivity-counter":
            require(not row["definition"].strip() and not definitions,
                    "Keep the missing counter procedure definition explicit in this source-bounded exercise.")
        else:
            require(row["definition"].strip()
                    and definitions == {Literal(row["definition"], lang="en")},
                    f"The sourced definition must agree between CSV and Turtle for {slug}.")
        require(set(graph.objects(iri, SKOS.scopeNote)) == {Literal(row["scope_note"], lang="en")},
                f"The scope note differs from the worksheet for {slug}.")
        require(list(graph.objects(iri, SKOS.editorialNote)) and list(graph.objects(iri, DCTERMS.source)),
                f"Retain the editorial question/status and source link for {slug}.")
        require(not set(graph.objects(iri, SKOS.prefLabel)) & set(graph.objects(iri, SKOS.altLabel)),
                f"A preferred label cannot also be an alternative label for {slug}.")
        require(not list(graph.objects(iri, SKOS.altLabel)),
                f"Do not add an unsupported alternative label for {slug}.")
    return {"status": "pass", "scope": "bounded vocabulary structure and source bindings",
            "concepts": 4, "definitions": 3, "explicit_definition_gaps": 1,
            "source_rows": len(source_rows), "triples": len(graph),
            "scientific_approval": "not assessed", "stewardship_adoption": "not assessed"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vocabulary", type=Path, default=Path("output/semantic-lab/estimate-methods.ttl"))
    parser.add_argument("--concepts", type=Path, default=Path("semantic-lab/worksheets/vocabulary-concepts.csv"))
    args = parser.parse_args()
    kit_root = Path.cwd()
    # Reuse the existing preparation contract instead of a second review marker.
    sys.path.insert(0, str(kit_root / "scripts"))
    from workshop import check_preparation
    check_preparation()
    print(json.dumps(validate_vocabulary(args.vocabulary, args.concepts, kit_root), indent=2))


if __name__ == "__main__":
    main()
