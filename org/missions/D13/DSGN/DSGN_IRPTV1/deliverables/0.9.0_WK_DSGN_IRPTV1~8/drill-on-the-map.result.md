# DSGN_IRPTV1.TO-IV-e-13 -- drill-on-the-map -- result

**Worker:** `0.9.0_WK_DSGN_IRPTV1~8` | **Branch pair:** `wk-DSGN_IRPTV1-8` / `wk-DSGN_IRPTV1-8-portal` |
**Portal commit:** `1fcef85de0a306b13ccc91e5fff53b46ea94ef20` | **Order:** the AMENDED text (issuer amendment
`1215c0d07a`, item N5 -- the worker's on-disk copy of the TO predates that amendment; the amended text
supplied in the launch prompt is authoritative for this run, per the launch instruction).

## What was built

- **`AllocationBars.tsx` (a).** `categoryBarsFrom` now recurses: an L0 branch that carries a `kind ===
  'model'` node ANYWHERE beneath it is expanded into ONE BAR PER MODEL (never past the model into its
  own sleeve/security children); a branch with no model anywhere below it keeps IV-e-5's original single
  L0 bar, unchanged. Each bar's fill is now `categoryBarColor(category.modelCode)` -- the library colour
  for the served `modelCode` (small, deliberate duplicate of `DrillTree.tsx`'s
  `MODEL_CODE_FOR_REGISTRY_KEY` + `getModelColor` resolution chain, since DrillTree.tsx is out of this
  cell's grant beyond its legend block) -- never the bar's own label, and `ASSET_CLASS.other`
  (Unclassified grey) when no code resolves, retiring the old hardcoded
  `bg-[hsl(var(--palette-navy))]` fill entirely.
- **`HoldingsTreemap.tsx` (b).** New `modelOptionsFrom` reads the distinct `model` ancestors actually
  present among the map's own leaves. `treemapLeavesFrom` gained an optional `modelRef` argument:
  `null` (the default) is byte-identical to the pre-cell behaviour (the "back to all" state); a model's
  own `nodeRef` narrows to exactly that model's securities via the nearest `model` ancestor (never
  `sleeve`, so a narrowed set cannot leak a security that merely shares a sleeve label with a different
  model). A chooser `<nav>` ("All securities" + one button per model) drives `useState`. The hover card
  (`TreemapHoverTooltip`, now exported) is rebuilt onto the portal's shared `@/components/DataTooltip`
  (header = ticker + name, rows = Value / Weight / Asset Class) instead of the old bespoke `<div>` card --
  the Positioning `HoldingsTreemapTooltip` pattern (read only, never imported).
- **`DrillTree.tsx` (c), legend block only.** `<Legend />` now takes a `content={renderDrillLegend}`
  custom renderer (new, exported for direct testing) that wraps entries to COLUMNS (`flex-wrap`) inside a
  bounded, scrollable strip (`max-h-32 overflow-y-auto`) instead of recharts' bare default, so a
  20+-entry legend stays readable with nothing clipped or truncated. No other line in this file changed.
- **Three new tests**, `__tests__/dsgn-irptv1/iv-e-13.{bars-stop,map-drill,legend-scale}.test.ts`, each
  printing its own VERDICT only when every arm holds. Every fixture is an **in-memory `HoldingsSnapshot`
  built inline in the test file** -- `fixtures/` is NOT in this cell's `<paths>` grant (only
  `__tests__/dsgn-irptv1/` is), so this follows the exact precedent `iv-e-12.unclassified.test.ts`
  already set rather than adding a new file under `fixtures/`. (First attempt built two new fixture JSON
  files under a new `fixtures/iv-e-13/` directory; caught during self-review against the grant and
  redone before any commit -- no surprise row filed, since nothing shipped outside the grant and the
  order's own BOUNDS language ("discover fixture names from disk") together with the sibling orders'
  identical `<paths>` blocks made the intended path unambiguous once checked.)

## Why `renderDrillLegend`/`TreemapHoverTooltip` are tested directly, not through a full component mount

