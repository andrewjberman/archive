# PAGE_NOTES -- run 7 browser leg, proved offline (0.9.0_WK_IRPT_ANLREQ~323, cell AR-y-454)

**Read this before the GO.** The proof now runs against the fix branch `cand/dell2/anlreq-submission-guard-commentary`
at `e9ca1106dd9f85a1f5cb08fa52c89c52a53ed4cd` (one commit on origin/PROD `f48e09ddf95e`), not plain PROD. On plain PROD the
page cannot complete B2 (surprise `IRPT_ANLREQ-D2-W323-S1`, BLOCKING, ARMED; the issuer owns the disposition). With the
fix in the tree the offline composite reaches B3 (section 5). The live run must still be pressed only after the fix is
deployed to PROD.

## 1. What was built and against what

- Tree: the portal worktree `C:/dev/wk-irpt-anlreq-323/portal`, detached at `e9ca1106dd` (read-only; nothing committed
  there). `git diff --numstat f48e09ddf95e HEAD` lists exactly two files: `src/pages/InvestorReporting/contracts/submission-request.ts`
  (+2 -1) and `src/pages/InvestorReporting/__tests__/submission-request.test.ts` (+40 -0).
- Build: `bun run build` (= `tsc -b && vite build --configLoader runner`), RC 0, 11.71 s. Output in `portal/dist`
  (gitignored in the portal submodule).
- Instrument: `run7_browser_leg.mjs` drives the page's own controls with `playwright-core` (Edge, headless) against the
  build served from disk. It copies `serveFromDist` from `portal/scripts/ui-dist.mjs` and imports nothing else from the
  portal tree. `--token-file` sends a real bearer as the session accessToken, the way ui-smoke `--token` does.
