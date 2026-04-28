# 2.1.0_SC_CompLearns — Session 05 Log
# Date: 2026-04-27
# Project: COMP_LEARNS
# Session scope: V1.2 grader-governance delivery + sphinx q03/q05 pilot + pool closeout

---

## Session Overview

Session resumed from context-compacted prior session (Session 04). SC was holding up the
COMP_LEARNS Stage 3 workforce. Executed all pending SC TOs: .078 (R-SC-2 amendments),
.079 (disagreement emission schema), .080 (sphinx prescreen retroactive relabel), .082
(sphinx q03/q05 pilot). Also executed three CTO rulings: q02-q12 SENTINEL reclassification,
q05 trial label correction (parseable-wrong), q03/q05 triage → SENTINEL/ceiling.

---

## Work Completed

### COMP_LEARNS.078 — R-SC-2 Taxonomy Amendment
**Commit:** a699f612

Amended `comp/results/r_sc_2_semantic_labels.md`:

1. **grader_artifact subtype split** (§4.3a + §4.3b):
   - §4.3a `format-elicitation-gain`: zs=scbu, fs=parseable-correct; judge already correct;
     context only changed format. SENTINEL. pilot_eligible=false. Sphinx q01/q07 confirmed.
   - §4.3b `semantic-prior-unparseable`: both regimes scbu; judge correct in both; context
     unchanged gradeability. SENTINEL. pilot_eligible=false. Sphinx q02/q04/q06/q08-q12 confirmed.
   - Legacy `grader_artifact` documented as retired.

2. **Sixth label** §1.6 `semantic-partial-correct-unparseable`:
   - M of N gold set members in prose; rest absent (not asserted-wrong)
   - 5 cross-regime subtype rules (promote/grader_artifact/escalate/anomaly/full_source_overload)
   - Multi-trial guard >=4/6 stable coverage
   - click q03 confirmed parseable-wrong (not partial-correct)

3. **§3 triage table updated**: scbu+parseable-correct → SENTINEL (format-elicitation-gain);
   scbu+scbu → SENTINEL (semantic-prior-unparseable); partial-correct rows added.

4. **§7 amendment log** added. Total named values: 6 primary labels + 5 subtypes = 11.

---

### COMP_LEARNS.079 — SC Disagreement Emission Schema
**Commit:** 8d716e5d

Gate confirmed: `_semantic_grade_response` importable (DS .078 runner dual-output shipped at dbb30c32).

Amended `comp/results/sphinx/prescreen/prescreen_protocol.md`:
- §2 Step 3: V1.2 source note (semantic_label from runner dual-output); sixth label added;
  Step 6 added (disagreement flag derivation rule)
- §2 Step 4 triage matrix: scbu+parseable-correct → SENTINEL; scbu+scbu → SENTINEL
- §2 Step 5 subtype table: format-elicitation-gain + semantic-prior-unparseable added
- §3 per-question YAML schema: disagreement field added to both regimes
- §4 summary schema: grader_governance block added
- §8 added: Disagreement Rate Interpretation (3-tier threshold table)

---

### COMP_LEARNS.080 — Sphinx Prescreen Retroactive Relabel
**Commit:** fd16d063

- q01, q07: triage_category INCLUDE→SENTINEL; investigate_subtype→format-elicitation-gain;
  sentinel_reason per .076; pilot_eligible→false
- q02, q04, q06, q08, q09, q10, q11, q12: investigate_subtype grader_artifact→semantic-prior-unparseable
- prescreen_summary.yaml: include_count→0, sentinel_count→2 (interim; upgraded later per CTO rulings)

---

### COMP_LEARNS.082 — Sphinx q03/q05 Narrow Pilot
**Commits:** 7f1f4eb7 (pilot artifacts + runner fixes), c046ac8f (initial prescreen label corrections)

**Pre-flight:** 22 pilot machinery tests pass. q03 + q05 pilot_eligible=true confirmed.
Compiler sha: 768213db.

**Runner compatibility fixes** bundled with pilot commit (`comp/loop/runner.py`):
- sphinx ab_questions.yaml uses `questions:` top-level key (not flat list like click)
- sphinx ab_questions.yaml uses `text` field (not `question` like click)
Both backwards-compatible; ds-commit-gate.sh clean.

**Pilot results (32 total trials):**

- **q03** (EpubBuilder direct parent, gold=StandaloneHTMLBuilder):
  C4=0/8, C1=0/8, delta=0 → DEMOTE_CEILING
  All 16 trials: semantic-wrong-unparseable. Judge gives "Builder" consistently.
  v0 imports-only compiler cannot surface class declaration inheritance edges.

- **q05** (ClassDocumenter base classes, gold={DocstringSignatureMixin,ModuleLevelDocumenter}):
  C4=0/8, C1=0/8, delta=0 → DEMOTE_CEILING
  All 16 trials: judge gives DocstringStripSignatureMixin+ModuleLevelDocumenter.
  1/2 gold members correct (ModuleLevelDocumenter); DocstringStripSignatureMixin is wrong name.
  Initial semantic label: semantic-partial-correct-unparseable (revised per CTO ruling below).

