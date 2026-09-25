# DSGN_IRPTV1.TO-IV-e-25 -- repairs-batch -- result

Worker 0.9.0_WK_DSGN_IRPTV1~15, worktree pair `wk-DSGN_IRPTV1-15` / `wk-DSGN_IRPTV1-15/portal` (base
`8242412dde9a3ef807e118f648242cf24ffe2981`).

## What changed

- `portal/src/pages/InvestorReporting/__tests__/fe-s-5/states.test.ts` -- the unsupported-benchmark
  sub-test now asserts `NOT_SUPPLIED` (`ReturnsHeatmap.tsx`'s own word) with the reason on the cell's
  hover, never the retired page-level `UNAVAILABLE_WORD`; the two sub-tests pinning the retired
  `render/performance/Summary.tsx` block (`data-block="summary"`/`"account-detail"`) are re-scoped to
  `AnswerStatus`'s `data-slot="answer-status" data-state="PARTIAL"` and `AccountsTable`'s
  `data-slot="accounts-table"`. Each change cites R6 (`RULINGS_IRPT_20260925.md@75156f2b18`).
- `portal/src/components/CategoryViewTree.tsx` -- additive `rowColor?: (key, label) => string |
  undefined` prop (new `RowColorContext`), consulted by `useRowColorOf()` ahead of the pre-existing
  name-keyed `l1ColorOf` on every surface an L1 row's own colour is drawn (the tile's bar segment via
  `l1Segments`, its row dot, and the breakdown dialog's L1 mark via `breakdownSegments`). Absent
  (default `null`) keeps every existing caller, Model Portfolios included, byte-identical.
- `portal/src/pages/InvestorReporting/tabs/holdings/DrillTree.tsx` -- `colorForServedModelCode`
  factored out of `modelSliceColor` (no behaviour change) and reused by the new
  `modelRowColorMap(snapshot)`, which maps every L1 child (one level beneath a top-level category --
  the level the hero card's rows read) carrying a served `modelCode` to that code's colour, wired as
  `rowColor` at the `<CategoryViewTree>` mount. New `drillSliceColor(node, label)` routes a SECURITY
  drill-pie slice through `ASSET_CLASS_COLOR[assetClassOf(node)]` (`assetClass.ts`, read only) instead
  of `modelSliceColor`'s name-hash fallback; a non-security row is unchanged.
- `portal/src/components/ui/SearchSelect.tsx` -- the input is `role="combobox"` with `aria-expanded`,
  `aria-controls` (a `useId`-generated listbox id) and `aria-activedescendant`; the list is
  `role="listbox"`; each option is `role="option"` with `aria-selected`. The keyboard rule is the
  exported pure function `handleSearchSelectKeyDown(key, activeIndex, options)`: ArrowDown/ArrowUp move
  the active index (clamped), Enter returns `{type:'select', option}` for the active option (or
  `'none'`), Escape returns `{type:'close'}`.
- Three new tests under `portal/src/pages/InvestorReporting/__tests__/dsgn-irptv1/`:
  `iv-e-25.states-rescope.test.ts` (AC1), `iv-e-25.colour-by-code.test.ts` (AC2),
  `iv-e-25.search-select-a11y.test.ts` (AC3).

## Per-criterion

- **IVE25-AC1** PASS -- `VERDICT: STATES-RESCOPED-OK`. `fe-s-5/states.test.ts` carries >=3 R6
  citations, no longer pins the retired heatmap `UNAVAILABLE` word or the retired
  `data-block="summary"`/`"account-detail"` assertions, and runs 6 pass / 0 fail as a subprocess.
- **IVE25-AC2** PASS -- `VERDICT: COLOUR-BY-CODE-OK`. A model node with served code `ULT` and a
  misleading "Short Term" label resolves ULT's colour on both the drill pie and the hero card (through
  DrillTree's own `rowColor` resolver); a security node resolves `ASSET_CLASS_COLOR` for its served
  class across all 5 classes (+ the `cashNode` override), never the extended-palette name hash;
  `ModelPortfolios.tsx` carries no diff against the worktree's base and omitting `rowColor` reproduces
  the exact pre-existing colour resolution.
- **IVE25-AC3** PASS -- `VERDICT: SEARCH-SELECT-A11Y-OK`. Combobox/listbox/option roles and aria
  attributes present in the rendered markup; the exported keydown function moves/clamps on
  ArrowDown/ArrowUp, selects on Enter, closes on Escape, and is a no-op on an unrelated key.
- **IVE25-AC4** RECORD (judgment, `2.0.0_SA_COO~D` at the round-4 drain per CTO 100991).

## Controls

- Mutant: reverted `drillSliceColor` in-worktree (never staged) to call `modelSliceColor`
  unconditionally for every row -- `IVE25-AC2` failed as expected (`VERDICT: COLOUR-BY-CODE-FAIL`,
  every security's drill-pie colour fell to the extended-palette name hash). Reverted; `git diff`
  against the committed file empty (byte-identical restore); `IVE25-AC2` re-run to
  `VERDICT: COLOUR-BY-CODE-OK` before this proof was written.
- Determinism: AC1/AC2/AC3 re-run twice back-to-back, identical VERDICT and expect-call counts both
  times. Regression: the full `src/pages/InvestorReporting/__tests__/` suite run twice (300s bound),
  both times 704 pass / 27 skip / 79 fail / 2 errors / 3129 expect() calls across 810 tests in 202
  files. The 79 failures are pre-existing `EnvelopeMismatch` contract-fixture failures
  (`contracts/envelope.ts`), confirmed absent from every file this cell touched (grep of the failing
  test names against `CategoryViewTree`/`DrillTree`/`SearchSelect`/`states.test.ts`/`dsgn-irptv1`
  `iv-e-25` finds zero matches); `bun run typecheck` rc=0 both before and after.

## Surprise

`DSGN_IRPTV1-W15-S1` (OBSERVATION, INERT): cell (b) says "a colour resolver per member", but a model
in a `HoldingsSnapshot` lands as `CategoryViewTree`'s L1 row (a category's direct child, via
`mdpfResultFromSnapshot`'s `children`), never as an L2 `MdpfCategoryMember` -- confirmed by reading the
`holdingsSnapshot.success.json` fixture's own node hierarchy (account -> model -> security) and by
`comp-find` showing `aum.ts`'s member/child types carry no `model_code` field at any grain. The shipped
`rowColor` prop resolves at the L1-row grain the actual data shape offers, over the field that IS
served (`HoldingsNode.modelCode`, the same one the drill donut already read since IV-e-11). Not
blocking: IVE25-AC1/AC2/AC3 all PASS-by-output under this shape.
