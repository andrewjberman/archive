# DSGN_IRPTV1.TO-IV-e-31 -- model-colour-code-only -- result

CTO round-4 analysis section 3 item 2 (FWD-12 remainder): `DrillTree.tsx#modelSliceColor` fell back to
`colorForSlice(label)` (a name-hash guess) whenever a MODEL node's served `modelCode` didn't resolve --
the same class of bug IV-e-11 already fixed for a MODEL carrying a code (a misleading label could still
repaint an unresolved model with a wrong colour). `AllocationBars.tsx#categoryBarColor` already took
`ASSET_CLASS.other` in that case; this cell brings the drill donut's `drillSliceColor` to the same rule
for MODEL nodes specifically.

## Change

`portal/src/pages/InvestorReporting/tabs/holdings/DrillTree.tsx#drillSliceColor` gained one new branch,
checked before the generic dispatch: a `kind === 'model'` node's colour is
`colorForServedModelCode(node.modelCode) ?? ASSET_CLASS.other` (`ASSET_CLASS` imported from
`@/lib/chartColors`, READ ONLY) -- never `colorForSlice`/`modelSliceColor`'s label path. Sleeve, account
and cash rows are untouched: they still fall through to `modelSliceColor(node?.modelCode, label)`
exactly as before (task order BOUNDS explicitly preserves their current colouring). Security rows are
untouched (IV-e-25 (c), pre-existing).

## Acceptance

- **IVE31-AC1** (`iv-e-31.code-only.test.ts`) -- PASS. Three arms against the real `holdingsSnapshot.
  success.json` fixture's model/security nodes: (1) difference control -- a model node served
  `opal_long_term_conservative` under the label "Opal Ultra Long Term" (a DIFFERENT canonical model)
  renders Long Term's colour, never Ultra-Long Term's and never the label-hash colour; (2) a model
  node with `modelCode: null` (and separately an unregistered code) under a TRUTHFUL label ("Opal
  Ultra Long Term", a real canonical model) renders `ASSET_CLASS.other` (`#6b7280`), never the label's
  own colour; (3) a security node keeps its served asset-class colour, unaffected. `VERDICT:
  MODEL-CODE-ONLY-OK`.
- **IVE31-AC2** (`iv-e-31.no-label-path.test.ts`) -- PASS. A disk scan of every `getModelColor(`
  occurrence under `tabs/holdings/{DrillTree,AllocationBars,SecurityList}.tsx` (denominator: 3 found)
  classifies each by whether its argument is fed by `canonicalModelCode(...)` of a served code:
  `colorForServedModelCode` and `categoryBarColor` are code-fed (the two functions that colour a MODEL
  node); the one remaining label-fed occurrence (`colorForSlice`, reached only by the retained
  sleeve/account/cash path per this cell's own BOUNDS) is proven structurally unreachable from a MODEL
  node by reading `drillSliceColor`'s own `kind === 'model'` branch as bytes (calls
  `colorForServedModelCode`/`ASSET_CLASS.other` only). `VERDICT: NO-LABEL-PATH-OK`.
- **IVE31-AC3** -- judgment=true. RECORDED, no verdict taken by this worker; graded by
  `2.0.0_SA_COO~D` at the round-5 drain (the signed-in admin + Dev walk).

## Controls

- **Mutant:** removed the new `if (node && node.kind === 'model') return colorForServedModelCode(...)
  ?? ASSET_CLASS.other` branch from `drillSliceColor` (in-worktree only, never staged). AC1 failed as
  expected (arm2/arm2b: a model with no resolvable code resolved the TRUTHFUL label's own colour
  `#ef4444` instead of `ASSET_CLASS.other` `#6b7280`); AC2 failed as expected (the structural byte-read
  found no `kind === 'model'` branch to prove the bypass). Reverted; `git diff --stat` showed zero diff
  against the committed state; both tests re-ran to their OK verdicts, twice, with identical console
  output each time.
- **Determinism:** both tests run together, twice, post-revert -- identical `VERDICT:
  MODEL-CODE-ONLY-OK` / `VERDICT: NO-LABEL-PATH-OK` and 2 pass / 0 fail / 2 expect() calls both times.
  `bun x tsc -b --noEmit` rc=0 (0 diagnostics) before and after all edits. The full
  `__tests__/dsgn-irptv1/` directory (76 files) ran 90 pass / 0 fail both before and after this cell's
  edit (one earlier run in that directory showed a transient 1-fail that did not reproduce on any
  subsequent run and is unrelated to this cell's two new files, which never failed across ~6 runs).

## Declared exclusions

- Editing `contracts/**`/`api/**` -- not needed; no wire/contract shape changed (`HoldingsNode.
  modelCode` already existed and is read-only here).
- Touching `src/lib/**` -- read only (`chartColors.ts`, `modelPortfolioColors.ts`), per BOUNDS.
- Starting a dev server / exercising `localhost:5174` -- reserved to `2.0.0_SA_COO~D`'s drain
  (IVE31-AC3); the environment note also says do not start any server.
- Push, merge, rebase, `checkout --` or `clean` of either repository -- forbidden by BOUNDS. All
  commits are LOCAL on `wk-DSGN_IRPTV1-21` (workspace) and `wk-DSGN_IRPTV1-21-portal` (portal).

No surprises filed -- every premise in the WORKER FACE held against live state: `DrillTree.tsx`'s
`modelSliceColor`/`colorForSlice` sat exactly at the cited lines (~:241/~:277 in the base; ~:241/~:279
in this worktree after IV-e-25's own edits shifted them slightly, immaterial to the fix), and
`AllocationBars.tsx#categoryBarColor` (~:170) already took `ASSET_CLASS.other`, confirmed by reading it
before writing any code.
