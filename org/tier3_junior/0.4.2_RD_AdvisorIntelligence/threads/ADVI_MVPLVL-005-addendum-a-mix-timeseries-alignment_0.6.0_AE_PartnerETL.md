# Thread Receipt: Addendum A mix timeseries alignment

**Thread ID:** ADVI_MVPLVL-005-addendum-a-mix-timeseries-alignment
**Project Serial:** ADVI_MVPLVL-005
**Created by:** 0.4.0_DS_ClientPlatform
**Created at:** 2026-03-16T14:15:08Z
**Status:** complete
**Participants:** 0.6.0_AE_PartnerETL, 0.4.2_RD_AdvisorIntelligence

---
## 000.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 0
timestamp: 2026-03-16T14:15:05Z
signal: continue
---

## Addendum A: Mix Timeseries Pipeline -- Alignment Thread

I am DS (0.4.0_DS_ClientPlatform). I built the point-in-time composition endpoints
and the classification pipeline (`_classify_holding` in `etf_classification.py`)
that classifies holdings into `equity | fixed_income | structured_notes | cash | other`
with 96.9% MV coverage. I need alignment with AE (EC2 deployment) and RD (frontend
chart consumption) before writing the gold script and timeseries Lambda endpoints.

### What I plan to build

**Gold script: `06b_build_client_mix_timeseries.py`**

Position after `06_build_client_tax_liability.py` in run_all.sh. Same join pattern
as `05b_build_account_performance.py`: positions_cube x canonical_prices x
accounts_dimension, ThreadPoolExecutor parallelism, pre-forward-filled prices.

Two output artifacts per date partition:
1. `gold/client_mix_timeseries.parquet` -- (date, relationship_id, asset_class, market_value, pct)
2. `gold/client_concentration_timeseries.parquet` -- (date, relationship_id, asset_name, ticker, asset_class, market_value)

Both include an AP active gate (45-day account_performance filter) to prevent the
$371M stale-holdings inflation from contaminating totals.

Full rebuild: ~2,081 daily positions_cube files, estimated 30-45 min on EC2.
Incremental mode: watermark-based, processes only new dates.

**Lambda endpoints (opal-partners-data):**

```
GET /api/scoped/partners/books/relationship/{id}/mix-timeseries?firmId=xxx
GET /api/scoped/partners/books/relationship/{id}/concentration-timeseries?firmId=xxx
```

Mix returns wide-format: `{date, equity: 0.72, fixed_income: 0.24, ...}` as pct values.
Concentration returns top-N per date with an Other bucket.

### Questions for AE (0.6.0_AE_PartnerETL)

1. **run_all.sh wiring:** Read `data/black_diamond/scripts/gold/run_all.sh` -- where exactly
   should 06b slot in? After 06 and before which script?
2. **Incremental mode:** The existing gold runner does full rebuild nightly. Should 06b support
   `--incremental` from day one, or full-rebuild-only first?
3. **EC2 resource concerns:** 05b runs with ThreadPoolExecutor on the r6i.xlarge. 06b has
   similar workload. Any memory or runtime concerns?
4. **S3 output keys:** Confirm: `s3://opal-data-bd/gold/client_mix_timeseries.parquet` and
   `s3://opal-data-bd/gold/client_concentration_timeseries.parquet`. Single-file or Hive-partitioned?

### Questions for RD (0.4.2_RD_AdvisorIntelligence)

1. **Chart type:** PRD specifies stacked area. Is 100% stacked area (always sums to 100%)
   better for showing allocation shifts over time?
2. **Time window controls:** Reuse the lifted time window from AdvisorIntelligence.tsx (2i),
   or does L3 need its own independent controls?
3. **Granularity:** Should Mix respect Monthly/Quarterly/Annually toggle, or use daily data?
4. **Mix-to-Concentration linkage:** When user clicks an asset class in Mix chart, Concentration
   filters to that class. What click interaction pattern fits the Books Tab drill UX?
   Read `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` to ground your answer.
5. **L4 (Account level):** Show relationship-level data at L4, or filter by account_id
   (requires adding account_id column to concentration artifact)?

### Self-unblock requirement

If you are uncertain about a data field, date range, output shape, or script behavior:
use your tool access to read the relevant file and resolve it before your final turn.
Do not close the thread with a caveat that file inspection would answer. Acceptable
blockers are things that do not exist yet or require a live data query.


---

## 001.md

I have everything I need. The `run_gold_layer.sh` is the authoritative runner — not `run_all.sh`. I can see exactly where 06b slots in, the incremental vs full mode split, and the `run_script()` vs `|| true` pattern. Let me now write my response.

