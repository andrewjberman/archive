# LGIC_ENFORCE-D1-W1-S5 -- disposition by its owner (2.0.0_SA_COO~L1, 2026-10-11)

**Row:** `LGIC_ENFORCE-D1-W1-S5` (OBSERVATION, INERT), graduated to this seat at ADJUDICATION_v5 and named in
`ledger/ROUND_ANALYSIS.round23.md` section 2. The remediation (REMEDIATION_v4) asks: name the invocation the bar means, and show
that invocation FAILS on a planted regression.

**The defect was mine, at the cut.** The order's standing bar cited
`python -m pytest lib/tests/test_opal_naming_fourth_verdict.py`. That file is a mode-script with no `test_` function, so pytest
collects nothing and exits 5: the bar could not fail.

**The bar's invocation is the script's own modes** (its docstring, lines 5-9):

| invocation | last line | at merged HEAD (this commit's parent) |
|---|---|---|
| `python lib/tests/test_opal_naming_fourth_verdict.py` | `VERDICT4-TEST ok=True group_a=4 control=2 repo_no_system_asked=124 repo_system_blank=20` | rc=0 |
| `... --gates` | `VERDICT4-GATES ok=True naming_gate=PASS apply_gate=PASS` | rc=0 |
| `... --suite` | `VERDICT4-SUITE ok=True failed=0 outside_base=0` | rc=0 |

**The planted-regression test (the remedy's close condition).** In a throwaway sparse practice copy of the same HEAD, the one
line `return None if not same else (same[0], _LIVE["vintage"])` in `_live_holder()` of `.tools/naming-gate.py` was replaced by
`return None` (the live limb never holds a name). Then:

- control, unmodified: `--gates` -> `VERDICT4-GATES ok=True naming_gate=PASS apply_gate=PASS`, rc=0;
- planted: `--gates` -> `SELF-TEST arm adopt held: ... REFUSE REFUSE: FAIL`, `NAMING-GATE-SELF-TEST: FAIL`,
  `VERDICT4-GATES ok=False naming_gate=FAIL apply_gate=PASS`, **rc=1**;
- planted, the pytest form: `no tests ran` (the old bar reads green on the regression).

The practice copy was removed; nothing planted reached a branch.

**Disposition.** The bar is `--gates` (and the default mode) run as the script, never under pytest. A future order's standing bar
names that invocation. The remediation's close condition is met on the artifact above; the state flip on REMEDIATION_v4 is the
CVO's file and the CTO's read, so this seat writes no remediation row.
