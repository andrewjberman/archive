# Thread Receipt: Pattern 0: stacked bar + rolling flows data contract

**Thread ID:** ADVI-004-pattern-0-stacked-bar--rolling-flows-dat
**Project Serial:** ADVI-004
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-03T22:05:12Z
**Status:** complete
**Participants:** 0.4.0_DS_ClientPlatform, 0.4.0_DE_ClientPlatform, 0.4.2_RD_AdvisorIntelligence

---
## 000.md

---
agent: 2.0.0_SA_COO
turn: 0
timestamp: 2026-03-03T22:04:59Z
signal: continue
---

## Pattern 0 Alignment -- Advisors Tab Stacked Bar + Rolling 1Y

I am the COO convening this alignment thread. The Advisors tab rolling flows visualization is being redesigned: replacing 30d/90d/1Y window line charts with a stacked bar (period aggregations) primary view and a fixed-1Y rolling line secondary view. DS, DE, and RD must agree on the data shape before any code is modified.

**Turn order:** DS -> DE -> RD. Three turns per agent.

**DS (0.4.0_DS_ClientPlatform) -- your turn first.**

Read script 10 (10_generate_advisor_rolling_flows.py in context) and data_contract.xml before answering. Name specific variable and column names from the file, not from memory.

1. What does script 10 currently compute? Name the specific parquet input files and their columns. Does the source data have inflows and outflows as SEPARATE columns, or only net NNA? Name the exact column names.

2. For the stacked bar: can you compute period-anchored totals (QTD, YTD, 1Y, 3Y, Max) for inflows, outflows, and nna_net per architect AND per implementor? If inflows and outflows are not separate in the source data, flag this as a data gap and propose how to derive them.

3. For the rolling 1Y line: script 10 already has rolling windows. Can it produce daily points across a 3Y+ lookback? What date range does the source data actually cover?

4. What is the current output file and its S3 key? Show the current top-level JSON keys so DE and RD know what already exists vs what is new.

**DE (0.4.0_DE_ClientPlatform):** Read types.ts and AdvisorsTab.tsx before responding. Specify:
- TypeScript interface for the stacked bar data per period
- TypeScript interface for the rolling 1Y series
- How the period toggle maps to data keys
- Outflow encoding requirement from a portal typing perspective

**RD (0.4.2_RD_AdvisorIntelligence):** Read AdvisorsTab.tsx before responding. Specify:
- How negative outflows should be encoded in the data (negative number? separate field? absolute with sign flag?)
- Which charting library (Recharts/Nivo/other) and any constraint it imposes on the data format
- What tooltip fields are required for both views

**IMPORTANT (M2):** If any answer references a parquet column, S3 key, or interface field without citing a specific file in the repo, ask for the exact path or column name before accepting it as ground truth.

**Final turn must produce a structured contract block with:**
- advisor_rolling_flows.json top-level structure (full key list, not just new keys)
- stacked_bar entry shape (exact fields for a single advisor per period)
- rolling_1y series shape (per-advisor structure, date+value format)
- How outflows are encoded (sign convention or separate field)
- TypeScript interface names DE will define
- Period key names (exactly: qtd/ytd/1y/3y/max or confirmed equivalents)
- Any data feasibility caveat (especially if inflows/outflows are derived, not native)


---

## 001.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 1
timestamp: 2026-03-03T22:06:10Z
signal: continue
---

### 1) What script 10 currently computes (inputs + columns; inflows/outflows availability)

Script 10 is `script-10----advisor-rolling-flows-generator.py` (header says “10_generate_advisor_rolling_flows.py”). It reads **three** core gold parquets plus `client_dimension.parquet` for “new clients” counts:

**Inputs (S3 bucket + keys)**
- `s3://opal-data-bd/gold/views/nna_aua_by_advisor.parquet` (loaded into `adv_ts`)
  - Columns explicitly read in `load_data()`:
    - `['date', 'architect', 'total_aua', 'cum_inflows', 'cum_outflows', 'nna', 'num_relationships']`
- `s3://opal-data-bd/gold/client_performance.parquet` (loaded into `client_perf`)
  - Columns explicitly read:
    - `['date', 'relationship_id', 'total_aua', 'cum_inflows', 'cum_outflows', 'nna']`
- `s3://opal-data-bd/gold/accounts_dimension_latest.parquet` (loaded into `acct_dim`)
  - Columns explicitly read:
    - `['relationship_id', 'implementor']`
- `s3://opal-data-bd/gold/client_dimension.parquet` (loaded into `client_dim`)
  - Columns explicitly read:
    - `['relationship_id', 'first_seen_date', 'primary_architect', 'primary_implementor']`

**Key point for stacked bar feasibility:** inflows and outflows are available as **separate columns** in the source data as **cumulative** measures:
- `cum_inflows`
- `cum_outflows`
and net is also present:
- `nna`

This is true in both architect pre-agg (`nna_aua_by_advisor.parquet`) and relationship grain (`client_performance.parquet`). So we do **not** have a “only net NNA” limitation here.

Also note: in rolling computation, script comments: “Outflows are stored as positive cumulative sums” and it outputs `outflows` as a positive number (see `compute_rolling_series()`).

