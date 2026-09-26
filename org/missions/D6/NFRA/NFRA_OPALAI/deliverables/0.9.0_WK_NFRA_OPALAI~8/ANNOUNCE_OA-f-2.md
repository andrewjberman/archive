# ANNOUNCE -- OA-f-2, opal-gateway narrow release (one deployer at a time, CTO ruling @75117e60d6)

Deployer: 0.9.0_WK_NFRA_OPALAI~8 (issuer 2.0.0_SA_COO~O). Task order:
org/missions/D6/NFRA/NFRA_OPALAI/task-orders/NFRA_OPALAI.TO-OA-f-2.gateway-client-scope-release.md

STATE: announced, NOT started. Nothing touched on the instance, nothing uploaded, no ledger open.
Waiting for GO.

| field | value |
|---|---|
| service / instance | opal-gateway / i-07dccb1615503ac99 |
| release branch | rel-nfra-opalai-zs18-gateway (LOCAL, worktree /c/tmp/oa-8-rel) |
| base commit (live now) | 0af72fb1d071209b953168924bc64d391dfb92ff (1.0.0_SA_CTO's laptop release, origin/rel-laptop-teams-reader-gw) |
| release commit | c5f809944076dd444e50353672720dd51f67776a (base + OA-f-1 38d47e22a9, 5 gateway files) |
| mcportal (dashboard bundle) | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054 |
| artifact to upload at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-c5f8099440.tar.gz (+ opal-gateway-latest.tar.gz, as the script does) |
| NEVER-2 ledger slug | nfra-opalai-zs18-gateway-client-scope |

## Base, resolved by content (SSM Success, command 4d421efb-8e4c-4f03-8776-6aa9399cb7d2)

| file | live md5 | 0af72fb1d0 | 88377e148e | 1f7128201a (CLOUD manifest) |
|---|---|---|---|---|
| app/identity_scope.py | 06b5f86a12007f6e3f7794e1d3b386f0 | match | match | 82b4918b... no |
| app/tools.py | 6c888e51a3c652dfe89c74654fde39e3 | match | match | 7c0d2941... no |

88377e148e (the later laptop commit, "Deploy EC2 opal-gateway @ 0af72fb1d0") changes only
infra/aws/ec2/EC2_MANIFEST.json, so the base is 0af72fb1d0.

## Census

`git -C /c/tmp/oa-8-rel diff --stat 0af72fb1d0 HEAD -- infra/aws/ec2/opal-gateway` gives 5 files
(202 insertions, 33 deletions): app/context.py, app/identity_scope.py, app/server.py,
identity_tool_allowlist.txt and tests/test_identity_scope.py. The whole-tree diff gives the same 5.
The channel file INVESTIGATION_v1.Z.md is absent at the base (a modify/delete conflict), so it was
restored to the base and not carried. There were no textual conflicts in the gateway files. Two files
auto-merged, and both sides were kept:
- identity_scope.py: the laptop's _SEED row read_chat_message_images for opalbloomberg@ stays.
- server.py: the laptop base has no taxsma_workbook import or route, and the release keeps that absence.
tests/test_identity_scope.py in the release tree: 9 passed.

## Rollback (built, not uploaded)

Clean tree /c/tmp/oa-8-rb (branch rb-nfra-opalai-zs18-base at 0af72fb1d0, mcportal at a3bff71ffa).
The build-only mirror of deploy-to-ec2.sh:60-99 produced opal-gateway-0af72fb1d0.tar.gz (381002
bytes). Compared per file with the live base artifact in S3 (381254 bytes, 2026-09-25T23:01:15Z):
70 of 75 files are byte-identical and all .py files match. The other 5 (.md/.json/.jsonl/.html) differ
only in CR bytes, the laptop's CRLF checkout.

Redeploy command:
`cd /c/tmp/oa-8-rb && HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPALAI~8 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`

The halt gate reads 0 STOP and 186 routine messages pending, so HALT_ACK=1 is the right pre-ack. It
takes about 24 minutes, not 12 (row NFRA_OPALAI-Z-W8-S2, ARMED, the issuer's call on the guard (ii)
rollback path).

## Guard 4(i), .env render (markers only)

deploy-to-ec2.sh:196 in the release tree has 9 %s and 9 markers, and each marker lands on its own key:
AWS_REGION, BIND_PORT, TENANT_ID, CLIENT_ID, CLIENT_SECRET, FERNET_KEY, OTP_BEARER, MS_INGEST_BEARER
and GRAPH_READ_BEARER. No misalignment. The script is byte-identical in the rollback tree.

## Open item carried from OA-f-1

Row NFRA_OPALAI-Z-W8-S1: tests/test_data_entitlement_guard.py still cannot be run on this device (no
moto). That row says it needs one run on a device with moto before OA-f-2 deploys. It is still unread.
