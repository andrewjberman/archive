# TO-EG-s-17 -- THE FILLED-IN DAY: result

**Worker:** `0.9.0_WK_ETFS_GUARDRAIL~2` | **Branch:** `wk-etfs_guardrail-2-2` (worktree `C:/tmp/wk-etfs-2-2`; the fire ran at `4155c85a1f`, this pass at `b8637e5216`)
**Task order:** `org/missions/D8/ETFS/ETFS_GUARDRAIL/task-orders/ETFS_GUARDRAIL.TO-EG-s-17.the-filled-in-day.md`@`5507841f04` (AMENDED)
**AWS identity for every call:** `arn:aws:iam::313476888478:user/Andrew_Berman` (`sts get-caller-identity`, UserId AIDAUR7FNW6PEXHN2JIOH) -- the launching seat's, per decomposition s.3 decision 1.
**Battery:** `test_egs17_filled_in_day.py` (this folder). **Firing run transcript, verbatim:** `egs17_fire_run.transcript.txt`. **Invoke record:** `invoke_record.json`.

> **PASS 2, 2026-09-10 ~00:2xZ.** The issuer's AMENDMENT (@`5507841f04`, on rows `W1-S13` / `W2-S7`, standing
> authority @`9f4a57262f` / @`1ced87e810`) re-cut arms (b), (c), (d) and (g) onto instruments that exist, after
> pass 1 measured that `lambda:Invoke` is a CloudTrail DATA event no trail selects. The battery was re-run on the
> re-cut arms **against the SAME fire** -- request id `0840a0d3-15aa-4884-a12e-20e75cfa6136`, no second fire and no
> new write (the served object still carries the original ETag `5da999e2fbfadfe302df35ef24407372` and LastModified
> `Wed, 09 Sep 2026 23:15:52 GMT`). The pre-fire census is read from `egs17_fire_run.transcript.txt`; it cannot be
> re-measured, because the fire filled the hole. **Result: 7 of 7 arms hold, rc=0, `EGS17-FILLED-IN-DAY` printed,
> with `CATCHUP-BRANCH-NOT-EXERCISED` printed beside it.** Sections 1, 3-9 below are pass-1 measurements and stand
> unchanged; sections 2, 6 and 10 carry the pass-2 re-cut.

---

## 0. THE ONE-LINE ANSWER

A REAL class-C hole existed and was FILLED by the producer's own fire with its rule's own payload:
**cottonwood 2026-09-08**, recovered at 2026-09-09T23:15:51Z, 4 ETF rows, $53,641,351.75, `source_as_of=2026-09-08`.

**S17-AC1 PASSES by output on the amended face: 7 of 7 arms hold.**

| arm | verdict | evidence |
|---|---|---|
| (a) hole census + probes | HOLD | 20 trading days x 2 partners = 40 cells, 1 absent, 1 real class-C hole (probe `partition=true, priced=12016, output_exists=false`) |
| (b) the rule's own payload | HOLD | `Target.Input` ABSENT on **0 of 2 targets across 2 of 2 daily rules**; the payload fired is that default envelope and carries **no `date` key** |
| (c) the invocation pinned | HOLD | `START RequestId: 0840a0d3-...` **1 of 1** in the log group read BY TIME over its own window; AssumeRole inside the invocation **0**, at the rule's cron instant **0**; `COVERAGE-ABSENT: 0 of 2 trails select AWS::Lambda::Function` printed, never graded |
| (d) the log names the recovered date | HOLD | HEAD-OF-WINDOW hole -> the MAIN PATH's own line, `OK: wrote s3://opal-data-etfs/daily/cottonwood/2026-09-08.json`, **1 of 4** log lines; `CATCHUP-BRANCH-NOT-EXERCISED` printed beside the token |
| (e) slice exists after | HOLD | head-object 1345 B at 23:15:52Z (after the 23:15:47Z invoke), second reader re-downloaded and parsed 4 rows |
| (f) positive control (a present date) | HOLD | 2026-09-04 PRESENT, named in **0 of 4** log lines, never fired at |
| (g) schedules' firings from history | HOLD | the fire-instant AssumeRole management events: cot **30 of 30 days at 10:30:24Z**, bd **30 of 30 at 10:45:05Z**; negative control holds (0 AssumeRole in the manual invoke, 1 client START RequestId); `COVERAGE-ABSENT` printed |

