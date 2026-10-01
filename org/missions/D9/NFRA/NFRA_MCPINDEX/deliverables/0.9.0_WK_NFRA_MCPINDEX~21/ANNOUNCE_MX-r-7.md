# ANNOUNCE -- MX-r-7 PHASE A: the Black Diamond release on the live ref d61fde4693 (MX-t-13 `blackdiamond_list_fees` + MX-t-10 `etfs_get_positioning`, `blackdiamond` in ENABLED_INTEGRATIONS), with two BLOCKING rows for the halves

Deployer: 0.9.0_WK_NFRA_MCPINDEX~21 (issuer 2.0.0_SA_COO~MI). Order (amended A1-A3):
org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-7.bd-release.md. Pattern: MX-r-6 PHASE A (ANNOUNCE_MX-r-6_v3.md).

STATE: PHASE A only. Nothing deployed, no ledger open, nothing uploaded to S3, no `terraform apply`, no grant, identity or sign-in created or changed.
AWS contact was read-only and Opal's own: S3 `head-object` / `list-objects-v2` / `cp` download of the `-latest` artifact, three SSM `AWS-RunShellScript`
reads (file hashes, `.env` KEY NAMES only, health code), IAM / Secrets Manager / EventBridge / Lambda / CloudWatch Logs reads, and `terraform plan -lock=false`
(plan only; two saved plan binaries, never applied; placeholder values for the two grant-writer owner variables).

**TWO ROWS BLOCK THE ORDER AS WRITTEN, and the halves must see them before any GO:**
- **Z-W21-S12 (BLOCKING):** the tool reads `BLACKDIAMOND_READER_ROLE_ARN` and `BLACKDIAMOND_READER_EXTERNAL_ID` from the host environment and the release's `.env` renders neither
  (0 of 35 keys). With only `blackdiamond` added, the tool registers (tool count moves +2, r7.AC2 passes) and every first call refuses with `RoleConfigError`.
