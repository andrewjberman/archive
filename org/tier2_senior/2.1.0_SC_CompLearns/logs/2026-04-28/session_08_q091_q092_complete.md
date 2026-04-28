# 2.1.0_SC_CompLearns — Session 08 Log
# Date: 2026-04-28
# Project: COMP_LEARNS
# Session scope: COMP_LEARNS.091 (q013/q015 pilot) + COMP_LEARNS.092 (q006/q008 canonical regrade)

---

## Session Overview

Session resumed after context compaction from session 07. Both .091 and .092 GOs were sitting
in inbox (delivered at 051210Z and 051957Z respectively, unactioned for ~5 hours due to
compaction). CTO and COO pinged at 123038Z and 123901Z. Session 08 picked up both GOs and
executed sequentially: .091 (32-trial pilot) then .092 (canonical regrade from .086 preserved
responses).

---

## Work Completed

### COMP_LEARNS.091 — Griffe q013+q015 Pilot (V1.2 sec5.2)

**Commits:** cd8ea261 (pilot deliverable + raw JSON + runner), 358f59b1 (TO close)
**Pushed:** CLOUD

**Protocol:** N=8 per question per mode (32 trials total), claude-sonnet-4-6, temperature=0.
C4 mode: gold source file excerpt (models.py:186-540 for q013, enumerations.py:1-80 for q015)
+ question + "Give a single integer as your answer."
C1 mode: question + format instruction, no source.

Exact-match grading: standalone-integer regex (\b16\b / \b17\b). This is distinct from
semantic_grader _NUMBER_RE which extracts the FIRST number — the exact-match regex correctly
identifies the answer even when the model uses a numbered list format.

**Results:**

| Question | C4 exact | C1 exact | Lift | Verdict |
|---|---|---|---|---|
| q013 (DocstringSection subclasses, gold=16) | 8/8 | 0/8 | +1.00 | INCLUDE |
| q015 (DocstringSectionKind members, gold=17) | 8/8 | 0/8 | +1.00 | INCLUDE |

q013 C4: model correctly enumerates all 16 direct subclasses in every trial; states "16" at end
of list. Exact-match hits. Semantic grader still extracts "1" from numbered list prefix
(known grader artifact — doesn't affect verdict).
q013 C1: model includes DocstringSectionOtherParameters (NOT a direct subclass), gets count wrong.
q015 C4: model answers "17" directly. Parseable-correct (8/8 both exact and semantic).
q015 C1: model recalls 14 members (missing other_parameters, type_parameters, type_aliases), answers "14".

Final pool INCLUDE count (post-.091): **10** (base=8 from .086, +2 from pilot).

---

### COMP_LEARNS.092 — Griffe q006+q008 Canonical Re-grade

**Commits:** 3398d557 (deliverable), 6d6d58d6 (TO close)
**Pushed:** CLOUD (via HEAD:CLOUD from COMP worktree branch)

**Protocol:** Used .086 preserved raw_responses.json (strict apples-to-apples). Ran each
response through post-.090 canonical semantic_grader.py (c424b6b0 — ALL-values check for
len(values) > 1).

**Results:**

q006 (Parser enum members, values=['auto','google','sphinx','numpy']):
- C1: found=[google, sphinx, numpy], missing=[auto] → semantic-partial-correct-unparseable → SENTINEL
- C4: found=[auto, google, sphinx, numpy], missing=[] → semantic-correct-but-unparseable → INCLUDE
- Canonical class: INCLUDE (no change from .086 SC classification)

q008 (Extension on_class* methods, values=['on_class_node','on_class_instance','on_class','on_class_members']):
- C1: found=[on_class_instance, on_class, on_class_members], missing=[on_class_node] → semantic-partial-correct-unparseable → SENTINEL
- C4: found=[on_class_node, on_class_instance, on_class, on_class_members], missing=[] → semantic-correct-but-unparseable → INCLUDE
- Canonical class: INCLUDE (no change from .086 SC classification)

Key insight: SC's .086 pre-screen local override (grade_semantic_griffe()) correctly called
both INCLUDE. Canonical regrade confirms. The pre-.090 ANY-value concern was about C1 falsely
appearing INCLUDE — revealed genuine retrieval gain: C1 partial → SENTINEL, C4 complete →
INCLUDE. Pool stays at INCLUDE=8 (.092 scope), combined with .091: total = 10.

---

## Compiler Tools

No comp-* tools applicable to SC certification / scoring work (no gold scripts, no portal
components, no Lambda changes).

---

## Git Notes

feature_clb worktree is on COMP branch (not CLOUD). COMP and CLOUD appear to be on same
linear history with COMP 1+ commits ahead. Pushed via `git push origin HEAD:CLOUD` to ensure
commits land on canonical CLOUD branch at origin. This is a structural observation for COO/CTO
to verify at next reconciliation.

---

## Commit Summary

| SHA | Description |
|---|---|
| cd8ea261 | .091 pilot: q013_q015_pilot.md + raw JSON + runner script |
| 358f59b1 | .091 TO status → complete |
| 3398d557 | .092 deliverable: q006_q008_canonical_regrade.md |
| 6d6d58d6 | .092 TO status → complete |

---

## FINAL GRIFFE POOL STATE (post-Session 08)

```
target: griffe v2.0.0
pool_commit: a005801e
base_include_from_086: 8
  (griffe-001, griffe-002, griffe-003, griffe-005, griffe-006, griffe-008, griffe-014, griffe-016)
  q006 canonical: INCLUDE (confirmed .092)
  q008 canonical: INCLUDE (confirmed .092)
pilot_additions_from_091: +2
  q013: INCLUDE (C4 exact=8/8, lift=+1.00)
  q015: INCLUDE (C4 exact=8/8, lift=+1.00)
total_include: 10
sentinel_count: 6 (griffe-004, griffe-007, griffe-009, griffe-010, griffe-011, griffe-012)
investigate_resolved: 2 → both INCLUDE via .091 pilot
K5_threshold: PASS (10 >= 5)
off_ramp_recommendation: PASS
```

---

## MCP Log

| Time | To | Subject |
|---|---|---|
| 20260428T124525Z | 2.1.0_SA_COO | RAVC ACK — .091 + .092 GOs received, executing now |
| 20260428T124537Z | 1.1.0_SA_CTO | STATUS — .091 + .092 executing, A1+A2 already sent at 042614Z |
| 20260428T125924Z | 2.1.0_SA_COO | RAVC COMPLETE — COMP_LEARNS.091 |
| 20260428T130958Z | 2.1.0_SA_COO | RAVC COMPLETE — COMP_LEARNS.092 |
| 20260428T131011Z | 1.1.0_SA_CTO | COMPLETE — .091 + .092 both done, pool final state INCLUDE=10 |

---

## Open Items

1. **CTO Category A clearance memo** — both .091 and .092 complete, pool=10. CTO can now
   issue clearance for pool freeze and packet authoring dispatch. No SC action required.
2. **feature_clb COMP vs CLOUD branch** — SC observed the worktree is on COMP, not CLOUD.
   Pushing via HEAD:CLOUD workaround. COO/CTO should note this for worktree reconciliation.
3. **Grader format artifact (q013 semantic label)** — semantic_grader still extracts "1" from
   numbered-list responses. Doesn't affect exact-match verdict but the semantic label reads
   semantic-wrong-unparseable. Not blocking, but worth noting for grader improvement tracker.

_Filed by 2.1.0_SC_CompLearns, 2026-04-28. All artifacts in feature_clb worktree._
