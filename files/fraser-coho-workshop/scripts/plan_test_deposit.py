"""Chapter 7: credential-free TEST plan only, with no live-upload switch."""
import sys
from pathlib import Path
import metasalmonpy as ms
from workshop import check_preparation
check_preparation()
if len(sys.argv) != 2:
    raise SystemExit("Supply a separate local reference-package copy under output/.")
path = Path(sys.argv[1]).resolve()
if not path.is_relative_to(Path("output").resolve()) or path == Path("output").resolve():
    raise SystemExit("Use a separate package copy under output/ before this exercise.")
validation = ms.validate_salmon_datapackage(str(path), require_iris=True)
if not validation["issues"].empty:
    raise SystemExit("Resolve strict SDP issues first.")
ms.write_eml_from_sdp(str(path), knb_environment="test", overwrite=True)
plan = ms.publish_sdp_to_knb(str(path), public=True, dry_run=True,
    representation="expanded", knb_environment="test", overwrite=True)
print(plan)
print("TEST dry run only; no objects uploaded and no production action performed.")
