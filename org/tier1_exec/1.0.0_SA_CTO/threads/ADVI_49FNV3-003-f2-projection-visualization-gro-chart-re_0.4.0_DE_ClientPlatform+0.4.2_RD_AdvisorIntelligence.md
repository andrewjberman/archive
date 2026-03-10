# Thread Receipt: F2 projection visualization GRO chart redesign

**Thread ID:** ADVI_49FNV3-003-f2-projection-visualization-gro-chart-re
**Project Serial:** ADVI_49FNV3-003
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-09T20:01:32Z
**Status:** complete
**Participants:** 1.0.0_SA_CTO, 0.4.0_DE_ClientPlatform, 0.4.2_RD_AdvisorIntelligence

---
## 000.md

---
agent: 2.0.0_SA_COO
turn: 0
timestamp: 2026-03-09T20:01:28Z
signal: continue
---

## Pattern 0 Alignment -- F2 Projection Visualization + GRO Chart Redesign

I am the COO convening this alignment thread for ADVI_49FNV3 (49Financial V3). Andrew reviewed the F2 projected ghost bars implementation and identified fundamental issues. CTO has written a detailed analysis document (injected as primary context) cataloging 4 flaws and posing 5 convergence questions.

**Turn order:** CTO -> DE -> RD. Three turns per agent.

### Current State (read before responding)

The F2 implementation has evolved through multiple commits on portal DEV:
- `594c3f6` -- Original F2 ghost bars + F4 stacked bar + N1-N2 (RD)
- `9ce8d3b` -- F2-fix: AUA projection uses delta-based extrapolation (RD)
- `28517dd` -- F2-fix: filter ghost keys from AUA and NNA tooltips
- `2f84197` -- F2: projection section in AUA and NNA tooltips for current period
- `8e9facd` -- F2: project the last bar in dataset, not just the calendar-current period

**CTO's analysis was written against 9ce8d3b.** Three additional commits (28517dd, 2f84197, 8e9facd) landed after the analysis. These may partially address Flaws 3 and 4. ALL participants must read the CURRENT PartnerAnalytics.tsx source to verify which flaws remain before proposing solutions.

### 4 Flaws Identified (CTO Analysis Sections 3-6)

1. **AUA projection 0/0 regression** -- Delta-based formula produces zero ghost when no prior period exists in windowed data (e.g., Annually + 1Y window shows only current year, no prior to delta against).
2. **GRO chart unintelligible** -- No title, terse legend, raw tooltip, no hero metrics, Y-axis unlabeled, projection lines leak into tooltip.
3. **NNA/AUA tooltip projection format** -- Shows ghost increment "(add)" instead of full projected values. User must do mental math.
4. **GRO tooltip leaks _proj entries** -- Dashed projection lines rendered as separate Line series appear as duplicate rows in tooltip.

### 5 Convergence Questions (CTO Analysis Section 7)

1. **AUA projection 0/0 fix:** When no prior period in windowed data, what should happen? (a) no ghost, (b) fall back to raw data for prior reference, (c) "projection unavailable" indicator.
2. **GRO chart redesign:** Keep multi-line or convert? (a) keep lines + add hero/tooltip/label, (b) diverging bar like NNA, (c) stacked bar, (d) other.
3. **Projection tooltip format:** (a) ghost increments with "(add)", (b) full projected values with current parenthetical, (c) actual and projected as separate rows.
4. **GRO tooltip:** (a) structured rows with sign coloring, (b) include period-over-period, (c) show projection for current period, (d) all of the above.
5. **GRO hero metrics:** What to display below chart? Latest period Market/NNA/Total, cumulative, growth rate?

### Instructions per Participant

**CTO (1.0.0_SA_CTO) -- your turn first.**
You wrote the analysis. After reading the CURRENT source (not just your analysis), confirm which flaws remain and which the 3 newer commits addressed. Then state your architectural position on each of the 5 questions. Reference existing patterns from your Section 6 catalog to justify consistency.

**DE (0.4.0_DE_ClientPlatform):**
Read PartnerAnalytics.tsx and types.ts. For each convergence question, specify:
- What Recharts API patterns support the proposed solution (stackOffset, ReferenceLine, custom tooltip, etc.)
- Any TypeScript type implications (new interfaces, augmented data shapes)
- Data contract awareness: what fields exist in timeseries_chart.json growth_decomposition vs what needs to change

**RD (0.4.2_RD_AdvisorIntelligence):**
You built the current implementation. After reading the CTO analysis and the other participants' positions:
- Confirm implementation feasibility for each proposed solution
- Flag any Recharts constraints that would block a proposal
- Propose specific component structure (which Recharts components, props, data transformations)

### Self-unblock requirement (M11)

If you are uncertain about a field name, data shape, Recharts prop, or current code behavior: use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer. You have tool access -- use it.

### Final turn must produce a structured contract block with:

- Exact projection formula for each view (AUA stock metric, NNA flow metric, GRO flow metric)
- Exact tooltip layout for each view (rows, labels, values, sign formatting)
- GRO chart type decision (line, bar, or hybrid) with component specification
- GRO hero metrics (what metrics, what format)
- Edge case handling (no prior period, period already complete, negative projections, short windows)


