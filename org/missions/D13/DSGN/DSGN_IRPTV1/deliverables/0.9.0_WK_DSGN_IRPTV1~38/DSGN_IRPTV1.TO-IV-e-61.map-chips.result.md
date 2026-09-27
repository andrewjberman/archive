# DSGN_IRPTV1.TO-IV-e-61.map-chips -- session log (0.9.0_WK_DSGN_IRPTV1~38)

## What was wrong (window 9 + Andrew's UI review)

`modelOptionsFrom`'s chooser de-duplicated by the model ANCESTOR's own node id. A model held
under several sleeves of one account is several distinct NODES sharing one label, so the same
model repeated as several chips ("Model: Opal Long Term" x3, "Model: Opal Ultra Long Term" x2).

Amendment 1 (UIW-0927-07): the grouped small-items tile ("Other") shared its word AND its
`ASSET_CLASS_COLOR.Other` purple fill with the genuinely `other`-classified asset class.

Amendment 2 (UIR-33/36/47, carried from IV-e-60 -- the CVO FAILed IV-e-60's own UIR-33 arm
because it only re-asserted the existing "% of total"/"% of parent" strings, which name no base
a client reads): every percentage the holdings drill shows needed to state its base in client
words instead.

## Fix

- **Chips (window 9).** `HoldingsTreemap.tsx`'s new `accountGroupsFrom` groups the map's own
  leaves by nearest `account` ancestor (first-seen order; a leaf with none falls into one
  implicit, unheaded group -- every existing fixture with no account layer). WITHIN one group,
  chips are de-duplicated by model IDENTITY (`modelCode` when served, else the label) rather
  than the model ancestor's own node id. Each `TreemapModelOption` now carries `nodeRefs`, the
  SET of every node instance sharing that identity; `treemapLeavesFrom`'s second argument
  accepts that set (or a bare single id, normalized, so every existing caller is unchanged).
  `modelOptionsFrom` is kept, flattened over every group, for IV-e-13(b)'s and IV-e-44's own
  no-account-layer fixtures. The render groups chips under an optional heading (the account's
  own masked label), omitted with only one group.
- **Amendment 1.** `OTHER_TILE_LABEL` = 'Smaller holdings' (was 'Other'); `OTHER_TILE_COLOR` =
  `PALETTE.slate400` (was `ASSET_CLASS_COLOR.Other`). The tile's internal `assetClass: 'Other'`
  field (legend bucketing) is unchanged -- out of this narrow build's own scope.
- **Amendment 2.** `DrillTree.tsx`'s new `pctBaseOf(nodes, currentRef)` walks the existing
  `breadcrumbPath`: 'client' at the top of the view or above the account layer, 'account' when
  the level sits under (or is) one. `SliceTable.tsx` gains an optional `pctBaseWords` prop (the
  header and row hover both use it when passed, else the OLD literal words); `DonutHoverTooltip`
  gains an optional `baseWords` prop and `renderInsideLabel` an optional second argument, both
  defaulted to the OLD literal so every direct call outside this file's own render (iv-e-42's own
  two UIR-47/UIR-33 unit checks) reads byte-for-byte what it always has. `iv-e-60.drill-bases.
  test.tsx`'s own UIR-33 arm is re-goldened to the new wording (both the account level and a new
  client-level control), per the amendment's own instruction.

## Test

New `iv-e-61.map-chips.test.tsx`, one VERDICT line gating:
- One model under 3 sleeves of one account -> exactly 1 chip, whose own node set covers all 3
  instances; choosing it filters to all 3 sleeves' own leaves.
- Two accounts holding the same model -> one chip in EACH group (its own masked heading); a
  CONTROL confirms a single-sleeve chip still filters to its own account's security alone.
- Amendment 1: the grouped tile's label is not literally 'Other' and its fill matches no
  `ASSET_CLASS_COLOR` entry.
- Amendment 2: account-level (SOLO_ACCOUNT_FULL) and client-level (BASE_SNAPSHOT's own top-level
  account list) header/hover read the new words and never the old ones; the donut tooltip and
  in-slice label are checked as direct-call units (recharts draws no SVG under
  `renderToStaticMarkup` without a real DOM -- the same instrument note `iv-e-13.map-drill.
  test.ts`/`iv-e-27.other-colour.test.ts` already accept).

