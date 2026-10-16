# Does the Performance tab still render an Inflection client's PATH A performance on 75a71ae3? -- 2.0.0_SA_COO~C2, 2026-10-16 ~22:2xZ

Asked by the CTO (msg 9927). Booleans first; evidence below; claim words: MEASURED = read from the branch (`git show`/`git diff origin/DEV...cand/dell2/irpt-49f-performance-template-mount`, head `75a71ae39089`), INFERRED = from the code, not run against a login. This seat has no staff login on 5174, so nothing here is a live render.

| question | answer | claim |
|---|---|---|
| Did DB-b-309 turn the PATH A body into a worded-absent? | NO | MEASURED |
| Is the PATH A branch (`answer && report` -> `PerformanceHeadline`, `PerformanceChart`, monthly/accounts) changed on the branch? | NO (the diff of `ReportingTab.tsx` against origin/DEV touches only: the import and mount of `PerformanceTemplateView`, the removal of the firm-binding banner, `dashboardTenant` and the focus context taking `header?.selectedTenant` first) | MEASURED |
| Does the PATH A request change for an Inflection client? | Only its `selected_tenant`: `header?.selectedTenant ?? scope.registryTenant`. `selectedTenantFor` returns `scope.registryTenant` unless the Global firm context for the picked client's firm exists, so for a single-firm login the value is the same as before | MEASURED (code) / INFERRED (that Andrew's Global login resolves the same tenant) |
| Do the tests that exercise PATH A still pass? | the whole `InvestorReporting` suite has the identical failing-name set (51) on the branch and on origin/DEV `fcbf2bce`; no PATH A test is in the difference | MEASURED earlier today |
| Is the template mount limited to 49 Financial (CTO msg 9927: "the template mount is the 49 Financial template only")? | NO. `PerformanceTemplateView` is mounted unconditionally at `ReportingTab.tsx:931` for any selected client; `firmId` is only used for the report's title (`PerformanceReport.tsx:159`); no firm test exists in `PerformanceTemplateView.tsx` | MEASURED |

## The consequence (a defect against the CTO's stated intent, not a PATH A regression)

For an Inflection client (no filled report), the template block prints UNDER the PATH A performance: in the dev server (`!import.meta.env.PROD`, port 5174 included) a failed read falls back to the fixture, so the page shows the "SYNTHETIC PREVIEW" banner and the 49 Financial synthetic report with Inflection's name; in a production build it prints the sentence for the read's reason (for example "The performance report for this client is not published yet."). Both appear on the Inflection page. Cottonwood has served filled-report objects, so its block is a real report; 49 Financial likewise.

## Correction after the CTO's ruling (msg 9934, 22:09Z)

The paragraph above and the recommendation below treated Cottonwood as serving a filled report because its GOLD `filled_report_values` table holds 65 partitions. That is the producer's input table, not the served report the route reads; `~D2` measured (msg 9901) that no Cottonwood filled report is served. The CTO ruled: the block mounts for 49 Financial only, Cottonwood joins when its filled report is served, Inflection never. The ruling stands; the "in" reading below is withdrawn.

## What I recommend (for `2.0.0_SA_COO~D2` to fix before Andrew's smoke; a page cell, not this seat's open cell)

Gate the mount in `ReportingTab.tsx:931` on the firms that serve a filled report (49 Financial and Cottonwood, measured above: 65 Cottonwood partitions; the 49 Financial template is the one DB-b-307 built); every other firm mounts nothing, so an Inflection client shows its PATH A performance and nothing else. One test pins it: Inflection firm -> no `template-words` and no `synthetic-preview-banner` in the markup; the positive control is the 49 Financial markup, which has them. CTO decides whether Cottonwood is in or out of the gate; this seat's reading is "in" because its served report exists and renders through the same template.
