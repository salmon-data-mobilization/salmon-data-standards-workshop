"""Shared preparation and source checks for the Python workshop lane."""
import csv
import datetime
import hashlib
import json
import re
from pathlib import Path

SOURCE = Path("raw_data/nuseds-fraser-coho-2023-2024.csv")
PACKAGE = Path("output/fraser-coho-workshop-sdp")


def check_preparation():
    required = ["dataset-nodes.csv", "dataset-edges.csv", "data-dictionary.csv",
                "variable-decomposition.csv", "peer-review.md"]
    if not all((Path("worksheets") / p).is_file() for p in required):
        raise ValueError("Complete the Chapter 2-3 worksheets first.")
    review = Path("worksheets/peer-review.md").read_text()
    date_matches = re.findall(r"^Review date: (\d{4}-\d{2}-\d{2})$", review, re.M)
    if not re.search(r"^Completion: complete$", review, re.M) or not re.search(r"^Reviewer: \S", review, re.M) or len(date_matches) != 1:
        raise ValueError("Chapter 3 peer review is pending. Record the real reviewer and Completion: complete.")
    datetime.date.fromisoformat(date_matches[0])
    # Mechanical shape checks never establish the quality of a human review.
    def sheet(name):
        with (Path("worksheets") / name).open(newline="") as stream:
            return list(csv.DictReader(stream))
    nodes, edges = sheet("dataset-nodes.csv"), sheet("dataset-edges.csv")
    node_ids = {r.get("node_id", "") for r in nodes}
    if len(nodes) < 2 or len(node_ids) != len(nodes) or not all(
        all(r.get(k, "").strip() for k in ("node_id", "label", "node_kind")) and
        (r.get("evidence", "").strip() or r.get("question", "").strip()) for r in nodes):
        raise ValueError("Complete named graph nodes and their evidence or questions.")
    if not edges or not all(r.get("subject_id") in node_ids and r.get("object_id") in node_ids and
        r.get("relationship", "").strip() and (r.get("evidence", "").strip() or r.get("question", "").strip()) for r in edges):
        raise ValueError("Complete labelled graph edges with valid endpoints and evidence or questions.")
    adult = [r for r in sheet("variable-decomposition.csv") if r.get("column_name") == "NATURAL_ADULT_SPAWNERS"]
    slots = ("variable_label", "entity", "property", "result_value", "unit", "method_field")
    if len(adult) != 1 or not (all(adult[0].get(k, "").strip() for k in slots) or adult[0].get("open_question", "").strip()):
        raise ValueError("Decompose the adult-spawner variable or record the unresolved interpretation explicitly.")
    with Path("worksheets/data-dictionary.csv").open(newline="") as f:
        human = list(csv.DictReader(f))
    with SOURCE.open(newline="") as f:
        columns = next(csv.reader(f))
    if len(human) != 14 or {r["column_name"] for r in human} != set(columns):
        raise ValueError("Review all 14 source fields before importing the table.")
    if not all(r["working_definition"].strip() or r["open_question"].strip() for r in human):
        raise ValueError("Every field needs a working definition or an explicit question.")
    return human


def read_source():
    import pandas as pd
    manifest = json.loads(Path("raw_data/source-manifest.json").read_text())
    expected = next(r["sha256"] for r in manifest["files"] if r["path"] == str(SOURCE))
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != expected:
        raise ValueError("Source CSV changed; re-extract the unchanged source from the kit.")
    return pd.read_csv(SOURCE, dtype=str, keep_default_na=False)


def fill_metadata(pkg, human):
    dictionary = pkg["dictionary"]
    descriptions = {r["column_name"]: r["working_definition"] or "Open interpretation question: " + r["open_question"] for r in human}
    dictionary["column_description"] = dictionary["column_name"].map(descriptions)
    dictionary["column_role"] = "attribute"
    dictionary.loc[dictionary.column_name == "POP_ID", "column_role"] = "identifier"
    dictionary.loc[dictionary.column_name.isin(["ANALYSIS_YR", "START_DTT", "END_DTT"]), "column_role"] = "temporal"
    dictionary.loc[dictionary.column_name == "NATURAL_ADULT_SPAWNERS", "column_role"] = "measurement"
    categories = ["SPECIES", "RUN_TYPE", "ESTIMATE_METHOD", "ESTIMATE_CLASSIFICATION", "ESTIMATE_STAGE", "AREA"]
    dictionary.loc[dictionary.column_name.isin(categories), "column_role"] = "categorical"
    dictionary["value_type"] = "string"
    dictionary.loc[dictionary.column_name == "ANALYSIS_YR", "value_type"] = "integer"
    dictionary.loc[dictionary.column_name == "NATURAL_ADULT_SPAWNERS", "value_type"] = "number"
    dictionary.loc[dictionary.column_name.isin(["START_DTT", "END_DTT"]), "value_type"] = "date"
    dictionary.loc[dictionary.column_name == "NATURAL_ADULT_SPAWNERS", "unit_label"] = "Individual"
    for field in ("term_iri", "unit_iri", "property_iri", "entity_iri", "constraint_iri", "statistical_modifier_iri", "term_type"):
        dictionary[field] = ""
    values = {
        "title": "Workshop demonstration: NuSEDS Fraser Coho — KNB Test Node",
        "description": "Teaching derivative of the Open Canada NuSEDS Fraser and BC Interior workbook: 173 Coho records from analysis years 2023-2024, retaining 14 source columns. Population-year pairs are not unique; retain waterbody and source record context. Working interpretations are pending scientific review by Bruno and Tom.",
        "creator": "Fisheries and Oceans Canada (source data)",
        "contact_name": "Brett Johnson", "contact_email": "brett.johnson@dfo-mpo.gc.ca",
        "license": "Open Government Licence - Canada",
        "source_citation": "Fisheries and Oceans Canada. NuSEDS: Fraser and BC Interior NuSEDS_20251014. Original publication: https://open.canada.ca/data/en/dataset/c48669a3-045b-400d-b730-48aafe8c5ee6",
        "provenance_note": "The metasalmon v0.5.0 derivation selects Coho and analysis years 2023-2024, retains 14 columns and converts survey dates to ISO format. The workshop preserves all 173 rows and source values.",
    }
    for field, value in values.items():
        pkg["dataset"][field] = value
    pkg["tables"]["description"] = "A NuSEDS source estimate record with population identifier, waterbody, analysis year and reported estimation context. POP_ID plus ANALYSIS_YR is not a unique record key."
    pkg["tables"]["observation_unit"] = "Population described within source location and analysis-year context; multiple records can describe a population-year pair."
    if pkg.get("codes") is not None and not pkg["codes"].empty:
        pkg["codes"] = pkg["codes"].loc[pkg["codes"].column_name.isin(categories)].copy()
        # The pinned unseeded path can still prefill code IRIs. Retire this
        # clearing step when the released path leaves them empty; acceptance
        # belongs to the later human semantic-review activity.
        for field in ("vocabulary_iri", "term_iri", "term_type"):
            pkg["codes"][field] = ""
        pkg["codes"]["code_description"] = pkg["codes"].apply(lambda r:
            f"Source label in {r.column_name}: {r.code_value}. Exact operational meaning is not established by the selected table; retain this source question for review.", axis=1)
    return pkg


def write_package(pkg, path, overwrite=False):
    import metasalmonpy as ms
    return ms.write_salmon_datapackage(resources=pkg["resources"], dataset_meta=pkg["dataset"],
        table_meta=pkg["tables"], dict_df=pkg["dictionary"], codes=pkg.get("codes"),
        path=str(path), overwrite=overwrite)
