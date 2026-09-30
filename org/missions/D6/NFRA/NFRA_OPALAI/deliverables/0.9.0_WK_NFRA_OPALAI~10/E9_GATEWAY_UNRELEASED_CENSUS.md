# E9 -- what CLOUD holds on the gateway that the served commit does not (OA-e-9, round 2)

Measured by 0.9.0_WK_NFRA_OPALAI~10 at 2026-09-29. Read-only: no release, no deploy, no gateway file edited.

BASE: f791522306ded5a95e72839d119dd99e96db5513
HEAD: 60fb85b5dddc2ec7d3389a6b81ec1291b42d767f
LIVE-MATCH: yes
DENOMINATOR: 51

## How BASE was matched (step 1, amendment 2)

Live md5 over SSM (i-07dccb1615503ac99, status Success, command 02c9e8ef-a287-4cdc-b745-105463510cdf) of the six named files:

| file | live md5 |
|---|---|
| app/identity_scope.py | ed56bec258c400724ccf9be029b76845 |
| app/data_entitlement.py | 964504343c24d412a266da74e7108e69 |
| app/asker_scope.py | 02b110489ab49c6a35ac33d0782613ae |
| app/tools.py | 7ead9892a2f75b5b3326c0c16a1bcd46 |
| app/server.py | 1339aca9648e88ed754edcf902b7af26 |
| identity_tool_allowlist.txt | 19f4fef5c05aaa93571fdfb72bce243a |

Candidates compared: `6a98a0553a`, `fe94911257`, `3371f18803`, `f791522306`, `d287ffb346`, `7c7ebe14d3`, `20a58c4edb`, `54e26d66a0` and every local or
origin `rel-*` ref (19 refs). Matching all six files: `f791522306` (`rel-nfra-opalai-r2-asker-switch-on-gateway`), `7c7ebe14d3` (the deploy-only tree the
host was built from), `a48b9ce3c2` (`rel-...-switch-on-gateway-v2` tip) and `4248b70b39` (`rel-nfra-oplgtw-stream-export-v2`, OG-x-3 A2). The live `.env` key
set (27 names, values never read) equals the `deploy-to-ec2.sh` template's at all four. The survivors differ only in gateway trees: `f791522306`, `7c7ebe14d3`
and `a48b9ce3c2` share gateway tree `01264d4d90f96166712dfb375ebb5b1ac654d86e`; `4248b70b39` has `4224c9940c` and differs in nine files. Live md5 of the four
app files where it differs, against each survivor:

| file | live md5 | f791522306 | 4248b70b39 |
|---|---|---|---|
| app/integrations/schwab/engine.py | 10b0417a192de2a3beda7cfba2b23a56 | 10b0417a192de2a3beda7cfba2b23a56 | b06a27f7317b1f664f75c66d757e8491 |
| app/integrations/schwab/envelope.py | c4ade82d98c030868ba10752b3438c62 | c4ade82d98c030868ba10752b3438c62 | 651359f19abc63a2b77811df1f3fbf29 |
| app/integrations/schwab/export.py | 28b5c7ffe1b367788d8912f18558d8fe | 28b5c7ffe1b367788d8912f18558d8fe | c9943e7840e2e1ea2cb97df75feccf90 |
| app/integrations/schwab/integration.py | e8a45441e9e16281da8c380ab5fe28be | e8a45441e9e16281da8c380ab5fe28be | f436630c352d0cedfd1dbaedc67b43d3 |

