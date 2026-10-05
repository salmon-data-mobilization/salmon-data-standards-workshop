#!/usr/bin/env python3
"""Trusted workflow_run publisher. Treat every artifact byte as untrusted data.

Standard library only. Run this file from a reviewed default-branch commit.
Never extract the archive, execute its scripts or load its configuration.
"""

import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import sys
import time
from urllib.error import HTTPError
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import uuid
from zipfile import ZipFile

REPOSITORY = "salmon-data-mobilization/salmon-data-standards-workshop"
WORKFLOW = ".github/workflows/workshop-preview-build.yml"
MAX_ARCHIVE = 100 * 1024 * 1024
MAX_TOTAL = 250 * 1024 * 1024
MAX_FILE = 50 * 1024 * 1024
MAX_FILES = 20000
SHA = re.compile(r"[0-9a-f]{40}")
SAFE_PATH = re.compile(r"[A-Za-z0-9_./+ @()-]+")
# Exact inert marker files produced by the existing workshop build. No other
# hidden paths are accepted, and these bytes must match the reviewed values.
STATIC_MARKERS = {
    "files/fraser-coho-workshop/checkpoints/" + checkpoint + "/.metasalmon-package":
        b"metasalmon-owned\n"
    for checkpoint in ("draft-sdp", "reference-sdp", "seeded-sdp")
}


class PreviewValidationError(ValueError):
    """A fixed diagnostic written by this trusted publisher, never remote data."""


def require(condition, message):
    if not condition:
        raise PreviewValidationError(message)


