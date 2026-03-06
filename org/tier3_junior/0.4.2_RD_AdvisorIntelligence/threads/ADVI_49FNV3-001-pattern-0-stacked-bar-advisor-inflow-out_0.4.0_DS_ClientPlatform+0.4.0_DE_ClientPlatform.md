# Thread Receipt: Pattern 0: stacked bar advisor inflow outflow

**Thread ID:** ADVI_49FNV3-001-pattern-0-stacked-bar-advisor-inflow-out
**Project Serial:** ADVI_49FNV3-001
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-06T20:48:29Z
**Status:** complete
**Participants:** 0.4.0_DS_ClientPlatform, 0.4.0_DE_ClientPlatform, 0.4.2_RD_AdvisorIntelligence

---
## 000.md

---
agent: 2.0.0_SA_COO
turn: 0
timestamp: 2026-03-06T20:48:24Z
signal: continue
---

## Pattern 0 Alignment -- F4: Top Ten Advisors Stacked Bar

I am the COO convening this alignment thread for ADVI_49FNV3 (49Financial V3). The F4 fix requires redesigning the Top Ten Advisors panel in AdvisorsTab: replacing the current view with a stacked bar showing blue inflow bars (above zero), red outflow bars (below zero), and a gold horizontal dash showing the net NNA level for each advisor. This is analogous to the NNA bar in the main header panel and the triangle markers in ModelPortfolios Peer Performance.

DS, DE, and RD must agree on the data shape before any code is written.

**Turn order:** DS -> DE -> RD. Three turns per agent.

**DS (0.4.0_DS_ClientPlatform) -- your turn first.**

Read script 10 (10_generate_advisor_rolling_flows.py in context) and data_contract.xml before answering. Name specific variable and column names from the file, not from memory.

1. What does script 10 currently compute per advisor? Name the specific parquet input columns. Does the source data track INFLOWS and OUTFLOWS as separate values per advisor per period, or only net NNA? Name the exact column names in the parquet source.

2. For the F4 stacked bar: can you produce, for each of the top N advisors, an inflow total and outflow total for the selected period (the current window or a fixed look-back)? If inflows/outflows are not separate in source data, flag this as a data gap and propose whether they can be derived from transaction-level data (e.g. summing positive vs negative NNA events per advisor).

3. What is the current output key in advisor_rolling_flows.json for the stacked bar data (Y13 per data_contract.xml)? Show the current shape so DE and RD know what exists vs what is new.

4. What is the sorting key for the top N selection? The PRD says sorted by NNA descending (or total AUA -- confirm with Andrew). Which field do you recommend as the sort key?

**DE (0.4.0_DE_ClientPlatform):** Read types.ts and AdvisorsTab.tsx before responding. Specify:
- TypeScript interface for a single advisor's stacked bar entry (inflow, outflow, nna_net, advisor_name, sort_key)
- How outflows should be encoded in the data (negative number? absolute value with sign flag?)
- What query key or data key maps to this stacked bar in the API response
- How the existing leaderboard data (architect_leaderboard.json) relates to or can be combined with advisor_rolling_flows.json

**RD (0.4.2_RD_AdvisorIntelligence):** Read AdvisorsTab.tsx before responding. Specify:
- How negative outflows should be rendered (bar below zero line, or absolute value with downward orientation?)
- Tooltip fields required: what numbers should appear on hover for each advisor bar
- How the gold NNA dash should be positioned (overlay on bar? separate reference line?)
- Any constraint from the charting library (Recharts/Nivo) on mixed positive/negative bars

**IMPORTANT (M2):** If any answer references a parquet column, S3 key, or interface field without citing a specific file in the repo, ask for the exact path or column name before accepting it as ground truth.

**Final turn must produce a structured contract block with:**
- advisor_rolling_flows.json stacked_bar entry shape (exact fields for a single advisor)
- How outflows are encoded (sign convention or separate field)
- Top N selection: how many advisors, what sort key
- TypeScript interface name DE will define
- Any data feasibility caveat (especially if inflows/outflows must be derived)


---

## 001.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 1
timestamp: 2026-03-06T20:49:07Z
signal: continue
---
### F4 Data Feasibility — Script 10 / advisor_rolling_flows.json (source-grounded)

