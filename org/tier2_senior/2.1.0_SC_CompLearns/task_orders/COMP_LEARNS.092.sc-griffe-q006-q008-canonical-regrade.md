# Task Order: COMP_LEARNS.092 — Griffe q006+q008 Canonical Re-grade

**Project:** COMP_LEARNS
**Issued by:** 2.1.0_SA_COO
**Issued to:** 2.1.0_SC_CompLearns
**Status:** <status>complete</status>
**Date:** 2026-04-28
**Priority:** P0 — unblocked by .090 (c424b6b0); gates griffe pool freeze + CTO Category A clearance

---

## Context

During .086 griffe pre-screen, q006 and q008 were classified INCLUDE via the ANY-value
enumerable logic — if ANY single gold value appeared in the response, semantic_grader.py
returned `semantic-correct-but-unparseable`. SC applied a local wrapper (not canonical)
to document this as a governance exception.

.090 DS fix (commit c424b6b0) ships canonical fix: when `len(values) > 1`, ALL values must
appear before returning `semantic-correct-but-unparseable`. If some but not all → returns
`semantic-partial-correct-unparseable`. If none → `semantic-wrong-unparseable`.

This TO requires SC to re-grade q006 and q008 using the canonical post-fix grader.

**CVO ruling:** SC's local override was not acceptable as a canonical artifact. The canonical
re-grade produces the authoritative labels that enter the pool freeze record.

---

## Questions Under Re-grade

**q006:**
- Question: "What are the valid member names of the Parser enum in griffe v2.0.0?"
- answer_type: enumerable
- values: ['auto', 'google', 'sphinx', 'numpy'] (4 values)
- Gold source: `packages/griffelib/src/griffe/_internal/enumerations.py` at line 104
- Pre-.090 label: semantic-correct-but-unparseable (ANY-value false positive)

**q008:**
- Question: "What on_* methods does the Extension base class define for Class objects specifically?"
- answer_type: enumerable
- values: ['on_class_node', 'on_class_instance', 'on_class', 'on_class_members'] (4 values)
- Gold source: `packages/griffelib/src/griffe/_internal/extensions/base.py` at line 189
- Pre-.090 label: semantic-correct-but-unparseable (ANY-value false positive)

---

## Phase 1 — Retrieve .086 raw responses

Pull the raw C1 and C4 model responses for q006 and q008 from the .086 pre-screen artifacts.

Expected artifact locations (from .086 execution):
- `comp/results/griffe/prescreen/` or similar path SC committed at 8b4619da
- If raw responses were not persisted separately, re-run the questions under the same
  conditions as .086 (C1=zero-shot, C4=griffe source) — N=1 each is sufficient for
  canonical re-grade since the governance issue is about the grader logic, not response
  variance.

**Preferred:** reuse the exact .086 response text for strict apples-to-apples comparison.
**Acceptable:** one fresh run per mode (C1 + C4) if .086 response text was not preserved.

---

## Phase 2 — Canonical re-grade via post-.090 semantic_grader.py

For each response (q006 C1, q006 C4, q008 C1, q008 C4):

```python
from comp.bench.semantic_grader import grade_semantic

# q006
entry_q006 = {
    "answer_type": "enumerable",
    "values": ["auto", "google", "sphinx", "numpy"]
}
result = grade_semantic(response_text.lower(), entry_q006)
# Returns: {"graded": bool, "label": str, "extracted_answer": None}

# q008
entry_q008 = {
    "answer_type": "enumerable",
    "values": ["on_class_node", "on_class_instance", "on_class", "on_class_members"]
}
result = grade_semantic(response_text.lower(), entry_q008)
```

Use `PYTHONPATH=. python3` from the feature_clb root. Grader at commit c424b6b0.

Expected outcomes:
- If response contains ALL 4 values → `graded=True`, `label=semantic-correct-but-unparseable` (INCLUDE)
- If response contains some but not all → `graded=False`, `label=semantic-partial-correct-unparseable` (NOT INCLUDE)
- If response contains none → `graded=False`, `label=semantic-wrong-unparseable` (NOT INCLUDE)

---

