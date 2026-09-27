# DSGN_IRPTV1.TO-IV-e-51.commodities-chromatic -- result

Worker: 0.9.0_WK_DSGN_IRPTV1~30. Portal HEAD: c506381e (wk-DSGN_IRPTV1-30-portal). Workspace HEAD: 1ad23c7b36 (wk-DSGN_IRPTV1-30).

## What changed

CTO 101681 (on IV-e-49's pick) ruled `PALETTE.gray900` OUT for `ASSET_CLASS.commodities`/`MIX_PIE.commodities`:
`getAssetClassTextColor` uses gray900 as its dark-text ink, so a gray900 class colour is one hue with two
meanings (UIR-37, O7). The replacement is mechanical: the PALETTE token with the LARGEST minimum CIEDE2000
(dE00) against every MIX_PIE colour, every ASSET_CLASS colour and every model primary (canonical + the 6
EXTENDED_MODEL_COLORS, discovered via `getModelColor`'s 60-probe census), subject to (1) chromatic, (2) no
text/ink role, (3) minimum dE00 >= 20, preferring the amber/gold family (amber*/orange*) if any member
clears 20.

Census result (`iv-e-51.commodities-chromatic.test.ts`, run against the real `PALETTE`/`MIX_PIE`/
`ASSET_CLASS`/`MODEL_PORTFOLIO_COLORS`/`getModelColor`):
- No amber/gold-family token clears 20 (amber400=10.57, amber600=7.92, orange400=7.67, orange600=7.54,
  yellow500=9.89 -- all measured, none printed as a CANDIDATE).
- 6 chromatic, non-ink PALETTE tokens clear 20: blue900 (20.8323), green700 (21.7122), pink800 (22.1808),
  green800 (27.0491), blue950 (27.8465), **green900 (28.1954)**.
- Winner: `PALETTE.green900` (`#064e3b`), minimum dE00 = 28.1954 against `MIX_PIE.other`/`ASSET_CLASS.other`
  (`#6b7280`). White text on it measures 9.719:1 (>= 4.5:1; `getAssetClassTextColor`'s existing else-branch
  default, unchanged code).

`chartColors.ts`: `ASSET_CLASS.commodities` and `MIX_PIE.commodities` both moved from `PALETTE.gray900` to
`PALETTE.green900`; no other existing colour value changed. Comments at both sites rewritten to record the
CTO 101681 ruling and the new measured minimum.

`iv-e-46.class-readers.test.ts` and `iv-e-49.commodities-distance.test.ts`: both already assert
`dE00(...) >= 20` by reading `MIX_PIE.commodities`/`ASSET_CLASS.commodities` dynamically off the live
module (no hard-coded gray900 hex or value anywhere in either file, confirmed by search) -- both continue to
pass unmodified against the new green900 value; the cell's "update them to the rule" directive is satisfied
by the value change alone, since neither test ever hard-coded the old colour.

## Acceptance

- **IVE51-AC1** PASS-by-output. `VERDICT: COMMODITIES-CHROMATIC-OK`, 2 pass / 0 fail. Control arm confirmed:
  gray900 excluded by BOTH rule 1 (name-family match) and rule 2 (its hex is a real, dynamically-discovered
  output of `getAssetClassTextColor`/`getSubAssetTextColor`).
- **IVE51-AC2** PASS-by-output, with a denominator caveat (filed as surprise row W30-S3): the invocation
  names 5 test files; only 4 exist on this slot's portal branch (`iv-e-48.new-classes.test.tsx` belongs to a
  sibling worker's cell not yet merged into this build line). `bun test` silently runs the 4 that exist --
  rc=0, "8 pass / 0 fail", "Ran 8 tests across 4 files" -- so the literal "0 fail" expectation holds, but
  this worker's own change was never exercised against IV-e-48's readers.

## Surprises filed

- `DSGN_IRPTV1-W30-S3`: IVE51-AC2 names a test file absent from this slot's portal worktree (IV-e-48, not yet
  merged into this build line). Not blocking; recommend the drain re-run IVE51-AC2 post-merge.
- `DSGN_IRPTV1-W30-S4`: the mechanical winner `PALETTE.green900` is already used elsewhere in the portal
  (`Attribution/constants/holdings-shared.tsx`'s `'Hedge'` sub-asset colour) -- a reuse the cell's own
  3-condition population (MIX_PIE/ASSET_CLASS/model primaries only) does not check. Not blocking; followed
  the CTO's literal rule mechanically rather than widening it with an added exclusion of my own.
