# ANNOUNCE_OG-rl-3 -- PHASE A, `0.9.0_WK_NFRA_OPLGTW~15`, 2026-10-02 ~19:10Z

Nothing was applied, uploaded or deployed; no secret was written; no ledger is open; no manifest edit. The host was touched only by read-only SSM (4 commands, listed).
No secret value and no full identity is in this file; the only secret-adjacent reads were the owner-key variable (length only) and the identity hash compare (MATCH/DIFFER only).

| item | value |
|---|---|
| live commit | `3a7d6a7dc85fe3c54a4b63b27b59055abc9adca7` (EC2_MANIFEST `deployed_commit` at the issuance commit; S3 `opal-gateway-latest.tar.gz` metadata `git-ref` = the same sha, 472,247 bytes, last modified 2026-10-01T18:49:35Z) |
| host md5 vs live commit | **93 of 93 files match** (0 mismatch), SSM `98ab1c81-d586-482e-9ad6-513a63f58e81`; service active; `app/teams_route.py` absent on the host |
| release branch / tree | `rel-nfra-oplgtw-hx-teams` at `/c/tmp/og-rel8` (sparse cone: infra/aws/ec2, .tools, lib, infra/logic, org/ref, org/modules, org/standards, data/transcripts/scripts/outlook) |
| release HEAD | `4231bd2ddc6fd975304ed5a2c097473bdd5b41a5` (2 commits on live: `da66e3f2ff` gateway files, `4231bd2ddc` deploy-to-ec2.sh) |
| audited override | `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~15`, two uses, release-branch commits only: `da66e3f2ff`, `4231bd2ddc` |
| terraform commit (worktree branch) | `302d4eb0d5` (gateway-read-secrets.tf) |
| rollback tree | `/c/tmp/og-rb8`, detached at `3a7d6a7dc8`; artifact built, not uploaded |
| plan tree | `/c/tmp/og-tf8`, fresh sparse worktree detached at `302d4eb0d5` |
| host reads (SSM) | md5 `98ab1c81-...`; identity compare `0d2ed320-36e4-4e9f-85e1-fbda9f41675b`; verify BEFORE `1d2433a0-3fb2-4c9d-ad15-a22a898563bf`; verify negative control AFTER `c39ffdfd-9bd1-45e8-97d7-91a836082478` |

## Step 1 -- live ref by CONTENT
The manifest names `3a7d6a7dc8`; the host md5 of every shipped file (the 93-file list, reproduced from git at that ref by `rl3_release_md5`'s rule and equal to OG-tr-1's `tr_release_md5.txt`) is **93 of 93 identical**. Not an ancestor of CLOUD HEAD (M2); the release was cut from the live ref, not CLOUD.

