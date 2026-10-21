# Optional live Chapter 5 exercise. No purchase, paid model or paid fallback.
# Run from the extracted project root after completing Chapters 2-4.
library(metasalmon)
source("scripts/workshop.R")
check_preparation()
if (!nzchar(Sys.getenv("OPENROUTER_API_KEY"))) stop("No free API key configured. Use ai/README.md and the recorded assessments instead.")
pkg <- read_salmon_datapackage(workshop_path)
dict <- pkg$dictionary[pkg$dictionary$column_name == "NATURAL_ADULT_SPAWNERS", , drop = FALSE]
for (field in c("term_iri", "property_iri", "entity_iri", "unit_iri", "constraint_iri", "statistical_modifier_iri")) dict[[field]] <- NA_character_
context <- file.path("worksheets", c("dataset-nodes.csv", "dataset-edges.csv", "data-dictionary.csv", "variable-decomposition.csv"))
out <- file.path("output", paste0("ai-live-r-", format(Sys.time(), "%Y%m%dT%H%M%S", tz = "UTC")))
if (dir.exists(out)) stop("Output exists; wait a second before starting a separate attempt.")
dir.create(out, recursive = TRUE)
records <- list()
attempts <- 0L

# The public callback seam lets this teaching script count actual HTTP attempts
# and retain request/response evidence. It does not change package APIs.
# Retire the callback when the released package exposes equivalent evidence
# and request-budget controls. Never log configuration or authorization headers.
free_request <- function(messages, config) {
  if (!identical(config$provider, "openrouter") || !identical(config$model, "openrouter/free")) stop("Only openrouter/free is permitted by this exercise.")
  if (attempts >= 8L) stop("Workshop request limit reached. Continue with recorded assessments.")
  attempts <<- attempts + 1L
  body <- list(model = "openrouter/free", messages = messages,
               temperature = 0, max_tokens = 2500,
               response_format = list(type = "json_object"))
  # No HTTP-level automatic retries. Any package retry re-enters this callback
  # and counts against the same maximum of eight requests.
  request <- httr2::request("https://openrouter.ai/api/v1/chat/completions") |>
    httr2::req_headers(Authorization = paste("Bearer", Sys.getenv("OPENROUTER_API_KEY"))) |>
    httr2::req_body_json(body, auto_unbox = TRUE) |>
    httr2::req_timeout(45) |>
    httr2::req_error(is_error = function(resp) FALSE)
  response <- tryCatch(httr2::req_perform(request), error = function(e) NULL)
  status <- if (is.null(response)) 0L else httr2::resp_status(response)
  payload <- if (is.null(response)) NULL else tryCatch(httr2::resp_body_json(response, simplifyVector = FALSE), error = function(e) NULL)
  # Only successful content is retained; arbitrary provider error bodies can
  # contain request diagnostics. Status codes are sufficient for failure review.
  record <- list(attempt = attempts, utc = format(Sys.time(), tz = "UTC", usetz = TRUE),
                 request = body, http_status = status)
  if (status == 200L) record$response <- payload
  records[[length(records) + 1L]] <<- record
  jsonlite::write_json(records, file.path(out, "requests.json"), auto_unbox = TRUE, pretty = TRUE)
  if (status != 200L) stop("Free model HTTP request failed, status ", status, ". Use recorded assessments if unavailable.")
  content <- payload$choices[[1]]$message$content
  if (is.null(content) || !nzchar(content)) stop("Free model returned no assessment content.")
  content <- sub("^```(?:json)?[[:space:]]*", "", trimws(content), perl = TRUE)
  content <- sub("[[:space:]]*```$", "", content, perl = TRUE)
  jsonlite::fromJSON(content, simplifyVector = FALSE)
}

result <- suggest_semantics(
  df = pkg$resources, dict = dict, sources = c("smn", "gcdfo"),
  max_per_role = 3, llm_assess = TRUE, llm_provider = "openrouter",
  llm_model = "openrouter/free", llm_top_n = 3,
  llm_context_files = context, llm_request_fn = free_request
)
suggestions <- semantic_suggestions(result)
assessments <- semantic_llm_assessments(result)
successful <- if (is.null(assessments) || !nrow(assessments)) 0L else sum(
  !is.na(assessments$llm_decision) & nzchar(assessments$llm_decision) &
    (is.na(assessments$llm_error) | !nzchar(assessments$llm_error)))
readr::write_csv(suggestions, file.path(out, "suggestions.csv"), na = "")
readr::write_csv(assessments, file.path(out, "assessments.csv"), na = "")
hashes <- stats::setNames(vapply(context, function(p) digest::digest(file = p, algo = "sha256", serialize = FALSE), character(1)), context)
jsonlite::write_json(list(
  kind = "live-provider-recording", package = "metasalmon", version = as.character(packageVersion("metasalmon")),
  requested_model = "openrouter/free", actual_http_attempts = attempts,
  successful_assessment_rows = successful,
  rehearsal_status = if (successful > 0L) "response-recorded-needs-human-review" else "failed-no-successful-assessment",
  context_sha256 = as.list(hashes), source_csv_sha256 = digest::digest(file = workshop_source, algo = "sha256", serialize = FALSE),
  note = "Provider responses and package decisions are proposals, not human approval. Actual routed model IDs are in requests.json when returned."
), file.path(out, "provenance.json"), auto_unbox = TRUE, pretty = TRUE)
message("Saved ", attempts, " HTTP attempts and ", successful, " successful assessment rows at ", out, ".")
if (successful == 0L) stop("No successful AI assessment was returned. Retain the failure receipt and use the recorded comparison activity.")
message("Compare the recorded response against the human model before any application.")
