# Portal Time Machine — Research & Architecture PRD

**Project code:** `DRFR_PTMCH`
**Macro code:** `DRFR` (DataRefresh)
**Author:** 1.0.0_SA_CTO
**Date:** 2026-03-10
**Status:** Research Phase — AE audit required before implementation design is finalized

---

## 1. Problem Statement

The DataRefresh page has a "Rollback" button in the History tab that calls
`POST /data-refresh/rollback` with an execution ID. That endpoint does re-process
the yang pipeline from archived PKL files — but it is scoped only to yang pipeline
outputs. It does not touch BD pipeline data (advisor intelligence), news/trending
data, FRED data, or market-overview data. It also depends on S3 versioning being
enabled on `opal-data-portal-v2` for the preferred version-based path — which has
not been confirmed in production.

The goal of this project is to replace the narrow per-execution rollback with a
**portal-wide Time Machine**: given a target date (e.g., "2026-03-05"), restore
every portal data source to its state as of 5:00 PM ET on that date, across all
pipelines.

Use case: "What did the portal look like when I showed it to a client on March 5?"

---

## 2. What We Know — Architecture Inventory

### 2.1 Yang Pipeline (opal-data-portal-v2)

**Input files** (uploaded via DataRefresh page):
| File type | S3 path (uploads) | Archived to |
|-----------|------------------|-------------|
| `data_*.pkl` | `uploads/{filename}` | `data-refresh/archive/{execId}/data_{version}.pkl` |
| `model_*.pkl` | `uploads/{filename}` | `data-refresh/archive/{execId}/model_{version}.pkl` |
| `*.xlsx` (peer, attribution, CMA) | `uploads/{filename}` | `data-refresh/archive/{execId}/` |
| `manifest.json` | `uploads/manifest.json` | `data-refresh/archive/{execId}/metadata.json` |

**Processed inputs** (retained after pipeline):
| File | S3 path |
|------|---------|
| Versioned data.pkl | `benchmarks/data_{version}.pkl` |
| Versioned model.pkl | `benchmarks/model_{version}.pkl` |
| Current pointer | `benchmarks/LATEST.json` |

**JSON outputs** (overwritten on each run):
All generator Lambdas write to `json/latest/{file_type}.json` in `opal-data-portal-v2`.
Known file types from manifest: `data_pkl`, `model_pkl`, `peer_excel`,
`attribution_excel`, `cma_excel`, `saa_excel` — but the actual `json/latest/`
prefix likely contains many more files (positioning, benchmark-returns, volatility,
factor-tilts, valuation, macro, correlation, etc.). Full inventory unknown —
must be audited.

**Versioning/archive infrastructure** (already built):
- `yang-capture-output-versions` Lambda runs after pipeline success: scans
  `json/` prefix, captures S3 `VersionId` of all files modified in last 10 min,
  saves to `data-refresh/archive/{execId}/outputs-manifest.json`.
- `handle_rollback` in `opal-data-refresh-api` Lambda: reads `outputs-manifest.json`,
  calls `copy_object` with `CopySourceVersionId` to restore each file's exact version.
- **Critical dependency**: this only works if S3 versioning is enabled on
  `opal-data-portal-v2`. This has NOT been confirmed.

**DynamoDB** (unknown scope):
- `yang-ingest-dynamodb` Lambda writes something to DynamoDB. Table name and
  item structure are unknown. Rollback of DynamoDB state is not implemented.

**Timestamp convention:**
The `yang-generate-manifest` Lambda generates 5pm ET timestamps from `data_as_of`
date strings. This is the canonical "data as of date" for each upload.

---

### 2.2 BD Pipeline (opal-data-bd)

**Gold outputs** (overwritten on each run):
All advisory intelligence data written to `opal-data-bd/gold/`. Key files:

| File | Writer | Cadence |
|------|--------|---------|
| `timeseries_chart.json` | `bd-portal-publisher` Lambda | After each gold rebuild |
| `architect_leaderboard.json` | `bd-portal-publisher` | After each gold rebuild |
| `implementor_leaderboard.json` | `bd-portal-publisher` | After each gold rebuild |
| `clients_tab.json` | `bd-portal-publisher` | After each gold rebuild |
| `flows_chart.json` | `bd-portal-publisher` | After each gold rebuild |
| `advisor_rolling_flows.json` | `bd-portal-publisher` | After each gold rebuild |
| `client_performance.parquet` | `bd-portal-publisher` | After each gold rebuild |
| `client_dimension.parquet` | `bd-portal-publisher` | After each gold rebuild |
| `clients/{z_id}.json` | `bd-portal-advisor-publisher` | After each gold rebuild |
| `client_detail/{...}` | various | After each gold rebuild |
| `partner_analytics/header_metrics_quarterly.json` | EC2 gold scripts | After each gold rebuild |

