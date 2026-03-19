# Partners API v1.1.0 Addendum A Deploy -- 0.4.0_DT_ClientPlatform

**Date:** 2026-03-16
**Task Order:** ADVI_MVPLVL.005.lambda-deploy (requirements 1-5)

## Objective

Rebuild opal-partners-data Lambda artifact to include DS 005 Addendum A endpoints
(handle_mix_timeseries, handle_concentration_timeseries) and the 06b per-relationship
JSON refactor (33d490a9). Deploy via Terraform, verify all endpoints, tag partners-api-v1.1.0.

---

## Deployment Sequence

| Step | Action | Result |
|------|--------|--------|
| 1 | Verify source committed | Clean -- no uncommitted changes in source dir |
| 2 | build-and-upload.sh partners-api opal-partners-data | SHA256: `TuZ5v528GjA0tXo0cun6Bxjp0bd0WLjH8SXZoZYD6EE=`, 20K |
| 3 | Commit source map | `e9155577` ci: upload artifact for partners-api opal-partners-data |
| 4 | terraform plan | 1 changed (s3_object_version + source_code_hash update) |
| 5 | terraform apply | 0 added, 1 changed, 0 destroyed |
| 6 | 0-diff plan | No changes. Infrastructure is up-to-date. |
| 7 | Update deployment_map.xml | Added partners-api module + opal-partners-data Lambda entry |
| 8 | record-terraform-deploy.sh | `3bc778de` ci: record deploy partners-api @ e9155577, CHANGELOG.json created |
| 9 | Commit deployment_map.xml | `585bcaf9` |
| 10 | Tag + push | `partners-api-v1.1.0` pushed to CLOUD |

## Verification

All endpoints tested via `aws lambda invoke` with relationship z08327149, firmId=49financial:

| Endpoint | Status | Data |
|---|---|---|
| /books/relationship/{id}/timeseries | 200 | Daily AUA/NNA records |
| /books/relationship/{id}/composition | 200 | Mix + concentration snapshot |
| /books/relationship/{id}/mix-timeseries | 200 | 420 mix records (date, equity, fixed_income, structured_notes, cash, other) + 420 concentration records |
| /books/relationship/{id}/concentration-timeseries | 200 | 420 mix + 420 concentration records (date, holdings) |

Both Addendum A endpoints return valid JSON with 420 daily records each.

## Deployment Tags

| Pipeline | Tag | Commit |
|----------|-----|--------|
| partners-api | `partners-api-v1.1.0` | `585bcaf9` |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `infra/aws/lambda/ci/lambda-source-map.json` | artifact_sha256 + last_deployed_commit updated | Yes -- `e9155577`, `3bc778de` |
| `infra/aws/terraform/partners-api/CHANGELOG.json` | Created with v1.1.0 entry | Yes -- `3bc778de` |
| `org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/deployment_map.xml` | Added partners-api module + opal-partners-data Lambda | Yes -- `585bcaf9` |

---

## Current State

**Status:** COMPLETE (requirements 1-5). Requirement 6 (portal DEV->PROD merge) blocked on DE firmId fix.
**Active branch:** CLOUD

The opal-partners-data Lambda is deployed at `partners-api-v1.1.0` with all 8 Books Tab
endpoints functional: 4 original (timeseries, composition per relationship/account) plus
2 Addendum A (mix-timeseries, concentration-timeseries). The artifact includes both the
DS 005 commit (`6cae4815`) and the 06b per-relationship JSON refactor (`33d490a9`).

API Gateway routes for all 6 `/api/scoped/partners/books/*` paths are live with JWT
authorizer. The partners-api Terraform module is at 0-diff.

**Still open:** Portal DEV->PROD merge (task order requirement 6) is gated on DE fixing
7 portal API functions missing `?firm=` / `?firmId=` query parameters.

---

## Next Steps

1. **[0.4.0_DE_ClientPlatform] Fix 7 portal API functions** -- thread firmOverride/firmId through advisor-intelligence.ts. S3-routed need `?firm=`, Lambda-routed need `?firmId=`.
2. **[0.4.0_DT_ClientPlatform] After DE fix on portal DEV** -- verify Books Tab L2 drilldown end-to-end, then execute portal DEV->PROD merge (task order requirement 6).
3. **[0.4.0_DT_ClientPlatform] Update task order status** -- mark ADVI_MVPLVL.005.lambda-deploy as complete after portal merge.

**Do NOT:**
- Put opal-partners-data back in bd-pipeline -- it has its own module at `infra/aws/terraform/partners-api/`
- Merge portal DEV->PROD until DE firmId fix is committed on DEV and all endpoints verified
- Use `pyarrow_additional_kwargs` for filters -- broken in awswrangler 3.11.0
