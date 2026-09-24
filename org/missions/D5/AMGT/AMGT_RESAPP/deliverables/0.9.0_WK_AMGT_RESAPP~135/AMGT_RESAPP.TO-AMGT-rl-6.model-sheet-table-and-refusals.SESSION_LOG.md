# Session log -- `0.9.0_WK_AMGT_RESAPP~135` on `AMGT-rl-6`

Worktree: `C:/tmp/wk-amgt-37-135` (`/c/tmp/wk-amgt-37-135`), branch `wk-AMGT_RESAPP-135-portal` inside
`portal` (portal_ref 513bb3c5 at spawn).

## What changed

`portal/src/pages/SecurityAnalysis/tabs/ModelTab.tsx` (rewritten) and a new
`portal/src/pages/SecurityAnalysis/__harness__/modelPattern.harness.cjs`. `modelSheet.ts` was
inspected but NOT edited -- it already read `idiom=0 size=0 weight=0 radius=0 shadow=0` and its
computed shape (rows, years, absence, dedup, estimate-years) is exactly what this cell presents
differently, never recomputes (BOUNDS clause 2).

The whole tab is now ONE `Panel variant="heatmap"` (white surface). `IdentityLine` needs a dark
ground per its own docstring ("Dark-container-only, white idiom: rendered inside `Panel
variant="mixed"`"); `PanelHeader`'s own component always renders a dark bar
(`bg-[hsl(var(--bg-header))]`) regardless of the Panel's `variant` (confirmed by reading
`PanelHeader.tsx` and the precedent in `CommoditiesTab`/`EquitiesTab`, which use
`variant="heatmap"` with a dark header too), so IdentityLine now renders there via
`leftActions`, never on the white content surface.

A row with any REFUSE-verdict cell (this fixture: the DPS/`IS_DIV_PER_SHR` row, 10 of 10 years
REFUSED, one reason repeated) collapses to ONE `<td colSpan>` cell carrying a `status.danger`
icon (`lucide-react`'s `AlertCircle`, the same idiom `PanelStates.tsx`'s `PanelError` uses) and
ONE navy sentence built from the check-face reason(s), byte-identical to the payload's text.
Per-figure `data-model-cell` markers still render (as `sr-only` spans, no visible content) so
`tabs.harness.cjs`'s existing `model_fiscal_rows_rendered` check -- which counts
`data-model-cell` occurrences against the fixture's own fiscal-figure count -- keeps reading
true without being told about this cell's redesign.

Absent rows (rows whose EVERY year cell is null -- 5 of 24 for BA_US_Equity: Revenue/Sh, FCF
yield, FCF margin, RoTA, Earnings margin) are no longer rendered as a colSpan "ABSENT -- reason"
row each; they are omitted from the table body and named once in a footnote
(`data-model-absent-footnote`).

Three score tiles (Robustness, Peers V, Divergence D) render above the table, built local to
this file (`ScoreTile`/`ScoreTiles`) since `src/ui/components/Stat.tsx` is a dark idiom. A
missing/unread field shows "not read" (verified on a second render with `scores` forced to an
explicit read-failed shape, not just this fixture's natural `scores: null`).

A once-only navy-outline "machine" chip (`data-model-marker="machine"`) sits above the table --
the codebase's own established marker for a machine-derived surface (`PostureTab`/`LeadPanel`
already carry the identical word for the identical reason).

## A surprise, not a blocker

`@/ui/components/states` (`PanelEmpty`/`PanelLoading`/`PanelError`) is listed as a read-only
input (`src/ui/components/states/index.ts` in `<paths>`), and the target text calls for the four
C12 designed states. The round's shared `tabs.harness.cjs` (also read-only, also in `<paths>`)
stubs `@/ui/components/panels` but carries NO stub for `@/ui/components/states` -- importing it
from `ModelTab.tsx` makes `tabs.harness.cjs` throw `MODULE_NOT_FOUND` at module-load time (tried
and reverted; confirmed by direct run). Since `tabs.harness.cjs` is not this cell's file to edit,
the four states are built LOCAL to `ModelTab.tsx` (`ModelEmptyState`/`ModelLoadingState`/
`ModelErrorState`) carrying the same contract (navy ink on white, one `status.danger` icon on
ERROR, a `data-panel-state` hook) rather than importing the shared components. Filed as row
`AMGT_RESAPP-W135-S1`.

## Instrument work

Wrote `modelPattern.harness.cjs`: loads the ACTUAL `ModelTab`/`modelSheet`/`figureIdentity`/
`refusalPresentation`, and the ACTUAL `Panel` component (transpiled real source, not a stub) so
`panel_is_heatmap` is the component's own class decision; `PanelHeader`/`PanelContent` are
stubbed to forward only `children` (their internals are not this cell's claim).
`@/lib/utils`'s `cn` is a plain join, matching `tabs.harness.cjs`'s own stub.

Every expected count is derived from `tabsFixture.BA_US_Equity.json`'s `thesis` bundle through
the REAL `buildModelSheet`/`checkFor`/`displayValue`, never typed by hand: 10 years, 24 total
rows (19 visible, 5 absent), 1 refused row (DPS, 10 of 10 years), 165 fiscal figures, 58 negative
PASS-verdict figures.

12 of 12 CHECK lines PASS on the first run (`CHECKS-OK 12 of 12`, exit 0).

## Mutant + determinism controls

Mutant: `{refusal.refused ? (...` changed to `{false && refusal.refused ? (...` (row-collapse
forced off), same invocation re-run. 4 of 12 checks flipped WRONG-WAY as expected
(`negative_values_signed`, `refused_rows`, `refusal_sentences`, `refusal_chips` -- the DPS row's
10 REFUSE-verdict cells now render through `ModelCell`/`CheckFaceBadge` again, producing 10
chips and pushing the numeral-text array to 165 entries against an expectation of 155). File
reverted from `.scratch/ModelTab.tsx.bak` (byte-identical `diff -q`, silent = match), re-run
confirmed `CHECKS-OK 12 of 12` again. `.scratch/ModelTab.tsx.bak` and the two run logs are
worktree-local scratch, not committed.

Determinism: two consecutive runs of the unmutated harness, `diff` on stdout: identical.

## AC2/AC3, unaffected by this cell beyond the intended file

`ui-class-census.mjs` over `ModelTab.tsx` + `modelSheet.ts`: `FILES 2 TOTAL 0` (was `idiom=17
size=5 weight=1 total=23` on `ModelTab.tsx` alone before this cell; `modelSheet.ts` was already
`total=0`).

`tabs.harness.cjs` (unmodified, run as-is): `model_fiscal_rows_rendered` reads `true` (5 of 5,
`BA_US_Equity:165/165 SAP_GY_Equity:190/190 BABA_US_Equity:183/183`), byte-identical to the
pre-cell baseline measured before any edit. Only `exec_officers_rendered` reads
`CHECKS-WRONG-WAY`, which is pre-existing (measured at HEAD before this cell touched anything)
and belongs to another cell's `<paths>`, per AC3's own instruction to report it AS-IS.

`tsc --noEmit -p tsconfig.json` from the portal root: 0 errors, exit 0.

## Commits

Portal (nested repo, branch `wk-AMGT_RESAPP-135-portal`): `423dc7bb` -- `ModelTab.tsx` rewritten,
`__harness__/modelPattern.harness.cjs` added.

Outer worktree commit (gitlink + deliverables + proof instance): see the WORKER REPORT.
