# Validation and delivery status

Observed on 2026-09-08. The workshop is an implemented teaching draft; the full
scientific/publication acceptance criteria are **not all complete**.

| Check | Observed outcome |
| --- | --- |
| Fixed source and package checkpoints | All retain 173 rows, 14 columns, 164 population–year pairs and the original CSV bytes. |
| Human artifacts | Complete working graph/dictionary/decomposition examples and blank learner review forms supplied. Bruno and Tom's scientific review is pending. |
| R learner build and review validation | Passed using metasalmon v0.5.0, exact tag `af84689df5d6365c1abaa49f8cd9012cbe8494c5`, R 4.5.2. |
| Python learner build and review validation | Passed using exact metasalmonpy v0.4.0 tagged source, Python 3.14 and pandas 3.0.5. |
| Preparation and overwrite guards | Passed isolated negative/positive checks in both lanes; mechanical fixtures did not claim human approval. |
| Optional AI script behavior | Offline mocks verified fixed free routing, eight-attempt maximum, counted failures and explicit unsuccessful status. |
| Reference strict MetaSalmon/EML/test preview | R strict checks and EML 2.2.0 validation passed; expanded TEST dry-run artifacts included. See `reference-validation.json` for final lane export results. |
| Independent SDP specification validator | **Blocked** by its known exact-comparison mismatch over semantic properties in descriptor fields. The semantic annotations remain intact; no validator bypass is shipped. |
| Required AI comparison without credentials | Available using an actual, identified Codex authoring-assistant recording and blank human decision worksheet. It is not native OpenRouter output. |
| Site and navigation | Sandpaper 0.20.2 rendering passed locally; lesson links, glossary anchors, diagrams, downloads and R/Python/Spreadsheet tabs were checked. Varnish 1.1.1 has missing incubator favicon assets and a narrow-header layout limitation; these are reported separately from lesson-content checks. |
| Live OpenRouter/free rehearsal | **Blocked:** one HTTP 401 request, no response, no retries. Successful free inference and its request consumption remain unverified. |
| Public KNB test endpoint | **Not created or verified.** Only a dry-run plan exists; test credentials and remaining review/validation work are needed. |
| Production publication / DOI | Neither performed nor included in the execution. |

`lane-smoke.json` records the 28 isolated checks, expected refusals, versions
and script hashes. It is evidence about those executions, not a claim that all
operating systems, provider responses or scientific interpretations were tested.

Two unposted upstream issue drafts preserve observed defects without altering
package APIs or schemas:

- `upstream-validator-issue.md`: canonical descriptor semantic fields rejected
  by the independent validator's comparison.
- `unseeded-code-iri-issue.md`: the pinned unseeded build can prefill code IRIs;
  the workshop helper clears those assignments before the review exercise.

The workshop's distribution check does not replace strict SDP validation:

```text
python3 scripts/build-workshop-kit.py
python3 scripts/check-workshop.py
python3 scripts/check-workshop.py --site site/docs
```

These commands run from the workshop repository, where `scripts/` contains
maintainer utilities. Learner scripts run from the extracted kit instead.
Use the independent specification validator command in its issue draft and
retain its actual failure until an upstream fix is validated.

Before delivery, obtain the scientific review through Brett, resolve that
validator defect, rehearse the free provider with working access and verify the
separate public Test Node record anonymously. Then update status from the
actual evidence. There is no fixed September completion deadline.

## Day 2 reference checks

`day2-reference-checks.json` records the local technical inspection of the distributed vocabulary, model and bridge. The maintainer command is `python scripts/check-semantic-lab.py` from the lesson repository, using the pinned dependencies in the kit's `semantic-lab/scripts/requirements.txt`. The result records checked input hashes. Re-run it after changing these artifacts, regenerate the receipt, then rebuild the kit inventory and ZIP.

The vocabulary check covers the fixed four-concept teaching selection and its source bindings. Model and bridge checks cover selected OWL RL consequences, actual SHACL conditions, and explicit error examples. This is not complete OWL DL verification, a new general-purpose ontology validator, or independent scientific approval. No learner review is simulated by the reference command; learner commands separately require their actual Day 1 preparation.

The Chapter 12 preview receipt is under `semantic-lab/contributions/`. It records the actual pinned R/Python candidate rendering, not a confirmed ontology gap or submitted request. Day 2 does not depend on a live catalog or AI service and does not close the outstanding Day 1 publication and review conditions above.

On 2026-09-08, a disposable, explicitly automated mechanical fixture also exercised the learner vocabulary CLI and both contribution preview CLIs after their preparation gate. The vocabulary passed with four concepts, three definitions and one explicit definition gap. R 4.5.2 / metasalmon 0.5.0 and Python 3.14.3 / metasalmonpy 0.4.0 each rendered two candidate rows and two local request previews. Both refused a second run into existing output without changing its bytes; the source and reference artifacts stayed unchanged. This fixture was not distributed and does not represent a human peer review. The supplied learner worksheets remain uncompleted.
