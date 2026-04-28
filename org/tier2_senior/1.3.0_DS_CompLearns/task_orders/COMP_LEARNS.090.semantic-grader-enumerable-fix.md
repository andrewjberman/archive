# Task Order: COMP_LEARNS.090 — semantic_grader.py Multi-Value Enumerable Fix

**Project:** COMP_LEARNS
**Issued by:** 2.1.0_SA_COO
**Issued to:** 1.3.0_DS_CompLearns
**Status:** <status>complete</status>
**Completion commit:** <completion_commit>c424b6b0</completion_commit>
**Completion date:** <completion_date>2026-04-28</completion_date>
**Date:** 2026-04-28
**Priority:** P0 — gates SC re-run of q006+q008 and griffe pool freeze

---

## Context

During .086 griffe pre-screen, SC discovered that `semantic_grader.py` evaluates multi-value
enumerable questions using ANY-value logic (if ANY single gold value appears in response →
`semantic-correct-but-unparseable`). For q006 (Parser enum, 5 values) and q008 (on_class*
methods, 4 values), C1 responses contained one correct value by chance — causing false-positive
INCLUDE classifications. SC applied a manual wrapper to fix this locally.

CTO ruling (revised per CVO R-DS-1 + R-SC-2): hidden local fix is NOT acceptable as canonical
artifact. DS must patch `semantic_grader.py`; SC re-runs q006+q008 under the canonical post-fix
grader.

**Scope: enumerable multi-value fix ONLY.** Do NOT touch numeric regex, set_membership logic,
or any other grader section. The numeric regex issue (q013/q015) is deprioritized this cycle
per CTO revised ruling.

---

## Objective

Fix `comp/bench/semantic_grader.py` enumerable branch: when `len(values) > 1`, require ALL
values to appear in the response before returning `semantic-correct-but-unparseable`.
Single-value enumerable behavior is unchanged.

---

## Phase 0 — Baseline gate

```bash
cd /c/Users/AndrewBerman/Desktop/feature_clb
comp-build && pytest comp/ -v -q 2>&1 | tail -20
```

All tests must PASS before editing. If baseline is red: STOP. Surface to COO.

---

## Phase 1 — Code change

**File:** `comp/bench/semantic_grader.py`

**Current enumerable substring section (approximate lines 171–178):**
```python
    # Substring: any correct enum value appears as a word in prose
    for val in values:
        if val and val in stripped_lower:
            return {
                "graded": True,
                "label": "semantic-correct-but-unparseable",
                "extracted_answer": None,
            }
    return {"graded": False, "label": "semantic-wrong-unparseable", "extracted_answer": None}
```

**Required change:** Replace the substring section with multi-value-aware logic:

```python
    # Substring: for multi-value enumerable, ALL values must appear; for single-value, ANY.
    if len(values) > 1:
        found = [val for val in values if val and val in stripped_lower]
        if len(found) == len(values):
            return {
                "graded": True,
                "label": "semantic-correct-but-unparseable",
                "extracted_answer": None,
            }
        if found:
            return {
                "graded": False,
                "label": "semantic-partial-correct-unparseable",
                "extracted_answer": None,
            }
        return {"graded": False, "label": "semantic-wrong-unparseable", "extracted_answer": None}
    else:
        for val in values:
            if val and val in stripped_lower:
                return {
                    "graded": True,
                    "label": "semantic-correct-but-unparseable",
                    "extracted_answer": None,
                }
        return {"graded": False, "label": "semantic-wrong-unparseable", "extracted_answer": None}
```

**Do NOT touch:** phrase extraction section, direct comparison section, set_membership branch,
numeric branch, fallback section, or any other code.

---

## Phase 2 — Tests

Add ≥ 3 new tests to `comp/bench/tests/test_semantic_grader.py`. All four behaviors must be
covered (new tests may overlap):

**Test 1 — multi-value all present → semantic-correct-but-unparseable:**
```python
def test_enumerable_multi_value_all_present():
    entry = {"answer_type": "enumerable", "values": ["on_class_node", "on_class_instance", "on_class", "on_class_members"]}
    response = "The Extension class defines on_class_node, on_class_instance, on_class, and on_class_members for class-level hooks."
    result = grade(response, entry)
    assert result["graded"] is True
    assert result["label"] == "semantic-correct-but-unparseable"
```

**Test 2 — multi-value some present → semantic-partial-correct-unparseable:**
```python
def test_enumerable_multi_value_partial():
    entry = {"answer_type": "enumerable", "values": ["on_class_node", "on_class_instance", "on_class", "on_class_members"]}
    response = "The class defines on_class_node and on_class_instance methods."
    result = grade(response, entry)
    assert result["graded"] is False
    assert result["label"] == "semantic-partial-correct-unparseable"
```

**Test 3 — multi-value none present → semantic-wrong-unparseable:**
```python
def test_enumerable_multi_value_none_present():
    entry = {"answer_type": "enumerable", "values": ["on_class_node", "on_class_instance", "on_class", "on_class_members"]}
    response = "I don't know the specific hook methods defined for class objects."
    result = grade(response, entry)
    assert result["graded"] is False
    assert result["label"] == "semantic-wrong-unparseable"
```

Verify existing `test_enumerable_correct_in_prose` (single-value) still passes — do not modify it.

---

## Phase 3 — Gate check

```bash
pytest comp/ -v -q 2>&1 | tail -20
```

All tests must PASS. New tests must be present and green.

---

## Phase 4 — Pre-commit gate

```bash
.tools/ds-commit-gate.sh comp/bench/semantic_grader.py comp/bench/tests/test_semantic_grader.py
```

Must exit 0.

---

## Phase 5 — Commit and push

```bash
.tools/safe-commit.sh --author "1.3.0_DS_CompLearns <1.3.0_DS_CompLearns@opal.agent>" \
  -m "fix(semantic_grader): multi-value enumerable requires ALL values present (v1.2 grader fix)" \
  -- comp/bench/semantic_grader.py comp/bench/tests/test_semantic_grader.py
git push origin CLOUD
```

---

## Acceptance criteria

1. `comp/bench/semantic_grader.py` enumerable branch updated: multi-value → ALL-values check
2. Single-value enumerable behavior unchanged (existing tests pass)
3. ≥ 3 new tests: all-present (semantic-correct-but-unparseable), partial (semantic-partial-correct-unparseable), none-present (semantic-wrong-unparseable)
4. `pytest comp/` exits 0 — all tests pass, no regressions
5. `ds-commit-gate.sh` exits 0
6. Committed with author 1.3.0_DS_CompLearns + pushed to CLOUD
7. RAVC COMPLETE MCP to 2.1.0_SA_COO: commit hash + pytest count + gate output

---

## RAVC COMPLETE format

```
Subject: COMPLETE — COMP_LEARNS.090 semantic_grader enumerable fix
Body:
  Commit: <hash>
  pytest: N tests passed (N new)
  ds-commit-gate: PASS
  Change: comp/bench/semantic_grader.py enumerable branch -- multi-value ALL-values check
```

---

## Dependencies

- comp-build baseline must be green before editing
- Downstream: SC re-runs q006+q008 under canonical post-fix grader (gates griffe pool freeze)