#### 1) What script 10 computes per advisor + exact parquet input columns
From `data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py` (script 10 in context):

**Inputs + columns loaded (explicit in `load_data()`):**

1) `s3://opal-data-bd/gold/views/nna_aua_by_advisor.parquet` → `adv_ts` (architect daily series)
- columns:
  - `date`
  - `architect`
  - `total_aua`
  - `cum_inflows`
  - `cum_outflows`
  - `nna`
  - `num_relationships`

2) `s3://opal-data-bd/gold/client_performance.parquet` → `client_perf` (relationship daily series)
- columns:
  - `date`
  - `relationship_id`
  - `total_aua`
  - `cum_inflows`
  - `cum_outflows`
  - `nna`

3) `s3://opal-data-bd/gold/accounts_dimension_latest.parquet` → `acct_dim` (relationship→implementor mapping)
- columns:
  - `relationship_id`
  - `implementor`

4) `s3://opal-data-bd/gold/client_dimension.parquet` → `client_dim` (new client counts)
- columns:
  - `relationship_id`
  - `first_seen_date`
  - `primary_architect`
  - `primary_implementor`

**Key point for F4:** inflows/outflows are **separate** in the source data as cumulative fields:
- `cum_inflows` (positive cumulative)
- `cum_outflows` (positive cumulative)
- `nna` (signed cumulative, and in multiple places script checks `nna == inflows - outflows`)

So we are **not** limited to net NNA; we can compute gross inflows and gross outflows per advisor for any period by differencing cumulative endpoints.

#### 2) Can we produce inflow + outflow totals per advisor for a selected period?
Yes. Script 10 already does this in `_compute_nna_for_range()`:

- It selects an **end snapshot** at `actual_end` (closest date `<= end_date`)
- It selects a **base snapshot** at `actual_base` (closest date `< start_date`)
- Then computes deltas per advisor:
  - `inflows = cum_inflows_end - cum_inflows_base`
  - `outflows = cum_outflows_end - cum_outflows_base`
  - `nna = nna_end - nna_base`

This is used in:
- `compute_period_summary()` (for MTD/QTD/YTD donut segments; includes inflows/outflows per advisor)
- `compute_stacked_bar()` (for qtd/ytd/1y/3y/max; includes inflows/outflows per advisor)
- plus the rolling series uses rolling diffs of `cum_inflows/cum_outflows/nna` as well.

So F4’s stacked bar requirements (blue inflows above 0, red outflows below 0, gold dash for net) are fully supported from existing computed fields.

No transaction-level derivation is needed.

#### 3) Current output key + shape for stacked bar data (what exists today)
Per script 10 (see `generate_advisor_rolling_flows()` return dict) and the contract excerpt in context:

Top-level JSON key:
- `stacked_bar`

Shape (period-outer / role-inner nesting):
```json
"stacked_bar": {
  "qtd": {
    "architects":   [AdvisorBarEntry...],
    "implementors": [AdvisorBarEntry...]
  },
  "ytd": { ... },
  "1y":  { ... },
  "3y":  { ... },
  "max": { ... }
}
```

Where `AdvisorBarEntry` is produced in `compute_stacked_bar()` as:
```json
{
  "advisor_name": "<display name>",
  "advisor_id":   "<arch_... or impl_... slug>",
  "inflows":  <float>,   // positive magnitude
  "outflows": <float>,   // positive magnitude
  "nna_net":  <float>    // signed (inflows - outflows)
}
```

Additionally, **Y13 monthly** exists as a separate top-level key:
- `monthly: { "YYYY-MM": [AdvisorBarEntry...] }`
This is already used by the portal’s “Rolling Flows” diverging bar (aggregate-by-month/quarter/year), but it’s also usable for an advisor-level monthly stacked bar if desired.

#### 4) Sorting key recommendation for “Top N”
For the F4 “Top Ten Advisors” stacked bar, I recommend sorting by:
- **primary:** `nna_net` descending (this matches the PRD default “sorted by NNA descending”)
- **secondary (tie-break):** `inflows` descending (or `advisor_name` asc for stable display)

Rationale:
- The visualization is explicitly about flows; net NNA is the most semantically aligned ordering.
- Sorting by `total_aua` would bias toward large legacy books even if they have low/negative flows; that’s a different story than “top performers by flows.”

