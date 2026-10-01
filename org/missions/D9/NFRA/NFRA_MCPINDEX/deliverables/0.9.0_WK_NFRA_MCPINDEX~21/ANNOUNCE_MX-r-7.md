# ANNOUNCE -- MX-r-7 PHASE A (v2, after issuer ruling A5): the Black Diamond release on the live ref d61fde4693 (MX-t-13 `blackdiamond_list_fees` + MX-t-10 `etfs_get_positioning`, `blackdiamond` in ENABLED_INTEGRATIONS, the reader ExternalId fetched on the host)

Deployer: 0.9.0_WK_NFRA_MCPINDEX~21 (issuer 2.0.0_SA_COO~MI). Order (amended A1-A5):
org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-7.bd-release.md. Pattern: MX-r-6 PHASE A (ANNOUNCE_MX-r-6_v3.md).
This file re-issues the v1 ANNOUNCE (worktree commit df1db63305). What changed is marked **[A5]**; every other section is kept current.

STATE: PHASE A only. Nothing deployed, no ledger open, nothing uploaded to S3, no `terraform apply`, no grant, identity or sign-in created or changed.
AWS contact in this re-issue was ONE read-only pair: the S3 `head-object` / `list-objects-v2` on the `-latest` artifact (git-ref metadata) and the CLOUD EC2_MANIFEST read, both Opal's own.
The v1 contact stands (S3 download of `-latest`, SSM `AWS-RunShellScript` reads of file hashes, `.env` KEY NAMES and health code, IAM / Secrets Manager / EventBridge / Lambda / CloudWatch Logs reads, `terraform plan -lock=false` with two saved plans never applied).

**[A5] BOTH BLOCKING ROWS ARE RULED AND THEIR RULINGS ARE IN THE RELEASE:**
- **Z-W21-S12 -> option B, DONE in the release.** `deploy-to-ec2.sh`'s REMOTE_SCRIPT fetches the ExternalId ON THE HOST at deploy time from `opal/mcp/opal-gateway-blackdiamond-reader-external-id` (JSON `{"data_read": <uuid>}`, per the secret_version in
  `blackdiamond_reader_iam.tf`; extracted with the same `python3.11 -c json.load` shape as GRAPH_JSON) and the LIVE `.env` printf gains exactly two keys, hand-merged onto the live line: `BLACKDIAMOND_READER_ROLE_ARN`
  (`arn:aws:iam::313476888478:role/gateway-blackdiamond-read-role`, non-secret) and `BLACKDIAMOND_READER_EXTERNAL_ID` (the fetched value, one added `%s` arg). **`.env` keys 35 -> 37 (keys only).** No gateway code change. No secret value is in the repo, this file or any log.
- **Z-W21-S13 -> Plan 6, the saved plan of record.** 6 to add, 0 to change, 0 to destroy; any change or destroy at the GO is a BLOCKING row.

## BASE-MOVED CLAUSE (A2/A3), by REF

**Every pin below is valid ONLY while the live ref is `d61fde46933221e8afbac7418f06d7525d3347c8`.** Read at 2026-10-01T04:19Z-04:22Z (the cut), 05:37:49Z-05:37:55Z (v1 ANNOUNCE) and
**06:03:05Z (immediately before this re-issue)**, unchanged: EC2_MANIFEST on CLOUD (CLOUD c11f162767) `services.opal-gateway.deployed_commit` = d61fde46933221e8afbac7418f06d7525d3347c8 (deployed_at 2026-10-01T01:38:29Z, `mcportal_commit` a3bff71ffa3f5c73aa0fb7ea1e7386434e233054, unchanged);
`-latest` carries object metadata `git-ref=d61fde46933221e8afbac7418f06d7525d3347c8` (LastModified 01:38:09Z, 430017 bytes, ETag 876918ff95069087000a7c85075c1aee); the newest keys under `ec2/opal-gateway/` are `-d61fde4693` (01:38:08Z) and `-latest` (01:38:09Z), none newer.
Host `/opt/opal-gateway` files were 87 of 87 byte-identical to the `-latest` artifact at 04:22Z, 05:35Z and 05:37Z (v1; the host was not re-read in this re-issue, the artifact and the manifest were), `/health` 200.
If the live ref is anything else at the GO or at PHASE B's first act, the release, the deploy-only tree and the rollback tree are VOID and are re-cut as below. The PHASE B deploy passes the base to the guard (`DEPLOY_BASE_REF`), so the check also happens at UPLOAD time inside `deploy-to-ec2.sh`.
Another gateway release is queued (NFRA_MCPMSP MS-d-2, `INTERNAL_READER_ROLE_ARN`): whichever lands second re-cuts on the first's ref.