Per the order's `<proof_of_spec>` clause -- "flip only when S17-AC1 PASSES by output" -- **the `<status>` line IS
flipped to `complete` in the same commit as this deliverable.**

### What the token does NOT claim

`CATCHUP-BRANCH-NOT-EXERCISED` is printed beside `EGS17-FILLED-IN-DAY`, not implied. The recovery was the producer's
own MAIN PATH writing the newest partition; `_catchup_missing_dates` never ran a date, because the only real hole in
the estate IS the newest partition and the sweep skips it as `skip_date`. Exercising the catch-up BRANCH needs a hole
OLDER than the newest priced partition; the estate has none, and making one is a served DELETE -- Andrew's word,
carried by the issuer, never by this worker. Unscoped corroboration: **0 CATCHUP lines in 152 cot / 103 bd log events
over 30 days.**

---

## 1. THE HOLE CENSUS (denominators printed)

Calendar: `lib/trading_calendar.py`, `calendar_source() = NYSE/pandas_market_calendars`.
Window: the last **20 TRADING days** through yesterday (2026-09-08). Note 2026-09-07 is Labor Day and is correctly
absent from the list; 2026-09-05/06 are the weekend.

```
2026-08-11 2026-08-12 2026-08-13 2026-08-14 2026-08-17 2026-08-18 2026-08-19 2026-08-20 2026-08-21 2026-08-24
2026-08-25 2026-08-26 2026-08-27 2026-08-28 2026-08-31 2026-09-01 2026-09-02 2026-09-03 2026-09-04 2026-09-08
```

| partner | prefix | keys under prefix (denominator) | absent in window | absent dates |
|---|---|---|---|---|
| cottonwood | `s3://opal-data-etfs/daily/cottonwood/` | 61 | **1 of 20** | `2026-09-08` |
| 49financial | `s3://opal-data-etfs/daily/49financial/` | 89 | 0 of 20 | -- |

`list-objects-v2` on both prefixes, `IsTruncated` absent on both (the denominator is the prefix, not a page).

**The producer's OWN window was censused too**, unscoped by the 20-day cut: the shipped signal
`s3://opal-data-etfs/platinum/reports/2026-08/etf_ownership.pdf` EXISTS (head-object rc=0, LastModified
`Tue, 01 Sep 2026 17:38:41 GMT`, 273,857 bytes), so `_window_dates` starts at the CURRENT month's 1st --
2026-09-01..2026-09-08, 5 trading days. Over the wider 2026-08-01..2026-09-08 span (26 trading days) cottonwood
was absent on exactly the same 1 date and 49financial on 0. **There was exactly one hole in the estate.**

### The probe answers (non-writing mode, `{"date": d, "probe": true}`)

Probed: every ABSENT date -- 1 of 1.

```
cot-etf-ownership-daily 2026-09-08 -> {"status": "probe", "date": "2026-09-08", "partition": true, "priced": 12016, "output_exists": false}
```

`partition=true` + `priced=12016 > 0` + `output_exists=false` = **CLASS C, a real hole.** Not class B: the
ZERO-vs-MISSING contract's `priced == 0` case (property 4, "NO invoke against it") does not apply -- 12,016
positions are priced. No class-B date and no upstream-absent date was fired at, because none was found.

### The probe DISCRIMINATES (it is not a constant)

Three further probes, all non-writing, run as this deliverable's control:

```
2026-09-04 (slice present)     -> {"partition": true,  "priced": 12033, "output_exists": true}
2026-07-31 (slice present)     -> {"partition": true,  "priced": 10960, "output_exists": true}
2026-09-06 (Sunday, no source) -> {"partition": false, "priced": 0,     "output_exists": false}
```

