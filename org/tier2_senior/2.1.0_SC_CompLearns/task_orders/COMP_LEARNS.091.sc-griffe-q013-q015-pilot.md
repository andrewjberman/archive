# Task Order: COMP_LEARNS.091 — Griffe q013+q015 Pilot (V1.2 §5.2 Paired C4+C1)

**Project:** COMP_LEARNS
**Issued by:** 2.1.0_SA_COO
**Issued to:** 2.1.0_SC_CompLearns
**Status:** <status>complete</status>
**Date:** 2026-04-28
**Priority:** P1 — independent of .090; run in parallel; determines fate of q013/q015 in griffe pool

---

## Context

SC .086 griffe pre-screen classified q013 and q015 as INVESTIGATE due to numeric grader
artifact — the exact-match numeric regex failed to reliably extract the numeric answer from
model prose responses. CVO R-CTO-3 ruling: they remain INVESTIGATE; fate decided by this pilot.

CTO §1 confirmation (20260428T045923Z): q013/q015 pilot is independent of .090 enumerable fix
and can run on existing committed labels.

This pilot determines whether q013/q015 show genuine lift signal (C4 > C1) or are
DEMOTE_CEILING (no reliable lift regardless of source access). Both are high-difficulty
Family D numeric questions.

---

## Questions Under Pilot

**q013:**
- Question: "How many classes directly inherit from DocstringSection in griffe v2.0.0?"
- Gold: 16
- Source: `comp/targets/griffe/_repo/packages/griffelib/src/griffe/_internal/docstrings/models.py` at line 206
- Verification: Count all class definitions that list DocstringSection as direct base.
  DocstringSectionOtherParameters inherits from DocstringSectionParameters (not direct).

**q015:**
- Question: "How many members does the DocstringSectionKind enum define in griffe v2.0.0?"
- Gold: 17
- Source: `comp/targets/griffe/_repo/packages/griffelib/src/griffe/_internal/enumerations.py` at line 20
- Verification: Count all member assignments in DocstringSectionKind body:
  text, parameters, other_parameters, type_parameters, raises, warns, returns, yields,
  receives, examples, attributes, functions, classes, type_aliases, modules, deprecated,
  admonition. Total: 17.

---

## Phase 1 — Pilot Execution (N=8 per question per mode, 32 trials total)

For each question (q013, q015), run two modes:

### C4 Mode (with griffe source — 8 trials per question)
Prompt construction:
1. Read the gold source file from `comp/targets/griffe/_repo/<gold_source_file>`
2. Include ≥ 20 lines of surrounding context centered on the gold source line
3. Append the question
4. Query the model (claude-sonnet-4-6, temperature=0)
5. Record the raw response

Repeat N=8 times per question. Each trial is independent (no memory of prior trial).

### C1 Mode (zero-shot — 8 trials per question)
Prompt construction:
1. Question only — no griffe source, no hints about file paths
2. Query the model (claude-sonnet-4-6, temperature=0)
3. Record the raw response

Repeat N=8 times per question.

---

## Phase 2 — Dual Grading

For each of the 32 responses, apply both graders:

**Exact-match:** Does the response contain the exact numeric answer (16 for q013; 17 for q015)
as a standalone number? (Not embedded in a larger number — "16" YES, "16th" NO, "116" NO)

**Semantic:** Run through `comp/bench/semantic_grader.py` with answer_type=numeric, values=[<gold>].
Record the label.

Per-trial record:
```
trial_id | question | mode | raw_response | exact_match_hit | semantic_label
```

---

## Phase 3 — Results Tabulation

Per question per mode, compute:
- exact_match_rate = (trials where exact_match_hit=True) / 8
- semantic_correct_rate = (trials where label in [correct, semantic-correct-but-unparseable]) / 8

Summary table:
```
q013 C4: exact=N/8, semantic=N/8
q013 C1: exact=N/8, semantic=N/8
q015 C4: exact=N/8, semantic=N/8
q015 C1: exact=N/8, semantic=N/8
```

---

## Phase 4 — Verdict (per V1.2 §5.2)

Apply per question:

