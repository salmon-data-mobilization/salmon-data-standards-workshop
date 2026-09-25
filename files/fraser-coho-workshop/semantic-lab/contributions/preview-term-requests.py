"""Local candidate/text preview; run from the workshop root after preparation."""
from pathlib import Path
import sys
import pandas as pd
import metasalmonpy as ms

sys.path.insert(0, str(Path("scripts").resolve()))
from workshop import check_preparation

if ms.__version__ != "0.4.0":
    raise RuntimeError("Use the workshop's pinned metasalmonpy 0.4.0 release.")
check_preparation()
destination = Path("output") / "term-request-preview-python"
if destination.exists():
    raise FileExistsError("Preview folder exists; preserve it and choose a new destination in this script.")
suggestions = pd.read_csv("checkpoints/seeded-sdp/semantic_suggestions.csv")
gaps = ms.detect_semantic_term_gaps(suggestions=suggestions)
previews = ms.render_ontology_term_request(
    gaps, scope="auto", ask=False,
    profile_name="fraser-coho-workshop-draft",
)
destination.mkdir(parents=True)
gaps.to_csv(destination / "candidate-gaps.csv", index=False)
for i, row in enumerate(previews.itertuples(index=False), start=1):
    (destination / f"request-{i:02d}.md").write_text(
        "# SOFTWARE PREVIEW: not a reviewed gap or submitted request\n\n"
        + row.request_title + "\n\n" + row.request_body + "\n",
        encoding="utf-8",
    )
print(f"{len(gaps)} candidate rows; {len(previews)} local request previews. Review against your source evidence.")
