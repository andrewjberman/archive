# DRFR_PTMCH.001 — CloudOps Infrastructure Findings
**Agent:** 0.7.0_AE_CloudOps
**Date:** 2026-03-10
**Task Order:** DRFR_PTMCH.P1 (issued by 2.0.0_SA_COO)
**Thread:** DRFR_PTMCH-001

---

## Summary

All six original task order requirements are resolved. Lifecycle rules are deployed on both
buckets (0-diff confirmed). CloudFront path routing is fully documented as a table. DynamoDB
PITR and S3 versioning were confirmed by Andrew via CLI on 2026-03-10 and are recorded here.
IAM gaps were removed from scope per COO revision (each pipeline AE owns their own role).

---

## Req 1 — S3 Versioning: opal-data-portal-v2

**Status: CONFIRMED (pre-existing)**

Versioning was already enabled on `opal-data-portal-v2` prior to this task.
Confirmed by Andrew via CLI on 2026-03-10:
```
{ "Status": "Enabled" }
```

Lifecycle rule now deployed (see Req 1 Lifecycle below).

---

## Req 2 — S3 Versioning: opal-data-bd

**Status: CONFIRMED (pre-existing)**

Versioning was already enabled on `opal-data-bd` prior to this task.
Confirmed by Andrew via CLI on 2026-03-10:
```
{ "Status": "Enabled" }
```

Lifecycle rule now deployed (see Req 2 Lifecycle below).

---

## Req 1 Lifecycle — opal-data-portal-v2 (Deployed)

**Status: DEPLOYED — shared-infra-v1.4.0, commit `5978d069`**

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "portal_v2_versions" {
  bucket = "opal-data-portal-v2"

  rule {
    id     = "expire-noncurrent-versions-90d"
    status = "Enabled"
    filter {}
    noncurrent_version_expiration { noncurrent_days = 90 }
  }

  rule {
    id     = "abort-incomplete-mpu-7d"
    status = "Enabled"
    filter {}
    abort_incomplete_multipart_upload { days_after_initiation = 7 }
  }
}
```

**Cost context:** Yang pipeline runs ~weekly, 83 files/run. Without a lifecycle rule,
~4,300 noncurrent versions accumulate per year. At 90-day expiry, steady state is
~(90/7) x 83 = ~1,070 versions maximum at any time, vs. unlimited accumulation.

**0-diff confirmed:** `No changes. Your infrastructure matches the configuration.`

---

## Req 2 Lifecycle — opal-data-bd (Deployed)

**Status: DEPLOYED — shared-infra-v1.4.0, commit `5978d069`**

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "bd_versions" {
  bucket = "opal-data-bd"

  rule {
    id     = "expire-noncurrent-versions-90d"
    status = "Enabled"
    filter {}
    noncurrent_version_expiration { noncurrent_days = 90 }
  }

  rule {
    id     = "abort-incomplete-mpu-7d"
    status = "Enabled"
    filter {}
    abort_incomplete_multipart_upload { days_after_initiation = 7 }
  }
}
```

**Cost context:** BD gold pipeline runs ~daily, ~80-100 files/run. Without a lifecycle rule,
~30,000+ noncurrent versions accumulate per year. At 90-day expiry, steady state is
~(90/1) x 90 = ~8,100 versions maximum. The 90-day window provides adequate historical
depth for Time Machine use (PRD target: 90-day restore window).

**0-diff confirmed:** `No changes. Your infrastructure matches the configuration.`

---

## Req 3 — IAM Gap Analysis

**Status: REMOVED FROM P1 SCOPE**

Per COO revision 2026-03-10: IAM changes are owned by each pipeline AE, not CloudOps.
CloudOps scope is lifecycle rules and CloudFront audit only. Pipeline AEs will add
time-machine restore permissions to their respective roles when the time-machine
Lambda is built by OpalETL.

Permissions each pipeline AE will need to add:

**Yang layer restore (opal-data-portal-v2):**
- `s3:GetObjectVersion` on `opal-data-portal-v2/*`
- `s3:CopyObject` on `opal-data-portal-v2/*` (for CopySourceVersionId)
- `s3:PutObject` on `opal-data-portal-v2/json/*`

**BD layer restore (opal-data-bd):**
- `s3:ListObjectVersions` on `opal-data-bd/*`
- `s3:CopyObject` on `opal-data-bd/*`
- `s3:PutObject` on `opal-data-bd/gold/*`

---

## Req 4 — DynamoDB PITR (Yang Pipeline)

**Status: CONFIRMED (pre-existing)**

Confirmed by Andrew via CLI 2026-03-10:
- PITR enabled on `opal-portal-market-data` table
- Continuous backup window: 35 days
- Earliest restorable time: approximately 2026-02-13

**Time Machine verdict:** DynamoDB rollback is NOT required for Phase 1 Time Machine.
The yang pipeline's DynamoDB writes are pre-computed market metrics used during pipeline
processing. The portal frontend reads from `opal-data-portal-v2/json/*` S3 files at
request time, not from DynamoDB directly. Restoring the S3 JSON files is sufficient
to restore portal state. DynamoDB PITR is available as a safety net but not on the
critical path for the Time Machine feature.

---

## Req 5 — CloudFront Path Routing (EVTSA9VEHNZVH)

**Status: AUDITED via CLI 2026-03-10**

Full behavior list from `aws cloudfront get-distribution-config --id EVTSA9VEHNZVH`.

### Invalidation Table for OpalETL

