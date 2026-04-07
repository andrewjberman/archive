# Attribution Page -- Mobile Readiness Audit (375px-428px)

**Agent:** 0.2.2_RD_Attribution
**Task Order:** ADHC_DESIGN-024
**Date:** 2026-04-07
**Scope:** portal/src/pages/Attribution/ (all .tsx/.ts files)
**Target viewport:** 375px-428px (iPhone SE through iPhone 15 Pro)

---

## 1. Fixed-Width Elements

### AssetAllocationSummary.tsx -- Table columns (CRITICAL)
- Line 146: `width: '130px'` -- Asset Class column
- Line 147: `width: '95px'` -- Style Weight
- Line 148: `width: '95px'` -- Benchmark Weight
- Line 149: `width: '85px'` -- Tilt
- Line 150: `width: '95px'` -- Asset Allocation
- Line 151: `width: '95px'` -- Fund Selection
- Line 152: `width: '95px'` -- Style Allocation
- Line 153: `width: '95px'` -- Total
- **Minimum table width: ~795px** -- 2.1x wider than 375px viewport

### SelectionTab.tsx -- Table columns (CRITICAL)
- Line 402: `width: '80px', minWidth: '80px'` -- Asset Class
- Line 403: `width: '110px', minWidth: '110px'` -- Sub Asset Class
- Line 404: `width: '55px', minWidth: '55px'` -- Ticker
- Line 405: `width: '250px', minWidth: '250px'` -- Name (largest offender)
- Line 406: `width: '60px', minWidth: '60px'` -- Weight
- Lines 408-414: 6 more data columns at 65-85px each
- **Minimum table width: ~995px** -- 2.65x wider than 375px viewport

### HoldingsTab.tsx -- Table columns (CRITICAL)
- Lines 648-695: 24+ columns with fixed widths:
  - Basic info (5 cols): 80+110+55+250+60 = 555px
  - Model breakdown (5 cols): 5x45px = 225px
  - Characteristics (7 cols): ~360px
  - Performance (6 cols): 6x100px = 600px
  - Attribution (4 cols): ~500px
- **Minimum table width: ~2,240px** -- 5.97x wider than 375px viewport
- Line 651: Name column at 250px alone is 67% of viewport

### AllocationHeatmap.tsx -- Grid (CRITICAL)
- Line 498: `const CATEGORY_WIDTH = '300px'` -- 80% of viewport consumed by one column
- Line 499: `repeat(5, 1fr)` -- remaining 75px split across 5 columns = 15px per column (illegible)

---

## 2. Hardcoded Heights

| File | Line | Value | Impact |
|------|------|-------|--------|
| HoldingsTab.tsx | 567 | `h-[400px]` | Treemap container -- 60% of mobile viewport height |
| HoldingsTab.tsx | 569 | `h-[400px]` | Empty state -- same |
| HoldingsTab.tsx | 638 | `h-32` (128px) | Table loading state |
| SelectionTab.tsx | 392 | `h-32` (128px) | Loading state |
| SelectionTab.tsx | 394 | `h-32` (128px) | Empty state |
| StylePolicyComparison.tsx | 60, 266 | `h-16` (64px) | Diverging bar containers |
| StylePolicyComparison.tsx | 301 | `h-12` (48px) | Underweight bar height |

Recommendation: Treemap height should use responsive values (`h-[250px] md:h-[400px]`). Bar heights are acceptable.

---

## 3. Non-Responsive Grids/Layouts

### AllocationHeatmap.tsx (CRITICAL)
- Line 499: `gridTemplateColumns: '300px repeat(5, 1fr)'` -- 6-column grid with 300px fixed left column
- At 375px: 300px category + 5 columns at 15px each = unreadable
- Recommendation: Stack to 2-column or card layout on mobile

### StylePolicyComparison.tsx
- Line 238: `max-w-4xl mx-auto` (896px) -- constrains but content is flexible; works at 375px with compressed bars
- Line 228: `p-8` (32px padding each side) -- reduces content area to 311px on a 375px screen

---

## 4. Touch Targets

### Portfolio/Period Selector Buttons (MARGINAL)
- StylePolicyComparison.tsx lines 108, 128, 200, 222: `px-3 py-1.5` = ~6px vertical touch area below 44px minimum
- SelectionTab.tsx line 353: Same pattern
- HoldingsTab.tsx line 550: Same pattern
- Actual rendered size: ~32px height. Below 44px recommendation but functional.

### View Mode Toggles (HoldingsTab.tsx)
- Lines 623-634: 3 toggle buttons in tight flex gap-1 -- cramped at 375px

---

## 5. Charts

### Treemap (HoldingsTab.tsx)
- Line 573: `ResponsiveContainer width="100%" height={400}` -- width is responsive, height is fixed
- Treemap cells shrink proportionally; at 375px, smallest cells become unreadable (<20px)
- Treemap tooltip may overflow viewport edges on small screens

### Diverging Bars (StylePolicyComparison.tsx)
- Lines 266-350: Absolute-positioned bars within `relative h-16` container
- Works at 375px but bars become very narrow; tilt percentage labels may overlap center line

---

## 6. Tables

All three data tables share the same critical problem: they are designed for 1920px desktop and have no mobile adaptation.

| Table | File | Min Width | Columns | Scroll Required |
|-------|------|-----------|---------|-----------------|
| Allocation Summary | AssetAllocationSummary.tsx:143 | 795px | 8 | 420px horizontal scroll |
| Selection Detail | SelectionTab.tsx:398 | 995px | 11 | 620px horizontal scroll |
| Holdings Detail | HoldingsTab.tsx:642 | 2,240px | 24+ | 1,865px horizontal scroll |

