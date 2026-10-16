# Never-widen ask -- OG-ap-28: the round-38 batched gateway release (FINAL TEXT: release `bf9d23b518`; signatures blank)

By: `0.7.0_AE_CloudOps~Z`, 2026-10-16. Order `NFRA_OPLGTW.TO-OG-ap-28` at A3 (`1a74cf39b7`). For three halves: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O`, `3.0.0_SA_CVO~Z`.
`base_sha` = the live ref `d14445961dd6d04275ca8186372a4df4c4fcc5cc` (EC2_MANIFEST `deployed_commit` at HEAD; the S3 `git-ref` of `opal-gateway-latest.tar.gz` reads the same; the host md5 walk below).
`trunk_sha` = `858e9275589e51f0f15d8c55462125c7152f621c` (the GO of msg 35164; it holds the CRO's four lookup-alias rows `ca679b6560`; the catalog blob is still `b81c48aa3c`). `mcportal_sha` = `59e802a4185a62129bf28ebb4df6eda9b70e03ff`. `prelude_sha` = `2dc919cf26ce4190157b21c7f3c18737de10c573`. **`release_sha` = `bf9d23b518527e0e5f9a26aa240fd5af72af6c11`** (the tip; its parent is the prelude, whose parent is `base_sha`). `W/ap28_release.json` records all of them.
No deploy, no apply. Everything below is measured on the re-cut tree `C:/tmp/og-rel-batch2` (uncommitted take) or on the live host, read-only.

## 0. What I measured at the live ref (Phase A step 1)

| read | result |
|---|---|
| host md5 walk over `app/`, `deploy/`, `lib/` (SSM, `W/ap28_host_md5.json`) | 139 expected files (git blobs of the live ref), 141 on the host (the two staged `app/refs` files): **139 equal, 0 differ, 0 missing, 0 unexplained extra**; both staged refs equal trunk's blobs. The dashboard bundle is excluded by grain (built from the mcportal checkout). |
| `.env` key NAMES (never values) | 64 keys; `MUSE_CLIENT_ID` is **not** a key; `BLACKDIAMOND49FLIVE_READER_ROLE_ARN` is not a key yet. After the release the count is **65**. (Nine keys end in `_READER_ROLE_ARN`: the six vendor keys plus three others; the release adds the tenth.) |
| `tools_list_before` (`W/ap28_toolslist.json`) | registry count **103**; `tools/list` to a master_admin stand-in **103**; health 200. |
| `iam get-role gateway-49f-blackdiamond-live-read-role` | resolves. Trust: `opal-gateway-role`. One inline policy `gateway-49f-blackdiamond-live-read-policy`. |
| simulate, one resource per call, on that role | `s3:GetObject` on `opal-data-bd/silver/{unrealized,transactions,allocations,fees}/<date>.parquet`: **allowed** x4; `s3:ListBucket` with prefix `silver/unrealized/`: allowed; controls `bronze/` and `silver_legacy/`: **explicitDeny** x2; bucket `opal-data-bd` exists (`head-bucket`). A simulation proves the pattern, not the served read: the served read is Phase B's. |

## 1. CTO half -- the `diff` (what changes, by file)

Cut at the live ref; every file below is taken from the earlier trunk `066649b10f`, and `858e927558` changed none of them (the only gateway change since is `harvest_research.py`, which is not in the take, plus the registry file the prelude carries), and each live-to-trunk hunk is attributed to a named order (`W/ap28_attr.json`: 17 app files, 0 unattributable hunks). The seams are enumerated (`W/ap28_seams.out`: 66 distinct seams over 169 importer edges; the six STOP-class edges were checked and are order-only or pre-existing, see `W/AP28_PHASE_A_NOTES.md`).

| file | change | order |
|---|---|---|
| `app/client_core.py`, `app/client_role.py` | a catalog row resolved by `address`; the real prefix read in the row's own bucket; flat `<date>.parquet` and `date=<d>/` both accepted; the `-live` tools routed to key `blackdiamond49flive` / env `BLACKDIAMOND49FLIVE_READER_ROLE_ARN`, unset answers `live_role_unset` and reads nothing | OG-en-12 |
| `app/client_adapter_{bd49f,bdcottonwood,commonwealth,orion,schwab,smartx}.py` | holdings rows gain `weight_unit`, `currency`, `currency_basis` (orion's unit stays null) | OG-en-4 |
| `app/news_typed.py` | `coverage_floor` beside an empty news answer | OG-en-5 |
| `app/harvest_press.py` | `trading_days_behind_t1` on the chatter answer | OG-en-6 |
| `app/data_entitlement.py`, `app/config.py`, `app/server.py` | the Muse client narrowing, INERT unless `MUSE_CLIENT_ID` is set; the `/teams/poll` route | OG-en-8 |
| `app/query_v0.py`, `app/graphql_plumbing/catalog_gate.py` | a key with no catalog row answers 404 (it answered 200 with an error body) | OG-en-9 |
| `app/ratelimit.py`, `app/server.py`, `app/audit.py` | a 429 writes one audit row `event=gw_ratelimit` with the hashed `by_client` split; **the 120 per 60 s limit is unchanged** | OG-en-10 |
| `app/refs/DATA_CATALOG.yaml` | taken WHOLE at blob `b81c48aa3c6c0ce3e79628e55cc5e8501f73dcf3` (A1: MI's one emitted file; four NEW live 49F Black Diamond rows with `address` and `read_tool`, eight legacy rows re-bucketed) | NFRA_MCPINDEX MX-c-26 |
| tests | 4 modified, 9 new test files, all named by the orders' `<paths>`; 9 named paths do not exist at trunk (`W/ap28_take.json`) | en-4/5/6/8/9/10/12, ts-1 |
| `deploy-to-ec2.sh` (the hunk, against the LIVE script) | 3 changed lines: `READER_ARN_BD49FLIVE="$(_vr_arn gateway-49f-blackdiamond-live-read-role)"` after the SMARTX line; `BLACKDIAMOND49FLIVE_READER_ROLE_ARN=%s\n` after `SMARTX_READER_ROLE_ARN=%s\n` in the one env printf; `"${READER_ARN_BD49FLIVE}"` after `"${READER_ARN_SMARTX}"` in its argument list. Every other slot is unmoved; the existing `_vr_arn` helper refuses the deploy with no upload if the role does not resolve. | order step 2 |
| `infra/aws/ec2/EC2_MANIFEST.json` | `services.opal-gateway.mcportal_commit` `c66ca82952` to `59e802a418`, NOTHING else (one-value text replacement; parent `c66ca82952` is the pin on the host now; origin DEV holds `59e802a418`) | MP-pf-11 |
| **naming-gate prelude (A3), carried below the release tip (`2dc919cf26`)** | `infra/logic/registry/catalog_fork_keys.json` and `infra/logic/registry/legacy_addresses.json`, byte-equal to `858e927558` (blob `1591eb3a55` and `07581da3da`). They do not ship (the archive carries `app`, `deploy`, `lib`, the dashboard). Needed because the ENFORCE gate reads its registry with `git show HEAD:` only. Landed under the audited `GIT_COMMIT_AUTHOR_OVERRIDE=PLATFORM_LOGIC_DOCS` on the prelude commit only; the release commit is under `CLOUD_OPS_OR_ETL`. The four entry files are dropped (A3). | A2, A3 |

NOT in the release: `app/tools.py`, `app/destructive_ops.py` (order-only differences from the base), `admin_people_access.py`, `family_depth.py`, `refs/silver_families.json`, the yearinreview files, `integrations/opal_discover/integration.py`, `app/refs/partner_roster.json` and `scopes.json` (the deploy script stages them from the repo; never committed, row Z-S161). No Terraform, no IAM.

Gate state to read: the release commit `bf9d23b518` EXITED 0 under ENFORCE: `NAMING-GATE: WARN 46 graded`, **0 REFUSE**, `CATALOG-EXEMPT admitted=12 refused=0 new_via_registry=8`. The 46 graded lines: 12 REGISTRY-HELD, 8 CONFORMANT, 10 OUT-OF-PATTERN (existing, WARN), 4 ALIAS (existing, WARN), **4 RAISE-EXISTING** (`blackdiamond/49f-live/silver/{allocations,fees,transactions,unrealized}/` at `DATA_CATALOG.yaml` lines 3372, 3437, 3503, 3570: 'pre-LGIC key; conformance via its migration project, Rule 30') and **8 RAISE** ('rule or registry defect': the eight `blackdiamond/49financial/silver_legacy/<table>/` prefixes at lines 4110, 4182, 4478, 4554, 4626, 4771, 4842, 4916, admitted as registry-held but still printed). The durable fix for the tier grammar is the CTO's and the CRO's, not this release's. (Earlier attempts, rows Z-S301 and Z-S303, refused the four entry files and the 49f-live literals; A3 ruled the route that cleared them.)

## 2. COO half -- the `widening`, stated plainly

- **NO new IAM. NO tool added or removed** (registry 103 before and after; `tools.py` untouched).
- **The four 49F Black Diamond `-live` tools serve their first real answer.** Measured (OG-en-11, row Z-S293): today `client_get_holdings`, `_transactions`, `_allocation` and `_fees` answer `absent_reason no_catalog_row` for lack of a catalog row and read nothing. After the release they read `opal-data-bd/silver/{unrealized,transactions,allocations,fees}/` (flat dated files) through the DEDICATED role `gateway-49f-blackdiamond-live-read-role`, **to master_admin only** (the data-grant class, OG-ad-1). The role's grant is exactly those four prefixes (simulated above), and it is live from OG-ap-29.
- Answer rows gain `weight_unit`, `currency`, `currency_basis` (client positions), `coverage_floor` (news), `trading_days_behind_t1` (chatter).
- A key with no catalog row answers HTTP 404 (it answered 200 with an error body).
- A 429 writes an audit row with the hashed `by_client` split and no raw identity. The limit is not changed (CTO msg 35000).
- The Muse client narrowing is INERT: `MUSE_CLIENT_ID` is not set; the act that sets it is a later, separate ask.
- The mcportal pin moves to `59e802a418` (two CSS and test files, no gateway code).

## 3. COO half -- the `order` of acts

Phase B, on the issuer's GO naming all three halves signed at `release_sha`: (1) ledger `nfra-oplgtw-gateway-release-batch2`, entry AND sentinel first; (2) ONE deploy from `C:/tmp/og-rel-batch2` through `safe-ec2-deploy.sh` with `DEPLOY_BASE_REF=<base_sha>` under the stale-base guard (the declared base equals the live ref, so a prelude below the tip is legal), no `HALT_OVERRIDE`; (3) the served read through the installed code and the public endpoint (`W/CODE2_SERVED.json`: one real call per arm by an Opal stand-in); (4) the issuer's `OG-en-11` re-run. Before (2) the overlay files the naming gate needed in the release tree are restored.

## 4. CVO half -- `both branches` (role unset / set; admin / non-admin)

- Role unset (`BLACKDIAMOND49FLIVE_READER_ROLE_ARN` absent): the four tools answer `live_role_unset` and read nothing (stated by the order and the code; `test_og_en12` is among the 167 taken tests that pass in the re-cut tree; the served read in Phase B is the proof).
- Role set, a non-admin principal: refused (the data-grant class), zero S3 reads; Phase B counts the reads on a counter.
- Role set, master_admin: served from `opal-data-bd`, rows above 0, the session's assumed-role name `gateway-49f-blackdiamond-live-read-role` (names only).

## 5. COO half -- the `rollback`

Redeploy the base (`d14445961d`) through the same wrapper; the manifest pin returns with it. The release changes no IAM and writes nothing to any bucket or table, so there is no data to restore.
## 6. COO half -- the `triggers` (any one: redeploy the base and file an ARMED row naming `2.0.0_SA_COO~O`)

Health not 200 within 60 s; a tool of the 27 that answered before not answering; the `.env` key count not 65 (64 now); the `tools/list` count changing (103 to a master_admin stand-in).

## 7. CVO half -- the CVO's condition on OG-ap-29

The routing change (the `-live` tools to the key `blackdiamond49flive`) ships in THIS release, as the CVO required: `app/client_role.py` and `app/client_core.py` (OG-en-12), the seventh env key and the deploy hunk above.

## 8. Evidence index

`W/ap28_attr.json` (hunk attribution), `W/ap28_seams.out` (seams), `W/ap28_take.json`, `W/ap28_tests.out` (169 taken tests run, 167 pass, 2 fail identically at the live ref and are carried by name: `test_og_gt8::test_oggt8_ac03_deploy_stages_lib`, `test_data_entitlement_guard::test_ogz1_ac08`), `W/ap28_hostshape.json` (18 of 18 modules import with 0 reads), `W/ap28_host_md5.json`, `W/ap28_toolslist.json`, `W/AP28_PHASE_A_NOTES.md`. Untracked test support (not committed): the two `app/refs` copies at trunk bytes and the `~109`, `~110` deliverable files the gp1/gf1/ts1 tests read.

## Signatures (to be filled by the halves, at the final ask sha256)

CTO ___ . COO ___ . CVO ___ .