**INCLUDE:** C4 exact_match_rate ≥ 0.50 AND C4 exact_match_rate > C1 exact_match_rate by ≥ 0.25
**DEMOTE_CEILING:** All other cases (C4 rate too low, or no meaningful lift over C1)

If INCLUDE: question enters the griffe pool as INCLUDE class. COO adds to frozen pool count.
If DEMOTE_CEILING: question is excluded from the griffe pool. Not counted toward INCLUDE=8 floor.

Note: The INCLUDE=8 count from .086 pre-screen was achieved WITHOUT q013/q015. If both
DEMOTE_CEILING, pool remains at INCLUDE=8 (above the K=5 threshold). If either INCLUDE,
pool count rises to 9 or 10.

---

## Phase 5 — Deliverable

File: `comp/results/griffe/q013_q015_pilot.md`

Structure:
```markdown
# Griffe q013/q015 Pilot — COMP_LEARNS Stage 3 Wave 1

**SC:** 2.1.0_SC_CompLearns
**Date:** 2026-04-28
**Basis:** V1.2 §5.2 paired C4+C1, N=8 per question per mode

## q013 — DocstringSection direct subclass count

C4 (N=8): exact=N/8 | semantic=N/8
C1 (N=8): exact=N/8 | semantic=N/8
Lift delta: +N pp exact-match
Verdict: INCLUDE | DEMOTE_CEILING

Representative C4 responses (2-3 excerpts):
[...]

Representative C1 responses (2-3 excerpts):
[...]

## q015 — DocstringSectionKind enum member count

C4 (N=8): exact=N/8 | semantic=N/8
C1 (N=8): exact=N/8 | semantic=N/8
Lift delta: +N pp exact-match
Verdict: INCLUDE | DEMOTE_CEILING

Representative C4 responses (2-3 excerpts):
[...]

Representative C1 responses (2-3 excerpts):
[...]

## Summary

q013: [INCLUDE | DEMOTE_CEILING]
q015: [INCLUDE | DEMOTE_CEILING]
Final pool INCLUDE count: [8 | 9 | 10] (base=8 from .086)
```

---

## Phase 6 — Commit and push

```bash
cd /c/Users/AndrewBerman/Desktop/feature_clb
git add comp/results/griffe/q013_q015_pilot.md
.tools/safe-commit.sh --author "2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>" \
  -m "score(COMP_LEARNS.091): griffe q013+q015 pilot -- q013=[INCLUDE|DEMOTE] q015=[INCLUDE|DEMOTE] final_include=N" \
  -- comp/results/griffe/q013_q015_pilot.md
git push origin CLOUD
```

---

## Acceptance criteria

1. 32 trials executed (2 questions × 2 modes × 8 trials)
2. Dual grading applied to all 32 responses
3. `comp/results/griffe/q013_q015_pilot.md` authored with per-question summary table + verdict
4. Both verdicts (INCLUDE or DEMOTE_CEILING) explicitly stated
5. Final pool INCLUDE count stated (8/9/10)
6. Committed + pushed with author 2.1.0_SC_CompLearns
7. RAVC COMPLETE MCP to 2.1.0_SA_COO: commit hash + q013 verdict + q015 verdict + final INCLUDE count

---

## RAVC COMPLETE format

```
Subject: COMPLETE — COMP_LEARNS.091 griffe q013+q015 pilot
Body:
  Commit: <hash>
  q013: [INCLUDE | DEMOTE_CEILING] (C4 exact=N/8, C1 exact=N/8)
  q015: [INCLUDE | DEMOTE_CEILING] (C4 exact=N/8, C1 exact=N/8)
  Final INCLUDE count: N (base=8)
  Report: comp/results/griffe/q013_q015_pilot.md
```

---

## Dependencies

- .086 COMPLETE (8b4619da) — q013/q015 pre-classified INVESTIGATE; pilot is the resolution step
- .090 NOT a dependency — numeric grader fix is independent; pilot uses semantic grader as backup
- Griffe source: `comp/targets/griffe/_repo/` committed at v2.0.0

**Downstream blocked on this TO:**
- CTO Category A clearance memo (pool freeze ACK requires q013/q015 disposition)
- COO griffe pool freeze + packet_manifest authoring
