# DSGN_IRPTV1.TO-IV-e-12 -- cash is green (Positioning too); unclassified says so -- result

**Cell:** IV-e-12 | **Worker:** 0.9.0_WK_DSGN_IRPTV1~8 | **Base:** portal a6cf99f2 (post IV-e-11), workspace 7b1bf213

## What changed

`portal/src/lib/chartColors.ts`:
- `ASSET_CLASS.cash` moved from `PALETTE.amber500` (`#f59e0b`) to `PALETTE.green300` (`#86efac`) --
  a lighter tint step on the SAME green hue ramp as `fixedIncome` (`green500`, `#10b981`), so a
  cash tile reads as fixed-income's family while staying visibly its own step. Comment names the
  token and the reason at the definition site.
- `getAssetClassTextColor`'s `lightBackgrounds` list and its measured-contrast doc comment updated
  from `amber500` to `green300` for the Cash row (white 1.404:1, gray900 12.634:1 -- computed and
  printed in the source comment), so the dark-text invariant over an ASSET_CLASS background still
  holds for Cash's new colour.

No other file needed an edit: `portal/src/pages/InvestorReporting/tabs/holdings/assetClass.ts` and
`HoldingsTreemap.tsx` already implement part (b) as of commit 13b5356f -- `assetClassOf` already
returns the literal `'Unclassified'` for a security with no served `assetClass` member or one
served `'unclassified'`, and `ASSET_CLASS_COLOR.Unclassified` already resolves to `ASSET_CLASS.other`
(gray500), never a borrowed class colour. `Positioning/tabs/HoldingsTab.tsx`'s own
`ASSET_CLASS_COLORS` map is built directly off the shared `ASSET_CLASS` registry
(`ASSET_CLASS.cash` at HoldingsTab.tsx:171), so the colour change reaches Positioning without a
Positioning-side edit -- confirmed by IVE12-AC2 by mirroring that exact map and diffing base vs now.

## Criteria

- **IVE12-AC1** (`iv-e-12.cash-green.test.ts`): cash is a green hue (independent hex->HSL check,
  band 80-160deg; cash lands at 141.7deg vs fixedIncome's 160.1deg), distinct from fixedIncome's
  hex, and every OTHER `ASSET_CLASS` key is pinned to its base-commit hex. PASS.
- **IVE12-AC2** (`iv-e-12.positioning-reader.test.ts`): Positioning's own colour map (mirrored
  verbatim from HoldingsTab.tsx:161-171, that file out of grant/never edited) diffed base
  (13b5356f) vs now over all 6 keys -- exactly `{Cash}` changed. PASS.
- **IVE12-AC3** (`iv-e-12.unclassified.test.ts`): a security with no `assetClass` member and one
  served `'unclassified'` both resolve, via `treemapLeavesFrom`, to `assetClass: 'Unclassified'`
  and `color: ASSET_CLASS.other`, never any of the six classified bases -- checked at the data
  layer (which both the legend and `TreemapHoverTooltip` render verbatim) AND against the
  `HoldingsTreemap` component's own server-rendered legend markup (`renderToStaticMarkup`, no
  browser/DOM), which shows the literal word "Unclassified" with a `#6b7280` swatch. A classified
  equity control rides along and correctly keeps its own blue -- the negative arm is real. PASS.
- **IVE12-AC4**: judgment, recorded, not self-graded.

## Controls

- **Mutant** (AC1/AC2): `ASSET_CLASS.cash` reverted in-worktree ONLY to `PALETTE.amber500`.
  AC1 failed (`ASSET_CLASS.cash did not move off its base amber`; `hue 37.7 is outside the green
  band 80-160`). AC2 failed (`expected the ONLY changed key to be "Cash", got []`; `Cash did not
  move off its base value`). File restored; `git diff --stat -- src/lib/chartColors.ts` reported
  the same 1 file / 11 insertions / 6 deletions as before the mutant, and the full suite + typecheck
  re-ran clean before this proof was written.
- **Regression**: full `__tests__/dsgn-irptv1/` suite, 42 pass / 0 fail / 247 expect() calls across
  28 files (up from 39/39/244/25 at the IV-e-11 base -- the 3 new files this cell adds). `bun run
  typecheck` (`tsc -b --noEmit`) rc=0, 0 diagnostics.

## Declared exclusion

`Positioning/tabs/HoldingsTab.tsx` line ~168's comment ("it keeps its own amber so a cash row is
distinguishable...") is now stale prose describing a colour this cell moved off amber. That file is
named a reference page in BOUNDS ("read and copied from, never edited") and is out of this cell's
`<paths>` grant; the comment's staleness is a foreseeable, on-task consequence of the ratified
colour change (Andrew's call C1) that this task order names, not an unexpected mismatch between
spec and world -- no surprise row filed for it.
