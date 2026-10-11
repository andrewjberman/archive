# MDPF_CANON -- L5 facts for the COO's decomposition

Read-only research, measured 2026-10-09 ~18:2xZ-18:4xZ. Repo at `box/dell1` working tree; AWS through `.tools/aws`.
No object bodies were read. Keys, sizes, dates and counts only. PRD read: `org/missions/D8/MDPF/MDPF_CANON/prd/MDPF_CANON_PRD.md` v2.8
(CONTRACTS :189-202, CELL CANDIDATES :352-374, PATHS :376-393).

Listings were made with `list-objects-v2 --max-items 20000` (or 100000); each returned count is below its cap, so each is complete:
- `opal-data-assets/gold/mdpf_revamp/`: **512** objects
- `opal-data-assets/portal/gold/mdpf/`: **746** objects
- `opal-data-portal-v2/platinum/mdpf/`: **553** objects
- `opal-data-mdpf` (whole bucket): **3088** objects

---

## 1. Who writes the four gold artifacts today

### The live clock (read from the LIVE plane, not the trigger map)

Census: `scheduler list-schedules --max-items 500` returned 33 schedules, and `events list-rules --max-items 500` returned 154 rules.
`get-schedule` / `describe-rule` on each MDPF hit:

| trigger | plane | expr (UTC) | target | invoke role |
|---|---|---|---|---|
| `mdpf-feeder-backstop-daily` | Scheduler, ENABLED | `cron(52 12 * * ? *)` | Lambda `mdpf-feeder-trigger` | `mdpf-feeder-scheduler-role` |
| `mdpf-feeder-accelerator` | EventBridge rule, ENABLED | pattern: S3 Object Created `opal-data-inf` `gold/meta/pipeline-complete.json` | Lambda `mdpf-feeder-trigger` | -- |
| `mdpf-scheduled-floor` | Scheduler, ENABLED | `cron(30 13 * * ? *)`, input `run_class=production` | Lambda `mdpf-gold-lambda` | `mdpf-floor-scheduler-role` |
| `mdpf-accrual-bridge-daily` | Scheduler, ENABLED | `cron(40 13 * * ? *)` | Lambda `mdpf-accrual-trigger`, which SSMs the EC2 runner | `mdpf-accrual-scheduler-role` |
| `opal-assets-mdpf-portal-publisher-daily` | Scheduler, ENABLED | `cron(50 13 * * ? *)` | Lambda `opal-assets-mdpf-portal-publisher` | `opal-assets-mdpf-portal-publisher-scheduler-role` |

Also listed: `mdpf-secclass-new-security-daily` (ENABLED) and `advi-49f-publisher` (DISABLED). These are not gold-artifact writers and were not described.

**Drift between the declared map and the live plane:**
- `EC2_MANIFEST.json:485` says the runner is fired by EventBridge rule `mdpf-daily-refresh-trigger`. **That rule is ABSENT from the 154-rule census.** A grep for `refresh` finds only `yang-refresh-fred-cache-weekly`.
- The trigger map's 15:45 / 16:15 times (brief IV.10) are wrong. Live is 13:40 / 13:50.
- The object last-modified times match the live crons: revamp 13:31Z, portal gold 13:31Z and 13:40Z, platinum 13:50Z.

### Writer 1: `mdpf-gold-lambda` (the main writer of every artifact)

- **Code:** `data/mdpf/scripts/gold/mdpf_gold_consolidator.py`, packaged by `infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py`.
- **Deployment:** `infra/aws/terraform/mdpf-pipeline/gold-lambda.tf:96-311`, handler `mdpf_gold_consolidator.lambda_handler` (:99).
- **Code home:** `s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip` (:115-116).
- **Live:** `get-function-configuration` shows role `mdpf-gold-lambda-role`, `MDPF_GOLD_COMMIT=e20899bce7`, LastModified `2026-10-09T18:00:35Z`. The zip was rewritten 17:58:35Z today, after the 13:30Z fire.
- **Principal:** `mdpf-gold-lambda-role`. Its inline policies are `mdpf-gold-scoped`, `mdpf-gold-taxsma-policy` and `mdpf-gold-etf-universe-policy`. `mdpf-gold-scoped` (live `get-role-policy`) grants:
  - Put/Get on `opal-data-assets/portal/gold/mdpf/*`, `gold/mdpf_revamp/*` and `gold/mdpf_revamp/_aggregate_aua/*`;
  - Get on `opal-data-mdpf/mdpf/feeds/*`;
  - **no write on `opal-data-mdpf` except the Tax control key, and no write on any firm bucket.**

