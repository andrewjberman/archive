# ANNOUNCE -- MX-r-3, opal-gateway narrow release, shipped DORMANT (one deployer at a time, CTO ruling @75117e60d6)

Deployer: 0.9.0_WK_NFRA_MCPINDEX~1 (issuer 2.0.0_SA_COO~O). Task order:
org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-3.narrow-release.md

STATE: announced, NOT started. Nothing on the instance has been changed. The only instance contact was one
read-only SSM md5sum (step 0). Nothing has been uploaded and no ledger is open. Waiting for GO.

| field | value |
|---|---|
| service / instance | opal-gateway / i-07dccb1615503ac99 |
| release branch | rel-nfra-mcpindex-r2-gateway (LOCAL, worktree /c/tmp/mx-rel) |
| base commit (live now) | df724ef284bccb8b78a370d4a116a42b93115685 (NFRA_OPALAI OA-g-2, branch rel-nfra-opalai-portal-grant-gateway; not an ancestor of CLOUD) |
| release commit | 110d93fb7395d36b7bf7af82119b89b5a839cb65 (base + this project's 12 gateway commits, gateway files only) |
| mcportal (dashboard bundle) | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054 (unchanged; nested clone in both trees, row NFRA_MCPINDEX-Z-W1-S9) |
| artifact to upload at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-110d93fb73.tar.gz (+ opal-gateway-latest.tar.gz, as the script does). head-object on that key: 404 now. |
| NEVER-2 ledger slug | nfra-mcpindex-r2-gateway-release |
| worker branch (ledger, manifest) | wk-NFRA_MCPINDEX-1-r3, worktree /c/tmp/mx-r3, cut from CLOUD cb5f440613 |

## Step 0: base, resolved by content (SSM Success, command e4b77b31-4c45-4450-9fb5-a1a058d8a1d1)

| file (/opt/opal-gateway/app/) | live md5 | df724ef284 | c5f8099440 | 1f7128201a |
|---|---|---|---|---|
| identity_scope.py | 442c9755d14aa1ffbbccf5bf0fe73656 | match | match | no |
| data_entitlement.py | f370003f2bb6bb0e644fcf98df4caa23 | match | no | no |
| asker_scope.py | f21b86141a7145fb70b5f77d37774d85 | match | no | no |
| admin_grants.py | 8a1cd1f5c7ba5646139fe0070592d60c | match | no | no |
| tools.py | 6c888e51a3c652dfe89c74654fde39e3 | match | match | no |

df724ef284 matches 5 of 5. The controls match 2 of 5 (c5f8099440) and 0 of 5 (1f7128201a). No branch or commit
descends from df724ef284 (`git branch -a --contains` lists only rel-nfra-opalai-portal-grant-gateway at
df724ef284 itself), so there is no later candidate. The base is df724ef284.

## Step 1: this project's commits (CLOUD, touching infra/aws/ec2/opal-gateway, author 0.9.0_WK_NFRA_MCPINDEX~<n>), oldest first

650c9a99cb (~1 MX-c-2), 119a49eef0 (~1 MX-c-4), 37f208249f (~1 MX-c-5), 4bfab1bcf2 (~2 MX-d-2),
8829b066d1 (~2 MX-d-2), 81d37aafda (~3 MX-t-8), 2c25c4c831 (~3 MX-t-8), 84a725073b (~3 MX-t-8),
d36d31f8c5 (~3 MX-t-8), bc0cde67f0 (~3 MX-t-8), e1cdb12550 (~2 MX-v-6), bcb48cf626 (~1 MX-c-5).

That is 12 by author, not the 14 in the hand-off. The other 2 are drain merges authored 2.0.0_SA_COO~O,
b10111278c and fe618516f3. Their subjects name the worker, and both have an empty remerge-diff (row
NFRA_MCPINDEX-Z-W1-S7).

## Step 2: release tree, census, conflicts, tests

`git worktree add -b rel-nfra-mcpindex-r2-gateway /c/tmp/mx-rel df724ef284`, then
`cherry-pick --no-commit` of the 12 in order. Every non-gateway path they touch (org/missions/...,
workflows/atom_decomposition/...) was pinned back to the base. Commit 110d93fb73 was made under audited
override use 1 of 1 of `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_MCPINDEX~1`. That is the only use.

Census, `git -C /c/tmp/mx-rel diff --stat df724ef284 HEAD -- infra/aws/ec2/opal-gateway`: 19 files, 2091
insertions and 12 deletions. The whole-tree diff names the same 19. The set equals the union of the 12 commits'
gateway files (0 extra, 0 missing).
- app/: data_entitlement.py, destructive_ops.py, refs/DATA_CATALOG.yaml
- app/integrations/: base.py, registry.py, globgrph/integration.py, opal_portal/integration.py,
  ycharts/integration.py, schwab/integration.py, opal_discover/{__init__,integration}.py (new),
  portal_index/{__init__,integration}.py (new)
- tests/: test_entitlement_admin.py, test_tool_classification_composition.py (new), test_opal_discover.py
  (new), test_portal_index.py (new), routing/questions.yaml (new), routing/run_routing.py (new)

18 of 19 files are byte-identical to CLOUD. test_entitlement_admin.py differs from CLOUD in one comment
only; the value 51 is the same on both.

Conflicts. All three were in tests/test_entitlement_admin.py, in test_ogz2_ac08's tool-count pin, and each
was resolved keeping both sides:
- H1, 119a49eef0: the commit's by-name composition block is added. The base's `== 46` pin (the
  read_chat_message_images line) is kept in place of the commit's `== 44` context line.
- H2, 84a725073b: base 46 + 12 (10 portal_index + 2 opal_discover) = `== 58`.
- H3, bc0cde67f0: base 46 + 5 (3 portal_index + 2 opal_discover) = `== 51`, the value CLOUD carries.

These merged with no conflict:
- app/data_entitlement.py: the INDEX_TOOLS block from 2c25c4c831 and bc0cde67f0, on top of the base's
  OA-f-1/OA-g-1 content.
- app/destructive_ops.py (119a49eef0): read_teams_attachment is now listed twice in the SAFE_TOOLS literal,
  once from the laptop's 0af72fb1d0 in the base and once from MX-c-4. This is harmless in a frozenset and
  byte-identical to CLOUD.

Tests. Each ran as `timeout 120 python -m pytest tests/<f>.py -q` from infra/aws/ec2/opal-gateway in /c/tmp/mx-rel.

| test file | rc | result |
|---|---|---|
| test_tool_classification_composition | 0 | 7 passed |
| test_portal_index | 1 | 1 failed, 6 passed |
| test_opal_discover | 0 | 4 passed |
| test_identity_scope | 0 | 9 passed |
| test_portal_grant | 1 | 2 failed, 5 passed |
| test_asker_scope | 0 | 4 passed |

- test_portal_index and test_portal_grant fail on repo files the release holds at the base: the
  catalog_entries sources and the contract's portal_grant section. Neither is shipped. The control on
  CLOUD@cb5f440613 is 7 passed each, rc=0 (row NFRA_MCPINDEX-Z-W1-S8).
- test_entitlement_admin was not run: `import moto` raises ModuleNotFoundError. Moto was not installed.

## Step 4: rollback (built, not uploaded)

The clean tree is /c/tmp/mx-rb, branch rb-nfra-mcpindex-r2-base at df724ef284, with mcportal at a3bff71ffa.
A build-only mirror of deploy-to-ec2.sh:60-100 was run, with no upload line and the tmp-dir trap removed.
- It built opal-gateway-df724ef284.tar.gz, 383861 bytes, rc=0. bun install reported "no changes".
- It was compared per file with the live base artifact in S3 (ec2/opal-gateway/opal-gateway-df724ef284.tar.gz,
  383914 bytes, 2026-09-26T23:15:30Z). All 75 of 75 files are byte-identical, including 63 of 63 .py files.

Redeploy command:
`cd /c/tmp/mx-rb && HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_MCPINDEX~1 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
(HALT_ACK=1 only when the halt gate reads 0 STOP; the gate can take ~24 minutes, accepted.)

The rollback re-uploads the same key, opal-gateway-df724ef284.tar.gz. Its content is identical, but the gzip
bytes differ.

deploy-to-ec2.sh and safe-ec2-deploy.sh are byte-identical in the release and rollback trees (md5
8e3b010ca473d46dc575fc2c089630ac and f45295fb0565f1bc97dc44162c093c18). Neither is edited.

## Guard (i): .env render (markers only, no secrets)

deploy-to-ec2.sh:196 in the release tree has 9 %s and 9 printf arguments. Rendered through both layers (the
local heredoc expansion, then the on-host printf), it gives 26 lines. Every marker lands on its own key:
TENANT_ID, CLIENT_ID, CLIENT_SECRET, FERNET_KEY, OTP_BEARER, MS_INGEST_BEARER and GRAPH_READ_BEARER.
- AWS_REGION=us-east-1, BIND_PORT=8080.
- GATEWAY_JWT_PRIVATE_KEY_FILE=/opt/opal-gateway/.jwt_key.pem.
- ENABLED_INTEGRATIONS=ycharts opal_portal globgrph, the same literal the byte-identical base script wrote at
  the 23:15Z OA-g-2 act. portal_index and opal_discover are not in it, so both stay DORMANT.

The render reads ALIGNED.

## At GO (not done yet)

1. Read on-host over SSM:
   - the tool list (expect 46);
   - the .env ENABLED_INTEGRATIONS line (value only);
   - /health, `curl 127.0.0.1:8080/health`.
2. Open the ledger nfra-mcpindex-r2-gateway-release on wk-NFRA_MCPINDEX-1-r3 and commit the entry and its
   sentinel.
3. From /c/tmp/mx-rel, run
   `HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_MCPINDEX~1 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
4. Read /health on-host. If it is not 200 within 90 s: roll back at once.
5. Read the tool list on-host again: 46 = 46, empty diff.
6. Record the manifest by hand on an LF copy if the Step-3 auto-commit fails, then close the ledger.

Rows filed (UNDER_INVESTIGATION, disarm_owner 2.0.0_SA_COO~O): NFRA_MCPINDEX-Z-W1-S7, -S8, -S9, all
OBSERVATION / INERT.

Announced 2026-09-27T03:1xZ (23:1x EDT), which is outside US business hours.
