# Task Order: ADVI_INFSHIP.B5 — Transactions Pull Fix and Daily Integration

**Project:** ADVI_INFSHIP (Inflection Bronze Pipeline)
**Assigned to:** 0.4.0_DS_ClientPlatform~D
**Authored by:** 0.6.1_AE_PartnerETL
**Date:** 2026-04-29
**Priority:** HIGH — blocks daily incremental bronze completeness for Inflection pipeline

---

## Background

The Inflection bronze runner (`inf-bronze-runner` EC2, `orchestrator.py`) pulls 7 daily dims
via `concurrent.futures`. Six succeed; **transactions has never succeeded** — it has been
failing since the runner was first deployed.

`data/orion/manual_api/pull_inflection_transactions.py` (authored by 0.7.0_AE_CloudOps_B,
ADVI_INFSHIP.B1) uses `POST /api/v1/Reporting/Custom/28198/Generate/csv`. AE 0.6.1
diagnosed today (2026-04-29):

- The original body format (`parameters[]` with `name`/`value`) causes HTTP 500.
- The correct format is `prompts[]` with `id`/`code`/`value` (all 5 prompts required,
  including `@type` and `@selectedType`). With the corrected format, the endpoint
  returns HTTP 201 + Location header as expected.
- **However:** Custom Report 28198 ("Homepage Daily Transactions - Rep") returns
  header-only CSV (0 data rows) for ALL parameter combinations including all reps
  (`@RepIDs=0`), full date range (01/01/2020–04/29/2026), and all activity types.
  This report is a UI-context report with no API-accessible data. The approach is
  fundamentally broken for production use.

The existing reference pull in `bronze/orion/2026-04-21/trn/` (19 CSVs, 4.5M Inflection
TRN rows) was obtained via a different mechanism — likely a bulk SlickGrid/CSV export
from the Orion UI, NOT via the Custom Reports API.

`bronze/orion-api/` has **no transactions.csv in any date** (2026-04-28 or 2026-04-29).

---

## Your Task

### Step 1 — Review existing transaction files

Read `bronze/orion/2026-04-21/trn/` to understand the shape of the existing TRN data:
- Column names, data types, row structure
- Date range of transactions present
- Identify the pull mechanism if possible (file headers, metadata)

Reference file: `data/orion/manual_api/pulls/` for any prior manual pulls.

### Step 2 — Review Orion API docs and working scripts

Review the following to understand what transaction data is accessible via the API:

- `data/orion/manual_api/probe_tax_txn.py` — probes Transaction.* and Tax.* fields
  via the Envision/ExcelReports builder API (same approach as billing/tax scripts)
- `data/orion/manual_api/orion_billing_dim.py` — working example of the
  Envision/ExcelReports saved-query pattern (finds query by name, generates CSV)
- `data/orion/manual_api/orion_tax_dim.py` — working tax pull using same pattern
- `docs/architecture/INFLEC_API_ENDPOINTS_CATALOG.md` — API endpoint catalog
  (if exists; may be under `docs/architecture/`)
- Any HAR captures in `data/orion/` directories

Identify whether the Envision/ExcelReports API has a saved "Transactions" query
(analogous to "Billing Dim") that can be used for daily incremental pulls.

### Step 3 — Design and implement `pull_inflection_transactions_v2.py`

Write a replacement transactions pull script that:

1. **Uses the Envision/ExcelReports API** (same pattern as billing/tax) — find or
   create a saved query with the transaction fields matching the `bronze/orion/trn/`
   column schema (see Step 1).
2. **Scopes to Inflection reps** (`rep_id IN {3, 11, 12}`) — use whatever filter
   mechanism the Envision API supports (entity filter, database scoping, or
   post-pull filter).
3. **Date window:** rolling 7-day default (same as `DEFAULT_INCREMENTAL_DAYS=7` in
   the current script); backfill mode via `--start-date`/`--end-date` args.
4. **Output:**
   - Local: `data/orion/manual_api/pulls/{run_date}_inflection_transactions.csv`
   - S3 mirror (with `--upload-bronze`):
     `s3://opal-data-inf/bronze/orion-api/{run_date}/transactions.csv`
