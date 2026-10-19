# PROD promote payload -- the dell2 portal set, recut onto PROD (Andrew-direct 2026-10-19)

**Issuer:** 2.0.0_SA_COO~D2 (the IRPT_DASHBD issuer; no task order: an Andrew-direct act relayed by the CTO, msgs 10707 and 10727). **Records:** `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261019_142xZ_PROMOTE_ALL_DELL2_PORTAL_WORK_TO_PROD.md` and `..._144xZ_ALL_HOLDS_LIFTED.md`.
**Candidate branch:** `cand/dell2/irpt-promote-all-dell2-ir-set-20261019`, head `6656627a` (two commits on origin/PROD `d729ee6d`: the Investor Reporting set `4766293f`, then the Trade Request set `6656627a` after the hold was lifted). **Source:** origin/DEV `f7074536`, file bytes written as DEV holds them.

## What it carries

48 files: 31 new, 16 modified, 1 deleted (one test file DEV removed with DB-b-309, whose assertion about the firm banner the new behaviour retires). The tree differs from origin/DEV in exactly 5 `src` files, all dell1's and all left out: `lib/cottonwoodTrend.ts`, `lib/trendGrouping.ts`, `pages/ModelPortfolios.tsx`, and the two files of `pages/SecurityAnalysis/__harness__/`. The Ticket Center analysis-request and meeting-request files are already byte-equal on PROD. The branch `cand/dell2/anlreq-commentary-always-requested` is NOT included (ruling `RULING_COMMENTARY_GAP_TWO_CAUSES_20261017.md`).

## Gates (run on the committed head in a workspace-layout worktree, 2026-10-19 ~15:0xZ)

| gate | result |
|---|---|
| typecheck (`tsc -b --noEmit`) | 0 errors |
| eslint on the 47 added or modified `.ts`/`.tsx` files | 0 errors, 54 warnings (the files are DEV's bytes, so no warning is new against DEV) |
| `bun test src/pages/InvestorReporting src/pages/TicketCenter` | 15 failing test names on the recut against 17 on DEV; NONE fails on the recut that does not also fail on DEV (the two only DEV fails are F45-AC9 and FE-s-90); the two Trade Request files alone: 18 pass, 0 fail |
| production build (`tsc -b && vite build`) | green, built in 18 s |
| payload list | the table below |

## Pages changed and their class

Investor Reporting > Performance tab and its report, export and print: **client-facing**. Ticket Center > Trade Request form: **client-facing**.

## Files (path under `src/`, status against PROD, DEV commits over PROD touching it, newest such DEV commit)

| path | status | commits | newest |
|---|---|---|---|
| `api/endpoints/tickets.ts` | modified | 3 | b8f78379 |
| `pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-112.firm-binding-said-in-words.test.tsx` | deleted | 2 | 23a95f72 |
| `pages/InvestorReporting/__tests__/dsgn-irptv1/iv-t-2.headline.test.ts` | modified | 1 | b16965e5 |
| `pages/InvestorReporting/__tests__/fe-s-10/parity.test.ts` | modified | 1 | 25696621 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/dashboard-chart-breaks.test.ts` | new | 1 | c95a3d65 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/disclosure-placeholder.test.tsx` | new | 2 | cf141157 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/performance-headline-order-and-money.test.tsx` | new | 1 | 23a95f72 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/performance-holdings-panels.test.tsx` | new | 3 | 1f525845 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/performance-print-fresh-window.test.tsx` | new | 1 | 23a95f72 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/performance-tab-global-and-firm.test.tsx` | new | 2 | 75a71ae3 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/performance-template-firm-gate.test.tsx` | new | 2 | 25696621 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/performance-template-states.test.tsx` | new | 1 | 23a95f72 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/report-export.test.tsx` | new | 5 | f6833785 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/report-render-fixes.test.tsx` | new | 6 | 5907b695 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/report-render-r103.test.tsx` | new | 4 | dba19069 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/report-render-r104.test.tsx` | new | 5 | 5907b695 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/report-render-r105.test.tsx` | new | 3 | f6833785 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/report-render-r106.test.tsx` | new | 4 | 5907b695 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/report-render-r107.test.tsx` | new | 2 | ca3f080d |
| `pages/InvestorReporting/__tests__/irpt-dashbd/report-render-r109.test.tsx` | new | 3 | 5907b695 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/report-render-r110.test.tsx` | new | 2 | 6a37d883 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/report-render-r111.test.tsx` | new | 1 | 6a37d883 |
| `pages/InvestorReporting/__tests__/irpt-dashbd/report-tab.test.tsx` | new | 4 | dba19069 |
| `pages/InvestorReporting/dashboard/DashboardPerformance.tsx` | modified | 4 | 588d869e |
| `pages/InvestorReporting/dashboard/report/PerformanceReport.tsx` | new | 6 | f82cd241 |
| `pages/InvestorReporting/dashboard/report/ReportChart.tsx` | new | 2 | b167ce67 |
| `pages/InvestorReporting/dashboard/report/contractMembers.ts` | new | 1 | 3c423b41 |
| `pages/InvestorReporting/dashboard/report/fixtures/syntheticReport.ts` | new | 3 | d12a46b9 |
| `pages/InvestorReporting/dashboard/report/reportModel.ts` | new | 12 | 6a37d883 |
| `pages/InvestorReporting/export/Preview.tsx` | modified | 3 | 23a95f72 |
| `pages/InvestorReporting/header/HeaderSelectionContext.ts` | modified | 2 | 23a95f72 |
| `pages/InvestorReporting/index.tsx` | modified | 2 | 23a95f72 |
| `pages/InvestorReporting/render/PrintEntry.tsx` | modified | 3 | 23a95f72 |
| `pages/InvestorReporting/render/clientreport/ClientReportDocument.tsx` | modified | 1 | f6833785 |
| `pages/InvestorReporting/render/disclosurePlaceholder.ts` | new | 1 | f6833785 |
| `pages/InvestorReporting/render/manifest.ts` | modified | 1 | 14443687 |
| `pages/InvestorReporting/render/performance/report/PerformanceReportDocument.tsx` | new | 9 | f6833785 |
| `pages/InvestorReporting/render/performance/report/documentSheets.ts` | new | 11 | f6833785 |
| `pages/InvestorReporting/tabs/reporting/AccountsTable.tsx` | modified | 1 | 23a95f72 |
| `pages/InvestorReporting/tabs/reporting/PerformanceHeadline.tsx` | modified | 1 | 23a95f72 |
| `pages/InvestorReporting/tabs/reporting/PerformanceHoldingsPanels.tsx` | new | 3 | 1f525845 |
| `pages/InvestorReporting/tabs/reporting/PerformanceTemplateView.tsx` | new | 3 | 23a95f72 |
| `pages/InvestorReporting/tabs/reporting/ReportingTab.tsx` | modified | 9 | 25696621 |
| `pages/InvestorReporting/tabs/reporting/currency.ts` | new | 1 | 23a95f72 |
| `pages/TicketCenter/TicketCenter.tsx` | modified | 15 | 4d4dc68c |
| `pages/TicketCenter/TradeRequestParts.tsx` | modified | 1 | c05e3dda |
| `pages/TicketCenter/__tests__/trade-form-upload.test.tsx` | new | 1 | c05e3dda |
| `pages/TicketCenter/__tests__/trade-request.test.tsx` | modified | 1 | c05e3dda |