The host matches `f791522306` on 4 of 4 and `4248b70b39` on 0 of 4. BASE is `f791522306`, cross-checked by the served gateway tree (the
deploy-only tree `7c7ebe14d3` that was built and uploaded has gateway tree `01264d4d90...`, equal to `f791522306`'s). Survivors by the six files: all four above.
The newest of them (`4248b70b39`) is not what the host runs (the same defect as rows Z-W10-S3 and the OA-e-3 resolution).

HEAD is the CLOUD commit this worktree sat on when the census was counted.

## The census

Population: `git rev-list --no-merges f791522306..HEAD -- infra/aws/ec2/opal-gateway`, 51 commits (the DENOMINATOR). One row each.
Class rule, mechanical and stated so it can be re-run: a file of a commit is ON HOST when BASE's blob of it equals the commit's blob or a later population
commit's blob, or when every non-blank line the commit added is in BASE's file and every line it removed (and did not re-add) is absent from it (the line
test, for cherry-picks that landed with a different parent). `released-elsewhere` = every file on host (a file replaced afterwards counts on host when the
rest is; the row's note names it). `superseded` = no file on host and none of the lines the commit added survive at HEAD (the replacing commit is named).
`unreleased` = anything else. The project is the code in the subject; where the subject carries only an order id (OA-, MP-, MX-, OG-, TX-) the project is
that prefix's (column 2 says `-` for none). No code and no order id = UNATTRIBUTED_GW.

| commit | project order | class | files |
|---|---|---|---|
| 82824d829f | NFRA_OPLGTW OG-h-1 | unreleased | tests/conftest.py, tests/test_ratelimit.py, tests/test_schwab_engine.py, tests/test_schwab_export.py |
| af104d6353 | NFRA_OPALAI OA-f-7 | released-elsewhere | app/asker_scope.py, tests/test_asker_binding.py, tests/test_asker_nochannels.py, tests/test_portal_grant.py |
| 0906bf01e5 | NFRA_OPLGTW OG-u-2 | unreleased | app/oauth_as.py, tests/test_dcr_idle_lifetime.py |
| 0c3d545002 | NFRA_OPLGTW OG-x-2 | unreleased | app/integrations/schwab/engine.py, app/integrations/schwab/envelope.py, app/integrations/schwab/export.py, app/integrations/schwab/integration.py, tests/acceptance/conftest.py +4 more |
| 2df96ab2b2 | NFRA_OPLGTW OG-v-6 | unreleased | tests/acceptance/WALKTHROUGH_PROTOCOL.md |
| c4d2274c6d | NFRA_OPLGTW OG-u-1 | unreleased | app/ratelimit.py, app/server.py, tests/test_auth_hardening.py |
| 344cca64a1 | NFRA_OPLGTW OG-t-1 | unreleased | tests/test_data_entitlement_guard.py, tests/test_principal_cutover.py |
| d292b6c0b9 | NFRA_OPLGTW OG-v-6 | unreleased | tests/acceptance/WALKTHROUGH_PROTOCOL.md |
| b5a585cf2f | NFRA_OPLGTW OG-t-1 | unreleased | app/config.py, app/guard.py, app/integrations/base.py, app/tier.py, app/token_broker.py +2 more |
| a8cd1b06d3 | NFRA_OPLGTW OG-o-3 | unreleased | runbooks/SCHWAB_PILOT_RUNBOOK.md |
| 4bbb30017a | NFRA_MCPINDEX MX-r-4 | released-elsewhere | deploy-to-ec2.sh |
| 357d85c0ba | NFRA_MCPINDEX MX-x-2 | released-elsewhere | app/integrations/portal_index/integration.py, app/refs/DATA_CATALOG.yaml |
| a2c96703b1 | NFRA_OPALAI OA-e-1 | released-elsewhere | tests/test_portal_grant.py |
| 8ed37b3266 | NFRA_OPALAI OA-e-10 | unreleased | app/server.py, tests/test_login_retire.py |
| 2254910889 | NFRA_OPALAI OA-e-1 | released-elsewhere | app/asker_scope.py, app/tools.py, tests/test_asker_binding.py, tests/test_asker_scope.py |
| 85e1158e6e | NFRA_MCPINDEX MX-d-3 | released-elsewhere | app/integrations/opal_discover/integration.py, tests/test_opal_discover.py |
| 31b9d1975e | NFRA_MCPORTAL MP-f-1 | unreleased | tests/conftest.py |
| 14f5219039 | NFRA_OPLGTW OG-s-1 | released-elsewhere | deploy-to-ec2.sh |
| f660b89f55 | NFRA_OPLGTW OG-e-1 | released-elsewhere | ops/schwab_entitlement_admin.py, tests/test_email_deny.py, tests/test_portal_grant.py |
| 3e936f77bd | NFRA_OPLGTW OG-e-1 | released-elsewhere | app/access_state.py, app/data_entitlement.py, app/server.py, app/token_broker.py, ops/schwab_entitlement_admin.py +2 more |
| 9a28cfbbe6 | NFRA_OPALAI OA-g-1 | released-elsewhere | app/admin_grants.py, tests/test_portal_grant.py |
| da7749916d | NFRA_OPALAI OA-g-1 | released-elsewhere | app/asker_scope.py, app/data_entitlement.py, ops/schwab_entitlement_admin.py, tests/test_portal_grant.py |
| bcb48cf626 | NFRA_MCPINDEX MX-c-5 | released-elsewhere | app/integrations/schwab/integration.py |
| e1cdb12550 | NFRA_MCPINDEX MX-v-6 | released-elsewhere | tests/routing/questions.yaml, tests/routing/run_routing.py |
| 38d47e22a9 | NFRA_OPALAI OA-f-1 | released-elsewhere | app/context.py, app/identity_scope.py, app/server.py, identity_tool_allowlist.txt, tests/test_identity_scope.py |
| bc0cde67f0 | NFRA_MCPINDEX MX-t-8 | unreleased | app/data_entitlement.py, app/integrations/portal_index/integration.py, app/refs/DATA_CATALOG.yaml, tests/test_entitlement_admin.py, tests/test_portal_index.py |
| d36d31f8c5 | NFRA_MCPINDEX MX-t-8 | released-elsewhere | tests/test_portal_index.py |
| 84a725073b | NFRA_MCPINDEX MX-t-8 | unreleased | app/integrations/portal_index/integration.py, tests/test_entitlement_admin.py, tests/test_portal_index.py |
| d6f2689497 | UNATTRIBUTED_GW - | released-elsewhere | app/destructive_ops.py, tests/test_teams_reader_fallback.py |
| 7acf3b41bb | UNATTRIBUTED_GW - | superseded | tests/test_entitlement_admin.py |
| 5db82fca44 | UNATTRIBUTED_GW - | released-elsewhere | app/audit.py, app/identity_scope.py, app/tools.py, tests/test_teams_reader_fallback.py |
| 678891171b | UNATTRIBUTED_GW - | released-elsewhere | app/data_entitlement.py, app/destructive_ops.py, app/tools.py, tests/test_entitlement_admin.py, tests/test_teams_reader_fallback.py |
| 2c25c4c831 | NFRA_MCPINDEX MX-t-8 | released-elsewhere | app/data_entitlement.py, app/integrations/portal_index/__init__.py, app/integrations/registry.py, app/refs/DATA_CATALOG.yaml, tests/test_portal_index.py |
| b2fb5c6adb | NFRA_MCPORTAL MP-d-1 | released-elsewhere | app/owner_gate.py, tests/test_admin_round2.py |
| 81d37aafda | NFRA_MCPINDEX MX-t-8 | released-elsewhere | tests/test_portal_index.py |
| 8829b066d1 | NFRA_MCPINDEX MX-d-2 | released-elsewhere | tests/test_opal_discover.py |
| 4bfab1bcf2 | NFRA_MCPINDEX MX-d-2 | released-elsewhere | app/integrations/opal_discover/__init__.py, app/integrations/opal_discover/integration.py, tests/test_opal_discover.py |
| 83cbd1a605 | NFRA_MCPORTAL MP-d-1 | released-elsewhere | deploy-to-ec2.sh |
| 37f208249f | NFRA_MCPINDEX MX-c-5 | released-elsewhere | app/integrations/globgrph/integration.py, app/integrations/opal_portal/integration.py, app/integrations/ycharts/integration.py |
| ece3aab4b5 | NFRA_MCPORTAL MP-d-1 | released-elsewhere | deploy-to-ec2.sh |
| d0ba96d27c | NFRA_MCPORTAL MP-g-1 | released-elsewhere | app/admin_api.py, app/admin_grants.py, app/owner_gate.py, tests/test_admin_round2.py |
| 17b7e01c0f | NFRA_MCPORTAL MP-t-4 | released-elsewhere | app/admin_api.py, app/admin_grants.py, app/server.py, tests/test_admin_grants.py |
| 050035f941 | NFRA_OPALAI OA-t-6 | released-elsewhere | app/audit.py |
| 98ad7e253f | NFRA_MCPORTAL MP-t-1 | unreleased | app/admin_api.py, app/config.py, app/owner_gate.py, app/server.py, tests/test_owner_gate.py |
| cc22fdfb9d | NFRA_OPALAI OA-t-5 | unreleased | app/asker_scope.py, app/data_entitlement.py, app/tools.py, tests/test_asker_scope.py |
| 119a49eef0 | NFRA_MCPINDEX MX-c-4 | released-elsewhere | app/destructive_ops.py, app/integrations/base.py, app/integrations/registry.py, tests/test_entitlement_admin.py, tests/test_tool_classification_composition.py |
| 650c9a99cb | NFRA_MCPINDEX MX-c-2 | released-elsewhere | app/refs/DATA_CATALOG.yaml |
| 9e4074c33a | NFRA_OPLGTW OG-r-2 | unreleased | tests/acceptance/onhost_bench.py |
| 6c37cc6b00 | NFRA_OPLGTW OG-r-1 | superseded | runbooks/SCHWAB_PILOT_RUNBOOK.md |
| 8dce9aeb0b | MDPF_TAXSMA TX-g-1 | unreleased | tests/test_taxsma_workbook.py |
| 6abf60e5d5 | MDPF_TAXSMA TX-g-1 | unreleased | app/config.py, app/server.py, app/taxsma_workbook.py, tests/test_principal_cutover.py, tests/test_taxsma_workbook.py |

### Notes per commit (evidence at BASE; author; subject)

- `82824d829f` unreleased [subject]: 4 of 4 files not on host (tests/conftest.py, tests/test_ratelimit.py, tests/test_schwab_engine.py...) -- 0.9.0_WK_NFRA_OPLGTW~13 -- fix(NFRA_OPLGTW OG-h-1, 0.9.0_WK_NFRA_OPLGTW~13): batch hygiene -- out-of-repo citation register (S43), env-honouring AU
- `af104d6353` released-elsewhere [order-id]: app/asker_scope.py: BASE blob == this commit's blob f15394fefd; tests/test_asker_binding.py: BASE blob == this commit's blob eefc8b6699; tests/test_asker_nochannels.py: BASE blob == this commit's blob 2466b57abc (+1 more, all on host) -- 0.9.0_WK_NFRA_OPALAI~22 -- OA-f-7 code: an asker grant with no portal_channels gets no portal catalog (fail closed)
- `0906bf01e5` unreleased [subject]: 2 of 2 files not on host (app/oauth_as.py, tests/test_dcr_idle_lifetime.py) -- 0.9.0_WK_NFRA_OPLGTW~12 -- build(NFRA_OPLGTW OG-u-2, 0.9.0_WK_NFRA_OPLGTW~12): a DCR client expires after a 30-day idle lifetime, checked at every 
- `0c3d545002` unreleased [subject]: 9 of 9 files not on host (app/integrations/schwab/engine.py, app/integrations/schwab/envelope.py, app/integrations/schwab/export.py...) -- 0.9.0_WK_NFRA_OPLGTW~11 -- build(NFRA_OPLGTW OG-x-2, 0.9.0_WK_NFRA_OPLGTW~11): streaming Schwab CSV export -- wired end to end, refused on the coun
- `2df96ab2b2` unreleased [subject]: 1 of 1 files not on host (tests/acceptance/WALKTHROUGH_PROTOCOL.md) -- 0.9.0_WK_NFRA_OPLGTW~10 -- complete(NFRA_OPLGTW.TO-OG-v-6 A1, 0.9.0_WK_NFRA_OPLGTW~10): five stale protocol lines corrected (:38 :242 answer path, 
- `c4d2274c6d` unreleased [subject]: 3 of 3 files not on host (app/ratelimit.py, app/server.py, tests/test_auth_hardening.py) -- 0.9.0_WK_NFRA_OPLGTW~12 -- build(NFRA_OPLGTW OG-u-1, 0.9.0_WK_NFRA_OPLGTW~12): /ms/site_children checks the credential before its parameters (W3-S1
- `344cca64a1` unreleased [subject]: 2 of 2 files not on host (tests/test_data_entitlement_guard.py, tests/test_principal_cutover.py) -- 0.9.0_WK_NFRA_OPLGTW~12 -- build(NFRA_OPLGTW OG-t-1 A1, 0.9.0_WK_NFRA_OPLGTW~12): test_principal_cutover.py and test_data_entitlement_guard.py move
- `d292b6c0b9` unreleased [subject]: 1 of 1 files not on host (tests/acceptance/WALKTHROUGH_PROTOCOL.md) -- 0.9.0_WK_NFRA_OPLGTW~10 -- wip(NFRA_OPLGTW OG-v-6, 0.9.0_WK_NFRA_OPLGTW~10): pre-seal state -- D_NEW/D_PREV fixed, 12-snapshot grain declaration me
- `b5a585cf2f` unreleased [subject]: 7 of 7 files not on host (app/config.py, app/guard.py, app/integrations/base.py...) -- 0.9.0_WK_NFRA_OPLGTW~12 -- build(NFRA_OPLGTW OG-t-1, 0.9.0_WK_NFRA_OPLGTW~12): the person tier is keyed on the principal tid/oid, never the email (
- `a8cd1b06d3` unreleased [subject]: 1 of 1 files not on host (runbooks/SCHWAB_PILOT_RUNBOOK.md) -- 0.9.0_WK_NFRA_OPLGTW~13 -- fix(NFRA_OPLGTW OG-o-3, 0.9.0_WK_NFRA_OPLGTW~13): runbook text repair -- three cross-references (6.1, 8, 6.1), the secti
- `4bbb30017a` released-elsewhere [subject]: deploy-to-ec2.sh: BASE blob == this commit's blob 20a76d2421 -- 0.9.0_WK_NFRA_MCPINDEX~10 -- build(NFRA_MCPINDEX MX-r-4 A1, 0.9.0_WK_NFRA_MCPINDEX~10): ENABLED_INTEGRATIONS gains opal_discover and portal_index on 
- `357d85c0ba` released-elsewhere [subject]: app/integrations/portal_index/integration.py: BASE blob == this commit's blob 31af36ec34; app/refs/DATA_CATALOG.yaml: BASE blob == this commit's blob 8828103032 -- 0.9.0_WK_NFRA_MCPINDEX~13 -- feat(NFRA_MCPINDEX MX-x-2 A1, 0.9.0_WK_NFRA_MCPINDEX~13): portal_* catalog rows get their own portal_datasets section na
- `a2c96703b1` released-elsewhere [subject]: tests/test_portal_grant.py: BASE blob == blob at later commit af104d6353 -- 0.9.0_WK_NFRA_OPALAI~10 -- test(NFRA_OPALAI OA-e-1, 0.9.0_WK_NFRA_OPALAI~10): tests/test_portal_grant.py asker fixtures follow the repair -- config
- `8ed37b3266` unreleased [subject]: 2 of 2 files not on host (app/server.py, tests/test_login_retire.py) -- 0.9.0_WK_NFRA_OPALAI~16 -- build(NFRA_OPALAI OA-e-10, 0.9.0_WK_NFRA_OPALAI~16): census of legacy /login (0 uses in the journal window, 1 server-hel
- `2254910889` released-elsewhere [subject]: app/asker_scope.py: BASE blob == blob at later commit af104d6353; app/tools.py: BASE blob == this commit's blob fafe604df4; tests/test_asker_binding.py: BASE blob == blob at later commit af104d6353 (+1 more, all on host) -- 0.9.0_WK_NFRA_OPALAI~10 -- feat(NFRA_OPALAI OA-e-1, 0.9.0_WK_NFRA_OPALAI~10): asker-scoping repair -- tenant class gate, bound message and reply, g
- `85e1158e6e` released-elsewhere [subject]: app/integrations/opal_discover/integration.py: BASE blob == this commit's blob 7278ad9af5; tests/test_opal_discover.py: BASE blob == this commit's blob b68b02c9f4 -- 0.9.0_WK_NFRA_MCPINDEX~10 -- feat(NFRA_MCPINDEX MX-d-3, 0.9.0_WK_NFRA_MCPINDEX~10): opal_discover ranks its matches; a dataset ask routes to its data
- `31b9d1975e` unreleased [subject]: 1 of 1 files not on host (tests/conftest.py) -- 0.9.0_WK_NFRA_MCPORTAL~4 -- feat(NFRA_MCPORTAL MP-f-1, 0.9.0_WK_NFRA_MCPORTAL~4): session-scoped audit-path fixture in gateway tests/conftest.py
- `14f5219039` released-elsewhere [subject]: deploy-to-ec2.sh: BASE blob == blob at later commit 4bbb30017a -- 0.9.0_WK_NFRA_OPLGTW~9 -- build(NFRA_OPLGTW OG-s-1, 0.9.0_WK_NFRA_OPLGTW~9): SPRINT_VIEW_ALLOWED_EMAILS=andrew@opalinvest.com in the .env printf l
- `f660b89f55` released-elsewhere [subject]: ops/schwab_entitlement_admin.py: BASE blob == this commit's blob 07bb68373e; tests/test_email_deny.py: BASE blob == this commit's blob b35109894b; tests/test_portal_grant.py: BASE blob == blob at later commit af104d6353 -- 0.9.0_WK_NFRA_OPLGTW~7 -- fix(NFRA_OPLGTW.TO-OG-e-1, 0.9.0_WK_NFRA_OPLGTW~7): AMENDMENT A1 -- a restricted activate/prepare with no resolvable ema
- `3e936f77bd` released-elsewhere [subject]: app/access_state.py: BASE blob == this commit's blob c3e6c5f025; app/data_entitlement.py: BASE blob == this commit's blob a44ff20ed1; app/server.py: line test: all 39 added lines present and 0 removed lines absent at BASE (+4 more, all on host) -- 0.9.0_WK_NFRA_OPLGTW~7 -- build(NFRA_OPLGTW.TO-OG-e-1, 0.9.0_WK_NFRA_OPLGTW~7): the email-keyed deny record and its guard (row W3-S22)
- `9a28cfbbe6` released-elsewhere [subject]: app/admin_grants.py: BASE blob == this commit's blob e3f591ef5a; tests/test_portal_grant.py: BASE blob == blob at later commit af104d6353 -- 0.9.0_WK_NFRA_OPALAI~9 -- build(NFRA_OPALAI.TO-OA-g-1 item 5, 0.9.0_WK_NFRA_OPALAI~9): the owner read-back (app/admin_grants.py _grant_json) carri
- `da7749916d` released-elsewhere [subject]: app/asker_scope.py: BASE blob == blob at later commit af104d6353; app/data_entitlement.py: BASE blob == blob at later commit 3e936f77bd; ops/schwab_entitlement_admin.py: BASE blob == blob at later commit f660b89f55 (+1 more, all on host) -- 0.9.0_WK_NFRA_OPALAI~9 -- build(NFRA_OPALAI.TO-OA-g-1, 0.9.0_WK_NFRA_OPALAI~9): the existing grant grammar admits a portal-only asker grant (adden
- `bcb48cf626` released-elsewhere [subject]: app/integrations/schwab/integration.py: BASE blob == this commit's blob 944b2945b6 -- 0.9.0_WK_NFRA_MCPINDEX~1 -- build(NFRA_MCPINDEX.TO-MX-c-5, 0.9.0_WK_NFRA_MCPINDEX~1): the 5 schwab tools declare their class in integrations/schwab/
- `e1cdb12550` released-elsewhere [subject]: tests/routing/questions.yaml: BASE blob == this commit's blob fa1c6d59f4; tests/routing/run_routing.py: BASE blob == this commit's blob 98fc8ef1ff -- 0.9.0_WK_NFRA_MCPINDEX~2 -- build(NFRA_MCPINDEX.TO-MX-v-6, 0.9.0_WK_NFRA_MCPINDEX~2): routing harness over 27 real staff asks -- ROUTING 21 of 27, p
- `38d47e22a9` released-elsewhere [subject]: app/context.py: BASE blob == this commit's blob 90a2cb4121; app/identity_scope.py: line test: all 51 added lines present and 14 removed lines absent at BASE; app/server.py: line test: all 13 added lines present and 7 removed lines absent at BASE (+2 more, all on host) -- 0.9.0_WK_NFRA_OPALAI~8 -- build(NFRA_OPALAI.TO-OA-f-1, 0.9.0_WK_NFRA_OPALAI~8): identity_scope keys the upload row on (identity, OAuth client_id) 
- `bc0cde67f0` unreleased [subject]: 1 of 5 files not on host (tests/test_entitlement_admin.py); 4 already on host -- 0.9.0_WK_NFRA_MCPINDEX~3 -- build(NFRA_MCPINDEX.TO-MX-t-8, 0.9.0_WK_NFRA_MCPINDEX~3): portal_index cut to the 3 tools catalog_gate resolves (order i
- `d36d31f8c5` released-elsewhere [subject]: tests/test_portal_index.py: BASE blob == blob at later commit bc0cde67f0 -- 0.9.0_WK_NFRA_MCPINDEX~3 -- fix(NFRA_MCPINDEX.TO-MX-t-8, 0.9.0_WK_NFRA_MCPINDEX~3): test_portal_index prints into pytest's capture, so each -v verdi
- `84a725073b` unreleased [subject]: 1 of 3 files not on host (tests/test_entitlement_admin.py); 2 already on host -- 0.9.0_WK_NFRA_MCPINDEX~3 -- build(NFRA_MCPINDEX.TO-MX-t-8, 0.9.0_WK_NFRA_MCPINDEX~3): portal_index takes every key from its own catalog row through 
- `d6f2689497` released-elsewhere [none]: app/destructive_ops.py: line test: all 1 added lines present and 1 removed lines absent at BASE; tests/test_teams_reader_fallback.py: BASE blob == this commit's blob bc3c0a9206 -- 1.0.0_SA_CTO -- fix(1.0.0_SA_CTO, opal-gateway): classify read_teams_attachment SAFE -- the guard refused it as write-class UNCLASSIFIED
- `7acf3b41bb` superseded [none]: replaced by bc0cde67f0 -- 1.0.0_SA_CTO -- test(1.0.0_SA_CTO, opal-gateway): pinned tool count 46 on rel-laptop-teams-reader-gw -- 45 at the deployed 1f7128201a pl
- `5db82fca44` released-elsewhere [none]: app/audit.py: BASE blob == this commit's blob daaa73ec04; app/identity_scope.py: line test: all 3 added lines present and 0 removed lines absent at BASE; app/tools.py: BASE blob == blob at later commit 2254910889 (+1 more, all on host) -- 1.0.0_SA_CTO -- fix(1.0.0_SA_CTO, opal-gateway): the two changes from site Z 1.0.0_SA_CTO~O's review of 32438a3fa9 -- seed row for opalb
- `678891171b` released-elsewhere [none]: 3 of 5 files on host; the other 2 replaced by bc0cde67f0, d6f2689497 -- 1.0.0_SA_CTO -- fix(1.0.0_SA_CTO, opal-gateway): Teams readers survive a Graph 500 on $select; new read_chat_message_images reads pasted
- `2c25c4c831` released-elsewhere [subject]: app/data_entitlement.py: BASE blob == blob at later commit 3e936f77bd; app/integrations/portal_index/__init__.py: BASE blob == this commit's blob b5f35229ef; app/integrations/registry.py: BASE blob == this commit's blob c9130cd0ee (+2 more, all on host) -- 0.9.0_WK_NFRA_MCPINDEX~3 -- build(NFRA_MCPINDEX.TO-MX-t-8 PHASE 1, 0.9.0_WK_NFRA_MCPINDEX~3): the LEGACY-READ entries, registry and entitlement line
- `b2fb5c6adb` released-elsewhere [subject]: app/owner_gate.py: BASE blob == this commit's blob 6135ad2afd; tests/test_admin_round2.py: BASE blob == this commit's blob c7525d851d -- 0.9.0_WK_NFRA_MCPORTAL~2 -- fix(NFRA_MCPORTAL MP-d-1 step 0, 0.9.0_WK_NFRA_MCPORTAL~2): the owner header capture logs claim KEYS only
- `81d37aafda` released-elsewhere [subject]: tests/test_portal_index.py: BASE blob == blob at later commit bc0cde67f0 -- 0.9.0_WK_NFRA_MCPINDEX~3 -- build(NFRA_MCPINDEX.TO-MX-t-8, 0.9.0_WK_NFRA_MCPINDEX~3): portal tools -- tests, catalog entries and rows land; the port
- `8829b066d1` released-elsewhere [subject]: tests/test_opal_discover.py: BASE blob == blob at later commit 85e1158e6e -- 0.9.0_WK_NFRA_MCPINDEX~2 -- fix(NFRA_MCPINDEX.TO-MX-d-2, 0.9.0_WK_NFRA_MCPINDEX~2): the discover tests print through pytest's capture, so '-v' keeps
- `4bfab1bcf2` released-elsewhere [subject]: app/integrations/opal_discover/__init__.py: BASE blob == this commit's blob 7f2c44790e; app/integrations/opal_discover/integration.py: BASE blob == blob at later commit 85e1158e6e; tests/test_opal_discover.py: BASE blob == blob at later commit 85e1158e6e -- 0.9.0_WK_NFRA_MCPINDEX~2 -- build(NFRA_MCPINDEX.TO-MX-d-2, 0.9.0_WK_NFRA_MCPINDEX~2): the discover family answers from the ONE catalog, dormant by d
- `83cbd1a605` released-elsewhere [subject]: deploy-to-ec2.sh: BASE blob == blob at later commit 4bbb30017a -- 0.9.0_WK_NFRA_MCPORTAL~2 -- fix(NFRA_MCPORTAL.TO-MP-d-1, 0.9.0_WK_NFRA_MCPORTAL~2): restore the space before "${REGION}" in deploy-to-ec2.sh's .env 
- `37f208249f` released-elsewhere [subject]: app/integrations/globgrph/integration.py: BASE blob == this commit's blob be6e9e3680; app/integrations/opal_portal/integration.py: BASE blob == this commit's blob 577701d04a; app/integrations/ycharts/integration.py: BASE blob == this commit's blob 4c404533ef -- 0.9.0_WK_NFRA_MCPINDEX~1 -- build(NFRA_MCPINDEX.TO-MX-c-5, 0.9.0_WK_NFRA_MCPINDEX~1): the 9 ycharts/opal_portal/globgrph tools declare their class o
- `ece3aab4b5` released-elsewhere [subject]: deploy-to-ec2.sh: BASE blob == blob at later commit 4bbb30017a -- 0.9.0_WK_NFRA_MCPORTAL~2 -- build(NFRA_MCPORTAL.TO-MP-d-1, 0.9.0_WK_NFRA_MCPORTAL~2): the gateway deploy ships Andrew's dashboard bundle and the thr
- `d0ba96d27c` released-elsewhere [order-id]: app/admin_api.py: BASE blob == this commit's blob e608f6e977; app/admin_grants.py: BASE blob == blob at later commit 9a28cfbbe6; app/owner_gate.py: BASE blob == blob at later commit b2fb5c6adb (+1 more, all on host) -- 0.9.0_WK_NFRA_MCPORTAL~2 -- build(MP-g-1, 0.9.0_WK_NFRA_MCPORTAL~2): the gateway captures the verified OWNER header's claim keys (OWNER-HEADER-CLAIM
- `17b7e01c0f` released-elsewhere [subject]: app/admin_api.py: BASE blob == blob at later commit d0ba96d27c; app/admin_grants.py: BASE blob == blob at later commit 9a28cfbbe6; app/server.py: line test: all 21 added lines present and 1 removed lines absent at BASE (+1 more, all on host) -- 0.9.0_WK_NFRA_MCPORTAL~2 -- feat(NFRA_MCPORTAL MP-t-4, 0.9.0_WK_NFRA_MCPORTAL~2): admin grant read/narrow/widen/changes handlers, plus the drain ame
- `050035f941` released-elsewhere [subject]: app/audit.py: BASE blob == blob at later commit 5db82fca44 -- 0.9.0_WK_NFRA_OPALAI~2 -- fix(NFRA_OPALAI OA-t-6, 0.9.0_WK_NFRA_OPALAI~2): declare opal_asker_query in audit.py's _ARGS_ALLOWLIST
- `98ad7e253f` unreleased [subject]: 1 of 5 files not on host (app/server.py); 4 already on host -- 0.9.0_WK_NFRA_MCPORTAL~2 -- build(NFRA_MCPORTAL round 1 MP-t-1, 0.9.0_WK_NFRA_MCPORTAL~2): owner-gate + serving for Andrew's dashboard
- `cc22fdfb9d` unreleased [subject]: 1 of 4 files not on host (tests/test_asker_scope.py); 3 already on host -- 0.9.0_WK_NFRA_OPALAI~2 -- build(NFRA_OPALAI OA-t-5, 0.9.0_WK_NFRA_OPALAI~2): the asker-scoped query tool -- opal_asker_query resolves the Teams me
- `119a49eef0` released-elsewhere [subject]: app/destructive_ops.py: line test: all 25 added lines present and 2 removed lines absent at BASE; app/integrations/base.py: BASE blob == this commit's blob 03b8c84f07; app/integrations/registry.py: BASE blob == blob at later commit 2c25c4c831 (+2 more, all on host) -- 0.9.0_WK_NFRA_MCPINDEX~1 -- build(NFRA_MCPINDEX.TO-MX-c-4, 0.9.0_WK_NFRA_MCPINDEX~1): classification and registration compose from each integration'
- `650c9a99cb` released-elsewhere [subject]: app/refs/DATA_CATALOG.yaml: BASE blob == blob at later commit 357d85c0ba -- 0.9.0_WK_NFRA_MCPINDEX~1 -- build(NFRA_MCPINDEX.TO-MX-c-2, 0.9.0_WK_NFRA_MCPINDEX~1): silver dataset entries, one source file per dataset -- schema,
- `9e4074c33a` unreleased [subject]: 1 of 1 files not on host (tests/acceptance/onhost_bench.py) -- 0.9.0_WK_NFRA_OPLGTW~2 -- build(NFRA_OPLGTW OG-r-2, 0.9.0_WK_NFRA_OPLGTW~2): on-host capacity/regression benchmark harness + probe
- `6c37cc6b00` superseded [subject]: replaced by a8cd1b06d3 -- 0.9.0_WK_NFRA_OPLGTW~2 -- amend(NFRA_OPLGTW.TO-OG-r-1, 0.9.0_WK_NFRA_OPLGTW~2): R-56 items 2-3 -- AC19's rollback census (probe + s7.2 states NO V
- `8dce9aeb0b` unreleased [subject]: 1 of 1 files not on host (tests/test_taxsma_workbook.py) -- 0.9.0_WK_MDPF_TAXSMA~1 -- fix(MDPF_TAXSMA.TO-TX-g-1, 0.9.0_WK_MDPF_TAXSMA~1): three instrument defects the first probe run measured
- `6abf60e5d5` unreleased [subject]: 5 of 5 files not on host (app/config.py, app/server.py, app/taxsma_workbook.py...) -- 0.9.0_WK_MDPF_TAXSMA~1 -- feat(MDPF_TAXSMA.TO-TX-g-1, 0.9.0_WK_MDPF_TAXSMA~1): GET /ms/taxsma-workbook capability, route, config keys, tests, prob

## Summary

Per class: released-elsewhere 31, unreleased 18, superseded 2 (total 51 = DENOMINATOR).

| project | released-elsewhere | unreleased | superseded | total |
|---|---|---|---|---|
| MDPF_TAXSMA | 0 | 2 | 0 | 2 |
| NFRA_MCPINDEX | 13 | 2 | 0 | 15 |
| NFRA_MCPORTAL | 5 | 2 | 0 | 7 |
| NFRA_OPALAI | 7 | 2 | 0 | 9 |
| NFRA_OPLGTW | 3 | 10 | 1 | 14 |
| UNATTRIBUTED_GW | 3 | 0 | 1 | 4 |

### The unreleased commits a move from BASE would carry (18)

Commits with an `app/` file not yet on the host (would change the served behaviour when released): `0906bf01e5` (NFRA_OPLGTW OG-u-2), `0c3d545002` (NFRA_OPLGTW OG-x-2), `c4d2274c6d` (NFRA_OPLGTW OG-u-1), `b5a585cf2f` (NFRA_OPLGTW OG-t-1), `8ed37b3266` (NFRA_OPALAI OA-e-10), `98ad7e253f` (NFRA_MCPORTAL MP-t-1), `6abf60e5d5` (MDPF_TAXSMA TX-g-1).

Commits whose not-on-host files are tests, runbooks or benchmarks only (no served effect): `82824d829f` (NFRA_OPLGTW OG-h-1), `2df96ab2b2` (NFRA_OPLGTW OG-v-6), `344cca64a1` (NFRA_OPLGTW OG-t-1), `d292b6c0b9` (NFRA_OPLGTW OG-v-6), `a8cd1b06d3` (NFRA_OPLGTW OG-o-3), `31b9d1975e` (NFRA_MCPORTAL MP-f-1), `bc0cde67f0` (NFRA_MCPINDEX MX-t-8), `84a725073b` (NFRA_MCPINDEX MX-t-8), `cc22fdfb9d` (NFRA_OPALAI OA-t-5), `9e4074c33a` (NFRA_OPLGTW OG-r-2), `8dce9aeb0b` (MDPF_TAXSMA TX-g-1).

### Two commits outside the DENOMINATOR

`git rev-list --full-history` names 53 commits in the same range; git's default history simplification (the command the criterion fixes) drops two. Both are this
worker's OA-e-3 commits, ON the host through `f791522306`'s cherry-picks: `c06a3a4379` (the identity_scope seed + test) and `685fabc691` (the test_asker_scope fixture).
They are not table rows, so rows = DENOMINATOR. Row NFRA_OPALAI-Z-W10-S7 records the difference.

### Limits of this census

- The class is decided by file content and lines at BASE, not by intent: a commit that touches a test file only is classed `unreleased` when the host's copy of the
  test differs, though the host runs no tests. The table shows the files so a reader can discount those.
- `released-elsewhere` by the line test can over-match on lines common to many files; the per-commit notes show which test fired.
- The mixed rows (some files on host, some not) are classed `unreleased`; the note counts both halves.
