# ANNOUNCE_OG-rl-5 -- PHASE A, STOPPED AT STEP 4b, `0.9.0_WK_NFRA_OPLGTW~15` (re-hand), 2026-10-04

Nothing was uploaded or deployed; no ledger, sentinel or manifest edit; no grant written; the real state store was not touched. The host was touched only by
read-only SSM runs (scratch under /tmp/og_rl5_run, removed in the same command list: SCRATCH_REMOVED=yes, leftovers 0 on every run). `.env` was never read.
Steps 5 (verify script) and 6 (announce for GO) are NOT done as an act: step 4b STOPS the order (rows Z-W15-S33, Z-W15-S34).

| step | outcome | evidence |
|---|---|---|
| 1 live ref | `af2d762970` = EC2_MANIFEST `deployed_commit` = S3 `opal-gateway-latest.tar.gz` git-ref (478,828 bytes, 2026-10-03T16:55Z). Host md5 **94 of 94 identical, 0 mismatch, 0 host-only files under app/ and deploy/** | SSM a2524410 (`rl5_live_md5_host.out`) |
| 1 release tree | `/c/tmp/og-rel10`, `rel-nfra-oplgtw-r16` @ `95a7dccc4d`, clean; `git diff --name-only af2d762970 HEAD` = 7 files, all under infra/aws/ec2/opal-gateway (outside 0); template untouched | `rl5_cmp_release.out` |
| 1 whole files | query.py, datasets.json, test_schwab_grain_r9.py, test_schwab_semantics.py, test_schwab_transactions.py: release == CLOUD HEAD (5 of 5); the four that pre-exist equal live at gr-3's parent (4 of 4) | same |
| 1 integration.py clause | `git diff -U0 af2d762970` on the release vs gr-3's own diff of the file: **15 = 15 changed lines EQUAL** (hunk md5 0c2e1bf559); test_schwab_query.py **9 = 9 EQUAL**; release still carries `environ_with_external_ids` (CLOUD's copy does not) | same |
| 2 tests | grain_r9 5 passed; semantics 14; query 26 (incl. `test_ogq2_ac20` 1 passed); transactions 4; `test_ogz2_ac08` 1 (`DENOMINATOR 60 registered tool(s) ... 0 hit(s)`); total **50 passed**, tree clean, audit file 0 bytes | pytest on og-rel10 |
| 3 rollback | `/c/tmp/og-rb10` at af2d762970 (clean); built artifact (97 files) vs a fresh download of the live S3 object: **97 of 97 identical**, `diff -rq` empty; the 94 non-dashboard files equal the rb10 git tree; `rb10.tar.gz` extraction equals the staged tree | `rl5_cmp_rollback.out` |
| 4b census | **SERVED: 0 snapshots servable** (24 marker dates per master: 10 legacy_marker, 14 REJECTED; dim_position 0, dim_asset 0, at both masters). The zero is REAL (row S33), not a helper defect: the live contract lists dim_transaction in `datasets` but not in `data_prefixes`, so every closure-bearing day is rejected. COUNTERFACTUAL (same code, in-memory contract copy plus the dim_transaction prefixes): 56 snapshots (14 dates x 2 masters x 2 datasets), 0 missing R9 column, 0 blank | `rl5_diag.out`, `rl5_diag2.out`, `rl5_census.out` |
| 4 paging BEFORE | master 08242234, 2026-10-01, page_size 5, synthetic principal and grant in memory. SERVED: dim_position REFUSED `INCOMPLETE_SNAPSHOT snapshot_incomplete`; dim_asset REFUSED `UNAVAILABLE asset_policy_selection_unavailable` (row S34). Counterfactual contract: dim_position REFUSED `INVALID_REQUEST paging_refused_no_unique_grain` (the expected grain refusal); dim_asset UNAVAILABLE (policy). Seam (asset_policy set): both `paging_refused_no_unique_grain` | `rl5_paging_before.out` |

Rows: `NFRA_OPLGTW-Z-W15-S33` (BLOCKING, ARMED), `NFRA_OPLGTW-Z-W15-S34` (BLOCKING, INERT); both disarm_owner `2.0.0_SA_COO~O`.
