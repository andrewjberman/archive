# 1.2.0_DS_CompLearns — Session Log 2026-04-27

**TO:** COMP_LEARNS.071 — INVESTIGATE pilot machinery (R-DS-2)
**Outcome:** SHIPPED
**Commit:** 710c973e

---

## Objective

Implement non-ratchet INVESTIGATE pilot runner mode: paired C4+C1 N=8 trials per question, dual-condition gate (PRD §5.2, CVO R-DS-2), pilot artifact schema per §5.2.

---

## Work Completed

### Phase 0 — Baseline gate
- `pytest comp/ --ignore=comp/targets -q --tb=no`: 458 passed. PASS.

### Phase 1 — Implementation

**comp/loop/runner.py:**
- Added `import datetime` and `import math` to module-level imports (removed local `import datetime` inside `do_halt`).
- Added `PilotConfig` dataclass: `judge_mode`, `questions: list`, `n: int = 8`, `compiler_content_sha: str = ""`.
- Added `_pilot_decision_rule(c4, c1, n)` — dual-condition gate. Thresholds computed as fractions of N (not hardcoded): `promote_floor = ceil(5/8*N)`, `demote_ceiling_max = floor(1/8*N)`, `demote_prior_floor = floor(6/8*N)`. Returns `(decision, rule_description)`.
- Added `_run_n_trials(judge, system_prompt, user_msg, n, answer_entry)` — runs N independent judge calls, grades with `_grade_response` from ab.py, returns `list[bool]`.
- Added `run_pilot(target, cfg)` — full non-ratchet pilot runner:
  - Compiles graph once via `_load_compiler` + `compiler_fn(target_root)`
  - Uses `KeywordSelector` for C4 context (mechanical addressing per PRD §5 four-condition table)
  - Empty context for C1 (unaided)
  - Writes `pilot_<qID>.json` per question and `pilot_summary.json` to `comp/results/<target>/pilot/<timestamp>/`
  - Does NOT touch `champion.json`, `experiment_log.jsonl`, or any ratchet state
  - Returns `ExitCode.THRESHOLD_REACHED` (exit 0) on success

**comp/bin/comp-learns-ratchet:**
- Imported `PilotConfig` and `run_pilot` from `comp.loop.runner`
- Added `--pilot` to the mutually exclusive mode group
- Added `--questions` (comma-separated qIDs) and `--n` (int, default 8) arguments
- Added pilot handling in `main()`: validates `--judge` and `--questions` required, parses question list, constructs `PilotConfig`, calls `run_pilot`

**comp/loop/tests/test_pilot_decision_rule.py (new, 22 tests):**
- `TestPilotDecisionRuleN8`: boundary cases for N=8 (PROMOTE min-delta, DEMOTE_CEILING boundary, DEMOTE_PRIOR_DOMINATED, HOLD middle, delta-only HOLD)
- `TestPilotDecisionRuleGeneralN`: N=4 and N=16 cases verifying threshold scaling
- `TestPilotDecisionRuleDescription`: rule description strings contain threshold values

### Phase 2 — Pre-commit gate

| File | Gate | Result |
|------|------|--------|
| `comp/loop/runner.py` | `.tools/ds-commit-gate.sh` | PASS (All 3 checks exit 0) |
| `comp/bin/comp-learns-ratchet` | `python -m py_compile` + `ast.parse` | PASS |

`pytest comp/ --ignore=comp/targets -q --tb=short`: **480 passed, 0 failed** (+22 new pilot tests).

### Phase 4 — Smoke test

```
python comp/bin/comp-learns-ratchet click --pilot --questions q03 --n 4 --judge mock
```

Output:
```
[pilot] q03: C4=4/4 C1=0/4 delta=4 -> PROMOTE
[pilot] artifact: .../comp/results/dev-click-001/pilot/20260427T173654Z/pilot_q03.json
[pilot] summary: .../comp/results/dev-click-001/pilot/20260427T173654Z/pilot_summary.json
[pilot] promote=1 demote_ceiling=0 demote_prior=0 hold=0
```

Artifact check:
- `decision: PROMOTE`, `c4: 4`, `c1: 0`, `schema_version: 1`, `n_trials: 4`, `delta: 4`
- `decision_rule: "c4_successes >= ceil(5/8*N)=3 AND delta >= 2"`

Non-ratchet verification:
- `experiment_log.jsonl`: 7 entries [1-7] — unchanged
- `champion.json`: sha=7beb09b — unchanged

### Phase 5 — Commit + push

- Commit: `710c973e` — author `1.2.0_DS_CompLearns`
- Push: `9254655c..710c973e CLOUD -> CLOUD` from feature_clb

---

## Decisions Made

- KeywordSelector used for C4 context: matches "mechanical addressing" in PRD §5 four-condition table (C4 = background_index=True, addressing=mechanical).
- Thresholds computed as `math.ceil` / `math.floor` fractions of N — correct for arbitrary N, not hardcoded for N=8.
- Smoke test pilot artifacts NOT committed — mock run artifacts have no research value.
- `list` used as type annotation for `PilotConfig.questions` (not `list[str]`) since `from __future__ import annotations` is already in runner.py.

---

## Files Modified

| File | Change |
|------|--------|
| `comp/loop/runner.py` | +`PilotConfig`, `_pilot_decision_rule`, `_run_n_trials`, `run_pilot`; `import datetime`/`math` added top-level |
| `comp/bin/comp-learns-ratchet` | `--pilot` mode, `--questions`, `--n` flags; `PilotConfig`/`run_pilot` imported |
| `comp/loop/tests/test_pilot_decision_rule.py` | NEW — 22 unit tests for decision rule |

---

## Blockers

None.

---

## Current State

COMP_LEARNS.071 complete. Pilot machinery live on CLOUD at 710c973e.

---

## Next Steps

Await pilot execution dispatch (gated on .075 pre-screen + .076 CTO off-ramp per TO cross-domain notes).

---

## Compiler Tools

| Phase | Run | Expected | Observed | Pass/Fail |
|-------|-----|----------|----------|-----------|
| Before write | `pytest comp/ --ignore=comp/targets -q --tb=no` | 458 passed, 0 failed | 458 passed in 63.13s | PASS |
| Before commit | `.tools/ds-commit-gate.sh comp/loop/runner.py` | All 3 checks exit 0 | All checks passed! | PASS |
| Before commit | `python -m py_compile comp/bin/comp-learns-ratchet` | exit 0 | exit 0 | PASS |
| Before commit | `pytest comp/ --ignore=comp/targets -q --tb=short` | 458+ passed, 0 failed | 480 passed in 36.32s | PASS |
| Smoke test | `comp-learns-ratchet click --pilot --questions q03 --n 4 --judge mock` | artifact written, valid decision | pilot_q03.json PROMOTE c4=4 c1=0 | PASS |
