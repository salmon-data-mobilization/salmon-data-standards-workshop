# Chapter 4 onward: validate a draft, or use --strict for the final SDP gate.
library(metasalmon)
source("scripts/workshop.R")
check_preparation()
args <- commandArgs(trailingOnly = TRUE)
strict <- "--strict" %in% args
paths <- args[args != "--strict"]
path <- if (length(paths)) paths[[1]] else workshop_path
validation <- validate_salmon_datapackage(path, require_iris = strict)
print(validation$issues)
print(validation$semantic_validation$issues)
if (nrow(validation$issues)) stop("Validation reported issues; read and resolve them before continuing.")
message("SDP validation passed. This does not establish scientific approval or EML readiness.")
