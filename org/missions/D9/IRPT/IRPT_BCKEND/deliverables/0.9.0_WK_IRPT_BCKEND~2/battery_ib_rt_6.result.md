# BATTERY IB-rt-6 -- RESULT

**Cell:** `IB-rt-6` -- the refresh builds behind the ENABLED schedule
**Task order:** `IRPT_BCKEND.TO-IB-rt-6`
**Run by:** `0.9.0_WK_IRPT_BCKEND~2`
**Run at HEAD:** `5d71d45442` on `wk-irpt_bckend-2-2c` (LOCAL)
**Invocation:** `timeout 1500 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/battery_ib_rt_6.py`
**Exit code:** `1`

## THE VERDICT IN ONE LINE

**PASS 14 | FAIL 0 | BLOCKED 3 across 17 graded checks. THE ACCEPTANCE TOKEN IS WITHHELD and
RT6-AC1 is FAIL.** The DISPATCH half of this cell is built, deployed, exercised in production and
proven; the BUILD half cannot land an artifact, on a premise this order's `<paths>` cannot reach.

## WHAT IS TRUE, MEASURED AGAINST THE DEPLOYED WORLD

- The deployed `irpt-directory-refresh` DISPATCHES. Three firms, three real SSM command ids, read
  back from the SERVED manifests in the three firm buckets rather than from the invoke's own
  return value -- a producer's self-report is never the served artifact.
- Its served bytes equal the committed bytes (`CodeSha256` == source-map `artifact_sha256`), its
  timeout is UNCHANGED at 60 s (a raised timeout would be the tell that something waits), and the
  bundle uri agrees across all three places it exists: the one Python authority, the Terraform
  local, and the SERVED environment.
- The schedule reads ENABLED on the SCHEDULER plane (`aws scheduler get-schedule`, not
  `aws events describe-rule` -- different planes, and the wrong one answers about a different
  object).
- The runner's IMPORT CHECK PASSES ON THE HOST, in the host's own stdout, dispatched by the
  deployed function. WITH A NEGATIVE CONTROL: the SAME script on the SAME host printed
  `IMPORT-FAIL` two mints earlier, so the pass is a measurement and not a constant.
- Three of the arms read PAIRWISE DISTINCT envelope values: `REFRESH_DISPATCHED` (real path),
  `DIRECTORY_OVER_AGE`, `REFRESH_TRIGGER_MISSED`.
- The APPLIED role carries this cell's four statements and NONE of `ec2:StopInstances`,
  `ec2:TerminateInstances`, `ssm:CancelCommand` or `iam:PassRole`.
- Five change-management entries, all CLOSED, sentinel absent.

## WHAT IS BLOCKED, AND WHY IT IS NOT A FAILURE OF NERVE

- **arm (b), 0 of 3 firms have a landed directory artifact.** Row `IRPT_BCKEND-W2-S49`:
  `mdpf-daily-runner-ec2-role` is AccessDenied on 5 of the 9 prefixes the runner reads and on
  3 of 3 firm destination prefixes -- measured FROM THE HOST, by the host, with a positive control
  in the same sweep. The remedy is an IAM change on a shared host role in a root this order does
  not grant.
- **2 of the 4 arms** (source completion, new revision) need a landed artifact to read a source
  date or a revision FROM. They are not simulated here: a self-wrapping harness is not evidence.
- **the build stops at a NAMED missing dependency**, verbatim from the host. Row
  `IRPT_BCKEND-W2-S51` enumerates all seven by subtraction over a printed denominator.

## CONTROLS

**MUTANT -- FIRED AS EXPECTED.** A copy of this battery with `IMPORT_OK_COMMAND` repointed at the
THREE-member run (the command that printed `IMPORT-FAIL`) was executed at the same tree depth:

```
  [d.1] FAIL      the runner's import check PASSES on the host, first-party modules printed: trading_calendar, ids   denominator: 2 of 3 modules named
  PASS 13 | FAIL 1 | BLOCKED 3   denominator: 17 graded check(s)
```

The arm moved PASS -> FAIL and the totals moved 14/0/3 -> 13/1/3. A passing assertion never
mutated has never been tested; this one has.

**DETERMINISM -- STABLE.** Two full runs against LIVE AWS, diffed: **0 differing lines**.

## THE RUN, VERBATIM

