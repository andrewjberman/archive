# ANNOUNCE v3 -- MX-r-6 PHASE A RE-CUT (A6) on the live ref 4ce7946426: MX-s-15, MX-q-3, the contract change, `schwab` in ENABLED_INTEGRATIONS, the Schwab host inputs, the stale-base guard, and ETFS_RIVALS' and MCPMSP's releases kept whole

Deployer: 0.9.0_WK_NFRA_MCPINDEX~19 (issuer 2.0.0_SA_COO~MI). Order (amended A1-A6):
org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-6.schwab-enable-release.md

STATE: PHASE A only. Nothing deployed, no ledger open, nothing uploaded to S3, no `terraform apply`, no grant, identity or sign-in created or
changed. AWS contact was read-only and Opal's own: `s3api list-objects-v2` / `head-object`, `s3 cp` download of the `-latest` artifact, two SSM
`AWS-RunShellScript` reads (file hashes, `.env` KEY NAMES only, health code), Secrets Manager read of the ExternalIds by the in-process proof (no
value printed), and `terraform plan -lock=false` (plan only, placeholders for the two grant-writer owner variables). v2 (release 63d6094823 / deploy-only
2e2254156e) is VOID and ROLLED-BACK; nothing of it is reused except the project commits' diff, re-applied below. MX-t-10 does NOT ride.

## BASE-MOVED CLAUSE (A4/A6), by REF

**Every pin below is valid ONLY while the live ref is `4ce794642699e78a718b8154664e1428737f996a`.** Read at 2026-09-30T16:13Z-16:15Z (the cut) and again
**17:08Z-17:09:39Z (immediately before this write)**, unchanged. If the live ref is anything else at the GO or at PHASE B's first act, the release, the
deploy-only tree and the rollback tree are VOID and are re-cut as in Step 2. The deploy passes the base to the guard (`DEPLOY_BASE_REF`, below), so the
check also happens at UPLOAD time, inside `deploy-to-ec2.sh`, not only at the GO.

## THE PINS (for G-A and both never-widen halves)

