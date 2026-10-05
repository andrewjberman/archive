# ANNOUNCE_OG-rl-6-C -- PHASE C-A COMPLETE (amendment A1, steps 11-17), `0.9.0_WK_NFRA_OPLGTW~15`, 2026-10-05

Nothing was uploaded or deployed; no ledger, sentinel or manifest edit; no grant written; the real state store was not touched. The host was touched only
by read-only SSM runs (scratch under `/tmp/og_rl6c_run`, removed in the same command list: `SCRATCH_REMOVED=yes`, leftovers 0 on every run). `.env` was never
sourced; the verify script reads its key NAMES only. Local only: nothing pushed. PHASE C-B (step 18 onward) is NOT started.

| step | outcome | evidence |
|---|---|---|
| 11 live ref | `e91819e2819df8c8df5708bc66e4f4273bb1a834` is live: host md5 **94 of 94 identical, 0 mismatch, 0 host-only files under app/ and deploy/** against the list built from the og-rel12 tree at `e91819e281` (equal to `rl6_release_md5.txt` 94 of 94) | SSM e392ab0a (`rl7_md5_host.py` through `rl6c_ssm.py`), `rl7_live_md5_host.out`, `rl7_live_md5.txt` |
| 12 CLOUD source | commit **`17d151f6cc`** on `wk-NFRA_OPLGTW-15-r17`: 3 kit files copied from origin/CLOUD (view.py and test blobs byte-equal to the kit's; index.html committed as LF, row **Z-W15-S43**); `apply_hookup.py` -> `OK: 3 edits applied` (3 of 3 anchors); `tests/test_yearinreview_view.py` **5 passed**, `tests/test_sprint_view.py` **8 passed**, `app/tests/test_rivalfunds_view.py` **11 passed** (each its own process); `app.server` imports and registers `/yearinreview` and `/yearinreview/` beside `/sprint*` and `/rivalfunds*` | git, pytest |
| 13 release tree | `/c/tmp/og-rel12`, branch `rel-nfra-oplgtw-r17b` at `e91819e281`, then ONE commit **`14e0af86fa322c8eb71a7aafe59210d5d0b207a9`**; `git diff --name-status e91819e281 HEAD` = `app/server.py` (M), `app/yearinreview_view.py` (A), `app/static/yearinreview/index.html` (A), `tests/test_yearinreview_view.py` (A), all under `infra/aws/ec2/opal-gateway/`; 0 paths outside it (numstat: server.py +5/-2, index.html +344, view.py +83, test +77) | git |
| 13 diff equality | release `git diff e91819e281 -- app/server.py` (32 lines) vs my worktree's diff of the same file (`8068200b8f..17d151f6cc`, 32 lines): body lines (+, -, context) **equal**; the whole text equal except ONE hunk header, `@@ -1008,6 +1008,9 @@` vs `@@ -994,6 +994,9 @@`, because CLOUD's server.py also carries OA-e-10's 18-line `/login` change that is not on live. Row **Z-W15-S44** | `.scratch` diffs reproduced by the two commands |
| 13 R13 (a) | release commit under `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~15`; audit log `org/git-author-override-audit.log` (shared main workspace) lines **21073 and 21074**: `2026-10-05T03:12:04Z OVERRIDE  0.9.0_WK_NFRA_OPLGTW~15  4  (--author-override 0.9.0_WK_NFRA_OPLGTW~15 applied)` and the `03:12:07Z` twin; N_FILES 4 = the four kit files | audit log |
| 14 tests, release tree | each target in its own process: `test_yearinreview_view.py` **5 passed**; `test_sprint_view.py` **8 passed**; `app/tests/test_rivalfunds_view.py` **11 passed**; `test_schwab_q7_asset_download.py` **4 passed**; `test_entitlement_admin.py::test_ogz2_ac08` **1 passed** (`DENOMINATOR 60 registered tool(s) ... 0 hit(s)`). Release tree clean after the runs (`PYTHONDONTWRITEBYTECODE=1`) | pytest |
| 15 rollback | `/c/tmp/og-rb12` detached at `e91819e281`, clean. Live S3 artifact `opal-gateway-e91819e281.tar.gz`: 97 files = 94 gateway + 3 dashboard; **94 of 94 gateway files equal the rb12 git tree, 94 of 94 equal the live md5 list, 0 only-in-artifact** | `rl7_cmp_rollback.py`, `rl7_cmp_rollback.out` |
| 16 verify script | `rl7_verify.sh before|after` + `rl7_verify.py` (reuses `rl6_host.py.txt`, `rl6_host_prelude.py.txt`, runner `rl6c_ssm.py`) + `rl7_release_md5.txt` (**96 files** = the 94 live, `app/server.py` replaced `173dbf15..` -> `b13b1e54bf22c5955f425177c799cd7c`, plus `app/yearinreview_view.py` `3895b0cf..` and `app/static/yearinreview/index.html` `1869ef21..`; equal to the og-rel12 tree 96 of 96). 15 checks in `after`: /health 200 and active; shipped md5 = release bytes; 65 tools unchanged; 50 `.env` key names unchanged; host scratch removed; **host-local GET /yearinreview with no identity = 401**; **public unauthenticated GET = 302 to login.microsoftonline.com** (not followed); pre-act read on live = download OK; r17 behaviour equals the pre-act read; download OK, held-only (49 returned, 0 unheld), held graded (49 < universe 2160), empty-holdings REFUSED `asset_read_denied_unqualified`, query OK and held-equal, synthetic / grants_written 0 / state_store_written false. Then `rl6.AC1.sh`, `rl4.AC1.sh`, `ht.AC2.sh` (the `.sh`) | `rl7_before.out`, `rl7_negative_control.out` |
| 16 `before` run | saved on live today: MainPID 664116, 50 env key names, 65 tools, /health 200, **host-local /yearinreview 404**, r17 download OK (49 returned, 0 unheld) | SSM 833f70e5 and 85d259c0, `rl7_before.out`; state file in `.scratch/` (not committed) |
| 16 negative control | `after` against the UNDEPLOYED host (served-release = `14e0af86fa`, scratch `--out`): **rc 1, VERIFY FAIL 13 of 15**: md5 93 of 96 (server.py, view.py, index.html), host-local 404; the other 13 PASS, correctly (public 302 and the r17 reads do not depend on the new release). Nothing written to `RL6_DOWNLOAD.json`; the failing run writes `RL6_DOWNLOAD.r17b_failed.json` beside it instead | `rl7_negative_control.out` |
| 16 positive control | the same script with the two undeployed-host observations forced to their deployed values (copy under `.scratch/`, scratch out dir): VERIFY PASS 15 of 15; the writer branch produced `RL6_DOWNLOAD.json` with `served_release` = the new sha, `before` carried from the r17 file (REFUSED), `after` the fresh read, and `RL6_DOWNLOAD.r17.json` byte-equal to the r17 original. Row **Z-W15-S45** | scratch, reproduced in the row |
| 16 floor on live today | `rl6.AC1.sh` PASS (r17 file, e91819e281); `rl4.AC1.sh` PASS 4 of 4; `ht.AC2.sh` PASS 4 of 4. Pre-cut reads stand: `yr.AC3.sh` FAIL (**1 of 4**, public 302 yes, host-local 404); `yr.AC4.sh` FAIL (no ledger, deployed = e91819e281) | `rl7_floor_preGO.out` |

## Blast radius, written for the three halves (read from the release diff `e91819e281..14e0af86fa`, not the README)

- **CTO (served output).** Four files change, all under `infra/aws/ec2/opal-gateway/`: `app/server.py` (+5/-2: the `yearinreview_view` import; one
  added `or yearinreview_view.is_yearinreview_path(path)` in GuardMiddleware's existing identity branch, the one `/login`, `/sprint*` and `/rivalfunds*` use; two
  `Route`s after `/rivalfunds/{day}`), plus new `app/yearinreview_view.py`, new `app/static/yearinreview/index.html` (48,022 bytes, ASCII, shipped inside the artifact), and
  new `tests/test_yearinreview_view.py` (not shipped). Served output that moves: `GET /yearinreview` goes from 404 to the page (401 with no identity; 200 with a verified
  identity; `Cache-Control: private, no-store`; framed only by self and Teams/Office hosts), `/yearinreview/` 307 to `/yearinreview`. Unchanged: every other route and tool (65
  tools, 50 env key names), the `dim_asset` download behaviour of r17, the contract. No S3 read or write (the page is inside the release), no IAM, ALB, Terraform, template or
  contract file in the diff (0 of 4 paths outside the gateway app tree). Rollback per key: re-deploy `opal-gateway-e91819e281.tar.gz` from `/c/tmp/og-rb12`; the artifact
  equals the rb12 tree file by file; the release differs from it by exactly the 4 files above.
- **COO (act).** One `safe-ec2-deploy.sh` run from `/c/tmp/og-rel12` with `DEPLOY_BASE_REF=e91819e2819df8c8df5708bc66e4f4273bb1a834 HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~15`;
  NEVER-2 ledger `nfra-oplgtw-gateway-release-r17b`, legs upload / install + verify / manifest / rollback-proven, entry AND sentinel committed first; `rl7_verify.sh` immediately;
  any failure, or `rl6.AC1` regressing: roll back, re-verify, close ROLLED BACK. The service restarts; the verify script re-reads the 50 `.env` key names after.
- **CVO (what it means).** The release publishes Andrew's Year One Operating Review page at `mcp.opalinvest.dev/yearinreview` and nothing else. **The wall is the same at the guard and
  different at the page:** the GuardMiddleware identity wall (ALB-OIDC identity, blocklist, email deny list) is identical to `/sprint`'s, but `/sprint` ALSO filters by a roster
  (`SPRINT_VIEW_ALLOWED_EMAILS`, owner-only on the host) and `/yearinreview` has no roster check, so **every signed-in tenant account can read the page, not the owner alone**
  (row **Z-W15-S46**). The ALB's own sign-in is the outer wall: an unauthenticated public GET is already 302 to `login.microsoftonline.com` today for every path. What this
  run did NOT measure: a signed-in 200 (Andrew's act at his browser; the order does not grade it) and the ALB's OIDC audience.

## Notes for the issuer
- **`yr.AC3` cannot read 4 of 4** (row **Z-W15-S42**, BLOCKING on that criterion): the deploy tarball ships `app/`, `deploy/`, `requirements.txt`, `identity_tool_allowlist.txt` only, and
  `/opt/opal-gateway/tests` does not exist on the host, so `tests/test_yearinreview_view.py` cannot be there. After a correct deploy the check reads **3 of 4**. Amend the
  check to the 3 shipped files, or place the kit's test under `app/tests/` (outside this order's `<paths>` and a change to the kit). `yr.AC4` is unaffected (it counts git paths:
  4 shipped, 0 outside the kit set).
- `rl6.AC1.sh` needs `RL6_DOWNLOAD.json` re-written for the new sha (row **Z-W15-S45**); `rl7_verify.py` does it only on a full pass and keeps the r17 file as `RL6_DOWNLOAD.r17.json`.
- The page committed on CLOUD and in the release is the repo's LF form (row **Z-W15-S43**).
- `AC2` of this order (r17 shipped set) is not re-run, as the amendment says.

## Phase C-B, when GO is given (steps 18-21)
Re-read live (`rl7_md5_host.py` through `rl6c_ssm.py`); if it moved, re-cut. Open NEVER-2 ledger `nfra-oplgtw-gateway-release-r17b`, entry AND sentinel committed first.
`rl7_verify.sh before .scratch/rl7_before.json` again immediately before the act; the act from `/c/tmp/og-rel12` with
`DEPLOY_BASE_REF=e91819e2819df8c8df5708bc66e4f4273bb1a834 HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~15` through `infra/aws/ec2/safe-ec2-deploy.sh`;
`rl7_verify.sh after .scratch/rl7_before.json <deployed sha>` IMMEDIATELY. Any FAIL: roll back from `/c/tmp/og-rb12`, re-verify, close ROLLED BACK.
The deploy wrapper's own manifest commit lands on the release branch only, as at r17 (`59cc25a023`).

Rows: `NFRA_OPLGTW-Z-W15-S42` (BLOCKING on yr.AC3, INERT), `S43`, `S44`, `S45`, `S46` (OBSERVATION, INERT); all site-z, disarm_owner `2.0.0_SA_COO~O`.
