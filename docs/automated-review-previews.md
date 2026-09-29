# Automated shared review previews

## Initial enablement

These workflows require setup before the first live preview:

1. Create a dedicated Netlify preview site, separate from the live workshop and
   any production domain, secrets, functions, Git-connected builds or plugins.
2. Create the GitHub environment `workshop-preview-publisher`. Select deployment
   branches explicitly: allow only branch `main`, with no tags. Do not select
   all protected branches. Confirm this restriction is supported and active
   before adding the token. Protect `main` and review publisher/workflow changes.
3. In that environment only, add secret `NETLIFY_AUTH_TOKEN` and variables
   `NETLIFY_SITE_ID` (lowercase UUID) and `NETLIFY_SITE_NAME` (without the domain).
   Use the narrowest available Netlify identity; personal tokens should not be
   assumed to be restricted to one site. No required environment reviewer is
   needed for routine automatic uploads once the branch restriction is verified.
4. The publisher must be merged onto `main` before GitHub can trigger it via
   `workflow_run`. The PR build also needs `scripts/prepare-review-preview.py`.
5. Test a harmless PR update: inspect the complete R build and rendered pages,
   verify the receipt matches the PR head and the deploy is a draft on the
   separate site, and verify the live site's deployment did not change. Check
   a fork PR and a superseded build before relying on routine automation.

Offline validation initially passed 20 security-boundary tests. That does not
substitute for this live trial. The workflow pins its top-level Actions; the
existing R setup and upstream composite dependencies are not fully locked.

## Routine operation

The preview build renders the exact PR head using R 4.4.2, Pandoc and the
repository's existing Sandpaper setup and preview helper. It runs the semantic
teaching-artifact check, the helper's workshop checks and full lesson build.
Only the resulting ZIP is uploaded as an Actions artifact.

A separate workflow uses reviewed code from `main` to publish that artifact.
Its environment, `workshop-preview-publisher`, must allow only `main` and must
hold the `NETLIFY_AUTH_TOKEN` secret plus `NETLIFY_SITE_ID` and
`NETLIFY_SITE_NAME` variables. Never move the token into the build workflow or
repository-wide secrets. Use a dedicated preview site and protect `main`.

After publication, open **Workshop preview / Netlify** in the PR checks or the
link in the publishing workflow's summary. The URL is unique to that deploy;
new commits produce new links. Check `_preview.json` for the associated PR,
commit and build run, then inspect the changed pages. Do not treat the preview
status as scientific approval or as a content-security certification.

Draft PRs are skipped. Closed PRs, superseded revisions/rerun attempts, failed
builds, mismatched artifacts and unsafe archives cannot post a success status.
An update during upload can leave an older isolated draft but will not advertise
it as the current preview. The separate live workshop is not the deploy target.

For a failed publish, inspect the failed Actions step and check that the PR is
still open at the same commit, the build artifact is present and unexpired, the
workflow exists on `main`, and the environment/site values are correct. The
publisher deliberately avoids logging API response bodies and signed URLs.
If the artifact exceeds the limits or contains a prohibited filename, review the
actual output before changing the validator; do not bypass it to make CI green.

Local preparation via `scripts/prepare-review-preview.py` remains optional for
reviewed, trusted revisions. Its disposable clone prevents stale-file mixing;
it does not isolate code from that machine's files or credentials. Public draft
previews are not private hosting: access control requires separate Netlify setup.
