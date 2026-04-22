# Session 13 — Wave 2 PRD Authoring + COO TO Handoff

**Date:** 2026-04-22  
**Agent:** 1.1.0_SA_CTO  
**Principal:** Andrew  
**Predecessor:** session12 (pilot wave 1 complete, all 8 PASS, integrity audit `6dcbdf22`)  
**Trigger:** Wave 2 planning session — GPT briefing on Content for Testing + Speed of Testing

---

## Objective

Author two Wave 2 PRDs, iterate through GPT review, and produce a locked handoff
package for COO to decompose into actionable TOs.

---

## Final Documents (locked, ready for TO decomposition)

| Document | Path | Final Commit |
|----------|------|--------------|
| BACKLOG_V1 | `docs/architecture/COMP_LEARNS_BACKLOG_V1.md` | `034f9ad7` |
| AUTOMATION_V1 | `docs/architecture/COMP_LEARNS_AUTOMATION_V1.md` | `034f9ad7` |

Both documents are in the `feature_clb` worktree on branch `CLOUD`.
Remote: `https://github.com/Opal-Capital/ajb_workspace.git`

---

## Revision History (for audit)

| Commit | Description |
|--------|-------------|
| `92ff41bd` | v1 — initial drafts |
| `8a343557` | v2 — dev/eval mode split, dual-lane backlog, Archetype E, micro-cycle contract |
| `36dd6984` | v3 — result.json breadcrumbs, experiment_log schema, .044 prioritization, baseline pinning rule, dev-4 seed |
| `034f9ad7` | housekeeping — v3 headers, seed count 3→4, TO .039 aligned, dev-4 success condition |

---

## TO Decomposition for COO

### From BACKLOG_V1

| TO | Assignee | Scope | Gates |
|----|----------|-------|-------|
| **.037** | 2.1.0_SA_COO + 1.x_DS | Rebuild `comp/backlog/` with dual-lane structure: create `comp/backlog/benchmark/` and `comp/backlog/dev/` directories; migrate bl-httpx-001 and bl-click-001 to new schema (add `lane: benchmark` field, all other fields retained); author `comp/backlog/BACKLOG.md` index with lane column | none — first TO, can start immediately |
| **.038** | 2.1.0_SA_COO | Download SWE-bench Verified dataset (`SWE-bench/SWE-bench_Verified` on HuggingFace); filter to Python repos with `harness_relevance >= 3` and `aided_unaided_safe = true`; propose 3 Case 3 candidates as `comp/backlog/benchmark/bl-sweb-*.yaml` entries | .037 complete (benchmark/ dir must exist) |
| **.039** | 1.1.0_SA_CTO | Review + approve one Case 3 candidate from .038; author Case 4 `bl-*.yaml` (OSS historical cross-module bug, httpx or requests); author 4 dev_backlog seed entries (dev-1 selector_ceiling, dev-2 cache_identity, dev-3 rapid-intake generalization, dev-4 compiler-win Archetype A/B) | .038 complete (need candidates to review) |
| **.040** | 1.x_DS | Author task packet for Case 3 (`comp/tasks/{case3-id}/packet.yaml`) from approved backlog entry | .039 complete (approved bl-*.yaml must exist) |
| **.041** | 1.x_DS | Author task packet for Case 4 (`comp/tasks/{case4-id}/packet.yaml`) from approved backlog entry | .039 complete |

**Gate:** .040 + .041 are prerequisites for Wave 2 formal scoring. Dev seed (.039) is
parallel to packet authoring — dev cases do not require full task packets.

---

### From AUTOMATION_V1