## Step 2 -- release tree
- `teams_route.py` sha256 `f4705400...87337` and `tests/test_teams_route.py` `d7632f56...d79`: both equal the request's table.
- The three merged files carry only `db92656c72`'s hunks, applied onto the LIVE bytes (`git apply` of `db92656c72~1..db92656c72` for those three paths): `git diff 3a7d6a7dc8 -- <file>` equals `db92656c72`'s hunk line for line: **config.py 7 = 7 changed lines EQUAL; server.py 9 = 9 EQUAL; taxsma_workbook.py 7 = 7 EQUAL**. (config.py and taxsma_workbook.py also equal the CLOUD blobs, `3128d463bd6f` and `56d4f49017e4`; server.py is `6fc1f00c658a`, not `2a34bd9fe175`, because the live file differs from CLOUD's elsewhere, as M3 says.)
- **Census `git diff --stat 3a7d6a7dc8 HEAD`: 6 files, 804 insertions, 3 deletions** -- app/teams_route.py (new, 365), tests/test_teams_route.py (new, 407), app/config.py +7, app/server.py +9, app/taxsma_workbook.py +5/-2, deploy-to-ec2.sh +11/-1. Outside `infra/aws/ec2/opal-gateway/`: 0.

## Step 3 -- the template edit (hand-merged onto the LIVE `deploy-to-ec2.sh`)
Host-side `TEAMS_BEARER` read from `gateway/teams/bearer`, placed beside the Tax block (before `sudo install`, the S3 pull, the extract, the `.env` write, the restart); `|| exit 3` on a failed read, `exit 3` on empty or `None`; length printed only. The printf gains `TEAMS_BEARER=%s` and `TEAMS_BEARER_LABELS=teamsassist`.
`rl3_render_test.py` (run on the release template, live ref `3a7d6a7dc8`): **live 17 `%s` / 17 args / 48 keys; release 18 `%s` / 18 args / 50 keys, 50 unique**; the existing 48 unchanged and in order; the release format = the live format + the two lines only; PRINTF-RENDER PASS. Synthetic stubbed-`aws` runs: **failed read rc 3, empty rc 3, `None` rc 3, each before the first-write marker; a value rc 0, marker reached**; no value printed; block position 3177 < tar extract 3892 < `.env` tee 18713 < restart 19883. `bash -n` rc 0.
(The order's step 3 text says 48 -> 50 keys; `%s` goes 17 -> 18 because the label is a literal.)

## Step 4 -- tests on the release tree (`AUDIT_PATH` isolated, tree clean after)
`tests/test_teams_route.py` **14 passed**; `tests/test_taxsma_workbook.py` **21 passed**; `tests/test_mail_route.py` **10 passed**; `tests/test_mail_listing.py` **12 passed**; `tests/test_entitlement_admin.py::test_ogz2_ac08` **1 passed**: `DENOMINATOR 60 registered tool(s) (42 native + 9 integration ...) -- 0 hit(s)` on the release tree AND the same line on the LIVE tree (`/c/tmp/og-rb8`): **LIVE 60 + OWN 0 = 60**. (Two suites first skipped/failed on the sparse cone -- the Tax data contract and `data/transcripts/scripts/outlook/criterion.py` were not in the checkout -- and passed after `git sparse-checkout add org/standards data/transcripts/scripts/outlook`.)

## Step 5 -- Terraform
`gateway-read-secrets.tf` @`302d4eb0d5`: a fourth `data "aws_secretsmanager_secret" "gateway_teams_bearer"` and its ARN in the SAME statement (same action `secretsmanager:GetSecretValue`, no wildcard); the header says four. `hx-capability.tf` already carries `/hx/teams/*` (8e6872f265). Fresh sparse worktree `/c/tmp/og-tf8` of that commit, fed per Z-S27 (owner-key variables from the live grant-writer Lambda; `build_package.py` staged build; deps-layer zip copied from the main tree).
- **Targeted plan** (`-target=aws_iam_role_policy.gw_gateway_read_secrets -target=aws_lb_listener_rule.hx_capability`, saved to `.scratch/rl3_targeted.tfplan`): **`Plan: 0 to add, 2 to change, 0 to destroy.`** The policy gains `arn:...:secret:gateway/teams/bearer-93ZHiU`; rule 35 values `[/hx/mail/*, /hx/transcripts/*]` -> `[/hx/mail/*, /hx/teams/*, /hx/transcripts/*]`. Both in place. The owner key occurs 0 times in the plan text. Text: `rl3_targeted_plan.txt`.
- **Untargeted plan: `Plan: 0 to add, 3 to change, 0 to destroy.`** The third is `aws_lambda_function.mcportal_grant_writer` (source_code_hash only). NOT applied; row `NFRA_OPLGTW-Z-W15-S25`. Text: `rl3_untargeted_plan.txt`.
- The saved plan binds to this state and lineage; at GO, if the live listener rule or policy has moved, re-plan.

## Step 6 -- the identity the live template needs
`rl3_identity.py check`: `values.tenant_id + "/" + values["opalbloomberg@opalinvest.com"]` from the Part D file, its sha256 compared on the host with the sha256 of the host's current `TAXSMA_WORKBOOK_IDENTITY` (`.env` name-anchored parse, never sourced): **`IDENTITY_SHA256 MATCH`** (SSM `0d2ed320-...`). Value never printed. PHASE B export: `eval "$(python .../rl3_identity.py export)"` in the deploying shell, output never shown.

## Step 7 -- rollback, built not uploaded
`/c/tmp/og-rb8` at `3a7d6a7dc8` (clean); mcportal `a3bff71ffa` (the main repo's pin, built in a scratch detached worktree, since removed): `bun install --frozen-lockfile` + `bun run build`, then the deploy's tar step: 472,212 bytes, **96 files**. The live S3 object `opal-gateway-latest.tar.gz` (also `opal-gateway-3a7d6a7dc8.tar.gz`, both `git-ref` `3a7d6a7dc8`, 472,247 bytes) downloaded and extracted: 96 files. **`diff -rq` of the two extracted trees: empty, 96 of 96 identical** (35-byte container difference).
**Re-deploy (rollback) command** (the live template needs the identity export; `<release deploy commit>` = the live ref after the release = `4231bd2ddc6fd975304ed5a2c097473bdd5b41a5` unless the wrapper's manifest commit moves it; read it live at that time):
`cd /c/tmp/og-rb8 && eval "$(python <deliverables>/rl3_identity.py export)" && DEPLOY_BASE_REF=<live full sha> HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~15 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
It renders the 48-key `.env` (no TEAMS keys) and restores the 96-file artifact. Terraform rollback per key: revert the fourth ARN (policy back to 3), revert rule 35 to 2 values.

## Step 8 -- verify script (row W15-S24)
`rl3_verify.sh before|after <state.json>` (+ `rl3_verify.py`, `rl3_release_md5.txt` = 94 files) in this folder. `before` saved `rl3_before.json` (keys 48, tools 65, route 404). Negative control `after` on the un-deployed host: **VERIFY FAIL 5 of 9**, failing exactly the four release files, the 48 -> 50 keys, the TEAMS pair and the route refusal; the unchanged checks PASS. After a real deploy: host /health 200, 94-file md5, tool list unchanged, 48 -> 50 keys with the other 48 unchanged and TEAMS_BEARER non-empty + label `teamsassist`, ENABLED_INTEGRATIONS unchanged, 9 probe codes (Tax route included) as before, `/hx/teams/me` 401 no bearer; then `ht.AC2`, `ht.AC3` (GRAPH-SCOPE-MISSING reported, not rolled back), `ht.AC4` arms 1-2.

## Rows filed (INVESTIGATION_v1.md)
`NFRA_OPLGTW-Z-W15-S24` (the verify script's row id), `-S25` (untargeted plan's third diff), `-S26` (the ruling file absent at the issuance commit); all OBSERVATION, INERT.

## At GO (PHASE B, not authorized)
Re-read the live ref (`3a7d6a7dc8`); if moved, re-cut and re-run steps 1-9. Ledger `nfra-oplgtw-hx-teams-infra` (legs iam, alb) entry + sentinel committed, `safe-apply` of `.scratch/rl3_targeted.tfplan` from `/c/tmp/og-tf8`, `ht.AC1.sh`, close; then ledger `nfra-oplgtw-hx-teams-release`, `rl3_verify.sh before`, the act from `/c/tmp/og-rel8`, `rl3_verify.sh after`, manifest, closes, section 4. The halt gate resolves a serial file inside the calling worktree (the wrapper's comment): the issuer provisions it for the release tree if the wrapper refuses.