Open question for COO/Andrew: confirm whether “Top Ten” means top 10 by `nna_net` (recommended) or top 10 by `total_aua` (available in other endpoints like leaderboards / summary segments, but **not** included in `AdvisorBarEntry` today).

---

### One implementation caveat (for DE/RD)
**Outflows sign convention:** script 10 emits `outflows` as **positive magnitude**. For a diverging/stacked bar, frontend should render outflows below zero by negating client-side (e.g., `outflowsNeg = -outflows`). This is already the convention used elsewhere in the portal code (per the AdvisorsTab snippet in context).

---

## 002.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 2
timestamp: 2026-03-06T20:49:33Z
signal: continue
---
### F4 (Top Ten Advisors stacked bar) — DE contract proposal (source-grounded)

DS confirmed the backend already supports **separate inflows/outflows** per advisor via cumulative parquet columns (`cum_inflows`, `cum_outflows`, `nna`) and script 10 emits `stacked_bar` entries with `{ inflows, outflows, nna_net }`. So F4 is **frontend wiring + contract alignment**, not a new data build.

---

## 1) TypeScript interface (single advisor bar entry)

This matches the existing portal type block in context (`advisorintelligence-typescript-types.ts`) and DS’s script 10 output:

```ts
// portal/src/pages/AdvisorIntelligence/types.ts

export interface AdvisorBarEntry {
  advisor_name: string
  advisor_id: string
  inflows: number    // positive magnitude
  outflows: number   // positive magnitude (frontend negates for below-zero bar)
  nna_net: number    // signed (inflows - outflows)
}
```

Optional (if we want explicit sort metadata without recomputing client-side):
```ts
export interface AdvisorBarEntryWithSort extends AdvisorBarEntry {
  sort_key?: number // typically nna_net
}
```
But **not required**—we can sort by `nna_net` in the portal.

---

## 2) Outflows encoding (sign convention)

**Contract decision:** keep backend as-is:
- `outflows` is **positive magnitude** in JSON (per script 10 + data_contract.xml excerpt).
- Frontend derives `outflowsNeg = -outflows` for rendering below zero.

This is consistent with the existing AdvisorsTab implementation pattern in the provided snippet:
- `outflowsNeg: -v.outflows` in `RollingFlowsDivergingBar`.

So: **no backend change requested**.

---

## 3) Data key mapping in API response (where the stacked bar lives)

From the `AdvisorRollingFlowsResponseV2` type in context:

- Endpoint: `GET /api/scoped/advisor-intelligence/advisor_rolling_flows.json`
- Portal API function: `getAdvisorRollingFlows()` (already used in `AdvisorsTab.tsx`)
- Response key for F4: `flowsData.stacked_bar[period][role]`

Where:
- `period` is `StackedBarPeriodKey`: `'qtd' | 'ytd' | '1y' | '3y' | 'max'`
- `role` is `'architects' | 'implementors'`

So the exact lookup for the panel is:

```ts
const entries: AdvisorBarEntry[] =
  flowsData?.stacked_bar?.[period]?.[role] ?? []
```

---

## 4) Relationship to leaderboard data (architect_leaderboard.json)

We should **not** combine leaderboard + rolling_flows for F4 unless we need extra fields (e.g., `total_aua`).

- `architect_leaderboard.json` / `implementor_leaderboard.json` provide ranked entries with `nna`, `total_aua`, etc. (LeaderboardResponse).
- `advisor_rolling_flows.json` provides the **gross flows split** needed for stacked bars: `inflows`, `outflows`, `nna_net`.

For F4’s visual (blue inflows / red outflows / gold net dash), **advisor_rolling_flows.json alone is sufficient**.

If COO later insists “Top Ten” must be by `total_aua`, then we’d need either:
- (A) backend to add `total_aua` into `AdvisorBarEntry`, or
- (B) client-side join on `advisor_id/name` with leaderboard entries.
But for MVP, follow PRD default: **sort by `nna_net`**.

---

## 5) Proposed “Top Ten” selection + sorting (DE recommendation)

- **Top N:** 10
- **Sort key:** `nna_net` descending (DS recommendation; aligns with “Top Performers” semantics)
- **Tie-break:** `advisor_name` asc (stable display)

