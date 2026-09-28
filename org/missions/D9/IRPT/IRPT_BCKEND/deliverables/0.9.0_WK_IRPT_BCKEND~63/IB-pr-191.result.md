# IB-pr-191 / IB-pr-194 -- session log (0.9.0_WK_IRPT_BCKEND~63, round 19, REOPENED)

## Base

Worktree `wk-irpt-p-63` (branch `wk-IRPT_BCKEND-63`) on CLOUD @57a58117fb, which already carries cell
`IB-pr-191` built and merged: `f49_engine.EngineReturnImplausible` (beside `WindowNotRuled`), the
`calculate` guard raising it when a linked daily `r_net <= -1.0` falls inside the window, the
`entry.py` reasons-table line (`"EngineReturnImplausible": "DEPENDENCY_UNAVAILABLE"`), and the
NEW-01 test in `tests/test_f49_engine.py`. Verified in place, unchanged, and re-run (see acceptance
below) rather than rebuilt.

## Cell IB-pr-194 (the reopen's own cell)

The Performance page reopens RETAINED reports (`retained.py` `_compute` -> `reopen`) and never
re-runs `f49_engine.calculate`, so IB-pr-191's guard never reaches a report accepted before it
existed. Built in `retained.py`:

1. Module function `implausible_engine_series(report)`: reads
   `report["returns"]["daily_cumulative_series"]`, each point a plain number or a dict carrying its
   value under `cumulative` (the current `normalize.py` shape) or `value` -- True when any point
   is `<= -1.0`.
2. `reopen(pointer, *, check_engine_series)` -- a new keyword parameter rather than an unconditional
   check inside the function body. The genuine "an accepted pointer already exists" branch
   (`_compute`'s `if existing is not None:`) calls `reopen(existing, check_engine_series=True)`: when
   the owner's firm is 49 Financial and `implausible_engine_series(accepted["report"])` is True, it
   raises `f49_engine.EngineReturnImplausible` before returning. The FRESH path's own call to
   `reopen(pointer, ...)` right after persisting passes `check_engine_series=False` -- **unchanged**,
   per the build note ("every other reopen, every other firm and the fresh path are unchanged").

   SURPRISE (not filed as a row -- see below): my first attempt put the check unconditionally inside
   `reopen()`. Because `_compute`'s fresh path also calls `reopen()` at its own end (line 252, to
   reuse the same formatting/validation), that made a freshly-computed implausible report ALSO
   refuse via the same call -- which sounds correct in isolation, but the task order's own AC1
   check (`p19_4_ac1_reopen_fixture.py`) simulates "a report accepted under the pre-guard code" by
   monkeypatching `retained.f49_engine` to the OLD (pre-guard) module for exactly the first
   `compute()` call, and expects that FIRST call to succeed (it asserts `first["report"]` reflects
   the implausible series, not an exception) -- only the SECOND, independent `compute()` call
   (hitting the real "existing pointer" reopen branch) must raise. Running the check first surfaced
   `AttributeError: module 'f49_engine_preguard' has no attribute 'EngineReturnImplausible'` because
   the unconditional check fired inside that same first call while `retained.f49_engine` was still
   swapped. The `check_engine_series` split resolves this without touching the fresh path's
   behavior at all -- this is a build-time correction inside my own draft, not a spec ambiguity or a
   premise failure, so no surprise row was filed.

3. Tests added to `tests/test_retained_performance.py`:
   `test_reopen_refuses_a_pre_guard_implausible_engine_report` -- Arm A persists the real
   `f49_engine.calculate` output for the NEW-01 account directly through
   `composition.build_retained_repositories` (bypassing `RetainedPerformance.compute`, whose own
   fresh path always ends in its own `reopen()` call and would otherwise mask a "genuinely
   pre-existing pointer" scenario), with the last `daily_cumulative_series` point hand-set to -1.0
   (simulating what a pre-guard-computed report would have carried); the real service's SECOND,
   independent `compute()` call against that pointer raises `f49_engine.EngineReturnImplausible`
   with no further engine read. Arm B is a distinct clean account computed and reopened normally,
   asserting the unpoisoned report reopens unchanged with no second engine read.

## Verification

`python -m pytest infra/aws/lambda/investor-reporting/performance/tests/` -- 212 passed (includes
the existing 10 `test_f49_engine.py` tests, unchanged, and 19 `test_retained_performance.py` tests,
18 pre-existing + 1 new covering both arms).

`ruff check --target-version py39` on `retained.py`, `tests/test_retained_performance.py`,
`f49_engine.py`, `entry.py`, `tests/test_f49_engine.py` -- all checks passed.

All five acceptance criteria run from the worktree root per their exact invocations; see the proof
instance for verbatim output.

## Surprises

None filed. The one build-time correction above (the `check_engine_series` split) was found and
fixed within this order's own scope by running the order's own named AC1 check, not an off-task
observation.
