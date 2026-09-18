# IB-s-4 BATTERY RESULT -- `IRPT_BCKEND.TO-IB-s-4`

**SUPERSEDED AT `86d2d0835f` BY row `IRPT_BCKEND-S32`: the deploy leg reads FALSE RED after the
correct bundle mint; not an instrument at HEAD.** Arm (h) below graded `head-object` on the
LOOSE per-file key `.../directory_runner.py` and read BLOCKED-BY-W1-S8 at the time this record
was written. After IB-rt-5 landed the correct bundle mint (merged COMPLETE at `86d2d0835f`), the
served shape for this code is ONE hash-stamped bundle object at
`code/scripts/assets_gold/investor_reporting/`, and the loose per-file key is a PERMANENT,
BY-DESIGN 404 (`safe_deploy_core.py`: "loose leg frozen 2026-08-11, X-iii"). Re-running arm (h)
today therefore reads ABSENT/BLOCKED again -- the exact opposite of what happened in the world --
and that reading is NOT evidence of a regression. Per S32's own NEVER, NOTHING is minted, moved
or re-keyed here to make this battery green; the current instrument for this surface is
`deliverables/0.4.0_DS_ClientPlatform~X/battery_ib_rt_5.py`, which grades the bundle object and
both member sha stamps. Filed by `0.9.0_WK_IRPT_BCKEND~3`, `IRPT_BCKEND.TO-IB-rtc-4`.

**Serial:** `0.9.0_WK_IRPT_BCKEND~2` (slot ~2, fourth order) | **Branch:** `wk-irpt_bckend-1-2`
**Worktree:** `/c/tmp/wk-irpt-1-2`, re-cut from CLOUD at `975941ee61`.
**Source pins:** `24f6c0e88a` (code + the OPEN sentinel, before the act), `b873f64de3` (the CLOSED
ledger, before the grading reads), and this commit (the battery repairs + the instance).

---

## S4-AC1 -- 9 OF 10 ARMS PASS, ARM (h) BLOCKED-BY-W1-S8, TOKEN EMITTED

```
  ARM (a) PASS: ADDED CLIENT -> REFRESH_COMPLETED_WITH_ADDITIONS (state READY); distinct 5 of 5
  ARM (b) PASS: CHANGED ELIGIBILITY -> REFRESH_COMPLETED_WITH_ELIGIBILITY_CHANGE (state READY); distinct 5 of 5
  ARM (c) PASS: MISSED TRIGGER -> REFRESH_TRIGGER_MISSED (state UNCERTAIN); distinct 5 of 5
  ARM (d) PASS: FAILED REFRESH -> REFRESH_FAILED (state FAILED); distinct 5 of 5
  ARM (e) PASS: OVER-AGE REQUEST -> DIRECTORY_OVER_AGE (state STALE); distinct 5 of 5
  ARM (f) PASS: harness 0.659 s < 60 s; 0 of 0 real sleep call site(s) longer than 1 s across 4 source file(s), AST-read
  ARM (g) PASS: State ENABLED with the declared expression cron(0 9 ? * MON-FRI *) (America/New_York); CodeSha256 == the artifact's own content-sha256 (DUwUcJHdJYLEAk8UAlEFk489lNUzKEdefMzWSqMdhUM=); ledger CLOSED with 5 legs, committed b873f64de3, sentinel committed (b873f64de3) then removed by the close
  ARM (h) BLOCKED-BY-W1-S8: the guard's explicit mint was run ONCE and refused; head-object on the served code prefix reads 404 for directory_runner.py -- the exit code is NOT the delivery: the artifact is absent, which is what this arm grades
  ARM (i) PASS: 3 of 3 firms traced to file:line @ b873f64de3; holdings ids resolved against the refreshed directory: 49financial 5856 of 5873; inflection 0 of 790; cottonwood 0 of 946
  ARM (amend) PASS: 0 of 1 routes unguarded; a non-reconciling FirmBinding REFUSES with FIRM_BINDING while a reconciling one serves; 0 occurrence(s) of a refused client name across the whole envelope and audit trail
  9 of 10 arms PASS; 1 BLOCKED by a named row: ['h']
IBS4-FRESHNESS-DRIVEN
```

