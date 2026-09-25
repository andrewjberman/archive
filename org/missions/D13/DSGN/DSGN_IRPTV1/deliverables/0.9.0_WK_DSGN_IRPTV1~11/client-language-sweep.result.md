# DSGN_IRPTV1.TO-IV-e-18 -- session log, 0.9.0_WK_DSGN_IRPTV1~11

## What was built

- `ReportingTab.tsx` / `HoldingsTab.tsx` -- `AnswerStatus` (P-written, never edited) is now
  mounted inside a new `<details data-slot="report-details-disclosure">`; the Performance
  mount also brings back the previously-orphaned `MethodAndSources` inside the same
  disclosure, so the state word, reason code, revision id, lineage and raw ISO timestamps
  are all one click away instead of on the face.
- `ReturnsHeatmap.tsx` (N2) -- an unsupported metric cell reads `not supplied`; the reason
  (`fact.return.unavailableReason`) was already on that cell's own `title` hover and is
  unchanged. `UNAVAILABLE_WORD` import dropped.
- `PerformanceControls.tsx` -- the "Basis: net" chip's fact moves into the chip's own
  `title`; the visible face reads "Fee basis" only.
- `AccountsTable.tsx` -- the period-returns cell shows the value(s) only; the per-period
  "YTD:"-style label moves into that cell's own `title`.
- `HoldingsSummary.tsx` (N3) -- the Observed source date is formatted through
  `@/lib/dateUtils` `formatPanelTimestamp` (the same formatter `PanelFooter` already uses
  elsewhere in this tree), never the raw ISO string the wire carries.
- `SliceTable.tsx` (N4) -- Supervision/Advisory cells print advisor words ("Opal supervised",
  "Advised", ...); the raw contract token is retained on the row's own `title` (added beside
  the existing Basis/Denominator/Source facts).
- N1 (`GenerateComposer.tsx`'s "select a client above" text) was already closed by the
  drain's `HeaderSelectionContext` hookup at this worktree's base (8cd2dab2) -- confirmed,
  not re-implemented.
- `fe-s-5/fields.test.ts` re-scoped citing CTO 100865: account ids (never printed, by rule)
  and a period's own window (never individually displayed) are excluded from the leaf walk,
  each counted and printed; formatted currency counts as reached in either display form the
  tab's own components actually use (comma-grouped for the `accounts` group, plain for the
  `summary` group).
- Three new tests under `__tests__/dsgn-irptv1/`: `iv-e-18.census.test.ts` (IVE18-AC1),
  `iv-e-18.retained.test.ts` (IVE18-AC2), `iv-e-18.fields-rescope.test.ts` (IVE18-AC3, runs
  the re-scoped `fe-s-5/fields.test.ts` as a real subprocess).

## Verification

- Each of the three new tests: 1 pass / 0 fail, its own `VERDICT: *-OK`/`*-CLEAN` line, run
  twice for determinism (identical output both times).
- `fe-s-5/fields.test.ts`: baseline (before this worker's edits) 3 of 4 sub-tests FAILED
  (missing account ids, period-window dates, and comma-formatted per-account currency,
  plus five `method` fields with nowhere to render). After: 4 of 4 pass (24/24, 24/24,
  22/22 fields reached per firm fixture).
- Mutant control: reverted `ReportingTab.tsx`'s Performance mount to the parent commit's
  plain `<AnswerStatus .../>` (no `<details>` wrap, no `MethodAndSources`) -- `iv-e-18.
  census.test.ts` failed with `state tokens leaked in performance: Partial` and `reason
  codes leaked in performance: METRIC_NOT_SUPPORTED`, no VERDICT line. File restored
  byte-for-byte (`git diff --stat` empty afterward); re-ran clean.
- No-regression sweep of every file importing a component this order touches (fe-s-7 x2,
  fe-s-55, fe-s-32, fe-s-39, fe-s-76, iv-e-10, iv-e-6 x2, iv-e-16, iv-e-11, iv-e-12, iv-e-13,
  fe-s-10, fe-s-5): 123 pass / 14 fail total. 11 of the 14 are pre-existing at this
  worktree's HEAD, unrelated to this order's files (fe-s-39's `EnvelopeMismatch` throws from
  `contracts/envelope.ts` before any rendering; fe-s-5/states.test.ts's `data-block="summary"`
  checks a component retired from `ReportingTab.tsx` in round 1). The remaining 3 are ONE
  new failure this order's own mandated N2 change causes in `fe-s-5/states.test.ts` (an
  out-of-grant file asserting the literal `UNAVAILABLE` word this amendment explicitly
  retires for this cell) -- filed, not silently absorbed.

## Declared exclusion

- The firm-attribution chip (`global/FirmAttribution.tsx`) was left unmoved: its visible
  name text is the load-bearing assertion of the out-of-grant `fe-s-10/parity.test.ts`
  (`globalMarkup.includes('49 Financial<')`); moving it to a disclosure breaks that pinned
  sibling-cell test. Every other item the cell names (status band, "Basis:" chip,
  accounts-table PERIOD labels, plus N1-N4) was implemented.

## Surprise rows

- `DSGN_IRPTV1-W11-S1` (OBSERVATION, ARMED) -- the firm-attribution chip conflict above.
- `DSGN_IRPTV1-W11-S2` (OBSERVATION, ARMED) -- N2's mandated `UNAVAILABLE` removal breaks
  the out-of-grant `fe-s-5/states.test.ts`'s stale assertion of the same word for the same
  cell.
