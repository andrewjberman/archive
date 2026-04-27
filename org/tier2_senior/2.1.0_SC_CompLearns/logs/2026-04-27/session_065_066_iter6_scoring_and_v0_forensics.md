# Session Log — 2026-04-27
# 2.1.0_SC_CompLearns — COMP_LEARNS.065 + COMP_LEARNS.066

## Session Overview

Two task orders executed in this session:
- .065 (read-only diagnostic): v0 champion random_unique_win question forensics
- .066 (scoring run): iter-6 click compiler scoring — class_hierarchy_summary node

---

## COMP_LEARNS.065 — v0 Question Forensics (COMPLETE)

### Objective
Identify which of q02/q03/q11 the v0 champion (sha 7beb09b) got correct that the H3-v2 full-source baseline missed. Reproducibility assessment.

### Findings

**v0 champion scorecard**: `comp/targets/click/scorecards/7beb09b_d869779f.json`
- compiler_sha: 7beb09b, graph_hash: e3b0c44298fc1c14 (empty graph), structural_f1=0.0
- ab_lift: random=0.0909 (1/11), centrality=0.0, keyword=0.0
- random_unique_win: true, primary_metric: 0.11804865

**H3-v2 baseline**: 8/11 correct. Failed q02, q03, q11.

**Key finding**: The v0 random_unique_win was on **q05** (enumerable "yes"), NOT on q02, q03, or q11. All three improvable questions were WRONG for v0 as well as H3-v2. The champion's 1/11 lift did not come from any improvable question.

**How the win occurred**: q05 asks whether click's context manager support is backwards-compatible. Gold answer: "yes". The random selector's 10-token context elicited the response "Yes" (bare), which matched the enumerable grader exactly. The H3-v2 full-source baseline produced "Yes." (with trailing period) — strict `text.lower().strip() in values` failed on the period. The win was a format artifact, not a knowledge gain.

**Reproducibility**: PROBABLE LUCK. The judge answered from training knowledge (not from compiler context), and the win depends on whether the judge appends punctuation. Different random selections or rephrasing would not reliably reproduce this.

**Implications for iter-7**: The v0 win was NOT on q03 (class hierarchy), q02 (module count), or q11 (TYPE_CHECKING imports). dispatch_class body nodes did not address any improvable question. Iter-7 strategy should not be informed by v0 body-node coverage.

**Why q02/q11 are wrong in v0**: Both have numeric answer type. The grader calls `float(response_text)` on the FULL response. v0 cache responses are verbose (e.g., "...the answer is **7**...") — `float("... **7**...")` raises ValueError → marked incorrect. This is a grader format limitation: verbose numeric responses cannot be graded. The correct number appears in the text but the judge is not constrained to emit bare numerics.

**MCP sent to 1.1.0_SA_CTO**: Subject: COMP_LEARNS.065 COMPLETE — v0 random win was q05 (not q02/q03/q11), all improvable WRONG. Full findings included.
**CC sent to 2.1.0_SA_COO**: Same content.

### Compiler Tools

```
Phase 1 (before diagnostic):
  ls comp/targets/click/scorecards/ | grep "7beb09b"
  Result: 7beb09b_d869779f.json present -- cache lookup not required

Phase 2 (after diagnostic):
  N/A -- read-only. No commit.
```

---

## COMP_LEARNS.066 — Iter-6 Scoring (COMPLETE)

### Objective
Score iter-6 click compiler (class_hierarchy_summary node) against champion. Standard dev-loop scoring run.

### Pre-run Gate

```
git pull origin CLOUD --ff-only && git log --oneline -3
# 18563c7a feat(COMP_LEARNS.064): click compiler v6 -- class_hierarchy_summary node -- present on CLOUD PASS

python3 -c "import json; rows=[json.loads(l) for l in open('comp/results/dev-click-001/experiment_log.jsonl')]; print(len(rows), [r['iteration'] for r in rows])"
# 5 [1, 2, 3, 4, 5] -- PASS
```

### Scoring Run

```
ANTHROPIC_API_KEY=$(aws secretsmanager get-secret-value --secret-id anthropic-api-key --query SecretString --output text)
python3 comp/bin/comp-learns-ratchet click --judge real --max-iter 1 --compiler-content-sha ecaf3bc0
# Exit: MAX_ITER (10). Elapsed: 1:55. 33 fresh LLM calls.
```

Note: target name is `click` (not `dev-click-001`). `comp/targets/dev-click-001/` has no compiler.py; `comp/targets/click/` is the authoritative target. This was discovered during the session and is the correct invocation.

### Scorecard

