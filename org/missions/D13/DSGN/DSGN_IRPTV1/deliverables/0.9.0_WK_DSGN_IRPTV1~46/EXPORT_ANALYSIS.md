# TO-IV-e-85 -- Export on the Analysis tab (FWD-9, row W35-S2)

Finding: NEEDS_SERVED_ROUTE. Product files changed: none. Rows: DSGN_IRPTV1-D2-W46-S2 (the missing served identity), S3 (grant names a file that does not exist).

## How the header's Export gets a target on each tab

- The one Export control is built in `index.tsx:312` from `exportKind` (`index.tsx:64-68`: reporting = performance, holdings = null, analysis = analysis) and, on Performance only, from a target the tab publishes up.
- Performance: `ReportingTab` calls `onExportTarget` (`ReportingTab.tsx:783-793`). The target carries the report's own `retainedReport` id and revision (`:268-277`); it is null when the report is not answer-bearing. `TabShell.tsx:160` passes `onReportingExportTarget`; `index.tsx:216` stores it, `:293` and `:299` read it on the reporting tab only, and `:316-332` feed it to `ExportButton`.
- Holdings: no export kind (`index.tsx:66`), so the header shows the disabled control.

## Why the Analysis tab supplies none

- `AnalysisTabProps` (`AnalysisTab.tsx:70-103`) has no export prop, `TabShell.tsx:164-172` mounts it without one, `index.tsx` holds no state for one, and `index.tsx:311` keeps the Analysis gate permanently closed (row W35-S2 at IV-e-57). `AnalysisTab.tsx:430` only says the header's Export targets this tab.
- Adding a prop would not be enough. The server resolves exactly one retained report by `authorized_report_revisions[0].report_id` and `.revision` (`export/retained_export.py:95-99`) and pins it as `analysis_report_ref` (`export/submit_service.py:71-76`). Performance serves that identity as `retained_ref` (`contracts/wire/PerformanceReport.ts:64-68`). The Analysis wire (`contracts/wire/AnalysisReport.ts`) and the owned-history view (`contracts/index.ts:1408-1412`, state at `OwnedRequestHistory.tsx:236`) carry request id and attempt id only.
- With no override, `index.tsx:319` would name the client scope revision as the report ref, which is not a retained report id. `ExportButton.tsx:239` also never uses `buildAnalysisSubmitRequest` (`export/submit.ts:116`) and no production file sets `analysisReportRef` (`contracts/adapt.ts:1575`).

## What is missing

A served member on the Analysis report response for the request shown: the retained report's `report_id`, `revision`, `sha256` and `report_kind` ANALYSIS. The CTO rules the route and which of the tab's report sources Export follows (the legacy request list is refused live at `api/endpoints/investor-reporting.ts:1274`; the report the advisor sees after Generate lives in the owned-history dialog).

## Not established

Whether the producer already holds an Analysis retained id that a route could return (no handler returns one today); whether the server refuses a live Analysis export through the current button (no AWS call, no dev server).