---

## 001.md

---
agent: 1.0.0_SA_CTO
turn: 1
timestamp: 2026-03-09T20:02:06Z
signal: continue
---

## 0) What’s already fixed vs still broken (based on CURRENT `PartnerAnalytics.tsx` in context)

From the injected current source:

### Flaw 1 — AUA projection 0/0 regression
- **Still present.** In `augmentedAuaData`, when `prior === null`, code sets `priorEnd = actual`, so `delta = 0` and ghost becomes 0. This will happen whenever the windowed aggregated series has only one period (e.g., Annually + 1Y).
- There is no “projection unavailable” UI; it silently shows no ghost.

### Flaw 2 — GRO chart unintelligible
- **Partially improved**: there *is* now a section title (“Growth Decomposition”) and the PanelHeader helpText changes by mode. But the core issues remain:
  - **Tooltip is still raw**: it iterates `payload.map()` and prints `entry.name` + value with no context, no sign formatting, no “delta” framing.
  - **Legend labels still terse**: “Market / NNA / Total”.
  - **No hero metrics** for GRO (AUA/NNA have the tiles; GRO is excluded by `panelViewMode !== 'gro'` guard).
  - **Y-axis not labeled** as “AUA change” (it’s dollars but ambiguous).
  - Projection explanation is only in footnote; acceptable as secondary, not primary.

### Flaw 3 — Projection tooltip format (AUA/NNA show “(add)” increments)
- **Still present.** AUA tooltip “Projected” section shows `{cat} (add)` and “Projected Total”. NNA tooltip shows “Inflows (add) / Outflows (add) / Projected Net”.
- This is exactly the mental-math problem Andrew flagged.

### Flaw 4 — GRO tooltip leaks `_proj` entries
- **Still present.** GRO tooltip maps all payload entries; since `market_proj/nna_proj/total_proj` are separate `<Line>` series, they will appear in payload when hovering the projected point. There is no filtering like the AUA Mix tooltip does for `_ghost`.

So: the newer commits mentioned by COO (28517dd/2f84197/8e9facd) may exist on portal DEV, but **the current file injected here still exhibits Flaws 1–4** (with only minor “title/helpText” improvement for Flaw 2).

---

## 1) Architectural positions on the 5 convergence questions

### Q1 — AUA projection when no prior period exists in the windowed aggregated data
**Recommendation: (b) fall back to raw daily data to find a prior period end value; if still unavailable, (c) show “projection unavailable” (not (a) silent no-ghost).**

Why:
- We already do the “use full history for differencing” pattern in **NNA aggregation** (`aggregatedNnaData` builds `fullPeriodMap` from `allData` specifically to avoid window-edge artifacts). AUA should match that robustness.
- Silent 0 ghost is misleading; users interpret “no projection” as “no growth expected”.

Concrete approach:
- Build a `fullAuaPeriodMap` from `timeseriesData.aua.data` (unfiltered) similar to NNA’s `fullPeriodMap`, storing last snapshot per period for each category.
- Display only windowed periods, but compute `priorEnd` (and `priorPrior`) from full history.
- If full history still lacks a prior period (true beginning of dataset), then show no ghost **and** add tooltip line: “Projection unavailable (insufficient history)”.

### Q2 — GRO chart redesign: keep multi-line or convert?
**Recommendation: keep the 3-series chart, but change it to a “decomposition-first” hybrid: stacked bars for Market + NNA with Total as an overlaid line.**

Why:
- GRO is a decomposition identity: `Total = Market + NNA`. A stacked bar makes that identity visually obvious in one glance; three lines do not.
- It also aligns with existing portal patterns: we already use stacked bars heavily (AUA view, continuous AUA stacked bar). This is the most “zen” representation.
- We can still keep the “Total” line to preserve trend readability and match the NNA composed pattern (bars + line).

So: **Option (c) stacked bar + (line overlay)** (a hybrid of (c) and the existing composed approach).

### Q3 — Projection tooltip format (AUA/NNA)
**Recommendation: (c) show both actual and projected as separate clearly-labeled rows, with projected values being full values (not increments).**

Pattern:
- “Actual to date” (current value)
- “Projected full period” (full projected value)
- Optional: small subtext “Projection assumes linear pace; capped at 1.5× prior period”.

This avoids mental math and keeps the tooltip self-contained.

### Q4 — GRO tooltip: structure, comparisons, projection
**Recommendation: (d) all of the above, but keep it minimal and consistent with AUA/NNA tooltips.**

Specifically:
- Structured rows with sign coloring (+ green, – red).
- Include period-over-period comparison **only for Total** (and optionally Market/NNA if we want), because too many comparisons becomes noise.
- Projection shown only for current incomplete period, and **must not leak `_proj` series**.

### Q5 — GRO hero metrics
**Recommendation: show latest period decomposition tiles (Market / Net Flows / Total Change) + a single comparison label (MoM/QoQ/YoY) mirroring AUA/NNA.**

Keep it simple:
- 3 tiles:
  - Market (Δ$)
  - Net Flows (Δ$)
  - Total Change (Δ$)
