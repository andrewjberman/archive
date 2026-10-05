# ANNOUNCE_OG-rl-6 -- PHASE A COMPLETE, `0.9.0_WK_NFRA_OPLGTW~15`, 2026-10-05

Nothing was uploaded or deployed; no ledger, sentinel or manifest edit; no grant written; the real state store was not touched. The host was touched
only by read-only SSM runs (scratch under /tmp/og_rl6_run, removed in the same command list: SCRATCH_REMOVED=yes, leftovers 0 on every run). `.env`
was never sourced; the verify script reads its key NAMES only. Local only: nothing pushed. PHASE B (step 7 onward) is NOT started.

| step | outcome | evidence |
|---|---|---|
| 1 live ref | `4b6b823faec5288c714b70117fcd691239a2633f` is live: host md5 **94 of 94 identical, 0 mismatch, 0 host-only files under app/ and deploy/** (list = `rl6_live_md5.txt`, equal to the og-rel11 tree 94 of 94) | SSM 822b5abe (`rl6_md5_host.py` through `rl6_ssm.py`), `rl6_live_md5_host.out` |
| 1 release tree | `/c/tmp/og-rel11`, branch `rel-nfra-oplgtw-r17` at `4b6b823fae`, then ONE commit **`e91819e2819df8c8df5708bc66e4f4273bb1a834`**; `git diff --name-status 4b6b823fae HEAD` = 3 files: `app/integrations/schwab/integration.py` (M), `tests/test_schwab_q7_asset_download.py` (A), `tests/test_schwab_rl5_asset_query.py` (M); all inside the release set (integration.py + `tests/test_schwab_*.py`) | git |
| 1 hunk-set equality | q-7's own diff `git diff fc70572578^1 fc70572578 -- integration.py` (159 lines, 5 hunks, 108 changed lines) was applied to the LIVE bytes with `git apply`. `git diff 4b6b823fae HEAD -- integration.py` on the release has the SAME 5 hunks, 108 changed lines, and its patch text equals q-7's apart from the `index` line (`diff` of the two, index lines removed: empty). Pre-q-7 CLOUD vs live differs in ONE line (`environ_with_external_ids` in `build_default_service()`), left as live has it (count 1 in both live and release). Patches: `rl6_q7_integration.patch`, `rl6_release_integration.patch` | git, `.scratch` copies committed here |
| 1 tests whole | both test files are byte copies of CLOUD `17dd36e08b` (`cmp` equal); `tests/test_schwab_rl5_asset_query.py` is the merged file (ti-1's service patch + q-7's restatement). **`tests/conftest.py` is NOT shipped**: it is outside rl6.AC2's release set. The release tree keeps live's conftest; row **Z-W15-S40** names the choice | git |
| 1 R13 (a) | release commit under `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~15`; audit log `org/git-author-override-audit.log` (shared main workspace) lines **20972 and 20973**: `2026-10-05T01:44:26Z OVERRIDE  0.9.0_WK_NFRA_OPLGTW~15  3  (--author-override 0.9.0_WK_NFRA_OPLGTW~15 applied)` and the `01:44:30Z` twin; N_FILES 3 = the 3 files above | audit log |
| 2 tests, release tree | each target in its OWN process: q7 asset download **4 passed** (test_ogq7_ac01-04); rl5_asset_query **2 passed**; test_schwab_query **26 passed**; test_schwab_grain_r9 **5 passed**; `test_entitlement_admin.py::test_ogz2_ac08` **1 passed** (`DENOMINATOR 60 registered tool(s) ... 0 hit(s)`). One process for all five: 4 failed + 2 errors on the release tree, **6 failed on CLOUD `17dd36e08b` too** (ti-1's conftest present): not caused by the carry; row Z-W15-S40 | `rl6_step2_perfile.txt`, `rl6_step2_oneprocess.txt` |
| 3 rollback | `/c/tmp/og-rb11` detached at `4b6b823fae`, clean. Live S3 artifact `opal-gateway-4b6b823fae.tar.gz` (bucket opal-313476888478-lambda-artifacts, prefix ec2/opal-gateway): 97 files = 94 gateway + 3 dashboard; **94 of 94 gateway files equal the rb11 git tree, 94 of 94 equal the live md5 list, 0 only-in-artifact** | `rl6_cmp_rollback.py`, `rl6_cmp_rollback.out` |
| 4 BEFORE | master 08242234, 2026-10-01, synthetic principal and grant in memory (10 accounts): **dim_asset `prepare_download` REFUSED `UNAVAILABLE asset_policy_selection_unavailable`**; dim_asset query **OK, 49 returned, 0 unheld, 1 page**. Re-read by the verify script's `before` mode (same values; MainPID 658002, 50 env key names, 65 tools, /health 200) | SSM 5725a3b6 `rl6_before.out`; `rl6_verify.sh before` |
| 4 rehearsal | the AFTER program ran on the host against a scratch copy of `app/` whose integration.py is the RELEASE file (shipped zlib+base64; staged md5 `8c1d4b1cf9bb0b460d535bd3d451e449` = the release tree's). Installed tree untouched, no deploy. Result: download **OK**; held check **returned 49, unheld 0, held_cusips_in_dim_position 49 < asset_universe_cusips 2160 (graded)**; empty-holdings grant REFUSED `ENTITLEMENT_DENIED asset_read_denied_unqualified`; query OK 49, **query held set == download held set: true**; grants_written 0, state_store_written false. The same program on the live bytes reads REFUSED (an earlier SSM run, before the release file was staged) | SSM 32d33e0a, `rl6_rehearsal_after.out` |
| 5 verify script | `rl6_verify.sh before|after` + `rl6_verify.py` + `rl6_host.py.txt` + `rl6_host_prelude.py.txt` + `rl6_ssm.py` + `rl6_release_md5.txt` (94 files = live list with integration.py's md5 replaced by the release's; equal to the og-rel11 tree 94 of 94). Checks: /health 200; shipped md5 = release bytes; tool list unchanged (65); .env 50 key names unchanged; the AFTER run (download OK; held check graded only when held < universe; empty-holdings REFUSED; query OK and held-equal); synthetic/0 grants; writes `RL6_DOWNLOAD.json`; then the floor `rl4.AC1.sh`, `ht.AC2.sh`. NEGATIVE CONTROL against the undeployed host (rc 1, "VERIFY FAIL: 7 of 12": md5 93 of 94, download REFUSED, held 0, empty-holdings reason wrong, query not equal), written to a scratch `--out`, so no `RL6_DOWNLOAD.json` exists. Floor on live today: `rl4.AC1.sh` PASS (4 of 4), `ht.AC2.sh` PASS (4 of 4) | `rl6_negative_control.out` |

## Blast radius, written for the three halves

- **CTO (served output).** One shipped file changes: `app/integrations/schwab/integration.py` (5 hunks, 77 insertions, 31 deletions). Served output that moves:
  `dim_asset` `prepare_download` and the download's redemption (`export_query`) go from always REFUSED to serving the same holdings-restricted set the query path
  already serves (the C3 rule: only CUSIPs held by the grant's accounts at that master and date). A grant whose accounts hold nothing is REFUSED
  `asset_read_denied_unqualified`, never "all CUSIPs". Unchanged: the `dim_asset` query (49 held of 2160 on the synthetic grant), every other dataset and
  tool (65 tools, 50 env key names), the contract, Terraform, IAM, the ALB. Rollback per key: re-deploy `opal-gateway-4b6b823fae.tar.gz` from `/c/tmp/og-rb11`;
  the artifact equals the rb11 tree file by file, and only integration.py differs between the two trees.
- **COO (act).** One `safe-ec2-deploy.sh` run from `/c/tmp/og-rel11` with `DEPLOY_BASE_REF=4b6b823faec5288c714b70117fcd691239a2633f`; NEVER-2 ledger
  `nfra-oplgtw-gateway-release-r17`, legs upload / install + verify / manifest / rollback-proven, entry AND sentinel committed first; verify immediately;
  any failure or ANY unheld CUSIP: roll back, re-verify, close ROLLED BACK. The service restarts; the verify script re-reads the 50 `.env` key names after.
- **CVO (what it means).** The release opens `dim_asset` downloads under C3 and nothing else: no grant is created or changed, so the real holder's
  first download is her own act at her next use. The discriminator is graded (held 49 < universe 2160), so "every downloaded CUSIP is held" is a
  statement that could have failed. What this run did NOT measure: a real principal's download (none is made), and the deployed-bytes path (the rehearsal
  runs the release file in a scratch copy; Phase B's AFTER run is the deployed read).

## Notes for the issuer
- The one-process pytest failure is not the release's (CLOUD fails the same way): row Z-W15-S40. The rl6 criteria do not run the tests; `rl6.AC2`'s release-set
  check will read integration.py + the two `tests/test_schwab_*.py` files, none outside it (conftest.py unshipped).
- `patch` is not installed on the host; the rehearsal ships the release file instead of a patch (runner `rl6_ssm.py`, `OG_RL6_STAGE_FILE`).
- Pre-GO the host's `deployed_commit` in `EC2_MANIFEST.json` is still `4b6b823fae` (so `rl6.AC1/AC2` read FAIL until Phase B, as the cut recorded).

## Phase B, when GO is given (steps 7-10)
Re-read live; if it moved, re-cut. Open NEVER-2 ledger `nfra-oplgtw-gateway-release-r17` with entry AND sentinel committed first.
`rl6_verify.sh before .scratch/rl6_before.json` again immediately before the act; the act from `/c/tmp/og-rel11` with
`DEPLOY_BASE_REF=4b6b823faec5288c714b70117fcd691239a2633f HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~15` through `infra/aws/ec2/safe-ec2-deploy.sh`;
`rl6_verify.sh after .scratch/rl6_before.json <deployed sha>` IMMEDIATELY (writes `RL6_DOWNLOAD.json`). Any FAIL: roll back from `/c/tmp/og-rb11`, re-verify, close ROLLED BACK.

Rows: `NFRA_OPLGTW-Z-W15-S40` (OBSERVATION, INERT, disarm_owner `2.0.0_SA_COO~O`).