**What it writes:**
- **Dated canonical JSON** at `s3://opal-data-assets/portal/gold/mdpf/{scope}/{artifact-type}/{data-as-of}.json` (`a4_key()` :2170-2171; constants :111-115).
  - Types: `aggregate-aua-timeseries`, `aum-metrics`, `account-distribution` and `category-views` (emit loop :2765-2799; scope-set map :153-156).
  - Scopes: `49financial`, `inflection`, `cottonwood`, `global` (:117). **No `demo` scope exists in code or in S3.**
  - Writes are conditional: same bytes give `unchanged`, different bytes give `conflict`, and an existing key is never overwritten (`conditional_put`, :2151; docstring :38-40).
- **Staging single objects** under `gold/mdpf_revamp/` (`stage_put` :2158-2167):
  - `{49financial,inflection}/aggregate_aua_timeseries.json` (:2434);
  - `global/aggregate_aua_timeseries.json` (:2451);
  - `global/non_model_assets.json` (:2487);
  - dated `_aggregate_aua/{date}.json` through `mdpf_aggregate_aua` (:2454-2468).
- **Cottonwood, in-process** (`run_cottonwood_family` :2225-2231, called :2415):
  - `data/assets/scripts/gold/build_cottonwood_mdpf_slice.py` writes `gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json` (:28, :1501);
  - `data/assets/scripts/gold/build_cottonwood_mdpf_pair.py` writes `gold/mdpf_revamp/cottonwood/{account_distribution,aum_metrics,account_units}.json` (:910-912). **This is the only `account_units` producer.**
- **Run manifest:** `portal/gold/mdpf/_manifests/{data-as-of}/{process-ts}.json` (:2829-2836).
- **`account_units` for 49financial, inflection and global** is not a standalone object. It is folded into aum-metrics as `total.account_units` (:550-574).

### Writer 2: accrual bridge (EC2 runner via SSM, 13:40Z)

- **Code:** `data/mdpf/scripts/gold/build_portal_gold_accrual.py`. It reads `gold/mdpf_revamp/{scope}/{underscore}.json` (:88, :225-227) and writes dated `portal/gold/mdpf/{scope}/{hyphen}/{date}.json` with no overwrite (:283-290).
- **Declared types** (:58-84): `aggregate-aua-timeseries`, `account-distribution`, `aum-metrics` (all scopes); `non-model-assets` (global only); `account-units` (cottonwood only, marked "UNVERIFIED -- needs a consumer trace").
- **Trigger:** Lambda `infra/aws/lambda/mdpf-pipeline/mdpf-accrual-trigger/lambda_function.py:103-122`. It copies the bundle from `ACCRUAL_BUNDLE_URI`, untars it, runs `python3 /opt/mdpf/scripts/gold/build_portal_gold_accrual.py`, and calls `ssm.send_command` on `RUNNER_INSTANCE_ID=i-02448edb624a7a7cf`.
- **Live:** the env names bundle `s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-accrual-bridge.tar.gz`. Role `mdpf-accrual-trigger-role`.
- **Runner principal:** instance profile `mdpf-daily-runner-profile` (`describe-instances`: state `stopped`, LaunchTime `2026-10-09T13:30:35Z`).
- **Effect today:** it is the effective writer of `portal/gold/mdpf/cottonwood/account-units/{date}.json` and `portal/gold/mdpf/global/non-model-assets/{date}.json`, whose last-modified is 13:40:28Z. For the other types, the Lambda's 13:31Z writes land first.

### Writer 3, declared but dead: the EC2 daily runner's Stage 6 (M17)

- **Code:** `infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:455-634`.
- **Declared targets:** `gold/mdpf_revamp/{49financial,inflection,global}/{aggregate_aua_timeseries,account_distribution}.json`, `global/non_model_assets.json`, `{scope}/aum_metrics.json` x4 (:576), and the marker `meta/cycle-complete.json` (:631).
- **Live evidence that it is dead:**
  - `{49financial,inflection,global}/account_distribution.json` last written 2026-08-18;
  - `{49financial,inflection,global}/aum_metrics.json` last written 2026-08-14;
  - `meta/cycle-complete.json` last written 2026-08-14T07:28Z.