Gold rebuild runs on `bd-gold-layer-runner` EC2 (manual or scheduled — exact
cadence unknown). `bd-portal-publisher` is triggered by S3 event on
`opal-data-bd/gold/pipeline-complete.json`.

**No snapshot mechanism exists.** Gold files are overwritten in-place. No
historical state is preserved. Rolling back BD data requires either:
a) S3 versioning enabled on `opal-data-bd`, or
b) A snapshot archive written at the end of each gold rebuild.

---

### 2.3 News/Trending Data (opal-data-portal-v2)

**Output:** `json/semantic-trending/latest.json`
**Source:** DynamoDB table `semantic-news-trending-daily`, keyed by `date` (YYYY-MM-DD)
**Refresh cadence:** 9:20 AM ET daily via `semantic-trending-topics-portal-publisher` Lambda

**This data source has an inherent time machine**: the DynamoDB table is keyed by
date. To show "news as of 2026-03-05", we just query DynamoDB for `date = 2026-03-05`
and rebuild `latest.json`. No S3 versioning needed. Publisher Lambda already has the
query logic.

---

### 2.4 FRED / Market Data (unknown)

`yang-refresh-fred-cache` Lambda updates FRED data. Unclear whether it writes to
`json/latest/` (captured by yang archive) or to a separate path outside the archive
scope. Must be audited.

---

### 2.5 Market-Overview Pipeline (unknown)

`MKOV` macro. Separate pipeline. Unknown S3 write pattern. Must be audited by
`0.5.0_AE_OpalETL`.

---

### 2.6 SmartX Pipeline (unknown)

`SXPL` macro. Separate pipeline. Unknown relevance to time machine (portfolio
analytics, not market data). May not require rollback depending on data semantics.
Must be scoped by AE audit.

---

## 3. Time Machine Design Hypothesis

The following is the CTO's architectural hypothesis, to be validated or corrected
by AE findings. AEs should flag any assumption that conflicts with production reality.

### 3.1 Target State

A Time Machine invocation — `POST /portal/time-machine { "target_date": "YYYY-MM-DD" }` —
produces the same portal state that existed at 5:00 PM ET on `target_date`, across
all data sources simultaneously. It is exposed in the DataRefresh page's History tab
as a "Travel to date" control replacing (or extending) the per-execution Rollback button.

### 3.2 Layer 1 — Yang Outputs (opal-data-portal-v2/json/)

**Mechanism: S3 version ID restore**

The `yang-capture-output-versions` Lambda already captures version IDs of all
`json/` files after each run. The time machine selects the execution whose
`dataAsOfDate` is closest to (but not after) `target_date` AND whose
`pipeline_started_at` is before or equal to 5pm ET on `target_date`.

Steps:
1. Scan `data-refresh/archive/*/outputs-manifest.json` to find the matching execution.
2. For each file in `outputs.keys()`, call `copy_object` with `CopySourceVersionId`.
3. Update `benchmarks/LATEST.json` to point to the PKL version from that execution.
4. Invalidate CloudFront for `/api/public/*`.

**Prerequisite:** S3 versioning must be enabled on `opal-data-portal-v2`.
Without versioning, `VersionId` is `null` in all captured manifests and restore
is impossible. This is the single hardest dependency to confirm.

**Known gap:** `yang-ingest-dynamodb` DynamoDB data cannot be version-restored
via S3 mechanisms. If this table is query-time (portal fetches from DynamoDB on
each request), rolling back those items may be required. If it's only used during
pipeline processing (not portal reads), it can be skipped. Must be confirmed.

### 3.3 Layer 2 — BD/Advisory Intelligence (opal-data-bd/gold/)

**Mechanism: Snapshot archive + copy-back**

Since gold files are overwritten in-place, a snapshot pattern must be added to the
gold rebuild. At the end of each successful gold rebuild, the `bd-portal-publisher`
(or a new post-publisher Lambda) copies the full `gold/` output set to:

