# TO-OS-s-25 -- THE DRIFT HALF ON DEMAND: what I measured

**Seat:** `0.7.0_AE_CloudOps~W` · **Order:** `NFRA_OUTSET.TO-OS-s-25`, amended @`a6be2b52dd`,
mechanism addendum @`77858dc2f8` · **Written:** 2026-09-10T00:45Z

**STATUS: O25-AC1 PASSES. rc=0, stdout ends `OS25-DRIFT-ON-DEMAND`, all six arms evaluated and
passed.** Arm (e) was unblocked by the OS-s-24 re-cut @`584003bcae` on the CTO's ruling 94820: the
00:29:57Z run IS the manual served day, and its own version of the 09-09 key is the acceptance
artifact.

---

## The headline

The drift task fired on demand, twice, and the second run is the one this order is graded on. The
first run published a correct artifact with a WRONG VINTAGE FIELD, which is what rows S28 and S29
came out of; the fix was ordered, made, and the re-run is clean.

| | first run | re-run (the accept's run) |
|---|---|---|
| `Start-ScheduledTask` | 2026-09-09T22:54:33Z | 2026-09-09T23:58:07Z |
| `LastTaskResult` | 0 | 0 |
| artifact VersionId | `sm4ktX4NckwQOXAzLELPJKqXz4_d5Tlv` | `3AE8of7Q44VkfbsNNpwWD0EH8lqPj.Sn` |
| `git_head` stamped | `4155c85a1f56` -- **the PARENT of the tree the rows were measured at** | `03e336fe54ee` -- the tree the rows were measured at |
| `git_head_moved` | field did not exist | **false** |

## O25-AC1, arm by arm

**Invocation:** `timeout 600 python org/missions/D11/NFRA/NFRA_OUTSET/deliverables/0.7.0_AE_CloudOps~W/test_os25_drift_on_demand.py`
**Expect:** `OS25-DRIFT-ON-DEMAND` · **Run 2026-09-10T00:36:48Z, rc=1** with exactly one arm
outstanding (e).

### (a) The configuration read -- rule (4)'s never-fired form. PASS

Captured ~2026-09-09T22:54:2xZ, BEFORE the first `Start-ScheduledTask`:

```
State              : Ready
Enabled            : True
Trigger            : MSFT_TaskDailyTrigger DaysInterval=1 StartBoundary=2026-09-09T07:30:00
Trigger in UTC     : 07:30 local == 11:30Z (America/New_York, -04:00 on this date)
NextRunTime  UTC   : 2026-09-10T11:30:00Z
LastRunTime        : 11/30/1999 00:00:00   (the never-fired sentinel)
LastTaskResult     : 267011                (SCHED_S_TASK_HAS_NOT_RUN -- 0 runs before)
NumberOfMissedRuns : 0
LogonType          : Interactive
StartWhenAvailable : True
ExecutionTimeLimit : PT1H
DisallowOnBatteries: False
```

⛔ **THIS ARM IS EVIDENCE OF RECORD AND IS DELIBERATELY NOT RE-DERIVED.** Once a task has fired,
`LastTaskResult` 267011 and `LastRunTime` 11/30/1999 cannot be produced again. A battery that
"re-read" them would be scoring a state it cannot represent. What IS re-derivable is checked live
and passes: the installed action string is BYTE-EQUAL to the line recorded at the pre-read.

### (b) The task's OWN accounting after the run. PASS

`LastTaskResult` **0**, `LastRunTime` **2026-09-09T23:58:07Z**, `MissedRuns` 0. The field
DISCRIMINATES rather than reading 0 from the prior run: it advanced from 22:54:34Z.

### (c) The artifact, and its `n` against the device. PASS

`LastModified` 2026-09-09T23:58:14Z, at/after the run start. `device` `laptop`. `publisher_arn`
`arn:aws:sts::313476888478:assumed-role/outset-drift-publisher-laptop/outset-drift-laptop`.
`tracked_total` 31,128 non-zero, which is what makes an `n` of 0 readable as QUIET rather than
OUT-OF-CORPUS. Internally `n` 153 = `n_modified` 3 + `n_untracked` 150 = `len(rows)` 153.
`git_head_pre` `03e336fe54ee` @23:58:08Z, `git_head` `03e336fe54ee` @23:58:11Z, `git_head_moved`
**false**.

⛔ **THE COUNTS MATCHED WHILE THE SETS DID NOT, AND THAT IS THE FINDING OF THIS ARM.** The artifact's
`n` is 153 and the device's live porcelain count is 153 -- but one path had LEFT the set and a
different one had JOINED it. A count-only check passes there and reports clean on a coincidence. The
battery compares SETS and attributes every difference:

| direction | path | attribution |
|---|---|---|
| left | `org/missions/D0/NFRA/NFRA_CLDGRPH/surprise-channel/investigations/INVESTIGATION_v1.md` | committed in `88091d4945`, after the artifact |
| joined | the battery's own file | mtime 2026-09-10T00:36:28Z, after the artifact's 23:58:09Z |

Zero unattributed. **An unattributed difference FAILS the arm** -- that is the control.

Also stated because it bit me: `git status --porcelain | wc -l` UNDERCOUNTS BY ONE when the final
line carries no trailing newline. The set comparison sidesteps the question entirely.

### (d) The identity plane -- AssumeRole, re-cut on row S29. PASS

AssumeRole **2026-09-09T23:58:09Z**, role `outset-drift-publisher-laptop`, `roleSessionName`
`outset-drift-laptop`, `assumedRoleUser.arn` byte-equal to the artifact's `publisher_arn`.
**DENOMINATOR 82 AssumeRole events across 2 pages**, exactly 1 matching. Bracketed: run start
23:58:07Z < assume 23:58:09Z < object 23:58:14Z.

This is the point of the re-cut: `publisher_arn` in the artifact is a SELF-REPORT, and CloudTrail's
AssumeRole record is an instrument INDEPENDENT of it. A copied `publisher_arn` could not produce a
matching AssumeRole at the right second.

**NEGATIVE CONTROL:** a bogus `roleSessionName` matches **0** of the same 82 events. A filter that
cannot return zero is a constant wearing a measurement's clothes.

### (d2) The object-level plane. COVERAGE-ABSENT, not NOT-YET

`COVERAGE-ABSENT: no data-event trail on opal-estate-report`. **DENOMINATOR: 2 trails, 0 CloudTrail
Lake event data stores**, read live. `opal-organization-trail`'s only data selector is `ReadOnly`
over `opal-data-bd/` and `opal-data-inf/`; `opal-served-key-write-trail`'s advanced selector names
three `platinum/firm/` prefixes. Neither mentions this bucket. Separately, `LookupEvents` serves
management events only and would not return a data event even for a covered key.

⛔ **RECORDED AS ABSENT COVERAGE, NEVER AS NOT-YET.** The original arm's only contemplated failure
mode was lag, and from a single read lag and absent coverage are indistinguishable. An arm whose
absence-handling is "record NOT-YET and re-read" would record NOT-YET forever, and NOT-YET reads to
every later seat as "coming" -- the more expensive of the two wrong answers. The battery re-reads
coverage LIVE, so if a selector is ever added the arm FAILS rather than keeping a stale line.

### (e) The negative arm from OS-s-24's manual served day. PASS

Read FROM OS-s-24's report, cited by key + VersionId, never re-derived:
`daily/2026/09/09/estate-report-2026-09-09.json` @ VersionId `F3CLuHhwgcRKo7OdbCdLbexIO6BUo3Mw`.

⛔ **THE VersionId IS THE WHOLE POINT AND `latest` WOULD HAVE BEEN A CLEAN WRONG READ.** That key's
`latest` is the restored 15:32:41Z pin, written by the SCHEDULE nine hours before this run. Reading
it would have returned a well-formed report with a laptop row in it and graded a different run
entirely. The report carries `run_bundle.trigger` `manual` and `run_id`
`a588a7ea-8ad2-4f03-a814-4f02668a66d6`, which is how the right version is known to be the right one.

The consumer's per-device composition, 3 device segments over a declared roster:

```
A_propagation@laptop: comp-heat drift produced 2026-09-09T23:58:09Z (tool vintage: none reported), age 0.6 h
site-z: UNREAD (s3://opal-estate-report/outset/site-z/comp_heat_drift.json)
_os22_probe_device: comp-heat drift (OS-s-22 PROBE FIXTURE) produced 2026-09-09T15:55:15Z (tool vintage: none reported), age 8.6 h
```

`ai.groups.A.stratum_status` = **OK**.

- **POSITIVE half:** `laptop` reads with **THIS run's** vintage, 2026-09-09T23:58:09Z at age 0.6 h.
  Not the 15:55Z hand publish, not the 22:54Z first run.
- **NEGATIVE half, and it must be a DIFFERENT device or the green means nothing:** `site-z` reads
  UNREAD. 1 of the 2 other rostered devices. Without it every device could be rendering from one
  blob and look identical.

The three devices sit in three different states and are **never summed**, which is the S23 ruling
working as intended.

⛔ **A FINDING INSIDE THIS PASS, filed as `NFRA_OUTSET-S36`:** site-z reads UNREAD because the
consumer got **AccessDenied**, not NoSuchKey, on a key that has simply never been published. The
runner role's only `ListBucket` statement is conditioned to `daily/*`, `manifest/*`, `code/*`, so
`outset/` is excluded and S3 masks a missing key as a permission failure. Group A survives it
because a failed read is SILENT **per device**; group B does not, because its source list is a
precedence chain that only ABSENCE advances. That is why group B is INSTRUMENT_FAILED on this same
report while group A is OK.

---

## Rows filed under this order

**`NFRA_OUTSET-S28`** (OBSERVATION, ARMED) @`b811fe7b91` -- the artifact's `git_head` named a
different commit than the rows beside it were measured at. Proven TWICE on different substrates: the
device's HEAD reflog, and -- independently of it -- the fact that the single file the child commit
added appears in ZERO of the artifact's 153 rows, which it could not do if HEAD had really been the
parent. The row named the `:96`-`:125` read-order gap as a CANDIDATE and REFUSED to assert it,
because the clock did not fit.

**The mechanism was closed by `2.0.0_SA_COO`, not by me, and it is worth carrying:** A REFLOG
TIMESTAMP IS THE COMMIT'S IDENT DATE, CAPTURED BY `git commit` BEFORE THE PRE-COMMIT HOOKS RUN. On
this estate's hook chain the ref moves up to ~15 s after its own stamp (measured: stamp 23:47:34Z,
ref move 23:47:49Z). So a reflog read places the move EARLIER than it happened, the window that
looked impossible was real, and the candidate mechanism was right. That trap is now in the code
comment beside the second HEAD read.

