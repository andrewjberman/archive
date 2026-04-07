# Positioning Page — Mobile Readiness Audit

**Agent:** 0.2.1_RD_Positioning
**Date:** 2026-04-07
**Task Order:** ADHC_DESIGN-021
**Target viewport:** 375px-428px (iPhone SE / iPhone 14)

---

## Summary

The Positioning page is a desktop-first data-dense layout with 3 active files:
- `Positioning.tsx` (59 lines) — wrapper, no mobile issues
- `panels/PositioningSummary.tsx` (857 lines) — grid-based allocation bars + matrix table
- `tabs/HoldingsTab.tsx` (~1700 lines) — treemap chart + dense attribution table
- `shared/gridConfig.ts` (22 lines) — grid template constants

**Verdict:** Page is non-functional at 375px. The grid forces 300px + 5 columns, the table forces 635px+ minimum width, and the treemap is unusable below ~600px. Horizontal scroll is present but the experience is poor. Requires significant restructuring for mobile.

---

## Critical Issues (Broken at 375px)

### C1. Grid template forces minimum ~700px width
**File:** `shared/gridConfig.ts:8-9`
```
CATEGORY_WIDTH = '300px'
PORTFOLIO_GRID_TEMPLATE = `${CATEGORY_WIDTH} repeat(5, minmax(min-content, 1fr))`
```
The 300px fixed first column + 5 portfolio columns = minimum ~700px before content renders. At 375px the entire PositioningSummary requires horizontal scroll. No breakpoint variant exists.

### C2. Holdings table minimum width ~635px (Characteristics) / ~1240px (with AGG model breakdown)
**File:** `tabs/HoldingsTab.tsx:1096-1100`
```
col width: 105px + 165px + 55px + 250px + 60px = 635px (base 5 columns)
```
Plus 7 characteristics columns (375px) or 8 performance columns (605px). Total: 1010px-1240px. Far exceeds 375px. Table scrolls but sticky first column alone is 105px — that's 28% of viewport for just "Fixed Income" or "Equity" labels.

### C3. Treemap cells unreadable below ~600px
**File:** `tabs/HoldingsTab.tsx:398-406`
```
canShowFull = width >= 60 && height >= 55
canShowMedium = width >= 50 && height >= 40
canShowTicker = width >= 35 && height >= 25
```
At 375px viewport with `ResponsiveContainer width="100%"`, the treemap gets ~343px (375 - padding). With 30+ holdings, most cells fall below minimum thresholds. Only the largest 2-3 holdings show tickers.

### C4. Stacked allocation bars fixed at w-14 (56px) with absolute percentage labels
**File:** `panels/PositioningSummary.tsx:702, 736`
```
w-14 h-44 (56px x 176px bars)
```
**File:** `panels/PositioningSummary.tsx:761`
```
absolute left-[calc(100%+0.75rem)] ... text-xl font-semibold
```
The percentage labels are positioned absolutely to the right of each 56px bar. At 375px inside a 5-column grid, each column is ~15px wide (after the 300px first column is scrolled past). The bars + labels cannot fit.

---

## Warnings (Degraded at 375px)

### W1. Portfolio selector buttons may overflow PanelHeader
**File:** `tabs/HoldingsTab.tsx:992`
```
<div className="flex gap-1.5 bg-white/5 rounded-lg p-1 ...">
```
6 buttons (AGG, UST, ST, INT, LTC, LTA) at px-3 py-1.5 each. Estimated ~270px total. Combined with "Portfolio Composition" title, the PanelHeader actions overflow at 375px. No `flex-wrap` or mobile stacking.

### W2. View mode toggle in PositioningSummary header
**File:** `panels/PositioningSummary.tsx:614`
```
<div className="flex gap-1 bg-white/5 rounded-lg p-1 ...">
```
3 buttons (Portfolio, Benchmark, Relative) + "View:" label. ~220px. Combined with "Positioning Summary" title and help icon, will crowd or overflow the PanelHeader.