---

### 2) Stacked bar: can we compute period-anchored totals (QTD/YTD/1Y/3Y/Max) for inflows/outflows/nna_net per architect + implementor?

**Yes, for architect and implementor, using existing cumulative columns.**

The script already computes **period-anchored** totals for **MTD/QTD/YTD** in `compute_period_summary()` by diffing cumulative snapshots:
- `_compute_nna_for_range(sorted_df, advisor_col, start_date, end_date)`:
  - Uses `nna`, `cum_inflows`, `cum_outflows` at `actual_end` minus `actual_base`.

So extending to **1Y / 3Y / Max** is straightforward:
- For **1Y**: `start_date = latest_date - Timedelta(days=365)` (or “same date last year” logic)
- For **3Y**: `start_date = latest_date - Timedelta(days=365*3)`
- For **Max**: `start_date = min(date)` (or base snapshot = earliest available)

**Architects**
- Use `adv_ts` (already at `(date, architect)` grain with cumulative fields).

**Implementors**
- Script builds implementor daily cumulative series on the fly in `build_implementor_daily()`:
  - Joins `client_perf` to modal implementor per relationship derived from `acct_dim.groupby('relationship_id')['implementor'].agg(_modal_str)`
  - Then aggregates to `(date, implementor)` with:
    - `cum_inflows=('cum_inflows','sum')`
    - `cum_outflows=('cum_outflows','sum')`
    - `nna=('nna','sum')`
So we can apply the same period-diff method to implementors too.

**No data gap on inflows/outflows**: we do not need to derive inflows/outflows from net; they exist as `cum_inflows` and `cum_outflows` and are differenced over the period.

One caveat to decide with DE/RD: whether the stacked bar should encode outflows as **negative** (for plotting below axis) or keep positive and let frontend negate. Script 10 currently outputs outflows as positive magnitudes.

---

### 3) Rolling 1Y line: can script 10 produce daily points across a 3Y+ lookback? What date range does source cover?

**Mechanically yes**, but with an important nuance:

- Current rolling series output is produced by `compute_rolling_series()` for windows in `WINDOWS = {'30d':30,'90d':90,'1Y':365}`.
- It computes rolling diffs via `pd.merge_asof` using `target_date = date - window_td`.
- It outputs a point for every date where a past date exists (so for 1Y, you need at least ~365 days of history per advisor).

**To support the new UI requirement:**
- Secondary view wants **fixed 1Y rolling window**, but the **x-axis window** can be QTD/YTD/1Y/3Y/Max.
- That means we should output `rolling_1y` daily points for as long as we have history (ideally “Max”), and the frontend slices by selected period.

**Date range coverage:** script 10 does not hardcode a range; it uses whatever is in:
- `adv_ts['date']` and `client_perf['date']`.
It sets:
- `latest_date = adv_ts['date'].max()`
but does **not** print or enforce `min(date)`.

So: it *can* produce 3Y+ lookback **if** the underlying parquets contain 4Y+ of daily history (because 1Y rolling needs 1Y warmup before the first valid point). If the gold data is only ~2 years, then “3Y/Max” x-axis will not have full coverage.

Action item for me (outside this thread) is to check actual min/max dates in those parquets (but per thread rules, I’m not going to claim a date range without reading the actual parquet).

---

### 4) Current output file, S3 key, and current top-level JSON keys

**Output location (constants at top of script 10):**
- `OUTPUT_BUCKET = 'opal-data-bd'`
- `OUTPUT_KEY = 'gold/advisor_rolling_flows.json'`
So: `s3://opal-data-bd/gold/advisor_rolling_flows.json`

**Current top-level JSON keys** returned by `generate_advisor_rolling_flows()`:
- `generated_at`
- `data_as_of`
- `firm_id`
- `summary`
  - `architects` (period summaries)
  - `implementors` (period summaries)
- `architects` (rolling series list)
- `implementors` (rolling series list)

**Current rolling series shape (per advisor)** (from `compute_rolling_series()`):
- `advisor_name`
- `advisor_id` (prefix `arch_` or `impl_` + slug)
- `series`:
  - `30d`: list of `{date, nna, inflows, outflows}`
  - `90d`: same
  - `1Y`: same

---

### Questions / alignment needed before I implement changes (so we don’t thrash)

1) **Outflows sign convention for stacked bar**: do we want backend to emit `outflows` as negative numbers for bar chart stacking, or keep positive and let frontend render downward? (Script currently treats outflows as positive magnitudes everywhere.)

2) **Advisor identifier**: stacked bar requires “one bar per person”. We already have `advisor_id` in script 10 (`arch_{slug}` / `impl_{slug}`). Confirm DE/RD want to key on `advisor_id` (stable) and display `name`, vs keying on `name`.

3) **Periods**: stacked bar needs `qtd/ytd/1y/3y/max`. Script currently has `mtd/qtd/ytd` in `summary`. We can add new periods without breaking existing consumers, but DE should confirm whether to keep `mtd` (legacy) or deprecate it.

I can propose a concrete JSON extension in my next turn once DE/RD state their typing + charting constraints.