| Path Pattern | Origin | Source Bucket | Time Machine Invalidation Needed? | Invalidation Path |
|---|---|---|---|---|
| `/api/general/json-tiered/*` | S3-opal-data-portal-v2-json | opal-data-portal-v2 | YES — yang outputs | `/api/general/json-tiered/*` |
| `/api/general/*` | S3-opal-data-portal-v2-json | opal-data-portal-v2 | YES — yang catch-all | `/api/general/*` |
| `/json-tiered/*` | S3-opal-data-portal-v2-json | opal-data-portal-v2 | YES — legacy path | `/json-tiered/*` |
| `/api/scoped/advisor-intelligence/*.json` | S3-opal-data-bd | opal-data-bd | YES — BD gold outputs | `/api/scoped/advisor-intelligence/*` |
| `/api/scoped/advisor-intelligence/clients/*` | APIGateway-portal | (API Gateway) | NO — API Gateway, not S3 | N/A |
| `/api/scoped/data-refresh/*` | APIGateway-portal | (API Gateway) | NO | N/A |
| `/api/scoped/security-scanner/*` | APIGateway-portal | (API Gateway) | NO | N/A |
| `/api/general/trades/*` | APIGateway-portal | (API Gateway) | NO | N/A |
| `/api/private/portfolio*` | APIGateway-portfolio | (API Gateway) | NO | N/A |
| `/api/private/*` | APIGateway-portal | (API Gateway) | NO | N/A |
| `/v1/*` | APIGateway-portal | (API Gateway) | NO | N/A |
| `/auth/*` | APIGateway-portal | (API Gateway) | NO | N/A |
| Default (`*`) | S3 static site (React SPA) | (static assets) | NO | N/A |

### Key Finding for OpalETL

**Yang restore requires TWO invalidation paths** (not one):
```
/api/general/*
/api/general/json-tiered/*
```
Both route to `S3-opal-data-portal-v2-json`. A single `/api/general/*` wildcard covers both,
but they use different cache policies so separate invalidations are safer.

**BD restore requires ONE invalidation path:**
```
/api/scoped/advisor-intelligence/*
```
This covers `/api/scoped/advisor-intelligence/*.json` (the S3-opal-data-bd behavior).
Note: `/api/scoped/advisor-intelligence/clients/*` routes to API Gateway, not S3 — no
S3 cache to invalidate there.

**Answer to PRD question:** `/api/public/*` (or `/api/general/*`) does NOT cover BD data.
BD data is served on `/api/scoped/advisor-intelligence/*.json` via a SEPARATE behavior
pointing to `S3-opal-data-bd`. The two pipelines require separate CloudFront invalidation calls.

### Lambda@Edge on Data Paths

| Behavior | viewer-request | origin-request | origin-response |
|---|---|---|---|
| `/api/general/json-tiered/*` | auth-validator-edge:7 | public-data-router:4 | cache-control-injector:1 |
| `/api/general/*` | auth-validator-edge:7 | public-data-router:4 | cache-control-injector:1 |
| `/api/scoped/advisor-intelligence/*.json` | auth-validator-edge:7 | shared-advisor-router:3 | (none) |

The `shared-advisor-router:3` on the BD path likely maps the advisor intelligence request to
a specific S3 key in opal-data-bd/gold/ based on JWT claims (advisorKey/advisorRole). After
a Time Machine restore, `shared-advisor-router` will continue routing correctly since the S3
objects are restored by version, not rekeyed.

---

## Req 6 — Archive Manifest Health

**Status: CONFIRMED (pre-existing, confirmed 2026-03-10)**

Archive manifest for yang outputs: 83 files, all versionIds non-null.
Confirmed by `yang-capture-output-versions` execution `7a407b33`.
The existing rollback mechanism (`handle_rollback` in `opal-data-refresh-api`) already uses
`CopySourceVersionId` to restore files — this mechanism is functional for yang data.

---

## Deployment Record

| Step | Action | Result |
|---|---|---|
| 1 | CloudFront audit (CLI read-only) | 12 behaviors documented, 4 S3-backed paths identified |
| 2 | Write lifecycle rules to shared-infra/main.tf | 71-line addition, 2 resources |
| 3 | Commit source | `5aea13f0` infra(shared-infra): add S3 lifecycle rules for DRFR_PTMCH |
| 4 | Fix filter{} warning | `5978d069` infra(shared-infra): add filter{} to lifecycle rules |
| 5 | terraform plan | 2 to add, 0 to change, 0 to destroy |
| 6 | terraform apply | 2 added, 0 changed, 0 destroyed |
| 7 | 0-diff plan | No changes. Infrastructure is up-to-date. |
| 8 | Update pipeline_inventory.xml | shared-infra-v1.4.0, new S3 and CF entries |
| 9 | Write findings doc | This file |
| 10 | Commit + tag + push | shared-infra-v1.4.0 |

---

## For OpalETL — Time Machine Orchestrator Wiring

When building the portal-time-machine orchestrator Lambda, use these invalidation paths:

```python
# Yang layer restore invalidation
yang_invalidation_paths = ["/api/general/*", "/api/general/json-tiered/*"]

# BD layer restore invalidation
bd_invalidation_paths = ["/api/scoped/advisor-intelligence/*"]

# CloudFront distribution ID
CLOUDFRONT_DIST_ID = "EVTSA9VEHNZVH"
```

Both lifecycle rules are in effect. S3 version history is bounded to 90 days on both
buckets. The orchestrator can use `s3:ListObjectVersions` to find the correct version
ID at any date within the 90-day window.