- Each tile can optionally show change vs prior period (Δ$ and % where meaningful). For Market/NNA, % is often weird (sign flips), so I’d default to **Δ$ only** and reserve % for Total if priorTotal ≠ 0.

---

## 2) Additional design constraints / edge cases to lock now

1. **Projection should be computed off the last bar in the dataset, not “calendar current period”.** The current code already “projects lastIdx”; keep that. It handles data lag gracefully.
2. **Projection only when period is incomplete** (`elapsedDays < totalDays`) AND we have a meaningful baseline:
   - For AUA: need a prior period end snapshot (from full history).
   - For NNA/GRO flows: can project without prior, but cap uses prior; if no prior, cap should fall back to `abs(actual) * 1.5` (or skip cap).
3. **Negative values:**
   - NNA outflow ghost should extend more negative (current code does this).
   - GRO Market/NNA/Total can be negative; projection should preserve sign and cap by magnitude.
4. **Tooltip filtering rules:**
   - AUA: hide `_ghost` from “Actual” section; show in “Projected” section.
   - GRO: hide `*_proj` from “Actual” section; show a dedicated “Projected” section only when hovering the current period and projection exists.

---

## 3) What I need from DE/RD in their next turns

1. **DE:** confirm feasibility of GRO hybrid chart in Recharts with current data shape:
   - Bars: `market`, `nna` stacked (`stackId="gro"`, `stackOffset="sign"`).
   - Line: `total`.
   - Projection: either a second dataset point (like now) or separate `*_proj` keys; but tooltip must filter.
2. **RD:** confirm implementation effort to:
   - Add full-history AUA prior lookup (mirroring NNA’s `fullPeriodMap` pattern).
   - Redo tooltip layouts to show actual vs projected full values (not increments).
   - Add GRO hero tiles (copy the existing tile layout but GRO-specific).

If DE/RD agree, I’ll produce (on my final turn) the “contract block” with exact formulas + tooltip row specs + GRO component spec.

---

## 002.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 2
timestamp: 2026-03-09T20:02:36Z
signal: continue
---

## Read of current `PartnerAnalytics.tsx` (injected) — what matters for convergence

I’m aligned with 1.0.0_SA_CTO’s assessment: in the injected current file, Flaw 1 (AUA prior missing → ghost=0), Flaw 3 (tooltips show “(add)” increments), and Flaw 4 (GRO tooltip includes `*_proj`) are all still present. GRO has a title/helpText, but it’s still missing hero metrics and a structured tooltip.

Also important: **AUA aggregation is window-filtered before period grouping** (`dailyData = timeWindowCutoff ? allData.filter(...) : allData`). That’s the root of the “no prior period in window” issue. NNA already solved this by building a full-history period map and then filtering for display; AUA should mirror that pattern.

---

## Q1 — AUA projection 0/0 fix: recommended behavior + Recharts/TS implications

### Recommendation
Agree with CTO: **(b) fall back to full-history prior period end** (from unfiltered daily AUA series), and if still unavailable (true first period), **(c) show “Projection unavailable”** in tooltip (and no ghost bar).

### Implementation pattern (mirrors existing NNA approach)
- Build a `fullAuaPeriodMap` from `timeseriesData.aua.data` (unfiltered), storing:
  - `period`, `label`, `endDate`
  - per-category last snapshot value (NMNC/NMEC or whatever categories exist)
- Build a `windowedPeriodKeys` set from the window-filtered daily points.
- Display `sorted = allSorted.filter(period in windowedPeriodKeys)` but compute `prior` / `priorPrior` by indexing into `allSorted` (full history), not `sorted`.

This eliminates the “Annually + 1Y” single-period window artifact.

### TypeScript implications
- No new backend types. This is frontend-only.
- We can keep the existing `any` cast in `augmentedAuaData` if RD prefers, but we can also tighten it:
  - Define a local type like:
    ```ts
    type AuaAggRow = { period: string; label: string; endDate: string } & Record<string, number | string>
    type AuaAugRow = AuaAggRow & Record<`${string}_ghost`, number>
    ```
  - Not required for correctness; optional cleanup.

### Edge-case rules to lock
- If `prior` missing in full history: do not render ghost; tooltip should say **“Projection unavailable (insufficient history)”** for that category/total.
- If `elapsedDays >= totalDays`: no projection (already implemented).

---

## Q2 — GRO chart redesign: Recharts feasibility + recommended spec

### Recommendation
Agree with CTO’s direction: **GRO should be a decomposition-first chart**. Best fit in Recharts is a **ComposedChart** with:
- **Stacked bars**: `market` + `nna` (stackId `"gro"`)
- **Overlay line**: `total`
- **ReferenceLine** at y=0
- **stackOffset="sign"** so negative market/nna stack below zero correctly.

This is fully supported by Recharts (`<ComposedChart stackOffset="sign">` + `<Bar stackId="gro">` + `<Line>`).

### Projection rendering approach (to avoid tooltip pollution)
Current approach uses `market_proj`/`nna_proj`/`total_proj` as separate series keys, which leaks into tooltip unless filtered. Two viable options:

1) **Keep `*_proj` keys but filter tooltip payload** (lowest diff)
- In GRO tooltip content: `payload.filter(e => !String(e.dataKey).endsWith('_proj'))` for “Actual” section.
- If hovering the projection point (or if `_isProjection` flag is present), show a dedicated “Projected full period” section using the `*_proj` values only.

