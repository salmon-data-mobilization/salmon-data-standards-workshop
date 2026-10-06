# Run from the extracted workshop root after actual Chapter 2-3 preparation.
# Candidate detection and text rendering only: no retrieval, AI, or submission.
stopifnot(as.character(utils::packageVersion("metasalmon")) == "0.5.0")
source("scripts/workshop.R")
check_preparation()
destination <- file.path("output", "term-request-preview-r")
if (dir.exists(destination)) stop("Preview folder exists; preserve it and choose a new destination in this script.")
suggestions <- readr::read_csv(
  "checkpoints/seeded-sdp/semantic_suggestions.csv", show_col_types = FALSE
)
gaps <- metasalmon::detect_semantic_term_gaps(suggestions = suggestions)
previews <- metasalmon::render_ontology_term_request(
  gaps, scope = "auto", ask = FALSE,
  profile_name = "fraser-coho-workshop-draft"
)
dir.create(destination, recursive = TRUE)
readr::write_csv(gaps, file.path(destination, "candidate-gaps.csv"))
if (nrow(previews)) {
  for (i in seq_len(nrow(previews))) {
    writeLines(c("# SOFTWARE PREVIEW: not a reviewed gap or submitted request", "",
      previews$request_title[[i]], "", previews$request_body[[i]]),
      file.path(destination, sprintf("request-%02d.md", i)))
  }
}
message(nrow(gaps), " candidate rows; ", nrow(previews), " local request previews. Review against your source evidence.")
