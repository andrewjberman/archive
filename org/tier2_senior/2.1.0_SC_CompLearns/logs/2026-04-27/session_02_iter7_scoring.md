# 2.1.0_SC_CompLearns — Session Log — 2026-04-27

## Session: COMP_LEARNS.068 — iter-7 scoring (class_hierarchy_correction)

**Date:** 2026-04-27  
**TO:** COMP_LEARNS.068.sc-iter7-click-scoring.md  
**Status:** COMPLETE  
**Commit:** 4e0ecd69

---

## Work Done

### Phase 0 — Pre-run gate
- Pulled CLOUD, verified 7ee0859c (class_hierarchy_correction compiler) + f5095ac0 (path fix) present
- Confirmed experiment_log had 6 iters [1-6] before run
- Gate: PASS

### Phase 1 — Scoring run
- Command: `python comp/bin/comp-learns-ratchet click --judge real --max-iter 1 --compiler-content-sha 923071d5`
- Exit: MAX_ITER (exit code 10) — expected
- Duration: ~2:01
- Cache: cold (33 warm-up entries written, 33 cache hits on scoring pass)
- ANTHROPIC_API_KEY retrieved from AWS Secrets Manager

### Phase 2 — Scorecard assessment

**Scorecard:** comp/targets/click/scorecards/38c712a_d869779f.json

| Metric | Value |
|---|---|
| primary_metric (ab_lift) | 0.0 |
| keyword lift | 0.0 |
| centrality lift | 0.0 |
| random lift | 0.0 |
| tied_at_best | true |
| random_unique_win | false |
| structural_f1 | 0.6545 |
| mutation_stability | 0.8582 |
| compiler_loc | 171 |
| judge_mode | real |
| benchmark_honest | true |

**Champion:** pm=0.1180 (7beb09b)  
**ab_lift vs champion:** -0.1180  
**Verdict: DISCARD**  
**PATTERN: C** — all three selectors flat at 0.0

**q03 flip:** NO  
**q02/q11 flip:** NO (R-SC-1 monitoring: no format-variance event triggered)

### Phase 3 — Experiment log auto-append check

The runner.py path fix (f5095ac0) did NOT redirect the experiment_log write to comp/results/dev-click-001/experiment_log.jsonl. Runner still wrote to comp/targets/click/experiment_log.jsonl (schema v2). Manual backfill applied to comp/results/dev-click-001/experiment_log.jsonl (schema v3, iteration=7). Note filed in result.json evaluation_notes and MCP.

### Phase 4 — Commit and push

- result.json: comp/dev-bundles/dev-click-001/iter-7/result.json
- experiment_log.jsonl: 7 iters [1-7] confirmed
- Commit: 4e0ecd69 — author 2.1.0_SC_CompLearns
- Push: CLOUD — PASS

---

## Compiler Tools

| Tool | Run | Result |
|---|---|---|
| git pull + log check | git pull origin CLOUD + grep for 7ee0859c | PASS — both commits confirmed |
| experiment_log pre-check | python3 -c "...open(experiment_log.jsonl)..." | PASS — 6 [1-6] |
| post-run log check | same | FAIL — runner still wrote to click/experiment_log.jsonl (v2) |
| post-commit log check | python3 -c last entry | PASS — iter-7 DISCARD pm=0.0 confirmed |

No comp-* tools applicable (scoring-only TO, no gold script or portal component work).

---

## Assessment Notes

iter-7 is the second consecutive PATTERN C across two different mutation families:
- iter-6: summary_fact_node (hierarchy_summary, Group-perspective) — DISCARD PATTERN C
- iter-7: class_hierarchy_correction (Command-perspective, NOT-exclusion) — DISCARD PATTERN C

Seven iters total on dev-click-001. Champion still 0.1180 (random selector, iter-2 vintage). Two mutation families exhausted: import/class_inherits (iters 2-5), class_hierarchy_* nodes (iters 6-7).

