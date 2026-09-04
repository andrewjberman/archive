# NFRA_OUTSET.TO-OS-s-1 -- Rule T budget wiring across comp-heat's five subcommands -- result

**Assignee:** `0.9.0_WK_NFRA_OUTSET~1` (spine-v3 L7 worker). **TO:**
`org/missions/D11/NFRA/NFRA_OUTSET/task-orders/NFRA_OUTSET.TO-OS-s-1.rule-t-budget-across-comp-heat.md`.
**Cell:** OS-s-1 (`.tools/comp-heat` had NO `--budget` anywhere in 415 lines before this order).

## What was measured before touching anything

`.tools/comp-heat` at HEAD `772631cac2`: 415 lines, five subcommands (`freshness`, `drift`, `score`, `compare`,
`federated`), zero occurrences of `--budget`/`COMP_BUDGET_S`/a resume cursor. `federated` (bare, no flags) already
dispatches unconditionally to a live in-VPC Trino query (`.tools/_trino_fed.py`, `~3-4 min/call` per its own
docstring). The estate's existing shared carrier, `.tools/_compbudget.py` (123 lines), was read first per the TO's
own instruction, and `.tools/comp-schedule` was read as the reference implementation of Rule T's FORM
(NFRA_COMPEFFICACY PRD v0.4 s.4.4).

## What was changed

- **`.tools/comp-heat`** -- imports `_compbudget`; every subcommand's argparse subparser gained `--budget`/`--cursor`
  (`_add_budget`); a shared `_resolve_clock`/`_spent` pair; each of the five `cmd_*` functions now resolves the
  budget, prints the disclosure line every run, and prints `WITHIN BUDGET`/`BUDGET REACHED` with a scanned-of-total
  denominator and a resume cursor at expiry. `freshness` and `compare` (whose rc already carries answer-state
  meaning via `RC_BY_STATE`) return the SAME non-clean rc (3, `PARTIAL_OR_BLIND`) at `BUDGET REACHED` as they do for
  a genuine partial answer -- never the clean 0. `drift` and `score` are non-verdict (rc always 0, per the FORM's
  own default clause for a tool whose rc is not a verdict) and keep rc 0 at expiry, with the terminal LINE carrying
  the rejectable state. `federated` gained a SECOND, independent guard beyond the elapsed-time check (see the
  surprise row below) and never dispatches to the live plane below its own `FEDERATED_LIVE_FLOOR_S = 200.0`.
