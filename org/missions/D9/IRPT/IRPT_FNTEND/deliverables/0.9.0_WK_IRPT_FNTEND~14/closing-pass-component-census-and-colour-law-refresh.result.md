# FE-s-64 result -- component census and colour-law scan, refreshed (RECORD; NO VERDICT)

This pass reads the COMMITTED tree at portal DEV `ddb172bf` (the hash `git -C portal rev-parse --short HEAD` printed in this worktree; workspace base CLOUD `fcf38f866b`) and nothing here reaches a live route. No portal file was written. The census script was run from a COPY (`census.ts`, beside this file); FE-s-11's committed `component-census.json`/`.md` were not touched.

## Refreshed census beside FE-s-11's

| vintage | COMPONENTS | REUSED | NEW | scanned | defined-not-imported | PRD reuse rows |
|---|---|---|---|---|---|---|
| FE-s-11 round 1 (`9e0370009f`, and F11-AC1 in its result file) | 65 | 27 | 38 | (not re-read) | 2 | 11 of 11 |
| FE-s-11 committed file at CLOUD `fcf38f866b` (re-run at FE-s-18, `899b41d773`) | 70 | 27 | 43 | 40 tree files + App.tsx | 0 | 11 of 11 |
| THIS pass (`ddb172bf`) | 73 | 28 | 45 | 41 tree files + App.tsx | 0 | 11 of 11 |

Printed by my run: `COMPONENTS: 73 (REUSED 28, NEW 45)` / `SCANNED: 41 tree files + src/App.tsx` / `DEFINED-BUT-NOT-IMPORTED: 0` / `PRD-REUSE-ROWS: 11 of 11 accounted`. rc=0.

NOTE the order's "65" is round 1; the file FE-s-11 has COMMITTED now says 70 (it was re-run by FE-s-18). Both baselines are set out above.

### ADDED / REMOVED

- REMOVED since round 1: none (0 of 65 baseline names absent; classification changes 0).
- ADDED since round 1 (8): `AnswerStatus` NEW, `AppliedBranding` NEW, `ExportModalPanel` NEW, `GenerateComposer` NEW, `PanelEmpty` REUSED, `ReceiptPanel` NEW, `RevisionIdentity` NEW, `UnnamedReasonCodeFlag` NEW. Five of these (`AppliedBranding`, `ReceiptPanel`, `ExportModalPanel`, `GenerateComposer`, `RevisionIdentity`) entered by the 65 -> 70 step; three since the committed 70: `AnswerStatus` (FE-s-30), `PanelEmpty` (REUSED, `@/ui/components/states`, used in `tabs/analysis/VendorPdfPreview.tsx:11`), `UnnamedReasonCodeFlag` (`render/Page.tsx:115`, FE-s-40).
- The 73 -> 45 NEW / 28 REUSED split: REUSED names = CartesianGrid, CategoryViewTree, Cell, Combobox, ComboboxDescription, ComboboxLabel, ComboboxOption, Dialog, DialogActions, DialogBody, DialogTitle, Legend, Line, LineChart, PageHeaderCleanBadge, PageSurfaceControl, PageThemeProvider, Panel, PanelContent, PanelEmpty, PanelHeader, Pie, PieChart, RechartsTooltip, ResponsiveContainer, TabNavigation, XAxis, YAxis.

## The 45 NEW components: stated need, and the point a reviewer can dispute

The census script's own `reason` strings are mostly a role label ("FE-s-4 -- ...") rather than a need the existing set cannot meet. The reasons below are the worker's reading of each file's own header, offered for dispute; this pass did NOT search the wider portal for an equivalent beyond the census's 28 REUSED rows and the 11 PRD reuse rows, so "no existing equivalent" is NOT asserted.