### W3. View mode toggle in Holdings table header
**File:** `tabs/HoldingsTab.tsx:1066-1079`
2 buttons (Characteristics, Performance). Smaller, but still competes with panel title for space.

### W4. Treemap height fixed at 400px
**File:** `tabs/HoldingsTab.tsx:1016, 1022`
```
h-[400px] / ResponsiveContainer width="100%" height={400}
```
400px is a reasonable desktop height but on a 667px-tall phone screen, this consumes 60% of the viewport for a chart that's barely readable anyway.

### W5. Font sizes in treemap content go below 12px
**File:** `tabs/HoldingsTab.tsx:404-406`
```
tickerSize = Math.max(10, Math.min(14, 14 * scaleFactor))
weightSize = Math.max(9, Math.min(12, 12 * scaleFactor))
returnSize = Math.max(9, Math.min(11, 11 * scaleFactor))
```
Minimum font sizes of 9px and 10px. Below the 12px (text-xs) floor recommended by the design system. At 375px, scaleFactor will drive most cells to minimums.

---

## Touch Targets (< 44px)

| Element | File:Line | Size | Issue |
|---------|-----------|------|-------|
| Portfolio selector buttons | HoldingsTab.tsx:999 | `px-3 py-1.5` (~36x28px) | Below 44px tap target |
| View mode buttons (Summary) | PositioningSummary.tsx:617 | `px-3 py-1` (~36x24px) | Below 44px tap target |
| View mode buttons (Table) | HoldingsTab.tsx:1071 | `px-2 py-1` (~32x24px) | Below 44px tap target |
| Section collapse toggles | PositioningSummary.tsx:570 | `py-2 px-4` (full-width x 32px) | Height below 44px |
| Expand/Collapse buttons | PositioningSummary.tsx:818, 845 | `px-4 py-2` (~120x32px) | Height below 44px |
| Legend color swatches | HoldingsTab.tsx:1042, 1046 | `w-3 h-3` (12x12px) | Non-interactive but appear clickable |

---

## Charts

### Treemap (HoldingsTab)
- **Container:** `ResponsiveContainer width="100%" height={400}` — width is responsive, height is fixed
- **Custom content renderer** uses `foreignObject` with HTML text. Font sizes scale down to 9px minimum.
- **Tooltip:** Recharts tooltip positions relative to cursor. At 375px, tooltips for right-edge cells will overflow viewport.
- **Recommendation:** Consider replacing treemap with a ranked bar chart or stacked list at narrow viewports. Treemaps are inherently desktop-scale visualizations.

### Stacked Bars (PositioningSummary)
- **Bars:** Fixed `w-14 h-44` (56x176px). No responsive scaling.
- **Labels:** Absolute-positioned `text-xl` percentage values to the right of each bar.
- **Recommendation:** Stack portfolios vertically on mobile. Use inline labels instead of absolute positioning.

---

## Tables

### Holdings Breakdown Table
- **Scroll wrapper:** `overflow-x-auto max-w-full scrollbar-none` (HoldingsTab.tsx:1092) -- present
- **Sticky column:** First column (`sticky left-0 z-10`) at 105px (HoldingsTab.tsx:1342) -- works but 105px is 28% of 375px viewport
- **Column count:** 12-20 columns depending on mode (5 base + 5-8 model breakdown + 7 characteristics or 8 performance)
- **Name truncation:** `truncate block` with title attribute (HoldingsTab.tsx:1375) -- present
- **Text size:** `text-xs` (12px) and `text-sm` (14px) -- acceptable
- **Column widths:** All hardcoded in pixels via `<col>` elements (no responsive variants)
- **Recommendation:** Consider card-based layout per holding on mobile. Show ticker, weight, and top 2-3 metrics. Expand for detail.

### Allocation Matrix Table (PositioningSummary)
- **Scroll wrapper:** `overflow-x-auto scrollbar-none` (PositioningSummary.tsx:650) -- present
- **Grid-based** (CSS Grid, not HTML table), using PORTFOLIO_GRID_TEMPLATE
- **No sticky column** for row labels
- **Recommendation:** Add sticky first column for metric labels. On mobile, consider transposing (portfolios as rows, metrics as columns).