**`NFRA_OUTSET-S29`** (BLOCKING, ARMED) @`b811fe7b91` -- arm (d) read an instrument that does not
cover the key. RULED, REC (a) adopted: re-cut onto AssumeRole. REC (b), a data-event selector, was
NAMED AND NOT CUT -- a new billed AWS resource under Andrew's no-new-work word. **I did not add one**:
that is not an act to slip inside an accept.

## The fix, and its ledger

`infra/aws/ec2/outset-drift-device/publish_drift.py` now reads HEAD twice and stamps the SECOND
read; `git_head_pre`, `git_head_read_at`, `git_head_pre_read_at` and `git_head_moved` ride beside it.
**Stamp-and-flag, never refuse** -- the rows were never wrong, it was the VINTAGE that was wrong, and
refusing would discard a good measurement to punish a label.

Ledger `org/critical_paths/change_management/20260909T2355Z_outset-drift-publisher-git-head-read-order.md`,
OPEN @`03e336fe54` -> CLOSED @`3ea7ede8a7`. It recorded the refusal condition IN ADVANCE: if the two
reads agree with each other and still disagree with the rows, file a row and take NO third run. It
did not fire.

## O25-AC2 -- the never-fired schedule's history. NO VERDICT (CVO grades at L9)

- **Rule (4)'s form for this schedule** is the configuration read above plus the first fire recorded
  as history. The first SCHEDULED run is 2026-09-10T11:30:00Z; it is recorded as confirmation when
  it happens and is NEVER waited for.
