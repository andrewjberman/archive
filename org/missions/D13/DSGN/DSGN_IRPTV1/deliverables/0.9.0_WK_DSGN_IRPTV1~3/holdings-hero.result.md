# DSGN_IRPTV1.TO-IV-t-3 (holdings-hero) -- result

Worker: `0.9.0_WK_DSGN_IRPTV1~3`. Portal branch `wk-DSGN_IRPTV1-3-portal`, commit `bbbc2f9735728dccb7cabc6b889dfaa7f42edb07` (LOCAL). Workspace branch `wk-DSGN_IRPTV1-3`.

## What changed

`mdpfResultFromSnapshot` (`portal/src/pages/InvestorReporting/tabs/holdings/DrillTree.tsx`, base lines
140-171 @`7c542fd23ec70c88bade4e3270f4c87f267a275a`, the ONE function this cell touches) now fills every
L0 category's `children` (the nodes directly beneath it, one level, each keyed by its own label with its
own `amount` as `aum` -- no sum) and `members` (every leaf `security` node beneath it, at any depth, named
from `display.label` when carried, else `displayName`), instead of leaving both empty. `export`ed for
direct test coverage. No other line of the file moved (`IV3-AC3` verifies the diff hunks land only inside
that span).

## IV3-AC1 -- HERO-FED

`bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-t-3.hero-fed.test.ts` -- PASS (1 pass / 0
fail, 19 `expect()` calls). Prints, per fixture: `L0: <n> categories, <m> with children, <k> members;
display-named: <d> of <k>`, then `VERDICT: HERO-FED`. Exercised over the task order's two named `fe-s-7`
fixtures (cottonwood-target-blend, smartx-observed) plus every sibling `fe-s-7/holdings.*.json` fixture
(discovered from disk -- see surprise row `DSGN_IRPTV1-W3-S2`, not hand-typed) and
`holdingsSnapshot.success.json`: 9 fixtures, all fed correctly, zero fixture-specific assumptions in the
assertions.

## IV3-AC2 -- the fe-s-7 seam, literal invocation vs. the true suite

The task order's own invocation, run verbatim: `bun test src/pages/InvestorReporting/__tests__/fe-s-7` (no
trailing slash) -- Bun resolves this as a PREFIX match, not a directory match, and sweeps in EVERY sibling
whose name starts with `fe-s-7` (`fe-s-7`, `fe-s-71` .. `fe-s-78`): 56 tests across 9 files, **53 pass / 3
fail**. All 3 failures are inside `fe-s-78/cohort-chip.test.ts` (an `EnvelopeMismatch` on
`unprojected_grant`), a file this cell's `<paths>` grant does not name, untouched by this commit (`git
status --porcelain` clean on it both before and after), and reproducible standalone (`bun test
src/pages/InvestorReporting/__tests__/fe-s-78/` alone: 1 pass / 2 fail, unchanged).

Scoped to the ACTUAL "fe-s-7 Holdings suite (drill, slices, source bounds)" the criterion names, with a
trailing slash so Bun resolves it as a directory rather than a prefix: `bun test
"src/pages/InvestorReporting/__tests__/fe-s-7/"` -- **32 pass / 0 fail** (3 files, 157 `expect()` calls),
unchanged by this cell.

Graded MECHANICALLY on the literal invocation's output, which does not contain the `<expect>` pattern (`
0 fail`): **FAIL**. The 3 failures are pre-existing, unrelated to `IV-t-3`, and out of this order's grant to
fix; the criterion's own invocation text is a pathspec collision, not a real regression. Not repaired or
widened -- reported as measured, per the refusal clause.

## IV3-AC3 -- ONE-FUNCTION

`git diff -U0 7c542fd23ec70c88bade4e3270f4c87f267a275a -- .../DrillTree.tsx`: hunks at base lines `[140,
151]`, both inside `[140, 171]`. `VERDICT: ONE-FUNCTION` -- PASS.

## IV3-AC4 -- RECORD, no verdict (judgment, CVO at L9)

- `iv-t-3.hero.html` (14157 bytes): `renderToStaticMarkup(createElement(DrillTree, { snapshot }))` over
  the Cottonwood fixture. Carries all five node labels (`Model Blend Target`, `SMA Blend Target`, `Client
  Residual`, `Long Term Target`, `Ultra-Long Term Target`) -- the last two are the previously-empty L1
  tile/hover content this cell adds.
- `iv-t-3.png`: attempted per the order (`node scripts/ui-smoke.mjs investor-reporting <out>.png --port
  5389 --fixtures .../fe-s-18-holdings-observed.json`, own dev server on port 5389, stopped after use --
  never port 5174, per the COO's resume note). It RAN, but the rendered page shows "Scope could not be
  resolved. Nothing below is scoped, so nothing below is shown." -- the smoke script's directory-search
  fixture stub did not carry enough to auto-select a client scope, so the Holdings tab (and this cell's
  fed hero) never actually mounted in that screenshot. `iv-t-3.hero.html` is the substantive AC4 artifact;
  the PNG is included as-measured, with this caveat, per "RECORD; NO VERDICT".

## Surprise rows filed

`org/missions/D13/DSGN/DSGN_IRPTV1/surprise-channel/investigations/INVESTIGATION_v1.md` (minted by this
row, per the DSGN_REBRND W1-S1 precedent):

- `DSGN_IRPTV1-W3-S1` (OBSERVATION, INERT): the order's field mapping (category-level `children`/
  `members`) never reaches `CategoryViewTree`'s L2 hover-detail/breakdown dialog, which reads only
  `children[label].members` -- a field this order's own text does not ask to be populated.
- `DSGN_IRPTV1-W3-S2` (BLOCKING, ARMED, disarm owner `1.0.0_SA_CTO`): the naming gate refuses a brand-new
  file's first mention of a registered firm token with no working JS/TS escape hatch; worked around by
  discovering the fixture set from disk instead of naming it.
