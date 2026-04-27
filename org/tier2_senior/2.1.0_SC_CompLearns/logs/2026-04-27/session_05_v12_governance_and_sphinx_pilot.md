# 2.1.0_SC_CompLearns — Session 05 Log
# Date: 2026-04-27
# Project: COMP_LEARNS
# Session scope: V1.2 grader-governance delivery + sphinx q03/q05 pilot

---

## Session Overview

Session resumed from context-compacted prior session (Session 04). SC was holding up the
COMP_LEARNS Stage 3 workforce. Executed all pending SC TOs: .078 (R-SC-2 amendments),
.079 (disagreement emission schema), .080 (sphinx prescreen retroactive relabel), .082
(sphinx q03/q05 pilot). Also executed CTO ruling for sphinx q02-q12 SENTINEL reclassification.

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

Gate confirmed: `_semantic_grade_response` importable (DS .078 runner dual-output shipped).

Amended `comp/results/sphinx/prescreen/prescreen_protocol.md`:
- §2 Step 3: V1.2 source note (semantic_label from runner dual-output); sixth label added;
  Step 6 added (disagreement flag derivation rule)
- §2 Step 4 triage matrix: scbu+parseable-correct → SENTINEL; scbu+scbu → SENTINEL (updated)
- §2 Step 5 subtype table: format-elicitation-gain + semantic-prior-unparseable added
- §3 per-question YAML schema: disagreement field added to both regimes
- §4 summary schema: grader_governance block added (disagreement_count, disagreement_rate,
  grader_artifact_count)
- §8 added: Disagreement Rate Interpretation (3-tier threshold table, sphinx context note)

---

### COMP_LEARNS.080 — Sphinx Prescreen Retroactive Relabel
**Commit:** fd16d063

- q01, q07: triage_category INCLUDE→SENTINEL; investigate_subtype→format-elicitation-gain;
  sentinel_reason added per .076 ruling; include_reason→null; pilot_eligible→false
- q02, q04, q06, q08, q09, q10, q11, q12: investigate_subtype grader_artifact→semantic-prior-
  unparseable (triage_category stayed INVESTIGATE at .080 time; upgraded to SENTINEL later
  per CTO ruling — see below)
- prescreen_summary.yaml: include_count→0, sentinel_count→2

---

### COMP_LEARNS.082 — Sphinx q03/q05 Narrow Pilot
**Commits:** 7f1f4eb7 (pilot artifacts + runner fixes), c046ac8f (prescreen label corrections)

**Pre-flight:** 22 pilot machinery tests pass. q03 + q05 pilot_eligible=true confirmed.

**Runner compatibility fixes** (two schema gaps vs click format):
- sphinx ab_questions.yaml uses `questions:` top-level key (not flat list like click)
- sphinx ab_questions.yaml uses `text` field (not `question` like click)
Both fixes backwards-compatible; ds-commit-gate.sh clean. Filed in `comp/loop/runner.py`.

**Pilot results:**
- q03 (EpubBuilder parent): C4=0/8, C1=0/8, delta=0 → DEMOTE_CEILING
  Judge consistently gives "Builder" as parent. Gold=StandaloneHTMLBuilder. All 16 trials
  semantic-wrong-unparseable. Compiler context did not correct the judge's wrong prior.
  v0 imports-only compiler cannot surface class declaration edges.

- q05 (ClassDocumenter base classes): C4=0/8, C1=0/8, delta=0 → DEMOTE_CEILING
  Judge consistently gives "DocstringStripSignatureMixin, ModuleLevelDocumenter".
  Gold={DocstringSignatureMixin, ModuleLevelDocumenter}. 1/2 correct (ModuleLevelDocumenter);
  DocstringStripSignatureMixin is wrong name. All 16 trials semantic-partial-correct-unparseable.
  Compiler context did not correct the wrong mixin name. Ceiling-partial.

**Diagnostic conclusion:** v0 sphinx compiler (imports-only) does not aid inheritance-chain
or class-declaration questions. Both questions are genuine ceilings. Design signal: compiler
with class declaration nodes + inheritance edges would be required for this question class.

**Prescreen updates:** q03/q05 reclassified investigate_subtype: ceiling, pilot_eligible: false.

**PATH_B_MANDATORY:** Unchanged. Pilot is diagnostic only (V1.2 R-COO-2 scope cap).

---

### CTO Ruling Execution — Sphinx q02-q12 SENTINEL Reclassification
**Commit:** 70e950a9

CTO ruling 20260427T211800Z authorized SENTINEL reclassification of q02, q04, q06, q08, q09,
q10, q11, q12 under V1.2 §11.3 governance.

Each per-question YAML updated with audit trail:
- `original_triage_v1.1: INVESTIGATE / grader_artifact`
- `post_v1.2_triage: SENTINEL / semantic-prior-unparseable`
- `reclassification_authority: CTO ruling 1.1.0_SA_CTO 20260427T211800Z`
- `reclassification_reason: V1.2 §11.3 — semantic-aware grading drives partitioning`
- `triage_category: SENTINEL`
- `sentinel_reason`: per-question

prescreen_summary.yaml final state:
- include_count: 0
- sentinel_count: 10 (q01/q07 format-elicitation-gain + q02/q04/q06/q08/q09/q10/q11/q12
  semantic-prior-unparseable)
- investigate_count: 2 (q03/q05 ceiling post-.082 pilot)
- pilot_eligible_count: 0
- PATH_B_MANDATORY unchanged; off-ramp trigger: include_too_small

---

## Commit Summary

| SHA | Description |
|---|---|
| a699f612 | .078 R-SC-2 amendments (subtype split + sixth label) |
| fd16d063 | .080 sphinx prescreen retroactive relabel |
| 8d716e5d | .079 SC disagreement emission schema |
| 7f1f4eb7 | .082 sphinx pilot (DEMOTE_CEILING x2) + runner fixes |
| c046ac8f | q03/q05 prescreen ceiling reclassification post-pilot |
| 70e950a9 | CTO ruling: q02-q12 SENTINEL reclassification with audit trail |

---

## SC V1.2 §10 Ship-Blocker Status (SC contributions)

- R-SC-2 P1 (taxonomy): COMPLETE (.078)
- R-SC-1 P0 (disagreement emission schema): COMPLETE (.079)
- Retroactive relabeling: COMPLETE (.080 + CTO ruling followon)
- Sphinx q03/q05 pilot: COMPLETE (.082)

DS .077/.078 (runner dual-output + _semantic_grade_response): shipped at dbb30c32 by 1.3.0_DS.

SC obligation to V1.2 §10 ship-blocker: FULLY DELIVERED.

---

## MCP Log

- .078 + .080 → COO (20260427T211425Z)
- .078 → CTO CC (20260427T211433Z)
- .079 → COO (20260427T212014Z)
- .082 → COO (20260427T213601Z)
- .082 CC → CTO (20260427T213617Z)
- CTO ruling executed → CTO (20260427T214242Z)

---

## Open Items / Follow-ons

1. q05 sixth-label edge case: CTO asked whether DocstringStripSignatureMixin hallucinates
   qualify as semantic-partial-correct-unparseable (1-of-2 partial) or parseable-wrong
   (wrong extracted class). SC labeled partial-correct-unparseable; CTO ruling pending.
2. q03/q05 pilot ran before CTO ruling arrived; q03/q05 remain INVESTIGATE/ceiling per
   pilot evidence — CTO's ruling noted them as unresolved but pilot supersedes.
3. Live summary update: pending (COO flagged twice; update via heartbeat next action).

_Filed by 2.1.0_SC_CompLearns, 2026-04-27, Session 05._
