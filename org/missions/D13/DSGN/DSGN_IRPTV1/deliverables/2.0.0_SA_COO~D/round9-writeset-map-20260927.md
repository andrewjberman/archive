# DSGN_IRPTV1 -- round-9 prep: read-only write-set map at local portal DEV 3b98939b (issuer, 2026-09-27 ~21:2xZ)

Input for the round-9 cut after the round-8 L10. Items: PRD v0.18 UI CLEANUP FINDINGS (UIC-01..23, DSGN's 20; UIC-06 is ~P's,
UIC-15/16 ~M's), row S26, the UIR-45 residue, UIR-40, and the Analysis Export signal (W35-S2). Paths under portal/src/; IR =
pages/InvestorReporting. File:line facts from a read of 3b98939b.

| item | files (key lines) |
|---|---|
| UIC-01 | IR/tabs/reporting/PerformanceHeadline.tsx metricText :73, values :103-108, Tiles :156-161 |
| UIC-02 | IR/tabs/reporting/PerformanceChart.tsx per-day table :125-143 |
| UIC-03 | IR/tabs/reporting/AnswerStatus.tsx :36, :84-112; MethodAndSources.tsx :39-67 (in ReportingTab "Report details" :606-614) |
| UIC-04 | IR/tabs/reporting/AccountsTable.tsx :47-63, :155-199; ReturnsHeatmap.tsx ReturnCell :43-56 |
| UIC-05 | IR/tabs/reporting/ReportingTab.tsx YTD effect :446-466, :592; IR/tabs/holdings/AccountFilter.tsx :126-132, :269 |
| UIC-07 | IR/tabs/reporting/period.ts SINCE_INCEPTION_START :38, :95; ReportingTab.tsx :478 (no contract carries an inception date) |
| UIC-08 | ReportingTab.tsx WORDED_REFUSAL_WORDS :252, ReportingRefusal :315-336 |
| UIC-09 | IR/tabs/StatusPanel.tsx :62, :73; IR/state/status.ts :140, :342, :484-496 |
| UIC-10/11/12 | IR/tabs/holdings/DrillTree.tsx :162-186, :220, :349, :562, :704; palette.ts ACCOUNT_PALETTE :40-55 (14 greys); slices.ts :583; SliceTable.tsx |
| UIC-13 | IR/header/IdentityCard.tsx account list :560-589 inside Panel overflow-hidden :497 |
| UIC-14 | IR/tabs/holdings/slices.ts holdingsFooterSource :344-348 (AllocationBars :305, HoldingsTreemap :560, SecurityList :291); PerformanceHeadline.tsx :129-131 |
| UIC-17 | IR/header/ScopeSummary.tsx :104-106; cause contracts/adapt.ts adaptResolvedScope :731-740 (businessAsOf never passed) |
| UIC-18..22 | IR/tabs/analysis/composer.ts :159-168, :244-250; GenerateComposer.tsx :256, :288-297, :353-357, :428-435, :469-509; VariantCards.tsx :87-90; AnalysisTab.tsx :157-171 |
| UIC-23 | IR/tabs/analysis/OwnedRequestHistory.tsx :75-80, :204, :219 (owner scoping is server-side) |
| S26 | contracts/envelope.ts parseIrEnvelope :321 (data required; public-status.ts :20-42 still binds); api/endpoints/investor-reporting.ts submitExport :1212-1227 (+ interface :826, fixture :1524), getExportReceipt :1229; IR/export/submit.ts interpretSubmitExportAnswer :363-382 (unused), SubmitOutcome :149-165, flowAcked :324; IR/export/ExportButton.tsx handleSubmit :213-232 |
| UIR-45 residue | IR/tabs/reporting/PerformanceControls.tsx :136-146 prints raw requested/actual dates |
| UIR-40 | the band colour rgb(10,23,51) is --bg-header (index.css :366, :377), painted by ui/components/panels/PanelHeader.tsx :62 and PanelFooter.tsx :92 (shared across the portal) in IdentityCard :498, AllocationBars :259/:305, HoldingsTreemap :473/:560, SecurityList :201/:291, PerformanceHeadline :135/:180, PerformanceChart :82 |
| Analysis Export signal | AnalysisTab.tsx (report :116 is always null live; listAnalysisRequests rejects, investor-reporting.ts :1150), TabShell.tsx :55, :164; index.tsx gate :270, ExportButton :272-291; submit.ts buildAnalysisSubmitRequest :100 |

**Shared files (chain edges):** GenerateComposer.tsx and composer.ts (UIC-18..22); ReportingTab.tsx (UIC-03/05/07/08);
PerformanceHeadline.tsx (UIC-01/14, UIR-40); PerformanceChart.tsx (UIC-02, UIR-40); IdentityCard.tsx (UIC-13/17, UIR-40); DrillTree.tsx
(UIC-10/11/12); slices.ts (UIC-12/14); AllocationBars / HoldingsTreemap / SecurityList (UIR-40, UIC-14); PerformanceControls.tsx (UIR-45,
UIC-05/07); AnalysisTab.tsx and OwnedRequestHistory.tsx (UIC-22/23, Analysis signal); ExportButton.tsx and submit.ts (S26, Analysis
signal); StatusPanel.tsx and state/status.ts (UIC-09, S26 display); PanelHeader/PanelFooter (UIR-40, portal-wide).
