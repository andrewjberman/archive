# DB-c-23 -- what the page says about coverage today (FWD-10, round 145)

Worker 0.9.0_WK_IRPT_DASHBD~415, branch wk-IRPT_DASHBD-415. Read of the code only: no write, no AWS call, no run, no network.
Record: COTTONWOOD_SCREEN_COVERAGE_READ_R145.json (same folder). Claim: inferred.

## The four ACCEPT cases

| case | verdict | on the page today |
|---|---|---|
| partial_history_account | EXPLAINED | Dashboard note under the headline when history_scope is not FULL (DashboardPerformance.tsx:147). Report path has no history member. |
| day_not_measured | EXPLAINED | Dashboard counts non-MEASURED window days and prints one sentence per state (DashboardPerformance.tsx:141-146, tooltip :160). |
| fallback_day | NOT_REACHED | No fallback state exists: PRD v0.4 ruling 17 withdrew it; return_basis is TWR or NOT_MEASURABLE only. |
| window_before_news_data | NOT_REACHED | No news or market-history state on the tab. The sentence "Market history is not available before" prints only in the export document, when includeNarrative is set (PerformanceDocument.tsx:198). The account-history start IS explained (DashboardPerformance.tsx:104, 122). |

## Label

MethodAndSources.tsx still contains the literal "Time-weighted, net of fees" (line 25, inside a comment). The rendered label is
composed from RETURN_METHOD_WORDS and FEE_BASIS_WORDS (lines 33, 37), so a net payload reads "Time-weighted, net of fees."
It sits under the Report details disclosure (ReportingTab.tsx:922-930) and never on the dashboard path (ReportingTab.tsx:906-912).

## Eight members

Sentence on the dashboard screen: 3 of 8 (PARTIAL_HISTORY, FLOW_UNRECONCILED, SOURCE_LAG).
Sentence in the export document only: 1 of 8 (MISSING_HISTORY, narrative path).
No sentence on any screen: 4 of 8 (FULL is suppressed, NO_LOTS, UNCLASSIFIED_HOLDINGS, FEE_RAIL_UNUSED is mapped but never called).

## Cottonwood

cottonwood_account_dim.py assigns coverage (lines 137, 139, 141). cottonwood_report_reader.py assigns none. The value reaches no
page. The Cottonwood partial-history flag the page reads comes from cottonwood_bd_account_return_daily.py:372.

## Premise drift

- PRD C-LABEL cites holdings_gold.py:259 for TIME_WEIGHTED and NET. The file has no such constant there; the label is set at
  line 306 as TIME_WEIGHTED, GROSS. Filed as IRPT_DASHBD-D2-W415-S1.
- The PRD's "news data" (FWD-10) and "news history" (FWD-6) name different states; see row S2.

Rows filed: IRPT_DASHBD-D2-W415-S1 to S6 (investigation channel, INVESTIGATION_v1.md).
