# NEVER-WIDEN ASK -- OG-ap-23: the code batch release -- 27 READ tools and the six vendor reader keys, one deploy

To: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O` and `3.0.0_SA_CVO~Z` -- THREE halves, each signed on its own.
From: `0.7.0_AE_CloudOps~Z`. Phase A of `NFRA_OPLGTW.TO-OG-ap-23` as amended through **A3** (`be681541ec`); re-GO msg 34751, rulings msgs 34755 and 34770.
**NOTHING IS DEPLOYED AND NOTHING IS APPLIED.** 191 taken and deploy-script tests pass; 11 more fail, and fail identically on the base script (section 9). The release commit grades 0 REFUSE in ENFORCE.
This ask **replaces** the one at sha256 `2f1a1499a109` (release `5939062746`), which stated two gaps; A3 ruled both, and this cut carries the ruling.

| | |
|---|---|
| **release** | `56c0f8ce1d602b309abaf3f25dd28974c7736d39` on `rel-nfra-oplgtw-code-a3` (worktree `C:/tmp/og-rel-code`), its single parent the live ref |
| **base** | `d577e0e7297b3ecba183023d8374855a93f148a7` -- OG-ap-21's release, live since 2026-10-16T00:09:44Z; the manifest, the S3 `git-ref` and a host md5 walk (123 of 123 equal) all name it |
| **taken from** | `box/sitez` pinned at `396b0690d5760a9a773610fd31e7182bd8883b03` |
| **mcportal bundle** | `090b9cdc85ce3463e73915e68b44f4c21053a71c` (origin DEV; descends from `421f8fbe84`; live is `17dcbb28624e`) |
| **ledger** | `nfra-oplgtw-gateway-release-code` (Phase B; **not opened**) |
| **record** | `W/ap23_release.json`; `ap23.AC1` PASS, exit 0 (run from the shared tree, see section 9) |
| **superseded cut** | `5939062746` stays on branch `rel-nfra-oplgtw-code` as the A2 record; the worktree's HEAD is now `rel-nfra-oplgtw-code-a3` |

## 0. READ THIS FIRST: what A3 changed, and the one thing a half should still weigh

**Gap 1, closed in this cut.** The deploy script now writes the six vendor reader keys into the `.env` it rebuilds:
`BLACKDIAMOND49F_`, `BLACKDIAMONDCOTTONWOOD_`, `ORION_`, `ECLIPSE_`, `COMMONWEALTH_` and `SMARTX_READER_ROLE_ARN`.
Before it, the host held 58 `.env` keys and none of the six (measured, names only, `W/ap23_host_env_key_names.txt`),
so the client tools would have stayed on the instance role. Each ARN is **read from IAM, never typed**: the script
resolves the account (`sts get-caller-identity`), then runs `iam get-role` for each of the six names and compares the
returned ARN to `arn:aws:iam::<account>:role/<name>`; **any mismatch refuses the deploy with no upload.** Both calls are
read-only and run before the upload. A role ARN is not a secret and no value is printed.

**Gap 2, ruled to a separate cell.** `OG-ap-26` moves the `etf-classifications` GetItem grant from the instance role to
`gateway-global-internal-reader-role` (the identity `mdpf_classification.py` actually reads as) and removes it from the
instance role. All three of its halves are signed. **Phase B's precondition is now `ap26.AC2.sh` PASS**, and this
release still ships `mdpf_get_security_classification`.

**What a half should still weigh: this release is not dormant.** With Gap 1 closed the client tools really do assume the
six roles, so the widening in section 3 takes effect at the deploy, not at a later release. Nothing is shipped
dormant (the ruling said so).

## 1. The `diff`, by file -- 44 files, base to release

Counts: **31 added, 13 modified, 0 deleted.** Nothing under `infra/aws/terraform/`; no `.tf` file differs
(AC1: terraform files differing 0). Files outside the batch set: 0.

| file | how taken |
|---|---|
| `app/client_core.py`, `app/client_role.py` | WHOLE (new at this base) |
| `app/client_adapter_{schwab,bd49f,orion,eclipse,bdcottonwood,smartx,commonwealth}.py` | WHOLE (new) |
| `app/etfs_rivals.py`, `app/etfs_rivals_flow.py`, `app/etfs_silver.py` | WHOLE (new) |
| `app/portal_served.py`, `app/portal_json_served.py`, `app/mdpf_classification.py` | WHOLE (new) |
| `app/admin_gateway_breakdown.py`, `app/admin_people.py`, `lib/opal_naming.py` | WHOLE (existing at the base, replaced by trunk's) |
| `app/tools.py` | BY HUNK: 5 import lines and the 27 `@mcp.tool()` registrations; nothing else moves |
| `app/destructive_ops.py`, `app/data_entitlement.py` | BY HUNK: the 27 names added to `SAFE_TOOLS` and `NATIVE_TOOLS`, nothing else |
| `tests/test_entitlement_admin.py`, `tests/test_data_entitlement_family.py` | BY HUNK: pins **95 to 122** and **86 to 113** (3 spots) |
| `app/integrations/portal_index/integration.py` | the MX-c-22 hunk, which is **all** that differs base to trunk (checked, not assumed) |
| `deploy-to-ec2.sh` | **two hunks**, 30 lines added and 1 changed, below |
| `infra/aws/ec2/EC2_MANIFEST.json` | ONE field: `services.opal-gateway.mcportal_commit` `17dcbb28624e` to `090b9cdc85ce` |
| 16 added test files | WHOLE: `test_og_{cl1..7,ch1,rv1,rv2,gp1,gf1,sv1,sv2,ac2}` and `test_positioning_extension`; `test_admin_gateway_breakdown` and `test_admin_people` are modified, taken WHOLE |

**The `deploy-to-ec2.sh` hunks.**
(a) *Staging:* a presence check, three `cp` lines, and the two `app/refs/` files named on the `tar` line. It ships
`lib/opal_naming.py`, `data/mdpf/config/partner_roster.json` and `infra/logic/registry/scopes.json` into the bundle from their
repo sources and refuses with no upload if a source is absent. The tar-line edit is one thing more than the order's staging
sentence names; without it the staged files never reach the host.
(b) *Reader keys (A3):* the account lookup, a six-call role resolution that refuses the deploy on any mismatch, six `%s` keys in the
`.env` `printf` and six arguments. **They sit immediately before the two `ADVI_*` roots, not at the end**, because
`test_ogab1_ac03` and `test_ogab2_ac03` pin the market-update argument second-to-last and the fee-statement argument last
(my first placement appended them and broke both tests; the printf now reads 28 slots to 28 arguments).
Nothing else in the `.env` `printf` changes.

**Not committed as data:** `app/refs/partner_roster.json` and `app/refs/scopes.json` (AC1: data copies committed 0).
Phase B proves both by host md5 against trunk's blobs.

### Not taken, named rather than left for a half to find

1. **Trunk's `OG-bd-3` hunks in `data_entitlement.py`** (the `decide()` tier branch and the two `tier = ...` lines): a behaviour
   change at the entitlement chokepoint, not a name or a pin. **Live behaviour there is unchanged.**
2. **Trunk's `OG-db-1` preflight and its `.env` `printf` re-order in `deploy-to-ec2.sh`.**
3. **The re-order of `harvest_get_published_analysis`** in `tools.py`, `destructive_ops.py` and `data_entitlement.py`
   (cosmetic; the function and its two list entries stay where the base has them).
4. `app/family_depth.py`, `refs/silver_families.json`, the yearinreview files, `admin_people_access.py`:
   not imported by anything taken (seam enumeration, 61 distinct seams, **0 STOP**, `W/ap23_seams_r2.out`).
   `test_og_cd1.py` is out of scope (it is not one of the order's cells) and is the file that imports `family_depth`.

## 2. The `tools` -- 27 added, every one class READ

Registry on the host **76 to 103**; repo pins 122 and 113. Each tool is in `SAFE_TOOLS` (27 of 27) and `NATIVE_TOOLS`
(27 of 27), which AC1 recomputes. Every tool admits an Opal principal first (`typed_scope.admit_scope`) and
refuses a non-Opal one **before** any S3, DynamoDB or catalog read.

| group | tools | reads as | firm fence | `refused` arm |
|---|---|---|---|---|
| rival funds (10) | `etfs_get_peer_group_members`, `etfs_get_rival_fund_holdings`, `etfs_who_holds`, `etfs_get_security_reference`, `etfs_get_coverage`, `etfs_get_fund_trades`, `etfs_get_fund_flows`, `etfs_compare_peers`, `etfs_get_research_notes`, `etfs_get_rival_page_status` | the internal reader role, `opal-data-etfs/rivalfunds/etfs/gold/*` and `.../platinum/page/*` (granted by OG-ap-20, live) | none: fund data, not client data | non-Opal: refusal, 0 reads |
| client (5) | `client_resolve_account`, `client_get_holdings`, `client_get_transactions`, `client_get_allocation`, `client_get_fees` | the **vendor read role**, now keyed in `.env` | **yes**: `firm` must be canonical (`49financial`, `cottonwood`, `inflection`, or an alias) or `firm_not_canonical`, 0 reads; one master segment per firm where the vendor splits | non-Opal: refusal, 0 reads. Also `no_catalog_row`, `window_too_long` (over 396 days), `registry_unavailable` (0 reads) |
| silver etfs (3) | `etfs_get_new_securities`, `etfs_get_fund_bloomberg_characteristics`, `etfs_get_fund_snapshot` | the internal reader role, `opal-data-etfs/silver/*` | none | non-Opal: refusal, 0 reads |
| portfolio (1) | `mdpf_get_model_composition` | the internal reader role, served portfolio tables | by `scope` argument | non-Opal: refusal, 0 reads |
| json-served (7) | `portal_get_correlations`, `portal_get_etf_returns`, `portal_get_factor_tilts`, `portal_get_model_portfolio_timeseries`, `portal_get_peer_performance`, `portal_get_trending`, `portal_get_cma_assumptions` | the internal reader role, `opal-data-portal-v2/json/*` (the gateway role's `queryv0` grant holds `json/*` and `platinum/*`) | none | non-Opal: refusal, 0 reads |
| classification (1) | `mdpf_get_security_classification` | the internal reader role's DynamoDB client; the GetItem grant is `OG-ap-26`'s | none | non-Opal: refusal, 0 reads |

The client tools return one envelope (`as_of`, `partition_date`, `source_keys`, `denominator`, `absent_reason`,
`platform_label`, `platform_label_source`, `label_claim`, `freshness_td`) projected to 50 KB. A resolve asks **every**
adapter that holds the firm and merges, and never picks one; an account is referenced as `****<last4>/<vendor>/<alias>`,
never a full number.

## 3. The `widening`, stated plainly

**No new IAM in this release.** No Terraform, no apply, no catalog edit, no object or item written anywhere.
What changes is what the gateway can do with grants that already exist:

- **The client tools turn the six live vendor read roles from unused to used**, each through an assumed role
  scoped to its vendor and firm prefixes, **and the gateway can now return client account-level data (holdings,
  transactions, fees, allocation) to named Opal principals.** Which tool uses which role, and the fence:

| role | vendor, firm | adapter | env key this release writes |
|---|---|---|---|
| `gateway-49f-blackdiamond-read-role` | Black Diamond, `49financial` | `client_adapter_bd49f` | `BLACKDIAMOND49F_READER_ROLE_ARN` |
| `gateway-cot-blackdiamond-read-role` | Black Diamond, `cottonwood` | `client_adapter_bdcottonwood` | `BLACKDIAMONDCOTTONWOOD_READER_ROLE_ARN` |
| `gateway-inf-orion-read-role` | Orion, `inflection` | `client_adapter_orion` | `ORION_READER_ROLE_ARN` |
| `gateway-inf-eclipse-read-role` | Eclipse, `inflection` | `client_adapter_eclipse` | `ECLIPSE_READER_ROLE_ARN` |
| `gateway-cot-commonwealth-read-role` | Commonwealth, `cottonwood` | `client_adapter_commonwealth` | `COMMONWEALTH_READER_ROLE_ARN` |
| `gateway-smartx-read-role` | SmartX, `49financial` | `client_adapter_smartx` | `SMARTX_READER_ROLE_ARN` |

  The six trust policies were read today: each names `opal-gateway-role` as the only principal, `sts:AssumeRole`, **no
  condition**, so no ExternalId is needed. Schwab (`client_adapter_schwab`, firm `49financial`) uses the existing
  `SCHWAB_READER_ROLE_ARN`, already set; it is not one of the six.
- **The 22 non-client tools** read prefixes and tables the internal reader role already holds (OG-ap-20's etfs grant, the
  `json/*` grant, the news tables); they add readers, not reach. `mdpf_get_security_classification` adds the one table read
  that `OG-ap-26` grants to that role.
- Never widened: no write or `Scan` verb is reachable; no role gains a statement from this release; the six trust policies are unchanged.

## 4. The `order` of acts (Phase B, only on the issuer's GO naming all three halves signed at `release_sha`)

1. PRECONDITION: **`ap26.AC2` PASS** (the classification policy reads back on `gateway-global-internal-reader-role` and is gone
   from the instance role). Not met = STOP and report.
2. Ledger `nfra-oplgtw-gateway-release-code`, **entry AND sentinel first**.
3. ONE deploy from `C:/tmp/og-rel-code` through `safe-ec2-deploy.sh` with `DEPLOY_BASE_REF=d577e0e7297b3ecba183023d8374855a93f148a7`,
   the A1 guard (HEAD = the full signed `release_sha`, parent = the live `deployed_commit`, no other release in flight), no `HALT_OVERRIDE`.
4. The served read through the **installed** code, host and public endpoint (60 s ALB).
5. The CVO's conditions (section 8), then the standing clauses and the close.

## 5. `Both branches` of a call

| branch | what happens |
|---|---|
| **refused** | non-Opal principal, non-canonical firm, no catalog row, window over 13 months, or registry unreadable: every arm fires BEFORE any S3, DynamoDB or catalog read. **Zero reads**: the host-shaped check, with `boto3.client` replaced by a counter that refuses, recorded 0 reads in both arms (with and without `lib/opal_naming.py`; without it every adapter's firm binding answers `registry_unavailable`). |
| **admitted** | an Opal principal: capped (50 KB), projected to the envelope, fenced by firm (client tools), reading one partition per call. |

**The classification tool's admitted branch carries one more fact the served read must SHOW (CVO condition on `OG-ap-26`, msg 34770).**
For `mdpf_get_security_classification`, `W/CODE_SERVED.json` records `via_internal_reader: true` beside `opal_served`,
`non_opal_refused` and `reads_on_refusal`. The evidence is the assumed-role identity of the session that made the `get_item`
(`sts get-caller-identity` ARN of the DynamoDB client's session, names only, no credential), which must read
`assumed-role/gateway-global-internal-reader-role/...` and not `assumed-role/opal-gateway-role/...`.

## 6. The `rollback`

1. **The code**: redeploy the base `d577e0e7297b3ecba183023d8374855a93f148a7`, the live commit and this release's parent.
   Nothing in this release is irreversible and no IAM moves, so a binary rollback undoes the whole act.
2. The six `.env` keys leave with the redeploy (the `.env` is rebuilt at each deploy); the host returns to 58 keys.

## 7. The `triggers` Phase B reads back

| trigger | expected |
|---|---|
| `/health` | serving |
| registry on the host | 76 to **103** |
| repo pin | 95 to **122**, `non_data` 86 to **113** |
| host `.env` key names | 58 to **64**: the six names above added, nothing removed (names only, over SSM, no value printed) |
| host md5 | equal to the release blobs across `app/`, `deploy/`, `lib/`, **and** `app/refs/partner_roster.json`, `app/refs/scopes.json` equal to trunk's blobs `3d309b267e69` and `fd17416171b2` |
| per tool | 27 of 27: an Opal stand-in is served an enveloped answer, a non-Opal is refused with 0 reads |
| classification | `via_internal_reader: true` (section 5) |
| IAM | no change from this release; the only movement in the window is `OG-ap-26`'s own |

Any trigger red: redeploy the base and file an ARMED row naming `2.0.0_SA_COO~O`.

## 8. The CVO's two conditions from `OG-ap-24`, and where Phase B meets them

- **C1: one REAL AssumeRole of a vendor read role by the gateway role** (a simulate cannot see a trust). Step 5, from the host, one
  `sts:AssumeRole` of `gateway-smartx-read-role`; the call is recorded, no credential printed. It also stands as evidence beside the
  keys: `reader_env_keys_present: 6` (names read over SSM) and the six `iam get-role` resolutions the deploy script made before the upload.
- **C2: SmartX counts as firm-safe only after the two-firm negative arm.** Step 5, through the installed `client_*` tools: a SmartX read
  for firm A returns only firm A's rows, and the same read naming the other firm refuses or returns only that firm's rows, never A's
  (counts only). **Met by the installed keys**: with `SMARTX_READER_ROLE_ARN` written, the read goes through the assumed role.

## 9. Readings a half should have that are not about the diff

- **How the release tree ran the gates.** It is cut on a base older than the gate: I laid trunk's `naming-gate.py`,
  `naming-apply-gate.py`, `infra/logic/`, `NAMING_SCHEMA.json`, `DIRECTIVES.yaml` and the `lib/opal_naming_*.py` siblings over it
  as **uncommitted** files (`W/ap23_gate_overlay_manifest.txt`), because the base-era gate cannot load the newer registry
  (`KeyError: 'interval_form'`). With them: `ng2.AC2` PASS (0 REFUSE, 10 RULED), `ng3.AC1` PASS (0 REFUSE, 11 RULED), and the release
  commit itself `NAMING-GATE: WARN 14 graded`, 0 REFUSE. None of the overlay is in the commit. The deploy tree keeps trunk's
  `scopes.json` and `partner_roster.json` on disk because they are the bundle sources.
- **Eleven tests fail on the BASE deploy script as well**, so they are not this release's: `test_schwab_host_inputs.py` (3: one is a stale
  `%s` count of 19 against 22 on the base; I did not read the other two), `test_deploy_base_guard.py` (8: the two I read fail on an
  unreadable `meeting_allowlist.json` in the test sandbox; I did not read the other six). I ran the six test files that read the script against the base script and against this one: 11 and 11.
  The two that this release's first hunk placement would have added (`test_ogab1_ac03`, `test_ogab2_ac03`) pass now.
- **A first attempt at this cut was REFUSED by the gate** (23 lines; row `Z-S161`). A2 moved the roster and the registry copy out
  of the commit and `OG-ng-3` ruled the other three lines.
- **AC1 is run from the shared tree, not the release tree**: its `live` is read from `HEAD`'s `EC2_MANIFEST.json`, and the release
  branch's own manifest baseline is older (`daa56d81ac`), so run there it would compare against a value that was never live here.
- **Test support kept out of the commit:** three worker evidence files and the check scripts are copied into the tree untracked.
- `tools.py` carries 7 lines with non-ASCII characters (commit-gate WARN, not blocking); they come from trunk's registrations.
- **The record commits are not pushed**: only the integrator may push `box/sitez`; the ask, `4ddb577912` and the OG-ap-21 proof are LOCAL.

## 10. The CTO half -- `1.0.0_SA_CTO~Z`

Signs: sections 1 and 2 (the `diff` and the `tools`) and the not-taken list. The CTO's own gate condition is met on the release commit
(0 REFUSE in ENFORCE). **Asked of this half in particular:** that the second `deploy-to-ec2.sh` hunk (the six reader keys and their
role resolution) is inside the amended A3 hunk as the COO wrote it, and the tar-line edit of the first.

## 11. The COO half -- `2.0.0_SA_COO~O`

Signs: sections 4 to 7 (the `order`, `both branches`, the `rollback`, the `triggers`). Your rulings are carried: Gap 1 is closed in the
hunk, Gap 2 is `OG-ap-26`'s and gates Phase B, nothing ships dormant, and the served read adds `via_internal_reader`.

## 12. The CVO half -- `3.0.0_SA_CVO~Z`

Signs: sections 3 and 8 (the `widening` and the two conditions). **Asked of this half in particular:** that the widening it signs is
live at the deploy (the keys are written), and that C1 and C2 are met in Phase B by the installed keys and the real AssumeRole.
