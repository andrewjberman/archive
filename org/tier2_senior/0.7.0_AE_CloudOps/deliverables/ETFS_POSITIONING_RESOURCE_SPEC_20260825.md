# ETFS_POSITIONING — COMPONENT RESOURCE SPEC
**For:** Andrew (direct ask ~04:00Z / 04:1xZ 2026-08-25) — *"spec out what all the component resources are so that we can run a terraform later on the laptop device"* / *"make a briefing that has all of them listed"*
**Author:** `0.7.0_AE_CloudOps~Z` · site Z · 2026-08-25T04:2xZ
**Status:** SPEC ONLY. Nothing consolidated, nothing moved, no state touched.

---

## 0. READ THIS FIRST — TWO CONSTRAINTS THAT SHAPE THE WHOLE THING

**(1) NO TERRAFORM GROUP CAN COVER THIS PIPELINE END TO END.** The Bloomberg leg that writes
`bbg/{date}/` — the input gold *cannot run without* — is a **Windows Scheduled Task on a physical box
behind a signed-in terminal.** It is not an AWS resource and cannot become one. Any grouping must
name it as an out-of-band leg, or the group looks complete while omitting the component that was the
live risk on 08-24.

**(2) CONSOLIDATING STATE IS THE DESTRUCTIVE HALF.** Merging roots moves resources between state
files — where Terraform destroys things when it goes wrong, on a client-facing pipeline. Declaring
and tagging a group needs **no** state migration. Those are separable and should be decided
separately.

---

## 1. MEMBERSHIP — HOW THE BOUNDARY WAS DRAWN

Not by name. **By measured bucket access** (IAM inline policy read, live):

| function | role | buckets reached | in this pipeline? |
|---|---|---|---|
| `etfs-netassets-daily` | `etfs-netassets-daily-role` | `opal-data-assets`, `opal-data-etfs` | **YES** |
| `etf-positioning-producer` | `etf-positioning-producer-role` | `opal-data-etfs`, `opal-data-portal-v2` | **YES** |
| `opal-assets-silver-etf` | `opal-assets-silver-etf-role` | `opal-data-assets` | **ADJACENT** (sweep) |
| `etfs-canon-fanin` | `etfs-canon-fanin-role` | `opal-data-etfs` | **NO** — ownership product |
| `etf-ownership-dashboard` | `etf-ownership-dashboard-role` | `opal-data-etfs` | **NO** — ownership product |
| `yang-generate-positioning` | `yang-pipeline-lambda-role` | `opal-data-portal-v2` | **NO** — models, not ETFs |

⚠ **`etfs-canon-fanin` and `etf-ownership-dashboard` DO touch `opal-data-etfs`** — bucket access alone
is necessary, not sufficient. They are a different product (49f ETF *ownership*), and are excluded on
product grounds, stated so the exclusion is arguable rather than silent.

---

## 2. THE PIPELINE, IN ORDER

```
ISSUERS                     INGEST                     BLOOMBERG                  PRODUCE            SERVE
filepoint (PFDE,PFOE) ─┐                                                                        
trueshares (DIVZ,IDVZ)─┴─► etfs-netassets-daily ──► [bbg pull, NOT AWS] ──► etf-positioning-producer ──► portal
                            cron(0 22) 22:00Z          ~11:00Z site Z          cron(0 13) 13:00Z
                            writes bronze+silver       writes bbg/{date}/       writes gold + platinum
```

---

## 3. RESOURCE INVENTORY

### 3.1 `etfs-netassets` — INGEST (bronze + silver)
**TF root** `infra/aws/terraform/etfs-netassets/` · **state key** `etfs-netassets/tfstate`

