# What the Performance tab calls for a client, and what it does when a read fails -- 2.0.0_SA_COO~C2, 2026-10-17 ~01:2xZ

For `2.0.0_SA_COO~D2` (msg 10124; CTO msg 10123). Measured with `git show` on `cand/dell2/irpt-49f-performance-template-mount` @`1f525845` (paths under `portal/src/pages/InvestorReporting/`). No ids; no live call made. MEASURED = read from the code; the live route behaviour (what the Lambda returns for a missing object) is NOT read here.

## (1) The routes (all GET, all through `apiRequest` with the contract-version header, `dashboard/reportingRead.ts:59-60`)

| # | route (shape) | query | called by | needed to render a Cottonwood Performance body? |
|---|---|---|---|---|
| 1 | `/api/scoped/investor-reporting/reporting/{account_id}/manifest` (`reportingRead.ts:22-31`) | `selected_tenant=<tenant>` when known | `readDashboard` (`:124-148`), from `ReportingTab.tsx:595` for the focused account and, once one account is served, for each other listed account | YES, first. It is the switch: a served manifest is what shows the dashboard figure instead of the PATH A figure (`:8-10`). |
| 2 | `/api/scoped/investor-reporting/reporting/{account_id}/series` (same builder) | `selected_tenant`; `version_id` only for an export's frozen print | `readDashboard` after the manifest is served (`:141-145`); `readFrozenSeries` (`:107-122`) for the export/print reads the series ALONE, on a render token the edge admits on the series route only | YES, second. The body draws from it. A series that cannot be read is shown as the contract's refusal on the face (`:141-146`), not as the PATH A figure. |
| 3 | `/api/scoped/investor-reporting/reporting/client/{client_id}/summary` (`:38-41`) | `selected_tenant` | `readClientSummaryAnswer` (`:78-93`), from `ReportingTab.tsx:635`, only when the client lists more than one account | NO. It feeds the picker's per-account YTD line only; absent/refused falls back to the per-account manifests (`ReportingTab.tsx:648-660`), so the first Cottonwood cut can omit it and pay for it in extra manifest requests (two at a time once one account is served). |
| 4 | `/api/scoped/investor-reporting/reporting/client/{client_id}/report` (template read, `tabs/reporting/PerformanceTemplateView.tsx`, `clientReportPath`) | `selected_tenant` | `PerformanceTemplateView`, mounted ONLY when `clientFirmId === '49financial'` (`ReportingTab.tsx:938`) | NO for Cottonwood: the block does not mount for it (CTO ruling 9934). |

Not on this function: the holdings snapshot (`getHoldingsSnapshot`), the PATH A `/performance` and `/selections` reads, the export submit. The Cottonwood body needs only routes 1 and 2, plus the snapshot for the holdings panels (a different route).

## (2) Is a 404 or a refusal from a second function page-visible?

Booleans, from the code:
- A thrown error (HTTP 404, 502, non-JSON): `readDashboard` catches it and returns `absent` with the `public_reason_code` parsed from the error text, else `null` (`reportingRead.ts:71-75`, `:133-136`). Page-visible difference from a refusal: NO. Both are `absent`, and the PATH A figure stays.
- A refusal envelope (`ok:false` + `public_reason_code`, for example OBJECT_NOT_COVERED, NOT_READY): `absent` with the code (`:62-69`, `:137-138`). The page has no per-code behaviour here; only the old FIRM_BINDING banner read the code, and DB-b-309 removed it. So a router that returns 404 for an unmapped firm instead of the estate envelope is invisible to the page, as is a second function behind it.
- Two page-visible exceptions a router MUST preserve: (a) the SERIES response keeps `Content-Encoding: gzip` (the browser inflates it, `:3-5`); (b) a manifest that is served but unreadable gives `absent` / `MANIFEST_UNREADABLE`, and a series that is served but unreadable gives a visible contract refusal on the face, so a router must not turn a good series into an envelope or the reverse. Also pass through `selected_tenant`, `version_id`, and the contract-version request header; the render-token admission on the series route is the edge's, not the page's.
- NOT read here: what the existing Lambda returns for an account whose firm is not in its directory map (the CTO traced it to the single-firm map). If it returns a 200 envelope `ok:false` or a 404, the page treats both the same (above).

## One consequence for the plan

Because every failure is `absent` and falls back to the PATH A figure, a Cottonwood client with NO PATH A report would render the empty Performance body Andrew saw (INFERRED: this seat did not read whether PATH A serves Cottonwood; the code path is as stated). The first Cottonwood cut (routes 1 and 2) turns that into the dashboard figure with no page change; the page needs a cell only for words on a still-`absent` body (outside this file).
