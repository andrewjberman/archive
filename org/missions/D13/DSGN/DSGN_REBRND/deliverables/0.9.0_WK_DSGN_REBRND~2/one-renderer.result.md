# DSGN_REBRND.TO-RB-s-11 -- one rendering system -- RESULT (amended order)

Worker: `0.9.0_WK_DSGN_REBRND~2` | Cell: `RB-s-11` | Portal branch: `wk-dsgn_rebrnd-2` (from `feature/d13-visual-elevation`)

**Status: all five mechanical criteria PASS by output; `RB11-AC6` recorded for the CVO's L9 grade.**

This order was AMENDED by the issuer at the drain, on this worker's row `DSGN_REBRND-W2-S1`. The first
pass ended with `RB11-AC2` and `RB11-AC3` FAIL and the status left `pending`, because the word cloud in
`TopicCloud.tsx` cannot move to recharts without changing what the chart shows. The amendment carved the
word cloud out of the census (bounded to that one file) and granted `portal/vite.config.ts` on row
`DSGN_REBRND-W2-S2`. **Both amended criteria were re-run here BEFORE anything else was touched**, to test
the issuer's claim that they already passed on work already done rather than accept it: they did.

## What moved (the list is the evidence)

### Charting -- migrated to recharts (4 apexcharts files + 1 nivo file), portal `19be39c1`

