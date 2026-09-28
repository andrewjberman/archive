# IRPT_BCKEND.TO-IB-pr-193 -- async export log says REFUSED, never FAILED, for a refused replay

**Worker:** `0.9.0_WK_IRPT_BCKEND~62`. **Worktree:** `wk-irpt-p-62` (branch `wk-IRPT_BCKEND-62`).

## What changed

`infra/aws/lambda/investor-reporting/export/entry.py`, `run_async_submit` (lines 327-341 before the edit): added
one `except _async.AsyncSubmitRefused as exc` arm BEFORE the general `except Exception`, printing the same
`{"irpt_export_async": {...}}` line with `"stage": "REFUSED"` and `"reason": type(exc).__name__`, then
re-raising the exception unchanged. Every other exception still prints `"stage": _async.FAILED` and re-raises,
byte-for-byte as before. `submit_async.py` was not touched.

Added one test to `infra/aws/lambda/investor-reporting/export/tests/test_submit_async.py`:
`test_a_refused_replay_logs_stage_refused_never_failed` -- builds a real export via the in-memory world, replays
the same marked event a second time (no BUILDING pointer left, matching `AsyncSubmitRefused`'s own raise site at
`submit_async.py:166`), captures stdout via `capsys`, and asserts the only `irpt_export_async` line printed on
the replay carries `stage: REFUSED` and that the pointer never left `SUBMITTED` (i.e. the replay's failure to
log-as-REFUSED, not the pointer, was the bug).

## Verification

1. Baseline (before the fix), the task order's own checker:
   `p19_3_ac1_async_log.py` printed `FAIL AsyncSubmitRefused: stages ['FAILED']` -- confirmed the defect as
   described before touching anything.
2. After the fix: `P19-3-AC1 PASS` (both arms: AsyncSubmitRefused -> `['REFUSED']` re-raised; ExportBuildFailed
   control -> `['FAILED']` re-raised).
3. Full existing suite `pytest tests/test_submit_async.py -v`: 13 passed (12 pre-existing + the 1 new test), 1
   pre-existing failure unrelated to this cell -- see surprise row `IRPT_BCKEND-W62-S1`. Reproduced identically
   against the unmodified HEAD `entry.py` (this cell's edit backed out and restored), so it predates and is
   independent of this change.

## Out of scope, left alone

- `submit_async.py`, the receipt route, and every stage constant it defines -- untouched, per BOUNDS.
- The one pre-existing, unrelated test failure in the same file (`test_the_marked_event_builds_and_the_handle_reaches_the_receipt`,
  `AttributeError: module 'handler' has no attribute 'finalize_export'`) -- rowed at `IRPT_BCKEND-W62-S1`, not
  fixed (outside this cell's `<paths>` grant and outside `submit_async.py`/`entry.py`'s `run_async_submit`).
