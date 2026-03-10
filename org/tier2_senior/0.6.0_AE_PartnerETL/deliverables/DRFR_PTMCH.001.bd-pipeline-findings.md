# DRFR_PTMCH.001 — BD Pipeline Findings: Portal Time Machine

**Prepared by:** 0.6.0_AE_PartnerETL
**Date:** 2026-03-10
**Task Order:** `org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/DRFR_PTMCH.P3.bd-time-machine.md`

---

## Summary

The PRD snapshot-archive approach is **SUPERSEDED**. S3 versioning is already enabled on
`opal-data-bd` (confirmed 2026-03-10 via CLI). Every gold/ file that gets overwritten by
`bd-portal-publisher` or EC2 gold scripts already has its previous versions preserved in S3.
The time machine restores BD data by CopyObject-ing versioned gold/ files, not by maintaining
a separate snapshot archive. A manifest Lambda (`bd-capture-output-versions`) records VersionIds
after each rebuild for fast restore without scanning full version history.

---

## 1. Versioning Status

| Bucket | Versioning | Confirmed By |
|--------|-----------|-------------|
| `opal-data-bd` | ENABLED | CLI 2026-03-10 (DRFR_PTMCH-001 thread) |
| `opal-data-portal-v2` | ENABLED | CLI 2026-03-10 (DRFR_PTMCH-001 thread) |

**PRD snapshot approach: SUPERSEDED.** `snapshots/{YYYYMMDD}/` pattern is not needed.
`snapshots/manifests/` is used instead for O(1) VersionId lookups per rebuild.

---

## 2. Earliest Available Historical Date

CLI output from `s3api list-object-versions` on `gold/timeseries_chart.json`:

```
Most recent versions (newest first):
  2026-03-10T18:08:18Z  VersionId: J5xGD4l.oLFQrotfM_X1.CF3o7hjTLV_
  2026-03-10T17:16:43Z  VersionId: dYloeH4h1FB6GfVhIqelhFwiCzcDwC.T
  2026-03-10T15:58:22Z  VersionId: G8726nQ1ETBhBBaLFojvZWJTFcEgdF4w
  2026-03-06T23:37:47Z  VersionId: B9t1CHOPvQa4vxlYsWGEHpLr2tw0CYyV
  2026-03-06T23:30:25Z  VersionId: Ruff7vdFohNjgqUQU5s39D9Rbv9OwzoZ

Earliest version:
  2026-02-25T22:02:47Z  VersionId: gPL4d7HpRQWoJJe2ZsdOH4YFahMGHbAF
```

**Earliest date Time Machine can serve for BD data: 2026-02-25.**

For dates before 2026-02-25, `bd-time-machine` returns 404 with
`earliest_available: 2026-02-25` in the response body.

Before manifests exist (all dates prior to first `bd-capture-output-versions` run),
`bd-time-machine` uses the `list_object_versions` fallback path.

---

## 3. Gold Rebuild Cadence

| Trigger | Schedule | Notes |
|---------|---------|-------|
| EventBridge `bd-gold-nightly-fallback` | Mon-Fri 23:00 UTC | Starts `i-01003b035d2988dfb`, systemd service now enabled |
| S3 event on `silver/prices/20*.parquet` | On data arrival | `bd-gold-trigger` Lambda |
| Manual SSM | Ad hoc | Legacy; no longer needed after systemd fix (ADVI_49FNV3.004) |

Gold rebuild cadence: **~5 runs/week (Mon-Fri nightly), plus event-driven on price data arrival.**

Publisher trigger: S3 `ObjectCreated` on `opal-data-bd/gold/pipeline-complete.json`
(written by `bd-gold-layer-runner` EC2 at pipeline completion). Confirmed in `s3-notifications.tf`.

---

## 4. Snapshot Storage Cost: NOT NEEDED

With versioning already enabled, no additional snapshot copies are stored.
Version overhead is minimal — S3 keeps prior versions of overwritten files only.
Lifecycle rules (90-day noncurrent version expiry) will be added by CloudOps P1
to prevent unbounded accumulation.

Manifest files (`snapshots/manifests/*.json`) are small (< 50 KB each).
At 5 runs/week = ~260 manifests/year, total manifest storage is negligible.