- So the accrual bridge's aum-metrics and account-distribution sources for the three non-cottonwood scopes are frozen at August.

### Summary per scope (today's effective writer)

| scope | aggregate_aua_timeseries | aum_metrics | account_distribution | account_units |
|---|---|---|---|---|
| 49financial | gold Lambda (portal dated plus revamp single) | gold Lambda (portal dated); revamp single stale 08-14 | gold Lambda (portal dated); revamp single stale 08-18 | none standalone (folded in aum-metrics) |
| inflection | same as 49financial | same | same | none standalone |
| cottonwood | gold Lambda, in-process slice (revamp single); Lambda (portal dated) | gold Lambda, in-process pair (revamp) plus Lambda (portal dated) | same as aum_metrics | gold Lambda, in-process pair (revamp single); **accrual bridge** (portal dated, 13:40Z) |
| global | gold Lambda fold (both trees) | gold Lambda (portal dated); revamp single stale 08-14 | gold Lambda (portal dated); revamp single stale 08-18 | none standalone |
| demo | **no writer, no object anywhere** | -- | -- | -- |

---

## 2. The two legacy trees: history storage

### `s3://opal-data-assets/gold/mdpf_revamp/` (512 objects): SINGLE objects, history inside the body (not read)

| key | size B | last-modified |
|---|---|---|
| `49financial/aggregate_aua_timeseries.json` | 207801 | 2026-10-09T13:31:29Z |
| `49financial/aum_metrics.json` | 5269 | 2026-08-14 (stale) |
| `49financial/account_distribution.json` | 5652 | 2026-08-18 (stale) |
| `inflection/aggregate_aua_timeseries.json` | 176115 | 2026-10-09T13:31:29Z |
| `inflection/aum_metrics.json` | 5892 | 2026-08-14 (stale) |
| `inflection/account_distribution.json` | 7124 | 2026-08-18 (stale) |
| `cottonwood/aggregate_aua_timeseries.json` | 162091 | 2026-10-09T13:31:12Z |
| `cottonwood/aum_metrics.json` | 7054 | 2026-10-09T13:31:13Z |
| `cottonwood/account_distribution.json` | 12894 | 2026-10-09T13:31:13Z |
| `cottonwood/account_units.json` | 9666 | 2026-10-09T13:31:13Z |
| `global/aggregate_aua_timeseries.json` | 508960 | 2026-10-09T13:31:29Z |
| `global/aum_metrics.json` | 7734 | 2026-08-14 (stale) |
| `global/account_distribution.json` | 7719 | 2026-08-18 (stale) |

Other objects in this tree:
- **Dated:** `_aggregate_aua/{YYYY-MM-DD}.json`, 491 objects, 491 dates, first 2024-11-01, last 2026-10-09. This is the longest dated history in either tree.
- **Not one of the four artifacts:**
  - `cottonwood/aggregate_aua_timeseries_interpolated.json` (87262 B, 07-23);
  - `global/non_model_assets.json` (99278 B, today);
  - `global/non_model_assets_precutover_frozen.json` (44480 B, 07-21);
  - `meta/cycle-complete.json` (801 B, 08-14);
  - `portfolios/aum-metrics.json` (7734 B, 08-14);
  - `portfolios/aum-timeseries.json` (289962 B, 07-23);
  - `_audit/` (2 objects, 2026-07-23).
- No `account_units` exists for 49financial, inflection or global, and **no `demo/` prefix exists.**

### `s3://opal-data-assets/portal/gold/mdpf/` (746 objects): DATED objects, one per data-as-of (`{scope}/{type}/{date}.json`)

| scope / type | dates (= objects) | first | last |
|---|---|---|---|
| 49financial/aggregate-aua-timeseries | 51 | 2026-07-27 | 2026-10-08 |
| 49financial/aum-metrics | 42 | 2026-07-30 | 2026-10-08 |
| 49financial/account-distribution | 44 | 2026-07-28 | 2026-10-09 |
| inflection/aggregate-aua-timeseries | 50 | 2026-07-27 | 2026-10-08 |
| inflection/aum-metrics | 41 | 2026-07-30 | 2026-10-08 |
| inflection/account-distribution | 58 | 2026-07-27 | 2026-10-09 |
| cottonwood/aggregate-aua-timeseries | 42 | 2026-07-22 | 2026-10-08 |
| cottonwood/aum-metrics | 34 | 2026-07-20 | 2026-10-08 |
| cottonwood/account-distribution | 34 | 2026-07-20 | 2026-10-08 |
| cottonwood/account-units | 32 | 2026-07-20 | 2026-10-08 |
| global/aggregate-aua-timeseries | 42 | 2026-07-27 | 2026-10-08 |
| global/aum-metrics | 33 | 2026-07-30 | 2026-10-08 |
| global/account-distribution | 37 | 2026-07-28 | 2026-10-09 |

