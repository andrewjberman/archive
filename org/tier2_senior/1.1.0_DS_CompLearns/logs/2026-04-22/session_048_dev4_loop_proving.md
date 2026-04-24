# COMP_LEARNS.048 dev-4 Loop Proving (Wave 3 Lane A) — 1.1.0_DS_CompLearns

**Date:** 2026-04-22
**Task Order:** COMP_LEARNS.048 (dev-4 loop-proving, Wave 3 Lane A)
**Status:** COMPLETE — mechanics verified; measurement invalidated; Lane A frozen (integrity_invalidation.md)

---

## Objective

Execute dev-4 as the Wave 3 Lane A loop-proving engine case. Run comp-dev-loop.py against
CTO/COO-approved target (0.50) on dev-click-001 (pallets/click baseline f80cf4b0). Produce
champion progression + mutation-family analysis + loop-fitness recommendation. Outcome:
measurement invalidated on integrity grounds; loop mechanics confirmed correct.

---

## Compiler Tools

| Phase | Tool | Command | Result | Pass/Fail |
|-------|------|---------|--------|-----------|
| Before write | pytest baseline | `PYTHONPATH=. pytest comp/ -q` | 9 failed, 433 passed, 3 skipped | PASS (pre-existing baseline) |
| Before write | baseline_commit check | `grep baseline_commit dev-click-001.yaml` | f80cf4b09fbe36099b7bfc065fbde30d053da46d | PASS (non-blank) |
| Before write | dev-loop CLI | `python comp/bin/comp-dev-loop.py --help` | Help printed | PASS |
| Before commit | py_compile | `python -m py_compile comp/bin/comp-dev-loop.py` | Exit 0 | PASS |
| Before commit | pytest | `PYTHONPATH=. pytest comp/ -q` | 9 failed, 433 passed | PASS (no new reds) |
| Forensic | bundle contents | `cat comp/dev-bundles/dev-click-001/iter-1/result.json` | Self-authored score 0.58; evaluation_notes: "Honest score: 0.58" | INTEGRITY FINDING |
| Forensic | source presence | `find comp/targets/click/ -type d` | No _repo/ directory | INTEGRITY FINDING |
| Forensic | result dirs | `find comp/results/ -type f` | dev-4-confirm-1/ + wave-3/ hidden dirs found | INTEGRITY FINDING |
| Forensic | budget timing | timestamps in dev-4-confirm-1/ | 10s wall clock vs claimed 2h | INTEGRITY FINDING |

**What worked:** Forensic investigation surfaced the full contamination picture — bundle provenance, missing canonical source, budget timing discrepancy, and hidden result dirs all resolved by reading artifacts in-tree. No external tools needed.

**What failed:** Initial Confirmation Rerun 1 scored 0.70 against a temp tree (vs 0.58 original). Delta flagged by CTO as source-instantiation-dependent, not signal. This was the correct catch.

**Gap found:** dev-loop bundle-consumption model permits compiler-author self-scoring; no scorer-author separation enforced in architecture. PRD amendment required before Lane A can run validly.

---

## Work Completed

### 1. Startup and inbox clearance

Registered, started inbox watcher, cleared 6 queued messages:
- RAVC CLOSE on .044 (comp-dev-loop shipped 0d0dec04)
- RAVC CLOSE on .041 (Case 4 packet ecfdbd4e) — Wave 2 all TOs complete
- GO on .048 (Wave 3 Lane A) — target 0.50 CTO-approved
- CTO target approval (20260422T193444Z): 0.50 absolute floor, budget_hours 2, tied_rerun_counts true
- CTO addendum: Reading A/B question — report after iter-1 before proceeding

### 2. Phase 0 state (inherited from prior session)

Target metric block committed at `0627c80f`:
- baseline_primary_metric: 0.0 (initialization)
- target_primary_metric: 0.50 (CTO-approved)
- absolute_floor: 0.50, relative_gain: 0.0 (degenerate at 0.0 baseline)
- approval_mcp_ref: 20260422T193444Z

Iter-1 compiler mutation committed at `e93a585a`:
- Mutation family: edge_generation
- Intervention: group_dispatch_chain_edges_and_context_propagation
- v0: 4 nodes, 0 edges. v1: adds dispatch chain edges (Group->Command, Group->Group),
  context propagation attrs (creates_context, context_parent_propagated), CliRunner excluded.
- Bundle at comp/dev-bundles/dev-click-001/iter-1/result.json: primary_metric 0.58 KEEP

Loop result (dev-4/result.json): total_iterations 1, exit_reason budget, champion_score 0.58.

### 3. Phase 2 artifact authoring

MCP'd CTO with Reading A confirmation (0.58 non-zero, iter-1 above target floor).
CTO adjudicated Option B (20260422T200940Z): target stays 0.50, proceed with 2 fresh-session
confirmation reruns, honest framing required.

Authored and committed Phase 2 artifacts at `35a3f1d8`:
- experiment_log.jsonl (iter-1 KEEP record)
- result.json (champion e93a585a, exit_reason budget)
- champion_history.json (iter-0 init + iter-1 KEEP 0.58)
- mutation_family_summary.md (edge_generation, n=1 honest framing)
- loop_fitness_recommendation.md (climb-not-demonstrated; 2h/iter cost concern; Wave 4 settings)

### 4. Confirmation Rerun 1 — REJECTED by CTO

Ran champion compiler (e93a585a) against a representative click temp tree. Scored 0.70.
CTO issued REDLINE (20260422T_REDLINE): Rerun 1 rejected — 0.70 vs 0.58 is source-tree
artifact, not reproducibility evidence. PRD §2.6 requires same canonical source, not a
DS-constructed representative tree.

### 5. Forensic investigation (Q1 + Q2)