---

## 5. bd-portal-publisher Source Path Analysis

**Verdict: Source path is env-var backed. No code surgery needed.**

```python
INPUT_BUCKET  = os.environ.get('INPUT_BUCKET',  'opal-data-bd')
OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET', 'opal-data-bd')
```

Terraform module (`lambdas.tf`) sets these explicitly. The publisher reads gold parquets
and writes JSON — it does NOT trigger a gold rebuild. The `bd-time-machine` sentinel
approach fires the publisher cleanly without any `time_machine` flag or source-path
parameterization.

No blast radius. Publisher code unchanged except for the capture fan-out addition.

---

## 6. bd-portal-advisor-publisher Scope

**Independent reader — needs no separate handling.**

`bd-portal-advisor-publisher` reads from `opal-data-bd/gold/` (parquets and JSON)
and writes per-advisor and per-client files. It is triggered by `bd-portal-publisher`
via Lambda-to-Lambda async fan-out at handler start, running concurrently.

When `bd-time-machine` restores gold/ files and writes the sentinel,
`bd-portal-publisher` fires and immediately invokes `bd-portal-advisor-publisher`
as normal. Both publishers re-publish from the restored gold data automatically.
No additional wiring needed.

---

## 7. Fan-out Chain (bd-portal-publisher)

S3 does not allow two notification rules with the same prefix+suffix filter.
`bd-portal-publisher` uses Lambda-to-Lambda async for all downstream fan-out:

```
S3: gold/pipeline-complete.json (ObjectCreated)
    -> bd-portal-publisher (S3 event trigger)
        -> bd-portal-advisor-publisher (Lambda async, at handler START — concurrent)
        -> bd-capture-output-versions  (Lambda async, at handler END — after writes)
```

`CAPTURE_VERSIONS_FUNCTION` env var added to publisher Terraform module.
`bd_gold_layer_invoke` IAM policy extended to allow invoking `bd-capture-output-versions`.

---

## 8. New Lambdas: Deployment Notes

| Lambda | Role | Memory | Timeout | Trigger |
|--------|------|--------|---------|---------|
| `bd-capture-output-versions` | `bd-capture-versions-lambda-role` | 256 MB | 120 s | Lambda-to-Lambda from bd-portal-publisher |
| `bd-time-machine` | `bd-time-machine-lambda-role` | 256 MB | 300 s | Direct invocation (API GW / console) |

**Phase A (complete — this session):**
- Lambda source written
- Terraform modules in `lambdas.tf`
- IAM roles in `iam.tf`
- `lambda-source-map.json` entries added (artifact_sha256/last_deployed fields null — not yet built)
- `bd-portal-publisher` fan-out addition committed

**Phase B (gated on CloudOps P1):**
- Confirm CloudOps P1 lifecycle rules deployed on `opal-data-bd` (90-day noncurrent version expiry)
- Confirm CloudOps P1 findings doc (full CloudFront path table)
- `build-and-upload.sh` for both new Lambdas + `bd-portal-publisher` (fan-out change)
- `terraform plan` -> `terraform apply` -> 0-diff -> tag `bd-v2.18.0` -> push

**CloudFront invalidation path in bd-time-machine:**
`/api/scoped/advisor-intelligence/*` — confirmed from ADVI_APISCP work (DT Lambda@Edge v4
dynamic routing maps this path to `opal-data-bd`). Full path table (all behaviors) pending
CloudOps P1 findings doc. Hardcoded for now; update if CloudOps P1 reveals a different scope.

---

## 9. Known Gaps / Follow-up

| Item | Owner | Status |
|------|-------|--------|
| Lifecycle rules on opal-data-bd (90-day noncurrent expiry) | 0.7.0_AE_CloudOps (P1) | PENDING |
| Full CloudFront invalidation path table | 0.7.0_AE_CloudOps (P1) | PENDING |
| `build-and-upload.sh` + terraform apply for two new Lambdas + publisher | 0.6.0_AE_PartnerETL | Blocked on CloudOps P1 |
| Verify `s3://opal-data-bd/scripts/gold_layer/` archive/11 version | 0.6.0_AE_PartnerETL | Pending (flagged in ADVI_APISCP.001) |