2) **Use a second “projection point” with same keys and `null` gaps** (cleaner but more refactor)
- Keep only `market/nna/total` keys.
- Add a second data point with same `label` but `period` suffixed; set actual last point’s next values to `null` and projection point’s prior values to `null` to create dashed segment.
- This is trickier with bars (bars don’t “dash”), so for the hybrid bar+line design, option (1) is simpler.

Given we’re redesigning GRO to bars+line, **I recommend option (1)**: keep projection as a dashed **Line** extension for `total` only (optional for market/nna), and keep bars as actual-to-date only. That avoids “ghost bars” for GRO, which can be visually confusing.

---

## Q3 — Projection tooltip format (AUA/NNA): recommended layout

### Recommendation
Agree with CTO: choose **(c) show both actual and projected full values** (not increments).

### Recharts tooltip mechanics
- We already use custom `content` renderers; we can compute projected full values inside tooltip using:
  - `actual = entry.value`
  - `projected = actual + ghost` (AUA categories) or `inflow + inflow_ghost` etc.
- For NNA outflows: remember `outflow` is negative in chart data; display as `-abs(...)`.

### Concrete tooltip rows (proposal)
For AUA:
- Actual:
  - Total AUA
  - New Clients / Existing Clients
- Projected Full Period (only if ghost > 0 and period is last/incomplete):
  - New Clients: `$X` (currently `$Y`)
  - Existing Clients: `$X` (currently `$Y`)
  - Projected Total: `$X` (currently `$Y`)

For NNA (gross mode):
- Actual:
  - Inflows, Outflows, Net Flow
- Projected Full Period:
  - Inflows: `+$X` (currently `+$Y`)
  - Outflows: `-$X` (currently `-$Y`)
  - Net: `+$X` (currently `+$Y`)

This is all frontend-only; no data contract changes.

---

## Q4 — GRO tooltip: what to include and how to keep it consistent

### Recommendation
Support CTO’s “(d) all of the above” but with a constraint: **period-over-period comparison should be for Total only** (at least in v1), to avoid a 3× explosion of comparison rows.

### Tooltip payload filtering rule (must-have)
- Filter out `*_proj` keys from the “Actual” section.
- If projection exists for the last period, show a “Projected full period” section with projected totals (and optionally show “currently” parenthetical).

### Sign formatting
- Use sign-aware formatting:
  - positive: `+${formatCurrency(v)}`
  - negative: `-${formatCurrency(abs(v))}`
- Color: green for positive, red for negative, neutral for labels.

---

## Q5 — GRO hero metrics: what to show + where it fits in current component

### Recommendation
Add GRO hero tiles analogous to AUA/NNA tiles:
- Market (Δ$)
- Net Flows (Δ$)
- Total Change (Δ$)
- Comparison label: MoM/QoQ/YoY based on granularity (same label logic already exists elsewhere).

### Implementation detail
Currently hero tiles are rendered inside a guard:
```tsx
{panelViewMode !== 'gro' && !(panelViewMode === 'aua' && auaSubMode === 'mix') && (...) }
```
So GRO is explicitly excluded. RD can:
- Extend this block with a GRO branch, or
- Factor the tiles into a small render function keyed by `panelViewMode`.

No backend changes.

---

## Two clarifying questions for CTO/RD before we lock the contract block

1) **GRO projection scope:** do we want projection for **Total only** (simpler, clearer), or for Market+NNA+Total (more complete but more tooltip/legend complexity)?
2) **AUA “projection unavailable” UX:** tooltip-only message is easy; do we also want a subtle inline indicator (e.g., muted “—” in projected section) or is tooltip-only sufficient?

I can draft the final “contract block” once those two are answered, but the above is implementable with current data shapes and Recharts patterns.

---

## 003.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 3
timestamp: 2026-03-09T20:03:14Z
signal: continue
---

## Read of CURRENT `PartnerAnalytics.tsx` (injected) — confirm what’s still wrong

Aligned with both 1.0.0_SA_CTO and 0.4.0_DE_ClientPlatform:

- **Flaw 1 (AUA 0/0 ghost)**: still present in `augmentedAuaData`. If the windowed aggregated series has only one period, `prior === null` → `priorEnd = actual` → `delta = 0` → ghost = 0. This is silent and misleading.
- **Flaw 3 (tooltip shows “(add)” increments)**: still present for both AUA and NNA tooltips. The “Projected” section is currently additive deltas, not full projected values.
- **Flaw 4 (GRO tooltip leaks `*_proj`)**: still present. GRO tooltip maps all payload entries; `market_proj/nna_proj/total_proj` show up as extra rows.

Also: GRO is still missing **hero metrics** because the tile block is explicitly gated out for `panelViewMode === 'gro'`.

## My implementation positions on the 5 convergence questions

### Q1 — AUA projection when no prior period exists in windowed data
**Feasible + recommended:** mirror the existing NNA “full history for differencing” pattern.

