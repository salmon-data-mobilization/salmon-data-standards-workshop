---
title: Setup
---

## What to bring

Bring a laptop and choose a spreadsheet, R, or Python lane. The workshop supplies the data and all required review material. You do not need a personal dataset, AI account, API key, purchased credits, or catalog account.

Everyone uses **173 rows and 14 columns** from `nuseds-fraser-coho-2023-2024.csv`. This is the Fraser Coho 2023–2024 example, with `NATURAL_ADULT_SPAWNERS` as the measurement field. Its [provenance](glossary.html#provenance) is supplied in the kit and described in the [bundled example notes][metasalmon-example-data]. Keep the original CSV unchanged and retain missing values as missing.

## Download and open the workshop kit

The example dataset is already included in [metasalmon v0.5.0][metasalmon-example-data]. The workshop ZIP contains an identical copy, plus the worksheets, scripts, recorded AI outputs, and package checkpoints used by R, Python, and spreadsheet learners.

Download [fraser-coho-workshop.zip][workshop-kit] and extract it to a location where you can save your work. Use `fraser-coho-workshop/` as the project root. Open the included source, context, and exercise files before the workshop; ask the facilitator for a local copy if downloads are restricted.

The core working paths are:

```text
fraser-coho-workshop/
  raw_data/
    nuseds-fraser-coho-2023-2024.csv
  scripts/
    build_sdp.R                 # R lane
    build_sdp.py                # Python lane
  output/
    fraser-coho-workshop-sdp/
  semantic-lab/                 # Day 2: draft vocabularies, model, bridges, requests
```

The kit also supplies worksheets, source context, recorded AI outputs, and three package checkpoints: `draft-sdp`, `seeded-sdp`, and `reference-sdp`. Follow its README and each chapter to choose the correct checkpoint. Keep your own exercise answers separate from the supplied reference files. The reference is a technical draft pending Bruno and Tom's domain review.

All chapters use dataset ID `fraser-coho-workshop` and table ID `escapement`. Code paths are relative to the project root. In RStudio, use **File > New Project > Existing Directory** to open the extracted folder as a project. In Python, open a terminal or editor in that folder. Do not change the working directory partway through a build.

## Spreadsheet lane

Use Excel, LibreOffice Calc, or another spreadsheet editor. Open CSVs through the import dialog so identifiers and code values can remain text. The first three chapters also use paper or a simple drawing tool; no ontology editor is needed.

You will write and peer-review a human dictionary, inspect the same generated package as the code lanes, compare supplied candidate evidence, and record decisions in the exercise files. An R or Python collaborator runs the validator and export steps. Manual inspection does not establish that these automated checks passed.

## R lane

Use R 4.3 or newer with RStudio, Positron, or another R editor. Install the pinned release before the workshop:

```r
install.packages(c("remotes", "readr", "dplyr", "purrr"))
remotes::install_github("salmon-data-mobilization/metasalmon@v0.5.0")

library(metasalmon)
packageVersion("metasalmon")
```

The version should be `0.5.0`. This release provides the native review and metadata helpers used later in the workshop. The lesson build pins the same release; install the tag rather than a moving default branch.

For local EML export in Chapter 7, also install:

```r
install.packages(c("emld", "jsonvalidate"))
```

The facilitator provides a test publication demonstration. Learners do not need DataONE credentials to inspect it or run the local dry-run exercise.

## Python lane

Use Python 3.9 or newer in a dedicated virtual environment. From the workshop project root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install \
  "metasalmonpy @ https://github.com/salmon-data-mobilization/metasalmonpy/archive/refs/tags/v0.4.0.tar.gz"
python -c "import metasalmonpy; print(metasalmonpy.__version__)"
```

On Windows, activate the environment using `.venv\Scripts\Activate.ps1` in PowerShell. The package version should be `0.4.0`.

R and Python are pinned to different releases because the R-native review queue and `set_sdp_*()` helpers have not yet shipped in this Python release. Follow the Python alternatives and supplied candidate evidence in the chapters; a matching package format does not imply identical available functions. See the [parity guide][metasalmonpy-parity].

For Chapter 7's optional code-run export and catalog planning, install the pinned release with its `knb` extra, which includes EML support:

```bash
python -m pip install \
  "metasalmonpy[knb] @ https://github.com/salmon-data-mobilization/metasalmonpy/archive/refs/tags/v0.4.0.tar.gz"
```

If a dependency cannot be installed on your machine, use the supplied checkpoint and work with a partner for the affected command. Keep participating in the interpretation and review activities.

## AI comparison and optional live access

**Everyone completes the human–AI comparison using the supplied recorded outputs.** They are material to critique, not accepted definitions. This route needs no account and does not make a network request.

For optional live practice, choose one of these routes before the workshop:

- **OpenRouter free router:** create your own account and API key, then keep the supplied script's model fixed to `openrouter/free`. This router selects an available free model; record the actual responding model returned with the output. Use no paid model fallback. No credit purchase is part of the workshop. Free models have availability and rate limits; if access fails or requests a purchase, use the supplied outputs. See the [free-router documentation][openrouter-free] and review the provider's data-handling terms before sending context.
- **Ollama local model:** follow the [Ollama quickstart][ollama-quickstart] to install a local model suitable for your computer. Download it before the workshop. This optional route needs local disk space and compute; the supplied outputs remain the common comparison if setup is incomplete.

Keep API keys in a local credential store or session environment, never in a worksheet, script, shared notebook, screenshot, or repository. Live LLM review requires an explicit `llm_assess = TRUE` / `llm_assess=True`; providing context paths alone must not enable it. Review only the supplied public workshop material with an external provider.

## Day 2 tools and preparation

Day 2 uses the same reviewed human graph and dictionary. Work through [Chapters 8–12](advanced.html) with a plain-text editor and the `semantic-lab/` worksheets. Spreadsheet participants can edit the concept and mapping tables and review the generated Turtle with a partner. R users can use their editor for these files; RDF validation is an additional tool, not a new metasalmon API.

For the optional local code checks, use **Python 3.9 or newer** in a separate environment. Install the pinned RDF parser and limited rule reasoner before the class:

```bash
python3 -m venv .venv-semantic
. .venv-semantic/bin/activate
python -m pip install -r semantic-lab/scripts/requirements.txt
```

The file pins `rdflib==7.1.4`, `owlrl==7.1.4`, and `pyshacl==0.30.1`. On Windows use `.venv-semantic\Scripts\Activate.ps1`. After installation, the lab checks read local files and make no network requests. They demonstrate selected inference rules and SHACL checks; they do not perform complete OWL DL consistency checking or prove source meanings correct. Run the command documented in Chapter 10 and the [semantic lab guide](files/fraser-coho-workshop/semantic-lab/README.html), or inspect the supplied result with a partner. Keep execution and inspection distinct in your notes.

All Day 2 namespaces and releases remain teaching drafts. No GitHub account, shared-term submission, vocabulary hosting, or new inference service is needed.

## Before you arrive

- Confirm that the extracted kit opens and that the source has 173 rows and 14 columns.
- Locate the worksheets, source notes, recorded AI outputs, and three checkpoints in the kit README.
- Open the [Glossary](glossary.html) and [Field reference](field-reference.html).
- If using code, check that your pinned package imports and your editor starts in `fraser-coho-workshop/`.
- Read the [teaching-record status](reference.html#teaching-record). A Test Node demonstration and a software check do not establish domain approval or production publication.
