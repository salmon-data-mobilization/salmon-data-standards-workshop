Salmon Data Package Review Checklist

Dataset ID: fraser-coho-workshop

Do this review in R. Every step below prints the exact call for the next one,
so pasting those calls into a script leaves a record of what you decided and why --
which is the one thing editing the CSVs in a spreadsheet cannot give you.

Throughout, pkg_path is the folder this file is in:
  pkg_path <- "<path to this folder>"

Checklist:
[ ] 1. No semantic_suggestions.csv was written for this package, so there is no shortlist to review. Set an IRI you already know with set_sdp_column(pkg_path, "<column>", term_iri = "..."), or request a new term rather than forcing a bad match.
[ ] 2. Fill in the free text and any remaining gaps:  review_metadata(pkg_path) It lists every field that still blocks validation -- placeholders, blank required fields, and required IRIs no candidate was ever found for -- and prints the set_sdp_*() call that fills each one. Replace the <...> in the printed call with the real value and paste it.
[ ] 3. If metadata/codes.csv exists, confirm the coded values with set_sdp_code(pkg_path, "<column>", "<code>", ...).
[ ] 4. Validate:  validate_salmon_datapackage(pkg_path, require_iris = TRUE). It passes only once every placeholder and REVIEW marker is gone.
[ ] 5. If you need EDH XML after review, rebuild it from the finalized package with write_edh_xml_from_sdp(pkg_path).
[ ] 6. Share the whole package folder (or a zip of the whole folder) so the metadata and data stay together.

If you need a new ontology term, route it here:
- Shared cross-organization/domain term request (salmon-domain): https://github.com/salmon-data-mobilization/salmon-domain-ontology/issues/new/choose
- DFO-specific policy/operations term request (gcdfo / DFO salmon ontology): https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/new/choose

The authoritative files are metadata/column_dictionary.csv and metadata/tables.csv; semantic_suggestions.csv is the evidence trail, including the decision and reason once you apply them.

Editing metadata/*.csv in a spreadsheet still works and is still supported. It is the fallback,
not the recommended path: a spreadsheet edit leaves no record of why a term was chosen.
If you do use one, save the files back as CSV before re-validating in R.
Guide: https://salmon-data-mobilization.github.io/metasalmon/articles/post-review-package-publication.html
