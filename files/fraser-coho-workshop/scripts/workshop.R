# Shared workshop checks. Source this file from the extracted project root.
# These checks make the preparation step visible; they cannot verify the
# quality of a peer's scientific judgement.
workshop_source <- "raw_data/nuseds-fraser-coho-2023-2024.csv"
workshop_path <- "output/fraser-coho-workshop-sdp"

check_preparation <- function() {
  required <- file.path("worksheets", c(
    "dataset-nodes.csv", "dataset-edges.csv", "data-dictionary.csv",
    "variable-decomposition.csv", "peer-review.md"
  ))
  if (!all(file.exists(required))) stop("Complete the Chapter 2-3 worksheets first.")
  review <- readLines("worksheets/peer-review.md", warn = FALSE)
  if (!any(grepl("^Completion: complete$", review)) ||
      !any(grepl("^Reviewer: \\S", review, perl = TRUE)) ||
      !any(grepl("^Review date: [0-9]{4}-[0-9]{2}-[0-9]{2}$", review))) {
    stop("Chapter 3 peer review is pending. Record the real reviewer and Completion: complete.")
  }
  review_date <- sub("^Review date: ", "", review[grepl("^Review date: ", review)])
  if (length(review_date) != 1L || is.na(as.Date(review_date, format = "%Y-%m-%d"))) stop("Enter a valid review date as YYYY-MM-DD.")
  # This is a shape check, not an automated judgement about scientific quality.
  # A human must still reconcile the graph, evidence and dictionary.
  read_sheet <- function(name) readr::read_csv(file.path("worksheets", name),
    col_types = readr::cols(.default = readr::col_character()), show_col_types = FALSE)
  filled <- function(x) !is.na(x) & nzchar(trimws(x))
  nodes <- read_sheet("dataset-nodes.csv")
  edges <- read_sheet("dataset-edges.csv")
  decomposition <- read_sheet("variable-decomposition.csv")
  if (!all(c("node_id", "label", "node_kind", "evidence", "question") %in% names(nodes)) ||
      nrow(nodes) < 2L || anyDuplicated(nodes$node_id) ||
      !all(filled(nodes$node_id) & filled(nodes$label) & filled(nodes$node_kind)) ||
      !all(filled(nodes$evidence) | filled(nodes$question))) stop("Complete the named graph nodes and their evidence or questions.")
  if (!all(c("subject_id", "relationship", "object_id", "evidence", "question") %in% names(edges)) ||
      nrow(edges) < 1L || !all(filled(edges$relationship)) ||
      !all(edges$subject_id %in% nodes$node_id & edges$object_id %in% nodes$node_id) ||
      !all(filled(edges$evidence) | filled(edges$question))) stop("Complete labelled graph edges with valid endpoints and evidence or questions.")
  slots <- c("variable_label", "entity", "property", "result_value", "unit", "method_field")
  if (!all(c("column_name", slots, "open_question") %in% names(decomposition))) stop("Use the supplied decomposition worksheet columns.")
  adult <- decomposition[decomposition$column_name == "NATURAL_ADULT_SPAWNERS", , drop = FALSE]
  if (nrow(adult) != 1L || !(all(vapply(adult[slots], function(x) all(filled(x)), logical(1))) ||
      filled(adult$open_question))) stop("Decompose the adult-spawner variable or record the unresolved interpretation explicitly.")
  human <- readr::read_csv("worksheets/data-dictionary.csv", show_col_types = FALSE,
                          col_types = readr::cols(.default = readr::col_character()))
  columns <- names(readr::read_csv(workshop_source, n_max = 0, show_col_types = FALSE))
  if (nrow(human) != 14L || anyDuplicated(human$column_name) ||
      !setequal(human$column_name, columns)) stop("Review all 14 source fields before importing the table.")
  described <- !is.na(human$working_definition) & nzchar(trimws(human$working_definition))
  questioned <- !is.na(human$open_question) & nzchar(trimws(human$open_question))
  if (!all(described | questioned)) stop("Each field needs a working definition or an explicit question.")
  invisible(human)
}

read_workshop_source <- function() {
  manifest <- jsonlite::read_json("raw_data/source-manifest.json", simplifyVector = FALSE)
  entry <- Filter(function(x) identical(x$path, workshop_source), manifest$files)[[1]]
  if (!identical(digest::digest(file = workshop_source, algo = "sha256", serialize = FALSE), entry$sha256)) {
    stop("The source CSV has changed. Re-extract it from the teaching kit; do not edit the source.")
  }
  # Character input preserves identifiers and code spelling. Explicit dictionary
  # types below distinguish nominal IDs from numeric estimates and calendar dates.
  readr::read_csv(workshop_source, col_types = readr::cols(.default = readr::col_character()),
                  show_col_types = FALSE, progress = FALSE)
}

