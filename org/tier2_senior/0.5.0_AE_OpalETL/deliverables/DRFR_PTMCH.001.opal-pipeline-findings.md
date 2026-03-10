# DRFR_PTMCH.001 — OpalETL Pipeline Findings
**Agent:** 0.5.0_AE_OpalETL
**Date:** 2026-03-10
**Task Order:** DRFR_PTMCH.001.opal-pipeline-archive-audit.md (complete) + DRFR_PTMCH.P2 (in progress)
**Thread:** DRFR_PTMCH-001

---

## 1. Step Functions Placement — CONFIRMED GREEN

**Verdict:** `yang-capture-output-versions` runs on EVERY pipeline execution. Time Machine implementation is unblocked.

**Evidence** (`infra/aws/terraform/yang-pipeline/yang-pipeline-definition.json`):

State machine end sequence:
```
GenerateManifest → CleanupUploads → CaptureOutputVersions → InvalidateCloudFront → PipelineSuccess
```

- `CaptureOutputVersions` is NOT conditional — it always executes after `CleanupUploads`.
- All generator Lambdas (25+) complete before `CleanupUploads` runs.
- `CaptureOutputVersions` has a `Catch` block routing to `InvalidateCloudFront` on any error
  (comment: "Don't fail pipeline if version capture fails"). Pipeline never fails due to capture error.
- The Lambda itself captures all `json/**/*.json` files modified within the **last 10 minutes** via
  `head_object` + timestamp comparison. Writes to `data-refresh/archive/{execId}/outputs-manifest.json`.

**Known limitation (10-minute capture window):**
The 10-minute rolling time window is a heuristic. If the yang pipeline run takes longer than 10 minutes
between the first generator writing its file and `CaptureOutputVersions` running, early-written files
may not be captured. Production manifests show ~83 files consistently captured (confirmed via thread
DRFR_PTMCH-001 CLI audit, exec `7a407b33`), indicating this is working in practice. Documented as a
known limitation — not a blocker. Do NOT extend the capture window without benchmarking pipeline
runtime; extending it risks capturing stale files from prior runs.

---

## 2. Archive Manifest Schema

`data-refresh/archive/{executionId}/outputs-manifest.json`:
```json
{
  "schema_version": "1.0",
  "executionId": "exec-abc123",
  "capturedAt": "2026-03-08T...",
  "pipelineStartedAt": "2026-03-08T...",
  "dataAsOfDate": "YYYY-MM-DD",
  "inputFiles": { "data_pkl": "...", "model_pkl": "..." },
  "outputCount": 83,
  "outputs": {
    "json/some/file.json": {
      "versionId": "AbCdEf...",
      "size": 12345,
      "etag": "...",
      "lastModified": "..."
    }
  },
  "stats": { "totalScanned": N, "totalCaptured": 83, "cutoffTime": "..." }
}
```

`data-refresh/archive/{executionId}/metadata.json` (written by `handle_trigger`):
```json
{
  "executionId": "exec-...",
  "executionArn": "arn:aws:states:...",
  "uploadId": "...",
  "dataAsOfDate": "YYYY-MM-DD"
}
```

`data-refresh/archive/{executionId}/manifest.json` (original input manifest, archived during trigger):
```json
{
  "version": "20260308_v1",
  "date": "YYYY-MM-DD",
  "files": { "data_pkl": "data_20260308_v1.pkl", "model_pkl": "model_20260308_v1.pkl", ... },
  "auto_generated": true,
  "generated_at": "..."
}
```

The `manifest.json` is the source for rebuilding `benchmarks/LATEST.json` during a time-travel restore.

---

## 3. Yang-Time-Machine Implementation Notes

**Lambda location:** `infra/aws/lambda/v2_portal/yang_pipeline/outputs/yang-time-machine/lambda_function.py`
**Terraform:** `infra/aws/terraform/yang-pipeline/lambdas.tf` — `module.time_machine` (512MB, 300s)
**Role:** `yang-pipeline-lambda-role`
**New IAM statement:** `S3VersionedRestore` — `s3:GetObjectVersion` + `s3:ListObjectVersions` on
`opal-data-portal-v2`. Added to `yang-pipeline/iam.tf` in commit `5ce67698`.

**Restore logic:**
1. List all `data-refresh/archive/*/outputs-manifest.json` (paginated)
2. Read each manifest to get `dataAsOfDate` and `capturedAt`
3. Select latest execution where `dataAsOfDate <= target_date` AND `capturedAt <= 22:00 UTC on target_date`
4. `copy_object` with `CopySourceVersionId` for each key/versionId in `outputs` (partial restore on error)
5. Read archived `manifest.json` → rebuild `benchmarks/LATEST.json`
6. Invalidate both CF distributions (`/*` on `E2LPCXXBLDGWXY` + `EVTSA9VEHNZVH`)
7. Return `{ restored_execution, data_as_of, files_restored, files_failed, cloudfront }`

**Deployment status:** Code committed (`5ce67698`). HOLD deploy until CloudOps P1 confirms:
- S3VersionedRestore IAM applied to `yang-pipeline-lambda-role` (already in TF, needs apply)
- CloudFront invalidation scope confirmed (current impl uses `/*` on both dists — conservative and correct)

