# IRPT_FNTEND.TO-FE-s-3 -- result (0.9.0_WK_IRPT_FNTEND~1)

**Cell `FE-s-3`: the tab shell, the selection store with its revision guard, and the status renderer
every tab uses.** Ten criteria: nine mechanical, all PASS by output; one (`F3-AC10`) is judgment and is
RECORDED with no verdict for `3.0.0_SA_CVO` at L9.

- Portal commit **3600af67fc8539a7fee1046272f57b733a4f4d19** -- LOCAL on branch `wk-irpt_fntend-1-3-fe-s-3`
  of the PORTAL repo (15 files, +1333 / -31). Never pushed.
- Workspace commit **467534723636823a7201b7dcfba8e3679eae023b** (the two surprise rows) -- LOCAL on the
  same branch name in the WORKSPACE repo. The proof, the three PNGs and the `<status>` flip ride the
  workspace commit after it.
- Proof of spec: `IRPT_FNTEND.TO-FE-s-3.tabs-selection-lifecycle.proof_of_spec.json`,
  `proof-of-spec-check.py` result recorded below.

---

## WHAT WAS BUILT

| Path (portal repo) | What it is |
|---|---|
| `src/pages/InvestorReporting/tabs/TabShell.tsx` | tab strip (`TabNavigation`/`useTabNavigation`, imported unedited) + three StatusPanel mount points |
| `src/pages/InvestorReporting/tabs/StatusPanel.tsx` | the status renderer: label, source age, safe-action buttons, reason-code text |
| `src/pages/InvestorReporting/state/selection.ts` | the selection store, no React: `{firm,scope,revision}`, `applyResponse`'s drop guard, `switchScope`'s synchronous clear |
| `src/pages/InvestorReporting/state/status.ts` | nine-state -> nine-label map, `isCompleteState`, `winsOverCachedReady`, `envelopeFromAvailability`, `formatSourceAge` |
| `src/pages/InvestorReporting/state/hooks.ts` | binds the store to React via `useSyncExternalStore` |
| `src/pages/InvestorReporting/header/FirmDropdown.tsx` | AMENDED: `className` copied verbatim from `ModelPortfolios.tsx:1268-1275` |
| `src/pages/InvestorReporting/index.tsx` | header controls moved to their own re-flowing row; `TabShell` mounted in FE-s-2's `data-slot="tabs"` |
| `src/pages/InvestorReporting/fixtures/smoke/fe-s-3-{loading,failed}.json` | the two new smoke fixture maps |
| `src/pages/InvestorReporting/__tests__/fe-s-3/*.test.ts` (+`ambient-shims.d.ts`) | 18 tests, 0 fail |
| `src/pages/InvestorReporting/__tests__/fe-s-2/app-diff.test.ts` | AMENDED: `test.skip` when `.scratch/app.diff` is absent |

### Design decisions worth reading

1. **All three tab bodies fetch through the typed client, not a static placeholder.** The cell says
   each tab starts "in LOADING against an empty envelope" -- read literally as the state BEFORE any
   response lands (`EMPTY_ENVELOPE`, a module constant). Reporting calls `getPerformanceReport`,
   Analysis calls `listAnalysisRequests` (not `getAnalysisReport`, which needs a `requestId` this cell
   has none of -- a scope-only status check is what `analysis-requests` is for), Holdings calls
   `getHoldingsSnapshot`; only each response's own `.availability` is read (state / sourceAsOf /
   publicReasonCode), never the report body itself. This is why F3-AC4's fixture map can drive Analysis
   to FAILED while Reporting/Holdings stay READY: it is not a static prop, it is what each operation's
   own fixture answers.
2. **`envelopeFromAvailability` bridges a real gap.** `Availability` (what `PerformanceReport` /
   `AnalysisRequest` / `HoldingsSnapshot` actually carry) has no `safeActions` field -- only
   `StatusEnvelope` does. `defaultSafeActions(state, reasonCode)` derives one recovery action per
   non-READY/LOADING state so the panel never shows a reason code with nothing to do about it.
