# ANNOUNCE -- OA-g-2, opal-gateway narrow release (one deployer at a time, CTO ruling @75117e60d6)

Deployer: 0.9.0_WK_NFRA_OPALAI~9 (issuer 2.0.0_SA_COO~O). Task order:
org/missions/D6/NFRA/NFRA_OPALAI/task-orders/NFRA_OPALAI.TO-OA-g-2.portal-grant-release.md

STATE: announced, NOT started. Nothing on the instance has been changed, nothing has been uploaded and no
ledger is open. Waiting for GO.

BLOCKING row NFRA_OPALAI-Z-W9-S3 (ARMED, disarm_owner 2.0.0_SA_COO~O): the census reads 5 gateway files. The
face lists 4. The fifth is app/admin_grants.py, from 9a28cfbbe6, which the hand-off names. The issuer
dispositions this row before GO.

| field | value |
|---|---|
| service / instance | opal-gateway / i-07dccb1615503ac99 |
| release branch | rel-nfra-opalai-portal-grant-gateway (LOCAL, worktree /c/tmp/oa-9-rel) |
| base commit (live now) | c5f809944076dd444e50353672720dd51f67776a (OA-f-2's release, rel-nfra-opalai-zs18-gateway) |
| release commit | df724ef284bccb8b78a370d4a116a42b93115685 (base + OA-g-1 da7749916d + 9a28cfbbe6, gateway files only) |
| mcportal (dashboard bundle) | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054 (unchanged) |
| artifact to upload at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-df724ef284.tar.gz (+ opal-gateway-latest.tar.gz, as the script does). The key is absent now (head-object 404). |
| NEVER-2 ledger slug | nfra-opalai-portal-grant-gateway |

## Step 0: base, resolved by content (SSM Success, command a3708411-40a3-49eb-9005-1e16d107a4e6)

| file | live md5 | c5f8099440 | 0af72fb1d0 | 88377e148e | 1f7128201a | c97839d7c8 | f1f0fc6780 |
|---|---|---|---|---|---|---|---|
| app/identity_scope.py | 442c9755d14aa1ffbbccf5bf0fe73656 | match | no | no | no | no | no |
| app/data_entitlement.py | 85fddfe3f23e4f5e0851834bcbb3fef3 | match | match | match | no | no | no |
| app/asker_scope.py | cb7be663e09ce9c93cdf66058ad40b5f | match | match | match | match | match | match |
| app/admin_grants.py (extra) | 136bf855e95cead696dd2a780dc5235a | match | match | match | match | match | no |

Candidates checked: c5f8099440, 0af72fb1d0 and every branch tip on origin/rel-laptop-* and rel-nfra-*
(88377e148e, 1f7128201a, c97839d7c8, f1f0fc6780). Only c5f8099440 matches all three named files.
The base is c5f8099440.

## Step 2: release tree and census

`git worktree add -b rel-nfra-opalai-portal-grant-gateway /c/tmp/oa-9-rel c5f8099440`, then
`cherry-pick --no-commit da7749916d 9a28cfbbe6`. There were no conflicts.
org/standards/NFRA_OPLGTW_CONTRACT.json was restored to the base. The commit is df724ef284, under
audited override use 1 of `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPALAI~9`, the only use so far.

Census, `git -C /c/tmp/oa-9-rel diff --stat c5f8099440 HEAD -- infra/aws/ec2/opal-gateway`, rc=0: 5 files,
411 insertions and 18 deletions.
- app/admin_grants.py 10 (NOT in the face's list; row W9-S3)
- app/asker_scope.py 24
- app/data_entitlement.py 58
- ops/schwab_entitlement_admin.py 47
- tests/test_portal_grant.py 290

The whole-tree diff names the same 5 files. Each is byte-identical to its version at 9a28cfbbe6.
The nested mcportal is a local clone at a3bff71ffa.

Tests in the release tree (`python -m pytest <file> -q`, from infra/aws/ec2/opal-gateway):
- tests/test_portal_grant.py: rc=1, 2 failed, 5 passed. Both failures read the repo contract, which is
  restored to the base and has no portal_grant section (row W9-S4, OBSERVATION INERT). The control on the
  CLOUD-merged tree, with contract v1.2, gives rc=0 and 7 passed.
- tests/test_asker_scope.py: rc=0, 4 passed.
- tests/test_identity_scope.py: rc=0, 9 passed.
- tests/test_admin_grants.py: rc=0, 5 passed, 1 warning.

## Step 3: rollback (built, not uploaded)

Clean tree /c/tmp/oa-9-rb, branch rb-nfra-opalai-portal-grant-base at c5f8099440, with mcportal at
a3bff71ffa. The build-only mirror of deploy-to-ec2.sh:59-99 (no upload lines) built
opal-gateway-c5f8099440.tar.gz, 382468 bytes, rc=0. It was compared per file with the live base artifact in
S3 (ec2/opal-gateway/opal-gateway-c5f8099440.tar.gz, 382528 bytes, 2026-09-26T07:42:56Z). All 75 of 75 files
are byte-identical, including 63 of 63 .py files.

Redeploy command:
`cd /c/tmp/oa-9-rb && HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPALAI~9 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`

The halt gate was not read at this cut. The gate can take up to about 24 minutes (rows NFRA_MCPORTAL-Z-S8
and NFRA_OPALAI-Z-W8-S2). The act runs only outside US business hours (row NFRA_OPALAI-Z-S24).
At announcement, the time is 2026-09-26T12:4xZ, which is inside US business hours.

deploy-to-ec2.sh and safe-ec2-deploy.sh are byte-identical in the release and rollback trees (md5
8e3b010ca473d46dc575fc2c089630ac and f45295fb0565f1bc97dc44162c093c18).

## Step 4(i): .env render (markers only)

deploy-to-ec2.sh:196 in the release tree has 9 %s and 9 printf arguments. Every marker lands exactly on
its own key: AWS_REGION, BIND_PORT, TENANT_ID, CLIENT_ID, CLIENT_SECRET, FERNET_KEY, OTP_BEARER,
MS_INGEST_BEARER and GRAPH_READ_BEARER. The render reads ALIGNED.