Implementation is frontend-only:
```ts
const top10 = [...entries]
  .sort((a,b) => (b.nna_net - a.nna_net) || a.advisor_name.localeCompare(b.advisor_name))
  .slice(0, 10)
```

---

## Open question for RD (so we don’t build the wrong thing)
Do we want the gold “NNA dash” to be:
1) a `Line` series at `nna_net` (like the existing `RollingFlowsDivergingBar` does), or
2) a per-bar `ReferenceDot`/custom shape dash centered on each advisor’s x position?

Both are doable in Recharts; #2 matches the PRD wording more literally (“dash per advisor”), while #1 is simpler and already used in the monthly aggregate chart.

---

## Contract block (draft for final convergence)
- **Source:** `advisor_rolling_flows.json`
- **Key:** `stacked_bar.{period}.{role}[]`
- **Entry fields:** `{ advisor_name, advisor_id, inflows, outflows, nna_net }`
- **Outflows encoding:** positive magnitude in JSON; frontend renders below zero via negation
- **Top N:** 10
- **Sort:** `nna_net` desc (tie: `advisor_name` asc)
- **TS interface:** `AdvisorBarEntry` (already defined in `portal/src/pages/AdvisorIntelligence/types.ts` per context)

RD turn should confirm the exact Recharts approach for the gold dash + tooltip field list.

---

## 003.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 3
timestamp: 2026-03-06T20:50:10Z
signal: continue
---

### F4 (Top Ten Advisors stacked bar) — RD rendering contract (AdvisorsTab.tsx grounded)

I’m aligned with DS + DE: we already have `advisor_rolling_flows.json -> stacked_bar` with `inflows/outflows/nna_net` per advisor, and outflows are **positive magnitude** in JSON. Frontend should negate for below-zero rendering.

In the current `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` pattern (see `RollingFlowsDivergingBar` in context), we already use:
- `ComposedChart stackOffset="sign"`
- `Bar` for inflows (positive)
- `Bar` for outflows as a negative field (`outflowsNeg`)
- a gold `Line` for net NNA

For F4, we’ll apply the same diverging-bar mechanics, but at **advisor** grain (top 10 advisors) instead of month/quarter/year aggregates.

---

## 1) Negative outflows rendering (bar below zero)
**Decision:** render outflows below the zero line by negating client-side.

- Data prep:
  - `outflowsNeg = -entry.outflows` (since backend emits outflows as positive magnitude)
- Chart:
  - Use `stackOffset="sign"` on the chart container (ComposedChart or BarChart)
  - Use a shared `stackId` so inflows/outflows share the same x-position (single column per advisor)
  - Add `ReferenceLine y={0}` for the baseline

This matches the existing working pattern in `RollingFlowsDivergingBar` and avoids any backend sign convention changes.

---

## 2) Tooltip fields required (hover on advisor bar)
For each advisor (bar), tooltip should show:

- **Advisor name** (`advisor_name`)
- **Inflows** (positive, formatted currency)
- **Outflows** (positive, formatted currency; display `Math.abs(outflowsNeg)` or original `outflows`)
- **Net NNA** (`nna_net`, signed; show `+` prefix when positive)

Optional but useful (if we keep it consistent with other portal tooltips):
- Percent contribution is *not* available in `AdvisorBarEntry` and not required for F4.

This is exactly the same information we show today in the monthly aggregate tooltip (Inflows/Outflows/NNA).

---

## 3) Gold “NNA dash” positioning (per advisor)
PRD asks for a **gold horizontal dash** per advisor (not a connecting trend line).

**Recommendation:** implement as a per-bar marker, not a line series:
- Use `ReferenceDot` (if available in our Recharts version) at `(x=advisor_name, y=nna_net)` with a custom `shape` that draws a short horizontal segment (dash).
- If `ReferenceDot` isn’t available/behaves oddly with categorical x-axis, use a `Scatter` series with `shape` as a dash (each point renders a dash).
- Fallback (acceptable but less literal): a gold `Line` series with `dot={false}` and `activeDot` customized. This is simpler but visually implies continuity across advisors, which is not semantically true.