## Controls

- **Mutant** (three, applied together): reverted the chip-identity dedup to the model node's own
  ref, `OTHER_TILE_COLOR` back to `ASSET_CLASS_COLOR.Other`, and `SliceTable`'s header/hover back
  to the hardcoded old literals. Re-ran IVE61-AC1 -- 14 failures pushed across all four arm
  groups. Restored (python edit); `git diff --stat f04c0c1e` before commit showed exactly the
  3 files' intended hunks, unchanged from the pre-mutant measurement. Re-ran clean: both
  `iv-e-61` and `iv-e-60` print their own VERDICT lines.
- **Determinism**: ran IVE61-AC1's exact invocation twice post-restore -- identical `VERDICT:
  MAP-CHIPS-OK`, 1 pass / 0 fail, 1 expect() call, both runs.

## No-regression sweep

- Full suite (`__tests__/`, no path filter): 829 pass, 27 skip, 8 fail, 864 tests across 239
  files. 2 of the 8 are THIS cell's own directed, sanctioned changes (see Surprises); the other
  6 are PRE-EXISTING and unrelated to this cell's grant (`fe-s-1/fixtures.test.ts` route-map
  coverage, `fe-s-1/source-bounds.test.ts` 'ycharts' forbidden token, `fe-s-25/absent-vs-
  null.test.ts` x2, `fe-s-45/residuals.test.ts` dev-script junction) -- confirmed by reading each
  failure's own text: none touch `tabs/holdings/{HoldingsTreemap,SliceTable,DrillTree}.tsx` or
  either drill-bases/map-chips test file.

## Compiler tools

- `bun run typecheck` (`tsc -b --noEmit`, full portal): 0 errors. (This cell's own new test file
  initially tripped TS2367 -- a literal-type comparison against the now-narrower
  `OTHER_TILE_LABEL` type; fixed by widening to a local `string` binding before comparing.)
- `bun run lint` (`eslint .`, full portal): 0 errors, 196 warnings (was 193 at f04c0c1e). The +3
  is exactly this cell's own new value-level exports co-located with components
  (`HoldingsTreemap.tsx`: `OTHER_TILE_COLOR`, `accountGroupsFrom`; `DrillTree.tsx`:
  `PCT_BASE_WORDS`, `pctBaseOf`) -- the same `react-refresh/only-export-components` pattern these
  files already carry in abundance (`DrillTree.tsx` itself carried 9 pre-existing instances at
  f04c0c1e, confirmed by lint-testing that exact blob directly; an earlier proof's "3
  pre-existing" text undercounted and is not reconciled here).

## Declared exclusion

AC2 (UIR-41 read on the running page) is judgment-graded by 3.0.0_SA_CVO at L9 per the task
order; this worker's grant does not include a live portal DEV walk, so AC2 is recorded
UNVERIFIABLE-BY-INSTRUMENT, never self-graded.

## Surprises

`DSGN_IRPTV1-W38-S1` filed: Amendment 1 and Amendment 2 each break ONE hardcoded assertion in a
regression test outside this cell's `<paths>` grant (`iv-e-44.securities-map.test.tsx`'s own
`other.color === ASSET_CLASS_COLOR.Other` check; `iv-e-42.drill-bases.test.tsx`'s own
UIR-33/36/47 block, reachable only through a real `DrillTree` render this build now changes
unconditionally). Unlike IV-e-60 (whose own task order explicitly granted edit access to
`iv-e-42.drill-bases.test.tsx` to reconcile its superseded control), THIS cell's `<paths>` names
only `iv-e-60.drill-bases.test.tsx` for re-goldening and no file at all for Amendment 1 -- so
these two breaks could not be fixed in-grant. Backward-compatible defaults were added everywhere
reachable to shrink the blast radius to exactly these two. Disposition UNDER_INVESTIGATION,
hazard_standing ARMED (a red CI signal if left), disarm owner named as a cell/drain act whose
grant covers those two files.
