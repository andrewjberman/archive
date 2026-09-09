# NFRA_OUTSET.TO-OS-s-2 -- RESULT: `comp-heat freshness` answers at a PATH grain

**Assignee:** `0.9.0_WK_NFRA_OUTSET~1` (L7 worker subagent of `2.0.0_SA_COO`, spine v3)
**Branch:** `wk-OUTSET-1` (linked worktree `C:\tmp\wk-OUTSET-1`) · **Code commit:** `2282527e51` (LOCAL)
**Cell:** `OS-s-2` · **outcome_ref:** FWD-1 · **verb:** fix · **depends_on:** `OS-s-1` (landed `b3bf6c98d8`)

---

## 1. WHAT WAS MEASURED FIRST (the premise, re-grounded before any edit)

Both halves of the cell's claim were re-measured on this worktree at `79ec54bb37`, BEFORE any change:

| invocation (each under `timeout 120`) | rc | printed denominator | engine `used` | wall |
|---|---|---|---|---|
| `.tools/comp-heat freshness .tools --budget 60` | 0 | `scanned 30543 of 30543 files` | 5.25 s | 5.611 s |
| `.tools/comp-heat freshness org/modules/heatmap --budget 60` | 0 | `scanned 30544 of 30544 files` | 4.234 s | 4.805 s |

The header line already carried the corner's count (`files=387`, `files=8`) but the Rule T terminal
line beside it carried the WHOLE REPO's -- **two grains in one output, neither labelled**. The cost
was the whole repo's too: `object_freshness.build_budgeted()` ran `git log --format=... --name-only
--no-renames` with **no pathspec**, and `.tools/comp-heat` then prefix-filtered the result. Its own
comment said so, verbatim at `79ec54bb37`: *"Subtree scoping is therefore a wrapper-side PREFIX
FILTER over the engine's pure analytic"*.

## 2. WHAT CHANGED

**`org/modules/heatmap/object_freshness.py`**
- `_scope_pathspec(scope)` -- the argv tail: `[]` for the whole-estate form (so the no-path call is
  byte-unchanged), `["--", scope]` for a named corner.
- `build_budgeted(root, p, now_ts, clock, cursor=None, scope=None)` -- `scope` is threaded into
  **all three** git calls (`enumerate`, `tracked-history`, `untracked-mtime`). Every return echoes
  `scope`, and the DEFERRED reasons name the pathspec they were bounded on.
- The history pass also carries `--full-history` **when and only when** it carries a pathspec.
  This is load-bearing, not decoration: `git log -- <path>` default-simplifies history and can
  prune a side branch's own write, which would let a scoped answer disagree with the unscoped one.
  The unscoped walk applies no simplification, so the scoped walk must not either.

**`.tools/comp-heat`**
- `cmd_freshness` passes `scope=rel or None`.
- New `_denominator_line()` / `_scoped_git_call()`: the output now states **which population the
  number counts** and **the exact git call that produced it** -- on the human render, in the JSON
  carrier (a `denominator` block with `"claim": "measured"`), and on a BUDGET REACHED cut.
- The wrapper prefix filter is **retained as a safety net, not as the scoping**, and its residue is
  printed (`wrapper prefix-filter dropped 0 row(s)`). A regression to unscoped rows would surface
  as a non-zero number in the tool's own output instead of being silently absorbed.
- `--help` and the usage docstring disclose the grain.

**`.tools/tests/test_os2_path_grain.py`** -- new, 10 arms, 10/10 PASS, ~23 s.

## 3. ACCEPTANCE -- invocation, output verbatim, rc, denominator

All three at code vintage `2282527e51`, each under `timeout 120`.

### O2-AC1 -- PASS-by-output
`<invocation>` `.tools/comp-heat freshness .tools --budget 60` · `<expect>` `denominator`

```
=== comp-heat freshness  scope=.tools/  files=388  half_life=30.0d ===
budget: 60 s (flag)
WITHIN BUDGET: scanned 388 of 388 files; budget: 60 s (flag), used 1.219 s
  denominator: 388 of 388 files under .tools/ -- PATH-SCOPED to this corner, NOT the whole repository; git call: `git log --format=%ct --name-only --no-renames --full-history -- .tools`; wrapper prefix-filter dropped 0 row(s) (0 = the engine scoped it)
  basis: band = age vs barriers [hot<=7d, warm<=30d, cold>30d]; score = exp(-ln2*age/30d half-life)
  bands: hot=99 warm=42 cold=246 (cold_frac=0.64)
