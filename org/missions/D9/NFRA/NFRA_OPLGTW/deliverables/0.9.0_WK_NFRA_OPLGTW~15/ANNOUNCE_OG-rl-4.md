# ANNOUNCE_OG-rl-4 -- PHASE A, `0.9.0_WK_NFRA_OPLGTW~15`, 2026-10-03 ~01:50Z

Nothing was uploaded or deployed; no secret was written; no ledger or sentinel is open; no manifest edit. The host was touched only by read-only SSM.
No secret value and no full identifier is in this file or its sibling outputs. Four runs of the verify script read the public gateway with each route's own bearer
(held in memory, never printed): the BEFORE run and three negative-control AFTER runs (3 reads each; only status codes and top-level key names kept).

| item | value |
|---|---|
| live commit | `4231bd2ddc6fd975304ed5a2c097473bdd5b41a5` (EC2_MANIFEST `deployed_commit` at HEAD; S3 `opal-gateway-latest.tar.gz` and `opal-gateway-4231bd2ddc.tar.gz`, both 478,107 bytes, `git-ref` the same sha, last modified 2026-10-02T19:23Z) |
| host md5 vs live commit | **94 of 94 files identical, 0 mismatch, 0 host-only files under app/ and deploy/** (SSM `e2b54996-99eb-4b81-829d-5ec840894f7d`); the 94 are the live commit's app/**, deploy/**, requirements.txt, identity_tool_allowlist.txt, and the list equals rl3's `rl3_release_md5.txt` (`rl4_live_md5.txt`) |
| release branch / tree | `rel-nfra-oplgtw-r14` at `/c/tmp/og-rel9` (sparse cone: .tools, lib, infra/logic, infra/aws/ec2, org/ref, org/modules, org/standards, data/transcripts/scripts/outlook, infra/aws/lambda/mcportal/mcportal-grant-writer-lambda) |
| release HEAD | **`af2d7629702528c050860314a7867d8ea0cecfbf`** (2 commits on live: `25335f8ac3` gateway files, `af2d762970` template + test) |
| audited override | `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~15`, two uses, release-branch commits only: `25335f8ac3`, `af2d762970` |
| rollback tree | `/c/tmp/og-rb9`, detached at `4231bd2ddc`; artifact built, not uploaded |
| mcportal for the bundle | `a3bff71ffa` (manifest pin) in scratch worktree `/c/tmp/og-mcp9`: `bun install --frozen-lockfile`, `bun run build`, `dist/index.html` present |
| host reads (SSM) | md5 `e2b54996-...`; unit + process-env shape `cd9faf88-...`, `c1b4943f-3529-4c80-8706-10c1cd555b3b`; identity hash compare `2ef71046-31f9-4fdd-92d5-b9c6363ab043`; verify BEFORE `b9b5caa4-a8ab-4440-b1a6-aba6fcd6c880`; negative control AFTER (5 SSM, in `rl4_verify_negative_control.out`) |

## Step 1 -- live ref by CONTENT
Manifest names `4231bd2ddc`; host md5 of every shipped file = **94 of 94**. `4231bd2ddc` is not an ancestor of CLOUD HEAD: the release was cut from it, not from CLOUD.

## Step 2 -- audit (OG-au-1)
`git apply` of `070444e520`'s diff (app/audit.py, app/tools.py, tests/test_audit_bytes_principal.py) onto the LIVE bytes (the two live files equal `070444e520~1`'s blobs). `git diff 4231bd2ddc -- <file>` body vs `070444e520`'s own, per file: **audit.py 12 = 12 changed lines EQUAL; tools.py 8 = 8 EQUAL; test_audit_bytes_principal.py 63 = 63 EQUAL** (hunk md5 equal in all three).

## Step 3 -- symmetric shared-value refusal (OG-sr-1)
`git apply` of `03a23664b4`'s diff. Per file against `03a23664b4`'s own diff: **mail_route.py 13 = 13 EQUAL; transcript_route.py 13 = 13 EQUAL; test_mail_route.py 11 = 11 EQUAL; test_transcript_route.py 9 = 9 EQUAL** (hunk md5 equal in all four). The live and OG-sr-1-parent copies of the four files were byte-equal.
**Census `git diff --stat 4231bd2ddc HEAD`: 9 files, 225 insertions, 22 deletions** -- the seven files above (+155/-4), deploy-to-ec2.sh (+11/-15), tests/test_schwab_host_inputs.py (+59/-3). Outside `infra/aws/ec2/opal-gateway/`: 0. `app/ms_ingest.py`, `app/taxsma_workbook.py`, `app/teams_route.py` in the diff: 0. **The artifact differs from the live artifact in exactly 4 files** (app/audit.py, mail_route.py, tools.py, transcript_route.py; 97 = 97 files): the other five are not in the artifact (tests, the template). All 9 changed files are inside rl4.AC3's allowed set (outside the set 0).

## Step 4 -- `.env` shape (rows Z-S32, Z-W15-S29)
Template edit: `OTP_BEARER`, `OTP_BEARER_LABELS`, `ENABLED_INTEGRATIONS` and `MAIL_SENDER_TABLE` double-quoted; `FIRM_ROLE_ARNS` single-quoted (printf octal 047): its JSON carries double quotes and `_env_shape_host.py`'s parse does not unescape. **Five values quoted, not four** (row S29). `rl4_render_test.py` (output `rl4_render_test.out`): live 18 `%s` / 18 args / 50 keys; release 18 / 18 / 50, 50 unique, the same keys in the same order; release format minus one quote pair per value equals the live format; args line identical; PRINTF-RENDER PASS.
**MASKED SAMPLE through `_env_shape_host.py`'s own program: live `env_keys 50 whitespace_values 4 disagreeing 4` (calibration, equals the host read of 4); release `env_keys 50 whitespace_values 4 disagreeing 0`.** With a whitespace sender table: live 5, release 0. Key names unchanged at 50 including `TEAMS_BEARER` and `TEAMS_BEARER_LABELS`. Host fact read for the design (SSM `c1b4943f`): systemd 252; the live service process holds `FIRM_ROLE_ARNS` as valid JSON, 1 key, with double quotes and no backslash, and the three other whitespace values with a space and no `"` or `\`. Single-quoted behaviour under real systemd 252 is by its documented rules, not exercised in PHASE A: PHASE B's verify compares **all 50 service-process value hashes before and after** (a quoting change that altered what the app reads fails it).

## Step 5 -- roster log count (row Z-S34)
`ROSTER_COUNTS` computed from the parsed roster JSON (`len(master_admin.split(","))`, `len(write_capable.split(","))`) after the validators; the log line reads `master_admin <n> pair; write_capable <m> pairs; taxsma_workbook_identity 1 pair`. Stubbed-`aws` runs: 1 / 2 pairs reads `1 ... 2`; a 3-pair roster reads `3`.

## Step 6 -- Tax identity host-side (row Z-W15-S32)
New parse of the `taxsma_workbook_identity` key of `gateway/principals/rosters`, matched by the template's pair regex, `|| { ...; exit 3; }` before the extract and any `.env` write; `TAXSMA_WORKBOOK_IDENTITY` is the host variable the printf already renders. The `OG_TAXSMA_WORKBOOK_IDENTITY` shell input and its upload-time check are removed: **its code lines 4 on live, 0 on the release**. Validator refusals (stubbed `aws`, no value printed): **missing rc 3, non-string rc 3, empty rc 3, malformed rc 3, two pairs rc 3, each with the first-write marker NOT reached; valid rc 0, marker reached; an extra key admitted rc 0.** Position: identity read 1293 < extract 4559 < `.env` tee 19396 < restart 20566.
**PHASE B must add the key before the act**: a deploy with the key absent refuses rc 3 and leaves the host untouched. `bash -n` rc 0.

## Step 7 -- contract single source (row NFRA_MCPINDEX-Z-W19-S13)
Shipped `deploy/NFRA_OPLGTW_CONTRACT.json` sha256 `a86f7e667cfc` = `org/standards/NFRA_OPLGTW_CONTRACT.json` at this worktree's HEAD and at the main workspace's CLOUD HEAD (`5e62e3e420`): equal; the release ships it unchanged. `tests/test_schwab_host_inputs.py` gains `test_grant_writer_stages_the_contract_only_from_the_standard` (loads the grant-writer's `build_package.py`, derives its data files and stages a package into a temp dir: the contract must come from `org/standards` only and be the only `NFRA_OPLGTW_CONTRACT.json` in the package) and `test_values_that_can_hold_whitespace_are_rendered_quoted`. **Planted-mutant control** (`rl4_mutant_control.out`): unmutated 9 passed; M1 (`_CONTRACT_PATH` points at the byte-equal shipped copy) 1 failed (the stager test); M2 (shipped copy off by one byte) 2 failed (equality + stager); M3 (OTP_BEARER quoting removed) 1 failed (the quoting test); restored, tree clean, 9 passed. Two stale expectations in that file (live ENABLED_INTEGRATIONS 7 ids, `%s` count 18) failed on the LIVE bytes before any edit (row Z-W15-S28).

## Step 8 -- tests on the release tree (`AUDIT_PATH` isolated, tree clean after, audit file 0 bytes)
`test_audit_bytes_principal.py` **3 passed**; `test_mail_route.py` **11 passed**; `test_transcript_route.py` **10 passed**; `test_teams_route.py` **14 passed**; `test_schwab_host_inputs.py` **9 passed**; `test_taxsma_workbook.py` **21 passed**; `test_mail_listing.py` **12 passed**; `test_entitlement_admin.py::test_ogz2_ac08` **1 passed**: `DENOMINATOR 60 registered tool(s) (42 native + 9 integration ...) -- 0 hit(s)` on the release tree AND the same line on the LIVE tree `/c/tmp/og-rb9`: **LIVE 60 + OWN 0 = 60**. Also run (not asked): `test_deploy_base_guard.py` 6 passed.

## Step 9 -- rollback, built not uploaded
`/c/tmp/og-rb9` at `4231bd2ddc` (clean), the deploy's own tar step with the `a3bff71ffa` dashboard bundle: 97 files. The two live S3 objects downloaded and extracted: 97 files each. **`diff -rq` rollback vs `opal-gateway-latest.tar.gz`: empty; vs `opal-gateway-4231bd2ddc.tar.gz`: empty. 97 of 97 identical** (container size 477,989 vs 478,107).
**Identity export** (rollback template still reads it from the shell): `rl4_identity.py check` (from `%LOCALAPPDATA%/opal/og-principals/part_d_20260930.json`, python eval, never printed, sha256 compared on the host with the host's current `TAXSMA_WORKBOOK_IDENTITY`): **`IDENTITY_SHA256 MATCH`** (SSM `2ef71046-...`).
**Rollback command** (`<live full sha>` = read live at that time):
`cd /c/tmp/og-rb9 && eval "$(python <deliverables>/rl4_identity.py export)" && DEPLOY_BASE_REF=<live full sha> HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~15 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
It restores the 97-file artifact and the unquoted 50-key `.env`. The extra `taxsma_workbook_identity` key in the roster secret stays; it is ignored by the old template.

## Step 10 -- verify script (rows Z-W15-S30, S31)
`rl4_verify.sh before|after <state.json>` (+ `rl4_verify.py`, `rl4_release_md5.txt` = 94 files). After a real deploy: host /health 200 and service active; 94 shipped files md5 = release bytes; tool list unchanged; `.env` names equal `RL4_ENV_KEYS_BEFORE.txt` (50) and the BEFORE state; all 50 service-process value hashes equal their BEFORE hashes; ENABLED_INTEGRATIONS unchanged and both Tax keys non-empty; 10 host probe codes as before; one read per route with its OWN bearer; then `rl4.AC1.sh`, `tr.AC1.sh`, `ht.AC2.sh`. `before` saved at `.scratch/rl4_before.json` (not committed): env keys 50, process hashes 50, tools 65, /health 200; **/hx/mail listing 200, /hx/teams/me 200, /hx/transcripts 403 meeting_not_allowed**.
**Two departures from the order's text, both rows:** `/hx/transcripts` cannot return 200 (the live meeting allowlist is empty), so the arm asserts the bearer is ACCEPTED (403 `meeting_not_allowed` or 200) and not refused (401); `tr.AC1.sh` arm 4 hard-codes 48 keys and fails today, so the wrapper grades its arms 1-3 plus the 50-key host line. Negative control `after` on the un-deployed host: **VERIFY FAIL 9 of 10** (failing only the 4 release files' md5); `rl4.AC1` **3 of 4** (arm 2: disagreeing 4); `tr.AC1` 3 of 4 (stale arm 4, graded yes-with-stale-arm-4); `ht.AC2` 4 of 4.

## Rows filed (INVESTIGATION_v1.md)
`NFRA_OPLGTW-Z-W15-S28` (stale test on live bytes), `-S29` (FIRM_ROLE_ARNS single-quoted, 5 quoted values), `-S30` (transcripts 200 unproducible), `-S31` (tr.AC1 arm 4 stale), `-S32` (no key-set validator to extend); all OBSERVATION, INERT, disarm_owner `2.0.0_SA_COO~O`.

## At GO (PHASE B, not authorized)
Re-read the live ref (`4231bd2ddc`); if moved, re-cut and re-run steps 1-11. Open NEVER-2 ledger `nfra-oplgtw-gateway-release-r14` (legs: secret key, upload, install + verify, manifest, rollback-proven), commit entry and sentinel before the act. Step 13 secret key; `rl4_verify.sh before .scratch/rl4_before.json` again immediately before the act (the saved BEFORE is from PHASE A); the act from `/c/tmp/og-rel9` with `OG_TAXSMA_WORKBOOK_IDENTITY` unset; `rl4_verify.sh after` immediately. The halt gate resolves a serial file inside the calling worktree: the issuer provisions it for the release tree if the wrapper refuses.