---

## 4. DataRefresh API New Endpoints

Added to `infra/aws/lambda/data_refresh/lambda_function.py` in commit `5ce67698`:

**`GET /data-refresh/archive`:**
- Lists all outputs-manifest.json files in `data-refresh/archive/`
- Returns `{ restore_points: [{ execution_id, data_as_of, pipeline_completed_at, files_captured }], count }`
- Ordered newest-first by `data_as_of`, then `pipeline_completed_at`
- Dev-gated (requires Dev userType)

**`POST /data-refresh/time-machine`:**
- Body: `{ "target_date": "YYYY-MM-DD" }`
- Invokes `yang-time-machine` Lambda async (`InvocationType=Event`)
- Returns immediately: `{ status: "initiated", target_date }`
- `TIME_MACHINE_FUNCTION_NAME` env var controls target (default: `yang-time-machine`)
- IAM policy `data-refresh-time-machine-invoke` added to `data-refresh/main.tf`

**Deployment status:** Code committed. HOLD deploy until CloudOps P1 IAM is applied.

---

## 5. News Publisher Parameterization

**Lambda:** `infra/aws/lambda/semantic-trending-topics-portal-publisher/lambda_function.py`
**Change:** `lambda_handler` now accepts optional `event.target_date`. If present, queries DynamoDB
for that specific date instead of auto-discovering latest. Fully backward compatible.
**Status: DEPLOYED as `news-v2.7.0` (commit `08e3e981`, tag pushed 2026-03-10)**

---

## 6. FRED Cache — Explicit Exception

**Lambda:** `yang-refresh-fred-cache`
**Write path:** `opal-data-portal-v2/cache/fred/` (e.g., `cache/fred/BAMLC0A0CM.csv`)
**Not under:** `json/` prefix — NOT captured by `yang-capture-output-versions`

**Documented exception:** FRED cache (`cache/fred/BAMLC0A0CM.csv`, `cache/fred/BAMLH0A0HYM2.csv`)
is NOT restored by Time Machine. FRED data updates weekly and represents macro market conditions
(credit spreads). Accepted exception: FRED cache always reflects current data during time-travel.
This is correct behavior — restoring historical FRED data would show stale macro conditions that
don't reflect the current risk environment.

Do NOT extend `yang-capture-output-versions` to capture `cache/` in this phase.

---

## 7. DynamoDB Portal Runtime Read

**Verdict:** Portal reads DynamoDB at runtime: YES.

**Table:** `opal-portal-market-data`
**Writer:** `yang-ingest-dynamodb` Lambda (IAM confirmed: `DynamoDBAccess` statement in `yang-pipeline/iam.tf`)
**Reader:** `opal-portal-data-proxy` Lambda reads from this table at request time for portfolio data.

**Time Machine implication:** DynamoDB PITR is enabled with a 35-day window (confirmed via thread
DRFR_PTMCH-001 CLI audit, earliest restore ~2026-02-13). Layer 2 of the Time Machine (full fidelity,
Phase 5) would require a DynamoDB point-in-time restore to align portal API responses with the
restored S3 data. Layer 1 (yang S3 restore only) is acceptable for Phase 1 — the portal JSON files
are the primary display data source.

---

## 8. Market-Overview Output Prefixes

Market-overview Lambdas write exclusively to `opal-data-portal-v2` (confirmed ADVI_APISCP.001):

| Lambda | Write Prefix |
|--------|-------------|
| opal-trending-topics-portal-publisher | `json/semantic-trending/latest.json` |
| opal-market-overview-tiered-generator | `json-tiered/` |
| opal-market-regime-classifier | `json/market/` |
| opal-market-rsi-tiered-generator | (json-tiered based) |
| opal-portal-fear-greed-fetcher | `json/sentiment/fear-greed-index.json` |

Market-overview outputs are NOT under `json/` prefix for all Lambdas — `json-tiered/` is a separate
prefix. `yang-capture-output-versions` scans `json/` only. Market-overview files are NOT captured
in the yang archive manifests. Time Machine Layer 1 restores yang outputs only. Market-overview
is out of scope for Phase 1; Phase 4 (if implemented) would cover this separately.

---

## 9. Deployment Gate Summary

| Item | Status |
|------|--------|
| Req 5: semantic publisher target_date | DEPLOYED — news-v2.7.0 (2026-03-10) |
| Req 2: yang-time-machine Lambda code | Committed `5ce67698` — hold for CloudOps P1 |
| Req 3: DataRefresh API endpoints | Committed `5ce67698` — hold for CloudOps P1 |
| Req 6: yang-pipeline TF (time_machine module) | Committed `5ce67698` — hold for apply |
| Req 6: yang-pipeline IAM (S3VersionedRestore) | Committed `5ce67698` — hold for apply |
| Req 6: data-refresh TF (env var + invoke policy) | Committed `5ce67698` — hold for apply |

**CloudOps P1 deliverable required before proceeding:**
`org/tier2_senior/0.7.0_AE_CloudOps/deliverables/DRFR_PTMCH.001.cloudops-findings.md`
containing confirmed CloudFront invalidation path table.
