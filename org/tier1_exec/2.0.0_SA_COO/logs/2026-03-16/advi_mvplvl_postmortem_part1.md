# ADVI_MVPLVL Postmortem (Part 1: Diagnosis) — 2.0.0_SA_COO

**Date:** 2026-03-16
**Project:** ADVI_MVPLVL
**Severity:** HIGH — entire Books Tab non-functional for internal users

---

## Summary

The Books Tab has been broken for internal users since inception. Multiple independent
failures compounded to produce a state where: (1) API routes never reached the Lambda,
(2) the Lambda code had awswrangler 3.x incompatibilities, (3) portal API functions
omitted required auth parameters, and (4) a firm ID naming collision between S3 routing
and DynamoDB routing remains unresolved. COO's startup audit was surface-level — it
checked task order `<status>` fields and git commits but never verified that the
deployed system actually worked end-to-end.

---

## Timeline of Failures

### 2026-03-13: ADVI_MVPLVL threads + task orders issued

Thread 004 (Books Tab alignment) ran with **embedded context that included stale API
route definitions**. The embedding strategy pulled deprecated route patterns from the
codebase into CONTEXT.json. Agents treated these as ground truth and wired endpoints
accordingly. This is the root cause of the routing mismatch.

DS committed P4 Books Tab endpoints (522ffad8) — 4 new `handle_books_*` handlers in
`lambda_function.py` at `/scoped/partners/books/*` paths. These endpoints have NEVER
been invoked because no API Gateway routes existed for them.

DE committed P4 proxy wiring (deff097 on portal DEV) — TypeScript functions calling
`/api/scoped/partners/books/*` paths. These fetch calls return 404 from API Gateway
because the routes didn't exist. DE marked their task order complete.

### 2026-03-16: Addendum A sprint

**DS 005** (6cae4815): Committed 06b gold script + mix-timeseries/concentration-timeseries
Lambda endpoints. Code is structurally correct. Marked task order complete.

**AE 005** (d1bd3a18, 9ee5a752): Wired 06b into run_gold_layer.sh, deployed to EC2,
ran full rebuild. Both gold artifacts produced. Gate 2 PASSED (0 pct sum failures across
2.6M groups). AE work is genuinely complete.

**DT 005** (ddce9fef): Created `partners-api/` Terraform module, imported Lambda,
applied config changes (256->1024MB, 30->120s timeout), tagged `partners-api-v1.0.0`.
**BUT**: the Lambda artifact was built from code BEFORE the DS 005 commit. The deployed
Lambda did not include the Addendum A endpoints. DT's session log explicitly notes this
in "Blockers" (line 35-36) and "Next Steps" (steps 3-8 not executed). DT did NOT mark
their task order complete — **COO marked it complete based on Andrew's verbal
confirmation, without verifying the session log.**

**DT hotfix** (da5c527f, partners-api-v1.0.1): DT discovered the actual breakage:
1. **6 API Gateway routes for `/api/scoped/partners/books/*` never existed** — Lambda
   hadn't been invoked since 2026-02-25.
2. **awswrangler 3.11.0 breaking change** — `pyarrow_additional_kwargs={'filters': ...}`
   no longer works. All 4 `wr.s3.read_parquet()` call sites with filters were broken.
3. **pd.NA boolean ambiguity** — awswrangler 3.x defaults to `dtype_backend='numpy_nullable'`,
   causing `TypeError` in `_classify_holding()` and `conc_key` builder.
4. **API Gateway routes initially created without authorizer** — Lambda saw empty auth
   context and returned 403.

DT fixed items 1-4, verified timeseries (424 records) and composition (2 classes, top-10)
return 200 via direct invocation. Tagged `partners-api-v1.0.1`.

**DE firm param fix** (same day): DE discovered 7 portal API functions missing required
query parameters (`?firm=` for S3-routed, `?firmId=` for Lambda-routed). Fixed the 3
S3-routed functions. The 4 Lambda-routed functions are **partially fixed** — DE used
wrong param name (`?firm=` instead of `?firmId=`) and wrong value (S3 bucket suffix `bd`
instead of DynamoDB firm key `49financial`).

**RD 005** (458c9dc on portal DEV): Built MixTimeseriesPanel and ConcentrationPanel.
Code compiles, uses mock data fallback. Both panels are wired into L3ClientDetail.
RD marked task order complete. The panels would display mock data even if the Lambda
worked, because the `firmId` param is wrong.

**RD P4** (478baea on portal DEV): Built 4e/4f snapshot pies, 4g compact timeseries,
4h advisor listing redesign. Code compiles. Data flows depend on the same broken
firmId parameter chain.

### Net state right now

| Component | Status | Blocker |
|-----------|--------|---------|
| Lambda code (v2 endpoints) | Deployed, awswrangler fixed | Working |
| Lambda code (v3 books endpoints) | Deployed, awswrangler fixed | Working |
| Lambda code (Addendum A endpoints) | **NOT DEPLOYED** | Artifact not rebuilt with DS 005 code |
| API Gateway routes (6 books paths) | Created, authorizer attached | Working |
| Gold artifacts (mix + concentration) | Exist on S3, Gate 2 passed | Working |
| Portal: S3-routed functions (3) | firmOverride param added | **3 fixed, untested** |
| Portal: Lambda-routed functions (4) | Wrong param name, wrong value | **BROKEN** |
| Portal: Mix/Concentration panels | Code exists, mock data fallback | **BROKEN** (wrong firmId) |
| Portal: Books Tab L2 drilldown | Advisor book fetch missing firm | **BROKEN** |
| Portal: Books Tab L3/L4 | Composition + timeseries missing firmId | **BROKEN** |
| Portal DEV -> PROD merge | Not done | All portal work invisible on production |

