# ANNOUNCE -- MX-r-6 PHASE A (A3 delta applied), the Schwab enable release: MX-s-15, MX-q-3, the contract change, `schwab` in ENABLED_INTEGRATIONS, and the Schwab service's host inputs

Deployer: 0.9.0_WK_NFRA_MCPINDEX~19 (issuer 2.0.0_SA_COO~MI). Order (amended A1, A2, A3):
org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-6.schwab-enable-release.md

STATE: PHASE A only. Nothing was deployed, no ledger is open, nothing was uploaded to S3, no `terraform apply`, no grant, identity
or sign-in was created or changed. AWS contact was read-only and Opal's own: `s3api list-objects-v2`, `s3 cp` download of the
`-latest` artifact, ONE SSM `AWS-RunShellScript` read (file hashes, `.env` KEY NAMES only, health code; 28a12bb3-2fa0-4da0-9aca-04f50b71f144),
`lambda get-function-configuration` (the two grant-writer owner variables, needed only to let `terraform plan` evaluate), `head-object`
on the future key (404), and `terraform plan -lock=false` (S3 state read). MX-t-10 does NOT ride (not drained).

## A3 DELTA (2.0.0_SA_COO~MI, row Z-S66) -- what changed since the first ANNOUNCE; the NEW PIN is here

**New pins.** Release **9def06ff2f** (child of ac77acf9e8, branch rel-nfra-mcpindex-r5-schwab-enable, /c/tmp/mx-rel7). Deploy-only **0d3e953c76** (child of abee4587f7, branch
dep-nfra-mcpindex-r5-schwab-enable, /c/tmp/mx-dep7, on CLOUD 0440cd4e4d). Both are audited GIT_COMMIT_AUTHOR_OVERRIDE uses (rel-/dep- branches, Z-W14-S8 precedent; uses 3 and 4);
they are CHILDREN of the first cut, nothing rewritten. Gateway tree object, release = deploy-only: **c8e4449bcf57e3357371dbf9bb41c3b6b1cb45ad**
(`git rev-parse 0d3e953c76:infra/aws/ec2/opal-gateway` = `9def06ff2f:infra/aws/ec2/opal-gateway`; `git diff --stat 9def06ff2f 0d3e953c76 -- infra/aws/ec2/opal-gateway` is empty).
The deploy-only commit differs from CLOUD 0440cd4e4d in 46 files, **0 outside infra/aws/ec2/opal-gateway**. Artifact key at GO:
s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-0d3e953c76.tar.gz (head-object: 404 now). mcportal a3bff71ffa unchanged. The pins ac77acf9e8 / abee4587f7
below are SUPERSEDED by these. Halt gate: the MX-r-6 order at the deploy-only HEAD is still `<status>pending</status>`, issued to ~19.

**Z-W19-S7 (host inputs), how each ships -- no secret VALUE in the repo, the artifact or `.env`:**