5. **Column shape** MUST be compatible with `silver/transactions/` — the canonical
   silver path (written by `convert_orion_to_silver.py` from `bronze/orion/2026-04-21/trn/`).
   Inspect a sample parquet from `s3://opal-data-inf/silver/transactions/2020-06-04.parquet`
   to get the exact column list before authoring the script. Output CSV columns must
   map cleanly into that schema so the same or minimal silver builder can ingest both paths.
6. **Exit codes and `--upload-bronze` flag** follow the same contract as
   `orion_billing_dim.py` (the orchestrator passes `--upload-bronze` for bronze writes).

### Step 4 — Validate

Run the script locally for a test window (e.g., 01/01/2026–04/29/2026) and confirm:
- HTTP 201 Generate response
- CSV with actual data rows (not header-only)
- Columns match expected schema
- S3 write works with `--upload-bronze`

Run the pre-commit gate:
```
.tools/ds-commit-gate.sh data/orion/manual_api/pull_inflection_transactions_v2.py
```

### Step 5 — Backfill

Once validated, run backfill for the dates the bronze runner has run without
transactions data:
- 2026-04-28 (bronze runner ran; no transactions.csv)
- 2026-04-29 (bronze runner ran; no transactions.csv)

Command example:
```
python data/orion/manual_api/pull_inflection_transactions_v2.py \
  --start-date 04/22/2026 --end-date 04/28/2026 \
  --run-date 2026-04-28 --upload-bronze
```

### Step 6 — Update orchestrator reference

Update the `DimSpec` entry in the S3 orchestrator
(`s3://opal-data-inf/code/bronze-runner/orchestrator.py`) to point at the new script
name. Upload the updated orchestrator to S3:
```
aws s3 cp data/orion/scripts/bronze/orchestrator.py \
  s3://opal-data-inf/code/bronze-runner/orchestrator.py
```
(Note: the orchestrator lives in S3; local edits go in `data/orion/scripts/bronze/`
or `data/orion/manual_api/` per existing file layout.)

---

## Acceptance Criteria

- [ ] `pull_inflection_transactions_v2.py` returns non-zero rows for a date range
      covering known activity periods
- [ ] Column schema matches `bronze/orion/2026-04-21/trn/` format (or is documented
      if the schemas diverge and a silver adapter is needed)
- [ ] `bronze/orion-api/2026-04-28/transactions.csv` uploaded to S3
- [ ] `bronze/orion-api/2026-04-29/transactions.csv` uploaded to S3
- [ ] Orchestrator updated to call `pull_inflection_transactions_v2.py`
- [ ] Pre-commit gate passes
- [ ] Committed to CLOUD and pushed

---

## Context / Blockers

- **Do NOT use Custom Report 28198** (`/api/v1/Reporting/Custom/28198/Generate/csv`).
  It is a UI-context report with no API-accessible data. The fix is documented above.
- **JWT** is fresh (exp 2026-04-29T22:26:01Z) — no need to wait for a new JWT cycle.
- **Silver nomenclature:** The canonical silver path is `silver/transactions/` (date-partitioned
  parquet, written by `convert_orion_to_silver.py`). There is no `silver/trn/`. The new
  pull's output must feed `silver/transactions/` incremental partitions — either by extending
  `convert_orion_to_silver.py` to also read `bronze/orion-api/{date}/transactions.csv`, or
  via a new silver builder. Flag schema divergence to AE for architectural decision.
- **Escalation path:** If the Envision API has no saved transactions query and creating
  a new template is blocked by permissions, flag to AE 0.6.1 for an alternative approach.

---

## Files to read before starting

- `data/orion/manual_api/pull_inflection_transactions.py` — broken original
- `data/orion/manual_api/orion_billing_dim.py` — working Envision pattern
- `data/orion/manual_api/probe_tax_txn.py` — transaction field probing
- `data/orion/scripts/silver/_orion_api_silver_lib.py` — silver shared lib
- `infra/aws/ec2/inf-bronze-runner/` or `s3://opal-data-inf/code/bronze-runner/orchestrator.py`
