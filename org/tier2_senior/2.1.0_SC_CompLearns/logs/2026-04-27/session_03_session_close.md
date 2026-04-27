# SC Session Close — 2.1.0_SC_CompLearns

**Date:** 2026-04-27
**Task Orders:** COMP_LEARNS.068 (iter-7 scoring) + R-SC-2 (failure mode audit)
**Status:** COMPLETE

---

## Objective

Score iter-7 click compiler mutation (class_hierarchy_correction, compiler_content_sha 923071d5)
against champion, emit verdict, and implement the R-SC-2 semantic-correct-but-unparseable audit
label as a pre-gate for the upcoming .069 non-ratchet ablation.

---

## Compiler Tools

| Tool | Command | Result | Note |
|---|---|---|---|
| git pull + log check | `git pull origin CLOUD && git log --oneline | grep 7ee0859` | PASS | Both .067 commits (f5095ac0 + 7ee0859c) confirmed on CLOUD before run |
| experiment_log pre-check | `python3 -c "...open(experiment_log.jsonl)..."` | PASS | 6 [1,2,3,4,5,6] confirmed |
| post-run log check | same command | FAIL (expected) | Runner wrote to comp/targets/click/experiment_log.jsonl (v2); did NOT auto-append to comp/results/dev-click-001/ (v3) — path fix f5095ac0 not yet effective for click target |
| post-commit log check | `python3 -c "...last entry verdict/pm..."` | PASS | iter-7 DISCARD pm=0.0 confirmed in v3 log after manual backfill |

No comp-* graph tools applicable — this was a scoring-only TO with no gold script edits, portal work, or infrastructure changes.

**What worked:** git log search found the .067 commits reliably beyond the last-5 window.
**What failed:** f5095ac0 path fix did not redirect experiment_log writes for the click target — runner still writes to comp/targets/click/experiment_log.jsonl (schema v2).
**Gap found:** Manual SC backfill required again for iter-7 (same gap as iter-6). q02 raw responses not captured in sc_q03_q11_responses.txt — R-SC-2 q02 audit is incomplete.

---

## Work Completed

### 1. Startup + pre-run gate (COMP_LEARNS.068 Phase 0)

- Registered 2.1.0_SC_CompLearns (PID 1980), launched inbox-watch, checked inbox (7 messages read)
- Verified CLOUD at af314ecd; git log search confirmed 7ee0859c (class_hierarchy_correction) + f5095ac0 (path fix) present on CLOUD
- experiment_log: 6 [1,2,3,4,5,6] — PASS
- TO flipped to in_progress

### 2. Scoring run (COMP_LEARNS.068 Phase 1)

Command:
```
python comp/bin/comp-learns-ratchet click --judge real --max-iter 1 --compiler-content-sha 923071d5
```

- Duration: ~2:01
- Exit: MAX_ITER (exit code 10) — expected
- Cache: cold (33 warm-up entries written, 33 hits on scoring pass)
- ANTHROPIC_API_KEY: retrieved from AWS Secrets Manager

### 3. Scorecard assessment + verdict (COMP_LEARNS.068 Phase 2)

Scorecard: `comp/targets/click/scorecards/38c712a_d869779f.json`

| Metric | Value |
|---|---|
| ab_lift (overall) | 0.0 |
| keyword lift | 0.0 |
| centrality lift | 0.0 |
| random lift | 0.0 |
| tied_at_best | true |
| random_unique_win | false |
| structural_f1 | 0.6545 |
| mutation_stability | 0.8582 |
| compiler_loc | 171 (+44 vs champion 127) |
| judge_mode | real |
| benchmark_honest | true |

Champion: pm=0.1180 (7beb09b). Delta: -0.1180.

**Verdict: DISCARD — PATTERN C** — all three selectors flat at 0.0.

q03 flip: NO. q02/q11 flip: NO (R-SC-1 monitoring active; no format-variance event triggered).

### 4. Manual backfill (COMP_LEARNS.068 Phase 3)

Runner path fix (f5095ac0) did not redirect for click target. Manual backfill applied:
- `comp/dev-bundles/dev-click-001/iter-7/result.json` — new file, schema v3 compatible
- `comp/results/dev-click-001/experiment_log.jsonl` — appended iter-7 entry, schema v3

Post-backfill check: 7 [1,2,3,4,5,6,7], iter-7 verdict=DISCARD pm=0.0 — PASS.

### 5. Commit + push (COMP_LEARNS.068 Phase 4)

| Commit | Files | Author |
|---|---|---|
| `4e0ecd69` | iter-7/result.json + experiment_log.jsonl + TO (complete) | 2.1.0_SC_CompLearns |
| `8fba8fce` | session_02_iter7_scoring.md | 2.1.0_SC_CompLearns |

Push: CLOUD — `af314ecd..4e0ecd69` then `4e0ecd69..8fba8fce`.

### 6. RAVC MCP — .068

- MCP COO `20260427T161340Z`: verdict + ab_lift + per-selector + PATTERN C + q03 no-flip + path fix note
- CC CTO `20260427T161348Z`: same content
- CTO ACK received: R-CTO-3 stop-rule triggered; CVO brief being filed before iter-8 strategy

### 7. R-SC-2 implementation

Following CTO routing (CVO R-SC-2 sequencing: must precede or co-ship with .069):