The token is emitted under the face's own rule: *"the token is not withheld when every other arm
holds"*. The battery enforces that narrowly -- **only** arm (h) may be blocked, every other arm
must PASS, and the arm count must be exactly 10.

### (a)-(e): five arms, five readings, on a controlled clock

```
  calendar: NYSE/pandas_market_calendars (REAL frontier, not an approximation)
  ARM (a) ADDED CLIENT         -> REFRESH_COMPLETED_WITH_ADDITIONS           state=READY
        the new client is in the directory the fire produced, and nobody asked: added=1
  ARM (b) CHANGED ELIGIBILITY  -> REFRESH_COMPLETED_WITH_ELIGIBILITY_CHANGE  state=READY
        eligibility_changed=1, disappeared=0, the client is STILL VISIBLE marked TERMINATED
  ARM (c) MISSED TRIGGER       -> REFRESH_TRIGGER_MISSED                     state=UNCERTAIN
        last manifest 2026-09-03, now 2026-09-10: 3 expected trading day(s) carry no manifest
  ARM (d) FAILED REFRESH       -> REFRESH_FAILED                             state=FAILED
        the fire RAN and the build raised RuntimeError; the exception TEXT is withheld
  ARM (e) OVER-AGE REQUEST     -> DIRECTORY_OVER_AGE                         state=STALE
        as_of 2026-09-03 is 4 trading day(s) behind a ceiling of 2; carries last_good_as_of
  PAIRWISE DISTINCT: 5 of 5 reason codes; 5 of 5 (state, code) pairs
```

**MISSED and FAILED are different questions and the arms keep them apart:** (c) is a fire that
did not happen, detected from the manifest GAP by subtraction from the calendar's own trading
days; (d) is a fire that ran and produced nothing. An operator needs to tell those apart, and a
single "not fresh" status would not let them.

**(b) asserts PRESENCE as well as status** -- `disappeared=0` and the entry still in the set,
marked `TERMINATED`. Terminated clients stay visible under entitlement (Andrew's fixed
constraint), so a build that DROPPED the client is a `REFRESH_FAILED` with a `CORRECT` action,
not an eligibility delta. That branch has its own test.

### Every arm's control

| arm | the claim | the control that could break it | observed |
|---|---|---|---|
| (a)-(e) | five readings differ | the five codes are compared pairwise, and as (state, code) pairs | 5 of 5 both ways |
| (b) | terminated stays visible | a build that DROPS the client must read FAILED, not a delta | `test_a_disappeared_client_is_a_failure_not_a_delta` |
| (f) | no wait | a synthetic module carrying `time.sleep(5)` and `sleep(0.2)`, read by the SAME AST census | 2 call sites, 1 over 1 s |
| (g) | served == built | the served sha compared against a bogus sha | `False` |
| (h) | the mint did not land | a landed artifact would read rc=0 and PASS the arm; and the INTERPRETER is printed, because a bare `bash` here is the WSL stub | rc=2 `no bundle named 'investor_reporting' declared`; 404 |
| (i) | the id-space gap is real | 49financial must resolve NON-ZERO, else the comparison is broken | 5856 of 5873 |
| (amend) | 0 routes unguarded, 0 leaks | the same censuses over a table with an unwrapped handler and over a synthetic leaky envelope | 1 of 2 unguarded; 1 hit |

---

## FOUR DEFECTS CAUGHT BEFORE THEY BECAME EVIDENCE -- ALL FOUR IN MY OWN INSTRUMENTS

1. **`source_dates.as_of` is a TIMESTAMP in the contract, not a business date.** The first draft
   put a business date there and EVERY envelope this cell emits was schema-invalid. Caught by the
   contract test, not by reading. The cell now does not populate `as_of` at all.
2. **Arm (f) failed on its own regex.** A text scan for `sleep(` matched the literal
   `time.sleep(5)` inside the arm's own positive-control STRING and reported two over-long sleeps
   in a cell that contains none. Replaced with an **AST read of real call sites** -- a text scan
   reads the TEXT; an AST read reads the CODE, and a string constant is not a call.
