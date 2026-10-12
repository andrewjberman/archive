# IB160-3 -- the pages that render the performance route's returns (TO-IB-pr-466, a code read)

Base `7c00a44b5ab2a1cb5259fe5bed4e9acb5cc63a40`. Portal read at `C:/dev/ajb_workspace/portal/`, commit `dbeb6764eaa688230f44cfcc1763bd73db6e1142`: another checkout at its own commit, possibly ahead of or behind what is served, and its working tree may differ from that commit. No page opened, no sign-in, no API call, no product file edited.

Route: `GET /api/scoped/investor-reporting/performance/{accountSetId}` (routes.json:61; entry.py:311). Wire body: `{**report, retained_ref?, _status}` (entry.py:301).
Members: `claim` = `optional_facts.value_facts.claim` (holdings_gold.py:291/295); `days_excluded` = `optional_facts.value_facts.days_excluded` (holdings_gold.py:274); `absences` is NOT on the wire (holdings_gold.py:342 returns it, entry.py:301 drops it), only a state `_status.state` PARTIAL / `PERFORMANCE_PARTIAL` (entry.py:279-288). None of the three is a named member in PerformanceReport.schema.json (value_facts is an open object, :332-338).

Subtraction: 156 files name the route, client function, wire type or a member (12 patterns, in the json). 9 render + 12 fetch_or_adapt + 135 neither = 156. Nine more render files name none of the patterns and were found by following the data (listed in the json).

## Pages (the three "shows" columns first)

| shows_claim | shows_absences | shows_days_excluded | page or component | code_line | what it renders | firms |
|---|---|---|---|---|---|---|
| not shown | state only: amber left border when PARTIAL (:877-879); no list | not shown | Reporting tab body (PATH A) | tabs/reporting/ReportingTab.tsx:875 | container; fetch at :751; replaced by the dashboard (another route) when pathBServes (:748) | internal-tier admins with dev (App.tsx:462) |
| not shown | "Partial" + "Qualified answer -- not a complete report" (:89-96); code and reason in data attributes only; inside a closed `<details>` | not shown | AnswerStatus | tabs/reporting/AnswerStatus.tsx:52 | state word, business date | same |
| not shown | state and reason code in the panel help tip only (:154-155) | not shown | PerformanceHeadline | tabs/reporting/PerformanceHeadline.tsx:97 | period return, benchmark, ending and beginning value, answered window | same |
| not shown | not shown | not shown | PerformanceChart | tabs/reporting/PerformanceChart.tsx:81 | cumulative line from the daily series | same |
| not shown | not shown | not shown | ReturnsHeatmap (closed disclosure) | tabs/reporting/ReturnsHeatmap.tsx:78 | period returns by label | same |
| not shown | not shown | not shown | AccountsTable (closed disclosure) | tabs/reporting/AccountsTable.tsx:117 | per-account return and value; uncovered accounts | same |
| not shown | not shown on the face (state in a data attribute only) | not shown | MethodAndSources (tab) | tabs/reporting/MethodAndSources.tsx:89 | method and source in words | same |
| not shown | not shown | not shown | PerformanceControls | tabs/reporting/PerformanceControls.tsx:72 | period picker, requested vs answered window | same |
| not shown | not shown (PARTIAL reads as a plain value) | not shown | Account picker YTD suffix | tabs/reporting/ReportingTab.tsx:341 | one account's YTD return per account, own call at :350 | same |
| not shown | "Report state: Partial -- Qualified -- not a complete report", then the date, then "Reason: PERFORMANCE_PARTIAL", on every printed page | not shown | Print band (ReportStateBand) | render/Page.tsx:313 | state band on each print page | print route App.tsx:614, same three requirements |
| not shown | not shown | not shown | Print Summary / PeriodResults / AccountDetail / CumulativeReturnChart | render/performance/Summary.tsx:41 | answered period, values, return, tables, chart | same |
| not shown | state, partial reason and reason code in the "Report availability" row (:169-190); no list | not shown (window notes compare dates by the trading calendar) | Print Methods and sources | render/performance/MethodsAndSources.tsx:73 | method, window, source, availability | same |
| not shown | not shown | not shown | Print "The period in context" (narrative toggle) | render/narrative/PeriodInContextPage.tsx:90 | narrative and series chart | same |

## What the adapter drops

`adaptPerformanceReport` (contracts/adapt.ts:767-843) reads `value_facts` only for `period_start`, `period_end`, `currency` (:797-799) and `beginning_market_value`, `ending_market_value` (:839-840). So `days_excluded`, `claim`, `missing_trading_days`, `days_linked`, `days_observed`: dropped. `absences`: nothing on the wire to keep. The state and reason code: kept as `availability` (adapt.ts:305-337, envelope.ts:386). The producer writes `start_value` / `end_value` (holdings_gold.py:273), which the adapter does not read.

## By the code (not seen on a served response)

holdings_gold.py:308-313 adds three absences on every call, so entry.py:279 gives PARTIAL for every holdings-basis answer, whether or not a day was excluded. So the one trace of absences the screen can show does not distinguish a window with a non-OK day from one without.

## Not searched / not established

Other front ends; the server-side PDF or export path; the dashboard route family (PATH B), named not read; generated files beyond the wire type; the 135 neither files, placed by path. Not established: what is served today; what a signed-in user sees; which accounts get PATH B instead of this route's body; whether the served body carries `claim` and `days_excluded`.
