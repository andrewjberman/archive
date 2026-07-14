# OPAL_ASSETS MASTER PLAN -- the grand consolidation, pipeline by pipeline

**From:** 0.4.0_DS_ClientPlatform
**To:** 1.0.0_SA_CTO -- **for PRD + TO dispatch. ANDREW: "this is the highest priority now."**
**Date:** 2026-07-13
**Every status below is MEASURED (live EventBridge / live S3 / source), not recalled.**

> **THE MANDATE (Andrew, verbatim):** *"a grand consolidation... an opal-data-assets bucket that basically takes
> all of these things, brings them into one place, organizes them religiously, and is hyperrobust... smartx,
> orion/eclipse, the schwab ec2 box, etf issuers, black diamond (for cottonwood), all of it, accruing into a
> dedicated opal-data-assets bucket, bronze raw, silver parquet, gold master table."*
> **Standing constraint:** no new alarms, no gates, no process layers. **ONE bucket. ETL ON.**

---

# 1. THE MASTER MATRIX -- every pipeline, every layer, today

`HAVE` = exists and accrues automatically. `STALE` = exists, not current. `MANUAL` = exists, human-run.
`NONE` = does not exist. `HELD` = deliberately stopped (not this plan's to fix).

| # | pipeline | feeds (cohorts) | PULL today | BRONZE | SILVER | GOLD row | schedule to CREATE/FIX |
|---|---|---|---|---|---|---|---|
| 1 | **Schwab 0824 SmartX** (SI2 EC2 box) | `49f_schwab_custody` 1621.25 + RPS basis for 49F ETF ownership | 🔴 **CRON FIRES, PULL FUNCTIONALLY DEAD since 07-02** (rc=0 landing NOTHING -- CTO correction 00:07Z, grounded by 0.6.2 vs Schwab's live catalogue, 5,966 files; IAM apply GO for the rebuilt puller sent) | 🟡 HAVE thru 07-02 (wrong bucket, flat keys, no master) | 🔴 **MANUAL** (`/49-schwab-conv`, 7 steps, human-run) | ✅ HAVE (stale) | **UNBLOCK THE REBUILT PULLER (in flight)** + SCHEDULE THE SILVER CONVERSION + retarget bronze -> one bucket |
| 2 | **Schwab 0833 Black Diamond** | `49f_schwab_account` ~1.71b | 🔴 **NONE** (puller BUILT, not deployed) | 🔴 NONE (85-file backfill parked) | 🔴 NONE (CBUGL converter = spec only) | 🔴 **NO ROW** (disclosed `incomplete`) | **DEPLOY + SCHEDULE the puller; build CBUGL silver on first bytes** |
| 3 | **SmartX exporter** (models) | 5 term models + 2 SMAs + platform view | 🔴 **DISABLED** (`smartx-daily-export-trigger`, weekdays 14:00Z) | 🔴 NONE (exports go straight to Dynamo, no raw kept) | 🔴 NONE | ✅ HAVE (stale 07-06 via mdpf G1) | **RE-ENABLE the trigger** (find out why it was disabled) **+ add raw drop to bronze** |
| 4 | **Orion (Inflection)** | `inflection_models` inputs, positions/txn/accounts | ✅ RUNS (5 pulls, 13:17-13:47Z) | ✅ HAVE (in `opal-data-inf`) | ✅ HAVE (event-driven inf silver chain) | ✅ HAVE, fresh 07-10 | none -- **MIRROR bronze into one bucket** (router) |
| 5 | **Eclipse (Inflection models)** | model assignments (the $11.4M IWM->Opal conversion lives here) | ✅ RUNS daily | ✅ HAVE (in `opal-data-inf`) | partial (JSON, not parquet) | ✅ HAVE | **MIRROR in + add parquet conversion** to the registry |
| 6 | **Black Diamond / cot (Cottonwood)** | Cottonwood ETF ownership; **AUA total = NOWHERE** | ✅ RUNS (nightly cube + `cron(30 10)` ownership) | ✅ HAVE (in `opal-data-cot`) | ✅ HAVE (cube) | 🟡 ETF ownership only -- **NO AUA COHORT EXISTS** | **MIRROR in + SOURCE A COTTONWOOD AUA FIGURE** (from the cube; none exists today) |
| 7 | **ETF issuers** (TrueShares DIVZ/IDVZ, Pathfinder PFOE/PFDE) | 4 `etf_*` net-assets cohorts + FLOAT | 🟡 **LAPTOP Task Scheduler** (10/28 trading days MISSING); cloud producer mid-migration (`0.5.0`, parity 07-14/15) | 🟡 building (cloud, bronze-first) | 🟡 quarantined `_cloudprobe/` until parity | ✅ HAVE (gappy) | **FINISH laptop->cloud; RETARGET landing -> one bucket NOW, pre-cutover** |
| 8 | **ETFS_CANON fan-in** (per-partner ETF ownership -- derived) | `etf_*__held_{partner}` x 3 partners, + FLOAT residual | ✅ RUNS `cron(45 15)` | n/a (derived -- GOLD rows, not bronze) | n/a | 🟡 HAVE; **49F input FROZEN 06-24** (~12 trading days) | **FIX THE 49F INPUT** (the fan-in runs; its input died) |
| 9 | **mdpf aggregate** (emitter's upstream) | all 49F/inflection blocks | ⛔ **HELD** (event trigger armed, INF gold DISABLED -> never fires; frozen 07-10) | -- | -- | -- | **NOTHING. Deliberate. Listed so nobody "fixes" it.** |
| 10 | **Gold emitter** -> `opal-assets-daily-aua` | ALL cohort rows, 1/day | ✅ RUNS `cron(15 17)` | -- | -- | ✅ writes daily | **REPOINT reads -> one bucket; ADD 0833 + Cottonwood-AUA cohorts; daily snapshot dump** |

## HAVE vs DON'T HAVE, in one look
```
HAVE (automatic, fresh):     Orion bronze+silver - Eclipse - cot cube + Cottonwood ETF ownership -
                             Inflection cohort rows - the Dynamo gold table + emitter - 0824 RAW pull
HAVE BUT BROKEN/PARTIAL:     ETF net assets (1/3 of trading days missing, laptop) - 49F ETF ownership
                             (frozen 06-24) - SmartX models (source trigger DISABLED, stale via G1)
MANUAL WHERE IT MUST BE AUTO: Schwab silver conversion (BOTH masters) -- raw lands 2x/day, then WAITS FOR A HUMAN
DON'T HAVE AT ALL:           0833 (pull, bronze, silver, gold row) - Cottonwood AUA (any layer) -
                             SmartX raw bronze - the opal-data-assets bucket itself (NoSuchBucket, verified)
HELD ON PURPOSE:             INF gold -> mdpf refresh (the hold; out of this plan's scope)
```

---

# 2. THE ONE BUCKET -- structure (religiously uniform)

```
s3://opal-data-assets/                      grammar: {layer}/{source}/{scope}/{feed}/{date}/
  bronze/                                   RAW, byte-for-byte. NEVER parquet. Vendors only.
    schwab/08242234/{TYPE}/{YYYY-MM-DD}/CRS{yyyymmdd}.{EXT}
    schwab/08335338/{TYPE}/{YYYY-MM-DD}/{m}.CRS{date}.{CODE}.zip
    smartx/49financial/exports/{YYYY-MM-DD}/{raw export}
    orion/inflection/{feed}/{YYYY-MM-DD}/...
    eclipse/inflection/models/{YYYY-MM-DD}/portfolios_full.json
    blackdiamond/cottonwood/{feed}/{YYYY-MM-DD}/...
    trueshares/{DIVZ|IDVZ}/{YYYY-MM-DD}/...      pathfinder/{PFOE|PFDE}/{YYYY-MM-DD}/...
  silver/                                   CLEAN PARQUET. Dedup + dtype ONLY. Every vendor column kept.
    {source}/{scope}/{feed}/date=YYYY-MM-DD/data.parquet
  gold/                                     DynamoDB opal-assets-daily-aua (1 item/cohort/day, by run_date)
    snapshots/{run_date}.parquet            daily table dump -> the bucket is self-contained
```
**Laws:** master/partner/ticker **in the key** · 0824 and 0833 are **separate folders, never commingled** ·
Schwab identity read from the file's **H1 header**, never the folder (unreadable -> quarantine, no default) ·
derived series (per-partner ownership, float) are **GOLD rows only** -- nothing appears twice · an absent day is
**ABSENT** (no roll-forward, no zeros) · every writer verifies its landed object (`exit 0` = bytes in S3) ·
everything idempotent (skip / `--force` / `--since`).

**ONE new component: the ingest-router.** Event-driven copy Lambda, static prefix map, mirrors the
already-running Orion/Eclipse/cot bronze in (one-way fan-in -- the ETFS_CANON precedent; per-source READ grants,
assets WRITE). Never transforms; head-object verifies. **Each native retarget retires one map row.** No
schedulers, no orchestrator, no queue. Silver is **event-driven off bronze** (one parser registry keyed by
source+TYPE) -- **no cron anywhere downstream of the pulls.**

---

# 3. THE SCHEDULE BOARD

**RUNS TODAY (keep, retarget where noted):**
```
08:35+20:35Z  canonical-schwab-si2-download    0824 pull            -> retarget landing to one bucket
10:30Z        cot-etf-ownership-daily          Cottonwood ownership -> keep; mirror bronze in
13:17-13:47Z  inf-api-* x5                     Orion pulls          -> keep; mirror bronze in
15:45Z        etfs-canon-fanin-daily           per-partner fan-in   -> keep; FIX its dead 49F input
17:15Z        opal-assets-daily-emitter-daily  gold writer          -> repoint reads to one bucket
22:00Z        etfs-netassets-daily             ETF cloud side       -> becomes real at cutover
```
**CREATE (does not exist):**
```
0833 puller schedule            daily, same Schwab window           0.6.2
Schwab silver conversion        daily, event-driven off bronze      AE deploys, DS authors (BOTH masters)
SmartX raw->bronze drop         with the re-enabled export          AE
silver parser registry          event-driven off bronze/            DS
gold snapshot dump              daily after emitter                 DS
ingest-router                   event-driven (no schedule)          AE
```
**RE-ENABLE (exists, off):** `smartx-daily-export-trigger` (weekdays 14:00Z) -- **diagnose why it was disabled
first**, then flip.
**DO NOT TOUCH:** `inf-gold-*` (the hold) · **`inf-canonical-prices-daily` -- CTO RULED 00:07Z: HELD, not a gap**
(INF-domain; the functional test is "would this advance the INF chain," not "does the row say INF") ·
`bd-49f-*` (sovereign hold) · and **nobody writes `opal-data-inf/gold/meta/pipeline-complete.json`** -- the
armed mdpf trigger fires on that exact key.

> **CORRECTION LOG (CTO, 2026-07-14T00:07Z):** row 1's pull was listed "RUNS" -- true of the CRON, false of the
> PULL (functionally dead since 07-02, rc=0 landing nothing). **Corrected above so "RUNS" is never quoted as
> freshness.** *The cron firing is a statement about a SCHEDULER; only landed bytes are a statement about a PULL --
> a producer cannot report its own death.*

---

# 4. SEQUENCING + TOs (every deliverable = a LANDED BYTE)

**P1 -- this week: everything accruing.**
| TO | what | assignee |
|---|---|---|
| 1 | Terraform `opal-data-assets` + prefixes + router IAM | AE CloudOps |
| 2 | Ingest-router live (Orion/Eclipse/cot mirroring in) | AE CloudOps |
| 3 | 0833 puller deployed -> `bronze/schwab/08335338/` + scheduled; backfill copied in | 0.6.2_AE_PartnerETL |
| 4 | ETF cloud producer landing retargeted -> one bucket (pre-cutover, now) | 0.5.0_AE_OpalETL |
| 5 | SmartX trigger diagnosed + re-enabled + raw bronze drop | AE CloudOps |

**P2 -- convert + native landings.**
| 6 | Silver parser registry (Schwab CRS + **CBUGL** on first 0833 bytes, Orion, Eclipse, cot, issuers) -- Rule 17, event-driven | DS (me) |
| 7 | Schwab silver conversion SCHEDULED (kills the manual 7-step) | AE + DS |
| 8 | 0824 SI2 box retargeted to land natively in one bucket; router row retired | AE CloudOps |
| 9 | Fix the 49F ETFS_CANON input (frozen 06-24) | AE |
| 10 | Source the Cottonwood AUA figure from the cot cube -> new cohort | AE + DS |

**P3 -- one bucket is the only input.**
| 11 | Emitter reads ONLY `opal-data-assets`; 0833 + Cottonwood-AUA cohort rows live; daily gold snapshot | DS (me) |
| 12 | Legacy prefixes inventoried (NOT cleaned -- deletion-class; untouched) | DS doc only |

**OUT OF SCOPE, DELIBERATELY:** new alarms/monitoring/gates · legacy cleanup · 49F bucket reconciliation (ruled
out of scope 3x; a read-time query) · anything advancing the INF chain.

---

**DS commitments in this plan: TOs 6, 7(author), 10(gold side), 11, 12 -- started the moment CTO dispatches.**