| input | key (named by the code) | how it ships |
|---|---|---|
| contract file | `NFRA_OPLGTW_CONTRACT_PATH` (catalog.py:85, `load_contract`) | the file ships IN THE ARTIFACT as `deploy/NFRA_OPLGTW_CONTRACT.json` (a byte copy of the release tree's org/standards contract; `deploy` is already a tar root, so the build and tar roots need no change); `.env` = `${REMOTE_DIR}/deploy/NFRA_OPLGTW_CONTRACT.json`, i.e. /opt/opal-gateway/deploy/NFRA_OPLGTW_CONTRACT.json |
| reader role ARN | `SCHWAB_READER_ROLE_ARN` (aws_roles.py:78) | `.env` = arn:aws:iam::313476888478:role/gateway-schwab-read-role (read-only `iam get-role`; its role name must equal the contract's reader_role, which `role_config` checks) |
| catalog role ARN | `SCHWAB_CATALOG_ROLE_ARN` (aws_roles.py:78) | `.env` = arn:aws:iam::313476888478:role/gateway-schwab-catalog-read-role |
| ExternalId source | **`SCHWAB_EXTERNAL_IDS_SECRET_ID` (NEW key, row Z-W19-S12)** | `.env` = opal/mcp/opal-gateway-schwab-reader-external-ids (the secret's NAME). The code's own keys `SCHWAB_READER_EXTERNAL_ID` / `SCHWAB_CATALOG_EXTERNAL_ID` take a VALUE, which A3 bars from `.env`, so the release adds `aws_roles.environ_with_external_ids`: an unset value is read, once at service construction, from that secret's JSON fields `data_read` / `catalog_read` (the Gateway role's resource policy grants exactly that read); an env value still wins; `os.environ` is never written; no error text carries a value |
| account_ref secret id | `SCHWAB_ACCOUNT_REF_SECRET_ID` (account_ref.py:56) | `.env` = opal/mcp/opal-gateway-schwab-account-ref-key (the secret's NAME; the key stays in Secrets Manager) |

**Env keys added (names only): 5** -- NFRA_OPLGTW_CONTRACT_PATH, SCHWAB_READER_ROLE_ARN, SCHWAB_CATALOG_ROLE_ARN, SCHWAB_EXTERNAL_IDS_SECRET_ID, SCHWAB_ACCOUNT_REF_SECRET_ID; plus `schwab`
in ENABLED_INTEGRATIONS (line 197). The host `.env` goes from 27 keys (measured in PHASE A) to **32**. The printf still takes exactly its 9 runtime `%s` values. No `SCHWAB_*_EXTERNAL_ID` key is
written. `git diff --stat 093fc247c6 9def06ff2f -- infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` = 6 insertions, 1 deletion (5 comment lines, the printf line).

**CENSUS DELTA.** `git diff --stat 093fc247c6 9def06ff2f -- infra/aws/ec2/opal-gateway`: **21 files, 997 insertions, 43 deletions** (was 17 files, 505 insertions, 41 deletions): +4 files =
`app/integrations/schwab/aws_roles.py` (+40), `app/integrations/schwab/integration.py` (+1 -1), `deploy/NFRA_OPLGTW_CONTRACT.json` (NEW, 336 lines), `tests/test_schwab_host_inputs.py` (NEW, 7 tests);
deploy-to-ec2.sh grows from 1 to 6 insertions. Shipped files: **10** (the earlier 7 plus aws_roles.py, integration.py, the contract copy); not shipped: deploy-to-ec2.sh and 10 tests. Outside the gateway dir the release
still differs from 093fc247c6 in exactly the same 2 files (schwab_reader_iam.tf, NFRA_OPLGTW_CONTRACT.json). The artifact is **80 files** (was 79): +1, `deploy/NFRA_OPLGTW_CONTRACT.json`.

**Rebuilt artifacts (build-only mirror of deploy-to-ec2.sh:74-98, NO upload; mcportal rebuilt in each tree):**
- release tree vs deploy-only tree: **80 of 80 byte-identical** (67 of 67 .py), 0 only-release, 0 only-deploy-only (mx-rel7-art3.tar.gz 417593 bytes, mx-dep7-art3.tar.gz 417564 bytes).
- deploy-only artifact vs the LIVE `-latest` (79 files): **70 of 79 identical** (59 of 67 .py); 9 differ (app/data_entitlement.py, app/destructive_ops.py, app/integrations/opal_discover/integration.py,
  app/integrations/portal_index/integration.py, app/integrations/schwab/aws_roles.py, app/integrations/schwab/datasets.json, app/integrations/schwab/integration.py, app/integrations/schwab/query.py,
  app/schwab_audit.py); 1 only-in-new (the contract copy); 0 only-live. The dashboard bundle is unchanged.

**THE IN-PROCESS PROOF (read-only; probes/inprocess_schwab_host_inputs_MX-r-6_A3.txt and .py).** The DEPLOY-ONLY artifact (mx-dep7-art3) is extracted to a host-like directory
(C:/tmp/hs-dep7b/opal-gateway); the process environment is the operator's own AWS read credentials plus ONLY the five static keys the release's `.env` printf writes (the deploy-only tree's script is parsed, `${REMOTE_DIR}` mapped
to the extraction dir). No secret value is printed. The first Schwab call's construction and the two tools; one seam is disclosed: OG-z-1's admission guard needs a live principal, so `_admit` is replaced by a no-op.
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
With the keys, `build_default_service()` (the one place `ContractUnavailable` and `RoleConfigError` were raised) returns a `SchwabService`, and both tools reach the service's own entitlement check (no principal in this process) instead of
`UNAVAILABLE`. The ExternalIds were read from their secret by the operator's credentials into process memory; `BUILD: OK` includes `role_configs` (both ARNs match the contract's role names, both ExternalIds well-formed and different).
What this does NOT prove: an sts:AssumeRole (the reader roles trust the Gateway role only) or a served Schwab answer; those are PHASE B and r6.J1.

**Tests in the release tree after the delta** (from infra/aws/ec2/opal-gateway): the six-file set **55 passed, 3 failed** (the PHASE A set was 54 passed, 4 failed; test_portal_tools_catalog_refs_resolve passed this run and its earlier failure
is unexplained and not caused by this delta, row Z-W19-S13; the 3 still failing also fail on the live tree); the five Schwab files plus test_account_ref.py and the new test file **76 passed**; tests/acceptance/test_local_acceptance.py
**14 passed**. The release adds no failing test.

**Targeted plan: UNCHANGED.** No Terraform file moved in this delta (schwab_reader_iam.tf is byte-identical to ac77acf9e8's). /c/tmp/mx-r6-schwab-read-targeted.tfplan, sha256 ca611803f37c560aad820b54ae277903145eaff43e46af1a934a247fb2ca7ffa:
**0 to add, 1 to change, 0 to destroy**, 8 added `dim_transaction` elements. It is not re-run here; per A3 it is re-planned, targeted, at the GO and applied only if it is the same one change, through `safe-apply`.

**Tool count (re-measured on the deploy-only artifact, probes/tools_depA3_6ids_MX-r-6.json):** integration tools 21 at 6 ids (16 at the same 5 ids, which include MX-q-3's `gateway_query_catalog`; the LIVE host's 5 ids give 15), total **37 native + 21 = 58**
against the live 52: **+6, 0 removed**, unchanged by this delta (the host-input change adds and removes no tool): `schwab_get_access`, `schwab_list_files`, `schwab_describe_dataset`, `schwab_query`, `schwab_prepare_download`, `gateway_query_catalog`.

**Rows for this delta:** Z-W19-S12 (OBSERVATION / INERT, disarm 2.0.0_SA_COO~MI): the code names no ExternalId-source key, so one was added with a small resolver; Z-W19-S13 (OBSERVATION / INERT): the contract ships as a copy in the gateway's deploy/ root, cut from the
release tree's contract (older than CLOUD's), and one unexplained test flip. S7 is addressed by the above (ruled by Z-S66); S8 is addressed by the targeted plan. Nothing is deployed, applied or pushed; no grant is created or changed.

## FIRST ANNOUNCE (superseded where the A3 delta above differs) -- two BLOCKING rows, ruled by Z-S66

| row | what |
|---|---|
| **NFRA_MCPINDEX-Z-W19-S7** (BLOCKING, ARMED) | The release enables `schwab`, but the host carries none of the six inputs the Schwab service needs at its first call, and the deploy path ships none: the contract file is not in the artifact and not on the host, and the `.env` printf names no `NFRA_OPLGTW_CONTRACT_PATH`, `SCHWAB_READER_ROLE_ARN`, `SCHWAB_CATALOG_ROLE_ARN`, `SCHWAB_READER_EXTERNAL_ID`, `SCHWAB_CATALOG_EXTERNAL_ID` or `SCHWAB_ACCOUNT_REF_SECRET_ID`. Measured in-process: `ContractUnavailable`, `RoleConfigError`. Deployed as ordered, the 5 tools register and every call fails closed. Fixing it needs a deploy-script change beyond line 197. |
| **NFRA_MCPINDEX-Z-W19-S8** (BLOCKING, ARMED) | No whole-directory plan changes only `gateway-schwab-read-role`'s policy. From CLOUD's TF: 1 add (`gateway-rivalfunds-read-policy`, ETFS_RIVALS, unapplied), 2 change (the wanted policy, and another seat's `mcportal-grant-writer-lambda` hash, which moved during this cell). The saved plan is therefore TARGETED: 0 add, 1 change, 0 destroy. |

## THE PIN (for G-A and both never-widen halves)

| field | value |
|---|---|
| base = LIVE deployed commit | **093fc247c6306dc0e5d26d92107dc9519965c7ad** (MX-r-5's deploy-only commit, deployed 2026-09-29T10:11:34Z) |
| how it was read | BY CONTENT, see Step 1 |
| release branch (NEW) | rel-nfra-mcpindex-r5-schwab-enable, worktree /c/tmp/mx-rel7, never merged, never pushed |
| **release commit** | **ac77acf9e8fb8b5a5f482e4eeb1d351c8ea0e24b** (audited override, use 1 of 2, Z-W19-S10) |
| deploy-only branch (NEW) | dep-nfra-mcpindex-r5-schwab-enable, worktree /c/tmp/mx-dep7, on CLOUD 0440cd4e4d, never merged, never pushed |
| **deploy-only commit** | **abee4587f7032771189e21f95b72045d937a5b9a** (audited override, use 2 of 2) |
| gateway tree object, release = deploy-only | **a1e8533891de83fac014c8de564c35ad72c57c12** |
| rollback tree | /c/tmp/mx-rb7, detached at 093fc247c6, mcportal a3bff71ffa built |
| mcportal | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054 in all three trees, 0 status lines each (unchanged from the live deploy) |
| artifact key at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-abee4587f7.tar.gz (head-object: 404 now), plus `-latest` |
| saved plan (targeted) | /c/tmp/mx-r6-schwab-read-targeted.tfplan, sha256 ca611803f37c560aad820b54ae277903145eaff43e46af1a934a247fb2ca7ffa; text render PLAN_MX-r-6_targeted.txt. The binary is NOT committed (a plan file embeds state). |
| NEVER-2 ledger at GO | `nfra-mcpindex-r5-schwab-enable`, opened before the first act |
| worker branch | wk-nfra_mcpindex-5-19 (step 0 32ebe6bee6; the identical line-197 edit, blob bb6c19ef04) |

## Step 1: the live deployed commit, read BY CONTENT

- Manifest: `services.opal-gateway.deployed_commit` = 093fc247c6 (deployed_by ~14, 2026-09-29T10:11:34Z).
- S3 `ec2/opal-gateway/`: `-latest` (LastModified 2026-09-29T10:11:09Z, 410925 bytes, md5 6c2b43e562938ef4d1fb46a76f6a3d60) has the same ETag and size as
  key `opal-gateway-093fc247c6.tar.gz`; no key is newer.
- Host, one SSM read on i-07dccb1615503ac99: sha256 of every file under app, deploy, dashboard, requirements.txt and identity_tool_allowlist.txt
  (excluding `*.log` and `__pycache__`) against the `-latest` artifact: **79 of 79 identical**, 0 only-host, 0 only-artifact. `/health` 200.
  `.env` ENABLED_INTEGRATIONS = `ycharts opal_portal globgrph opal_discover portal_index` (5 ids).
- Independent: the rollback tree at 093fc247c6, rebuilt, equals the live artifact 79 of 79 (Step 4).

## Step 2: the release tree and the census

Cut: `git worktree add --no-checkout -b rel-nfra-mcpindex-r5-schwab-enable /c/tmp/mx-rel7 093fc247c6`. Files applied oldest first with
`git diff <c>^ <c> -- <paths> | git apply --3way --index`:

| order | commit | author | what | files |
|---|---|---|---|---|
| 1 | 925b0357a5 | ~19 | MX-s-15: `dim_transaction` declared beside the three dims | gateway: app/data_entitlement.py, app/integrations/schwab/datasets.json, app/integrations/schwab/query.py, app/schwab_audit.py, tests/test_schwab_semantics.py, tests/test_schwab_transactions.py, tests/test_schwab_wiring.py; TF: schwab_reader_iam.tf |
| 2 | aac92bdff8 | ~20 | MX-q-3: `gateway_query_catalog` as a portal_index tool; discover names it | gateway: app/data_entitlement.py, app/destructive_ops.py, app/integrations/opal_discover/integration.py, app/integrations/portal_index/integration.py, tests/test_entitlement_admin.py, tests/test_opal_discover.py, tests/test_portal_index.py, tests/test_query_v0_tool.py |
| 3 | 32ebe6bee6 | ~19 | step 0: the contract change | gateway: tests/test_schwab_catalog.py, tests/test_schwab_query.py; `org/standards/NFRA_OPLGTW_CONTRACT.json` |
| 4 | (release commit) | ~19 | step 2: `ENABLED_INTEGRATIONS` gains `schwab` | gateway: deploy-to-ec2.sh line 197 |

One conflict: tests/test_entitlement_admin.py (the 52 pin; the release base has the older two lines). MX-q-3's text was taken (portal_index 5 tools,
total 53). Row S10 records the override uses and the two non-gateway files in the release commit (the TF file for the plan, the contract for the
tests that read it at `parents[5]`).

**Census** `git diff --stat 093fc247c6 ac77acf9e8 -- infra/aws/ec2/opal-gateway`: **17 files, 505 insertions, 41 deletions**: the 7 shipped files
(app/data_entitlement.py, app/destructive_ops.py, app/integrations/opal_discover/integration.py, app/integrations/portal_index/integration.py,
app/integrations/schwab/datasets.json, app/integrations/schwab/query.py, app/schwab_audit.py), deploy-to-ec2.sh (not in the artifact), and 9
test files. That is the union of the three commits' gateway files plus line 197: 0 extra, 0 missing. Outside the gateway dir the release
differs from 093fc247c6 in exactly 2 files: schwab_reader_iam.tf (+2) and NFRA_OPLGTW_CONTRACT.json (+21 -2).
`deploy-to-ec2.sh:197` now reads `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph opal_discover portal_index schwab` (6 ids); the printf still
carries 9 `%s`; `git diff` of that file is 1 insertion and 1 deletion. No other id moved.

**Tests in the release tree** (from infra/aws/ec2/opal-gateway): test_entitlement_admin, test_data_entitlement_guard,
test_tool_classification_composition, test_opal_discover, test_portal_index, test_query_v0_tool: **54 passed, 4 failed**. The 4 are the ones that fail
on the LIVE tree (run in /c/tmp/mx-rb7: 50 passed, the same 4): test_ogz2_ac06, test_ogz1_ac05, test_ogz1_ac08, test_portal_tools_catalog_refs_resolve.
The five Schwab files (wiring, semantics, transactions, catalog, query): **64 passed**. tests/acceptance/test_local_acceptance.py: **14 passed**
(8 failed before step 0). The release adds no failing test.

## Step 3: the plan

Saved: the TARGETED plan, `terraform plan -target=aws_iam_role_policy.schwab_data_read_policy`, run from a tree whose Terraform directory equals CLOUD's
(`git diff HEAD CLOUD -- infra/aws/terraform/opal-gateway` empty at the cut). **Plan: 0 to add, 1 to change, 0 to destroy.** The only diff lines are 8
added list elements, every one a `dim_transaction` prefix or ARN for masters 08242234 and 08335338 (NotResource, StringNotLike `s3:prefix`,
Resource, StringLike `s3:prefix`), 0 removed. The gateway role, the ALB, the ExternalIds and the secrets do not appear.

Why targeted (row S8): the two whole-directory plans are kept as evidence, not as the plan.
- From the release tree (093fc247c6 TF): 0 add, 2 change, **5 destroy** (`aws_eip.gw`, `aws_eip_association.gw`, `aws_iam_role.inf_firm_reader` and its
  two policies: state holds resources whose .tf landed on CLOUD after 093fc247c6). That tree is not the apply tree.
- From CLOUD's TF: **1 add** (`aws_iam_role_policy.gw_rivalfunds_read`, ETFS_RIVALS, not applied), 2 change (the wanted policy, and
  `aws_lambda_function.mcportal_grant_writer`'s `source_code_hash`, which moved between my two plans: another seat applied that function at
  2026-09-30T10:44:58Z; its planned hash comes from an untracked `.build/staged` directory).
- Apply-form is the issuer's and the CTO's call. Both `terraform plan` runs used `-lock=false`; the two owner variables of the grant writer were read from
  the live function's configuration and passed by environment, never written to a file.

**IAM rollback:** the prefix list without `dim_transaction` is 093fc247c6's `schwab_reader_iam.tf` (the release differs by exactly its 2 prefix lines).
Proof: a targeted plan from the rollback tree against the live policy reads **"No changes"** (probes/rollback_tree_iam_plan_MX-r-6.txt); after a
Phase B apply the same command from /c/tmp/mx-rb7 plans the 8 removals.

## Step 4: the rollback tree

/c/tmp/mx-rb7 = detached 093fc247c6, mcportal a3bff71ffa cloned beside it and built (`bun install --frozen-lockfile`, `bun run build`). A build-only mirror
of deploy-to-ec2.sh:74-91 (the same `tar -czf` and excludes, NO upload line) produced a 410913-byte artifact. Against the downloaded live `-latest`:
**79 of 79 files byte-identical** (67 of 67 .py), 0 only-live, 0 only-rebuilt.
- **Host rollback command:** `cd /c/tmp/mx-rb7 && HALT_ACK=1 AGENT_NAME=<deployer serial> bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
  (HALT_ACK=1 only when the halt gate reads 0 STOP; the rollback tree has no order at HEAD, so a worker is refused there and the issuer or the deployer
  identity runs it). It restores the `opal-gateway-093fc247c6` key, `-latest`, the 5-id `.env` value and the 52-tool surface.
- **IAM rollback command:** `terraform -chdir=/c/tmp/mx-rb7/infra/aws/terraform/opal-gateway apply` of a targeted plan
  (`-target=aws_iam_role_policy.schwab_data_read_policy`) made in that tree, through `safe-apply`.

## Step 5: the deploy-only tree

`git worktree add --no-checkout -b dep-nfra-mcpindex-r5-schwab-enable /c/tmp/mx-dep7 CLOUD` (CLOUD 0440cd4e4d), then `git rm -r -q infra/aws/ec2/opal-gateway`
and `git checkout ac77acf9e8 -- infra/aws/ec2/opal-gateway`, ONE commit abee4587f7.
- **Tree-object equality:** `git rev-parse abee4587f7:infra/aws/ec2/opal-gateway` = `ac77acf9e8:infra/aws/ec2/opal-gateway` =
  **a1e8533891de83fac014c8de564c35ad72c57c12**; `git diff --stat ac77acf9e8 abee4587f7 -- infra/aws/ec2/opal-gateway` is empty. The commit touches 42
  files vs CLOUD, every one under infra/aws/ec2/opal-gateway (row S11: 17 deleted and 25 modified files of other projects' unreleased gateway work are NOT shipped).
- **Artifact equality:** artifacts rebuilt (no upload) from the dep tree and the release tree: **79 of 79 byte-identical** (67 of 67 .py).
- **Artifact delta against LIVE:** 72 of 79 identical; only the 7 shipped files above differ. The dashboard bundle (mcportal a3bff71ffa) is unchanged.
- **Halt gate:** at the dep tree's HEAD the MX-r-6 order is `<issued_to>0.9.0_WK_NFRA_MCPINDEX~19</issued_to>`, `<status>pending</status>`, byte-identical to the worker copy.
  `git status` of the dep tree shows ` M mcportal` (CLOUD's gitlink names another mcportal commit than the nested clone), as in MX-r-5.
- `deploy-to-ec2.sh` in the dep tree differs from CLOUD's in exactly line 197.

## The tool-count delta (in-process on the live and release artifacts; probes/tools_live_5ids_MX-r-6.json, tools_release_6ids_MX-r-6.json)

| | integration tools | total (37 native + integration) |
|---|---|---|
| live, 5 ids | 15 | 52 |
| release, 6 ids | 21 | **58** |

**+6, 0 removed:** `schwab_get_access`, `schwab_list_files`, `schwab_describe_dataset`, `schwab_query`, `schwab_prepare_download` (the 5 Schwab tools), and
`gateway_query_catalog` (MX-q-3, the 5th portal_index tool). MX-t-10's tools are not included. Read-back at Phase B: the tool-name list moves by exactly these 6.
Per-integration at 6 ids: ycharts 6, opal_portal 1, globgrph 2, opal_discover 2, portal_index 5, schwab 5.

## The contract change (widens what a GRANT may name; creates and changes no grant)

`org/standards/NFRA_OPLGTW_CONTRACT.json`: `datasets` gains `dim_transaction`; `fields.dim_transaction` = the 15 served columns of SCHEMA_MX-s-15.md (account_ref,
business_date, trade_date, settlmnt_date, tr_cd, sb_cd, transaction_category, tran_srcde, debit_credit, cusip, ticker_symbol, quantity, price, gross_amount,
net_amount); `additive_fields.dim_transaction` = [] (nothing summable, as datasets.json). `contract_version` unchanged. Existing grants name the three dims
explicitly and stay as they are (ruling B2).

**How the served gateway gets the contract (the A1 question), answered -- AS BUILT AT THE FIRST CUT; SUPERSEDED by the A3 delta above, where the contract now ships in the artifact at deploy/NFRA_OPLGTW_CONTRACT.json and `.env` names its path:** it does not read it from the artifact. `build_default_service()` (first Schwab call) calls
`catalog.load_contract()`: the `NFRA_OPLGTW_CONTRACT_PATH` environment value, else the repository layout (`Path(catalog.py).parents[7]/org/standards/...`, which is
`None` on the host: its path has 6 parents). The artifact's tar roots are app, deploy, requirements.txt, identity_tool_allowlist.txt and dashboard, so the
contract file is in no shipped file, the host has no copy, and `.env` names no path. **As built, the release does not ship the contract and the enable cannot
serve Schwab calls (row S7).** The contract change is therefore inert on the host until the issuer grants the shipping route; it is exercised now by the local
acceptance suite (14 of 14) and the five Schwab test files.

A second place holds a copy: the mcportal grant-writer Lambda's staged package carries its own `org/standards/NFRA_OPLGTW_CONTRACT.json` (0 occurrences of
`dim_transaction`), so granting `dim_transaction` through the grant admin tool also needs that package rebuilt and applied (row S9; Andrew's list).

## ENTITLEMENT_MX-s-15.md's finding (same directory)

**No. An existing Schwab grant does not cover `dim_transaction`.** A grant stores its datasets and columns explicitly, so a request for `dim_transaction` is
refused (`("datasets", "dataset 'dim_transaction' is not granted")`); declaring the dataset only lets a grant NAME it. Three layers must all move before any
principal reads it: (a) the contract lists it (DONE in this release's contract edit, but not shipped, see S7), (b) the reader role is applied (the targeted plan),
(c) an operator re-issues a grant naming it, per principal (NOT done; A2 carries it to Andrew's list). The current policy: dim_position allowed and
dim_transaction `explicitDeny` on the APPLIED reader role (issuer-measured 2026-09-30). The IAM apply alone gives the gateway's reader role the read; it gives no
principal access.

## What PHASE B would read on the host after the deploy (nothing below has been done)

`/health` 200; `.env` names 6 ids (`... portal_index schwab`); tool count 52 -> 58, exactly the 6 names above; per-file host hashes equal to the release's 79 files
(7 changed: the shipped files above); the live reader role allowed `dim_transaction` for both masters (simulate-principal-policy). NEVER-2 ledger
`nfra-mcpindex-r5-schwab-enable` opened first. Nothing below the two BLOCKING rows is a reason not to proceed; they are the reason the GO cannot be given as
the order is written.

## Rows filed (channel INVESTIGATION_v1.md)

| id | class / hazard | what |
|---|---|---|
| NFRA_MCPINDEX-Z-W19-S7 | BLOCKING / ARMED (disarm 2.0.0_SA_COO~MI) | the enable ships none of the six Schwab service inputs; every call would fail closed |
| NFRA_MCPINDEX-Z-W19-S8 | BLOCKING / ARMED (disarm 2.0.0_SA_COO~MI) | no whole-directory plan is confined to the reader policy; the saved plan is targeted |
| NFRA_MCPINDEX-Z-W19-S9 | OBSERVATION / INERT | the grant-writer Lambda bundles a contract copy without `dim_transaction` |
| NFRA_MCPINDEX-Z-W19-S10 | OBSERVATION / INERT | two audited overrides on rel-/dep-; two non-gateway files in the release commit; the line-197 edit is also on the worker branch |
| NFRA_MCPINDEX-Z-W19-S11 | OBSERVATION / INERT | the deploy-only tree drops 42 files of other projects' unreleased gateway work |
| NFRA_MCPINDEX-Z-W19-S12 | OBSERVATION / INERT (disarm 2.0.0_SA_COO~MI) | A3: the code names no ExternalId-source key; `SCHWAB_EXTERNAL_IDS_SECRET_ID` and a small resolver added |
| NFRA_MCPINDEX-Z-W19-S13 | OBSERVATION / INERT | A3: the contract ships as a copy in deploy/ from the release tree's (older) contract; one unexplained test flip |