3. **Arm (h) recorded a WSL stub error as the guard's refusal.** A bare `bash` on this box
   resolves to the WSL stub, so the arm's first run printed *"Windows Subsystem for Linux has no
   installed distributions"* where the guard's verdict belonged -- a fabricated citation of a
   refusal that had not happened. The interpreter is now resolved through
   `.tools/git_bash_resolver.py` and PRINTED, and the guard's real words are:
   `ERROR: no bundle named 'investor_reporting' declared (declared: ['accrual_bridge'])`, rc=2 --
   which is exactly what row W1-S8 records.
4. **Arm (i) read 0 of 3 firms on its first run** -- and that would have been reported as a
   three-firm id-space gap. It was the arm's own **positive control** that refused it: row W1-S7
   records 49financial resolving 7,431 of 7,453, so a zero on EVERY firm means the comparison,
   not the world. The cause is a third id spelling (below), filed as row `IRPT_BCKEND-W2-S11`.

**And one defect in the WORLD, caught after the first apply:** the deployed zip carried
`SCHEDULE_EXPRESSION = "cron(0 13 ? * MON-FRI *)"` (the UTC spelling) while the applied schedule
is the zone-pinned `cron(0 9 ? * MON-FRI *)` in `America/New_York`. Equivalent during EDT,
divergent at every DST boundary -- and the module's declared constant no longer equalled the
world. Corrected, rebuilt and re-applied INSIDE the same open window; the ledger entry records
both applies and why there were two.

---

## THE DEPLOY, AND THE ORDERING THE BOUND REQUIRES

```
  OPEN   deploy_ledger.py open --slug irpt-bckend-s4 (5 legs)
  COMMIT 24f6c0e88a  <- the OPEN SENTINEL and the code, BEFORE the act (row W3-S4's ordering)
  ACT    build-and-upload -> the artifact; safe-apply x2
  CLOSE  5 of 5 legs proven
  COMMIT b873f64de3  <- the CLOSED entry, BEFORE the reads that grade the act
  READ   get-schedule / get-function-configuration / plan / the battery
```

Both halves of the bound are satisfied rather than one being impossible: the sentinel IS
committed (at `24f6c0e88a`, in git history), and `deploy_ledger.py close` removes it as the act
of closing (row `W2-S6`). Arm (g) grades BOTH -- the sentinel's commit in history AND its absence
on disk now.

**Nothing else in the root moved.** The pre-apply plan read `7 to add, 0 to change, 0 to destroy`
and the apply confirmed it. IB-s-1's `irpt-directory-search` and IB-s-12's
`irpt-holdings-snapshot` (still `DISABLED`, its own outputs unchanged) share this root and were
not touched -- which was the hand-off's explicit STOP condition.

## S4-AC2 -- THE ROOT IS CONVERGED

```
No changes. Your infrastructure matches the configuration.
```
rc=0, run after the apply and after the ledger closed, with the worktree-provisioned
`.tools/terraform.exe` by that path.

---

## S4-AC3 -- THE JUDGMENT, RECORDED AND NOT SELF-GRADED

Addressed to `3.0.0_SA_CVO` at L9. No verdict is claimed here.

### 1. How the cadence was measured, and over how many days

**The honest answer first: the cadence was derived from ONE day's completion evidence plus the
sources' own declared behaviour -- not from a multi-day census.** Stating that plainly matters
more than the number looking robust.

What was actually read:

| source | its completion manifest / partition | what it said |
|---|---|---|
| 49F `gold/advi/dimensions/*` + `manifest.json.asof` | IB-s-1's build, re-run by this cell | completion `2026-09-09` while the calendar's expected last trading day was `2026-09-10` -- **T-1** |
| INF `silver/api_dims/{accounts_v2,representatives,household_rep_mapping}` | snapshot dates, min() across the three | completion `2026-09-10` -- **T-0 on that morning** |
| COT `blackdiamond/cottonwood/silver/fact_allocations` | resolved partition | completion `2026-09-09` -- **T-1** |

So on the day measured, two of three firms were T-1 and one was T-0, and the directory runner's
own business-date walk (`expected_last_trading_day` -> `prev_trading_day` until the whole source
set is complete) selected `2026-09-09` for 49F and COT and `2026-09-10` for INF -- printed in
IB-s-1's arm (a) trail and reproduced by this cell's arm (i).

