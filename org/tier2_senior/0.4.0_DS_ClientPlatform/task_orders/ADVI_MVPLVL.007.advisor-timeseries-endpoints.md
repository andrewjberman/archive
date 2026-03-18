# Task Order: ADVI_MVPLVL.007 — Advisor-Level Timeseries Endpoints for Books L2

**To:** `0.4.0_DS_ClientPlatform`
**From:** `0.4.0_DE_ClientPlatform`
**Project:** `ADVI_MVPLVL`
**Date:** 2026-03-18

---

## Context

The Books tab has been upgraded with a `ConsolidatedOverviewPanel` that replaces the old
`OverviewPanel` + `CompositionPies` pair. The new panel displays:
- Left: ApexCharts donut (asset class segments, total AUA in center) + clickable legend + quarterly AUA metrics bar
- Right: Top holdings horizontal bars, filtered to selected asset class

The quarterly metrics bar shows Current AUA + last 3 quarter-end snapshots with QoQ % deltas.

**Data availability by drill level:**

| Level | Donut (point-in-time) | Quarterly History |
|-------|----------------------|-------------------|
| N1 Firm | via `firmComposition` + `getFirmMixViews` | ✅ `getFirmMixViews` |
| L2 Advisor | via `advisorComposition` synthesis | ❌ **MISSING — this task** |
| L3 Relationship | via `getBooksRelationshipComposition` | ✅ derived from `getBooksRelationshipTimeseries` × `getMixTimeseries('Max')` |
| L4 Account | via `getBooksAccountComposition` | ❌ no account-level mix timeseries (acceptable for now) |

At L2, the quarterly bar currently shows `—` for all 3 historical columns. This task
closes that gap.

---

## Requested Endpoints

### 1. Advisor AUA Timeseries

```
GET /api/scoped/partners/books/advisor/{advisor_id}/timeseries?firmId=
```

**Response shape** — same as `BooksTimeseriesResponse`:
```typescript
interface BooksTimeseriesResponse {
  generated_at: string
  data_as_of: string
  relationship_id?: string  // omit or null at advisor level
  account_id?: string       // omit or null at advisor level
  data: BooksTimeseriesPoint[]
}

interface BooksTimeseriesPoint {
  date: string        // 'YYYY-MM-DD'
  total_aua: number   // advisor book aggregate AUA on that date
  cum_inflows: number
  cum_outflows: number
  nna: number
}
```

- Daily rows from earliest available date to `data_as_of`
- Aggregated across all relationships in the advisor's book
- `firmId` query param maps to DynamoDB firm key (same as existing endpoints)

---

### 2. Advisor Mix Timeseries

```
GET /api/scoped/partners/books/advisor/{advisor_id}/mix-timeseries?firmId=&window=
```

**Response shape** — envelope matching `ClientTimeseriesEnvelope` (same Lambda pattern):
```typescript
interface ClientTimeseriesEnvelope {
  generated_at: string
  data_as_of: string
  relationship_id: string | number  // use advisor_id here
  mix: MixTimeseriesPoint[]
  concentration: ConcentrationResponse
}
```

Where `MixTimeseriesPoint` is:
```typescript
interface MixTimeseriesPoint {
  date: string          // 'YYYY-MM-DD'
  equity: number        // 0-1 fraction
  fixed_income: number
  structured_notes: number
  cash: number
  other: number
}
```

- Daily rows; each row sums to 1.0
- Aggregated across all relationships in the advisor's book (AUA-weighted)
- `window` param: `1Y | 3Y | Max` (same as relationship endpoint)

---

## Frontend Integration

Once deployed, the DE will add to `advisor-intelligence.ts`:

```typescript
export async function getBooksAdvisorTimeseries(advisorId: string, firmOverride?: string): Promise<BooksTimeseriesResponse> {
  const base = `/api/scoped/partners/books/advisor/${advisorId}/timeseries`
  return await apiRequest<BooksTimeseriesResponse>(firmOverride ? `${base}?firmId=${LAMBDA_FIRM_ID[firmOverride] ?? firmOverride}` : base)
}
```

And add to `ClientsTab.tsx` L2 state:
```typescript
// L2: advisor timeseries for quarterly mix bar
const [l2AuaTimeseries, setL2AuaTimeseries] = useState<{ date: string; total_aua: number }[] | null>(null)
const [l2MixTimeseries, setL2MixTimeseries] = useState<MixTimeseriesPoint[] | null>(null)
```

These feed `deriveQuarterlyFromTimeseries` (already implemented) to produce `l2QuarterlyMix`
for the L2 `CanonicalBookView` call (currently passing `quarterlyMix={null}`).

---

## Acceptance Criteria

1. `GET /api/scoped/partners/books/advisor/{advisor_id}/timeseries?firmId=49financial` returns
   daily AUA rows for a known advisor (e.g., `travis_penfield`)
2. `GET /api/scoped/partners/books/advisor/{advisor_id}/mix-timeseries?firmId=49financial&window=Max`
   returns daily mix rows summing to ~1.0 per row
3. At L2 in the portal, the quarterly metrics bar shows real AUA values instead of `—`
4. Zero TypeScript errors: `bun x tsc -b --noEmit`
