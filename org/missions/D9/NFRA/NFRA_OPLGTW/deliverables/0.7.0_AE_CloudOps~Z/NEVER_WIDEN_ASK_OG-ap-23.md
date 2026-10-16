# NEVER-WIDEN ASK -- OG-ap-23: the code batch release -- 27 READ tools, one deploy

To: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O` and `3.0.0_SA_CVO~Z` -- THREE halves, each signed on its own.
From: `0.7.0_AE_CloudOps~Z`. Phase A of `NFRA_OPLGTW.TO-OG-ap-23` as amended through A2 (`e8b666bc17`), re-GO msg 34751.
**NOTHING IS DEPLOYED AND NOTHING IS APPLIED.** 172 of 172 taken tests pass; the release commit grades 0 REFUSE in ENFORCE.

| | |
|---|---|
| **release** | `59390627467423d84ff0e5fc8bb9498751cac072` on `rel-nfra-oplgtw-code` (worktree `C:/tmp/og-rel-code`) |
| **base** | `d577e0e7297b3ecba183023d8374855a93f148a7` -- OG-ap-21's release, live since 2026-10-16T00:09:44Z; the manifest, the S3 `git-ref` and a host md5 walk (123 of 123 equal) all name it |
| **taken from** | `box/sitez` pinned at `396b0690d5760a9a773610fd31e7182bd8883b03` |
| **mcportal bundle** | `090b9cdc85ce3463e73915e68b44f4c21053a71c` (origin DEV; descends from `421f8fbe84`; live is `17dcbb28624e`) |
| **ledger** | `nfra-oplgtw-gateway-release-code` (Phase B; **not opened**) |
| **record** | `W/ap23_release.json`; AC1 PASS, exit 0 (run from the shared tree, see section 9) |

## 0. READ THIS FIRST: two measured gaps between what this release says and what the host will do

Both are about the **installed** behaviour, not the diff, and both change what section 3 can honestly claim.
I did not fix either: each needs a ruling that is not mine, and the order bounds this release to code only.

**GAP 1 -- the vendor read roles stay UNUSED on the host as this release is cut.** The client tools assume a
vendor's role from the env key `<VENDOR>_READER_ROLE_ARN` (`app/client_role.py`, `role_env_name`); a client
whose key is unset falls to `default_client()`, the instance role's own credentials (`client_for`).
The keys the six roles need are `BLACKDIAMOND49F_`, `BLACKDIAMONDCOTTONWOOD_`, `ORION_`, `ECLIPSE_`,
`COMMONWEALTH_` and `SMARTX_READER_ROLE_ARN`. **MEASURED, names only, no value read:** the live host's
`.env` holds 58 keys and the only reader keys among them are `BLACKDIAMOND_READER_ROLE_ARN`,
`BLACKDIAMOND_READER_EXTERNAL_ID`, `FIRM_ROLE_ARNS`, `INTERNAL_READER_ROLE_ARN`, `SCHWAB_CATALOG_ROLE_ARN` and
`SCHWAB_READER_ROLE_ARN` (`W/ap23_host_env_key_names.txt`). **None of the six is there**, and neither the base
nor trunk `deploy-to-ec2.sh` writes one (the `.env` is rebuilt by one `printf` at each deploy; the trunk
`printf` differs from the base only by a re-order). So after this deploy a client read for those vendors runs as
the instance role (I did not read whether it holds any grant on the vendor prefixes; the six roles exist to carry them, so a read as the instance role is expected to be denied), and CVO condition C1 (a real AssumeRole of a vendor
role) and C2 (the SmartX two-firm arm through the installed tools) cannot be shown by the installed code.
The six trust policies are the same shape: principal `opal-gateway-role`, `sts:AssumeRole`, **no condition**
(so no ExternalId is needed).

**GAP 2 -- `mdpf_get_security_classification` reads as the internal reader role, and OG-ap-25's grant is on the
instance role.** `app/mdpf_classification.py` takes its DynamoDB client from `internal_role.dynamodb_client()`
whenever `INTERNAL_READER_ROLE_ARN` is set, and it is set on the host. **MEASURED:**
`gateway-global-etf-classification-read-policy` reads back on `opal-gateway-role` (GetItem on the
`etf-classifications` table ARN, 1 statement) and is **absent** on `gateway-global-internal-reader-role`
(NoSuchEntity). An assumed-role session holds only the assumed role's policies, so the call is expected to be
denied. `ap25.AC2` PASSES because it simulates the instance role; that is the right question for a grant on the
instance role and the wrong one for this code path. Phase B's per-tool served read would show it as the one tool of
27 that does not serve.

**What I ask a half to decide before signing, and what I recommend.** (1) Gap 1: amend the `deploy-to-ec2.sh`
hunk by six `printf` keys carrying the six role ARNs (role ARNs, not secrets; `arn:aws:iam::313476888478:role/<name>`
for the six names in section 3); this widens nothing beyond turning the signed roles from unused to used, which
section 3 already states. (2) Gap 2: a one-policy grant on the internal reader role, as a separate cell, **or**
point the module at the instance role -- either is a change I cannot make inside this order. If neither lands
before the halves sign, the release is still safe to sign as a **dormant** release: Gap 1 makes the client
tools fail closed and Gap 2 makes one tool refuse; neither can return data a principal should not see.
Signing it dormant means C1 and C2 stay owed, not met.

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
| `deploy-to-ec2.sh` | the staging hunk only: a presence check, three `cp` lines and two names on the `tar` line |
| `infra/aws/ec2/EC2_MANIFEST.json` | ONE field: `services.opal-gateway.mcportal_commit` `17dcbb28624e` to `090b9cdc85ce` |
| 16 added test files | WHOLE: `test_og_{cl1..7,ch1,rv1,rv2,gp1,gf1,sv1,sv2,ac2}` and `test_positioning_extension`; `test_admin_gateway_breakdown` and `test_admin_people` are modified, taken WHOLE |

**Not committed as data:** `app/refs/partner_roster.json` and `app/refs/scopes.json` (AC1: data copies committed 0).
The deploy script stages `lib/opal_naming.py`, `data/mdpf/config/partner_roster.json` and
`infra/logic/registry/scopes.json` into the bundle from their repo sources, refuses with no upload if a source
is absent, and ships the two `app/refs/` files by naming them on the `tar` line. **That tar-line edit is part of
the hunk and is one thing more than the order's sentence names**: without it the staged files never reach the
host. Phase B proves both by host md5 against trunk's blobs.

### Not taken, named rather than left for a half to find

1. **Trunk's `OG-bd-3` hunks in `data_entitlement.py`** (the `decide()` tier branch and the two `tier = ...`
   lines): a behaviour change at the entitlement chokepoint, not a name or a pin. **Live behaviour there is unchanged.**
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
| client (5) | `client_resolve_account`, `client_get_holdings`, `client_get_transactions`, `client_get_allocation`, `client_get_fees` | the **vendor read role** (Gap 1) | **yes**: `firm` must be canonical (`49financial`, `cottonwood`, `inflection`, or an alias) or `firm_not_canonical`, 0 reads; one master segment per firm where the vendor splits | non-Opal: refusal, 0 reads. Also `no_catalog_row`, `window_too_long` (over 396 days), `registry_unavailable` (0 reads) |
| silver etfs (3) | `etfs_get_new_securities`, `etfs_get_fund_bloomberg_characteristics`, `etfs_get_fund_snapshot` | the internal reader role, `opal-data-etfs/silver/*` | none | non-Opal: refusal, 0 reads |
| portfolio (1) | `mdpf_get_model_composition` | the internal reader role, served portfolio tables | by `scope` argument | non-Opal: refusal, 0 reads |
| json-served (7) | `portal_get_correlations`, `portal_get_etf_returns`, `portal_get_factor_tilts`, `portal_get_model_portfolio_timeseries`, `portal_get_peer_performance`, `portal_get_trending`, `portal_get_cma_assumptions` | the internal reader role, `opal-data-portal-v2/json/*` (the gateway role's `queryv0` grant already holds `json/*` and `platinum/*`) | none | non-Opal: refusal, 0 reads |
| classification (1) | `mdpf_get_security_classification` | the internal reader role's DynamoDB client (Gap 2) | none | non-Opal: refusal, 0 reads |

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

| role | vendor, firm | adapter | env key it needs |
|---|---|---|---|
| `gateway-49f-blackdiamond-read-role` | Black Diamond, `49financial` | `client_adapter_bd49f` | `BLACKDIAMOND49F_READER_ROLE_ARN` |
| `gateway-cot-blackdiamond-read-role` | Black Diamond, `cottonwood` | `client_adapter_bdcottonwood` | `BLACKDIAMONDCOTTONWOOD_READER_ROLE_ARN` |
| `gateway-inf-orion-read-role` | Orion, `inflection` | `client_adapter_orion` | `ORION_READER_ROLE_ARN` |
| `gateway-inf-eclipse-read-role` | Eclipse, `inflection` | `client_adapter_eclipse` | `ECLIPSE_READER_ROLE_ARN` |
| `gateway-cot-commonwealth-read-role` | Commonwealth, `cottonwood` | `client_adapter_commonwealth` | `COMMONWEALTH_READER_ROLE_ARN` |
| `gateway-smartx-read-role` | SmartX, `49financial` | `client_adapter_smartx` | `SMARTX_READER_ROLE_ARN` |

  Schwab (`client_adapter_schwab`, firm `49financial`) uses the existing `SCHWAB_READER_ROLE_ARN`, already set; it is
  not one of the six. **Today, with Gap 1 open, none of the six is used**: the widening in this bullet is real only
  once the keys exist.
- **The 22 non-client tools** read prefixes and tables the internal reader role already holds (OG-ap-20's etfs
  grant, the `json/*` grant, the news tables); they add readers, not reach.
- Never widened: no write or `Scan` verb is reachable; no role gains a statement; the six trust policies are unchanged.

## 4. The `order` of acts (Phase B, only on the issuer's GO naming all three halves signed at `release_sha`)

1. PRECONDITION: `ap25.AC2` PASS and the classification policy's **role** read back (Gap 2). Not met = STOP and report.
2. Ledger `nfra-oplgtw-gateway-release-code`, **entry AND sentinel first**.
3. ONE deploy from `C:/tmp/og-rel-code` through `safe-ec2-deploy.sh` with `DEPLOY_BASE_REF=d577e0e7297b3ecba183023d8374855a93f148a7`,
   the A1 guard (HEAD = the full signed `release_sha`, parent = the live `deployed_commit`, no other release in flight), no `HALT_OVERRIDE`.
4. The served read through the **installed** code, host and public endpoint (60 s ALB).
5. The CVO's two conditions (section 8), then the standing clauses and the close.

## 5. `Both branches` of a call

| branch | what happens |
|---|---|
| **refused** | non-Opal principal, non-canonical firm, no catalog row, window over 13 months, or registry unreadable: every arm fires BEFORE any S3, DynamoDB or catalog read. **Zero reads**: the host-shaped check, with `boto3.client` replaced by a counter that refuses, recorded 0 reads in both arms (with and without `lib/opal_naming.py`; without it every adapter's firm binding answers `registry_unavailable`). |
| **admitted** | an Opal principal: capped (50 KB), projected to the envelope, fenced by firm (client tools), reading one partition per call. |

## 6. The `rollback`

1. **The code**: redeploy the base `d577e0e7297b3ecba183023d8374855a93f148a7`, the live commit and this release's parent.
   Nothing in this release is irreversible and no IAM moves, so a binary rollback undoes the whole act.
2. If Gap 1 is amended, the six `.env` keys leave with the redeploy (the `.env` is rebuilt at each deploy).

## 7. The `triggers` Phase B reads back

| trigger | expected |
|---|---|
| `/health` | serving |
| registry on the host | 76 to **103** |
| repo pin | 95 to **122**, `non_data` 86 to **113** |
| host `.env` key names | 58 unchanged (64 if Gap 1 is amended) |
| host md5 | equal to the release blobs across `app/`, `deploy/`, `lib/`, **and** `app/refs/partner_roster.json`, `app/refs/scopes.json` equal to trunk's blobs `3d309b267e69` and `fd17416171b2` |
| per tool | 27 of 27: an Opal stand-in is served an enveloped answer, a non-Opal is refused with 0 reads |
| IAM | unchanged: 31 inline policies across the two gateway roles (25 on `opal-gateway-role`, 6 on the internal reader, read 2026-10-16), none added or removed |

Any trigger red: redeploy the base and file an ARMED row naming `2.0.0_SA_COO~O`.

## 8. The CVO's two conditions from `OG-ap-24`, and where Phase B meets them

- **C1: one REAL AssumeRole of a vendor read role by the gateway role** (a simulate cannot see a trust). Step 5, from the host,
  one `sts:AssumeRole` of `gateway-smartx-read-role`; the call is recorded, no credential printed. Needs nothing from Gap 1.
- **C2: SmartX counts as firm-safe only after the two-firm negative arm.** Step 5, through the installed `client_*` tools:
  a SmartX read for firm A returns only firm A's rows, and the same read naming the other firm refuses or returns only that
  firm's rows, never A's (counts only). **This needs Gap 1 closed** (`SMARTX_READER_ROLE_ARN` set); with it open the read
  cannot reach SmartX data and the arm is hollow.

## 9. Readings a half should have that are not about the diff

- **How the release tree ran the gates.** It is cut on a base older than the gate: I laid trunk's `naming-gate.py`,
  `naming-apply-gate.py`, `infra/logic/`, `NAMING_SCHEMA.json`, `DIRECTIVES.yaml` and the `lib/opal_naming_*.py` siblings over it
  as **uncommitted** files (`W/ap23_gate_overlay_manifest.txt`, 30 entries), because the base-era gate cannot load the newer
  registry (`KeyError: 'interval_form'`). With them: `ng2.AC2` PASS (0 REFUSE, 10 RULED), `ng3.AC1` PASS (0 REFUSE, 11 RULED), and
  the release commit itself `NAMING-GATE: WARN 14 graded`, 0 REFUSE. None of the overlay is in the commit. The deploy tree keeps
  trunk's `scopes.json` and `partner_roster.json` on disk because they are the bundle sources.
- **A first attempt at this cut was REFUSED by the gate** (23 lines in the committed roster, `portal_served.py` and `etfs_silver.py`;
  row `Z-S161`). A2 moved the roster and the registry copy out of the commit and `OG-ng-3` ruled the other three lines.
- **AC1 is run from the shared tree, not the release tree**: its `live` is read from `HEAD`'s `EC2_MANIFEST.json`, and the release
  branch's own manifest baseline is older (`daa56d81ac`), so run there it would compare against a value that was never live here.
- **Test support kept out of the commit:** three worker evidence files and the check scripts are copied into the tree untracked
  (`test_oggf1_ac01`, `test_oggp1_ac01`, `test_oggp1_ac04`, `test_ogsv1_ac01` read them); 172 pass with them.
- `tools.py` carries 7 lines with non-ASCII characters (commit-gate WARN, not blocking); they come from trunk's registrations.
- **The record commit is not pushed**: only the integrator may push `box/sitez`; `4ddb577912` and the commit that carries this ask are LOCAL.

## 10. The CTO half -- `1.0.0_SA_CTO~Z`

Signs: sections 1 and 2 (the `diff` and the `tools`) and the not-taken list. The CTO's own gate condition is met on
the release commit (0 REFUSE in ENFORCE). **Asked of this half in particular:** whether the tar-line edit in section 1 is inside
the hunk; and a ruling on Gap 2's route (grant on the internal reader role, or the module on the instance role).

## 11. The COO half -- `2.0.0_SA_COO~O`

Signs: sections 4 to 7 (the `order`, `both branches`, the `rollback`, the `triggers`). **Asked of this half in particular:**
Gap 1 (the six `.env` keys: amend the hunk, or ship dormant), because it decides whether Phase B can meet C1 and C2.

## 12. The CVO half -- `3.0.0_SA_CVO~Z`

Signs: sections 3 and 8 (the `widening` and the two conditions). **Asked of this half in particular:** that the widening it signs
is the one in section 3 **with Gap 1 stated**, and whether C2 is accepted as owed (dormant) or required before the sign.