**Diagnostic conclusion:** v0 sphinx compiler does not aid inheritance-chain or class-declaration
questions. Design signal: class declaration nodes + inheritance edges required for this question class.

PATH_B_MANDATORY unchanged. Pilot diagnostic only (V1.2 R-COO-2 scope cap).

---

### CTO Ruling 1 — Sphinx q02-q12 SENTINEL Reclassification
**Commit:** 70e950a9
**Authority:** CTO ruling 20260427T211800Z

q02, q04, q06, q08, q09, q10, q11, q12 reclassified INVESTIGATE→SENTINEL with full audit trail:
- `original_triage_v1.1: INVESTIGATE / grader_artifact`
- `post_v1.2_triage: SENTINEL / semantic-prior-unparseable`
- `reclassification_authority` and `reclassification_reason` per CTO spec
- sentinel_count: 2→10

---

### CTO Ruling 2 + 3 — q05 Trial Relabel + q03/q05 → SENTINEL/ceiling
**Commit:** 8c95a5b4
**Authority:** CTO rulings 20260427T213841Z + 20260427T214600Z

**Ruling 2 (q05 trial relabel):** semantic-partial-correct-unparseable → parseable-wrong for all 16 q05 trials.
Reasoning: DocstringStripSignatureMixin is asserted-wrong (positive claim), not absent.
§1.6 requires rest ABSENT (not asserted). Near-miss hallucination = parseable-wrong.
Audit trail preserved per trial (original_label_v1.2 + label_correction fields).

**Ruling 3 (q03/q05 triage → SENTINEL):** V1.2 §5.2 demotion rule — C4 ≤ 1/8 → SENTINEL.
- q03: triage_category INVESTIGATE→SENTINEL; sentinel_reason: ceiling-no-knowledge
- q05: triage_category INVESTIGATE→SENTINEL; sentinel_reason: ceiling-near-miss

**prescreen_summary.yaml FINAL STATE:**
- include_count: 0
- sentinel_count: 12
- investigate_count: 0
- pilot_eligible_count: 0
- final_pool_after_pilot breakdown: format_elicitation_gain=[q01,q07]; semantic_prior_unparseable=[q02,q04,q06,q08,q09,q10,q11,q12]; ceiling_no_knowledge=[q03]; ceiling_near_miss=[q05]

---

## Commit Summary

| SHA | Description |
|---|---|
| `a699f612` | .078 R-SC-2 amendments (subtype split + sixth label) |
| `fd16d063` | .080 sphinx prescreen retroactive relabel |
| `8d716e5d` | .079 SC disagreement emission schema |
| `7f1f4eb7` | .082 sphinx pilot (DEMOTE_CEILING x2) + runner schema fixes |
| `c046ac8f` | q03/q05 prescreen ceiling reclassification (interim) |
| `70e950a9` | CTO ruling 1: q02-q12 SENTINEL + audit trail (sentinel=10) |
| `3a109444` | Session log (interim) |
| `8c95a5b4` | CTO rulings 2+3: q05 parseable-wrong relabel + q03/q05 SENTINEL/ceiling; sphinx pool FINAL SENTINEL=12 |

---

## SC V1.2 §10 Ship-Blocker — Contributions

| Item | Status |
|---|---|
| R-SC-2 P1 taxonomy amendment (.078) | COMPLETE |
| R-SC-1 P0 disagreement emission schema (.079) | COMPLETE |
| Retroactive relabeling (.080) | COMPLETE |
| Sphinx q03/q05 pilot (.082) | COMPLETE |
| CTO ruling followons (pool closeout) | COMPLETE |

DS .077/.078 (runner dual-output): shipped at dbb30c32 by 1.3.0_DS.

SC obligation to V1.2 §10 ship-blocker: **FULLY DELIVERED.**

---

## Sphinx Pool — Final State

Sphinx is closed as a measurement-room target under V1.2 semantic-aware triage.
INCLUDE=0 / SENTINEL=12 / INVESTIGATE=0. PATH_B_MANDATORY unchanged.
CVO brief 213900Z supplement reflects this pool state.

---

## MCP Log

| Time | To | Subject |
|---|---|---|
| 20260427T211425Z | COO | .078 + .080 COMPLETE |
| 20260427T211433Z | CTO | .078 CC |
| 20260427T212014Z | COO | .079 COMPLETE |
| 20260427T213601Z | COO | .082 COMPLETE |
| 20260427T213617Z | CTO | .082 CC |
| 20260427T214242Z | CTO | CTO ruling 1 executed (70e950a9) |
| 20260427T214813Z | CTO | CTO rulings 2+3 executed (8c95a5b4) |

---

## Open Items

1. Path B target re-selection — SC input may be needed on question pool triage for new target.
   Awaiting Path B sub-PRD from CTO/COO.
2. sphinx revisit scope: if Path B target proves insufficient, sphinx may serve as shakedown
   target with improved compiler (class declaration nodes needed per .082 pilot finding).
3. Session log for .072/.075 work (authored in prior sessions) exists at session_03/session_04;
   this log covers session 05 only.

_Filed by 2.1.0_SC_CompLearns, 2026-04-27, Session 05. All logs in feature_clb worktree._