---

## 002.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 2
timestamp: 2026-03-03T22:06:38Z
signal: continue
---

### DE response — portal typing + encoding constraints for Pattern 0 (stacked bar + rolling 1Y)

Anchors (per COO instruction):
- Portal types live in `portal/src/pages/AdvisorIntelligence/types.ts` (excerpt in context includes current `AdvisorRollingFlowsResponse`, `AdvisorRollingSeries`, etc.).
- Current Advisors tab implementation is `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` (excerpt in context shows it consumes `AdvisorRollingFlowsResponse` and expects `series[window]` where `window` is `'30d'|'90d'|'1Y'`).

DS has confirmed script 10 inputs include **separate cumulative** `cum_inflows` and `cum_outflows` plus `nna` (net) in:
- `gold/views/nna_aua_by_advisor.parquet` and `gold/client_performance.parquet` (and implementors derived via join).

So from a portal perspective, we can safely contract for `inflows`, `outflows`, `nna_net` without inventing fields.

---

## 1) Proposed TypeScript interfaces (new contract additions)

We should **extend** the existing `AdvisorRollingFlowsResponse` rather than replace it, to avoid breaking any deployed portal code while RD migrates the UI.

### Period keys (exact)
Per PRD: `qtd | ytd | 1y | 3y | max` (lowercase in JSON).  
Note: existing response uses `mtd/qtd/ytd` in `summary` (legacy). We can keep that as-is and add the new structure under new keys.

```ts
// Advisors Tab (new Pattern 0 contract)
export type AdvisorRoleKey = 'architects' | 'implementors'
export type RollingPeriodKey = 'qtd' | 'ytd' | '1y' | '3y' | 'max'

// Stacked bar entry (one bar per advisor for a selected period)
export interface AdvisorBarEntry {
  advisor_name: string
  advisor_id: string
  inflows: number        // dollars, >= 0
  outflows: number       // dollars, see encoding decision below
  nna_net: number        // dollars, can be negative
}

// Stacked bar payload by role and period
export interface AdvisorStackedBarByRole {
  architects: Record<RollingPeriodKey, AdvisorBarEntry[]>
  implementors: Record<RollingPeriodKey, AdvisorBarEntry[]>
}

// Rolling 1Y series point (fixed rolling window = 1Y)
export interface Rolling1YDataPoint {
  date: string           // YYYY-MM-DD
  nna: number
  inflows: number
  outflows: number
}

// One advisor’s rolling 1Y series
export interface AdvisorRolling1YSeries {
  advisor_name: string
  advisor_id: string
  series: Rolling1YDataPoint[]
}

// Rolling 1Y payload by role
export interface AdvisorRolling1YByRole {
  architects: AdvisorRolling1YSeries[]
  implementors: AdvisorRolling1YSeries[]
}
```

### Top-level response extension
```ts
export interface AdvisorRollingFlowsResponseV2 extends AdvisorRollingFlowsResponse {
  // New Pattern 0 additions
  stacked_bar?: AdvisorStackedBarByRole
  rolling_1y?: AdvisorRolling1YByRole
}
```

This keeps backward compatibility: existing keys `summary`, `architects`, `implementors` remain valid for the current line-chart implementation until RD switches.

---

## 2) Period toggle mapping (portal behavior)

UI period toggle values (per PRD) should map 1:1 to JSON keys:

| UI label | JSON key |
|---------|----------|
| QTD | `qtd` |
| YTD | `ytd` |
| 1Y | `1y` |
| 3Y | `3y` |
| Max | `max` |

For the **rolling 1Y line** secondary view: the toggle controls **x-axis slice only**. The data itself is always 1Y-rolling; portal slices `series` to the selected lookback window.

---

## 3) Outflow encoding requirement (typing + charting)

We need one explicit convention in the contract so RD doesn’t guess:

**My recommendation (portal-friendly, least ambiguous):**
- `inflows`: positive number (>= 0)
- `outflows`: **positive magnitude** (>= 0)
- `nna_net`: signed (can be negative)

Reason: this matches script 10’s current semantics (“outflows stored as positive cumulative sums; rolling diff stays positive”) and avoids mixing sign conventions across fields.

**Rendering rule in stacked bar:**
- When plotting, frontend can render outflows downward by using `-outflows` for the outflow stack segment, while still showing tooltip values as absolute dollars.

If RD strongly prefers backend to emit `outflows` as negative for stacked bars, we can do that, but then we must also decide whether rolling_1y outflows should be negative (I’d avoid that; it will confuse tooltips and any “inflows - outflows == nna” validation).

So: I’m asking RD to confirm they can work with **positive outflows** + “negate for chart only”.

---

## 4) Contract deltas vs existing portal types

Current portal type (from `portal/src/pages/AdvisorIntelligence/types.ts`) is:

- `AdvisorRollingFlowsResponse`:
  - `summary` keyed by `mtd/qtd/ytd`
  - `architects[]` and `implementors[]` each with `series: Record<'30d'|'90d'|'1Y', RollingFlowsDataPoint[]>`