def failure_message(error):
    # Only require()'s fixed messages are safe to expose. Other exceptions can
    # contain API response bodies, credentials, signed URLs or archive contents.
    detail = str(error) if isinstance(error, PreviewValidationError) else type(error).__name__
    return "Preview publication stopped: " + detail + ". No success status was posted."


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(url, token=None, method="GET", data=None,
            content_type="application/json", limit=10 * 1024 * 1024):
    """Never forward a credential through an HTTP redirect."""
    headers = {"User-Agent": "workshop-preview-publisher",
               "Accept": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    if data is not None:
        headers["Content-Type"] = content_type
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with build_opener(NoRedirect()).open(req, timeout=60) as response:
            body = response.read(limit + 1)
            require(len(body) <= limit, "Response exceeds size limit")
            return body
    except HTTPError as error:
        # GitHub's artifact endpoint returns a short-lived signed URL. Fetch it
        # separately, with NO Authorization header and no further redirects.
        if (error.code == 302 and method == "GET" and token and
                url.startswith("https://api.github.com/repos/" + REPOSITORY +
                               "/actions/artifacts/") and url.endswith("/zip")):
            target = error.headers.get("Location", "")
            parsed = urlsplit(target)
            require(parsed.scheme == "https" and parsed.hostname and
                    not parsed.username and not parsed.password and
                    parsed.port in (None, 443), "Unsafe artifact redirect")
            return request(target, limit=limit)
        # Do not print response bodies, credential-bearing URLs or headers.
        raise RuntimeError("API request failed with HTTP " + str(error.code)) from None


class API:
    def __init__(self, root, token):
        require(bool(token), "Missing API credential")
        self.root, self.token = root, token

    def call(self, path, method="GET", payload=None, raw=None):
        require(path.startswith("/") and not path.startswith("//"), "Invalid API path")
        require(payload is None or raw is None, "Ambiguous request body")
        data = json.dumps(payload).encode() if payload is not None else raw
        result = request(self.root + path, self.token, method, data,
                         "application/octet-stream" if raw is not None else "application/json")
        return json.loads(result) if result else None


def validate_run(run, event_run, workflow, repository_id):
    require(run["id"] == event_run["id"], "Wrong workflow run")
    require(run["run_attempt"] == event_run["run_attempt"], "Superseded run attempt")
    require(run["repository"]["id"] == repository_id and
            run["repository"]["full_name"] == REPOSITORY, "Wrong repository")
    require(workflow["path"] == WORKFLOW and
            run["workflow_id"] == workflow["id"], "Wrong build workflow")
    require(run["status"] == "completed" and run["conclusion"] == "success" and
            run["event"] == "pull_request", "Build is not a successful PR run")
    require(bool(SHA.fullmatch(run["head_sha"])), "Invalid build SHA")


def validate_pr(pr, run, repository_id):
    require(pr["state"] == "open" and not pr["draft"], "PR is closed or draft")
    require(pr["base"]["repo"]["id"] == repository_id and
            pr["base"]["repo"]["full_name"] == REPOSITORY and
            pr["base"]["ref"] == "main", "Wrong PR target")
    require(pr["head"]["sha"] == run["head_sha"], "PR has a newer revision")
    require(pr["head"]["repo"] and run["head_repository"] and
            pr["head"]["repo"]["id"] == run["head_repository"]["id"],
            "Wrong PR source repository")


def archive_files(blob, *, per_file=MAX_FILE, total_limit=MAX_TOTAL):
    """Read bounded regular files in memory; do not extract to the filesystem."""
    require(len(blob) <= MAX_ARCHIVE, "Archive too large")
    result, seen, total = {}, set(), 0
    with ZipFile(io.BytesIO(blob)) as archive:
        entries = archive.infolist()
        require(len(entries) <= MAX_FILES, "Too many archive entries")
        for entry in entries:
            name = entry.filename
            # ZipInfo truncates filenames at NUL; reject the original too.
            require(entry.orig_filename == name and len(name) <= 512 and
                    bool(SAFE_PATH.fullmatch(name)), "Unsafe archive filename")
            parts = name.rstrip("/").split("/")
            require(all(p not in ("", ".", "..") for p in parts), "Unsafe archive path")
            key = name.rstrip("/").casefold()
            require(key not in seen, "Duplicate archive path")
            seen.add(key)
            kind = stat.S_IFMT(entry.external_attr >> 16)
            require(kind in (0, stat.S_IFREG, stat.S_IFDIR) and
                    not (entry.flag_bits & 1), "Special or encrypted archive entry")
            if entry.is_dir():
                require(kind in (0, stat.S_IFDIR) and entry.file_size == 0,
                        "Invalid archive directory")
                continue
            require(kind in (0, stat.S_IFREG), "Invalid archive file")
            total += entry.file_size
            require(entry.file_size <= per_file and total <= total_limit,
                    "Expanded archive exceeds size limit")
            with archive.open(entry) as source:
                contents = source.read(entry.file_size + 1)
            require(len(contents) == entry.file_size, "Archive size mismatch")
            result[name] = contents
    # Reject file/directory collisions regardless of ZIP entry order.
    files_folded = {p.casefold() for p in result}
    for name in result:
        parts = name.casefold().split("/")
        require(all("/".join(parts[:i]) not in files_folded
                    for i in range(1, len(parts))), "File/directory collision")
    return result


def prepare_site(artifact_bytes, receipt):
    outer = archive_files(artifact_bytes, per_file=MAX_ARCHIVE)
    require(set(outer) == {"site.zip"}, "Unexpected artifact wrapper")
    bundle = archive_files(outer["site.zip"])
    files = {}
    for name, contents in bundle.items():
        if name == "netlify.toml":
            continue  # Legacy Drop configuration is never interpreted.
        require(name.startswith("public/"), "File outside public site")
        path = name[len("public/"):]
        if path == ".nojekyll":
            require(contents == b"", "Unexpected Jekyll marker content")
            continue  # GitHub Pages marker has no purpose on Netlify.
        if path in STATIC_MARKERS:
            require(contents == STATIC_MARKERS[path], "Unexpected teaching marker content")
            files[path] = STATIC_MARKERS[path]
            continue
        parts = path.casefold().split("/")
        require(not any(p.startswith(".") for p in parts), "Hidden file in site")
        require(not any(p in {"netlify.toml", "_redirects", "_headers", "_worker.js"}
                        for p in parts), "Untrusted deployment configuration")
        # Teaching .R/.py/.zip downloads remain ordinary static bytes.
        if path.casefold() == "_preview.json":
            continue  # Replace build-controlled provenance with API metadata.
        files[path] = contents
    require("index.html" in files and files["index.html"], "Missing site index")
    files["_preview.json"] = (json.dumps(receipt, indent=2) + "\n").encode()
    files["_headers"] = ("/*\n  X-Robots-Tag: noindex, nofollow\n"
                         "  X-Content-Type-Options: nosniff\n").encode()
    return files


def validate_preview_deploy(deploy, site_id, deploy_id):
    require(deploy.get("id") == deploy_id and deploy.get("site_id") == site_id,
            "Netlify returned a different deploy or site")
    # Netlify accepts draft=true in the request, but its response may omit the
    # draft property. A manual deploy-preview is the equivalent server-side
    # non-production signal. Never treat missing metadata alone as a draft.
    if "draft" in deploy:
        require(deploy["draft"] is True, "Netlify explicitly returned a non-draft deploy")
    else:
        require(deploy.get("context") == "deploy-preview" and
                deploy.get("manual_deploy") is True,
                "Netlify did not confirm a manual preview deploy")
        print("Netlify confirmed a manual deploy-preview; draft field omitted", flush=True)
    require(deploy.get("context") != "production" and not deploy.get("published_at"),
            "Netlify returned a production or published deploy")
    require(not any(deploy.get(k) for k in
                    ("required_functions", "required_edge_functions", "required_server")),
            "Unexpected executable deployment")


def deploy_static(netlify, site_id, site_name, files, title):
    require(str(uuid.UUID(site_id)) == site_id, "Site ID must be a UUID")
    require(bool(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,62}", site_name)), "Invalid site name")
    print("Validating the configured Netlify preview site", flush=True)
    site = netlify.call("/sites/" + site_id)
    require(site["id"] == site_id and site["name"] == site_name, "Preview site mismatch")
    hashes = {"/" + path: hashlib.sha1(data).hexdigest() for path, data in files.items()}
    by_hash = {digest: path.lstrip("/") for path, digest in hashes.items()}
    # Explicit JSON draft flag avoids ambiguity around ZIP query parameters.
    print("Creating a static draft deploy", flush=True)
    deploy = netlify.call("/sites/" + site_id + "/deploys?title=" + quote(title, safe=""), "POST", payload={
        "files": hashes, "draft": True, "async": False,
        "functions": {},
    })
    deploy_id = deploy["id"]
    require(bool(re.fullmatch(r"[a-zA-Z0-9-]{1,80}", deploy_id)), "Invalid deploy ID")
    validate_preview_deploy(deploy, site_id, deploy_id)
    print("Uploading the requested static files", flush=True)
    for digest in deploy.get("required", []):
        require(digest in by_hash, "Unexpected requested file digest")
        path = by_hash[digest]
        netlify.call("/deploys/" + deploy_id + "/files/" + quote(path, safe="/"),
                     "PUT", raw=files[path])
    print("Waiting for the draft deploy to become ready", flush=True)
    deadline = time.monotonic() + 480
    while deploy.get("state") != "ready":
        require(deploy.get("state") != "error", "Netlify deploy failed")
        require(time.monotonic() < deadline, "Netlify deploy timed out")
        time.sleep(3)
        deploy = netlify.call("/deploys/" + deploy_id)
        validate_preview_deploy(deploy, site_id, deploy_id)
    published = netlify.call("/sites/" + site_id).get("published_deploy") or {}
    require(published.get("id") != deploy_id, "Preview replaced the published deploy")
    url = "https://" + deploy_id + "--" + site_name + ".netlify.app"
    require(deploy.get("deploy_ssl_url", "").rstrip("/") == url,
            "Unexpected deploy URL")
    return url


def main():
    require(os.environ.get("GITHUB_EVENT_NAME") == "workflow_run", "Wrong event")
    require(os.environ.get("GITHUB_REPOSITORY") == REPOSITORY and
            os.environ.get("GITHUB_REF") == "refs/heads/main", "Untrusted publisher ref")
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    require(event["action"] == "completed", "Wrong run action")
    event_run = event["workflow_run"]
    run_id = event_run["id"]
    require(type(run_id) is int and run_id > 0, "Invalid run ID")
    repository_id = event["repository"]["id"]
    github = API("https://api.github.com/repos/" + REPOSITORY, os.environ["GH_TOKEN"])
    run = github.call("/actions/runs/" + str(run_id))
    workflow = github.call("/actions/workflows/workshop-preview-build.yml")
    validate_run(run, event_run, workflow, repository_id)

    candidates = run.get("pull_requests") or github.call(
        "/commits/" + run["head_sha"] + "/pulls?per_page=100")
    matches = []
    for candidate in candidates:
        number = candidate["number"]
        require(type(number) is int and number > 0, "Invalid PR number")
        pr = github.call("/pulls/" + str(number))
        try:
            validate_pr(pr, run, repository_id)
            matches.append(pr)
        except ValueError:
            continue
    require(len(matches) == 1, "No unique current open PR for this build")
    pr = matches[0]
    listing = github.call("/actions/runs/" + str(run_id) + "/artifacts?per_page=100")
    require(listing["total_count"] <= 100, "Too many artifacts")
    artifacts = [a for a in listing["artifacts"]
                 if a["name"] == "workshop-preview-" + run["head_sha"]]
    require(len(artifacts) == 1, "Missing or ambiguous preview artifact")
    artifact = artifacts[0]
    require(not artifact["expired"] and artifact["size_in_bytes"] <= MAX_ARCHIVE,
            "Artifact expired or too large")
    artifact_id = artifact["id"]
    require(type(artifact_id) is int and artifact_id > 0, "Invalid artifact ID")
    blob = request(github.root + "/actions/artifacts/" + str(artifact_id) + "/zip",
                   github.token, limit=MAX_ARCHIVE)
    require(artifact.get("digest") == "sha256:" + hashlib.sha256(blob).hexdigest(),
            "Artifact digest missing or mismatched")
    receipt = {"repository": REPOSITORY, "pr": pr["number"],
               "commit": run["head_sha"], "build_run": run_id,
               "build_attempt": run["run_attempt"], "artifact_id": artifact_id,
               "artifact_sha256": hashlib.sha256(blob).hexdigest(),
               "publisher_commit": os.environ["GITHUB_SHA"],
               "note": "Build association verified; content remains untrusted preview material."}
    files = prepare_site(blob, receipt)
    validate_run(github.call("/actions/runs/" + str(run_id)), event_run,
                 workflow, repository_id)
    validate_pr(github.call("/pulls/" + str(pr["number"])), run, repository_id)
    netlify = API("https://api.netlify.com/api/v1", os.environ["NETLIFY_AUTH_TOKEN"])
    url = deploy_static(netlify, os.environ["NETLIFY_SITE_ID"],
                        os.environ["NETLIFY_SITE_NAME"], files,
                        "PR " + str(pr["number"]) + " / " + run["head_sha"][:12])
    # A force-push during upload can leave an isolated draft, but must not
    # advertise it as the current PR preview.
    validate_run(github.call("/actions/runs/" + str(run_id)), event_run,
                 workflow, repository_id)
    validate_pr(github.call("/pulls/" + str(pr["number"])), run, repository_id)
    github.call("/statuses/" + run["head_sha"], "POST", payload={
        "state": "success", "context": "Workshop preview / Netlify",
        "description": "Preview published; content still needs review",
        "target_url": url,
    })
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary:
        summary.write("[Open workshop preview](" + url + ")\n\nPR #" +
                      str(pr["number"]) + " · commit `" + run["head_sha"] + "`\n")
    print("Workshop preview: " + url)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        # No traceback: third-party response text/URLs might contain secrets.
        print(failure_message(error), file=sys.stderr)
        sys.exit(1)