CTO diagnosis was that iter-6 encoded what the judge already knows (Group's children). iter-7 reframed from Command's perspective with NOT-exclusion strings. Still no q03 flip. The q03 failure may be:
- (H1) Token budget (~45 tokens) does not reliably surface the correction node vs graph edges
- (H2) Judge's q03 confusion is framing-level, not hierarchy-level
- (H3) The correction information is present in the full-source graph; the compiled context doesn't add net signal

Path fix note for CTO/DS: f5095ac0 is confirmed present on CLOUD but did NOT redirect the experiment_log write path for the click target. Runner still uses comp/targets/click/experiment_log.jsonl (schema v2). Manual SC backfill required again for iter-7.

---

## Open Items

- R-SC-2 (semantic-correct-but-unparseable audit label for q02/q11): queued for iter-8, non-blocking per CTO
- Path fix (f5095ac0) still not working for click target experiment_log — should be flagged to DS/COO for iter-8
- iter-8 strategy: gates on CTO assessment of iter-7 result

---

## Session: COMP_LEARNS.065 — v0 question forensic (Option A diagnostic)

**Date:** 2026-04-27  
**TO:** COMP_LEARNS.065.sc-option-a-v0-question-forensics.md  
**Status:** COMPLETE  
**Commits:** none (read-only diagnostic)

---

### Work Done

#### Phase 1 — Champion verification

- champion.json: sha=7beb09b, pm=0.1180, baseline_commit=f80cf4b09fbe36099b7bfc065fbde30d053da46d, iteration=0
- Scorecard file: comp/targets/click/scorecards/7beb09b_d869779f.json — present
- Scorecard confirms: random.lift=0.09090909 (1/11), centrality.lift=0.0, keyword.lift=0.0, random_unique_win=true

#### Phase 2 — Per-question results lookup

Cache lookup attempted: v0 source_hash = d505e5e5eb2b9cc9 (SHA-256 of compiler.py at 7beb09b, first 16 chars).  
Result: ZERO cache entries for this source_hash in feature_clb ab_cache (297 entries across 6 other source_hashes).  
Cache was cleared/reinitialized between v0 run (2026-04-24T16:30:10Z) and current session.

Scorecard format does not include per-question breakdown (aggregate only). Direct per-question evidence is not recoverable.

#### Phase 3 — Analytical reconstruction

**v0 compiler type correction:** The v0 compiler (sha 7beb09b) is a DISPATCH-CHAIN compiler, not imports-only. `subtypes_enabled: ["imports"]` in the scorecard is a hardcoded ratchet metadata field that does not describe compiler output.

**v0 graph contents (confirmed by running compiler logic against click/_repo):**
- dispatch_class: Command (root, no bases listed)
- dispatch_class: Group(Command) — Group directly subclasses Command in click 8.3.1
- can_dispatch_to edges: Group → Command, Group → Group
- command_registration nodes: decorator-decorated functions with @command/@group
- ABSENT: _BaseCommand (no invoke() defined), _MultiCommand, CommandCollection, all import edges

**Per-question ruling:**

| QID | Finding | Evidence |
|---|---|---|
| q02 | NOT the win — no import data in v0 graph | Honesty note: "all verbose, giving 7 (wrong value)" |
| q03 | NOT the win — v0 graph missing _BaseCommand (no invoke()) | Judge with v0 context would answer "Group" only; fails set_membership against gold {_BaseCommand, Group}. sc_q03_q11_responses.txt q03 responses all wrong ("MultiCommand") |
| q11 | NOT the win — no import data; all 6 v0 responses scored false | R-SC-2 audit: 3/6 semantic-correct-but-unparseable, 2/6 semantic-wrong, 1/6 ambiguous |

**Conclusion:** The v0 random_unique_win was on a PRIOR-KNOWLEDGE question, most likely q09 (star imports in __init__.py = 0) or q10 (no importlib.import_module call = "no"). Both are adversarial questions with "null/false" correct answers that the judge supplies from training priors regardless of context. The random selector's sparse dispatch-chain context produced less noise than the centrality/keyword selections, allowing the judge's training prior to surface.

**Reproducibility:** PROBABLE-LUCK. No compiler-context-driven knowledge gain demonstrated.

**CTO diagnostic answer:** Does the v0 win suggest dispatch_class body nodes address q03? NO. _BaseCommand is absent from the v0 graph entirely; the q03 mechanism was not present. The CTO's iter-8 ruling (q03 CLOSED) stands independently.

#### Phase 4 — Stage 3 rulings ACK

CTO Stage 3 rulings received this session (R-SC-1 P0, R-SC-2 P1). ACK sent. Standing by for Stage 3 PRD.

---

## Compiler Tools

| Tool | Run | Result |
|---|---|---|
| ab_cache source_hash lookup | python3 scan of 297 cache files for d505e5e5eb2b9cc9 | 0 entries — v0 cache not recoverable |
| v0 compiler graph inspection | python3 inline AST walk of click/_repo using v0 compiler logic | 2 dispatch_class nodes confirmed (Command, Group); _BaseCommand absent |
| H3-v2 baseline read | direct file read | 8/11 correct (q01, q04-q10); q02/q03/q11 incorrect |
| R-SC-2 audit read | comp/results/dev-click-001/r_sc_2_failure_mode_audit.md | q11: 3/6 format-failure, 2/6 semantic-wrong; q02 incomplete |

No comp-* tools applicable (read-only diagnostic, no gold script or portal work).

---

## Open Items (updated)

- R-SC-1 (P0): Stage 3 pre-screen must use R-SC-2 semantic labels in INCLUDE/SENTINEL/INVESTIGATE. Will implement on PRD arrival. Gated on Stage 3 PRD.
- R-SC-2 (P1): Add "full-source overload candidate" label to pre-screen Wrong|Wrong output. Will define separation rule. Gated on Stage 3 PRD.
- R-SC-2 q02 extension: capture raw q02 responses in next warm-up run. Prerequisite for completing q02 retroactive audit.
- Path fix (f5095ac0): still not working for click target experiment_log. DS/COO flag remains open.
- .069 ablation: COO TO dispatch pending (gates on iter-8 ruling sequence).