Other objects in this tree:
- **Not one of the four artifacts:**
  - `category-views` (49financial 24, inflection 23, cottonwood 17, global 19; all 2026-08-27..10-08);
  - `global/non-model-assets` (38, 07-27..10-08);
  - `_manifests/` (83 objects over 40 data-as-of folders, 2026-08-05..10-08);
  - `_code/mdpf-gold-lambda.zip` (1734711 B);
  - `_code/mdpf-accrual-bridge.tar.gz` (14828 B).
- The date counts are uneven across types and scopes, so the dated series have gaps. Each dated aggregate-aua-timeseries object is itself a full-series snapshot. Its internal date axis was not read.

### Backfill implications (M3)

- The per-day history for aum_metrics, account_distribution and account_units exists only as the portal dated objects. It starts at 2026-07-20 (cottonwood) or 07-27..07-30 (the others), and has gaps.
- The time-series history back to 2024-11-01 lives inside the single `aggregate_aua_timeseries.json` bodies, plus two dated sets:
  - `gold/mdpf_revamp/_aggregate_aua/` (491 dates);
  - `opal-data-portal-v2/platinum/mdpf/archive/aggregate_aua/` (439 dates, 2024-11-01..2026-08-05).

---

## 3. Today's served platinum, `s3://opal-data-portal-v2/platinum/mdpf/` (553 objects)

| scope | key | last-modified |
|---|---|---|
| 49financial | `account-distribution.json`, `aggregate-aua-timeseries.json`, `aum-metrics.json`, `category-views.json` | 2026-10-09T13:50:50Z |
| inflection | `account-distribution.json`, `aggregate-aua-timeseries.json`, `aum-metrics.json`, `category-views.json` | 2026-10-09T13:50:52Z |
| cottonwood | `account-distribution.json`, `account-units.json`, `aggregate-aua-timeseries.json`, `aum-metrics.json`, `category-views.json` | 2026-10-09T13:50:50-51Z |
| global | `account-distribution.json`, `aggregate-aua-timeseries.json`, `aum-metrics.json`, `category-views.json`, `non-model-assets.json` | 2026-10-09T13:50:51-52Z |
| demo | **none** | -- |

Other objects:
- `_manifests/`: 90 dated run manifests (2026-08-07..10-09) plus `_manifests/latest.json` (13:50:52Z).
- `archive/`: 444 objects, all written 2026-08-06:
  - `aggregate_aua/{date}.json`: 439 objects, 2024-11-01..2026-08-05;
  - `aggregate_aua_timeseries.json`: 1 object;
  - `etf_ownership_timeseries/{DIVZ,IDVZ,PFDE,PFOE}.json`: 4 objects.

---

## 4. The publisher

- **Source:** `infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py` (566 lines). Terraform: `infra/aws/terraform/opal-assets/mdpf_portal_publisher.tf:143-145`.
- **Reads:**
  - It lists `GOLD_BUCKET/GOLD_ROOT` = `opal-data-assets/portal/gold/mdpf/` (:77-78, :243-245).
  - It picks the latest `{scope}/{type}/{YYYY-MM-DD}.json` per pair (`_KEY_RE` :200, `derive_publish_set` :236-258) and gets the body (:370).
  - Second read: the Tax control at `address("mdpf","global","state","taxsma_control","current.json")` = `s3://opal-data-mdpf/mdpf/global/state/taxsma_control/current.json` (:141-158).
- **Writes:**
  - `SERVE_BUCKET/SERVE_ROOT/{scope}/{type}.json` = `opal-data-portal-v2/platinum/mdpf/...` (:79-80, :366, :418);
  - `_manifests/{date}/{run-id}.json` (:534-535) and `_manifests/latest.json` (:341-342, :553).
