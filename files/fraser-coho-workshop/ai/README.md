# Offline AI evaluation for the Fraser Coho workshop

This folder lets every attendee complete the required AI-comparison exercise
without buying API credits or making a live inference request. Complete the
human diagram, dictionary/decomposition and actual peer review first.

## What is recorded

- `recorded-assessment.md`: an actual Codex workshop-authoring assistant
  assessment, with its authorship, timestamp, evidence and limits.
- `recorded-suggestions.csv`: the assessment's candidate propositions and
  recommended accept/revise/reject dispositions. Rejected alternatives are
  explicitly labelled as such.
- `comparison-worksheet.csv`: the learner's blank decision/reason record,
  including fields for evidence, revisions, reviewer and review date.

These are workshop teaching artifacts. They are **not native
`semantic_llm_assessments` or `semantic_suggestions.csv` outputs**, and should
not be passed to package functions that expect those schemas. Do not relabel
them as OpenRouter output, a successful package API run, or scientific approval.

## Complete the exercise offline

1. Keep your human graph and dictionary beside the unchanged source and saved
   official dictionary and `reference/metamodel-source-notes.md`. Use the original
   kit sources matching the recording.
2. Read the recorded assessment and one proposition at a time. Its
   recommendation is advice to test, not a decision already made for you.
3. Enter your own `human_decision` as accept, revise or reject. Give a reason,
   name the evidence you checked and describe any graph/dictionary revision.
   If evidence is missing, explain the unresolved issue instead of asserting a
   final mapping.
4. Have a peer compare at least one agreement and one disagreement. Record the
   actual reviewer/date when that comparison occurs.
5. Carry only your reviewed decisions into later mapping work. Keep rejected
   alternatives and open questions in the evidence trail.

All 13 proposals can be read without network access. The focus set for a short
comparison is AI02 (natural origin), AI04 (activity/result), AI05 (year basis),
AI07 (method), AI08 (missingness) and AI10 (repeated records). AI01 and AI03 provide
supported working interpretations to compare with the rejected alternatives.

## Live inference is a separate optional extension

A live free-provider API attempt is recorded separately by the workshop scripts.
A failed request is evidence of a failed request. This authoring-assistant
recording supplies the required evaluation activity; it is not proof of live
provider availability, native-package behavior or a response to a learner's
later edits. Fresh inference must stay clearly labelled and pass its own setup
and source-sharing checks.

Read [live-rehearsal-status.json](live-rehearsal-status.json) for the actual
preparation-run outcome. An available account or key does not establish that a
model response succeeded.

For the optional live lane, create your own free OpenRouter account/key as
described in the lesson Setup. Make the key available only to the current
session through the `OPENROUTER_API_KEY` environment variable. Do not enter it
into a kit file. From the project root, deliberately running
`scripts/review_ai.R` in R or `python scripts/review_ai.py` opts into the
package's `llm_assess` step. Inspect the four worksheet context files and the
script first. It uses only `openrouter/free`, caps actual HTTP attempts at eight,
and saves the submitted requests and returned evidence under a new `output/`
directory. It never applies a response to package metadata or purchases credits.

If the key or free route is unavailable, use the required offline comparison.
Do not purchase credits or substitute a paid model to complete this exercise.

No API credentials are included in these files. The local learner worksheet has
blank human-review fields; completing it requires an actual human decision.

## Optional OpenRouter setup and rehearsal

Instructions checked on 2026-09-08 against the
[official free-router documentation](https://openrouter.ai/docs/guides/routing/routers/free-router).
Create a personal free account and API key at OpenRouter. No credit purchase is
required by this workshop. Configure `OPENROUTER_API_KEY` in your session
environment with your usual local credential tool. Do not save its value in
the project, a command history, output file or screenshot.

After the human checkpoint and Chapter 4 build, run either:

```text
Rscript scripts/review_ai.R
python scripts/review_ai.py
```

The scripts use the packages' existing OpenRouter provider configuration with
the fixed model `openrouter/free`. They assess only the adult-spawner column
using the source context and text node/edge tables. They never send the drawing
image or claim the package can interpret it. The provider routes to an available
free model; its returned `model` identifies the actual responder.

The packages select context excerpts for the request; passing a file does not
guarantee every line reaches the model. Inspect `requests.json` and the returned
`llm_context_sources` to see which graph/dictionary passages were actually used.
Missing relationship context is itself something to flag in your evaluation.

A public request callback counts every actual HTTP attempt, including any
package retry, up to eight requests. There are no automatic HTTP retries and
no paid fallback. Each attempt retains a timestamp, request payload and status;
only successful response bodies are retained. The output includes candidates,
assessment rows and provenance in a new `output/ai-live-*` directory. Inspect
all of these before changing metadata. Repeated errors, an exhausted quota or
an unsuitable response are reasons to continue with the recorded activity.

`live-rehearsal-status.json` records the current measured attempt: one R request,
HTTP 401, no successful model output and no retries. The configured credential
was rejected, so successful-run request consumption remains unmeasured. Python
was not sent another live request with the same rejected credential. Before
delivery, rehearse both lanes with working personal free access and retain the
actual request count, retries, routed model and success/failure status. Free
availability and limits can change; recheck the official instructions then.

## Optional local Ollama extension

The shared exercise still uses the recorded assessment. An experienced
facilitator can separately test a downloaded local model using
[Ollama's OpenAI-compatible endpoint](https://docs.ollama.com/api/openai-compatibility).
In the packages this is the existing `openai_compatible` provider, not a new
`ollama` provider. Use `llm_base_url = "http://localhost:11434/v1"`, the name of a
model actually installed locally, and the non-secret placeholder key `ollama`
required by the client configuration. Pass the same restricted dictionary and
text context, and opt in explicitly with `llm_assess = TRUE` (Python: `True`).

Do not modify the fixed free-only callback in `review_ai.R`/`.py` to do this;
make a separate, clearly labelled local experiment. Confirm the endpoint is
local and inspect its response format before using it in a class. This optional
extension was not rehearsed here because no local Ollama service was available.
