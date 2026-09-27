# ANNOUNCE -- OG-s-1, opal-gateway narrow release of /sprint owner-only roster, PHASE A ONLY

Deployer: 0.9.0_WK_NFRA_OPLGTW~9 (issuer 2.0.0_SA_COO~O). Task order:
org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-s-1.sprint-owner-only.md

STATE: announced, NOT started. Nothing on the instance has been changed. The only instance
contact was one read-only SSM md5sum (step 2). Nothing has been uploaded and no ledger is
open. Waiting for GO.

| field | value |
|---|---|
| service / instance | opal-gateway / i-07dccb1615503ac99 |
| release branch | rel-nfra-oplgtw-sprint-owner (LOCAL, worktree /c/tmp/og-s1-rel) |
| base commit (live now) | fe94911257c2c3c4845f5dfa8bb8128804cd05ec (OG-e-2's release) |
| release commit | 6a98a0553a (base + this cell's one deploy-to-ec2.sh commit) |
| mcportal (dashboard bundle) | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054 (unchanged; nested clone in release + rollback trees) |
| artifact to upload at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-6a98a0553a.tar.gz (+ opal-gateway-latest.tar.gz) |
| NEVER-2 ledger slug | nfra-oplgtw-sprint-owner-release |
| worker worktree (this record) | wk-NFRA_OPLGTW-9-s1, /c/tmp/og-s1, cut from CLOUD 95e499c916 |

## Step 1: the edit (deploy-to-ec2.sh, printf literal near :196)

Diff (`git diff` on wk-NFRA_OPLGTW-9-s1, commit 69fdcf1830): 1 file changed, 2 insertions(+),
1 deletion(-). Exactly: one comment line added above the printf literal citing
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260927_195xZ_CTO_O_SPRINT_OWNER_ONLY_AND_BD_MFA_USE_THE_TRUST_TOKEN_ROUTE.md@785fc4d71f`,
and `SPRINT_VIEW_ALLOWED_EMAILS=` inserted into the literal immediately after the
`DASHBOARD_OWNER_EMAILS=` segment. No new `%s`, nothing else touched. Both new lines are pure
LF (verified via `od -c` / `cat -A`, matching the file's existing line-ending convention).

Commit: 69fdcf1830 on wk-NFRA_OPLGTW-9-s1, author `0.9.0_WK_NFRA_OPLGTW~9 <...>` -- lane was
NOT refused for this commit (worker's own branch carries its own task order); no override used.

## Step 2: live commit, resolved by content (SSM Success, command 8fa0899f-37a1-4b29-b8b2-c530ed624ada)

| file (/opt/opal-gateway/app/) | live md5 | fe9491125 7 (this repo, git show) |
|---|---|---|
| access_state.py | 6d2c021b7f1c126dcb78325103e53400 | match |
| data_entitlement.py | 964504343c24d412a266da74e7108e69 | match |
| server.py | 1339aca9648e88ed754edcf902b7af26 | match |
| token_broker.py | aa08edc2a4c4d349b7c6b2d87b83729e | match |

4 of 4 match. `infra/aws/ec2/EC2_MANIFEST.json` `services.opal-gateway.deployed_commit` reads
`fe94911257c2c3c4845f5dfa8bb8128804cd05ec`, confirmed live by content. No STOP.

## Step 3: release tree, census, commit

`git worktree add -b rel-nfra-oplgtw-sprint-owner /c/tmp/og-s1-rel fe94911257`, then
`git checkout 69fdcf1830 -- infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` (this cell's own
step-1 commit, applied cleanly -- single file, no conflict).

Commit: 6a98a0553a on rel-nfra-oplgtw-sprint-owner, under
`GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~9` (issuer-authorized for this
release-branch commit; 1 of 1 use, this commit only -- lane-refused on the first attempt
because the release worktree's HEAD, fe94911257, predates this task order's own file in the
repo, so no NON-TERMINAL task order at that HEAD names the path; the override was then used).

Census, `git diff --stat fe94911257 HEAD -- infra/aws/ec2/opal-gateway`: exactly ONE file,
`deploy-to-ec2.sh`, 1 file changed, 2 insertions(+), 1 deletion(-). No other file in the
gateway tree changed.

## Step 4: render check (counts only, no address)

- `%s` count in the printf format string: 9 (unchanged from fe94911257's base, also 9 -- verified
  by parsing both the release-tree file and `git show fe94911257:...` directly).
- printf argument count: 9 (matches the `%s` count, both base and release).
- `SPRINT_VIEW_ALLOWED_EMAILS=` occurrences in the rendered `.env` (split on literal `\n`
  markers): exactly 1 (0 in the fe94911257 base, 1 in the release).
- Rendered line count: 28 (release) vs 27 (fe94911257 base) -- exactly +1 line, as expected for
  one inserted `\nKEY=value` segment.
- `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph` is present verbatim, unchanged, in both
  base and release.

## Step 5: mcportal pin

Copied `/c/tmp/og-rel/mcportal` (existing clone with node_modules, at the manifest's pin) into
`/c/tmp/og-s1-rel/mcportal` and `/c/tmp/og-s1-rb/mcportal` (`cp -r`, no `bun install` network
fetch needed for the pin-check itself). HEAD in both:
`a3bff71ffa3f5c73aa0fb7ea1e7386434e233054`, matching `EC2_MANIFEST.json`
`services.opal-gateway.mcportal_commit` exactly. `node_modules/` present in both.

## Step 6: rollback proven (built, not uploaded)

Worktree `/c/tmp/og-s1-rb`, HEAD `fe94911257c2c3c4845f5dfa8bb8128804cd05ec` (the live commit,
detached, unedited), mcportal at `a3bff71ffa3f5c73aa0fb7ea1e7386434e233054`
(`bun install --frozen-lockfile`: "Checked 77 installs across 128 packages (no changes)";
`bun run build`: `dist/index.html` produced, 268.63 kB JS + 3.65 kB CSS bundle).

A build-only mirror of `deploy-to-ec2.sh`'s tar step (app, deploy, requirements.txt,
identity_tool_allowlist.txt + the dashboard bundle at `dashboard/`, same excludes, no upload)
built `opal-gateway-fe94911257.tar.gz`, 398857 bytes, 79 files (in a scratch build dir outside
the worktree, `/c/tmp/og-s1-rb-build/`).

Live S3 artifact `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-fe94911257.tar.gz`:
398947 bytes (head-object), 79 files after extraction. `diff -rq` between the two extracted
trees: 0 differences -- 79 of 79 files byte-identical. (The two `.tar.gz` containers differ in
size/bytes only via gzip metadata; content is identical.)

Redeploy command:
`cd /c/tmp/og-s1-rb && HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~9 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`

## Surprise row filed

`NFRA_OPLGTW-Z-W9-S1` (UNDER_INVESTIGATION, disarm_owner 2.0.0_SA_COO~O): the pre-commit
risk-reflex's cross-file HOLD advisory keyed off the basename `deploy-to-ec2.sh` names three
unrelated services' deploy scripts (bd-gold-layer-runner, m365-mcp-gateway, smartx-exporter) as
danger nodes for both landed commits, citing a change_management line that is actually about
opal-gateway's own OTP_BEARER history. Advisory only -- did not block either commit.

## At GO (not done yet)

1. Read on-host over SSM: the tool-name list (expect 46), `ENABLED_INTEGRATIONS` (value only,
   must be the literal), the process env's `SPRINT_VIEW_ALLOWED_EMAILS` count (expect 0). Print
   no other `.env` line.
2. Open the ledger `nfra-oplgtw-sprint-owner-release` on `wk-NFRA_OPLGTW-9-s1`; commit the entry
   + sentinel BEFORE the act.
3. From `/c/tmp/og-s1-rel`, run
   `HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~9 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
4. Verify on host: `/health` 200; process env carries `SPRINT_VIEW_ALLOWED_EMAILS` once with 1
   entry; tool list AFTER = 46, sorted diff EMPTY; `ENABLED_INTEGRATIONS` unchanged; app md5 4/4
   = fe94911257 (this release changes no app file). Any failure: roll back, re-verify, close
   ROLLED BACK.
5. Record `infra/aws/ec2/EC2_MANIFEST.json` (LF copy): deployed_commit = the release commit,
   previous = fe94911257, deployed_at/deployed_by, mcportal unchanged, release_note. Close the
   ledger; commit the close; run the AC1-3 criteria.

Announced 2026-09-27T20:1xZ.
