# NFRA_CLDGRPH.TO-CG-B-1 -- CG-s-1: the marker write becomes a queue message

**Seat:** `0.7.0_AE_CloudOps~P` · **Issuer:** `2.0.0_SA_COO~A` · **GO:** msg 93401 @`585daff578` (READ-acked)
**Cell:** `CG-s-1` of `../../decompositions/NFRA_CLDGRPH_DECOMP.md` @`994c9381d0` (ROUND 2, STAGE 1's first cell)
**Window:** 2026-09-03 08:5xZ - 11:1xZ (with an account-wide usage-limit pause 09:38Z-11:0xZ, issuer 93509)
**Applied:** YES -- scoped, under the issuer's 09:16Z ruling. **The four foreign items never landed.**

---

```json
{
  "to_id": "NFRA_CLDGRPH.TO-CG-B-1",
  "cell": "CG-s-1",
  "seat": "0.7.0_AE_CloudOps~P",
  "queue_arn": "arn:aws:sqs:us-east-1:313476888478:opal-globgrph-projection-events",
  "dlq_arn": "arn:aws:sqs:us-east-1:313476888478:opal-globgrph-projection-events-dlq",
  "role_arn": "arn:aws:iam::313476888478:role/opal-globgrph-projection-worker",
  "notification_rule_id": "projection-branch-head-marker",
  "bucket": "opal-313476888478-globgrph",
  "key_prefix": "warehouse/_branch_head.main.json",
  "live_config_before": "EMPTY (rc=0, 0 bytes) -- proven with a positive AND a negative control",
  "live_config_after": "exactly ONE QueueConfiguration; the diff is the one added rule",
  "apply": "safe-apply -target on the six; 'Apply complete! Resources: 6 added, 0 changed, 0 destroyed.'",
  "unscoped_replan": "EXACTLY the 4 known foreign items, NONE of the 6 -- asserted by ADDRESS LIST, not by count",
  "exercised": "2 real producer stamps -> 2 distinct messages (+1 S3 TestEvent); producer = opal-globgrph-incremental-updater, NOT this seat",
  "dlq_caveat": "DLQ was 0 throughout the exercise; it is now 3 because THIS SEAT over-polled -- see D.3. Self-inflicted, disclosed, benign.",
  "visibility_timeout": "30 (AWS default) -- CG-s-2 SETS THIS from CG-s-10's measured duration",
  "surprise_rows": ["NFRA_CLDGRPH-S13"]
}
```

---

## A. B1-AC1 -- the live config, read FIRST, and the hazard it defuses

`aws_s3_bucket_notification` is the **whole** notification configuration of a bucket: applying one silently replaces
any live configuration Terraform does not declare. That is why this is criterion one. **The read was taken before a
line of Terraform was written.**

**BEFORE:**

```
aws s3api get-bucket-notification-configuration --bucket opal-313476888478-globgrph
  -> rc=0, 0 bytes.   EMPTY. No notification configuration of any kind.
```

⛔ **An empty read here carries a verdict, so it was PROVEN, not assumed** -- three calls, same command shape:

| arm | bucket | result | what it rules out |
|---|---|---|---|
| target | `opal-313476888478-globgrph` | rc=0, **0 bytes** | -- |
| **POSITIVE CONTROL** | `opal-data-portal-v2` | rc=0, **1486 bytes** (`LambdaFunctionConfigurations`) | the call returning empty because it is broken |
| **NEGATIVE CONTROL** | a nonexistent bucket | **rc=255 `NoSuchBucket`** | an error being mistaken for an empty success |

So `rc=0`-and-empty is genuinely ABSENCE. **Nothing pre-existed, so nothing could be lost** -- the hazard is real in
general and vacuous here, which is a measured conclusion rather than a lucky one. `item2b`'s CloudTrail path is
**EventBridge**, not a bucket notification, so it never appears in this configuration and was never at risk.

**AFTER (the control the criterion asks for -- the diff is exactly the one added rule):**

```json
{"QueueConfigurations": [{
  "Id": "projection-branch-head-marker",
  "QueueArn": "arn:aws:sqs:us-east-1:313476888478:opal-globgrph-projection-events",
  "Events": ["s3:ObjectCreated:*"],
  "Filter": {"Key": {"FilterRules": [{"Name": "Prefix", "Value": "warehouse/_branch_head.main.json"}]}}}]}
```

EMPTY -> one rule. Nothing carried, nothing dropped, no EventBridge configuration to preserve.

## B. B1-AC2 -- the DESIRED text

`infra/aws/terraform/globgrph/projection.tf`, beside `item2b.tf`, whose queue/DLQ/redrive/policy shape it copies with
the queue-policy **principal changed from `events.amazonaws.com` to `s3.amazonaws.com`**:

- `aws_sqs_queue.globgrph_projection_events` -- retention 3600s and long-poll 20s mirroring `item2b.tf:18,19`;
  redrive to the DLQ at `maxReceiveCount 3`; **`visibility_timeout_seconds = 30`, the AWS default, deliberately**,
  carrying a comment that **CG-s-2 sets it from CG-s-10's measured full-fallback duration.**
- `aws_sqs_queue.globgrph_projection_events_dlq` -- 86400s, mirroring `item2b.tf:30`.
- `aws_sqs_queue_policy.globgrph_projection_events` -- `s3.amazonaws.com` only, `sqs:SendMessage` only, conditioned
  on **`aws:SourceArn` = the bucket ARN** and `aws:SourceAccount` = the account. Without those conditions this would
  be an open grant to the whole S3 service.
- `aws_s3_bucket_notification.globgrph_warehouse_marker` -- ONE queue rule, `s3:ObjectCreated:*`, prefix
  `warehouse/_branch_head.main.json`, `depends_on` the queue policy **because S3 validates queue reachability at
  create time** and the apply fails without it.
- `aws_iam_role.globgrph_projection_worker` -- trust policy naming **both** `lambda.amazonaws.com` and
  `ecs-tasks.amazonaws.com`, so CG-s-2's still-open runtime choice does not have to reopen this cell.
- `aws_iam_role_policy.projection_worker_sqs` -- **statement (i) of TO-CG-V-2's B.3 delta ONLY**: the four
  queue-consume actions on the new queue ARN. The S3-read / projection-write / logs statements of that same delta are
  CG-s-2's; granting them now would give an identity permissions it cannot yet use.

No CloudTrail rule, no EventBridge rule, no schedule, no Lambda, no ECS task, no event source mapping.

**Checks before any apply:** `terraform init` OK · `terraform validate` **Success** · `terraform fmt -check` **clean
(rc=0, no diff)** · `comp-iam gaps` delta confined to **the parser's own denominators** -- 396 -> 397 `.tf` files
scanned, 357 -> 358 attached policy blocks -- with the gap counts **UNCHANGED** at
`14 missing | 292 deny-present | 0 coverage-unknown | 2 resource-mismatch across 31 services`. The new role adds
**zero gaps**, which is correct while no code calls it. `comp-iam role opal-globgrph-projection-worker` parses to
1 statement / 4 sqs actions.

## C. B1-AC3 -- the STOP, the ruling, and the scoped apply

### C.1 The plan refused

```
Plan: 8 to add, 2 to change, 0 to destroy.
```

The face's own words: *"a non-zero change/destroy count is a STOP and a row."* **My six were exactly the six
specified.** Four were foreign to this cell:

| address | action | owner |
|---|---|---|
| `aws_glue_partition.tool_activity["rolling_log"]` | update in place | `tool_activity.tf` @`981719334a`, `0.8.0_AE_CloudComp`, 2026-08-21 |
| `aws_glue_partition.tool_activity["rolling_log_summary"]` | update in place | as above |
| `aws_glue_partition.tool_activity["routing"]` | create | as above |
| **`aws_sns_topic_subscription.critical_surface_alerts_email`** | **create, email -> `andrew@opalinvest.com`** | `item2c_surface_alarm.tf` @`446f00ecaf`, `0.7.0_AE_CloudOps`, **2026-06-17** |

⛔ **The last one is a RECORDED ANDREW EXCLUSION**, not merely an unowned resource:
`ZGATES_PREFLIGHT_VERIFIED_20260714.md:37` -- *"THE EXCLUSION (must NOT land)"*; the 2026-07-14 CloudOps session log
-- *"NOT touched (by design) ... excluded per Andrew"*; and `3.0.0_SA_CVO~Z` flagged the identical module-wide-apply
hazard as a **P1 apply-leg flag** on 2026-07-14. A bare apply would have sent a real confirmation email to a real
person and landed three Glue changes owned by another cell.

⭐ **These are not peer worktree edits -- they are COMMITTED text never applied**, which is what makes them a standing
trap rather than a transient one. Measured: `git status --porcelain infra/aws/terraform/globgrph` returned **exactly
one line**, `?? projection.tf`, this seat's own file. The tree has carried unapplied DESIRED Terraform for up to
**~2.5 months**. That is Rule 22a's DESIRED != APPLIED axis in the concrete, and it is a hazard for **every** seat
that applies here, not only for this task order. Filed as **`NFRA_CLDGRPH-S13`** (BLOCKING/ARMED) and routed to the
issuer in the same turn.

### C.2 The ruling, and the apply under it

`2.0.0_SA_COO~A` msg 93430 adopted the recommendation: `-target` the six; verify with **one UNSCOPED re-plan asserted
by ADDRESS LIST**, never a `-target` re-plan (CLAUDE.md Rule 22's scoped-check specimen); the four foreign items never
land; B1-AC3's 0-diff limb amended to that bar on the face @`e23ac771bf`.

```
TARGETED PLAN:  Plan: 6 to add, 0 to change, 0 to destroy.     (all six "will be created")
safe-apply:     Apply complete! Resources: 6 added, 0 changed, 0 destroyed.
```

`safe-apply` first **blocked** on the HALT gate with 2 pending base-inbox messages. Both were read before
acknowledging: a 2026-08-31 `1.0.0_SA_CTO` measurement request about Cottonwood session cadence (itself saying "no
deploy/apply"), and a **later message from the same sender standing that request down as superseded**. Neither
STOP-class, neither globgrph-related, both addressed to the base serial. Re-run with `HALT_ACK=1`. The apply consumed
a **saved plan file**, so what landed is exactly what was reviewed.

### C.3 The verification -- unscoped, by address list

```
UNSCOPED RE-PLAN -- FULL ADDRESS LIST: 4
   will be updated in-place  aws_glue_partition.tool_activity["rolling_log"]
   will be updated in-place  aws_glue_partition.tool_activity["rolling_log_summary"]
   will be created           aws_glue_partition.tool_activity["routing"]
   will be created           aws_sns_topic_subscription.critical_surface_alerts_email
Plan: 2 to add, 2 to change, 0 to destroy.

ASSERTION 1 -- none of the six appears:            PASS  (a missing one would reappear as an add)
ASSERTION 2 -- exactly the four known foreign:     EXACT MATCH (0 absent, 0 extra)
```

**This control fails in both directions**, which is why it replaces the unreachable 0-diff: a resource of mine that
failed to land would reappear as an add, and a foreign item that accidentally landed would vanish from the list.
**Re-confirmed unchanged at 11:10Z**, ~90 minutes and one account-wide pause later.

**Independent live confirmation that the excluded resource did not land** -- read on SNS itself, not inferred from the
plan: `list-subscriptions-by-topic` on `opal-critical-surface-alerts` returns an `sqs` subscription and an `sms`
subscription, and **no `email` subscription to `andrew@opalinvest.com`**.

**APPLIED-plane read (L2).** `comp-iam refresh-census` -> `2026-09-03T09:27:12Z`, role denominator **216 -> 217**.
`opal-globgrph-projection-worker` is PRESENT and **matches DESIRED exactly**: trust policy
`Service: [lambda.amazonaws.com, ecs-tasks.amazonaws.com]`, one inline `SQSConsume` statement, exactly the four sqs
actions, scoped to the new queue ARN and nothing else.

**Ledger.** `cldgrph-cgs1-marker-notification-projection-queue`, opened **before** the plan per NEVER-2. L1/L2/L3
closed with proof. While the apply was refused, the entry was deliberately left OPEN/RED -- `deploy_ledger.py hold`
refused it ("a half-landed deploy cannot be HELD") and closing a leg that never ran would have put a **false CLOSED**
on the record. Nothing was ever half-landed.

## D. B1-AC4 -- EXERCISED on real producer stamps

### D.1 Two real stamps, two messages

Observed 09:23Z-09:26Z, depth `0 -> 3`:

| # | eventTime | eventName | eTag | sequencer |
|---|---|---|---|---|
| TestEvent | 2026-09-03T09:23:39.600Z | `s3:TestEvent` | -- | -- |
| 1 | 2026-09-03T09:24:47.402Z | `ObjectCreated:Put` | `edd69d9801308a45559ab0171d8d0c30` | `006A993CDF6073941A` |
| 2 | 2026-09-03T09:25:18.902Z | `ObjectCreated:Put` | `2e0ac88ebcef5b496823a559c349df62` | `006A993CFEDCDE5C9D` |

**2 distinct eventTimes, 2 distinct eTags, 2 distinct sequencers** -- genuinely two separate writes, not one message
counted twice. That is the "a SECOND stamp lands a SECOND message" arm, and it could have failed.

⭐ **The `s3:TestEvent` is a bonus control I did not have to construct:** AWS emits exactly one when a notification
configuration is created. Its presence at 09:23:39Z is independent proof the rule was wired by this apply.

One full body, verbatim in the deciding fields:

```json
{"eventSource":"aws:s3","awsRegion":"us-east-1","eventTime":"2026-09-03T09:25:18.902Z",
 "eventName":"ObjectCreated:Put",
 "userIdentity":{"principalId":"AWS:AROAUR7FNW6PIZYLEKZRE:opal-globgrph-incremental-updater"},
 "s3":{"configurationId":"projection-branch-head-marker",
       "bucket":{"name":"opal-313476888478-globgrph","arn":"arn:aws:s3:::opal-313476888478-globgrph"},
       "object":{"key":"warehouse/_branch_head.main.json","size":1508,
                 "eTag":"2e0ac88ebcef5b496823a559c349df62","sequencer":"006A993CFEDCDE5C9D"}}}
```

**NO STAMP WAS MADE BY THIS SEAT, and the proof is stronger than an invocation log:** every event carries
`userIdentity.principalId = ...opal-globgrph-incremental-updater` -- a real producer, on the event's own face. The
marker key was never written by this seat (`probe_ifmatch_cas.py:81` forbids it).

**Marker consistency:** `head-object` on the key at the time returned ETag `2e0ac88ebcef5b496823a559c349df62`,
LastModified `09:25:19 GMT` -- matching event 2 exactly. The marker's own schema carries `committed_at_iso`,
`nessie_commit_hash`, `table_metadata`, `writer_id`.

**Routing:** every real event carries `configurationId: projection-branch-head-marker` -- this cell's rule did the
routing, not some pre-existing path.

### D.2 Why the queue reads 0 now, and why that is CORRECT

At 11:10Z the main queue is empty. That has two possible causes and they were **discriminated rather than assumed**:
the marker's `LastModified` is **09:42:42Z**, i.e. the producer wrote once more (during the account-wide pause) and
has been **quiet ~88 minutes since**. Retention is 3600s, so the 09:42 message expired ~10:42Z. The notification rule
is still configured and was re-read to confirm it. **Depth 0 is the producer being quiet, not a broken notification**
-- and it corroborates the face's own warning that stamps are not guaranteed frequent (CG-s-10 measured a 1h58m quiet
window; the nightly derive at 02:00Z guarantees one per day).

### D.3 ⛔ THE DLQ IS 3, AND THIS SEAT PUT IT THERE

**DLQ depth was 0 throughout the exercise above.** It is now **3**, and the cause is my own probing, not a defect:

> I called `receive-message` **four times** while collecting the message bodies. **Every `ReceiveMessage` increments
> `ApproximateReceiveCount`, including with `--visibility-timeout 0`** -- which I had used precisely to leave the
> messages visible. The redrive policy is `maxReceiveCount: 3`. So the fourth poll redrove all three messages to the
> DLQ.

**Impact: benign, and disclosed rather than tidied.** No consumer exists yet (CG-s-2 is unbuilt), so nothing was lost
from a pipeline; the DLQ retains 24h and will self-clear by ~09:25Z on 2026-09-04; the messages were never deleted.
**The wiring is not implicated -- if anything the redrive policy is now demonstrably exercised**, which no criterion
asked for. The DLQ was NOT purged: purging would destroy the evidence of what happened.

⭐ **AND IT IS A REAL HANDOFF FINDING FOR CG-s-2, which is why it is written up rather than buried.** It is a live
demonstration of what happens when consumption outlives the visibility timeout: at `visibility_timeout = 30s` and
`maxReceiveCount = 3`, **a worker whose run exceeds 30s will re-receive its own message and DLQ it on the third
attempt.** CG-s-10's measured full-fallback duration is very unlikely to be under 30 seconds. **CG-s-2 must raise the
visibility timeout before it consumes anything** -- the face already says so; this is the concrete cost of not doing it.

## E. B1-AC5 -- the handoff lines for CG-s-2

| | value |
|---|---|
| **queue ARN** | `arn:aws:sqs:us-east-1:313476888478:opal-globgrph-projection-events` |
| **queue URL** | `https://sqs.us-east-1.amazonaws.com/313476888478/opal-globgrph-projection-events` |
| **DLQ ARN** | `arn:aws:sqs:us-east-1:313476888478:opal-globgrph-projection-events-dlq` |
| **role ARN** | `arn:aws:iam::313476888478:role/opal-globgrph-projection-worker` |
| **trust** | `lambda.amazonaws.com` **and** `ecs-tasks.amazonaws.com` -- the runtime choice is still CG-s-2's |
| **role holds** | queue-consume ONLY. **CG-s-2 adds** the S3 read, the `projection/` write and logs (TO-CG-V-2 B.3 (i)) |
| **redrive** | `maxReceiveCount: 3` -> the DLQ |
| **retention** | main 3600s, DLQ 86400s |

**Message body shape:** the standard S3 event envelope -- `{"Records":[{...}]}` with `eventName`
(`ObjectCreated:Put`), `eventTime`, `userIdentity.principalId` (the producing writer),
`s3.configurationId` (`projection-branch-head-marker`), `s3.bucket.name`, and `s3.object.{key,size,eTag,sequencer}`.
⚠ **Two shapes arrive on this queue, and a consumer must tolerate both:** the real event above, and the one-off
`{"Service":"Amazon S3","Event":"s3:TestEvent",...}` which has **no `Records` key at all**. A consumer that assumes
`Records` will crash on it -- this seat's own first parser did exactly that.
⚠ **Bucket versioning is Andrew-locked OFF** (GLOBGRPH PRD s.0 #5), so events carry **no `versionId`**; use `eTag` +
`sequencer` for object identity, never a version.

> ### VISIBILITY TIMEOUT IS CG-s-2's TO SET
> It is **30s (the AWS default)** and deliberately untuned here, because the number comes from **CG-s-10's measured
> full-fallback duration**, which this cell does not have. See D.3 for what happens if it is left at 30.

## F. B1-AC6 -- push state and the proof instance

Recorded in the report to `2.0.0_SA_COO~A` and in section G, measured with `ls-remote` + `is-ancestor`, never
defaulted.

## G. Surprise channel

**`NFRA_CLDGRPH-S13`** (BLOCKING / ARMED, disarm owner `2.0.0_SA_COO~A`) -- **filed as S11 and renumbered to S13**
after `0.7.0_AE_CloudOps~Q` claimed S11, then S12, in the same minutes on the shared append-only file. The issuer's
ruling (93430) is titled "RULING on NFRA_CLDGRPH-S11" and refers to **this row, now S13**; the id `S11` no longer
exists and `S12` is `~Q`'s unrelated row. Recorded here because a citation that silently retargets is worse than a
renumber that is announced. **DISARMED** by the issuer's ruling + face amendment @`e23ac771bf`; the apply then
proceeded under it.

The DLQ event in D.3 is **not** filed as a row: it is not a spec-vs-world divergence but this seat's own probing
error, fully disclosed here, in the ledger and in the report.
