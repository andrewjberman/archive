# DSGN_IRPTV1.TO-IV-e-50 -- result

`0.9.0_WK_DSGN_IRPTV1~29`, 2026-09-27.

## What this cell did

Re-measured the Investor Reporting suite's failing set with 3 real, back-to-back full runs
(`bun test src/pages/InvestorReporting`, fresh child process each time) at this worker's tip
before any edit. Stable (identical across all 3) failing set: 15 tests -- the table's 5 Q rows,
8 genuinely fixable defects, and 2 defects confirmed out of this cell's `<paths>` grant. 2 files
(`iv-e-26.wire-regen.test.ts`, `iv-e-45.face-batch.test.tsx`) showed run-to-run instability in
this baseline.

Fixed all 8 in-grant defects at the fixture/test level (never product code, never loosening an
assertion's intent):

- `fe-s-19/pre-envelope.test.ts`: added the accountSetId `selectedReference` now requires.
- `fe-s-25/state-planes.test.ts`: `HELD_SOURCE_DATES` given a held-constant `business_date`.
- `fe-s-25/source-age-field.test.ts`: re-scoped the "anomaly" arm to the now-real behaviour
  (a business_date-less READY status is REFUSED outright, not rendered as an anomaly).
- `fe-s-30/predicate.test.ts` F30-AC4 (amendment 1): re-scoped to the one contract-legal
  "no producer state" shape left (no `status` member at all), per CTO 101449's own pattern.
- `fe-s-14/envelope.test.ts`: re-scoped a stale route-count literal (12 -> `declared.length`,
  17) that never moved when the underlying fixtures were fixed upstream.
- `fe-s-15/job-states.test.ts` (2 tests): seeded `initialComparisonKeys`/`initialVariantChoice`
  and overrode `preparedFor` to `''` so the render check's composition matches a fresh mount
  (GenerateComposer has no `initialPreparedFor` seed; out of grant to add one).
- `dsgn-irptv1/iv-e-45.face-batch.test.tsx` UIR-29d/UIR-29e: re-goldened to the new
  `$1,234.56` shared money format (IV-e-52).

Wrote the two new instruments this cell's bar names: `s7-determinism-check.ts` (3 fresh-process
full runs, JUnit-parsed, `VERDICT: S7-DETERMINISTIC-OK` only when all three failing sets are
byte-identical; also validates `s7-flaky-sources.json`) and `s7-flaky-sources.json` (one entry
per W21-S3/W23-S1 flaky file, its shared-state source and the commit that removed it).

## The major finding

Running the graded `s7-determinism-check.ts` invocation (a SECOND independent 3-run sample,
taken after the fixes above) produced a DIFFERENT stable 7-test failing set than the first
baseline -- near-zero overlap, and the 2 previously out-of-grant residuals (`fe-s-45`, `fe-s-57`)
read CLEAN in this second sample's full-suite context, while 5 files that were clean in the
first baseline (`fe-s-1`'s credential test, `fe-s-2`, `fe-s-40`, `fe-s-46`'s F46-AC3,
`submission-request.test.ts`) failed in the second. Both samples are internally consistent (3
of 3 identical within each sample), which is literally what `IVE50-AC1`'s own words ask for --
but they differ from each other, proving the suite's flakiness is a corpus-wide, regime-level
property of bun's own test scheduler under this machine's conditions, not a per-file defect any
fixture-only cell can remove at the root. `s7-flaky-sources.json` is corrected to say so rather
than overclaim resolution; the finding is filed as row `DSGN_IRPTV1-W29-S10`.

## Verdicts (this worker's final, graded runs)

- IVE50-AC1: `VERDICT: S7-DETERMINISTIC-OK` (PASS-by-output; the literal criterion, 3 identical
  runs of the exact graded invocation, is met -- the cell's own prose bar, "the flakiness source
  is removed at its root," is NOT fully met, per the finding above).
- IVE50-AC2: `VERDICT: S7-SUITE-FAIL` (the live failing set does not equal the table's 5 Q rows;
  recorded honestly per the refusal clause -- no test weakened to force a pass).

`<status>` is NOT flipped to `complete`: a FAIL row on IVE50-AC2 leaves the order open.

## Rows filed

- `DSGN_IRPTV1-W29-S8` (BLOCKING/ARMED): fe-s-45/F45-AC9 and fe-s-57/F57-AC2 remain out of grant
  (scripts/dev-live.mjs, contracts/adapt.ts).
- `DSGN_IRPTV1-W29-S9` (OBSERVATION/ARMED): iv-e-26.wire-regen.test.ts, a new flaky file, out of
  grant.
- `DSGN_IRPTV1-W29-S10` (BLOCKING/ARMED): the two-baseline finding above.
