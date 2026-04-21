# 1.4.0_DS_CompLearns — Session Log 2026-04-21

**TO:** COMP_LEARNS.015 (bench-scorecard-ab)
**Outcome:** COMMITTED — all Phase 1 + Phase 2 gates PASS; CTO ACCEPT received 20260421T171634Z; commit cleared

---

## Objective

Implement bench scorecard + structural scorer + A/B comparator with model-agnostic JudgeBackend
protocol, v3 ratchet-critical/exploratory scorecard split, and v3 cached-answer regime.

---

## Work Completed

1. Phase 1 gates all PASS (anthropic 0.84.0, deps ok, ratchet_critical_call signature correct,
   gold files present).
2. Flipped .015 staged -> pending.
3. Sent wire-contract consult to 1.1.0_DS_CompLearns (20260421T171216Z). Awaiting ack.
4. Implemented all scope:
   - `comp/bench/primary.py` — primary_metric formula (ab_lift * (1+alpha*token_reduction) *
     mutation_stability * (1-conflict_penalty)), alpha=0.3, SelectorGameDetected check.
   - `comp/bench/structural.py` — precision/recall/F1 vs gold JSONL; heuristic discount (weight 0.5)
     in denominator; per-subtype + aggregate.
   - `comp/bench/behavioral.py` — thin adapter over comp.framework.harness_base.
   - `comp/bench/efficiency.py` — extraction_time (bucketed), graph_size_bytes, peak_memory_mb.
   - `comp/bench/generalization.py` — v0 unevaluated=True stub.
   - `comp/bench/ab.py` — A/B comparator with full cached-answer regime. warm_up_cache writes
     to ABCache; run() uses require_hit (raises CacheMissDuringPrimaryMetric on miss). Uses real
     SelectedContext API (selector.select(question, graph, token_budget=N) -> SelectedContext).
   - `comp/bench/ab_answer_key_validator.py` — added validate_gold_survey_attestation() per
     AC #7 (COMP_LEARNS_TARGET_CLOSEOUT §7.1). Raises GoldSurveyAttestationMissing when
     dimension coverage < 100% and attestation missing or lacks grep evidence.
   - `comp/bench/scorecard.py` — additive extension: token_reduction_pct: float = 0.0 added to
     SelectorAB; serializers updated for round-trip safety.
   - `comp/bench/__init__.py` — updated public surface to export .015 symbols.
   - Selector stubs: added centrality.py, harness.py stubs; real .020 implementation shipped at
     d6e9f1fb (CTO) before my session ended.
5. Test files written:
   - `comp/bench/tests/test_scorecard_eq.py` — 11 tests, Scorecard.__eq__ discipline
   - `comp/bench/tests/test_primary_metric.py` — 8 tests, formula + determinism + exploratory isolation
   - `comp/bench/tests/test_selector_game_detected.py` — 6 tests, random-wins trigger
   - `comp/bench/tests/test_cached_answer_regime.py` — 4 tests, cache-miss halt + warm-up
   - `comp/bench/tests/test_gold_survey_attestation.py` — 5 fixture tests (a-e)
   - `comp/bench/tests/test_structural_scorer.py` — 5 tests, F1 + heuristic discount
   - `comp/bench/tests/test_ab_selector_integration.py` — 3 tests, per-selector + argmax
6. Full pytest comp/bench/ -v: 138/138 PASSED.
7. ds-commit-gate.sh: OK for all 18 new .py files.

---

## Decisions Made

- **token_reduction_pct added to SelectorAB:** Wire contract in TO requires it for primary_metric
  formula. Added as default=0.0 additive field — backward compatible, serializers updated.
- **ab.py uses real SelectedContext API from .020 selectors.base:** Conforms to actual Selector
  protocol (question, graph, *, token_budget) -> SelectedContext, not a simplified tuple return.
- **structural.py heuristic discount direction:** Heuristic wrong edges penalize precision LESS than
  certain wrong edges (weight 0.5 in denominator). Correct per §5.1 — heuristic predictions are
  discounted, not excluded.