```
BATTERY IB-rt-6 -- the refresh builds behind the ENABLED schedule
repo: C:\tmp\wk-irpt-2-2c
subject: the DEPLOYED irpt-directory-refresh, its APPLIED role, the three firm buckets, and the SSM records the function itself created

==============================================================================
ARM (a) WIRED -- the deployed function dispatches, and the manifest says so
==============================================================================
  [a.1] PASS      served CodeSha256 /qyUho5JNtliMMu79XjnVVsvl6Y2CAlfxEgPANXouJE= == source-map artifact_sha256
  [a.2] PASS      dispatch configuration present on the SERVED function: IRPT_DIRECTORY_RUNNER_INSTANCE_ID, IRPT_DIRECTORY_BUNDLE_URI   denominator: 2 of 2
  [a.3] PASS      function Timeout 60s (send-and-return: unchanged from round 1)
  [a.4] PASS      bundle uri: spec authority == terraform local == SERVED env  (s3://opal-data-mdpf/code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz)
      49financial  reason=REFRESH_DISPATCHED     build_dispatch=SSM command=a83c5d88-2392-43f2-be55-c9845a0b1384
      cottonwood   reason=REFRESH_DISPATCHED     build_dispatch=SSM command=2e2cb3b7-cb8b-4740-97ab-88cae25f78f6
      inflection   reason=REFRESH_DISPATCHED     build_dispatch=SSM command=a787fdc6-169c-451b-92e3-78c1d76f0498
  [a.5] PASS      SERVED manifests for 2026-09-11 carrying a real SSM dispatch fact   denominator: 3 of 3 firms (read back: 3)
  [a.6] PASS      schedule LIVE state ENABLED cron(0 9 ? * MON-FRI *) America/New_York, target irpt-directory-refresh

==============================================================================
ARM (b) THREE OF THREE, BEFORE/AFTER -- the production builds
==============================================================================
      49financial  opal-data-bd     directory artifacts=0  latest.json=0  (objects under the prefix=1)
      cottonwood   opal-data-cot    directory artifacts=0  latest.json=0  (objects under the prefix=1)
      inflection   opal-data-inf    directory artifacts=0  latest.json=0  (objects under the prefix=1)
  [b.1] BLOCKED   firms with a landed directory artifact AND its pointer -- row IRPT_BCKEND-W2-S49: the runner host's identity is AccessDenied on 5 of 9 source prefixes and 3 of 3 destinations, so no build can land   denominator: 0 of 3

==============================================================================
ARM (c) FOUR ARMS -- each reading its own distinct envelope value
==============================================================================
      the REAL build command a83c5d88-2392-43f2-be55-c9845a0b1384 ended Failed rc=1 -- which is what a later fire reads back
      expiry: a directory as-of 2026-08-01 read at 2026-09-11 -> DIRECTORY_OVER_AGE, age 29 trading day(s) against a ceiling of 2, calendar NYSE/pandas_market_calendars
      missed: last manifest 2026-09-01, clock 2026-09-11 -> 7 expected trading day(s) with no manifest -> REFRESH_TRIGGER_MISSED
      source completion / new revision: both require a LANDED directory artifact to read a source date or a revision from. 0 of 3 firms have one (arm b) -- BLOCKED on row IRPT_BCKEND-W2-S49, not simulated here.

      dispatched-or-failed (REAL PATH)       -> REFRESH_DISPATCHED
      expiry (controlled clock)              -> DIRECTORY_OVER_AGE
      missed trigger (controlled clock)      -> REFRESH_TRIGGER_MISSED
  [c.1] PASS      the arms that can run read PAIRWISE DISTINCT envelope values: DIRECTORY_OVER_AGE, REFRESH_DISPATCHED, REFRESH_TRIGGER_MISSED   denominator: 3 distinct of 3 arms run
  [c.2] BLOCKED   source completion and new revision cannot be driven on the REAL build path   denominator: 2 of 4 arms on the real path

==============================================================================
ARM (d) THE HOST CAN RUN IT -- the import check, in the host's own stdout
==============================================================================
      | [irpt-directory] firm=49financial as_of=2026-09-11 run=49financial-2026-09-11
      | [irpt-directory] bundle sha256 d949b7881c01c18599e472225166d34805c8645da4f283d112df009ae07b1758
      | [irpt-directory] member directory_runner.py
      | [irpt-directory] member holdings_snapshot.py
      | [irpt-directory] member ids.py
      | [irpt-directory] member trading_calendar.py
      | [irpt-directory] --- import check (arm d) ---
      | [irpt-directory] python3 3.9.25
      | [irpt-directory] dep boto3      1.42.97
      | [irpt-directory] dep pandas     2.3.3
      | [irpt-directory] dep pyarrow    21.0.0
      | [irpt-directory] dep jsonschema 3.2.0
      | [irpt-directory] IMPORT-OK first-party modules resolved: trading_calendar, ids, contract
      | [irpt-directory] SOURCE_SETS ['49financial', 'cottonwood', 'inflection']
      | [irpt-directory] --- build ---
      | [irpt-directory] rc=1 firm=49financial as_of=2026-09-11
  [d.1] PASS      the runner's import check PASSES on the host, first-party modules printed: trading_calendar, ids, contract   denominator: 3 of 3 modules named
  [d.2] PASS      host dependency versions printed by the run itself: boto3, pandas, pyarrow, jsonschema   denominator: 4 of 4
  [d.3] PASS      NEGATIVE CONTROL -- the SAME script on the SAME host with the 3-member bundle printed IMPORT-FAIL (command 940c828f-c176-4a2d-afcc-1693d3d97fe6), so the pass above is a measurement and not a constant
      NEXT BLOCKER (verbatim): FileNotFoundError: [Errno 2] No such file or directory: '/tmp/irpt-directory-refresh/49financial-2026-09-11/infra/aws/lambda-edge/_shared/firm-config.
  [d.4] BLOCKED   the build stops at a NAMED missing dependency -- row IRPT_BCKEND-W2-S51 enumerates all seven by subtraction over a printed denominator   denominator: 1 named line(s)

==============================================================================
ARM (e) LEDGERS -- every entry closed, the sentinel gone, the plan clean
==============================================================================
      20260912T0655Z_irpt-bckend-rt6_deploy_completion.md        CLOSED
      20260912T0821Z_irpt-bckend-rt6_deploy_completion.md        CLOSED
      20260912T0833Z_irpt-bckend-rt6_deploy_completion.md        CLOSED
      20260912T0844Z_irpt-bckend-rt6_deploy_completion.md        CLOSED
      20260912T0856Z_irpt-bckend-rt6_deploy_completion.md        CLOSED
  [e.1] PASS      change-management entries for this cell, all CLOSED   denominator: 5 of 5
  [e.2] PASS      the cell's OPEN sentinel is absent (every entry closed and committed)
  [e.3] PASS      the APPLIED role carries this cell's four statements: DispatchTheDirectoryBuildToOneRunnerOnly, StartThatRunnerNeverStopIt, ReadBackTheCommandsThisFunctionSent, ListExactlyWhatItMayAlreadyRead   denominator: 4 of 4 (role holds 7 statements)
  [e.4] PASS      the role holds NONE of StopInstances / TerminateInstances / CancelCommand / PassRole   denominator: 0 of 10 actions are forbidden ones

==============================================================================
VERDICT
==============================================================================
  a.1    PASS      served CodeSha256 /qyUho5JNtliMMu79XjnVVsvl6Y2CAlfxEgPANXouJE= == source-map artifact_sha256
  a.2    PASS      dispatch configuration present on the SERVED function: IRPT_DIRECTORY_RUNNER_INSTANCE_ID, IRPT_D
  a.3    PASS      function Timeout 60s (send-and-return: unchanged from round 1)
  a.4    PASS      bundle uri: spec authority == terraform local == SERVED env  (s3://opal-data-mdpf/code/scripts/a
  a.5    PASS      SERVED manifests for 2026-09-11 carrying a real SSM dispatch fact
  a.6    PASS      schedule LIVE state ENABLED cron(0 9 ? * MON-FRI *) America/New_York, target irpt-directory-refr
  b.1    BLOCKED   firms with a landed directory artifact AND its pointer -- row IRPT_BCKEND-W2-S49: the runner hos
  c.1    PASS      the arms that can run read PAIRWISE DISTINCT envelope values: DIRECTORY_OVER_AGE, REFRESH_DISPAT
  c.2    BLOCKED   source completion and new revision cannot be driven on the REAL build path
  d.1    PASS      the runner's import check PASSES on the host, first-party modules printed: trading_calendar, ids
  d.2    PASS      host dependency versions printed by the run itself: boto3, pandas, pyarrow, jsonschema
  d.3    PASS      NEGATIVE CONTROL -- the SAME script on the SAME host with the 3-member bundle printed IMPORT-FAI
  d.4    BLOCKED   the build stops at a NAMED missing dependency -- row IRPT_BCKEND-W2-S51 enumerates all seven by 
  e.1    PASS      change-management entries for this cell, all CLOSED
  e.2    PASS      the cell's OPEN sentinel is absent (every entry closed and committed)
  e.3    PASS      the APPLIED role carries this cell's four statements: DispatchTheDirectoryBuildToOneRunnerOnly, 
  e.4    PASS      the role holds NONE of StopInstances / TerminateInstances / CancelCommand / PassRole

  PASS 14 | FAIL 0 | BLOCKED 3   denominator: 17 graded check(s)
  THE ACCEPTANCE TOKEN IS WITHHELD. 3 check(s) are BLOCKED on a premise this order cannot clear:
    IRPT_BCKEND-W2-S49  mdpf-daily-runner-ec2-role is AccessDenied on 5 of 9 source
                        prefixes and 3 of 3 firm destinations -- no build can land
    IRPT_BCKEND-W2-S51  the minted bundle cannot carry the seven repo files the
                        runner reaches, three of them per-firm runner_commons
  RT6-AC1 is FAIL. The order stays open.
```