So: **primary plan = per-advisor dash marker**; **fallback = gold line** if Recharts constraints bite.

---

## 4) Recharts constraints / implementation notes
- **Mixed positive/negative bars at same x-position:** requires `stackOffset="sign"` + shared `stackId`. Without `stackOffset="sign"`, stacking will be additive and visually wrong (we already learned this in Y4 work).
- **Per-category marker dash:** easiest with custom `shape` rendering; we should avoid SVG absolute positioning hacks. Recharts custom shapes are stable.
- **Sorting + truncation:** top-10 advisors sorted by `nna_net desc` (DE proposal). X-axis labels will need truncation/rotation (we already do `angle={-45}` + truncation in existing charts).

---

## Proposed RD contract additions (to finalize thread)
- **Outflows rendering:** `outflowsNeg = -outflows` client-side; render as red bar below zero with `stackOffset="sign"`.
- **Tooltip fields:** advisor_name, inflows, outflows (abs), nna_net (signed).
- **Gold marker:** per-advisor horizontal dash at `y=nna_net` (custom shape via ReferenceDot/Scatter). Avoid connecting line if possible.

---

## One question back to COO/DE (to avoid rework)
For “Top Ten” selection: confirm we are sorting by **`nna_net`** (flows performance) and not by **`total_aua`** (book size). If it’s `total_aua`, we’ll need either:
- backend to include `total_aua` in `AdvisorBarEntry`, or
- a client-side join with leaderboard entries (more brittle).

---

## 004.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 4
timestamp: 2026-03-06T20:50:44Z
signal: continue
---

## F4 Data Contract — confirm stacked bar feasibility + “top 10” sort decision

### 1) Data feasibility (inflows/outflows are separate — no gap)
Per `data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py`:

- **Architect source parquet**: `gold/views/nna_aua_by_advisor.parquet` loaded with columns  
  `['date','architect','total_aua','cum_inflows','cum_outflows','nna','num_relationships']` (see `load_data()`).
- **Implementor source**: built from `gold/client_performance.parquet` (`cum_inflows`, `cum_outflows`, `nna`) joined to `gold/accounts_dimension_latest.parquet` (`relationship_id`, `implementor`) via `build_implementor_daily()`.

So **gross inflows and gross outflows exist as separate cumulative columns** (`cum_inflows`, `cum_outflows`) and script 10 already computes period deltas via `_compute_nna_for_range()` (delta of cumulative endpoints). No transaction-level derivation required.

### 2) Existing JSON key + exact entry shape (what RD should consume)
`advisor_rolling_flows.json` already contains the advisor-grain stacked bar data under:

- `stacked_bar.{period}.{role}[]` where:
  - `period ∈ ('qtd','ytd','1y','3y','max')` (see `STACKED_BAR_PERIODS`)
  - `role ∈ ('architects','implementors')`

Each entry is produced in `compute_stacked_bar()` as:

```json
{
  "advisor_name": "...",
  "advisor_id": "arch_<slug>" | "impl_<slug>",
  "inflows": 123.45,
  "outflows": 67.89,
  "nna_net": 55.56
}
```

**Sign convention:** `outflows` is **positive magnitude** in JSON (script comment + implementation). Frontend should negate for below-zero rendering.

### 3) Sorting key recommendation (needs COO/Andrew confirmation)
My recommendation remains:

- **Top 10 selection sorted by `nna_net` descending** (flows performance; matches PRD default language “sorted by NNA descending”).
- Tie-break: `advisor_name` asc (stable).

If leadership instead wants “Top 10 by book size”, we have a **data gap in this specific payload**: `AdvisorBarEntry` does **not** include `total_aua`. That would require either:
- backend extension to include `total_aua` in `AdvisorBarEntry`, or
- a client-side join to leaderboard entries (more brittle due to name/id normalization).

### 4) Contract block (ready for converge once sort key confirmed)

```yaml
source: advisor_rolling_flows.json
path: stacked_bar.{period}.{role}[]
period_keys: [qtd, ytd, 1y, 3y, max]
role_keys: [architects, implementors]

AdvisorBarEntry:
  advisor_name: string
  advisor_id: string
  inflows: number        # positive
  outflows: number       # positive magnitude; frontend renders as negative
  nna_net: number        # signed (inflows - outflows)

outflows_encoding: positive magnitude in JSON; client computes outflowsNeg = -outflows
top_n: 10
sort_key: nna_net desc   # pending COO/Andrew confirmation vs total_aua
typescript_interface: AdvisorBarEntry (already defined in portal types)
```

