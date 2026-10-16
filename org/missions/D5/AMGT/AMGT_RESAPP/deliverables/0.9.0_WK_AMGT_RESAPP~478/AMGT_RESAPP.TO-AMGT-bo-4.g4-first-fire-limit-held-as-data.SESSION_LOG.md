# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~478 on AMGT_RESAPP.TO-AMGT-bo-4.g4-first-fire-limit-held-as-data

Worktree C:/dev/wk-resapp-478, branch wk-AMGT_RESAPP-478, cut at f1ff07c456. TREE-OK at the first act.
Premises re-grounded: the run.py line that runs the argv (`rc, out = runner(task.command)`) is present;
`lib/research/filings/batch.py` accepts `--limit` (argparse, `type=int`, default None); the package holds the
19 round-107 tests.

## Pre-edit runs (unchanged tree, literal invocations)

AC1 -- `cd C:/dev/wk-resapp-478 && timeout 300 python -m pytest lib/research/llm_batch/tests/test_first_fire_limit.py -q; echo "exit=$?"`
  output: `ERROR: file or directory not found: lib/research/llm_batch/tests/test_first_fire_limit.py` / `no tests ran in 0.00s` / `exit=4`

AC2 -- `cd C:/dev/wk-resapp-478 && timeout 120 python -m lib.research.llm_batch.run filings --print-command; echo "exit=$?"`
  output: `python.exe -m lib.research.llm_batch.run: error: unrecognized arguments: --print-command` / `exit=2`

AC3 -- `cd C:/dev/wk-resapp-478 && timeout 300 python -m pytest lib/research/llm_batch/tests -q; echo "exit=$?"`
  output: `19 passed in 0.95s` / `exit=0` (19 of 23 needed)

## Red before the build

The new test file was written first, with 13 tests (T1, T2 x7 plus T2b, T3, T3b, T4, T4b). On the unchanged tree:
`12 failed, 1 passed` (the one pass is T3b, the no-limits regression guard). The failures are AttributeError on
`command_for`, `load_limits` and `LIMITS_PATH`, and TypeError on the `limits` keyword of `run_task`.

## Build

Commit 96c408f05a (LOCAL on wk-AMGT_RESAPP-478): `first_fire_limit.json` (new), `run.py` (command_for, load_limits,
LIMITS_PATH, run_task `limits=None`, main passes the loaded limits and gains --print-command), and the test file.
Gate: `bash .tools/commit-gate.sh` on the two .py files -- `OK: pre-commit gate clean for 2 of 2 file(s)`.
ASCII check: 0 non-ASCII bytes in all three files.

## Post-edit runs (committed tree, literal invocations)

AC1 -- `13 passed in 0.81s` / `exit=0`
AC2 -- `LLM-BATCH task=filings command=python -m lib.research.filings.batch --universe newest --write-pool --limit 20` / `exit=0`
AC3 -- `32 passed in 0.94s` / `exit=0` (23 needed: 19 of round 107 plus 13)
Register plan -- `python -m lib.research.llm_batch.register --plan | tail -1` -- `PLAN: 3 task(s), 0 created`

The AC2 line was printed twice with identical bytes (determinism).

## Not done, by the order's bounds

Nothing registered, enabled or run as a Windows task. No AWS call. The filings batch was not run.
tasks.py, register.py, trigger.py, inputs.py, the launchers and the surprise channel are untouched.
The task order's `<status>` flip is left to the issuer, as the order states.
