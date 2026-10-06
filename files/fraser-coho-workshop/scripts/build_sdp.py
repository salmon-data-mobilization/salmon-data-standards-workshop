"""Chapter 4: run from the extracted fraser-coho-workshop project root."""
import shutil
import metasalmonpy as ms
from workshop import PACKAGE, check_preparation, read_source, fill_metadata, write_package

if ms.__version__ != "0.4.0":
    raise RuntimeError("Use the workshop's pinned metasalmonpy 0.4.0 release.")
human = check_preparation()
raw = read_source()
if PACKAGE.exists():
    raise FileExistsError("A package exists. Review it or choose a new versioned output folder; no overwrite was performed.")
# Human preparation precedes inference. Seeding and AI remain off here.
ms.create_sdp({"escapement": raw}, path=str(PACKAGE), dataset_id="fraser-coho-workshop",
              table_id="escapement", seed_semantics=False, llm_assess=False,
              check_updates=False, overwrite=False)
pkg = fill_metadata(ms.read_salmon_datapackage(str(PACKAGE)), human)
write_package(pkg, PACKAGE, overwrite=True)  # only the draft just created above
shutil.copyfile("worksheets/peer-review.md", PACKAGE / "preparation-review.md")
print("Draft created. Missing semantic IRIs are expected until Chapter 5.")
