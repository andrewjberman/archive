# DSGN_IRPTV1.TO-IV-e-69 -- session log (0.9.0_WK_DSGN_IRPTV1~35)

## What was built

**UIC-01 (PerformanceHeadline.tsx):** the four tiles (period return, vs benchmark, ending value,
beginning value) split into `suppliedTiles`/`missingTiles`. Only the supplied ones render as
tiles; every missing one collapses into ONE `data-slot="performance-headline-missing"` line
(`Label: not supplied` per item, joined with ` -- `), never its own tile. An answer with every
figure present renders exactly as before (four tiles, no missing line).

**UIC-02 (PerformanceChart.tsx):** the per-day table and its "Every plotted observation ..." count
line now sit inside a closed-by-default `<details data-slot="performance-chart-daily-disclosure">`.
The chart area and the series-endpoint figures (start/end date + value) stay the unconditional
default view.

**UIC-04 (ReturnsHeatmap.tsx, AccountsTable.tsx):** the heatmap's portfolio/benchmark/spread rows
each render only when the report carries at least one fact for that row (`portfolio.length > 0` /
`benchmarkReturns.length > 0` / a real `spread.value`); an omitted row is named once in a
`data-slot="returns-heatmap-missing"` line instead of a row of matching "not supplied" cells --
this is the real defect on the shipped fixture (no benchmark ever states a `spread`, so the spread
row previously read "not supplied" in every column). AccountsTable's `extraUncovered` ids (an
uncovered account with no other fact, not even a name) collapse from one "not supplied" row per id
into ONE stated row naming the count.

**UIC-05 (ReportingTab.tsx, AccountFilter.tsx):** the picker-figure fetch effect (`ytdCache`/
`ytdFetchedKeys`/`accountYtd`) moved below `period`/`requestedWindow` and now requests the SAME
window the tab's own report request uses, instead of a window hard-coded to `dateWindowForPreset
('YTD', ...)`. `AccountFilter` gained an additive, optional `periodLabel` prop (default `'YTD'`,
byte-identical to every pre-existing call site) -- `ReportingTab` passes the selected preset's own
label (`PERIOD_PRESETS`) or `'Custom'`.

**UIC-07 (PerformanceControls.tsx):** on the `SI` preset only, the "Requested" line's start reads
"the account's first data point" instead of the raw `1970-01-01` request sentinel
(`period.ts`'s own `SINCE_INCEPTION_START`, unchanged -- it is still what the request itself
carries; only the face never prints it). Every other preset/custom range is unchanged.

**UIC-08 (ReportingTab.tsx):** `WORDED_REFUSAL_WORDS`' two messages now also name WHO makes the
figure available (the Opal Capital service team / the upstream data source Opal Capital relies
on), keeping the exact substrings `iv-e-39.account-picker-refusal.test.tsx`'s pinned battery reads
for ("not covered"/"temporarily unavailable", "becomes available", and the message text itself
verbatim -- so the wording was written to carry no apostrophe, since that pinned test's own
`wordsVisible` check is a raw, non-HTML-escaped substring compare against `renderToStaticMarkup`'s
output).

**UIC-09 (StatusPanel.tsx / state/status.ts):** left untouched -- measured, not assumed, to already
hold: `LOADING`'s label is the plain word `'Loading'`, and `formatSourceAgeForState`/
`sourceAgeKindFor` already read `NO_SOURCE_AGE_YET` ("No source age yet") for every no-answer
state including `LOADING`, never a raw timestamp/`undefined`/`NaN`. `fe-s-25`'s own pinned battery
(`absent-vs-null.test.ts`, `state-planes.test.ts`) already locks this exact wording for QUEUED/
RUNNING/the unanswered browser -- touching either file risked breaking that battery for no
behaviour change this cell's acceptance line asks for. `iv-e-69`'s own UIC-09 arm proves the
current behaviour directly instead (control arm: an answered state's source age carries a real
reading, never the no-source-yet wording).

## A regression found and fixed mid-cell

The first UIC-08 wording used an apostrophe ("Opal Capital's service team"). Two PINNED sibling
tests (`iv-e-39.account-picker-refusal.test.tsx`'s `wordsVisible` check, `iv-e-34.focus-refusal-
export.test.tsx`) compare `WORDED_REFUSAL_WORDS`'s value against `renderToStaticMarkup`'s raw,
HTML-escaped output with a straight (non-escaped) substring match -- so the apostrophe silently
broke both. Reworded to "the Opal Capital service team" (no apostrophe); both tests, plus this
cell's own `iv-e-69` battery, are green afterward.

## Regression sweep

28 pass / 0 fail across 18 sibling files that mount a touched component (`iv-t-2.*`, `iv-e-6`,
`iv-e-34.*`, `iv-e-39`, `iv-e-40`, `iv-e-58`, `iv-e-19.*`, `iv-e-21.*`, `iv-e-63`, `fe-s-5.*`,
`fe-s-25/state-planes.test.ts`). `fe-s-25/absent-vs-null.test.ts` fails 0/3 on this worktree on a
pre-existing baseline defect in `contracts/adapt.ts`/`contracts/envelope.ts` -- confirmed
unrelated (`git diff --stat HEAD -- contracts state` prints nothing) and out of this cell's
`<paths>` grant; filed as row `DSGN_IRPTV1-W35-S3`.

`bun run typecheck` (`tsc -b --noEmit`): clean. `bun run lint`: 0 errors, 198 pre-existing warnings
(react-refresh/only-export-components etc.), none new to this cell's files.
