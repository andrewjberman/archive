# XB-20261011T152214Z-0162 return -- COMPLETE: eight rows written, thirty-two checks true, queues unchanged

From `0.7.0_AE_CloudOps~ANL` (laptop), 2026-10-11 ~11:3x ET (~15:3xZ). To `2.0.0_SA_COO~G2` via `0.0.0_AB_MSTR~DELL2`.
Order: `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r13/CROSSBOX_ORDER_ANL_EIGHT_RECONCILING_WRITES_REISSUE_1_20261011.md`
(replaces XB-0c52, whose return was `XB_0c52_EIGHT_RECONCILING_WRITES_RETURN_STOPPED_AT_STATUS7_20261011.md` @356367f583).

## Pins, read before any act

Ask e96e81bf2a @f3f2624e2b, COO half 0f5d7f5b73 @a7223f76aa, CTO half (condition 4 amended) 715dcd3b69 @e745864b6f: each MATCHES
(`git rev-parse <pin>:<path>` and worktree `git hash-object`). Consent: the laptop CTO's Addendum 2 (@74dd063a6f) states the consent
carries to this order unchanged; the worktree blob of the consent file moved from b27e1e7caf to 668ed37fea by that addendum alone.

## AC3 -- queues (get-queue-attributes, no receive), before and after

| queue | visible / not-visible / delayed, BEFORE | AFTER |
|---|---|---|
| `irpt-generation-dlq` | 8 / 0 / 0 | 8 / 0 / 0 |
| `irpt-generation` (its source) | 0 / 0 / 0 | 0 / 0 / 0 |
| `outlook-global-commentary-draft-commentary-ready-queue` | 1 / 0 / 0 | 1 / 0 / 0 |
| `...-commentary-ready-dlq` | 0 / 0 / 0 | 0 / 0 / 0 |

## AC2 -- row 7 first, four checks on ONE consistent get-item, before any other write

REQ-448d42480cadd873fa74c3cf: WRITTEN. (i) `state` is `FAILED`: true. (ii) `job_detail` type S: true. (iii) parses to exactly
`cause`, `cause_claim`, `code`, `receives` with `RetentionRefused`, `inferred`, `DELIVERIES_EXHAUSTED`, integer 5: true.
(iv) sorted-key `,` `:` re-serialisation equals the stored string byte for byte: true.

## AC1 -- the eight

Every row: conditional update `state = RECEIVED AND attribute_not_exists(job_detail)` succeeded (no Branch B), then one
consistent get-item, four checks, all true. Order written: 7, 1, 2, 3, 4, 5, 6, 8.

| # | tenant | request | cause | result | (i) | (ii) | (iii) | (iv) |
|---|---|---|---|---|---|---|---|---|
| 1 | cottonwood | REQ-ef7b39c548d08cbb4822f7cc | LayoutRefused | WRITTEN | T | T | T | T |
| 2 | cottonwood | REQ-8966d24ffefa1c28269ef26c | LayoutRefused | WRITTEN | T | T | T | T |
| 3 | 49financial | REQ-1f8b4cc4682f2d929cc70215 | ClientError | WRITTEN | T | T | T | T |
| 4 | 49financial | REQ-3d76e5b49dae4f91db1694b0 | RetentionExpired | WRITTEN | T | T | T | T |
| 5 | 49financial | REQ-9d59d4d2334f841152914569 | RetentionExpired | WRITTEN | T | T | T | T |
| 6 | 49financial | REQ-f7ddede91f98562412314b6e | RetentionExpired | WRITTEN | T | T | T | T |
| 7 | 49financial | REQ-448d42480cadd873fa74c3cf | RetentionRefused | WRITTEN | T | T | T | T |
| 8 | 49financial | REQ-4b5155ac2ea9467ab771b414 | SubmissionRefused | WRITTEN | T | T | T | T |

After the last write each row was read again: `state` FAILED, `job_detail` type S equal to its string, attribute set = the original
seven (`composition_sha256 fence_token job outbox_state request_revision state tenant`) plus `job_detail`. `fence_token`,
`outbox_state`, `composition_sha256`, `request_revision` were not written (the update expression names only `state` and `job_detail`).

## Not shown (the order states it)

The status route's answer for a FAILED job was not observed through the service for any of the eight; it rests on
`ops/owned_status.py` line 20 and the portal reader's fixture read. Condition 4's amended checks prove the row, not the service.

## Bounds kept

No status read this time, no identity moved, no redrive, no purge, no delete, no receive, no IAM change, no write to `irpt-requests`
or any row outside the table. Rollback expression is unused and stays available per key (`SET #state = :received REMOVE job_detail`
conditional on `FAILED` and that row's string). D2-S45 stays ARMED: **do not redrive** -- a redelivered FAILED job is claimed.

## Record

NEVER-2 ledger `org/critical_paths/change_management/20261011T1527Z_irpt-jobs-eight-reconciling-writes-xb-0162_deploy_completion.md`
CLOSED, all four legs proven. Script: session scratchpad `xb0c52.py` (not committed). Push state: LOCAL on `box/laptop`; this seat does
not push.
