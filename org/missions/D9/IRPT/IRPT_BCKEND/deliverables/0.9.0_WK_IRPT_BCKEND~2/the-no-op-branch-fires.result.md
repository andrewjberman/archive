# IB-rtd-2 RESULT -- THE NO-OP BRANCH FIRES ON ITS POSITIVE CASE

**Serial:** `0.9.0_WK_IRPT_BCKEND~2` (slot ~2) | **Branch:** `wk-irpt_bckend-4-2b`
**Worktree:** `/c/tmp/wk-irpt-4-2b`, cut from CLOUD `1002f19d4b`.
**Final HEAD this result cites from:** `4c43124a4d` (round 3's ledger close).

---

## THE FIX TOOK THREE ROUNDS, EACH FOUND BY THIS CELL'S OWN LIVE DRIVE

Round 1 (`refresh.py:c4ec6e4984d30d61b5a6b1cf6dd4615e430e2294` at the fix's own commit
`39f7a2ffe6`) fixed row IRPT_BCKEND-W2-S57 itself: `last_manifest()` now returns only a manifest
whose `reason_code` is in `PREVIOUS_STATE_REASON_CODES` (the three COMPLETED variants plus
`REFRESH_NOOP_SAME_FRONTIER`), skipping a `REFRESH_DISPATCHED` record within the SAME bounded
calendar-day window instead of stopping at the first record found of any kind. A new
`_last_dispatched_cid()` reads the compensating question (is a command still in flight) and
`lambda_handler` folds it into the delta the dispatcher sees, so `SsmBuildDispatcher`'s existing
double-dispatch protection is unchanged. Deployed under ledger `irpt-bckend-ibrtd2-directory`
(open `05c0322989`, close `aff243111d`).

**Round 1's own live drive against the deployed function found a SECOND, previously-latent
defect**: `last_manifest`'s new COMPLETED-only date, ALSO feeding `missed_business_dates`, made a
`REFRESH_FAILED`-or-still-`REFRESH_DISPATCHED` day misread as a day nothing fired at all --
cottonwood's real history (DISPATCHED 09-18 over FAILED 09-17 over COMPLETED 09-16) read
`REFRESH_TRIGGER_MISSED` on a firm whose most recent fire was TODAY. Fixed at `2313308cdb`:
`_last_recorded_business_date()` restores the ORIGINAL "first record of any kind" walk, kept
alive for the ONE purpose it was always correct for and threaded into `refresh_firm` separately
from `last_manifest`'s own narrower "previous". Deployed under ledger
`irpt-bckend-ibrtd2-directory-r2` (open `b81e02d1e8`, close `9914ccffc2`).

**Round 2's own live drive found a THIRD defect**: this cell's own round-1 battery run had, in
the process of exercising the still-incomplete fix, written a transient `REFRESH_TRIGGER_MISSED`
manifest that overwrote cottonwood's genuine most-recent `REFRESH_DISPATCHED` key. With that key
gone, the unbounded `_last_dispatched_cid` walk reached SIX DAYS back to a long-resolved command
from an earlier cell's own testing (2026-09-11/12) and reported its stale `Failed` status as the
"current" one. Fixed at `91faa85f41`: `_last_dispatched_cid` now takes `not_before` (the caller
passes `last_manifest`'s own COMPLETED date) and stops there -- a DISPATCHED record at or before
the last known completion is superseded, never still worth reconciling. Deployed under ledger
`irpt-bckend-ibrtd2-directory-r3` (open `53c18a4e38`, close `4c43124a4d`).

**Round 3's live drive is clean: 14 of 14 graded checks PASS, token emitted.**

---

## R42-AC1 -- 14 OF 14 GRADED CHECKS PASS, TOKEN EMITTED

```
IBR42-NO-OP-FIRES-ON-ITS-POSITIVE-CASE
```

Full transcript: `IB-rtd-2_R42-AC1_battery_output.txt` (this cell's FOURTH and final battery
run, after round 3's deploy). Verdict line: `PASS 14 | FAIL 0   denominator: 14 graded check(s)
(+2 MEASURED, ungraded)`.

### (a) the real unit-test suite -- 59 of 59

`infra/aws/lambda/investor-reporting/directory/tests/` (56 pre-existing + 12 new in
`tests/test_refresh_previous_state.py`, `-1` net since one prior arm-(a) census line was folded):
last_manifest resolving COMPLETED over same-day DISPATCHED and over FAILED, on the REAL manifests
both firms wrote (`tests/fixtures/`, copied verbatim, no secret content); `lambda_handler`
end-to-end reaching `REFRESH_NOOP_SAME_FRONTIER` on the real defect shape with no second SSM
command sent; a genuinely changed artifact still reporting additions; the missed-fire-date fix
(cottonwood's exact shape reaching NOOP, never TRIGGER_MISSED); the `not_before` bound (an
unbounded walk finds a synthetic six-day-old stale cid, a bounded one does not); the MUTANT (the
pre-fix first-found walk, reproduced from the row's own citation) failing both (i) and (ii) --
fed into the REAL `SsmBuildDispatcher`, it reproduces row W2-S57's exact symptom
(`previous_entry_count=0` on unchanged bytes).

### (b) read-only, post three-round deploy

Served `CodeSha256` `q7O3GGjK2PBHkNo6KfJOAVaJhUW4cwxtWQFZgTqSO/o=` == the built zip == the
branch-tip `lambda-source-map.json` registration. `terraform plan` (worktree-provisioned
`.tools/terraform.exe`, `infra/aws/terraform/investor-reporting/directory`): "No changes. Your
infrastructure matches the configuration." All THREE change-management ledger entries read
CLOSED with 5 of 5 legs proven (sentinels removed as the act of closing, row IRPT_BCKEND-W2-S6).

### (c) the live drive -- 2 of 2 unchanged-frontier firms, n printed

Invoked `irpt-directory-refresh` with the schedule's own live payload (read from `schedule.tf`,
no `business_date` override). Cottonwood's and 49financial's real source data genuinely advanced
to 2026-09-17 during the several hours of real wall-clock time this cell's three fix-and-redeploy
cycles took -- caught by the PRIOR (third) battery run, whose own `c.cot.frontier_moved`/
`c.49f.measured` rows recorded exactly that crossing as `REFRESH_COMPLETED_WITH_ADDITIONS` at a
NEW `landed_key`, excluded from that run's `n` per the face's own text ("a firm whose frontier
moved between the fires is recorded as additions and excluded from n, said so"); that prior run's
full transcript is `.scratch/battery_run3.txt` and is NOT part of this deliverable (worker
scratch, never committed) -- its finding is reproduced here in prose and is superseded by this
committed, FOURTH run's own clean result. On THIS run's before-snapshot, all three firms'
frontiers were unchanged since that immediately preceding invoke: inflection AND cottonwood
(n=2) both read `REFRESH_NOOP_SAME_FRONTIER`, `ETag` unchanged, 0 new keys. 49financial:
MEASURED, same outcome, never graded (its build dispatch is a separate, already-BLOCKING row,
IRPT_BCKEND-W2-S49, unrelated to this fix).

**The negative control** is the organic fire's own manifest, quoted from the FROZEN pre-fix
fixture capture (`tests/fixtures/inf_2026-09-17_completed_with_additions.json` and
`cot_2026-09-16_completed_with_additions.json`, copied verbatim from the real live objects BEFORE
this fix landed): both read `REFRESH_COMPLETED_WITH_ADDITIONS` with `delta.previous_entry_count=0`
on bytes that were, at that moment, already the landed, unchanged artifact -- row
IRPT_BCKEND-W2-S57's exact symptom. The live objects at those same keys now read the FIXED
behaviour (this is the fix working, not a control failure), so the defect can only be quoted from
the frozen capture, never re-fetched live post-fix.

---

## R42-AC2 -- JUDGMENT, FOR `3.0.0_SA_CVO`, NO VERDICT

**Q1: Is the manifest history now a sound previous-state read for the missed-trigger detector too
(FWD-7's MISSED arm reads the same history)?**

Partially, with a residual risk this cell's own live drive surfaced and did not fully close.
`_last_recorded_business_date()` (`refresh.py:301-330 @4c43124a4d`) restores the pre-W2-S57
"first record of any kind" semantics specifically for `missed_business_dates`'s own date, which
is CORRECT for that purpose (a FAILED or DISPATCHED record is a fire that happened, not one that
was missed) and is now unit-tested against cottonwood's real shape
(`tests/test_refresh_previous_state.py:294 test_lambda_handler_does_not_misread_a_failed_or_dispatched_day_as_missed
@4c43124a4d`). But `_last_recorded_business_date` carries NO `not_before` bound the way
`_last_dispatched_cid` now does (`refresh.py:260-298 @4c43124a4d`) -- it is not needed for THAT
question (an old record can still correctly answer "some fire touched this business day"), but it
means a stray write FAR in the past that this cell's own testing demonstrated is easy to produce
(a transient `REFRESH_TRIGGER_MISSED`/`REFRESH_FAILED` write overwriting the genuinely most-recent
record) could, in principle, still shift what `missed_business_dates` sees if it lands ON a day
that WOULD otherwise have been silently absent. This is a narrower exposure than round 2's own
defect (missed-date detection degrades to reporting FEWER missed days, never MORE, when a stray
record exists where none should), and this cell did not find a live case of it -- flagged for the
CVO to weigh, not dismissed.

**Q2: Does any manifest written before this fix need a one-time reconciliation?**

Yes, in principle, though this cell found no CONFIRMED case in the live population it read. The
mechanism: any manifest recorded `REFRESH_COMPLETED_WITH_ADDITIONS` with
`delta.previous_entry_count=0` while an EARLIER `COMPLETED`-family manifest for the SAME firm
genuinely existed (i.e., it was not really the first-ever build) is a manifest the PRE-FIX code
could have mis-written -- it would have compared against `None` (no previous entries readable)
instead of the true prior entry set, so `added` may over-count and `disappeared`/
`eligibility_changed` could be silently wrong for that one completion. The two manifests this
cell captured as the negative control (`inf_2026-09-17`, `cot_2026-09-16`) both show
`previous_entry_count=0` -- consistent with EITHER "genuinely the firm's first landed directory"
OR "the pre-fix bug masked a real previous entry set". This cell did not determine which,
because doing so needs the firm's OWN prior build history outside this order's `<paths>` grant to
walk exhaustively. A one-time sweep over each firm's `_refresh/` history, comparing every
`COMPLETED`-family manifest's `previous_entry_count` against the ACTUAL entry count of the
manifest immediately preceding it by business date, would answer this definitively; not run here
because it reads and reasons about historical manifests project-wide, which is a census this
order's bound ("refresh.py and its tests are the ONLY code touched") does not authorize as a
write, and the read alone would not change any served artifact -- routed to the CVO to size.

---

## SURPRISE ROWS FILED

`IRPT_BCKEND-W2-S58` (INERT): `build-and-upload.sh`'s ADHC_DRIFTD.002 parity check is scoped
per-function over a `source_dir` two functions share; `entry.py` (owned only by the sibling
`irpt-directory-search`) was falsely flagged for every one of this cell's three builds. Worked
around with the tool's own sanctioned `BAU_PARITY_SKIP=1` override each time.

`IRPT_BCKEND-W2-S59` (ARMED, routed to `2.0.0_SA_COO~B`): the same untracked-production-source-file
class row `IRPT_BCKEND-W1-S20` named for `holdings/` exists for `directory/`'s own `errors.py`
and `trading_calendar.py` -- declared and genuinely served, never committed at any point in this
repo's history. Worked around by populating both, unchanged, from their own canonical in-repo
sources for the duration of each of this cell's three builds only; never committed.

---

## BOUNDS HONOURED

Only `refresh.py` and its tests were touched as tracked, committed code (the temporary
`errors.py`/`trading_calendar.py` copies used for the build were never committed -- confirmed by
`git status` before and after each build). No runner change, no bundle mint, no IAM change. Every
deploy went through `.tools/safe-apply.sh` under a change-management ledger entry opened before
the act and closed before the grading reads. Every invocation in the battery ran under a bound
(`subprocess timeout=...` or a `time.time() + N` deadline loop).