### One explicit question to close F4
Please confirm: **Top 10 is by `nna_net` (recommended) vs `total_aua`**. Once that’s answered, DS side is fully resolved (no backend changes needed for the stacked bar itself).

---

## 005.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 5
timestamp: 2026-03-06T20:51:03Z
signal: continue
---
## F4 (Top Ten Advisors stacked bar) — DE confirmation + final open decision

We have everything we need **data-wise** for F4. DS has cited the exact source columns and script logic; RD has a clear Recharts rendering plan. From the portal side, our types already match the emitted shape.

### 1) Data contract (confirmed)
**Source:** `GET /api/scoped/advisor-intelligence/advisor_rolling_flows.json` via `getAdvisorRollingFlows()`  
**Key path:** `stacked_bar[period][role]` where:
- `period: 'qtd' | 'ytd' | '1y' | '3y' | 'max'`
- `role: 'architects' | 'implementors'`

**Entry shape (already typed in `portal/src/pages/AdvisorIntelligence/types.ts`):**
```ts
export interface AdvisorBarEntry {
  advisor_name: string
  advisor_id: string
  inflows: number   // positive magnitude
  outflows: number  // positive magnitude
  nna_net: number   // signed
}
```

**Outflows encoding:** backend emits `outflows` as positive magnitude; frontend renders below zero via `outflowsNeg = -outflows`. This matches the existing pattern in `AdvisorsTab.tsx`’s `RollingFlowsDivergingBar`.

### 2) Visualization contract (RD-aligned)
- Diverging stacked bars at same x-position: `stackOffset="sign"` + shared `stackId`
- Tooltip fields: `advisor_name`, `inflows`, `outflows` (abs), `nna_net` (signed)
- Gold net marker: prefer per-advisor dash (custom shape via `ReferenceDot`/`Scatter`); fallback to gold `Line` if Recharts constraints.

### 3) The only remaining decision (COO/Andrew)
We need a single explicit decision to lock the contract:

**Top 10 selection + sort key**
- Option A (recommended, PRD-consistent): **sort by `nna_net` desc**, take top 10
- Option B (book-size): sort by `total_aua` desc — **NOT available** in `AdvisorBarEntry` today, would require backend adding `total_aua` to stacked_bar entries or a client-side join to leaderboard (brittle).

**Request:** COO/Andrew confirm A vs B. Once confirmed, RD can implement without any backend changes.

### 4) If COO chooses Option A (nna_net)
No further work needed from DS/DT. DE will just ensure the PRD contract block reflects:
- `top_n = 10`
- `sort_key = nna_net desc` (tie-break `advisor_name asc`)

### 5) If COO chooses Option B (total_aua)
I will open a DS task order to extend script 10 output to include `total_aua` in `AdvisorBarEntry` (or alternatively define a stable join key strategy with leaderboard). But I recommend avoiding this unless explicitly requested.

## Question to close
COO/Andrew: confirm **Top 10 sorted by `nna_net`** (yes/no).

---

## 006.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 6
timestamp: 2026-03-06T20:51:18Z
signal: continue
---

## F4 (Top Ten Advisors stacked bar) — RD final UI contract + implementation-ready details

I’m aligned with DS + DE: **no backend work is required** for the stacked bar itself. `advisor_rolling_flows.json` already provides `stacked_bar.{period}.{role}[]` entries with `inflows`, `outflows` (positive magnitude), and `nna_net` (signed). Frontend will negate outflows for below-zero rendering.

### 1) Rendering contract (Recharts)
**Chart type:** `ComposedChart` (preferred) so we can do bars + net marker overlay in one coordinate system.

**Diverging bars at same x-position (required):**
- `stackOffset="sign"` on the chart container
- `Bar` inflows: `dataKey="inflows"` (positive)
- `Bar` outflows: `dataKey="outflowsNeg"` where `outflowsNeg = -entry.outflows`
- Both bars share `stackId="flows"`
- `ReferenceLine y={0}` baseline

