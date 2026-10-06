# KNB test teaching destination

**Status on 2026-09-08: local test dry run prepared; no public teaching record
created or anonymously verified.** No production deposit or DOI request occurred.

Expected title: **Workshop demonstration: NuSEDS Fraser Coho — KNB Test Node**.
The intended deposit is a new workshop series under Brett's authenticated test
identity. The existing private rehearsal must remain unchanged.

Inspect `../checkpoints/reference-sdp/publication/test/knb-manifest.json`:
`status` is `dry_run`, `knb_environment` is `test`, representation is `expanded`,
and the node is `urn:node:mnTestKNB`. Its planned identifiers are not evidence
that these objects exist in the catalog. The expanded plan lists data,
individual metadata files, EML and their resource-map relationships.

## Completion steps for Brett and the facilitator

1. Obtain Bruno and Tom's review through Brett and record corrections and
   remaining questions in `reference/scientific-review-packet.md`. Do not
   relabel an agent-authored technical selection as their approval.
2. Resolve the independent SDP validator mismatch described in
   `validation/upstream-validator-issue.md`; rerun strict SDP, specification and
   EML checks on the exact revised package. Preserve the existing reference as
   a record; produce a new copy when metadata changes.
3. Reconfirm the source licence and contributor roles in `metadata/eml-mapping.yml`.
   It credits DFO for source data, Brett for metadata/contact, and the workshop
   for the teaching derivative. The original Open Canada publication is linked.
4. Configure a KNB **test** credential locally, never in the kit or repository.
   The package accepts it through `options(dataone_test_token = ...)`; read a
   local `DATAONE_TEST_TOKEN` environment variable without printing its value.
5. Build a fresh plan in a separate working copy. Verify public access,
   expanded membership, the expected test subject and all checksums. The
   learner preview scripts have no live-upload switch.
6. For the already authorized public test deposit, call the existing package
   publisher from the maintainer's working copy with `dry_run = FALSE`,
   `public = TRUE`, `representation = "expanded"` and `knb_environment = "test"`.
   Keep the resulting manifest and evidence. Never change the environment to
   production as a fallback.
7. Run `scripts/verify-test-record.py` from the workshop repository against the
   published working copy. Without credentials, it checks every object download,
   size and SHA-256, the resource-map membership, system-metadata public access,
   the catalog view and Solr indexing. Inspect metadata rendering in a signed-out
   browser and save screenshots locally. A successful upload can precede indexing.
8. Record the observed public URL and receipt in the learner Reference page,
   Chapter 1 destination and this status file only after verification. Keep the
   local kit available when the test service is unavailable.

The Test Node UI is <https://dev.nceas.ucsb.edu/>; its member-node endpoint is
<https://dev.nceas.ucsb.edu/knb/d1/mn>. The [DataONE environment documentation](https://dataone-operations.readthedocs.io/en/latest/MN/deployment/environments.html)
explains why staging and production are independent. Test uploads are already
used in [NCEAS teaching](https://nceas.github.io/sasap-training/materials/reproducible_research_in_r_fairbanks/data-documentation-and-publishing.html).

Test records are non-durable and cannot receive a DOI through this workflow.
Production publication is a separate future decision requiring a fresh plan,
review and authorization. It is outside this workshop's execution scope.