```
opal-data-bd/snapshots/{YYYYMMDD}/
  timeseries_chart.json
  architect_leaderboard.json
  ...
  clients/{z_id}.json
  ...
```

Where `YYYYMMDD` = the data-as-of date of that rebuild.

Time machine restore: copy `snapshots/{target_date}/` back to `gold/`, then
trigger `bd-portal-publisher` (by writing `pipeline-complete.json`), then
invalidate CloudFront for `/api/scoped/advisor-intelligence/*`.

**Alternative**: enable S3 versioning on `opal-data-bd` and use the same
version ID mechanism as Layer 1. Simpler code, but versioning on a large bucket
with many daily-overwritten files accumulates cost quickly. AE to assess.

**Risk**: No historical snapshots exist yet. The Time Machine cannot go back to
dates before this project deploys the snapshot mechanism. Needs a clear
"Time Machine available from {date}" indicator in the UI.

### 3.4 Layer 3 — News/Trending (DynamoDB)

**Mechanism: Date-keyed re-publish**

`semantic-news-trending-daily` table is already keyed by date. The
`semantic-trending-topics-portal-publisher` Lambda can be parameterized to accept
`target_date` and query that date's data instead of `get_latest_trending_date()`.

Time machine: invoke the publisher Lambda with `{ "target_date": "YYYY-MM-DD" }`.
No S3 versioning needed.

### 3.5 Layer 4 — FRED / Market-Overview / SmartX

