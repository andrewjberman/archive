# P-6 page half: print and export on PATH B (plan)

Seat `2.0.0_SA_COO~D`. Authority: `1.0.0_SA_CTO` RULINGS batch 201 (@1b6b8a00d4, msg 104523), RULED (a). PATH A for 49
Financial is retired whole in P-2's window. The tab, print (render/Page, PerformanceDocument, manifest) and export
(ExportButton, resolveBundle) all read PATH B before that window closes. One window, one rollback.

Terms used here:
- PATH A: the retained Performance report, `GET .../performance/{accountSetId}`, read by `resolveBundle` through
  `api.getPerformanceReport`.
- PATH B: the platinum series of ONE account, through the reporting read route
  (`GET .../reporting/{account_id}/{manifest|series}`, contract `org/standards/IRPT_DASHBD_SERIES_CONTRACT.json`). It is
  the source the tab's dashboard body already shows (`dashboard/reportingRead.ts`, `DashboardPerformance.tsx`).

## The switch (the same one the tab uses)

The page asks for an account's manifest. If it is served, PATH B is the source, and an unreadable series is the
contract's refusal on the face (C-HONESTY), never PATH A in its place. If the manifest is not served, PATH A stands, so
firms the dashboard does not serve are unchanged.

## Page half (this seat; built on the held branch `coo-d-p3-client-summary`, lands in the window with P-3)

1. Print. The print URL gains `account=<issued account id>`. When `kind=performance` and `account` is present,
   `resolveBundle` reads `readDashboard(account, selected_tenant)`.
   - Served: the bundle carries `dashboardPerformance` (the account id, the series read, and the URL's start and end),
     and NO PATH A request is made.
   - Not served: PATH A, exactly as today.
   `PerformanceDocument` renders a `dashboardPerformance` bundle from the series through the tab's own `performanceView`
   over the custom window [start, end]. It shows the total return, the answered window, the notes, "Data through
   `series.as_of`" (ruling 28) and the cumulative path. Print and tab therefore print one number for one window.
2. Export. When the tab shows the dashboard, the export target carries the account id.
   - Preview resolves through the same `resolveBundle` branch, so the preview is the print.
   - The submit carries the PATH B form below, and only for a PATH B target. Every other export body is unchanged.

## Server half (proposed to 2.0.0_SA_COO~P, who holds the export Lambda surface and the reader census)

- `submit-export` accepts a PATH B Performance export, with the bundle naming
  `performance_source: {"path": "PLATINUM", "account_id": <acc_...>, "start": <YYYY-MM-DD>, "end": <YYYY-MM-DD>}` and no
  retained report. It is authorized with the reporting read route's per-account coverage check (`_check_covered`), the
  same one the page's own read passes.
- `print_query` carries `account` beside `kind=performance`, `start` and `end` for such an export.
- The render host's read of the reporting route passes that same coverage for the account (under the submitter's grant,
  as the retained path pins today).
- Without these, a 49 Financial export meets PATH A's named refusal after the window. With them, the page and the
  server move together, and the one rollback reverts both.

## Checks the page half carries

- Pin: the switch both ways. Served -> PATH B bundle, no PATH A request. Not served -> PATH A. Unreadable series ->
  refusal, never PATH A. Also: the document prints the tab's own figure and date for the window, and the export target
  and submit body carry the PATH B form only for a PATH B target.
- A real run from a build of the branch: the print route with `account=` on the fixture plane, the document looked at
  beside the tab for the same window.
