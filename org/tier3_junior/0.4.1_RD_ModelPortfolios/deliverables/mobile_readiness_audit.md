# Mobile Readiness Audit -- ModelPortfolios
**Agent:** 0.4.1_RD_ModelPortfolios
**Date:** 2026-04-07
**Task Order:** ADHC_DESIGN-023
**Viewport:** 375px-428px (iPhone SE / iPhone 14)

## Summary

ModelPortfolios is a desktop-first data visualization page with significant mobile blockers. The page uses a two-column flex layout for the Portfolio Analytics panel (donut chart + distribution chart), hardcoded chart dimensions, and inline SVG quartile charts -- none of which degrade gracefully below ~900px. The Growth tab's bar and area charts render acceptably via ResponsiveContainer but x-axis labels will collide. The Peers tab is the worst offender: 5-7 inline SVG charts in a horizontal row with no responsive stacking.

**Critical issues:** 8
**Warnings:** 11
**Touch target violations:** 5

---

## 1. Fixed-Width Audit

| # | File | Line | Value | Impact at 375px |
|---|------|------|-------|-----------------|
| 1 | ModelPortfolios.tsx | 539 | `max-w-[700px]` | Container clips to 375px; content inside is wider than viewport |
| 2 | ModelPortfolios.tsx | 677 | `width={380}` | ApexCharts donut wider than viewport (380 > 375). Overflows or clips. |
| 3 | ModelPortfolios.tsx | 789 | `max-w-[700px]` | Right partition same issue as #1 |
| 4 | PeersTab.tsx | 154 | `const width = 160` | SVG chart is 160px fixed. 5+ charts side by side = 800px+ total. Requires horizontal scroll. |
| 5 | ModelPortfolios.tsx | 678 | `height={380}` | Donut chart takes 380px vertical space even when clipped horizontally. Disproportionate on small screens. |

---

## 2. Hardcoded Height Audit

| # | File | Line | Value | Purpose | Issue |
|---|------|------|-------|---------|-------|
| 1 | ModelPortfolios.tsx | 541 | `h-[450px]` | Donut chart container | Wastes vertical real estate on mobile; no responsive reduction |
| 2 | ModelPortfolios.tsx | 810,845 | `h-[450px]` | Distribution chart containers | Same issue |
| 3 | ModelPortfolios.tsx | 1103 | `height={380}` | Period End Summary BarChart ResponsiveContainer | Acceptable but tall for mobile |
| 4 | ModelPortfolios.tsx | 1226 | `height={450}` | Daily AUA AreaChart ResponsiveContainer | 450px is ~60% of mobile viewport height |
| 5 | PeersTab.tsx | 500 | `height={700}` | QuartileChart component height prop | 700px is nearly 2x mobile viewport height per chart |

---

## 3. Non-Responsive Grid/Flex Audit

| # | File | Line | Layout | Behavior at 375px |
|---|------|------|--------|-------------------|
| 1 | **CRITICAL** ModelPortfolios.tsx | 524 | `<div className="flex overflow-hidden">` | Two-column layout: donut (left) + distribution (right). Both get ~187px. Charts don't fit. Needs `flex-col` at mobile breakpoint. |
| 2 | **CRITICAL** PeersTab.tsx | 494 | `<div className="flex justify-around items-end overflow-x-auto">` | 5-7 quartile charts in a row. overflow-x-auto saves from breakage but user must scroll a long distance. Should stack vertically or use tabs/carousel on mobile. |
| 3 | ModelPortfolios.tsx | 462 | `<div className="flex flex-wrap justify-center gap-x-8 gap-y-2 pt-4">` | Trend legend. flex-wrap is correct but gap-x-8 (32px) between items will consume most of 375px width. Items wrap to many rows. |
| 4 | PeersTab.tsx | 462 | `<div className="flex flex-wrap items-center gap-8 ...">` | Peers legend. gap-8 (32px) is generous for mobile. Legend alone could be 4-5 rows tall. |
| 5 | PeersTab.tsx | 473 | `<div className="flex items-center gap-6 ml-8">` | Quartile color legend nested row. ml-8 pushes content right; at 375px leaves ~280px for 4 legend items. |
| 6 | ModelPortfolios.tsx | 998 | `<div className="flex items-center justify-between mb-4 pr-[27px]">` | Period End Summary header row with View selector. justify-between at 375px may squish or overlap the title and dropdown. |
| 7 | ModelPortfolios.tsx | 1377 | `<div className="flex items-center gap-6">` | Benchmark tab controls: two toggle groups with gap-6. At 375px, both toggle groups plus labels won't fit in one row. |

