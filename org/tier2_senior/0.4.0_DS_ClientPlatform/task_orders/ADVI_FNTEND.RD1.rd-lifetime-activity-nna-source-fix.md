# Task Order: ADVI_FNTEND.RD1 — Lifetime Activity NNA Source Fix

**To:** 0.4.2_RD  
**From:** 1.0.0_SA_CTO  
**Date:** 20260416  
**Status:** COMPLETE — commit 75d0ddc (portal DEV). Lifetime Activity NNA hero draws from D_00c MAX leaderboard (same source as Summary Max). All ACs pass per CTO 2026-04-16T18:03Z.

---

## Problem

In `AdvisorPublicProfile.tsx`, the Lifetime Activity panel "Net Flow" hero tile and the Summary (Max) NNA tile show different values for the same advisor. They use different data sources:

- **Summary (Max) NNA** (line 389): `periodNna = entry.nna` — from `PlatinumLeaderboardEntry`, D_00c employee_leaderboard.json MAX window, fee-adjusted via `applyFeeBucket`.
- **Lifetime Activity Net Flow hero** (line 970): `nnaHeroMetrics.totalNet = pickNnaCanon(last)` — from D_02 advisor timeseries `nna_canonical` (last point ITD cumulative).

Different gold scripts, different aggregation grains, different numbers. Travis confirmed ~$95K gap for a real advisor (D_02: $9.46M, D_00c: $9.36M).

The prior fix (`last - first` → `last`) was correct for the timeseries but did not align the source. "Lifetime" semantically means inception-to-date = MAX window. The hero should match Summary (Max).

---

## Fix

**File:** `portal/src/pages/AdvisorIntelligence/AdvisorPublicProfile.tsx`

**Step 1** — Add a `maxWindowEntry` memo (place after `rawEntry` memo, ~line 1498). This always resolves the MAX-window leaderboard entry for the advisor, independent of the current `window` toggle:

```tsx
const maxWindowEntry = useMemo<PlatinumLeaderboardEntry | null>(() => {
  if (!advisorId) return null
  const win = employeeData.windows['MAX']
  return win?.entries.find(e => e.advisor_id === advisorId) ?? null
}, [employeeData, advisorId])

const maxEntry = useMemo(
  () => maxWindowEntry ? applyFeeBucket(maxWindowEntry, feeView) : null,
  [maxWindowEntry, feeView],
)
```

**Step 2** — In `nnaHeroMetrics` (lines 966-974), replace the `totalNet` source:

Current:
```tsx
const nnaHeroMetrics = useMemo(() => {
  if (timeseriesData.length === 0) return { totalNet: 0, totalInflows: 0, totalOutflows: 0 }
  const last = timeseriesData[timeseriesData.length - 1]
  return {
    totalNet:      pickNnaCanon(last),
    totalInflows:  pickInflowsCanon(last),
    totalOutflows: pickOutflowsCanon(last),
  }
}, [timeseriesData, pickNnaCanon, pickInflowsCanon, pickOutflowsCanon])
```

Replace with:
```tsx
const nnaHeroMetrics = useMemo(() => {
  if (timeseriesData.length === 0) return { totalNet: 0, totalInflows: 0, totalOutflows: 0 }
  const last = timeseriesData[timeseriesData.length - 1]
  return {
    totalNet:      maxEntry?.nna ?? pickNnaCanon(last),
    totalInflows:  pickInflowsCanon(last),
    totalOutflows: pickOutflowsCanon(last),
  }
}, [timeseriesData, pickNnaCanon, pickInflowsCanon, pickOutflowsCanon, maxEntry])
```

`maxEntry?.nna` is the MAX-window leaderboard NNA (same source as Summary). Falls back to timeseries cumulative only if MAX entry is not found (should not happen for any active advisor).

---

## Acceptance Criteria

- AC#1: For any advisor with a MAX leaderboard entry, the Lifetime Activity "Net Flow" hero value equals Summary (Max) NNA tile value to the dollar.
- AC#2: QTD/YTD window toggle does not affect the Lifetime Activity NNA hero (it always shows MAX-window leaderboard value).
- AC#3: `bun run build` exits 0, no TypeScript errors.
- AC#4: `comp-transform schema-check AdvisorPublicProfile` exits clean (no new MISSING fields).

---

## Commit

```
git commit --author="0.4.2_RD <0.4.2_RD@opal.agent>" -m "fix(portal): align Lifetime Activity NNA hero to MAX leaderboard source"
```

Push to DEV. Report commit hash + AC results to 1.0.0_SA_CTO.
