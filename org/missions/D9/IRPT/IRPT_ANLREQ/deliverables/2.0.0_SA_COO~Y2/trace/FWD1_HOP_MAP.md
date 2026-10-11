# IRPT_ANLREQ -- FWD-1 hop map (the project map; kept current by 2.0.0_SA_COO~Y2 by CTO msg 4919)

**Source:** worker `0.9.0_WK_IRPT_ANLREQ~52`'s read-only trace `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/trace/FWD1_HOP_TRACE.json` (read 2026-10-11T12:20:12Z, tree e41eab5325), merged @3ec19cb307.
**FWD-1** (`org/missions/D9/IRPT/IRPT_ANLREQ/prd/IRPT_ANLREQ_PRD.md:28`): FWD-1  One Analysis Request goes from the Ticket Center form to a finished package on the same open ticket, with no person in between. DONE WHEN EXERCISED -- on DEV, a seat files ONE request through the form (analysis type, Opal-model checkboxes, other ETFs, holdings Excel) for a 49financial client with an eligible advisor; with nobody touching it, the ticket ends up carrying the report, the branded Opal PDF with the investment commentary, and the original Excel, each opened from the ticket page (PRD lines 28-35)

**How to read the state column.** The trace marked a portal hop LIVE only when it is on portal PROD; that was the issuer's instruction and it was wrong for this outcome, which reads "DONE WHEN EXERCISED -- on DEV". The column `for FWD-1` corrects it: a portal hop that is on DEV is PRESENT for FWD-1. Nothing else in the trace is changed. Every state is the worker's reading unless the last column says the issuer spot-read it.

