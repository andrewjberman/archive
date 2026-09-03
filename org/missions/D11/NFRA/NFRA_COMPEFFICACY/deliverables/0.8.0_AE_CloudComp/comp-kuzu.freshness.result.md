# comp-kuzu freshness layer -- NFRA_COMPEFFICACY per-cell result (TO-CE-G-5, T-16 shape for the applicable fields)

Cell: `CE-g-5` (decomp v0.2 @`f54000091d`). Engine: `infra/aws/globgrph/_canonical.py` +
`infra/aws/globgrph/kuzu_cli.py`. Measured by `0.8.0_AE_CloudComp`, 2026-09-03T04:47Z-05:11Z,
read-vintage HEAD @`f659b4edd2` (issuance), engine @ this cell's own commit (cited below). Every
value is MEASURED on this box unless its own field says otherwise.

```json
{
  "schema": "NFRA_COMPEFFICACY_PRD v0.4 s.4 (fields that apply to an engine-layer fix, per the TO's own instruction)",
  "cell": "CE-g-5",
  "measured_by": "0.8.0_AE_CloudComp",
  "measured_at_utc": "2026-09-03T04:47Z..05:11Z",
  "read_vintage": "HEAD @f659b4edd2 (issuance); fix committed this cell",

  "identity": {
    "engine_path": "infra/aws/globgrph/_canonical.py (746 lines after this cell) + infra/aws/globgrph/kuzu_cli.py (189 lines) -- the freshness layer comp-find's --corpus aws pull sits on top of, never modified until this cell",
    "the_defect_object": "infra/aws/globgrph/_canonical.py:ensure_fresh() (:600, pre-cell) + the three rebuild-subprocess call sites (_default_rebuild, _incremental_or_full_rebuild, _incremental_or_serve_stale)"
  },

  "fix_a_no_orphan": {
    "design_chosen": "Windows Job Object (JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE), stated in the new _run_child_supervised() docstring; POSIX process-group (start_new_session + killpg) as the parallel path, same function, platform-branched -- ONE of the two per the TO's own instruction (not both duplicated as separate mechanisms; both live in one function because the choice is made at the OS-detection line, not by the caller)",
    "mechanism": "the rebuild child (kuzu_nessie_load.py / kuzu_incremental_refresh.py) is assigned to a job with kill-on-close BEFORE this process (kuzu_cli.py) does anything else with it; if THIS process is torn down for any reason -- including an external TerminateProcess this code never gets to react to -- the OS closes this process's handles, including the job handle, and closing a kill-on-close job's LAST handle terminates every process still assigned to it. No cooperation from the dying process is required or assumed.",
    "validated_standalone_before_wiring_in": "a throwaway parent/child pair (not this engine) was built, run, and killed via PowerShell Stop-Process -Force on the LIVE Win32 pid; the grandchild was confirmed DEAD after the kill, before this mechanism was wired into _canonical.py at all -- so the production wiring is an application of an already-proven primitive, not an untested one",
    "measured_in_production": "battery arm G5-AC1-NO-ORPHAN: a real wrapper subprocess (calling the SHIPPED _run_child_supervised, imported from the real _canonical.py) spawns a grandchild that writes its own pid then sleeps 90s; the wrapper is killed externally via proc.kill() (the same act comp-find performs on kuzu_cli.py) well before either the grandchild's sleep or the supervised call's own 90s timeout could fire; the grandchild's pid is read from the OS process table (tasklist, not this process's own bookkeeping) after the kill -- NOT alive. PASS.",
    "mutant_result": "G5-AC1-MUTANT-STILL-ORPHANS: the identical exercise against an UNSUPERVISED spawn (bare subprocess.Popen, the pre-fix shape) shows the grandchild pid STILL ALIVE after the parent's kill -- the arm correctly reds on the old behavior, proving it is a live control, not a tautology. PASS (the mutant is RED as required)."
  },

  "fix_b_serve_stale_immediately": {
    "design": "ensure_fresh() gained a wait_for_peer parameter (default True, unchanged back-compat for --mode full/auto). kuzu_cli.py's --mode inc branch (comp-find's own path) now passes wait_for_peer=False. A LOSER that finds the lock held by a LIVE peer (the steal-a-dead-lock path is unchanged either way) returns IMMEDIATELY -- 'STALE (age <H>h): peer rebuild in progress -- served immediately, no wait' -- instead of entering the RECHECK_SLEEP_S/MUTEX_WAIT_S poll loop.",
    "disclosure": "kuzu_cli.py's _run_query prints 'INFO: canonical surface NOT refreshed (mode=inc): STALE (age <H>h): ...' to stderr whenever ensure_fresh returns this reason -- previously this reason string was computed but NEVER PRINTED (a real, related gap found while implementing: refreshed=False silently discarded its own reason unless an exception occurred), so the caller had no way to see the age/stale label at all before this cell.",
    "measured": "battery arm G5-AC2-SERVE-STALE-IMMEDIATELY: a fresh (unstolen-age) lock directory planted beside a temp DB path with no manifest (needs_refresh() is unconditionally True with no manifest -- no real Kuzu DB required for this check); ensure_fresh(db_path, wait_for_peer=False) returned in 0.0x s (measured, printed in the arm's own detail) carrying a reason starting 'STALE' -- orders of magnitude under MUTEX_WAIT_S=180s. PASS."
  },

  "fix_c_two_waits_reconciled": {
    "carrier": "wait_for_peer=False derives the wait from the caller: it is ZERO, unconditionally, the moment a live peer is found -- not a timer. wait_for_peer=True (unchanged, comp-kuzu-full / comp-kuzu-auto) keeps RECHECK_SLEEP_S/MUTEX_WAIT_S exactly as before this cell; those constants are UNUSED on the wait_for_peer=False path, stated in ensure_fresh's own docstring rather than left implicit.",
    "citation": "comp-read infra/aws/globgrph/_canonical.py --enumerate 'MUTEX_WAIT_S|ORPHAN_LOCK_S|INCREMENTAL_TIMEOUT_S|remaining' -- 20 hits (DOCSTRING=4, COMMENT=4, CODE=12), all consumers agree: MUTEX_WAIT_S consumed at the wait_for_peer=True loop only (:695,:697 post-cell line numbers); the new wait_for_peer=False branch returns before reaching that loop at all (verified by reading the diff, not asserted)."
  },

  "fix_d_cadence_measured": {
    "trigger_predicate": "infra/aws/globgrph/_canonical.py:needs_refresh() (three OR'd conditions): (1) no manifest -> True; (2) Nessie HEAD status == 'behind' (_provenance._nessie_head_status); (3) build age > age_warn_hours",
    "measurement": "NO PERSISTENT PER-TRIGGER LOG EXISTS on this box for needs_refresh() firing -- _write_refresh_failure/_clear_refresh_failure overwrite ONE status file per DB (not an append log), and the .fallback.jsonl sink (_append_fallback_sink) records only the narrower 'served labeled-stale on a large delta' sub-case, not every trigger. A full 24h retrospective count is therefore NOT COMPUTABLE from existing logs without adding one, which this cell's bounds do not permit (no new file outside the two named + battery + deliverable + proof instance).",
    "nearest_available_signal": "this seat's OWN first-hand, session-scoped measurement (not a full 24h): 3 rebuild-trigger events observed directly within a ~51-minute window, 2026-09-03 03:16Z-04:07Z (03:16Z this seat, 03:53Z 3.0.0_SA_CVO, 04:07Z the live orphan measured directly -- row NFRA_COMPEFFICACY-S2/S3/S5/S6). Denominator: every --corpus aws call this seat and 3.0.0_SA_CVO made during that window, NOT a full 24h count and NOT claimed as one.",
    "finding": "FINDING G5-F1: the freshness layer has no persistent record of its own trigger cadence -- the exact instrument that would tell an owner whether 3 triggers/51min is normal or a defect (e.g. an unstable Nessie-HEAD signal, or an age_warn_hours set too tight for this box's real workload) does not exist. Owner: whoever owns comp-kuzu's operational logging next -- candidate this seat's own comp-kuzu engine lane (CE-t-22), not fixed under this cell (a measurement, not a change, per the TO's own bound)."
  },

  "battery": {
    "file_grain": "13 of 13 PASS, direct and under pytest (python .tools/tests/test_comp_find_battery.py; python -m pytest -q .tools/tests/test_comp_find_battery.py, 36.85s) -- the 6 original arms (A1-A5, E) unchanged GREEN, the 4 Rule-T arms (F,F2,F3,G) unchanged GREEN, THREE new arms this cell (G5-AC1-NO-ORPHAN, G5-AC1-MUTANT-STILL-ORPHANS, G5-AC2-SERVE-STALE-IMMEDIATELY) all GREEN with the mutant correctly RED under the reverted (unsupervised) code",
    "directory_grain": "unchanged from the prior cell's census: pytest --collect-only .tools/tests/ still INTERNALERROR / SystemExit at test_fabric_check_classify.py:76 (one of CTO's three named F6 files, not this cell's); this file (test_comp_find_battery.py) collects 1 test cleanly in isolation at both grains",
    "production_sha": {
      "_canonical.py": {"before": "edaa00ae4617f06b07932f8706c20fbbe0482ee610f8854ac1f7d591a1dd601c (HEAD @f659b4edd2)", "after": "d494be6660b0dd9674383a2504756d4fb852677eee5729718cc3298ff69b2952"},
      "kuzu_cli.py": {"before": "ac7f2e5cca7d12838e8b807bd426f17c0adef4ea166ce1cad2ae99363e5e0eaf (HEAD @f659b4edd2)", "after": "37a8accbd12f9fc11d6b3de3c07393ac28c0529eb91f17af0f211f82e0eb7c49"}
    }
  },

  "bounds_respected": {
    "no_new_dependency": "win32api/win32job/win32con (pywin32) and the stdlib subprocess/signal/os primitives used are ALREADY INSTALLED on this box (verified before writing any code); no new pip/package requirement added",
    "no_new_file_beyond_the_named": "infra/aws/globgrph/_canonical.py (edited), infra/aws/globgrph/kuzu_cli.py (edited), .tools/tests/test_comp_find_battery.py (edited), this deliverable, the proof instance -- no other file created or left behind (all test fixtures live in tempfile.TemporaryDirectory(), auto-cleaned)",
    "live_rebuild_untouched": "PID 25896 (or its successor) was NEVER signaled, killed, or otherwise touched by any exercise in this cell -- every G5 arm operates on disposable temp fixtures (a synthetic wrapper/child pair for AC1, a bare lock directory beside a nonexistent temp db_path for AC2), matching the TO's explicit bound",
    "rule_T_client_side_unchanged": "comp-find's --budget/--cursor/90s-default form is untouched by this cell; only kuzu_cli.py's internal mode=inc call to ensure_fresh gained one new keyword argument"
  },

  "push_state": "MEASURED at report -- see the DELIVERABLE REPORT message; expected LOCAL under Andrew's standing push hold (LD-0522)."
}
```

