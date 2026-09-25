# Chapter 7: credential-free TEST plan only. There is no live-upload switch.
# Copy the supplied reference checkpoint to a new local output directory before
# planning; published/checkpoint files must not be overwritten during practice.
library(metasalmon)
source("scripts/workshop.R")
check_preparation()
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1L) stop("Supply the path to a separate local reference-package copy.")
path <- args[[1]]
if (!startsWith(normalizePath(path), paste0(normalizePath("output"), "/"))) stop("Use a separate package copy under output/ before this exercise.")
validation <- validate_salmon_datapackage(path, require_iris = TRUE)
if (nrow(validation$issues)) stop("Resolve strict SDP issues first.")
# A draft dictionary alone cannot pass the EML gate. The reference package
# needs vocabulary evidence, explicit selection records and an EML sidecar.
write_eml_from_sdp(path, knb_environment = "test", overwrite = TRUE)
plan <- publish_sdp_to_knb(path, public = TRUE, dry_run = TRUE,
  representation = "expanded", knb_environment = "test", overwrite = TRUE)
print(plan)
message("TEST dry run only; no objects uploaded and no production action performed.")
