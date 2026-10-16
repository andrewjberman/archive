# NEVER-WIDEN ASK -- OG-ap-23: the code batch release -- 27 READ tools, client tools master_admin only, OG-bd-3, one deploy

To: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O` and `3.0.0_SA_CVO~Z` -- THREE halves, each signed on its own.
From: `0.7.0_AE_CloudOps~Z`. Phase A of `NFRA_OPLGTW.TO-OG-ap-23` as amended through **A7** (`ddba57dc08`); GO msg 34825.
**NOTHING IS DEPLOYED AND NOTHING IS APPLIED.** 224 taken and related tests pass; 12 more fail, and fail on the base too (section 9). The release commit grades 0 REFUSE in ENFORCE.
This ask **replaces** the one at sha256 `a4c90d32c29f` (release `56c0f8ce1d`), which the CTO and the CVO halves refused. Section 0 says what changed.

| | |
|---|---|
| **release** | `3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4` on `rel-nfra-oplgtw-code-a5` (worktree `C:/tmp/og-rel-code`), its single parent the live ref |
| **base** | `d577e0e7297b3ecba183023d8374855a93f148a7` -- OG-ap-21's release, live since 2026-10-16T00:09:44Z; the manifest and the S3 `git-ref` both name it (re-read at the GO), and a host md5 walk read 123 of 123 equal |
| **taken from** | `box/sitez` pinned at `23587956e9cb9bde3f0ad74a505d65693c706c84` (`OG-ad-1` merged) |
| **mcportal bundle** | `090b9cdc85ce3463e73915e68b44f4c21053a71c` (origin DEV; descends from `421f8fbe84`; live is `17dcbb28624e`) |
| **ledger** | `nfra-oplgtw-gateway-release-code` (Phase B; **not opened**) |
| **records** | `W/ap23_release.json`, `W/ap23_tar_census.json`; `ap23.AC1` PASS, exit 0 (run from the shared tree, section 9) |
| **superseded cuts** | `5939062746` (A2) on `rel-nfra-oplgtw-code`, `56c0f8ce1d` (A3) on `rel-nfra-oplgtw-code-a3`; both kept, neither deployable |

## 0. READ THIS FIRST: what changed since the refused ask, and the two widenings a half should weigh

1. **The tar line (A5, the CTO's refusal).** The previous cut had no tar-line edit: the staged `app/refs` copies never reached the archive,
   and an untracked test copy in the release tree would have shipped instead. The error was mine, and so was the sentence in the last ask
   that said the edit existed. Now the bundle group is listed first on the tar line with the two files named, the same two names are
   excluded from the `$SRC` group, and the existing excludes still sit ahead of both groups. GNU tar's `--exclude` carries forward from
   where it appears, so a position test was needed: I ran it, and the script's own staging block and tar line against a synthetic tree.
   **`W/ap23_tar_census.json` reads the real member list: each of the two files once, md5 equal to trunk's blobs, the planted decoy
   copy not shipped, a SRC-only file under `app/refs/` still shipped.** The same census on the previous cut's script FAILS (the decoy ships), so the
   instrument can tell the two apart.
2. **The client tools are master_admin only (A6, PRD v3.14 @`f2b066d9ad`, the CVO's refusal).** `OG-ad-1` moves the five `client_*` tools out
   of `NATIVE_TOOLS` into `CLIENT_TOOLS`, a member of both `DATA_GRANT_TOOLS` and `TIER_ADMITTED_TOOLS`, as `blackdiamond_list_fees` is. An
   unprofiled principal is refused unless its tier is master_admin; a profiled one is confined to its grant. **That is narrower than the
   previous cut and narrower than v3.1 Ruling 2's intent, never wider.** Phase B shows it on a real call (section 5).
3. **`OG-bd-3` ships in this release (A7), and that IS a widening.** The live base lacks `OG-bd-3`'s `decide()` branch and its two tier
   lines, in the same file as `OG-ad-1`'s change, so `app/data_entitlement.py` is taken **whole**. Effect, from the diff: on the restricted
   branch a `TIER_ADMITTED_TOOLS` member now **also passes when the caller's tier is master_admin, whatever the profile's state (active or
   not)**, and `tool_denial` / `visible_tools` now resolve the tier for a restricted principal too. Before, a profiled master_admin was
   denied `blackdiamond_list_fees` and (after this release) the five client tools; after, it is admitted. The CTO ruled it (msg 33941,
   route a); it is the purpose of `OG-ap-17`, which this release supersedes. **It is a widening at the entitlement chokepoint, scoped to
   the master_admin tier and to the six tier-admitted tools, and the halves weigh it.**
4. **Gap 1 and Gap 2 of the earlier ask stay closed** (A3): the six vendor reader keys are written by the deploy script, each ARN read from
   IAM and compared before any upload; `OG-ap-26` (signed) moves the classification grant to the internal reader role and gates Phase B.

## 1. The `diff`, by file -- 48 files, base to release

Counts: **33 added, 15 modified, 0 deleted.** Nothing under `infra/aws/terraform/`; no `.tf` file differs (AC1: terraform files differing 0).
Files outside the batch set: 0.

| file | how taken |
|---|---|
| `app/client_core.py`, `app/client_role.py` | WHOLE (new at this base) |
| `app/client_adapter_{schwab,bd49f,orion,eclipse,bdcottonwood,smartx,commonwealth}.py` | WHOLE (new) |
| `app/etfs_rivals.py`, `app/etfs_rivals_flow.py`, `app/etfs_silver.py` | WHOLE (new) |
| `app/portal_served.py`, `app/portal_json_served.py`, `app/mdpf_classification.py` | WHOLE (new) |
| `app/admin_gateway_breakdown.py`, `app/admin_people.py`, `lib/opal_naming.py` | WHOLE (existing at the base, replaced by trunk's) |
| **`app/data_entitlement.py`** | **WHOLE (A7)**: 45 lines added, 9 removed against the base. It carries `OG-bd-3`, `OG-ad-1` (the `CLIENT_TOOLS` set and its two memberships), the 27 names, and trunk's cosmetic re-order of `harvest_get_published_analysis`; the `OG-bd-3` hunks are item 3 of section 0 |
| `app/tools.py` | BY HUNK: 5 import lines and the 27 `@mcp.tool()` registrations; nothing else moves |
| `app/destructive_ops.py` | BY HUNK: the 27 names added to `SAFE_TOOLS`, nothing else |
| `app/integrations/portal_index/integration.py` | the MX-c-22 hunk, which is **all** that differs base to trunk (checked, not assumed) |
| `deploy-to-ec2.sh` | **three hunks**, 34 lines added and 4 changed, below |
| `infra/aws/ec2/EC2_MANIFEST.json` | ONE field: `services.opal-gateway.mcportal_commit` `17dcbb28624e` to `090b9cdc85ce` |
| 4 modified tests, WHOLE | `test_entitlement_admin` (pin 122), `test_data_entitlement_family` (non-data pin 108), `test_data_entitlement_guard`, `test_og_bd2`: they pin the module taken whole, and their follow-ups are trunk's own |
| 2 modified tests, WHOLE | `test_admin_gateway_breakdown`, `test_admin_people` |
| 18 added test files, WHOLE | `test_og_{cl1..7,ch1,rv1,rv2,gp1,gf1,sv1,sv2,ac2,ad1,bd3}` and `test_positioning_extension` |

**The three `deploy-to-ec2.sh` hunks.** (a) *Staging:* a presence check and three `cp` lines that ship `lib/opal_naming.py`,
`data/mdpf/config/partner_roster.json` and `infra/logic/registry/scopes.json` into the bundle from their repo sources, refusing with no
upload if a source is absent. (b) *The tar line (A5):* the bundle group first and the two `app/refs` files named in it, the same two names
excluded from the `$SRC` group (section 0 item 1). (c) *Reader keys (A3):* the account lookup, six role resolutions that refuse the deploy
on any mismatch, six `%s` keys in the `.env` `printf` and six arguments, placed before the two `ADVI_*` roots (`test_ogab1_ac03` and
`test_ogab2_ac03` pin the market-update argument second-to-last and the fee-statement argument last). Nothing else in the `printf` changes.

**Not committed as data:** `app/refs/partner_roster.json` and `app/refs/scopes.json` (AC1: data copies committed 0). Phase B proves both by
host md5 against trunk's blobs.

### Not taken, named rather than left for a half to find

1. **Trunk's `OG-db-1` preflight and its `.env` `printf` re-order in `deploy-to-ec2.sh`.**
2. `app/family_depth.py`, `refs/silver_families.json`, the yearinreview files, `admin_people_access.py`: not imported by anything taken
   (seam enumeration on this trunk, 61 distinct seams, 0 STOP, `W/ap23_seams_r5.out`). `test_og_cd1.py` is out of scope.

## 2. The `tools` -- 27 added, every one class READ

Registry on the host **76 to 103**; repo pins 122 and 108 (non-data). Each tool is in `SAFE_TOOLS` and in `data_entitlement.py` (27 of 27 each,
which AC1 recomputes). Every tool admits an Opal principal first (`typed_scope.admit_scope`) and refuses a non-Opal one **before** any S3, DynamoDB or
catalog read.

| group | tools | reads as | firm fence | `refused` arm |
|---|---|---|---|---|
| rival funds (10) | `etfs_get_peer_group_members`, `etfs_get_rival_fund_holdings`, `etfs_who_holds`, `etfs_get_security_reference`, `etfs_get_coverage`, `etfs_get_fund_trades`, `etfs_get_fund_flows`, `etfs_compare_peers`, `etfs_get_research_notes`, `etfs_get_rival_page_status` | the internal reader role, `opal-data-etfs/rivalfunds/etfs/gold/*` and `.../platinum/page/*` (OG-ap-20, live) | none: fund data | non-Opal: refusal, 0 reads |
| **client (5), master_admin only** | `client_resolve_account`, `client_get_holdings`, `client_get_transactions`, `client_get_allocation`, `client_get_fees` | the **vendor read role**, keyed in `.env` | **two fences**: admission (`CLIENT_TOOLS` is data-grant and tier-admitted: an unprofiled non-master_admin principal is `entitlement_denied`, a profiled one is confined to its grant, so today only master_admin) and `firm` (canonical `49financial`, `cottonwood`, `inflection` or an alias, else `firm_not_canonical`, 0 reads) | non-Opal, or Opal without master_admin or a grant: refusal, 0 reads. Also `no_catalog_row`, `window_too_long` (over 396 days), `registry_unavailable` (0 reads) |
| silver etfs (3) | `etfs_get_new_securities`, `etfs_get_fund_bloomberg_characteristics`, `etfs_get_fund_snapshot` | the internal reader role, `opal-data-etfs/silver/*` | none | non-Opal: refusal, 0 reads |
| portfolio (1) | `mdpf_get_model_composition` | the internal reader role, served portfolio tables | by `scope` argument | non-Opal: refusal, 0 reads |
| json-served (7) | `portal_get_correlations`, `portal_get_etf_returns`, `portal_get_factor_tilts`, `portal_get_model_portfolio_timeseries`, `portal_get_peer_performance`, `portal_get_trending`, `portal_get_cma_assumptions` | the internal reader role, `opal-data-portal-v2/json/*` | none | non-Opal: refusal, 0 reads |
| classification (1) | `mdpf_get_security_classification` | the internal reader role's DynamoDB client; the GetItem grant is `OG-ap-26`'s | none | non-Opal: refusal, 0 reads |

The client tools return one envelope (`as_of`, `partition_date`, `source_keys`, `denominator`, `absent_reason`, `platform_label`,
`platform_label_source`, `label_claim`, `freshness_td`) projected to 50 KB. A resolve asks **every** adapter that holds the firm and merges, and never picks
one; an account is referenced as `****<last4>/<vendor>/<alias>`, never a full number. **The 22 non-client tools are unchanged by the admission ruling.**

## 3. The `widening`, stated plainly

**No new IAM in this release.** No Terraform, no apply, no catalog edit, no object or item written anywhere. Three things change what the
gateway can do, in this order of weight:

- **A. `OG-bd-3` (section 0, item 3).** A profiled principal whose tier is master_admin is admitted to the six tier-admitted tools whatever its
  profile's state; before, a profile confined it. The tier still comes from the deploy-time rosters (`app/tier.py`), unchanged. Cost: the
  chokepoint's behaviour for that one population changes at this deploy. Non-application: nobody else's verdict moves.
- **B. The client tools turn the six live vendor read roles from unused to used, and the gateway can now return client account-level data (holdings,
  transactions, fees, allocation) to named Opal principals, who today can only be master_admin.** Which tool uses which role, and the fence:

| role | vendor, firm | adapter | env key this release writes |
|---|---|---|---|
| `gateway-49f-blackdiamond-read-role` | Black Diamond, `49financial` | `client_adapter_bd49f` | `BLACKDIAMOND49F_READER_ROLE_ARN` |
| `gateway-cot-blackdiamond-read-role` | Black Diamond, `cottonwood` | `client_adapter_bdcottonwood` | `BLACKDIAMONDCOTTONWOOD_READER_ROLE_ARN` |
| `gateway-inf-orion-read-role` | Orion, `inflection` | `client_adapter_orion` | `ORION_READER_ROLE_ARN` |
| `gateway-inf-eclipse-read-role` | Eclipse, `inflection` | `client_adapter_eclipse` | `ECLIPSE_READER_ROLE_ARN` |
| `gateway-cot-commonwealth-read-role` | Commonwealth, `cottonwood` | `client_adapter_commonwealth` | `COMMONWEALTH_READER_ROLE_ARN` |
| `gateway-smartx-read-role` | SmartX, `49financial` | `client_adapter_smartx` | `SMARTX_READER_ROLE_ARN` |

  The six trust policies were read on 2026-10-16: each names `opal-gateway-role` as the only principal, `sts:AssumeRole`, **no condition**, so no
  ExternalId is needed. Schwab (`client_adapter_schwab`, firm `49financial`) uses the existing `SCHWAB_READER_ROLE_ARN`; it is not one of the six.
- **C. The 22 non-client tools** read prefixes and tables the internal reader role already holds (OG-ap-20's etfs grant, the `json/*` grant, the news
  tables); they add readers, not reach. `mdpf_get_security_classification` adds the one table read that `OG-ap-26` grants to that role.
- Never widened: no write or `Scan` verb is reachable; no role gains a statement from this release; the six trust policies are unchanged.

## 4. The `order` of acts (Phase B, only on the issuer's GO naming all three halves signed at `release_sha`)

1. PRECONDITION: **`ap26.AC2` PASS**. Not met = STOP and report.
2. Ledger `nfra-oplgtw-gateway-release-code`, **entry AND sentinel first**.
3. ONE deploy from `C:/tmp/og-rel-code` through `safe-ec2-deploy.sh` with `DEPLOY_BASE_REF=d577e0e7297b3ecba183023d8374855a93f148a7`, the A1 guard
   (HEAD = the full signed `release_sha`, parent = the live `deployed_commit`, no other release in flight), no `HALT_OVERRIDE`.
4. The served read through the **installed** code, host and public endpoint (60 s ALB).
5. The CVO's conditions (section 8), then the standing clauses and the close.

## 5. `Both branches` of a call

| branch | what happens |
|---|---|
| **refused** | non-Opal principal, an Opal principal with no grant that is not master_admin (the client tools), non-canonical firm, no catalog row, window over 13 months, or registry unreadable: every arm fires BEFORE any S3, DynamoDB or catalog read. **Zero reads**: the host-shaped check, with `boto3.client` replaced by a counter that refuses, recorded 0 reads in both arms. |
| **admitted** | an Opal principal (the client tools: master_admin): capped (50 KB), projected to the envelope, fenced by firm (client tools), reading one partition per call. |

**Two facts the served read must SHOW, written into `W/CODE_SERVED.json`:**
- `client_admission` (A6): `{"unprofiled_nonadmin_refused": true, "reads_on_refusal": 0, "master_admin_served": true}`. The negative arm is an Opal
  principal with no grant that is not master_admin calling `client_get_holdings`: refused, 0 reads. The positive arm is master_admin: served.
- `via_internal_reader: true` on `mdpf_get_security_classification` (CVO condition on `OG-ap-26`), with the assumed-role identity of the session that
  made the `get_item` as evidence (names only): `assumed-role/gateway-global-internal-reader-role/...`, not `opal-gateway-role`.

## 6. The `rollback`

1. **The code**: redeploy the base `d577e0e7297b3ecba183023d8374855a93f148a7`, the live commit and this release's parent. Nothing in this release is
   irreversible and no IAM moves, so a binary rollback undoes the whole act, including `OG-bd-3`'s branch.
2. The six `.env` keys leave with the redeploy (the `.env` is rebuilt at each deploy); the host returns to 58 keys.

## 7. The `triggers` Phase B reads back

| trigger | expected |
|---|---|
| `/health` | serving |
| registry on the host | 76 to **103** |
| repo pins | registered 95 to **122**, non-data **108** |
| host `.env` key names | 58 to **64**: the six names above added, nothing removed (names only, over SSM, no value printed) |
| host md5 | equal to the release blobs across `app/`, `deploy/`, `lib/`, **and** `app/refs/partner_roster.json` = md5 `3d309b267e69` (git blob `eb3bff48c847`) and `app/refs/scopes.json` = md5 `2af41e5f393f` (git blob `dde73e4bd061`), both read from `trunk_sha`; the host md5 is the md5 column, the blob id is how git names the same bytes |
| per tool | 27 of 27: an Opal stand-in is served an enveloped answer (the client tools: a master_admin stand-in), a non-Opal is refused with 0 reads |
| `client_admission` | all three fields true (section 5) |
| classification | `via_internal_reader: true` (section 5) |
| IAM | no change from this release; the only movement in the window is `OG-ap-26`'s own |

Any trigger red: redeploy the base and file an ARMED row naming `2.0.0_SA_COO~O`.

## 8. The CVO's two conditions from `OG-ap-24`, and where Phase B meets them

- **C1: one REAL AssumeRole of a vendor read role by the gateway role** (a simulate cannot see a trust). Step 5, from the host, one `sts:AssumeRole` of
  `gateway-smartx-read-role`; the call is recorded, no credential printed. Beside it: `reader_env_keys_present: 6` (names read over SSM) and the six
  `iam get-role` resolutions the deploy script made before the upload.
- **C2: SmartX counts as firm-safe only after the two-firm negative arm.** Step 5, through the installed `client_*` tools **as a master_admin stand-in**
  (the only tier that reaches them): a SmartX read for firm A returns only firm A's rows, and the same read naming the other firm refuses or returns only
  that firm's rows, never A's (counts only). Met by the installed keys.

## 9. Readings a half should have that are not about the diff

- **How the release tree ran the gates.** It is cut on a base older than the gate: I laid trunk's `naming-gate.py`, `naming-apply-gate.py`, `infra/logic/`,
  `NAMING_SCHEMA.json`, `DIRECTIVES.yaml` and the `lib/opal_naming_*.py` siblings over it as **uncommitted** files (`W/ap23_gate_overlay_manifest.txt`),
  because the base-era gate cannot load the newer registry. With them: `ng2.AC2` PASS (0 REFUSE, 10 RULED), `ng3.AC1` PASS (0 REFUSE, 11 RULED), and the
  release commit itself `NAMING-GATE: WARN 14 graded`, 0 REFUSE. None of the overlay is in the commit. The deploy tree keeps trunk's `scopes.json` on
  disk because it is a bundle source.
- **Twelve tests fail on the BASE as well**, so they are not this release's: `test_schwab_host_inputs.py` (3), `test_deploy_base_guard.py` (8) and
  `test_data_entitlement_guard.py::test_ogz1_ac08` (1: the test's route table lacks `/hx/teams/teams`, which the base server serves; I saw it fail with the entitlement
  change removed as well). I ran the test files that read the deploy script against the base script and against mine: the same set. 224 pass, including
  every taken test and the four entitlement tests. The host-shaped import check on this cut: 18 of 18 modules import with and without
  `lib/opal_naming.py`, 0 reads in both arms (`W/ap23_hostshape_r5.json`).
- **AC1 is run from the shared tree, not the release tree**: its `live` is read from `HEAD`'s `EC2_MANIFEST.json`, and the release branch's own manifest
  baseline is older (`daa56d81ac`).
- **Branches.** A `git reset` of the A2 tip was refused by the head-move guard, so each re-cut is a new branch at the base with HEAD pointed at it
  (`-a3`, then `-a5`); no commit was discarded and no guard was forced.
- **Test support kept out of the commit:** worker evidence files, the check scripts and the two `app/refs` copies are in the tree untracked.
- `tools.py` carries 7 lines with non-ASCII characters (commit-gate WARN, not blocking); they come from trunk's registrations.
- **The record commits are not pushed**: only the integrator may push `box/sitez`.

## 10. The CTO half -- `1.0.0_SA_CTO~Z`

Signs: sections 1 and 2 (the `diff` and the `tools`) and the not-taken list. **Asked of this half in particular:** that the tar line (section 0 item 1,
census in `W/ap23_tar_census.json`) is what its refusal asked for, and that `data_entitlement.py` taken whole is within A7.

## 11. The COO half -- `2.0.0_SA_COO~O`

Signs: sections 4 to 7 (the `order`, `both branches`, the `rollback`, the `triggers`). Carried: A5 to A7, the `client_admission` and
`via_internal_reader` facts, the md5 and blob ids restated from `trunk_sha`.

## 12. The CVO half -- `3.0.0_SA_CVO~Z`

Signs: sections 3 and 8 (the `widening` and the two conditions). **Asked of this half in particular:** that the client tools are now master_admin only
(item 2), and the `OG-bd-3` widening (item A of section 3) which this release delivers and which the earlier ask did not carry.
