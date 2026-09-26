# DSGN_IRPTV1.TO-IV-e-44 -- securities map (UIR-41/42/43) -- result

**Worker:** 0.9.0_WK_DSGN_IRPTV1~28 | **Portal commit:** `80763061cbe880a17f022119b6d7dc4b0cf3a928` on `wk-DSGN_IRPTV1-28-portal` (LOCAL)

## What changed

`portal/src/pages/InvestorReporting/tabs/holdings/HoldingsTreemap.tsx`:

- **UIR-41.** The model-filter chip nav (`treemap-model-filter-option`) now renders `Model: <label>`
  for each de-duplicated model option (unchanged: `modelOptionsFrom` already de-duplicated by
  model), and carries a new `data-chip-kind="model"` / `data-chip-kind="all"` attribute. "All
  securities" is unchanged text (already self-describing).
- **UIR-42.** `treemapLeavesFrom`'s last step is the new exported `groupSmallIntoOther`: below
  `SMALL_TILE_SHARE_THRESHOLD` (2%) of the displayed set's own total weight, and only when at
  least two such leaves exist, every leaf that small rolls into one tile (`nodeRef:
  OTHER_TILE_NODE_REF`, `tileText: "Other"`, summed weight/amount), coloured
  `ASSET_CLASS_COLOR.Other` (the existing miscellaneous-bucket colour -- `assetClass.ts` itself is
  untouched, per this cell's own BOUNDS note). A lone below-threshold leaf is left alone (grouping
  one leaf for no reduction in tile count would only rename it).
- **UIR-43.** `treemapLeavesFrom` now groups its filtered node set by security identity
  (`securityId`, falling back to the node's own `nodeRef` when a producer serves no `securityId`,
  so an identity-less security never merges with another) before building each leaf: amount and
  weight SUM across the group; a security held in two models resolves to ONE tile with the total.
  Narrowing to one model (the existing chip nav) filters BEFORE this grouping, so the model's own
  instance -- the split -- is one click away, never the cross-model sum.

`portal/src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-44.securities-map.test.tsx` (new):
one test, one shared `failures` array, three named-arm check functions (`checkUir41`/`checkUir42`/
`checkUir43`), synthetic in-memory `HoldingsSnapshot` fixtures per arm (the `iv-e-12`/`iv-e-13`
technique -- no real fixture on disk carries a duplicate security across models or several
sub-threshold securities). Prints `VERDICT: SECURITIES-MAP-OK` only when every arm holds.

## Why no real fixture was used for two of the three arms

`fixtures/holdingsSnapshot.success.json` and every file in `fixtures/fe-s-7/` carry at most 4
securities per snapshot, none sharing a `securityId`, and no leaf's own share of its snapshot's
total falls under 2%. Confirmed by direct inspection (bun script) before writing the test: neither
the aggregation path (UIR-43) nor the small-item grouping path (UIR-42) is ever exercised by any
committed fixture, so a synthetic in-memory snapshot -- exactly the technique
`iv-e-12.unclassified.test.ts` / `iv-e-13.map-drill.test.ts` already establish and cite for this
same reason -- is the only way to exercise either new code path. The chip fixture (UIR-41) is also
synthetic for the same reason (kept minimal, two models one security each, shares far above the
2% floor so UIR-42 does not interfere with the chip count).

## Regression

`iv-e-5.treemap.test.ts`, `iv-e-12.unclassified.test.ts`, `iv-e-13.map-drill.test.ts`,
`iv-e-20.tooltips.test.ts`, `iv-e-27.other-colour.test.ts`, `s6.names-and-tiles.test.ts` (every
test file importing `HoldingsTreemap`/`treemapLeavesFrom`/`modelOptionsFrom` besides this cell's
own new file) all re-run unchanged and pass (14 pass / 0 fail combined with this cell's own file,
38 expect() calls). `bun run typecheck` (`tsc -b --noEmit`): rc=0, 0 diagnostics.

## Judgment criterion

IVE44-AC2 is `judgment="true"`, graded at L9 by `3.0.0_SA_CVO` on the issuer's live walk of portal
DEV after the drain (PRD v0.15). Not self-graded; RECORDED only.
