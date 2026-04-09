# FactorTilts Mobile Readiness Audit

**Agent:** 0.2.3_RD_FactorTilts
**Date:** 2026-04-07
**Task Order:** ADHC_DESIGN-020
**Target viewport:** 375px-428px (iPhone SE / iPhone 14)
**Files audited:** 7 (.tsx/.ts)

---

## Summary

FactorTilts is a desktop-first analytics page with dense chart/table layouts. At 375px, 14 critical issues and 11 warnings were found. The page is **not mobile-ready** -- the radar chart, bar chart, 6-column summary table, and multi-control PanelHeaders would all overflow or become unusable. The page requires a mobile-specific layout strategy (stacked panels, simplified controls, collapsed sections) before it can function at mobile widths.

---

## Critical Issues

| # | File:Line | Component | Issue | Impact at 375px |
|---|-----------|-----------|-------|------------------|
| C1 | FactorTiltOverviewPanel.tsx:323 | Overview grid | `grid-cols-1 xl:grid-cols-2` -- radar + summary stack vertically but each gets full 375px. Radar chart margins (100-140px L/R) leave ~95px for the actual chart. | Radar chart is unreadable |
| C2 | FactorTiltOverviewPanel.tsx:130-157 | Radar margins | Responsive margins only handle 1280/1536/1920px. No breakpoint below 1280px. Smallest margins: `{ top: 70, right: 100, bottom: 70, left: 100 }` -- leaves ~175px at 375px. | Radar needs ~60px margins at mobile |
| C3 | FactorTiltOverviewPanel.tsx:285 | PanelHeader actions | Two dropdowns (Portfolio + Lookback) in horizontal flex row. Each `<select>` is `px-3 py-1.5` with label. Approx 280px minimum. PanelHeader itself has title + help icon. | Controls overflow panel header |
| C4 | FactorTiltOverviewPanel.tsx:556 | Factor exposures grid | `grid-cols-2 gap-0` -- each column gets ~187px. Left column has description (truncated) + abbreviation (w-12) + tilt badge (w-16). Right column has gradient bar with w-20 labels on each side. | Content heavily compressed, gradient bar labels may collide |
| C5 | SummaryMetricsTable.tsx:119 | Regression table | 6 fixed-width columns at percentage widths (12.5% x4 + 25% x2). At 375px: 12.5% = 47px per metric column. Model+color dot, R2 value, Alpha with sign all need >47px. | Columns collapse, text overlaps |
| C6 | SummaryMetricsTable.tsx:118 | Table wrapper | `overflow-hidden` clips content instead of allowing horizontal scroll. No `overflow-x-auto` wrapper. | Data clipped and invisible |
| C7 | FactorTiltBarsTab.tsx:189-216 | PanelHeader actions | View mode toggle (Snapshot/Time Series buttons) + Lookback dropdown in horizontal flex. Toggle alone is ~200px. | Controls overflow panel header |
| C8 | FactorTiltBarsTab.tsx:241 | Bar chart | `h-[400px]` with 6 factor groups x 5 bars each. XAxis labels are full descriptions ("Equity vs Fixed Income"). At 375px, labels overlap severely. | Unreadable axis labels |
| C9 | FactorTiltTimeSeriesTab.tsx:300-332 | PanelHeader actions | Two dropdowns (Rolling + Display) side by side. ~250px minimum width. | Controls overflow panel header |
| C10 | FactorTiltTimeSeriesTab.tsx:383 | Line chart | `h-[350px]` is adequate but XAxis `minTickGap={50}` with date labels may crowd at 375px. | Axis labels may overlap |
| C11 | ModelTiltTimeSeriesView.tsx:241 | Model selection grid | `grid-cols-2 xl:grid-cols-3` -- no mobile breakpoint. At 375px each cell is ~187px. `p-2.5` padding + color dot + text fits but is tight. | Barely fits, touch targets small |
| C12 | ModelTiltTimeSeriesView.tsx:320-358 | Controls row | Two dropdown groups + right-aligned text in `flex justify-between flex-wrap`. Each dropdown group is ~180px. Will wrap but wrap order may be confusing. | Wraps unpredictably |
| C13 | ModelTiltTimeSeriesView.tsx:367 | Chart container | `h-[400px]` with `p-4` padding. Effective chart area is 343px x ~368px. Legend `height={36}` reduces further. | Chart cramped but functional |
| C14 | FactorTilts.tsx:243-248 | Loading/error containers | No explicit min-height or responsive height. Error text is single line centered. | Minor -- works but wastes space |

---

## Warnings

