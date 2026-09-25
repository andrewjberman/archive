# DSGN_IRPTV1.TO-IV-e-11 -- model-colour-by-code -- result

Worker 0.9.0_WK_DSGN_IRPTV1~8, worktree pair `wk-DSGN_IRPTV1-8` / `wk-DSGN_IRPTV1-8/portal` (base 13b5356f).

## What changed

- `portal/src/lib/modelPortfolioColors.ts` -- `getModelColor` now (1) resolves through
  `canonicalModelCode` / `getCanonicalModelName` first (a code or known alias exact-matches and
  never touches partial match); (2) exact-matches the raw string; (3) on partial match, normalizes
  hyphens/whitespace and picks the **longest** matching key, never the first one
  `Object.entries` iteration reaches. This closes the screenshot-151107 bug:
  `getModelColor('Opal Ultra Long Term')` used to return `'Long Term'`'s blue because that shorter
  key sits earlier in the map and is itself a substring of "...ultra long term".
- `portal/src/pages/InvestorReporting/tabs/holdings/DrillTree.tsx` -- `modelSliceColor` restructured
  so the label fallback (`colorForSlice`) is reached **only** when no served code resolves a colour
  -- never while a code is on hand, even a deliberately misleading label. `colorForSlice` itself is
  unchanged (it already stripped the "Opal " prefix from a prior round).
- Three new tests under `portal/src/pages/InvestorReporting/__tests__/dsgn-irptv1/`:
  `iv-e-11.model-color.test.ts` (AC1), `iv-e-11.readers.test.ts` (AC2), `iv-e-11.irpt-by-code.test.ts`
  (AC3).

## Per-criterion

- **IVE11-AC1** PASS -- `VERDICT: MODEL-COLOR-OK`. 5 canonical names distinct; 7 codes (5 + 2 legacy)
  resolve to their canonical colour; the screenshot bug itself ("Opal Ultra Long Term" -> red, never
  blue); 3 planted longer-name-embeds-shorter-key cases all resolve to the longer key's colour.
- **IVE11-AC2** PASS -- `VERDICT: READERS-UNCHANGED`. 11 importers of `getModelColor` printed as the
  denominator (`ModelPortfolios.tsx`, `ModelPortfolios/tabs/PeersTab.tsx`, this cell's own
  `DrillTree.tsx`, `RollingSharpeChart.tsx`, `RollingCaptureChart.tsx`, `MaxDrawdownChart.tsx`,
  `ReturnVolatilityScatter.tsx`, `SatelliteModal.tsx`, `ModelPortfolioModal.tsx`,
  `CategoryViewTree.tsx`, `BenchmarkHeatmap.tsx`); 22 correctly-named/coded input shapes those
  readers actually pass, each resolving to the identical base-committed hex now. `Positioning` and
  `Attribution` (named in the cell text) import only `displayModelName`, never `getModelColor` --
  confirmed by source read, so they carry no colour to compare and are outside this criterion's
  domain.
- **IVE11-AC3** PASS -- `VERDICT: IRPT-BY-CODE-OK`. All 5 MDPF registry codes resolve their own
  canonical colour even with a deliberately misleading label planted; the label path is exercised
  correctly only when no code (null/unregistered) is served.
- **IVE11-AC4** RECORD (judgment, `3.0.0_SA_CVO` at L9, the real localhost:5174 run).

## Controls

- Mutant: reverted `getModelColor`'s partial-match to the original first-match-in-insertion-order
  logic (worktree-only, never staged) -- `IVE11-AC1` failed as expected (`VERDICT: MODEL-COLOR-FAIL`,
  "Opal Ultra Long Term" resolved `#3b82f6` (Long Term's blue) instead of `#ef4444`). Reverted; `git
  diff` against the committed file is empty (byte-identical restore).
- Determinism: AC1/AC2/AC3 re-run twice back-to-back, identical VERDICT and expect-call counts both
  times.
- Regression: `bun test src/pages/InvestorReporting/__tests__/dsgn-irptv1/` -- 39 pass / 0 fail / 244
  expect() calls, unchanged from before this cell. `bun run typecheck` rc=0.

## Surprise

`DSGN_IRPTV1-W8-S1` (OBSERVATION, INERT): the cell text's clause (b) says the hero cards colour a
model "by its served modelCode", but `CategoryViewTree`'s L2 members (the hero-card contract,
`MdpfCategoryNode`/`MdpfCategoryChildNode` in `src/api/endpoints/aum.ts`) carry no `modelCode` field
at all -- only a name -- and `CategoryViewTree.tsx` is out of this cell's grant (its own docstring:
"IMPORTED, NEVER EDITED"). The hero cards resolve colour by canonicalized NAME
(`memberColor` -> `getModelColor(getCanonicalModelName(name))`), and this cell's library-level fix
(AC1) is what makes that NAME path correct for "Opal Ultra Long Term" -- not a served code, because
none is served there. Only the drill donut (`HoldingsNode.modelCode`) is genuinely code-keyed, and
that half is covered by AC3. No blocking effect: AC1/AC2/AC3/AC4 are all met either way.
