# Mobile Readiness Audit: Macroeconomics

## Summary

The Macroeconomics page is a data-dense desktop dashboard with multiple charts, tables, and interactive controls. It is **not mobile-ready**. At 375px, the heatmap table overflows, charts become unreadable, the time series modal is unusable, and most control bars stack poorly. The page requires significant responsive redesign for mobile -- this is not a CSS-tweak effort but a layout restructuring with progressive disclosure.

## Critical Issues (would break on mobile)

| File:Line | Issue | Current Value | Impact at 375px |
|-----------|-------|---------------|-----------------|
| MacroHeatmap.tsx:182 | Value mode table has 13 columns (indicator + 12 months) with `tableLayout: fixed` and `width: 22%` / `78%/12` splits | 13 fixed-layout cols, `col style={{ width: '22%' }}` | Table cells compress to ~5px each. Values completely unreadable. Needs horizontal scroll with sticky first column. |
| MacroHeatmap.tsx:237 | Position mode table has 9 columns with fixed percentage widths (22%, 10%, 9%, 11%, 9.6% x5) | 9 fixed-layout cols | Same issue -- 375px cannot hold 9 columns. Needs card layout or horizontal scroll. |
| MacroTimeSeriesModal.tsx:405 | Modal width `w-[1200px] max-w-[95vw]` | 1200px nominal, capped at 356px on 375px screen | Modal content (stats row, chart, controls) designed for wide layout. Stats row `flex gap-8` will wrap chaotically. Controls will overflow. |
| MacroTimeSeriesModal.tsx:449 | Summary stats row `flex gap-8` with 4 stat blocks + controls in `flex justify-between` | ~800px natural width | Stats and controls will wrap unpredictably. 2xl font sizes too large for mobile. |
| MacroTimeSeriesModal.tsx:504 | Controls section `flex items-center gap-6` with two stacked label+input pairs | ~250px minimum | Will collide with stats at narrow widths. No responsive stacking. |
| YieldCurveTab.tsx:334 | Curve toggle checkboxes `flex items-center gap-4` in PanelHeader actions | 3 checkboxes ~280px | Will overflow PanelHeader at 375px. Labels will wrap or clip. |
| YieldCurveTab.tsx:525 | Yield change bars `grid grid-cols-10` | 10 fixed columns | Each column gets ~33px. Bars + text overlap. Needs horizontal scroll or reduced tenor set. |
| VolatilityTab.tsx:167 | Speedometer SVG container `w-80` (320px) | Fixed 320px width | Leaves only 55px margin at 375px. `max-w-full` added in Phase 2 helps, but tick labels at 7px SVG fontSize may overlap. |

## Warnings (would degrade on mobile)

| File:Line | Issue | Current Value | Recommendation |
|-----------|-------|---------------|----------------|
| YieldCurveTab.tsx:371 | Chart container `h-[400px]` | Fixed 400px height | Consider `h-[250px] sm:h-[400px]` for mobile -- shorter charts prevent excessive scrolling. |
| VolatilityTab.tsx:586 | Historical chart `h-[400px]` | Fixed 400px height | Same -- reduce on mobile. |
| MacroTimeSeriesModal.tsx:583 | Modal chart `h-[400px]` | Fixed 400px height | Modal already caps at 90vh. Chart may need `h-[300px]` on mobile to leave room for header/stats. |
| YieldCurveTab.tsx:121 | Custom tooltip `min-w-[200px]` | 200px minimum width | Could overlap chart edges at 375px viewport. Consider reducing or removing min-width on mobile. |
| VolatilityTab.tsx:253 | Current value display `text-5xl` | 48px font | May overflow container on very long values. Consider `text-3xl sm:text-5xl`. |
| VolatilityTab.tsx:257 | Regime badge `text-base px-4 py-2 rounded-full` | ~120px width | Fine for mobile but takes significant horizontal space. |
| VolatilityTab.tsx:285 | Change stats `grid grid-cols-3 max-w-md` | 3 columns in 448px max | Fits at 375px but tight. Consider `gap-4` instead of `gap-6`. |
| MacroHeatmap.tsx:133 | Header row `flex items-center justify-between gap-3` | Title + controls side by side | Controls will wrap below title. Needs explicit `flex-wrap` and mobile stacking. |
| MacroHeatmap.tsx:327 | Percentile legend `flex items-center gap-6 flex-wrap` | 5 legend items | Has `flex-wrap` which helps. But items are wide (~120px each). Will wrap to 2-3 rows. Acceptable. |
| Macroeconomics.tsx:60 | Page description with 3 bold spans | ~300px natural width | May wrap awkwardly. Minor issue. |

## Touch Target Violations

| File:Line | Element | Estimated Size | Minimum Required |
|-----------|---------|----------------|------------------|
| MacroHeatmap.tsx:149-170 | Display mode toggle buttons `px-3 py-1.5` | ~60x30px | 44px height. Buttons are 30px tall (py-1.5 = 6px + ~18px text). **Fails 44px minimum.** |
| MacroHeatmap.tsx:393 | Group header row (click to expand/collapse) | Full row width x ~38px | Row height `py-2.5` = ~38px. Close to 44px but slightly under. |
| MacroHeatmap.tsx:520-525 | Indicator name click target | Variable width x ~32px | `py-2` = ~32px text area. **Fails 44px minimum.** |
| YieldCurveTab.tsx:336-364 | Checkbox toggles `gap-2` | ~16x16px checkbox | Checkbox itself is tiny. Label adds click area but total height ~24px. **Fails 44px minimum.** |
| VolatilityTab.tsx:93-111 | VIX/MOVE toggle buttons `px-3 py-1.5` | ~50x30px | Same as display mode toggle. **Fails 44px.** |
| MacroTimeSeriesModal.tsx:511-530 | Display mode buttons in modal `px-3 py-1.5` | ~70x30px | **Fails 44px.** |
| MacroTimeSeriesModal.tsx:429-433 | Close button `p-2` with 20px icon | ~36x36px | Close to but under 44px. `p-2` = 8px padding + 20px icon = 36px. |
| VolatilityTab.tsx:761-764 | Period select dropdown `px-3 py-1.5` | ~100x30px | **Fails 44px height.** |