Measured this session: `renderToStaticMarkup(createElement(DrillTree, {snapshot}))` renders an EMPTY
`recharts-wrapper` div (console: "The width(-1) and height(-1) of chart should be greater than 0")
because `ResponsiveContainer` needs a real layout measurement this portal's test environment (no jsdom/
happy-dom, per the established precedent in `__tests__/fe-s-76/revision-mismatch-guard.test.ts`'s own
header) cannot provide. `renderDrillLegend` and `TreemapHoverTooltip` are therefore exercised directly
with the exact payload shape the real chart would hand them (for the legend: `buildSliceRows` output
colour-resolved by the same `modelSliceColor` DrillTree's own `<Cell>` uses) -- the only reachable unit,
and the one piece of markup each cell actually owns.

## Acceptance

- **IVE13-AC1** `bun test .../iv-e-13.bars-stop.test.ts` -> `VERDICT: BARS-STOP-OK`, 1 pass/0 fail. PASS.
- **IVE13-AC2** `bun test .../iv-e-13.map-drill.test.ts` -> `VERDICT: MAP-DRILL-OK`, 1 pass/0 fail. PASS.
- **IVE13-AC3** `bun test .../iv-e-13.legend-scale.test.ts` -> `VERDICT: LEGEND-SCALE-OK`, 1 pass/0 fail. PASS.
- **IVE13-AC4** judgment="true" -- RECORDED, no verdict taken by this worker; graded at L9 by
  `3.0.0_SA_CVO` from the real `localhost:5174` run.

## Controls

- **Mutant.** `categoryBarColor` temporarily forced to always return the retired
  `'hsl(var(--palette-navy))'`, ignoring `modelCode` entirely. Re-ran IVE13-AC1: FAILED on every colour
  arm (`nd-model-a`, `nd-model-b`, `nd-model-c`, `nd-cat-client`, plus the direct `categoryBarColor(...)`
  calls) -- 8 failures printed, 0 pass/1 fail, exactly as expected. Restored to the real implementation;
  `git diff --stat -- AllocationBars.tsx` after restore matched the pre-mutant diff exactly (76
  insertions / 7 deletions both times; the committed diff, `git show --stat 1fcef85d --
  AllocationBars.tsx`, is the same 76/7). Full `dsgn-irptv1/` suite and `bun run typecheck` re-run clean
  after restore.
- **Regression.** `bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/` -- 45 pass / 0 fail / 250
  expect() calls across 31 files (IV-e-12's base was 42/28/247; +3 files/+3 pass/+3 expect() calls
  matches exactly this cell's 3 new test files, no other file regressed). `bun run typecheck` (`tsc -b
  --noEmit`) rc=0, 0 diagnostics, both before and after the mutant/restore cycle.
- **Repo-wide spot check.** `bun test src/pages/InvestorReporting/__tests__/` (172 files, 780 tests):
  85 pre-existing failures in files that do NOT import from any of this cell's three touched files
  (`fe-s-9`, `fe-s-90`, `mvp-selection/directory-browse.test.ts`, etc. -- none of which import
  `AllocationBars`/`HoldingsTreemap`/`DrillTree`); every one of the 13 files across the whole
  `InvestorReporting` suite that DOES import from a touched file (found via grep) passed, individually
  re-run: `fe-s-76/revision-mismatch-guard.test.ts`, `dsgn-irptv1/{model-colors,s6.names-and-tiles,
  iv-e-1.l2-members,exact-amounts,iv-e-5.allocation-bars,iv-e-5.treemap,iv-e-11.irpt-by-code,
  iv-e-12.unclassified,iv-t-3.hero-fed}.test.ts` plus this cell's own three -- 45 pass / 0 fail across the
  `dsgn-irptv1/` group and 24 pass / 0 fail for `fe-s-76` + the four others run separately.
- **Lint.** `bun run lint` (eslint, repo-wide): 0 errors both before and after this cell's edits; the only
  new warnings on the three touched files are `react-refresh/only-export-components` (a file exporting
  more than one component/function), the SAME pre-existing warning class already present on dozens of
  other files in this codebase (e.g. `SecurityList.tsx`), not introduced by this cell's design.

## Declared exclusions

- Wiring the new `treemap-model-filter` chooser or the allocation bars into any cross-component
  "selected model" state shared with `AllocationBars` -- the order's own bounds hold `HoldingsTab.tsx`
  (the only file that could carry shared state between the two) out of this cell's `<paths>` grant;
  cell (b) says "the Securities map carries the drill", so the drill's own state is self-contained inside
  `HoldingsTreemap.tsx`, which is what was built.
- Editing `DataTooltip.tsx` -- not needed. Its existing `header`/`rows` props expressed every field the
  criterion asks for (ticker, name, value, weight, asset class) without a prop change, so the "if the
  hover pattern cannot be expressed through its existing props, render inside HoldingsTreemap.tsx
  instead" branch of the launch instruction was not reached.
- Push, merge, rebase, `checkout --` or `clean` of either repository -- forbidden by BOUNDS. Every commit
  is LOCAL on `wk-DSGN_IRPTV1-8` (workspace) and `wk-DSGN_IRPTV1-8-portal` (portal).

## Surprises

None filed for this cell. `DSGN_IRPTV1-W8-S2` was reserved by the launch instruction but not needed: the
one near-miss (the fixtures/ directory placement) was caught and corrected before anything left the
grant, so it never became a surprise (nothing shipped outside `<paths>`, nothing contradicted a premise
of the order once the grant was re-read).
