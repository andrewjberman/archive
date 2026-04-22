# Session Log — 1.2.0_DS_CompLearns — 2026-04-22
# TO: COMP_LEARNS.052 dev-1 + dev-2 apparatus-stress monitors

## Summary

Both dev-stress monitors executed. No stop-the-line events.
dev-1: ordinary coverage gap | dev-2: ordinary coverage gap
Commit: 43945614 — pushed to origin/CLOUD 2026-04-22.

## dev-1 — selector_ceiling stress (3-hop import chain)

Baseline commit pin: same_as_bl-httpx-001 (apparatus used synthetic source; no _repo/ clone).

Probe setup: 4-module synthetic mini-repo (_client -> _auth -> _models -> _utils).
Compiler output: 4 nodes, 3 edges — full 3-hop chain correctly compiled. No compiler truncation.

Selector (CentralitySelector v0) results at varying budgets:
- budget=5:  1 node, 0 edges. hop-3 _utils EXCLUDED.
- budget=10: 2 nodes, 0 edges. hop-3 _utils EXCLUDED. hop-1 _auth EXCLUDED. Disconnected context.
- budget=20: 4 nodes, 3 edges. Full chain. No truncation.

Finding: Selector is NOT hop-chain-aware. Ranking is PageRank + question-boost. At the
standard _WARM_UP_BUDGET_TOKENS=2048, the 15-token 4-node chain fits entirely. Truncation
appears at tight budgets or dense real graphs where unrelated high-centrality nodes
compete for budget. Classification: ordinary coverage gap.

## dev-2 — ABCache cache_identity near-collision

Baseline commit pin: compiler.py at 1f7db976 (feature_clb CLOUD HEAD 2026-04-22).

Scenario A (same version string, different non-structural source):
- compute_target_version: identical when _repo/ absent (gold-only hash)
- graph_hash: identical (EXTRA_LINE constant does not affect import edges)
- Near-collision: True (same cache key). Correctness failure: No.
- Reason: LLM sees graph context; identical graph -> cached response valid for both states.

Scenario B (different entry-point questions): keys differ. No collision.
Scenario C (different token count): keys differ. No collision.
Scenario D (different source_hash): keys differ. Correct.

Finding: 9-tuple key scheme prevents false hits in all scenarios where the LLM would
receive different context. Near-collision in Scenario A is not a correctness failure.
Gap: source_hash = gold-only when _repo/ absent; non-structural source changes invisible.
Classification: ordinary coverage gap.

## Compiler Tools

### Phase 1 (before write)
- comp-build: PASS
- pytest comp/ -q: 9 failed (pre-existing baseline), 430 passed — PASS

### Phase 2 (before commit)
- ls comp/results/dev-stress/: dev-1-selector-ceiling.md + dev-2-cache-identity.md — PASS
- grep Classification: both "ordinary coverage gap" — PASS
- pytest comp/ -q: 9 failed (same pre-existing), 430 passed — PASS

### Phase 3 (after commit)
- comp-build: PASS

## Acceptance Criteria Check

1. dev-1 stress run + doc at comp/results/dev-stress/dev-1-selector-ceiling.md — PASS
2. dev-2 stress run + doc at comp/results/dev-stress/dev-2-cache-identity.md — PASS
3. Both files have explicit classification lines — PASS (ordinary coverage gap x2)
4. No stop-the-line events (no cache-identity or comparability corruption) — PASS
5. baseline_commits pinned on dev-httpx-001 + dev-httpx-002 YAMLs — PASS
6. Commit --only --author=1.2.0_DS_CompLearns -- comp/results/dev-stress/** + backlog YAML — PASS
7. Pushed to CLOUD (43945614) — PASS
8. Session log — this file
9. MCP COMPLETE to 2.1.0_SA_COO — sent post-log

## Informational Flags for COO

dev-1 flag: The CentralitySelector does not guarantee inclusion of a full hop-3 import
chain at tight token budgets. Suggested future TO: path-aware selector mutation (dev-loop
goal per dev-httpx-001 notes). No action required from main lanes.

dev-2 flag: When _repo/ is absent (harness scaffold mode), source_hash = gold-only.
Suggested future TO: add comp-preflight WARN when _repo/ absent during eval-mode runs.
No action required from main lanes.
