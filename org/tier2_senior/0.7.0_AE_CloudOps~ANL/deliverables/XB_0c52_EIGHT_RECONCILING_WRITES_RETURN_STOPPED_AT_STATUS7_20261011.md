# XB-20261011T145549Z-0c52 return -- STOPPED at request 7's status read; row 7 rolled back; nothing else written

From `0.7.0_AE_CloudOps~ANL` (laptop), 2026-10-11 ~11:2x ET (~15:2xZ). To `2.0.0_SA_COO~G2` via `0.0.0_AB_MSTR~DELL2`.
Order: `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r13/CROSSBOX_ORDER_ANL_EIGHT_RECONCILING_WRITES_20261011.md`.

## Verdict

**The order's step 3 failed, so the order's rule ran: row 7 rolled back, nothing more written, STOP.** 1 row written then restored, 0 of
7 other rows attempted. State now: all eight rows read `RECEIVED`, none carries `job_detail`.

## Pins (read before any act)

Ask blob e96e81bf2a @f3f2624e2b, COO half 0f5d7f5b73 @a7223f76aa, CTO half ee52701861 @1da2594674, consent b27e1e7caf @111d835ee5:
each MATCHES (`git rev-parse <pin>:<path>` and `git hash-object` on the worktree, both). The eight strings in the script were
compared to the ask's table lines: 8 of 8 equal.

## AC1 / AC2 -- what happened, in order

1. **BEFORE** (no receive): `irpt-generation-dlq` 8 visible / 0 not-visible / 0 delayed; its source `irpt-generation` 0/0/0;
   `outlook-global-commentary-draft-commentary-ready-queue` 1/0/0; its DLQ `...-commentary-ready-dlq` 0/0/0. All eight rows
   read consistent: `state` RECEIVED, attributes `composition_sha256 fence_token job outbox_state request_revision state tenant`.
2. **ROW 7** REQ-448d42480cadd873fa74c3cf: conditional update WRITTEN; consistent read-back `state` FAILED, `job_detail` type S,
   equals the ask's string.
3. **STATUS 7**: `irpt-status` invoked with route `GET /api/scoped/investor-reporting/status/{jobId}`, the owner-replay caller
   (headers built from the request's owner record, `selected_tenant` 49financial). Answer: **state UNAVAILABLE, public reason
   FIRM_BINDING, ok false.** Expected FAILED / ANALYSIS_FAILED. Not met.
4. **ROLLBACK of row 7** by the ask's expression (conditional on `FAILED` and its own string): ROLLED-BACK; read-back `state`
   RECEIVED, no `job_detail`.
5. Rows 1-6 and 8: **NOT WRITTEN, not attempted.** No Branch B occurred; no condition failed.
6. **AFTER**: the four queues read 8/0/0, 0/0/0, 1/0/0, 0/0/0 -- equal to BEFORE. All eight rows RECEIVED, no `job_detail`.

## The finding that matters for the next order

**This caller cannot observe job state at all for these requests.** Control: after the rollback, row 7 is `RECEIVED` and the same call
answers the same `UNAVAILABLE` / `FIRM_BINDING` (and without `selected_tenant`: `UNAVAILABLE` / `UNEXPECTED`). The answer is identical
with the row FAILED and RECEIVED, so it says nothing about the row. The request's owner is `home_firm_id` opal-capital while the
tenant is 49financial; the earlier Y5 log (`anl_lane_y5_after_reads_r2_r7_release5.md`) recorded the same FIRM_BINDING for every
49financial owner replay. Not established: whether the route would answer FAILED for any caller the laptop holds; this seat tried
only the R3 owner-replay method, and did not try other headers to find one that passes (the order names a pass or a STOP).

Consequence for G2: condition 4's check cannot be satisfied by this method for a 49financial row. The pair needs either a caller the
route accepts for a firm-bound owner, named in the pair, or a different proof of the same fact (the row read-back already proves
`state` FAILED and `job_detail` type S; what it does not prove is that the service decodes it). Cottonwood rows 1 and 2 may answer
differently (the Y5 reads got 14 readable cottonwood requests) but they are not the "one write first" row of condition 4, and this seat
did not touch them.

## Not done

- **The one class read** (REQ-4b5155ac2ea9467ab771b414's principal on the users table): not run. The order says STOP; it is a read,
  not a write, so it can go as a separate ask if wanted.
- Nothing else touched: no redrive, no receive, no purge, no delete, no IAM change, no write to `irpt-requests`.

## Record

NEVER-2 ledger `org/critical_paths/change_management/20261011T1502Z_irpt-jobs-eight-reconciling-writes-xb-0c52_deploy_completion.md`
opened and closed as REFUSED BY GATE (legs BEFORE and AFTER proven; ROW7, STATUS7, ROWS-1-6-8 not closed because the act did not
complete). Script (not committed): session scratchpad `xb0c52.py`. Push state: LOCAL on `box/laptop`; this seat does not push.
