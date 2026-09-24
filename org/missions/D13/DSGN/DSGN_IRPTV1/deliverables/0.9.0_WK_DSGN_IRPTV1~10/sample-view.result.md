# DSGN_IRPTV1.TO-IV-e-15 -- session log (0.9.0_WK_DSGN_IRPTV1~10)

## What was built

`portal/src/pages/InvestorReporting/tabs/SampleView.tsx` (new) replaces the one-line "select a
client" box `TabShell.tsx` rendered for the Performance and Holdings tabs when no client,
relationship or account is selected (Analysis is untouched -- it already works without a
selection). For each tab it renders:

- **Performance**: a sample headline (`data-slot="sample-headline"`, 4 tiles matching
  `PerformanceHeadline.tsx`'s own shape), a sample chart (`data-slot="sample-chart"`, a flat
  neutral bar sparkline over a round-number path), and a sample card (`data-slot="sample-card"`,
  method notes).
- **Holdings**: a sample hero (`data-slot="sample-hero"`, matching `HoldingsSummary.tsx`'s
  current-value/account-count shape), a sample map (`data-slot="sample-map"`, a flat neutral
  allocation strip), and a sample card (model coverage notes).
- Exactly one `data-slot="sample-choose-client-prompt"` per tab.
- Every one of the six panels carries the literal word "Sample" (a small badge in its
  `PanelHeader`'s `actions` slot) plus a disclosure line ("Illustrative sample -- not a client's
  data.").

`TabShell.tsx`'s only change: the `activeTab !== 'analysis' && !scopeRef` branch now renders
`<SampleView tab={...} />` instead of the old `<p data-slot="selection-required">` box.

## Provenance -- the round-number rule and the collision it caught

Every sample figure is `SampleView.tsx`'s own constant; the file imports nothing from
`fixtures/**` or any other real-data path (verified mechanically, `iv-e-15.sample-provenance`
ARM 1). The FIRST draft used 900,000 (beginning value) and 1,000,000 (ending value / holdings
current value) -- clean round numbers, but they turned out to exactly equal
`custodyTotalAmount` in two real fixtures (`fixtures/fe-s-7/holdings.cash-remainder.json` ->
900000.0, `holdings.cottonwood-target-blend.json` / `holdings.duplicate-relationship.json` ->
1000000.0). The provenance test's ARM 3 (a targeted diff of the sample's three dollar figures
against every `custodyTotalAmount` / `endingValue.value` / `beginningValue.value` leaf across
`fixtures/**/*.json`) caught this before it shipped; the values were changed to 2,500,000 /
2,250,000 / 750,000, none of which collide with any fixture in the corpus (25 distinct real
dollar facts scanned, 0 collisions). That check stays in the test, so a future edit reintroducing
a collision fails loudly.

ARM 3 is scoped to these three NAMED facts (not every integer in the corpus) on purpose: an
unscoped scan flags trivial small integers (list lengths, indices, percentages) that appear
everywhere and prove nothing -- a first attempt at that wider scan produced 6 false-looking
collisions on `0`, `2`, `4`, `10` before this narrower, well-grounded design replaced it.

## Tests written (none existed at base)

- `iv-e-15.sample-performance.test.ts` -- IVE15-AC1, 4 arms, `VERDICT: SAMPLE-PERFORMANCE-OK`.
- `iv-e-15.sample-holdings.test.ts` -- IVE15-AC2, 4 arms, `VERDICT: SAMPLE-HOLDINGS-OK`.
- `iv-e-15.sample-provenance.test.ts` -- IVE15-AC3, 3 arms, `VERDICT: SAMPLE-NOT-REAL-OK`.
- `ambient-shims.d.ts` -- adds the one `node:fs` export (`statSync`) this folder's tests need
  that no other `declare module 'node:fs'` block in the program already carries (see
  `__tests__/fe-s-1/node-builtins.d.ts`'s own header on why @types/node is out of the tsconfig
  program and ambient shims merge globally, not per-folder).

`bun run typecheck` (`tsc -b --noEmit`) is clean over the whole portal after these changes.

## Mutation control (IVE15-AC1)

Mutated `SampleChart`'s wrapper `data-slot="sample-chart"` to `"sample-chart-MUTATED"`.
`iv-e-15.sample-performance.test.ts` failed as expected: `ARM2: sample chart present: false`,
`VERDICT: SAMPLE-PERFORMANCE-FAIL arm 2: sample-chart slot missing; arm 3: chart not marked
Sample`, 0 pass / 1 fail. Restored from the scratchpad backup; `git diff --stat` against the
committed file showed no change, and the test re-ran clean 3x with byte-identical VERDICT lines
each time (determinism).

## IVE15-AC4

Judgment criterion, graded at L9 by `3.0.0_SA_CVO` from the real dev-server run the COO takes at
the drain -- recorded `UNVERIFIABLE-BY-INSTRUMENT` per the task order's own instruction; no
worker-assigned PASS/FAIL.

## Surprises

None filed for this cell. No premise failed, no path was elsewhere, no capability was missing;
the tree bar (`git rev-parse --abbrev-ref HEAD` -> `wk-DSGN_IRPTV1-10`; `org/` and `.tools/`
present) passed at the start.