| TO | Assignee | Scope | Gates |
|----|----------|-------|-------|
| **.042** | 1.x_DS | Implement `comp/bin/comp-preflight.py`: both modes (`--mode dev\|eval`); dev mode runs CHECKs 1, 2, 2b only; eval mode runs all 7 checks; unit tests must cover both mode paths; CHECK 2b is soft warning (non-blocking) | none — can start immediately |
| **.043** | 1.x_DS | Implement `comp/bin/comp-wave-runner.py`: wave config YAML schema with per-task mode override; mixed-mode event routing (dev vs eval); event-driven loop (inbox-watch, not polling); dry-run mode verified against wave 1 data | .042 complete |
| **.044** | 1.x_DS | Implement `comp/bin/comp-dev-loop.py`: 3-level validation ladder (Level 1 per-iteration, Level 2 on KEEP candidate, Level 3 optional); burst mode (`--burst-n`, default 3); plateau detection (`--plateau-n`, default 5); kill switch (sentinel file `comp/dev-loop-stop`); `experiment_log.jsonl` with full schema (iteration, verdict, delta, mutation_type, intervention_tag, validation_level, burst_position, compiler_sha, baseline_commit) | .042 complete |
| **.045** | 2.1.0_SA_COO + 1.1.0_SA_CTO | Stage 2 eval-mode activation review: dry-run comp-wave-runner against wave 1 data; verify preflight unit tests pass; COO reviews handoff protocol; CTO issues explicit activation authorization TO | .042 + .043 complete |

**Priority rule:** If resourcing is tight, .044 ships before .043. The inner dev
loop is the Wave 2 throughput driver. The wave runner is secondary and can follow
once .044 has real iteration data to justify the orchestration design.

**Dev mode activation:** .044 may activate independently of .045. If comp-dev-loop.py
and `comp-preflight --mode dev` pass their tests, dev mode may begin without waiting
for the full Stage 2 eval-mode gate (.045). Dev mode does not touch measurement
integrity.

---

## Key Design Decisions for COO Awareness

These are not TOs — they are constraints that COO must enforce when dispatching the
above TOs and when executing wave operations.

### Dev mode artifact contract
DS in dev mode produces: `changes.patch` + `result.json`. The result.json must
include: `pass`, `validation_level`, `compiler_sha`, `target_version`,
`baseline_commit`, `mutation_type`, `intervention_tag`. Bundles missing these fields
fail CHECK 2 in dev mode and must be corrected before the loop runner accepts them.

### Baseline pinning gate
A `dev_candidate` backlog entry may have blank `baseline_commit` at intake. Before
any DS agent begins a `comp-dev-loop.py` run, `baseline_commit` must be pinned and
committed. COO enforces this: a GO message for a dev_active run requires a committed
pinned baseline in the YAML. This is a hard gate — unpinned active runs produce
unreliable result.json identity.

### dev-4 success condition
The dev-4 seed case (compiler-win) is not satisfied by a local validation pass alone.
Success condition is a real `primary_metric KEEP` under the ratchet loop. COO should
confirm this explicitly when reviewing the first dev-4 run outcome with CTO.

### COO relay (eval mode only)
The COO spot-check relay is preserved in eval mode. Dev mode explicitly removes COO
from the critical path — human intervention triggers only on plateau signal, kill
switch, or budget exhaustion. COO does not need to relay micro-cycle bundles.

---

## What This Handoff Does NOT Authorize

- CTO authorization for Stage 2 eval-mode activation — that requires .045 (separate TO)
- Task packet authoring for dev_backlog cases — dev cases do not need full task packets
- Gold survey execution or gold patch handling — separate from backlog scope
- Harness authoring for new repos (e.g. `requests`) — separate TO if needed for Case 4

---

## Next Steps for CTO After This Handoff

1. .039 (CTO-owned): once .038 candidates land, review and select Case 3; author
   Case 4 bl-*.yaml; author 4 dev seed entries. This is the highest-leverage CTO
   action for Wave 2 unblocking.
2. .045 (CTO sign-off): once .042+.043 are shipped, issue explicit Stage 2 eval-mode
   activation authorization TO. Do not treat .043 completion as implicit authorization.

---

## Compiler Tools

No comp-build or pytest invocations this session — CTO lane is architecture.
All reads + writes in feature_clb worktree per worktree discipline.
