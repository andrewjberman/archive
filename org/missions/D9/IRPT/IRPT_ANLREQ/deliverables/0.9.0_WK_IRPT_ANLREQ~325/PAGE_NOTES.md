# PAGE_NOTES -- run 7b browser leg, re-proved offline against the Advisor-required form (0.9.0_WK_IRPT_ANLREQ~325, cell AR-y-459)

**Read this before the GO.** The copy is built against the detached portal tree d5d2fdeab3af8fcbc1f74ef2d5f2eefd7a89c3d3
(branch cand/dell2/anlreq-andrew-walk-v2, the portal worktree C:/dev/wk-irpt-anlreq-325/portal, read-only; nothing committed
there). This tree carries the run 7 submission-guard fix (e9ca1106, AR-y-455; an ancestor of d5d2fdea through the 4546cee
release merge) and the Advisor-required fix (the commit subject's "msg 11384"). It is not the PROD tip as it stood at run 7.
The live run 7b must be pressed only after this build is deployed to PROD by the issuer.

## 1. The build

- `git diff --numstat 4546cee0528c1b2e21726666f8a97bf2f1f5f5bc HEAD` lists 12 files, all under `src/pages/TicketCenter/`:
  AnalysisRequestParts.tsx (+69 -18), TicketCenter.tsx (+13 -7), analysisRequest.ts (+9 -1), and nine test files.
- `bun run build` (= tsc -b && vite build): rc 0, built in 11.59 s, output in the portal's `dist/` (gitignored).
- The instrument: `run7_browser_leg.mjs` drives the page's own controls with playwright-core (Edge, headless) against that
  build, served from disk. It imports nothing from the portal tree except playwright-core from `--portal`.
- Offline: no network, no AWS, no push, no deploy, no token. Every API answer is in `fixtures_offline.json` (synthetic:
  household `E2E7 SYNTHETIC`, tickers `SYNTH-*`, value 12.5, ticket and request ids of the cell's shapes).

## 2. What the copy changes (against the ~323 copy)

1. **Advisor is read, never typed.** The normal path reads the Advisor's placeholder (`advisor=`) and its value at first
   paint (`advisor_prefilled=`). It does not type into or clear the field.
2. **B1 line** is `B1 form labels=<n> advisor=<optional|required|absent> advisor_prefilled=<yes|no> report_type=... commentary=...
   firms=... models=...`. Every other B1 field is kept.
3. **Composite checks** now require `advisor=required` and `advisor_prefilled=yes` at B1, and print the OK line with
   `advisor=required advisor_prefilled=yes`.
4. **Needed by and Other ETFs.** The ~323 script never looked for the Needed by control and never typed Other ETFs, so nothing
   was removed. The form has no Needed by control any more; Other ETFs is now a chip input and the run types nothing into it.
   The catalogue is read only when Other ETFs is typed (`catalogueForFiling` and `readCatalogueForTyping`), so no catalogue call
   is made in this run.
5. **Stub session.** `buildSession()` in the script already sets `user.name` to `Dev User`. The `/auth/refresh` route answers
   with that session; AuthContext's refresh stores `data.user` as `auth.user`; TicketCenter pre-fills the Advisor from
   `auth.user?.name` (startingAnalysisForm at first render, and the effect at TicketCenter.tsx 257-259 when the name arrives
   later). `fixtures_offline.json` carries no session key; the name lives in the script, not in the fixtures. Unchanged.
6. **`--blank-advisor`** (the control). The script fills the form as in the normal path, clears the Advisor with `fill('')`,
   then waits for the page to hold the submit. The page holds it by DISABLING the button (`disabled={creating || heldReason !== null}`),
   so no press is possible and none is made. The held words are read from the page's own held line
   (`data-slot="submit-held-reason"`) and printed on the B2 line as `B2 filed REFUSED <words>`; the composite then prints
   `B-LEG-OFFLINE-BAD b2 submit held <words>`. CALLS lists no `POST /api/scoped/tickets`.
7. **heldWords** reads `data-slot="submit-held-reason"` first and falls back to the old text search.
8. Keep is still never pressed; no hint control is pressed (no TICKER_NOT_FOUND in the offline fixtures). The output is still
   closed lines only: no URL, no token, no header, no file content.

## 3. Accessible names (read at d5d2fdea)

| step | control | accessible name / selector | source |
|---|---|---|---|
| board | button | `New Ticket` (toggles the New Ticket panel) | TicketCenter.tsx |
| type | select | option value `analysis_request` (label "Analysis Request") | TicketCenter.tsx |
| title | input | placeholder `Title (what is being requested?)`; no label | TicketCenter.tsx 691-697 |
| Advisor | input | aria-label `Advisor`; placeholder `Advisor presenting (required)` for every filer (no staff "optional"); a `title` tooltip is set but the aria-label wins | AnalysisRequestParts.tsx 193-195 |
| Firm | select | aria-label `Choose the firm this request is filed under` (empty first option with the same words); shown when the firm list loaded and is non-empty | AnalysisRequestParts.tsx 196-201 |
| Household | input | aria-label `Household`; placeholder `Household (required)` | AnalysisRequestParts.tsx 206-207 |
| comparables | fieldset `data-slot="comparables"` | five checkboxes, names from `comparisonLabel(model)` | AnalysisRequestParts.tsx 209-231 |
| Other ETFs | input in `div[data-slot="etf-chips"]` | aria-label `Other ETFs`; Enter adds a chip, each chip has `Remove <TICKER>`, Backspace in an empty box removes the last chip, blur adds a typed ticker | AnalysisRequestParts.tsx 267-299 |
| Holdings file | input type file | aria-label `Holdings file`, accept `.csv,.xlsx` | AnalysisRequestParts.tsx 244-245 |
| submit | button | text `File Analysis Request`; reads `Uploading...` while creating; DISABLED while a held reason is shown | TicketCenter.tsx 717-723 (partner) and 886-892 (staff) |
| held line | p | `data-slot="submit-held-reason"`, role status; holds the words of `submitHeldReason` | AnalysisRequestParts.tsx 408-414 |
| hint presses | buttons | `Yes`, `Replace` (reveals `Replacement ticker for <symbol>` and `Check`), `No`. No control reads Keep | AnalysisRequestParts.tsx 364-383 |
| row | buttons | `Claim`, `Request report` (`data-slot="request-report"`), `Retry analysis request`, `Open report` (`data-slot="open-report"`, only with a report_ref) | AnalysisRequestParts.tsx 452-486 |
| report | panel | `data-slot="opened-report"` with `data-state`; button `Close` | AnalysisRequestParts.tsx 595-607 |

Needed by is gone: no input carries that label in this tree (the copy never looked for it).

## 4. The held words (the Advisor hold)

`ADVISOR_HELD` (analysisRequest.ts) reads: `Advisor is required. Add the advisor presenting this report to submit it.`
`submitHeldReason` checks in this order: title, advisor, firm, household, comparables, holdings file. The Advisor is always
sent (`answersFromForm` sends `advisor` on every filing); the ticket service requires it.

## 5. Call sequence observed offline (fixtures_offline.json, this build)

Board load: `GET /api/scoped/tickets`, `GET /api/scoped/tickets/metrics`, `GET /api/scoped/portal-content`, and the five
`GET /api/scoped/advisor-intelligence/platinum/firm/*.json` shell reads.
Form open (staff): `POST /api/scoped/investor-reporting/directory/resolve` (the firm list). No model call (the five models are
static). No catalogue call (Other ETFs not typed).

B2 filing, as the page makes it (the four writes, in order; the composite's `b2_calls` names them):
1. `POST /api/scoped/investor-reporting/analysis/inputs` (upload, answer NORMALIZED). `analysis-input-upload`.
2. `POST /api/scoped/tickets` (ticket create). `ticket-create`.
3. `POST /api/scoped/investor-reporting/analysis` (analysis submit, `commentary_requested: true`). `analysis-request`.
4. `POST /api/scoped/tickets/{id}/report` (record the REQ id on the ticket). `ticket-report`.
After the filing the board is re-read (`GET` tickets, metrics and portal-content).
B3: `GET /api/scoped/investor-reporting/analysis/{requestId}/sections`.

Unanswered calls: the board-shell reads `GET .../advisor-intelligence/platinum/firm/*.json` and `GET /api/scoped/portal-content`
have no fixture and answer 404 from the route; a scratch diagnostic of the offline run listed those six paths and no form call.
They are not the form's calls and were so before this change (~323 notes section 3). Every form call (directory resolve, upload,
ticket create, analysis submit, report record, sections) is answered from the fixtures.

## 6. Where the new form differs from ~323 PAGE_NOTES and ADDENDUM 9 (the issuer reads these before the GO)

1. **Advisor is required for every filer,** not optional for staff (the ~323 notes said optional). B1 now reads `advisor=required`.
2. **Advisor is pre-filled** from the signed-in filer's name. This build is proven offline only with the stub name `Dev User`.
   The live pre-fill is the real signed-in filer's name, which was NOT seen (no live page was reached).
3. **A blank Advisor HOLDS the submit by disabling it.** The page shows the held line and the button is disabled. There is no
   press to make with a blank Advisor, so the blank control clears the field and reads the hold; it does not press.
4. **Needed by is removed** and the form-as-filled summary has no Variant, Needed by or Add commentary row.
5. **Other ETFs is a chip input.** The run types nothing into it; the catalogue is read only when a ticker is typed.
6. **Keep: none**, as before. The hint presses are Yes, Replace and No (no hint is exercised offline).
7. **Firm chooser** lists three firms offline (`49 Financial`, `Cottonwood Capital Advisors`, `Inflection Wealth Management`);
   the live labels were not checked.
8. **Models:** five at first paint (static list, no call), as before.

## 7. Results on this worktree (the proof instance cites these)

- AC1 (`OFFLINE_STDOUT.txt`, rc 0): the B1, B2 and B3 lines, then
  `B-LEG-OFFLINE-OK b1_labels=11 advisor=required advisor_prefilled=yes report_type=absent commentary=absent firms=3 models=5 b2_calls=analysis-input-upload,ticket-create,analysis-request,ticket-report b3_face=yes`
- AC2 (`--blank-advisor`, rc 1): `B2 filed REFUSED Advisor is required. Add the advisor presenting this report to submit it.`
  then `B-LEG-OFFLINE-BAD b2 submit held Advisor is required. Add the advisor presenting this report to submit it.`
  The B2 CALLS block holds no `ticket-create` and no `analysis-request`.
- Determinism: a second AC1 run, with `at=` masked, matches the first line for line (38 lines).
- AC3: the leak grep over this file and `OFFLINE_STDOUT.txt` (token-shaped run, web-address prefix, bearer prefix) prints 0.

## 8. Live run notes (for the issuer, not run here)

- The live run needs the filer's session name to pre-fill the Advisor. A blank name holds the submit; the normal path then stops
  at B2 with `submit held` and nothing is filed.
- The script's B2 waits up to 15 s for the submit to enable; a held form stops there, before any press.
- Keep is never pressed. One submit is pressed, in the normal path only.

## 9. Files

- `run7_browser_leg.mjs` (the copy), `fixtures_offline.json` (unchanged), `holdings_sample.csv` (unchanged).
- `OFFLINE_STDOUT.txt` (AC1 stdout), `shots_offline/` (AC1 screenshots), `shots_blank_advisor/` (AC2 screenshots),
  `shots_baseline/` (the unmodified copy against this build, which stopped at B1 on the old advisor check; kept as evidence).
- Synthetic data only in every screenshot.
