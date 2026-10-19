# AMGT-cf-6 receipt -- the filings launcher runs the batch on Python 3.12

**Worker:** `0.9.0_WK_AMGT_RESAPP~527` (re-seated on slot 527 for Part B) **Order:** `AMGT_RESAPP.TO-AMGT-cf-1` (Part B, cell `AMGT-cf-6`)
**Cut:** `e78a163ce5` (the tree at the start of Part B; the re-open commit `77ce2ac555` is its ancestor)
**Code commit:** `7066ce85d3` on branch `wk-AMGT_RESAPP-527` (LOCAL; not pushed, not merged, not deployed).
**Interpreter present:** `py -3.12 --version` printed `Python 3.12.10` (rc=0) at Step A.

## What changed

- `lib/research/llm_batch/launchers/run_filings.cmd`: 24 lines (was 23; 2 insertions, 1 deletion). Line 22 is the
  command, changed from `python -m lib.research.llm_batch.run filings` to `py -3.12 -m lib.research.llm_batch.run filings`.
  One REM line added (line 10). The cd guard, the stamp, the log name, the redirect and the exit line are byte-identical.
- `lib/research/llm_batch/tests/test_launcher_capture.py`: 130 lines (2 insertions, 1 deletion). `COMMAND_LINE` now holds
  the `py -3.12` command; the stub prints one more line, `py=<major>.<minor>`, from `sys.version_info`.
- `lib/research/llm_batch/tests/test_run.py`: 87 lines (2 insertions, 1 deletion). Surprise row `AMGT_RESAPP-D1-W527-S1`:
  `test_t12` asserted the old `python -m ... filings` line for every launcher key, which the order did not name. The expected
  line is now `py -3.12 -m ... filings` for the filings key and `python -m ...` for the other keys. No other assertion touched.
- `lib/research/llm_batch/tests/test_launcher_interpreter.py`: 103 lines, new. Tests T1 (two cases), T2, T3, T4.
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`: 26 lines appended (one row,
  `AMGT_RESAPP-D1-W527-S1`, `disarm_owner` `2.0.0_SA_COO~R1`, `class` OBSERVATION, `hazard_standing` INERT).

Not touched: `run.py` (Part A), `run_management.cmd` and `run_scores.cmd` (sha256 unchanged), `tasks.py`,
`lib/research/filings/`, `portal/`, `org/devices/`. No AWS, model, SEC, vendor or Bloomberg call; no pip install; no
environment variable changed; the real `tmp/llm_batch/` of the repo root was not created or written; no push; no schedule change.

### Final text of the launcher (`lib/research/llm_batch/launchers/run_filings.cmd`, commit `7066ce85d3`)

```bat
@echo off
REM lib/research/llm_batch/launchers/run_filings.cmd -- AMGT-bn-6 (G4): the scheduled task's launcher.
REM The workspace root is DERIVED from this file's own location (%~dp0 is this directory, four
REM levels under the root) -- no device path is baked here.
REM The task is created DISABLED: enabling it is a separate act, Andrew's word.
REM AMGT-ce-2: the run's stdout, stderr and exit code are kept in a dated log beside last_run.json,
REM tmp\llm_batch\filings_<UTC stamp>.log (the stamp comes from PowerShell, not python; the literal
REM nostamp if it comes back empty). A log is appended to, never overwritten. If the cd to the root
REM fails, the launcher appends a line to %TEMP%\opal_filings_launcher_cd_failed.log and exits 1.
REM AMGT-cf-6: the batch runs on Python 3.12 (py -3.12) because the pinned anthropic SDK is installed there and the 3.14 python on this box is not.
cd /d "%~dp0..\..\..\.."
if errorlevel 1 (
  echo launcher: cd failed>>"%TEMP%\opal_filings_launcher_cd_failed.log"
  exit /b 1
)
if not exist "tmp\llm_batch" mkdir "tmp\llm_batch"
set "STAMP="
for /f "delims=" %%S in ('powershell -NoProfile -Command "[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ', [Globalization.CultureInfo]::InvariantCulture)"') do set "STAMP=%%S"
if not defined STAMP set "STAMP=nostamp"
set "LOG=tmp\llm_batch\filings_%STAMP%.log"
echo launcher start %STAMP% cwd=%CD% >>"%LOG%"
py -3.12 -m lib.research.llm_batch.run filings >>"%LOG%" 2>&1
echo exit=%errorlevel% >>"%LOG%"
exit /b %errorlevel%
```

## Tests

**Base, dry-run of the new file on the unedited head (`e78a163ce5` plus the new file only, before any product edit):**
`python -m pytest lib/research/llm_batch/tests/test_launcher_interpreter.py -q` gave `3 failed, 2 passed in 2.21s`, exit 1.
The failures were `test_t1 [0]` and `test_t1 [7]` (`assert "py=3.12" in lines` with the log holding `py=3.14`) and
`test_t2` (`COMMAND_LINE` absent from the launcher). The passes were the two controls, T3 and T4.

**Base, the whole directory at HEAD `e78a163ce5` (no edits, no new file):** `68 passed`. Measured from an export of `lib`
and `infra` at HEAD into `.scratch/base527`, run with `--rootdir=. -c /dev/null`. The worktree's `pytest.ini` was bypassed
for this run only: from the export, its `lib` resolved to the worktree and read the edited launcher.

**After (committed tree `7066ce85d3`), each literal invocation run twice with the same counts:**

| Criterion | Invocation | Run 1 | Run 2 |
|---|---|---|---|
| AC1 | `python -m pytest lib/research/llm_batch/tests/test_key_read.py -q` | `8 passed in 0.68s`, exit=0 | `8 passed in 0.65s`, exit=0 |
| AC2 | `python -m pytest lib/research/llm_batch/tests/test_launcher_interpreter.py -q` | `5 passed in 2.18s`, exit=0 | `5 passed in 2.56s`, exit=0 |
| AC3 | `python -m pytest lib/research/llm_batch/tests -q ... \| tail -2` | `73 passed in 6.75s` | `73 passed in 7.07s` |

The directory went from `68 passed` (base) to `73 passed` (after): the five new tests. Part A's eight tests in `test_key_read.py`
pass unchanged.

**The five tests of `test_launcher_interpreter.py` by name (collected):** `test_t1_stub_runs_on_python_312_and_exit_code_is_kept[0]`,
`test_t1_stub_runs_on_python_312_and_exit_code_is_kept[7]`, `test_t2_launcher_carries_the_py312_command_and_no_bare_python_command`,
`test_t3_control_start_line_exit_line_and_log_name`, `test_t4_control_sibling_launchers_unchanged`.

## Not verified

- The scheduled task `OpalResearch-FilingsAnalyzer` was not run, edited, enabled, disabled or re-scheduled here. The one
  on-demand run that proves the chain end to end is the issuer's cell `AMGT-cf-5`, after the merge.
- Whether `py.exe` (the launcher of Python 3.12) is on the PATH of the task's user is not read here. `AMGT-cf-5` reads it.
- The real batch and the real launcher from the repo root were not run; every launcher test ran a copy in a temporary tree
  against a stub module. The real `tmp/llm_batch/` was not written by these tests.
- The model call on Python 3.12 (the step that failed on 3.14, surprise row `AMGT_RESAPP-D1-S62`) is not exercised here:
  no model call is in this cell's bounds.