| n | hop | trace state | for FWD-1 | owner | waits on (trace) | cut or ruling since | claim |
|---|---|---|---|---|---|---|---|
| 1 | A person fills the Analysis Request form on the Ticket Center page (analysis type, Opal-model checkboxes, other ETFs, firm choice, holdings file). | BUILT_NOT_LIVE | PRESENT ON DEV | PORTAL | A portal DEV to PROD push. Built by TCKT_VNEXT/IRPT_ANLREQ orders TO-AR-v11 and TO-AR-y-35 (both complete). origin/DEV 8ed372cb differs from origin/PROD 37aa1247 by 85 files, 53 of them under src/pages/InvestorReporting, |  | measured (issuer spot-read) |
| 2 | The form sends the holdings file to the upload door (POST analysis/inputs) and the door answers NORMALIZED with an input id. | LIVE | LIVE | IRPT_ANLREQ_Y | NOTHING to deploy. Reached through the API by the TCKT_VNEXT seat runner, never by a browser form; the portal form's call to it is DEV-only (hop 1). The source map's artifact_sha256 for this function does not equal the l |  | inherited |
| 3 | The form creates the analysis_request ticket (POST /tickets) holding the answers and the upload handle, only after the door says NORMALIZED. | LIVE | LIVE | TCKT_VNEXT | NOTHING to deploy. The older PROD form already performs hops 2 and 3 (fileAnalysisRequest in origin/PROD analysisRequest.ts:92-121); no browser-driven filing has been recorded. |  | measured (issuer spot-read) |
| 4 | After the ticket exists, the form immediately posts the analysis request carrying the new ticket id (sequence I1, step 3), so no person claims or clicks. | BUILT_NOT_LIVE | PRESENT ON DEV | PORTAL | The same portal DEV to PROD push as hop 1. On PROD the form stops after filing the ticket; the report is requested only when an assignee claims the ticket and clicks Request report (origin/PROD analysisRequest.ts:144-176 |  | measured |
| 5 | The analysis service accepts the request, stores ticket_id on the acceptance record and queues the generation job (answer NOT_READY/QUEUED is the accepted answer). | LIVE | LIVE | IRPT_ANLREQ_Y | NOTHING to deploy. Not yet seen accepting a request that carries a ticket_id: the fourth run (TCKT_VNEXT.TO-RUN-R3-tr1, status pending, ledger opened 11:09Z) is the first to drive it with the I1 id. |  | measured |
| 6 | The queued job is taken from the generation queue by the resident worker on the resident host. | LIVE | LIVE | IRPT_YCDGEN | NOTHING to deploy. st30 admits a request that names ticket_id (S2) but is APPLIED, UNEXERCISED; its first exercise is TCKT_VNEXT.TO-RUN-R3-tr1 (pending). |  | inherited |
| 7 | The resident generates the report for a ticket-bound request, persists it and reaches READY. | NOT_DETERMINED | NOT_DETERMINED | IRPT_YCDGEN | The fourth run (TCKT_VNEXT.TO-RUN-R3-tr1, pending) and the dead-letter record (IRPT_YCDGEN.TO-YCD-e-11 pending; TO-YCD-a-11 pending). Run 3's accepted request was consumed and produced no report, with no failure reason r | stays NOT_DETERMINED until a ticket-bound request reaches READY; waits on the vendor session (CTO msg 4919) | inherited |
| 8 | The resident builds the report with the Opal engine (the producer FWD-1's branded report needs) for the person who filed. | BUILT_NOT_LIVE | BUILT_NOT_LIVE | IRPT_YCDGEN | The Opal producer allow list, which names one sign-in only; every other caller, including the service identities, takes the vendor-facing YCharts producer. The allow-list question is recorded as carried to Andrew (YC2 lo |  | inherited |
| 9 | On READY the resident sends the closed analysis_ready message to the commentary queue (interface I3). | BUILT_NOT_LIVE | BUILT_NOT_LIVE | IRPT_ANLREQ_G | A resident release that binds the analysis-ready queue (the unit has no IRPT_ANALYSIS_READY_QUEUE_URL, so each READY only logs a WARN). Round-3 workstream G names it 'the attach release (G3, third part)'; no task order f | ATTACH RELEASE: 2.0.0_SA_COO~G2, own order and pair, after AR-g-32 (CTO msg 4919) | inherited |
| 10 | The commentary function takes an analysis_ready message, reads the report composition, drafts the commentary and stores the DRAFT. | LIVE | LIVE | OTHER | NOTHING to deploy (owner: workstream T, 2.0.0_SA_COO~T2, orders TO-AR-t-11, t-12, t-21 all complete). Nothing feeds it: the analysis-ready queue reads 0 and no sender is bound (hop 9). It has run once, on a synthetic req |  | inherited |
| 11 | The commentary function puts commentary_ready on its queue and the resident packager takes it (interface I4). | BUILT_NOT_LIVE | BUILT_NOT_LIVE | IRPT_ANLREQ_G | The same resident release as hop 9: the unit has no commentary_ready_queue_url binding, so nothing polls the queue. The packager module is in the installed root. One test message sits on the queue (row IRPT_ANLREQ-D2-S26 | ATTACH RELEASE (as hop 9) | inherited |
| 12 | The packager's own service identity (svc-irpt-packager) exists with a credential the resident can read. | NOT_DETERMINED | NOT_DETERMINED | IRPT_ANLREQ_G | The mint was planned as 'the packager mint (G3, second part), under its own pair' (IRPT_ANLREQ_DECOMP_R3_G.md line 26). No order or record that performs it was found among the 26 org markdown files naming svc-irpt-packag | stays NOT_DETERMINED until a ticket-bound request reaches READY (CTO msg 4919) | inherited |
| 13 | The packager renders the branded PDF with the commentary page from the stored report and the stored draft, and stores it. | BUILT_NOT_LIVE | BUILT_NOT_LIVE | IRPT_ANLREQ_G | Hop 11's binding (nothing starts the packager) and hop 12. Never run anywhere: the render and I7 pdf_ref writer are inside the installed root, behind the unset binding. |  | inherited |
| 14 | The packager posts the package pointers to the ticket (POST /tickets/{id}/package, interface I5) as svc-irpt-packager. | BUILT_NOT_LIVE | BUILT_NOT_LIVE | IRPT_ANLREQ_G | The packager binding (api_base, email, secret_name) is absent, so both live ticket ports refuse PACKAGER_PRINCIPAL_UNSET; and hop 12. Code (TO-AR-g-31, complete) is in the installed root but has not run. | ATTACH RELEASE (as hop 9) | measured |
| 15 | The ticket service accepts the package pointers from the one named principal and stores them on the open ticket. | LIVE | LIVE | TCKT_VNEXT | NOTHING to deploy. Not exercised with a real call from that principal (it does not exist or is not proven, hop 12). |  | measured |
| 16 | The ticket learns the id of its own report request (report_ref) so the page can open the files; for a ticket filed through the form's one-step sequence nothing records it. | NO_CODE | NO_CODE | TCKT_VNEXT | No order or cell found that records report_ref for an I1 ticket. The only writers are the assignee-only report route (needs an in-progress claimed ticket, which the I1 sequence never makes, and the page hides Request rep | one build cell in TCKT_VNEXT, 2.0.0_SA_COO~V2, after the code read is confirmed against row IRPT_ANLREQ-D2-W52-S5 (CTO msg 4919) | inferred (issuer spot-read) |
| 17 | The open ticket page shows the package block (the four pointers and who attached them) as text. | LIVE | LIVE | PORTAL | NOTHING. Text refs only on PROD; it renders only once a ticket carries a package (hop 15). |  | measured |
| 18 | The Investor Reporting status service serves the finished report for a request id (analysis-report read). | LIVE | LIVE | IRPT_ANLREQ_Y | NOTHING to deploy. What is NOT live on this function: retained_ref on that read and the history client (release 5, applied 10:25:40Z and ROLLED BACK 11:26:53Z; row D2-S43/S44), so nothing from rounds 3 or 4 is serving. |  | measured |
| 19 | From the ticket page, the Report file opens the finished report (not the request record). | BUILT_NOT_LIVE | PRESENT ON DEV | PORTAL | The portal DEV to PROD push (same as hop 1) and hop 16 (the Open buttons need report_ref). On PROD, Open report still reads the request record (getOwnedAnalysisRequest), the S20 finding. Built by TO-AR-y-31 and TCKT_VNEX |  | measured |
| 20 | From the ticket page, the Branded PDF file opens through a signed link. | BUILT_NOT_LIVE | PRESENT ON DEV | PORTAL | The portal DEV to PROD push, hop 16, and hops 13-14 (no PDF exists until the packager has run). The service route (analysis-request-pdf) is in the live irpt-status package; it has never been read against a real PDF by an |  | measured |
| 21 | From the ticket page, the Original file opens the advisor's uploaded Excel through a signed link. | BUILT_NOT_LIVE | PRESENT ON DEV | PORTAL | The portal DEV to PROD push and hop 16. The service side is live: the original route is on the live API and irpt-status; its read answered 200 on revision 6 (applier's result file, inherited) and the original-file reader |  | measured |

**Where the journey stops, read on DEV:** hops 7, 8, 9, 11, 12, 13, 14, 16.
Of those, the CTO ruled three cuts (msg 4919): the ATTACH RELEASE for hops 9, 11, 14; one TCKT_VNEXT build cell for hop 16; hops 7 and 12 wait on a ticket-bound request reaching READY. Hops not named in that ruling keep the trace's own `waits on`.

**No closer:** the CTO did not carry one to Andrew: every stopped hop has an owner (msg 4919).

## Change log

- 2026-10-11 ~12:5xZ: first issue, from the trace; the FWD-1 column added; the three cuts of CTO msg 4919 entered. No hop state re-measured by the issuer beyond the spot reads of hops 1, 3 and 16.
- 2026-10-11 ~14:4xZ: changes since the first issue, each from a record named here; no hop state re-measured by the issuer unless said.
  - Hop 16 (TCKT_VNEXT, `report_ref` on a one-step-filed ticket): the service half is APPLIED (TCKT_VNEXT R3-rf-2; the integrator's
    receipt msg 5074 rests on `2.0.0_SA_COO~V2`'s report of its after-reads, not re-read here) and the portal half (this lane's
    `AR-y-61`) is ON portal DEV `cece88f603` (issuer's `ls-remote`). UNEXERCISED: no real one-step filing has run it.
  - Hop 19 (the page's Report opens the finished report): a binding was added behind it and is NOT live -- the service cell `AR-y-71`
    is merged (31d02ad19c) and enters no build until release 5's return; the portal cell `AR-y-72` is a reviewed candidate
    (`5f64f409b0`) held until the service is live. Both wait on the portal history reader reaching PROD (Andrew's word).
  - Hops 9 and 10 (the resident's `analysis_ready`; the commentary drafter): the drafter never reads the job or the report
    (`trace/COMMENTARY_READY_WHAT_IT_READS_20261011.md`). CTO msg 5133: one cell, not urgent, OWED BY THIS LANE and not yet cut -- the
    drafter refuses a request whose job does not read READY; it lands BEFORE the analysis-ready binding (workstream G's attach
    release, cell 4). Un-parks at this lane's next issuance.
  - Hops 9, 11, 14: the attach release is four cells in workstream G (CTO msg 4972); its third reads this lane's row S26 message.

### PARKED for this seat's NEXT issuance (owner `2.0.0_SA_COO~Y2`; un-parks at the next L10 analysis this seat receives, or sooner on a CTO word)

- **The one-account check (TCKT_VNEXT FWD-3's ACCEPT line), passed 2026-10-11 ~20:1xZ by `2.0.0_SA_COO~V2` msg 5744 on CTO ruling
  msg 5737** ("its issuer is the lane the owned-paths tool names for intake/parse.py ... pass FWD-3's ACCEPT line to that issuer for
  its next issuance"). The lane read by `2.0.0_SA_COO~V2`: `IRPT_COMPLETION_Y`, this seat. DONE WHEN (TCKT_VNEXT PRD :41-45): a
  known-bad sheet (several accounts in one file, a totals row, a holding that cannot be priced) is turned back with what to fix,
  and a known-good sheet goes through. ACCEPT: a file that today would come back by email comes back from the form instead.
  RECORD (the TCKT_VNEXT worker's read, `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~20/ONE_ACCOUNT_CHECK_READ.json`):
  the normalizer sees NO account column today, so the cell must first make an account column visible to it. CORRECTED 2026-10-11
  ~21:4xZ (row `IRPT_ANLREQ-D2-W52-S9`, cell `AR-y-146`): that record and this note first named `intake/parse.py` as the file the
  form's upload reaches. It is NOT: the form reaches `intake/template_reader.py`, and the deployed service refuses the `parse.py`
  lane by name. Owed to `2.0.0_SA_COO~V2`: the
  order id when it is cut.
- **UN-PARKED 2026-10-11 ~21:1xZ:** the one-account check above is cut as round 14 (issuance @35c3c4bd45, six cells; the form's
  door is `intake/template_reader.py`, NOT `parse.py`: row `IRPT_ANLREQ-D2-W52-S9`).
- **PARKED (owner `2.0.0_SA_COO~Y2`; un-parks when `2.0.0_SA_COO~P2`'s release of the submission's `commentary_requested` member is
  LIVE AND READ, never before): the form sends `commentary_requested`** (CTO msg 5864, IRPT_YCDGEN PRD v0.13 @e31454a778, signed
  @6f8aeb03b7): the boolean equals the `add_commentary` answer the form writes to the ticket, sent only on a ticketed request; the
  vendored schema copy moves with it; a portal candidate to the CTO. SERVICE FIRST: the live submission refuses an unknown member,
  so a form that sends it early breaks every filing (the same class as row `IRPT_ANLREQ-D2-S59`: cut after the act, not held by text).
- **RULED 2026-10-11 ~21:5xZ (CTO msg 5911), binding the upload door's release pair (round 14, cell `AR-y-145` and the issuer's pair):**
  (a) the live provider ask is WITHDRAWN (it writes rows, a stored original only Andrew may delete, and a vendor call on a stopped
  path); (b) the release's after-read does NOT include a synthetic upload unless the pair shows, FROM THE CODE, which provider the
  ticker check calls and that it is not the stopped YCharts path; otherwise the after-read is the reader's refusal alone and the
  labels SUBTOTAL, SUM and ALL stay UNEXERCISED LIVE, said so; (c) PARKED for this seat's next issuance (owner `2.0.0_SA_COO~Y2`;
  un-parks at the next L10 analysis): one cell, no call -- are SUBTOTAL, SUM or ALL real tickers? Any that is not joins the total
  list with a Rule 24 record. INFERRED by this seat, not read from the repository: ALL is a listed company's symbol, so it is not
  expected to join.
- **PARKED 2026-10-11 ~22:4xZ for this seat's next issuance (owner `2.0.0_SA_COO~Y2`; un-parks at the next L10 analysis this seat
  receives): the ticket page shows `commentary_sent`.** Passed by `2.0.0_SA_COO~V2` msg 5999 on the CTO's TCKT_VNEXT round-6 analysis
  @0b932076f0, section 3 item 3. The line: the ticket panel shows who sent the final commentary and when, from the ticket member
  `commentary_sent {sent_by, sent_at}`; and a control an internal person presses that calls
  `POST /api/scoped/tickets/{ticketId}/commentary-sent` with NO body. INHERITED from that message, not read by this seat: the route
  is live since 2026-10-11T21:27:13Z, answers 200 `{ticket_id, commentary_sent}`, 409 with four codes (SENT_WRONG_TICKET_TYPE,
  SENT_NO_DRAFT, SENT_ALREADY_RECORDED, SENT_TICKET_CHANGED), 404 outside the caller's firm scope, 400 on any body key; it is
  written ONCE and cannot be undone, and is unexercised. So the cell needs a confirm step before the press, words for each of the
  four refusals, and no live press in any test. Owed to `2.0.0_SA_COO~V2`: the order id when it is cut.
- **PARKED 2026-10-11 ~22:5xZ for this seat's next issuance (owner `2.0.0_SA_COO~Y2`; un-parks at the next L10 analysis this seat
  receives): ARM F2 on the original-file route of `irpt-status`** (CTO msg 6012, on TCKT_VNEXT FWD-2: "someone signed in for a
  DIFFERENT FIRM"). One cell and its pair to the CTO: a caller shaped as another firm's CLIENT asks for the original of a REAL
  request and is refused; its twin, the record's own owner, gets the signed link's PRESENCE only -- never written, never followed.
  READ FIRST (the cell's first step, no live call): the route's rule and its trusted headers, and which instrument they allow.
  Arm F1 (an internal caller with a firm list, refused for two other firms) is accepted by the CTO for what it shows and is NOT
  F2: no arm has reached a real record, so the owner check has never run. A signed link is never logged, written or reported.