4 probes, 3 distinct answer shapes; `output_exists` came back `false` for the hole and `true` for both non-holes,
and `partition` came back `false` where there is genuinely no upstream. (2026-07-31's answer contradicts the
producer's own docstring, which still calls it a known upstream gap -- filed as `ETFS_GUARDRAIL-W2-S9`.)

---

## 2. THE RULE'S OWN PAYLOAD, READ LIVE

```
aws events describe-rule --name cot-etf-ownership-daily-schedule   rc=0
  ScheduleExpression = cron(30 10 * * ? *)   State = ENABLED
aws events list-targets-by-rule --rule cot-etf-ownership-daily-schedule   rc=0
  Targets: [ { "Id": "CotEtfOwnershipDailyLambda",
               "Arn": "arn:aws:lambda:us-east-1:313476888478:function:cot-etf-ownership-daily" } ]
```

**There is no `Target.Input`, no `InputPath` and no `InputTransformer`** -- measured on BOTH daily rules in pass 2:
`Target.Input present on 0 of 2 target(s) across 2 of 2 daily rules` (`cot-etf-ownership-daily-schedule`,
`cron(30 10 * * ? *)`; `bd-49f-etf-ownership-scheduled-floor`, `cron(45 10 * * ? *)`). Neither
`events list-targets-by-rule` nor an EventBridge Scheduler schedule carries a payload for these producers, because
they are EventBridge RULES with no Input override: the rule delivers the DEFAULT scheduled-event envelope.

**Neither target carries a `RoleArn` either** (0 of 2) -- an EventBridge rule invokes a Lambda through the
function's own resource policy (`Principal: events.amazonaws.com` + `AWS:SourceArn` = the rule ARN), not by
assuming a role. That is row `ETFS_GUARDRAIL-W2-S10` and it is why arms (c) and (g) below are graded on the
execution role's assumption at the INVOCATION interval and at the CRON INSTANT, rather than on a "rule role" that
does not exist for these two rules.

The payload fired was therefore that envelope:

```json
{"version": "0", "id": "egs17-manual-20260909T231545Z", "detail-type": "Scheduled Event",
 "source": "aws.events", "account": "313476888478", "time": "2026-09-09T23:15:45Z", "region": "us-east-1",
 "resources": ["arn:aws:events:us-east-1:313476888478:rule/cot-etf-ownership-daily-schedule"], "detail": {}}
```

**The payload carries NO `date` key** -- which the amended arm (b) now requires, and which is what was fired. The
original face's "plus the date field the port honors" was deliberately NOT taken, and that was the crux of
`ETFS_GUARDRAIL-W2-S8` (ruled, and the arm re-cut to match): adding a `date` key routes the handler to the explicit-date branch
(`lambda_function.py`@`4155c85a1f`:304-308), which returns `_process_date(...)` DIRECTLY and never populates
`catchup_processed` at all. "The scheduled payload plus the date field" and "the recovered date named in
`catchup_processed`" cannot both be satisfied by the deployed code. The envelope WITHOUT a date field is both
byte-equal to what the schedule delivers and the only path that reaches the catch-up sweep, so it is the payload
that gives FWD-1 its best chance -- and it is what was fired.

---

## 3. THE FIRE

Guard first: `head-object daily/cottonwood/2026-09-08.json` -> **rc=255 (ABSENT)**. The battery refuses to fire at
any date whose slice exists; the guard is in the code path, not in the prose.

```
FIRING cot-etf-ownership-daily at 2026-09-08 with the rule's own payload -- start UTC 2026-09-09T23:15:47Z
aws lambda invoke rc=0  end UTC 2026-09-09T23:15:50Z
INVOKE ENVELOPE: {"StatusCode": 200, "ExecutedVersion": "$LATEST"}
RESPONSE PAYLOAD:
{"status": "ok", "date": "2026-09-08", "key": "daily/cottonwood/2026-09-08.json", "slices": 4,
 "total_ownership": 53641351.75, "source_as_of": "2026-09-08",
 "catchup_processed": [], "catchup_failed": [], "catchup_skipped_unpriced": []}
```

**Request id and UTC (from the function's OWN log, not the client):** `0840a0d3-15aa-4884-a12e-20e75cfa6136`,
START `2026-09-09T23:15:50.560Z`. The CLI v1 `lambda invoke` envelope does not carry a request id; the authoritative
id is the one the function logged.

### The log lines for THIS invocation, verbatim (4 of 4 events in the window)

```
2026-09-09T23:15:50.560Z START RequestId: 0840a0d3-15aa-4884-a12e-20e75cfa6136 Version: $LATEST
2026-09-09T23:15:51.163Z OK: wrote s3://opal-data-etfs/daily/cottonwood/2026-09-08.json (4 ETF slices, total_ownership=53641351.75, source_as_of=2026-09-08, generated_at=2026-09-09T23:15:51Z)
2026-09-09T23:15:51.233Z END RequestId: 0840a0d3-15aa-4884-a12e-20e75cfa6136
2026-09-09T23:15:51.233Z REPORT RequestId: 0840a0d3-15aa-4884-a12e-20e75cfa6136	Duration: 673.14 ms	Billed Duration: 674 ms	Memory Size: 512 MB	Max Memory Used: 267 MB
```

ONE write, and it is the recovered slice. No `CATCHUP:` line, no `CATCHUP-SKIP:` line, no `SKIP:` line -- the sweep
ran over 2026-09-01..2026-09-08 and found nothing to do, because every other date's output already existed and the
one date it might have recovered was the `skip_date`.

> **Instrument trap, recorded because it cost two runs:** `describe-log-streams` selected by
> `firstEventTimestamp` OR `lastEventTimestamp` MISSES this invocation. A warm Lambda REUSES its container's log
> stream, and the stream index is eventually consistent -- the stream carrying this fire reported
> `lastEventTimestamp = 23:15:37Z` while the invocation's own events sat at `23:15:50Z` INSIDE it. Read the LOG
> GROUP by time (`filter-log-events --start-time`), never the stream index. A single un-retried read here returns
> zero events and reads exactly like "the function logged nothing".

---

## 4. THE SLICE AFTER (arm (e))

```
aws s3api head-object --bucket opal-data-etfs --key daily/cottonwood/2026-09-08.json   rc=0
  LastModified  : Wed, 09 Sep 2026 23:15:52 GMT     (invoke started 23:15:47Z -- AFTER)
  ContentLength : 1345                              (> 0)
  ETag          : "5da999e2fbfadfe302df35ef24407372"
  ContentType   : application/json
```

**Second reader** -- the object re-downloaded (`aws s3 cp`, rc=0) and parsed independently of the producer's
response: **4 rows** (denominator 4 of 4 universe ETFs), every row `date=2026-09-08` and `source_as_of=2026-09-08`.

| etf | ownership_value | account_count |
|---|---|---|
| DIVZ | 19,079,942.93 | 330 |
| IDVZ | 15,516,123.03 | 331 |
| PFDE | 12,430,725.84 | 320 |
| PFOE | 6,614,559.95 | 319 |
| **total** | **53,641,351.75** | |

The total matches the producer's own `total_ownership` in the response and in the log line, computed by three
different readers (the function, the response, this deliverable's re-parse).

---

## 5. THE POSITIVE CONTROL (arm (f)) -- a READ, never a re-run

Control date: **2026-09-04**, a date that is NOT missing. `head-object daily/cottonwood/2026-09-04.json` rc=0,
LastModified `Wed, 09 Sep 2026 10:30:30 GMT`. It appears in **0 of 4** log lines of this invocation and in
`catchup_processed` (which is `[]`).

NOT-LISTED is the evidence, and it is the mechanism's own shape: `_catchup_missing_dates` `continue`s on an
existing output (`lambda_function.py`:270-271) with no log line at all, so a present date is reported recovered by
neither carrier. It was never invoked against.

---

## 6. THE SCHEDULES' OWN FIRINGS, FROM HISTORY (arm (g))

**The instrument the criterion names does not exist in this account.** Measured before concluding anything from a
zero:

```
aws cloudtrail describe-trails -> 2 trails
  opal-organization-trail    -- management events (All) + AWS::S3::Object ReadOnly on opal-data-bd/, opal-data-inf/
  opal-served-key-write-trail -- eventCategory=Data on AWS::S3::Object under 3 platinum/firm/ prefixes
  trails selecting AWS::Lambda::Function data events: 0 of 2
```

`lambda:Invoke` is a CloudTrail DATA event. With no selector for it, no `Invoke` record is written for ANY
invocation. Positive control: this worker's own probe (23:15:36Z) and fire (23:15:47Z) demonstrably executed
(RequestIds above) and `lookup-events` over that exact window returns `eventName=Invoke = 0`.

30-day sweep, both producers, `lookup-events --lookup-attributes AttributeKey=ResourceName,...`
(2026-08-10T23:16Z..2026-09-09T23:16Z, CLI-paginated, counted client-side):

| function | events scanned | `Invoke` | `AssumeRole` |
|---|---|---|---|
| cot-etf-ownership-daily | 73 | **0** | 71 |
| bd-49f-etf-ownership-daily | 64 | **0** | 62 |

**What IS available, and what was delivered instead:** every fire causes Lambda to `AssumeRole` the function's
execution role, and that IS a management event. Listing them by day gives the schedules' own firing history:

| producer | rule | cron | days with a fire AT the cron instant | off-cron invokes seen |
|---|---|---|---|---|
| cot-etf-ownership-daily | cot-etf-ownership-daily-schedule | `cron(30 10 * * ? *)` | **30 of 30 days seen**, all at 10:30:24Z | 2026-09-01 16:50:17Z; 2026-09-05 01:45:49Z, 06:21:57Z, 06:30:35Z (round-1 deploy testing); 2026-09-09 22:58:18Z, 23:15:36Z (**this worker**) |
| bd-49f-etf-ownership-daily | bd-49f-etf-ownership-scheduled-floor | `cron(45 10 * * ? *)` | **30 of 30 days seen**, all at 10:45:05Z | 2026-09-05 03:11:51Z (round-1 deploy testing) |

The per-day table is printed in full in the battery's ARM-G output. **Rule (4) -- the schedule fires -- is met from
history on both producers, 30 of 30 days, with the manual invokes appearing in a separate off-cron column** as the
negative control.

**PASS 2, the amended arm (g).** The AMENDMENT re-cut this arm onto exactly this instrument, so it is now graded
rather than recorded: the `Invoke` read prints `COVERAGE-ABSENT: 0 of 2 trails select AWS::Lambda::Function` and is
never a pass or a fail, and the firing history comes from the fire-instant `AssumeRole` management events above.

What this instrument CANNOT do, stated rather than glossed: `AssumeRole`'s userIdentity is
`{"type":"AWSService","invokedBy":"lambda.amazonaws.com"}` for a rule-initiated and a person-initiated invoke alike,
and the assumption itself is a COLD-START artifact, not an initiator signal. So the discrimination is carried by the
INSTANT, measured at two grains and both printed:

```
NEGATIVE CONTROL -- this battery's manual invoke (2026-09-09T23:15:47Z):
  AssumeRole by arn:aws:iam::313476888478:role/cot-etf-ownership-daily-role
    between its own START and END           : 0 of 1 in a +/-2 min window
    at the rule's cron instant 10:30Z       : 0
  START RequestId in the log group by time  : 0840a0d3-15aa-4884-a12e-20e75cfa6136 (1 of 1) -- a CLIENT's call
```

The 1 AssumeRole that IS in the surrounding window sits at 23:15:36Z and belongs to the PROBE's cold start:
`AssumeRole 23:15:36Z -> INIT_START 23:15:37.757Z -> START RequestId ec6e9232-... 23:15:40.735Z`. The fire's own
`START 23:15:50.560Z` has no preceding `INIT_START` and no assumption -- it ran warm. A scheduled fire would have
had to land at 10:30:24Z, 12 h 45 m earlier, and that fire's log names a different date (2026-09-04).

---

## 7. WHY 2026-09-08 WAS MISSING -- the log says it, and it is a measured race

The cot schedule fires at **10:30Z**. The cot `fact_holdings` partition for date D lands at **D+1 ~11:46Z** --
10 of 10 dates sampled:

| date D | partition LastModified |
|---|---|
| 2026-08-25 | Wed, 26 Aug 11:46:04 GMT |
| 2026-08-26 | Thu, 27 Aug 15:39:37 GMT |
| 2026-08-27 | Fri, 28 Aug 11:46:01 GMT |
| 2026-08-28 | Sat, 29 Aug 11:46:05 GMT |
| 2026-08-31 | Tue, 01 Sep 11:46:04 GMT |
| 2026-09-01 | Wed, 02 Sep 11:46:05 GMT |
| 2026-09-02 | Thu, 03 Sep 11:46:04 GMT |
| 2026-09-03 | Fri, 04 Sep 11:46:14 GMT |
| 2026-09-04 | Sat, 05 Sep 11:46:04 GMT |
| 2026-09-08 | Wed, 09 Sep 11:46:01 GMT |

So the fire on D+1 runs **76 minutes BEFORE** D's partition exists, and the sweep's third skip ("upstream partition
absent, never fabricate") correctly takes it. The proof is today's scheduled fire's own log, verbatim:

```
2026-09-09T10:30:25.298Z INIT_START ...
2026-09-09T10:30:28.237Z START RequestId: 1b463933-0b3d-4425-b4f7-bd276e795ca5 Version: $LATEST
2026-09-09T10:30:29.474Z OK: wrote s3://opal-data-etfs/daily/cottonwood/2026-09-04.json (4 ETF slices, total_ownership=53905394.72, source_as_of=2026-09-04, generated_at=2026-09-09T10:30:29Z)
2026-09-09T10:30:29.570Z END RequestId: 1b463933-0b3d-4425-b4f7-bd276e795ca5
```

At 10:30Z today the newest partition was still 2026-09-04; 2026-09-08's landed 76 minutes later; the slice stayed
absent for the next 11 h 30 m, until this order's fire at 23:15:51Z. **This is a genuine reporting hole, not a bookkeeping one,
and it repeats every day** -- which is why `ETFS_GUARDRAIL-W2-S8` is ARMED. The bd twin does NOT have the race: its
floor is `cron(45 10 * * ? *)`, deliberately 29 minutes AFTER the measured fact_rps landing (D+1 10:16Z), and
49financial was absent on 0 of 20 trading days.

**Unscoped catch-up history** (`filter-log-events`, 30 days): cot 142 log events scanned, **CATCHUP lines = 0**;
bd 103 log events scanned, **CATCHUP lines = 0**. Since the round-1 port the sweep has never named a recovered date
on either producer -- consistent with a hole that is always at the head of the window, where `skip_date` sits.

---

## 8. THE PORT RESPECTED THE REPORTING-OBLIGATION WINDOW (for S17-AC2)

Read, not assumed, at `lambda_function.py`@`4155c85a1f`:180-191 and exercised live:

- the terminus is a **SHIPPED SIGNAL**: `_report_shipped` does `head_object` on
  `platinum/reports/<YYYY-MM>/etf_ownership.pdf`; a denied/errored read is treated as NOT shipped and logged `WARN:`
  so a blocked render never silently ends the reconciliation. The 2026-08 report IS shipped (measured above), so the
  window correctly started at 2026-09-01, not 2026-08-01.
- **no day-count**: there is no `CATCHUP_WINDOW_DAYS` and no walk-back constant anywhere in either producer; the
  window is `tcal.trading_days_between(start, today - 1 day)`.
- the **ZERO-vs-MISSING** contract is touched and unchanged (`priced == 0` -> `skipped-no-valued-source`, no slice
  written, listed in `catchup_skipped_unpriced` rather than hidden). It was not exercised by this order because no
  class-B date existed in the window -- and the order forbids manufacturing one.
- **class B was never fired against**: the only date fired at had `priced=12016`.

## 9. WHAT THIS WORKER DID NOT DO

| not done | why |
|---|---|
| fired a SECOND time in pass 2 | the amendment: "RE-RUN the battery on the re-cut arms against the SAME fire ... NO second fire, no new write." Proven, not asserted: the served object still carries ETag `5da999e2fbfadfe302df35ef24407372`, ContentLength 1345 and LastModified `Wed, 09 Sep 2026 23:15:52 GMT` after three pass-2 runs -- byte-identical to the single original write. |
| manufactured a hole | decomposition s.6 bound 1 -- a controlled hole means deleting a served object, which needs a human's word. A real hole existed, so the question did not arise; and a hole the catch-up BRANCH could name would have to be mid-window, which only a served delete can create. |
| deleted or overwrote any served object | the ONE write in this order is the producer's own run creating `daily/cottonwood/2026-09-08.json`, a key that did not exist (guard: head-object rc=255 before the fire). |
| fired at a date whose slice exists | guarded in code; the only non-probe invoke targeted the confirmed class-C date. |
| fired the bd-49f producer | 0 absent dates of 20 -- no hole, no fire. Its history was read only. |
| changed any code or deployed anything | "NO CODE CHANGE, NO DEPLOY" -- the defects found are rows with measurements, not hot fixes. |
| built a CloudTrail data-event trail | outside `<paths>`, and a monitoring/observability build is gated behind Andrew's explicit word (CLAUDE.md HARD STOPS). |
| read any firm bucket directly | NEVER#1 -- `opal-data-etfs` and the firm-scoped producers only; the probe answered for the firm data. |
| (pass 1) flipped `<status>` to complete | S17-AC1 did not PASS by output then; the order's own clause forbade the flip. In pass 2, on the amended face, S17-AC1 PASSES 7 of 7 and the flip is made in the same commit as this deliverable. |
| re-cut any arm myself | a re-cut is the issuer's act. Pass 1 filed the measurements as rows and stopped; the AMENDMENT @`5507841f04` is the issuer's, under the standing authority. Where the amendment's own instrument description did not match the world (there is no "rule role" on these two rules), the finer grain was measured, printed at BOTH grains, and filed as `ETFS_GUARDRAIL-W2-S10` -- never silently re-read. |

## 10. ROWS FILED

| id | class / hazard | one line |
|---|---|---|
| `ETFS_GUARDRAIL-W2-S7` | BLOCKING / INERT | no trail selects Lambda data events, so the CloudTrail `Invoke` record arms (c) and (g) name does not exist for any invocation; firings delivered from `AssumeRole` instead |
| `ETFS_GUARDRAIL-W2-S8` | BLOCKING / **ARMED**, disarm `2.0.0_SA_COO` | the only real hole is the newest partition, which the sweep skips as `skip_date`, so `catchup_processed` came back empty on a fire that filled the hole -- and the cause is a measured 76-minute schedule/landing race that repeats daily |
| `ETFS_GUARDRAIL-W2-S9` | OBSERVATION / INERT | the producer's docstring still calls 2026-07-31 a known upstream gap; the deployed probe answers `partition=true, priced=10960, output_exists=true` |
| `ETFS_GUARDRAIL-W2-S10` | OBSERVATION / INERT | the amendment's arms (c)/(g) name "the rule's role", but 0 of 2 daily-rule targets carry a `RoleArn` -- an EventBridge rule invokes a Lambda through the function's resource policy, so the only role CloudTrail names is the EXECUTION role, assumed on a cold start by either initiator. Arms graded at the finer grain (invocation interval + cron instant), both printed |

**Ruled by the issuer @`5507841f04`:** `W2-S7` and `W2-S8` -> arms (b), (c), (d), (g) re-cut in place; the
76-minute schedule/landing race and `W2-S9`'s stale docstring are carried to the CTO's L10 by the issuer, with
nothing owed by this worker. `W2-S10` is filed by this pass and is not blocking -- both arms it touches HOLD.