1. `portal/src/pages/ModelPortfolios.tsx` -- apexcharts donut (AUA-by-model) -> recharts `PieChart`/`Pie`/`Cell`. Same data, same per-model colours (`getModelColor`), same click-to-select (Non-Model detected by name, not index), same center label (selected model name+value, or `Total <assetLbl>` / NOT_TRACKED / AUA_UNAVAILABLE when absent). Custom legend below untouched.
2. `portal/src/pages/AdvisorIntelligence/_shared/panels/ConsolidatedOverviewPanel.tsx` -- apexcharts donut (asset mix) -> recharts. Same `composition.mix` data, same `colorFor` mapping, same click-to-select gated by `readonlyAssetClass`, same center label.
3. `portal/src/pages/AdvisorIntelligence/_shared/AdvisorPublicProfile.tsx` -- apexcharts donut (role composition) -> recharts. The original carried NO chart-level interactivity (labels disabled, hover/active `filter:none`; the center text was already a custom overlay driven by tile hover), so the migrated donut is a plain static ring and `hoverIdx` is untouched.
4. `portal/src/pages/AdvisorIntelligence/_shared/tabs/DistributionTab.tsx` -- apexcharts donut (AUM/NNA distribution, drillable) -> recharts. Same per-segment colour rule (Other / NNA-diverging / canonical category map / cohort palette fallback), same `handleSegmentClick`, same center label. The "warm the react-apexcharts lazy chunk" mount effect is gone -- nothing to warm once the chart is eager recharts.
5. `portal/src/pages/FactorTilts/panels/FactorTiltOverviewPanel.tsx` -- `@nivo/radar`'s `ResponsiveRadar` -> a new `FactorRadarChart` on recharts `RadarChart`/`PolarGrid`/`PolarAngleAxis`/`PolarRadiusAxis`/`Radar`/`Customized`/`Tooltip`. Recharts' default angle convention for N evenly-spaced categories (12 o'clock, clockwise, 360/N per step) is identical to the retired nivo layer's, so the benchmark-parity ring (fixed at 60% of outer radius by construction of `minValue = -1.5 * maxValue`) and the per-factor label offsets port over with the same trigonometry. Tooltip content (`DataTooltip`, real un-transformed values via each point's `_original`) preserved.

### Build config -- `portal/vite.config.ts`, portal `8274a955` (granted by the amendment)

`'vendor-apexcharts': ['apexcharts']` and `'vendor-nivo': ['@nivo/core','@nivo/radar']` removed from
`build.rollupOptions.output.manualChunks`. Both named packages that are no longer dependencies and that
no `.tsx` imports -- a chunk rollup can only emit empty, or fill from a stale `node_modules` copy a clean
install will not have. `vendor-react`, `vendor-recharts`, `vendor-ui`, `vendor-query` unchanged.

**This edit is covered by `RB11-AC1`, and that coverage is measured, not assumed:** `tsconfig.node.json`
carries `include: ["vite.config.ts"]`, so `tsc -b` type-checks it. Proven by positive control -- an
injected `const __rb11_probe: number = "not a number"` made the criterion's own invocation fail
`rc=2` naming `vite.config.ts(239,7)`; restored, `rc=0`, and `git diff --stat` then showed only the
intended 6 insertions / 2 deletions.

### Icons

`phosphor-react` had **zero importing `.tsx`/`.ts` files** at issuance (row `DSGN_REBRND-W2-S3`: the
order's "1 file" was `portal/src/components/TrendingTopicImage.README.md`, documentation for a
Lambda-side renderer). No call site existed to migrate; the orphaned dependency line was removed.
`lucide-react` survives at 99 importing files.

### Carved out, not migrated -- `TopicCloud.tsx` (row `DSGN_REBRND-W2-S1`)

`portal/src/components/market-performance/TopicCloud.tsx` keeps `@visx/text` + `@visx/wordcloud`. It draws
a sentiment-coloured word cloud via an Archimedean-spiral layout, with per-word size and (x,y) position
solved by the library. recharts ships no word-cloud chart type, and any substitute (a ranked bar list, a
treemap) shows different content. The amended order carves it out for the same reason `ag-grid` was
carved out: a word-cloud primitive carries no axis, no tick, no tooltip and no legend, so it is not in the
population FWD-8 grades.

**The carve-out is bounded and `RB11-AC2` enforces the bound**: `visx` must appear in at most one file and
that file must be `TopicCloud.tsx`. Measured this run -- `VISX-FILES: ['portal\src\components\market-performance\TopicCloud.tsx']`,
exactly one. A second visx importer re-opens the criterion.

### Animation

`framer-motion` had zero importing files (dead dependency); `motion` (`motion/react`) is the live one
(`portal/src/ui/components/catalyst/{sidebar,navbar}.tsx`, untouched). `framer-motion` removed, `motion` retained.

### `package.json`

Removed: `apexcharts`, `react-apexcharts`, `@nivo/core`, `@nivo/radar`, `@visx/scale` (zero importers
anywhere), `phosphor-react`, `framer-motion` -- seven packages. Retained: `@visx/text`, `@visx/wordcloud`
(the carved-out word cloud genuinely imports both), `motion`, `recharts`, `lucide-react`, `ag-grid-*`
(out of census), everything else unchanged.

`portal/bun.lock` intentionally untouched -- see `declared_exclusions` in the instance, including the
stated consequence that the lockfile still carries entries for the removed packages until a legitimate
`bun install` runs.

## The defect this cell found in its own work

The first `FactorRadarChart` used recharts' `<ResponsiveContainer>`, which measured `width(-1) height(-1)`
for that panel -- it is an `xl:grid-cols-2` grid item, and a 100%-width `ResponsiveContainer` child inside
a grid item with the browser default `min-width: auto` is a circular sizing dependency. The radar rendered
NOTHING (zero `.recharts-wrapper` elements) while an unrelated recharts bar chart lower on the same page
rendered fine, because that one is not a grid item. **`tsc` was clean throughout**; nothing in the
acceptance battery required rendering that route. It was found only by live-rendering `/factor-tilts` with
a hand-built data fixture, and fixed by measuring the container with a `ResizeObserver` (the pattern
`TopicCloud.tsx` already uses in this codebase) and passing explicit pixel width/height, dropping
`ResponsiveContainer` entirely. Re-verified against the same fixture: hexagonal area, dashed
benchmark-parity ring, six labels at their designed offsets, dots.

The four donuts were never exposed to that interaction -- they pass fixed pixel `width`/`height` straight
to `<PieChart>`, matching the original ApexCharts calls' own fixed dimensions.

## Acceptance (full invocations and verbatim output in the proof-of-spec instance)

| criterion | verdict | deciding output |
|---|---|---|
| `RB11-AC1` typecheck | **PASS** | `rc=0` (covers `src/` AND `vite.config.ts`; positive control fired) |
| `RB11-AC2` one renderer | **PASS** | `RETIRED-IMPORTS: 0 VISX-FILES: [...TopicCloud.tsx]` / `VERDICT: ONE-RENDERER` |
| `RB11-AC3` packages removed | **PASS** | `RETIRED-STILL-PRESENT: 0 []` / `VERDICT: REMOVED` |
| `RB11-AC4` one animation lib | **PASS** | `ANIMATION-LIBS: 1 ['motion']` / `VERDICT: SINGLE` |
| `RB11-AC5` `/market` renders | **PASS** | `LOC : /market`, `CANVAS: rgb(195, 202, 218)`, `rc=0`; PNG re-captured after the vite edit and read |
| `RB11-AC6` shared treatment | RECORDED | `UNVERIFIABLE-BY-INSTRUMENT`, graded by `3.0.0_SA_CVO` at L9 |

**Note for the AC6 grade:** none of this cell's migrated charts render on `/market` -- they live on
`/portfolios`, the AdvisorIntelligence pages and `/factor-tilts`. The `/market` capture's own charts were
not touched by this cell, and the capture taken after the `vite.config.ts` edit is identical to the one
taken before it except for the Fear & Greed clock, which is the only moving value on the route.

## Rows filed

- `DSGN_REBRND-W2-S1` (OBSERVATION, ARMED, disarm `2.0.0_SA_COO~D`) -- the word-cloud migration blocker. **Resolved by the amendment**; disposition remains the CVO's at L9.
- `DSGN_REBRND-W2-S2` (OBSERVATION, INERT) -- dead `manualChunks` entries. **Acted on** in portal `8274a955` under the amended grant.
- `DSGN_REBRND-W2-S3` (OBSERVATION, INERT) -- "phosphor-react 1 file" was a README, not code.
- `DSGN_REBRND-W2-S4` (OBSERVATION, ARMED, disarm `2.0.0_SA_COO~D`) -- the amended TO reached this worktree but the merged 6-row channel document did not; the union is still owed at the drain, on a file whose two sides are an add/add conflict by construction. Disarm bar stated in the row: after the merge, the document must carry all four `W2` ids plus W1's and W3's, and the id set must be counted.
