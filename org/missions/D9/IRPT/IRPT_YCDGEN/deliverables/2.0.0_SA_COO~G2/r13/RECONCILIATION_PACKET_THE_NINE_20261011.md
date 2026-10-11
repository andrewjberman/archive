# IRPT_YCDGEN round 13, cell YCD-a-13 -- reconciliation packet: the nine, by record, with nothing deleted

**Author:** `2.0.0_SA_COO~G2`, 2026-10-11. **For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Ruling:** the round-13 analysis @7fa981f907
section 2 item 2 and section 3 item 1. **WRITTEN, NOT APPLIED.** This packet proposes eight writes; it makes none. No message
is purged, redriven, deleted or received by it.

## 1. The nine, named

Eight messages on `irpt-generation-dlq` and one on `outlook-global-commentary-draft-commentary-ready-queue`. The ninth names
the eighth's request, so **nine messages name EIGHT requests.**

| # | request id | firm | sent | owner kind | job now | failure class on each of its five deliveries, in order | claim |
|---|---|---|---|---|---|---|---|
| 1 | REQ-ef7b39c548d08cbb4822f7cc | cottonwood | 2026-10-07T18:07:49Z | OPAL_STAFF | RECEIVED / SENT | LayoutRefused x5 | inferred |
| 2 | REQ-8966d24ffefa1c28269ef26c | cottonwood | 2026-10-08T21:10:30Z | SERVICE:svc-irpt-analysis | RECEIVED / SENT | LayoutRefused x5 | inferred |
| 3 | REQ-1f8b4cc4682f2d929cc70215 | 49financial | 2026-10-09T09:13:26Z | SERVICE:svc-irpt-analysis | RECEIVED / SENT | ClientError x5 | inferred |
| 4 | REQ-3d76e5b49dae4f91db1694b0 | 49financial | 2026-10-09T09:51:25Z | OPAL_STAFF | RECEIVED / SENT | ClientError x2, then RetentionExpired x3 | inferred, and not separable from #5 |
| 5 | REQ-9d59d4d2334f841152914569 | 49financial | 2026-10-09T09:51:30Z | OPAL_STAFF | RECEIVED / SENT | ClientError x2, then RetentionExpired x3 | inferred, and not separable from #4 |
| 6 | REQ-f7ddede91f98562412314b6e | 49financial | 2026-10-09T09:53:51Z | OPAL_STAFF | RECEIVED / SENT | ClientError x1, then RetentionExpired x4 | inferred |
| 7 | REQ-448d42480cadd873fa74c3cf | 49financial | 2026-10-09T10:37:05Z | SERVICE:svc-irpt-analysis | RECEIVED / SENT | RetentionRefused x5 | inferred, and CORROBORATED: this is this project's own F1 re-run, whose cause was read that day (st29 packet, "Why") |
| 8 | REQ-4b5155ac2ea9467ab771b414 | 49financial | 2026-10-09T14:59:07Z | OTHER | RECEIVED / SENT | SubmissionRefused x5, code CLOSED_COMPOSITION_REQUIRED | inferred |
| 9 | the `commentary_ready` message for request #8 | 49financial | 2026-10-11T06:10:50Z | (as #8) | (as #8) | not delivered to any consumer; receive count 1 of 3, from the laptop's read | measured |

All eight owners read `principal_class` OPAL_GLOBAL, `home_firm_id` opal-capital, `firm_id` equal to the tenant, with a
`prospect_input_id` present. No person's address is in this packet or in any record it cites.

## 2. Where each column comes from, and what each can and cannot say

- **Ids, firms, send times, job states:** MEASURED by the laptop's executor, `IRPT_YCDGEN_DEAD_LETTER_INVENTORY_irpt-generation-dlq_20261011.md`
  @f2053cfdd8 and, for the ninth, `IRPT_ANLREQ_COMMENTARY_READY_QUEUE_MESSAGE_20261011.md` @87e2151436. Both read by this seat
  at their commits.
- **Owner kind:** MEASURED by the laptop's executor, `IRPT_YCDGEN_OWNERS_OF_THE_EIGHT_DEAD_LETTERED_REQUESTS_20261011.md`
  @666b94c57d, with each RETENTION sibling as its control. "OTHER" for #8 means a principal that is neither a service subject
  nor at opalinvest.com; who it is did not leave the laptop and is NOT established here.
- **Failure class: INFERRED, by time.** The host journal for the window (order `TO-APPLY-j3`,
  `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_j3/DEAD_LETTER_JOURNAL_20261011.txt`; coverage FULL, oldest
  line 2026-09-24) holds 0 lines carrying any of the eight ids and 40 `retained_for_retry` lines, each a class and a code with
  no id. Each message was delivered five times, 900 seconds apart. I matched every retained line to the message whose send
  time it follows by a multiple of 900 seconds: **40 of 40 matched, 5 per message, each within 4 seconds of the multiple; 0
  left over.** The applier's row D2-S56 says the journal does not hold the cause; it is right that no line NAMES a request,
  and this match is the only bridge. It is an inference, and the packet carries it as one.
  - Its one corroboration: #7's class, RetentionRefused, is the cause read on the day by another route.
  - Its one known limit: #4 and #5 were sent 5 seconds apart, so their ten lines cannot be divided between them. Both read
    the same sequence, so the proposal below is the same for both whichever way they divide.
  - A class is not a reason. `ClientError` is an AWS client's refusal with its code not logged; `LayoutRefused` and
    `RetentionExpired` are named classes of this estate. What each refusal was ABOUT is not in the journal.