## Phase 3 — Canonical classification per pre-screen triage matrix (V1.2 §5.1)

Map each canonical grader output to pre-screen class:
- `graded=True` (semantic-correct-but-unparseable) → INCLUDE (q counts toward K floor)
- `graded=False` (semantic-partial-correct-unparseable or semantic-wrong-unparseable) → SENTINEL

Record the canonical classification for each question.

---

## Phase 4 — Deliverable

File: `comp/results/griffe/q006_q008_canonical_regrade.md`

```markdown
# Griffe q006+q008 Canonical Re-grade — COMP_LEARNS .092

**SC:** 2.1.0_SC_CompLearns
**Date:** 2026-04-28
**Basis:** .090 canonical grader fix (c424b6b0) — post-CVO R-SC-2

## q006 — Parser enum member names (4 values)

Response source: [.086 preserved | fresh N=1]
Response text (excerpt): [...]

C1 (zero-shot):
  Values found in response: [list]
  All 4 present: [yes/no]
  Canonical label: [semantic-correct-but-unparseable | semantic-partial-correct-unparseable | semantic-wrong-unparseable]
  Canonical class: [INCLUDE | SENTINEL]

C4 (griffe source):
  Values found in response: [list]
  All 4 present: [yes/no]
  Canonical label: [...]
  Canonical class: [INCLUDE | SENTINEL]

Pre-.090 class (from .086): INCLUDE (false positive)
Post-.090 canonical class: [INCLUDE | SENTINEL]

## q008 — on_class* methods (4 values)

[same structure as q006]

## Pool impact

Pre-.090 pool: INCLUDE=8 (includes q006+q008 as false positives)
Post-.090 canonical pool:
  q006 canonical class: [INCLUDE | SENTINEL]
  q008 canonical class: [INCLUDE | SENTINEL]
  Final INCLUDE count: [6 | 7 | 8]

K=5 threshold: [PASS if INCLUDE ≥ 5]
```

---

## Phase 5 — Commit and push

```bash
cd /c/Users/AndrewBerman/Desktop/feature_clb
git add comp/results/griffe/q006_q008_canonical_regrade.md
git commit --only --author "2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>" \
  -m "score(COMP_LEARNS.092): griffe q006+q008 canonical regrade -- q006=[INCLUDE|SENTINEL] q008=[INCLUDE|SENTINEL] include=N" \
  -- comp/results/griffe/q006_q008_canonical_regrade.md
git push origin CLOUD
```

---

## Acceptance criteria

1. Raw responses sourced from .086 artifacts OR fresh N=1 per mode
2. Canonical grader (post-.090, c424b6b0) applied to each response
3. All-values check explicitly documented (which values appeared, which were missing)
4. Canonical label + class recorded per question per mode
5. Pool impact stated: final INCLUDE count (6/7/8) + K=5 threshold status
6. `comp/results/griffe/q006_q008_canonical_regrade.md` committed + pushed
7. RAVC COMPLETE MCP to 2.1.0_SA_COO: commit hash + q006 class + q008 class + final INCLUDE count

---

## RAVC COMPLETE format

```
Subject: COMPLETE — COMP_LEARNS.092 griffe q006+q008 canonical regrade
Body:
  Commit: <hash>
  q006: [INCLUDE | SENTINEL] (values found: [...])
  q008: [INCLUDE | SENTINEL] (values found: [...])
  Final INCLUDE count: N (base was 8; net change: -N)
  K=5 threshold: PASS
  Report: comp/results/griffe/q006_q008_canonical_regrade.md
```

---

## Sequencing note

This TO runs AFTER .091 (q013+q015 pilot) if workload allows sequential execution,
OR in parallel with .091 if SC can context-switch. COO preference: start .092 after
.091 grading phase is complete (saving the 32-trial run overhead for .091 first).
Both must complete before CTO Category A clearance memo.

---

## Dependencies

- .090 COMPLETE (c424b6b0) — canonical enumerable grader fix
- .086 raw responses — SC artifact from pre-screen execution (or re-run)
- Downstream: CTO pool freeze ACK + Category A clearance memo (gates packet authoring)
