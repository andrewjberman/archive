# ANNOUNCE -- MX-r-8 PHASE A: the slot-4 gateway release on the live ref daa56d81ac (MX-d-6 discover reads silver_datasets + Schwab rows, MX-g-3 G-RDR internal-reader routing)

Deployer: 0.9.0_WK_NFRA_MCPINDEX~22 (issuer 2.0.0_SA_COO~MI). Order:
org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-8.slot4-rdr-release.md. Pattern: MX-r-7 PHASE A (ANNOUNCE_MX-r-7.md, `git show b92561fbec:...`).
Probes: org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~22/probes_r8/ (every file named below is there).

STATE: PHASE A only. Nothing deployed, no ledger opened, nothing uploaded to S3, no Terraform, no grant, identity, role or sign-in created or changed.
AWS contact: read-only, Opal's own: S3 `head-object` / `list-objects-v2` and one `-latest` download; SSM `AWS-RunShellScript` reads of file hashes, `.env` KEY NAMES, the key STATE of `MAIL_SENDER_TABLE`, and the health code (the host `.env` parsed in Python by `probes_r8/host_read.py`, never shell-sourced: row Z-S73); IAM `get-role`, `list-role-policies`, `get-role-policy`, `simulate-principal-policy` on the internal reader role.

## BASE-MOVED CLAUSE, by REF