## 3. The proposal: the record st31 writes for a new failure, written for these eight

For each of the eight jobs, ONE conditional update of its own row in `irpt-jobs`:

- `state` from `RECEIVED` to `FAILED`;
- detail `{"code": "DELIVERIES_EXHAUSTED", "cause": <the class of its FIFTH delivery>, "receives": 5, "reconciled": true}`;
- written ONLY IF the row still reads `state = RECEIVED` at the moment of the write (a job that has moved is left alone and
  reported).

| # | proposed `cause` (the class on the fifth delivery) |
|---|---|
| 1, 2 | LayoutRefused |
| 3 | ClientError |
| 4, 5, 6 | RetentionExpired |
| 7 | RetentionRefused |
| 8 | SubmissionRefused |

`reconciled: true` is the one member st31's own branch does not write. It says the record was written afterwards from the
journal, by inference, and not by the worker at the moment of failure. If the CTO does not want a member st31 does not
write, the alternative is a different code, `DELIVERIES_EXHAUSTED_RECONCILED`; one or the other, so a reader can tell an
inferred record from a measured one. That choice is the CTO's and is not taken here.

**The ninth is not written to.** A queue message has no record of its own. It is accounted for by this packet's line 9 and
by request #8's row once written. It stays where it is until its retention ends: sent 2026-10-11T06:10:50Z on a queue that
keeps four days, so by that arithmetic it is gone at 2026-10-15T06:10:50Z, unless it is received twice more first, which
moves it to that queue's dead-letter queue.

## 4. Blast radius, and both branches read from the consumer's rule

- **What is written:** eight rows of `irpt-jobs`, one attribute pair each. The table sits behind the key no dell2 seat
  decrypts with, so the writer is the laptop's executor. Writers of a job's `state` today: the resident worker. This act is
  a second writer, once, for eight named keys.
- **The served answer that changes:** the status route. By `ops/owned_status.py` line 13 a RECEIVED job answers state
  QUEUED, reason ANALYSIS_QUEUED; by line 20 a FAILED job answers state FAILED, reason ANALYSIS_FAILED. So for these eight
  requests a status read stops saying "queued" about a job that will never run and says "failed". The detail is not passed
  to a caller. The portal's status reader at PROD accepts that answer (`st31_release/CONDITION1_PORTAL_READERS_AT_PROD_20261011.md`
  @5643d0e811). What the PAGE draws for it was not run.
- **Who sees it:** the owners of the eight. Four are Opal staff, three are the service subject, one is OTHER. No partner
  firm's user owns any of them (all eight are OPAL_GLOBAL from opal-capital).
- **Branch A (expected):** eight rows written, each read back FAILED with its detail; the two queues unchanged (8 and 0; 1
  and 0).
- **Branch B:** a row no longer reads RECEIVED: it is not written, and that is reported as a finding with its state.
- **What this does NOT do:** it does not make a redrive safe. Whether the worker would run, refuse or overwrite a job it
  finds FAILED on a redelivery was NOT read. The rule stands unchanged: no redrive of any of the eight without a pair naming
  each.

## 5. Rollback, per key

For each row written: `state` back to `RECEIVED` and the detail removed, conditional on the row reading exactly what this
act wrote. Eight keys, each independent.

## 6. The hold on the binding (attach cell 4)

The binding is held until the waiting commentary-ready message is accounted for (CTO msgs 5064 and 5081). This packet names
it. What a bound resident would do with it, by reading `opal_packager.handle_commentary_ready`: the accepted record of
request #8 carries no `ticket_id`, so the handler refuses `TICKET_ID_ABSENT`; that name is not one of the message refusals
that delete a message, so the message is kept and dead-letters on its third receive. So the binding's own pre-read must
show that queue at 0 and 0, or name what waits there, whenever it is cut.

## 7. Not established

- Why each job failed, beyond a class. Who the OTHER owner of #8 is. How a commentary-ready message came to be sent on
  2026-10-11 for a request whose job never left RECEIVED and whose record carries no commentary ref: that is IRPT_ANLREQ's
  to read, and it is the sharper question in this packet.
- What the worker does with a FAILED job on a redelivery.
- The dead-letter queue's expiry for the eight: its retention is 1,209,600 seconds; whether that runs from the original
  send or from the move was not read.

## COO HALF

**COO half SIGNED for the PROPOSAL only** -- `2.0.0_SA_COO~G2`: the eight are named, the claim on each column is stated, and
the write, its condition, its two branches and its per-key rollback are as sections 3 to 5 say. This half is not a go: no
write is ordered until the CTO half, and the executor is the laptop's.

## CTO HALF

(owed; and the PRD line for a failed job's record, which the CTO writes against these cases)