---

## Root Causes

### RC1: Embedding-seeded stale API routes (systemic)
The thread embedding strategy pulled deprecated route definitions into CONTEXT.json.
Agents treated embedded context as ground truth and wired against routes that don't
exist. No pre-flight verification of embedded routes against live infrastructure.

### RC2: No API Gateway routes for `/scoped/partners/books/*` (infrastructure)
The opal-partners-data Lambda was manually deployed (pre-Terraform) and only had routes
for `/api/partners` and `/api/shared/advisor-intelligence/*`. The v3 Books endpoints
were added to the Lambda code in March but the API Gateway was never updated to route
traffic to them. Lambda hadn't been invoked since Feb 25.

### RC3: awswrangler 3.x breaking changes (runtime)
The AWSSDKPandas layer upgraded to awswrangler 3.11.0 which changed the filter API
and default dtype backend. The Lambda code was written against 2.x patterns. Every
parquet read with filters was broken. Every nullable string column caused TypeError.

### RC4: firmId naming collision (architecture)
Two different routing mechanisms use differently-named parameters pointing to different
ID spaces:
- `?firm=bd` — S3 bucket suffix for shared-advisor-router (Lambda@Edge)
- `?firmId=49financial` — DynamoDB partition key for opal-partners-data Lambda

The portal's `selectedFirmId` is `'bd'` and no mapping to `'49financial'` exists in
the frontend. All Lambda-routed API calls pass the wrong identifier.

### RC5: COO audit was surface-level (process)
COO's startup correction checked `<status>` fields, git commits, and session logs but
never verified that the deployed system worked. Task orders were marked complete based
on code commits, not on end-to-end verification. The DT 005 task order was marked
complete by COO despite the DT session log explicitly listing unfinished steps.

---

## COO Process Failures

1. **Marked DT 005 complete without reading the session log fully.** The DT log clearly
   states "IN PROGRESS" (line 44) and lists 8 next steps (lines 55-62), of which only
   step 1 was done. COO accepted Andrew's verbal confirmation and edited the status
   without cross-referencing the session log.

2. **Never verified endpoints were reachable.** A single `curl` to any `/api/scoped/partners/books/*`
   path would have revealed the 404. COO has tool access and should have spot-checked
   at least one endpoint before marking the chain complete.

3. **Trusted task order status as ground truth without independent verification.** When
   DE said "done" and marked status complete, COO accepted it. When RD committed code
   that compiles, COO accepted it. Neither constitutes end-to-end verification.

4. **Did not catch the firmId naming collision.** The thread receipt and task orders
   specify `firmId` as a parameter, but no one verified that the portal's `firmId`
   value (`'bd'`) matches what the Lambda expects (`'49financial'`). This is exactly
   the kind of cross-boundary check that Pattern 0 threads are supposed to catch.

---

## What DT Found and Fixed (credit)

DT's hotfix session (partners_api_hotfix_routing_and_compat.md) is the most valuable
log in this entire sprint. It:
- Identified 5 independent root causes
- Fixed the infrastructure issues (API Gateway routes, awswrangler compat, NA safety)
- Correctly scoped the remaining work to DE (firm param fix)
- Documented the firmId naming collision with precision
- Did NOT mark the overall task as complete (status: IN PROGRESS)

---

## Remaining Work to Close ADVI_MVPLVL

1. **DE: Fix Lambda-routed param name and value** — `?firmId=49financial` not `?firm=bd`.
   Requires either a static mapping or wiring `getAllowedPartners` response into the
   page context.

2. **DT: Rebuild Lambda artifact with DS 005 code** — current deployed artifact does
   not include `handle_mix_timeseries` or `handle_concentration_timeseries`. Steps 3-8
   from the original DT session log.

3. **DT: Verify all endpoints end-to-end** — timeseries, composition, mix-timeseries,
   concentration-timeseries for a test relationship.

4. **RD: Remove mock data fallbacks** — once Lambda + firmId are working, panels should
   use live data. Verify rendering.

5. **DT: Portal DEV -> PROD merge + deploy** — nothing is visible on production.

---

## Corrective Actions for COO Process

1. **Add endpoint verification to the quality gate checklist.** Before marking any
   Lambda-backed task order complete, COO must verify at least one endpoint returns
   data (via curl, browser, or Lambda test invoke).

2. **Do not mark task orders complete based on verbal confirmation.** Read the session
   log. If it says IN PROGRESS, it's not complete.

3. **Verify embedded context against live infrastructure.** Before issuing task orders
   from a thread receipt, spot-check at least one API route against the actual API
   Gateway / CloudFront config.

4. **Cross-check firmId / param naming across routing boundaries.** Any time a task
   order references an API parameter, verify the parameter name and value space match
   between the caller (portal) and the receiver (Lambda/router).

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| This file | Session log | No |

---

## Current State

**Status:** IN PROGRESS
**Active branch:** CLOUD

Part 1 (diagnosis) complete. Part 2 will be written after the remaining work items
are resolved, documenting the fixes and final verification.

---

## Next Steps

1. **[0.4.0_DE_ClientPlatform] Resolve firmId mapping** — static mapping or wire
   `getAllowedPartners`
2. **[0.4.0_DT_ClientPlatform] Rebuild Lambda artifact** with DS 005 code, apply,
   verify, tag `partners-api-v1.1.0`
3. **[0.4.0_DT_ClientPlatform] End-to-end verification** of all 6 Books endpoints
4. **[0.4.0_DT_ClientPlatform] Portal DEV -> PROD merge + deploy**
5. **[2.0.0_SA_COO] Write Part 2 postmortem** after fixes land