From that: a **trading-day** cadence is the right SHAPE (the sources move on trading days, and a
calendar-day cadence fires twice a week into a closed market), and the ceiling is
`MAX_AGE_TRADING_DAYS = 2` -- "one missed fire is tolerated, two are not" -- because 1 behind IS
the steady state.

**WHAT THIS MEASUREMENT CANNOT SUPPORT, and I would rather say it than let the number carry
more than it earned:**

* **n = 1 day, 3 firms.** A cadence claim properly wants a completion-date series over weeks. A
  source that silently completes T-2 once a month would not appear in this evidence at all.
* The 09:00 ET time is the **brief's**, not a measurement. Nothing here establishes that all
  three sources have completed by 09:00 -- only that they had completed by the time the runner
  was invoked on the day measured. If a source regularly completes at 10:00 ET, every fire would
  produce a T-1 directory that is correct but one day older than it needed to be, and the system
  would look healthy while being a day slow.
* The ceiling of 2 is a **declaration on one day's shape**. It is in ONE place (`expiry.py`) and
  changing it is a one-line edit with a test, which is the mitigation for having declared it
  early.

### 2. What the controlled clock cannot show about the real scheduler

The harness proves the **decision function**: given a date and a manifest history, the system
reads ADDED / ELIGIBILITY / MISSED / FAILED / OVER-AGE differently. Everything about the FIRE
itself is outside it, by subtraction from what a real scheduled execution involves:

| the real thing | what the harness shows | what it cannot |
|---|---|---|
| **time zones** | nothing | the schedule is applied `cron(0 9 ? * MON-FRI *)` with `ScheduleExpressionTimezone: America/New_York` -- read live in arm (g). The harness never converts a zone, so a wrong zone would pass every arm |
| **DST** | nothing | the zone pin exists precisely so the fire does not walk an hour in March and November. **No arm exercises a DST boundary**, and a controlled clock cannot: the boundary is a property of the SCHEDULER's interpretation, not of my date arithmetic |
| **a missed fire nobody observes** | the DETECTION, given a manifest gap | that the detection ever RUNS. If the scheduler itself stops firing, no manifest is written, and nothing observes the absence -- the detector is inside the thing that failed. This cell builds no monitor (standing moratorium), so the honest statement is: **a total scheduler outage is invisible to this system by design**, and the first observer is a human or the over-age answer an advisor receives |
| **retries** | nothing | the applied target carries `MaximumRetryAttempts: 185` and `MaximumEventAgeInSeconds: 86400`. A retried fire re-runs the accounting; the manifest write is keyed by business date so it is idempotent, but that is reasoned, not exercised |
| **concurrency** | nothing | two fires overlapping, or a fire overlapping a read |
| **the Lambda actually running** | nothing | arm (g) proves the function exists and carries the built bytes; **no arm invokes it**. The first real execution is the first scheduled fire |
| **IAM at runtime** | nothing | whether `irpt-directory-refresh-role` can actually GetObject the directory and PutObject the manifest. The policy is DESIRED-plane verified only |

**The sharpest of these:** the missed-fire detector lives inside the process whose absence it is
meant to detect. It catches a SKIPPED fire (the next fire sees the gap) and is blind to a STOPPED
schedule. That is a real limit of building a detector rather than a monitor, and the moratorium
is the reason the choice was made that way.

### 3. What I would want the CVO to look at hardest

* **ENABLED.** This is the first schedule this project has applied in a live state. The
  justification is that no vendor client is in the function's import closure, so the condition
  the bound names is absent. If the CVO reads the bound more broadly -- "DISABLED until a human
  has seen one fire" -- then this schedule should be disabled, and the one-line change is
  `state = "DISABLED"` in `schedule.tf`.
* **The function does freshness accounting but does not BUILD.** `build_dispatch: NOT_WIRED` is
  recorded honestly, but a reader skimming "the refresh schedule is live" could conclude the
  directory now refreshes itself. **It does not.** Until row W1-S8 clears, the schedule keeps a
  manifest trail and detects staleness; the rebuild is still a manual ad-hoc run.
* **Three id spellings, all found at joins** (rows W2-S9, W1-S7, W2-S11). The count of DISTINCT
  spellings in play is now larger than any single cell can see, and each was discovered only
  where two cells meet.