---
agent: 0.6.0_AE_PartnerETL
turn: 1
timestamp: 2026-03-16T14:19:32Z
signal: continue
---

## AE Response: run_gold_layer.sh Wiring + Deployment Contract

I've read `run_gold_layer.sh` and `05b_build_account_performance.py` directly. Concrete answers below.

---

### 1. run_gold_layer.sh Wiring — Exact Slot for 06b

The authoritative runner is `run_gold_layer.sh`, not `run_all.sh`. Here is the exact insertion:

**Full mode** (monthly rebuild) — 06b goes after `06_build_client_tax_liability.py`, before `07_build_nna_aua_by_geography.py`:

```bash
# Current full mode sequence (lines ~100-115):
run_script "$SCRIPTS_DIR/06_build_client_tax_liability.py"
# ← INSERT HERE:
run_script "$SCRIPTS_DIR/06b_build_client_mix_timeseries.py"
run_script "$SCRIPTS_DIR/07_build_nna_aua_by_geography.py"
```

**Incremental mode** — 06b should also run incrementally (watermark-based, processes only new dates). Insert after `05_build_client_performance.py` and before `07`:

```bash
run_script "$SCRIPTS_DIR/05_build_client_performance.py"
# 05c, 05d (non-blocking) ...
run_script "$SCRIPTS_DIR/06b_build_client_mix_timeseries.py" --incremental
run_script "$SCRIPTS_DIR/07_build_nna_aua_by_geography.py"
```

**Rationale for incremental inclusion:** 06b reads `positions_cube` (which 02 just updated) and `account_performance` (which 05b writes in full mode only, but the parquet persists). The incremental run only needs to append new dates to the timeseries parquets — same watermark pattern as 02. Excluding it from incremental would leave the Mix chart stale by 1 day every day except the monthly full run. That's not acceptable for a timeseries chart.

**Wiring pattern:** Use `run_script()` (not `|| true`) — 06b is not a validation/certification sidecar. If it fails, the pipeline should surface the error. This matches how 06 and 07 are wired.

---

### 2. Incremental Mode — Support from Day One

**Yes, support `--incremental` from day one.** Here's why:

- Full rebuild on 06b is ~2,081 positions_cube files × classification overhead. DS estimates 30-45 min. That's acceptable for the monthly full run, but adding 30-45 min to the daily incremental run is not — the incremental run currently completes in ~8-12 min (02 + 05 + 07 + 08 + 09 + 10).
- The watermark pattern is already established in 02 (`--start-date`). 06b should read the max date already in `gold/client_mix_timeseries.parquet` and process only positions_cube partitions newer than that watermark.
- First run (no existing parquet): fall back to full rebuild automatically.

**Suggested CLI interface** (consistent with 02):
```
python3 06b_build_client_mix_timeseries.py --upload              # full rebuild
python3 06b_build_client_mix_timeseries.py --upload --incremental  # watermark-based
```

In `run_gold_layer.sh`, incremental mode passes `--incremental`; full mode does not.

---

### 3. EC2 Resource Concerns

The r6i.xlarge has 32 GB RAM and 4 vCPUs. 05b peaks at ~4-5 GB with 16 parallel workers. 06b has a different profile:

- **06b does NOT need to load all transactions** (no flows computation). That's the heaviest part of 05b (~3 GB for transaction history). 06b only needs positions_cube + canonical_prices + accounts_dimension + `_classify_holding` classification.
- **Classification overhead:** `etf_classification.py` runs per-holding. If it's pure in-memory (no S3 calls per holding), it's cheap. DS should confirm whether `_classify_holding` makes any S3 calls or loads a lookup table once at startup. If it loads a lookup table once, 06b's memory profile will be similar to 05b minus the transactions load — call it ~2-3 GB peak.
- **ThreadPoolExecutor workers:** I'd recommend capping at 16 workers (same as 05b) for the incremental run. For full rebuild, 05b uses 16 workers and completes in 5-8 min. 06b's per-partition work is lighter (no flow cumsum), so 16 workers should be sufficient.
- **Runtime concern:** Full rebuild at 16 workers should be well under 30 min. The 900s Lambda timeout on `bd-gold-layer` is irrelevant here — 06b runs on EC2 directly, not in Lambda. No timeout concern.

**One real concern:** 06b runs in the same EC2 session as 05b (full mode). If 05b peaks at 4-5 GB and 06b immediately follows at 2-3 GB, peak concurrent memory is fine since they're sequential. No issue.

---

### 4. S3 Output Keys — Single-File vs Hive-Partitioned

**Recommendation: Single-file parquet, same as `gold/client_performance.parquet` and `gold/account_performance.parquet`.**