3. **`isCompleteState` reuses `NON_ASSERTABLE_STATES` from FE-s-1's own contracts** rather than
   re-typing "which states count as complete" a second time (Rule 24: reuse the estate's domain). That
   denominator says STALE data is still WHOLE data (just old), so `isCompleteState` is true for READY
   and STALE, false for the other seven -- PARTIAL included, which is the one claim the cell names.

---

## CRITERIA -- 9 of 9 mechanical PASS by output, 1 judgment RECORDED

### F3-AC1 -- typecheck clean
`cd .../portal && timeout 120 bun run typecheck; echo rc=$?` -> `$ tsc -b --noEmit` / `rc=0`.

### F3-AC2 -- selection survives tabs; late response dropped; switchScope clears before fetch
`bun test .../fe-s-3/selection.test.ts` -> `5 pass, 0 fail, 32 expect() calls`. `DROPPED-LATE: 1 of 1`;
`ADAPTER CALL LOG: 1 entry, logged AFTER the synchronous clear` (against a REAL `FixtureAdapter`, not a
stand-in).

### F3-AC3 -- nine states distinct; FAILED-analysis leaves holdings; STALE wins; PARTIAL never complete
`bun test .../fe-s-3/status.test.ts` -> `8 pass, 0 fail, 34 expect() calls`. `LABELS: 9 distinct of 9
states`; `COMPLETE-ELIGIBLE: READY, STALE (2 of 9)`.

### F3-AC4 -- Analysis tab renders FAILED with source age, actions, reason code
`node scripts/ui-smoke.mjs ... --click Analysis` -> `rc=0`, `FIXTURES: 4 declared; 4 matched >=1 URL`.
PNG (`fe-s-3_failed_1440.png`): panel shows `Failed` / `Updated 8h ago` / `IR-ANALYSIS-ENGINE-UNAVAILABLE`
/ one `Retry` button.

### F3-AC5 -- tabs + LOADING panel at 390
`node scripts/ui-smoke.mjs ... fe-s-3-loading.json` -> `rc=0`. PNG (`fe-s-3_loading_390.png`): three tabs
render, Reporting panel shows `Loading` / `Source time unknown`.

### F3-AC6 -- no return arithmetic, no clock outside age formatting
`bun test .../fe-s-3/source-bounds.test.ts` -> `3 pass, 0 fail, 6 expect() calls`. `RETURN-FIELD CHECKS:
55 of 55 clean (5 files x 11 tokens)`; `Date.now: 1 occurrence(s) in state/status.ts` (0 elsewhere).

### F3-AC7 -- FirmDropdown select: primary-purple + ring-1, no text-white
`bun test .../fe-s-3/dropdown-class.test.ts` -> `2 pass, 0 fail, 6 expect() calls`. Token-level check on
47 rendered classes: contains `text-[hsl(var(--primary))]` and `ring-1`; does NOT contain the exact
token `text-white` (only the conditional `hover:text-white` remains). **Needed `bun:test`'s
`mock.module`** to load the real `FirmDropdown`/`PageSurfaceControl` chain at all -- see surprise
`IRPT_FNTEND-W1-S5` below.

### F3-AC8 -- drained diff test skips cleanly
`bun test .../fe-s-2/app-diff.test.ts` -> `0 pass, 1 skip, 0 fail`. `SKIPPED: .scratch/app.diff absent`.

### F3-AC9 -- re-flowed header row renders at 390
`node scripts/ui-smoke.mjs ... fe-s-2-default.json` -> `rc=0`. PNG (`fe-s-3_header_390.png`): Firm
dropdown and search box each in their own full-width row below the title, no clipping.

### F3-AC10 (judgment) -- RECORDED, NO VERDICT
Read of `fe-s-3_header_390.png` and `fe-s-3_failed_1440.png`: the firm control reads primary-purple on
white/transparent (not the control's default white), and both the dropdown and the search box are fully
visible below the title at 390. Backed by F3-AC7's class-level read as the substitute oracle. Graded by
`3.0.0_SA_CVO` at L9.

---

## CONTROLS

**Mutant (two, FIRED-AS-EXPECTED):** (1) removed the `(scope,revision)` guard from `applyResponse` in
`state/selection.ts` -> `selection.test.ts` went `3 pass / 2 fail`, failing exactly the two
`droppedLate` arms and nothing else. (2) collided `ENVELOPE_STATE_LABELS.STALE` onto `'Ready'` in
`state/status.ts` -> `status.test.ts` went `7 pass / 1 fail`, failing exactly the nine-distinct-labels
assertion. Both files restored from byte copies; `git status --porcelain` clean afterward; both test
files back to 0 fail.

**Determinism (STABLE):** all four `fe-s-3` test files run twice; the only differing line each time was
the wall-clock `Ran N tests ... [Xms]` line -- every count and every `console.log` line identical.

---

## SURPRISES FILED (workspace commit `467534723636823a7201b7dcfba8e3679eae023b`)

- **`IRPT_FNTEND-W1-S5`** (ARMED, disarm_owner `2.0.0_SA_COO~F`): `bun test` cannot resolve the portal's
  `@/*` alias AT ALL -- root `tsconfig.json` carries no `paths`, the alias lives only in the referenced
  `tsconfig.app.json`, which `tsc -b` honours via project references and Bun's own loader does not merge
  in. Reproduced independent of this cell with a one-line `import('@/lib/utils')` probe. Worked around
  entirely inside `dropdown-class.test.ts` with `bun:test`'s `mock.module`, re-exporting the real files
  by relative path -- `FirmDropdown.tsx` and `PageSurfaceControl.tsx` (do-not-edit) both load completely
  unmodified. ARMED because the workaround is per-test-file; any future `bun test` file importing a
  component that touches an `@/`-aliased module (most of the shared component library) hits the same
  failure.
- **`IRPT_FNTEND-W1-S6`** (ARMED, disarm_owner `2.0.0_SA_COO~F`): this order's assigned port 5181 was
  already bound by an orphaned vite dev server from the already-integrated FE-s-2 worker's worktree;
  5182/5183 were likewise held by orphaned servers from two other already-landed worktrees (FE-s-4,
  FE-s-8). None had stopped its server before its own final report, per every worker's identity brief.
  Terminated only the PID bound to THIS order's assigned port (5181) to bind this worker's own instance;
  the other two were left running since killing them is outside this lane.

---

## PROOF OF SPEC

`org/missions/D9/IRPT/IRPT_FNTEND/deliverables/0.9.0_WK_IRPT_FNTEND~1/IRPT_FNTEND.TO-FE-s-3.tabs-selection-lifecycle.proof_of_spec.json`

```
python .tools/proof-of-spec-check.py <instance> F3-AC1,F3-AC2,F3-AC3,F3-AC4,F3-AC5,F3-AC6,F3-AC7,F3-AC8,F3-AC9,F3-AC10
```

Result recorded by the checker's own exit code -- see the WORKER REPORT for the measured rc.
