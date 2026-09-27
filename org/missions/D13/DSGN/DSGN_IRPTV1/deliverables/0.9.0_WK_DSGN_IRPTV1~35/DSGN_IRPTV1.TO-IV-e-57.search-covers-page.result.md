# DSGN_IRPTV1.TO-IV-e-57 -- session log (0.9.0_WK_DSGN_IRPTV1~35)

## What was built

**UIR-11 (root fix, window 9):** `TabShell.tsx`'s pre-selection sample branch
(`activeTab !== 'analysis' && !scopeRef`) now forks FIRST on a new `searchActive` prop (default
false): true mounts nothing in place of `SampleView` (`data-slot="selection-required-searching"`,
empty -- never merely a CSS-hidden `SampleView`); false is the exact prior branch, unchanged.
`ClientSearch.tsx` tells `index.tsx` on every keystroke through a new optional
`onSearchActiveChange` prop, called from the SAME `onQuery` handler that already tracks local
`query` state, using `SearchSelect.tsx`'s own exported `searchSelectShouldOpen(next)` rule --
never a second, independently-derived guess at when the list is open. `index.tsx` holds this in a
new `searchActive` state and relays it into `TabShell`. `SearchSelect.tsx`'s open listbox also
gains a bounded `max-h-72 overflow-y-auto` (additive; the Build text's "the list itself sits above
every panel with a bounded height").

**UIR-06 (amendment 1, CTO 101880):** `SampleView.tsx`'s six money/percent tiles (period return,
vs benchmark, ending/beginning value, current value, unique accounts) now render a new
`FigurePlaceholder` -- a flat, `aria-hidden`, no-digit shape -- instead of `money()`/`signedPct()`/
`String(count)` text, so nothing in the pre-selection sample can be mistaken for a client's own
figure even before the Sample badge is noticed (the CRO round-8 walk's own example: "+10.00%,
$2,500,000.00"). The underlying numeric constants and their `SAMPLE_*_DOLLAR_VALUES` exports are
unchanged (`iv-e-15.sample-provenance.test.ts`'s own real-figure collision diff still reads the
same values); the now-dead `money`/`signedPct` string helpers were removed.

**UIR-20 (amendment 1, CTO 101880):** `index.tsx` gains a second, independent export gate,
`analysisExportGateOk` (permanently `false` when `activeTab === 'analysis'`), ANDed alongside the
existing, byte-for-byte UNCHANGED `exportGateOk` line -- closing the CRO's finding that Export was
live on the Analysis tab with no report generated. The disabled fallback `<button>` gains `inert`
beside its existing `disabled`/`aria-disabled="true"`.

## The AnalysisTab.tsx gap (row DSGN_IRPTV1-W35-S2)

Amendment 1's Build text asks Export to gate on whether "the active tab" -- Analysis included --
has an answer-bearing report, the same shape Performance already has via `ReportingTab.tsx`'s own
`onExportTarget` effect. `AnalysisTab.tsx` holds its own `report`/`selectedRequest` state entirely
locally and threads no equivalent signal up, and it is out of this cell's `<paths>` grant (the
decomp's own `writes` column for `IV-e-57` names only SearchSelect/index.tsx/TabShell/SampleView/
ClientSearch) -- the same KNOWN GAP class already on record for the retired per-tab control
(`iv-e-16.page-export.test.ts`'s own docstring). Resolved in-lane CONSERVATIVELY: Analysis's own
gate can only ever prove "no signal published", so it stays permanently closed rather than the
prior unconditional `true`, which satisfies AC1's own literal arms (disabled with no report;
Performance enabled with an answer-bearing report, control) without a false enable. Filed as row
`DSGN_IRPTV1-W35-S2` (OBSERVATION, ARMED) for the future cell that wires `AnalysisTab.tsx`'s own
report state up.

## Verification

- `bun test iv-e-57.search-covers.test.tsx`: 1 pass / 0 fail, `VERDICT: SEARCH-COVERS-OK` (20 named
  arms: UIR-11a-h, UIR-06a-c x2 tabs, UIR-20a-c).
- 9 sibling files sharing the touched components (`iv-e-15` x3, `iv-e-37`, `iv-e-16`, `iv-e-45`,
  `iv-e-25`, `iv-e-9`, `fe-s-10/tabs-mounted`): 14 pass / 0 fail, 53 expect() calls -- none
  regressed, including `iv-e-45.face-batch.test.tsx`'s own regex-pinned UIR-20b/20c arms over
  `index.tsx`'s source (the exact prior `exportGateOk` line still matches byte-for-byte) and
  `iv-e-37.search.test.tsx`'s own UIR-06/UIR-11 arms (a different, already-fixed prior bug --
  confirmed non-overlapping).
- Full `bun test ./src/pages/InvestorReporting`: 880 pass / 27 skip / 5 fail, 912 tests, 247 files
  -- identical 5-fail count before and after this cell's edits (confirmed by import audit: none of
  the 4 failing files -- `fe-s-1/fixtures.test.ts`, `fe-s-1/source-bounds.test.ts`,
  `fe-s-25/absent-vs-null.test.ts` x2 -- import any file this cell touches).
- `bun run typecheck`: 0 errors. `bun run lint`: 0 errors; 0 NEW warnings in any of the 5 touched
  files (2 transient `money`/`signedPct` unused-var warnings introduced then removed within this
  same delivery; `ClientSearch.tsx:113`'s setState-in-effect and `SampleView.tsx`'s two Fast-refresh
  warnings both pre-exist this cell's diff).
- Mutant (`TabShell.tsx`'s `searchActive` gate forced unreachable): fires as expected (4 named arms
  fail -- UIR-11a/b/c/h -- `VERDICT: SEARCH-COVERS-FAIL`); restored to the exact committed text
  (`git diff --stat` empty), re-ran clean 3x, `VERDICT: SEARCH-COVERS-OK` every time.

## Commits

- Portal: `e774605738cec7840a625d1f3948c048f6de4b25` on `wk-DSGN_IRPTV1-35-portal` (LOCAL).
- Workspace: see the WORKER REPORT for the committed hash.
