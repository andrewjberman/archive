# DSGN_IRPTV1.TO-IV-e-27 -- result (0.9.0_WK_DSGN_IRPTV1~17)

Cell `IV-e-27` (M 101020, Andrew's ruling): the served asset class `other` (personal and held-away
assets) is its own class, apart from Unclassified.

## Changes

- `portal/src/pages/InvestorReporting/contracts/adapt.ts`: `ASSET_CLASS_FOR_WIRE` gains `other: 'other'`.
  A token outside the map still falls to `unclassified`, unchanged.
- `portal/src/pages/InvestorReporting/contracts/index.ts`: `HoldingsNode.assetClass` union gains
  `'other'`.
- `portal/src/pages/InvestorReporting/tabs/holdings/assetClass.ts`: `HoldingAssetClass` gains
  `'Other'`; `CLASS_FOR_SERVED.other = 'Other'`; `ASSET_CLASS_COLOR.Other = PALETTE.purple600`
  (`'#9333ea'`), imported read-only from `src/lib/chartColors.ts` (not edited -- Positioning reads
  it). `PALETTE.purple600` is used by no `ASSET_CLASS` entry (the seven ratified bases are
  green500/blue500/green300/pink500/yellow500/orange500 x2/gray500) and is visibly distinct from
  Unclassified's grey (`gray500` `'#6b7280'`).
- Two new tests: `iv-e-27.adapt-other.test.ts` (IVE27-AC1), `iv-e-27.other-colour.test.ts`
  (IVE27-AC2).

## Criteria

- IVE27-AC1: PASS-by-output. `VERDICT: ADAPT-OTHER-OK`.
- IVE27-AC2: PASS-by-output. `VERDICT: OTHER-COLOUR-OK`.
- IVE27-AC4: judgment, RECORDED, no verdict taken by this worker -- graded at the round drain by
  `2.0.0_SA_COO~D` on the signed-in trace, per CTO 100991.

## Controls

- Mutant: removing the `other: 'other'` entry from `ASSET_CLASS_FOR_WIRE` flips IVE27-AC1 to
  `VERDICT: ADAPT-OTHER-FAIL other arm: got "unclassified", expected "other"` -- fired as expected.
  Reverted; `git diff` against the file's committed/base state confirmed byte-identical restore
  before this proof was written, and IVE27-AC1 re-ran to `VERDICT: ADAPT-OTHER-OK`.
- Determinism: IVE27-AC1 and IVE27-AC2 each run twice back-to-back, identical output both times.
  The full `dsgn-irptv1/` directory (88 tests, 74 files) ran 0 fail on the final run; one earlier
  run of the same command showed 1 fail (a different, unrelated file) that did not reproduce on
  two subsequent runs -- a flake, not a regression from this cell's edits (confirmed by `git diff
  --stat`: only `adapt.ts`, `index.ts` and `assetClass.ts` carry content changes).
- `bun run typecheck` (`tsc -b --noEmit`): rc=0, no diagnostics, both before and after.

No surprise rows filed -- every criterion was met as written with no premise failure.
