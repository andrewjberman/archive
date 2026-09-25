# Session log -- 0.9.0_WK_NFRA_OPALAI~6, TO-OA-w-3

- Built `opal_ai/opal/checks/run_checks.sh`: finds its own repo root from its own location
  (`cd "$(dirname "${BASH_SOURCE[0]}")/../.." `), needs only bash/python/ruff on PATH. Runs
  py_compile, ruff (py39), an ASCII-byte rule and a no-device-path rule over `opal/`, plus
  pytest over any `test_*.py` if present. Last line is exactly `CHECKS: PASS` or `CHECKS: FAIL`,
  with each failing check named on its own line above.
- The device-path detector builds its `C:\Users\` / `/c/Users/` / `ajb_workspace` search
  patterns from concatenated string parts (`"C:" + chr(92) + "Users" + chr(92)`, etc.) so the
  detector's own source text never contains the literal it searches for -- an early version
  self-flagged on its own comments and regex string.
- Built `opal_ai/.github/workflows/ci.yml`: `on: push` (all branches) + `pull_request`, one job
  installing python 3.9 + ruff, one step running `bash opal/checks/run_checks.sh`.
- Committed both to the nested `opal_ai` repo (a separate repository) at
  `25427629aee4e77e62a6a531e2a3773e779c5778` on branch `wk-NFRA_OPALAI-6-opal_ai`.
- Ran AC1-AC3 from `/c/tmp/oa-6` (the parent worktree root). AC1 and AC3 PASS-by-output. AC2's
  harness (`w3.AC2.sh`) reads `rc=$?` off the trailing `tr -d '\r'` in its capture pipe rather
  than off `run_checks.sh`, so `rc` is always 0 regardless of run_checks.sh's own exit code
  (confirmed by a positive control: `out=$(false | tr -d '\r'); echo $?` prints 0). Direct
  invocation of run_checks.sh against the same planted mutant (bypassing the broken pipe) shows
  it correctly exits 1 and names both `py_compile` and `ascii`. Filed
  `NFRA_OPALAI-Z-W6-S1` (OBSERVATION/ARMED, disarm_owner `2.0.0_SA_COO~O`); did not edit
  `w3.AC2.sh` (outside this order's `<paths>`). AC2 reported FAIL-by-output on the recorded
  invocation.