**Every pin below is valid ONLY while the live ref is `daa56d81ac7c91795f1a9c47b2c2430cb3879e24` (NFRA_OPLGTW OG-rl-1, train slot 3).**
Read three ways, all equal, at 2026-10-01T11:49:44Z-11:49:56Z, immediately before this ANNOUNCE (probes_r8/live_ref_reread_FINAL.txt):
- S3 `ec2/opal-gateway/opal-gateway-latest.tar.gz` metadata `git-ref` = daa56d81ac7c91795f1a9c47b2c2430cb3879e24 (LastModified 10:43:27Z, 457214 bytes, ETag b78383f960d3cfa8ea7e37446374386e); the newest keys are `-daa56d81ac` (10:43:25Z) and `-latest` (10:43:27Z), none newer;
- CLOUD `infra/aws/ec2/EC2_MANIFEST.json` `services.opal-gateway.deployed_commit` = daa56d81ac7c91795f1a9c47b2c2430cb3879e24 (deployed_at 10:43:56Z, deployed_by 0.9.0_WK_NFRA_OPLGTW~15, `mcportal_commit` a3bff71ffa3f5c73aa0fb7ea1e7386434e233054), CLOUD bc4452a2aa;
- the host `/opt/opal-gateway`, by content: 94 of 94 files byte-identical to `-latest`, `/health` 200, 46 `.env` keys (46 distinct), `ENABLED_INTEGRATIONS` = `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (7 ids).

**OG-rl-1's ledger `nfra-oplgtw-trnspt-deps-release` at this moment is CLOSED on the shared tree**: CLOUD carries the entry `org/critical_paths/change_management/20261001T1038Z_nfra-oplgtw-trnspt-deps-release_deploy_completion.md` (1 entry file) and 0 sentinels under `.open_deploys/`. (At the first read, 10:57Z, it was NOT closed: the S3 ref was daa56d81ac and the CLOUD manifest still read 2c0f84966d. By 11:34Z the drain had landed, and the three reads agree.)
If the live ref is anything else at the GO or at PHASE B's first act, the release, the deploy-only tree and the rollback tree are VOID and are re-cut as below. PHASE B passes the base to the guard (`DEPLOY_BASE_REF`), so the check also happens at UPLOAD time inside `deploy-to-ec2.sh`.

## THE PINS (for G-A and both never-widen halves)

| field | value |
|---|---|
| base = LIVE ref | **daa56d81ac7c91795f1a9c47b2c2430cb3879e24** (OG-rl-1, live since 2026-10-01T10:43:27Z on 2c0f84966d) |
| release branch | `rel-nfra-mcpindex-r6-rdr-release`, worktree C:/tmp/mx-rel11, sparse, never merged, never pushed |
| **release commit** | **01845e91cf1b77dc00780d87c25f41b6951ff9a9** (parent daa56d81ac; 5 gateway files, +449 -13; 0 files outside the gateway dir) |
| deploy-only branch | `dep-nfra-mcpindex-r6-rdr-release`, worktree C:/tmp/mx-dep11, on CLOUD 220a74350a, never merged, never pushed |
| **deploy-only commit** | **e3567ce5f788f45195bec065f4d2fc5a68a38cd3** (parent 220a74350a) |
| **gateway tree object, release = deploy-only** | **7d222e01f6bf0c5bf9405060246e7c3d1f1f7f8a** (`git rev-parse 01845e91cf:infra/aws/ec2/opal-gateway` = `git rev-parse e3567ce5f7:infra/aws/ec2/opal-gateway`; `git diff 01845e91cf e3567ce5f7 -- infra/aws/ec2/opal-gateway` is 0 lines) |
| **rollback tree** | C:/tmp/mx-rb11, detached at daa56d81ac, gateway tree **c28f3706ee7229463f947f904e21532834dfa7f3**; artifact built from it equals the live artifact **94 of 94 files (80 of 80 .py)** (probes_r8/rollback_vs_live_PHASEA.txt) |
| mcportal | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054 (the live manifest's, unchanged); the dashboard bundle in the build-only artifacts is the dist already built at C:/tmp/mx-rb9/mcportal/dist, and the live host's `dashboard/` files equal the build-only artifacts' (94 of 94) |
| artifact key at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-e3567ce5f7.tar.gz (+ `-latest`), both written with `git-ref` metadata by the deploy script |
| Terraform | none. `ENABLED_INTEGRATIONS` unchanged. `deploy-to-ec2.sh` untouched: byte-identical to the live ref's (`cmp` equal) |
| NEVER-2 ledger at GO | `nfra-mcpindex-r6-rdr-release`: entry under `org/critical_paths/change_management/` AND sentinel `org/critical_paths/.open_deploys/nfra-mcpindex-r6-rdr-release.json`, opened before the first act |
| manifest edit | this release's own (the order's `<paths>` carry `EC2_MANIFEST.json`); OG-rl-1's rel-branch manifest commit 8611e9eab3 is NOT merged or cherry-picked |

## Step 1: the content, identified on CLOUD and applied by content

The gateway-path commits of the two cells (CLOUD, landing order), identified by `git log CLOUD --grep` and confirmed as the ONLY CLOUD commits attributed to them that touch the gateway dir:
- MX-d-6: **c6adb5f700** (opal_discover reads silver_datasets, 4 Schwab catalog rows, reachability) and **d9a4a03721** (A1: fail closed on cross-firm visibility, row Z-W22-S1);
- MX-g-3: **e647748786** (portal_index and opal_discover read portal-v2 through `internal_role.s3_client()`, fail closed on an unavailable role).

Applied with `git diff <c>^ <c> -- infra/aws/ec2/opal-gateway | git apply --3way --index`, in that order: **0 conflicts**, every patch "applied cleanly". Not applied: the non-gateway parts of c6adb5f700 (`workflows/atom_decomposition/catalog_entries/schwab_*.yaml` are repo-level emitter inputs, not in the artifact), each cell's proof instance, task-order flip and channel rows. No foreign payload: no MDPF_TAXSMA TX-g-1, no NFRA_OPALAI OA-e-10, no MCPMSP or OPLGTW commit (the live ref already carries MS-d-2 and OG-rl-1 whole).
**Blob equality**: the 5 files the release changes are each byte-equal to CLOUD (blob compare, `git rev-parse`) AND to the cell state e647748786: 5 of 5 (opal_discover/integration.py, portal_index/integration.py, refs/DATA_CATALOG.yaml, tests/test_opal_discover.py, tests/test_internal_role_routing.py).

## Step 2: the CENSUS (release 01845e91cf vs the live ref daa56d81ac)

Inside the gateway dir **5 files, +449 -13**; outside it **0**:

| file | +/- | shipped in the artifact |
|---|---|---|
| app/integrations/opal_discover/integration.py | +119 -4 | yes |
| app/integrations/portal_index/integration.py | +19 -5 | yes |
| app/refs/DATA_CATALOG.yaml | +94 -2 | yes |
| tests/test_opal_discover.py | +88 -2 | no |
| tests/test_internal_role_routing.py (NEW) | +129 -0 | no |

The artifact is **94 files (80 .py)**, the same count as the live artifact. The removed lines are MX-g-3's replaced instance-role client lines and docstrings (4 in opal_discover, 5 in portal_index), MX-d-6's replaced sort key (opal_discover), and the 2 catalog provenance-stamp lines; **0 removed lines in the whole diff name** principal, tier, rivalfunds, tenant, firm_role, master_admin, schwab, taxsma, mcpmsp, internal_reader, transcript or mail.

**THE PRESERVATION PROOF** (probes_r8/preservation_live_vs_deployonly_PHASEA.txt). Every file in the LIVE artifact (94) against the deploy-only artifact (94), file by file, sha256:
- **0 absent, 0 only-in-new.**
- **91 of 94 identical (78 of 80 .py). 3 changed, each ours:** app/integrations/opal_discover/integration.py (MX-d-6 + MX-g-3), app/integrations/portal_index/integration.py (MX-g-3), app/refs/DATA_CATALOG.yaml (MX-d-6: 4 Schwab rows, silver rows).
- OG-rl-1's release (transcript and mail tools, /hx routes, rosters host-side, MAIL_* keys), MS-d-2's (internal_role, sender_gate, admin_refusals), MX-r-7's (blackdiamond, etfs_get_positioning) and the Schwab host inputs are all among the 91 identical.
- The build-only artifacts from the release tree and the deploy-only tree are **94 of 94 identical** (probes_r8/release_vs_deployonly_PHASEA.txt).

**The deploy-only tree vs CLOUD 220a74350a** (the tree the deploy runs from): 21 files, all inside infra/aws/ec2/opal-gateway, 0 outside: 2 A, 5 D, 14 M. These are CLOUD's other-seat or later gateway bytes that the live ref does not carry, replaced by the live ref's bytes, and are NOT shipped: deleted app/taxsma_workbook.py, tests/acceptance/onhost_bench.py, tests/acceptance/test_onhost_bench_grader.py, tests/test_login_retire.py, tests/test_taxsma_workbook.py; modified-to-the-live-ref's-bytes app/admin_refusals.py, app/config.py, app/server.py, app/integrations/schwab/aws_roles.py, app/integrations/schwab/integration.py, the runbook, WALKTHROUGH_PROTOCOL.md, tests/conftest.py, test_admin_refusals.py, test_principal_cutover.py, test_ratelimit.py, test_schwab_engine.py, test_schwab_export.py, deploy-to-ec2.sh ; added deploy/NFRA_OPLGTW_CONTRACT.json and tests/test_schwab_host_inputs.py (on the live ref, not on CLOUD). CLOUD has since moved to bc4452a2aa and then 3efe9f0598; `git diff 220a74350a bc4452a2aa -- infra/aws/ec2/opal-gateway` is 0 lines (read), so the deploy-only tree's CLOUD base is current for the gateway dir; the tree is a closed object and does not depend on it.

## Step 3: what the deploy now needs (the LIVE script read, deploy-to-ec2.sh at daa56d81ac)

- `DEPLOY_BASE_REF` is required (exit 2 without it); the guard reads the live ref from the artifact plane twice (early and immediately before the upload) and refuses on a mismatch (exit 3).
- **The principal rosters are read HOST-SIDE** from Secrets Manager `gateway/principals/rosters` (R4, row Z-S24): `OG_MASTER_ADMIN_PRINCIPALS` and `OG_WRITE_CAPABLE_PRINCIPALS` are NOT needed and are not in the deploying shell. Both principal keys stay (`MASTER_ADMIN_PRINCIPALS`, `WRITE_CAPABLE_PRINCIPALS`: present on the host, rendered by the printf).
- **ONE deploy-time data input remains: `OG_MAIL_SENDER_TABLE`** (address list, default empty, validated against an address character set, rendered as `MAIL_SENDER_TABLE`). **The host's `MAIL_SENDER_TABLE` is SET (3 items, 67 characters)** (host_read_FINAL.txt, 11:49:56Z). A PHASE B deploy run without the same value rewrites it to EMPTY, which refuses every mail-route message, and the key census cannot see it. **Row NFRA_MCPINDEX-Z-W22-S4, ARMED, disarm_owner 2.0.0_SA_COO~MI**: the issuer supplies the same value OG-rl-1 deployed, in the shell only, and PHASE B reads the key's state (`SET items=3 len=67`) before and after.

## Step 4: the `.env` KEY CENSUS (keys only, never values; probes_r8/env_keys_PHASEA.txt, host_read_PHASEA.txt, host_read_FINAL.txt)

- host before: **46 keys, 46 distinct** (46 lines). The deploy-only script's `.env` printf (the live script, unchanged), rendered with dummy inputs: **46 keys, 46 distinct. Dropped: none. Added: none. Keys before == after.**
- Both principal keys are in the set, and **`INTERNAL_READER_ROLE_ARN` is in the live key set** (MS-d-2 added it; present on the host, non-empty). Also present and non-empty: `MASTER_ADMIN_PRINCIPALS`, `WRITE_CAPABLE_PRINCIPALS`, `BLACKDIAMOND_READER_ROLE_ARN`, `BLACKDIAMOND_READER_EXTERNAL_ID`. `MSP_CALLING_IDENTITIES` and `TRANSCRIPT_MEETING_ALLOWLIST` are present and EMPTY by design, as on the live ref.
- `ENABLED_INTEGRATIONS`: rendered = host, both 7 ids, EQUAL. Control: the live ref's own script (the rollback tree) renders the same 46 (env_keys_control_liveref_PHASEA.txt); the two scripts are byte-identical.
- No value is in any file here: the render uses dummy inputs, the host read prints names and one non-secret state line.

## Step 5: the tool count (in-process on the extracted artifacts, MOCK_GRAPH=1, the 7 live ids; probes_r8/tools_live.json, tools_deployonly.json, tools_delta_PHASEA.txt)

| | native | integration | total |
|---|---|---|---|
| live daa56d81ac artifact | 42 | 23 | **65** |
| deploy-only artifact | 42 | 23 | **65** |

**0 added, 0 removed, delta 0; the two sorted name lists are equal.** 65 is also OG-rl-1's recorded count (60 -> 65). The ac08 pin (train C3) is LIVE + OWN = 65 + 0: this release changes no registered tool, so the pin equals the live count and no test pin moves (`test_ogz2_ac08`'s `== 60` counts the entitlement sets without the schwab five and is the live ref's own, unchanged by this release).

## Step 6: the TESTS (gateway dir, MOCK_GRAPH=1; release tree vs live-ref tree, the same commands)

- **Targeted set** (test_opal_discover, test_internal_role_routing, test_portal_index, test_blackdiamond, test_entitlement_admin, test_data_entitlement_guard, test_tool_classification_composition, test_query_v0_tool, test_mcpmsp_internal_role, test_schwab_catalog; tests_targeted_*_PHASEA.txt): **release 93 passed, 3 failed**; live-ref tree (the same files minus the new one) 84 passed, 4 failed. The 3 common failures are the live ref's own: `test_ogz2_ac06`, `test_ogz1_ac05`, `test_ogz1_ac08`. The 4th at the live ref, `test_opal_discover::test_index_vocabulary_routes_the_real_catalog` (row Z-W21-S15), **passes in the release** (MX-d-6's test update).
- **Per-file full sweep** (every `tests/test_*.py`, one pytest run per file, 90 s bound each; tests_perfile_*_PHASEA.txt, tests_perfile_compare_PHASEA.txt): **live ref 57 files, 468 passed, 14 failed, 0 error, 0 timeouts; release 58 files, 477 passed, 13 failed, 0 error, 0 timeouts.** Failing ids: 14 at the live ref, 13 in the release; **13 in both (the same 13), 1 fixed by the release (the one above), 0 NEW failures.** Only two files' counts differ: test_opal_discover.py (14 passed 1 failed -> 20 passed 0 failed) and the new test_internal_role_routing.py (3 passed).
- A whole-directory single run (`pytest tests/test_*.py`) was started on both trees and hit my 570 s bound at the SAME place in both (rc=124, the stall is at the same place in both trees, as in MX-r-7's record; the file was not identified); it is NOT a result and is kept as recorded (tests_broad_*_PHASEA.txt). The per-file sweep above is the full-directory result: the stall is a cross-file interaction, not a test of this release.

## Step 7: the served path MX-g-3 turns on (read-only facts for the halves)

After the release, `portal_index` and `opal_discover` read `opal-data-portal-v2` through `app/internal_role.s3_client()` whenever `INTERNAL_READER_ROLE_ARN` is set (it IS set on the host), failing CLOSED (never falling back to the instance role) if the role is unavailable. The role `gateway-global-internal-reader-role` (created 2026-10-01T01:17:40Z) has one inline policy, one statement: `Allow s3:GetObject` on `arn:aws:s3:::opal-data-portal-v2/json/*` and `.../platinum/*` (probes_r8/internal_reader_policy_statements_PHASEA.txt); no ListBucket, no other statement. That is the same read surface query_v0 already uses (MS-d-2). `discover` on that path runs its HEAD through the shared cached role client under an 8 s wall-clock bound (row Z-W22-S3). **Row NFRA_MCPINDEX-Z-W22-S6, INERT:** with no ListBucket an absent object reads as AccessDenied, which `portal_index.s3_getter` raises as a named IntegrationError rather than returning None. A first `simulate-principal-policy` attempt returned one placeholder result and is not a verdict; the policy statement is the evidence. r8.AC2 reads the served path at PHASE B.

## What PHASE B does, in this order, on the GO (nothing below has been done)

1. **Ledger** `nfra-mcpindex-r6-rdr-release` opened first (NEVER-2; the entry names every task family that pulls the tag; BOTH paths named in the commit). Re-read the live ref (the clause above); if not daa56d81ac, STOP.
2. **Halt gate in a worktree**: if `safe-ec2-deploy.sh` resolves the issuer's serial, write `0.9.0_WK_NFRA_MCPINDEX~22` into the worktree's gitignored `org/mcp/sessions/<session>.serial` (row Z-W21-S21).
3. **Deploy** from the deploy-only tree: `cd /c/tmp/mx-dep11 && DEPLOY_BASE_REF=daa56d81ac7c91795f1a9c47b2c2430cb3879e24 OG_MAIL_SENDER_TABLE=<issuer-supplied, the same value OG-rl-1 deployed; shell only> HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_MCPINDEX~22 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`. No roster values are needed. The deploy-only worktree has no nested `mcportal/` checkout: place a3bff71ffa there as MX-r-7's PHASE B did. If the live ref moved, the script refuses at upload with both values printed and nothing written.
4. **Read back**: (a) `r8.AC2.sh` as written (status Success, `/health` 200, BD ask next_tools includes `blackdiamond_list_fees`, ETF ask next_tools includes `etfs_get_positioning`); (b) host `.env` KEY names: 46 before == 46 after, 0 dropped, and `MAIL_SENDER_TABLE` state `SET items=3 len=67` before and after; (c) tool count 65 -> 65, sorted names equal; (d) host files equal to the deploy-only artifact's 94; (e) both S3 objects carry `git-ref` = e3567ce5f788f45195bec065f4d2fc5a68a38cd3; (f) `e1z.AC1.sh` on the deployed tree reads `unrouted=0`; (g) the Schwab rows are catalogued through discover in-process on the host (the order's MX-d-6 evidence, by outcome class).
5. **Rollback on any failed leg** (never half-landed): `cd /c/tmp/mx-rb11 && DEPLOY_BASE_REF=<the then-live ref> OG_MAIL_SENDER_TABLE=<same> HALT_ACK=1 AGENT_NAME=<serial> bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` (the rollback tree's script is the same live script; its artifact equals the live one 94 of 94). No Terraform to undo.
6. After PHASE B: `r8.AC1.sh` (entry at HEAD, no sentinel, not listed OPEN/HELD), the proof instance, the status flip.

## Rows (channel INVESTIGATION_v1.md; fabric site-z; disarm_owner 2.0.0_SA_COO~MI)

| id | class / hazard | what |
|---|---|---|
| NFRA_MCPINDEX-Z-W22-S4 | OBSERVATION / **ARMED** | the host's `MAIL_SENDER_TABLE` is SET and the live script renders it from `OG_MAIL_SENDER_TABLE`; PHASE B without the same value empties it, invisible to the key census. Disarm: the issuer supplies it. |
| NFRA_MCPINDEX-Z-W22-S5 | OBSERVATION / INERT | the release and deploy-only commits were made under the audited `GIT_COMMIT_AUTHOR_OVERRIDE` (the cut trees do not carry this order); scratch branches; tree objects equal. |
| NFRA_MCPINDEX-Z-W22-S6 | OBSERVATION / INERT | the internal reader role has no ListBucket: an absent portal object reads as AccessDenied, a named IntegrationError, not None. |
