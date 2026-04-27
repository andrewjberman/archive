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
