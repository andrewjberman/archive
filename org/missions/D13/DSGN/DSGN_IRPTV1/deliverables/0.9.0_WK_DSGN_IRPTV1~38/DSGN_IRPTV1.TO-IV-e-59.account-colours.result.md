# DSGN_IRPTV1.TO-IV-e-59.account-colours -- session log (0.9.0_WK_DSGN_IRPTV1~38)

## What was wrong (w9c)

`DrillTree.tsx#drillSliceColor` sent every ACCOUNT-kind node to `modelSliceColor(node?.modelCode,
label)`. An account never carries a served `modelCode`, so it always took the label path
(`colorForSlice` -> `getModelColor`'s partial-match-then-hash), the same fallback used for an
unrelated model name -- three differently-named accounts could (and did) resolve to the same
model's colour (measured: teal `#14b8a6`, the 50/50 INT/LT model's canonical primary).

## Fix

- `palette.ts`: new `ACCOUNT_PALETTE`, 14 ordered, neutral (gray/slate/zinc/stone) hex entries.
  Checked against every `MODEL_PORTFOLIO_COLORS` primary and every `ASSET_CLASS`/`ASSET_CLASS_COLOR`
  entry -- no collision.
- `DrillTree.tsx`: `drillSliceColor` gains an optional `siblingIndex` (default 0). An ACCOUNT-kind
  node now resolves `ACCOUNT_PALETTE[siblingIndex % ACCOUNT_PALETTE.length]` -- never the label-hash
  fallback. Model and security branches are unchanged. The one call site (`donutData` useMemo) now
  passes each row's own index in the mapped array.

## Test

New `iv-e-59.slice-colours.test.ts`, four named arms, one VERDICT line:
- Arm 1: a 3-account level resolves 3 distinct colours.
- Arm 2: a 12-account level resolves 12 distinct colours.
- Arm 3: no `ACCOUNT_PALETTE` entry equals a model canonical primary or an `ASSET_CLASS`/
  `ASSET_CLASS_COLOR` entry.
- Arm 4 (control): a MODEL slice and a SECURITY slice resolve the SAME colour regardless of
  `siblingIndex` -- the fix is account-only.

## Controls

- **Mutant**: removed the ACCOUNT branch (so an account fell back through to `modelSliceColor` as
  before the fix), re-ran the exact AC1 invocation -- Arm 1 and Arm 2 both failed, reproducing the
  exact w9c defect shape (repeated colours across differently-named accounts, e.g. two accounts both
  landing on `#0ea5e9`). Restored `DrillTree.tsx` from the committed blob (`git show HEAD:<path> >
  <path>`); `git diff --stat` against HEAD printed nothing afterward (only a CRLF line-ending
  warning). Re-ran clean: `VERDICT: SLICE-COLOURS-OK`.
- **Determinism**: ran the exact AC1 invocation twice post-restore -- identical `VERDICT:
  SLICE-COLOURS-OK`, 1 pass / 0 fail, 1 expect() call, both runs.

## No-regression sweep

Ran the 13 other test files that import `DrillTree.tsx` or `palette.ts` (found via a bounded
`Grep`, not the full `dsgn-irptv1` directory, which times out under a 120s bound): 32 pass, 0 fail,
151 expect() calls. `iv-e-43.one-colour.test.tsx` (the nearest-neighbour colour cell) still prints
`VERDICT: ONE-COLOUR-OK` unchanged.

## Compiler tools

- `bun run typecheck` (`tsc -b --noEmit`, full portal): 0 errors.
- `bun run lint` (`eslint .`, full portal): 0 errors, 193 pre-existing warnings; the only warnings
  in `DrillTree.tsx` are three PRE-EXISTING `react-refresh/only-export-components` warnings on
  functions this cell did not touch (`renderInsideLabel`, `renderDrillLegend`, `modelSliceColor`);
  `palette.ts` and the new test file carry none.

## Declared exclusion

AC2 (UIR-25/46/37 read on the running page) is judgment-graded by 3.0.0_SA_CVO at L9 per the task
order; this worker's grant does not include a live portal DEV walk, so AC2 is recorded
UNVERIFIABLE-BY-INSTRUMENT, never self-graded.

## Surprises

None filed. No premise failed, no path was elsewhere, no capability was missing.
