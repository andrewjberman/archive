# ANNOUNCE v2 -- MX-r-6 PHASE A RE-CUT (A4) on the live base 288fa78c93: MX-s-15, MX-q-3, the contract change, `schwab` in ENABLED_INTEGRATIONS, the Schwab host inputs, and MCPMSP's release kept whole

Deployer: 0.9.0_WK_NFRA_MCPINDEX~19 (issuer 2.0.0_SA_COO~MI). Order (amended A1-A4):
org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-6.schwab-enable-release.md

STATE: PHASE A only. Nothing deployed, no ledger open, nothing uploaded to S3, no `terraform apply`, no grant, identity or sign-in created or
changed. AWS contact was read-only and Opal's own: `s3api list-objects-v2` / `head-object`, `s3 cp` download of the `-latest` artifact, three SSM
`AWS-RunShellScript` reads (file hashes, `.env` KEY NAMES only, health code), `lambda get-function-configuration` (the two grant-writer owner
variables, read into the process environment only so `terraform plan` can evaluate, never written), Secrets Manager read of the ExternalIds by the
in-process proof (no value printed), and `terraform plan -lock=false`. MX-t-10 does NOT ride.

## BASE-MOVED CLAUSE (A4)

**Every pin below is valid ONLY while the live gateway is `288fa78c93`.** That is the commit read by content at 2026-09-30T12:27Z, 13:00Z and again
13:08Z (this write). If the live commit is anything else at the GO or at PHASE B's first act, the release, the deploy-only tree and the rollback
tree are VOID and must be re-cut exactly as in this document (the procedure is in the Step 2 table). The first cut (release 9def06ff2f /
deploy-only 0d3e953c76 / rollback /c/tmp/mx-rb7, base 093fc247c6) is VOID and is not to be deployed: it would drop MCPMSP's `tenant_registry.py`,
`firm_role.py` and `admin_tenants.py` and rewrite `asker_scope`, `audit`, `config`, `access_state`, `admin_api` and the `.env` shape.
CLOUD also moved during this cut (fc97abbdf7 -> 6caac02338 -> 777631c63b); `git diff --stat 6caac02338 777631c63b` over infra/aws/ec2,
infra/aws/terraform/opal-gateway, the contract and the order directory is empty, so the deploy-only base is unaffected.

## THE PINS (for G-A and both never-widen halves)