---

## 4. Touch Target Audit

Minimum standard: 44px x 44px per WCAG / Apple HIG.

| # | File | Line | Element | Current Size | Violation |
|---|------|------|---------|--------------|-----------|
| 1 | ModelPortfolios.tsx | 697 | Donut legend buttons | `px-3 py-2` = ~36px height | Under 44px |
| 2 | ModelPortfolios.tsx | 968-987 | Value/Count toggle buttons | `px-3 py-1.5` = ~30px height | Under 44px |
| 3 | ModelPortfolios.tsx | 1387-1407 | Benchmark/Return type toggle buttons | `px-2 py-1` = ~26px height | Under 44px |
| 4 | PeersTab.tsx | 441-454 | Model selector buttons (UST/ST/INT/LTC/LTA) | `px-3 py-1.5` = ~30px height | Under 44px |
| 5 | ModelPortfolios.tsx | 1005-1016 | Period View select dropdown | `px-3 py-1.5` = ~30px height | Under 44px |

---

## 5. Chart Audit

### ModelPortfolios.tsx

| Chart | Container | Axis Labels at 375px | Legend | Verdict |
|-------|-----------|---------------------|--------|---------|
| **Donut** (ApexCharts, line 610) | Fixed 380x380. NO ResponsiveContainer. | N/A (donut) | Custom vertical legend adjacent to chart -- won't fit side-by-side at 375px | CRITICAL: needs ResponsiveContainer or responsive width prop |
| **Period End BarChart** (Recharts, line 1104) | ResponsiveContainer 100% x 380px. OK. | Custom tick renderer with -45deg rotation (line 1113-1130). At 375px, ticks will be dense and may overlap. | Shared `renderTrendLegend` with flex-wrap. OK. | WARNING: tick density at narrow width |
| **Daily AUA AreaChart** (Recharts, line 1226) | ResponsiveContainer 100% x 450px. OK. | Custom tick renderer with -45deg rotation (line 1258-1275). Weekly ticks every 5 data points -- at 375px, ticks will overlap heavily. | Same shared legend. OK. | WARNING: tick density |

### PeersTab.tsx

| Chart | Container | Issue |
|-------|-----------|-------|
| **QuartileChart** (inline SVG, line 263) | Fixed `width=160`, `height=700`. Not responsive. | CRITICAL: SVG dimensions are hardcoded constants (line 154). No responsive scaling. At 375px, only 2 charts fit side-by-side. With 5-7 charts, user scrolls ~800px horizontally. Each chart is 700px tall = massive scroll area. |

---

## 6. Table Audit

No tables in ModelPortfolios. AccountDistributionMetrics is a component imported from shared -- out of scope for this page audit.

---

## 7. Text/Content Audit

