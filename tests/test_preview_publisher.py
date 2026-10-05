"""Offline security-boundary tests; never contact GitHub or Netlify."""
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import stat
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
import warnings
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

spec = importlib.util.spec_from_file_location(
    "publisher", Path(__file__).parents[1] / "scripts/publish-review-preview.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


def archive(entries):
    output = io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with ZipFile(output, "w", ZIP_DEFLATED) as z:
            for name, data in entries:
                z.writestr(name, data)
    return output.getvalue()


def artifact(entries):
    return archive([("site.zip", archive(entries))])


class SafeDiagnostics(unittest.TestCase):
    def test_validation_failure_explains_the_failed_check(self):
        try:
            p.require(False, "Preview site mismatch")
        except p.PreviewValidationError as error:
            self.assertIn("Preview site mismatch", p.failure_message(error))
        else:
            self.fail("Expected validation failure")

    def test_other_exceptions_do_not_expose_remote_data(self):
        for kind in (ValueError, RuntimeError, KeyError):
            with self.subTest(kind=kind):
                message = p.failure_message(kind("secret-token-or-signed-url"))
                self.assertNotIn("secret-token-or-signed-url", message)
                self.assertIn(kind.__name__, message)


class ArchiveBoundary(unittest.TestCase):
    def test_regular_site_and_teaching_code_are_data(self):
        code = b'raise RuntimeError("must never execute")'
        blob = artifact([("public/index.html", b"<h1>Preview</h1>"),
                         ("public/lesson.py", code),
                         ("public/_preview.json", b'{"commit":"forged"}'),
                         ("netlify.toml", b'command = "malicious"')])
        files = p.prepare_site(blob, {"commit": "trusted-api-value"})
        self.assertEqual(files["lesson.py"], code)
        self.assertEqual(json.loads(files["_preview.json"])["commit"], "trusted-api-value")
        self.assertNotIn("netlify.toml", files)
        self.assertIn(b"noindex", files["_headers"])

    def test_traversal_absolute_backslash_url_and_control_paths(self):
        for name in ["../secret", "/absolute", "a/../b", "a//b", "a/./b",
                     r"a\b", "C:/secret", "a%2fb", "a?x=1", "x\nY"]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                p.archive_files(archive([(name, b"bad")]))

    def test_embedded_nul_in_zip_headers(self):
        # ZipFile's writer strips NULs, so mutate the actual ZIP headers.
        blob = archive([("x_tail", b"bad")]).replace(b"x_tail", b"x\x00tail")
        with self.assertRaises(ValueError):
            p.archive_files(blob)

    def test_symlinks_and_devices_rejected(self):
        for kind in [stat.S_IFLNK, stat.S_IFIFO, stat.S_IFCHR]:
            info = ZipInfo("public/index.html")
            info.create_system = 3
            info.external_attr = (kind | 0o777) << 16
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                p.archive_files(archive([(info, b"/etc/passwd")]))

    def test_duplicates_and_case_collisions(self):
        for names in [("index.html", "index.html"), ("A.html", "a.html")]:
            with self.subTest(names=names), self.assertRaises(ValueError):
                p.archive_files(archive([(n, b"x") for n in names]))

    def test_file_directory_collision(self):
        with self.assertRaises(ValueError):
            p.archive_files(archive([("x", b"file"), ("x/y", b"child")]))

    def test_uncompressed_size_limits(self):
        blob = archive([("bomb.txt", b"x" * 10000)])
        with self.assertRaises(ValueError):
            p.archive_files(blob, per_file=100)
        with self.assertRaises(ValueError):
            p.archive_files(blob, total_limit=100)

    def test_file_count_limit(self):
        with patch.object(p, "MAX_FILES", 1), self.assertRaises(ValueError):
            p.archive_files(archive([("a", b""), ("b", b"")]))

    def test_unexpected_outer_file(self):
        with self.assertRaises(ValueError):
            p.prepare_site(archive([("run.py", b"evil")]), {})

    def test_hidden_files_and_deploy_configuration(self):
        for name in ["public/.git/config", "public/.netlify/functions/a.js",
                     "public/_redirects", "public/_headers", "public/netlify.toml",
                     "public/_worker.js", "outside.html"]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                p.prepare_site(artifact([("public/index.html", b"ok"), (name, b"bad")]), {})

    def test_missing_index(self):
        with self.assertRaises(ValueError):
            p.prepare_site(artifact([("public/a.html", b"ok")]), {})

    def test_known_workshop_markers_are_exact_inert_bytes(self):
        entries = [("public/index.html", b"ok"), ("public/.nojekyll", b"")]
        entries += [("public/" + path, value) for path, value in p.STATIC_MARKERS.items()]
        files = p.prepare_site(artifact(entries), {})
        self.assertNotIn(".nojekyll", files)
        for path, value in p.STATIC_MARKERS.items():
            self.assertEqual(files[path], value)

    def test_marker_exceptions_reject_changed_bytes_or_other_paths(self):
        for name, value in [
            ("public/.nojekyll", b"unexpected"),
            ("public/files/fraser-coho-workshop/checkpoints/draft-sdp/.metasalmon-package", b"unexpected"),
            ("public/files/other/.metasalmon-package", b"metasalmon-owned\n"),
            ("public/subdir/.nojekyll", b""),
        ]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                p.prepare_site(artifact([("public/index.html", b"ok"), (name, value)]), {})


class ProvenanceBoundary(unittest.TestCase):
    def setUp(self):
        self.repo = {"id": 17, "full_name": p.REPOSITORY}
        self.workflow = {"id": 25, "path": p.WORKFLOW}
        self.run = {"id": 99, "run_attempt": 1, "repository": self.repo,
                    "workflow_id": 25, "status": "completed", "conclusion": "success",
                    "event": "pull_request", "head_sha": "a" * 40,
                    "head_repository": {"id": 18}}
        self.event = {"id": 99, "run_attempt": 1}
        self.pr = {"number": 8, "state": "open", "draft": False,
                   "base": {"repo": self.repo, "ref": "main"},
                   "head": {"repo": {"id": 18}, "sha": "a" * 40}}

    def test_current_fork_pr_is_supported(self):
        p.validate_run(self.run, self.event, self.workflow, 17)
        p.validate_pr(self.pr, self.run, 17)

    def test_wrong_run_workflow_event_and_attempt(self):
        for key, value in [("id", 100), ("run_attempt", 2), ("workflow_id", 26),
                           ("event", "push"), ("status", "in_progress"),
                           ("conclusion", "failure"), ("head_sha", "injected/path")]:
            changed = {**self.run, key: value}
            with self.subTest(key=key), self.assertRaises(ValueError):
                p.validate_run(changed, self.event, self.workflow, 17)

    def test_wrong_workflow_path_or_repository(self):
        with self.assertRaises(ValueError):
            p.validate_run(self.run, self.event, {"id": 25, "path": "other.yml"}, 17)
        with self.assertRaises(ValueError):
            p.validate_run(self.run, self.event, self.workflow, 999)

    def test_closed_draft_stale_wrong_base_and_wrong_head_repo(self):
        cases = []
        for key, value in [("state", "closed"), ("draft", True)]:
            cases.append({**self.pr, key: value})
        for field, key, value in [("head", "sha", "b" * 40),
                                  ("head", "repo", {"id": 999}),
                                  ("base", "ref", "other")]:
            changed = copy.deepcopy(self.pr)
            changed[field][key] = value
            cases.append(changed)
        for changed in cases:
            with self.subTest(pr=changed), self.assertRaises(ValueError):
                p.validate_pr(changed, self.run, 17)


class DeploymentBoundary(unittest.TestCase):
    SITE_ID = "12345678-1234-1234-1234-123456789abc"
    SITE_NAME = "workshop-preview-test"

    class FakeNetlify:
        def __init__(self, owner, draft=True, site_name=None):
            self.owner, self.calls, self.draft = owner, [], draft
            self.site_name = site_name or owner.SITE_NAME

        def call(self, path, method="GET", payload=None, raw=None):
            self.calls.append((path, method, payload, raw))
            if path == "/sites/" + self.owner.SITE_ID:
                return {"id": self.owner.SITE_ID, "name": self.site_name}
            if method == "POST":
                self.payload = payload
                return {"id": "deploy123", "site_id": self.owner.SITE_ID,
                        "draft": self.draft, "state": "uploading",
                        "required": list(set(payload["files"].values()))}
            if method == "PUT":
                return {"sha": hashlib.sha1(raw).hexdigest()}
            return {"id": "deploy123", "site_id": self.owner.SITE_ID,
                    "draft": self.draft, "state": "ready",
                    "deploy_ssl_url": "https://deploy123--" + self.owner.SITE_NAME + ".netlify.app"}

    def test_draft_flag_and_only_static_bytes_uploaded(self):
        fake = self.FakeNetlify(self)
        with patch.object(p.time, "sleep"):
            url = p.deploy_static(fake, self.SITE_ID, self.SITE_NAME,
                                  {"index.html": b"hello"}, "PR 8")
        self.assertTrue(fake.payload["draft"])
        self.assertEqual(fake.payload["functions"], {})
        self.assertEqual(url, "https://deploy123--workshop-preview-test.netlify.app")
        puts = [c for c in fake.calls if c[1] == "PUT"]
        self.assertEqual(puts, [("/deploys/deploy123/files/index.html", "PUT", None, b"hello")])

    def test_production_response_rejected_before_file_upload(self):
        fake = self.FakeNetlify(self, draft=False)
        with self.assertRaises(ValueError):
            p.deploy_static(fake, self.SITE_ID, self.SITE_NAME, {"index.html": b"hello"}, "PR 8")
        self.assertFalse(any(c[1] == "PUT" for c in fake.calls))

    def test_wrong_site_rejected_before_deploy(self):
        fake = self.FakeNetlify(self, site_name="production")
        with self.assertRaises(ValueError):
            p.deploy_static(fake, self.SITE_ID, self.SITE_NAME, {"index.html": b"hello"}, "PR 8")
        self.assertFalse(any(c[1] == "POST" for c in fake.calls))

    def test_manual_preview_without_draft_response_field(self):
        fake = self.FakeNetlify(self)
        original_call = fake.call

        def missing_draft(*args, **kwargs):
            result = original_call(*args, **kwargs)
            if "draft" in result:
                del result["draft"]
                result.update(context="deploy-preview", manual_deploy=True)
            return result

        fake.call = missing_draft
        with patch.object(p.time, "sleep"):
            url = p.deploy_static(fake, self.SITE_ID, self.SITE_NAME,
                                  {"index.html": b"hello"}, "PR 11")
        self.assertTrue(fake.payload["draft"])
        self.assertEqual(url, "https://deploy123--workshop-preview-test.netlify.app")

    def test_missing_draft_does_not_accept_ambiguous_or_published_deploy(self):
        preview = {"id": "deploy123", "site_id": self.SITE_ID,
                   "context": "deploy-preview", "manual_deploy": True}
        cases = [
            {"context": "production"}, {"context": "branch-deploy"},
            {"context": None}, {"manual_deploy": False}, {"manual_deploy": None},
            {"draft": False}, {"draft": None}, {"draft": "true"},
            {"published_at": "2026-09-30T00:00:00Z"},
            {"site_id": "another-site"}, {"id": "another-deploy"},
            {"required_functions": ["function-sha"]},
            {"required_edge_functions": ["edge-sha"]},
            {"required_server": ["server-sha"]},
        ]
        for changed in cases:
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                p.validate_preview_deploy({**preview, **changed}, self.SITE_ID, "deploy123")

    def test_draft_flag_does_not_override_production_context(self):
        with self.assertRaises(ValueError):
            p.validate_preview_deploy({"id": "deploy123", "site_id": self.SITE_ID,
                                       "draft": True, "context": "production"},
                                      self.SITE_ID, "deploy123")

    def test_preview_cannot_be_the_published_site_deploy(self):
        fake = self.FakeNetlify(self)
        original_call = fake.call

        def became_published(*args, **kwargs):
            result = original_call(*args, **kwargs)
            if args[0] == "/sites/" + self.SITE_ID:
                result["published_deploy"] = {"id": "deploy123"}
            return result

        fake.call = became_published
        with patch.object(p.time, "sleep"), self.assertRaises(ValueError):
            p.deploy_static(fake, self.SITE_ID, self.SITE_NAME,
                            {"index.html": b"hello"}, "PR 11")

    def test_authenticated_redirects_are_never_automatically_followed(self):
        self.assertIsNone(p.NoRedirect().redirect_request(None, None, 302, "", {}, "https://other/"))

    def test_artifact_redirect_does_not_forward_token(self):
        class Response(io.BytesIO):
            pass

        class Opener:
            def __init__(self):
                self.requests = []

            def open(self, req, timeout):
                self.requests.append(req)
                if len(self.requests) == 1:
                    raise HTTPError(req.full_url, 302, "Found",
                                    {"Location": "https://artifacts.example.test/signed"}, None)
                return Response(b"archive")

        opener = Opener()
        with patch.object(p, "build_opener", return_value=opener):
            result = p.request("https://api.github.com/repos/" + p.REPOSITORY +
                               "/actions/artifacts/42/zip", "secret")
        self.assertEqual(result, b"archive")
        self.assertEqual(opener.requests[0].get_header("Authorization"), "Bearer secret")
        self.assertIsNone(opener.requests[1].get_header("Authorization"))


if __name__ == "__main__":
    unittest.main()
