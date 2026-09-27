# DSGN_IRPTV1.TO-IV-e-48 -- result (0.9.0_WK_DSGN_IRPTV1~31)

## What changed

Regenerated `portal/src/pages/InvestorReporting/contracts/wire/HoldingsSnapshot.ts` via the
existing `bun run src/pages/InvestorReporting/__tests__/fe-s-13/gen-wire.ts` generator (not
hand-edited); its `nodes[].asset_class` union now admits `structured` and `commodities`,
matching `docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json`'s node enum. A
full regeneration also touched the other 22 generated files, but `git diff --stat` confirmed
only `HoldingsSnapshot.ts` carries a real content diff (2 lines: the source sha256 comment and
the union); every other file's `M` status was CRLF/LF checkout noise (`git diff --ignore-space-at-eol`
shows 0 files), so only `HoldingsSnapshot.ts` was staged and committed.

Added `structured`/`commodities` to:
- `contracts/index.ts`'s `HoldingsNode.assetClass` union (:797);
- `contracts/adapt.ts`'s `ASSET_CLASS_FOR_WIRE` map (:983), carried verbatim (no rename, unlike
  `fixed_income` -> `fixedIncome`);
- `tabs/holdings/assetClass.ts`'s `CLASS_FOR_SERVED` map (:36-43) -- `HoldingAssetClass` and
  `ASSET_CLASS_COLOR` already carried `Structured`/`Commodities` with `ASSET_CLASS.structured`
  (pink500 `#ec4899`) / `ASSET_CLASS.commodities` (yellow500 `#eab308`), so no colour edit was
  needed. Verified (in the new test) distinct from every other `ASSET_CLASS_COLOR` entry and
  from every `MODEL_PORTFOLIO_COLORS` primary -- no collision, so no surprise row was needed
  for TO-IV-e-43's colour pass.

New test `__tests__/dsgn-irptv1/iv-e-48.new-classes.test.tsx`: a synthetic in-memory
`HoldingsSnapshotWire` (no real client figure, no firm token) proves three arms -- (1) the
regenerated wire union equals the contract's own enum, read from the schema at the same path
`gen-wire.ts#schemaFilePath` resolves; (2) a snapshot whose SECURITY nodes carry `structured`/
`commodities` adapts through `adaptHoldingsSnapshot` to those view classes and renders
"Structured"/"Commodities" in `HoldingsTreemap`'s legend with the correct, collision-free
swatch; (3) a control snapshot carrying only today's classes (`equity`, `cash`, `other`, and an
out-of-map token) adapts exactly as before, and its legend does not carry "Structured" or
"Commodities". Prints `VERDICT: NEW-CLASSES-OK`.

## Verification

- `bun test .../iv-e-48.new-classes.test.tsx` -> `VERDICT: NEW-CLASSES-OK`, 1 pass / 0 fail.
- `bun run typecheck` (`tsc -b --noEmit`) -> rc 0, 0 diagnostics.
- Full `__tests__/dsgn-irptv1/` regression -> 99 pass / 0 fail (490 expect() calls).
- `__tests__/fe-s-13/` regression (generator/content-pins/routes/etc.) -> 33 pass / 0 fail.

## Surprises

None filed. No colour collision was found (the arm that would have required one, per the task
order's own instruction, held clean).
