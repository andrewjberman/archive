# ADVI_APISCP.003 — CloudOps OAI Handoff to DT

**From:** 0.7.0_AE_CloudOps
**To:** 0.4.0_DT_ClientPlatform
**Date:** 2026-03-10
**Re:** Hard dependency delivered — you are unblocked for ADVI_APISCP.003.cloudfront-oai-cache-key-v5.md

---

## Dependency Status: DELIVERED

The hard dependency in your task order requirement 0 is complete.
Proceed immediately with ADVI_APISCP.003.cloudfront-oai-cache-key-v5.md.

---

## Values You Need

```
OAI ID:            E139998VWH0PD
S3CanonicalUserId: d4ad9d8c8d632c03dc0495c78f1d102f1de6a06056577e25de649eaa90d66c9e35c047cce9afa4e82f74dbadc058c161
```

Use the OAI ID wherever your task order says `{OAI_ID_from_CloudOps}`.

---

## What Was Done (CloudOps scope — already complete)

1. **OAI created:**
   - Name: `opal-scoped-advisor-oai`
   - ID: `E139998VWH0PD`
   - CallerReference: `opal-scoped-advisor-oai-2026-03-10`

2. **`opal-data-bd` bucket policy updated:**
   - Existing `AllowCloudFrontOACReadGold` statement preserved (unchanged)
   - New `AllowScopedAdvisorOAI` statement added:
     - Principal: OAI canonical user above
     - Action: `s3:GetObject`
     - Resource: `arn:aws:s3:::opal-data-bd/*`
   - Applied and verified with `get-bucket-policy`

   AWS normalizes the principal on storage to:
   `arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E139998VWH0PD`
   This is expected — same identity, just the ARN form.

3. **Partner onboarding checklist updated** — future partner buckets use same OAI canonical user ID, no new OAI per partner.

**Commit:** `19551b11` on `CLOUD`
**Evidence log:** `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-03-10/advi_apiscp_003_oai_setup_bucket_policy.md`

---

## What Remains (your scope)

Per `ADVI_APISCP.003.cloudfront-oai-cache-key-v5.md`:

1. **Migrate `S3-opal-data-bd` origin** on distribution `EVTSA9VEHNZVH` from OAC to OAI `E139998VWH0PD`
   - Set `S3OriginConfig.OriginAccessIdentity = "origin-access-identity/cloudfront/E139998VWH0PD"`
   - Remove `OriginAccessControlId` (OAC ID `E24L6358YRRKAE`) from this origin only

2. **Update cache policy** for `/api/scoped/advisor-intelligence/*` — add `X-Firm-Id` to cache key headers (compliance requirement, non-deferrable)

3. **Publish `shared-advisor-router:5`** — same code as `:4` (commit `4eff8dee`), no source change:
   ```bash
   aws lambda publish-version --function-name shared-advisor-router \
     --description "v5: OAI configured on distribution"
   ```

4. **Wire `:5` to the behavior**, wait for `Status: Deployed`

5. **Invalidate** `/api/scoped/advisor-intelligence/*` on `EVTSA9VEHNZVH`

6. **Verify** — GET with 49 Financial JWT, expect HTTP 200 + `Content-Type: application/json` + current gold date

7. **Tag** `shared-advisor-router-v5` pointing at `4eff8dee`, push with `--follow-tags`

---

## Do NOT

- Touch any other origin on the distribution (OAC stays on portal-v2 and all other origins)
- Create a new Lambda source package — `publish-version` from existing deployed code is correct
- Tag before end-to-end verification passes (200 JSON, not HTML)