Pattern 0 adds:
- `stacked_bar` (period-anchored totals with inflows/outflows/net)
- `rolling_1y` (single fixed rolling window series, long history)

No portal code should be modified until DS confirms final JSON shape + sign convention, but these interfaces are what I will ask RD to implement against once DS publishes the updated `data_contract.xml`.

---

## 5) Two clarifying questions for DS (to lock contract)

1) For `stacked_bar`, will DS compute `nna_net` directly as period diff of `nna` (preferred), and do we expect `nna_net ≈ inflows - outflows` always? (script 10 currently validates this for rolling points with a tolerance).
2) For `rolling_1y`, can DS emit a single `series[]` per advisor (not nested by window) to simplify the portal? (This matches PRD: rolling window fixed at 1Y.)

Once RD responds on outflow sign + chart constraints, we can converge on the final structured contract block in the thread’s final turn.

---

## 003.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 3
timestamp: 2026-03-03T22:07:04Z
signal: continue
---

### RD response — charting + encoding constraints for Pattern 0 (stacked bar + rolling 1Y)

Anchors:
- Current Advisors tab file: `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` (in context). It currently renders rolling flows as Recharts `LineChart` and expects `outflows` as a positive magnitude (it never negates it; it just plots whatever `pt[metric]` is).
- Existing types: `portal/src/pages/AdvisorIntelligence/types.ts` includes `RollingFlowsDataPoint { date, nna, inflows, outflows }` and `AdvisorRollingSeries.series[window]`.

Given that, I want the new contract to be explicit and consistent with existing semantics so we can migrate without breaking tooltips / validation.

---

## 1) Outflows encoding (stacked bar + rolling line)

**I agree with DE’s recommendation: keep `outflows` as a positive magnitude in the JSON** for both `stacked_bar` and `rolling_1y`.

- `inflows`: positive (>= 0)
- `outflows`: positive magnitude (>= 0)
- `nna_net` / `nna`: signed (can be negative)

**Frontend rendering rule:**
- For the stacked bar visualization only, I will render the outflow segment as negative by passing `-outflows` into the chart data for that series/stack key.
- Tooltips will display outflows as an absolute positive dollar amount (since the raw field is positive, no special casing needed).

This matches script 10’s current behavior and avoids a “sometimes negative, sometimes positive” outflows field across views.

---

## 2) Charting library + data format constraints

### Stacked bar (primary view)
I will use **Recharts** (already in use on this page; no new deps). Likely `ComposedChart` or `BarChart` with:
- One bar per advisor (`advisor_id` as stable key; `advisor_name` for label)
- Two stacked bars:
  - `inflows` (positive)
  - `outflowsNeg` (computed in UI as `-outflows`)

This requires the stacked-bar dataset to be an array of rows like:
```ts
{
  advisor_id: string
  advisor_name: string
  inflows: number
  outflows: number
  outflowsNeg: number // derived client-side = -outflows
  nna_net: number
}
```
So backend does **not** need to emit `outflowsNeg`.

Sorting requirement (per PRD): “sorted lowest to highest by NNA so highest performers are rightmost”.
- I will sort by `nna_net` ascending in the UI (or DS can pre-sort; either is fine, but UI sort is safer for determinism).

### Rolling 1Y line (secondary view)
Also **Recharts LineChart** (same as current `RollingFlowsChart` pattern), but simplified:
- One line per advisor
- Data points: `{ date, valueByAdvisorId... }` is how current code builds it (dateMap). That approach still works if DS emits `rolling_1y.series: {date, nna, inflows, outflows}[]`.

Constraint: to support period toggles (QTD/YTD/1Y/3Y/Max) controlling x-axis range, I need enough history in `rolling_1y.series[]` to slice. If history is limited, UI will still work but “3Y/Max” will just show what exists.

---

## 3) Tooltip fields required (both views)

### Stacked bar tooltip (per advisor)
Minimum fields I need present per `AdvisorBarEntry`:
- `advisor_name` (display)
- `advisor_id` (key)
- `inflows`
- `outflows` (positive magnitude)
- `nna_net`

Tooltip rows I will show:
- Net NNA (signed, formatted currency)
- Inflows (positive)
- Outflows (positive magnitude, displayed as “Outflows” but value positive)
Optionally: a derived “Gross Flows = inflows + outflows” (derived client-side).

### Rolling 1Y line tooltip (per date)
For each hovered date and advisor line:
- advisor display name (map from `advisor_id` -> `advisor_name`)
- value for selected metric (default NNA; possibly allow metric toggle later, but PRD says rolling line is “1-year rolling NNA value” so we can start with NNA only)

So for `rolling_1y` I need at least:
- `date`
- `nna`
(keeping `inflows/outflows` is still useful for future metric toggle parity and validation, but not strictly required if we commit to NNA-only line).

---

## 4) Two contract clarifications I need from DS/DE before we converge

1) **Advisor identity stability:** can we treat `advisor_id` as the canonical key across stacked bar + rolling 1Y + leaderboard row selection? Script 10 currently generates `arch_{slug(name)}` / `impl_{slug(name)}`. If names can change (spelling/casing), this could drift. If there is a more stable upstream ID, I’d prefer it, but I will accept slug IDs if that’s all we have.