This is the exact proven pattern we already use in `RollingFlowsDivergingBar` in `AdvisorsTab.tsx` (context snippet).

### 2) Tooltip fields (per advisor)
On hover for a given advisor bar, tooltip will show:

- `advisor_name`
- `Inflows` = `inflows` (formatted currency)
- `Outflows` = `abs(outflowsNeg)` (formatted currency)
- `Net NNA` = `nna_net` (signed, `+` prefix when positive)

No percent-of-total required (not in `AdvisorBarEntry`).

### 3) Gold “NNA dash” (per advisor, not a connecting line)
PRD wording is “gold horizontal dash showing NNA level” per advisor. I recommend we implement this as a **per-category marker**, not a line series:

**Primary approach (preferred):**
- Add a `Scatter` series with points `{ x: advisor_name, y: nna_net }`
- Use a custom `shape` that draws a short horizontal SVG line (dash) centered on the point.
- This avoids implying continuity across advisors (a line chart would suggest a trend).

**Fallback approach (acceptable if Scatter/custom shape is finicky with categorical x):**
- Use a gold `Line` with `dataKey="nna_net"` and `dot` customized to look like a dash (or `dot={false}` + `activeDot`), but this is less semantically correct.

### 4) Sorting + top-10 selection (needs COO/Andrew confirmation)
From a UI standpoint, both are easy, but the data contract differs:

- If **Top 10 = by `nna_net` desc**: we can do it purely from `stacked_bar` entries (no joins).
- If **Top 10 = by `total_aua` desc**: `total_aua` is **not** in `AdvisorBarEntry`, so we’d need either:
  - backend to add `total_aua` into stacked_bar entries, or
  - a client-side join with leaderboard (more brittle).

So I’m blocked only on the product decision: **Top 10 by `nna_net` (recommended) vs `total_aua`**.

### 5) Final RD acceptance criteria (what I’ll implement once sort key is confirmed)
- Blue inflows above zero, red outflows below zero (outflows negated client-side)
- Gold per-advisor dash at `y = nna_net`
- Tooltip shows inflows/outflows/net
- Period toggle uses existing `StackedBarPeriodKey` (`qtd|ytd|1y|3y|max`) and role toggle uses `architects|implementors`

## Question to close the thread
COO/Andrew: confirm **Top 10 sorted by `nna_net` descending** (yes/no). If yes, I can implement immediately with no backend changes.

---

## 007.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 7
timestamp: 2026-03-06T20:51:45Z
signal: converge
---

## F4 (Pattern 0) — DS final data contract confirmation (stacked bar advisor inflow/outflow)

### 1) Data feasibility: inflows/outflows are already separate (no data gap)
From `data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py`:

**Architect source parquet:** `s3://opal-data-bd/gold/views/nna_aua_by_advisor.parquet` loaded in `load_data()` with columns:
- `date`, `architect`, `total_aua`, `cum_inflows`, `cum_outflows`, `nna`, `num_relationships`

**Implementor source:** built in `build_implementor_daily()` by joining:
- `s3://opal-data-bd/gold/client_performance.parquet` (columns include `cum_inflows`, `cum_outflows`, `nna`)
- `s3://opal-data-bd/gold/accounts_dimension_latest.parquet` (columns include `relationship_id`, `implementor`)

**Therefore:** gross inflows/outflows exist as separate cumulative fields (`cum_inflows`, `cum_outflows`) and script 10 computes period deltas via `_compute_nna_for_range()` (delta of cumulative endpoints). No transaction-level derivation required.

---

### 2) Existing output key + entry shape (what frontend should consume)
`advisor_rolling_flows.json` already contains the advisor-grain stacked bar data under:

- `stacked_bar.{period}.{role}[]`

Where:
- `period ∈ ('qtd','ytd','1y','3y','max')` (see `STACKED_BAR_PERIODS`)
- `role ∈ ('architects','implementors')`

**AdvisorBarEntry shape** (emitted by `compute_stacked_bar()`):
```json
{
  "advisor_name": "Travis Penfield",
  "advisor_id": "arch_travis_penfield",
  "inflows": 123456.78,
  "outflows": 98765.43,
  "nna_net": 24691.35
}
```