Unknown. AE audit required. Three possible outcomes per data source:
- **Date-keyed DynamoDB** → re-publish with target date (same as Layer 3)
- **S3 json/latest/** file (captured by yang archive) → already handled by Layer 1
- **Out-of-scope** → data is static or updates on a different cadence where rollback is not meaningful

---

## 4. Open Questions — AE Discovery Required

### For 0.7.0_AE_CloudOps

1. **Is S3 versioning enabled on `opal-data-portal-v2`?** Check via
   `aws s3api get-bucket-versioning --bucket opal-data-portal-v2`. If not enabled,
   every existing `outputs-manifest.json` has `null` VersionIds and the preferred
   rollback path is broken. What is the safe enabling procedure (no in-flight pipeline)?
2. **Is S3 versioning enabled on `opal-data-bd`?** Same check.
3. **Versioning cost implications**: How many unique objects are in `json/` on
   `opal-data-portal-v2`? At ~weekly yang runs, how many versions accumulate per
   year? What lifecycle rule would bound this cost (e.g., retain 90 days)?
4. **DynamoDB tables used by yang pipeline**: List all DynamoDB tables the yang
   pipeline reads from OR writes to. For each write-path table, determine:
   - Is Point-in-Time Recovery (PITR) enabled?
   - Does the portal frontend read from this table at request time?
   - If yes: is per-item restore required for the Time Machine?
5. **CloudFront invalidation scope**: The current rollback invalidates `/api/public/*`.
   Does this cover ALL portal-served data (yang + BD + news + market-overview)?
   Or does BD data serve via `/api/scoped/*` which requires a separate invalidation?
   Map the full CloudFront path → origin → S3 bucket routing.
6. **IAM**: Does the `opal-data-refresh-api` Lambda have permissions to read from
   `opal-data-bd`? Does it have permissions to write to `opal-data-bd/gold/` for the
   copy-back step? Document any IAM gaps.

### For 0.5.0_AE_OpalETL

1. **Full `json/latest/` inventory**: List all files currently in
   `opal-data-portal-v2/json/latest/`. These are the files the yang archive must
   capture. Confirm `yang-capture-output-versions` is actually running post-pipeline
   (check CloudWatch Logs for recent `capture-output-versions` invocations).
2. **Are `outputs-manifest.json` files actually being written?** Check
   `opal-data-portal-v2/data-refresh/archive/` — do recent executions have an
   `outputs-manifest.json`? Do those manifests have non-null `versionId` values?
   This is the single most critical fact for the Time Machine feasibility.
3. **`yang-ingest-dynamodb` scope**: Read the Lambda source code and identify:
   - Which DynamoDB table(s) does it write to?
   - What items does it write (table, PK/SK structure, data)?
   - Does the portal read from this table at query time (portal fetch) or
     only during pipeline processing?
4. **`yang-refresh-fred-cache` output**: What S3 key(s) does it write?
   Is it under `json/latest/` (covered by yang archive) or a separate prefix?
5. **Market-overview pipeline**: What S3 bucket and prefix does it write to?
   What is the refresh cadence (daily, weekly, on-demand)?
   Is output under `json/` in `opal-data-portal-v2` (potentially captured by
   yang archive) or a separate path?
6. **Yang pipeline step sequence**: Confirm the Step Functions definition lists
   `yang-capture-output-versions` as a step (and it is NOT skipped on partial runs).
   Specifically: does it run before or after `yang-generate-manifest`?

### For 0.6.0_AE_PartnerETL

1. **Full `opal-data-bd/gold/` inventory**: List all files written by the gold
   rebuild pipeline. Include `partner_analytics/`, `clients/`, `advisors/`,
   `timeseries/` subdirectories. Approximate sizes and file count.
2. **Gold rebuild cadence**: How often does `bd-gold-layer-runner` run the full
   gold rebuild? Is it on a schedule or manually triggered? What event triggers
   `bd-portal-publisher` (S3 notification on `pipeline-complete.json`)?
3. **Snapshot feasibility**: How large is the full `gold/` output set (total GB)?
   At `N` rebuilds per week, how much S3 storage does 90-day snapshot retention require?
   Is this within acceptable cost bounds?
4. **`bd-portal-publisher` parameterization**: Does the Lambda read its source
   path from an environment variable, or is `opal-data-bd/gold/` hardcoded?
   What is the blast radius of pointing it at a snapshot path?
5. **`bd-portal-advisor-publisher` scope**: Does it also need snapshot support,
   or is its output derived from `gold/` files that `bd-portal-publisher` already
   handles?
6. **Existing historical data**: Is there any existing historical gold data in S3
   (e.g., from manual backups, old test runs)? This determines the earliest date
   the Time Machine can serve for BD data.

---

## 5. Implementation Scope (Post-Discovery)

The following is not actionable until AE audit findings are in. It defines the
work this project will produce.

### Phase 1 — Enable Versioning + Confirm Archive (0.7.0, 0.5.0)
- Enable S3 versioning on `opal-data-portal-v2` with 90-day lifecycle rule
- Confirm `yang-capture-output-versions` is running and capturing non-null version IDs
- Fix any gaps in the capture scope (e.g., FRED cache, market-overview outputs)

### Phase 2 — Yang Time Machine Lambda (0.5.0)
- New Lambda `yang-time-machine`: accepts `target_date`, finds matching execution,
  restores all `json/latest/` files via version IDs, updates `LATEST.json`, invalidates CloudFront
- Add `GET /data-refresh/archive` endpoint to list available restore points

### Phase 3 — BD Snapshot Mechanism (0.6.0)
- Add post-publish snapshot step to BD gold rebuild: copy `gold/` → `snapshots/{YYYYMMDD}/`
- New Lambda `bd-time-machine`: copies snapshot back to `gold/`, triggers publisher, invalidates

### Phase 4 — News Re-publish (0.5.0 or new Lambda)
- Parameterize `semantic-trending-topics-portal-publisher` to accept `target_date`

### Phase 5 — Portal Time Machine Orchestrator Lambda + Frontend (0.5.0 + 0.4.0_RD)
- New Lambda `portal-time-machine`: accepts `target_date`, invokes Layer 1-4 restores in parallel
- New frontend control in DataRefresh/HistoryTab: date picker → "Travel to this date"
- Show "Time Machine active" banner across all portal pages when viewing historical data

---

## 6. What Is Explicitly Out of Scope

- **SmartX pipeline**: portfolio construction data; does not represent "market state at a date"
  in a meaningful sense for client presentations. Descoped unless AE finds otherwise.
- **DynamoDB rollback at the item level**: only feasible if PITR is enabled and the portal
  reads from DynamoDB at request time (not pre-computed to JSON). If yang-ingest-dynamodb
  only feeds pipeline processing, skip.
- **Backward compatibility for dates before project launch**: the Time Machine will have a
  "earliest available date" per data source. UI must surface this clearly.

---

## 7. Deliverables from AE Discovery Phase

Each AE produces a structured findings document at:
```
{ae_agent_folder}/deliverables/DRFR_PTMCH.{layer}.discovery-findings.md
```

Format per document:
- Confirmed facts (CLI output, CloudWatch evidence)
- Assumptions that are WRONG (flag with correction)
- Assumptions that are CORRECT (confirm)
- Blockers or risks not covered by the PRD
- Estimated storage / cost impact of the proposed mechanism

Findings feed into an updated implementation PRD (Phase 1b).