| # | File | Line | Content | Issue |
|---|------|------|---------|-------|
| 1 | ModelPortfolios.tsx | 767-770 | Non-Model AUA footnote | `text-[10px]` is below 12px minimum for mobile readability |
| 2 | ModelPortfolios.tsx | 823-835 | Distribution footnotes | `text-[10px]` same issue |
| 3 | ModelPortfolios.tsx | 857-870 | Total distribution footnote | `text-[10px]` same issue |
| 4 | ModelPortfolios.tsx | 1182-1186 | Account count footnote | `text-[10px]` same issue |
| 5 | PeersTab.tsx | 296 | Y-axis tick labels | `fontSize={9}` in SVG. Below minimum. |
| 6 | PeersTab.tsx | 351 | Period labels | `fontSize={14}` OK |
| 7 | PeersTab.tsx | 508-510 | Footnotes | `text-xs text-white/40` = 12px. Borderline but acceptable. |
| 8 | ModelPortfolios.tsx | 884-885 | CORS error message | Developer-facing text shown to users. Not a mobile issue per se, but flagged in debt scan as C6 Stale Error. |
| 9 | ModelPortfolios.tsx | 530,780 | Section headers "AUA by Model" / "Client Holdings" | `text-xs uppercase tracking-wider` = 12px. Readable but could be larger on mobile. |
| 10 | PeersTab.tsx | 436 | helpText on PanelHeader | Long tooltip text. On mobile, help tooltips may extend past viewport edge. |
| 11 | ModelPortfolios.tsx | 502 | PageHeader description | Inline `<strong>` tag. May wrap oddly at narrow widths. Minor. |

---

## 8. Design Flaws

| # | File | Line | Issue | Recommendation |
|---|------|------|-------|----------------|
| 1 | ModelPortfolios.tsx | 524 | Two-column layout has no responsive breakpoint. Desktop-only assumption baked into the flex structure. | Add `md:flex-row flex-col` to stack columns on mobile. |
| 2 | ModelPortfolios.tsx | 945 | Growth tab content is a raw div with manual border/padding, not using Panel primitives. Inconsistent with Benchmark and Peers tabs which use `<Panel variant="chart">`. | Migrate to Panel component for consistent overflow/padding behavior. |
| 3 | ModelPortfolios.tsx | 677-678 | ApexCharts donut uses hardcoded width/height instead of responsive sizing. Only chart on the page not using ResponsiveContainer or responsive props. | Use ApexCharts responsive option or calculate from container width. |
| 4 | PeersTab.tsx | 154 | SVG chart dimensions are compile-time constants, not derived from container. | Accept width as prop, compute from parent via ref or CSS. |
| 5 | ModelPortfolios.tsx | 528,778 | Section headers use `absolute top-4 left-6` positioning inside relative parent. Works but fragile -- if content above grows, header stays fixed. | Use flow layout instead of absolute positioning. |

---

## 9. Enhancement Opportunities

| # | Category | Description |
|---|----------|-------------|
| 1 | **Collapsible sections** | Growth tab has two charts (Period End Summary + Daily AUA). On mobile, collapse Daily AUA by default with an expand toggle. Reduces initial scroll depth by ~500px. |
| 2 | **Tab-based chart switching** | PeersTab: instead of 5-7 horizontal quartile charts, show one at a time with period selector tabs (1M / 3M / 6M / 1Y / SI). Each chart gets full width. |
| 3 | **Progressive donut** | On mobile, show donut chart full-width without adjacent legend. Move legend below chart. Already partially feasible by stacking the flex column. |
| 4 | **Swipeable chart carousel** | Growth tab bar/area charts could be swipeable on touch devices instead of vertical scroll. |
| 5 | **Responsive ApexCharts** | ApexCharts supports `responsive` option in config: `responsive: [{ breakpoint: 480, options: { chart: { width: 300 } } }]`. Use this for the donut. |
| 6 | **Touch-friendly toggles** | Convert py-1/py-1.5 toggle buttons to minimum 44px touch targets on mobile via `md:py-1.5 py-3` breakpoint pattern. |
| 7 | **Condensed legend** | On mobile, reduce legend gap from gap-8 (32px) to gap-3 (12px). Use `md:gap-8 gap-3`. |
| 8 | **Sticky tab navigation** | TabNavigation is already sticky. Verify z-index stacking doesn't conflict with chart tooltips on mobile (tooltip zIndex=40 vs sticky nav). |