## THE PINS (for G-A and both never-widen halves) **[A5: release and deploy-only commits are NEW]**

| field | value |
|---|---|
| base = LIVE ref | **d61fde46933221e8afbac7418f06d7525d3347c8** (NFRA_OPLGTW OG-t-2, live since 2026-10-01T01:38:29Z, on 42c52ed4d9) |
| how it was read | BY REF: manifest + artifact `git-ref` metadata (re-read 06:03Z) + host hashes (v1, Step 1) |
| release branch | rel-nfra-mcpindex-r5-bd-release, worktree C:/tmp/mx-rel10, never merged, never pushed |
| carrier commit (outside the gateway dir) | 6dda22dd40 (row Z-W21-S14), unchanged |
| release commit v1 (SUPERSEDED, do not deploy) | 6e2f817066 |
| **release commit (A5)** | **08e6f78940e891696f20ba1b3319fb05c5dada00** (parent 6e2f817066; `deploy-to-ec2.sh` only, +6 -1) |
| deploy-only branch | dep-nfra-mcpindex-r5-bd-release, worktree C:/tmp/mx-dep10, on CLOUD 4fb6d9e164, never merged, never pushed |
| deploy-only commit v1 (SUPERSEDED) | cfd410608f |
| **deploy-only commit (A5)** | **05e3eff56307409fab574bba620ec22ba9dd0456** (parent cfd410608f; the release's `deploy-to-ec2.sh` bytes, +6 -1; made by plain safe-commit, no override needed) |
| **gateway tree object, release = deploy-only** | **b5733d7f9d58f57b400be419e97237e975e4772f** (`git rev-parse 08e6f78940:infra/aws/ec2/opal-gateway` = `git rev-parse 05e3eff563:infra/aws/ec2/opal-gateway`; `git diff 05e3eff563 08e6f78940 -- infra/aws/ec2/opal-gateway` is 0 lines). It differs from v1's 3afbcca038 by `deploy-to-ec2.sh` only, which is not in the artifact: the v1 artifact proof (rebuilt from both trees: 89 of 89 byte-identical, 75 of 75 .py) is unchanged and was not re-run. |
| rollback tree | C:/tmp/mx-rb10, detached at d61fde4693 (gateway tree 4418daa37119a8ade04065702b1358655b052634); artifact rebuilt from it equals the live artifact **87 of 87 files (73 of 73 .py)** (v1; unchanged) |
| mcportal | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054 (the live manifest's `mcportal_commit`, unchanged); the dist used for the build-only artifacts is the one already built at C:/tmp/mx-rb9/mcportal |
| **saved plan = Plan 6** | **C:/tmp/mx-r7-bd-reader-targeted6.tfplan, sha256 0401378f8e104c6b2d54c4f4548917bc4fb0f18a6c945fa4eec5f8eab64da3a2** (re-hashed 2026-10-01T06:0xZ), planned 2026-10-01T04:37Z, render PLAN_MX-r-7_targeted_6.txt. The binary is NOT committed (a plan embeds state). |
| plan 5 (SUPERSEDED by the ruling, never to be applied) | C:/tmp/mx-r7-bd-reader-targeted.tfplan sha256 492073669134077f2ab7cfeee7d088929321dd84c34fcbbb7e1684c45719b789, render PLAN_MX-r-7_targeted_5.txt |
| artifact key at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-05e3eff563.tar.gz (+ `-latest`), both written with `git-ref` metadata by the deploy script |
| NEVER-2 ledger at GO | `nfra-mcpindex-r5-bd-release`, opened before the first act |
| manifest edit | this release's own; OG-t-2's rel-branch manifest commit dc8f99b436 is NOT merged or cherry-picked (A3) |

## Step 1: the live ref, read BY REF

- **EC2_MANIFEST on CLOUD** (`git show CLOUD:infra/aws/ec2/EC2_MANIFEST.json`; 06:03Z CLOUD was c11f162767; earlier reads 4fb6d9e164 / 052ba7e940 / c7f9fa44fa, same value): `services.opal-gateway.deployed_commit` =
  d61fde46933221e8afbac7418f06d7525d3347c8, `mcportal_commit` a3bff71ffa.
- **The artifact**: S3 `ec2/opal-gateway/` newest keys are `opal-gateway-d61fde4693.tar.gz` (01:38:08Z) and `-latest` (01:38:09Z), one ETag; `head-object` on `-latest` returns Metadata `git-ref` =
  d61fde46933221e8afbac7418f06d7525d3347c8. No key is newer.
- **The host, by content** (v1): SSM 9aadfc8c/9fedc4fb (04:22Z), 97f40c5f (05:35:42Z), 1acec96b (05:37:55Z) on i-07dccb1615503ac99: sha256 of every file under app, deploy, dashboard,
  requirements.txt and identity_tool_allowlist.txt (excluding `*.log`, `__pycache__`) against the downloaded `-latest`: **87 of 87 identical** each time. `/health` 200. `.env`: ENABLED_INTEGRATIONS =
  `ycharts opal_portal globgrph opal_discover portal_index schwab` (6 ids), 35 lines.
- **Corroboration by the ref's own tree**: the rollback tree at d61fde4693 (Step 4) equals the live artifact 87 of 87. The ref IS the live ref by content.
- Probes: probes_r7/host_read_PHASEA.txt, probes_r7/host_vs_latest_PHASEA.txt.

## Step 2: the release tree, the preservation, and the census

Cut: `git worktree add --no-checkout -b rel-nfra-mcpindex-r5-bd-release /c/tmp/mx-rel10 d61fde4693`. The two cells' GATEWAY-PATH diffs, applied with `git apply --3way --index` in CLOUD's landing order
(MX-t-10's merge landed first: `29a40f5d4c^1..29a40f5d4c`, drained @29a40f5d4c, committed @78ee79c3ba; then MX-t-13's: `d3b0efe5c6^1..d3b0efe5c6`, drained @d3b0efe5c6, committed @6ccbf91e1c), plus
`blackdiamond_reader_iam.tf`. **One textual conflict**, in `app/refs/DATA_CATALOG.yaml`: the generated-file provenance stamp (the built-by HEAD line, `version`, `built_at_git_head`, `supersedes`) differs between the live
ref (stamp 120ff9b27f, from MX-r-6's cut) and CLOUD; resolved to the cells' side, so the shipped catalog is **byte-equal to CLOUD's** (blob compare below). Nothing else conflicted. Then `deploy-to-ec2.sh`:
ENABLED_INTEGRATIONS `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (**7 ids**), and **[A5]** the ExternalId fetch plus the two `.env` keys (below); `bash -n` passes. The `workflows/atom_decomposition` emitter sources
(`emit_catalog_v02.py`, `catalog_entries/*.yaml`) are repo-level inputs of the catalog and are NOT in the artifact or the release commit.

**Blob equality of the 10 gateway files the release changes other than `deploy-to-ec2.sh`, plus the .tf, against CLOUD (v1):** 8 byte-equal to CLOUD 4fb6d9e164 (blackdiamond/__init__.py, blackdiamond/integration.py,
portal_index/integration.py, registry.py, DATA_CATALOG.yaml, test_blackdiamond.py, test_portal_index.py, blackdiamond_reader_iam.tf) and 3 byte-equal to the drained cell state `d3b0efe5c6` (data_entitlement.py,
destructive_ops.py, test_entitlement_admin.py; CLOUD has since moved them for other seats' work). 11 of 11 equal one of the two named states. `git diff --shortstat d61fde4693 08e6f78940 -- infra/aws/ec2/opal-gateway`: **11 files, 1036 insertions, 17 deletions** (v1: 1031 / 17; the +5 net is the `deploy-to-ec2.sh` edit).

**THE PRESERVATION PROOF** (probes_r7/preservation_live_vs_deployonly_PHASEA.txt, v1; the artifact-bearing files are unchanged by the A5 edit). Every file in the LIVE artifact (87) against the deploy-only artifact (89), file by file:
- **0 absent.** 2 only-in-new: `app/integrations/blackdiamond/__init__.py`, `app/integrations/blackdiamond/integration.py`.
- **82 identical (69 of 73 .py). 5 changed, each ours**, and 0 of the removed lines in them name principal, tier, rivalfunds, tenant, firm_role, FIRM_ROLE, master_admin, schwab, taxsma or mcpmsp:

| changed file | removed / added | why it is ours |
|---|---|---|
| app/data_entitlement.py | -1 / +2 | MX-t-13 (blackdiamond classification) and MX-t-10 (etfs_get_positioning joins the portal_index set; the replaced line is the MX-t-9 comment) |
| app/destructive_ops.py | -1 / +5 | MX-t-13 (the registered-tool count comment and name set, +1 tool) |
| app/integrations/portal_index/integration.py | -1 / +16 | MX-t-10 (the sixth portal_index tool; the removed line is the display_name it widens) |
| app/integrations/registry.py | -0 / +10 | MX-t-13 (the `blackdiamond` factory) |
| app/refs/DATA_CATALOG.yaml | -7 / +96 | MX-t-13 and MX-t-10 catalog rows; the 7 removed lines are the provenance stamp lines v0.3 / 120ff9b27f and the `silver_datasets: []` placeholder |

- **OG-t-2's release** (the 15 gateway files of d61fde4693: tier, principal admission, auth hardening, DCR lifetime, the `.env` roster render) is preserved whole: none of its files is among the 5 changed; 82 of 87 identical.
- **MCPMSP / ETFS_RIVALS / MX-r-6** (rivalfunds view, firm_role, tenant_registry, the Schwab host inputs and the stale-base guard): all identical to the live artifact.
- **deploy-to-ec2.sh [A5]**: `git diff --numstat d61fde4693 08e6f78940` = **+6 -1**: ONE modified line, the `.env` printf line of the LIVE script (not CLOUD's), carrying all three printf edits (the ENABLED_INTEGRATIONS value gains ` blackdiamond`;
  the two keys inserted after `SCHWAB_ACCOUNT_REF_SECRET_ID`; one `"\$BD_READER_EXTERNAL_ID"` arg after the two OG_* principal args), plus 5 inserted lines: 3 comment lines and the 2 fetch lines (`BD_EXT_JSON`, `BD_READER_EXTERNAL_ID`) beside the GRAPH_JSON / FERNET_KEY fetches.
  The `.env` printf (probes_r7/env_keys_PHASEA_v2.txt) renders **37 keys (37 distinct): the same 35 as the host, 0 host keys unrendered, and exactly the 2 new BLACKDIAMOND_* keys**; `MASTER_ADMIN_PRINCIPALS` and `WRITE_CAPABLE_PRINCIPALS` are both rendered (C2), their values coming from the deploy-time `OG_*` inputs; no value is in any file here.
  The other 35 value lines equal the live ref's render except ENABLED_INTEGRATIONS (rendered with dummy inputs, both).

**CENSUS** (release 08e6f78940 vs the live ref d61fde4693): inside the gateway dir **11 files, +1036 -17**: 5 artifact files changed (table), 2 new artifact files, `deploy-to-ec2.sh` (not in the artifact), 3 tests
(test_blackdiamond.py NEW, test_entitlement_admin.py, test_portal_index.py). Outside it, the release branch differs from d61fde4693 in exactly 3 files: `infra/aws/terraform/opal-gateway/blackdiamond_reader_iam.tf` (NEW, +182),
and the carrier `.tools/naming-gate.py` and `org/standards/NAMING_LEGACY_READS.json` (CLOUD's bytes, +236 -7; row Z-W21-S14). The artifact is **89 files** (87 live + 2).

**.env KEY CENSUS [A5] (C1: keys only, never values):** host before 35 keys (`host_read_PHASEA.txt`) -> release renders **37**. Added: `BLACKDIAMOND_READER_ROLE_ARN`, `BLACKDIAMOND_READER_EXTERNAL_ID`. Preserved: all 35, including `MASTER_ADMIN_PRINCIPALS` and `WRITE_CAPABLE_PRINCIPALS`. Dropped: none.

**The deploy-only tree vs CLOUD 4fb6d9e164** (the tree the deploy runs from): 39 files, all inside infra/aws/ec2/opal-gateway, 0 outside: 13 D, 24 M, 2 A (unchanged by the A5 commit). These are other seats' unreleased gateway work CLOUD holds and the
live ref does not, and are NOT shipped: deleted app/admin_refusals.py, app/internal_role.py, app/sender_gate.py, app/taxsma_workbook.py and their tests, tests/test_login_retire.py, tests/run_release_suites.sh,
tests/acceptance/onhost_bench.py and test_onhost_bench_grader.py, tests/test_transcript_tools.py; modified-to-the-live-ref's-bytes app/asker_scope.py, audit.py, config.py, graph.py, query_v0.py, server.py, tools.py, schwab/aws_roles.py, schwab/integration.py and 11 test, runbook and conftest
files (9 + 11 = 20 of the 24 M); the other 4 M (data_entitlement.py, destructive_ops.py, test_entitlement_admin.py, deploy-to-ec2.sh) carry this release's edits on the live ref's bytes; added deploy/NFRA_OPLGTW_CONTRACT.json and tests/test_schwab_host_inputs.py (MX-r-6's, on the live ref, not on CLOUD).

**Tests** (v1; infra/aws/ec2/opal-gateway, MOCK_GRAPH=1; probes_r7/tests_*; the A5 edit touches no tested file):
- the seven-file set (test_blackdiamond, test_portal_index, test_entitlement_admin, test_data_entitlement_guard, test_tool_classification_composition, test_opal_discover, test_query_v0_tool): **63 passed, 4 failed** in the release
  tree; the same files minus test_blackdiamond in the live-ref tree: 55 passed, 3 failed. The three common failures (test_ogz2_ac06, test_ogz1_ac05, test_ogz1_ac08) are at the live ref itself. The fourth,
  `test_opal_discover::test_index_vocabulary_routes_the_real_catalog`, also fails at CLOUD 4fb6d9e164: row Z-W21-S15.
- the 14-file broad set (deploy base guard, acceptance, MCPMSP, Schwab, OG-t-2 tests): **108 passed, 15 failed + 3 errors in BOTH trees, an IDENTICAL set of 18 of 18 names**. The release adds no failing test there.
- A full-directory run was started on both trees and killed after 13 minutes stuck on one test in each (same place in both); it is not a result.

## [A5] Row S12's resolution, proved offline and in-process (probes_r7/env_keys_PHASEA_v2.txt, bd_inputs_probe_PHASEA_v2.txt)

1. **Render**: the REMOTE_SCRIPT heredoc of the deploy-only `deploy-to-ec2.sh` expanded with the script's own variables and DUMMY OG_*/fetched inputs, its `.env` printf executed: **37 keys, 37 distinct**; host keys not rendered `[]`; rendered not on host = exactly the two BLACKDIAMOND_* keys; MASTER_ADMIN_PRINCIPALS 1 and WRITE_CAPABLE_PRINCIPALS 1.
   Control: the same render of the live ref's script gives 35 keys, 0 vs the host.
2. **In-process**, on the deploy-only gateway tree, `app.integrations.blackdiamond.integration.role_config(<the rendered env, parsed as a dotenv>)` with the real role name and a DUMMY ExternalId of the secret's real shape (a uuid, taken through the host's own `json.load(...)["data_read"]` extraction):
   `role_config: OK type=RoleConfig`, `role_arn: arn:aws:iam::313476888478:role/gateway-blackdiamond-read-role`, external_id `<dummy, len 36>`.
   **Negative control**: the live ref's render (no BLACKDIAMOND_* keys) raises `RoleConfigError: BLACKDIAMOND_READER_ROLE_ARN is not set to an IAM role ARN`, the v1 finding.
3. **Where the real value goes**: from Secrets Manager into a host shell variable, then the printf's stdin into the `.env` (mode 600, `tee ... >/dev/null`). It is not in the SSM command text (only the variable NAME `$BD_READER_EXTERNAL_ID` is), the script, the repo or any log; the script echoes nothing of it.
4. **Failure mode, named**: the host script runs `set -euo pipefail`, so if the fetch fails (secret absent, no read grant) the REMOTE_SCRIPT aborts before the `.env` is written, after the new files are installed and before the service restarts: the old process keeps serving. That is why the apply (which creates the secret and the secret policy) comes first in PHASE B, and why a failed leg rolls back from the rollback tree.

## The plan (the IAM leg) **[A5: Plan 6 is the plan]**

`terraform plan -lock=false -input=false -target=... -var mcportal_owner_key_claim=sub -var mcportal_owner_key=PLAN-ONLY-PLACEHOLDER -out=<saved>`, run from `infra/aws/terraform/opal-gateway/` of the worker tree (CLOUD 4fb6d9e164;
its `blackdiamond_reader_iam.tf` blob equals the release's). Needed here and absent from a fresh worktree, copied from the main workspace: the provider cache `.terraform/`, `infra/aws/terraform/modules` (sparse add), the
grant-writer layer zip and staged dir (read for their hashes only). 2026-10-01T04:36Z-04:37Z.

**Plan 6 (the saved plan of record): 6 to add, 0 to change, 0 to destroy:** `aws_iam_role.bd_read` (gateway-blackdiamond-read-role), `aws_iam_role_policy.bd_read_policy` (gateway-blackdiamond-read-policy),
`aws_iam_role_policy.gw_assume_bd_reader` (gateway-assume-blackdiamond-reader-policy, on opal-gateway-role), `aws_secretsmanager_secret.bd_reader_external_id`, `aws_secretsmanager_secret_version.bd_reader_external_id`,
`aws_secretsmanager_secret_policy.bd_reader_external_id_gw_read` (GetSecretValue for opal-gateway-role only); 2 outputs. Targets: `aws_iam_role_policy.gw_assume_bd_reader`, `aws_iam_role_policy.bd_read_policy`, `aws_secretsmanager_secret_policy.bd_reader_external_id_gw_read`.
The secret exists because the role's trust and the gateway's assume statement both carry a dedicated ExternalId (a uuid generated once, frozen by `ignore_changes`, held in the
secret; its value is `(sensitive value)` in the plan and is in no file). **No existing resource changes or is destroyed**; the gateway role itself is not modified, only a new inline policy is attached to it
(16 inline policies, 5018 of 10240 non-whitespace characters before it: no quota risk). Measured absent before the plan (NotFound): the role, the gateway policy and the secret.
At PHASE B: re-plan with the same three targets at the GO, apply only if byte-equal in effect to Plan 6 (any change or destroy is a BLOCKING row), through `safe-apply`, as Terraform act #1 of the train (A4 C4); never an untargeted apply.
**IAM rollback:** the role, its policy and the secret are NEW, so rollback is a targeted destroy of exactly those resources from a plan made in the rollback tree (the secret has `prevent_destroy`; its removal is a deliberate
act and the secret then enters its 30-day recovery window).

## MX-a-8's read fence beside the role's resource list (so the halves can see they are equal)

MX-a-8's record (`analysis-blackdiamond.r5.result.md`, "Read fence", read 2026-09-30) against `gateway-blackdiamond-read-policy` as planned (`blackdiamond_reader_iam.tf` in the release):

| MX-a-8 fence line | the role's statement | equal |
|---|---|---|
| `s3:GetObject` on `arn:aws:s3:::opal-data-bd/silver/fees/*` | `AllowFeesObjectReads`: Action `s3:GetObject`, `s3:GetObjectVersion`; Resource `arn:aws:s3:::opal-data-bd/silver/fees/*` (one ARN) | resource EQUAL; **the role names one action the record does not: `s3:GetObjectVersion`** (bucket versioning is Enabled, read 2026-10-01; r7.J1's evidence reads the source object BY VersionId) |
| `s3:ListBucket` on `arn:aws:s3:::opal-data-bd` with condition `s3:prefix` = `silver/fees/*` only | `AllowFeesPrefixListing`: `s3:ListBucket`, Resource `arn:aws:s3:::opal-data-bd`, `StringLike s3:prefix = silver/fees/*` | EQUAL |
| "Nothing else in the bucket: no bronze/, forwardfill_v2/, other silver/ table, logs/" | `DenyReadsOutsideTheFeesPrefix` (Deny GetObject/GetObjectVersion, NotResource the fees ARN); `DenyListingOutsideTheFeesPrefix` (Deny ListBucket, StringNotLike prefix); `DenyListingOtherBuckets` (Deny ListBucket, NotResource this bucket); `DenyAllNonReadActions` (Deny NotAction GetObject/GetObjectVersion/ListBucket on `*`) | EQUAL (explicit denies, stronger than absence) |

The role has exactly 2 Allow statements and 4 Deny statements (6 of 6); the Allow resource list is **one object ARN and one bucket ARN**. No KMS grant (the bucket reads AES256, SSE-S3, measured 2026-09-30; the live
objects' `ServerSideEncryption` AES256 re-read 2026-10-01). The bucket policy has no Deny statement (2 Allow statements: CloudFront OAC / OAI `GetObject`), so the role's identity policy alone decides. The record's address note stands: the LGIC builder address for the
property is `opal-data-assets/blackdiamond/49financial/...` (MX-a-3, R19 gap, unchanged); the fence targets the LIVE bucket. The trust: only `opal-gateway-role`, under the role's own ExternalId.
**[A5] The secret's read grant is a second, separate surface the halves see here:** `aws_secretsmanager_secret_policy.bd_reader_external_id_gw_read` allows `secretsmanager:GetSecretValue` (Resource `*`, which in a resource policy means this secret) to the principal `opal-gateway-role` only, on one secret.
The role's effective permissions can be simulated only after the apply (the role does not exist yet).

## The writer of `s3://opal-data-bd/silver/fees/` (A1, row Z-W21-S3), from a read-only trace -- ATTRIBUTED (row Z-W21-S16)

**The writer is the Lambda `bd-49f-fees-runner` (role `bd-49f-fees-runner-role`), fired daily MON-FRI at 22:20Z by the ENABLED EventBridge rule `bd-49f-fees-session-daily` through the Lambda `bd-49f-session-trigger` (runner=fees).**
- Last-modified of the newest silver partitions 2026-09-27, -28, -29: **2026-09-30T22:21:10Z**, 18 seconds after bronze `Fees_OpalCapital_Daily_2026-09-16_to_2026-09-30.xlsx` (22:20:53Z).
- CloudWatch Logs `/aws/lambda/bd-49f-fees-runner`: streams for 2026-09-28, -29, -30 end at 22:21:08Z, 22:21:09Z, 22:21:09.766Z; the 09-30 stream prints `Raw rows: 59,702, columns: 34` then `OK: silver/fees/<date>.parquet` lines.
- The role's inline policy `bd-49f-fees-runner-policy`: `s3:GetObject` and `s3:PutObject` on `opal-data-bd/bronze/fees/*` and `silver/fees/*`; `DenyCotPlane` on opal-data-cot.
- The rule `bd-49f-fees-runner-daily` (cron 30 22) is DISABLED and describes itself as superseded by the session chain. The Playwright document whose last log is the 2026-09-25 login failure is NOT the writer: `logs/fees-download-*` stop at
  2026-09-25 while bronze and silver landed through 2026-09-30.
- Not read: the hand-off event between the session trigger and the runner (named `bd-49f-session-complete` in the disabled rule's description; that rule was not read). The attribution rests on the schedule, the runner's logs and policy, and the object timestamps.
- Z-W21-S3's staleness hazard is unchanged by this (no monitor, by moratorium): the tool's answer states `as_of` and `source_as_of`.

## The tool-count delta (in-process on the extracted artifacts; probes_r7/tools_live6ids.json, tools_dep7ids.json; v1, unchanged by A5)

| | native | integration | total |
|---|---|---|---|
| live d61fde4693 artifact, 6 ids | 37 | 21 | **58** |
| deploy-only artifact, 7 ids | 37 | 23 | **60** |

**+2, 0 removed: `blackdiamond_list_fees` and `etfs_get_positioning`.** Per integration at 7 ids: ycharts 6, opal_portal 1, globgrph 2, opal_discover 2, portal_index 6 (was 5), schwab 5, blackdiamond 1 (new). Registration errors: none.
Host `/health` 200 and the 58 count are the OG-t-2 record's (58 -> 58). Registration does not read the env, so the delta holds regardless of the host inputs; **[A5] a served answer now needs the apply first (the secret), then the deploy (the fetch)**.

## What PHASE B does, in this order, on the GO (nothing below has been done) **[A5]**

1. **Ledger** `nfra-mcpindex-r5-bd-release` opened first (NEVER-2; every task family that pulls the tag is named in it). Re-read the live ref (clause above); if not d61fde4693, STOP.
2. **`safe-apply` Plan 6**, never bare `terraform apply`: re-plan the three targets at the GO, confirm 6 to add / 0 change / 0 destroy and byte-equal in effect to the saved plan (sha256 0401378f8e10...), apply through `safe-apply`.
3. **Simulate** (`simulate-principal-policy`) that `opal-gateway-role` may `secretsmanager:GetSecretValue` the secret `opal/mcp/opal-gateway-blackdiamond-reader-external-id` AND `sts:AssumeRole` `gateway-blackdiamond-read-role` (the principal-policy limb; the ExternalId condition is on the call, so record the simulate's own context-key note). A denied or implicit-deny result stops here, before any deploy.
4. **Deploy** from the deploy-only tree: `cd /c/tmp/mx-dep10 && DEPLOY_BASE_REF=d61fde46933221e8afbac7418f06d7525d3347c8 OG_MASTER_ADMIN_PRINCIPALS=<off-repo, from 2.0.0_SA_COO~O> OG_WRITE_CAPABLE_PRINCIPALS=<off-repo> HALT_ACK=1 AGENT_NAME=<deployer serial> bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
   The deploy-only worktree has no nested `mcportal/` checkout (the script builds it at `$WORKSPACE_ROOT/mcportal`): place a3bff71ffa there, as the MX-r-6 PHASE B did. If the live ref moved, the script refuses at upload with both values printed and nothing written.
5. **Read back**: (a) r7.AC2 as written (status Success, `/health` 200, shipped 2 of 2, ids enabled 7 of 7); (b) host `.env` KEY names: 7 ids and **37 keys** (the 35 + the two BLACKDIAMOND_* keys, names only); (c) tool count 58 -> 60 with exactly the two names; (d) host files equal to the deploy-only artifact's 89;
   (e) both S3 objects carry `git-ref` = 05e3eff56307409fab574bba620ec22ba9dd0456; role and policies present; (f) **one in-process `blackdiamond_list_fees` call on the host (an SSM `AWS-RunShellScript` run under the gateway's venv with the host `.env`) that does NOT raise `RoleConfigError`** (the call is recorded by outcome class and denominators, never by ExternalId or any value).
6. **Rollback on any failed leg**: `cd /c/tmp/mx-rb10 && DEPLOY_BASE_REF=<the then-live ref> ... bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` (the rollback tree's OLD script re-uploads without the new guard, intended and it renders the live 35 keys); IAM per the plan section.
7. r7.J1's material after the deploy: the issuer asks the first tool's question class through a principal session; the worker records in-process which tools the host lists and what discover names for that question. **Bear in mind row Z-W21-S15**: after MX-t-10 a bare ETF holdings ask is catalogued.

## Rows (channel INVESTIGATION_v1.md)

| id | class / hazard | what |
|---|---|---|
| NFRA_MCPINDEX-Z-W21-S12 | BLOCKING / INERT | the release shipped no BLACKDIAMOND_* host inputs. **Ruled A5 option B; resolved in release 08e6f78940.** The row stands as filed (the surprise-row gate refuses an in-place edit); the ruling is recorded on row S17; disposition is the issuer's |
| NFRA_MCPINDEX-Z-W21-S13 | BLOCKING / INERT | the saved plan is 6 to add, not 3. **Ruled A5: Plan 6, sha256 0401378f8e10...** The row stands as filed; the ruling is recorded on row S17; disposition is the issuer's |
| NFRA_MCPINDEX-Z-W21-S14 | OBSERVATION / INERT | the carrier commit and the audited overrides on the scratch release / deploy-only branches (the A5 commits needed no override) |
| NFRA_MCPINDEX-Z-W21-S15 | OBSERVATION / INERT | test_index_vocabulary_routes_the_real_catalog is red at CLOUD itself after MX-t-10's catalog row |
| NFRA_MCPINDEX-Z-W21-S16 | OBSERVATION / INERT | the silver/fees writer named (Z-W21-S3's A1 ask) |
| NFRA_MCPINDEX-Z-W21-S17 | OBSERVATION / INERT | **[A5]** the A5 rulings on S12 and S13 recorded as a NEW row, because the row gate refuses an in-place edit of an existing row |
