# NFRA_OUTSET.TO-OS-s-5 -- RESULT: `comp-heat federated --sql` is bounded, or refused with its reason

**Assignee:** `0.9.0_WK_NFRA_OUTSET~1` (L7 worker subagent of `2.0.0_SA_COO`, spine v3)
**Branch:** `wk-OUTSET-1` (linked worktree `C:\tmp\wk-OUTSET-1`) · **Base:** `2eabc5197e`
**Cell:** `OS-s-5` · **outcome_ref:** FWD-2 · **verb:** fix · **depends_on:** `OS-s-1`

---

## 1. WHAT I MEASURED FIRST, AND ONE THING THE CELL ALREADY HAD

**`O5-AC1`'s own invocation already matched its `<expect>` before I changed anything.**
`.tools/comp-heat federated --sql "SELECT 1" --budget 30` at `2eabc5197e` returned rc=0 in 0.8 s
and printed `budget: 30 s (flag)`. That is not a coincidence and it is worth stating plainly rather
than quietly banking: 30 is below `FEDERATED_LIVE_FLOOR_S` (200 s), so the invocation takes the
**refuse-before-dispatch** path that `OS-s-1` added, and `budget` appears in the disclosure line.
**The criterion can only be satisfied by the refusal path, and that is the correct outcome** -- the
alternative would be raising the budget past 200 s to force a live dispatch, which would be paying a
shared plane to make a criterion look better.

**So the cell's actual defect is on the DISPATCH path, and it was real.** `_trino_fed.py:82` declares

```
def run_federated_query(sqls: list[str], *, delay: int = 15, max_attempts: int = 40)
```

and `cmd_federated` called it as `run_federated_query(qs)` -- **with neither parameter**. The ECS
`tasks_stopped` waiter therefore ran on a fixed **15 x 40 = 600 s** ceiling, *completely independent
of the caller's `--budget`*. That is the sense in which `--sql` was an unbounded remote query: the
caller's ceiling never reached the transport at all.

## 2. WHAT CHANGED (`.tools/comp-heat` only -- the transport file is not in this grant)

- **`_federated_waiter_bound(remaining)`** -- derives `(delay, max_attempts, ceiling, basis)` from
  `clock.remaining()`, holding back a 25 s reserve for the work that is not the waiter (client
  construction, `ecs:RunTask`, the `logs:GetLogEvents` read). `remaining is None` (`--budget 0`)
  returns the transport's **own** defaults and says so: Rule T's `0 = unbounded` means the tool must
  not invent a ceiling the caller declined.
  **Build ladder rung 4:** the transport already had the parameter. Nothing new is implemented, and
  `.tools/_trino_fed.py` is not touched.
- **`_federated_dispatch_bound_line(...)`** -- prints what the bound does *and what it does not do*,
  in one line so neither can be read alone: it bounds **this process's wait**, not the remote task.
- **The dispatch** now passes the derived values, and a `WaiterError` is caught and reported in the
  Rule T vocabulary with `ANSWER-STATE: PARTIAL_OR_BLIND` and **rc=3**, not a traceback.
- **The refusal line's parenthetical was corrected.** It used to say "a live call cannot be bounded
  once started", which this cell makes false. It now says the transport starts a remote task the
  wrapper cannot cancel, so a budget that could not cover one call is refused *before* dispatch
  rather than cut after it.
- **`--help` on `--sql`** discloses the bound.

### 2.1 The rc asymmetry, stated because it is a design choice and not an oversight

| path | rc | why |
|---|---|---|
| refuse-before-dispatch | **0** | a complete and correct answer to "should I run this?" -- and `OS-s-1`'s battery asserts this rc, so changing it would break a drained cell |
| dispatched, then the waiter ran out | **3** (`PARTIAL_OR_BLIND`) | the caller has **no answer at all**; rc 0 would say "fine" about nothing |

## 3. ACCEPTANCE -- invocation, output verbatim, rc, denominator

### O5-AC1 -- PASS-by-output
`<invocation>` `.tools/comp-heat federated --sql "SELECT 1" --budget 30` · `<expect>` `budget`

