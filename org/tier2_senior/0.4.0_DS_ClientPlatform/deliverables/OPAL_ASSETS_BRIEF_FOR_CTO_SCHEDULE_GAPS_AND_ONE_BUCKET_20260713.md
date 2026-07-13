# BRIEF -> CTO: what is NOT running, what is NOT accruing, and the ONE BUCKET

**From:** 0.4.0_DS_ClientPlatform
**To:** 1.0.0_SA_CTO -- **for PRD + TO dispatch to the AEs**
**Date:** 2026-07-13
**Commissioned:** Andrew-direct.

> **ANDREW, VERBATIM -- THE CONSTRAINT ON THIS ENTIRE PRD:**
> ***"What I DO NOT WANT, is a bunch of process architecture bullshit, alarms, and other middleman non-value
> bullshit, getting in the way of creating a clean bucket, with clean structure, and doing some GOD DAMN ETL."***
>
> ## **THIS PRD ADDS NO NEW ALARMS, NO NEW GATES, NO NEW PROCESS LAYERS.**
> ## **IT CREATES ONE BUCKET, ONE STRUCTURE, AND TURNS THE ETL ON.**
> *Existing guards stay where they are. Nothing new gets bolted on. Any TO that produces a monitoring
> deliverable instead of a landed byte is off-brief.*

---

# 1. SCHEDULES THAT ARE NOT ENACTED

**Measured on live EventBridge, 2026-07-13. Not from memory.**

| rule | schedule | state | consequence |
|---|---|---|---|
| **`smartx-daily-export-trigger`** | `cron(0 14 ? * MON-FRI)` | 🔴 **DISABLED** | **THE SMARTX DAILY EXPORT IS OFF.** This is the **0824 "49F Schwab SmartX"** source -- the ~$1.62bn cohort. |
| **`inf-gold-incremental-daily`** | `cron(0 18)` | ⛔ **DISABLED** | **DELIBERATE (the INF hold).** Not a gap -- listed so nobody "fixes" it. |
| `inf-gold-full-on-bronze-complete` | event | ⛔ DISABLED | same hold. |
| `inf-canonical-prices-daily` | `cron(47 14)` | 🔴 **DISABLED** | canonical prices not refreshing. |
| `bd-49f-runner-daily` | `cron(0 2)` | ⛔ DISABLED | 49F/bd sovereign hold. Deliberate. |
| `bd-49f-fees-runner-daily` | `cron(30 22)` | ⛔ DISABLED | same. |
| `bd-gold-layer-monthly-trigger` | `cron(0 8 1 * ?)` | ⛔ DISABLED | same. |

**AND THE ONE THAT IS *ARMED BUT NEVER FIRES*:**

| `mdpf-daily-refresh-trigger` | **event, no cron** | ENABLED | Fires on `ObjectCreated` of `opal-data-inf/gold/meta/pipeline-complete.json`. **INF gold is DISABLED, so that key is never written, so mdpf NEVER REFRESHES.** `aggregate_aua` is frozen at **2026-07-10**. |

## 🔴 SCHEDULES THAT **DO NOT EXIST AT ALL**

| what | status |
|---|---|
| **0833 Black Diamond pull** | **NO RULE EXISTS.** `canonical-schwab-si2-download-schedule` (`cron(35 8,20)`) pulls **0824 ONLY**. `0.6.2_AE`'s puller is **BUILT, NOT DEPLOYED**. |
| **Schwab SILVER conversion (BOTH masters)** | **NO SCHEDULE. IT IS A MANUAL, HUMAN-RUN PROCEDURE** (the `/49-schwab-conv` 7-step skill, AE-invoked by hand). **The raw files download twice a day on a cron and then WAIT FOR A PERSON.** |
| **Cottonwood partner-total** | **NO SOURCE, NO COHORT, NO ROW.** `cot-etf-ownership-daily-schedule` gives ETF ownership only -- **there is no Cottonwood AUA figure anywhere in the estate.** |

---

# 2. DATA THAT IS NOT ACCRUING

| figure | expected | actual | why |
|---|---|---|---|
| **49F Schwab Black Diamond (0833)** | daily | **NOTHING. EVER.** | never ingested. `0.6.2`'s ETL not deployed. |
| **49F ETF ownership** (`opal-data-etfs/daily/49financial/`) | daily | **frozen at 2026-06-24** (~12 trading days) | the fan-in cron runs; its **49F input died**. |
| **ETF net assets** (DIVZ/IDVZ/PFOE/PFDE) | every trading day | **10 of 28 trading days MISSING**, incl. a **5-day contiguous blackout** | the real producer is a **Windows Task Scheduler job on Andrew's laptop**. `0.5.0_AE` is mid-migration. |
| **mdpf `aggregate_aua`** (feeds every cohort) | daily | **frozen at 2026-07-10** | downstream of the INF hold. **Correctly idle, not broken.** |
| **SmartX 0824 export** | weekdays 14:00Z | **OFF** | `smartx-daily-export-trigger` **DISABLED**. |
| **Cottonwood AUA** | daily | **does not exist** | no source, no cohort. |
| **Schwab silver (both masters)** | daily | **only when a human runs it** | manual procedure. |

> ### **NET: of the 14 cohorts, the ONLY figures accruing automatically and freshly today are the Inflection ones and the ETF fund-level numbers -- and the ETF numbers are missing a third of their trading days.**

