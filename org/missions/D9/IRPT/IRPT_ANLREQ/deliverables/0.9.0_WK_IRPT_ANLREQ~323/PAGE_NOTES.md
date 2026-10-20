# PAGE_NOTES -- run 7 browser leg, proved offline (0.9.0_WK_IRPT_ANLREQ~323, cell AR-y-454)

**Read this before the GO.** The page on the PROD tip cannot complete step B2 of ADDENDUM 9 section 2: it files the
ticket, but it never sends the analysis request. The live run must not be pressed until surprise row
`IRPT_ANLREQ-D2-W323-S1` (BLOCKING, ARMED) is dispositioned.

## 1. What was built and against what

- Tree: `portal` at `origin/PROD` `f48e09ddf95e` (worktree `C:/dev/wk-irpt-anlreq-323/portal`, node_modules linked).
- Build: `bun run build` (= `tsc -b && vite build --configLoader runner`), RC 0, 12.35 s. Output in `portal/dist`
  (gitignored in the portal submodule). Nothing was committed in the portal.
- Instrument: `run7_browser_leg.mjs` drives the page's own controls with `playwright-core` (Edge, headless) against
  the build served from disk. It copies `serveFromDist` from `portal/scripts/ui-dist.mjs` and imports nothing else
  from the portal tree. `--token-file` sends a real bearer as the session accessToken, the way ui-smoke `--token` does.