All tables have `overflow-x-auto` (horizontal scroll) which prevents layout breakage, but UX is poor:
- Sticky first column preserves context during scroll
- At 375px, only 1-2 data columns visible at any time
- Users must scroll horizontally to compare values across columns

---

## 7. Text/Content Overflow

| File | Line | Issue |
|------|------|-------|
| SelectionTab.tsx | 542 | `whitespace-nowrap` on sub-asset class label -- may overflow 110px column |
| HoldingsTab.tsx | 907 | `whitespace-nowrap` on sub-asset class label -- same issue |
| HoldingsTab.tsx | 923 | ETF name has `truncate block` -- properly handled |
| SelectionTab.tsx | 560 | ETF name has `truncate block` -- properly handled |
| AssetAllocationSummary.tsx | 157-180 | Table headers at `text-[10px]` -- borderline readable on mobile |
| AllocationHeatmap.tsx | 548 | Section header `whitespace-nowrap` -- may push past 300px category column |

---

## 8. Control Bars

### Combined Portfolio + Period Selector (OVERFLOW RISK)
- StylePolicyComparison.tsx lines 181-226: Both selectors in `flex items-center gap-3`
- Portfolio selector: 5 buttons at ~32px + gaps = ~200px
- Gap between selectors: 12px
- Period selector: 4 buttons at ~32px + gaps = ~135px
- **Total: ~347px** -- fits at 375px but with only 28px margin
- With AGG button added (AssetAllocationSummary.tsx line 314): 6 buttons = ~240px -- will overflow with period selector

### PanelHeader Layout
- PanelHeader uses `flex items-center justify-between` (PanelHeader.tsx:61)
- Title (left) + actions (right, flex-shrink-0) -- actions won't shrink
- At 375px: title may be fully compressed to 0 width if actions exceed available space

---

## 9. Absolute Positioning

### StylePolicyComparison.tsx -- Diverging Bars
- Line 268: Center divider `absolute left-1/2 top-0 bottom-0`
- Lines 274, 284: Parity indicators `absolute left-0 right-1/2` and `absolute left-1/2 right-0`
- Lines 298, 318: Under/overweight bars with same split pattern
- Line 337: Center target icon `absolute left-1/2 -translate-x-1/2`
- All properly bounded within `relative h-16` parent -- works at 375px but spacing is tight

---

## 10. Design Flaws and Enhancement Opportunities

### A. Table-First Design Pattern (HIGH IMPACT)
**Files:** HoldingsTab.tsx, SelectionTab.tsx, AssetAllocationSummary.tsx
Tables with 8-24+ columns are a desktop-only pattern. Mobile alternatives:
- Card-based layout with expandable rows
- Tab-based column grouping (show Basic | Performance | Attribution as sub-tabs)
- Collapsible detail panels (tap ticker to expand full row data)

### B. AllocationHeatmap Fixed Grid (HIGH IMPACT)
**File:** AllocationHeatmap.tsx:498-499
300px fixed category column makes the grid unusable below 768px.
- Use `minmax(120px, 300px)` for the category column
- Consider vertical stacking on mobile (portfolio rows become columns)

### C. Treemap Height Responsiveness (MEDIUM IMPACT)
**File:** HoldingsTab.tsx:573
Fixed 400px height is excessive on mobile. Use responsive classes:
`h-[250px] md:h-[400px]` or a computed height based on viewport.

### D. Control Bar Stacking (MEDIUM IMPACT)
**Files:** StylePolicyComparison.tsx, AssetAllocationSummary.tsx, SelectionTab.tsx, HoldingsTab.tsx
Portfolio + period selectors should stack vertically on mobile:
- Current: `flex items-center gap-3` (horizontal)
- Mobile: `flex flex-col md:flex-row gap-2` (vertical stack)

### E. PanelContent Padding (LOW IMPACT)
**File:** StylePolicyComparison.tsx:228
`p-8` (32px) wastes 17% of viewport width on padding at 375px.
- Use `p-4 md:p-8` for responsive padding

### F. Data Density Reduction (LOW IMPACT)
The HoldingsTab table shows all 24+ columns simultaneously. Desktop users rarely need all columns at once. Consider:
- Column visibility toggles (let users choose which columns to display)
- Progressive disclosure (basic columns visible, expand for details)
- This benefits both mobile AND desktop UX

---

## Summary

| Category | Severity | Findings | Primary Files |
|----------|----------|----------|---------------|
| Fixed-width table columns | CRITICAL | 50+ columns across 3 tables | HoldingsTab, SelectionTab, AssetAllocationSummary |
| Fixed grid layout | CRITICAL | 300px column in 6-col grid | AllocationHeatmap |
| Fixed chart height | HIGH | 400px treemap, 64px bars | HoldingsTab, StylePolicyComparison |
| Control bar overflow | HIGH | Portfolio+period at 347-383px | StylePolicyComparison, AssetAllocationSummary |
| Touch targets | MEDIUM | Buttons at ~32px height | All files with selectors |
| Text overflow | MEDIUM | whitespace-nowrap in constrained columns | SelectionTab, HoldingsTab |
| Font size | MEDIUM | text-[10px] headers | AssetAllocationSummary |
| Padding waste | LOW | p-8 on 375px viewport | StylePolicyComparison |

### Files with zero mobile issues
- Attribution.tsx -- simple page wrapper, responsive
- types.ts -- TypeScript types only, no UI
- index.ts -- barrel export, no UI
- constants/etf-categories.ts -- data only, no UI
- utils/buildAttributionData.ts -- data processing only, no UI
- constants/holdings-shared.tsx -- types, utils, and treemap content (content renderer is responsive via SVG foreignObject scaling)
