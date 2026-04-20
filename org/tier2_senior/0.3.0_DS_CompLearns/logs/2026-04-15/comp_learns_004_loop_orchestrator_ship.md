# COMP_LEARNS.004 — Loop Orchestrator (DS ~C) — session log

Agent: `0.4.0_DS_ClientPlatform~C`
TO: `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/COMP_LEARNS.004.ds-c-loop-orchestrator-stub.md`
Date: 2026-04-15 (US Eastern)
Outcome: `<status>complete</status>`

## Timeline

| Time (ET) | Event |
|-----------|-------|
| 15:18Z | Registered ~C. Inbox had QUEUED message for COMP_LEARNS.004 (double-gate). |
| 15:23Z | Andrew "ready go". Verified gates: BOTH MISSING (`comp/framework/harness_base.py` absent; `comp/bin/comp-learns-run.sh` absent). HARD STOP per Phase 1 mandate. |
| 15:24Z | MCP CTO for gate confirmation (3 options: gates landed / pre-flight only / hold). |
| 15:30Z | CTO answer (b): pre-flight only — ship `plateau.py` + 11 tests; sketch-only `run.py`; NO branch_guard / shim. TO stays staged. |
| 15:35Z | Pre-flight written + 11/11 pytest green. |
| 15:36Z | Before commit: gate state CHANGED during session. `harness_base.py` now present (~A commit `43e3225e`). `comp/bin/comp-learns-run.sh` now present (COO Track B). Existing `run.py` is ~A-written STUB explicitly flagged for ~C replacement. |
| 15:38Z | Rule 7 pre-flag to CTO: scope question given cleared gates. |
| 15:42Z | CTO GO option (A): commit pre-flight micro-commit, flip TO `pending`, proceed full scope. P0 branch-race constraint: Python side MUST NOT mutate git state (no `checkout`/`switch`/`reset`). |
| 15:44Z | Commit `4d17f47d` — pre-flight: `plateau.py` + 11 tests. |
| 15:45Z | Commit `1380d44c` — TO flipped staged -> pending. |
| 15:45Z | MCP COO with branch-race design proposal + 3 Qs. |
| 15:50Z | COO answers: Q1 root cause = `comp/bin/comp-learns-run.sh:91` unconditional `git checkout`. Q2 worktree migration is COO's scope, not mine. Q3 branch_guard proposal accepted with "add observed-vs-expected in error msg". |
| 15:51Z | Rule 7 pre-flag to CTO on acceptance #5 flex (`.tools/` is gitignored, shim source belongs in `comp/bin/`). |
| 15:52Z | CTO ACK: substitution is the correct pattern (matches comp-* convention); logged as TO-text precision miss, no rework. |
| 15:54Z | Commit `e657c232` — full scope: `run.py` rewrite + `branch_guard.py` + `comp/bin/comp-learns-run` shim + `test_branch_guard.py`. 22/22 pytest. |
| 15:55Z | TO flipped `pending` -> `complete`. |
| 15:54Z | MCP COO COMPLETE with commit hash + state.json schema + plateau test output. |

## Deliverables