## The mechanism, before and after

**Before this cell** (measured, row S6 @`f659b4edd2`): a budgeted client (comp-find, via `subprocess.run(timeout=90)` on `kuzu_cli.py`) that wins the rebuild mutex and is then killed at its budget leaves its rebuild grandchild (`kuzu_nessie_load.py`) running, orphaned, holding the lock past its own ceiling. Every later caller polls `MUTEX_WAIT_S` (180s) -- longer than the 90s default -- and reports `BUDGET REACHED` with `0 scanned`. At `ORPHAN_LOCK_S` (900s) the lock is stolen, a new rebuild starts, and the cycle repeats. Measured three times in under an hour.

**After this cell:** (a) the rebuild subprocess is supervised by an OS-enforced mechanism (a Windows Job Object with kill-on-close, or a POSIX process group) that ties its life to the client's, so an external kill of the client reaps the grandchild too -- validated standalone, then in production via a red-first mutant. (b) a budgeted caller (`--mode inc`) that finds the lock already held by a live peer never waits: it returns immediately, serving the existing DB with an explicit `STALE (age ...)` disclosure that is now actually printed (previously computed and silently discarded). (c) the two waits no longer compete: the budgeted path's wait is unconditionally zero; the full/auto path's `MUTEX_WAIT_S`/`RECHECK_SLEEP_S` are untouched. (d) the trigger cadence is measured from this seat's own first-hand observation (3 events / ~51 min), with the gap that no persistent log exists for a true 24h count named as its own finding (G5-F1), not fixed here.

## Captures

Every quoted number above is from a direct execution this session (battery run + comp-read
`--enumerate` + `sha256sum` + `git show`), not from memory. The standalone Job-Object validation
(two throwaway scripts, removed after the test) preceded any production edit, per the estate's own
practice of proving a mechanism before wiring it in. `git status` clean of everything but this
deliverable + its proof-of-spec instance at write time.
