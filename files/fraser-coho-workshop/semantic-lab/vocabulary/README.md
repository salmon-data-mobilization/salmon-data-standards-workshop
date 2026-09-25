# Local teaching vocabulary: four NuSEDS estimate-method categories

These are draft teaching artifacts prepared by the Codex workshop-authoring
assistant. They have not been independently scientifically reviewed, adopted
by DFO or approved by the Salmon Domain Ontology stewards.

## Files and use

| File | Purpose |
| --- | --- |
| `estimate-methods.ttl` | Worked SKOS scheme with four concepts, three supported definition paraphrases and one explicit definition gap |
| `concepts-working.csv` | Source bindings, definitions, scope, evidence and review questions behind that Turtle |
| `routing-decisions-working.csv` | Seven worked scope/representation decisions for Chapter 8 |
| `stewardship-working.md` | Proposed responsibilities and change policy; actual reviewers and adoption decisions remain unset |
| `provenance.json` | Exact source-byte hashes, dates and the full SDO commit used |
| `check_vocabulary.py` | Bounded local structural and source-binding check; it does not assess scientific truth |

Complete the worksheets in `../worksheets/` before comparing the worked answers.
Save the learner's edited Turtle in `output/semantic-lab/estimate-methods.ttl`
from the extracted workshop-kit root. Preserve
the reference and all 173 source rows. This selection is not the complete
nine-value ESTIMATE_METHOD code list and does not replace package codes.csv.

## Representation and evidence boundaries

The scheme and its concepts use the teaching-only namespace
`https://example.org/fraser-coho-workshop/terms/`. These identifiers are not
production identifiers or resolving vocabulary pages. The source strings stay
in `code_value`; the CSV pair `source_column` + `code_value` binds each concept
to the unchanged data. Human-readable labels retain the exact source spelling.

The four concepts are `area-under-the-curve`, `combined-methods`,
`fixed-site-census` and `resistivity-counter`. None is an OWL class. The scheme is
`estimate-method-scheme`. No hierarchy, synonym or cross-vocabulary mapping is
asserted. In particular, the source does not make Combined Methods the parent
of its possible constituent methods.

The preserved official dictionary defines three selected procedures but gives
Resistivity Counter an N/A entry. Its concept therefore has scope and editorial
notes but no skos:definition. This omission is a documented source gap, not a
definition of the method or an invitation to infer one.

The current official dictionary was retrieved on 2026-09-08 and may postdate
the 2025 source workbook. Definition paraphrases and questions can be checked
against `../../raw_data/official-nuseds-dictionary.csv`, field ESTIMATE_METHOD,
and `../../reference/code-definitions-working.csv`.

SDO guidance is pinned to commit
`d45f8f7cc857d92af8bbe54a7c89b2a4a14784b2`: CONVENTIONS sections 2–4, 10–12 and
ontology/views/README.md. The shared core and the optional metamodel views have
different authority; the latter support orientation and do not approve this
source-specific model. No SDO files are changed by these exercises.

## Run the bounded check

After the actual Day 1 preparation and peer review, run from the extracted
workshop-kit root in the Day 2 Python environment (rdflib 7.1.4):

```sh
python semantic-lab/vocabulary/check_vocabulary.py
```

The default inputs are the learner worksheet and copied Turtle. The program
reuses `scripts/workshop.py` for the existing human-preparation gate. It reads
local files only, does not resolve source URLs or ontology imports, and writes
no files. It compares the four selected source bindings, CSV/TTL descriptions,
labels, types and explicit definition-gap record. A successful result describes
these checks only; scientific and adoption decisions remain separate.

Maintainers can import `validate_vocabulary()` to inspect the supplied reference
files independently. That reference check does not pass the learner preparation
gate or establish classroom completion. No fake reviewer should be entered to
make an authoring check pass.