- **Live:**
  - env `GOLD_BUCKET=opal-data-assets`, `GOLD_ROOT=portal/gold/mdpf`, `SERVE_BUCKET=opal-data-portal-v2`, `SERVE_ROOT=platinum/mdpf`, `MDPF_PUBLISHER_COMMIT=e8994f23af`;
  - role `opal-assets-mdpf-egress-publisher-role`. Grants: Get `opal-data-assets/portal/gold/mdpf/*`; Put `opal-data-portal-v2/platinum/mdpf/*` and `platinum/_staging/mdpf/*`; Get the one Tax control key. **No firm-bucket grant.**
- **CONSTRAINT FOR M5:** the live publisher is `python3.12`, 256 MB, 120 s, with **no layers**, so it has no pyarrow. The estate's `pandas-pyarrow-requests-layer` used by the gold Lambda is py3.11 (`gold-lambda.tf:67-71, :101-103`). Reading parquet needs a packaging decision.

### The three denominators (brief `docs/briefs/d8-mdpf-canon-migration-brief-20260913.md:304`, :145-147)

- **522: PLACED.** It is all objects under `platinum/mdpf/` at 2026-09-13 02:48Z.
  - Today there are 553. 31 dated `_manifests` objects were written after 2026-09-13T02:48Z.
  - 553 - 31 = **522** exactly. At that time it was 444 archive + 59 manifests + 18 leaves + `latest.json`.
- **13: PLACED.** It is the firm-slice leaves: 49financial 4 + cottonwood 5 + inflection 4 = **13**. The count is the same today, and `global`'s 5 leaves are excluded.
- **492: UNPLACED** as the brief attributes it ("all objects on 07-28", from the 08-25 inventory). The `archive/` set is dated 08-06, so a 07-28 tree cannot be rebuilt from today's listing, and the inventory file was not read.
  - Note: `gold/mdpf_revamp/` held **492** objects at the same 09-13 read (brief :145).
  - The 492 may be that tree's count conflated with platinum's. That is an inference.

---

## 5. The TAXSMA per-firm role precedent (`infra/aws/terraform/mdpf-pipeline/iam.tf:992-1230`)

**Name builder:**
- `module "taxsma_49f_role_name"` / `"taxsma_cot_role_name"` use `source = "../modules/opal_name"` with `system="mdpf"`, `scope="49financial"|"cottonwood"`, `function="taxsma"`, `kind="role"` (:992-1006).
- Policy names come from the same module with `kind="policy"` (:1040-1046, :1136-1142).
- Live names: `mdpf-49f-taxsma-role` / `mdpf-49f-taxsma-policy` and `mdpf-cot-taxsma-role` / `mdpf-cot-taxsma-policy`.

**Firm and bucket derived, never typed:**
- `local.taxsma_49f_long` comes from the module's `scope_short` / `scope_class == "FIRM"` maps, matched against the built name (:1008-1020).
- The bucket comes from `module...scope_bucket[long]` (:1021-1022).

**Trust:** `sts:AssumeRole`, Principal `aws_iam_role.mdpf_gold_lambda.arn` (:1023-1030). Live `get-role` shows principal `role/mdpf-gold-lambda-role` on both roles.

**Grants (49financial)** (:1048-1128):
- secret read;
- Schwab silver Get (three prefixes);
- the workbook bronze/silver Put+Get;
- `Tax49fStateRW`: Put/Get/GetObjectVersion on `{firm_bucket}/mdpf/{long}/state/taxsma_membership/*` and `{firm_bucket}/mdpf/{long}/gold/taxsma_assets/*`;
- GetBucketVersioning;
- ListBucket conditioned on those prefixes.

Cottonwood (:1144-1197) has the same shape with Black Diamond silver. **There is no inflection role.**

**Gold Lambda side:**
- Inline policy `mdpf_gold_taxsma` (`kind="policy"`, `function="gold-taxsma"`, :1202-1230) allows `sts:AssumeRole` on exactly the two roles, plus Put/Get on the global Tax control key.
- The role ARNs reach code through env `TAXSMA_PRELUDE_ROLE_ARN_{FIRM}` (`gold-lambda.tf:302-303`).
- The code is `taxsma_session()` in `mdpf_gold_consolidator.py:1168-1186`: `boto3.client("sts").assume_role(RoleArn=arn, RoleSessionName="mdpf-taxsma-prelude")`, building a session from the temporary credentials. If the env var is unset, it falls back to the function's own credentials.

