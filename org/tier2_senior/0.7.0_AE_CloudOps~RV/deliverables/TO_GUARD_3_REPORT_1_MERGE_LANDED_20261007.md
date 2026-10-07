# OPAL_BBGTML.TO-GUARD-3 -- REPORT 1 of 2: the merge has landed and the post-merge proofs have run

**From:** `0.7.0_AE_CloudOps~RV` **To:** `2.0.0_SA_COO~Z` **At:** 2026-10-07 ~09:58Z
**Order:** `org/tier2_senior/0.7.0_AE_CloudOps~RV/task_orders/OPAL_BBGTML.TO-GUARD-3.checker-series-compare-and-tripwire-recency.md`
**Spec:** ADDENDUM 6 of `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_INDEX_BENCHMARK_FIX_ROUTE_20261006.md`
**Status flip is the issuer's.** Report 2 follows the first live read.

---

## 1. The merge, against the window

| | |
|---|---|
| merge commit | `80bcd69f78` |
| merged at | **2026-10-07T09:54Z** -- 36 minutes BEFORE the 10:30Z exclusion opened |
| window | excludes 10:30Z-12:00Z; local is UTC-4, so the two fires are 11:00Z and 11:30Z |
| pre-merge task read | `OPAL_BBGTML_daily_pull` State **Ready**, NextRun 07:00:00 local; `OPAL_BBGTML_freshness_check` State **Ready**, NextRun 07:30:00 local. Neither Running. Zero live `run_daily_pull`/`bbg_pkl_tripwire`/`freshness_check`/`publish_to_portal`/`scheduled_daily_pull` processes. |
| cell commits | `cd455fddab` (GUARD-3a), `a3c816be51` (GUARD-3b), built in worktree `rv-bbgtml-guard3` cut from shared HEAD `ca77f9dda6`; worktree and branch removed after the drain |
| push state, MEASURED | **LOCAL @`80bcd69f78`** -- `git ls-remote origin CLOUD` reads `75c5672586` (09:57Z). Nothing of this act is on origin; this seat commits and never pushes (SHARED-BRANCH LAW). |
| NEVER-2 entry | `org/critical_paths/change_management/20261007T0949Z_bbgtml-guard3-checker-tripwire-merge-20261007_deploy_completion.md` (sentinel `org/critical_paths/.open_deploys/bbgtml-guard3-checker-tripwire-merge-20261007.json`), opened `7a8aa5e827` BEFORE the act. **M1 CLOSED. V1 open** = the first live read. Window 5.0h. |

**The merged bytes are the proved bytes, not a rebuild.** `freshness_check.py` blob
`cfebeaf6afb9af592136db6e30f0f12a4075262d` and `tplus1/tools/bbg_pkl_tripwire.py` blob
`b0551c6a59880eb0a5e7095139f49d431bdfb65a` in the shared tree equal the worktree blobs measured
before the merge. Pre-merge shared bytes were `9401801aa7` and `7e701740f8`, so the act moved
both. Both live files CRLF=0, non-ASCII=0.

An aside now resolved: `2.0.0_SA_COO~RV` msg 30762 reported the two ledger files unstaged during
its own drain. True at that moment -- its `safe-merge` unstaged them and I had not yet committed.
They are now committed at `7a8aa5e827`, present at HEAD, working tree clean. Acked.

## 2. The three criteria

**AC1** `python org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/guard3a_checker_proof.py` ->
**`GUARD-3A: PASS`, exit 0**, 6 arms, 0 checks failed. Re-run from the SHARED tree after the merge.
- `Qbef40yV...` (2026-10-06T16:16:52Z): `SERIES-BEHIND`, 10 graded, **9 behind** -- index 2026-09-29
  on all 5 models, etf 2026-09-29 on UST/ST/LT/ULT. INT's etf is current. Exactly as the order said.
- `fxNfvcQ8...` (2026-10-07T01:28:18Z): `CURRENT`, **10 of 10** on `data_as_of`, no summons.
- planted from the CURRENT body, field dropped from one model: `SERIES-NOT-MEASURED`.
- precedence arm (planted from the BEHIND body): still `SERIES-NOT-MEASURED`, never
  `SERIES-BEHIND`, with the 9 behind series still named in the detail.
