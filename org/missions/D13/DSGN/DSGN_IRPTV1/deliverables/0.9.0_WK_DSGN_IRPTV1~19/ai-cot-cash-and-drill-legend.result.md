# DSGN_IRPTV1.TO-IV-e-29 -- result summary (0.9.0_WK_DSGN_IRPTV1~19)

CTO 101039, `SIGNOFF_COT_CASH_S138_20260925.md` @d257eb67aa.

## IVE29-AC1 -- Cottonwood cash ON, coloured ASSET_CLASS.cash; other stays purple600
`portal/src/pages/AdvisorIntelligence/_partners/cottonwood/layout.ts`: `includesCash: false` -> `true`,
`colorPalette: { other: PALETTE.purple600 }` -> `{ other: PALETTE.purple600, cash: ASSET_CLASS.cash }`,
`ordered` gains `cash` at the front (`['cash', 'fixed_income', 'equity', 'alternatives', 'other']`).
49financial and Inflection layouts untouched, verified against the actual base commit's bytes
(`git show 7eec611ab155cf4b47310342f356a0b2c83c4f28:<path>`) inside the test itself, not a hand-typed
expectation. VERDICT: COT-CASH-ON-OK.

## IVE29-AC2 -- shares (cash + other together)
`normalizeMixTo4Class` already supported `{ includeCash, includeOther }` independently (built generically
by IV-e-28); no change needed to `composition.ts`. A 5-class Cottonwood mix (cash, equity, fixed_income,
alternatives, other) yields 5 entries summing to pct 1; an all-cash mix yields exactly one entry, cash, at
pct 1. VERDICT: COT-SHARES-OK.

## IVE29-AC3 -- the client-drill legend
`ConsolidatedOverviewPanel.tsx`'s vertical legend list gains `'other'` after `'alternatives'` (now
`['cash', 'fixed_income', 'equity', 'alternatives', 'other']`); the component gains an optional
`tenantLayout` prop, strictly additive (every existing caller that omits it keeps the exact prior
MIX_PIE-only colour behaviour). Colour resolution moved from a bare `mixPieColor` alias to
`resolveMixColor(cls, tenantLayout)`, which prefers `tenantLayout.assetClasses.colorPalette[cls]` -- the
same override mechanism `PartnerAnalytics.tsx`'s `resolveMixClassMeta` already uses -- falling back to the
global `MIX_PIE` palette. Rendered via `react-dom/server` with the real component, a Cottonwood composition
and the discovered Cottonwood layout: the legend lists "Cash" and "Other" with their formatted amounts and
each its own resolved colour (green300 / purple600); the 49financial-shaped comparison shows no "Other".
VERDICT: DRILL-LEGEND-OK.

MEASURED during this cell: `recharts`' `<PieChart>`/`<Cell>` does not synchronously emit SVG paths under
`renderToStaticMarkup` (the `recharts-wrapper` div renders empty in SSR), so the donut's own rendered fills
are not independently assertable from a test; the donut/legend colour parity is a source-level guarantee
instead (both read `composition.mix` through the same `colorFor` closure, donut unfiltered).

## IVE29-AC4 -- judgment, recorded only
Per the task order: graded by `2.0.0_SA_COO~D` on the PROD read after `2.0.0_SA_COO~M`'s C_06 cash run.
Not self-graded; RECORDED with no verdict in the proof instance.

## Surprise row filed: DSGN_IRPTV1-W19-S1 (ARMED)
`ConsolidatedOverviewPanel`'s new `tenantLayout` prop is correct and passes AC3 exactly as specified, but
none of its three real PROD call chains (`CanonicalBookView.tsx` and its own three callers) are in this
TO's `<paths>` grant, so they do not pass the prop yet. Until a follow-on TO threads it through, Cottonwood's
real client-drill donut/legend keeps the global `MIX_PIE` fallback colours (`cash` amber, `other` grey)
on PROD, even though the "Other" entry now lists at all (that part needs no new prop -- `composition.mix`
already carries `other` for Cottonwood via `AdvisorBookView.tsx`'s existing tenant-driven
`normalizeMixTo4Class` call). Amounts and shares are unaffected by this gap; only the colour half is.

## Controls
- Mutant: flipped `includesCash` back to `false` in-worktree only (never staged) -> IVE29-AC1 failed as
  expected (`Cottonwood includesCash = false, expected true`); reverted, `git diff` against HEAD empty,
  re-ran to VERDICT: COT-CASH-ON-OK before this proof was written.
- Determinism: AC1/AC2/AC3 each run twice back-to-back, identical VERDICT lines both times; the whole
  `cot-other/` directory (6 tests) run clean; `bun run typecheck` (`tsc -b --noEmit`) rc=0 both before and
  after.

## Commits
- portal: `3a87274ff4429c02ef12133782e512e32f498caa` on `wk-DSGN_IRPTV1-19-portal` (LOCAL).