- Offline: no network, no AWS, no push, no deploy. Every API answer is in `fixtures_offline.json` (synthetic:
  household `E2E7 SYNTHETIC`, tickers `SYNTH-*`, values such as 12.5, request and ticket ids of the cell's shapes).
- Output contract: stdout carries closed lines only (B1, B2, B3, CALLS, B-LEG-*). No URL, token, header or file
  content is printed. `RUN7_DEBUG=1` adds page console lines and must not be set for the live run.

## 2. Accessible names (read at f48e09dd)

| step | control | accessible name / selector | source |
|---|---|---|---|
| board | button | `New Ticket` (toggles the New Ticket panel; not a route) | TicketCenter.tsx ~905-910 |
| type | select | options from `TICKET_TYPE_LABELS`; choose value `analysis_request` (label "Analysis Request"); the staff default is Service Request | TicketCenter.tsx ~812-822; api/endpoints/tickets.ts 17-23 |
| title | input | placeholder `Title (what is being requested?)`; no label | TicketCenter.tsx ~823-829 |
| Advisor | input | aria-label `Advisor`; placeholder `Advisor (optional)` for staff, `Advisor (required)` for partners | AnalysisRequestParts.tsx 186-187 |
| Firm | select | aria-label `Choose the firm this request is filed under` (empty first option, same words); shown only when the firm list loaded and is non-empty | AnalysisRequestParts.tsx 120-121, 188-193 |
| Household | input | aria-label `Household`; placeholder `Household (required)` | AnalysisRequestParts.tsx 198-199 |
| comparables | fieldset `data-slot="comparables"` | five checkboxes, names from `comparisonLabel(model)` of the five OPAL_MODELS; legend "Compare against (optional, at most 5 in total)" | AnalysisRequestParts.tsx 201-223; opalModels.ts 7-12 |
| Other ETFs | input | aria-label `Other ETFs`; the served catalogue is read only when it is typed in | AnalysisRequestParts.tsx 224-226 |
| Needed by | input type date | aria-label `Needed by` | AnalysisRequestParts.tsx 236-237 |
| holdings | input type file | aria-label `Holdings file`, accept `.csv,.xlsx` | AnalysisRequestParts.tsx 241-242 |
| submit | button | text `File Analysis Request`; reads `Uploading...` while creating and is disabled while held | TicketCenter.tsx ~880-886 |
| hint presses | buttons | `Yes`, `Replace` (reveals input `Replacement ticker for <symbol>` and button `Check`), `No`. No control reads Keep | AnalysisRequestParts.tsx 252-329 |
| row | buttons | `Claim` (open), `Request report` (`data-slot="request-report"`), `Retry analysis request` (`data-slot="retry-analysis"`), `Open report` (`data-slot="open-report"`, only when the ticket carries a report_ref), `Complete` | AnalysisRequestParts.tsx 400-434; TicketCenter.tsx ~971-998 |
| report | panel | `data-slot="opened-report"` with `data-state` ready or waiting; the sections are IRPT's RetainedSections; button `Close` | TicketCenter.tsx 211-226 |

The run7 script finds: `New Ticket`, the analysis type select (by its option value), the firm select (by its aria-label),
`Household`, the title by placeholder, `Holdings file`, `File Analysis Request` (exact), `button[data-slot="open-report"]`
on the row whose text holds the ticket id, and `[data-slot="opened-report"]`. A missing control exits `B-LEG-BAD <phase>`.

## 3. Call sequence observed offline (f48e09dd, fixtures_offline.json)

Board load (shell and board, before any form):
`GET /api/scoped/tickets?status=open`, `GET /api/scoped/tickets/metrics`, and shell reads (`GET /api/scoped/portal-content`,
`GET /api/scoped/advisor-intelligence/platinum/firm/*.json`), which the CALLS lines show and which are not the form.

Form open (staff): `POST /api/scoped/investor-reporting/directory/resolve` (Global context, read when the form opens;
read again on a re-render). The model catalogue is a static list: no call (AR-y-419). `GET .../analysis/comparisons` is
read only when Other ETFs is typed; not exercised.

B2 filing, as the page makes it:
1. `POST /api/scoped/investor-reporting/analysis/inputs` (upload; answer NORMALIZED). Observed.
2. `POST /api/scoped/tickets` (ticket create, source `ticketcenter:i1`). Observed; the ticket id comes back.
3. `POST /api/scoped/investor-reporting/analysis` (analysis submit). **NOT sent on f48e09dd** (surprise S1). The page
   shows `Analysis: FAILED - Invalid analysis submission request.` and the ticket stays filed with no report.
4. `POST /api/scoped/tickets/{id}/report` (record the REQ id on the ticket). Not reached.

B3 (Open report): `GET /api/scoped/investor-reporting/analysis/{requestId}/sections?selected_tenant=..&ticket_id=..`.
Observed in the positive standalone control; answered by the fixture.

## 4. Where the page differs from ADDENDUM 9 section 2 (the issuer reads these before the GO)

1. **B2 analysis step (BLOCKING, surprise S1).** The addendum says the page performs the upload and the analysis
   request. On f48e09dd it performs the upload and the ticket create, then refuses the analysis submit client-side:
   `analysisBody` adds `commentary_requested: true`, and `readSubmissionRequest` admits only the required keys plus
   `input_id` and `ticket_id`. The ticket is filed with no REQ id, no report_ref, and therefore no Open report control
   for B3. The Retry analysis request path calls the same submit (read from source; not exercised live). Under the
   addendum's own terms this is a STOP at B2 naming the page's words.
2. **Four writes, not three (surprise S2).** upload, ticket create, analysis submit, and the record of the report id on
   the ticket (`POST .../tickets/{id}/report`). The composite prints the names the page actually makes.
3. **No Keep control (surprise S3).** The symbol hint presses are `Yes`, `Replace` and `No`. The addendum's "no Keep"
   means no press of a hint control. These offline fixtures never produce a finding, so no hint control was shown.
4. **Submit label.** The press is `File Analysis Request`; the addendum's word "submit" is the same control.
5. **New Ticket defaults to Service Request for staff.** The operator chooses Analysis Request first (the addendum says
   the same, so this is a note, not a difference).
6. **Advisor.** Labelled optional for staff through the placeholder `Advisor (optional)`: matches B1.
7. **No report-type and no commentary control on the form.** Matches B1 (report_type=absent, commentary=absent).
8. **Firm chooser.** Lists three firms in the offline run: `49 Financial`, `Cottonwood Capital Advisors`,
   `Inflection Wealth Management` (the labels come from `firmDisplayNameFor` because the fixture scope names none).
   The PROD labels may differ; not checked live.
9. **Models.** Five at first paint (static list, no call). Matches B1.
10. **Holdings bytes.** The page reads the file in the browser and sends its bytes in the upload body. The addendum's
    "sha256 printed" is the operator's step: this script prints no file content and no hash.
11. **B3 needs report_ref.** Open report exists only on a ticket that carries a report_ref. Because of S1, a live B3 on
    the ticket of this run would find no control and exit `B-LEG-BAD b3`.
12. **Fixture simplification.** The board list answer is static: it carries the finished ticket (with report_ref and a
    package map of four refs) in every phase, so B1 and B2 also show that ticket. The live board will not.

## 5. Offline results at the time of writing (see the proof instance for the verdicts)

- B1 (offline): `B1 form labels=12 advisor=optional report_type=absent commentary=absent firms=3 models=5`.
- B2 (offline): `B2 filed ok ticket=TCK-20261020-deadbeef req=none` then `B-LEG-OFFLINE-BAD b2 ... analysis request was not sent`.
- B3 positive (standalone, fixtures_offline.json): `B3 report face=yes headings=1 value=yes`, RC 0.
- B3 difference control (standalone, fixtures_offline_noreport.json): `B3 report face=no headings=0 value=no`,
  `B-LEG-BAD b3 face=no`, RC 1.
- The composite AC2 with the no-report fixture stops at B2 (`B-LEG-OFFLINE-BAD b2`), not at b3, for the same reason as
  item 1. The composite therefore cannot reach its b3 difference control until the analysis submit sends.
- Determinism: two composite runs agree line for line after the `at=` time is masked (26 lines).

## 6. Files

- `run7_browser_leg.mjs` (the script), `fixtures_offline.json`, `fixtures_offline_noreport.json`, `holdings_sample.csv`.
- `OFFLINE_STDOUT.txt` (AC1 stdout), `OFFLINE_NOREPORT_STDOUT.txt` (AC2 stdout), `shots_*` (screenshots, synthetic data).
