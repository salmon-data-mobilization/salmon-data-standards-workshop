# Fraser Coho workshop kit

Use this directory as your project root. The **Day 1 beginner sequence (six hours)** is:
inspect → diagram → dictionary and decomposition → peer review → package →
semantic and AI review → codes → validation and KNB test demonstration.

**Day 2 (six hours)** continues from the same human model: choose reuse or local/shared contribution → build a SKOS vocabulary → formalize a small OWL model → assess bridges → draft term requests and review plans. Start with [the semantic lab guide](semantic-lab/README.html). These are classroom drafts; their identifiers, mappings and passing checks do not confer shared or organizational authority.

The source is **173 rows and 14 columns**, including 13 blank adult-spawner
estimates and repeated population–year pairs. Every checkpoint preserves the
source CSV bytes. Do not rename fields, replace blanks, deduplicate or aggregate.

## Start here

1. Read `raw_data/PROVENANCE.md` and inspect the six introductory columns.
2. Draw the relationships and complete `worksheets/dataset-nodes.csv` and
   `worksheets/dataset-edges.csv` as text companions to your drawing.
3. Write the six core entries in `worksheets/data-dictionary.csv`; review the
   other eight supplied draft entries. Decompose the adult-spawner estimate in
   `worksheets/variable-decomposition.csv`.
4. Ask a peer to review the actual artifacts. Record their name, date, revisions
   and remaining questions in `worksheets/peer-review.md`. Only then change its
   completion marker. A question can remain explicit in a reviewed draft.
5. Follow Chapter 4 using `scripts/build_sdp.R` or `scripts/build_sdp.py`.
   Spreadsheet participants inspect the supplied same-source checkpoint with
   a collaborator running its automated checks.
6. Review saved vocabulary candidates, then complete `ai/comparison-worksheet.csv`
   against the recorded AI assessment. Live inference is optional.
7. Inspect the reference package and run Chapter 7's test-only preview on a
   separate local copy. Read `validation/README.md` for current limitations.
8. Continue in `semantic-lab/` for Chapters 8–12. Preserve your actual human preparation and create answers under `output/semantic-lab/`, following each chapter. The supplied examples remain separate draft evidence. No online service is needed for Day 2 after installing optional checking dependencies.

The scripts check that preparation artifacts exist and have usable structure.
They cannot establish whether a person performed a sound scientific review.
Do not fill a fictional reviewer name to bypass preparation.

## Contents

| Location | Purpose |
| --- | --- |
| `raw_data/` | Immutable source slice, original starter dictionary, current official dictionary, acquisition and derivation evidence. |
| `worksheets/` | Learner graph tables, interpretation dictionary, decomposition and peer review. |
| `reference/` | Working examples, editable conceptual diagram and scientific review packet. These are drafts awaiting Bruno and Tom. |
| `scripts/` | Pinned R/Python learner workflows, with preparation and source checks. |
| `checkpoints/draft-sdp/` | Structure and working descriptions; no accepted semantic IRIs. |
| `checkpoints/seeded-sdp/` | Same draft plus real saved deterministic candidates; no AI calls or applied decisions. |
| `checkpoints/reference-sdp/` | Explicit technical semantic selections, vocabulary evidence, valid EML and test dry-run objects; scientific review remains pending. |
| `ai/` | Actual recorded authoring-assistant assessment, blank human comparison worksheet and optional live instructions. |
| `publication/` | Public test-record status and maintainer completion steps. |
| `validation/` | Observed checks, capability gaps and unposted upstream issue drafts. |
| `semantic-lab/` | Day 2 worksheets, draft SKOS vocabulary, RDF/OWL model, bridges, contribution examples and offline checks. These are context artifacts outside canonical SDP metadata. |

`output/` is created when you work. Existing output directories are not replaced
by the build scripts. Keep your team's answers separate from the supplied
working examples. Do not treat a supplied example as your team's peer review.

## What has and has not been reviewed

The scientific answer key is **not yet reviewed by Bruno and Tom**. Their
decisions must come through Brett and be recorded in the review packet. Source
wording, working interpretations, technical mapping selections and independent
scientific approval are different records.

The source's original publisher is Fisheries and Oceans Canada. The teaching
materials are a derivative workshop, not a replacement source publication or
DFO endorsement. Source data are under the Open Government Licence – Canada;
workshop prose follows the repository's CC BY 4.0 licence.

The public KNB test destination is not yet verified. The local manifest is a
dry-run plan, not proof of upload. No production publication or DOI request
is included in this workshop. Check `publication/README.md` before delivery.