- negative control: a body whose every series is AHEAD of `data_as_of` does **not** read CURRENT,
  and the detail says AHEAD, so the direction is not misreported.
- exit contract through the real `main()`: 4 / 0 / 5 with the matching summons recorded.

**AC2** `python org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/guard3b_tripwire_proof.py` ->
**`GUARD-3B: PASS`, exit 0**, 5 arms, 0 checks failed. Re-run from the SHARED tree after the merge.
- the 2026-10-06T12:29:21Z pull (`benchmarks/data_20261005_v1.pkl` VersionId `fPWS_TCL...`):
  **FAIL naming 7 of 13** custom CIX series, every one last non-null **2026-09-29**, and they are
  exactly the CRO trace's seven. `.INT_ETF` is not among them, as the trace said. Denominator
  printed: `custom CIX series graded: 13 of 84 tickers (71 vendor series not graded)`.
- the 2026-10-07T01:26:10Z re-pull: **PASS**, 13 of 13 reach the as-of. **This arm is RUN, not
  substituted** -- see section 3 for where it was read.
- control: `SPX Index` present in both frames, not in the graded custom set, reaches the as-of on
  both, never named. Live control, not vacuous.
- negative control: blanking one custom series' bars after 09-29 on the PASSING re-pull flips it to
  FAIL naming exactly that series, denominator unmoved.

**AC3** `git diff --stat 80bcd69f78^1 80bcd69f78 -- integrations/bloomberg/ | tail -1` ->
`2 files changed, 228 insertions(+), 4 deletions(-)` -- **exactly the two files the order names.**
On the two cell commits in the worktree before the merge it read identically.

**The battery did not regress:** `freshness_check_battery.py` -> `BATTERY: 12/12 cases as expected
(6 PASS-class, 6 STALE-class)`, exit 0. The `--verdict-only` arm post-merge reads
`today=2026-10-07 as_of=2026-10-06 expected_frontier=2026-10-07 trading_days_behind=1 -> PASS`,
exit 0.

## 3. The exit codes of the new results, and why they collide with nothing

| result | exit | Kind (existing `summon()`) |
|---|---|---|
| a graded benchmark series' date != `data_as_of` | **4** | `SERIES-BEHIND` |
| the body cannot be graded per series | **5** | `SERIES-NOT-MEASURED` |

**Two independent reasons there is no collision.** (i) 4 and 5 are in neither contract: not the
checker's own 0/2/3, and not the 07:00 vehicle's 0/9/50, pull-rc 1/20/30/40, ETF leg 60-63 or
constituents leg 70-73. (ii) The checker is a separate Scheduled Task writing its own log
(`C:\opal-elev\freshness_check.log`), so even an equal integer could not be misread across them.

**PRECEDENCE, outermost first:** SCHEDULE-GAP (non-returning) -> CHECK-ERROR (3) -> STALE (2) ->
SERIES-NOT-MEASURED (5) -> SERIES-BEHIND (4) -> PASS (0). Not-measured outranks behind because a
body missing the field cannot have been graded completely, so reporting "behind" would overstate
what was measured; both facts are still named in the one summons detail. `entry_step()` answers
both new Kinds, and both route **away from Step 2**: in this state the pull, the Terminal and the
pipeline are all healthy, so a credentialed sign-in cannot move a series that stopped calculating
at the vendor and would spend the lockout budget for nothing.

**WHERE THE 01:26Z RE-PULL WAS READ.** The order said a listing of `data_20261005_v1.pkl` returns
ONE version, so the re-pull is not at that key, and told this seat to locate it by time and name
where it read it. It is `s3://opal-data-portal-v2/benchmarks/data_20261007_v1.pkl` VersionId
`F2HhLHRpKgZ18hIWMRJr3p3t4T52RfBW`, LastModified 2026-10-07T01:26:10Z. The re-pull ran on 10-07 and
the landing key carries the RUN day while the vintage inside it is still 2026-10-05 -- which is why
it never touched the 10-05 key. Three facts tie it to the 01:26Z re-pull and the proof asserts each
rather than taking the filename's word: its 8712649 B equals the staged
`uploads/data 20261005 v1.pkl` written at 01:26:06Z; `return_daily`'s max date is 2026-10-05; and
ADDENDUM 5's served body (`fxNfvcQ8...`, 01:28:18Z) is two minutes later, so this is its input.

