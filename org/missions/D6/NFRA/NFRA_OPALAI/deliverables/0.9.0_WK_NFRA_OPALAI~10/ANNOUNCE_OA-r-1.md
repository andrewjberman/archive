# ANNOUNCE -- NFRA_OPALAI OA-r-1: narrow opal-gateway release of the OA-e-1 asker-scoping repair

Seat: 0.9.0_WK_NFRA_OPALAI~10 (worker of 2.0.0_SA_COO~AI). Nothing below step 1 has been done; the instance is untouched.

- Target: opal-gateway on i-07dccb1615503ac99 (/opt/opal-gateway).
- Release branch: `rel-nfra-opalai-r2-asker-binding-gateway`, created at step 2 after GO from the base below.
- Base commit (resolved by content, row NFRA_OPALAI-Z-W10-S3): `6a98a0553a` (OG-s-1, `rel-nfra-oplgtw-sprint-owner`).
- Release commit: created at step 2 after GO; it is the base plus the cherry-pick of OA-e-1's code commits
  `2254910889` and `a2c96703b1`, nothing else. Its hash will be in the final report.
- Files shipped: `app/asker_scope.py`, `app/tools.py`, and the tests `test_asker_scope.py`, `test_asker_binding.py`,
  `test_portal_grant.py`. The tests do not run on the host. No tool is added, no `.env` key changes.
- Ledger slug: `nfra-opalai-r2-asker-binding-gateway` (opened at step 5, on the slot ~10 branch).
- Rollback: redeploy the base `6a98a0553a` built from a clean tree (`rb-nfra-opalai-r2-asker-binding-base`), halt gate
  pre-acknowledged; built without upload at step 3, before the act.
- Window: outside US business hours only (row Z-S24). One gateway deployer at a time (CTO ruling @75117e60d6).

## Base resolution (step 0, read-only over SSM, status Success)

Live md5 of the four named files equals `6a98a0553a` on all four:

| file | live md5 = 6a98a0553a |
|---|---|
| app/asker_scope.py | f21b86141a7145fb70b5f77d37774d85 |
| app/tools.py | 6c888e51a3c652dfe89c74654fde39e3 |
| app/identity_scope.py | 442c9755d14aa1ffbbccf5bf0fe73656 |
| app/data_entitlement.py | 964504343c24d412a266da74e7108e69 |

Candidates compared: the pinned `6a98a0553a` and `fe94911257`, plus 12 local or origin `rel-*` refs.
All four files match at: `6a98a0553a`, `fe94911257`, `rel-nfra-mcpindex-r3-gateway` (2dedae93df).

.env key-set tie-break (key names only, 27 live keys): `fe94911257` writes 26 (no SPRINT_VIEW_ALLOWED_EMAILS), so it
is out. Survivors: `6a98a0553a` and `2dedae93df`, a descendant that differs only in the value of ENABLED_INTEGRATIONS
and in three other files. The order's rule (newest survivor) would choose `2dedae93df`. Three further live files
(`opal_discover/integration.py`, `portal_index/integration.py`, `refs/DATA_CATALOG.yaml`) match `6a98a0553a` and do not
match `2dedae93df`, so the host is not running it. Base: `6a98a0553a`. Both survivors named; the departure from the
literal rule is row NFRA_OPALAI-Z-W10-S3. The manifest at CLOUD agrees (deployed_commit 6a98a0553a, 2026-09-27T22:17:33Z).

Status: ANNOUNCE READY. Waiting for GO.
