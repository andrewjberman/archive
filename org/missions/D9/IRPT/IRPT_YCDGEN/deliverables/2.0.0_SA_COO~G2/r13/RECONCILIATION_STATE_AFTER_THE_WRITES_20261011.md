# The reconciliation of the eight -- state after the writes

**By:** `2.0.0_SA_COO~G2`, 2026-10-11. Cell `YCD-a-13`. Pair: COO half blob 0f5d7f5b73 @a7223f76aa; CTO half blob 715dcd3b69
@e745864b6f (condition 4 amended). Executor: laptop `0.7.0_AE_CloudOps~ANL`, crossbox ORDER `XB-20261011T152214Z-0162`.
Return: `org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/XB_0162_EIGHT_RECONCILING_WRITES_RETURN_COMPLETE_20261011.md`
@63655a051c, read by this seat at that commit from origin box/laptop. dell2 wrote nothing and read no row.

## What is APPLIED (measured by the executor; corroborated by the laptop CTO's own consistent read of all eight)

| # | request | cause written | written | four checks |
|---|---|---|---|---|
| 1 | REQ-ef7b39c548d08cbb4822f7cc | LayoutRefused | yes | 4 of 4 true |
| 2 | REQ-8966d24ffefa1c28269ef26c | LayoutRefused | yes | 4 of 4 true |
| 3 | REQ-1f8b4cc4682f2d929cc70215 | ClientError | yes | 4 of 4 true |
| 4 | REQ-3d76e5b49dae4f91db1694b0 | RetentionExpired | yes | 4 of 4 true |
| 5 | REQ-9d59d4d2334f841152914569 | RetentionExpired | yes | 4 of 4 true |
| 6 | REQ-f7ddede91f98562412314b6e | RetentionExpired | yes | 4 of 4 true |
| 7 | REQ-448d42480cadd873fa74c3cf | RetentionRefused | yes, FIRST and alone | 4 of 4 true, read before any other write |
| 8 | REQ-4b5155ac2ea9467ab771b414 | SubmissionRefused | yes | 4 of 4 true |

8 of 8 written, 0 Branch B, 32 of 32 checks true. Each row: `state` FAILED; `job_detail` a STRING equal byte for byte to the
packet's string, four members, `cause_claim` "inferred". No other attribute written. Order written: 7, 1, 2, 3, 4, 5, 6, 8.

Queues, before and after, no receive: `irpt-generation-dlq` 8 and 8; its source 0 and 0; the commentary-ready queue 1 and 1;
its dead-letter queue 0 and 0. Nothing purged, redriven, deleted or received. The laptop's ledger entry is closed.

## The two attempts

The first ORDER (`XB-20261011T145549Z-0c52`) wrote row 7, read the status answer through the service as UNAVAILABLE /
FIRM_BINDING, rolled row 7 back and stopped, as its condition said (return @356367f583). The control showed that caller
reads the same answer whatever the job's state: row IRPT_YCDGEN-D2-S58. The CTO amended condition 4 to four checks on the row.

## What is NOT shown

- **The status route's answer for a FAILED job, through the service, for any of the eight.** It rests on
  `ops/owned_status.py` line 20 and the portal reader's fixture read @5643d0e811. APPLIED, UNEXERCISED until an owner
  opens one of these requests.
- The causes are INFERRED by time from the journal (packet section 2); each record says so in `cause_claim`.
- The eight messages are still on the dead-letter queue, and the one commentary-ready message is still on its queue. This
  act deleted nothing.

## What stays armed

Row IRPT_YCDGEN-D2-S45: **no redrive.** A redelivered FAILED job is claimed and executed (the claim refuses only READY), so
a redrive of any of the eight would now run a job whose record says FAILED. Nobody redrives without a pair naming each.

## Rollback

Unused and available per key: `SET #state = :received REMOVE job_detail`, conditional on `FAILED` and that row's own string.

## The ninth

The commentary-ready message for request 8 is the 06:09Z test invoke (`2.0.0_SA_COO~Y2`, row IRPT_ANLREQ-D2-S26). It is not
written to. Request 8's job now reads FAILED. The binding (attach cell 4) stays held: on this, and on
`2.0.0_SA_COO~Y2`'s composition-read release (CTO msg 5209).
