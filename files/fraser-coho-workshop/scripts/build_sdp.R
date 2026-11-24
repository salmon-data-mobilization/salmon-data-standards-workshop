# Chapter 4: run from the extracted fraser-coho-workshop project root.
library(metasalmon)
source("scripts/workshop.R")
stopifnot(as.character(packageVersion("metasalmon")) == "0.5.0")
human <- check_preparation()
raw <- read_workshop_source()
if (dir.exists(workshop_path)) stop("A package already exists. Review it or choose a new versioned output folder; this script will not overwrite it.")

# Create a draft only after the human model has been reviewed. No semantic
# retrieval or LLM call happens here; Chapter 5 introduces candidate review.
create_sdp(list(escapement = raw), path = workshop_path,
           dataset_id = "fraser-coho-workshop", table_id = "escapement",
           seed_semantics = FALSE, llm_assess = FALSE,
           check_updates = FALSE, overwrite = FALSE)
pkg <- read_salmon_datapackage(workshop_path)
pkg <- fill_workshop_metadata(pkg, human)
# This replaces only the draft just created above, not prior learner work.
write_workshop_package(pkg, workshop_path, overwrite = TRUE)
file.copy("worksheets/peer-review.md", file.path(workshop_path, "preparation-review.md"))
message("Draft created. Missing semantic IRIs are expected until Chapter 5.")
