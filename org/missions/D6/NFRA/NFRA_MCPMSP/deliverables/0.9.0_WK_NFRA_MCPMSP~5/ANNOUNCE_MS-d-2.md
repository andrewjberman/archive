# ANNOUNCE -- NFRA_MCPMSP.TO-MS-d-2 PHASE A (narrow gateway release) -- 0.9.0_WK_NFRA_MCPMSP~5

STATUS: PHASE A BUILT AND MEASURED; **THE RELEASE COMMIT DOES NOT EXIST** (row NFRA_MCPMSP-Z-W5-S1, BLOCKING). The release
content is STAGED in the release worktree `C:/tmp/ms-5d-rel` (branch `rel-NFRA_MCPMSP-d2`, HEAD still the base). No deploy, no
upload, no Terraform, no push was done.

## 1. The pin

| item | value |
|---|---|
| live ref, S3 `opal-gateway-latest.tar.gz` metadata `git-ref` | `05e3eff56307409fab574bba620ec22ba9dd0456` (LastModified 2026-10-01T07:13:52Z), read at start and again immediately before this file |
| `EC2_MANIFEST.json` services.opal-gateway.deployed_commit (worktree HEAD 69a05a00de) | `05e3eff56307409fab574bba620ec22ba9dd0456`, same value |
| BASE / `DEPLOY_BASE_REF` / rollback tree | `05e3eff563` |
| release branch | `rel-NFRA_MCPMSP-d2`, local, never merged |
| release commit | NONE (blocked, row Z-W5-S1). The staged content's tree object: `3ec0d875d99a8301efd367b34c2f7b3b0c0b0451` (`git write-tree` in `C:/tmp/ms-5d-rel`), 17 files vs base, 966 insertions, 21 deletions |
| CLOUD-side commit (item 0 + both keys on CLOUD's own printf line, not shipped) | `6ebfce0a2f` on `wk-NFRA_MCPMSP-5d` |

Content picked (the `infra/aws/ec2/opal-gateway/` part only, in the order given): 5d469f8e19, df4d410b66, e912944d2f,
5af362d473, fe61befd60, 720199de7d; plus item 0 (admin_api hookup) and the hand-merged `.env` keys. Not carried: da1f54bfda.
Non-gateway paths of those commits (the surprise-channel rows) were not applied.

## 2. Gateway-file census against the base (17 files, every one this project's)

| file | A/M | justification |
|---|---|---|
| app/internal_role.py | A | MS-ig-1 (5d469f8e19) |
| app/query_v0.py | M | MS-ig-1 (5d469f8e19) |
| tests/test_mcpmsp_internal_role.py | A | MS-ig-1 |
| app/sender_gate.py | A | MS-sg-1 (df4d410b66) |
| app/asker_scope.py | M | MS-sg-1 |
| app/audit.py | M | MS-sg-1 |
| tests/test_mcpmsp_sender_gate.py | A | MS-sg-1 |
| tests/test_asker_binding.py | M | MS-sg-1 amendment 1 (e912944d2f) |
| tests/test_asker_nochannels.py | M | MS-sg-1 amendment 1 |
| tests/test_asker_scope.py | M | MS-sg-1 amendment 1 |
| tests/test_mcpmsp_asker_firm.py | M | MS-sg-1 amendment 1 |
| app/admin_refusals.py | A | MS-rq-1 (5af362d473) |
| tests/test_admin_refusals.py | A | MS-rq-1 |
| app/admin_api.py | M | item 0: `from . import admin_refusals` and `*admin_refusals.routes,` (2 lines) |
| deploy-to-ec2.sh | M | MS-r-1 (fe61befd60, 720199de7d: mcportal resolved at the manifest commit) plus the two `.env` keys, hand-merged onto the LIVE printf line |
| tests/run_release_suites.sh | A | MS-r-1 (fe61befd60) |
| tests/test_deploy_base_guard.py | M | MS-r-1 amendment (720199de7d) |

Outside the order's allowed set: 0. Files dropped from the live tree: 0 (no deletion in the diff). Live-only bytes kept: the
live printf line was edited in place (only the two keys appended before the closing `\n'`; no argument added), so
MASTER_ADMIN_PRINCIPALS, WRITE_CAPABLE_PRINCIPALS and the `BD_READER_EXTERNAL_ID` fetch/argument stay as they are at base.
Exclusion by content: no MDPF_TAXSMA TX-g-1 or NFRA_OPALAI OA-e-10 file is in the 17.

## 3. `.env` KEY set, keys only (parsed from the printf format string, never a value)

Before (base 05e3eff563): **37** keys. After (release tree): **39** keys. Difference, nothing else: `+INTERNAL_READER_ROLE_ARN`,
`+MSP_CALLING_IDENTITIES` (empty value). Both principal keys: `MASTER_ADMIN_PRINCIPALS` present y (before y), `WRITE_CAPABLE_PRINCIPALS` present y
(before y). The values for both principal keys arrive as environment in PHASE B (`OG_MASTER_ADMIN_PRINCIPALS`,
`OG_WRITE_CAPABLE_PRINCIPALS`); none appears here.

Key set after (39): MOCK_GRAPH, IDENTITY_PROVIDER, AWS_REGION, PUBLIC_BASE_URL, BIND_HOST, BIND_PORT, TENANT_ID, CLIENT_ID,
CLIENT_SECRET, FERNET_KEY, GATEWAY_JWT_PRIVATE_KEY_FILE, GATEWAY_WORKERS, AUDIT_S3_BUCKET, OTP_BEARER, OTP_BEARER_LABELS,
OTP_MAILBOX, MS_INGEST_BEARER, MS_INGEST_BEARER_LABELS, MS_INGEST_IDENTITY, GRAPH_READ_BEARER, MASTER_ADMIN_EMAILS,
WRITE_CAPABLE_EMAILS, MASTER_ADMIN_PRINCIPALS, WRITE_CAPABLE_PRINCIPALS, ENABLED_INTEGRATIONS, NFRA_OPLGTW_CONTRACT_PATH,
SCHWAB_READER_ROLE_ARN, SCHWAB_CATALOG_ROLE_ARN, SCHWAB_EXTERNAL_IDS_SECRET_ID, SCHWAB_ACCOUNT_REF_SECRET_ID,
BLACKDIAMOND_READER_ROLE_ARN, BLACKDIAMOND_READER_EXTERNAL_ID, DASHBOARD_OWNER_EMAILS, SPRINT_VIEW_ALLOWED_EMAILS,
GRANT_WRITER_FUNCTION_NAME, MCPORTAL_CHANGES_TABLE, FIRM_ROLE_ARNS, INTERNAL_READER_ROLE_ARN, MSP_CALLING_IDENTITIES.

## 4. Tool count and the ac08 pin

0 tools added. The guard suites print `registered tools 51` (OGZ1-AC4/AC6/AC7) and `DENOMINATOR 55 registered tool(s)` (OGZ2-AC8) on
the base tree and the release tree, byte-identical (diff = IDENTICAL). The order does not say which "ac08" it pins: three tests
fail identically at base and release (test_ogz1_ac05, test_ogz1_ac08, test_ogz2_ac06); see row NFRA_MCPMSP-Z-W5-S3. The release
changes none of them.

## 5. The suite line

`bash tests/run_release_suites.sh` on the release tree over: test_mcpmsp_internal_role, test_mcpmsp_sender_gate,
test_admin_refusals, test_deploy_base_guard, test_asker_binding, test_asker_nochannels, test_asker_scope,
test_mcpmsp_asker_firm, test_admin_tenants, test_admin_grants, test_admin_round2, test_query_v0_tool, test_schwab_query:
**93 passed, 0 failed, rc=0**. Tracked `audit.jsonl` md5 `2e05d36768ee9b3cad061ee0da8ca396` before and after, `git status` clean for it.
Caveat (row Z-W5-S2): test_deploy_base_guard passes only with two valid-shaped placeholder principal pairs in the environment (zero-GUID
test inputs, not the issuer's values); without them 5 of its 6 fail at the live script's `:?` guard.

## 6. Rollback proof

Rollback tree = base 05e3eff563. The live S3 tarball was downloaded (439568 bytes) and every file compared by md5 with
`git show 05e3eff563:<path>`: **89 files in the tarball: 86 MATCH, 0 MISMATCH, 3 absent from the base tree**; the 3 are
`dashboard/index.html` and `dashboard/assets/index-BP6X9XJd.js|index-BqfQgt7G.css`, the mcportal build output, which is not a
gateway file and is rebuilt from the manifest's `mcportal_commit`. All 86 gateway files, including `app/org/mcp/*`, match.

## 7. Dry read

From the release tree: `MCPORTAL_RESOLVE_ONLY=1 DEPLOY_BASE_REF=05e3eff563 bash infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
printed `MCPORTAL-RESOLVED: /tmp/tmp.fK27vCsCX6 @a3bff71ffa3f5c73aa0fb7ea1e7386434e233054` and exited `0` at line 63, before any
aws/ssh/scp/build/upload line and before the principals guard (line 170).

## 8. What PHASE B needs from the issuer

1. A way to land the release commit on `rel-NFRA_MCPMSP-d2` (row Z-W5-S1): the staged tree `3ec0d875d9...` is the content.
2. The two principal values as environment only.
3. Both never-widen halves signed.