| field | value |
|---|---|
| base = LIVE ref | **4ce794642699e78a718b8154664e1428737f996a** (2.0.0_SA_COO~RV, deploy-only: 288fa78c93 + the 5 ETFS_RIVALS files; restored 2026-09-30T15:22:15Z under CTO~O Plan A) |
| how it was read | BY REF, Step 1 |
| release branch (NEW) | rel-nfra-mcpindex-r5-schwab-enable-c, worktree /c/tmp/mx-rel9, never merged, never pushed |
| **release commit** | **a5e73b6e72da1437e087821168e15a5655f60805** (audited override) |
| deploy-only branch (NEW) | dep-nfra-mcpindex-r5-schwab-enable-c, worktree /c/tmp/mx-dep9, on CLOUD d4fe6127ee, never merged, never pushed |
| **deploy-only commit** | **42c52ed4d9e834b0f1cf4f96eb83f9b0f7a183df** (audited override) |
| gateway tree object, release = deploy-only | **a3893da22ad839edb26e9537ac13d7347b02396d** (`git rev-parse a5e73b6e72:infra/aws/ec2/opal-gateway` = `git rev-parse 42c52ed4d9:infra/aws/ec2/opal-gateway`; `git diff --stat a5e73b6e72 42c52ed4d9 -- infra/aws/ec2/opal-gateway` is empty) |
| rollback tree | /c/tmp/mx-rb9, detached at 4ce794642699 (gateway tree 29b25ad6407330d556bb3013fd3dc2040e6783ed), mcportal a3bff71ffa built |
| mcportal | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054 in all three trees (the live manifest's `mcportal_commit`, unchanged) |
| guard commit on the worker branch | f1c302fbd3 (wk-nfra_mcpindex-5-19); the same diff is in the release |
| artifact key at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-42c52ed4d9.tar.gz (+ `-latest`), both written with `git-ref` metadata |
| saved plan (targeted) | /c/tmp/mx-r6-a6-schwab-read-targeted.tfplan, sha256 135af92ef7f2879c9f64d5ae692946c92a4c538a89942b22251e95d235927803, planned 2026-09-30T16:58Z; render PLAN_MX-r-6_A6_targeted.txt. The binary is NOT committed (a plan embeds state). |
| NEVER-2 ledger at GO | `nfra-mcpindex-r5-schwab-enable`, opened before the first act |
| superseded pins (VOID) | v1/v2: release 9def06ff2f, 63d6094823; deploy-only 0d3e953c76, 2e2254156e (d83183ec6b); rollback /c/tmp/mx-rb7, /c/tmp/mx-rb8; plans /c/tmp/mx-r6-schwab-read-targeted.tfplan, /c/tmp/mx-r6-a4-schwab-read-targeted.tfplan |

## Step 1: the live ref, read BY REF (16:13Z-16:15Z; re-read 17:08Z-17:09:39Z)

- **EC2_MANIFEST on CLOUD** (`git show CLOUD:infra/aws/ec2/EC2_MANIFEST.json`, CLOUD e0e7d72422 at the re-read): `services.opal-gateway.deployed_commit` =
  4ce794642699e78a718b8154664e1428737f996a, `mcportal_commit` a3bff71ffa.
- **The artifact**: S3 `ec2/opal-gateway/` has `-latest` (LastModified 15:22:18Z, 421088 bytes) and the key `opal-gateway-4ce7946426.tar.gz` (15:22:15Z, 421088 bytes)
  sharing one ETag; no key is newer (`opal-gateway-2e2254156e` at 14:41:23Z is v2's, since overwritten). The ETag is supporting evidence only.
- **The host, by content**: SSM ab7a521f-2a22-48e2-a960-21c5f90dc392 (sent 16:14:59Z) and a second read sent 17:08:12Z, both on i-07dccb1615503ac99: sha256 of every file under app,
  deploy, dashboard, requirements.txt and identity_tool_allowlist.txt (excluding `*.log`, `__pycache__`) against the downloaded `-latest`: **86 of 86 identical** both times, 0 differ,
  0 only-artifact, **1 only-host** (`deploy/NFRA_OPLGTW_CONTRACT.json`, v2's leftover, byte-equal to v3's copy; row Z-W19-S16). `/health` 200. `.env` ENABLED_INTEGRATIONS =
  `ycharts opal_portal globgrph opal_discover portal_index` (5 ids); 28 key names including `FIRM_ROLE_ARNS`; 0 `SCHWAB_*`, 0 `NFRA_OPLGTW*`.
- **Corroboration by the ref's own tree**: the rollback tree at 4ce794642699, rebuilt, equals the live artifact **86 of 86 files (73 of 73 .py)** (Step 4). The ref IS the live ref by content.
- Probes: probes/host_read_A6_1615Z_MX-r-6.txt, probes/host_vs_latest_MX-r-6_A6.txt (the 17:08Z read returned the same 86 of 86 and is summarised here).

## Step 2: the release tree, the preservation, and the census

Cut: `git worktree add --no-checkout -b rel-nfra-mcpindex-r5-schwab-enable-c /c/tmp/mx-rel9 4ce7946426`. This project's gateway changes, as the A4 release
carried them (`git diff 288fa78c93 63d6094823` limited to the gateway dir, `schwab_reader_iam.tf` and the contract = MX-s-15 925b0357a5, MX-q-3 aac92bdff8, step 0 32ebe6bee6,
line 197 9a94936ab5, A3 9def06ff2f, with MCPMSP's `FIRM_ROLE_ARNS` printf line kept and the five A3 `.env` keys added) applied with `git apply --3way --index`, **clean, 0 conflicts**
(none of the five RIVALS files is one this project changes); then the guard diff (`f1c302fbd3`), clean; then ONE release commit a5e73b6e72.
`git diff --stat 63d6094823 a5e73b6e72` = exactly the 5 ETFS_RIVALS files (+437 -2) and the guard (deploy-to-ec2.sh +81 -2, test_deploy_base_guard.py +189), nothing else.

**THE PRESERVATION PROOF** (probes/preservation_live_vs_deployonly_MX-r-6_A6.txt; probes/deploy_script_printf_merge_MX-r-6_A6.txt).
Every file in the LIVE artifact (86) against the deploy-only artifact (87), file by file:
- **0 absent.** 1 only-in-new: `deploy/NFRA_OPLGTW_CONTRACT.json` (A3).
- **77 identical (65 of 73 .py). 9 changed, each ours**, and 0 of the 19 removed lines in them name rivalfunds, MCPMSP, `tenant_firm`, `firm_role`, `tenant_registry` or `FIRM_ROLE_ARNS`:

| changed file | why it is ours |
|---|---|
| app/data_entitlement.py | MX-s-15 (dim_transaction) and MX-q-3 (gateway_query_catalog in the classification) |
| app/destructive_ops.py | MX-q-3 (+2 lines) |
| app/integrations/opal_discover/integration.py | MX-q-3 (discover names gateway_query_catalog as next_tool) |
| app/integrations/portal_index/integration.py | MX-q-3 (the 5th portal_index tool) |
| app/integrations/schwab/datasets.json | MX-s-15 (the dim_transaction declaration) |
| app/integrations/schwab/query.py | MX-s-15 |
| app/schwab_audit.py | MX-s-15 (+1 -1) |
| app/integrations/schwab/aws_roles.py | A3 (ExternalIds read from their secret; Z-W19-S12) |
| app/integrations/schwab/integration.py | A3 (passes the resolved environ to role_configs) |

- **ETFS_RIVALS**: the 4 live `rivalfunds`-named artifact files are byte-equal (4 of 4); the `rivalfunds` token count over the live `.py`/`.json` is 106 live and 106 new (**0 lines lost**); the five files of 288fa78c93..4ce7946426
  (gen_rivalfunds_location.py, rivalfunds_location.json, rivalfunds_view.py, **server.py**, app/tests/test_rivalfunds_view.py) are **5 of 5 byte-equal** release vs live ref.
- **MCPMSP**: the 13 files of 093fc247c6..288fa78c93, release vs live ref: **11 byte-equal** (access_state, admin_api, admin_tenants, asker_scope, audit, config, firm_role, tenant_registry,
  test_access_state, test_admin_tenants, test_mcpmsp_asker_firm); **2 changed, both ours**: `deploy-to-ec2.sh` and `org/standards/NFRA_OPLGTW_CONTRACT.json`.
- **deploy-to-ec2.sh**: the `.env` printf line has 29 items live and 34 in the release; the one live item not in the release is `ENABLED_INTEGRATIONS=... portal_index`, replaced by the same value plus
  ` schwab`; the other 5 added are the A3 keys; `FIRM_ROLE_ARNS` kept; `%s` count 9 and 9; the printf argument tail is byte-equal. Lines removed vs the live-ref script: 3 (the printf line, and the two `aws s3 cp` lines that gain `--metadata`). `bash -n` passes.
- **The contract**: `org/standards/NFRA_OPLGTW_CONTRACT.json` +23 -2 vs the live ref (MCPMSP's `tenant_firm` kept, step 0 added); `deploy/NFRA_OPLGTW_CONTRACT.json` is the byte copy of it.

**CENSUS** `git diff --shortstat 4ce7946426 a5e73b6e72 -- infra/aws/ec2/opal-gateway`: **22 files, 1268 insertions, 45 deletions**: the 9 changed artifact files above, the contract copy (+337), deploy-to-ec2.sh (+87 -3; not in the artifact),
and 11 test files (test_entitlement_admin, test_opal_discover, test_portal_index, test_query_v0_tool (NEW), test_schwab_catalog, test_schwab_host_inputs (NEW), test_schwab_query, test_schwab_semantics,
test_schwab_transactions (NEW), test_schwab_wiring, test_deploy_base_guard (NEW)): 9 + 1 + 1 + 11 = 22. Outside the gateway dir the release differs from 4ce7946426 in exactly 2 files:
`infra/aws/terraform/opal-gateway/schwab_reader_iam.tf` (+2) and `org/standards/NFRA_OPLGTW_CONTRACT.json` (+23 -2). `deploy-to-ec2.sh` line 197's ENABLED_INTEGRATIONS reads
`ycharts opal_portal globgrph opal_discover portal_index schwab` (6 ids); no other id moved. The artifact is **87 files** (86 live + 1).

**Tests in the release tree** (infra/aws/ec2/opal-gateway, MOCK_GRAPH=1):
- six-file set (test_entitlement_admin, test_data_entitlement_guard, test_tool_classification_composition, test_opal_discover, test_portal_index, test_query_v0_tool): **55 passed, 3 failed** (test_ogz2_ac06, test_ogz1_ac05, test_ogz1_ac08).
  The live-ref tree (rollback /c/tmp/mx-rb9, the five files): 50 passed, **4 failed** -- the same three plus test_portal_tools_catalog_refs_resolve, which the release fixes. The release adds no failing test (probes/tests_*_A6.txt).
- the five Schwab files plus test_account_ref.py and test_schwab_host_inputs.py: **76 passed**.
- MCPMSP's own tests (test_mcpmsp_asker_firm, test_admin_tenants, test_access_state): **17 passed**.
- tests/acceptance/test_local_acceptance.py: **14 passed**.
- tests/test_deploy_base_guard.py: **6 passed** (below).
- app/tests/test_rivalfunds_view.py (ETFS_RIVALS' own, byte-equal): 3 failed, 1 passed, 7 errors in the release tree AND in the live-ref tree (registry lacks a `rivalfunds` key; row Z-W19-S17). Not ours.

## THE STALE-BASE GUARD (A6) -- `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`, tests/test_deploy_base_guard.py

- **Design.** `DEPLOY_BASE_REF` is REQUIRED (env; `safe-ec2-deploy.sh` passes its environment through): unset -> `ERROR: REFUSED (no upload): DEPLOY_BASE_REF is required`, rc 2, before any AWS call.
  The live ref is READ from the artifact plane, never taken from an ETag match against a rebuilt tarball: (1) the `git-ref` object metadata the script now writes on BOTH uploads (read from `-latest`);
  (2) for a `-latest` written before the guard existed (the live one), the commit named by the one SHA-keyed object that shares `-latest`'s object (both keys are written together, so the same bytes); none or
  several -> the read fails. **An unreadable live ref refuses exactly like a different one (rc 3).** The declared ref is compared by hex prefix (>= 7) after `git rev-parse` if it is a name.
- **When.** Once early (fail fast, before the mcportal build) and **once immediately before the first `aws s3 cp`**; the second is the one that counts. On a mismatch it prints both values and exits 3 with no upload:
  `REFUSED (no upload) [immediately-before-upload]: STALE BASE -- declared base <sha> (DEPLOY_BASE_REF=...) != live ref <sha> (read <utc> from <source>)`.
- **Tests** (the real script run under bash in a throwaway workspace; `aws`, `bun`, `jq` are stubs on PATH, `s3 cp` IS the stubbed upload and is logged; nothing can reach AWS), `python -m pytest tests/test_deploy_base_guard.py`, run in the worker tree AND the release tree: **6 passed** each:
  - NEGATIVE, planted stale: live = c1, declared = c2 -> rc 3, `STALE BASE`, both values printed, **0 uploads**, refused at `[early]` (before the build).
  - POSITIVE control: declared = live (c1 full against the stub's 10-char read) -> rc 0, **2 stubbed uploads**, each with `--metadata git-ref=<HEAD sha>`, `base guard [immediately-before-upload]: declared base == live ref`.
  - MOVED at upload time: early read = c1, upload-time read = c2 -> rc 3, `[immediately-before-upload] STALE BASE`, **0 uploads**.
  - no-metadata fallback (the live case): the single SHA key sharing `-latest`'s ETag is the live ref -> declared equal proceeds (2 uploads), declared different refuses, 0 uploads.
  - unreadable live ref (no metadata, no key shares the ETag) -> rc 3, `could not be read`, 0 uploads.
  - missing `DEPLOY_BASE_REF` -> rc 2, 0 AWS calls.
  - Mutation: deleting the upload-time `base_guard_check` line fails 2 of 6 (the positive control's upload-time read and the moved test), so the tests grade the upload-time read.
- **Scope, recorded (row Z-W19-S18):** only a deploy whose tree carries this script is guarded; the currently-live `-latest` has no metadata, so the first read is the key-match fallback (it resolves to 4ce7946426 today). The rollback tree's OLD script re-uploads without the guard; that is intended (a rollback overwrites).

## Step 3: the plan (the IAM leg, unchanged)

`terraform plan -lock=false -input=false -target=aws_iam_role_policy.schwab_data_read_policy -var mcportal_owner_key_claim=sub -var mcportal_owner_key=PLAN-ONLY-PLACEHOLDER -out=/c/tmp/mx-r6-a6-schwab-read-targeted.tfplan`,
from the worker tree's Terraform dir (its `schwab_reader_iam.tf` blob 76a3076d8d45828e3177dd8f8bf1fddbbe98f1df = the release's), 2026-09-30T16:58Z. No layer zip or `.build/staged` copy was needed.
**Plan: 0 to add, 1 to change, 0 to destroy.** The diff is 8 added list elements, every one a `dim_transaction` prefix or ARN for masters 08242234 and 08335338 (`+` lines naming dim_transaction = 8, `-` lines = 0).
The body is identical to the v2 cut's plan (PLAN_MX-r-6_A4_targeted.txt) apart from the targeting warning v2's render trimmed. The gateway role, the ALB, the ExternalIds and the secrets do not appear.
At PHASE B: re-plan targeted at the GO, apply only if byte-equal in effect (the same one change) through `safe-apply`; never an untargeted apply. `gateway-rivalfunds-read-policy` and the grant-writer Lambda hash are other seats' acts and are not touched.
**IAM rollback:** the prefix list without `dim_transaction` is 4ce7946426's `schwab_reader_iam.tf` (blob da2bfee022a70dcfa4b242d39ebfbc985388f0fc, identical to 288fa78c93's and 093fc247c6's); the rolled-back live policy re-planned "No changes" at the issuer's rollback (@4b14925ac4).
After a Phase B apply the same targeted command from /c/tmp/mx-rb9 plans the 8 removals.

## Step 4: the rollback tree

/c/tmp/mx-rb9 = detached 4ce794642699, mcportal a3bff71ffa cloned beside it and built (`bun install --frozen-lockfile`, `bun run build`). A build-only mirror of deploy-to-ec2.sh:74-91 (same `tar -czf` and excludes, NO upload)
produced a 421052-byte artifact. Against the downloaded live `-latest`: **86 of 86 files byte-identical (73 of 73 .py)**, 0 only-live, 0 only-rebuilt (probes/rollback_vs_live_MX-r-6_A6.txt).
- **Host rollback command:** `cd /c/tmp/mx-rb9 && HALT_ACK=1 AGENT_NAME=<deployer serial> bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` (HALT_ACK=1 only when the halt gate reads 0 STOP;
  the rollback tree has no order at HEAD, so a worker is refused there and the issuer or the deployer identity runs it). It restores the 5-id `.env` value with `FIRM_ROLE_ARNS`, the 52-tool surface, and the 4ce7946426 artifact.
- **IAM rollback command:** `terraform -chdir=/c/tmp/mx-rb9/infra/aws/terraform/opal-gateway apply` of a targeted plan (`-target=aws_iam_role_policy.schwab_data_read_policy`) made in that tree, through `safe-apply`.

## Step 5: the deploy-only tree

`git worktree add --no-checkout -b dep-nfra-mcpindex-r5-schwab-enable-c /c/tmp/mx-dep9 CLOUD` (CLOUD d4fe6127ee), then `git rm -r -q infra/aws/ec2/opal-gateway` and `git checkout a5e73b6e72 -- infra/aws/ec2/opal-gateway`, ONE commit 42c52ed4d9.
- **Tree-object equality:** a3893da22ad839edb26e9537ac13d7347b02396d for both (pins table). The commit touches 34 files vs CLOUD, **0 outside infra/aws/ec2/opal-gateway**: 8 deleted, 23 modified, 3 added (row Z-W19-S19: other projects' unreleased gateway work is NOT shipped).
- **Artifact equality:** artifacts rebuilt (no upload) from the release and deploy-only trees: **87 of 87 byte-identical (73 of 73 .py)**, 0 only-either (probes/release_vs_deployonly_MX-r-6_A6.txt).
- **Halt gate:** at the dep tree's HEAD the MX-r-6 order is `<issued_to>0.9.0_WK_NFRA_MCPINDEX~19</issued_to>`, `<status>pending</status>`.
- **PHASE B command:** `cd /c/tmp/mx-dep9 && DEPLOY_BASE_REF=4ce794642699e78a718b8154664e1428737f996a HALT_ACK=1 AGENT_NAME=<deployer serial> bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
  If the live ref moved, the script refuses at upload with both values printed and nothing written.

## The tool-count delta (in-process on the extracted artifacts; probes/tools_A6_live5ids_MX-r-6.json, tools_A6_dep6ids_MX-r-6.json, tool_delta_A6.txt)

| | native | integration | total |
|---|---|---|---|
| live 4ce794642699 artifact, 5 ids | 37 | 15 | **52** |
| deploy-only artifact, 6 ids | 37 | 21 | **58** |

**+6, 0 removed**: `schwab_get_access`, `schwab_list_files`, `schwab_describe_dataset`, `schwab_query`, `schwab_prepare_download`, `gateway_query_catalog`. Per integration at 6 ids: ycharts 6, opal_portal 1, globgrph 2,
opal_discover 2, portal_index 5, schwab 5. Registration errors: none. (ETFS_RIVALS' `/rivalfunds` is a route set, not a tool: 52 is still the live count.)

## THE IN-PROCESS PROOF (A3, re-run on the NEW deploy-only artifact; probes/inprocess_schwab_host_inputs_MX-r-6_A6.txt, run 16:56Z)

The deploy-only artifact is extracted to C:/tmp/hs-dep9/opal-gateway; the environment is the operator's own AWS read credentials plus ONLY the five static keys the release's `.env` printf writes (parsed from the
deploy-only tree's script, `${REMOTE_DIR}` mapped to the extraction dir). No secret value is printed. One seam is disclosed: OG-z-1's admission guard needs a live principal, so `_admit` is a no-op.
```
=== without (negative control: no SCHWAB_*/NFRA_OPLGTW_* in the environment)
BUILD: RAISED ContractUnavailable no contract path: set NFRA_OPLGTW_CONTRACT_PATH to org/standards/NFRA_OPLGTW_CONTRACT.json
TOOL schwab_get_access isError=True {'code': 'UNAVAILABLE', 'reason': 'schwab_integration_unavailable'}
TOOL schwab_list_files isError=True {'code': 'UNAVAILABLE', 'reason': 'schwab_integration_unavailable'}
=== with (the release's .env shape)
MODE with ENV KEYS SET: ['NFRA_OPLGTW_CONTRACT_PATH', 'SCHWAB_ACCOUNT_REF_SECRET_ID', 'SCHWAB_CATALOG_ROLE_ARN', 'SCHWAB_EXTERNAL_IDS_SECRET_ID', 'SCHWAB_READER_ROLE_ARN']
CONTRACT PATH EXISTS: True
BUILD: OK SchwabService
TOOL schwab_get_access isError=True {'code': 'ENTITLEMENT_DENIED', 'reason': 'principal_required'}
TOOL schwab_list_files isError=True {'code': 'ENTITLEMENT_DENIED', 'reason': 'principal_required'}
```
With the keys, `build_default_service()` (where `ContractUnavailable` and `RoleConfigError` were raised) returns a `SchwabService` and both tools reach the service's own entitlement check instead of `UNAVAILABLE`.
Not proven here: an sts:AssumeRole (the reader roles trust the Gateway role only) or a served Schwab answer; those are PHASE B and r6.J1.

**Env keys added (names only): 5** -- NFRA_OPLGTW_CONTRACT_PATH, SCHWAB_READER_ROLE_ARN, SCHWAB_CATALOG_ROLE_ARN, SCHWAB_EXTERNAL_IDS_SECRET_ID, SCHWAB_ACCOUNT_REF_SECRET_ID; plus `schwab` in ENABLED_INTEGRATIONS.
The host `.env` goes from 28 key names (measured 17:08Z) to **33**. No secret VALUE is in the repo, the artifact or `.env`; no `SCHWAB_*_EXTERNAL_ID` key is written.

## The contract change (widens what a GRANT may name; creates and changes no grant)

`org/standards/NFRA_OPLGTW_CONTRACT.json`: `datasets` gains `dim_transaction`; `fields.dim_transaction` = the 15 served columns of SCHEMA_MX-s-15.md; `additive_fields.dim_transaction` = [].
`contract_version` unchanged. MCPMSP's `tenant_firm` text is kept. Existing grants name the three dims explicitly and stay as they are (ruling B2); Alyssa's ONE new Schwab grant is the issuer's act after PHASE B (A6).
The grant-writer Lambda's own contract copy (row Z-W19-S9) is INERT for this release. ENTITLEMENT_MX-s-15.md's finding is unchanged: an existing Schwab grant does not cover `dim_transaction`; the IAM apply gives the reader
role the read and gives no principal access.

## What PHASE B would read on the host after the deploy (nothing below has been done)

`/health` 200; `.env` names 6 ids (`... portal_index schwab`) and 33 key names (`FIRM_ROLE_ARNS` still present); tool count 52 -> 58, exactly the 6 names above; host file hashes equal to the deploy-only artifact's 87 files
(9 changed, 1 new-or-overwritten contract copy, 77 unchanged; the host already carries the contract copy, byte-equal); the live reader role allowed `dim_transaction` for both masters (simulate-principal-policy); both S3 objects
carry `git-ref` = 42c52ed4d9e834b0f1cf4f96eb83f9b0f7a183df. Re-read the live ref at PHASE B's first act (clause above); NEVER-2 ledger `nfra-mcpindex-r5-schwab-enable` opened first.

## Rows filed (channel INVESTIGATION_v1.md)

| id | class / hazard | what |
|---|---|---|
| NFRA_MCPINDEX-Z-W19-S16 | OBSERVATION / INERT | the host carries one stray file, `deploy/NFRA_OPLGTW_CONTRACT.json`, left by the rolled-back v2 (byte-equal to v3's) |
| NFRA_MCPINDEX-Z-W19-S17 | OBSERVATION / INERT | ETFS_RIVALS' test_rivalfunds_view.py is red at the live ref itself (registry lacks a `rivalfunds` key); not ours |
| NFRA_MCPINDEX-Z-W19-S18 | OBSERVATION / INERT | the guard covers only trees carrying the new script; the live `-latest` has no metadata so the first read is the key-match fallback |
| NFRA_MCPINDEX-Z-W19-S19 | OBSERVATION / INERT | A6 re-cut record: audited overrides (rel-c, dep-c) and the dropped / changed gateway files vs CLOUD |