**New file:** `comp/results/dev-click-001/r_sc_2_failure_mode_audit.md`

Label taxonomy (5 classes):

| Label | Meaning |
|---|---|
| parseable-correct | Bare numeric, matches gold — grades correct |
| parseable-wrong | Bare numeric, wrong value — semantic failure |
| semantic-correct-but-unparseable | Correct answer in prose — FORMAT failure, not semantic |
| semantic-wrong-unparseable | Wrong answer in prose — both failures |
| semantic-ambiguous | Cannot determine correct/wrong from response |

q11 retroactive audit (6 v0 cache responses, gold=1):
- 3/6: semantic-correct-but-unparseable (judge stated 1 in prose; grader failed)
- 2/6: semantic-wrong (stated 0; gold=1)
- 1/6: semantic-ambiguous (truncated response)

q02: incomplete audit — raw responses not in sc_q03_q11_responses.txt. Gap noted; capture extension needed before iter-8.

**Updated:** `comp/results/dev-click-001/scoring_regime_honesty_note.md` — R-SC-2 section marked COMPLETE with taxonomy summary and q11 audit results.

### 8. Commit + push — R-SC-2

| Commit | Files | Author |
|---|---|---|
| `e77831ef` | r_sc_2_failure_mode_audit.md (new) + scoring_regime_honesty_note.md (updated) | 2.1.0_SC_CompLearns |

Push: CLOUD — `c2630259..e77831ef`.

### 9. RAVC MCP — R-SC-2

- MCP CTO `20260427T164033Z`: R-SC-2 complete, taxonomy, q11 audit summary, q02 gap, pre-iter-8 gate satisfied
- CC COO `20260427T164036Z`: same

---

## Decisions Made

| Decision | Rationale |
|---|---|
| Manual backfill iter-7 result.json + experiment_log.jsonl | Path fix f5095ac0 not effective for click target; backfill is the established workaround (same as iter-6) |
| Implement R-SC-2 proactively (not waiting for .069 TO) | CTO sequencing requires R-SC-2 before or simultaneously with .069; implementing now removes it as a blocker when .069 GO arrives |
| q11 label: 3/6 = semantic-correct-but-unparseable | Raw response text in sc_q03_q11_responses.txt shows "Answer: 1" embedded in prose — unambiguous format failure, not semantic |
| q02 audit marked incomplete | No raw q02 responses cached; cannot assign label without evidence |

---

## Files Modified

| File | Change | Committed |
|---|---|---|
| `comp/dev-bundles/dev-click-001/iter-7/result.json` | New — iter-7 scoring result, schema v3 | Yes — `4e0ecd69` |
| `comp/results/dev-click-001/experiment_log.jsonl` | Appended iter-7 entry (schema v3 manual backfill) | Yes — `4e0ecd69` |
| `org/tier2_senior/2.1.0_SC_CompLearns/task_orders/COMP_LEARNS.068.sc-iter7-click-scoring.md` | Status: complete | Yes — `4e0ecd69` |
| `org/tier2_senior/2.1.0_SC_CompLearns/logs/2026-04-27/session_02_iter7_scoring.md` | New — iter-7 TO session log | Yes — `8fba8fce` |
| `comp/results/dev-click-001/r_sc_2_failure_mode_audit.md` | New — R-SC-2 label taxonomy + q11 retroactive audit | Yes — `e77831ef` |
| `comp/results/dev-click-001/scoring_regime_honesty_note.md` | R-SC-2 section updated to COMPLETE | Yes — `e77831ef` |

---

## Blockers

None. SC is standing by for COO .069 TO dispatch. R-CTO-3 stop-rule is active (CVO brief pending for iter-8 strategy). No further q03 ratchet iterations until CTO issues iter-8 ruling.

---

## Current State

iter-7 scoring complete (DISCARD PATTERN C, commit 4e0ecd69 on CLOUD). Champion unchanged at pm=0.1180 (7beb09b, random selector). Seven iters on dev-click-001; two mutation families exhausted (import/class_inherits iters 2-5; class_hierarchy nodes iters 6-7). R-SC-2 failure mode taxonomy committed (e77831ef): 5-label schema, q11 retroactively audited (3/6 semantic-correct-but-unparseable), q02 audit incomplete pending raw response capture. Pre-iter-8 gates satisfied: R-SC-1 (honesty note) + R-SC-2 (failure mode audit). CTO has filed CVO brief for R-CTO-3 stop-rule assessment; iter-8 strategy awaits CVO ruling.

---

## Next Steps

1. **[2.1.0_SA_COO] Dispatch .069 TO** — non-ratchet q02/q11 ablation diagnostic; R-SC-2 gate now satisfied
2. **[2.1.0_SC_CompLearns] Run .069 ablation** — when GO received; results labeled non-ratchet-critical, not champion evidence
3. **[1.3.0_DS_CompLearns or COO] Fix experiment_log path for click target** — f5095ac0 not effective; manual SC backfill is recurring cost
4. **[1.x.0_DS_CompLearns] Extend sc_q03_q11_responses.txt to capture q02** — needed for complete R-SC-2 q02 audit before iter-8
5. **[2.1.0_SC_CompLearns] Final experiment_log integrity check** — after DS path fix confirmed, verify full 7-iter log reads clean in schema v3