fill_workshop_metadata <- function(pkg, human) {
  definitions <- stats::setNames(human$working_definition, human$column_name)
  questions <- stats::setNames(human$open_question, human$column_name)
  pkg$dictionary$column_description <- vapply(pkg$dictionary$column_name, function(name) {
    definition <- definitions[[name]]
    if (is.na(definition) || !nzchar(definition)) paste("Open interpretation question:", questions[[name]]) else definition
  }, character(1))
  pkg$dictionary$column_role <- "attribute"
  pkg$dictionary$column_role[pkg$dictionary$column_name == "POP_ID"] <- "identifier"
  pkg$dictionary$column_role[pkg$dictionary$column_name %in% c("ANALYSIS_YR", "START_DTT", "END_DTT")] <- "temporal"
  pkg$dictionary$column_role[pkg$dictionary$column_name == "NATURAL_ADULT_SPAWNERS"] <- "measurement"
  pkg$dictionary$column_role[pkg$dictionary$column_name %in% c("SPECIES", "RUN_TYPE", "ESTIMATE_METHOD", "ESTIMATE_CLASSIFICATION", "ESTIMATE_STAGE", "AREA")] <- "categorical"
  pkg$dictionary$value_type <- "string"
  pkg$dictionary$value_type[pkg$dictionary$column_name == "ANALYSIS_YR"] <- "integer"
  pkg$dictionary$value_type[pkg$dictionary$column_name == "NATURAL_ADULT_SPAWNERS"] <- "number"
  pkg$dictionary$value_type[pkg$dictionary$column_name %in% c("START_DTT", "END_DTT")] <- "date"
  pkg$dictionary$unit_label[pkg$dictionary$column_name == "NATURAL_ADULT_SPAWNERS"] <- "Individual"
  # The hand-written interpretation does not silently become accepted ontology links.
  for (field in intersect(c("term_iri", "unit_iri", "property_iri", "entity_iri", "constraint_iri", "statistical_modifier_iri", "term_type"), names(pkg$dictionary))) pkg$dictionary[[field]] <- NA_character_
  pkg$dataset$title <- "Workshop demonstration: NuSEDS Fraser Coho — KNB Test Node"
  pkg$dataset$description <- paste(
    "Teaching derivative of the Open Canada NuSEDS Fraser and BC Interior workbook:",
    "173 Coho records from analysis years 2023-2024, retaining 14 source columns.",
    "Population-year pairs are not unique; retain waterbody and source record context.",
    "Working interpretations are pending scientific review by Bruno and Tom.")
  pkg$dataset$creator <- "Fisheries and Oceans Canada (source data)"
  pkg$dataset$contact_name <- "Brett Johnson"
  pkg$dataset$contact_email <- "brett.johnson@dfo-mpo.gc.ca"
  pkg$dataset$license <- "Open Government Licence - Canada"
  pkg$dataset$source_citation <- "Fisheries and Oceans Canada. NuSEDS: Fraser and BC Interior NuSEDS_20251014. Original publication: https://open.canada.ca/data/en/dataset/c48669a3-045b-400d-b730-48aafe8c5ee6"
  pkg$dataset$provenance_note <- "The metasalmon v0.5.0 derivation selects Coho and analysis years 2023-2024, retains 14 columns and converts survey dates to ISO format. The workshop preserves all 173 rows and source values."
  pkg$tables$description <- "A NuSEDS source estimate record with population identifier, waterbody, analysis year and reported estimation context. POP_ID plus ANALYSIS_YR is not a unique record key."
  pkg$tables$observation_unit <- "Population described within source location and analysis-year context; multiple records can describe a population-year pair."
  # Rebuild code lists only for fields explicitly marked categorical. The
  # packages' automatic code harvesting also includes identifiers; retaining
  # those rows would contradict the column-role contract in the SDP validator.
  code_fields <- pkg$dictionary$column_name[pkg$dictionary$column_role == "categorical"]
  if (!is.null(pkg$codes) && nrow(pkg$codes)) pkg$codes <- pkg$codes[pkg$codes$column_name %in% code_fields, , drop = FALSE]
  # create_sdp() can prefill code links even with semantic seeding disabled.
  # Preserve the code values while removing those unreviewed assignments.
  # Retire this clearing step when the pinned package's unseeded path leaves
  # code links empty; semantic decisions belong in the later review activity.
  for (field in intersect(c("vocabulary_iri", "term_iri", "term_type"), names(pkg$codes))) pkg$codes[[field]] <- NA_character_
  if (!is.null(pkg$codes) && nrow(pkg$codes)) pkg$codes$code_description <- paste0(
    "Source label in ", pkg$codes$column_name, ": ", pkg$codes$code_value,
    ". Exact operational meaning is not established by the selected table; retain this source question for review.")
  pkg
}

write_workshop_package <- function(pkg, path, overwrite = FALSE) {
  metasalmon::write_salmon_datapackage(
    resources = pkg$resources, dataset_meta = pkg$dataset,
    table_meta = pkg$tables, dict = pkg$dictionary, codes = pkg$codes,
    path = path, overwrite = overwrite
  )
}
