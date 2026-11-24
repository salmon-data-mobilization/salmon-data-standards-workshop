"""Optional free-only live Chapter 5 exercise; no paid fallback or purchase."""
import datetime
import hashlib
import json
import os
import re
from pathlib import Path
import urllib.error
import urllib.request
import metasalmonpy as ms
from workshop import PACKAGE, SOURCE, check_preparation

check_preparation()
if not os.environ.get("OPENROUTER_API_KEY"):
    raise SystemExit("No free key configured. Use ai/README.md and recorded assessments instead.")
pkg = ms.read_salmon_datapackage(str(PACKAGE))
dictionary = pkg["dictionary"].loc[pkg["dictionary"].column_name == "NATURAL_ADULT_SPAWNERS"].copy()
for field in ("term_iri", "property_iri", "entity_iri", "unit_iri", "constraint_iri", "statistical_modifier_iri"):
    dictionary[field] = ""
context = [str(Path("worksheets") / name) for name in ("dataset-nodes.csv", "dataset-edges.csv", "data-dictionary.csv", "variable-decomposition.csv")]
out = Path("output") / ("ai-live-python-" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S"))
out.mkdir(parents=True, exist_ok=False)
records = []
attempts = 0


def free_request(messages, config):
    global attempts
    if config["provider"] != "openrouter" or config["model"] != "openrouter/free":
        raise ValueError("Only openrouter/free is permitted.")
    if attempts >= 8:
        raise ValueError("Workshop request limit reached; continue with recorded assessments.")
    attempts += 1
    body = {"model": "openrouter/free", "messages": messages, "temperature": 0,
            "max_tokens": 2500, "response_format": {"type": "json_object"}}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"]})
    payload = None
    status = 0
    parse_error = False
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            status = response.status
            try:
                payload = json.load(response)
            except (ValueError, UnicodeDecodeError):
                parse_error = True
    except urllib.error.HTTPError as error:
        status = error.code
    except (urllib.error.URLError, TimeoutError):
        status = 0
    record = {"attempt": attempts, "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "request": body, "http_status": status, "parse_error": parse_error}
    if status == 200:
        record["response"] = payload
    records.append(record)
    (out / "requests.json").write_text(json.dumps(records, indent=2) + "\n")
    if status != 200:
        raise RuntimeError(f"Free model request failed, HTTP {status}. Use saved assessments if unavailable.")
    if parse_error or payload is None:
        raise ValueError("Free model returned invalid response JSON; request was counted.")
    content = payload["choices"][0]["message"].get("content") or ""
    content = re.sub(r"^```(?:json)?\s*", "", content.strip())
    content = re.sub(r"\s*```$", "", content)
    return json.loads(content)


result = ms.suggest_semantics(df=pkg["resources"], dict_df=dictionary, sources=["smn", "gcdfo"],
    max_per_role=3, llm_assess=True, llm_provider="openrouter", llm_model="openrouter/free",
    llm_api_key=os.environ["OPENROUTER_API_KEY"], llm_top_n=3, llm_context_files=context,
    llm_request_fn=free_request)
for attribute, filename in (("semantic_suggestions", "suggestions.csv"), ("semantic_llm_assessments", "assessments.csv")):
    evidence = result.attrs.get(attribute)
    if evidence is not None:
        evidence.to_csv(out / filename, index=False)
assessments = result.attrs.get("semantic_llm_assessments")
successful = 0 if assessments is None or assessments.empty else int((
    assessments["llm_decision"].fillna("").ne("") & assessments["llm_error"].fillna("").eq("")
).sum())
(out / "provenance.json").write_text(json.dumps({
    "kind": "live-provider-recording", "package": "metasalmonpy", "version": ms.__version__,
    "requested_model": "openrouter/free", "actual_http_attempts": attempts,
    "successful_assessment_rows": successful,
    "rehearsal_status": "response-recorded-needs-human-review" if successful else "failed-no-successful-assessment",
    "context_sha256": {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in context},
    "source_csv_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "note": "Provider responses and package decisions are proposals, not human approval. Actual routed model IDs are in requests.json when returned."
}, indent=2) + "\n")
print(f"Saved {attempts} HTTP attempts and {successful} successful assessment rows at {out}.")
if not successful:
    raise SystemExit("No successful AI assessment was returned. Retain the failure receipt and use the recorded comparison activity.")
print("Compare the recorded response against the human model before any application.")
