"""Maintainer/CI regression check of supplied drafts; no human review claimed.

Run from the kit root. This is not the learner exercise command. It deliberately
inspects the distributed references while the distributed human worksheet is
still pending. It never completes the worksheet or creates a learner artifact.
"""
import json
import sys
from lab_common import LAB
import check_model
import check_bridge


def main():
    try:
        results = {
            "status": "passed-reference-regression-checks",
            "human_review": "pending; not performed or simulated",
            "model": check_model.check(LAB / "model/model.ttl",
                                       LAB / "model/instances.ttl",
                                       LAB / "model/record-shapes.ttl", reference_only=True),
            "bridge": check_bridge.check(LAB / "bridge/bridge.ttl", reference_only=True),
        }
    except Exception as error:
        print(f"FAILED reference check: {error}", file=sys.stderr)
        return 1
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
