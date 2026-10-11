# FWD-1 hop trace -- from a filed Analysis Request ticket to the finished report opened on it

Worker `0.9.0_WK_IRPT_ANLREQ~52`, order `IRPT_ANLREQ.TO-AR-y-51`, read 2026-10-11T12:20Z at tree head `e41eab5325`.
Source of FWD-1: `org/missions/D9/IRPT/IRPT_ANLREQ/prd/IRPT_ANLREQ_PRD.md:28`. Evidence per hop is in `FWD1_HOP_TRACE.json`.
Claim words: measured = this worker ran or read it; inherited = rests on another seat's record (named in the evidence); inferred = reasoned from code.
Portal: `origin/PROD` 37aa1247, `origin/DEV` 8ed372cb. Live reads were single-resource only; the live packages of five functions were downloaded and hashed.

| n | hop | state | owner | waits on | claim |
|---|---|---|---|---|---|
| 1 | person fills the form (type, model checkboxes, other ETFs, firm choice, file) | BUILT_NOT_LIVE | PORTAL | portal DEV to PROD push (DEV is 85 files ahead, 53 under Investor Reporting); PROD has an older form | measured |
| 2 | form to upload door, file NORMALIZED | LIVE | IRPT_ANLREQ_Y | nothing to deploy; seen only through the API runner | inherited |
| 3 | form creates the ticket with answers and upload handle | LIVE | TCKT_VNEXT | nothing to deploy | measured |
| 4 | form posts the analysis with the ticket id, no person in between | BUILT_NOT_LIVE | PORTAL | same push; PROD needs an assignee to claim and click Request report | measured |
| 5 | service accepts, stores ticket_id on the record, queues the job | LIVE | IRPT_ANLREQ_Y | nothing to deploy; first ticket-id request is the pending fourth run | measured |
| 6 | resident takes the job from the generation queue | LIVE | IRPT_YCDGEN | nothing to deploy (st30 installed 10:32Z); unexercised | inherited |
| 7 | resident generates, persists the report, reaches READY (ticket-bound) | NOT_DETERMINED | IRPT_YCDGEN | TO-RUN-R3-tr1 (pending), TO-YCD-e-11 (pending), TO-YCD-a-11 (pending) | inherited |
| 8 | the Opal engine builds the report for the filer | BUILT_NOT_LIVE | IRPT_YCDGEN | Opal allow list names one sign-in; all others take the YCharts producer; question carried to Andrew | inherited |
| 9 | resident sends analysis_ready on READY (I3) | BUILT_NOT_LIVE | IRPT_ANLREQ_G | queue binding absent; "attach release" (G3 third part) has no order | inherited |
| 10 | commentary function takes analysis_ready, drafts, stores the DRAFT | LIVE | OTHER (workstream T, `2.0.0_SA_COO~T2`) | nothing to deploy; nothing feeds it (queue 0, no sender) | inherited |
| 11 | commentary_ready queued and taken by the resident packager (I4) | BUILT_NOT_LIVE | IRPT_ANLREQ_G | commentary queue binding absent; 1 test message on the queue (row S26, ARMED) | inherited |
| 12 | svc-irpt-packager identity and credential exist | NOT_DETERMINED | IRPT_ANLREQ_G | mint was planned as its own pair (G3 second part); no order or record found | inherited |
| 13 | packager renders the branded PDF with the commentary page | BUILT_NOT_LIVE | IRPT_ANLREQ_G | hops 11 and 12; code is in the installed root, never run | inherited |
| 14 | packager posts the package pointers to the ticket (I5) | BUILT_NOT_LIVE | IRPT_ANLREQ_G | `packager` binding absent (ports refuse PACKAGER_PRINCIPAL_UNSET); hop 12 | measured |
| 15 | ticket service stores the package on the open ticket | LIVE | TCKT_VNEXT | nothing to deploy; never called by the real principal | measured |
| 16 | ticket records its own request id (report_ref) for an I1 ticket | NO_CODE | TCKT_VNEXT | no order; row IRPT_ANLREQ-D2-W52-S5 | inferred |
| 17 | ticket page shows the package block as text | LIVE | PORTAL | nothing (text refs on PROD) | measured |
| 18 | status service serves the finished report for a request id | LIVE | IRPT_ANLREQ_Y | nothing to deploy; round 3 and 4 changes are not on it (release 5 rolled back) | measured |
| 19 | page Report file opens the finished report | BUILT_NOT_LIVE | PORTAL | portal push; hop 16; PROD still opens the request record | measured |
| 20 | page Branded PDF opens through a signed link | BUILT_NOT_LIVE | PORTAL | portal push; hops 13, 14, 16 | measured |
| 21 | page Original file opens through a signed link | BUILT_NOT_LIVE | PORTAL | portal push; hop 16 (service side is live) | measured |

Where the journey first stops. Counted from the form, hop 1 is the first hop that is not live: the form FWD-1 describes is on portal DEV only, and
FWD-1's own done-when names DEV. PROD's older form does reach hops 2 and 3 (file, ticket created) and then stops, because the step that requests
the report without a person (hop 4) is also DEV only. From hop 9 to hop 14 the hand-overs between the resident, the commentary function, the packager and the ticket are not bound: the
resident does not send READY (hop 9) and nothing polls for the commentary (hop 11), so no package can reach a ticket; the commentary
function (hop 10) and the ticket's package route (hop 15) are deployed but nothing connects them; the packager (hops 13, 14) has never run. Hop 16 has no code in the places searched.

What could not be determined. Hop 7: no ticket-bound request has run through the resident since st30 was installed, and run 3's accepted request
left no recorded failure; the fourth run (pending) or the dead-letter record (pending) would say. Hop 12: whether the packager's identity and
credential exist; a single-resource read of its row in the ticket users table and of its secret would say. Hop 10's event-source mapping was taken
from the applier's record, not read (a list call is barred). Hops 6, 9, 11 and 13 rest on the applier's install output, read by this worker from the
SSM invocation record; the running root was not re-read today.
