# ADVI_MVPLVL P4: firmId Mapping Fix on Lambda-Routed Functions -- 0.4.0_DE_ClientPlatform

**Date:** 2026-03-16
**Portal DEV commit:** `db52d31`
**Workspace CLOUD commit:** pending (DT)

## Objective

Fix the 6 Lambda-routed API functions in `advisor-intelligence.ts` that pass the wrong
parameter name (`?firm=`) and wrong value (`bd`, the S3 bucket suffix) to the
`opal-partners-data` Lambda, which expects `?firmId=49financial` (the DynamoDB partition key).

---

## Work Completed

### 1. Added LAMBDA_FIRM_ID Mapping Constant

Added `const LAMBDA_FIRM_ID: Record<string, string> = { bd: '49financial' }` at line 53
in `advisor-intelligence.ts`. This maps S3 bucket suffix to DynamoDB firm key. Only one
firm exists today; the fallback (`?? firmOverride`) handles future firms that may use
their bucket suffix as-is.

### 2. Fixed 4 Books Lambda-Routed Functions

Changed `?firm=${firmOverride}` to `?firmId=${LAMBDA_FIRM_ID[firmOverride] ?? firmOverride}`:

| Function | Line | Route |
|---|---|---|
| `getBooksRelationshipTimeseries` | 372 | `/api/scoped/partners/books/relationship/{id}/timeseries` |
| `getBooksAccountTimeseries` | 382 | `/api/scoped/partners/books/account/{id}/timeseries` |
| `getBooksRelationshipComposition` | 392 | `/api/scoped/partners/books/relationship/{id}/composition` |
| `getBooksAccountComposition` | 402 | `/api/scoped/partners/books/account/{id}/composition` |

### 3. Fixed 2 Addendum A Functions

These already used `?firmId=` (correct param name) but received the raw bucket suffix
as the value. Applied mapping in the `URLSearchParams` constructor:

| Function | Line | Route |
|---|---|---|
| `getMixTimeseries` | 420 | `/api/scoped/partners/books/relationship/{id}/mix-timeseries` |
| `getConcentrationTimeseries` | 442 | `/api/scoped/partners/books/relationship/{id}/concentration-timeseries` |

### 4. Verification

- `bun run build` -- clean, zero errors
- S3-routed functions (getHeaderMetrics, getPartnerAnalytics, getCumulativeChart, getClientsTab,
  getClientDetail, getArchitectLeaderboard, getImplementorLeaderboard, getAdvisorBook,
  getAdvisorRollingFlows, getBooksClientDetail) -- all unchanged, still use `?firm=${firmOverride}`

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Single static mapping object vs. runtime API call | Only one firm exists; static map avoids async complexity and latency. Fallback (`?? firmOverride`) is forward-compatible. |
| Fix at API layer, not at callsite | Callers pass `firmOverride` (bucket suffix) consistently. Translating at the API function boundary is the minimal-touch fix. |
| No changes to ClientsTab.tsx | Requirement 4 verified: the prop chain passes `firmOverride` which flows to `getMixTimeseries`/`getConcentrationTimeseries` as `firmId`. The mapping at the API function handles the translation. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/api/endpoints/advisor-intelligence.ts` | Add LAMBDA_FIRM_ID mapping; fix 4 Books + 2 Addendum A functions | Yes -- portal DEV `db52d31` |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

All 6 Lambda-routed functions in `advisor-intelligence.ts` now send `?firmId=49financial`
instead of `?firm=bd`. The static mapping `LAMBDA_FIRM_ID` at line 53 translates the S3
bucket suffix to the DynamoDB partition key. S3-routed functions are untouched. Task order
`ADVI_MVPLVL.004.p4-books-proxy-wiring.md` marked complete.

---

## Next Steps

1. **[0.4.0_DT_ClientPlatform] Push portal DEV** -- commit `db52d31`
2. **[0.4.0_DT_ClientPlatform] Browser verification** -- navigate to Books Tab, open a
   relationship, confirm timeseries + composition panels load (network tab should show
   `?firmId=49financial`). Also verify Addendum A mix-timeseries and concentration-timeseries.
3. **[0.4.0_DT_ClientPlatform] Commit this log + task order status to CLOUD**