---

# 3. THE ONE BUCKET

**TODAY THE ASSET PICTURE IS SMEARED ACROSS SIX BUCKETS + A DYNAMO TABLE:**
```
opal-data-schwab     0824 raw; FOUR competing layout generations; no master in the key
opal-data-etfs       ETF net assets + per-partner ownership
opal-data-inf        Orion / Eclipse (Inflection)
opal-data-cot        Cottonwood positions cube
opal-data-bd         legacy 49F transaction engine (held; on the way out)
opal-data-portal-v2  mdpf served aggregate
DynamoDB             opal-assets-daily-aua
```
**`opal-data-assets` DOES NOT EXIST.** *(Verified: `NoSuchBucket`.)*

## THE TARGET -- ONE BUCKET, THREE LAYERS, NOTHING ELSE

```
s3://opal-data-assets/
│
├── bronze/                                    RAW. BYTE-FOR-BYTE. WHATEVER THE SOURCE SHIPPED.
│   ├── schwab/08242234/{TYPE}/{YYYY-MM-DD}/CRS{date}.{EXT}          "49F Schwab SmartX"
│   ├── schwab/08335338/{TYPE}/{YYYY-MM-DD}/CRS{date}.{EXT}          "49F Schwab Black Diamond"
│   ├── orion/inflection/{TYPE}/{YYYY-MM-DD}/...                     Inflection positions
│   ├── eclipse/inflection/{TYPE}/{YYYY-MM-DD}/...                   Inflection models
│   ├── cot/cottonwood/{TYPE}/{YYYY-MM-DD}/...                       Cottonwood
│   └── etfs/{issuer}/{TICKER}/{YYYY-MM-DD}/...                      TrueShares, Pathfinder
│
├── silver/                                    CLEAN PARQUET. DEDUP + DTYPE ONLY.
│   └── {source}/{account_or_partner}/{TYPE}/date=YYYY-MM-DD/data.parquet
│                                              Every vendor column preserved. Nothing slimmed.
│
└── gold/                                      DynamoDB  opal-assets-daily-aua   (PK = run_date)
                                               1 row per cohort per day. Organized by date.
```

**FIVE RULES. THAT IS THE WHOLE DESIGN:**
1. **`bronze/` is raw.** Byte-for-byte. **No parquet in bronze, ever** -- parquet coerces schema at ingest and destroys the raw.
2. **`silver/` is parquet.** Dedup + dtype standardization **only**. No field slimming, no dropping vendor columns.
3. **`gold/` is the Dynamo table**, one row per cohort per day, keyed by date.
4. **The ACCOUNT/MASTER is in the KEY.** `08242234` and `08335338` are **separate folders and never commingle.**
   *(Today's `opal-data-schwab/silver/ACC/date=.../` has **no master in the key at all** -- it physically cannot
   keep them apart.)*
5. **The master is read from the file's `H1` header, never inferred from the folder.** *(`H1|SCHWAB|0008335338|...`)*

---

# 4. TOs TO DISPATCH

| # | TO | assignee | deliverable -- **a landed byte, not a document** |
|---|---|---|---|
| **1** | **Create `opal-data-assets`** + the bronze/silver/gold prefixes. Terraform. | **AE (CloudOps)** | the bucket exists |
| **2** | **Deploy the 0833 puller** (built, not deployed) + **schedule it**. | **`0.6.2_AE_PartnerETL`** | 0833 bronze accruing daily |
| **3** | **Re-enable `smartx-daily-export-trigger`** (0824). Find out why it was disabled first. | **AE (CloudOps)** | 0824 exporting weekdays |
| **4** | **SCHEDULE the Schwab silver conversion** -- both masters. **It is a manual human procedure today.** | **AE + DS** | silver parquet lands daily, unattended |
| **5** | **Finish the ETF net-assets laptop->cloud migration.** | **`0.5.0_AE_OpalETL`** | 0 missing trading days |
| **6** | **Fix the 49F ETF-ownership input** (frozen 06-24). | **AE** | `daily/49financial/` current |
| **7** | **Source a Cottonwood AUA figure.** None exists. | **AE + DS** | a Cottonwood partner-total row |
| **8** | **Point the emitter at `opal-data-assets`;** migrate the six-bucket reads. | **DS (me)** | one bucket in, Dynamo out |

**NOT IN SCOPE, AND DELIBERATELY SO:** new alarms, new gates, new monitoring, new process layers, cleanup of the
legacy `opal-data-schwab` prefixes (that is a **deletion-class action** -- inventory it, do not touch it), and any
reconciliation of the 49F figures against each other (**Andrew has ruled the summing question out of scope three
times; it is a read-time query**).

---

# 5. THE ONE THING THAT MUST NOT HAPPEN WHILE DOING THIS

**`mdpf-daily-refresh-trigger` is ENABLED and ARMED** on `ObjectCreated` of
**`s3://opal-data-inf/gold/meta/pipeline-complete.json`**.

> **A single `aws s3 cp` of that ~40-byte key DISPATCHES THE HELD INF CHAIN** -- bypassing the disabled cron
> entirely. It will look like *"unfreezing the AUM number."* **Nobody writes that key.** It is the one line in this
> brief that is a prohibition rather than a task, and it is the only one.