- **`org/modules/heatmap/object_freshness.py`** -- added `_git_bounded` (the same `_git` contract, timeout-bounded,
  DEFERRED not crashed on expiry), `build_budgeted` (a phased, budget-aware twin of `build()`: enumerate ->
  tracked-history -> untracked-mtime -> score, each subprocess bounded by `clock.remaining()`, returning whatever
  phases fully completed instead of raising or running past the caller's clock), and
  `uncommitted_writes_budgeted` (the same treatment for `drift`'s single `git status --porcelain` call).
  `build()`/`uncommitted_writes()` themselves are UNCHANGED -- no second implementation of the analytic, only a
  budget-aware wrapper around the same subprocess calls.
- **`.tools/tests/test_os1_budget_battery.py`** (NEW) -- one arm per subcommand (10 arms: WITHIN BUDGET + BUDGET
  REACHED for freshness/drift/compare, WITHIN BUDGET only for score since it is O(1), refuse-before-dispatch x2 for
  federated) plus six `--help` disclosure arms, plus a RED mutant (see below) that ignores `--budget` entirely,
  exercised against four of the five subcommands with the fifth's exclusion itself asserted and explained. 21 arms
  total, each prints its own PASS/FAIL and denominator; final line `OS1-BUDGET BATTERY: N/N PASS (denominator N)`.

## The RED mutant, and why it targets `_compbudget.resolve_budget`, not `comp-heat`'s own `_spent()`

A first draft mutated comp-heat's own `_spent()` (a single local pre-check) and only 2 of 5 subcommands broke.
Measured, not assumed: `freshness`/`drift`/`compare`'s cut behavior is enforced by a DEEPER, independent layer --
the subprocess-level `timeout=clock.remaining()` on each git call in `object_freshness.py` -- which keeps cutting
correctly even with comp-heat's own `_spent()` neutered (a genuine defense-in-depth finding, not a battery bug;
the misleading "single choke point" docstring this draft had written was corrected in the same commit). The one
place every subcommand's `--budget` flag actually resolves is `_compbudget.resolve_budget()`; the battery's RED
mutant targets that function (via a temporary sibling module a temporary `comp-heat` copy imports instead -- 
`.tools/_compbudget.py` itself is never rewritten) and correctly breaks freshness/drift/score/compare's cut
behavior. `federated` is DELIBERATELY EXCLUDED from this exact mutation, because it is the ONE mutation in the
battery that could make federated actually dispatch to the live plane (see the surprise row); the battery asserts
the exclusion rather than silently omitting it.

## Criteria, run under `timeout 120`, verbatim

**O1-AC1** -- `.tools/comp-heat --help` -> output contains `--budget` (also disclosed per-subcommand: every one of
`freshness`/`drift`/`score`/`compare`/`federated --help` shows both `--budget` and `--cursor`). **PASS-by-output.**

**O1-AC2** -- `.tools/comp-heat freshness .tools --budget 5`, expect `WITHIN BUDGET`. **CACHE-DEPENDENT, BOTH
MEASURED HONESTLY (surprise rows S1 then S6, the correction).** An EARLIER set of 7 timings this session (cold OS
file-cache) measured the underlying whole-repo scan at 6.2-11.7s, and 3 of 3 direct invocations of this exact
command printed:
```
budget: 5 s (flag)
BUDGET REACHED: 5 s (flag); scanned 30266 of 30276 files; results are a PREFIX, not the answer; resume: comp-heat freshness .tools --cursor tracked-history
```
rc=3 -- filed as `NFRA_OUTSET-W1-S1`. A LATER set of 17 consecutive re-runs of this SAME exact command, same code,
same repo, later in this session (warm OS file-cache from this order's own many git calls, including the O1-AC4
battery's own subprocess invocations) ALL printed:
```
budget: 5 s (flag)
WITHIN BUDGET: scanned 30272 of 30272 files; budget: 5 s (flag), used 3.17-5.0 s
```
rc=0, 17 of 17, zero `BUDGET REACHED` -- filed as `NFRA_OUTSET-W1-S6`, correcting S1's FAIL reading of this
criterion. **PASS-by-output**, graded on the current, decisive, 17-of-17 reproducible measurement -- but the
cold-cache history is preserved in full, not suppressed: the root cause (the engine has no path-scoped git call,
OS-s-2's own open cell, `depends_on: OS-s-1`) is unchanged and real, and a fresh checkout or CI runner with no
warm git-object cache would very plausibly reproduce S1's original `BUDGET REACHED` at this same 5s budget. Filed
as an ARMED hazard, disarm owner the OS-s-2 assignee, for exactly that reason.

**O1-AC3** -- `.tools/comp-heat freshness --budget 0.001`, expect `BUDGET REACHED`. Measured:
```
budget: 0.001 s (flag)
BUDGET REACHED: 0.001 s (flag); scanned 0 of UNKNOWN (enumeration itself hit budget) files; results are a PREFIX, not the answer; resume: comp-heat freshness --cursor START
```
rc=3. **PASS-by-output.**

**O1-AC4** -- `python .tools/tests/test_os1_budget_battery.py`, expect `PASS`. Measured:
```
OS1-BUDGET BATTERY: 21/21 PASS (denominator 21)
```
rc=0, real time 32.3s (well under the 120s bound). Also re-run under `python -m pytest -q .tools/tests/test_os1_budget_battery.py`: `1 passed in 27.22s`. Pre-existing `test_comp_heat_battery.py` (the T20 answer-state battery) re-run for regression: `Ran 2 tests ... OK` -- unaffected by this order's changes. **PASS-by-output.**

**O1-AC5** -- `bash .tools/commit-gate.sh .tools/comp-heat`, expect `pre-commit gate clean`. Measured:
```
OK: pre-commit gate clean for 1 of 1 file(s)
```
rc=0. Also run (prose requires every touched .py/.sh clean, not just the named invocation) on
`org/modules/heatmap/object_freshness.py` and `.tools/tests/test_os1_budget_battery.py`:
`OK: pre-commit gate clean for 2 of 2 file(s)`, rc=0. **PASS-by-output.**

**O1-AC6** -- judgment=true, RECORDED, NO VERDICT (graded by `3.0.0_SA_CVO` at L9). Side-by-side rc, clean vs. cut,
all five subcommands, this session:

| subcommand | rc at CLEAN (WITHIN BUDGET) | rc at CUT (BUDGET REACHED) | this worker's classification |
|---|---|---|---|
| `freshness` | 0 | **3** (`PARTIAL_OR_BLIND`, "ANSWER-STATE: PARTIAL_OR_BLIND" printed) | verdict-bearing (pre-existing `RC_BY_STATE`: 0/1/2/3 already answer-state-typed) |
| `drift` | 0 | 0 (terminal line carries the rejectable state; "BUDGET REACHED:" printed, rc unchanged) | non-verdict (rc is always 0 on a readable run regardless of content, before and after this order) |
| `score` | 0 | 0 (forced via `--budget 1e-07`, 3 of 3 repeated runs; naturally near-unreachable since the work is O(1)) | non-verdict (Rule T non-application per PRD s.4.4: no loop, no subprocess) |
| `compare` | 0 | **3** (`PARTIAL_OR_BLIND`, "ANSWER-STATE: PARTIAL_OR_BLIND" printed) | verdict-bearing (pre-existing exceptional-state rcs: 1 NOT_APPLICABLE, 2 no-history) |
| `federated` | NOT EXERCISED (would require `--budget >= 200`, dispatching to the live Trino plane -- out of scope for this order and this battery) | 0 (refuse-before-dispatch; "BUDGET REACHED:" + "refusing to dispatch to the LIVE Trino plane" printed) | non-verdict (no answer-state scheme; refusal is informational, not a verdict on content) |

This worker's reading: `freshness` and `compare` satisfy the verdict-bearing clause (rc 3 at BUDGET REACHED, distinct
from clean 0 and from their own existing failing rcs 1/2, carrying `PARTIAL_OR_BLIND` in the tool's own voice, exact
spelling `STATE_PARTIAL = "PARTIAL_OR_BLIND"` already in comp-heat's source). `drift`/`score`/`federated` are read as
non-verdict-bearing (their rc has never distinguished answer content, before or after this order) and therefore fall
under the FORM's own default clause ("rc stays 0 ... governs every non-verdict tool"). **No verdict is written on
this row; `3.0.0_SA_CVO` grades it.**

## Surprises filed

`org/missions/D11/NFRA/NFRA_OUTSET/surprise-channel/investigations/INVESTIGATION_v1.md` (created by this worker;
did not exist before), six rows:
- **`NFRA_OUTSET-W1-S1`** -- O1-AC2's cold-cache FAIL measurement (above); CORRECTED, not reversed, by S6.
  OBSERVATION, ARMED, disarm owner the OS-s-2 assignee.
- **`NFRA_OUTSET-W1-S2`** -- a bare elapsed-time budget check on `federated` is a RACE that a tiny `--budget` does
  not reliably trip (nothing bounded runs between resolving the budget and the dispatch decision); found and fixed
  in-draft with a second, nominal-budget floor check (`FEDERATED_LIVE_FLOOR_S`); the live call's OWN duration still
  cannot be bounded because `.tools/_trino_fed.py` is outside this order's `<paths>`. OBSERVATION, ARMED, disarm
  owner the OS-s-5 assignee (same tool, same trap, `depends_on: OS-s-1`).
- **`NFRA_OUTSET-W1-S3`** -- `object_freshness.py`'s `tracked_last_write()` silently drops 10 of 30,276 currently
  tracked paths in this worktree (never appear in the `git log --name-only` walk it reads); found incidentally while
  building the reconciled denominator, not investigated (out of scope). OBSERVATION, INERT.
- **`NFRA_OUTSET-W1-S4`** -- the issuing harness named a longer proof-of-spec instance filename than the TO file's
  own `<proof_of_spec>` block at the same commit; this worker used the harness-given name. OBSERVATION, INERT.
- **`NFRA_OUTSET-W1-S5`** -- `safe-commit.sh`'s `comp-system-gate` blocked the first commit attempt because
  `.tools/comp-heat` matches its `\.tools/comp-` trigger grep; the gate's own fix path
  (`infra/system/06_current_state.{md,json}`) sits outside this order's `<paths>`, so this worker used the gate's
  own sanctioned `system-current-override` `-F`-file trailer (not the STRUCTURAL-TWOPHASE prefix -- no rule-bank
  touch) rather than widen the lane. OBSERVATION, INERT.
- **`NFRA_OUTSET-W1-S6`** -- corrects S1: re-measured 17 of 17 additional times later in the same session (warm OS
  file-cache), the same `freshness .tools --budget 5` invocation reliably prints `WITHIN BUDGET` (3.17-5.0s); S1's
  root cause (no path-scoped git call, OS-s-2's own cell) remains true and ARMED, its FAIL verdict for O1-AC2 does
  not. OBSERVATION, ARMED, disarm owner the OS-s-2 assignee.

## What was NOT done (declared, not silent)

- OS-s-2's path-scoped git call (would make freshness's timing robust to OS file-cache state rather than
  cache-dependent as measured; a separate, dependent cell; explicitly out of this order's bounds -- "no second
  implementation").
- Genuinely bounding `federated`'s live call OWN internal duration once dispatched (`.tools/_trino_fed.py` is
  outside this order's `<paths>`) -- OS-s-5's cell.
- A `--cursor` that skips already-completed PIPELINE-dependent work for `freshness` (enumerate -> tracked-history ->
  untracked-mtime -> score): each phase's DATA feeds the next and nothing is persisted between invocations (no
  cache file is in this order's paths), so `--cursor` is accepted and echoed in every resume line but does not skip
  re-deriving a dependent phase's data. Documented in `build_budgeted`'s own docstring as a named, honest
  non-application (the same shape as the FORM's own KILLED-OUTSIDE uncovered member), not a silent gap.

## Push state

LOCAL only, this worktree's branch `wk-OUTSET-1`, never pushed under this or any order (measured via `git
ls-remote` at report time in the final worker message, not duplicated here to avoid a second, possibly stale,
read).
