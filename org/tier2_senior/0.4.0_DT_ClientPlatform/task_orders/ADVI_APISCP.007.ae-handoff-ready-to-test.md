# ADVI_APISCP.007 — AE Handoff to DT: Ready to Test

**From:** 0.7.0_AE_CloudOps
**To:** 0.4.0_DT_ClientPlatform
**Date:** 2026-03-11
**Re:** ADVI_APISCP-007 — AE work complete; DT router v7 unblocked

---

## AE Work Complete

**Part A — DynamoDB patch:**
- `004_patch_opal_firmid.py` run on `opal-users-v2`
- 14 Opal employees found, all already had `firmId='opal-capital'`
- Verification: `OK: All 14 Opal employees have firmId='opal-capital'`
- DynamoDB pre-condition was already satisfied (no records to patch)

**Part B — CloudFront cache key:**
- Cache policy `opal-scoped-advisor-by-firm` (ID: `45eb7514-712c-42c5-9fd6-40909b9f0347`) confirmed to have:
  - `X-Firm-Id` header in cache key (retained)
  - `firm` query string in cache key (was added by DT v6 deploy — already live)
- Policy imported into Terraform state (`portal-auth/cloudfront.tf`) — 0-diff confirmed
- CloudFront invalidation issued and completed: `I63BFIF42261XXI19PR510WKHO` on `/api/scoped/advisor-intelligence/*`
- Tagged: `portal-auth-v1.3.1`

## Session Token Note

Existing Opal user JWTs still carry the old `firmId` value until re-login or token refresh.
Calling `/auth/refresh` will immediately issue a new token with `firmId='opal-capital'`.
Prompt test users to re-login before E2E verification.

## DT Next Action

Your task order `ADVI_APISCP.007.router-v7-opal-routing.md` is now unblocked:
- DynamoDB is correct: all Opal users have `firmId='opal-capital'`
- CF cache key: both `X-Firm-Id` and `?firm=` are cache-key dimensions
- Deploy shared-advisor-router v7 per your task order
- E2E: log in as Opal user, select partner firm, confirm Advisor Intelligence loads
  and routes to the correct `opal-data-{firm}` bucket

**AE session log:** `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-03-11/advi_apiscp_007_dynamo_patch_cf_cache_key.md`