2) **Period boundary definitions:** For QTD/YTD/1Y/3Y/Max, confirm whether “1Y/3Y” are trailing-day windows (365/1095 days) vs calendar-year anchored. PRD reads like trailing windows (“1 year ago to today”), so I will assume trailing unless DS says otherwise.

Once those are confirmed, I’m aligned with DE’s proposed interfaces and can implement against:
- `stacked_bar.{architects|implementors}[period] -> AdvisorBarEntry[]`
- `rolling_1y.{architects|implementors} -> AdvisorRolling1YSeries[]`
with outflows positive magnitude and frontend-negated for stacked bar rendering.

---

## 004.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 4
timestamp: 2026-03-03T22:07:29Z
signal: continue
---

Locking in what we can ground in **script 10** (`script-10----advisor-rolling-flows-generator.py`) and answering RD’s two clarifications.

## A) Inflows/outflows availability + sign convention (grounded)

Per `load_data()` in script 10, both architect and relationship sources have **separate cumulative** columns:

- `gold/views/nna_aua_by_advisor.parquet` -> `adv_ts` reads:
  - `cum_inflows`, `cum_outflows`, `nna` (plus `date`, `architect`, `total_aua`, `num_relationships`)
- `gold/client_performance.parquet` -> `client_perf` reads:
  - `cum_inflows`, `cum_outflows`, `nna` (plus `date`, `relationship_id`, `total_aua`)
- Implementors are derived by joining `client_perf` to modal implementor from `gold/accounts_dimension_latest.parquet` (`relationship_id`, `implementor`) in `build_implementor_daily()`, then summing `cum_inflows/cum_outflows/nna` to `(date, implementor)`.

So stacked bar **does not require deriving inflows/outflows from net**; they exist as `cum_inflows` and `cum_outflows` and we period-diff them.

**Sign convention:** script 10 currently treats outflows as **positive magnitudes** (explicit comment in `compute_rolling_series()`):
> “Outflows are stored as positive cumulative sums; rolling diff stays positive”

I agree with DE+RD: keep `outflows` positive in JSON everywhere; frontend negates only for stacked bar rendering.

## B) Can we compute QTD/YTD/1Y/3Y/Max for stacked bar?

Yes. The existing period-diff machinery is `_compute_nna_for_range(sorted_df, advisor_col, start_date, end_date)` which diffs:
- `nna_end - nna_base`
- `cum_inflows_end - cum_inflows_base`
- `cum_outflows_end - cum_outflows_base`

Today it’s used for `mtd/qtd/ytd` inside `compute_period_summary()` (which calls `_get_period_boundaries()`).

To support Pattern 0 stacked bar, we can reuse `_compute_nna_for_range()` with new start dates:
- `qtd`: already defined by `_get_period_boundaries()`
- `ytd`: already defined
- `1y`: `latest_date - Timedelta(days=365)` (trailing window)
- `3y`: `latest_date - Timedelta(days=365*3)` (trailing window)
- `max`: base snapshot = earliest available date (effectively `min(date)`)

This works for both:
- architects: `adv_ts` at `(date, architect)`
- implementors: `impl_daily` at `(date, implementor)` produced by `build_implementor_daily()`

## C) Rolling 1Y line across 3Y/Max x-axis windows

Mechanically yes: `compute_rolling_series()` already computes windowed diffs using `WINDOWS = {'30d':30,'90d':90,'1Y':365}` and `pd.merge_asof` against `target_date = date - window_td`.

For Pattern 0, we would emit only the `1Y` window as a flat list (RD wants `series: Rolling1YDataPoint[]`), and the portal slices by period toggle.

**Caveat (data coverage):** script 10 does not constrain history; it uses whatever dates exist in the parquets. To have a full 3Y x-axis of 1Y-rolling values, we need ~4Y of underlying daily history (1Y warmup + 3Y display). I cannot claim the actual min/max dates without inspecting the parquet contents; this is a known feasibility caveat until we check.

## D) RD clarification #1: advisor_id stability

Grounded in script 10: advisor IDs are generated from names via `_slugify()` and prefixed:
- architects: `advisor_id = f"arch_{_slugify(advisor_name)}"`
- implementors: `advisor_id = f"impl_{_slugify(advisor_name)}"`

There is **no upstream stable numeric/person ID** in the inputs script 10 reads (architect is a string; implementor is a string). So the best we can do within current gold inputs is slug-of-name.

Risk: if display names change (spelling/casing), IDs drift. Mitigation options (not implemented yet):
1) Keep a persistent mapping table (name -> canonical_id) in gold (new artifact) and have script 10 use it.
2) If upstream BD exports contain a stable advisor identifier, extend gold tables to carry it (requires AE/ETL work).

For this Pattern 0 contract, I recommend we accept `advisor_id` as slug-of-name (current behavior) and treat it as “stable enough” until we see real churn.

## E) RD clarification #2: period boundary definitions

Per PRD language (“1 year ago to today”), I will implement:
- `1y` and `3y` as **trailing day windows** (365 / 1095 days), not calendar-year anchored.
- `qtd` and `ytd` remain calendar anchored (as in `_get_period_boundaries()`).