| resource | identifier | detail |
|---|---|---|
| `aws_lambda_function` (module `yang-lambda`) | `etfs-netassets-daily` | python3.11, **1024 MB / 300 s**, `lambda_function.lambda_handler` |
| `aws_iam_role` | `etfs-netassets-daily-role` | |
| `aws_iam_role_policy` | `…-role:s3-rw-etfs-bronze-silver` | `opal-data-assets` + `opal-data-etfs` |
| `aws_iam_role_policy_attachment` | basic execution | |
| `aws_cloudwatch_event_rule` | `etfs-netassets-daily` | **`cron(0 22 * * ? *)`** ENABLED |
| `aws_cloudwatch_event_target` | → the Lambda | |
| `aws_lambda_permission` | `EventBridgeEtfsNetassetsDaily` | |
| `aws_cloudwatch_metric_alarm` | `etfs-netassets-daily-errors` | ⚠ pre-dates the 2026-07-28 alarm moratorium |
| *(implicit)* log group | `/aws/lambda/etfs-netassets-daily` | |

**Env:** `TS_HOLDINGS_ENABLED=1`, `BRONZE_BUCKET=opal-data-assets`, `BRONZE_GRAMMAR=monolith`,
`ETFS_BUCKET=opal-data-etfs`, `SILVER_ROOT=""`
**Source:** `infra/aws/lambda/etfs-pipeline/etfs-netassets-daily/lambda_function.py`

### 3.2 `etfs-positioning` — PRODUCE (gold + platinum)
**TF root** `infra/aws/terraform/etfs-positioning/` · **state key** `etfs-positioning/tfstate`

| resource | identifier | detail |
|---|---|---|
| `aws_lambda_function` (module `yang-lambda`) | `etf-positioning-producer` | python3.11, **512 MB / 120 s**, `etf_positioning_gold.lambda_handler` |
| `aws_iam_role` | `etf-positioning-producer-role` | |
| `aws_iam_role_policy` | `…_s3` | `opal-data-etfs` r/w + `opal-data-portal-v2` platinum write |
| `aws_iam_role_policy_attachment` | basic execution | |
| `aws_lambda_layer_version` | **`opal-trading-calendar-layer:1`** | first-party; built by copy-at-build-time |
| *(referenced, not managed here)* | `pandas-pyarrow-requests-layer:1` | shared third-party layer |
| `aws_cloudwatch_event_rule` | `etf-positioning-producer-daily` | **`cron(0 13 * * ? *)`** ENABLED |
| `aws_cloudwatch_event_target` | → the Lambda | |
| `aws_lambda_permission` | events invoke | |
| *(implicit)* log group | `/aws/lambda/etf-positioning-producer` | |

**Env:** `ETFS_BUCKET=opal-data-etfs`, `OPAL_ETFS_PUBLISH_GRANT=1` **(deliberately no gold/serve keys — code defaults equal the contract)**
**Source:** `data/etfs/scripts/gold/etf_positioning_gold.py` + `etf_positioning_publisher.py`
**Artifact:** `s3://opal-313476888478-lambda-artifacts/etfs-positioning/etf-positioning-producer.zip`

### 3.3 S3 — BUCKETS AND PREFIXES *(data plane; not created by these roots)*

| bucket | prefixes used | role |
|---|---|---|
| `opal-data-assets` | `trueshares/{FUND}/bronze/holdings/{YYYYMMDD}/`, `filepoint/…` | **BRONZE** — raw vendor bytes |
| `opal-data-etfs` | `silver/holdings/{date}.parquet`, `silver/netassets/…`, `bbg/{date}/`, `gold/{book,holding}/date=…/`, `gold/_manifests/` | **SILVER + BBG + GOLD** |
| `opal-data-portal-v2` | `platinum/etfs/positioning_data.json` | **PLATINUM / served** |
| `opal-313476888478-lambda-artifacts` | `etfs-positioning/`, `etfs-netassets/` | build artifacts |
| `opal-313476888478-lambda-layers` | `opal-trading-calendar-layer.zip` | layer source |

⚠ **`platinum/etfs/positioning_data.json` is a LIVE SERVED KEY.** Moving it is NEVER#3 (never-widen sign-off).

### 3.4 ⛔ NOT TERRAFORM-MANAGEABLE — the out-of-band leg
**Site-Z Windows Scheduled Tasks.** No AWS resource exists for these; they cannot enter any TF root.

