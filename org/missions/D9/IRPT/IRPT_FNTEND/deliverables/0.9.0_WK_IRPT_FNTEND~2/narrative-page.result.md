# IRPT_FNTEND.TO-FE-s-8 -- narrative page -- result

Worker: `0.9.0_WK_IRPT_FNTEND~2`. Branches: workspace `wk-irpt_fntend-2-2-fe-s-8`
(HEAD at TO start `531ff06aab`); portal `wk-irpt_fntend-2-2-fe-s-8` (HEAD at TO
start `b86e6aa2`, committed to `21b17327` in this session).

## What was built

- `portal/src/pages/InvestorReporting/render/narrative/compose.ts` -- pure
  composition: windows (marker + terms + tone + coverage flag), missing-history
  span, coverage note, footnotes, the fixed statement.
- `portal/src/pages/InvestorReporting/render/narrative/PeriodInContextPage.tsx`
  -- the page component: reused `CumulativeReturnChart`, a real-DOM marker
  list, per-window supporting-context bars and topic terms, the missing-history
  block, coverage note and footnotes.
- Three fixtures (`narrative.two-markers.json`, `narrative.pre-history.json`,
  `bundle.performance-with-narrative.json`) and one smoke map
  (`fixtures/smoke/fe-s-8-narrative.json`).
- Six files under `__tests__/fe-s-8/` (`_load.ts` + five test files):
  `markers`, `missing-history`, `language`, `evidence`, `determinism`.
- `render/manifest.ts`: `runtime: 'browser'` added to `RENDER_PACKAGE`, per the
  FE-s-4 drain's assignment (row `IRPT_FNTEND-W2-S4`/`S4`).

## Two premise gaps, recorded once as `IRPT_FNTEND-W2-S6`

1. **The cell names fields the FE-s-1 `NarrativePacket` contract does not
   carry** (`annotations`, `trendingTopics`, `topicCloud`, `coverage`,
   `historyCutoff`) and a live-data trio
   (`MarketRegimeIndicator`/`SentimentGauge`/`SentimentPanel`) that is neither
   presentation-only nor loadable under `bun test` in this worktree (measured:
   `@/...`-aliased imports fail to resolve from any location; the root
   `tsconfig.json` bun reads is a references-only file with no `paths`).
   `compose.ts`/`PeriodInContextPage.tsx` are built entirely from the real
   fields (`events[].evidence`, `coveredWindow`, `uncoveredReason`) and
   reproduce the three components' visual pattern locally rather than
   importing them.
2. **`render/performance/PerformanceDocument.tsx`** -- the file whose own
   header calls its inline placeholder "THE SLOT FE-s-8 FILLS" -- is outside
   this TO's `<paths>` and on its Reuse "never edited" list. The new page is
   therefore fully built and tested standalone (F8-AC1..AC6, F8-AC9 all PASS
   directly against it), but nothing calls it from the print route: the
   captured PNG for F8-AC7/F8-AC8 still shows FE-s-4's original placeholder.
   F8-AC7 still passes mechanically (rc=0, route renders, LOC recorded).
   F8-AC8's PNG-based judgment grade should be read with this fact in hand.

Filed at `org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v1.md`,
row `IRPT_FNTEND-W2-S6`, `hazard_standing: ARMED`, `disarm_owner: 2.0.0_SA_COO~F`.

## Verification

- `bun run typecheck`: rc=0.
- `bun test src/pages/InvestorReporting/__tests__/fe-s-8/`: 8 pass, 0 fail, 39
  `expect()` calls, across `markers` / `missing-history` / `language` /
  `evidence` / `determinism`.
- Full `bun test src/pages/InvestorReporting`: 95 tests, 94 pass, 1 pre-existing
  unrelated fail (`App.tsx diff`, fe-s-2's `app-diff.test.ts` -- a criterion
  artifact test that reads a worktree-local scratch file; already recorded at
  row `IRPT_FNTEND-S2`, not introduced by this TO).
- Mutation control: `compose.ts`'s `coveredByHistory` filter forced to the
  constant `true`; `missing-history.test.ts` failed as expected (0 pass, 1
  fail, `Expected: true, Received: false`); reverted from a pre-mutation copy
  and confirmed byte-identical (`git status --short`: no diff), full fe-s-8
  suite re-passed 8/8.
- `node scripts/ui-smoke.mjs "investor-reporting/print?bundle=perf-narrative-fixture-1"`:
  rc=0, PNG saved (`fe-s-8_print_narrative_1440.png`), 1/1 fixture matched.
  Port note: this TO's `<PORT>` (5182) was already occupied by another process
  on this box (a different `node.exe`, PID 17632, not this worker's); vite
  reassigned 5183 and the smoke run used the port it actually printed, per
  BOUNDS ("use the port it prints").
- `python -c "... 'RUNTIME_BROWSER=%s' % (\"runtime: 'browser'\" in s)"`:
  `RUNTIME_BROWSER=True`.
- `.tools/surprise-row-gate.py` on the investigation file: 1 new row of 15
  total, all step-7/step-10 fields present, OK.

## Commits

- Portal repo: `21b17327` (13 files, 1436 insertions) on branch
  `wk-irpt_fntend-2-2-fe-s-8`, LOCAL (not pushed).
- Workspace repo: this instance, this result file, the PNG, the surprise row
  and the task order's `<status>` flip, committed together, LOCAL (not
  pushed).