## F) Proposed contract direction (no code yet; for final convergence)

I’m aligned with DE’s proposed additions:
- `stacked_bar.{architects|implementors}.{qtd|ytd|1y|3y|max} -> AdvisorBarEntry[]`
- `rolling_1y.{architects|implementors} -> AdvisorRolling1YSeries[]`
with `outflows` positive magnitude and `nna_net` signed.

Open item before we “converge” in the final structured contract block: confirm whether we keep existing `summary` (mtd/qtd/ytd donut) and existing rolling windows (`architects[].series['30d'|'90d'|'1Y']`) during migration (I recommend yes, additive only, to avoid breaking current portal until RD switches).

---

## 005.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 5
timestamp: 2026-03-03T22:07:49Z
signal: continue
---

Locking contract details from the portal side based on DS+RD alignment. I am treating this as **additive** to avoid breaking the currently deployed `AdvisorsTab.tsx` which consumes `AdvisorRollingFlowsResponse` (legacy 30d/90d/1Y windows).

## 1) Contract decisions (portal-facing)

### A) Outflows encoding (FINAL)
- `inflows`: positive magnitude (>= 0)
- `outflows`: positive magnitude (>= 0) in JSON everywhere
- `nna_net` / `nna`: signed (can be negative)

Frontend rule (RD confirmed): stacked bar renders outflows downward by using `-outflows` in chart data; tooltips show `outflows` as positive dollars.

This matches script 10 semantics: `cum_outflows` is positive cumulative and rolling diffs are positive.

### B) Period keys (FINAL)
Exact JSON keys (lowercase):
- `qtd`, `ytd`, `1y`, `3y`, `max`

Period boundary definitions (FINAL):
- `qtd`, `ytd`: calendar anchored (existing `_get_period_boundaries()` logic in script 10)
- `1y`, `3y`: trailing windows (365 / 1095 days) per PRD (“1 year ago to today”)
- `max`: inception-to-date (earliest available date in parquet)

### C) Backward compatibility (FINAL)
We keep existing top-level keys so current portal code continues to work until RD migrates:
- keep `summary` (mtd/qtd/ytd donut summaries)
- keep `architects[]` / `implementors[]` rolling series with `series['30d'|'90d'|'1Y']`

Pattern 0 adds **new optional keys**:
- `stacked_bar`
- `rolling_1y`

## 2) TypeScript interfaces DE will define (names + fields)

These will live in `portal/src/pages/AdvisorIntelligence/types.ts` alongside existing `AdvisorRollingFlowsResponse` types.

```ts
export type AdvisorRoleKey = 'architects' | 'implementors'
export type RollingPeriodKey = 'qtd' | 'ytd' | '1y' | '3y' | 'max'

export interface AdvisorBarEntry {
  advisor_name: string
  advisor_id: string
  inflows: number
  outflows: number      // positive magnitude
  nna_net: number       // signed
}

export interface AdvisorStackedBarByRole {
  architects: Record<RollingPeriodKey, AdvisorBarEntry[]>
  implementors: Record<RollingPeriodKey, AdvisorBarEntry[]>
}

export interface Rolling1YDataPoint {
  date: string          // YYYY-MM-DD
  nna: number           // signed
  inflows: number       // positive magnitude
  outflows: number      // positive magnitude
}

export interface AdvisorRolling1YSeries {
  advisor_name: string
  advisor_id: string
  series: Rolling1YDataPoint[]
}

export interface AdvisorRolling1YByRole {
  architects: AdvisorRolling1YSeries[]
  implementors: AdvisorRolling1YSeries[]
}

// Back-compat extension type (do not break existing consumers)
export interface AdvisorRollingFlowsResponseV2 extends AdvisorRollingFlowsResponse {
  stacked_bar?: AdvisorStackedBarByRole
  rolling_1y?: AdvisorRolling1YByRole
}
```

## 3) One remaining question for DS before final contract block (needs explicit yes/no)

For `rolling_1y`, do we guarantee the series is **daily points** (same cadence as current rolling series) and includes `nna/inflows/outflows` (not NNA-only)? RD said NNA-only is acceptable, but keeping all 3 fields is better for future metric toggle parity and validation.

If DS confirms “yes, daily + all 3 fields”, I’ll mark portal contract as fully converged next turn and we can emit the final structured contract block the COO requested.

---

## 006.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 6
timestamp: 2026-03-03T22:08:04Z
signal: continue
---

Portal-side confirmation from me (RD) + one remaining UI-driven requirement to lock before DS implements.

## 1) Confirmed (RD agrees) — outflows encoding + chart behavior

I am aligned with DS + DE:

- `inflows`: positive magnitude (>= 0)
- `outflows`: positive magnitude (>= 0) in JSON everywhere
- `nna_net` / `nna`: signed (can be negative)

**Stacked bar rendering rule (frontend-only):**
- I will derive `outflowsNeg = -outflows` in the chart dataset so the outflow segment renders below the x-axis.
- Tooltip will display `outflows` as a positive dollar amount (no sign confusion).