**Live proof the pattern already writes dated parquet in firm buckets:**
- `opal-data-49financial/mdpf/49financial/gold/taxsma_assets/date=2026-10-01/data.parquet` and onward: 9 dated `data.parquet` objects (10-01..10-09) plus 1 `state/taxsma_membership/.../dispositions.json`.
- `opal-data-cottonwood` has the same: 9 + 1.

---

## 6. `lib/opal_naming.py` `address()` output

- **Signature:** `address(source, scope, tier, table, partition, object=None)`.
- **Call:** `address("mdpf", scope, tier, artifact, "date=2026-10-08")`.
- **Coverage:** 40 calls (2 tiers x 5 scopes x 4 artifacts). **Zero refusals.**

| scope | gold | state |
|---|---|---|
| 49financial | `s3://opal-data-49financial/mdpf/49financial/gold/{artifact}/date=2026-10-08` | `s3://opal-data-49financial/mdpf/49financial/state/{artifact}/date=2026-10-08` |
| inflection | `s3://opal-data-inflection/mdpf/inflection/gold/{artifact}/date=2026-10-08` | `s3://opal-data-inflection/mdpf/inflection/state/{artifact}/date=2026-10-08` |
| cottonwood | `s3://opal-data-cottonwood/mdpf/cottonwood/gold/{artifact}/date=2026-10-08` | `s3://opal-data-cottonwood/mdpf/cottonwood/state/{artifact}/date=2026-10-08` |
| global | `s3://opal-data-mdpf/mdpf/global/gold/{artifact}/date=2026-10-08` | `s3://opal-data-mdpf/mdpf/global/state/{artifact}/date=2026-10-08` |
| demo | `s3://opal-data-demo/mdpf/demo/gold/{artifact}/date=2026-10-08` | `s3://opal-data-demo/mdpf/demo/state/{artifact}/date=2026-10-08` |

- `{artifact}` takes each of `account_distribution`, `account_units`, `aggregate_aua_timeseries` and `aum_metrics`. All 40 were printed individually, and each followed exactly this form.
- **With an object name:** `address(...,"aum_metrics","date=2026-10-08",object="data.parquet")` gives `s3://opal-data-49financial/mdpf/49financial/gold/aum_metrics/date=2026-10-08/data.parquet`. This is the same leaf grammar TAXSMA writes.
- **The PRD's platinum vector reproduces:**
  - `key("mdpf","49financial","platinum","aum_metrics","aum-metrics.json")` gives `mdpf/49financial/platinum/aum_metrics/aum-metrics.json`;
  - `address()` over the same arguments gives that key under `s3://opal-data-49financial/`.
- **Bucket existence:** `head-bucket` returns EXISTS for `opal-data-49financial`, `-inflection`, `-cottonwood`, `-demo` and `opal-data-mdpf`.
- **What the firm buckets hold under `mdpf/`** (`--max-items 200`):
  - 49financial: 10 (Tax only);
  - cottonwood: 10 (Tax only);
  - inflection: 0;
  - demo: 0.

---

## 7. Is parquet already written under `opal-data-mdpf`?

- **Top level** (`--delimiter / --max-items 50`): 5 prefixes: `bmkaud-evidence/`, `code/`, `diagnostics/`, `mdpf/`, `telemetry/`.
- **Under `mdpf/`:** 3 prefixes: `mdpf/bronze/`, `mdpf/feeds/`, `mdpf/global/`.
- **Full key census:** 3088 objects, of which **1601 are `.parquet`, all under `mdpf/feeds/`:**
  - `non_model_aua` 602
  - `partner_held_etf` 288
  - `etf_net_assets` 265
  - `model_aua_positions` 223
  - `model_composition` 223
- **No gold parquet for the four artifacts exists anywhere in `opal-data-mdpf`.**
- `mdpf/global/` holds 3 objects:
  - `gold/ai_classified_securities/date=2026-10-07/index.json`
  - `gold/ai_classified_securities/date=2026-10-08/index.json`
  - `state/taxsma_control/current.json`
- Other prefixes: `mdpf/bronze/` 1030 objects (the brief read 830 on 09-13); `code/` 71.
- The only gold-tier parquet in the estate on MDPF's key grammar is TAXSMA's `taxsma_assets` in the two firm buckets (section 5).