- **Z-W21-S13 (BLOCKING):** the saved plan is **5 to add** (the role, its policy, the gateway's assume permission, **plus the ExternalId secret and its version**), and the secret's resource policy is a
  6th resource a targeted plan does not pull in (**6 to add** when named). The order says "only the role, its policy and the assume permission". Both plans are saved and rendered below.

The worker did not choose between the ways forward and did not edit the release for either; both are the issuer's and the halves' calls (rows carry the options).

## BASE-MOVED CLAUSE (A2/A3), by REF

**Every pin below is valid ONLY while the live ref is `d61fde46933221e8afbac7418f06d7525d3347c8`.** Read at 2026-10-01T04:19Z-04:22Z (the cut) and again
**05:37:49Z-05:37:55Z (immediately before this write)**, unchanged: EC2_MANIFEST on CLOUD `deployed_commit` d61fde4693 (deployed_at 2026-10-01T01:38:29Z, by 0.9.0_WK_NFRA_OPLGTW~12);
`-latest` carries object metadata `git-ref=d61fde46933221e8afbac7418f06d7525d3347c8` (LastModified 01:38:09Z, 430017 bytes, ETag 876918ff95069087000a7c85075c1aee); host `/opt/opal-gateway` files **87 of 87
byte-identical** to the `-latest` artifact both times (0 differ, 0 only-host, 0 only-artifact); `/health` 200. If the live ref is anything else at the GO or at PHASE B's first act, the release, the
deploy-only tree and the rollback tree are VOID and are re-cut as below. The PHASE B deploy passes the base to the guard (`DEPLOY_BASE_REF`), so the check also happens at UPLOAD time inside `deploy-to-ec2.sh`.
Another gateway release is queued (NFRA_MCPMSP MS-d-2, `INTERNAL_READER_ROLE_ARN`): whichever lands second re-cuts on the first's ref.

## THE PINS (for G-A and both never-widen halves)

| field | value |
|---|---|
| base = LIVE ref | **d61fde46933221e8afbac7418f06d7525d3347c8** (NFRA_OPLGTW OG-t-2, live since 2026-10-01T01:38:29Z, on 42c52ed4d9) |
| how it was read | BY REF: manifest + artifact `git-ref` metadata + host hashes (Step 1) |
| release branch (NEW) | rel-nfra-mcpindex-r5-bd-release, worktree C:/tmp/mx-rel10, never merged, never pushed |
| carrier commit (outside the gateway dir) | 6dda22dd40 (row Z-W21-S14) |
| **release commit** | **6e2f817066908602bbc5793e501532242a017d20** |
| deploy-only branch (NEW) | dep-nfra-mcpindex-r5-bd-release, worktree C:/tmp/mx-dep10, on CLOUD 4fb6d9e164, never merged, never pushed |
| **deploy-only commit** | **cfd410608fe5d9e62fc83f68399ebf172862d041** |
| **gateway tree object, release = deploy-only** | **3afbcca038973eee87577c1b58d2111cd0ab8ebe** (`git rev-parse 6e2f817066:infra/aws/ec2/opal-gateway` = `git rev-parse cfd410608f:infra/aws/ec2/opal-gateway`; `git diff --stat cfd410608f 6e2f817066 -- infra/aws/ec2/opal-gateway` is empty; artifacts rebuilt from both: 89 of 89 byte-identical, 75 of 75 .py) |
| rollback tree | C:/tmp/mx-rb10, detached at d61fde4693 (gateway tree 4418daa37119a8ade04065702b1358655b052634); artifact rebuilt from it equals the live artifact **87 of 87 files (73 of 73 .py)** |
| mcportal | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054 (the live manifest's `mcportal_commit`, unchanged); the dist used for the build-only artifacts is the one already built at C:/tmp/mx-rb9/mcportal |
| saved plan, 5 resources | C:/tmp/mx-r7-bd-reader-targeted.tfplan sha256 492073669134077f2ab7cfeee7d088929321dd84c34fcbbb7e1684c45719b789, planned 2026-10-01T04:36Z, render PLAN_MX-r-7_targeted_5.txt |
| saved plan, 6 resources | C:/tmp/mx-r7-bd-reader-targeted6.tfplan sha256 0401378f8e104c6b2d54c4f4548917bc4fb0f18a6c945fa4eec5f8eab64da3a2, planned 2026-10-01T04:37Z, render PLAN_MX-r-7_targeted_6.txt. The binaries are NOT committed (a plan embeds state). |
| artifact key at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-cfd410608f.tar.gz (+ `-latest`), both written with `git-ref` metadata by the deploy script |
| NEVER-2 ledger at GO | `nfra-mcpindex-r5-bd-release`, opened before the first act |
| manifest edit | this release's own; OG-t-2's rel-branch manifest commit dc8f99b436 is NOT merged or cherry-picked (A3) |

## Step 1: the live ref, read BY REF

- **EC2_MANIFEST on CLOUD** (`git show CLOUD:infra/aws/ec2/EC2_MANIFEST.json`: at 05:35Z CLOUD was 052ba7e940 and at 05:37Z c7f9fa44fa, same value; the 04:19Z cut read the worker tree's copy at 4fb6d9e164, same value): `services.opal-gateway.deployed_commit` =
  d61fde46933221e8afbac7418f06d7525d3347c8, `mcportal_commit` a3bff71ffa.
- **The artifact**: S3 `ec2/opal-gateway/` newest keys are `opal-gateway-d61fde4693.tar.gz` (01:38:08Z) and `-latest` (01:38:09Z), one ETag; `head-object` on `-latest` returns Metadata `git-ref` =
  d61fde46933221e8afbac7418f06d7525d3347c8. No key is newer.
- **The host, by content**: SSM 9aadfc8c/9fedc4fb (04:22Z), 97f40c5f (05:35:42Z), 1acec96b (05:37:55Z) on i-07dccb1615503ac99: sha256 of every file under app, deploy, dashboard,
  requirements.txt and identity_tool_allowlist.txt (excluding `*.log`, `__pycache__`) against the downloaded `-latest`: **87 of 87 identical** each time. `/health` 200. `.env`: ENABLED_INTEGRATIONS =
  `ycharts opal_portal globgrph opal_discover portal_index schwab` (6 ids), 35 lines.
- **Corroboration by the ref's own tree**: the rollback tree at d61fde4693 (Step 4) equals the live artifact 87 of 87. The ref IS the live ref by content.
- Probes: probes_r7/host_read_PHASEA.txt, probes_r7/host_vs_latest_PHASEA.txt.

## Step 2: the release tree, the preservation, and the census

Cut: `git worktree add --no-checkout -b rel-nfra-mcpindex-r5-bd-release /c/tmp/mx-rel10 d61fde4693`. The two cells' GATEWAY-PATH diffs, applied with `git apply --3way --index` in CLOUD's landing order
(MX-t-10's merge landed first: `29a40f5d4c^1..29a40f5d4c`, drained @29a40f5d4c, committed @78ee79c3ba; then MX-t-13's: `d3b0efe5c6^1..d3b0efe5c6`, drained @d3b0efe5c6, committed @6ccbf91e1c), plus
`blackdiamond_reader_iam.tf`. **One textual conflict**, in `app/refs/DATA_CATALOG.yaml`: the generated-file provenance stamp (the built-by HEAD line, `version`, `built_at_git_head`, `supersedes`) differs between the live
ref (stamp 120ff9b27f, from MX-r-6's cut) and CLOUD; resolved to the cells' side, so the shipped catalog is **byte-equal to CLOUD's** (blob compare below). Nothing else conflicted. Then `deploy-to-ec2.sh`'s
ENABLED_INTEGRATIONS: `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (**7 ids**), `bash -n` passes. The `workflows/atom_decomposition` emitter sources
(`emit_catalog_v02.py`, `catalog_entries/*.yaml`) are repo-level inputs of the catalog and are NOT in the artifact or the release commit.

**Blob equality of the 11 files the release changes other than `deploy-to-ec2.sh` (10 gateway files + the .tf), against CLOUD:** 8 byte-equal to CLOUD 4fb6d9e164 (blackdiamond/__init__.py, blackdiamond/integration.py,
portal_index/integration.py, registry.py, DATA_CATALOG.yaml, test_blackdiamond.py, test_portal_index.py, blackdiamond_reader_iam.tf) and 3 byte-equal to the drained cell state `d3b0efe5c6` (data_entitlement.py,
destructive_ops.py, test_entitlement_admin.py; CLOUD has since moved them for other seats' work). 11 of 11 equal one of the two named states. `git diff --shortstat d61fde4693 6e2f817066 -- infra/aws/ec2/opal-gateway`: **11 files, 1031 insertions, 17 deletions**.

**THE PRESERVATION PROOF** (probes_r7/preservation_live_vs_deployonly_PHASEA.txt). Every file in the LIVE artifact (87) against the deploy-only artifact (89), file by file:
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
- **deploy-to-ec2.sh**: 1 line changed vs the live ref (+1 -1, the `.env` printf's ENABLED_INTEGRATIONS value gains ` blackdiamond`); the printf renders **35 keys, the same 35** as the host (0 host keys unrendered, 0 rendered-but-absent;
  probes_r7/env_keys_PHASEA.txt), so `MASTER_ADMIN_PRINCIPALS` and `WRITE_CAPABLE_PRINCIPALS` are preserved (their values come from the deploy-time `OG_*` inputs; no value is in any file here).

**CENSUS** (release 6e2f817066 vs the live ref d61fde4693): inside the gateway dir **11 files, +1031 -17**: 5 artifact files changed (table), 2 new artifact files, `deploy-to-ec2.sh` (not in the artifact), 3 tests
(test_blackdiamond.py NEW, test_entitlement_admin.py, test_portal_index.py). Outside it, the release branch differs from d61fde4693 in exactly 3 files: `infra/aws/terraform/opal-gateway/blackdiamond_reader_iam.tf` (NEW, +182),
and the carrier `.tools/naming-gate.py` and `org/standards/NAMING_LEGACY_READS.json` (CLOUD's bytes, +236 -7; row Z-W21-S14). The artifact is **89 files** (87 live + 2).

**The deploy-only tree vs CLOUD 4fb6d9e164** (the tree the deploy runs from): 39 files, all inside infra/aws/ec2/opal-gateway, 0 outside: 13 D, 24 M, 2 A. These are other seats' unreleased gateway work CLOUD holds and the
live ref does not, and are NOT shipped: deleted app/admin_refusals.py, app/internal_role.py, app/sender_gate.py, app/taxsma_workbook.py and their tests, tests/test_login_retire.py, tests/run_release_suites.sh,
tests/acceptance/onhost_bench.py and test_onhost_bench_grader.py, tests/test_transcript_tools.py; modified-to-the-live-ref's-bytes app/asker_scope.py, audit.py, config.py, graph.py, query_v0.py, server.py, tools.py, schwab/aws_roles.py, schwab/integration.py and 11 test, runbook and conftest
files (9 + 11 = 20 of the 24 M); the other 4 M (data_entitlement.py, destructive_ops.py, test_entitlement_admin.py, deploy-to-ec2.sh) carry this release's edits on the live ref's bytes; added deploy/NFRA_OPLGTW_CONTRACT.json and tests/test_schwab_host_inputs.py (MX-r-6's, on the live ref, not on CLOUD).

**Tests** (infra/aws/ec2/opal-gateway, MOCK_GRAPH=1; probes_r7/tests_*):
- the seven-file set (test_blackdiamond, test_portal_index, test_entitlement_admin, test_data_entitlement_guard, test_tool_classification_composition, test_opal_discover, test_query_v0_tool): **63 passed, 4 failed** in the release
  tree; the same files minus test_blackdiamond in the live-ref tree: 55 passed, 3 failed. The three common failures (test_ogz2_ac06, test_ogz1_ac05, test_ogz1_ac08) are at the live ref itself. The fourth,
  `test_opal_discover::test_index_vocabulary_routes_the_real_catalog`, also fails at CLOUD 4fb6d9e164: row Z-W21-S15.
- the 14-file broad set (deploy base guard, acceptance, MCPMSP, Schwab, OG-t-2 tests): **108 passed, 15 failed + 3 errors in BOTH trees, an IDENTICAL set of 18 of 18 names**. The release adds no failing test there.
- A full-directory run was started on both trees and killed after 13 minutes stuck on one test in each (same place in both); it is not a result.

## The plan (the IAM leg)

`terraform plan -lock=false -input=false -target=... -var mcportal_owner_key_claim=sub -var mcportal_owner_key=PLAN-ONLY-PLACEHOLDER -out=<saved>`, run from `infra/aws/terraform/opal-gateway/` of the worker tree (CLOUD 4fb6d9e164;
its `blackdiamond_reader_iam.tf` blob equals the release's). Needed here and absent from a fresh worktree, copied from the main workspace: the provider cache `.terraform/`, `infra/aws/terraform/modules` (sparse add), the
grant-writer layer zip and staged dir (read for their hashes only). 2026-10-01T04:36Z-04:37Z.

| plan | targets | result |
|---|---|---|
| **5** | `aws_iam_role_policy.gw_assume_bd_reader`, `aws_iam_role_policy.bd_read_policy` | **5 to add, 0 to change, 0 to destroy**: `aws_iam_role.bd_read` (gateway-blackdiamond-read-role), `aws_iam_role_policy.bd_read_policy` (gateway-blackdiamond-read-policy), `aws_iam_role_policy.gw_assume_bd_reader` (gateway-assume-blackdiamond-reader-policy, on opal-gateway-role), **`aws_secretsmanager_secret.bd_reader_external_id`, `aws_secretsmanager_secret_version.bd_reader_external_id`**; 2 outputs |
| **6** | the two above + `aws_secretsmanager_secret_policy.bd_reader_external_id_gw_read` | **6 to add, 0 to change, 0 to destroy**: the five plus the secret's resource policy (GetSecretValue for opal-gateway-role only) |

The three the order names are in both. The secret exists because the role's trust and the gateway's assume statement both carry a dedicated ExternalId (a uuid generated once, frozen by `ignore_changes`, held in the
secret; its value is `(sensitive value)` in the plan and is in no file). **No existing resource changes or is destroyed in either plan**; the gateway role itself is not modified, only a new inline policy is attached to it
(16 inline policies, 5018 of 10240 non-whitespace characters before it: no quota risk). Measured absent before the plan (NotFound): the role, the gateway policy and the secret.
**Which of 5 or 6 is the plan to apply is the halves' ruling on row Z-W21-S13** (6 is the whole design; 5 leaves the gateway unable to read the secret). At PHASE B: re-plan with the chosen targets at the GO, apply only if byte-equal in effect, through `safe-apply`;
never an untargeted apply. **IAM rollback:** the role, its policy and the secret are NEW, so rollback is a targeted destroy of exactly those resources from a plan made in the rollback tree (the secret has `prevent_destroy`; its removal is a deliberate
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

## The tool-count delta (in-process on the extracted artifacts; probes_r7/tools_live6ids.json, tools_dep7ids.json)

| | native | integration | total |
|---|---|---|---|
| live d61fde4693 artifact, 6 ids | 37 | 21 | **58** |
| deploy-only artifact, 7 ids | 37 | 23 | **60** |

**+2, 0 removed: `blackdiamond_list_fees` and `etfs_get_positioning`.** Per integration at 7 ids: ycharts 6, opal_portal 1, globgrph 2, opal_discover 2, portal_index 6 (was 5), schwab 5, blackdiamond 1 (new). Registration errors: none.
Host `/health` 200 and the 58 count are the OG-t-2 record's (58 -> 58). **The delta holds whether or not row S12 is resolved** (registration does not read the env); a served answer needs S12 resolved.

## Row S12 in one measured line (probes_r7/bd_inputs_probe_PHASEA.txt, env_keys_PHASEA.txt)

In-process on the deploy-only artifact with the release's `.env` shape: `role_config: RAISED RoleConfigError BLACKDIAMOND_READER_ROLE_ARN is not set to an IAM role ARN`. The `.env` keys the tool names, by the code (`integration.py:79-80`):
`BLACKDIAMOND_READER_ROLE_ARN` (non-secret) and `BLACKDIAMOND_READER_EXTERNAL_ID` (the ExternalId VALUE, which exists only after the apply). Key names only; no value is in this file.

## What PHASE B would do, once the halves rule S12 and S13 (nothing below has been done)

1. Ledger `nfra-mcpindex-r5-bd-release` opened first. Re-read the live ref (clause above).
2. `safe-apply` the saved plan the halves chose (5 or 6), never bare `terraform apply`; re-plan at the GO first.
3. Deploy from the deploy-only tree: `cd /c/tmp/mx-dep10 && DEPLOY_BASE_REF=d61fde46933221e8afbac7418f06d7525d3347c8 OG_MASTER_ADMIN_PRINCIPALS=<off-repo, from 2.0.0_SA_COO~O> OG_WRITE_CAPABLE_PRINCIPALS=<off-repo> HALT_ACK=1 AGENT_NAME=<deployer serial> bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
   The deploy-only worktree has no nested `mcportal/` checkout (the script builds it at `$WORKSPACE_ROOT/mcportal`): place a3bff71ffa there, as the MX-r-6 PHASE B did. If the live ref moved, the script refuses at upload with both values printed and nothing written.
4. Read back: host `.env` names 7 ids and 35 keys (plus any keys S12's resolution adds); `/health` 200; tool count 58 -> 60 with exactly the two names; host files equal to the deploy-only artifact's 89; both S3 objects carry `git-ref` = cfd410608f...; role and policies present.
5. Rollback on any failed leg: `cd /c/tmp/mx-rb10 && DEPLOY_BASE_REF=<the then-live ref> ... bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` (the rollback tree's OLD script re-uploads without the new guard, intended); IAM per the plan section.
6. r7.J1's material after the deploy: the issuer asks the first tool's question class through a principal session; the worker records in-process which tools the host lists and what discover names for that question. **Bear in mind row Z-W21-S15**: after MX-t-10 a bare ETF holdings ask is catalogued.

## Rows filed (channel INVESTIGATION_v1.md)

| id | class / hazard | what |
|---|---|---|
| NFRA_MCPINDEX-Z-W21-S12 | BLOCKING / INERT | the release ships no BLACKDIAMOND_* host inputs; the tool fails closed after deploy |
| NFRA_MCPINDEX-Z-W21-S13 | BLOCKING / INERT | the saved plan is 5 to add (6 with the secret policy), not the 3 the order names: the ExternalId secret and its version ride in |
| NFRA_MCPINDEX-Z-W21-S14 | OBSERVATION / INERT | the carrier commit and two audited overrides on the scratch release / deploy-only branches |
| NFRA_MCPINDEX-Z-W21-S15 | OBSERVATION / INERT | test_index_vocabulary_routes_the_real_catalog is red at CLOUD itself after MX-t-10's catalog row |
| NFRA_MCPINDEX-Z-W21-S16 | OBSERVATION / INERT | the silver/fees writer named (Z-W21-S3's A1 ask) |