- **The four local failure modes, as settled under TO-OS-s-21 and unchanged by this order:**
  (i) `LogonType` Interactive -- the task runs only while the user is logged on and does not wake the
  machine, but `StartWhenAvailable` true means it CATCHES UP when the laptop is next awake and
  logged on; (ii) `/ST 07:30` is local, so 11:30Z now and 12:30Z after the November clock change,
  both before 13:00Z; (iii) `ExecutionTimeLimit` PT1H kills a hung run so the next day's fire
  proceeds instead of being ignored; (iv) battery flags both false, so a run is neither refused nor
  stopped on battery. A day with no run at all still renders SILENT, which is the honest read.
- **There is no retry of a failed run** -- a failed run publishes nothing and the consumer's ceiling
  renders that device SILENT.
- **Does the on-demand run differ from the scheduled one in any observable?** It should not, and on
  the evidence it does not: same action string (byte-equal, checked live), same principal (the
  AssumeRole record names the same role and fixed session name), same key. The ONE observable
  difference is `LastTaskResult`/`LastRunTime` moving, which is the task's own accounting of any run
  whatever its origin. **The scheduled fire at 11:30Z will be the test of that claim**, and it is
  recorded as a prediction here, not as a result.

## Push state

**Not pushed by this seat** -- refused under this order's BOUNDS. Measured at 2026-09-10T00:09:52Z:
local commits `b811fe7b91`, `03e336fe54`, `3ea7ede8a7`, `adae68774f` are LOCAL; origin/CLOUD
@`c6bcb7b12b`.