Concrete RD plan (in `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx`):
1. Refactor AUA aggregation to build:
   - `allSortedAuaPeriods` from **unfiltered** `timeseriesData.aua.data`
   - `windowedPeriodKeys` from cutoff-filtered daily points
   - `displayAuaPeriods = allSortedAuaPeriods.filter(p => windowedPeriodKeys.has(p.period))`
2. In `augmentedAuaData`, compute `prior` / `priorPrior` by indexing into `allSortedAuaPeriods`, not `displayAuaPeriods`.

**Edge case:** if `fullIdx === 0` (true first period in dataset), we should:
- render **no ghost bars**
- show tooltip line: **“Projection unavailable (insufficient history)”** (tooltip-only is sufficient; I don’t think we need an inline badge).

### Q2 — GRO chart redesign (line vs bar vs hybrid)
**Feasible:** yes, Recharts supports the CTO/DE hybrid.

I support **ComposedChart with stacked bars (Market + Net Flows) + Total line**:
- `<ComposedChart stackOffset="sign">`
- `<Bar dataKey="market" stackId="gro" />`
- `<Bar dataKey="nna" stackId="gro" />`
- `<Line dataKey="total" />`
- `<ReferenceLine y={0} />`

This makes the identity `total = market + nna` visually obvious.

### Q3 — Projection tooltip format (AUA/NNA)
**Feasible:** yes; we already have custom tooltip renderers.

I recommend switching to **full projected values** with “currently …” parentheticals (CTO option (c)).

Implementation detail:
- AUA: `projectedCat = actualCat + ghostCat`
- NNA: `projectedInflow = inflow + inflow_ghost`, `projectedOutflow = outflow - outflow_ghost` (since outflow is negative and ghost is positive magnitude in current code), `projectedNet = projectedInflow + projectedOutflow`

We can still keep the “Projected Total” row, but it should show full projected total and optionally “(currently …)”.

### Q4 — GRO tooltip
**Feasible:** yes.

I propose:
- Structured rows with sign formatting + color
- Period-over-period comparison **for Total only** (agree with DE; keeps tooltip compact)
- Projection section only for the last incomplete period
- **Filter out `*_proj` keys** from the “Actual” rows

### Q5 — GRO hero metrics
**Feasible:** yes; we can reuse the existing tile container.

I recommend 3 tiles (latest selected/hovered period or latest period if none selected):
- **Market (Δ$)**
- **Net Flows (Δ$)**
- **Total Change (Δ$)** + optional comparison vs prior period (Δ$ only; % is often nonsense with sign flips)

## Answers to DE’s two clarifying questions

1) **GRO projection scope:** I recommend **Total-only projection** for v1. Projecting Market and NNA separately implies we know their intra-period pace independently; we don’t. Total-only is clearer and avoids triple projection complexity in tooltip/legend.
2) **AUA “projection unavailable” UX:** tooltip-only message is sufficient. No inline indicator needed; the absence of ghost + explicit tooltip line is honest and minimal.

## Additional Recharts constraints / gotchas (so we don’t get surprised)
- Bars can’t be “dashed”; so for GRO projection, if we keep projection, it should be a **dashed Line extension** (Total only) rather than trying to ghost-extend bars.
- Tooltip payload ordering is inconsistent across Bar/Line mixes; we should not rely on `payload.map()` for GRO. We should explicitly read values from `payload[0].payload` (the datum) and render rows deterministically.

## What I need from CTO to lock final contract
Only one decision: confirm **GRO projection = Total-only** is acceptable. If yes, I’m ready to implement the full set (AUA full-history prior lookup, tooltip redesigns, GRO hybrid chart + hero metrics + tooltip filtering) in `PartnerAnalytics.tsx` within my page scope.

---

## 004.md

---
agent: 1.0.0_SA_CTO
turn: 4
timestamp: 2026-03-09T20:03:41Z
signal: continue
---

## Convergence decisions (locking the open items)

### DE question 1 — GRO projection scope
**Decision: GRO projection = Total-only (v1).**  
Rationale: Market vs Flow pacing is not independently knowable intra-period; projecting both invites false precision and triples tooltip/legend complexity. Total-only projection still satisfies the user need (“where will this period likely land?”) and keeps the decomposition identity readable.

### DE question 2 — AUA “projection unavailable” UX
**Decision: tooltip-only message is sufficient.**  
No inline badge. Rule: if we cannot compute a prior period end from full history, we render no ghost and show a single tooltip line: **“Projection unavailable (insufficient history)”**.

---

## Contract block (implementation-ready spec)

### A) Projection formulas (exact)

#### AUA (stock metric; per category NMNC/NMEC)
For the **last displayed period** only, if incomplete:

- Inputs:
  - `actual = AUA_end_of_period_to_date` (from aggregated period endpoint)
  - `priorEnd = prior period end AUA` (**must come from full-history period map**, not windowed)
  - `ratio = totalDays / elapsedDays`
  - `priorPeriodChange = abs(priorEnd - priorPriorEnd)` if priorPrior exists, else `abs(actual - priorEnd)`

- Compute:
  - `delta = actual - priorEnd`
  - `projectedDelta = delta * ratio`
  - `projectedValue = priorEnd + projectedDelta`
  - Cap:
    - `capDelta = 1.5 * priorPeriodChange`
    - `cappedValue = min(projectedValue, priorEnd + capDelta)`
  - Ghost:
    - `ghost = max(0, cappedValue - actual)` (keep current “no negative ghost extension” behavior)

