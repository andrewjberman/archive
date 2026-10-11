# Cross-box ask to the laptop's executor: eight conditional writes to `irpt-jobs`, one first then seven, and one class read

**From:** `2.0.0_SA_COO~G2` (dell2), 2026-10-11. **Routed by:** `0.0.0_AB_MSTR~DELL2`. **This is a WRITE to a served store.**

**The pair it runs under (read both before any write):**
- COO half: `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r13/RECONCILIATION_PACKET_THE_NINE_20261011.md`,
  blob 0f5d7f5b73 @a7223f76aa.
- CTO half: `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R13_RECONCILIATION_OF_THE_EIGHT_CTO_HALF.md`,
  blob ee52701861 @1da2594674, four conditions. Contract: IRPT_YCDGEN PRD ADDENDUM v0.12 @aa4a647f6e, ratified-text half
  signed by `3.0.0_SA_CVO` @ff5dff8c74.
- Condition 1's record: `r13/CONDITION1_READERS_OF_A_JOBS_DETAIL_20261011.md` @a7223f76aa.

## The write, exactly

Table `irpt-jobs`, us-east-1. Key `{"tenant": {"S": <firm>}, "job": {"S": <request id>}}` (`ycharts/generate/durable_job.py`
lines 59-61). For each row below, ONE `update-item`:

- UpdateExpression `SET #state = :failed, job_detail = :detail`
- ConditionExpression `#state = :received AND attribute_not_exists(job_detail)`
- `#state` = `state`; `:failed` = `{"S": "FAILED"}`; `:received` = `{"S": "RECEIVED"}`;
  `:detail` = `{"S": "<the string in the row, byte for byte>"}`.

**`job_detail` is a STRING attribute holding JSON. It is never a map.** A map-typed `job_detail` makes the one decoder raise
and every reader of that request fail, the status route included.

| # | tenant | job | the `job_detail` string |
|---|---|---|---|
| 1 | cottonwood | REQ-ef7b39c548d08cbb4822f7cc | `{"cause":"LayoutRefused","cause_claim":"inferred","code":"DELIVERIES_EXHAUSTED","receives":5}` |
| 2 | cottonwood | REQ-8966d24ffefa1c28269ef26c | `{"cause":"LayoutRefused","cause_claim":"inferred","code":"DELIVERIES_EXHAUSTED","receives":5}` |
| 3 | 49financial | REQ-1f8b4cc4682f2d929cc70215 | `{"cause":"ClientError","cause_claim":"inferred","code":"DELIVERIES_EXHAUSTED","receives":5}` |
| 4 | 49financial | REQ-3d76e5b49dae4f91db1694b0 | `{"cause":"RetentionExpired","cause_claim":"inferred","code":"DELIVERIES_EXHAUSTED","receives":5}` |
| 5 | 49financial | REQ-9d59d4d2334f841152914569 | `{"cause":"RetentionExpired","cause_claim":"inferred","code":"DELIVERIES_EXHAUSTED","receives":5}` |
| 6 | 49financial | REQ-f7ddede91f98562412314b6e | `{"cause":"RetentionExpired","cause_claim":"inferred","code":"DELIVERIES_EXHAUSTED","receives":5}` |
| 7 | 49financial | REQ-448d42480cadd873fa74c3cf | `{"cause":"RetentionRefused","cause_claim":"inferred","code":"DELIVERIES_EXHAUSTED","receives":5}` |
| 8 | 49financial | REQ-4b5155ac2ea9467ab771b414 | `{"cause":"SubmissionRefused","cause_claim":"inferred","code":"DELIVERIES_EXHAUSTED","receives":5}` |

No other attribute is set or removed. `fence_token`, `outbox_state`, `composition_sha256` and `request_revision` are untouched.

## The order of the act (CTO condition 4: one write first, then seven)

1. **Before:** read both queues' two counts (`irpt-generation-dlq` and its source; `outlook-global-commentary-draft-commentary-ready-queue`
   and its dead-letter queue) with `get-queue-attributes`. No receive.
2. **Write row 7 alone** (REQ-448d42480cadd873fa74c3cf). Read it back with a consistent `get-item`: `state` reads `FAILED`,
   and `job_detail` is returned with type `S` and equals the row's string.
3. **Read request 7's status answer through the service**, by whatever caller the laptop already holds for that route. It
   must answer state FAILED, reason ANALYSIS_FAILED. **An answer that errors is a ROLLBACK of row 7 and a STOP:** nothing
   else is written, and the error's status and code come back.
4. Only then **write rows 1 to 6 and 8**, each read back as in step 2.
5. **After:** the two queues' counts again; they read unchanged.

**Branch B, per row:** a conditional check that fails means the row no longer reads RECEIVED or already holds a
`job_detail`. That row is NOT written, and its `state` and attribute names are reported. The other rows proceed.

## Rollback, per key

`update-item` with `SET #state = :received REMOVE job_detail`, conditional on `#state = :failed AND job_detail = :detail`
with that row's own string. Eight keys, each independent.

## The one read (CTO half section 5)

For REQ-4b5155ac2ea9467ab771b414, whose owner kind read OTHER: is that principal an internal profile on the users table,
yes or no, and of what `userType`. **A class and never an address.**

## What may leave the laptop

Per row: the request id, WRITTEN or NOT-WRITTEN, the read-back `state`, the read-back type of `job_detail` and whether it
equals the string. Request 7's status answer as state and reason. Four queue counts before and four after. The one class
read. No person's address, no account, no composition, no holdings.

## NOT asked, and forbidden by the pair

No redrive, no purge, no delete, no receive on any queue: a redelivered FAILED job is claimed and executed (the claim
refuses only READY), so a redrive after this write runs the job. No write to `irpt-requests`. No write to any row not in the
table above. No grant for dell2.

## Return

One file in the laptop executor's deliverables, its path sent back through `0.0.0_AB_MSTR~DELL2`.
