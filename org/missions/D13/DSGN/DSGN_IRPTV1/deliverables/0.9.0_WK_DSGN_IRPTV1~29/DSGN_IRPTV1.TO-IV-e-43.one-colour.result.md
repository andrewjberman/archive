# DSGN_IRPTV1.TO-IV-e-43.one-colour -- session log, 0.9.0_WK_DSGN_IRPTV1~29

## What was built (O7 one colour, one meaning: UIR-25/37/44/46)

- `assetClass.ts` (page-local, in-grant): `ASSET_CLASS_COLOR.Equity` / `'Fixed Income'` /
  `Alternatives` moved one step down their own family's `PALETTE` ramp (`blue600` / `green600` /
  `orange600`) instead of the shared `ASSET_CLASS.equity` / `.fixedIncome` / `.alternatives`
  (`blue500` / `green500` / `orange500`) they used to equal byte-for-byte -- each of those three
  hexes is ALSO one of the five canonical `MODEL_PORTFOLIO_COLORS` primaries (Long Term / Intermediate
  Term / Ultra-Short Term), so a served model's row colour (`DrillTree`'s `rowColor`) and a served
  security's asset-class colour (`breakdown.memberColor`, the SAME `CategoryViewTree` breakdown
  dialog) could paint the identical hue for two different meanings -- exactly UIR-37's defect. Every
  other `ASSET_CLASS_COLOR` entry (Cash, Structured, Commodities, Unclassified, Other) is unchanged.
  The shared `lib/chartColors.ts` (`ASSET_CLASS`) and `lib/modelPortfolioColors.ts`
  (`MODEL_PORTFOLIO_COLORS`) registries are READ, never edited, per BOUNDS.
- `palette.ts` (new, page-local): `MODEL_CODE_FOR_REGISTRY_KEY` -- the five MDPF registry keys, a
  map the worker face named as duplicated verbatim in `DrillTree.tsx` and `AllocationBars.tsx` --
  now lives in this ONE module; both files import it instead of keeping their own copy.
- `DrillTree.tsx` / `AllocationBars.tsx`: import `MODEL_CODE_FOR_REGISTRY_KEY` from `./palette`;
  no behaviour change (`colorForServedModelCode` / `categoryBarColor` resolve identically, verified
  against the existing iv-e-11/25/31/13 tests).
- New test `iv-e-43.one-colour.test.tsx`: one named arm per row (UIR-25, UIR-37, UIR-44, UIR-46),
  built from in-memory `HoldingsSnapshot` fixtures (the `iv-e-44.securities-map.test.tsx` /
  `iv-e-13.map-drill.test.ts` technique -- never a new file under `fixtures/`, out of grant):
  - UIR-25: `drillSliceColor` over 5 canonical-model slices (+ `renderDrillLegend` called
    directly, the `iv-e-13.legend-scale.test.ts` harness, since a `ResponsiveContainer` lays out
    no real SVG under `renderToStaticMarkup`); `AllocationBars`' 6 rendered category-bar fills
    (1 non-model grey + 5 expanded model bars); `HoldingsTreemap`'s 8 leaf colours (one per served
    `HoldingAssetClass`) -- each set checked for `Set` cardinality == length (no duplicate).
  - UIR-37: no `ASSET_CLASS_COLOR` entry equals any of the five `getAllModelColors()` primaries;
    `modelRowColorMap` and a full `<DrillTree>` render's own `CategoryTile` SegmentBar + row list
    (a plain-DOM component, unconditionally in the static markup -- verified empirically, unlike
    the donut/pie) both draw each model's canonical colour; a structural byte-read of
    `DrillTree.tsx` / `AllocationBars.tsx` / `palette.ts` confirms the map is deduplicated (the
    registry-key literal appears once, in `palette.ts`, and both consumers import it).
  - UIR-44: `HoldingsTreemap`'s rendered legend covers every rendered tile colour; a pairwise
    Euclidean-RGB distance check over every distinct legend colour (including the row's own named
    Cash-vs-Fixed-Income pair, measured 170.4) confirms none are near-identical -- dynamic, never a
    hardcoded `Commodities` hex (that class is being changed concurrently on TO-IV-e-49).
  - UIR-46: the model-row colour set actually rendered (`CategoryTile`'s SegmentBar, real DOM) has
    zero intersection with the asset-class colour set the SAME component's breakdown dialog would
    draw its member dots from (`assetClassOf`/`ASSET_CLASS_COLOR`, the exact building blocks
    `DrillTree`'s own `breakdown.memberColor` closure calls -- the dialog's `open` state cannot be
    forced under SSR, the same instrument constraint `iv-e-42.drill-bases.test.tsx` documents for
    this component tree).

## Verification

- `bun test iv-e-43.one-colour.test.tsx`: 1 pass, VERDICT: ONE-COLOUR-OK (twice, identical; once
  against a mutant reverting `ASSET_CLASS_COLOR.Equity` back to the colliding `blue500`, correctly
  FAILED on exactly the UIR-37 and UIR-46 arms, then restored -- `git diff --stat` clean afterward).
- `bun run typecheck`: clean (0 errors). `bun run lint`: 0 errors, 192 pre-existing warnings
  elsewhere, none in the 5 files this cell touched.
- No-regression sweep (`dsgn-irptv1/`, `fe-s-7/`, `fe-s-76/`, `fe-s-67/`): 150 pass, 1 fail -- the
  one failure is `iv-e-12.unclassified.test.ts`'s IVE12-AC3, a DIFFERENT cell's pre-existing
  acceptance test that pins `HoldingsTreemap`'s Equity leaf colour to the shared
  `lib/chartColors.ts` `ASSET_CLASS.equity` hex; this cell's own fix necessarily moves that colour
  page-locally to avoid the model collision, so the two cells' criteria are now in genuine tension.
  That test file is outside this cell's `<paths>` grant and was left untouched; filed as surprise
  row `DSGN_IRPTV1-W29-S1` (ARMED, owner `2.0.0_SA_COO~D`) for CTO/CVO disposition.

## Declared exclusions

- Forcing `CategoryViewTree`'s breakdown dialog into its `open` state to read a real rendered DOM
  for UIR-46's mixed-population check: not possible under `renderToStaticMarkup` (no effects, no
  client JS); proven instead against the exact pure functions (`modelRowColorMap`,
  `assetClassOf`/`ASSET_CLASS_COLOR`) the dialog's own `rowColor`/`breakdown.memberColor` props read
  from, per the task order's own instruction that a row a render cannot decide is asserted on the
  markup contract that produces it.