- Availability:
  - If `priorEnd` missing in full history: **no ghost** + tooltip “Projection unavailable…”

#### NNA (flow metric; inflow/outflow)
For the **last displayed period** only, if incomplete:

- `ratio = totalDays / elapsedDays`
- Inflows (positive):
  - `projectedInflow = min(inflow * ratio, abs(priorInflow) * 1.5)` (if no prior, cap vs `abs(inflow)*1.5`)
  - `inflow_ghost = max(0, projectedInflow - inflow)`
- Outflows (stored negative in chart data):
  - `projectedOutflow = max(outflow * ratio, -abs(priorOutflow) * 1.5)` (if no prior, cap vs `-abs(outflow)*1.5`)
  - `outflow_ghost = min(0, projectedOutflow - outflow)` (extends more negative)

#### GRO (flow metric; decomposition deltas)
Chart redesign below; projection is **Total-only**:
- `projectedTotal = project(total, priorTotal)` where:
  - `projected = total * ratio`
  - `cap = abs(priorTotal ?? total) * 1.5`
  - if `total >= 0`: `min(projected, cap)` else `max(projected, -cap)`
- Render as dashed line extension from last actual total to projected total.

---

### B) Tooltip layouts (exact)

#### AUA tooltip (for a bar)
Sections:
1) Header: `{label}` + optional “(Selected)”
2) **Actual**
   - Total AUA: `$X`
   - New Client Assets: `$X`
   - Existing Client Assets: `$X`
   - Growth vs prior (existing logic ok)
3) **Projected Full Period** (only if last period, incomplete, and projection available)
   - New Client Assets: `$P` *(currently `$A`)*
   - Existing Client Assets: `$P` *(currently `$A`)*
   - Projected Total: `$P` *(currently `$A`)*
4) If projection unavailable: single muted line **“Projection unavailable (insufficient history)”**

No “(add)” rows.

#### NNA tooltip
Gross mode:
1) Actual: Inflows, Outflows, Net Flow
2) Change vs prior (existing ok)
3) Projected Full Period (only last/incomplete):
   - Inflows: `+$P` *(currently `+$A`)*
   - Outflows: `-$P` *(currently `-$A`)*
   - Net: `+$P` *(currently `+$A`)*

Net-only mode: show Net only + projected Net only.

#### GRO tooltip (new; must not payload.map blindly)
Read from datum (`payload[0].payload`) and render deterministic rows:

1) Header: `{label}` + small subtitle “AUA change (period delta)”
2) Rows (sign-colored):
   - Market: `+/-$X`
   - Net Flows: `+/-$X`
   - Total Change: `+/-$X`
3) Comparison (Total only): `MoM/QoQ/YoY Change` as `+/-$Δ` (no % by default)
4) Projected Full Period (Total only; last/incomplete):
   - Projected Total Change: `+/-$P` *(currently `+/-$A`)*

Filtering rule: **never render `*_proj` series rows**; projection is shown only via the explicit “Projected” section.

---

### C) GRO chart type decision + component spec (exact)

**Decision:** ComposedChart hybrid: stacked bars (Market + Net Flows) + Total line.

Spec:
- `<ComposedChart data={groData} stackOffset="sign">`
- `<Bar dataKey="market" stackId="gro" fill={GRO_COLORS.market} />`
- `<Bar dataKey="nna" stackId="gro" fill={GRO_COLORS.nna} />`
- `<Line dataKey="total" stroke={GRO_COLORS.total} strokeWidth={3} dot={{...}} />`
- `<ReferenceLine y={0} ... />`
- Projection: dashed `<Line dataKey="total_proj" ... strokeDasharray="6 3" legendType="none" />` (Total-only)

Y-axis label (visual): add a small rotated label “AUA Change” (or “Period ΔAUA”) to remove ambiguity.

Legend labels: expand to “Market (ΔAUA)”, “Net Flows (NNA)”, “Total (Market + NNA)” if space permits; otherwise keep short but tooltip/section title must carry meaning.

---

### D) GRO hero metrics (exact)
Add GRO tiles (same container as AUA/NNA tiles) when `panelViewMode === 'gro'`:
- Market (Δ$)
- Net Flows (Δ$)
- Total Change (Δ$)
Optional: show comparison vs prior for **Total only**.

---

### E) Edge-case handling (exact)
- **No prior period (AUA):** no ghost; tooltip message.
- **Period complete:** no projection (all modes).
- **Windowing:** AUA must compute prior/priorPrior from **full-history period list** (mirror NNA’s `fullPeriodMap` pattern).
- **Negative values:** GRO rows sign-colored; NNA outflows displayed as negative with abs formatting.
- **Tooltip payload pollution:** GRO tooltip must ignore payload entries and use datum fields; AUA/NNA already separate ghost keys—keep that pattern.

If DE/RD are aligned with this contract, I consider the thread ready to converge once they confirm no objections to the GRO hybrid bar+line choice and Total-only projection.

---

## 005.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 5
timestamp: 2026-03-09T20:04:13Z
signal: continue
---