- **SelectorGameDetected in primary.py, not ab.py:** Check fires after DownstreamAB is populated;
  cleaner in primary.py alongside the formula that uses best_lift.

---

## Blockers

Commit blocked on:
1. `.014` (GraphBuilder full impl) landing from 1.3.0_DS_CompLearns — Phase 2 real GraphBuilder
   tests need the actual build/dedup/conflict logic to be non-stub.
2. 1.1.0_DS_CompLearns wire-contract ack (30-min silence window started 20260421T171216Z).

---

## Current State

COMP_LEARNS.015 pending. All Phase 2 tests green. Holding commit until .014 lands.
1.3.0 is actively writing .014 (GOd by COO at dcdfa5a0 session). Expected soon.

---

## Compiler Tools

| Phase | Run | Expected | Observed | Pass/Fail |
|-------|-----|----------|----------|-----------|
| .015 Phase 1 Step 1 | `import anthropic; print(anthropic.__version__)` | version string | 0.84.0 | PASS |
| .015 Phase 1 Step 2 | `from comp.bench import Scorecard...; from comp.graph_builder import GraphBuilder, BuildResult; print('deps ok')` | `deps ok` | `deps ok` | PASS |
| .015 Phase 1 Step 3 | `from comp.bench.judges.base import JudgeBackend; sig = signature(JudgeBackend.ratchet_critical_call); print(sig)` | ratchet_critical_call signature | `(self, system, user, *, max_tokens=1024, seed=None, **kwargs)` | PASS |
| .015 Phase 1 Step 4 | `ls comp/targets/httpx/gold/ab_questions.yaml ab_answer_key.yaml` | both files exist | both files present | PASS |
| .015 Phase 2 Step 1 | `pytest comp/bench/tests/test_judge_protocol.py -v` | all pass, exit 0 | 10/10 PASSED | PASS |
| .015 Phase 2 Step 2 | `pytest comp/bench/tests/test_cached_answer_regime.py -v` | cache miss -> halt; warm-up succeeds | 4/4 PASSED | PASS |
| .015 Phase 2 Step 3 | `pytest comp/bench/tests/test_ab_answer_key_validator.py -v` | open-ended ratchet -> rejected | 10/10 PASSED | PASS |
| .015 Phase 2 Step 4 | `pytest comp/bench/tests/test_scorecard_eq.py -v` | emitted_at excluded, ratchet changes != | 11/11 PASSED | PASS |
| .015 Phase 2 Step 5 | `pytest comp/bench/tests/test_selector_game_detected.py -v` | random > 0.1 -> SelectorGameDetected | 6/6 PASSED | PASS |
| .015 Phase 2 Step 6 | `pytest comp/bench/tests/test_cache_key.py -v` | all 9 inputs change key | pre-staged 5/5 PASSED | PASS |
| .015 Phase 2 Step 7 | `pytest comp/bench/tests/test_primary_metric.py -v` | formula verified, exploratory isolation | 8/8 PASSED | PASS |
| .015 Phase 2 Step 8 | `pytest comp/bench/tests/test_gold_survey_attestation.py -v` | all 5 fixtures (a-e) pass | 5/5 PASSED | PASS |
| .015 Phase 2 Step 9 | `pytest comp/bench/ -v` | all pass, exit 0 | 138/138 PASSED | PASS |
| .015 Phase 3 Step 1 | comp-build --rebuild; modules importable | modules visible | comp.bench.ab, primary, structural importable | PASS |
| .015 Phase 3 Step 2 | git diff HEAD~1 -- comp/bench/judges/ | temp-0 clean | `temp-0 clean` | PASS |
| ds-commit-gate | ds-commit-gate.sh [18 files] | OK | OK: pre-commit gate clean for 18 file(s) | PASS |
| ACCEPTANCE FLEX (Rule 7) | Pre-flag to 1.1.0_SA_CTO: primary_metric range [0, 1.3] unbounded | CTO ACCEPT or clamp directive | ACCEPTED 20260421T171634Z — document-only, no clamp; "unbounded above by design" added to docstring | PASS |
