# TCKT_VNEXT cell R5-sit-1 -- STAGED reads for Andrew's sitting. NOT RUN. Run only if he files.

**By:** `2.0.0_SA_COO~V2`, 2026-10-11 ~19:5xZ. **Authority:** the CTO's round-5 analysis @d94b65958b section 3 item 8: "A read-only
cell STAGED for Andrew's sitting, run only if he files: the ticket's report reference read after his request, and the laptop's
rendered walk of the Open report page asked through `0.0.0_AB_MSTR~DELL2`. An Opal job makes no vendor sign-in, so the stop on the
vendor path does not reach it."

**Trigger (the only one):** word, from Andrew or relayed by the CTO, that he has filed an Analysis Request through the portal's
Ticket Center form on DEV, with the ticket id or the minute he filed. Nothing here runs on a guess that he might have.

## Why this matters

It would be the FIRST execution of the form's own code (the one-step filing), of hop 16 by a real staff creator, and of the Opal
producer for a ticket-bound request. Run 5 replicated the form's four calls with a runner; it did not execute the form.

## The reads, in order (every one read-only; no token is minted; no ticket is written)

| # | read | by | instrument | what it answers |
|---|---|---|---|---|
| 1 | the ticket, by id | this seat cannot: it holds no portal sign-in. Asked of the CTO's terminal or read from the service's own log line for the create | `/aws/lambda/opal-ticket-api` log lines for that ticket id, tokens only | the ticket exists, `source` reads `ticketcenter:i1`, it is not claimed |
| 2 | the record call | this seat | the same log group, the `report_recorded` event for that ticket id | hop 16 ran as the creator; the recorded id is a `REQ-` id |
| 3 | the request's job | `2.0.0_SA_COO~G2`'s applier (the request table is behind the encryption fence; the host journal is not) | the host journal's named lines for the request id | received, the producer chosen (Opal expected for Andrew's sign-in), READY or where it stopped |
| 4 | the rendered page | the laptop's `/ui-walk`, asked through `0.0.0_AB_MSTR~DELL2` | a rendered walk of the ticket in Ticket Center on DEV | the Open report control shows, opens the finished report, and the waiting state if still reachable |
| 5 | the coded refusals | this seat | the ticket service's log for the same minute | whether any creator-branch refusal fired (three are unexercised) |

## What is NOT done under this cell

No request is submitted by any seat. No vendor sign-in is caused. No identity or token is minted. No ticket, row or env value is
written. If Andrew's request takes the YCharts producer instead of the Opal one, that is reported at once and nothing is retried.

## Unknown to this seat, to settle when the trigger comes

- Whether the ticket service logs the `source` and the `report_recorded` event in a form a log read can match by ticket id (read 1
  and 2 depend on it); if not, reads 1 and 2 need a person with a portal sign-in, and this file is corrected before anything runs.

## CORRECTION (2026-10-11 ~23:0xZ) -- the unknown above is now read, and reads 1 and 2 CANNOT be made from the log

Read by this seat: the ticket handler prints twelve log lines, all mail, enrichment and firm-scope tokens (`WE_DL_*`,
`WE_CLIENT_*`, `ENRICHMENT-*`, `FIRM-SCOPE-*`). It prints no line for a create, a `source`, or a `report_recorded` event: those
are rows in the ticket's own `events` member. So reads 1, 2 and 5 of the table need the ticket's members, read by a person with a
portal sign-in or by a direct invoke under a pair of the shape of `R6_RUN/R6_FN1_DIRECT_INVOKE_PAIR.md`. The log can show only
that the function was invoked in that minute. Reads 3 and 4 are unchanged.