Page-specific by subject (the need is the Investor Reporting domain itself; dispute = whether the portal already has a generic equivalent):
1. `InvestorReporting` (page shell), `InvestorReportingPrint` (print route `/investor-reporting/print`), `TabShell`, `ReportingTab`, `AnalysisTab`, `HoldingsTab` -- route/tab mount points. `TabShell` is a thin composition over the REUSED `TabNavigation`; dispute: is a wrapper a NEW component or reuse?
2. `ClientSearch`, `FirmDropdown`, `FirmAttribution`, `ScopeSummary` -- header. `ClientSearch` composes the REUSED catalyst Combobox and `FirmDropdown` composes the REUSED `PageSurfaceControl` (passing the Model Portfolios class string per its header); dispute: both are wrappers over reused parts, and the PRD row says the dropdown IS the Model Portfolios component.
3. `PeriodControls`, `PeriodResults`, `Summary`, `AccountDetail`, `CumulativeReturnChart`, `MethodsAndSources`, `MethodAndSources`, `Disclosures`, `PeriodInContextPage`, `PageSheet`, `PerformanceDocument`, `AnalysisDocument` -- the certified performance/analysis document and the on-screen Reporting tab. Need per their headers: landscape-letter and portrait-letter print templates with verbatim disclosures. Dispute: `MethodsAndSources` (print) and `MethodAndSources` (tab) are two near-named components for one subject.
4. `HoldingsSummary`, `DrillTree`, `SliceTable`, `InputReview`, `RequestList`, `StageDisplay`, `VariantSelector`, `VendorPdfPreview`, `NativeSections`, `GenerateComposer`, `RevisionIdentity` -- Holdings and Analysis tab bodies. Need per headers: model-led radial drilldown with a table equivalent beside every donut; analysis request/stage/variant flow. Dispute: `DrillTree` sits beside the REUSED `CategoryViewTree`.
5. `Metric`, `SourceValue` -- value rendering (one place, "so the rule is one rule"). Dispute: portal may already have a number formatter component.
6. `StatusPanel`, `AnswerStatus`, `UnnamedReasonCodeFlag` -- the status/availability face every tab and the export carries (FE-s-3/30/40). Dispute: the portal has a REUSED `PanelEmpty`/`Panel` set; this pass did not compare their states to these nine status labels.
7. `ExportButton`, `ExportAnchorSlot`, `ExportModal`, `ExportModalPanel`, `Preview`, `AppliedBranding`, `ReceiptPanel` -- export control, modal (built on the REUSED `Dialog*`), preview and receipt. `ExportAnchorSlot` finds a disabled control and portals into it (its own header). Dispute: `ExportModal`/`ExportModalPanel` are one file, and `ExportButton`/`ExportModalPanel` are counted with usedIn "(self -- no import statement)", which sits oddly with the script header's own import-only rule.

Census-record defect seen: `UnnamedReasonCodeFlag`'s recorded `reason` is `FE-s-4 -- the page frame both templates share: sheet, header, footer.` -- the same text as `PageSheet`, though the component is a reason-code flag (`render/Page.tsx:110-115`). Filed as a row.

## Tests run

- `F64-AC1` typecheck: `$ tsc -b --noEmit` then `rc=0`.
- `F64-AC2`/`AC3` census copy: rc=0, `COMPONENTS: 73 (REUSED 28, NEW 45)`.
- `F64-AC4` colour law: `SCANNED: 41 files`, `4 pass`, `0 fail`, rc=0.
- `F64-AC5` whole suite `src/pages/InvestorReporting`: `612 pass`, `22 skip`, `0 fail`, `Ran 634 tests across 114 files`, rc=0.
- `fe-s-11/census.test.ts` (not a criterion): `CENSUS DENOMINATOR: COMPONENTS: 70 (REUSED 27, NEW 43)`, `87 pass`, `0 fail`, rc=0. It PASSES because it grades FE-s-11's committed `component-census.json` (70), not the live tree (73), so it did not fail on the tree's movement. Filed as a row.

## F64-AC6 -- RECORDED, no verdict

Evidence is above. No verdict is given; graded at L9.