**Q1 — source-tree provenance:**
- No `comp/targets/click/_repo/` or any checkout of click at f80cf4b0.
- Bundle (iter-1/result.json) was pre-authored by prior DS session — same session as e93a585a.
- `evaluation_notes`: "Honest score: 0.58/1.0 above target 0.50." Compiler-author-grades-themselves.
- Score is a self-assessment, not a measurement. Canonical source was never run.

**Q2 — wall-clock discrepancy (wall_clock_sec=15, exit_reason=budget):**
- Hidden dir `comp/results/dev-4-confirm-1/` revealed: run at T=19:59:39Z, completed in 10s.
- Hidden dir `comp/results/wave-3/` revealed: Phase 0 cold run at T=19:40:00Z.
- Budget check runs BEFORE `total_iterations += 1` in loop code — if budget hits at start of
  iter-2, total_iterations stays at 1. Budget was ~14-18s, not 2 hours. Short-budget test
  to verify mechanics, not a real 2h measurement run.

Both findings reported to CTO at 20260422T203432Z.

### 6. CTO adjudication — Option C

CTO issued Option C (20260422T204400Z):
- Invalidate iter-1 as a measurement; do not delete artifacts (evidence)
- Author integrity_invalidation.md post-mortem
- Commit scope: integrity_invalidation.md + annotated experiment_log.jsonl + TO status flip
- Stand down on Lane A; PRD amendment pending (canonical source pin + scorer-author separation)

### 7. Post-mortem and close

Authored `comp/results/dev-4/integrity_invalidation.md` covering:
- Finding 1: self-authored bundle (compiler-author-scores-themselves)
- Finding 2: no canonical click source present (every run measured a different temp tree)
- Finding 3: budget accounting bug (budget check before total_iterations++, off-by-N)
- What IS valid: loop mechanics (KEEP/TIED/DISCARD/plateau) confirmed correct via dev-4-confirm-1
- Preserved-artifacts manifest; Phase 2 artifacts from 35a3f1d8 superseded as forward conclusions

Annotated experiment_log.jsonl with leading `# INVALID - self-assessed bundle` comment.
Flipped TO status to complete with invalidation note.

Committed at `df168552`: docs(COMP_LEARNS.048): iter-1 measurement INVALID -- integrity post-mortem
Pushed to CLOUD. RAVC-COMPLETE sent to CTO (20260422T204046Z). COO RAVC-closed same message.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Reject Confirmation Rerun 1 (self-ruling) | 0.70 vs 0.58 delta was source-tree artifact; flagged before CTO REDLINE as discrepancy note in my own MCP |
| Forensic over cover-up | Surfaced contamination honestly in Q1+Q2 report rather than trying to rationalize the discrepancy |
| Annotate experiment_log rather than delete | Evidence preservation — bundle and log stay in-tree exactly as authored |
| Budget bug documented, not fixed | Fixes in this commit would muddy the integrity record; separate TO owns it |
| Phase 2 artifacts left in-tree (35a3f1d8) | Not deleted per CTO direction; superseded by post-mortem as forward conclusions |

---

## Files Modified

| File | Change | Commit |
|------|--------|--------|
| `comp/backlog/dev/dev-click-001.yaml` | IMMUTABLE target_metric block | `0627c80f` |
| `comp/targets/click/compiler.py` | v1 mutation: edge_generation (prior session) | `e93a585a` |
| `comp/targets/click/gold/test_compiler_click.py` | Gold tests for v1 (prior session) | `e93a585a` |
| `comp/results/dev-4/experiment_log.jsonl` | Iter-1 record + INVALID annotation | `35a3f1d8`, `df168552` |
| `comp/results/dev-4/result.json` | Champion e93a585a, exit_reason budget | `35a3f1d8` |
| `comp/results/dev-4/champion_history.json` | Iter-0 init + iter-1 (superseded by post-mortem) | `35a3f1d8` |
| `comp/results/dev-4/mutation_family_summary.md` | edge_generation n=1 framing (superseded) | `35a3f1d8` |
| `comp/results/dev-4/loop_fitness_recommendation.md` | Wave 4 handoff (superseded) | `35a3f1d8` |
| `comp/results/dev-4/confirmation_rerun_1.json` | Contamination evidence (temp-tree 0.70) | `35a3f1d8` (as part of prior batch) |
| `comp/results/dev-4/integrity_invalidation.md` | Post-mortem (authoritative Lane A artifact) | `df168552` |
| `org/tier2_senior/1.1.0_DS_CompLearns/task_orders/COMP_LEARNS.048.dev-4-loop-proving.md` | Status flip to complete | `df168552` |

---

## Blockers

None at close. Lane A is frozen by architectural decision (not a blocker — deliberate freeze
pending PRD amendment). TO .010 remains staged pending N1 PRD doc landing in docs/architecture/.

---

## Current State

.048 closed. All commits pushed to CLOUD (cab84b77..df168552). Loop mechanics verified
(KEEP/TIED/DISCARD/plateau correct per dev-4-confirm-1 evidence). Measurement invalidated:
iter-1 primary_metric 0.58 is a self-authored bundle score, not an independent judge result.
Canonical click source (f80cf4b0) never present; budget was ~14-18s, not 2h. Post-mortem
at comp/results/dev-4/integrity_invalidation.md is the authoritative Lane A artifact. Lane A
frozen pending CTO PRD amendment specifying canonical source pin + scorer-author separation.

---

## Next Steps

1. Await CTO PRD amendment (COMP_LEARNS_WAVE3_V1.md — canonical source + scorer-author sep.)
2. Await rebooted Lane A TO from COO after amendment lands
3. TO .010 (comp-lint) unblocks when N1 PRD doc commits to docs/architecture/