- Offline: no network, no AWS, no push, no deploy. Every API answer is in `fixtures_offline.json` (synthetic: household
  `E2E7 SYNTHETIC`, tickers `SYNTH-*`, values such as 12.5, request and ticket ids of the cell's shapes).
- Output contract: stdout carries closed lines only (B1, B2, B3, CALLS, B-LEG-*). No URL, token, header or file content
  is printed. `RUN7_DEBUG=1` adds page console lines and must not be set for the live run.

## 2. Accessible names (read at e9ca1106; unchanged from f48e09dd)

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

## 3. Call sequence observed offline (e9ca1106, fixtures_offline.json)

Board load (shell and board, before any form):
`GET /api/scoped/tickets?status=open`, `GET /api/scoped/tickets/metrics`, and shell reads (`GET /api/scoped/portal-content`,
`GET /api/scoped/advisor-intelligence/platinum/firm/*.json`), which the CALLS lines show and which are not the form.

Form open (staff): `POST /api/scoped/investor-reporting/directory/resolve` (Global context, read when the form opens).
The model catalogue is a static list: no call (AR-y-419). `GET .../analysis/comparisons` is read only when Other ETFs is
typed; not exercised.

B2 filing, as the page makes it (the four writes, in order; the composite's `b2_calls` names them):
1. `POST /api/scoped/investor-reporting/analysis/inputs` (upload; answer NORMALIZED). `analysis-input-upload`.
2. `POST /api/scoped/tickets` (ticket create, source `ticketcenter:i1`). `ticket-create`.
3. `POST /api/scoped/investor-reporting/analysis` (analysis submit, body with `commentary_requested: true`; the guard now
   admits it). `analysis-request`. Answer: the REQ id, read into the B2 line.
4. `POST /api/scoped/tickets/{id}/report` (record the REQ id on the ticket). `ticket-report`.

B3 (Open report): `GET /api/scoped/investor-reporting/analysis/{requestId}/sections?selected_tenant=..&ticket_id=..`.

## 4. Where the page differs from ADDENDUM 9 section 2 (the issuer reads these before the GO)

1. **B2 analysis step: defect found, fixed on the branch (surprise S1, BLOCKING, ARMED; disposition the issuer's).**
   ADDENDUM 9 says the page performs the upload and the analysis request. On plain PROD (f48e09ddf95e) it did the upload
   and the ticket create, then refused the analysis submit client-side. Before the fix, the run's B2 line and page words
   were (kept as evidence):
   `B2 filed ok ticket=TCK-20261020-deadbeef req=none at=11:28:56Z` followed by
   `B-LEG-OFFLINE-BAD b2 the ticket is filed but the analysis request was not sent the page showed Analysis FAILED - Invalid analysis submission request`.
   The CALLS lines held `POST .../analysis/inputs` and `POST /api/scoped/tickets` only. Cause: `analysisBody` (analysisRequest.ts 651-667)
   adds `commentary_requested: true`, and `readSubmissionRequest` (contracts/submission-request.ts) admitted only the
   required keys plus `input_id` and `ticket_id`, so the TypeError refused the body before any POST. The ticket was filed with
   no REQ id, no report_ref and therefore no Open report control for B3.
   After the fix (e9ca1106: the allowed set gains `commentary_requested`, and a non-boolean value is refused): the analysis
   submit is sent, B2 reads `req=REQ-5e7a1c0d9b2f4a6e8c3d1b07`, the record POST is made, and B3 finds the Open report
   control. The Retry analysis request path calls the same submit and is fixed by the same change (by reading).
2. **Four writes, not three (surprise S2).** upload, ticket create, analysis submit, and the record of the report id on the
   ticket (`POST .../tickets/{id}/report`). The composite prints the four names the page actually makes:
   `b2_calls=analysis-input-upload,ticket-create,analysis-request,ticket-report`.
3. **No Keep control (surprise S3).** The symbol hint presses are `Yes`, `Replace` and `No`. The addendum's "no Keep" means
   no press of a hint control. These offline fixtures never produce a finding, so no hint control was shown.
4. **Submit label.** The press is `File Analysis Request`; the addendum's word "submit" is the same control.
5. **New Ticket defaults to Service Request for staff.** The operator chooses Analysis Request first (the addendum says the
   same, so this is a note, not a difference).
6. **Advisor.** Labelled optional for staff through the placeholder `Advisor (optional)`: matches B1.
7. **No report-type and no commentary control on the form.** Matches B1 (report_type=absent, commentary=absent).
8. **Firm chooser.** Lists three firms offline: `49 Financial`, `Cottonwood Capital Advisors`, `Inflection Wealth Management`
   (the labels come from `firmDisplayNameFor` because the fixture scope names none). The PROD labels may differ; not
   checked live.
9. **Models.** Five at first paint (static list, no call). Matches B1.
10. **Holdings bytes.** The page reads the file in the browser and sends its bytes in the upload body. The addendum's
    "sha256 printed" is the operator's step: this script prints no file content and no hash.
11. **B3 needs report_ref.** Open report exists only on a ticket that carries a report_ref, which the record step sets. On
    plain PROD (surprise S1) a live B3 would find no control; on the fix branch it does.
12. **Fixture simplification.** The board list answer is static: it carries the finished ticket (with report_ref and a
    package map of four refs) in every phase, so B1 and B2 also show that ticket. The live board will not.

## 5. Offline results on e9ca1106 (see the proof instance for the verdicts)

- AC1 composite (RC 0): `B1 form labels=12 advisor=optional report_type=absent commentary=absent firms=49 Financial,Cottonwood Capital Advisors,Inflection Wealth Management models=5`;
  `B2 filed ok ticket=TCK-20261020-deadbeef req=REQ-5e7a1c0d9b2f4a6e8c3d1b07 at=12:05:16Z`; `B3 report face=yes headings=1 value=yes`;
  final `B-LEG-OFFLINE-OK b1_labels=12 advisor=optional report_type=absent commentary=absent firms=3 models=5 b2_calls=analysis-input-upload,ticket-create,analysis-request,ticket-report b3_face=yes`.
- AC2 composite (RC 1): the same B1 and B2 lines, `B3 report face=no headings=0 value=no`, final
  `B-LEG-OFFLINE-BAD b3 face=no headings=0 value=no`.
- B3 standalone positive (fixtures_offline.json): `B3 report face=yes headings=1 value=yes`, RC 0.
- B3 standalone difference control (fixtures_offline_noreport.json): `B3 report face=no headings=0 value=no`,
  `B-LEG-BAD b3 face=no`, RC 1.
- Determinism: two composite runs agree line for line after the `at=` time is masked (38 lines).
- Leak control: the AC3 grep (token-shaped run, web-address prefix, bearer prefix) over PAGE_NOTES.md and OFFLINE_STDOUT.txt prints 0.

## 6. Files

- `run7_browser_leg.mjs` (the script), `fixtures_offline.json`, `fixtures_offline_noreport.json`, `holdings_sample.csv`.
- `OFFLINE_STDOUT.txt` (AC1 stdout), `OFFLINE_NOREPORT_STDOUT.txt` (AC2 stdout), `shots_*` (screenshots, synthetic data).
