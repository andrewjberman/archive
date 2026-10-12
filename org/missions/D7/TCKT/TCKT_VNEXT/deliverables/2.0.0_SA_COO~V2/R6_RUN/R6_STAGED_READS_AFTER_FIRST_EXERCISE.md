# TCKT_VNEXT round 6 -- FOUR STAGED reads, one per writer added or narrowed today. NOT RUN. Each runs ONCE, on its trigger.

**By:** `2.0.0_SA_COO~V2`, 2026-10-11 ~23:0xZ. **Authority:** the CTO's round-6 analysis @0b932076f0 section 3 item 1 and msg 5987:
"the four reads are STAGED now, one cell per writer with its trigger and its read named. Staged, never standing: each runs once
when its trigger is reported and polls nothing."

**No cell here polls, schedules, watches or alerts.** A trigger is a MESSAGE from the named seat, or Andrew's word; nothing here
goes looking for it. Until its trigger, a cell is a paragraph in this file. The fifth staged read (Andrew's sitting) is
`R5_RUN/R5_SIT1_STAGED_READS_FOR_ANDREWS_SITTING.md` and is not repeated here.

**What every read is, and is not:** a read of the ticket service's own log lines for one ticket id and one minute, as TOKENS and
COUNTS (event names, status codes, refusal codes), by this seat, from `/aws/lambda/opal-ticket-api`. It is not a read of the
ticket: no seat of this project holds an identity that may GET a ticket, and none is minted. Where a read needs the ticket's
members, it says who can make it.

| cell | the writer | live since | the trigger (the ONLY one) | the read, once | what it answers | what it cannot answer |
|---|---|---|---|---|---|---|
| `R6-sr-1` | the commentary-DRAFT route (`svc-commentary` sets a draft on the existing ticket, matched on the request id) | 21:27:13Z; the match 22:16:38Z | `2.0.0_SA_COO~T2` reports the drafter's switch is LIVE and names the first ticket id and minute it wrote to | the log for that ticket id in that minute: the invocation's outcome; the event `commentary_draft_set` with its `request_id=` note; any `DRAFT_*` code or deny | the route admitted its real caller; the match held on a real request; which arm answered | that the draft's TEXT is right (the drafter's); that a person can see it (the page) |
| `R6-sr-2` | the commentary-SENT route (an internal person records that the final commentary was sent) | 21:27:13Z | a page calls it: `2.0.0_SA_COO~Y2` reports the portal cell is on DEV, or a staff person's first click is reported | the log for that ticket id: the event `commentary_sent`; any `SENT_*` code | a real internal caller was admitted inside its firm scope; the stamp was written once | who the person was beyond the event's actor token; that a commentary was in fact sent (the service does not see it) |
| `R6-sr-3` | the PACKAGE door's admission (`svc-irpt-packager`, firm bound to the env list) | 15:18:51Z; the list 18:06:52Z | `2.0.0_SA_COO~G2` reports the resident's packager is BOUND and names its first attach (ticket id and minute) | the log for that ticket id: the event `package_attached` with its `report_ref=` note; any `PACKAGE_*` code or deny | the packager's token was admitted; the env list bound its firm; which of the five coded 409s, if any, fired | the PDF, the commentary page, or that the pointers open (the reader's side, `2.0.0_SA_COO~Y2`'s) |
| `R6-sr-4` | the CREATOR's record on the report route (hop 16), by the FORM | 13:34:27Z; exercised by the runner at 17:09Z, never by the form | a real one-step filing through the portal form on DEV is reported (Andrew's sitting, or a staff filing) with its ticket id | the log for that ticket id: the event `report_recorded`; any `REPORT_*` code | the FORM's own call reached the creator branch as a real staff creator; any of the three unexercised refusals | what the page showed the person |

**A limit of every read above, found while staging and NOT yet resolved:** the event names in the table
(`commentary_draft_set`, `commentary_sent`, `package_attached`, `report_recorded`) are rows the handler appends to the TICKET's
`events` member. What reaches the log group is only what the handler PRINTS, and this seat read the handler's print lines: they
are the mail and firm-scope tokens (`WE_DL_*`, `WE_CLIENT_*`, `FIRM-SCOPE-*`), not the event rows. **So a log read can show that
the route was invoked in that minute and how long it ran, and cannot show which event was written or which refusal code was
answered.** Each read therefore needs ONE of: the caller's own record of the answer it received (the drafter's, the packager's,
the form's), which the reporting seat supplies with the trigger; or a GET of the ticket's `events` names by a direct invoke
under a pair of the shape of `R6_FN1_DIRECT_INVOKE_PAIR.md`. The cell's read is the first where the caller's record carries the
status and code, and the second otherwise; that choice is made at the trigger and stated in the line to the CTO.

**Also staged, the digest (`R5-ml-1`, live 21:27:13Z):** it has no trigger a seat reports, because a client notice is sent by a
real claim. It is read in the SAME act as whichever of the four reads first covers a minute in which `WE_CLIENT_SENT` or
`WE_CLIENT_SEND_FAILED` was logged: the line carries `to_digest=` and no address. No separate cell.

**After each read:** one row of the drive log and one line to the CTO with the tokens; the cell's line here is marked RUN with
the time. A read that finds a refusal it did not expect is a surprise row, and nothing is retried.