| # | File:Line | Component | Issue |
|---|-----------|-----------|-------|
| W1 | FactorTiltOverviewPanel.tsx:68,105 | TiltGradientBar labels | `text-[9px]` with `w-20` (80px) fixed width. Below 12px minimum readability. |
| W2 | FactorTiltOverviewPanel.tsx:327 | Zero line legend | `text-[10px]` label. Below 12px minimum. |
| W3 | FactorTiltOverviewPanel.tsx:516 | Tooltip footnote | `text-[10px]` inside tooltip. Below 12px minimum. |
| W4 | FactorTiltOverviewPanel.tsx:632 | Methodology footnote | `text-[10px]` text. Below 12px minimum. |
| W5 | FactorTiltOverviewPanel.tsx:462 | Radar custom labels | `fontSize: labelFontSize` (9-10px). Already hard to read on desktop; illegible at mobile. |
| W6 | FactorTiltBarsTab.tsx:256,262 | Bar chart axis ticks | `fontSize: 11` for both axes. |
| W7 | FactorTiltTimeSeriesTab.tsx:397,405 | Line chart axis ticks | `fontSize: 10` for both axes. |
| W8 | ModelTiltTimeSeriesView.tsx:381,389 | Line chart axis ticks | `fontSize: 10` for both axes. |
| W9 | ModelTiltTimeSeriesView.tsx:411 | Legend wrapper | `fontSize: '11px'`. |
| W10 | SummaryMetricsTable.tsx:132 | HelpCircle icons | `size={12}` with `cursor-help`. Touch target is 12px -- well below 44px minimum. |
| W11 | FactorTiltOverviewPanel.tsx:93 | TiltGradientBar marker | `w-2.5 h-2.5` (10px) dot. Not a touch target but very small visually. |

---

## Touch Target Violations

All clickable elements evaluated at 375px:

| File:Line | Element | Current Size | Min Required |
|-----------|---------|-------------|--------------|
| SummaryMetricsTable.tsx:132,146,158,170,184,198 | HelpCircle tooltip triggers | 12x12px | 44x44px |
| FactorTiltBarsTab.tsx:192-215 | Snapshot/Time Series toggle buttons | `px-3 py-1.5` (~36x28px) | 44x44px |
| FactorTiltOverviewPanel.tsx:289-299 | Portfolio `<select>` | `px-3 py-1.5` (~auto x 28px) | Height < 44px |
| FactorTiltOverviewPanel.tsx:305-315 | Lookback `<select>` | `px-3 py-1.5` (~auto x 28px) | Height < 44px |
| FactorTiltTimeSeriesTab.tsx:304-314 | Rolling `<select>` | `px-3 py-1.5` (~auto x 28px) | Height < 44px |
| FactorTiltTimeSeriesTab.tsx:320-330 | Display `<select>` | `px-3 py-1.5` (~auto x 28px) | Height < 44px |
| FactorTiltTimeSeriesTab.tsx:344-377 | Factor selection cards | `p-3` (~auto x ~48px) | PASS |
| ModelTiltTimeSeriesView.tsx:246-276 | Model selection buttons | `p-2.5` (~auto x ~36px) | Height < 44px |
| ModelTiltTimeSeriesView.tsx:291-313 | Factor selection buttons | `p-2.5` (~auto x ~36px) | Height < 44px |
| ModelTiltTimeSeriesView.tsx:328-338 | Regression `<select>` | `px-3 py-1.5` (~auto x 28px) | Height < 44px |
| ModelTiltTimeSeriesView.tsx:347-357 | Period `<select>` | `px-3 py-1.5` (~auto x 28px) | Height < 44px |
| SummaryMetricsTable.tsx:109-113 | Show All Models button | `px-3 py-1.5` (~auto x 28px) | Height < 44px |

---

## Chart Responsiveness

| Chart | File:Line | Container | ResponsiveContainer | Mobile Risk |
|-------|-----------|-----------|---------------------|-------------|
| Nivo Radar | FactorTiltOverviewPanel.tsx:331 | `h-[400px] xl:h-[480px]` | N/A (Nivo handles internally) | HIGH -- margins eat available space. Custom label layer positions are absolute, not responsive below 1280px |
| Recharts Bar | FactorTiltBarsTab.tsx:242-302 | `h-[400px]` | Yes, `width="100%" height="100%"` | HIGH -- 6 groups x 5 bars. XAxis uses full factor descriptions. Bars become 2-3px wide at 375px |
| Recharts Line (spreads) | FactorTiltTimeSeriesTab.tsx:385-444 | `h-[350px]` | Yes | MEDIUM -- line chart scales well, but legend and axis labels crowd |
| Recharts Line (model tilts) | ModelTiltTimeSeriesView.tsx:369-434 | `h-[400px]` | Yes | MEDIUM -- same as above. Legend `height={36}` is fixed |

