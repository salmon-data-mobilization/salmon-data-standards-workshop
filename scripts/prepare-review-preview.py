#!/usr/bin/env python3
"""Build a committed lesson revision and package it for a shared Netlify preview.

Only prepares local files. Publishing and updating the PR are separate steps.
Uses a disposable normal clone because Sandpaper 0.20.2 cannot build in a Git
worktree whose .git is a file. No generated files are written to the checkout.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED


def run(command, cwd, **kwargs):
    return subprocess.run(command, cwd=cwd, check=True, text=True, **kwargs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="HEAD", help="Committed revision to preview")
    parser.add_argument("--output", type=Path, help="New output directory; default: temporary directory")
    parser.add_argument(
        "--installed-packages", action="store_true",
        help="Use installed R packages instead of the lesson renv profile; recorded in the receipt",
    )
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    commit = run(
        ["git", "rev-parse", "--verify", "--end-of-options", f"{args.ref}^{{commit}}"],
        repo, capture_output=True,
    ).stdout.strip()
    if args.ref == "HEAD" and run(
        ["git", "status", "--porcelain", "--untracked-files=no"], repo, capture_output=True,
    ).stdout.strip():
        parser.error("Commit tracked changes first, or use --ref to select an explicit committed revision.")

    if args.output:
        output = args.output.resolve()
        output.mkdir(parents=True, exist_ok=False)
    else:
        output = Path(tempfile.mkdtemp(prefix="salmon-workshop-preview-"))
    lesson = output / "lesson"
    log = output / "build.log"
    print(f"Building {commit}\nOutput: {output}\nLog: {log}", flush=True)

    # A fresh clone prevents old generated pages or uncommitted source changes
    # from being silently included in a preview labelled with a commit hash.
    with log.open("w") as stream:
        common = {"stdout": stream, "stderr": subprocess.STDOUT}
        run(["git", "clone", "--no-hardlinks", "--no-checkout", str(repo), str(lesson)], repo, **common)
        run(["git", "checkout", "--detach", commit], lesson, **common)
        run([sys.executable, "scripts/check-workshop.py"], lesson, **common)
        r_code = '''
options(sandpaper.use_renv = Sys.getenv("WORKSHOP_PREVIEW_INSTALLED") != "1")
# Reset before installing the template override; rebuild=TRUE would erase it.
sandpaper::reset_site(".")
source("scripts/prepare-site.R")
sandpaper::check_lesson()
sandpaper::build_lesson(rebuild = FALSE, preview = FALSE)
writeLines(c(paste("R", getRversion()),
             paste("sandpaper", packageVersion("sandpaper")),
             paste("varnish", packageVersion("varnish"))),
           "../build-environment.txt")
'''
        environment = os.environ.copy()
        environment["WORKSHOP_PREVIEW_INSTALLED"] = "1" if args.installed_packages else "0"
        run(["Rscript", "--vanilla", "-e", r_code], lesson, env=environment, **common)
        run([sys.executable, "scripts/check-workshop.py", "--site", "site/docs"], lesson, **common)

    site = lesson / "site/docs"
    if not (site / "index.html").is_file():
        raise RuntimeError("The build did not produce site/docs/index.html")
    files = sorted(path for path in site.rglob("*") if path.is_file())
    if any(path.is_symlink() for path in site.rglob("*")):
        raise RuntimeError("Refusing to package a site containing symlinks")
    receipt = {
        "repository": "https://github.com/salmon-data-mobilization/salmon-data-standards-workshop",
        "commit": commit,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "package_mode": "installed" if args.installed_packages else "lesson-renv",
        "toolchain": (output / "build-environment.txt").read_text().splitlines(),
        "checks": ["check-workshop.py", "sandpaper::check_lesson()", "check-workshop.py --site site/docs"],
        "file_count": len(files),
    }
    archive = output / f"workshop-preview-{commit[:12]}.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
        for path in files:
            bundle.write(path, "public/" + path.relative_to(site).as_posix())
        bundle.writestr("public/_preview.json", json.dumps(receipt, indent=2) + "\n")
        # Netlify Drop auto-detects the rendered config.yaml as Hugo. Explicit
        # configuration serves the finished pages without rebuilding the lesson.
        bundle.writestr("netlify.toml", '''[build]
  command = "echo Serving pre-rendered workshop preview"
  publish = "public"

[[headers]]
  for = "/*"
  [headers.values]
    X-Robots-Tag = "noindex"
''')
    manifest = {
        **receipt,
        "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
        "files": {
            path.relative_to(site).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in files
        },
    }
    (output / "preview-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Ready to upload: {archive}\nCommit: {commit}\nReceipt: {output / 'preview-manifest.json'}")
    print("Publish and verify this bundle using docs/entrypoints.md#shared-review-previews.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"Preview preparation failed: {error}. Inspect build.log in the reported output directory.", file=sys.stderr)
        sys.exit(1)
