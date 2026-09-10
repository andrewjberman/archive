# EG-s-18 result -- THE SCHEDULES' FIRING FROM HISTORY

**TO:** `ETFS_GUARDRAIL.TO-EG-s-18`, **AMENDED** by the issuer 2026-09-09 ~23:5xZ on rows
`ETFS_GUARDRAIL-W1-S13` / `ETFS_GUARDRAIL-W2-S7` (CLOUD @`5507841f04`), and arm (c) **CORRECTED
AGAIN** 2026-09-10 ~00:3xZ on `ETFS_GUARDRAIL-W2-S10` | **Worker:**
`0.9.0_WK_ETFS_GUARDRAIL~3` | **Branch:** `wk-etfs_guardrail-2-3`
**Method:** LIVE AWS reads only -- no invoke, no write, no deploy. Identity
`arn:aws:iam::313476888478:user/Andrew_Berman` (the launching seat's, decomposition s.3 decision 1).
85 read calls, all rc=0.
**Battery:** `test_egs18_schedules_from_history.py` in this folder, implementing the **AMENDED** arms.
**AC1 run:** rc=0, prints `EGS18-SCHEDULES-FIRED-FROM-HISTORY`. Full output verbatim at s.8.

---

## 1. THE HEADLINE, WITH ITS DENOMINATOR

```
  fires  4 of events 18, initiator = etfs-reports-scheduler-role   [etfs-reports-monthly-run, 90d]
  fires 30 of events 53, initiator = cot-etf-ownership-daily-schedule           [30d]
  fires 30 of events 31, initiator = bd-49f-etf-ownership-scheduled-floor       [30d]
```

All three schedules are **ENABLED** and **HAVE FIRED**. **3 of 3** monthly instants due in the 90-day
window fired (2026-07-01, 2026-08-01, 2026-09-01, each an `AssumeRole` at **14:00:14Z** joined to an
orchestrator `START` 1 second later). Both daily rules fired **30 of 30 days** -- cot at **10:30:24Z**,
bd-49f at **10:45:05Z** -- reproducing worker `~2`'s cited numbers **exactly**.

**The one finding that is not a green:** the **currently-served August artifact does not carry the
timestamp of any rule-initiated fire.** Every object under `platinum/reports/2026-08/` reads
`LastModified = 2026-09-01T17:38:41Z / 17:38:42Z` (head-object), while the 2026-09-01 fire ran at
14:00:14Z -- a **3 h 38 m** gap on a day with one orchestrator invocation. Evidence in s.4.2.

---

## 2. ARM (a) -- THE CONFIGURATION READ, LIVE

Two of the three are **not the same kind of object**, and that difference is load-bearing for arms (b)/(c):

| # | name | KIND | verb | expression | tz | state | target / role |
|---|---|---|---|---|---|---|---|
| 1 | `etfs-reports-monthly-run` | **EventBridge SCHEDULER schedule**, group `default` | `scheduler get-schedule` | `cron(0 10 1 * ? *)` | `America/New_York` | ENABLED | target `...:function:etfs-reports-orchestrator`, Input `{"mode":"run"}`, **RoleArn `.../etfs-reports-scheduler-role`**, RetryPolicy `{MaximumEventAgeInSeconds: 86400, MaximumRetryAttempts: 185}`, FlexibleTimeWindow OFF, CreationDate = LastModificationDate = `2026-06-25T22:27:48Z` |
| 2 | `cot-etf-ownership-daily-schedule` | **EventBridge RULE**, bus `default` | `events describe-rule` + `list-targets-by-rule` | `cron(30 10 * * ? *)` | UTC | ENABLED | target `...:function:cot-etf-ownership-daily`, Id `CotEtfOwnershipDailyLambda`, Input **ABSENT**, **RoleArn ABSENT** |
| 3 | `bd-49f-etf-ownership-scheduled-floor` | **EventBridge RULE**, bus `default` | same | `cron(45 10 * * ? *)` | UTC | ENABLED | target `...:function:bd-49f-etf-ownership-daily`, Id `Bd49fEtfOwnershipScheduledFloor`, Input **ABSENT**, **RoleArn ABSENT** |

**`RoleArn ABSENT` on both daily targets is measured, not assumed, and it is a divergence from the
amendment's text** (row `ETFS_GUARDRAIL-W3-S3`): the amendment names the daily roles "from
`list-targets-by-rule` / `get-schedule`", but an EventBridge rule targeting Lambda carries no role -- it
invokes through the function's resource-based policy -- and neither daily trigger is a Scheduler schedule.
The role whose history arm (c) reads is therefore the **function's execution role**, named from
`lambda get-function-configuration --query Role` and printed at the point of use:
`arn:aws:iam::313476888478:role/cot-etf-ownership-daily-role` and
`arn:aws:iam::313476888478:role/bd-49f-etf-ownership-daily-role`. The re-cut's numbers reproduce exactly
on those roles, so this is a naming gap and not a substantive one.

**NEXT SCHEDULED FIRE (UTC) -- CONFIRMATION, NEVER A GATE**, derived from the live expressions:

```
  etfs-reports-monthly-run                 2026-10-01T14:00:00Z   (cron(0 10 1 * ? *) America/New_York)
  cot-etf-ownership-daily-schedule         2026-09-10T10:30:00Z   (cron(30 10 * * ? *) UTC)
  bd-49f-etf-ownership-scheduled-floor     2026-09-10T10:45:00Z   (cron(45 10 * * ? *) UTC)
```

---

## 3. COVERAGE-ABSENT -- the CloudTrail `Invoke` read, re-cut

Executed and reported, **never a pass and never a fail** (amendment limb iii):

```
  trail=opal-organization-trail          data-resource types = AWS::S3::Object
  trail=opal-served-key-write-trail      data-resource types = AWS::S3::Object
  lookup-events EventName=Invoke over <90d window> : 0 event(s), 1 page(s)
  COVERAGE-ABSENT: 0 of 2 trails select AWS::Lambda::Function
```

A third independent read of the fact the amendment rests on (`W1-S13`, `W2-S7`), on this worker's own
instrument. **No new row is minted for it** -- post-amendment the face asks for this line, so it is no
longer a spec-vs-world mismatch.

---

## 4. ARM (b) -- THE MONTHLY HISTORY, FROM THE `AssumeRole` PLANE

### 4.1 The six rows, and why four of them are fires

`lookup-events ResourceName=arn:aws:iam::313476888478:role/etfs-reports-scheduler-role`, fully paginated:
**7 events, 6 AssumeRole, 6 distinct requestIDs**. Denominator printed: 6 of 7.

**A negative control on the lookup key**, so the ARN form is not taken on faith: the **bare** role name
returns 2 events (`CreateRole`, `PutRolePolicy`) and **0 AssumeRole**. An `AssumeRole` event's
`AWS::IAM::Role` resource carries the ARN form; the bare name reaches only IAM lifecycle events. A reader
who used the bare name would conclude the schedule never fired.

| AssumeRole (UTC) | class | requestID | orchestrator START (join tol 60 s) |
|---|---|---|---|
| 2026-06-25T22:27:48Z | ROLE-VALIDN | `9552122c-5856-4923-81a9-fdf63b6fd5eb` | (no START in window) |
| 2026-06-25T22:27:48Z | ROLE-VALIDN | `c5899520-1917-4b3e-97b3-b12f5c94e907` | (no START in window) |
| 2026-07-01T14:00:14Z | **FIRE** | `1c65f0db-5a68-429f-aacb-2396f0f6244b` | 2026-07-01T14:00:15Z `9d6a451d-...` |
| 2026-07-01T18:00:50Z | **FIRE** | `f1358e9f-1209-486a-b6aa-4b296548325f` | 2026-07-01T18:00:51Z `e56a4555-...` |
| 2026-08-01T14:00:14Z | **FIRE** | `ac4aaf56-9244-4832-818f-08446354c4d9` | 2026-08-01T14:00:15Z `9d6a6dfb-...` |
| 2026-09-01T14:00:14Z | **FIRE** | `79cb559a-3a3e-4b66-a55e-4c77db3d6ac4` | 2026-09-01T14:00:15Z `9d6a96da-...` |

**4 of 4 FIRE rows join to a START.** The two `ROLE-VALIDN` rows sit at the schedule's own
`CreationDate` **to the second** and join to nothing -- EventBridge Scheduler validating the role at
`CreateSchedule`. The amendment says "each is a rule-initiated fire"; 2 of 6 are not, filed as
`ETFS_GUARDRAIL-W3-S5`. **This does not weaken the re-cut** -- it makes its number right. How the
distinction surfaced is itself the control: at the 180 s join tolerance this battery first used, both
validation rows falsely joined to a **person's** invoke 99 s later (`7e5288cb-...` at 22:29:27Z); at 60 s
they join to nothing, and `AWS/Lambda Invocations` shows no invocation at that instant either.

**The orchestrator log group was read BY TIME, never by stream** (a warm stream's `lastEventTimestamp`
lags the invocation inside it -- W2's trap): 18 `START RequestId` records across 9 fully-followed pages,
**retention `NEVER-EXPIRE`** so the 90-day window is fully covered, and `AWS/Lambda Invocations` Sum = 18
over the same window -- two substrates, same denominator.

**The cron printed beside the history, so the two can disagree in the open:** 3 instants due, **3 of 3
FIRED**. One fire, **2026-07-01T18:00:50Z**, landed **off** a cron minute and is listed rather than
dropped. Cheapest hypothesis that fits: the live RetryPolicy (185 attempts / 86400 s) and
`LastModificationDate == CreationDate` (so the schedule was never edited) make a retry the likeliest
reading. **Measured, not diagnosed** -- and it is precisely the fire a cron-signature method would have
missed, which is why the issuer's re-cut is the harder instrument.

### 4.2 The August artifact, and which object was read

EG-s-14 has acted this round: an archive copy exists at
`platinum/reports/_archive/2026-08/20260909T230636Z/` (5 objects, 2026-09-09T23:11:30-39Z), listed in
full in the battery output. The issuer's amendment states the served objects were **not** rewritten by the
failed re-render, so **the live publish keys were read directly with `s3api head-object` and are the
objects the match table uses**:

```
  platinum/reports/2026-08/etf_ownership.html            LastModified=2026-09-01T17:38:41Z  62477
  platinum/reports/2026-08/etf_ownership.pdf             LastModified=2026-09-01T17:38:41Z  273857
  platinum/reports/2026-08/opaletfs_49financial_202608.csv  LastModified=2026-09-01T17:38:42Z  1952
  platinum/reports/2026-08/opaletfs_cottonwood_202608.csv   LastModified=2026-09-01T17:38:42Z  1828
  platinum/reports/2026-08/opaletfs_inflection_202608.csv   LastModified=2026-09-01T17:38:42Z  1828
```

The match, over **every** published month prefix in the bucket:

```
  2026-05  newest=2026-06-25T23:28:53Z  UNMATCHED; nearest fire 2026-07-01T14:00:14Z (-484281 s)
  2026-06  newest=2026-07-01T14:00:48Z  MATCHED to the rule-initiated fire at 2026-07-01T14:00:14Z (+34 s)
  2026-07  newest=2026-09-01T17:38:05Z  UNMATCHED; nearest fire 2026-09-01T14:00:14Z (+13071 s)
  2026-08  newest=2026-09-01T17:38:42Z  UNMATCHED; nearest fire 2026-09-01T14:00:14Z (+13108 s)
  matched 1 of 4 month prefix(es); the matcher is non-vacuous: YES
```

**2026-06 is the positive control** -- a published artifact 34 s after its fire, so "UNMATCHED" for
2026-08 is not a matcher that can only say no.

**What did happen on 2026-09-01, measured:** the fire at 14:00:14Z ran, and its own downstream
MANAGEMENT event carries the identity -- `SendCommand` at **14:01:06Z, username `etfs-reports-orchestrator`** --
dispatching `ETFS month-end render 2026-08` to `i-070477bf35fc54409`, **Status Success**. Then the served
objects were overwritten **3 h 38 m later**, and `ssm list-commands` over its ~30-day retention holds no
command at 17:38Z (only that 14:01:06Z Success and EG-s-14's `2026-09-09T23:15:09Z Failed`).
`org/critical_paths/change_management/20260901T1650Z_etfs-cottonwood-august-slice-backfill_completion.md`
(actor `4.0.0_SA_CRO`, ~16:4x-16:5xZ, i.e. **before** the write) states as a scope boundary: *"The served
monthly reports under `opal-data-etfs/platinum/reports/` were NOT re-rendered"* and *"the served reports
are now BEHIND the Desktop pack"* -- and closes with a table headed *"Numbers moved (previously published
-> complete data)"*. **What no instrument here can show:** `s3:PutObject` on `opal-data-etfs` is a data
event and neither trail selects that bucket, so there is no record of who wrote at 17:38Z. Offered as
evidence for S18-AC2, not as a verdict.

---

## 5. ARM (c) -- THE DAILY HISTORY, THREE INSTRUMENTS

**The issuer corrected this arm a second time** (2026-09-10 ~00:3xZ, on worker ~2's row
`ETFS_GUARDRAIL-W2-S10` -- the same finding this worker had measured independently and filed as
`ETFS_GUARDRAIL-W3-S3`, from two worktrees, within minutes). An EventBridge **rule** invokes a Lambda
through the function's **resource policy** (Principal `events.amazonaws.com` + SourceArn) and assumes no
role, so the `AssumeRole` rows at 10:30:24Z / 10:45:05Z are the functions' **execution** roles assumed on
a cold start *by whoever invoked*. They **corroborate a fire at the cron instant; they are not an
initiator signal.** Arm (c) as run therefore reads three instruments, in the order the correction names:

| instrument | what it is | cot | bd-49f | both (days x rules) |
|---|---|---|---|---|
| **PRIMARY** -- log GROUP by time, `START RequestId` at the cron instant, per day | a fire happened | 14 of 30 due | 14 of 30 due | **28 of 60 due; 28 of 28 REACHABLE** under 14-day retention |
| **CORROBORATION** -- execution-role cold-start `AssumeRole` at the same instants | a fire happened, reaching the whole window | 30 of 30 | 30 of 30 | **60 of 60** |
| **THIRD** -- `AWS/Events TriggeredRules`, `RuleName` dim | **rule-scoped by construction: the only initiator claim** | 30 datapoint-days, Sum 30 | 30 datapoint-days, Sum 30 | **60 of 60**, POPULATED |

`AWS/Lambda Invocations` (FunctionName dim) as the events denominator: **53** and **31**.
The corroboration reproduces worker `~2`'s cited numbers exactly (cot 30 of 30 at 10:30:24Z,
bd-49f 30 of 30 at 10:45:05Z). **The retention bound is stated rather than hidden:** both groups carry
`retentionInDays = 14`, so the PRIMARY instrument physically cannot reach 30 days and its denominator is
printed twice -- against the scheduled days due, and against what retention leaves reachable.

**Matched pairs: cot 18 of 30 fires, bd-49f 21 of 30**, every matched slice landing **+5 to +8 s** after
its fire instant. The unmatched fires, named, with the trading calendar resolved first (NEVER#4):

* **`bd-49f`** -- 2026-08-15 Sat, 08-16 Sun, 08-22 Sat, 08-23 Sun, 08-29 Sat, 08-30 Sun, 09-05 Sat,
  09-06 Sun, 09-07 Mon/**Labor Day**: **exactly** the non-trading days. The rule's own live Description
  says it runs "10:45Z daily incl weekends" and "Emits the newest available partition", so a weekend fire
  writing nothing is the design.
* **`cot`** -- 08-16 Sun, 08-17 Mon, 08-19 Wed, 08-21 Fri, 08-22 Sat, 08-23 Sun, 08-24 Mon, 08-30 Sun,
  08-31 Mon, 09-06 Sun, 09-07 Mon/Labor Day, 09-08 Tue: **five weekday entries**. The cot producer writes
  a slice dated ~2 days behind its fire, so the empty weekday fires of 08-17/08-19/08-21/08-24 line up
  with the CRO backfill entry's own missing-date list (2026-08-04, **08-18**, **08-20**, **08-21**,
  **08-31**), where the cause is recorded as **UNDIAGNOSED**. The lag is still open: the 2026-09-09 cot
  fire wrote `daily/cottonwood/2026-09-04.json` (5 days behind) while the 2026-09-09 bd-49f fire wrote
  `daily/49financial/2026-09-08.json` (1 day behind). Named, not chased -- EG-s-17 owns the producer.

## 6. ARM (d) -- THE NEGATIVE CONTROL, ON THE SAME PLANE

Both manual fires the amendment names by request id were exercised against the live plane:

```
  [2be062b2-6642-4092-852a-7dc4c0b714b5]  worker ~1's orchestrator invoke
      log GROUP /aws/lambda/etfs-reports-orchestrator read BY TIME, last 24 h:
      1 of 1 START record(s) carry this request id
         START 2026-09-09T23:14:47Z  RequestId: 2be062b2-6642-4092-852a-7dc4c0b714b5
      AssumeRole by etfs-reports-scheduler-role in THAT MINUTE (23:14:00Z -> 23:15:00Z): 0 of 0
      -> the SCHEDULER role is assumed by EventBridge Scheduler and by nothing else, so 0 IS
         the discriminator.

  [0840a0d3-15aa-4884-a12e-20e75cfa6136]  worker ~2's cot invoke
      1 of 8 START record(s) carry this request id
         START 2026-09-09T23:15:50Z  RequestId: 0840a0d3-15aa-4884-a12e-20e75cfa6136
      AssumeRole by cot-etf-ownership-daily-role in THAT MINUTE: 2 of 2
      -> the EXECUTION role is assumed on EVERY invocation, so the discriminator here is the
         MINUTE: is this a cron minute of cot-etf-ownership-daily-schedule ? -> False
```

A request id the client did not receive cannot appear as a START line, and it appears **exactly once**.

**The full non-rule populations, listed separately:** 14 of 18 orchestrator START records carry no
scheduler-role AssumeRole (including worker ~1's 23:14:47Z invoke); 8 cot and 2 bd-49f AssumeRole rows sit
off the cron minute -- among them the CRO's backfill at 2026-09-01T16:50:17Z and this round's work on
2026-09-05 and 2026-09-09. **Populations disjoint by requestID: True. Non-rule population non-empty:
True.**

**Mutant control.** The daily classification turns on `FIRE_TOL_S = 180`. Re-run over the same fetched
rows at tolerance 0, every RULE row collapses to 0 on both rules -- an AssumeRole lands seconds *after*
its cron minute, never on it. The monthly arm needs no tolerance at all and is the stronger control: the
scheduler role is assumed by EventBridge Scheduler and by nothing else, and arm (d) measured 0 such events
in a real manual invoke's minute.

---

## 7. WHAT THIS ORDER DID NOT DO

* **No invoke, no write, no deploy** -- 85 AWS calls, every one a read verb, every one rc=0.
* **Did not attribute the 2026-09-01T17:38:41-42Z August write.** It cannot be attributed from any
  instrument in reach (`s3:PutObject` on `opal-data-etfs` is a data event, unselected by both trails; no
  orchestrator invocation and no SSM command at that time). The fact, the offset, the bracketing entry and
  the instrument limit are all recorded. Manufacturing an attribution would have been the defect.
* **Did not diagnose the cot lag or its five empty weekday fires.** EG-s-17 owns the producer; the CRO's
  own entry records the cause as `UNDIAGNOSED`.
* **Did not diagnose the 2026-07-01T18:00:50Z off-cron scheduler fire.** Measured, with the RetryPolicy
  and `LastModificationDate == CreationDate` printed beside it as the cheapest fitting hypothesis.
* **Did not grade S18-AC2** -- `judgment="true"`, evidence only, the CVO grades at L9.
* **Did not fix `comp_trigger.py`** -- outside this order's `<paths>`. Its three invocations here all
  returned rc=0 WITHIN BUDGET; the CR-literal defect the issuer's nudge asks about was **not encountered**
  (the battery runs `org/modules/graph/comp_trigger.py` directly through `sys.executable` with
  `PYTHONIOENCODING=utf-8`, not through the `~/bin` forwarder).

## 8. ROWS FILED

| id | class / hazard | one line |
|---|---|---|
| `ETFS_GUARDRAIL-W3-S3` | OBSERVATION / INERT | The amendment names the daily roles "from `list-targets-by-rule` / `get-schedule`"; both daily targets return **RoleArn ABSENT** and neither is a Scheduler schedule. Measured independently here and, within minutes, by worker ~2 as `W2-S10`; the issuer's correction on that row is adopted in the battery (the execution role corroborates, it does not attribute). |
| `ETFS_GUARDRAIL-W3-S4` | OBSERVATION / INERT | `comp-trigger` prints `schedule: -` and no fired-evidence for the Scheduler schedule while the live API returns its cron -- both EventBridge rules are fully right in the same run. |
| `ETFS_GUARDRAIL-W3-S5` | OBSERVATION / INERT | The amendment says *each* `AssumeRole` on the scheduler role is a fire; 2 of 6 are `CreateSchedule`-time role validations at the schedule's own CreationDate and join to no START. `fires 4`, not 6. |

## 9. THE BATTERY OUTPUT, VERBATIM

`timeout 600 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~3/test_egs18_schedules_from_history.py`
-> **rc=0**

```text
EG-s-18 BATTERY -- THE SCHEDULES' FIRING FROM HISTORY
face: AMENDED by the issuer 2026-09-09 ~23:5xZ (CLOUD @5507841f04) on rows
      ETFS_GUARDRAIL-W1-S13 and ETFS_GUARDRAIL-W2-S7; arms (b)/(c) re-cut onto
      the AssumeRole MANAGEMENT plane. This battery implements the AMENDED arms.
run_at_utc: 2026-09-10T00:43:19Z
WINDOW-90D (start-time INCLUSIVE at the second; both ends printed): 2026-06-12T00:43:19Z -> 2026-09-10T00:43:19Z
WINDOW-30D (start-time INCLUSIVE at the second; both ends printed): 2026-08-11T00:43:19Z -> 2026-09-10T00:43:19Z
shim: C:\tmp\wk-etfs-2-3\.tools\aws.cmd   plane: READ-ONLY (no invoke, no write, no deploy)

==============================================================================
ARM (a) -- THE CONFIGURATION READ OF EACH SCHEDULE, LIVE
==============================================================================
[a.1] KIND: EventBridge SCHEDULER schedule (aws scheduler get-schedule)
      aws scheduler get-schedule --name etfs-reports-monthly-run
      rc=0  Name=etfs-reports-monthly-run  State=ENABLED
            ScheduleExpression=cron(0 10 1 * ? *)  Timezone=America/New_York  Group=default
            Target.Arn=arn:aws:lambda:us-east-1:313476888478:function:etfs-reports-orchestrator
            Target.Input={"mode":"run"}
            Target.RoleArn=arn:aws:iam::313476888478:role/etfs-reports-scheduler-role   <- the role arm (b) reads from history
            Target.RetryPolicy={"MaximumEventAgeInSeconds": 86400, "MaximumRetryAttempts": 185}
            FlexibleTimeWindow={"Mode": "OFF"}
            CreationDate=2026-06-25T22:27:48Z  LastModificationDate=2026-06-25T22:27:48Z
            (CreationDate is carried into arm (b): an AssumeRole at that exact
             instant is Scheduler VALIDATING the role at CreateSchedule, not a fire)

[a.2] KIND: EventBridge RULE on the default bus (aws events describe-rule) -- NOT a Scheduler schedule
      aws events describe-rule --name cot-etf-ownership-daily-schedule
      rc=0  Name=cot-etf-ownership-daily-schedule  State=ENABLED  ScheduleExpression=cron(30 10 * * ? *)  EventBusName=default
            Description=Daily -> compute the Cottonwood ETF-ownership slice from the latest cot canonical/holdings -> opal-data-etfs/daily/cottonwood/
      aws events list-targets-by-rule --rule cot-etf-ownership-daily-schedule
      rc=0  1 target(s)
            Id=CotEtfOwnershipDailyLambda  Arn=arn:aws:lambda:us-east-1:313476888478:function:cot-etf-ownership-daily
            Input=(none -- the rule sends the EventBridge scheduled-event envelope)
            RoleArn=(ABSENT)
      NOTE, MEASURED, NOT ASSUMED: an EventBridge RULE targeting Lambda
      carries NO RoleArn on its target -- it invokes through the function's
      resource-based policy. The amendment says 'the two daily rules' roles,
      named from list-targets-by-rule / get-schedule'; list-targets-by-rule
      has no such field here, so the role arm (c) reads from history is the
      FUNCTION'S EXECUTION ROLE, read from get-function-configuration.
      Filed as ETFS_GUARDRAIL-W3-S3.
      aws lambda get-function-configuration --function-name cot-etf-ownership-daily --query Role
      rc=0  -> arn:aws:iam::313476888478:role/cot-etf-ownership-daily-role

[a.3] KIND: EventBridge RULE on the default bus (aws events describe-rule) -- NOT a Scheduler schedule
      aws events describe-rule --name bd-49f-etf-ownership-scheduled-floor
      rc=0  Name=bd-49f-etf-ownership-scheduled-floor  State=ENABLED  ScheduleExpression=cron(45 10 * * ? *)  EventBusName=default
            Description=Scheduled floor for the 49F ETF-ownership rebate-basis producer (Andrew-direct 2026-07-29 revival; NEVER#4). 10:45Z daily incl weekends -- 2
      aws events list-targets-by-rule --rule bd-49f-etf-ownership-scheduled-floor
      rc=0  1 target(s)
            Id=Bd49fEtfOwnershipScheduledFloor  Arn=arn:aws:lambda:us-east-1:313476888478:function:bd-49f-etf-ownership-daily
            Input=(none -- the rule sends the EventBridge scheduled-event envelope)
            RoleArn=(ABSENT)
      NOTE, MEASURED, NOT ASSUMED: an EventBridge RULE targeting Lambda
      carries NO RoleArn on its target -- it invokes through the function's
      resource-based policy. The amendment says 'the two daily rules' roles,
      named from list-targets-by-rule / get-schedule'; list-targets-by-rule
      has no such field here, so the role arm (c) reads from history is the
      FUNCTION'S EXECUTION ROLE, read from get-function-configuration.
      Filed as ETFS_GUARDRAIL-W3-S3.
      aws lambda get-function-configuration --function-name bd-49f-etf-ownership-daily --query Role
      rc=0  -> arn:aws:iam::313476888478:role/bd-49f-etf-ownership-daily-role

ARM (a): 3 of 3 schedules read LIVE, all ENABLED and targeting the named function

==============================================================================
COVERAGE-ABSENT -- the CloudTrail `Invoke` read, re-cut (amendment limb iii)
==============================================================================
The pre-amendment arms read CloudTrail `Invoke` events for the initiator column.
That read is executed and reported here, and it is NEVER a pass and NEVER a fail:
   trail=opal-organization-trail          data-resource types = AWS::S3::Object
   trail=opal-served-key-write-trail      data-resource types = AWS::S3::Object
   lookup-events EventName=Invoke over 2026-06-12T00:43:19Z -> 2026-09-10T00:43:19Z : 0 event(s), 1 page(s)
   COVERAGE-ABSENT: 0 of 2 trails select AWS::Lambda::Function
   A THIRD READ, on this worker's own instrument, corroborating the issuer's
   amendment and the rows it rests on (ETFS_GUARDRAIL-W1-S13, W2-S7). No new row
   is minted for it: post-amendment the face ASKS for this line, so it is no
   longer a spec-vs-world mismatch.

==============================================================================
ARM (b) -- THE MONTHLY HISTORY (90 days), FROM THE AssumeRole PLANE
==============================================================================
[b.1] `etfs-reports-scheduler-role`'s AssumeRole MANAGEMENT events, lookup-events
      fully paginated, counted client-side. The lookup key is the ROLE ARN, not
      the bare role name: an AssumeRole event's AWS::IAM::Role resource carries
      the ARN form, and the bare name returns only IAM lifecycle events.
      aws cloudtrail lookup-events --lookup-attributes AttributeKey=ResourceName,AttributeValue=arn:aws:iam::313476888478:role/etfs-reports-scheduler-role
      -> 7 event(s) across 1 page(s); 6 are AssumeRole; 6 after dedupe by
         requestID (CloudTrail emits the assumption TWICE per fire, one requestID)
      DENOMINATOR: 6 of 7 events returned for this role are AssumeRole.
      NEGATIVE CONTROL ON THE LOOKUP KEY, so the ARN form is not taken on faith:
      the BARE name returns 2 event(s) (CreateRole, PutRolePolicy) -- 0 AssumeRole among them.

[b.2] The orchestrator log GROUP read BY TIME (never one stream picked by its
      first/last event timestamp -- a warm stream's lastEventTimestamp lags the
      invocation inside it, W2's trap).
      aws logs filter-log-events --log-group-name /aws/lambda/etfs-reports-orchestrator --start-time <ms> --end-time <ms>
      -> 18 START RequestId record(s) across 9 fully-followed page(s)
      LOG-GROUP RETENTION: NEVER-EXPIRE (NEVER-EXPIRE = the 90d window is fully covered)
      CROSS-SUBSTRATE CHECK: AWS/Lambda Invocations Sum = 18 over the same window

[b.3] THE JOIN -- each AssumeRole by the scheduler role IS a rule-initiated fire;
      the START it produced is the one within 60s after it.
      AssumeRole (UTC)       class          requestID                              orchestrator START (join tol 60s)
      2026-06-25T22:27:48Z   ROLE-VALIDN    9552122c-5856-4923-81a9-fdf63b6fd5eb   (no START in window)
      2026-06-25T22:27:48Z   ROLE-VALIDN    c5899520-1917-4b3e-97b3-b12f5c94e907   (no START in window)
      2026-07-01T14:00:14Z   FIRE           1c65f0db-5a68-429f-aacb-2396f0f6244b   2026-07-01T14:00:15Z 9d6a451d-6009-4da0-ba13-8875d1985316
      2026-07-01T18:00:50Z   FIRE           f1358e9f-1209-486a-b6aa-4b296548325f   2026-07-01T18:00:51Z e56a4555-a05a-481a-bc9b-08cd0533e235
      2026-08-01T14:00:14Z   FIRE           ac4aaf56-9244-4832-818f-08446354c4d9   2026-08-01T14:00:15Z 9d6a6dfb-e009-4da0-ba13-8875d1985316
      2026-09-01T14:00:14Z   FIRE           79cb559a-3a3e-4b66-a55e-4c77db3d6ac4   2026-09-01T14:00:15Z 9d6a96da-6009-4da0-ba13-8875d1985316
      6 AssumeRole row(s): 4 FIRE, 2 ROLE-VALIDN at the schedule's own
      CreationDate 2026-06-25T22:27:48Z (a CreateSchedule-time role check, never an execution --
      it is separated here rather than counted as a fire, and its 2 row(s) join
      to no START inside 60s). The amendment says 'each is a rule-initiated
      fire'; 2 of 6 are not. Filed as ETFS_GUARDRAIL-W3-S5.
      4 of 4 FIRE rows join to a START record.

      THE CRON, printed beside the history so the two can disagree in the open:
      cron(0 10 1 * ? *) (America/New_York) is due at 3 instant(s) in the window:
         2026-07-01T14:00:00Z  FIRED (AssumeRole 2026-07-01T14:00:14Z)
         2026-08-01T14:00:00Z  FIRED (AssumeRole 2026-08-01T14:00:14Z)
         2026-09-01T14:00:00Z  FIRED (AssumeRole 2026-09-01T14:00:14Z)
      3 of 3 scheduled instants due produced a fire.
      1 rule-initiated row(s) landed OFF a cron minute -- listed, never dropped:
         2026-07-01T18:00:50Z  session=ee4c1614beef325388e2b9ca469d3a00  START=2026-07-01T18:00:51Z

[b.4] THE AUGUST ARTIFACT, MATCHED BY TIME.
      WHICH OBJECT WAS READ, STATED: EG-s-14 has already acted this round -- an
      archive copy exists under platinum/reports/_archive/2026-08/. The issuer's
      amendment states the served objects were NOT rewritten by the failed
      re-render, so the LIVE PUBLISH KEYS are read DIRECTLY with head-object and
      are the objects the match table uses. The archive is listed beside them so
      a later re-publish cannot be mistaken for what was matched here.
      LISTED -- ARCHIVE (platinum/reports/_archive/2026-08/), 10 object(s):
         platinum/reports/_archive/2026-08/20260909T230636Z/etf_ownership.html  LastModified=2026-09-09T23:11:30Z  Size=62477
         platinum/reports/_archive/2026-08/20260909T230636Z/etf_ownership.pdf  LastModified=2026-09-09T23:11:32Z  Size=273857
         platinum/reports/_archive/2026-08/20260909T230636Z/opaletfs_49financial_202608.csv  LastModified=2026-09-09T23:11:35Z  Size=1952
         platinum/reports/_archive/2026-08/20260909T230636Z/opaletfs_cottonwood_202608.csv  LastModified=2026-09-09T23:11:37Z  Size=1828
         platinum/reports/_archive/2026-08/20260909T230636Z/opaletfs_inflection_202608.csv  LastModified=2026-09-09T23:11:39Z  Size=1828
         platinum/reports/_archive/2026-08/20260910T002002Z/etf_ownership.html  LastModified=2026-09-10T00:20:11Z  Size=62477
         platinum/reports/_archive/2026-08/20260910T002002Z/etf_ownership.pdf  LastModified=2026-09-10T00:20:16Z  Size=273857
         platinum/reports/_archive/2026-08/20260910T002002Z/opaletfs_49financial_202608.csv  LastModified=2026-09-10T00:20:22Z  Size=1952
         platinum/reports/_archive/2026-08/20260910T002002Z/opaletfs_cottonwood_202608.csv  LastModified=2026-09-10T00:20:27Z  Size=1828
         platinum/reports/_archive/2026-08/20260910T002002Z/opaletfs_inflection_202608.csv  LastModified=2026-09-10T00:20:33Z  Size=1828
      MATCHED -- LIVE PUBLISH KEYS (platinum/reports/2026-08/), 6 object(s), s3api head-object per key:
         platinum/reports/2026-08/coverage_verdict.json  LastModified=2026-09-10T00:24:44Z  ContentLength=1225
         platinum/reports/2026-08/etf_ownership.html  LastModified=2026-09-10T00:24:47Z  ContentLength=43376
         platinum/reports/2026-08/etf_ownership.pdf  LastModified=2026-09-10T00:24:48Z  ContentLength=252393
         platinum/reports/2026-08/opaletfs_49financial_202608.csv  LastModified=2026-09-10T00:24:48Z  ContentLength=2012
         platinum/reports/2026-08/opaletfs_cottonwood_202608.csv  LastModified=2026-09-10T00:24:50Z  ContentLength=1888
         platinum/reports/2026-08/opaletfs_inflection_202608.csv  LastModified=2026-09-10T00:24:49Z  ContentLength=1888

      The orchestrator's own SSM dispatch -- the fire's downstream MANAGEMENT
      event, which does carry an identity:
      lookup-events EventName=SendCommand 2026-09-01T13:55:14Z -> 2026-09-01T14:20:14Z : 1 event(s), 1 page(s)
         2026-09-01T14:01:06Z  SendCommand  username=etfs-reports-orchestrator
      ssm list-commands (Run Command history, ~30d retention):
         2026-09-10T00:23:26Z  Success  AWS-RunShellScript     ETFS month-end render 2026-08
         2026-09-09T23:15:09Z  Failed   AWS-RunShellScript     ETFS month-end render 2026-08
         2026-09-01T14:01:06Z  Success  AWS-RunShellScript     ETFS month-end render 2026-08

      EVERY published monthly artifact vs the rule-initiated fires
      (denominator = 4 published month prefix(es)):
         2026-05  newest=2026-06-25T23:28:53Z  UNMATCHED to any rule-initiated fire; nearest fire 2026-07-01T14:00:14Z (-484281 s)
         2026-06  newest=2026-07-01T14:00:48Z  MATCHED to the rule-initiated fire at 2026-07-01T14:00:14Z (+34s)
         2026-07  newest=2026-09-01T17:38:05Z  UNMATCHED to any rule-initiated fire; nearest fire 2026-09-01T14:00:14Z (+13071 s)
         2026-08  newest=2026-09-10T00:24:50Z  UNMATCHED to any rule-initiated fire; nearest fire 2026-09-01T14:00:14Z (+728676 s)
      matched 1 of 4 month prefix(es); the matcher is non-vacuous: YES

==============================================================================
ARM (c) -- THE DAILY HISTORY (30 days), THREE INSTRUMENTS
==============================================================================
RE-CUT AGAIN by the issuer 2026-09-10 ~00:3xZ on worker ~2's row
ETFS_GUARDRAIL-W2-S10, which this worker measured independently and filed as ETFS_GUARDRAIL-W3-S3:
0 of 2 daily-rule targets carry a RoleArn -- an EventBridge RULE invokes a Lambda
through the function's RESOURCE POLICY (Principal events.amazonaws.com +
SourceArn), assuming no role. The AssumeRole rows at the cron instants are the
FUNCTIONS' EXECUTION roles, assumed on a cold start by WHOEVER invoked, so they
CORROBORATE a fire at the cron instant and are NOT an initiator signal. So:
  PRIMARY       the producer's log GROUP read BY TIME, START RequestId lines at
                the rule's cron instant, counted PER DAY, denominator printed
  CORROBORATION the execution role's cold-start AssumeRole at the same instants
  THIRD         AWS/Events TriggeredRules (RuleName dim) per rule over 30 days

[c] cot-etf-ownership-daily-schedule -> cot-etf-ownership-daily   cron(30 10 * * ? *) (UTC; an EventBridge rule has no timezone field)
    SCHEDULED INSTANTS DUE in the 30d window: 30, on 30 distinct day(s).
    [c.1] PRIMARY -- aws logs filter-log-events --log-group-name /aws/lambda/cot-etf-ownership-daily
          --start-time <ms> --end-time <ms>  (the GROUP by time, never one
          stream picked by its first/last event timestamp -- W2's trap)
          -> 37 START record(s) across 16 fully-followed page(s)
          LOG-GROUP RETENTION = 14 day(s).
          START lines AT THE CRON INSTANT: 14 row(s) on 14 distinct day(s)
          DENOMINATOR: 14 of 30 scheduled day(s) in the window carry one.
          RETENTION-BOUNDED DENOMINATOR: the group holds 14 day(s), so the
          REACHABLE denominator is 14 of 30 -- 14 of 14 reached.
            2026-08-27T10:30:28Z  Thu  0ffb6689-0761-46ea-99a0-231b0005f82c
            2026-08-28T10:30:28Z  Fri  c03db66e-ebae-4a57-a183-1fc3058db9e7
            2026-08-29T10:30:27Z  Sat  48eea386-1ade-4cae-8364-fc5759b6775a
            2026-08-30T10:30:28Z  Sun  14f680c5-3e25-4e96-85ee-ebbb73662b98
            2026-08-31T10:30:28Z  Mon  fe264bdd-8c13-45da-b684-ac567f25aa64
            2026-09-01T10:30:29Z  Tue  a5db1d72-d7db-439a-b11f-2469398d2a3a
            2026-09-02T10:30:28Z  Wed  c79fd4fa-079b-4ca0-b891-4b1ef932277a
            2026-09-03T10:30:28Z  Thu  8f0a6aa6-48c1-4bee-957d-bf3c16102667
            2026-09-04T10:30:28Z  Fri  c4d9a7c7-98a1-4549-8bc5-c0874d3e94eb
            2026-09-05T10:30:28Z  Sat  23a1a905-63bd-4b60-9e28-08ffb76cb4b0
            2026-09-06T10:30:27Z  Sun  1d5f9922-d2f1-4900-98c0-2c735b8b16b1
            2026-09-07T10:30:27Z  Mon/HOL  68199d78-4248-422e-9ad0-3e97367551e9
            2026-09-08T10:30:27Z  Tue  43c20c32-953a-489d-bbf0-c7883055ae31
            2026-09-09T10:30:28Z  Wed  1b463933-0b3d-4425-b4f7-bd276e795ca5
    [c.2] CORROBORATION (not an initiator signal) -- the EXECUTION role
          arn:aws:iam::313476888478:role/cot-etf-ownership-daily-role, cold-start AssumeRole:
          lookup-events ResourceName=<that ARN>, fully paginated
          -> 75 event(s), 2 page(s); 75 AssumeRole; 38 after dedupe by requestID
          AT THE CRON INSTANT: 30 row(s) on 30 distinct day(s) of 30 due.
          CITED BESIDE THIS RUN'S NUMBER: W2 measured 30 of 30 days at 10:30:24Z.
          This is the instrument that reaches the WHOLE window: the log group
          cannot, at 14-day retention.
    [c.3] THIRD INSTRUMENT -- AWS/Events TriggeredRules, RuleName=cot-etf-ownership-daily-schedule,
          period 86400 over the 30d window:
          POPULATED: 30 datapoint-day(s), Sum = 30. DENOMINATOR: 30 of 30
          scheduled day(s) carry a datapoint. This IS rule-scoped -- the
          RuleName dimension counts only rule-initiated triggers -- so it is
          the one instrument of the three that carries an initiator claim.
          AWS/Lambda Invocations (FunctionName dim), the events denominator: 53
    [c.4] THE SLICES THOSE FIRES PRODUCED. Served slices under
          s3://opal-data-etfs/daily/cottonwood/ written in the window: 23
          The fire instants used here are the 30 cron-instant day(s) the
          CORROBORATION instrument reaches (the log group reaches only 14).

    fire instant (UTC)     day     requestID (AssumeRole)                 slice written within 900s
    2026-08-11T10:30:24Z   Tue     94d102fc-5b00-4999-9ec1-04b21f2985c1   daily/cottonwood/2026-08-07.json @ 2026-08-11T10:30:30Z (+6s)
    2026-08-12T10:30:24Z   Wed     6fb7d4a2-9ee4-4323-bf4f-3580016d7d2f   daily/cottonwood/2026-08-10.json @ 2026-08-12T10:30:32Z (+8s)
    2026-08-13T10:30:24Z   Thu     aa184a19-bc80-4c4f-af45-3f3adf6408db   daily/cottonwood/2026-08-11.json @ 2026-08-13T10:30:30Z (+6s)
    2026-08-14T10:30:24Z   Fri     ce391b3a-9dc5-4daa-9877-225e3521ac8c   daily/cottonwood/2026-08-12.json @ 2026-08-14T10:30:30Z (+6s)
    2026-08-15T10:30:24Z   Sat     22f6a44f-3688-4192-9293-c3e40dcd48bb   daily/cottonwood/2026-08-13.json @ 2026-08-15T10:30:30Z (+6s)
    2026-08-16T10:30:24Z   Sun     77c0c012-b97e-4051-83e7-e466d65516a4   (none)
    2026-08-17T10:30:24Z   Mon     7f39fd6b-6c59-43ac-8dbe-7a539bdb7043   (none)
    2026-08-18T10:30:24Z   Tue     2ebddd5d-171f-43b2-a716-fdf31a5971c4   daily/cottonwood/2026-08-14.json @ 2026-08-18T10:30:30Z (+6s)
    2026-08-19T10:30:24Z   Wed     6ac928e1-7a37-4a65-bb7c-db7ece20f9f3   (none)
    2026-08-20T10:30:24Z   Thu     c59716aa-04a6-478c-b051-d0564c98ffda   daily/cottonwood/2026-08-17.json @ 2026-08-20T10:30:30Z (+6s)
    2026-08-21T10:30:24Z   Fri     d0aa4266-a6ff-41f4-a4a6-fab16da3be01   (none)
    2026-08-22T10:30:24Z   Sat     2a4aa9a9-de97-4d3f-be3c-85a7400c67d5   (none)
    2026-08-23T10:30:24Z   Sun     d0eb5e9a-62c0-474f-9dcb-285651426cf0   (none)
    2026-08-24T10:30:24Z   Mon     5e2d7818-1d72-4c15-8ea9-c7e6f2ca468b   (none)
    2026-08-25T10:30:24Z   Tue     b416f115-3c93-4d27-91ab-8d0073eee5a5   daily/cottonwood/2026-08-19.json @ 2026-08-25T10:30:30Z (+6s)
    2026-08-26T10:30:24Z   Wed     20f09f8f-030a-4a31-9dae-59426715c0a5   daily/cottonwood/2026-08-24.json @ 2026-08-26T10:30:30Z (+6s)
    2026-08-27T10:30:24Z   Thu     0ffb6689-0761-46ea-99a0-231b0005f82c   daily/cottonwood/2026-08-25.json @ 2026-08-27T10:30:30Z (+6s)
    2026-08-28T10:30:24Z   Fri     c03db66e-ebae-4a57-a183-1fc3058db9e7   daily/cottonwood/2026-08-26.json @ 2026-08-28T10:30:30Z (+6s)
    2026-08-29T10:30:24Z   Sat     48eea386-1ade-4cae-8364-fc5759b6775a   daily/cottonwood/2026-08-27.json @ 2026-08-29T10:30:29Z (+5s)
    2026-08-30T10:30:24Z   Sun     14f680c5-3e25-4e96-85ee-ebbb73662b98   (none)
    2026-08-31T10:30:24Z   Mon     fe264bdd-8c13-45da-b684-ac567f25aa64   (none)
    2026-09-01T10:30:24Z   Tue     a5db1d72-d7db-439a-b11f-2469398d2a3a   daily/cottonwood/2026-08-28.json @ 2026-09-01T10:30:31Z (+7s)
    2026-09-02T10:30:24Z   Wed     c79fd4fa-079b-4ca0-b891-4b1ef932277a   daily/cottonwood/2026-08-31.json @ 2026-09-02T10:30:30Z (+6s)
    2026-09-03T10:30:24Z   Thu     8f0a6aa6-48c1-4bee-957d-bf3c16102667   daily/cottonwood/2026-09-01.json @ 2026-09-03T10:30:30Z (+6s)
    2026-09-04T10:30:24Z   Fri     c4d9a7c7-98a1-4549-8bc5-c0874d3e94eb   daily/cottonwood/2026-09-02.json @ 2026-09-04T10:30:30Z (+6s)
    2026-09-05T10:30:24Z   Sat     23a1a905-63bd-4b60-9e28-08ffb76cb4b0   daily/cottonwood/2026-09-03.json @ 2026-09-05T10:30:30Z (+6s)
    2026-09-06T10:30:24Z   Sun     1d5f9922-d2f1-4900-98c0-2c735b8b16b1   (none)
    2026-09-07T10:30:24Z   Mon/HOL 68199d78-4248-422e-9ad0-3e97367551e9   (none)
    2026-09-08T10:30:24Z   Tue     43c20c32-953a-489d-bbf0-c7883055ae31   (none)
    2026-09-09T10:30:24Z   Wed     1b463933-0b3d-4425-b4f7-bd276e795ca5   daily/cottonwood/2026-09-04.json @ 2026-09-09T10:30:30Z (+6s)
    matched pairs 18 of 30 fires (denominator = fires at the cron instant)
    FIRES THAT WROTE NO SLICE (named, never verdicted -- NEVER#4: resolve
    the trading calendar before calling any of these a stale pipeline):
       2026-08-16T10:30:24Z  Sun
       2026-08-17T10:30:24Z  Mon
       2026-08-19T10:30:24Z  Wed
       2026-08-21T10:30:24Z  Fri
       2026-08-22T10:30:24Z  Sat
       2026-08-23T10:30:24Z  Sun
       2026-08-24T10:30:24Z  Mon
       2026-08-30T10:30:24Z  Sun
       2026-08-31T10:30:24Z  Mon
       2026-09-06T10:30:24Z  Sun
       2026-09-07T10:30:24Z  Mon/HOL
       2026-09-08T10:30:24Z  Tue

[c] bd-49f-etf-ownership-scheduled-floor -> bd-49f-etf-ownership-daily   cron(45 10 * * ? *) (UTC; an EventBridge rule has no timezone field)
    SCHEDULED INSTANTS DUE in the 30d window: 30, on 30 distinct day(s).
    [c.1] PRIMARY -- aws logs filter-log-events --log-group-name /aws/lambda/bd-49f-etf-ownership-daily
          --start-time <ms> --end-time <ms>  (the GROUP by time, never one
          stream picked by its first/last event timestamp -- W2's trap)
          -> 15 START record(s) across 15 fully-followed page(s)
          LOG-GROUP RETENTION = 14 day(s).
          START lines AT THE CRON INSTANT: 14 row(s) on 14 distinct day(s)
          DENOMINATOR: 14 of 30 scheduled day(s) in the window carry one.
          RETENTION-BOUNDED DENOMINATOR: the group holds 14 day(s), so the
          REACHABLE denominator is 14 of 30 -- 14 of 14 reached.
            2026-08-27T10:45:09Z  Thu  c2d7ecc3-e2bb-4e84-878a-f18e8ad98915
            2026-08-28T10:45:09Z  Fri  71326197-8a27-4237-9073-8f53d74153ff
            2026-08-29T10:45:08Z  Sat  d5e174f6-df0e-49c2-957d-b28723d239dc
            2026-08-30T10:45:08Z  Sun  336918f7-bf86-4721-a1c9-f174343854d0
            2026-08-31T10:45:09Z  Mon  3567d264-a0d2-4086-b40d-6138a82c7467
            2026-09-01T10:45:09Z  Tue  a2a9858f-c64e-4599-b026-91493f416e80
            2026-09-02T10:45:08Z  Wed  c21c3632-e803-4714-aa75-70d1862b2259
            2026-09-03T10:45:09Z  Thu  4149ae6d-9e58-46b3-afb7-95f9b399bfcc
            2026-09-04T10:45:09Z  Fri  dfff0544-6769-475f-bf8b-d74948b22f95
            2026-09-05T10:45:09Z  Sat  8f438e28-e27c-4019-b881-fb8af4dda4aa
            2026-09-06T10:45:08Z  Sun  f18f410c-ed21-42cc-b820-0af38e6f892d
            2026-09-07T10:45:09Z  Mon/HOL  c2295db2-9c9e-45a6-9163-9ba85eadd6cd
            2026-09-08T10:45:09Z  Tue  718a7d96-6a51-4083-a6fa-8d580b86b449
            2026-09-09T10:45:09Z  Wed  643ff10d-5ddb-44bb-9317-1200b48f480d
    [c.2] CORROBORATION (not an initiator signal) -- the EXECUTION role
          arn:aws:iam::313476888478:role/bd-49f-etf-ownership-daily-role, cold-start AssumeRole:
          lookup-events ResourceName=<that ARN>, fully paginated
          -> 63 event(s), 2 page(s); 63 AssumeRole; 32 after dedupe by requestID
          AT THE CRON INSTANT: 30 row(s) on 30 distinct day(s) of 30 due.
          CITED BESIDE THIS RUN'S NUMBER: W2 measured 30 of 30 days at 10:45:05Z.
          This is the instrument that reaches the WHOLE window: the log group
          cannot, at 14-day retention.
    [c.3] THIRD INSTRUMENT -- AWS/Events TriggeredRules, RuleName=bd-49f-etf-ownership-scheduled-floor,
          period 86400 over the 30d window:
          POPULATED: 30 datapoint-day(s), Sum = 30. DENOMINATOR: 30 of 30
          scheduled day(s) carry a datapoint. This IS rule-scoped -- the
          RuleName dimension counts only rule-initiated triggers -- so it is
          the one instrument of the three that carries an initiator claim.
          AWS/Lambda Invocations (FunctionName dim), the events denominator: 31
    [c.4] THE SLICES THOSE FIRES PRODUCED. Served slices under
          s3://opal-data-etfs/daily/49financial/ written in the window: 21
          The fire instants used here are the 30 cron-instant day(s) the
          CORROBORATION instrument reaches (the log group reaches only 14).

    fire instant (UTC)     day     requestID (AssumeRole)                 slice written within 900s
    2026-08-11T10:45:05Z   Tue     ecd44786-bd92-423f-8b2e-3de6dff04e05   daily/49financial/2026-08-10.json @ 2026-08-11T10:45:12Z (+7s)
    2026-08-12T10:45:05Z   Wed     899e30f7-5cd0-441a-8640-dd6bfd8ef6f5   daily/49financial/2026-08-11.json @ 2026-08-12T10:45:12Z (+7s)
    2026-08-13T10:45:05Z   Thu     b22c0646-a6d0-4ba6-b018-77be2e05654a   daily/49financial/2026-08-12.json @ 2026-08-13T10:45:12Z (+7s)
    2026-08-14T10:45:05Z   Fri     da90e272-cdd3-407e-9a8c-db7508f0cdb3   daily/49financial/2026-08-13.json @ 2026-08-14T10:45:12Z (+7s)
    2026-08-15T10:45:05Z   Sat     7e41fdca-244d-439f-96a8-6ed241e7d1db   (none)
    2026-08-16T10:45:05Z   Sun     e0cc885f-37cf-4e38-9ded-8f6bfe40a387   (none)
    2026-08-17T10:45:05Z   Mon     c0d8be5b-b952-4ef3-acb4-f767c5aa0251   daily/49financial/2026-08-14.json @ 2026-08-17T10:45:12Z (+7s)
    2026-08-18T10:45:05Z   Tue     57b7385e-7299-46ed-96d1-86114693bbc7   daily/49financial/2026-08-17.json @ 2026-08-18T10:45:12Z (+7s)
    2026-08-19T10:45:05Z   Wed     a84cab18-79fd-43bc-a376-68ae234f7d25   daily/49financial/2026-08-18.json @ 2026-08-19T10:45:11Z (+6s)
    2026-08-20T10:45:05Z   Thu     a021c975-f831-4345-adb5-0c8640e49da2   daily/49financial/2026-08-19.json @ 2026-08-20T10:45:11Z (+6s)
    2026-08-21T10:45:05Z   Fri     6210a05e-d5f0-4778-ab29-ed55b8438d89   daily/49financial/2026-08-20.json @ 2026-08-21T10:45:12Z (+7s)
    2026-08-22T10:45:05Z   Sat     3f8b175f-20b7-4ccc-b81f-7bea631aa150   (none)
    2026-08-23T10:45:05Z   Sun     42e38f6c-dccd-451b-a6b2-65677b619e8a   (none)
    2026-08-24T10:45:05Z   Mon     bdc4ca5e-efd1-421b-b18c-734f7a9bbfab   daily/49financial/2026-08-21.json @ 2026-08-24T10:45:11Z (+6s)
    2026-08-25T10:45:05Z   Tue     beb86b43-9842-4a93-9e6e-203c12317f74   daily/49financial/2026-08-24.json @ 2026-08-25T10:45:12Z (+7s)
    2026-08-26T10:45:05Z   Wed     842cc510-dace-457d-b699-fbb15602a872   daily/49financial/2026-08-25.json @ 2026-08-26T10:45:12Z (+7s)
    2026-08-27T10:45:05Z   Thu     c2d7ecc3-e2bb-4e84-878a-f18e8ad98915   daily/49financial/2026-08-26.json @ 2026-08-27T10:45:12Z (+7s)
    2026-08-28T10:45:05Z   Fri     71326197-8a27-4237-9073-8f53d74153ff   daily/49financial/2026-08-27.json @ 2026-08-28T10:45:12Z (+7s)
    2026-08-29T10:45:05Z   Sat     d5e174f6-df0e-49c2-957d-b28723d239dc   (none)
    2026-08-30T10:45:05Z   Sun     336918f7-bf86-4721-a1c9-f174343854d0   (none)
    2026-08-31T10:45:05Z   Mon     3567d264-a0d2-4086-b40d-6138a82c7467   daily/49financial/2026-08-28.json @ 2026-08-31T10:45:12Z (+7s)
    2026-09-01T10:45:05Z   Tue     a2a9858f-c64e-4599-b026-91493f416e80   daily/49financial/2026-08-31.json @ 2026-09-01T10:45:12Z (+7s)
    2026-09-02T10:45:05Z   Wed     c21c3632-e803-4714-aa75-70d1862b2259   daily/49financial/2026-09-01.json @ 2026-09-02T10:45:12Z (+7s)
    2026-09-03T10:45:05Z   Thu     4149ae6d-9e58-46b3-afb7-95f9b399bfcc   daily/49financial/2026-09-02.json @ 2026-09-03T10:45:12Z (+7s)
    2026-09-04T10:45:05Z   Fri     dfff0544-6769-475f-bf8b-d74948b22f95   daily/49financial/2026-09-03.json @ 2026-09-04T10:45:12Z (+7s)
    2026-09-05T10:45:05Z   Sat     8f438e28-e27c-4019-b881-fb8af4dda4aa   (none)
    2026-09-06T10:45:05Z   Sun     f18f410c-ed21-42cc-b820-0af38e6f892d   (none)
    2026-09-07T10:45:05Z   Mon/HOL c2295db2-9c9e-45a6-9163-9ba85eadd6cd   (none)
    2026-09-08T10:45:05Z   Tue     718a7d96-6a51-4083-a6fa-8d580b86b449   daily/49financial/2026-09-04.json @ 2026-09-08T10:45:12Z (+7s)
    2026-09-09T10:45:05Z   Wed     643ff10d-5ddb-44bb-9317-1200b48f480d   daily/49financial/2026-09-08.json @ 2026-09-09T10:45:13Z (+8s)
    matched pairs 21 of 30 fires (denominator = fires at the cron instant)
    FIRES THAT WROTE NO SLICE (named, never verdicted -- NEVER#4: resolve
    the trading calendar before calling any of these a stale pipeline):
       2026-08-15T10:45:05Z  Sat
       2026-08-16T10:45:05Z  Sun
       2026-08-22T10:45:05Z  Sat
       2026-08-23T10:45:05Z  Sun
       2026-08-29T10:45:05Z  Sat
       2026-08-30T10:45:05Z  Sun
       2026-09-05T10:45:05Z  Sat
       2026-09-06T10:45:05Z  Sun
       2026-09-07T10:45:05Z  Mon/HOL

    ARM (c) DENOMINATOR ACROSS BOTH RULES (days x rules):
    scheduled day(s) due = 60 (30 days x 2 rules).
    PRIMARY (log group, START at the cron instant): 28 of 60 due; 28 of 28
    REACHABLE under the groups' retention.
    CORROBORATION (execution-role cold-start AssumeRole): 60 of 60 due.
    THIRD (AWS/Events TriggeredRules, rule-scoped): 60 of 60 due.

==============================================================================
ARM (d) -- THE NEGATIVE CONTROL, ON THE SAME PLANE
==============================================================================
A manual fire has NO AssumeRole by the rule's role in its minute, and its START
RequestId is the CLIENT'S x-amzn-RequestId -- a request id the client did not
receive cannot appear as a START line. The amendment names two, by request id.

   [2be062b2-6642-4092-852a-7dc4c0b714b5] worker ~1's orchestrator invoke, stated 2026-09-09T23:14:43Z
      log GROUP /aws/lambda/etfs-reports-orchestrator read BY TIME over the last 24 h:
      1 of 2 START record(s) carry this request id (1 of 1 is the bar).
         START 2026-09-09T23:14:47Z  RequestId: 2be062b2-6642-4092-852a-7dc4c0b714b5
      AssumeRole by etfs-reports-scheduler-role in THAT MINUTE (2026-09-09T23:14:00Z -> 2026-09-09T23:15:00Z):
      0 of 0 event(s).
      -> the SCHEDULER role is assumed by EventBridge Scheduler and by
         nothing else, so 0 in this minute IS the discriminator.

   [0840a0d3-15aa-4884-a12e-20e75cfa6136] worker ~2's cot invoke, stated 2026-09-09T23:15:50Z
      log GROUP /aws/lambda/cot-etf-ownership-daily read BY TIME over the last 24 h:
      1 of 7 START record(s) carry this request id (1 of 1 is the bar).
         START 2026-09-09T23:15:50Z  RequestId: 0840a0d3-15aa-4884-a12e-20e75cfa6136
      AssumeRole by cot-etf-ownership-daily-role in THAT MINUTE (2026-09-09T23:15:00Z -> 2026-09-09T23:16:00Z):
      2 of 2 event(s).
      -> the EXECUTION role is assumed on EVERY invocation, scheduled or
         not, so the discriminator here is the MINUTE: is this instant a
         cron minute of cot-etf-ownership-daily-schedule ? -> False

[d.2] THE FULL NON-RULE POPULATIONS, listed separately.
      MONTHLY etfs-reports-orchestrator -- 14 of 18 START records carry no scheduler-role AssumeRole:
         2026-06-25T22:29:27Z  7e5288cb-bc24-41c0-bd5e-8dca03c17126
         2026-06-25T23:01:46Z  96ddc07e-51af-4bc8-810b-81687e9ee094
         2026-06-25T23:08:16Z  2d553d48-753d-4710-8163-cc0c93ada24a
         2026-06-25T23:28:44Z  b14e4c9f-8363-42a6-9179-d8cdfd4c50cd
         2026-07-29T03:13:11Z  03693f66-9f78-4df1-90fb-3ada47809bb0
         2026-07-29T03:13:16Z  cbba4ff7-b9eb-49e0-bd4c-e61e3631f0b7
         2026-08-02T03:20:12Z  02f769dd-b0e1-4a74-acc3-017e133881af
         2026-08-02T03:20:37Z  60b5840c-7552-4cf1-854d-a2b749ca4dc1
         2026-09-05T06:02:14Z  2aebafa1-0c9f-4615-a0de-dc49e8f5476b
         2026-09-05T08:31:54Z  64983d5e-911c-4289-bb66-cc1f9ab8be5a
         2026-09-05T08:43:55Z  de83ec26-68c2-46e6-bc05-4a06e3f6e81e
         2026-09-05T08:44:45Z  24bf46ad-1f02-44e0-9cbf-6587dd546c88
         2026-09-09T23:14:47Z  2be062b2-6642-4092-852a-7dc4c0b714b5
         2026-09-10T00:23:04Z  a027eeb0-e954-4dde-9c4f-1d91cad77f67
      DAILY cot-etf-ownership-daily-schedule -- 8 AssumeRole row(s) OFF the cron minute:
         2026-09-01T16:50:17Z  session=cot-etf-ownership-daily  47af82e0-cb48-48b6-b8fe-906bcf360eaa
         2026-09-05T01:38:58Z  session=awslambda_349_20260905013858285  af61f61d-3ce9-4779-a5f8-d563ada1a55a
         2026-09-05T01:45:49Z  session=cot-etf-ownership-daily  ea3a253f-2630-4872-90a6-264d90fc2393
         2026-09-05T06:21:57Z  session=cot-etf-ownership-daily  de9daaf4-e873-4c65-8c5e-3367d267ddb5
         2026-09-05T06:30:35Z  session=cot-etf-ownership-daily  7026a5c7-d402-47ac-8a7d-1d7209d052b2
         2026-09-09T22:58:18Z  session=cot-etf-ownership-daily  d2110c01-6ca0-4f76-9ec5-7b5cebf5c456
         2026-09-09T23:15:36Z  session=cot-etf-ownership-daily  ec6e9232-7247-48ab-a0af-dcdf842ad50a
         2026-09-09T23:39:25Z  session=cot-etf-ownership-daily  26696b84-2bc9-4ad2-9698-479bddb2b9ad
      DAILY bd-49f-etf-ownership-scheduled-floor -- 2 AssumeRole row(s) OFF the cron minute:
         2026-09-05T03:05:45Z  session=awslambda_17_20260905030545122  ddfff317-2f51-478f-ae4b-bf5f330e882a
         2026-09-05T03:11:51Z  session=bd-49f-etf-ownership-daily  2ad79201-2153-4855-bba3-f24f63fd4519

[d.3] DO THE TWO POPULATIONS DIFFER ON THE INITIATOR COLUMN?
      populations disjoint by requestID: True
      the NOT-RULE population is non-empty (a discriminator that never separates
      is decoration): True

==============================================================================
ARM (e) -- THE TABLE PER SCHEDULE, AND THE NEXT FIRE (CONFIRMATION ONLY)
==============================================================================
fires 4 of events 18, initiator = etfs-reports-scheduler-role        [etfs-reports-monthly-run]
    provenance: MEASURED -- each fire is an AssumeRole MANAGEMENT event on
    arn:aws:iam::313476888478:role/etfs-reports-scheduler-role, a role EventBridge Scheduler alone assumes.
fires 30 of events 53, initiator = cot-etf-ownership-daily-schedule
    provenance: THREE INSTRUMENTS, and only the third carries an initiator
    claim. PRIMARY: 14 of 30 scheduled day(s) carry a START RequestId at the
    cron instant in the log GROUP read by time (bounded by 14-day retention).
    CORROBORATION: the execution role's cold-start AssumeRole at the same
    instants, 30 of 30 day(s) -- a fire signal, NOT an initiator signal, since
    an EventBridge rule assumes no role (row ETFS_GUARDRAIL-W3-S3).
    INITIATOR: AWS/Events TriggeredRules, RuleName dimension, reads 30 over the
    same window -- rule-scoped by construction.
fires 30 of events 31, initiator = bd-49f-etf-ownership-scheduled-floor
    provenance: THREE INSTRUMENTS, and only the third carries an initiator
    claim. PRIMARY: 14 of 30 scheduled day(s) carry a START RequestId at the
    cron instant in the log GROUP read by time (bounded by 14-day retention).
    CORROBORATION: the execution role's cold-start AssumeRole at the same
    instants, 30 of 30 day(s) -- a fire signal, NOT an initiator signal, since
    an EventBridge rule assumes no role (row ETFS_GUARDRAIL-W3-S3).
    INITIATOR: AWS/Events TriggeredRules, RuleName dimension, reads 30 over the
    same window -- rule-scoped by construction.

NEXT SCHEDULED FIRE (UTC) -- CONFIRMATION, NEVER A GATE:
    etfs-reports-monthly-run                 2026-10-01T14:00:00Z  (from cron(0 10 1 * ? *) America/New_York)
    cot-etf-ownership-daily-schedule         2026-09-10T10:30:00Z  (from cron(30 10 * * ? *) UTC)
    bd-49f-etf-ownership-scheduled-floor     2026-09-10T10:45:00Z  (from cron(45 10 * * ? *) UTC)

==============================================================================
MUTANT CONTROL -- is the initiator discriminator load-bearing or decoration?
==============================================================================
The DAILY classification turns on ONE constant, FIRE_TOL_S = 180s -- how far an
AssumeRole may sit from a cron minute and still be called that fire. Re-run the
SAME classification over the SAME already-fetched rows with it broken to 0:
   cot-etf-ownership-daily-schedule       FIRE_TOL_S=180  -> RULE=30 of 38
   cot-etf-ownership-daily-schedule       FIRE_TOL_S=0    -> RULE=0 of 38
   bd-49f-etf-ownership-scheduled-floor   FIRE_TOL_S=180  -> RULE=30 of 32
   bd-49f-etf-ownership-scheduled-floor   FIRE_TOL_S=0    -> RULE=0 of 32
The RULE population goes to 0 at tolerance 0 (an AssumeRole lands seconds AFTER
its cron minute, never on it): the constant is load-bearing, not decoration.

The MONTHLY arm needs no tolerance at all and is the stronger control: the
scheduler role is assumed by EventBridge Scheduler and by nothing else, so its
AssumeRole IS the fire. Arm (d) exercised exactly that against a REAL manual
invoke and measured 0 AssumeRole in its minute.

==============================================================================
SECOND INSTRUMENT -- comp-trigger (the estate's scheduler-forensics lens)
==============================================================================
Run beside CloudTrail, as the preflight directs. Its answer, verbatim:

   $ python org/modules/graph/comp_trigger.py etfs-reports --days 90 --budget 120  [rc=0]
   |   budget: 120 s (flag)
   | WITHIN BUDGET: scanned 1 of 1 match; budget: 120 s (flag), used 0.24 s
   | comp-trigger -- forensics for: "etfs-reports"
   |   denominator: 142 events-rules + 19 schedules scanned, region us-east-1
   |   scope: EventBridge rules + Scheduler schedules ONLY; S3 bucket notifications NOT scanned (v1 scope, by design). For an S3-notification/sentinel trig
   | 
   |   etfs-reports-monthly-run  [scheduler]  ENABLED
   |       matched by: name | schedule: -
   |       TF-DESIRED (declared-ness ONLY -- a text hit cannot tell landed from planned): infra/aws/terraform/cot-pipeline/schedule-et.tf, infra/aws/terraf

   $ python org/modules/graph/comp_trigger.py cot-etf-ownership --days 30 --budget 120  [rc=0]
   |   budget: 120 s (flag)
   | WITHIN BUDGET: scanned 1 of 1 match; budget: 120 s (flag), used 0.95 s
   | comp-trigger -- forensics for: "cot-etf-ownership"
   |   denominator: 142 events-rules + 19 schedules scanned, region us-east-1
   |   scope: EventBridge rules + Scheduler schedules ONLY; S3 bucket notifications NOT scanned (v1 scope, by design). For an S3-notification/sentinel trig
   | 
   |   cot-etf-ownership-daily-schedule  [events-rule]  ENABLED
   |       matched by: name | schedule: cron(30 10 * * ? *)
   |       target: arn:aws:lambda:us-east-1:313476888478:function:cot-etf-ownership-daily
   |       LIVE fired-evidence: FIRED 30x in window (last datapoint 2026-09-08)
   |       TF-DESIRED (declared-ness ONLY -- a text hit cannot tell landed from planned): infra/aws/terraform/cot-pipeline/cot-etf-ownership-daily.tf, infr

   $ python org/modules/graph/comp_trigger.py bd-49f-etf-ownership --days 30 --budget 120  [rc=0]
   |   budget: 120 s (flag)
   | WITHIN BUDGET: scanned 1 of 1 match; budget: 120 s (flag), used 0.95 s
   | comp-trigger -- forensics for: "bd-49f-etf-ownership"
   |   denominator: 142 events-rules + 19 schedules scanned, region us-east-1
   |   scope: EventBridge rules + Scheduler schedules ONLY; S3 bucket notifications NOT scanned (v1 scope, by design). For an S3-notification/sentinel trig
   | 
   |   bd-49f-etf-ownership-scheduled-floor  [events-rule]  ENABLED
   |       matched by: name | schedule: cron(45 10 * * ? *)
   |       target: arn:aws:lambda:us-east-1:313476888478:function:bd-49f-etf-ownership-daily
   |       LIVE fired-evidence: FIRED 30x in window (last datapoint 2026-09-08)
   |       TF-DESIRED (declared-ness ONLY -- a text hit cannot tell landed from planned): infra/aws/terraform/bd-pipeline/bd-49f-etf-ownership-daily.tf, in

   READING IT: comp-trigger's LIVE fired-evidence line covers the two EventBridge
   RULES and AGREES with this battery's AssumeRole day count and with AWS/Events
   TriggeredRules. For the SCHEDULER schedule it prints neither an expression nor
   fired-evidence -- filed as ETFS_GUARDRAIL-W3-S4.

==============================================================================
ARM LEDGER
==============================================================================
  ARM (a): HOLDS
  ARM (b): HOLDS
  ARM (c): HOLDS
  ARM (d): HOLDS
  ARM (e): HOLDS

  AWS read calls made: 85, all rc=0: True
  ROWS FILED: ETFS_GUARDRAIL-W3-S3 (list-targets-by-rule carries no RoleArn), ETFS_GUARDRAIL-W3-S4 (comp-trigger is
  quiet on Scheduler schedules), ETFS_GUARDRAIL-W3-S5 (not every AssumeRole on the scheduler role
  is a fire: 2 are CreateSchedule-time role validations)

EGS18-SCHEDULES-FIRED-FROM-HISTORY
```