```
**rc=0.** Denominator **388 of 388** (that corner's own; was 30543 of 30543). The basis block prints.
Repeated 3 consecutive times before the commit: `used` 0.875 / 0.797 / 1.016 s, wall 1859 / 1612 /
1897 ms, rc=0 3 of 3.

### O2-AC2 -- PASS-by-output
`<invocation>` `.tools/comp-heat freshness org/modules/heatmap --budget 60` · `<expect>` `denominator`

```
=== comp-heat freshness  scope=org/modules/heatmap/  files=8  half_life=30.0d ===
budget: 60 s (flag)
WITHIN BUDGET: scanned 8 of 8 files; budget: 60 s (flag), used 0.547 s
  denominator: 8 of 8 files under org/modules/heatmap/ -- PATH-SCOPED to this corner, NOT the whole repository; git call: `git log --format=%ct --name-only --no-renames --full-history -- org/modules/heatmap`; wrapper prefix-filter dropped 0 row(s) (0 = the engine scoped it)
```
**rc=0.** Denominator **8 of 8** (was 30544 of 30544). Against O2-AC1's 388: **the number moves with
the path**, which is the whole claim. Repeated 3 consecutive times: `used` 1.094 / 0.594 / 1.062 s,
wall 2372 / 2200 / 2168 ms, rc=0 3 of 3.

### O2-AC3 -- PASS-by-output
`<invocation>` `python .tools/tests/test_os2_path_grain.py` · `<expect>` `PASS`

```
[PASS] A-SCOPED-HUMAN-RENDER-PRINTS-DENOMINATOR-AND-GRAIN
[PASS] B-SCOPED-JSON-SELF-CONSISTENT-AT-CORNER-GRAIN -- {"grain": "PATH-SCOPED", "counts": ".tools", "scanned": 388, "total": 388, "scored": 388, ... "prefix_filter_dropped": 0, "claim": "measured"}
[PASS] C-SCOPED-DENOMINATOR-MATCHES-INDEPENDENT-CENSUS -- tool denominator=388 of 388 ; independent `git ls-files -- .tools` census=388 ; shortfall=0 (tolerance 25)
[PASS] D-DENOMINATOR-MOVES-WITH-THE-PATH -- .tools -> 388 (census 388) ; org/modules/heatmap -> 8 (census 8) ; distinct=True
[PASS] E-NO-PATH-FORM-STILL-SCORES-THE-WHOLE-REPO -- no-path denominator=30563 (whole-repo census 30573, shortfall 10) ; .tools=388 ; org/modules/heatmap=8
[PASS] F-SCOPED-ANSWER-IS-PARITY-WITH-THE-UNSCOPED-ANSWER -- compared 388 scoped vs 388 unscoped-filtered rows: key-diff=0 band-diff=0 age-diff(>0.01d)=0 []
[PASS] G-GIT-ARGV-CARRIES-THE-PATHSPEC-PLUS-NEGATIVE-CONTROL -- scoped calls=3 all-pathspec=True log--full-history=True | NEGATIVE CONTROL unscoped calls=3 none-carry-a-pathspec=True
[PASS] H-RED-MUTANT-SCOPED-CALL-RETURNS-THE-REPO-DENOMINATOR -- mutant scoped org/modules/heatmap denominator=30563 (production scoped=8, production no-path=30563), wrapper prefix-filter dropped=30555 -- the mutant reproduces the pre-OS-s-2 defect
[PASS] H2-MUTATION-ANCHOR-UNIQUE
[PASS] I-HELP-DISCLOSES-THE-PATH-GRAIN
OS2-PATH-GRAIN BATTERY: 10/10 PASS (denominator 10)
```
**rc=0. 10 of 10 arms PASS** (the battery prints its own denominator). Also collected under pytest:
`1 passed in 16.95s`.

The two arms the criterion names explicitly:
- **the no-path form still scores the whole repo** -- arm E, and it is checked against an
  independent `git ls-files` census, not against the tool's own other reading.
- **a RED mutant returning the repo denominator for a scoped call** -- arm H. `_scope_pathspec()`
  is neutered in a **temporary copy of the engine outside the repository**, reached via comp-heat's
  own `COMP_HEATMAP_DIR` indirection, so neither `org/modules/heatmap/` nor `.tools/comp-heat` is
  rewritten. The mutant reproduces the pre-OS-s-2 defect exactly: a scoped call answers **30563**
  instead of 8. Without it, arms B-D would be vacuous.

## 4. HOW THE EVIDENCE AVOIDS THE TRAP THAT NEARLY MIS-GRADED `O1-AC2`

`O1-AC2` was first graded PASS by ranking 17 warm-OS-cache runs above 3 cold-cache runs. **Recency
and repetition are not provenance axes**, and the warm cache had been manufactured by that order's
own git calls. This cell's PASSes therefore do **not** rest on a wall-clock reading:

- The **deciding output for O2-AC1/O2-AC2 is a COUNT, not a duration** -- 388 and 8 against 30543
  and 30544. A count does not move with cache state.
- The **structural claim** ("the whole-history walk is no longer in the scoped code path") is
  measured by **arm G, which reads the git ARGV in process and carries its own negative control**
  (`scope=None` emits no pathspec). No clock is involved.
- **Timings are disclosed as cache-sensitive and are not load-bearing.** For completeness: at the
  git level on this worktree, the unscoped walk took 2.40-2.49 s warm (`W1-S1` measured 6.2-11.7 s
  cold) and the scoped walk 0.32-0.71 s; end to end the engine's own `used` went 5.25 s -> 0.55-1.22 s.
  The margin is stated as a range across the readings taken, not as the last one.
- **Parity is checked separately from cost** (arm F): the cheaper answer is the SAME answer --
  key-diff 0, band-diff 0, age-diff 0 over 388 of 388 paths.

## 5. REGRESSION + GATES

| check | result |
|---|---|
| `python .tools/tests/test_os1_budget_battery.py` (OS-s-1's battery) | `OS1-BUDGET BATTERY: 21/21 PASS (denominator 21)`, rc=0 |
| `python .tools/tests/test_comp_heat_battery.py` (pre-existing T20) | `Ran 2 tests ... OK`, rc=0 |
| `bash .tools/commit-gate.sh` on the 3 touched files | `OK: pre-commit gate clean for 3 of 3 file(s)`, rc=0 |
| `python .tools/surprise-row-gate.py` (at commit, staged) | `2 new row(s) of 16 total checked ... OK`, rc=0 |
| `bash .tools/comp-system --gate` (worktree-local, after regen) | `SYSTEM CURRENT (no genuine drift) -- gate open.`, rc=0 |

## 6. ROWS FILED (append-only, `INVESTIGATION_v1.md`, 14 -> 16 rows)

- **`NFRA_OUTSET-W1-S10`** -- the DISARM RECORD for `W1-S1` / `W1-S6` / `W1-S8`. The path-scoped git
  call is real and measured. **The residual is named rather than implied:** the no-path form still
  pays the whole-history walk by design, so those rows' hazard is closed **for a named corner
  only**. `hazard_standing: INERT`, stated for the scoped path and not for the tool as a whole.
  Their rows are not edited, reordered or re-dispositioned.
- **`NFRA_OUTSET-W1-S11`** -- ARMED, `disarm_owner: 2.0.0_SA_COO`. The `<paths>` grant of
  `infra/system/06_current_state.{json,md}` is **necessary but not sufficient** for a worker in a
  linked worktree, for two independent measured reasons: (1) comp-system refuses to compile from an
  uncommitted source (`SYSTEM BLOCKED-ON-PEER-LANDING ... Wait for landing, then re-run`, rc=2), so
  06 cannot ride the same commit as the change that dirties it; (2) `safe-commit.sh:789` resolves
  `comp-system` through PATH and `~/bin/comp-system` hard-codes the MAIN workspace, whose own
  `WORKSPACE=$(dirname $0)/..` fixes the graded tree there -- discriminated by the two runs
  reporting DIFFERENT target fingerprints (`7c2df46efc` vs `45ec711d24`) from the same baseline.

**How this order handled it, in the open:** the source landed with the gate's own audited
`system-current-override:` trailer (the same escape `W1-S5` recorded), reason logged to
`org/git-author-override-audit.log`; then `bash .tools/comp-system` was run worktree-local against
the LANDED source and the regenerated pair committed here. `0 changed rows across 26 regions in 6
files` -- no sibling doc outside the granted pair was touched.

## 7. DECLARED NON-APPLICATION

- **The no-path form's cost is unchanged and deliberately so.** It is the whole-estate question; the
  cell asks that a NAMED corner get its own denominator, and arm E asserts the no-path form still
  scores the whole repo. A caller passing no path still pays 5-8 s.
- **`tracked_last_write()` still drops ~10 of ~30 560 tracked paths repo-wide** (`W1-S3`, a
  pre-existing engine characteristic). Out of this cell's scope; the battery therefore asserts a
  BOUNDED shortfall against the independent census (tolerance 25) and PRINTS both numbers rather
  than asserting a bare equality that would hide it. Measured shortfall on both corners: 0.
- **`build()` (the unbudgeted twin) and `object_freshness.py --root`'s own CLI are untouched.** They
  have no scope parameter and no caller in this cell's path.
- **No new dependency, no second implementation, no alarm/monitor/freshness-checker, nothing
  deleted.** The mutant's temporary copy lives in `tempfile.mkdtemp()` outside the repository.

## 8. PUSH STATE

**LOCAL.** Nothing was pushed under this order. Measured with `git ls-remote` at report time -- see
the WORKER REPORT for the reading and its vintage.
