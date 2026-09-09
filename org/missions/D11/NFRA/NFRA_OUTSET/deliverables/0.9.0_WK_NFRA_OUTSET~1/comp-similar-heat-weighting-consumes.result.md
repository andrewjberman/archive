# TO-OS-s-8 result -- comp-similar's heat weighting now CONSUMES comp-heat

**TO:** `NFRA_OUTSET.TO-OS-s-8` (`org/missions/D11/NFRA/NFRA_OUTSET/task-orders/NFRA_OUTSET.TO-OS-s-8.comp-similar-heat-weighting-consumes.md` @`b000632f27`)
**Cell:** `OS-s-8` · **outcome_ref:** FWD-7 · **verb:** wire · **depends_on:** OS-s-1 (`b3bf6c98d8`)
**Executed by:** `0.9.0_WK_NFRA_OUTSET~2` in worktree `C:/tmp/wk-OUTSET-2`, branch `wk-OUTSET-2`, base HEAD `79ec54bb37`
**Deliverable folder:** the order names `deliverables/0.9.0_WK_NFRA_OUTSET~1/` while spawning this work on slot 2 -- see row `NFRA_OUTSET-W2-S3`. This document is written at the path the order names, because that is the path its `<paths>` grant admits.

**Landing history (the order was BLOCKED and then unblocked):** the first commit attempt was
refused on 3 of 4 pathspecs -- `owned-paths-validate.py:213-215` keys the worker grant on
`<issued_to>` and the order then read `~1`. Filed as `NFRA_OUTSET-W2-S4` (BLOCKING) with a
positive control discriminating on the serial alone (4 of 4 granted to `~1`, 0 of 4 to `~2`).
`2.0.0_SA_COO` amended `<issued_to>` to `~2` on CLOUD at `b630052d6a`. The amendment was carried
onto this branch and COMMITTED before the artifacts, because the grant is read with
`git show HEAD:<order>` (`owned-paths-validate.py:173-181`, "a task order staged but absent at
HEAD grants nothing yet") -- measured: with the amended file present in the worktree AND staged,
the grant still returned 0 of 4; after the carry-in commit it returned 5 of 5. Filed as
`NFRA_OUTSET-W2-S6`.

---

## 1. WHAT I MEASURED -- the cell named one defect and the world held three

The cell (PRD s.7 row `OS-s-8`): *"`load_heat_live` at org/modules/graph/debtscan/comp_similar.py:346 returns an empty dict before reaching comp-heat"*.

The empty dict is real. Its cause is not where the cell puts it, and two further defects sit beneath it that an empty dict never reveals -- they produce a large, confident, entirely blind heat map instead.

| # | Defect | Where, at `79ec54bb37` | Measured before |
|---|---|---|---|
| 1 | **EXEC** | `comp_similar.py:373` built `subprocess.run([str(REPO/".tools"/"comp-heat"), ...])`. The shim is extensionless with a shebang; on this fabric that argv raises `OSError [WinError 193] "%1 is not a valid Win32 application"`. `_run_json:307-314` catches `OSError` and returns `None`, the out-file is never written, and `load_heat_live` returns `{}`. There is **no early return** in `load_heat_live` -- its control flow always reaches the comp-heat call; the exec plane is what stops it. | 2 of 2 shims tried (`comp-heat`, `comp-debris`), 0 of 2 executed |
| 2 | **FIELD** | `comp_similar.py:342` read `row.get("class", "")`. `comp-heat freshness` emits `band` (`hot`/`warm`/`cold`) and has never emitted `class`. | `comp-heat freshness .tools/tests --json OUT` -> 43 of 43 rows carry `band`, 0 carry `class`; `normalize_heat` banded **43 of 43 UNKNOWN** |
| 3 | **KEY** | `comp_similar.py:341` keyed the data band by `os.path.basename(path)`. Corpus names are AWS resource names; repo basenames are files. | **0 of 1774** corpus names joined a basename. basename-stem joined 70; path-component+stem joined 184 |

Defects 2 and 3 are the reason this cell matters more than its own wording: neither returns an empty dict. Before the fix, a `--heat-json` run offered ~30 000 heat keys, banded every one `UNKNOWN`, printed `heat: source=..., 30546 resources banded`, and then printed a confident **`0 candidates`** -- a measured-looking zero produced by a completely blind read.

### 1a. THE FAILURE WORE THE SHAPE OF A CLEAN ANSWER

This is the load-bearing finding, and it is not a detail of this cell. **The order named the one
defect that announces itself; the two it did not name are the dangerous ones precisely because
they do not.** An empty dict is loud -- `heat_present` goes false, the tool prints `NO HEAT
SOURCE -> 0 supersede verdicts`, and a reader knows the answer is missing. A `class`-vs-`band`
field read and an `os.path.basename` join are silent: they raise nothing, return nothing empty,
and hand the caller a large well-formed heat map in which every band is `UNKNOWN`. The tool then
does exactly what it was designed to do with heat that shows no divergence -- it emits **zero
candidates** -- and prints that zero beside a confident five-figure denominator.

So a fix aimed only at the named symptom would have gone GREEN while the consumer stayed blind:
the exec seam would have started reaching comp-heat, `load_heat_live` would have stopped returning
`{}`, the criterion as literally worded would have been satisfied, and `comp-similar supersede`
would have kept printing `0 candidates` from a completely unread heat axis. **The verification
that would have caught it is not "did the empty dict go away" but "how many CORPUS resources
carry a band" -- a denominator the tool did not previously compute about itself.** That is why
`heat_banded` (s.2) is part of the deliverable and not a nicety: the wire and the measurement of
the wire are the same act, and without the second one the first cannot be graded.

Recorded at the issuer's request as a member of a recurring family on this project: **a defect
whose observable signature is indistinguishable from a clean answer.** Its tell here is a zero
printed next to a large denominator, with nothing in the output stating which of the two the zero
came from -- the population being empty, or the instrument being blind. The repair carries that
distinction into the output itself (`HEAT READ BUT 0 OF <N> CORPUS RESOURCES BANDED ... a BLIND
result, not a measured zero`), so the next occurrence of the same family on this seam announces
itself instead of passing.

## 2. WHAT I CHANGED -- all inside `org/modules/graph/debtscan/comp_similar.py`

| Change | New location | What it does |
|---|---|---|
| `_tool_argv(tool, *args)` | `:323` | Resolves the interpreter from the shim's own shebang: python shims run under `sys.executable`, bash shims under Git Bash via the estate's `.tools/git_bash_resolver.py` `bash_argv()` (build-ladder rung 2 -- no new dependency, no second implementation, and never bare `bash`, the WSL-stub trap). Used for **both** `comp-debris` and `comp-heat`. |
| `normalize_heat` branch (c) | `:354`, branch at `:381-397` | Reads `band` with `class` kept only as a back-compat alias for a hand-rolled snapshot; keys the data band under the basename, its stem, and **every path component + stem**, so a resource whose source directory carries its name joins. |
| `_merge_band` + `_BAND_RANK` | `:151-165` | Collision resolution, replacing an order-dependent `setdefault`: **HOT wins, then WARM, then COLD, then UNKNOWN.** Never let one cold path make a resource look colder than its hottest evidence -- the cold member of a divergent pair is emitted as a decommission CANDIDATE and NEVER-AUTO-DELETE (PRD R-5) makes the conservative direction the only safe one. Deterministic: independent of row order. |
| `--budget` pass-down | `:429-435` | **This is the OS-s-1 consumption.** OS-s-1 wired Rule T's `--budget` across comp-heat's five subcommands; `load_heat_live` now hands comp-heat the caller's REMAINING budget instead of letting the child silently run to its own 90 s default inside a possibly-shorter outer subprocess timeout and report `WITHIN BUDGET` against the wrong clock. |
| `heat_banded` | `:853` and the print/JSON block | **The consumption measurement.** `len(heat)` counted keys the heat source OFFERED, which is not the question; `heat_banded` counts CORPUS resources the heat actually reached with a usable band, printed with its denominator. `heat_present` now keys on it, so an all-UNKNOWN map no longer reads as heat present, and a heat source that joins nothing prints `HEAT READ BUT 0 OF <N> CORPUS RESOURCES BANDED ... this is a BLIND result, not a measured zero` instead of a confident `0 candidates`. That clause is the cell's *"the empty-result path is gone or declared"*. |

**Not changed and deliberately so:** `.tools/comp-similar` (the 2-line shim needed nothing -- the defect was entirely in the engine), `.tools/comp-heat` (not in this order's `<paths>`, and another worker is writing it), and the 15 other call sites of the same exec class (row `NFRA_OUTSET-W2-S2`).

## 3. ACCEPTANCE

### O8-AC1 -- MECHANICAL -- PASS by output

**Invocation:** `timeout 120 python .tools/tests/test_os8_heat_consumed.py` · **expect:** `PASS` · **rc = 0**

```
=== OS-s-8 O8-AC1: comp-similar CONSUMES comp-heat (GREEN arms + RED mutants) ===
  PASS  A1 exec GREEN (_tool_argv reaches comp-heat): comp-heat wrote 30551 freshness row(s) via _tool_argv; _run_json stdout parsed=False
  PASS  A1 exec RED MUTANT (bare shim argv cannot reach comp-heat): bare argv raised OSError: [WinError 193] %1 is not a valid Win32 application -- exactly what _run_json swallowed into {}
  PASS  A2 field GREEN (comp-heat 'band' is read): 51855 of 51855 heat key(s) carry a non-UNKNOWN data band from 30551 comp-heat row(s); source bands seen=['COLD', 'HOT', 'WARM']
  PASS  A2 field RED MUTANT (pre-fix reader on the SAME bytes): pre-fix normalize_heat banded 0 of 25476 key(s) -- all UNKNOWN (denominator 30551 comp-heat rows)
  PASS  A2 provenance (every emitted band is a comp-heat band): emitted=['COLD', 'HOT', 'WARM'] subset of comp-heat's own=['COLD', 'HOT', 'WARM']
  PASS  A3 end-to-end GREEN (comp-similar output carries comp-heat's numbers): rc=0; heat_banded=208 of 1929 corpus resources; 8 of 8 candidate(s) cite a comp-heat band; heat_source=snapshot:C:\Users\ANDREW~1\AppData\Local\Temp\os8_heat_cuklxe62\heat_full.json
  PASS  A3 end-to-end RED MUTANT (pre-fix reader -> heat in name only): rc=0; heat_banded=0 of 1929 from 25476 key(s) offered; candidates=0
  PASS  A3 end-to-end RED MUTANT (load path returns the empty dict): rc=0; heat_keys=0; heat_banded=0; candidates=0
=== test_os8_heat_consumed: PASS (8/8) in 81.5s ===
```

**Denominator: 8 of 8 arms PASS**, printed by the battery on its own final line. Three RED mutants, one per defect, each EXECUTED (not described):

- `A1 exec RED` restores the pre-fix bare argv and shows the OSError that produced the empty dict. It is fabric-conditional and says so in its own detail line rather than scoring a dead control silently.
- `A2 field RED` runs the pre-fix reader (`class` + basename key, restored verbatim in behaviour) over the **same real comp-heat bytes** and bands 0 of 25476 keys.
- `A3 end-to-end RED` x2: the pre-fix reader against the same corpus, same snapshot, same argv -> `heat_banded=0`, `candidates=0`; and the literal empty-dict path (`normalize_heat -> {}`) -> `heat_keys=0`, `candidates=0`.

The battery exercises REAL comp-heat bytes (a whole-repo `comp-heat freshness --json OUT --budget 60`, 30 551 rows) rather than a fixture, because a fixture written from the implementation would have carried the same `class`-vs-`band` assumption that caused the defect. It never invokes comp-debris (live AWS, minutes). Every subprocess and every scan carries an explicit budget; the corpus build (~37 s) is paid once via a harness cache over the corpus LOADER, never over the code under test.

**Regression:** `timeout 120 python .tools/tests/test_comp_similar_battery.py` -> `=== comp-similar battery: PASS (12/12) ===`, rc 0. `timeout 120 bash .tools/comp-similar --self-test` -> `=== comp_similar self-test: PASS (11/11) ===`, rc 0.

### O8-AC2 -- JUDGMENT (`judgment="true"`) -- EVIDENCE ONLY, NO VERDICT

Graded by `3.0.0_SA_CVO` at L9. What the criterion asks for, in order:

**(a) `load_heat_live` BEFORE, at file:line** -- `org/modules/graph/debtscan/comp_similar.py:346-386` @`79ec54bb37` (`git show HEAD:...`), the two lines that decide the outcome:

```
346: def load_heat_live(timeout=280, *, clock=None, deferred=None) -> dict:
...
367:    dbg = (_run_json([str(REPO / ".tools" / "comp-debris"), "--json"],
368:                     timeout=debris_timeout) if debris_timeout != 0 else None)
...
373:        _run_json([str(REPO / ".tools" / "comp-heat"), "freshness", "--json", str(out_json)],
374:                  timeout=heat_timeout)
```

and the swallow that turns both into `{}`:

```
307: def _run_json(cmd, timeout=180):
308:     try:
309:         p = subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=timeout)
...
313:     except (subprocess.SubprocessError, OSError, ValueError):
314:         return None
```

and the two lines beneath it, `comp_similar.py:341-342` @`79ec54bb37`:

```
341:            base = os.path.basename(str(row["path"]).rstrip("/"))
342:            heat.setdefault(base, {}).setdefault("data", _norm_band(row.get("class", "")))
```

**(b) `load_heat_live` AFTER, at file:line** -- `comp_similar.py:400-440` (worktree, this commit):

```
400: def load_heat_live(timeout=280, *, clock=None, deferred=None) -> dict:
...
420:    dbg = (_run_json(_tool_argv(REPO / ".tools" / "comp-debris", "--json"),
421:                     timeout=debris_timeout) if debris_timeout != 0 else None)
...
429:        heat_args = ["freshness", "--json", str(out_json)]
430:        # OS-s-1 wired Rule T's --budget across comp-heat's five subcommands. Hand the CALLER's
431:        # remaining budget down, or the child silently runs to its own 90s default inside a
432:        # possibly-shorter outer timeout and reports WITHIN BUDGET against the wrong clock.
433:        if heat_timeout is not None:
434:            heat_args += ["--budget", str(max(1, int(heat_timeout)))]
435:        _run_json(_tool_argv(REPO / ".tools" / "comp-heat", *heat_args), timeout=heat_timeout)
```

with `_tool_argv` at `:323` and the repaired join at `:381-397`.

**(c) One real comp-similar run showing heat numbers in its output.**

```
$ timeout 120 python .tools/comp-heat freshness --json .scratch/ac2_heat.json --budget 60   # rc=0
$ timeout 120 bash .tools/comp-similar supersede --heat-json .scratch/ac2_heat.json --budget 90 --top 6   # rc=0

WITHIN BUDGET: scanned 1929 of 1929 ARN resource; budget: 90 s (flag), used 44.48 s
DEFERRED: 0 of 0 heat subprocess(s) did not return -- each names its reason below
ANSWER-STATE: PARTIAL_OR_BLIND -- corpus built: UNKNOWN -- vintage undisclosed by the retrieval; DO NOT read this denominator as current
corpus built: UNKNOWN -- vintage undisclosed by the retrieval; DO NOT read this denominator as current
scanned 1929 ARN resources; 1560 with purpose summary; 369 UNKNOWN-thin (no twin known); 29 hold-marked; ...
heat: source=snapshot:.scratch/ac2_heat.json, 208 of 1929 corpus resources banded from 51861 heat key(s) (UNKNOWN heat -> never a candidate -- C3)

=== superseded-twin candidates (advisory; verify before reap) [6] ===
  [MEDIUM sim=1.002] yang-canon-interlock  ->replaced by->  yang-generate-peer-performance  cold{'data': 'COLD', 'invoke': 'UNKNOWN'}
  [MEDIUM sim=1.002] yang-generate-correlation  ->replaced by->  yang-generate-peer-performance  cold{'data': 'COLD', 'invoke': 'UNKNOWN'}
  [MEDIUM sim=1.002] yang-generate-etf-returns  ->replaced by->  yang-generate-peer-performance  cold{'data': 'COLD', 'invoke': 'UNKNOWN'}
  [MEDIUM sim=1.002] yang-generate-factor-tilts  ->replaced by->  yang-generate-peer-performance  cold{'data': 'COLD', 'invoke': 'UNKNOWN'}
  [MEDIUM sim=1.002] yang-generate-macro  ->replaced by->  yang-generate-peer-performance  cold{'data': 'COLD', 'invoke': 'UNKNOWN'}
  [MEDIUM sim=1.002] yang-generate-macro-timeseries  ->replaced by->  yang-generate-peer-performance  cold{'data': 'COLD', 'invoke': 'UNKNOWN'}
```

**The same invocation shape on the same corpus before the change** printed `heat: source=..., 30546 resources banded` and `0 candidates` -- the `heat_banded` denominator and the `data: COLD` on every candidate row are comp-heat's numbers arriving where they never arrived before. The `ANSWER-STATE: PARTIAL_OR_BLIND` line that remains is the CORPUS VINTAGE arm (`corpus built: UNKNOWN`), a pre-existing, separately-owned disclosure, not the heat arm -- the heat arm no longer contributes `heat source absent` to it.

**The empty path is not gone; it is DECLARED**, which is the other half of the cell's bar. `--live-heat` still returns `{}` if both subprocesses fail, and a `--heat-json` snapshot that joins nothing still yields zero -- but the tool now says so in its own voice (`HEAT READ BUT 0 OF <N> CORPUS RESOURCES BANDED ... a BLIND result, not a measured zero`) instead of printing a confident `0 candidates`.

**A limit this worker does not soften:** 208 of 1929 is the join rate, not 1929 of 1929. comp-heat freshness is REPO-path-scoped and the corpus is AWS resources -- the docstring at `:400` has always said so, and only a resource whose name appears in a repo path can be banded from this source. The remaining 1721 stay `UNKNOWN`, which under control C3 means never a candidate. That is the honest ceiling of comp-heat-as-a-data-heat-source, not a defect in this wire; the `--heat-json` snapshot seam is what lets a better source (a per-bucket data-heat snapshot) be substituted without touching this code.

## 4. GATES

| Gate | Invocation | Result |
|---|---|---|
| commit-gate | `timeout 120 bash .tools/commit-gate.sh org/modules/graph/debtscan/comp_similar.py .tools/tests/test_os8_heat_consumed.py` | `OK: pre-commit gate clean for 2 of 2 file(s)`, rc 0 |
| ruff (py39) | `timeout 120 python -m ruff check --target-version py39 <both files>` | `All checks passed!`, rc 0 |
| comp-system | `timeout 120 comp-system --gate --changed org/modules/graph/debtscan/comp_similar.py .tools/tests/test_os8_heat_consumed.py` | `NOT_APPLICABLE: ... no comp-system _SOURCE in the changeset; not a trigger-surface commit, gate open`, **rc 0** |

`infra/system/06_current_state.{json,md}` was GRANTED by the order against the `safe-commit.sh:789` trigger. **Measured, not assumed: the gate returns rc 0 NOT_APPLICABLE on this changeset**, so there is nothing to regenerate and this order does not touch that pair. The grant was correct to make and correct not to use.

## 5. ROWS FILED

| id | class / hazard | one line |
|---|---|---|
| `NFRA_OUTSET-W2-S1` | OBSERVATION / INERT | the cell named one defect; the world held three stacked, and two of them produce a confident zero rather than an empty dict |
| `NFRA_OUTSET-W2-S2` | OBSERVATION / **ARMED** (`disarm_owner: 2.0.0_SA_COO`) | the exec cause is a CLASS -- a python module subprocessing an extensionless `.tools/` shim gets `OSError` and an `except OSError: return None` turns it into a clean-looking empty result; 16 of 269 `org/modules/**.py` are candidate call sites, 15 of them outside every `<paths>` grant this project has cut |
| `NFRA_OUTSET-W2-S3` | OBSERVATION / **ARMED** (`disarm_owner: 2.0.0_SA_COO`) | CUT DEFECT: `<issued_to>` is `~1` and every deliverable path is under `deliverables/0.9.0_WK_NFRA_OUTSET~1/`, but the order was spawned to `~2`; the row coordinate must be W2 and the folder must be the `~1` path, so the two cannot be reconciled by choosing one |

## 6. DECLARED NON-APPLICATIONS

- **`.tools/comp-similar` unchanged** -- the shim forwards `"$@"` to the engine; the defect was entirely engine-side and the shim's help text already documented `--heat-json` and `--live-heat` correctly.
- **`comp-debris` (the invoke axis) not exercised end to end** -- it is a live-AWS scan measured in minutes and the cell's verb is the comp-heat wire. Its argv is repaired by the same `_tool_argv` and covered by the A1 exec arm; every candidate above therefore still shows `invoke: UNKNOWN`, honestly, which under C3 caps confidence at MEDIUM.
- **No shared exec helper extracted** -- `.tools/` beyond `.tools/comp-similar` and `.tools/tests/` is not in this order's `<paths>`; row `NFRA_OUTSET-W2-S2` is the carrier so the work is not done off-grant.
- **No monitor, alarm, freshness-checker or SNS** built (standing moratorium). **No delete verb, no removal** -- the candidate list is advisory (PRD R-5).