Scorecard: `comp/targets/click/scorecards/8809a87_d869779f.json`

| Metric | Value |
|--------|-------|
| primary_metric | 0.0 |
| ab_lift (overall) | 0.0 |
| keyword lift | 0.0 |
| centrality lift | 0.0 |
| random lift | 0.0 |
| structural_f1 | 0.6545 |
| mutation_stability | 0.858 |
| token_reduction | ~0.955 |
| compiler_loc | 166 |
| random_unique_win | false |
| tied_at_best | true |
| PATTERN | C (all selectors flat at 0.0) |

**VERDICT: DISCARD** (ab_lift=0.0 < champion 0.1180, delta=-0.1180)

No question flipped vs H3-v2 baseline. q03 did NOT flip — the class_hierarchy_summary fact node did not correct the judge's class hierarchy reasoning.

### Artifacts Written

- `comp/dev-bundles/dev-click-001/iter-6/result.json` (schema_version=3)
- `comp/results/dev-click-001/experiment_log.jsonl` — iter-6 appended (manual backfill from runner-native log; runner appends to `comp/targets/click/experiment_log.jsonl` schema_version=2)

### Commit

```
git commit --author="2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>" \
  -m "score(COMP_LEARNS.066): click iter-6 scoring -- class_hierarchy_summary DISCARD" \
  -- comp/dev-bundles/dev-click-001/iter-6/result.json \
     comp/results/dev-click-001/experiment_log.jsonl
# Commit: 3fd4a31c
git push origin CLOUD
# Pushed: 8809a87f..3fd4a31c
```

### Post-commit Check

```
python3 -c "import json; rows=[json.loads(l) for l in open('comp/results/dev-click-001/experiment_log.jsonl')]; last=rows[-1]; print('iter-6 verdict:', last.get('verdict'), 'pm:', last.get('primary_metric'))"
# iter-6 verdict: DISCARD pm: 0.0 -- PASS
```

### Compiler Tools

```
Phase 1 (before run):
  git pull origin CLOUD --ff-only -- 18563c7a on CLOUD PASS
  experiment_log.jsonl: 5 entries [1,2,3,4,5] PASS

Phase 2 (after run, before commit):
  experiment_log.jsonl manually backfilled iter-6 (runner wrote to click/ target log, not dev-click-001/)
  6 entries [1,2,3,4,5,6] PASS

Phase 3 (after commit):
  iter-6 verdict: DISCARD pm: 0.0 PASS
```

### MCP

MCP sent to 2.1.0_SA_COO with verdict + ab_lift + per-selector breakdown + PATTERN call.
CC sent to 1.1.0_SA_CTO with same content.

---

## COMP_LEARNS.R-SC-1 — Scoring Regime Honesty Note (COMPLETE)

### Directive
R-SC-1 from 1.1.0_SA_CTO (via 3.1.0_SA_CVO review, 20260427T143500Z). Gate condition on .067 GO.

### Action
Formal scoring-regime honesty note written and committed before iter-7 scoring begins.

Artifact: `comp/results/dev-click-001/scoring_regime_honesty_note.md`
Commit: 7bc3c185 (pushed CLOUD)

### Finding
q02 and q11 ratchet-critical failure status is epistemically ambiguous. The proximate cause is
response-format variance, not semantic error. `float(full_response_text)` in `comp/bench/ab.py`
raises ValueError on verbose responses — judge reaches correct answer but grading fails.

- q11: H3-v2 response contains "Answer: 1" verbatim; float() fails on surrounding prose. H3-v2
  baseline is understated by at least 1 (minimum 9/11 under a format-aware grader).
- q02: all v0 cache responses verbose; format failure conflated with possible semantic error.
- iter-7 (q03): not affected — set_membership grader, different failure mode.
- R-SC-2 (audit label for "semantic-correct-but-unparseable"): deferred per CTO directive, required
  before iter-8.

MCP sent to 1.1.0_SA_CTO and 2.1.0_SA_COO. Hold cleared on SC side for .067 GO.

---

## Summary

| TO / Item | Status | Key Finding |
|-----------|--------|-------------|
| .065 | COMPLETE | v0 random win was q05 (not q02/q03/q11); all improvable questions WRONG for v0; format artifact (bare "Yes" vs "Yes." grader sensitivity) |
| .066 | COMPLETE | iter-6 DISCARD, ab_lift=0.0, PATTERN C; class_hierarchy_summary fact node produced no lift; q03 did not flip; commit 3fd4a31c |
| R-SC-1 | COMPLETE | Scoring-regime honesty note filed; q02/q11 ambiguity documented; commit 7bc3c185; .067 hold cleared |