| field | value |
|---|---|
| base = LIVE deployed commit | **288fa78c93e1c57be0ad7b8d6371c69145a69856** (NFRA_MCPMSP MS-d-1, deployed 2026-09-30T11:37:34Z; parent 093fc247c6) |
| how it was read | BY CONTENT, Step 1 |
| release branch (NEW) | rel-nfra-mcpindex-r5-schwab-enable-b, worktree /c/tmp/mx-rel8, never merged, never pushed |
| **release commit** | **63d6094823517e64749e681ce7f38821c17c4372** (audited override) |
| deploy-only branch (NEW) | dep-nfra-mcpindex-r5-schwab-enable-b, worktree /c/tmp/mx-dep8, on CLOUD 6caac02338, never merged, never pushed |
| **deploy-only commit** | **2e2254156e8559b051f64e59f2d14a6a2ed1426d** (audited override) |
| gateway tree object, release = deploy-only | **bf741bd45a6fd86ba1f0ee2509c8bf861d761bb2** (`git rev-parse 2e2254156e:infra/aws/ec2/opal-gateway` = `63d6094823:infra/aws/ec2/opal-gateway`; `git diff --stat 63d6094823 2e2254156e -- infra/aws/ec2/opal-gateway` is empty) |
| rollback tree | /c/tmp/mx-rb8, detached at 288fa78c93 (gateway tree e298beb2ac466840ff47f4ddac4a6707a9199a67), mcportal a3bff71ffa built |
| mcportal | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054 in all three trees, 0 status lines each (the live manifest's mcportal_commit, unchanged) |
| artifact key at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-2e2254156e.tar.gz (head-object: 404 now), plus `-latest` |
| saved plan (targeted) | /c/tmp/mx-r6-a4-schwab-read-targeted.tfplan, sha256 9ac94df09253743e719499b421ac3b2f75cc5ae94dbbe1af4f57515a9d8b0bfa; render PLAN_MX-r-6_A4_targeted.txt. The binary is NOT committed (a plan embeds state). |
| NEVER-2 ledger at GO | `nfra-mcpindex-r5-schwab-enable`, opened before the first act |
| superseded pins (VOID) | release 9def06ff2f, ac77acf9e8; deploy-only 0d3e953c76, abee4587f7; rollback /c/tmp/mx-rb7; plan /c/tmp/mx-r6-schwab-read-targeted.tfplan (sha ca611803f3...; same one change, re-planned) |

## Step 1: the live deployed commit, read BY CONTENT (2026-09-30T12:27Z; re-read 13:00Z and 13:08Z)

- Manifest on CLOUD: `services.opal-gateway.deployed_commit` = 288fa78c93 (deployed_by 0.9.0_WK_NFRA_MCPMSP~1, 2026-09-30T11:37:34Z, previous 093fc247c6).
- S3 `ec2/opal-gateway/`: `-latest` (LastModified 11:37:13Z, 415525 bytes, ETag be161c825e92471afe31c9f6ba4f3758) has the same ETag and size as key
  `opal-gateway-288fa78c93.tar.gz`; no key is newer.
- Host, SSM e29a6f89-425b-4e34-bc30-caea722ea8b2 on i-07dccb1615503ac99 (12:27Z): sha256 of every file under app, deploy, dashboard, requirements.txt and
  identity_tool_allowlist.txt (excluding `*.log`, `__pycache__`) against the downloaded `-latest`: **82 of 82 identical**, 0 only-host, 0 only-artifact; `/health` 200.
  SSM e6782853-9cfc-4515-b75e-341fbf3151fa (13:00Z): 82 of 82 again. A third hash-of-hashes read (13:08Z) returned `08e30fe9be...c469` for the host file set; ENABLED_INTEGRATIONS unchanged.
  `.env` ENABLED_INTEGRATIONS = `ycharts opal_portal globgrph opal_discover portal_index` (5 ids); `.env` names 28 key NAMES (27 at 093fc247c6 plus MCPMSP's `FIRM_ROLE_ARNS`); 0 `SCHWAB_*`, 0 `NFRA_OPLGTW*`.
- Independent: the rollback tree at 288fa78c93, rebuilt, equals the live artifact 82 of 82 (Step 4).
- Probes: probes/host_read_A4_1227Z_MX-r-6.txt, host_read_A4_1300Z_MX-r-6.txt.

## Step 2: the release tree, the merges, and the census

Cut: `git worktree add --no-checkout -b rel-nfra-mcpindex-r5-schwab-enable-b /c/tmp/mx-rel8 288fa78c93`. Each project commit's diff, limited to the gateway dir,
`schwab_reader_iam.tf` and the contract, applied oldest first with `git apply --3way --index`; then ONE release commit (63d6094823):

| order | source commit | what | result |
|---|---|---|---|
| 1 | 925b0357a5 (MX-s-15) | `dim_transaction` declared beside the three dims | clean |
| 2 | aac92bdff8 (MX-q-3) | `gateway_query_catalog` as a portal_index tool; discover names it | 1 conflict, tests/test_entitlement_admin.py (the tool-count pin); MX-q-3's 53 taken |
| 3 | 32ebe6bee6 (step 0) | `dim_transaction` in NFRA_OPLGTW_CONTRACT.json; acceptance 8 failed -> 14 passed | clean on MCPMSP's contract |
| 4 | 9a94936ab5 (line 197) | `ENABLED_INTEGRATIONS` gains `schwab` | **conflict with MCPMSP's FIRM_ROLE_ARNS printf line; MCPMSP's line kept, ` schwab` added** |
| 5 | 9def06ff2f (A3) | aws_roles resolver, integration.py, deploy/NFRA_OPLGTW_CONTRACT.json, 5 .env keys, test_schwab_host_inputs.py | clean on the code; the script's printf line hand-merged onto MCPMSP's (Step 2a) |

**Step 2a, the three merges where the live base changed a file we also change** (scripts/probes: probes/mcpmsp_preservation_MX-r-6_A4.txt is the output; the script is not committed, the commit gate refuses a .py with lint in a probe):
1. `deploy-to-ec2.sh`: the live printf line has 29 items and `FIRM_ROLE_ARNS`; the release line has 34 items. Live items missing from the release: 1 (`ENABLED_INTEGRATIONS=...portal_index`,
   replaced by the same value plus ` schwab`). Items added: `schwab` in that value, plus the 5 A3 keys. `%s` count live 9, release 9; the printf argument tail is byte-equal. `git diff --numstat 288fa78c93 63d6094823` on
   the file: 6 insertions, 1 deletion (5 comment lines, the one printf line). `bash -n` passes.
2. `org/standards/NFRA_OPLGTW_CONTRACT.json`: MCPMSP's `tenant_firm` lines kept (present in the release contract), step 0's hunks added: 23 insertions, 2 deletions vs the live base. `deploy/NFRA_OPLGTW_CONTRACT.json`
   is regenerated as a byte copy of this tree's contract (it now carries `tenant_firm`; `cmp` EQUAL).
3. `tests/test_entitlement_admin.py`: MX-q-3's pin of 53 registered tools. MCPMSP adds routes, not tools, so the pin is ours alone.

**THE MCPMSP-PRESERVATION PROOF.** The 13 files NFRA_MCPMSP changed from 093fc247c6 to 288fa78c93, release vs live (`git show 288fa78c93:<f>` against `git show 63d6094823:<f>`):
**11 byte-equal**: app/access_state.py, app/admin_api.py, app/admin_tenants.py, app/asker_scope.py, app/audit.py, app/config.py, app/firm_role.py, app/tenant_registry.py, tests/test_access_state.py,
tests/test_admin_tenants.py, tests/test_mcpmsp_asker_firm.py. **2 changed, both justified as ours and above**: deploy-to-ec2.sh (Step 2a-1), org/standards/NFRA_OPLGTW_CONTRACT.json (Step 2a-2).

**Every file in the LIVE artifact that is absent or changed in the new release (deploy-only artifact vs live `-latest`, file by file; probes/deployonly_vs_live_MX-r-6_A4.txt):**
82 live files; **73 identical (62 of 70 .py)**; **0 absent**; **9 changed**, each ours:

| changed file | why it is ours |
|---|---|
| app/data_entitlement.py | MX-s-15 (dim_transaction) and MX-q-3 (gateway_query_catalog in the native/integration classification) |
| app/destructive_ops.py | MX-q-3 (+2 lines) |
| app/integrations/opal_discover/integration.py | MX-q-3 (discover names gateway_query_catalog as next_tool) |
| app/integrations/portal_index/integration.py | MX-q-3 (the 5th portal_index tool) |
| app/integrations/schwab/datasets.json | MX-s-15 (the dim_transaction declaration) |
| app/integrations/schwab/query.py | MX-s-15 |
| app/schwab_audit.py | MX-s-15 (+1 -1) |
| app/integrations/schwab/aws_roles.py | A3 (ExternalIds read from their secret; Z-W19-S12) |
| app/integrations/schwab/integration.py | A3 (passes the resolved environ to role_configs) |

1 only-in-new: `deploy/NFRA_OPLGTW_CONTRACT.json` (A3). 0 only-live. The dashboard bundle is unchanged (mcportal a3bff71ffa).

**CENSUS** `git diff --shortstat 288fa78c93 63d6094823 -- infra/aws/ec2/opal-gateway`: **21 files, 998 insertions, 43 deletions**: the 9 changed artifact files above, the contract copy (+337), deploy-to-ec2.sh (+6 -1; not in the artifact),
and 10 test files (test_entitlement_admin, test_opal_discover, test_portal_index, test_query_v0_tool (NEW), test_schwab_catalog, test_schwab_host_inputs (NEW), test_schwab_query, test_schwab_semantics,
test_schwab_transactions (NEW), test_schwab_wiring): 9 + 1 + 1 + 10 = 21. Outside the gateway dir the release differs from 288fa78c93 in exactly 2 files: `infra/aws/terraform/opal-gateway/schwab_reader_iam.tf` (+2) and
`org/standards/NFRA_OPLGTW_CONTRACT.json` (+23 -2). `deploy-to-ec2.sh:197`'s ENABLED_INTEGRATIONS now reads `ycharts opal_portal globgrph opal_discover portal_index schwab` (6 ids); no other id moved.
Shipped files: 10 (the 9 changed plus the contract copy); the artifact is **83 files** (82 live +1).

**Tests in the release tree** (from infra/aws/ec2/opal-gateway, MOCK_GRAPH=1):
- six-file set (test_entitlement_admin, test_data_entitlement_guard, test_tool_classification_composition, test_opal_discover, test_portal_index, test_query_v0_tool): **55 passed, 3 failed** (test_ogz2_ac06, test_ogz1_ac05, test_ogz1_ac08).
  The LIVE tree (rollback /c/tmp/mx-rb8, five files, no test_query_v0_tool): 50 passed, **4 failed** -- the same three plus test_portal_tools_catalog_refs_resolve, which the release fixes. The release adds no failing test.
- the five Schwab files plus test_account_ref.py and test_schwab_host_inputs.py: **76 passed**.
- MCPMSP's own tests (test_mcpmsp_asker_firm, test_admin_tenants, test_access_state): **17 passed** in the release tree.
- tests/acceptance/test_local_acceptance.py: **14 passed**.

## Step 3: the plan (the IAM leg, unchanged)

`terraform plan -lock=false -target=aws_iam_role_policy.schwab_data_read_policy`, from the worker tree's Terraform dir (git diff to CLOUD 6caac02338 over it: empty), saved at 12:58Z.
**Plan: 0 to add, 1 to change, 0 to destroy.** The diff is 8 added list elements, every one a `dim_transaction` prefix or ARN for masters 08242234 and 08335338 (NotResource, StringNotLike `s3:prefix`,
Resource, StringLike `s3:prefix`; `+` lines with dim_transaction = 8 of 8, `-` lines = 0). The gateway role, the ALB, the ExternalIds and the secrets do not appear.
`schwab_reader_iam.tf` is byte-identical to the previous cut's and CLOUD's. At PHASE B: re-plan targeted at the GO, apply only if byte-equal in effect (the same one change) through `safe-apply`; never an untargeted apply.
`gateway-rivalfunds-read-policy` (ETFS_RIVALS) and the grant-writer Lambda hash are other seats' pending acts and are not touched.
**IAM rollback:** the prefix list without `dim_transaction` is 288fa78c93's `schwab_reader_iam.tf` (blob da2bfee022a70dcfa4b242d39ebfbc985388f0fc, identical to 093fc247c6's, for which a targeted plan against the live policy
read "No changes", probes/rollback_tree_iam_plan_MX-r-6.txt); after a Phase B apply the same command from /c/tmp/mx-rb8 plans the 8 removals.

## Step 4: the rollback tree

/c/tmp/mx-rb8 = detached 288fa78c93, mcportal a3bff71ffa cloned beside it and built (`bun install --frozen-lockfile`, `bun run build`). A build-only mirror of deploy-to-ec2.sh:74-91 (same `tar -czf`
and excludes, NO upload) produced a 415431-byte artifact. Against the downloaded live `-latest`: **82 of 82 files byte-identical (70 of 70 .py)**, 0 only-live, 0 only-rebuilt (probes/rollback_vs_live_MX-r-6_A4.txt).
- **Host rollback command:** `cd /c/tmp/mx-rb8 && HALT_ACK=1 AGENT_NAME=<deployer serial> bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
  (HALT_ACK=1 only when the halt gate reads 0 STOP; the rollback tree has no order at HEAD, so a worker is refused there and the issuer or the deployer identity runs it). It restores the `opal-gateway-288fa78c93` key,
  `-latest`, the 5-id `.env` value with MCPMSP's `FIRM_ROLE_ARNS` and the 52-tool surface.
- **IAM rollback command:** `terraform -chdir=/c/tmp/mx-rb8/infra/aws/terraform/opal-gateway apply` of a targeted plan (`-target=aws_iam_role_policy.schwab_data_read_policy`) made in that tree, through `safe-apply`.

## Step 5: the deploy-only tree

`git worktree add --no-checkout -b dep-nfra-mcpindex-r5-schwab-enable-b /c/tmp/mx-dep8 CLOUD` (CLOUD 6caac02338), then `git rm -r -q infra/aws/ec2/opal-gateway` and
`git checkout 63d6094823 -- infra/aws/ec2/opal-gateway`, ONE commit 2e2254156e.
- **Tree-object equality:** bf741bd45a6fd86ba1f0ee2509c8bf861d761bb2 for both (above). The commit touches 37 files vs CLOUD, **0 outside infra/aws/ec2/opal-gateway**: 12 deleted, 23 modified, 2 added
  (row Z-W19-S14: other projects' unreleased gateway work is NOT shipped; the two added are ours).
- **Artifact equality:** artifacts rebuilt (no upload) from the release and deploy-only trees: **83 of 83 byte-identical (70 of 70 .py)**, 0 only-either (probes/release_vs_deployonly_MX-r-6_A4.txt).
- **Halt gate:** at the dep tree's HEAD the MX-r-6 order is `<issued_to>0.9.0_WK_NFRA_MCPINDEX~19</issued_to>`, `<status>pending</status>`. `git status` of the dep tree shows ` M mcportal`
  (CLOUD's gitlink names another mcportal commit than the nested clone), as in MX-r-5.

## The tool-count delta (in-process on the extracted artifacts; probes/tools_A4_live5ids_MX-r-6.json, tools_A4_dep6ids_MX-r-6.json)

| | native | integration | total |
|---|---|---|---|
| live 288fa78c93 artifact, 5 ids | 37 | 15 | **52** |
| deploy-only artifact, 6 ids | 37 | 21 | **58** |

**+6, 0 removed** (52 is still the live count: MCPMSP added routes and a registry module, no tool): `schwab_get_access`, `schwab_list_files`, `schwab_describe_dataset`, `schwab_query`,
`schwab_prepare_download`, `gateway_query_catalog`. Per integration at 6 ids: ycharts 6, opal_portal 1, globgrph 2, opal_discover 2, portal_index 5, schwab 5. Registration errors: none.

## THE IN-PROCESS PROOF (A3, re-run on the NEW deploy-only artifact; probes/inprocess_schwab_host_inputs_MX-r-6_A4.txt)

The deploy-only artifact (mx-dep8-art) is extracted to C:/tmp/hs-dep8/opal-gateway; the environment is the operator's own AWS read credentials plus ONLY the five static keys the release's `.env` printf writes
(parsed from the deploy-only tree's script, `${REMOTE_DIR}` mapped to the extraction dir). No secret value is printed. One seam is disclosed: OG-z-1's admission guard needs a live principal, so `_admit` is a no-op.
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
The host `.env` goes from 28 key names (measured 12:27Z) to **33**. No secret VALUE is in the repo, the artifact or `.env`; no `SCHWAB_*_EXTERNAL_ID` key is written.

## The contract change (widens what a GRANT may name; creates and changes no grant)

`org/standards/NFRA_OPLGTW_CONTRACT.json`: `datasets` gains `dim_transaction`; `fields.dim_transaction` = the 15 served columns of SCHEMA_MX-s-15.md; `additive_fields.dim_transaction` = [].
`contract_version` unchanged. MCPMSP's `tenant_firm` row text is kept. Existing grants name the three dims explicitly and stay as they are (ruling B2). The grant-writer Lambda's own contract copy (row Z-W19-S9) is INERT this round.
ENTITLEMENT_MX-s-15.md's finding is unchanged: an existing Schwab grant does not cover `dim_transaction`; the IAM apply gives the reader role the read and gives no principal access.

## What PHASE B would read on the host after the deploy (nothing below has been done)

`/health` 200; `.env` names 6 ids (`... portal_index schwab`) and 33 key names (MCPMSP's `FIRM_ROLE_ARNS` still present); tool count 52 -> 58, exactly the 6 names above; host file hashes equal to the deploy-only artifact's 83 files
(9 changed, 1 new, 73 unchanged); the live reader role allowed `dim_transaction` for both masters (simulate-principal-policy). Re-read the live commit at PHASE B's first act (clause above); NEVER-2 ledger
`nfra-mcpindex-r5-schwab-enable` opened first.

## Rows filed (channel INVESTIGATION_v1.md)

| id | class / hazard | what |
|---|---|---|
| NFRA_MCPINDEX-Z-W19-S14 | OBSERVATION / INERT | A4 re-cut record: two more audited overrides (rel-b, dep-b); the deploy-only tree drops 37 gateway-dir files of other projects' unreleased work vs CLOUD |
| NFRA_MCPINDEX-Z-W19-S15 | OBSERVATION / INERT | A3's aws_roles.py / integration.py edits are written on the live-base copies; CLOUD's carry OG-i-3 / OG-x-2, so a later CLOUD release merges against them; the contract copy is regenerated |