This matches current `RollingFlowsDataPoint` semantics in `portal/src/pages/AdvisorIntelligence/types.ts` and avoids breaking the existing `AdvisorsTab.tsx` line chart which currently plots `outflows` directly.

## 2) Confirmed (RD agrees) — period keys + slicing behavior

I will implement the period toggle mapping exactly as:

- `qtd`, `ytd`, `1y`, `3y`, `max` (lowercase JSON keys)

And I will treat:
- `qtd`, `ytd` as calendar-anchored
- `1y`, `3y` as trailing windows (365/1095 days)
- `max` as inception-to-date

For the **rolling_1y** secondary view: the period toggle controls **x-axis slicing only** (not the rolling window, which is fixed at 1Y).

## 3) UI requirement to lock: ordering + determinism for stacked bar

PRD requires: “Sorted lowest to highest by NNA so the highest performers are visually rightmost.”

To avoid any ambiguity between backend pre-sort vs frontend sort, I propose we make this explicit in the contract:

- `stacked_bar.*.*` arrays may be **unsorted**; frontend will sort by `nna_net` ascending for display.
- However, each entry must include both `advisor_id` and `advisor_name` so sorting + stable React keys are deterministic.

If DS prefers to pre-sort, that’s fine, but I will still sort client-side to guarantee the visual rule.

## 4) One question for DS (blocking final contract wording)

For `rolling_1y` series points, please confirm:

- Are points **daily** (same cadence as current rolling windows in script 10 output), and
- Will each point include **all three fields**: `{ date, nna, inflows, outflows }` (preferred), not NNA-only?

Reason: even if the initial UI only plots NNA, having inflows/outflows in the same series keeps tooltip extensibility and allows a future metric toggle without another contract change.

Once DS answers this yes/no, I can “converge” next turn with the final structured contract block (top-level keys + stacked_bar + rolling_1y shapes) exactly as COO requested.

---

## 007.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 7
timestamp: 2026-03-03T22:08:17Z
signal: converge
---

## Answer to DE/RD blocking question (rolling_1y point cadence + fields)

Yes — for `rolling_1y`, I will emit **daily points** and each point will include **all three fields**:

- `{ date, nna, inflows, outflows }`

This is directly aligned with the existing rolling output produced by script 10’s `compute_rolling_series()` today (it already emits daily `{date, nna, inflows, outflows}` points for each window label in `WINDOWS`, including `'1Y'`).

Outflows will remain **positive magnitude** (consistent with script 10 comment: “Outflows are stored as positive cumulative sums; rolling diff stays positive”).

---

## Final Structured Contract Block — advisor_rolling_flows.json (Pattern 0 additions)

### File + S3 key (existing)
- **Bucket:** `opal-data-bd`
- **Key:** `gold/advisor_rolling_flows.json`
- Source: `script-10----advisor-rolling-flows-generator.py` constants:
  - `OUTPUT_BUCKET = 'opal-data-bd'`
  - `OUTPUT_KEY = 'gold/advisor_rolling_flows.json'`

### Top-level JSON structure (full key list; additive/back-compat)
```jsonc
{
  "generated_at": "ISO8601 UTC",
  "data_as_of": "YYYY-MM-DD",
  "firm_id": "49financial",

  // legacy (keep)
  "summary": {
    "architects": { "mtd": {...}, "qtd": {...}, "ytd": {...} },
    "implementors": { "mtd": {...}, "qtd": {...}, "ytd": {...} }
  },
  "architects": [ /* legacy rolling series with 30d/90d/1Y windows */ ],
  "implementors": [ /* legacy rolling series with 30d/90d/1Y windows */ ],

  // Pattern 0 additions (new; optional during migration)
  "stacked_bar": {
    "architects": {
      "qtd": [AdvisorBarEntry],
      "ytd": [AdvisorBarEntry],
      "1y":  [AdvisorBarEntry],
      "3y":  [AdvisorBarEntry],
      "max": [AdvisorBarEntry]
    },
    "implementors": {
      "qtd": [AdvisorBarEntry],
      "ytd": [AdvisorBarEntry],
      "1y":  [AdvisorBarEntry],
      "3y":  [AdvisorBarEntry],
      "max": [AdvisorBarEntry]
    }
  },
  "rolling_1y": {
    "architects": [AdvisorRolling1YSeries],
    "implementors": [AdvisorRolling1YSeries]
  }
}
```

### Period key names (FINAL)
Exactly (lowercase): `qtd`, `ytd`, `1y`, `3y`, `max`

Period boundary definitions (FINAL):
- `qtd`, `ytd`: calendar anchored (existing `_get_period_boundaries()` logic in script 10)
- `1y`, `3y`: trailing windows (365 / 1095 days) per PRD
- `max`: inception-to-date (earliest available date in parquet)

### Outflows encoding (FINAL)
- `inflows`: positive magnitude (>= 0)
- `outflows`: positive magnitude (>= 0) in JSON everywhere
- `nna_net` / `nna`: signed (can be negative)

Frontend stacked bar rule:
- render outflows downward by charting `-outflows` (derived client-side), while tooltips display `outflows` as positive dollars.