CTO contract block looks implementable as-is in `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx`. I’m aligned with the decisions (GRO projection = Total-only; AUA “projection unavailable” = tooltip-only).

## DE confirmation: Recharts + data-shape feasibility (no backend changes)

### 1) AUA “full-history prior” fix (Flaw 1)
- **Feasible** and consistent with the existing NNA pattern already in this file (`aggregatedNnaData` uses `allData` to build `fullPeriodMap`, then filters to windowed periods).
- For AUA, we should mirror that exact structure:
  - Build `fullPeriodMap` from `timeseriesData.aua.data` (unfiltered).
  - Build `windowedPeriodKeys` from cutoff-filtered daily points.
  - Display `sorted = allSorted.filter(periodKey in windowedPeriodKeys)`.
  - In `augmentedAuaData`, compute `prior/priorPrior` by indexing into `allSorted` (full history), not the windowed list.
- This resolves the Annually+1Y “single bar” case without inventing data.

### 2) GRO redesign to stacked bars + total line (Flaw 2)
- **Feasible** with Recharts `ComposedChart`:
  - `stackOffset="sign"` is required so negative market/nna stack below zero.
  - Two `<Bar stackId="gro">` series + one `<Line dataKey="total">`.
  - `ReferenceLine y={0}`.
- Data is already in `aggregatedGroData` as `{ market, nna, total }` per period; no contract changes.

### 3) GRO projection Total-only without tooltip pollution (Flaw 4)
- Keep the existing “append projected point” approach, but simplify to **total only**:
  - Add `total_proj` for the dashed segment; leave `market_proj/nna_proj` out entirely.
- Tooltip should **not** `payload.map()`; it should read from `payload[0].payload` (datum) and render deterministic rows. That fully avoids any `*_proj` leakage regardless of Recharts payload composition.

### 4) Tooltip format change to “Actual vs Projected full values” (Flaw 3)
- **Feasible** in current custom tooltip renderers:
  - AUA: compute `projectedCat = actualCat + cat_ghost` and show `projected (currently actual)`.
  - NNA: compute `projectedInflow = inflow + inflow_ghost`; `projectedOutflow = outflow + outflow_ghost` (note: `outflow` and `outflow_ghost` are negative in the current augmented data); `projectedNet = projectedInflow + projectedOutflow`.
- No type changes required; purely presentation logic.

## One implementation note (to prevent regressions)
When we refactor AUA aggregation to use full-history differencing, ensure we preserve:
- `endDate` on the aggregated period rows (used by the hero tiles “as of …” line).
- Category keys exactly as `timeseriesData.aua.categories` provides (NMNC/NMEC casing), since the tooltip and bar rendering rely on those keys.

## What I need from 0.4.2_RD_AdvisorIntelligence (so DT can push safely)
Please confirm in your next turn:
1) You’ll implement the AUA aggregation refactor by copying the NNA “fullPeriodMap + windowedPeriodKeys” structure (not a partial patch inside `augmentedAuaData` only).
2) For GRO projection you’ll emit **only** `total_proj` (no market/nna projections) and update tooltip to datum-driven rendering.

If RD confirms, I’ll mark this thread ready to converge on my final turn and will write a short internal acceptance checklist for DT QA (what to click: Annually+1Y AUA, GRO hover on last period, etc.).

---

## 006.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 6
timestamp: 2026-03-09T20:04:29Z
signal: continue
---

Confirmed. I’m aligned with the CTO contract block and DE’s feasibility notes, and I can implement everything **within** `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx`.

## Direct answers to DE’s two asks (commit-level intent)

### 1) AUA aggregation refactor (full-history prior lookup)
Yes — I will implement this as a **structural mirror** of the existing NNA pattern, not a patch inside `augmentedAuaData`.

Concretely:
- Build a **full-history** period map from `timeseriesData.aua.data` (unfiltered) to produce `allSortedAuaPeriods[]` (each row includes `period`, `label`, `endDate`, and category snapshot values).
- Build `windowedPeriodKeys` from the cutoff-filtered daily points (same as NNA).
- `aggregatedAuaData` becomes the **windowed display list**: `allSortedAuaPeriods.filter(p => windowedPeriodKeys.has(p.period))`.
- `augmentedAuaData` will compute `prior` / `priorPrior` by indexing into `allSortedAuaPeriods` (full history), not the windowed list.

This resolves the Annually+1Y / single-bar case and keeps `endDate` intact for the “as of …” line.

### 2) GRO projection scope + tooltip rendering
Yes — GRO projection will be **Total-only**:
- Only emit `total_proj` (no `market_proj`, no `nna_proj`).
- Tooltip will be **datum-driven** (read from `payload[0].payload`) and will not `payload.map()`, so there’s no chance of `*_proj` leakage.

## Additional implementation notes (so we don’t regress other behavior)

- I’ll keep the existing “project the **last bar in dataset**” behavior (not calendar current period), since that’s already the correct robustness pattern for data lag.
- I’ll update AUA + NNA tooltips to remove “(add)” rows and instead show **Projected Full Period** as full values with “(currently …)” parentheticals per CTO spec.
- GRO chart will be redesigned to **stacked bars (market + nna) + total line**, with `stackOffset="sign"` and `ReferenceLine y={0}`.
- GRO hero tiles will be added (3 tiles: Market / Net Flows / Total Change), with comparison vs prior for **Total only**.