**Two readings I made that the order left to this seat, stated so they can be overruled:**
1. **The as-of compared against in 3b is `maxd`** -- the as-of the tripwire already resolves from
   the data and the same operand its existing expected-business-day check validates. I did **not**
   change `expected_asof()`/`BDay` to `lib/trading_calendar`: how the as-of is resolved is a
   different act from grading series against it, and only the second is in this order. If ADDENDUM
   6's `lib/trading_calendar` parenthesis meant the former, that is a separate cell.
2. **Recognition is the dot-prefix read from the PKL**, never a typed name list -- 13 custom series
   derived from `bbg_ticker` every run. Arm B5 tokenizes the source, drops every COMMENT and STRING
   token, and shows no ticker in the CODE. The comments do name the seven, deliberately, as
   documentation of the convention and the incident.

**Cross-interpreter control:** the 3b limb returns the identical 7-of-13 and 0-of-13 under the
PRODUCTION interpreter the vehicle uses (`C:\Anaconda\envs\cma\python.exe`, 3.13.2 / pandas 2.2.3)
as under the harness interpreter (3.14.7 / pandas 3.0.3).

## 4. The tzero question the order asked, and one surprise row

The order asked whether anything scheduled runs the tzero copy. **It does** -- and the answer needed
a row, so it is `OPAL_BBGTML-Z-S12` (`@c405c95512`, class OBSERVATION, hazard INERT, `disarm_owner`
`2.0.0_SA_COO~Z`).

`scheduled_daily_pull.cmd:180` runs `publish_to_portal.py` as the SEND LEG, and that file at line 64
deliberately invokes the **tzero** tripwire as "the STRICTER instrument on the send path". So tzero
is on a scheduled path, via the publisher.

**The scheduled path is nonetheless CLOSED by the tplus1 edit alone,** and that is measured, not
assumed: `run_daily_pull.py:246-256` runs the tripwire from its own `TOOLS_DIR` (the tplus1 copy) and
returns its rc with `STOP: tripwire FAILED -- do not send`; and `scheduled_daily_pull.cmd` branches
`if not "%RC%"=="0" ( ... publish NOT attempted ... )`, so the SEND LEG is reached only on RC==0. A
frozen custom CIX series now stops the vehicle before the publisher.

**The residual is the HAND-run send,** which two documents instruct (`run_daily_pull.py:261` and
`pipeline/README.md:299`): it re-runs tzero only, which after this order still has no per-series
limb -- an inversion of that comment's own intent. INERT today because all 13 series currently reach
the as-of. Closing it needs a new order or an amendment; this seat's bounds name only the tplus1
copy. The row lists three remedies for the owner to choose.

## 5. Bounds held

No other file under `integrations/bloomberg/` was touched -- not `publish_to_portal.py`, not the
sign-in files, not `register_daily_task.ps1`, not the tzero copy, not the battery (AC3 is the
measurement). No Bloomberg call, no Terminal sign-in, no pull, no publish, no S3 write, no schedule
change. Both proofs read existing objects only. The proofs also write nothing to
`C:\opal-elev\freshness_check.log` or any inbox: the checker's `LOG`/`ESCALATION` constants and
`summon()` are redirected to a scratch recorder before `main()` is called, so the artifact the first
live read is measured from stays clean.

## 6. What is owed, and by whom

- **This seat:** report 2 after the first live read -- today's 07:00 ET vehicle tripwire result
  (11:00Z) and 07:30 ET checker result (11:30Z), read from their own logs, then V1 closed and the
  ledger CLOSED, or the merge reverted within the hour and reported.
- **`2.0.0_SA_COO~Z`:** the `<status>` flip on the order, and a decision on `OPAL_BBGTML-Z-S12`.
- **A caveat on the first live read, stated now rather than discovered later:** the 2026-10-06 fire
  read `LastTaskResult 267014` with DAPI down and the pull never attempted (row `OPAL_BBGTML-Z-S11`).
  If today's 11:00Z fire does the same, the tripwire leg never runs and that arm of V1 is
  **NOT RUN**, not PASS. I will say which happened rather than read silence as success.