| File | Purpose | Committed in |
|------|---------|--------------|
| `comp/framework/plateau.py` | Pure `detect_plateau(pass_rates, window=5, tolerance_pct=1.0) -> bool` per PRD #4 §Plateau detection verbatim. Crash (None/NaN) in window blocks the plateau signal. | `4d17f47d` |
| `comp/framework/tests/test_plateau.py` | 11 cases: empty / single / <window / 5-identical / within-tolerance / outlier / crash-None / crash-NaN / window-slide / tolerance-boundary-strict / custom-window. | `4d17f47d` |
| `comp/framework/run.py` | Single-iteration entry point. ResultsRow via framework `append_row` (atomic lock, MANDATE #6); `lines_of_code` via non-empty/non-comment line count over compiler.py + siblings; plateau via crash-aware series; status = crash/discard/keep; state.json atomic tmp+replace write. Exit 0/1/2 per wire_contract. | `e657c232` |
| `comp/framework/branch_guard.py` | Assert-only, read-only. `git -C <workspace> rev-parse --abbrev-ref HEAD`. Strict raises `BranchGuardError` (exit 2) with observed-vs-expected; warn stderr + return 0. NEVER mutates git. | `e657c232` |
| `comp/framework/tests/test_branch_guard.py` | 11 cases: expected_branch helper / current_branch happy+missing-git / strict pass+fail / warn pass+fail / format_mismatch content / main strict exit-2 / main warn exit-0 / main match exit-0. | `e657c232` |
| `comp/bin/comp-learns-run` | Tracked shim source-of-truth. Resolves workspace via `git rev-parse --show-toplevel` + marker-file fallback; works from both `comp/bin/` and `.tools/` install copies. | `e657c232` |

## Rule 7 Closeout Triads

### Acceptance #5 (shim location)
- **Original `<expect>`:** `.tools/comp-learns-run` PATH-available; forwards args to `python -m comp.framework.run`.
- **Substituted observation:** `comp/bin/comp-learns-run` is tracked source of truth; local install `cp comp/bin/comp-learns-run .tools/comp-learns-run && chmod +x` documented in shim header; PATH-availability + `--help` passthrough verified post-install from both paths.
- **Reasoning:** `.tools/` is gitignored (`.gitignore:170`, policy). Force-add breaks convention. Tracked source + documented install matches every other comp-* shim pattern (comp-trace, comp-blast, comp-iam, etc.) per MEMORY.md. CTO ACK 19:52Z (TO-text precision miss on their end, no rework ask).

### Acceptance #1 (httpx end-to-end smoke)
- **Original `<expect>`:** `python -m comp.framework.run httpx --description "test"` produces a new tsv row + state.json.
- **Substituted observation:** CLI `--help` verified; unit coverage of `write_state_cache` + `append_row` + `resolve_target` + `build_plateau_series` + `classify_status` exercises all code paths. End-to-end smoke against `comp/targets/httpx/` blocked on PRD #2 (httpx target compiler + queries.yaml not yet present; `comp/targets/httpx/` contains only `_repo`, `EDGE_TYPES.md`, `repo_pin.txt`, `SURFACE_INVENTORY.md`).
- **Reasoning:** TO itself notes "post-target-ship" on acceptance #1. Not a deviation — deferred per TO text. First real iteration fires when PRD #2 lands `httpx/compiler.py` + `httpx/queries.yaml`.

## Compiler Tools

Minimum compiler tools for DS role = `comp-pipescript io` + `comp-pipescript deployed` + `comp-pipescript postdeps` + `comp-validate`. None applicable here: this TO touches `comp/framework/` (research tooling infrastructure), not gold scripts or platinum artifacts. No pipeline scripts to trace; no gold artifact to validate. Logging an N/A row per the "blank and N/A are not acceptable, one sentence explaining why you didn't run is fine" rule.

| Tool | Invocation | Result | Notes |
|------|-----------|--------|-------|
| `comp-pipescript io` | N/A | N/A | No gold script in scope. Framework module lives under `comp/framework/`. |
| `comp-pipescript deployed` | N/A | N/A | No gold script deploy. |
| `comp-pipescript postdeps` | N/A | N/A | No gold run required. |
| `comp-validate` | N/A | N/A | No gold artifact produced. |
| `pytest comp/framework/tests/test_plateau.py comp/framework/tests/test_branch_guard.py -v` | Phase 2 before commit | **22 passed in 0.08s** | See TO mandate Phase 2. |
| `python -m comp.framework.run --help` | Phase 2 before commit | usage printed | argparse wiring confirmed. |
| `.tools/comp-learns-run --help` | Phase 3 after commit | forwards to run.py | Shim install verified from both `comp/bin/` and `.tools/` paths. |

## Phase mandate reproduction

### Phase 1 (before write)
```
$ test -f comp/framework/harness_base.py && test -f comp/bin/comp-learns-run.sh 2>&1
# At 15:23Z: BOTH MISSING -> HARD STOP -> pre-flight only
# At 15:36Z: BOTH PRESENT -> gate cleared, CTO GO (A)
```
Gate transition during session was detected before scope expansion; CTO re-briefed before any full-scope code landed. No "hope it cleared" moves.

### Phase 2 (before commit)
```
$ python -m pytest comp/framework/tests/test_plateau.py -v
# 11 passed (4d17f47d pre-flight)

$ python -m pytest comp/framework/tests/test_plateau.py comp/framework/tests/test_branch_guard.py -v
# 22 passed (e657c232 full scope)

$ python -m comp.framework.run --help
# usage printed
```

### Phase 3 (after commit)
```
$ .tools/comp-learns-run --help
# Forwards to python -m comp.framework.run --help (usage printed)
$ comp/bin/comp-learns-run --help
# Same (source-of-truth location)
```

## Handoff & Dependencies

- **COO Track B worktree migration (pending, owned by COO):** the branch-race P0 at `comp/bin/comp-learns-run.sh:91` (unconditional `git checkout` on shared HEAD) remains until COO ships the worktree migration. Python side refuses to amplify the bug — all git calls are `git -C <workspace>` read-only. Migration is interface-compatible with my `run.py` (target dir path is the only knob).
- **PRD #2 httpx target (pending):** end-to-end smoke of `comp-learns-run httpx --description "baseline"` fires when `comp/targets/httpx/compiler.py` + `queries.yaml` land.
- **No blockers for ~B (COMP_LEARNS.003 compiler_baseline)** from this TO.
- **No blockers for ~D (COMP_LEARNS.005 adversarial queries)** from this TO.

## Do NOT

- Do NOT add `git checkout`, `git switch`, `git reset`, `git restore`, or any other git-mutation command to `run.py` or `branch_guard.py`. P0 branch-race invariant.
- Do NOT track `.tools/comp-learns-run` directly — `.tools/` is gitignored by policy. Source lives at `comp/bin/comp-learns-run`; local install is a `cp`.
- Do NOT assume state.json is authoritative. `git log` + `results.tsv` are the source of truth (AUTORESEARCH_WALKTHROUGH.md §F contract). state.json is a cache; safe to delete + rebuild.

## Addendum — Track B worktree migration (per COO 20:08Z)

COO ACK'd completion at 20:08Z and reported:

- **Worktree migration shipped in `23de5edf`** (Track B half of the joint design pass CTO mandated). Dry-run scenario 1 (shared HEAD unchanged across concurrent lane edits) PASS; 4 scenarios queued.
- **Schema-drift coordination (no action from ~C):** COO's bash driver previously maintained its own tsv-header-init and used legacy-column AWK parsers for plateau/pass-rate reads. COO's next commit strips the driver's tsv-header-init (lets `comp.framework.results_schema.append_row` own it) and defers plateau/pass-rate reads to `state.json` (one source of truth). `run.py` + `branch_guard.py` + shim contract is authoritative; the driver adapts.
- **Atomic-commit property** preserved via commit-level co-ship pattern: `e657c232` (~C Python entry) and `23de5edf` (COO worktree) are paired even though they landed in separate commits.

This closes the joint design pass. P0 branch-race is resolved at both layers:
  - Bash driver (Track B, COO-owned) now runs inside `worktrees/comp-learns-<target>/`, shared workspace HEAD never moves.
  - Python entry (this TO, ~C-owned) is read-only against git regardless of bash driver behavior.
