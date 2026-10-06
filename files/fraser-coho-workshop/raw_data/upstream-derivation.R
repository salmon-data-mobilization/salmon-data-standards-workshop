# Recreate the fuller built-in Fraser coho example from the official NuSEDS
# Open Government Canada record.
#
# Run from the repository root with:
#   Rscript data-raw/nuseds_fraser_coho_examples.R
#
# Upstream record:
#   https://open.canada.ca/data/en/dataset/c48669a3-045b-400d-b730-48aafe8c5ee6
# Upstream resource:
#   https://api-proxy.edh-cde.dfo-mpo.gc.ca/catalogue/records/c48669a3-045b-400d-b730-48aafe8c5ee6/attachments/Fraser%20and%20BC%20Interior%20NuSEDS_20251014.xlsx
# Licence:
#   Open Government Licence - Canada
#
# Filter logic for the shipped fuller example:
#   - keep SPECIES == "Coho"
#   - keep ANALYSIS_YR in c(2023, 2024)
#   - keep a compact analysis-friendly subset of columns
#   - use NATURAL_ADULT_SPAWNERS because NATURAL_SPAWNERS_TOTAL is blank for
#     this official two-year slice
#   - convert START_DTT / END_DTT to ISO dates
#   - sort by ANALYSIS_YR, AREA, WATERBODY, POP_ID

required_pkgs <- c("readxl", "dplyr", "readr")
missing_pkgs <- required_pkgs[
  !vapply(required_pkgs, requireNamespace, logical(1), quietly = TRUE)
]
if (length(missing_pkgs) > 0) {
  stop(
    "Install required packages before running this script: ",
    paste(missing_pkgs, collapse = ", "),
    call. = FALSE
  )
}

record_url <- "https://open.canada.ca/data/en/dataset/c48669a3-045b-400d-b730-48aafe8c5ee6"
resource_url <- paste0(
  "https://api-proxy.edh-cde.dfo-mpo.gc.ca/catalogue/records/",
  "c48669a3-045b-400d-b730-48aafe8c5ee6/attachments/",
  "Fraser%20and%20BC%20Interior%20NuSEDS_20251014.xlsx"
)

script_arg <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
if (length(script_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", script_arg[[1]]), mustWork = TRUE)
} else {
  script_path <- normalizePath(
    file.path("data-raw", "nuseds_fraser_coho_examples.R"),
    mustWork = TRUE
  )
}
repo_root <- dirname(dirname(script_path))
output_path <- file.path(repo_root, "inst", "extdata", "nuseds-fraser-coho-2023-2024.csv")

options(timeout = max(120, getOption("timeout")))
workbook_path <- tempfile(fileext = ".xlsx")
utils::download.file(resource_url, workbook_path, mode = "wb", quiet = TRUE)

raw_nuseds <- suppressWarnings(readxl::read_excel(workbook_path, sheet = 1))

fraser_coho_fuller <- raw_nuseds |>
  dplyr::filter(.data$SPECIES == "Coho", .data$ANALYSIS_YR %in% c(2023, 2024)) |>
  dplyr::transmute(
    POP_ID = as.integer(.data$POP_ID),
    POPULATION = .data$POPULATION,
    AREA = .data$AREA,
    WATERBODY = .data$WATERBODY,
    ANALYSIS_YR = as.integer(.data$ANALYSIS_YR),
    SPECIES = .data$SPECIES,
    RUN_TYPE = .data$RUN_TYPE,
    NATURAL_ADULT_SPAWNERS = .data$NATURAL_ADULT_SPAWNERS,
    ESTIMATE_METHOD = .data$ESTIMATE_METHOD,
    ESTIMATE_CLASSIFICATION = .data$ESTIMATE_CLASSIFICATION,
    ESTIMATE_STAGE = .data$ESTIMATE_STAGE,
    START_DTT = as.Date(.data$START_DTT),
    END_DTT = as.Date(.data$END_DTT),
    WATERSHED_CDE = .data$WATERSHED_CDE
  ) |>
  dplyr::arrange(.data$ANALYSIS_YR, .data$AREA, .data$WATERBODY, .data$POP_ID)

stopifnot(
  nrow(fraser_coho_fuller) == 173L,
  identical(range(fraser_coho_fuller$ANALYSIS_YR), c(2023L, 2024L))
)

readr::write_csv(fraser_coho_fuller, output_path, na = "")

cat(
  "Wrote ", output_path,
  " (", nrow(fraser_coho_fuller), " rows, ", ncol(fraser_coho_fuller), " columns)\n",
  sep = ""
)
cat("Record: ", record_url, "\n", sep = "")
cat("Resource: ", resource_url, "\n", sep = "")