| task | schedule (local → UTC) | role |
|---|---|---|
| `OPAL_BBGTML_daily_pull` | 07:00 → **11:00Z** | **writes `bbg/{date}/characteristics.parquet` + `fund_daily.parquet` — gold's hard dependency** |
| `OPAL_BBGTML_freshness_check` | 07:30 → 11:30Z | staleness check + BG spawn backstop ⚠ *fires AFTER the pull it would rescue* |
| `OPAL_BLOOMBERG-FreezeTripwire` | ~00:21 local | freeze tripwire |
| `Bloomberg Updater` | vendor | terminal updater |

**Script:** `integrations/bloomberg/pipeline/etf_daily_pull.py` (repo path — the task runs the working tree)

### 3.5 ADJACENT — measured, deliberately NOT in the group
| resource | why excluded |
|---|---|
| `opal-assets-silver-etf` + `opal-assets-silver-etf-sweep-daily` `cron(30 23)` | **UNMANAGED — in no TF root.** A silver sweep on `opal-data-assets`. If it joins, it must be **imported**, not recreated. |
| `etfs-canon` root — DynamoDB `etfs_ownership_daily`, `etfs-canon-fanin`, `cron(45 15)` | 49f ETF **ownership** product |
| `etfs-reports` root — EC2 reporter, SNS `reports_alerts`, `etfs-reports-orchestrator` | reporting rig |
| `bd-49f-/cot-/inf-etf-ownership-daily`, `etf-ownership-dashboard`, `wsd-49f-partner-held-etf-daily` | ownership, per-firm |
| `yang-generate-etf-returns`, `yang-generate-positioning` | yang/models pipeline |

---

## 4. RUNNING IT FROM THE LAPTOP

**State is remote (S3 backend), so either device can drive it — nothing is device-pinned.**

```
per root:  cd infra/aws/terraform/<root> && terraform init      # required per device, once
           terraform plan -detailed-exitcode                     # 0 = no changes, 2 = changes, 1 = ERROR
           .tools/safe-apply.sh -chdir=<root> apply              # NEVER bare apply (NEVER#4)
state keys:  etfs-netassets/tfstate   etfs-positioning/tfstate   etfs-reports/tfstate
```

⚠ **An uninitialised root returns `rc=1`, not `rc=0`.** Measured on `portal-content` from site Z at
04:1xZ — *"Backend initialization required."* **`rc=1` is neither "no changes" nor "changes pending"**
and is easy to misread as either.
⚠ **`.tools/terraform.exe` does NOT exist on site Z** (terraform resolves on PATH). Resolve the binary
per device; do not bake a path.
⚠ **CLAUDE.md Rule 26** says the apply runs on the device that owns the work. Driving these from the
laptop is a deliberate exception and should be stated as one.

---

## 5. IF YOU CONSOLIDATE — RECOMMENDED SHAPE

**Merge `etfs-netassets` + `etfs-positioning` into one `etfs_positioning` root.** They are genuinely
one pipeline (ingest → gold → platinum) and `etfs-positioning`'s state is small and fresh (created
2026-08-24). **Leave `etfs-canon` and `etfs-reports` alone** unless you want the ownership and
reporting products in too — that is a scope call, not a technical one.

**Do the cheap half regardless of the state decision:** a consistent `System = ETFS_POSITIONING`
`default_tags` across every resource, plus a declared manifest naming the out-of-band bbg leg. That
makes the pipeline **queryable and ownable as one group without touching state at all.**

⛔ **The state merge itself is `terraform state mv` across backends or import/remove.** On a
client-facing pipeline that is the step that destroys resources when it goes wrong. It wants its own
window, its own ledger, and a rollback plan — not a side effect of a tidying commit.

---

## 6. WHAT THIS SPEC IS NOT

- **Not a plan of record.** Nothing here is authorised to execute.
- **Not complete on `etfs-reports`** — I enumerated its declarations, not its EC2/SSM operational surface.
- **Not a claim the excluded items are wrong to exclude** — §3.5 states the grounds so the boundary is arguable.
- **`comp-estate` has NO `etfs` thread** (only `etf-reports`, counts 0/0/0/0), so this spec is currently the only single-place inventory of this pipeline.