## Chart Responsiveness

| Chart | Container | ResponsiveContainer? | Mobile Concern |
|-------|-----------|---------------------|----------------|
| Yield Curve (YieldCurveTab:372) | `h-[400px] w-full overflow-hidden` | Yes | X-axis tenor labels (10 tenors) will overlap at 375px. `minTickGap` helps but needs testing. Tooltip `min-w-[200px]` may clip. |
| Volatility Historical (VolatilityTab:587) | `h-[400px] overflow-hidden` | Yes | X-axis date labels may overlap. ReferenceLine labels at `position: 'right'` will clip off-screen on narrow charts. |
| Macro Time Series Modal (MacroTimeSeriesModal:584) | `h-[400px] overflow-hidden` | Yes | Chart itself responsive, but 5 percentile ReferenceLine labels at right edge will overlap and clip. ReferenceArea bands fine. |
| Yield Change Bars (YieldCurveTab:525) | `grid grid-cols-10` (not a Recharts chart) | N/A | HTML grid, not Recharts. 10 columns at 375px = 33px each. Bar labels overlap. |
| Speedometer Gauge (VolatilityTab:168) | `w-80 max-w-full h-40` SVG `viewBox="0 0 200 100"` | N/A (SVG viewBox) | SVG scales via viewBox. At 320px, tick labels at fontSize 7 become hard to read. Needle and arcs still functional. |

## Table Responsiveness

| Table | Columns | Est. Width | Scroll Wrapper? | Mobile Strategy |
|-------|---------|------------|-----------------|-----------------|
| MacroHeatmap Value Mode (MacroHeatmap:182) | 13 (name + 12 months) | ~1200px effective | Yes (`overflow-auto max-h-[800px]`) but **only vertical scroll** | Needs `overflow-x-auto` on wrapper. Sticky first column (`sticky left-0 z-10`) already present -- would work with horizontal scroll. |
| MacroHeatmap Position Mode (MacroHeatmap:237) | 9 (name + 8 data cols) | ~900px effective | Same wrapper | Same fix needed. Already has sticky first column. |

## Design Flaws (not mobile-specific)

- **MacroHeatmap.tsx:179** — Wrapper has `overflow-auto` but the table uses `tableLayout: fixed` with percentage widths. On any viewport under ~900px, the fixed percentages force columns to compress rather than scroll. Adding `min-w-[1100px]` on the table element would enable horizontal scrolling.
- **MacroHeatmap.tsx:508, 582** — `isLastRow && ''` is a dead conditional: the empty string is falsy, so this `cn()` argument never contributes a class. Dead code.
- **MacroTimeSeriesModal.tsx:449-501** — Summary stats row uses a flat `flex gap-8` with 4 stats + controls in `flex justify-between`. This is fragile -- any additional stat or longer value breaks the layout. A responsive grid (`grid-cols-2 lg:grid-cols-5`) would be more robust.
- **VolatilityTab.tsx:371-394** — AI summary sections use `idx` as React key. If sections reorder between renders (unlikely but possible with different summaries), React will reuse wrong DOM nodes. Low risk.
- **YieldCurveTab.tsx:525** — The 10-col change bars grid has `min-w-0 overflow-hidden` (added in Phase 2) but the bars inside use absolute `height` via inline style. At very narrow widths, the bar text `text-xs font-mono` (change value + tenor) stacks to ~24px which exceeds the bar container. The `overflow-hidden` clips this rather than scrolling it.
- **MacroHeatmap.tsx:131** — Root container uses raw div with manual `bg-`, `border`, `rounded-lg` instead of `<Panel>` primitive. This is the only panel on the page not using the Panel component system. Inconsistent with other pages.

## Enhancement Opportunities

- **Progressive disclosure for heatmap**: On mobile, collapse the 12-month value grid to show only the latest month + sparkline indicator. Tap to expand full history. This is the single most impactful mobile enhancement.
- **Card layout for position mode**: Replace the 9-column table with a card-per-indicator layout on mobile: indicator name, percentile badge, and a mini percentile bar. Much more touch-friendly.
- **Bottom sheet for time series modal**: Replace the centered modal with a bottom sheet (`fixed bottom-0`) on mobile. Standard mobile pattern, avoids the 95vw squeeze issue.
- **Swipeable tabs**: The yield-curve/volatility tabs could use swipe gestures on mobile (react-swipeable or native touch events).
- **Simplified speedometer on mobile**: At 375px, the full gauge with tick labels is cramped. A simpler vertical progress bar or numeric display with color would communicate the same information more clearly.
- **Yield change bars as horizontal list**: Rotate the 10-col grid to a horizontal scrollable strip with `overflow-x-auto flex gap-2`, allowing each bar to maintain readable width.
- **Touch-friendly group headers**: Increase heatmap group header row height to 48px+ for comfortable mobile tapping. Currently ~38px.
- **Responsive chart heights**: All three `h-[400px]` chart containers should use `h-[250px] md:h-[400px]` to prevent excessive scrolling on mobile.
- **Collapsible AI summary**: Long AI summaries (3-4 sections with bullets) could use a "Show more" truncation on mobile, defaulting to the first section.