**Outflows encoding:** `outflows` is **positive magnitude** in JSON. Frontend renders below zero by computing `outflowsNeg = -outflows`.

---

### 3) Top N selection + sorting (DS recommendation; product confirmation required)
**Recommendation:** Top 10 sorted by `nna_net` descending (tie-break `advisor_name` asc).

**If leadership instead wants Top 10 by book size (`total_aua`)**: `total_aua` is **not present** in `AdvisorBarEntry` today, so that would require either:
- backend extension to include `total_aua` in stacked_bar entries, or
- a client-side join to leaderboard (brittle due to normalization).

---

## Final contract block (ready; only sort key needs COO/Andrew confirmation)

```yaml
source: advisor_rolling_flows.json
path: stacked_bar.{period}.{role}[]
period_keys: [qtd, ytd, 1y, 3y, max]
role_keys: [architects, implementors]

AdvisorBarEntry:
  advisor_name: string
  advisor_id: string
  inflows: number        # positive
  outflows: number       # positive magnitude; frontend negates for below-zero bar
  nna_net: number        # signed (inflows - outflows)

outflows_encoding: positive magnitude in JSON; client computes outflowsNeg = -outflows
top_n: 10
sort_key: nna_net desc   # pending COO/Andrew confirmation vs total_aua
typescript_interface: AdvisorBarEntry (portal/src/pages/AdvisorIntelligence/types.ts)
```

### Close-out question (must be answered to lock F4)
Confirm: **Top 10 sorted by `nna_net` descending** (recommended) vs **sorted by `total_aua`**.

---

## 008.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 8
timestamp: 2026-03-06T20:52:00Z
signal: converge
---

## F4 (Pattern 0) — Final contract + resolution (stacked bar advisor inflow/outflow)

We have full DS/DE/RD alignment that **inflows/outflows are already separate** and the portal can render the F4 stacked bar **without any backend changes**. The only remaining “product” choice is the **Top 10 sort key**; everything else is locked.

### ✅ Source of truth (already exists)
- **Endpoint:** `GET /api/scoped/advisor-intelligence/advisor_rolling_flows.json`
- **Portal API:** `getAdvisorRollingFlows()`
- **Data key:** `stacked_bar.{period}.{role}[]`

### ✅ Entry shape (contract)
```yaml
AdvisorBarEntry:
  advisor_name: string
  advisor_id: string
  inflows: number        # positive magnitude
  outflows: number       # positive magnitude
  nna_net: number        # signed (inflows - outflows)
```

### ✅ Period + role keys
```yaml
period_keys: [qtd, ytd, 1y, 3y, max]
role_keys: [architects, implementors]
```

### ✅ Outflows encoding (sign convention)
- Backend emits `outflows` as **positive magnitude** (per script 10 + DS confirmation).
- Frontend renders below zero by computing:
  - `outflowsNeg = -outflows`
- Recharts requirement: `stackOffset="sign"` + shared `stackId` + `ReferenceLine y=0`.

### ✅ Top N selection (locked except sort key)
```yaml
top_n: 10
```

### 🔒 Sort key (needs final COO/Andrew confirmation)
- **Option A (recommended / PRD-consistent):** sort by `nna_net` desc (tie-break `advisor_name` asc)
- **Option B (book-size):** sort by `total_aua` desc — **NOT available** in `AdvisorBarEntry` today; would require backend adding `total_aua` to stacked_bar entries or a brittle client-side join to leaderboard.

### ✅ TypeScript interface name (already present)
- **Interface:** `AdvisorBarEntry`
- **File:** `portal/src/pages/AdvisorIntelligence/types.ts`

### ✅ Gold “net dash” rendering (RD plan)
- Prefer **per-advisor dash marker** at `y = nna_net` (Scatter/ReferenceDot with custom dash shape).
- Fallback: gold `Line` series if categorical-x marker is problematic.

## Resolution / thread close
- Data feasibility: **confirmed** (separate `cum_inflows` / `cum_outflows` / `nna` in gold inputs; script 10 already emits `stacked_bar`).
- Implementation scope: **frontend-only**.
- Only remaining decision: **Top 10 sort key** (Option A vs B). Once COO/Andrew confirms, RD can implement immediately.

---
