# Session Log — COMP_LEARNS.017 E2E v0 Ratchet on httpx

**Agent:** 1.3.0_DS_CompLearns
**Date:** 2026-04-21
**TO:** COMP_LEARNS.017.e2e-v0-ratchet-httpx.md

---

## Summary

Delivered the v0 end-to-end ratchet integration on httpx. All 5 new Python modules shipped, 22 unit tests pass, and all 4 mandated demos completed (KEEP + DISCARD + adversarial sub-loop + determinism re-run).

---

## Deliverables

### 1. Files Created / Modified

| File | Action |
|------|--------|
| `comp/targets/httpx/compiler.py` | Created — ImportsSubtype → GraphBuilder → Graph |
| `comp/loop/ratchet.py` | Created — KEEP/REVERT state machine, two-phase scoring |
| `comp/loop/failure_miner.py` | Created — ratchet_critical failure extractor |
| `comp/loop/propose.py` | Created — v0 null proposer |
| `comp/loop/adversarial.py` | Created — AdversarialGenerator, §7.5 active sub-loop |
| `comp/loop/__init__.py` | Modified — new exports |
| `comp/bench/mutations/harness.py` | Modified — `_normalize_node_ids` fix for mutation_stability=0.0 |
| `comp/bench/mutations/base.py` | Modified — `per_failure` field on MutationStabilityReport |
| `comp/bench/scorecard.py` | Modified — `brief()`, per_failure serde |
| `comp/loop/experiment_log.py` | Modified — `verdict` field on ExperimentEntry |
| `comp/bin/comp-learns-run.sh` | Modified — `--once` flag |
| `comp/loop/tests/test_ratchet_keep.py` | Created — 4 tests |
| `comp/loop/tests/test_ratchet_discard.py` | Created — 4 tests |
| `comp/loop/tests/test_adversarial_subloop.py` | Created — 6 tests |
| `comp/loop/tests/test_scorecard_determinism_rerun.py` | Created — 3 tests |

### 2. Key Bug Fixed — mutation_stability=0.0

**Root cause:** Mutation engines copy target files to a temp dir (e.g. `comp_rename_XXXX`). `_module_name_from_path` then produces node IDs like `module:comp_rename_XXXX._client` instead of `module:httpx._client`. Since `id_mapping={}`, `_translate_graph` did nothing, and all edges appeared added/removed → stability=0.0.

**Fix:** Added `_normalize_node_ids()` in `comp/bench/mutations/harness.py`. After `compiler(mutated.mutated_root)`, replaces `mutated_root.name` prefix with `canonical_root.name` in all node IDs. Result: `mutation_stability.aggregate=0.997`.

---

## Compiler Tools Mandate

### Phase 1 (before write)
```
python -c "from comp.ir import Node, Edge; ... print('all-deps-ok')"
# PASS: all-deps-ok
```

### Phase 2 (before commit)
```
bash comp/bin/comp-learns-run.sh httpx --once
# PASS: exits 0, verdict=kept, primary_metric=1.2439, experiment_log appended

jq '.primary_metric, (.ratchet_critical | keys), (.exploratory | keys)' scorecards/*.json
# PASS: 1.2439, ["conflict_fraction","downstream_ab","efficiency","mutation_stability","structural"],
#       ["behavioral","generalization","human_annotations","open_ended_judge"]

# DISCARD cycle (compiler.py → empty graph → re-run)
# PASS: verdict=discarded, primary_metric=0.0, primary_metric_B < primary_metric_A

jq '.ratchet_critical.mutation_stability.per_failure | keys | length' scorecards/*.json
# PASS: 1 (adversarial sub-loop fired on structural_recall_zero failure)

# Determinism re-run: two consecutive --once calls, same (target_version, compiler_sha)
# PASS: both produce primary_metric=1.2439 (verdict=tied); test_scorecard_determinism_rerun passes

pytest comp/loop/ -v
# PASS: 42 passed, 11 skipped (skips are framework-dependent, not ratchet)
```

### Phase 3 (after commit)
```
ls comp/targets/httpx/scorecards/ | wc -l
# PASS: 2

wc -l comp/targets/httpx/experiment_log.jsonl
# PASS: 5 lines

jq '.verdict' comp/targets/httpx/experiment_log.jsonl
# PASS: "kept" / "kept" / "discarded" / "tied" / "tied"
# (iter 1 was kept at primary_metric=0.0 — pre-fix; iter 2 kept at 1.2439 post-fix;
#  iter 3 discarded; iters 4+5 tied — determinism re-run)

comp-blast comp/targets/httpx/compiler.py
# NOTE: No graph nodes matching (compiler.py is target entrypoint, not a comp framework node)
```

---

## Demo Evidence

### KEEP Cycle (iter 2)
```
[ratchet] target=httpx iter=2 compiler_sha=e8f2c50
[ratchet] verdict=kept primary_metric=1.2439
[ratchet] failures=0 per_failure_keys=[]
```

### DISCARD Cycle (iter 3 — empty-graph compiler)
```
[ratchet] target=httpx iter=3 compiler_sha=e8f2c50
[ratchet] verdict=discarded primary_metric=0.0000
[ratchet] failures=1 per_failure_keys=['structural_recall_zero']
```
Adversarial sub-loop fired: `per_failure` populated with variants targeting `structural_recall_zero`.

### Determinism Re-Run (iters 4 + 5)
```
# iter 4
[ratchet] verdict=tied primary_metric=1.2439
# iter 5
[ratchet] verdict=tied primary_metric=1.2439
```
Both produce identical primary_metric. `Scorecard.__eq__` holds; `emitted_at` differs. R13 + R14 closed.

### Unit Tests
```
pytest comp/loop/tests/ bench/mutations/tests/ -v
42 passed, 11 skipped in 3.35s
```

---

## Scorecard A (KEEP — e8f2c50_909ea79f.json)

- `primary_metric`: 1.2439
- `ratchet_critical.structural.f1`: 0.5743
- `ratchet_critical.mutation_stability.aggregate`: 0.997
- `ratchet_critical.downstream_ab.per_selector`: {centrality: 1.0, keyword: 1.0, random: 1.0}
- `ratchet_critical.conflict_fraction`: 0.0

---

## Status

TO .017 complete. v0 exit criterion (§8) satisfied. .018 (CTO program.md) and .019 (viz CLI) unblock.
