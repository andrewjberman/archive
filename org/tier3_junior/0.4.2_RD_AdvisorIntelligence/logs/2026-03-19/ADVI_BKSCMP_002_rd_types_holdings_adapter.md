# ADVI_BKSCMP.002 -- RD Types + Holdings Adapter

**Agent:** 0.4.2_RD_AdvisorIntelligence
**Date:** 2026-03-19
**Task Order:** ADVI_BKSCMP.002.rd-types-holdings-adapter.md
**Status:** COMPLETE
**Commit:** `6266d17` on portal DEV

## Summary

Extended types.ts and ConsolidatedOverviewPanel holdings block for schema-adaptive
N1/L2 composition support (ADVI_BKSCMP WS3a + WS3b).

## Changes

### types.ts
- MixItem: added optional `top_holdings?: ConcentrationItem[]` and `other?: { market_value; pct }`
- BooksCompositionResponse.scope: added optional `advisor_id` and `firm_id`
- BooksCompositionResponse: added root-level optional `top_holdings?: ConcentrationItem[]` and `other?: { market_value; pct }`

### ClientsTab.tsx (ConsolidatedOverviewPanel only)
- Replaced derivation block (lines 875-884) with schema-adaptive version:
  - `hasPreAggregated` flag detects N1/L2 schema via `mix.some(m => top_holdings?.length > 0)`
  - `cappedItems` IIFE resolves from per-class or global top_holdings (N1/L2) or flat concentration.items (L3/L4)
  - `otherEntry` IIFE resolves from per-class/global other (N1/L2) or concentration.other (L3/L4)
- Removed `showFilteredOther` -- replaced two render blocks with single unified `showOther && otherEntry` block
- Updated empty state: `!hasPreAggregated && concentration.items.length === 0`
- Added `ConcentrationItem` to type import

## Verification
- `bunx tsc -b` passes clean (zero type errors)
- Backward-compatible: L3/L4 path unchanged; 404 from new Lambda routes causes `hasPreAggregated=false` fallback
- No other ConsolidatedOverviewPanel code modified (donut, legend, quarterly bar untouched)

## Gate
- This commit is a WS6 portal merge gate
- RD does NOT push -- DT pushes portal DEV to remote
