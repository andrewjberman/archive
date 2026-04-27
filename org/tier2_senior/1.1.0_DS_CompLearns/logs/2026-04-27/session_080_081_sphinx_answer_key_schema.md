# Session: COMP_LEARNS.080 + .081 -- Sphinx Answer Key Schema Conversion

**Date:** 2026-04-27
**Task Orders:** COMP_LEARNS.080 (covered by .081) + COMP_LEARNS.081 (primary)
**Status:** COMPLETE
**Commit:** c5f5c89d

---

## Objective

Convert comp/targets/sphinx/gold/ab_answer_key.yaml from the narrative gold_answer/gold_source_file
schema (authored in .074) to the canonical answer_type/values schema required by _grade_response()
and the ratchet runner. All 12 sphinx questions currently graded False under the standard runner.

Two GOs received simultaneously (.080 and .081 both dispatched for same task). .081 is the
authoritative version (canonical flat-key format + provenance file split). .080 fully covered.

---

## Compiler Tools

| Phase | Tool | Command | Result | Pass/Fail |
|-------|------|---------|--------|-----------|
| before commit | YAML safe_load (ab_answer_key.yaml) | python3 yaml.safe_load | No exception, 12 keys | PASS |
| before commit | YAML safe_load (ab_answer_key_provenance.yaml) | python3 yaml.safe_load | No exception, 12 keys | PASS |
| before commit | Grader self-test | _grade_response(gold, entry) x12 | 12/12 True | PASS |
| before commit | q05 order-independence | _grade_response(reversed order) | True | PASS |
| before commit | wrong-answer rejection | _grade_response(wrong, q01_entry) | False | PASS |
| before commit | pytest regression | python -m pytest comp/ --ignore=comp/targets -q | 480 passed, 0 failed | PASS |

---

## Work Completed

### Phase 0 — Schema review

Read both schemas:
- Current sphinx: `answers:` list format, fields: id, gold_answer, gold_source_file, gold_source_line, verification_note
- Reference click: flat-key format `q01:` etc., fields: pool, answer_type, values/value/tolerance

Grader function confirmed (_grade_response in comp/bench/ab.py):
- enumerable: text.lower().strip() in [str(v).lower().strip() for v in entry.get("values", [])]
- set_membership: raw_set (comma-split, lowered) == gold_set (lowered)
- numeric: abs(float(text) - entry.get("value")) <= entry.get("tolerance")

### Phase 1 — answer_type assignments

| QID | Gold Answer | answer_type | Rationale |
|-----|-------------|-------------|-----------|
| q01 | register_directive | enumerable | single function name |
| q02 | directives.register_directive | enumerable | single dotted name |
| q03 | StandaloneHTMLBuilder | enumerable | single class name |
| q04 | ClassDocumenter | enumerable | single class name |
| q05 | DocstringSignatureMixin, ModuleLevelDocumenter | set_membership | two base classes, order may vary |
| q06 | none | enumerable | single string value |
| q07 | I18nBuilder | enumerable | single class name |
| q08 | doctree-resolved | enumerable | single event name |
| q09 | doctree-read | enumerable | single event name |
| q10 | Directive | enumerable | single class name |
| q11 | setup | enumerable | single function name |
| q12 | BaseAdmonition | enumerable | single class name |

All assignments match TO Phase 1 table exactly. No deviations.

### Phase 2 — Files written

**ab_answer_key.yaml** — rewritten to canonical flat-key format:
- Top-level keys: q01-q12
- Each entry: pool: ratchet_critical, answer_type, values
- Header comment documents schema convention
- Provenance fields removed (moved to provenance file)

**ab_answer_key_provenance.yaml** (new file):
- Top-level keys: q01-q12
- Each entry: gold_answer, gold_source_file, gold_source_line, verification_note
- Preserves full audit trail from .074 original authoring

### Phase 3 — Validation

- YAML load: PASS both files
- Self-grade 12/12: PASS
- q05 order-independent: PASS
- pytest 480/0: PASS

### Phase 4 — Commit + push

Commit: c5f5c89d — 4 files changed: ab_answer_key.yaml (converted) + ab_answer_key_provenance.yaml (new) + .080 TO (complete) + .081 TO (complete)
Push: CLOUD confirmed

### Phase 5 — MCP

MCP 2.1.0_SA_COO at 20260427T203140Z with commit sha + validation summary.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Execute .081 as authoritative (not .080) | .081 is more complete: flat-key format + provenance file split. Both TOs dispatched for same task; .081 supersedes .080. |
| Mark .080 complete with note | .080 acceptance criteria fully satisfied by .081 deliverable. Single commit covers both. |
| Provenance to separate file (not inline) | .081 TO spec: "Keep gold_source_file and verification_note in a separate companion file." Keeps grader-facing schema clean. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| comp/targets/sphinx/gold/ab_answer_key.yaml | Rewritten: flat-key canonical schema, 12 entries | c5f5c89d |
| comp/targets/sphinx/gold/ab_answer_key_provenance.yaml | New: source audit trail for all 12 entries | c5f5c89d |
| org/tier2_senior/1.1.0_DS_CompLearns/task_orders/COMP_LEARNS.080.ds-sphinx-answer-key-schema.md | Status: complete | c5f5c89d |
| org/tier2_senior/1.1.0_DS_CompLearns/task_orders/COMP_LEARNS.081.ds-sphinx-answer-key-schema-fix.md | Status: complete | c5f5c89d |

---

## Blockers

None.

---

## Current State

.080 and .081 complete (c5f5c89d on CLOUD). Sphinx ab_answer_key.yaml now fully compatible with
_grade_response() — all 12 questions will grade correctly under the standard runner.
Downstream: .081 (SC sphinx q03/q05 pilot) can now use load_answer_key() + _grade_response() directly.

Standing by for next dispatch (R-DS-1 runner dual-output TO expected from COO).

---

## Next Steps

1. Await R-DS-1 TO from COO (runner dual-output emission, V1.2 grader-governance)
2. Watchdog mode at 270s cadence until next dispatch