---

## Table Responsiveness

| Table | File:Line | Columns | Width Strategy | Scroll Wrapper | Mobile Risk |
|-------|-----------|---------|----------------|----------------|-------------|
| SummaryMetricsTable | SummaryMetricsTable.tsx:119 | 6 | `table-fixed` with % widths | `overflow-hidden` (clips, no scroll) | CRITICAL -- needs `overflow-x-auto` and sticky first column |

---

## Design Flaws

| # | File:Line | Issue | Recommendation |
|---|-----------|-------|----------------|
| D1 | FactorTiltOverviewPanel.tsx:130-157 | Radar margin calculation uses `window.innerWidth` with `resize` listener instead of CSS breakpoints. This is a React anti-pattern (causes re-renders on resize, doesn't SSR). | Use CSS container queries or Tailwind breakpoint classes |
| D2 | FactorTiltOverviewPanel.tsx:407-474 | Radar custom labels layer computes absolute (x,y) positions using trigonometry and hardcoded per-label offsets. Fragile -- any new factor or label text change requires manual offset tuning. | Consider a legend-style list below the radar instead of embedded SVG labels |
| D3 | SummaryMetricsTable.tsx:51-61 | Column widths hardcoded as string percentages (`'12.5%'`, `'25%'`). Not responsive. | Use `minmax()` grid or remove `table-fixed` for auto-sizing |
| D4 | FactorTiltOverviewPanel.tsx:556-619 | Factor exposures section is a nested `grid-cols-2` with sub-grids (description + abbr + badge | gradient bar). Three levels of layout nesting for one row. | Flatten to a single flex row with mobile stack |
| D5 | ModelTiltTimeSeriesView.tsx:232 | Entire component is `space-y-6` (24px gaps) between controls and chart. At mobile, the controls section (model grid + factor list + dropdowns) takes 500+px before the chart is visible. | Collapse controls into an expandable drawer at mobile |

---

## Enhancement Opportunities

| # | Category | Description | Affected Components |
|---|----------|-------------|---------------------|
| E1 | Progressive disclosure | Collapse model/factor selection grids into a `<details>` or drawer at `<md` breakpoint. Show selected items as pills, expand on tap. | ModelTiltTimeSeriesView, FactorTiltTimeSeriesTab |
| E2 | Simplified mobile view | Replace the 6-column SummaryMetricsTable with stacked cards at `<md`. Each card shows one model row with key metrics vertically. | SummaryMetricsTable |
| E3 | Stacked controls | Move PanelHeader actions to a row below the title at `<md`. Use full-width dropdowns stacked vertically. | All PanelHeaders with actions |
| E4 | Chart height reduction | Reduce chart containers from `h-[400px]` to `h-[280px]` at `<md` to show more content above the fold. | All chart containers |
| E5 | Bar chart rotation | At `<md`, rotate the bar chart to horizontal bars (factor names on Y axis, values on X). Eliminates overlapping X labels. | FactorTiltBarsTab |
| E6 | Radar simplification | At `<md`, replace radar chart with a simple horizontal bar list (factor name + bar + value). Radar charts are inherently poor on small screens. | FactorTiltOverviewPanel |
| E7 | Swipeable tabs | Factor selection cards in FactorTiltTimeSeriesTab could become a horizontal scrollable strip at `<md`. | FactorTiltTimeSeriesTab |
| E8 | Sticky column | SummaryMetricsTable first column (Model) should be sticky with `position: sticky; left: 0` when wrapped in `overflow-x-auto`. | SummaryMetricsTable |
| E9 | Touch-friendly dropdowns | All `<select>` elements: increase padding to `py-2.5` at `<md` for 44px touch targets. | All select elements |

---

## Files Covered

| File | Status |
|------|--------|
| FactorTilts.tsx | Audited |
| constants.ts | Audited (no layout concerns) |
| types.ts | Audited (no layout concerns) |
| index.ts | Audited (barrel export only) |
| panels/FactorTiltOverviewPanel.tsx | Audited |
| panels/SummaryMetricsTable.tsx | Audited |
| tabs/FactorTiltBarsTab.tsx | Audited |
| tabs/FactorTiltTimeSeriesTab.tsx | Audited |
| components/ModelTiltTimeSeriesView.tsx | Audited |