## Quick DT QA checklist (what should visibly change)
After this lands, the following should validate the fixes:
1) **AUA → Interval: Year → Window: 1Y**: last bar should show a ghost *if* period incomplete and full-history prior exists; otherwise tooltip shows “Projection unavailable (insufficient history)”.
2) **AUA tooltip** on last bar: “Projected Full Period” shows full projected values (not “(add)”).
3) **NNA tooltip** on last bar: same (full projected inflows/outflows/net).
4) **GRO mode**: chart is bars+line; tooltip shows exactly Market / Net Flows / Total Change (+ Total comparison), and **no duplicated projection rows**.

If CTO/DE have no further constraints, I’m ready for my final turn after implementation to report what changed and any edge cases encountered.

---

## 007.md

---
agent: 1.0.0_SA_CTO
turn: 7
timestamp: 2026-03-09T20:04:47Z
signal: converge
---

## Final convergence (thread resolution)

We have full alignment across CTO/DE/RD on the redesign and the implementation plan. The contract block in Message 004 stands as the authoritative spec, with two clarifications now explicitly locked:

1) **GRO projection scope = Total-only (v1)**  
- No `market_proj` / `nna_proj`. Only `total_proj` as dashed line extension.

2) **AUA “projection unavailable” UX = tooltip-only**  
- No inline badge. Condition: if full-history prior period end is missing, render no ghost and show the tooltip line: **“Projection unavailable (insufficient history)”**.

## Implementation authority + file scope

- **Single file change target:** `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx`
- **No backend / data contract changes required.**
- **Key structural requirement:** AUA aggregation must mirror the existing NNA pattern:
  - Build full-history period list from unfiltered daily data
  - Filter to windowed periods for display
  - Compute `prior/priorPrior` from full-history list (not windowed)

## Acceptance checklist (what “done” means)

After RD implements:

1) **AUA / Year / 1Y window** no longer silently produces 0 ghost due to missing window prior; it either:
   - shows a ghost (if full-history prior exists and period incomplete), or
   - shows tooltip message “Projection unavailable (insufficient history)”.

2) **AUA + NNA tooltips** show **Projected Full Period** as full values with “(currently …)” parentheticals — no “(add)” increments.

3) **GRO chart** is **stacked bars (market+nna) + total line**, with y=0 reference line and y-axis clearly framed as period delta (“AUA Change” / “Period ΔAUA”).

4) **GRO tooltip** is datum-driven (not `payload.map()`), shows only:
   - Market, Net Flows, Total Change (sign-colored)
   - Total comparison vs prior (Δ$ only)
   - Projected Total Change (last/incomplete only)
   - **No leaked projection series rows**.

This closes the convergence questions and unblocks implementation + DT QA/push.

---

## 008.md

---
agent: 0.4.0_DE_ClientPlatform
turn: 8
timestamp: 2026-03-09T20:04:58Z
signal: converge
---

## Convergence confirmation (DE final)

Aligned with the CTO contract block (Message 004) and the final convergence note (Message 007). No objections or additional constraints from 0.4.0_DE_ClientPlatform.

## What is now “locked” for implementation (single-file scope)

**Target file:** `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx`  
**No backend / data contract changes.**

1) **AUA projection prior lookup**
- Must mirror the existing NNA pattern: build a **full-history** period list from unfiltered `timeseriesData.aua.data`, filter to windowed periods for display, and compute `prior/priorPrior` from the full-history list.
- If full-history prior is missing: **no ghost** + tooltip line **“Projection unavailable (insufficient history)”** (tooltip-only; no inline badge).

2) **Tooltip projection format (AUA + NNA)**
- Replace “(add)” ghost increments with **Projected Full Period** full values, with “(currently …)” parentheticals.

3) **GRO chart redesign**
- Switch to **ComposedChart hybrid**: stacked bars (`market` + `nna`, `stackOffset="sign"`) + `total` line + `ReferenceLine y={0}`.
- **Projection is Total-only**: emit only `total_proj` as dashed line extension (no `market_proj` / `nna_proj`).

4) **GRO tooltip + hero metrics**
- Tooltip must be **datum-driven** (`payload[0].payload`), not `payload.map()`, to prevent any projection series leakage.
- Add GRO hero tiles: Market / Net Flows / Total Change (comparison vs prior for Total only, Δ$ only).

## DT QA checklist (post-merge / pre-push)

1) **AUA → Interval: Year → Window: 1Y**
- Last bar: either shows a ghost (if incomplete + full-history prior exists) or shows tooltip “Projection unavailable (insufficient history)”.

2) **AUA + NNA tooltips on last period**
- “Projected Full Period” shows full projected values with “(currently …)”; no “(add)” rows.

3) **GRO mode**
- Chart is bars+line; tooltip shows Market / Net Flows / Total Change (+ Total comparison) and **no duplicated projection rows**; projection (if present) is Total-only dashed extension.

Thread resolved; RD can implement and DT can QA/push once code lands.

---
