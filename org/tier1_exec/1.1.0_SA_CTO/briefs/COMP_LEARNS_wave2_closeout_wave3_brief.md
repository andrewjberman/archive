# COMP_LEARNS — Wave 2 Closeout + Wave 3 Transition Brief

**Date:** 2026-04-22
**Author:** 1.1.0_SA_CTO
**Purpose:** GPT review + Wave 3 planning input

---

## Program Recap

COMP_LEARNS is a measurement substrate for a specific question: does structured compiler assistance change what frontier models can do on hard systems-programming work, and at what cost?

"Compiler assistance" means a custom tool (`comp/`) that builds import graphs, selector trees, and cross-module dependency maps for a target OSS repo. A DS agent works a task with the compiler available (aided) vs. without (unaided). The terminal measurement is the aided-vs-unaided delta on correctness, reasoning quality, and harness usefulness.

Wave 1 (pilot, `.032`) ran two manually-curated tasks against two conditions. 8/8 PASS on local validation. That integrity result gated Wave 2 design.

---

## What Wave 2 Built

Wave 2 was a setup wave, not a measurement wave. Priority was velocity — building the apparatus fast enough to run a real eval in Wave 3. It produced:

### Backlog infrastructure
A dual-lane standing backlog (`comp/backlog/`):
- **benchmark lane** — cases with `harness_relevance >= 3`, `aided_unaided_safe = true`, full schema, SC formal scoring. These are the measurement-grade cases for Wave 3+ credibility.
- **dev lane** — relaxed intake, dev_purpose required, no comparability requirement. These are the fuel for high-velocity compiler iteration.

Current benchmark backlog:
| Case | Target | Archetype | Relevance | Status |
|------|--------|-----------|-----------|--------|
| Case 1 (bl-httpx-001) | encode/httpx | A | 4 | packet complete (pilot) |
| Case 2 (bl-click-001) | pallets/click | B | 4 | packet complete (pilot) |
| Case 3 (bl-sweb-002) | sphinx-doc/sphinx | D | 4 | packet complete (.040) |
| Case 4 (bl-httpx-002) | encode/httpx | D | 4 | packet complete (.041) |

Current dev backlog:
| Seed | Type | Purpose |
|------|------|---------|
| dev-1 (dev-httpx-001) | selector_ceiling stress | 3-hop import chain; where does selector truncate |
| dev-2 (dev-httpx-002) | cache_identity stress | ABCache near-collision key verification |
| dev-3 (dev-requests-001) | coverage_gap | Rapid harness generalization to requests repo |
| dev-4 (dev-click-001) | compiler-win ratchet | Prove comp-dev-loop.py achieves a primary_metric KEEP on Archetype B |

### Automation tools
Three tools now live in `comp/bin/`:
- `comp-preflight.py` — deterministic pre-scoring checker (7 checks, eval + dev modes)
- `comp-wave-runner.py` — wave dispatch loop; manages event sequencing, dependency order, preflight gating, scorer worktree provisioning
- `comp-dev-loop.py` — inner dev iteration loop; runs micro-cycles, tracks champion state, ratchets KEEP, detects plateau

Stage 2 eval-mode is **ACTIVE** as of 2026-04-22. This means preflight + wave-runner now replace manual COO bundle inspection as the default eval-mode dispatch path. COO workload per scoring event dropped from ~5-10 min to ~30s.

### Test coverage
84 tests GREEN across the three tools.

---

## What's Runnable Now

**Eval mode (Stage 2):** comp-wave-runner can dispatch a `wave-2.yaml` config against Case 3 (sphinx) or Case 4 (httpx). SC formally scores, verdict is committed. This is the first real Wave 2 measurement event.

**Dev mode:** comp-dev-loop.py can run against dev-4 (dev-click-001, click triple-nested chain, Archetype B). Success criterion is a ratchet KEEP on `primary_metric` — not merely a local validation pass. dev-1..3 need `baseline_commit` pinning before they can run (§9 gate).

These are both ready today. Both require an explicit trigger decision (which runs first, which DS agent drives dev-4).

---

## Stage 2 Exit Criterion (gate to Stage 3)

Stage 3 (audit-sampled automation) requires: **2+ Stage 2 eval-mode waves with zero preflight false-passes AND zero integrity violations.** This is the credibility gate for Wave 3 comparative measurement claims.

Stage 3 design is deliberately deferred — not specified in the current PRDs. It requires the Stage 2 track record before the design is warranted.

---

## What Wave 3 Is Not Yet Defined

Wave 2 deliberately deferred two things to Wave 3:

1. **Comparability.** Wave 2 benchmark cases (Cases 3+4) were authored to measurement-grade schema, but have not been scored yet. Wave 3 is where aided-vs-unaided deltas become the primary output — not just PASS/FAIL on local validation.

2. **Cross-model evaluation.** The automation loop supports a `judge_model_id` pinned field. Running the same wave config against a different judge model is the cross-model comparison axis. Not yet run.

Wave 3 is therefore the first wave where the program starts generating the measurement output it was designed to produce.

---

## Open Questions for GPT Review

**On Wave 3 scope definition:**

1. Wave 3 should produce the first real aided-vs-unaided delta measurements. Should Wave 3 be defined as running all 4 existing cases (Cases 1-4) under both conditions, or is there a reason to run a subset first — e.g., only Cases 3+4 (the new Archetype D cases) before re-running the pilot cases?

2. Cases 1+2 (httpx NetRC, click Group.invoke) were already run in the pilot under manual Stage 1 conditions. Re-running them under Stage 2 automation gives a cleaner apples-to-apples measurement. Is there a methodological argument for keeping the pilot runs as the unaided baseline, or should we rerun clean?

3. The current benchmark backlog has 2 Archetype A cases and 2 Archetype D cases. For Wave 3 credibility, do we need at least one Archetype B or C case scored formally, or is A+D coverage sufficient for the first wave of comparative claims?

**On the dev mode / Wave 3 relationship:**

4. dev-4 (compiler-win ratchet) is the highest-priority dev seed. If it achieves a ratchet KEEP, that proves the dev loop works. How should that result be interpreted in relation to Wave 3 eval planning? Does a dev-4 KEEP accelerate Wave 3 (because the compiler is demonstrably better) or is it orthogonal?

5. dev-1 and dev-2 are apparatus stress tests (selector_ceiling and cache_identity) rather than real tasks. Their purpose is to surface failure modes in the compiler, not to produce measurement-grade results. Should these run before Wave 3 eval dispatch (to catch silent apparatus failures first), or in parallel?

**On Wave 3 architecture decisions:**

6. Wave 3 is the first wave where the Stage 2 exit criterion matters. Should Wave 3 be designed as exactly 2 waves (minimum to gate Stage 3), or should it be sized by the measurement goals (e.g., enough events to have statistical confidence on the aided-vs-unaided delta)?

7. Cross-model comparison (same wave config, different `judge_model_id`) is in scope but not yet run. Is Wave 3 the right place to introduce this, or should Wave 3 establish a clean single-model baseline first and defer cross-model to Wave 4?

8. The backlog currently has 4 benchmark cases. Case 5 would be a new repo family (sphinx harness exists from .046; pylint and pytest harnesses don't yet exist). Should Case 5 be commissioned before Wave 3 runs — to have a third repo family in the pool — or is the 4-case pool sufficient for Wave 3 measurement claims?
