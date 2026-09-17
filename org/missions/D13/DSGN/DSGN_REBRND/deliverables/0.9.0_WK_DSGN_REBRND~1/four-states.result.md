# RB-s-10 result -- the four designed states

TO `DSGN_REBRND.TO-RB-s-10` | worker `0.9.0_WK_DSGN_REBRND~1` | portal branch `wk-dsgn_rebrnd-1i`
Portal commit `a65b939a` on base `e216de95` (LOCAL, not pushed). Contract: `portal/DESIGN.md` C12, C3, C5.8.

**ORDER STATE: COMPLETE (Amendment 1).** RB10-AC2 read `RAW-REMAIN`. Its one remaining hit was an unrendered
`console.error` line outside `<paths>`, which I filed as BLOCKING row `DSGN_REBRND-W1-S32`. The issuer ruled that
row by retiring RB10-AC2 for RB10-AC2R, which excludes `console.*` lines and prints each exclusion. RB10-AC2R
reads `VERDICT: MIGRATED`. No portal file changed for the amendment, and no log message was edited.

## What was built

`portal/src/ui/components/states/` (new):

| component | state | form |
|---|---|---|
| `PanelEmpty` | EMPTY | one navy sentence naming what would appear; an optional detail line (#6B7280 on #FFFFFF, 4.83:1); an optional action |
| `PanelLoading` | LOADING | a skeleton (`lines` / `table` / `chart`) in `palette.lightGray`; `animate-pulse`, which becomes `motion-reduce:animate-none`; `role=status`, `aria-busy`; no spinner |
| `PanelError` | ERROR | a `status.danger` icon beside navy text: what failed, then what to do, then the cause once; a secondary-button retry where a retry can succeed; `role=alert` |
| `PanelNoPermission` | NO-PERMISSION | a navy lock and one sentence saying the viewer lacks access and who grants it; the frame is kept |
| `innermostCause()` | -- | returns the innermost stringified Error of a wrapped message chain, so a cause is shown once |

**Ground.** Every state paints its own `#FFFFFF` (`--bg-surface`) with navy ink (`--palette-navy`), exactly as
C12 fixes it. Most host panels on the rendered routes are still band-valued (C3 known divergence, rows
W1-S9 and W2-S5), so an inherited ground would have put navy on navy. This choice is row
`DSGN_REBRND-W1-S33`. `surface="panel"` adds the `#C4CBDB` hairline, so a state that stands on the canvas
is a panel, never a notice on the bare canvas. Output opacity is 1.0 throughout (C5.8).

Shared adapters now route through the states, so their existing callers migrate too:
- `components/ErrorMessage.tsx` renders `PanelError`;
- `ui/components/EmptyState.tsx`, the legacy API, renders `PanelEmpty`;
- `LoadingContent` and `LoadingContainer` render `PanelLoading`.

`LoadingSpinner`, `LoadingInline`, `LoadingOverlay` and `LoadingModal` are unchanged.

## What was migrated

56 files under `src/components` and `src/pages` (109 scripted edits, each asserting its exact match count),
plus the 4 shared files, `MarketPerformance/hooks.ts` (exposes `refetch`), and dead-import cleanup:

- **The six counted treatments.** The centred grey sentence, the two-line grey sentence, the bordered red
  error and the duplicated error string on the raw canvas each become exactly one state. So does the panel
  that rendered its header and then nothing: the Top and Bottom Performers cards now render EMPTY when no
  index has a return. The em-dash-filled table is not in the AC2 pattern set; see Not done.
- **Messages say which, in plain words.** For example: "No holdings for INT.", "No correlations for the
  selected tickers.", "Market returns could not be loaded." and "No index returns for the WTD period yet."
- **Errors that had been shown as EMPTY** now render ERROR. Four sites did this:
  - MarketRegimeIndicator's single "Unable to load" branch is split on whether a cause exists;
  - SentimentGauge splits on `aaiiError`;
  - InflectionInsightsPanel's six `isError` branches had used its local EmptyState;
  - YieldCurveTab's failed fetch had rendered its EMPTY sentence; it gained a `loadFailed` flag.
- **EMPTY treatments that had been shown as ERROR** now render EMPTY: `ErrorMessage` with "No ... data"
  on Valuation, ModelPortfolios, SummaryMetricsTable and FactorTiltOverviewPanel.
- **Loading branches adjacent to migrated sites** moved from `LoadingInline` to `PanelLoading`: HoldingsTab
  x2, SelectionTab, MarketRegimeModal, MarketRegimeIndicator, AdvisorAnalytics, ConsolidatedOverviewPanel
  x2, and Inflection x6.

**The duplicated message was an assembly bug.** `lib/dataLoader.ts:110` throws
`` `Failed to load market data: ${error}` ``, which stringifies the inner Error as "Error: ...".
`MarketPerformance.tsx:41` then prefixed the same wrapper again. The page now says "Market returns could not
be loaded." once, shows "Cause: Failed to fetch market returns from all available sources" once, and offers
"Try again" (react-query `refetch`). The request itself is unchanged.

## NO-PERMISSION -- the gap, recorded (row `DSGN_REBRND-W3-S1`)

`PanelNoPermission` is built, exported, and has **no consumer**, by the issuer's amendment. Every access
denial in `portal/src` today is non-rendering:
- `ProtectedRoute.tsx` has three `Navigate`-replace branches;
- `AdvisorPublicProfile.tsx` and `useTradeSubmissionState.ts` omit an element;
- `UploadPortfolioModal.tsx` fires one transient toast.

No access denial was re-routed. Whether NO-PERMISSION should become a rendered state at all is a product
decision for the CTO at L10, and this project is not chartered to make it. The census below prints
`designed_PanelNoPermission 0`, as intended.

## Criteria as run (verbatim invocations, final bytes)

| id | output (deciding line) | verdict |
|---|---|---|
| RB10-AC1 | `$ tsc -b --noEmit` / `rc=0` | PASS by output |
| RB10-AC2 (retired by Amendment 1) | `RAW-STATE-STRINGS: 1 across 265 files` / `VERDICT: RAW-REMAIN` | not an acceptance row |
| RB10-AC2R | `RENDERED-STATE-STRINGS: 0 across 0 file(s)` / `EXCLUDED ...: 1` (TimeMachineProvider.tsx:42) / `VERDICT: MIGRATED` over 265 files | PASS by output |
| RB10-AC3 | `LOC : /positioning` / `CANVAS: rgb(244, 246, 250)` / `rc=0` | PASS by output; PNG read |
| RB10-AC4 | `LOC : /market` / `CANVAS: rgb(244, 246, 250)` / `rc=0` | PASS by output; PNG read |
| RB10-AC5 | judgment -- recorded below | UNVERIFIABLE-BY-INSTRUMENT (3.0.0_SA_CVO at L9) |

**Typecheck control.** The instrument can fail. A planted `src/ui/components/states/__rb10_mutant.ts`
(`const x: number = 'not a number'`) gave `TS2322` and `rc=2`, and the file was then removed.

**AC2's one remaining hit.** `portal/src/context/TimeMachineProvider.tsx:42`,
`console.error('[TimeMachine] Failed to load restore points:', err)`. It is a log line, not a rendered state,
and `portal/src/context/` is not in `<paths>`. Inside the three granted directories the count is 0.

## Census (the order's "print the denominator")

`rb-s-10_census.py` is a text-level idiom census over `portal/src/**/*.tsx`. The before is read from git
objects at `e216de95`; the after is the worktree carrying `a65b939a`. Output is in `rb-s-10_census.json`.
**Denominator: 264 .tsx files before, 265 after.** The denominator certifies the sweep, not that the pattern
list is complete.

| category | before | after |
|---|---|---|
| ac2_raw_state_strings (the criterion's 4 patterns) | 143 in 57 files | 1 in 1 file |
| empty_sentence_no_x (`'No <word>` / `>No <word>`, ad-hoc and designed alike) | 130 in 77 | 132 in 77 |
| error_red_ink_or_tint (`text-red-300/400/500`, `bg-red-500/N`, `text-danger`) | 208 in 61 | 196 in 56 |
| error_could_not_load_text | 10 in 4 | 4 in 3 |
| loading_spinner_component (`<LoadingInline/Spinner/Modal/Overlay`) | 50 in 29 | 36 in 23 |
| loading_animate_spin | 29 in 21 | 29 in 21 |
| loading_text (`Loading...`) | 5 in 4 | 3 in 3 |
| no_permission_text | 2 in 2 | 3 in 3 |
| designed PanelEmpty / PanelLoading / PanelError / PanelNoPermission | 0 / 0 / 0 / 0 | 73 / 17 / 29 / 0 |
| adapter ErrorMessage / EmptyState / LoadingContent+Container | 7 / 15 / 15 | 0 / 3 / 14 |

How to read it:
- `empty_sentence_no_x` rises by 2 because the designed EMPTY messages open "No ..." too.
- `error_red_ink_or_tint` is dominated by data colouring (negative returns, and "danger" accents on
  performer cards), not error states. It is printed so the reader can see it was looked at.
- The 36 remaining spinner uses are the declared exclusion below.

## Rendered evidence (read before this report)

- **`rb-s-10_positioning_empty_1440.png`** (AC3). Portfolio Composition and Holdings Breakdown each render
  EMPTY, "No holdings for INT.", navy on a white well inside the band-valued panel. The frame and size are
  kept: 400px and 128px, as before.
- **`rb-s-10_market_error_1440.png`** (AC4):
  - The tab body renders one ERROR standing as its own hairline panel: danger icon, "Market returns could
    not be loaded.", the hint, the cause once, and "Try again". Nothing repeats, and no red text sits on
    the canvas.
  - U.S. Regime renders ERROR with its 401 cause.
  - Bullish, Bearish, Top Performers, Bottom Performers and Daily Cloud each render EMPTY.
- **Before, same routes, on `e216de95`:** `rb-s-10_market_error_before_1440.png` shows the duplicated red
  string on the canvas, the performers cards with a header and then nothing, and "Unable to load" in grey on
  navy. `rb-s-10_positioning_empty_before_1440.png` shows "No holdings data available" in grey on navy.

## RB10-AC5 (judgment) -- recorded, no verdict

For 3.0.0_SA_CVO at L9, graded from the renders and the census:
- every panel with nothing to show uses exactly one of the four states;
- the message says which in plain words;
- no message repeats itself;
- no error is painted on the bare canvas.

The evidence is the two after-renders against the two before-renders, and the census table. Every AC2 site
in the granted directories migrated. The panel-level residue is listed under Not done.

## Rows filed

- `DSGN_REBRND-W1-S32`: BLOCKING, ARMED; disarm owner `2.0.0_SA_COO~D`. RB10-AC2 is unsatisfiable inside
  the grant because of the one hit in `portal/src/context/`.
- `DSGN_REBRND-W1-S33`: OBSERVATION, INERT. Each state paints its own white ground; the order did not say
  to, and C12's navy-on-white requires it while host panels are band-valued.

## Not done (declared, with reason)

- **`TimeMachineProvider.tsx:42`**: a log line outside `<paths>`, left untouched. Row W1-S32 was ruled by
  Amendment 1, and RB10-AC2R excludes this line and prints it.
- **36 spinner-component uses and 29 `animate-spin`** outside the migrated sites were not converted. Most
  are `LoadingInline` inside buttons, modals and small inline contexts, not panel loads. Where the load
  WAS a panel's, only the branches adjacent to AC2 sites were moved. A full LOADING sweep is its own
  census-sized change.
- **The em-dash-filled table** (one of the six counted treatments) is not reached by the AC2 patterns, and
  was not searched for separately.
- **Failure-swallowed-as-EMPTY**: not censused beyond the four sites found while migrating.
- **Red and translucent idioms inside host panels** that are not state renderings: they belong to other
  cells (C5.8 and C6 migrations).
- **Dev server**: stopped (0 listeners on 5188) before this report.
