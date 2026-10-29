"""Validate a draft, or pass --strict for the final SDP gate."""
import sys
import metasalmonpy as ms
from workshop import PACKAGE, check_preparation
check_preparation()
args = sys.argv[1:]
strict = "--strict" in args
paths = [arg for arg in args if arg != "--strict"]
validation = ms.validate_salmon_datapackage(paths[0] if paths else str(PACKAGE), require_iris=strict)
print(validation["issues"])
print(validation["semantic_validation"]["issues"])
if not validation["issues"].empty:
    raise SystemExit("Validation reported issues; resolve them before continuing.")
print("SDP validation passed. This does not establish scientific approval or EML readiness.")