---

## Text / Content

| Issue | File:Line | Detail |
|-------|-----------|--------|
| Portfolio names truncated | gridConfig.ts:17-22 | "Long-Term Conservative" (22 chars) and "Long-Term Aggressive" (20 chars) in narrow grid columns |
| ETF names long | HoldingsTab.tsx:1375 | Handled by `truncate block` + title attr |
| Section headers | PositioningSummary.tsx:580 | `whitespace-nowrap` — won't wrap, relies on scroll |
| Holding name fallbacks | HoldingsTab.tsx:88-150 | Some names are 50+ chars (e.g., "ProShares Ultra VIX Short-Term Futures ETF") |

---

## Design Flaws

### D1. Console.log statements in production code
**File:** `tabs/HoldingsTab.tsx:551, 566-573, 596, 632, 638, 644`
Multiple `console.log` and `console.warn` calls in useEffect callbacks and data builders. These should be removed or gated behind a debug flag.

### D2. Unused function kept with void suppress
**File:** `tabs/HoldingsTab.tsx:603-609`
```
const _getReturn = (ticker: string): number => { ... }
void _getReturn
```
Dead function with explicit void suppression. Should be removed.

### D3. Three separate useEffect calls for data fetching
**File:** `tabs/HoldingsTab.tsx:547, 562, 580`
Three independent useEffect hooks each making their own API call (positioning, attribution, AUM). Could be consolidated into a single useEffect or migrated to useQuery (as PositioningSummary already does for attribution).

### D4. Grid template uses fixed px for category column
**File:** `shared/gridConfig.ts:8`
`CATEGORY_WIDTH = '300px'` — a responsive value like `minmax(200px, 300px)` or `clamp(200px, 30vw, 300px)` would help at intermediate widths.

---

## Enhancement Opportunities

### E1. Progressive disclosure for holdings table
Show only ticker, weight, and asset class by default on mobile. Tap a row to expand full characteristics/performance metrics. Eliminates 12-column horizontal scroll.

### E2. Swipeable portfolio selector
Replace the 6 horizontal buttons with a swipeable pill selector or horizontal scroll container with snap points. More natural on touch.

### E3. Vertical portfolio stack for allocation bars
On screens < 768px, stack the 5 portfolios vertically instead of in a 5-column grid. Each portfolio shows its bar horizontally (like a progress bar) with inline labels.

### E4. Collapsible treemap
Make the treemap panel collapsible on mobile, defaulting to collapsed. The holdings table below provides the same data in a more mobile-accessible format.

### E5. Responsive grid breakpoints
Add Tailwind breakpoint variants to PORTFOLIO_GRID_TEMPLATE:
- `>= 1024px`: Current 6-column layout
- `768px-1023px`: 2-column (label + scrollable row of 5 values)
- `< 768px`: Single column (portfolio cards stacked)

### E6. Migrate remaining useEffect fetches to useQuery
HoldingsTab still uses 3x useEffect + setState for data fetching (lines 547, 562, 580). PositioningSummary already uses useQuery. Consistent patterns improve maintainability.

---

## Files Covered

| File | Lines | Status |
|------|-------|--------|
| `Positioning.tsx` | 59 | No issues (simple wrapper) |
| `panels/PositioningSummary.tsx` | 857 | C1, C4, W2, touch targets, grid issues |
| `tabs/HoldingsTab.tsx` | ~1700 | C2, C3, W1, W3, W4, W5, touch targets, table issues, design flaws |
| `shared/gridConfig.ts` | 22 | C1 (fixed 300px category width) |
| `constants/etf-categories.ts` | N/A | No mobile issues (data only) |
| `types.ts` | N/A | No mobile issues (types only) |
| `index.ts` | N/A | No mobile issues (barrel export) |