```
budget: 30 s (flag)
BUDGET REACHED: 30 s (flag); scanned 0 of UNKNOWN (enumeration itself hit budget) queries; results are a PREFIX, not the answer; resume: comp-heat federated --sql 'SELECT 1' --cursor START
comp-heat federated: refusing to dispatch to the LIVE Trino plane -- budget below the transport's own known floor (~200s; _trino_fed.py: '~3-4 min/call') (the transport starts a remote task this wrapper cannot cancel, so a budget that could not cover one call is refused BEFORE dispatch rather than cut after it -- .tools/_trino_fed.py, OS-s-5)
VINTAGE: 0 catalog(s) joined (none), 0 table(s), 0 measured / 0 UNREAD -- the ARTIFACT's build time, never the query's clock
  (no fully-qualified catalog.schema.table appears in the SQL about to run -- nothing to date, and nothing is assumed)
```
**rc=0.** The criterion's `<expect>` `budget` is matched by the disclosure line `budget: 30 s
(flag)`, and the clause "or refuses naming the reason" is matched by the refusal line, which names
the floor, its source and the transport's own docstring figure. **3 of 3 consecutive runs: rc=0,
identical output, wall 1113 / 2608 / 1230 ms, and 0 of 3 contained the transport's own dispatch
banner** -- so this criterion cost the live Trino plane nothing.

The `VINTAGE` block (from `OS-s-4`) correctly reports **0 catalogs** for `SELECT 1`, because the
table list is derived from the SQL rather than recited.

### O5-AC2 -- PASS-by-output
`<invocation>` `python .tools/tests/test_os5_sql_bound.py` · `<expect>` `PASS`

```
[PASS] A-AC1-INVOCATION-REFUSES-AND-DISPATCHES-NOTHING -- rc=0 | budget: 30 s (flag) | live-banner-absent=True
[PASS] B-SQL-PATH-TINY-BUDGET-STILL-REFUSES
[PASS] C-FLOOR-IS-NOMINAL-NOT-ELAPSED-TIME -- --budget 199.9 -> refused (rc=0) ; --budget 200.1 -> dispatched to the STUB (transport received {'delay': 5, 'max_attempts': 35, 'ceiling_s': 175, 'n_sqls': 1}). 0.2 s of nominal budget separates them; wall-clock does not
[PASS] D-WAITER-CEILING-DERIVES-FROM-AND-MOVES-WITH-THE-BUDGET -- --budget 250 -> transport received {'delay': 5, 'max_attempts': 45, 'ceiling_s': 225} ; --budget 400 -> {'delay': 5, 'max_attempts': 75, 'ceiling_s': 375} ; monotone=True ; both under the pre-cell fixed 600 s
[PASS] E-UNBOUNDED-IS-HONOURED-AND-DISCLOSED -- transport received {'delay': 15, 'max_attempts': 40, 'ceiling_s': 600} ; disclosure line present=True
[PASS] F-WAITER-TIMEOUT-IS-A-BUDGET-EVENT-NOT-A-TRACEBACK -- rc=3 (3 = PARTIAL_OR_BLIND; refuse-before-dispatch stays rc 0) | traceback-absent=True
[PASS] G-RED-MUTANT-SQL-RUNS-UNBOUNDED-AND-IS-CAUGHT -- mutant at --budget 250 -> transport received {'delay': 15, 'max_attempts': 40, 'ceiling_s': 600} (the transport's OWN defaults, a fixed 600 s wait no --budget can shorten) vs production at the SAME budget -> {'delay': 5, 'max_attempts': 45, 'ceiling_s': 225}
[PASS] H-MUTATION-ANCHOR-UNIQUE
[PASS] I-HELP-DISCLOSES-THE-SQL-BOUND
[PASS] Z-NO-LIVE-TRINO-DISPATCH-BY-THIS-BATTERY -- swept 10 captured child-process outputs for the real transport's own dispatch banner 'launching in-VPC Trino query task' -- 0 hit(s)
OS5-SQL-BOUND BATTERY: 10/10 PASS (denominator 10; 10 child runs, 0 live Trino dispatches -- arm Z is the check, not the claim)
```
**rc=0. 10 of 10 arms PASS.** Also under pytest: `1 passed in 5.04s`. Stable across 3 direct runs.

**The RED mutant the criterion names** is arm G: it restores the pre-cell `run_federated_query(qs)`
call in a temporary copy of comp-heat, and the battery catches it **by reading what the transport
actually received** -- the transport's own defaults (600 s) instead of the caller's derived 225 s, at
the same `--budget 250`. Without it, arm D would be vacuous.

## 4. HOW THIS BATTERY GETS PAST A 200 s FLOOR WITHOUT PAYING A LIVE PLANE

The cell's whole subject is the path *beyond* the refusal, so some arms must get there. None of them
dispatch:

1. Refusal arms use the real tool below the floor.
2. **Past-the-floor arms run a temporary copy of comp-heat in a `tempfile` directory beside a STUB
   `_trino_fed.py`.** comp-heat resolves its transport with `sys.path.insert(0, _HERE)` where
   `_HERE` is its own directory -- so the copy imports the stub and **the real transport is not
   reachable from those arms by construction**, not by care.
3. **Arm Z is the falsifier rather than a restatement:** it sweeps every captured stdout+stderr from
   every child process this battery ran for the real transport's own banner
   `launching in-VPC Trino query task`. **10 outputs swept, 0 hits.**

The stub is also the only instrument that can answer the question the cell actually asks -- *did the
caller's budget reach the transport?* -- because that value is a **parameter**, invisible in any
output. Reading it required standing where the transport stands.

## 5. `NFRA_OUTSET-W1-S2` CLOSED BY LIMB, WHICH IS THE ONLY HONEST WAY TO CLOSE IT

`W1-S2` names the OS-s-5 assignee as its disarm owner. "Bounded" turned out to be **three** claims:

| limb | standing | evidence |
|---|---|---|
| 1. the tiny-budget **race** -- a bare elapsed-time check lets a near-zero budget dispatch | **DISARMED** | arm C: `--budget 199.9` refuses, `--budget 200.1` dispatches. They differ by **0.2 s of declared budget and by nothing in wall-clock**, so no elapsed-time check could separate them -- the guard is provably nominal. Arm B re-exercises the near-zero case on the `--sql` path specifically, which `W1-S2`'s original arms did not cover |
| 2. the **caller's wait** | **DISARMED by this cell** | arm D: 225 s at `--budget 250`, 375 s at `--budget 400`, monotone, both under the pre-cell fixed 600 s |
| 3. **cancelling the remote task** | **STILL ARMED** | `run_federated_query` returns only `[{sql, columns, rows}]`; the ECS task ARN never crosses that boundary, so there is nothing to pass to `ecs:StopTask` -- and `.tools/_trino_fed.py` is **not** in this order's `<paths>` |

I did **not** disarm limb 3 by having reached this cell. It is recorded in `NFRA_OUTSET-W1-S15` with
`2.0.0_SA_COO` as disarm owner, because the fix is a grant decision and not a worker act, and the
tool now **prints** the limitation on every dispatch rather than leaving it to the channel.

**What a bounded caller wait does not buy:** it does not reduce the COST of a dispatched query. The
Fargate task and its Trino work are paid for either way. What changes is that the caller gets a
stated `PARTIAL_OR_BLIND` answer at its own ceiling instead of blocking for up to 600 s.

## 6. TWO MORE ROWS

- **`NFRA_OUTSET-W1-S16`** (INERT, **not** BLOCKING) -- this face's title asserts "an unbounded
  remote query is not a mode", and the third limb of that needs `.tools/_trino_fed.py`, which the
  `<paths>` block does not name. `W1-S2`'s own note had predicted it would be "inside OS-s-5's likely
  one". **I did not file this as BLOCKING**: no criterion is stopped -- both are satisfiable, and
  were satisfied, entirely within `.tools/comp-heat` and `.tools/tests/`. A blocking row on a
  criterion that passes would be a false stop.
- **`NFRA_OUTSET-W1-S17`** (ARMED) -- comp-heat's own docstring says *"ADVISORY-ONLY + READ-ONLY ...
  never writes to the repo or any store"*, but `--sql` passes the caller's statement through
  unread: **nothing in `comp-heat` or `_trino_fed` inspects the verb.** The read-only claim is a
  docstring, not a control.
  **I deliberately did not build a guard**, and the reasons matter more than the gap: (1) CLAUDE.md
  forbids implementing an approval gate on work Andrew did not ask for, and a statement-verb filter
  on a caller's own query is exactly that; (2) a keyword filter over arbitrary SQL is a **false**
  sense of safety -- it reads as enforcement while being trivially evadable, which is worse than a
  documented gap. **Not claimed, and deliberately not tested: that a write would succeed.** Proving
  that would mean issuing a destructive statement against a live shared store. The claim is exactly
  and only that *nothing in the tool checks*, which is a code read at a named commit.

## 7. LIVE-PLANE DISCIPLINE

| what | held |
|---|---|
| Trino queries dispatched under this order | **0** -- and arm Z checks it across every child process rather than asserting it |
| budget raised to make something pass | **never**; `O5-AC1` passes on the refusal path and that is stated, not worked around |
| AWS API calls made by this cell | **0** -- every arm is either below the floor or against the stub |
| new dependency / second implementation | none; the bound uses the transport's **own** existing parameters |

## 8. REGRESSION + GATES

| check | result |
|---|---|
| `python .tools/tests/test_os5_sql_bound.py` | `10/10 PASS`, rc=0 (x3) |
| `python -m pytest -q .tools/tests/test_os5_sql_bound.py` | `1 passed in 5.04s`, rc=0 |
| `python .tools/tests/test_os1_budget_battery.py` | `21/21 PASS`, rc=0 |
| `python .tools/tests/test_os2_path_grain.py` | `10/10 PASS`, rc=0 |
| `python .tools/tests/test_os4_federated_vintage.py` | `9/9 PASS`, rc=0 |
| `python .tools/tests/test_comp_heat_battery.py` | `Ran 2 tests ... OK`, rc=0 |
| `bash .tools/commit-gate.sh` on the 2 touched files | `OK: pre-commit gate clean for 2 of 2 file(s)`, rc=0 |

**Two gate blocks I hit and what I did about them**, since a gate that fires is evidence too:
- **ruff F401** on two imports left over from an earlier draft -- removed.
- **the strict-utf8 log-read lint** on `with open(log, ...)`. The gate was **right and I did not
  work around it**: `log_open_lint.LOG_NAME_RE` matches a variable named `log`, and my variable held
  a single-writer JSON record written by the stub in the same process tree -- so the *name* was the
  misleading part. I renamed it `rec_path` rather than adding `errors="replace"` to a read that has
  no multi-writer exposure, which keeps the lint's coverage intact for real logs.

**One arm was wrong before it was right, and it is worth recording.** Arm D first hardcoded
`max_attempts == 45` for `--budget 250` and FAILED at 44 -- the ceiling derives from
`clock.remaining()` *at dispatch*, already a second or two below the nominal budget because the
disclosure and vintage block run first. **The code was right and my expectation was wrong.** The arm
now asserts the *property* (delay is 5; the ceiling never exceeds what the caller has left; it is
monotone in the budget; it is under the pre-cell 600 s) and prints the numbers. A constant there
would have been a brittle red that teaches re-tuning instead of reading -- the same failure mode as
the arm F flake on `OS-s-2`.

## 9. DECLARED NON-APPLICATION

- **`.tools/_trino_fed.py` untouched** -- not in this order's `<paths>`. This is what leaves limb 3
  of `W1-S2` armed, and it is recorded rather than routed around.
- **No Trino session property / query timeout** (`query_max_execution_time`) -- that would mean
  editing `_runtime_script` in the transport file. Named because it is the one mechanism that could
  bound the *remote* work, and it is out of grant.
- **No SQL-content restriction** -- `W1-S17`, above.
- **No change to the refuse-before-dispatch rc** -- it stays 0 because `OS-s-1`'s drained battery
  asserts it; the new non-clean rc 3 is on the new dispatch-cut path only.
- **Nothing deleted, no alarm/monitor/freshness-checker, no new dependency.**

## 10. PUSH STATE

**LOCAL.** Nothing pushed under this order. Measured with `git ls-remote` at report time -- the
reading and its vintage are in the WORKER REPORT.
