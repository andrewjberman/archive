# ANNOUNCE -- OG-e-2, opal-gateway narrow release of OG-e-1's email-keyed deny guard, PHASE A ONLY

Deployer: 0.9.0_WK_NFRA_OPLGTW~8 (issuer 2.0.0_SA_COO~O). Task order:
org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-e-2.email-deny-release.md

STATE: announced, NOT started. Nothing on the instance has been changed. The only instance contact was one
read-only SSM md5sum (step 1). Nothing has been uploaded and no ledger is open. Waiting for GO.

| field | value |
|---|---|
| service / instance | opal-gateway / i-07dccb1615503ac99 |
| release branch | rel-nfra-oplgtw-email-deny (LOCAL, worktree /c/tmp/og-rel) |
| base commit (live now) | 110d93fb7395d36b7bf7af82119b89b5a839cb65 (NFRA_MCPINDEX MX-r-3's release) |
| release commit | fe94911257 (base + OG-e-1's 2 gateway commits, gateway files only) |
| mcportal (dashboard bundle) | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054 (unchanged; nested clone in both trees) |
| artifact to upload at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-fe94911257.tar.gz (+ opal-gateway-latest.tar.gz) |
| NEVER-2 ledger slug | nfra-oplgtw-email-deny-release |
| worker worktree (this record) | wk-NFRA_OPLGTW-8-e2, /c/tmp/og-e2, cut from CLOUD 17f7d7b477 |

## Step 1: live commit, resolved by content (SSM Success, command 91965f35-0e57-4104-bdd5-df09aa170a62)

| file (/opt/opal-gateway/app/) | live md5 | 110d93fb73 (this repo) |
|---|---|---|
| access_state.py | d889ac69eb99873943b1393a41cce604 | match |
| data_entitlement.py | 4a248147b97addc391bd9522ac48c1b0 | match |
| server.py | 0bbd320098859380818e9f1febf47dc8 | match |
| token_broker.py | 86c6fc3b4fcc5296a7c64a5b328fdfc9 | match |

4 of 4 match. `infra/aws/ec2/EC2_MANIFEST.json` `services.opal-gateway.deployed_commit` reads
110d93fb7395d36b7bf7af82119b89b5a839cb65, confirmed live by content. No STOP.

## Step 2: this cell's commits (CLOUD, touching infra/aws/ec2/opal-gateway, author "0.9.0_WK_NFRA_OPLGTW~7 <"), oldest first

`git log --all --author="0.9.0_WK_NFRA_OPLGTW~7 <" --format="%H %s" -- infra/aws/ec2/opal-gateway` returns exactly 2:

- 06eff3b73f75d52a565f4762c73863e1680d32b2 -- build: the email-keyed deny record and its guard (row W3-S22)
- 744e4468e1222fb0d3576bb30970dca36aad133d -- fix: AMENDMENT A1 (restricted activate/prepare with no
  resolvable email raises CandidateRejected, writes nothing)

Matches the expected 06eff3b73f and 744e4468e1, no more, no fewer.

## Step 3: release tree, census, conflict, commit

`git worktree add -b rel-nfra-oplgtw-email-deny /c/tmp/og-rel 110d93fb73`, then `cherry-pick --no-commit`
06eff3b73f followed by 744e4468e1 (applied as two --no-commit picks onto the same uncommitted tree, since a
single multi-commit `--no-commit` invocation cannot `--continue` past a conflict on an uncommitted tree --
"your local changes would be overwritten by cherry-pick" -- so each commit's `--no-commit` apply/resolve was
run and staged in turn before applying the next).

Conflict: 06eff3b73f also touches
`org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/investigations/INVESTIGATION_v1.md` (a non-gateway path,
since 06eff3b73f files its own surprise row there). Resolved `git checkout --ours` (pinning it to the live
commit's bytes) + `git add`; the file shows 0 diff against 110d93fb73 after resolution. 744e4468e1 touches no
non-gateway path and applied clean.

Commit: fe94911257 on rel-nfra-oplgtw-email-deny, under `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~8`
(issuer-authorized for this release-branch commit; 1 of 1 use, this commit only).

Census, `git -C /c/tmp/og-rel diff --stat 110d93fb73 HEAD -- infra/aws/ec2/opal-gateway`: 8 files, +579/-13.
The whole-tree diff `git diff --stat 110d93fb73 HEAD` names the SAME 8 files -- 0 extra, 0 missing.

- app/: access_state.py, data_entitlement.py, server.py, token_broker.py
- ops/: schwab_entitlement_admin.py
- tests/: test_email_deny.py (new), test_owner_gate.py, test_portal_grant.py

That is exactly the union of the 2 commits' gateway-path files. No STOP.

## Step 4: tests on the release tree

`AUDIT_PATH=$(mktemp)` set first, then `python -m pytest tests/test_email_deny.py tests/test_owner_gate.py
tests/test_portal_grant.py tests/test_sprint_view.py tests/test_asker_scope.py -q -p no:cacheprovider` from
`/c/tmp/og-rel/infra/aws/ec2/opal-gateway`:

| test file | rc | result |
|---|---|---|
| test_email_deny | 0 | 11 passed |
| test_owner_gate | 0 | 5 passed |
| test_portal_grant | 1 | 2 failed, 5 passed |
| test_sprint_view | 0 | 8 passed |
| test_asker_scope | 0 | 4 passed |

Combined: rc=1, 2 failed, 33 passed (35 total). moto was not installed; no moto module was run (none of the
five named modules imports moto).

test_portal_grant's 2 failures (test_admin_accepts_portal_only_candidate, KeyError 'portal_grant';
test_admin_rejects_unknown_portal_channel, regex mismatch) are caused by the release holding
`org/standards/NFRA_OPLGTW_CONTRACT.json` (a non-gateway path, pinned to the live base per step 3) which has
no `portal_grant` contract section at 110d93fb73. Control on CLOUD @17f7d7b477 in /c/tmp/og-e2: test_portal_grant
rc=0, 7 passed. The shipped gateway diff is not implicated. Same class as MX-r-3's row NFRA_MCPINDEX-Z-W1-S8
and OA-g-2's NFRA_OPALAI-Z-W9-S4. Row filed: NFRA_OPLGTW-Z-W8-S1 (UNDER_INVESTIGATION, disarm_owner
2.0.0_SA_COO~O).

## Step 5: mcportal pin

Cloned `/c/tmp/mx-rel/mcportal` (an existing clone already at the manifest's pin) into
`/c/tmp/og-rel/mcportal` and `/c/tmp/og-rb/mcportal`; `node_modules` copied from the same source into both
so `bun install` fetches nothing. HEAD in both: a3bff71ffa3f5c73aa0fb7ea1e7386434e233054, matching
`EC2_MANIFEST.json` `services.opal-gateway.mcportal_commit` exactly.

## Step 6: rollback proven (built, not uploaded)

Clean tree `/c/tmp/og-rb`, HEAD 110d93fb7395d36b7bf7af82119b89b5a839cb65 (the live commit), mcportal at
a3bff71ffa3f5c73aa0fb7ea1e7386434e233054 (`bun install --frozen-lockfile`: "Checked 77 installs across 128
packages (no changes)"; `bun run build`: dist/index.html produced).

A build-only mirror of deploy-to-ec2.sh's tar step (app, deploy, requirements.txt,
identity_tool_allowlist.txt + the dashboard bundle at `dashboard/`, same excludes, no upload) built
`opal-gateway-110d93fb73.tar.gz`, 397077 bytes, 79 files.

Live S3 artifact `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-110d93fb73.tar.gz`:
397183 bytes (head-object), 79 files after extraction. `diff -rq` between the two extracted trees: 0
differences -- 79 of 79 files byte-identical. (The two .tar.gz containers differ in size/bytes only via gzip
metadata; content is identical.)

Redeploy command:
`cd /c/tmp/og-rb && HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~8 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`

## Step 7: .env render (markers only, no secrets)

`deploy-to-ec2.sh:196` (identical in the release tree) has 9 `%s` markers (AWS_REGION, BIND_PORT,
TENANT_ID, CLIENT_ID, CLIENT_SECRET, FERNET_KEY, OTP_BEARER, MS_INGEST_BEARER, GRAPH_READ_BEARER) and 9
printf arguments (`"${REGION}" "${GATEWAY_PORT}" "\$TENANT_ID" "\$CLIENT_ID" "\$CLIENT_SECRET" "\$FERNET_KEY"
"\$OTP_BEARER" "\$MS_INGEST_BEARER" "\$GRAPH_READ_BEARER"`) -- counts equal. The format string renders 26
lines (26 `\n` markers).

The static literal `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph` is present verbatim in the format
string (no `%s` substitution on that line); this cell adds no new integration and does not touch
`deploy-to-ec2.sh`.

The render reads ALIGNED. `deploy-to-ec2.sh` and `safe-ec2-deploy.sh` are neither edited nor authored by
this cell.

## At GO (not done yet)

1. Read on-host over SSM: the tool list (expect 46), the `.env` `ENABLED_INTEGRATIONS` line (value only),
   `/health`.
2. Open the ledger `nfra-oplgtw-email-deny-release` on `wk-NFRA_OPLGTW-8-e2` and commit the entry and its
   sentinel.
3. From `/c/tmp/og-rel`, run
   `HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~8 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
4. Read `/health` on-host. If not 200 within 90 s: roll back at once.
5. Read the tool list on-host again: 46 = 46, empty diff. Read `ENABLED_INTEGRATIONS` unchanged.
6. Record the manifest by hand on an LF copy if the wrapper's auto-commit fails, then close the ledger.

Row filed (UNDER_INVESTIGATION, disarm_owner 2.0.0_SA_COO~O): NFRA_OPLGTW-Z-W8-S1.

Announced 2026-09-27T16:5xZ.