---

## New object shapes

### `AdvisorBarEntry` (stacked bar; one advisor per period)
```jsonc
{
  "advisor_name": "string",
  "advisor_id": "string",     // script 10: arch_{slug(name)} or impl_{slug(name)}
  "inflows": 123.45,          // >= 0
  "outflows": 67.89,          // >= 0 (positive magnitude)
  "nna_net": 55.56            // signed; computed as period diff of `nna`
}
```

### `AdvisorRolling1YSeries` (rolling line; fixed 1Y rolling window)
```jsonc
{
  "advisor_name": "string",
  "advisor_id": "string",
  "series": [
    { "date": "YYYY-MM-DD", "nna": 0.0, "inflows": 0.0, "outflows": 0.0 }
  ]
}
```

Cadence: **daily points** (subject to whatever daily dates exist in gold parquets; first valid point requires ~365 days of history due to rolling warmup).

---

## TypeScript interface names DE will define (as agreed)

- `AdvisorBarEntry`
- `AdvisorStackedBarByRole`
- `RollingPeriodKey = 'qtd'|'ytd'|'1y'|'3y'|'max'`
- `Rolling1YDataPoint`
- `AdvisorRolling1YSeries`
- `AdvisorRolling1YByRole`
- `AdvisorRollingFlowsResponseV2 extends AdvisorRollingFlowsResponse` with optional `stacked_bar?` and `rolling_1y?`

(Per DE message turn 5.)

---

## Feasibility caveat (explicit)

To display a full **3Y** x-axis of **1Y-rolling** values, we need roughly **4Y** of underlying daily history (1Y warmup + 3Y display). Script 10 will emit whatever history exists in:
- `gold/views/nna_aua_by_advisor.parquet` (`adv_ts['date']`)
- `gold/client_performance.parquet` (for implementors via `build_implementor_daily()`)

I am not asserting the available min/max date range until we inspect the actual parquet contents.

---

This thread is now contract-complete from DS side; next step is implementation work in script 10 + `data_contract.xml` update under the Stream A3 task order.

---

## 008.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 8
timestamp: 2026-03-03T22:08:35Z
signal: converge
---

## Converged — Pattern 0 data contract accepted (stacked bar + rolling 1Y)

I accept DS turn 7 as the final contract for **Pattern 0**. This is now the portal-side source of truth for the Advisors tab redesign (stacked bar primary + fixed 1Y rolling line secondary), and it is consistent with:

- Existing portal types in `portal/src/pages/AdvisorIntelligence/types.ts` (legacy `AdvisorRollingFlowsResponse`)
- Existing UI consumption patterns in `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx`
- Script 10 semantics in `script-10----advisor-rolling-flows-generator.py` (outflows positive magnitude; rolling diffs from cumulative `cum_inflows/cum_outflows/nna`)

### Final contract summary (what portal will build against)

**File / key (unchanged):**
- `s3://opal-data-bd/gold/advisor_rolling_flows.json`

**Top-level keys (full list; additive/back-compat):**
- Keep legacy: `generated_at`, `data_as_of`, `firm_id`, `summary`, `architects`, `implementors`
- Add new optional keys:
  - `stacked_bar`
  - `rolling_1y`

**Periods (exact JSON keys):**
- `qtd`, `ytd`, `1y`, `3y`, `max` (lowercase)

**Outflows encoding (final):**
- `inflows` >= 0
- `outflows` >= 0 (positive magnitude in JSON everywhere)
- `nna_net` / `nna` signed
- Frontend stacked bar renders outflows downward by charting `-outflows` (derived client-side)

**Shapes (final):**
- `AdvisorBarEntry = { advisor_name, advisor_id, inflows, outflows, nna_net }`
- `AdvisorRolling1YSeries = { advisor_name, advisor_id, series: [{ date, nna, inflows, outflows }] }` with **daily points** and all 3 fields present.

### Portal typing plan (DE-owned)

I will define the following interfaces in `portal/src/pages/AdvisorIntelligence/types.ts` (names exactly as agreed in-thread):
- `RollingPeriodKey = 'qtd'|'ytd'|'1y'|'3y'|'max'`
- `AdvisorBarEntry`, `AdvisorStackedBarByRole`
- `Rolling1YDataPoint`, `AdvisorRolling1YSeries`, `AdvisorRolling1YByRole`
- `AdvisorRollingFlowsResponseV2 extends AdvisorRollingFlowsResponse` with optional `stacked_bar?` and `rolling_1y?`

### One explicit caveat (recorded)

We are not guaranteeing 3Y/Max visual completeness for `rolling_1y` until DS inspects actual parquet min/max dates; portal will slice whatever history exists.

## Next actions (outside this thread)

- **[0.4.0_DS_ClientPlatform]** Implement script 10 changes + update `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml` (Stream A3).
- **[0.4.0_DT_ClientPlatform]** Deploy updated gold script / publisher outputs per DS brief once ready.
- **[0.4.2_RD_AdvisorIntelligence]** Implement new stacked bar + rolling_1y UI once DS/DT publish the new keys (keep legacy path until then).

Thread complete.

---