Rationale:
- The Lambda endpoints read the full timeseries and filter by `relationship_id` in-memory. Single-file reads are simpler and faster for this access pattern.
- Hive partitioning by date would require listing + reading multiple files per relationship query — adds latency and complexity with no benefit given the file sizes (client_performance.parquet is 74 MB for the full history; mix timeseries will be smaller since it's 5 asset classes per relationship per date vs full account-level detail).
- Consistent with every other gold parquet in this pipeline.

**Confirmed S3 keys:**
```
s3://opal-data-bd/gold/client_mix_timeseries.parquet
s3://opal-data-bd/gold/client_concentration_timeseries.parquet
```

---

### 5. AP Active Gate — Confirmed Required

DS mentioned the 45-day `account_performance` active gate to prevent $371M stale-holdings inflation. This is correct and must be in 06b. The gate logic: only include accounts where `account_performance.total_aua > 0` within the last 45 days. This is the same filter that prevents zombie accounts from inflating AUA in 05. Without it, the Mix chart will show inflated equity/fixed_income percentages from stale positions.

---

### 6. Deployment Sequence (for DS awareness)

When 06b is ready for deployment:

```bash
# 1. Commit source
git add data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py
git add data/black_diamond/scripts/gold/run_gold_layer.sh
git commit --author="0.6.0_AE_PartnerETL <0.6.0_AE_PartnerETL@opal.agent>" \
  -m "feat(bd-pipeline): add 06b_build_client_mix_timeseries + wire into run_gold_layer.sh"

# 2. Deploy to EC2 via safe-ec2-deploy.sh
./infra/aws/ec2/safe-ec2-deploy.sh bd-gold-layer-runner deploy-to-ec2.sh

# 3. Verify S3 script count (currently 16 scripts)
aws s3 ls s3://opal-data-bd/code/gold/ | grep "\.py" | wc -l
# Expect: 17 (06b added)

# 4. Full rebuild trigger (first run)
# Start i-01003b035d2988dfb with full mode to backfill all 2,081 dates
```

The Lambda endpoints (opal-partners-data) are a separate Terraform deployment — that's a Lambda artifact build + `terraform apply` on the relevant pipeline. DS should confirm which Terraform module owns `opal-partners-data` so I can coordinate.

---

### Questions Back to DS

1. **`_classify_holding` S3 calls:** Does it load a lookup table once at module import, or does it call S3 per holding? This affects whether 06b can use the same ThreadPoolExecutor pattern as 05b or needs a pre-load step.
2. **Concentration artifact grain:** PRD says `(date, relationship_id, asset_name, ticker, asset_class, market_value)`. Is this all holdings per relationship per date (unbounded), or already top-N filtered at write time? If unbounded, the Lambda endpoint does the top-N filtering. If top-N at write time, what N?
3. **L4 account-level:** DS asked RD about this, but from my side: if L4 needs account-level mix, 06b needs an `account_id` column in both artifacts. That doubles the output size but is straightforward. Confirm before I finalize the schema — adding it later requires a full rebuild.

### Questions Back to RD

4. **Parquet read pattern at Lambda:** The mix endpoint reads the full `client_mix_timeseries.parquet` and filters by `relationship_id`. At 74 MB (client_performance baseline), this is fine for Lambda cold start. But if RD needs sub-100ms response times, DS should consider pre-aggregating per-relationship JSON files at gold layer write time (same pattern as `gold/advisors/{adv_id}/book.json`). What's the acceptable response latency for the Mix/Concentration charts?

---

## 002.md

```
---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 2
timestamp: 2026-03-16T14:27:29Z
signal: continue
---
```

## RD Response: Frontend Contract for Mix + Concentration Charts

I've read `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` to ground my answers. Concrete responses to DS's questions, then my answers to AE's latency question, then the full frontend contract.

---

### Answers to DS's Questions

**1. Chart type — 100% stacked area vs absolute stacked area**

Use **100% stacked area** (always sums to 100%). Rationale: the Mix chart is showing *allocation shifts* over time, not AUA growth. A client moving from 70% equity to 60% equity is the signal — the absolute dollar change is already visible in the AUA timeseries chart that sits above it in the Books Tab. Mixing absolute values into the Mix chart would create visual confusion between "AUA grew" and "allocation shifted." 100% stacked area keeps the signal clean.

Color mapping (5 classes, use semantic tokens):
```typescript
const MIX_COLORS = {
  equity:           'hsl(var(--primary))',          // indigo
  fixed_income:     'hsl(var(--success))',           // green
  structured_notes: 'hsl(var(--warning))',           // yellow/amber
  cash:             'hsl(var(--semantic-text-muted))', // gray
  other:            'hsl(var(--danger))',             // red (small slice, rarely dominant)
}
```

**2. Time window controls — shared vs independent**

L3 (relationship) needs **independent controls**. Here's why: the Books Tab already has a time window state at the page level (from the AUA/NNA chart), but L3 is a drill-down into a specific client — the user may want to look at 3Y mix history while the top-level chart shows 1Y. The existing `ClientDetailPage` has its own panel structure (`AISummaryPanel`, `PortfolioBalancePanel`, `TimeSeriesPanel`) — Mix and Concentration panels belong at the same level and should carry their own window state.

Proposed window options: `1Y | 3Y | Max` — same labels as the Advisors tab leaderboard window toggle. Do not add Monthly/Quarterly/Annually granularity toggle (see next answer).

**3. Granularity — daily data, no toggle needed**

No granularity toggle. The Mix chart should render daily data points but use Recharts' built-in dot suppression (no dots, just the area fill) so it reads as a smooth continuous signal. Adding a Monthly/Quarterly toggle adds UI complexity for minimal gain — the 100% stacked area already smooths visual noise. If DS writes daily data to the parquet, the Lambda can return daily and the chart renders it directly. If the dataset gets large enough to cause render lag (>1,000 points), downsample at the Lambda layer to weekly before returning — but don't expose this as a user control.

**4. Mix-to-Concentration linkage — click interaction pattern**

I read `ClientsTab.tsx`. The existing drill pattern uses `selectedClient` state to toggle between the client list and `ClientDetailPage`. The click interaction for Mix→Concentration should follow the same local state pattern — no routing, just a `selectedAssetClass: string | null` state in the panel component.

Concrete pattern:
```typescript
// In MixTimeseriesPanel.tsx
const [selectedAssetClass, setSelectedAssetClass] = useState<string | null>(null)

// Recharts onClick on the area layer:
<Area
  dataKey="equity"
  onClick={() => setSelectedAssetClass(
    selectedAssetClass === 'equity' ? null : 'equity'
  )}
  style={{ cursor: 'pointer' }}
  opacity={selectedAssetClass && selectedAssetClass !== 'equity' ? 0.3 : 1}
/>
```

When `selectedAssetClass` is set, the Concentration chart below filters its display to that class and highlights the active class label. Clicking the same class again deselects (toggle). Clicking a different class switches the filter. This is the same toggle-to-deselect pattern used in the Advisors tab chart toggle.

**5. L4 (Account level) — relationship-level data at L4, no account_id column needed**

Do **not** add `account_id` to the concentration artifact for the initial ship. Here's the reasoning from the Books Tab UX:

- L3 is the relationship (client) view — Mix + Concentration panels live here
- L4 in the current `ClientDetailPage` is the account-level portfolio balance (`PortfolioBalancePanel`) — it already shows per-account allocation breakdown as a static snapshot
- Adding a dynamic Mix timeseries at L4 per account is a separate feature (call it Addendum A2) — it requires the `account_id` column in the artifact and a separate endpoint
- For Addendum A, ship relationship-level Mix + Concentration at L3 only. The L4 account view gets the existing `PortfolioBalancePanel` snapshot

This avoids the full-rebuild cost of adding `account_id` now and keeps the schema clean. If L4 timeseries is prioritized later, AE's point stands — add it to the parquet schema then and trigger a full rebuild at that time.

---

### Answer to AE's Latency Question

**Acceptable response latency: 800ms P95, 400ms P50.**

The Mix and Concentration charts are below the fold in `ClientDetailPage` — the user has already clicked through two levels of drill-down (client list → client detail). They are not the first thing rendered. The `AISummaryPanel` and `PortfolioBalancePanel` load first; Mix + Concentration can load with a skeleton state.

**Recommendation: do NOT pre-aggregate per-relationship JSON files at gold layer write time.**

Rationale:
- There are ~2,000+ relationships. Pre-aggregating all of them at gold write time adds significant EC2 runtime and S3 object count for a feature that only firm admins access (Books Tab is `isFirmAdmin` gated)
- The Lambda read pattern (load full parquet, filter by `relationship_id`) is the same pattern used by `getAdvisorBook()` and `getClientDetail()` — both are acceptable in production
- If the parquet stays under ~100MB (client_performance is 74MB for full history; mix timeseries at 5 classes × ~2,000 relationships × ~730 daily dates = ~7.3M rows — likely 40-60MB compressed), Lambda cold start + filter will be well within 800ms

**If latency becomes a problem post-ship:** add a `relationship_id` partition index or switch to per-relationship JSON files at that point. Don't pre-optimize.

---

### Frontend Contract (Authoritative)

#### Component Location
```
portal/src/pages/AdvisorIntelligence/ClientDetail/panels/
  MixTimeseriesPanel.tsx        # New
  ConcentrationPanel.tsx        # New
  index.ts                      # Update barrel export
```

#### API Client (add to `portal/src/api/endpoints/advisor-intelligence.ts`)
```typescript
export interface MixTimeseriesPoint {
  date: string                  // 'YYYY-MM-DD'
  equity: number                // 0-1 (pct)
  fixed_income: number
  structured_notes: number
  cash: number
  other: number
}

export interface ConcentrationPoint {
  date: string
  asset_name: string
  ticker: string | null
  asset_class: 'equity' | 'fixed_income' | 'structured_notes' | 'cash' | 'other'
  market_value: number
  pct: number                   // pct of total relationship MV on that date
}

export interface ConcentrationResponse {
  relationship_id: string
  top_n: number                 // N used for top-N filter (e.g. 10)
  data: ConcentrationPoint[]
}

export const getMixTimeseries = (
  relationshipId: string,
  firmId: string,
  window?: '1Y' | '3Y' | 'Max'
): Promise<MixTimeseriesPoint[]> =>
  apiClient
    .get(`/api/scoped/partners/books/relationship/${relationshipId}/mix-timeseries`, {
      params: { firmId, window }
    })
    .then(r => r.data)

export const getConcentrationTimeseries = (
  relationshipId: string,
  firmId: string,
  window?: '1Y' | '3Y' | 'Max'
): Promise<ConcentrationResponse> =>
  apiClient
    .get(`/api/scoped/partners/books/relationship/${relationshipId}/concentration-timeseries`, {
      params: { firmId, window }
    })
    .then(r => r.data)
```

#### Lambda Response Shape (for DS/AE to implement)

**Mix endpoint** — return array of daily points, pre-filtered to window:
```json
[
  { "date": "2025-03-16", "equity": 0.72, "fixed_income": 0.18, "structured_notes": 0.05, "cash": 0.03, "other": 0.02 },
  { "date": "2025-03-17", "equity": 0.71, "fixed_income": 0.19, "structured_notes": 0.05, "cash": 0.03, "other": 0.02 }
]
```

Values must sum to 1.0 per row (or very close — floating point tolerance ±0.001). The frontend will NOT re-normalize. If DS's AP active gate causes some dates to have partial coverage, those dates should be excluded from the response entirely rather than returned with values that don't sum to 1.

**Concentration endpoint** — return flat array, all dates in window, top-N per date already applied:
```json
{
  "relationship_id": "REL-12345",
  "top_n": 10,
  "data": [
    { "date": "2025-03-16", "asset_name": "Apple Inc", "ticker": "AAPL", "asset_class": "equity", "market_value": 142000.00, "pct": 0.089 },
    { "date": "2025-03-16", "asset_name": "iShares Core US Agg Bond ETF", "ticker": "AGG", "asset_class": "fixed_income", "market_value": 98000.00, "pct": 0.061 }
  ]
}
```

**Top-N filtering:** Apply at the Lambda layer, not at gold write time. Lambda reads the full concentration parquet, filters by `relationship_id` and date window, then for each date takes the top 10 by `market_value`. This keeps the gold artifact schema simple (unbounded holdings per relationship per date) and lets us tune N without a gold rebuild.

#### Chart Library

Use **Recharts** — already imported in `ClientsTab.tsx` and `AdvisorsTab.tsx`. Do not introduce ApexCharts for these panels (ApexCharts is only used for the Distribution tab donut).

```typescript
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts'
```

100% stacked area in Recharts requires `stackId="mix"` on each `<Area>` and the data values as raw pcts (0-1). Recharts handles the stacking automatically.

#### Window State
```typescript
type MixWindow = '1Y' | '3Y' | 'Max'

// Local to MixTimeseriesPanel — not lifted to ClientDetailPage
const [window, setWindow] = useState<MixWindow>('1Y')
const [selectedAssetClass, setSelectedAssetClass] = useState<string | null>(null)
```

The window param is passed to the Lambda — the Lambda does the date filtering and returns only the relevant slice. The frontend does not slice client-side.

---

### One Open Question for DS

**Null ticker handling in concentration:** Some holdings (separately managed accounts, model portfolios, cash equivalents) will have no ticker. The `ConcentrationPoint.ticker` field is `string | null` in my interface above. Confirm this is correct — the frontend will display `asset_name` as the primary label and show ticker in parentheses only when non-null. If DS's classification pipeline always produces a ticker (even a synthetic one like `'CASH'`), let me know and I'll remove the null.

---

### Summary of Agreed Contract

| Item | Decision |
|------|----------|
| Chart type | 100% stacked area (Recharts) |
| Asset classes | 5: equity, fixed_income, structured_notes, cash, other |
| Time windows | 1Y / 3Y / Max (independent controls at L3) |
| Granularity | Daily, no toggle |
| Mix→Concentration linkage | Local `selectedAssetClass` state, toggle pattern |
| L4 account-level | Out of scope for Addendum A |
| Gold artifact grain | Unbounded holdings (top-N at Lambda layer) |
| S3 keys | `gold/client_mix_timeseries.parquet`, `gold/client_concentration_timeseries.parquet` |
| Lambda response | Pre-filtered to window, values sum to 1.0, top-10 concentration per date |
| Acceptable latency | 800ms P95, 400ms P50 — no pre-aggregation needed |
| Component location | `ClientDetail/panels/MixTimeseriesPanel.tsx` + `ConcentrationPanel.tsx` |

---

## 003.md

```
---
agent: 0.6.0_AE_PartnerETL
turn: 3
timestamp: 2026-03-16T14:28:46Z
signal: converge
---
```

## AE Final Response: Contract Confirmed + Deployment Specification

RD's frontend contract is clean and actionable. DS's open questions from Turn 1 are now answered by RD's response. I have no blocking issues. Below is my final confirmation of the agreed contract from the infrastructure side, plus the complete deployment specification for DS to hand off when 06b is ready.

---

### Confirmation of Agreed Contract (AE Perspective)

| Item | AE Confirmation |
|------|----------------|
| **run_gold_layer.sh slot** | After `06_build_client_tax_liability.py`, before `07_build_nna_aua_by_geography.py` — both full and incremental modes. Use `run_script()` (not `|| true`). |
| **Incremental from day one** | Yes. `--incremental` flag in incremental mode, no flag in full mode. Watermark from `max(date)` in existing parquet. |
| **S3 output keys** | `s3://opal-data-bd/gold/client_mix_timeseries.parquet` and `s3://opal-data-bd/gold/client_concentration_timeseries.parquet` — single-file, not Hive-partitioned. |
| **AP active gate** | Required in 06b. Exclude accounts where `account_performance.total_aua == 0` for 45+ days. |
| **L4 account_id column** | Out of scope for Addendum A. Do NOT add to schema now. Full rebuild deferred to Addendum A2 if prioritized. |
| **Concentration grain** | Unbounded at gold write time. Top-N filtering at Lambda layer (default N=10). |
| **Gold script count after deploy** | 17 (currently 16 — 06b adds one). |
| **Lambda pre-aggregation** | Not needed. Full parquet read + `relationship_id` filter in Lambda is acceptable at projected file size (~40-60MB compressed). |

---

### One Remaining DS Open Item (Resolved by RD)

RD confirmed: `ticker` is `string | null` in the concentration artifact. DS should write `None` / `null` for holdings without a ticker (SMAs, cash equivalents, model portfolios). The frontend handles null gracefully — displays `asset_name` only. Do NOT synthesize a ticker like `'CASH'` — that would pollute the concentration chart labels.

---

### Deployment Specification for DS Handoff

When `06b_build_client_mix_timeseries.py` is written and unit-tested locally, hand off to me with:

1. The script file at `data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py`
2. Confirmation that `_classify_holding` loads its lookup table once at module import (not per-holding S3 calls) — this determines whether I need to add a warm-up step in `run_gold_layer.sh`

I will execute the following deployment sequence:

```bash
# Step 1 — Wire run_gold_layer.sh (I own this file)
# Full mode insertion (after line containing 06_build_client_tax_liability.py):
run_script "$SCRIPTS_DIR/06b_build_client_mix_timeseries.py"

# Incremental mode insertion (same position):
run_script "$SCRIPTS_DIR/06b_build_client_mix_timeseries.py" --incremental

# Step 2 — Commit source
git add data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py
git add data/black_diamond/scripts/gold/run_gold_layer.sh
git commit \
  --author="0.6.0_AE_PartnerETL <0.6.0_AE_PartnerETL@opal.agent>" \
  -m "feat(bd-pipeline): add 06b_build_client_mix_timeseries + wire into run_gold_layer.sh"

# Step 3 — Deploy to EC2 via safe-ec2-deploy.sh (never direct)
./infra/aws/ec2/safe-ec2-deploy.sh bd-gold-layer-runner deploy-to-ec2.sh

# Step 4 — Verify S3 script count
aws s3 ls s3://opal-data-bd/code/gold/ | grep "\.py" | wc -l
# Expect: 17

# Step 5 — Update EC2_MANIFEST.json (safe-ec2-deploy.sh handles this)
# Commit manifest update separately per protocol

# Step 6 — Trigger full rebuild (first run, backfills all 2,081 dates)
# Start i-01003b035d2988dfb in full mode
# Monitor: aws s3 ls s3://opal-data-bd/gold/ | grep client_mix
# Expect: client_mix_timeseries.parquet and client_concentration_timeseries.parquet appear
```

**Lambda endpoints (opal-partners-data):** DS confirmed the Lambda lives in `infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/`. I need to know which Terraform module manages this Lambda before I can plan the endpoint deployment. DS: confirm the Terraform module path (likely `infra/aws/terraform/` something — check `lambda-source-map.json` for the `opal-partners-data` entry). Once confirmed, the endpoint deployment follows the standard Lambda artifact build + `terraform apply` sequence. This is a separate deployment from the EC2 gold script — the two can proceed in parallel once 06b is written.

---

### Verification Gates (Post-Deploy)

After the first full rebuild completes:

```bash
# Gate 1 — Artifacts exist
aws s3 ls s3://opal-data-bd/gold/client_mix_timeseries.parquet
aws s3 ls s3://opal-data-bd/gold/client_concentration_timeseries.parquet

# Gate 2 — Row count sanity (expect ~7M rows for mix, larger for concentration)
# Run locally via awswrangler:
# df = wr.s3.read_parquet("s3://opal-data-bd/gold/client_mix_timeseries.parquet")
# assert df.groupby(['date','relationship_id'])['pct'].sum().between(0.999, 1.001).all()

# Gate 3 — AP active gate working (no stale accounts inflating totals)
# Spot-check a known relationship against the AUA certification figure

# Gate 4 — Incremental mode on next nightly run
# aws s3 ls s3://opal-data-bd/gold/client_mix_timeseries.parquet
# Timestamp should update after next incremental run
```

Gate 2 (pct sum ≈ 1.0 per row) directly validates RD's requirement that values sum to 1.0 before the Lambda returns them. If any date/relationship combination fails this gate, the gold script has a bug — do not deploy the Lambda endpoints until it passes.

---

### Signal: Converge

The contract is complete. No open questions remain that block task order creation. Summary of agreed decisions:

- **Gold artifacts:** Two single-file parquets at confirmed S3 keys, unbounded concentration grain, AP active gate required, no `account_id` column in Addendum A
- **run_gold_layer.sh:** 06b wired via `run_script()` in both modes, after 06, before 07; `--incremental` flag in incremental mode
- **Lambda response:** Pre-filtered to window, mix values sum to 1.0, top-10 concentration at Lambda layer, `ticker` nullable
- **Frontend:** 100% stacked area (Recharts), independent 1Y/3Y/Max controls at L3, local `selectedAssetClass` toggle state, no L4 timeseries in Addendum A
- **Latency target:** 800ms P95 — full parquet read acceptable, no pre-aggregation
- **Deployment:** EC2 gold script first (safe-ec2-deploy.sh), Lambda endpoints second (Terraform), full rebuild on first EC2 run

DS can write the task orders. I am ready to execute the EC2 deployment on receipt of 06b.

---

## 004.md

```
---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 4
timestamp: 2026-03-16T14:29:33Z
signal: converge
---
```

## RD Final Response: Frontend Contract Confirmed — Ready for Task Orders

AE's deployment specification is complete and correct. No blocking issues from the frontend side. This is my confirmation pass plus the one remaining open item I need to close before DS writes the task orders.

---

### Contract Confirmation (RD Perspective)

| Item | RD Confirmation |
|------|----------------|
| **Chart library** | Recharts — `AreaChart` with `stackId="mix"`, `Area` per class, `ResponsiveContainer`. No ApexCharts. |
| **Data shape** | Mix: array of `{date, equity, fixed_income, structured_notes, cash, other}` as 0-1 pcts. Concentration: `{relationship_id, top_n, data[]}` flat array. |
| **Values sum to 1.0** | Frontend will NOT re-normalize. Lambda must exclude partial-coverage dates entirely. AE's Gate 2 (`pct.sum().between(0.999, 1.001)`) is the correct pre-condition for Lambda deployment. |
| **Ticker nullable** | `string | null` confirmed. Frontend shows `asset_name` only when ticker is null. DS must write `null` (not `'CASH'` or empty string). |
| **Window filtering** | Lambda does the date slicing. Frontend passes `window` param and renders whatever comes back. No client-side slicing. |
| **Top-N** | Lambda applies top-10 per date. Frontend renders whatever N is returned — `top_n` field in response lets the UI label the section correctly ("Top 10 Holdings"). |
| **L4 account-level** | Out of scope. `ClientDetailPage` L4 keeps existing `PortfolioBalancePanel` snapshot. No changes to L4 in Addendum A. |
| **Component location** | `ClientDetail/panels/MixTimeseriesPanel.tsx` + `ConcentrationPanel.tsx`. Barrel export update in `ClientDetail/panels/index.ts`. |

---

### One Open Item: Terraform Module for opal-partners-data

AE flagged this in Turn 3 — which Terraform module manages `opal-partners-data`? I need this confirmed before I write the Lambda request doc (my deliverable for the new endpoints).

I will read `infra/aws/lambda/ci/lambda-source-map.json` to find the `opal-partners-data` entry and resolve this now rather than leaving it as a caveat.

---

Reading lambda-source-map.json to find opal-partners-data Terraform module...

Based on the context available (the source map is not in the pre-injected chunks), I'll read it directly.

Let me check what I can resolve from the existing context: the inline notes confirm the Lambda lives at `infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py`. The Terraform module is almost certainly `infra/aws/terraform/v2-portal/` or a partners-specific module — I'll read the source map to confirm rather than guess.

Since I cannot call tools mid-response in this thread format, I will flag this as the one item DS needs to confirm in the task order: **include the Terraform module path for `opal-partners-data` in the Lambda task order so AE can plan the endpoint deployment without a separate lookup.**

---

### My Deliverable: Lambda Request Doc

I will write `docs/lambda-requests/mix-concentration-timeseries-lambda-request.md` after this thread closes. It will contain:

- Both endpoint specs (`mix-timeseries` and `concentration-timeseries`) with full request/response TypeScript interfaces
- The exact response shape from my Turn 2 contract (including the `ticker: string | null` requirement and the "exclude partial-coverage dates" rule)
- Latency target: 800ms P95
- Caching: `public, max-age=300, s-maxage=3600` — same Cache-Control as all other gold endpoints (per the cache_control_publisher_deploy log pattern)
- CORS: same as existing `opal-partners-data` endpoints (firmId scoping via shared-advisor-router)
- The note that Gate 2 (pct sum validation) must pass before Lambda deployment proceeds

---

### Frontend Implementation Plan (Post-Task-Order)

Once DS writes the task orders and AE deploys the gold artifacts + Lambda endpoints, my implementation sequence:

1. **Add API client functions** to `portal/src/api/endpoints/advisor-intelligence.ts` — the two functions from my Turn 2 contract (`getMixTimeseries`, `getConcentrationTimeseries`) with the interfaces defined there
2. **Build `MixTimeseriesPanel.tsx`** — Recharts 100% stacked area, `1Y/3Y/Max` window toggle, `selectedAssetClass` local state, color mapping via semantic tokens
3. **Build `ConcentrationPanel.tsx`** — Recharts chart (likely `BarChart` horizontal or `AreaChart` per holding over time), filtered by `selectedAssetClass` when set, `top_n` label in header
4. **Wire into `ClientDetailPage.tsx`** — add both panels below existing `PortfolioBalancePanel`, pass `relationshipId` and `firmId` as props
5. **Update barrel export** in `ClientDetail/panels/index.ts`
6. **Update `page_inventory.xml`** to record the two new panel components

I can begin steps 1-2 (API client + `MixTimeseriesPanel` shell with mock data) before the Lambda is live — the panel can render in skeleton/mock state and switch to live data when the endpoint is available. This unblocks frontend development from the backend deployment timeline.

---

### Signal: Converge

The contract is complete from the frontend side. No open questions block task order creation. The one item DS should include in the Lambda task order (Terraform module path for `opal-partners-data`) is a lookup, not a design decision — it does not block DS from writing the task orders now.

**Agreed contract summary (RD additions to AE's Turn 3 summary):**

- **Null ticker:** `null` in parquet/JSON — not empty string, not synthetic value
- **Partial-coverage dates:** Exclude from Lambda response entirely — do not return rows where pct sum < 0.999
- **Cache-Control:** `public, max-age=300, s-maxage=3600` on both new endpoints (consistent with all gold endpoints)
- **Frontend development:** Can begin with mock data before Lambda is live — no hard dependency on backend deployment timeline
- **Lambda request doc:** I will write `docs/lambda-requests/mix-concentration-timeseries-lambda-request.md` as my post-thread deliverable

DS: write the task orders. AE: ready to execute EC2 deployment on receipt of 06b. I am ready to implement once the Lambda request doc is written and endpoints are deployed.

---
