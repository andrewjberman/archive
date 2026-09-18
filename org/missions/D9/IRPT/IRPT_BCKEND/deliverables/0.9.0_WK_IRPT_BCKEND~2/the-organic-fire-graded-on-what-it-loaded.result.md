# IB-rtd-1 -- the 13:00Z organic fire, graded on what it actually loaded

TO: `IRPT_BCKEND.TO-IB-rtd-1`. Worker: `0.9.0_WK_IRPT_BCKEND~2`. Branch: `wk-irpt_bckend-4-2`.
Evidence: `rtd1_evidence/` (19 files, all captured live from AWS on 2026-09-18, timestamps below).
Battery: `battery_ib_rtd_1.py` / `IB-rtd-1_R41-AC1_battery_output.txt` (token
`IBR41-ORGANIC-FIRE-READ-BY-ITS-ARTIFACTS`, 23 of 23 arms PASS, rc 0).

## ARM (a) -- T0 row (read BEFORE 13:00:00Z, timestamped)

All reads below completed 12:48:46Z-12:57:44Z, i.e. before the fire; each command's own wall-clock
was printed immediately after the read (`date -u`) as the discriminator against a post-hoc claim.

| item | value | read at |
|---|---|---|
| Lambda `CodeSha256` | `JkY/lBc2Wucz/XIPzyH0zmJt22ucItxjDehbKJko6i4=` | 12:49:07Z |
| Bundle `VersionId` | `.v.aG6Rbk5wXOjGgb4vnQIeGPzrabMKo` | 12:49:26Z |
| Bundle `ETag` | `a8e1a036b4e26cd2fca45f3a295a4c71` (LastModified 12:20:09Z, i.e. minted ~28min before T0) | 12:49:26Z |
| Env keys (5) | `IRPT_DIRECTORY_BUCKET_MAP`, `IRPT_DIRECTORY_PREFIX`, `IRPT_DIRECTORY_RUNNER_INSTANCE_ID`, `IRPT_DIRECTORY_BUNDLE_URI`, `IRPT_DIRECTORY_SOURCE_ROLE_MAP` -- 4 + SOURCE_ROLE_MAP as expected | 12:49:07Z |
| Schedule state | `irpt-directory-refresh`, `cron(0 9 ? * MON-FRI *)` America/New_York, `State: ENABLED` (`get-schedule` carries no explicit next-fire field; the cron + timezone are the schedule's own declaration) | 12:49:49Z |
| 49financial `_refresh/2026-09-18/manifest.json` (clock-date pointer) | `reason_code=REFRESH_DISPATCHED`, `state=RUNNING`, `delta.ssm_command_id=6a856ec7-c0a1-4d1a-b49d-b87bda4ac9d4`, `redispatched=true`. ETag `9c734ca5436a50115a0898cbcb76c0f7`, LastModified 09:02:04Z (an EARLIER driven-arm dispatch's own write; this key is keyed by clock date and, per the code, is never rewritten by a later COMPLETED branch) | 12:50:22-12:51:36Z |
| cottonwood `_refresh/2026-09-18/manifest.json` | same shape, `delta.ssm_command_id=c25a3bdb-7d18-41f0-b521-cf9d513ea6a2` | 12:53:03-12:55:27Z |
| inflection `_refresh/2026-09-18/manifest.json` | same shape, `delta.ssm_command_id=e0f6a54c-d43c-4276-a3e4-41923573d79d` | 12:53:03-12:55:27Z |
| 49financial landed directory | `s3://opal-data-bd/investor-reporting/directory/2026-09-16/directory.json`, ETag `fcdf90de75f24a591c1073489ad1b21f` (matches round-3's own certified ETag) | 12:50:22Z |
| cottonwood landed directory | `s3://opal-data-cot/investor-reporting/directory/2026-09-16/directory.json`, ETag `264e0fbedc24c09bd066ee9eb278ea5f` | 12:54:15Z |
| inflection landed directory | `s3://opal-data-inf/investor-reporting/directory/2026-09-17/directory.json`, ETag `782324f961078b228a32af9316af9836` | 12:54:15Z |

None of the above is a claim about the fire. These are the served identities the fire was about to meet.

## ARM (b) -- the fire, observed

- Polled `describe-log-streams` on `/aws/lambda/irpt-directory-refresh` every 20s from 12:59:53Z;
  the new stream `2026/09/18/[$LATEST]f60df2a19d64437f85e273bbf290a6cc` (firstEventTimestamp
  1789736429688ms = **2026-09-18T13:00:29Z**) appeared at the 13:00:57Z poll -- `.scratch/poll_progress.log`.
- Log events (`get-log-events`): `START RequestId: 986aad35-d0ab-4b76-9161-0ac88e100734 Version: $LATEST`,
  `END RequestId: 986aad35-...`, `REPORT ... Duration: 4783.76 ms ... Max Memory Used: 126 MB`. No error
  line, no traceback -- the invocation completed normally.
- `CodeSha256` re-read immediately after (13:03:51Z): `JkY/lBc2Wucz/XIPzyH0zmJt22ucItxjDehbKJko6i4=` --
  **EQUAL to T0**. The bundle was not re-fetched by this fire (no new SSM dispatch, see below), so there
  is no host-printed bundle identity FROM THIS FIRE to compare; the bundle's identity in the SSM
  transcripts below is the one the ORIGINAL 09:02Z driven dispatch printed, and it is unchanged
  (`sha256=e2a933b923d50626578969b3544e070161f029bdb4132b6f600db66859504b3b` across all 3 firms'
  transcripts).
- **The invoker.** CloudTrail `lookup-events` (`EventName=AssumeRole`, 12:59:00Z-13:02:00Z) contains a
  THIRD `AssumeRole` at 2026-09-18T13:00:29Z (the exact second the log stream begins), distinct from the
  two `invokedBy: lambda.amazonaws.com` calls the function's own code made:
  `userIdentity.type=AWSService`, `userIdentity.invokedBy=scheduler.amazonaws.com`,
  `requestParameters.roleArn=arn:aws:iam::313476888478:role/irpt-directory-refresh-scheduler-role`,
  `requestID=fd5b1376-28f0-41a7-994e-eb1721153098`. That role's ONLY inline policy statement
  (`irpt-directory-refresh-scheduler-policy`) grants exactly `lambda:InvokeFunction` on this function's
  ARN and nothing else (`rtd1_evidence/scheduler_role_policy.json`). **The invoker is EventBridge
  Scheduler** -- discriminated against a manual invoke (no IAM user/role other than the scheduler's own
  assumed exactly this narrow role in this window; `lambda:Invoke` itself is a data event this account's
  trail does not log, so the AssumeRole-on-the-single-purpose-role is the strongest available evidence,
  named as such rather than overclaimed).
- **SSM commands dispatched BY this fire: ZERO**, bounded and measured two ways: (i) `ssm list-commands
  --filters key=InvokedAfter,value=2026-09-18T13:00:00Z,key=InvokedBefore,value=2026-09-18T13:01:30Z`
  returns 0 commands whose `Comment` matches `irpt directory refresh` (a later, UNBOUNDED
  `InvokedAfter`-only re-check caught an unrelated `mdpf accrual bridge` command dispatched at
  13:40:38Z on the same shared host -- cross-pipeline noise, not this fire's dispatch; the battery is
  bounded to avoid exactly that false positive); (ii) each firm's `delta.ssm_command_id` recorded by
  this fire's own write (arm c below) is the SAME id the 09:02Z driven dispatch already held. This is
  CORRECT per the deployed mechanism, not a missed dispatch: `SsmBuildDispatcher.__call__`
  (`infra/aws/lambda/investor-reporting/directory/refresh.py:598-660`, byte-identical deployed-vs-repo,
  confirmed by `sha256sum` on both: `732383dc04fc0b30c62fc665817e49908cacbbbe933ac7fc334dce0e48a8dae7`)
  reads the previous manifest's `ssm_command_id`, finds it `Success`, and only re-dispatches if the
  pointer's key still equals the already-accounted `directory_key` (the no-op branch) -- here the
  previous record read is the STALE clock-date `RUNNING` pointer (never superseded, `directory_key=None`),
  so the "landed" branch fires and NO new command is sent.

## ARM (c) -- the artifacts, by hash: 3 of 3 firms

**Key correction made mid-investigation:** the manifest a completed build actually lands on is NOT the
clock-date key (`_refresh/2026-09-18/manifest.json`, frozen since 09:02Z, checked first and
mistakenly treated as the only carrier) but the RUNNER-DATE key
(`_refresh/2026-09-16/manifest.json` for 49financial and cottonwood, `_refresh/2026-09-17/manifest.json`
for inflection) -- `new_manifest()` keys a COMPLETED build by the runner's own business date
(AMENDMENT 2, `refresh.py:813-823`). That key's `head-object` shows the actual write:

| firm | SSM command status | landed directory ETag before/after | row count | runner-date manifest `reason_code` | manifest write time (this fire) |
|---|---|---|---|---|---|
| 49financial | `Success` (cid `6a856ec7-...`, ran 09:02:03-09:02:17Z, unrelated to this fire) | `fcdf90de75f24a591c1073489ad1b21f` -> `fcdf90de75f24a591c1073489ad1b21f` (UNCHANGED) | 4562 | `REFRESH_COMPLETED_WITH_ADDITIONS` (`delta.added=4562`, `delta.previous_entry_count=0`) | 2026-09-18T13:00:33Z |
| cottonwood | `Success` (cid `c25a3bdb-...`, ran 09:02:04-09:02:13Z) | `264e0fbedc24c09bd066ee9eb278ea5f` -> `264e0fbedc24c09bd066ee9eb278ea5f` (UNCHANGED) | 248 (deduped client_id grain; raw entry_count 259) | `REFRESH_COMPLETED_WITH_ADDITIONS` (`delta.added=248`) | 2026-09-18T13:00:34Z |
| inflection | `Success` (cid `e0f6a54c-...`, ran 09:02:05-09:02:14Z) | `782324f961078b228a32af9316af9836` -> `782324f961078b228a32af9316af9836` (UNCHANGED) | 291 | `REFRESH_COMPLETED_WITH_ADDITIONS` (`delta.added=291`) | 2026-09-18T13:00:35Z |

All three: the runner-date manifest's ETag is BYTE-IDENTICAL before/after this fire (bd
`fae8edbd077fe9f432a89322219667e9`, cot `cfed0f715b4cd5dd04a6d9448474178b`, inf
`19b472c4c4818d00c981b767b3f0addf` -- unchanged from the 10:25Z driven-arm write, confirming
`new_manifest()`'s deterministic byte output), so the OBJECT was rewritten (LastModified moved to
13:00:33-35Z, inside the fire's own 4.78s duration) but the CONTENT did not change: no client failed,
no client disappeared (`delta.disappeared=0` all three), no new build ran. **3 of 3 firms accounted for.**

**Row IRPT_BCKEND-W2-S57 named exactly this shape in advance** (surfaced 2026-09-18T10:06:07Z, from a
DRIVEN fire): `last_manifest()`'s calendar-day backward walk finds the stale clock-date `RUNNING`
manifest before it ever reaches the runner-date COMPLETED one, so `previous_entries()` reads `None`
every time and every re-fire on an unmoved frontier reads `REFRESH_COMPLETED_WITH_ADDITIONS` on
unchanged bytes rather than the `REFRESH_NOOP_SAME_FRONTIER` branch the design names. **This 13:00Z
organic fire reproduces that exact, already-GROUNDED finding via the REAL schedule path** rather than a
manual/driven one -- per the order's own instruction ("Know W2-S57 going in ... record it as the row
predicts, without grading it"), no new row is filed for this; S57 stands as the governing record and is
now independently confirmed by the negative arm.

## ARM (d) -- the negative arm, stated

- **Invoker:** EventBridge Scheduler (`scheduler.amazonaws.com`), via `irpt-directory-refresh-scheduler-role`
  -- see arm (b). The driven fires (IB-rtc-3, IB-rtc-7) were invoked directly by a seat/harness with an
  explicit `business_date` on the event; this fire's Lambda event carried the schedule's OWN payload
  (`{"kind":"irpt_directory_refresh","note":"..."}`, no `business_date` key -- `_event_business_date`
  therefore reads `None` and the handler falls back to `dt.date.today()`), matching the schedule's
  `Target.Input` verbatim (`rtd1_evidence/T0_schedule.json`).
- **Payload:** the schedule's own, unmodified; no override.
- **What the organic fire exercised that the driven fires' own results did not:** the REAL
  `scheduler.amazonaws.com` -> IAM role -> `lambda:InvokeFunction` path end to end, for the first time
  this cell has a live capture of it (IB-rt-6/IB-rtc-3/IB-rtc-7 exercised the SSM/build mechanism directly
  or via a manual/harness invoke, never the schedule's own trigger). **What it did NOT exercise:** a
  missed-trigger path (the schedule was not overdue -- `missed_business_dates` found `len(missed) <= 1`
  for all three firms, since `last_manifest_as_of` read back as today's own date every time) and the
  `REFRESH_NOOP_SAME_FRONTIER` branch (per S57, structurally unreachable today given the manifest-walk
  order). It otherwise **repeated** exactly the branch the driven fires already exercised
  (`SsmBuildDispatcher`'s "landed, no re-dispatch" path), now via the schedule rather than a harness.
- `EventBridge Invocations` was not used as evidence for any arm above; every claim is bound to an
  artifact's own content hash or the log/CloudTrail record it produced.

## R41-AC2 (judgment, for `3.0.0_SA_CVO`, no verdict)

- The organic fire **merely repeated** the branch the driven fires (IB-rtc-3/IB-rtc-7) already
  exercised at the code level (`SsmBuildDispatcher.__call__`'s "prior command Success, pointer differs
  from the stale record's `directory_key`, therefore landed" path) -- it did not hit a missed-trigger,
  over-age, or no-op branch. What is NEW is that this is the first LIVE capture of the schedule's own
  trigger mechanism (`scheduler.amazonaws.com` AssumeRole, `refresh.py:598-660` @`732383dc04`) rather than
  a manual/harness invoke.
- T0 == invocation on every hash checked: Lambda `CodeSha256`
  (`JkY/lBc2Wucz/XIPzyH0zmJt22ucItxjDehbKJko6i4=`, `T0_lambda_config.json`@this commit vs live re-read
  13:03:51Z), and the three firms' landed directory ETags (unchanged, table above). Nothing moved between
  T0 and the invocation; the only thing that moved was each firm's runner-date manifest object being
  rewritten with byte-identical content (S57's pattern, now confirmed organic).
- **What FWD-7's five arms still lack after this fire:** a fire that actually DISPATCHES a new SSM
  command organically has still never been observed (every dispatch on record, this fire included, either
  reused an already-`Success` command or was a manual/driven dispatch) -- that would require the prior
  command to be genuinely stale/failed AT a real 13:00Z fire, which this cell cannot manufacture
  (READ-ONLY, no re-fire). The `REFRESH_NOOP_SAME_FRONTIER` branch remains unexercised by any fire, driven
  or organic, per S57's structural finding (`refresh.py:195-218` `last_manifest()`'s walk order). A
  missed-trigger (`REFRESH_TRIGGER_MISSED`) fire has not been observed either, organic or driven.

## Files

`battery_ib_rtd_1.py`, `IB-rtd-1_R41-AC1_battery_output.txt` (token
`IBR41-ORGANIC-FIRE-READ-BY-ITS-ARTIFACTS`, 23/23 PASS, rc 0, re-run 3 times during this investigation --
the SSM-window check was tightened between run 2 and run 3 after a false positive from an unrelated
pipeline's command was caught, see battery source comment), `rtd1_evidence/` (19 files: T0 reads,
invocation log stream/events, CloudTrail AssumeRole, SSM command-invocation transcripts x3, post-fire
manifests x3, scheduler role policy).
