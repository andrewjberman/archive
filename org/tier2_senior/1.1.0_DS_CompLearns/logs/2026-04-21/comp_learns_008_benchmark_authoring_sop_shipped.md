# COMP_LEARNS.008 -- Benchmark Authoring SOP

**Agent:** 1.1.0_DS_CompLearns
**Date:** 2026-04-21
**TO:** `org/tier2_senior/1.1.0_DS_CompLearns/task_orders/COMP_LEARNS.008.benchmark-authoring-sop.md`
**Commit:** `2d7060b6`

## Objective

Turn CTO's qualitative framework 7-step protocol into a DS-runnable checklist + 4 template files.
Source: `COMP_LEARNS_QUALITATIVE_FRAMEWORK.md` (CTO 2026-04-15) + `COMP_LEARNS_HTTPX_TARGET.md`.

## Work Completed

7 files (1 modified, 6 created):
- `docs/architecture/COMP_LEARNS_BENCHMARK_AUTHORING_SOP.md` -- 192 lines; 7 steps 1:1; 3+ Goodhart guards; 5-dim quota table; 7-item CTO spot-check checklist
- `comp/framework/templates/SURFACE_INVENTORY.md.template`
- `comp/framework/templates/EDGE_TYPES.md.template`
- `comp/framework/templates/QUERY_MATRIX.yaml.template`
- `comp/framework/templates/VERIFIABILITY_AUDIT_CHECKLIST.md.template`
- `comp/framework/query_schema.py` -- added `validate_queries_file()` (SOP entry point alias)
- `comp/framework/tests/test_benchmark_sop.py` -- 5 tests

## Compiler Tools

| Phase | Run | Observed | Expected | Result |
|-------|-----|----------|----------|--------|
| 1 | `cat docs/architecture/COMP_LEARNS_QUALITATIVE_FRAMEWORK.md \| head -100` | 7-step protocol + 5 dims + 6 Goodhart modes visible | all readable | PASS |
| 1 | `cat docs/architecture/COMP_LEARNS_HTTPX_TARGET.md \| head -60` | PRD #2 pattern, httpx target, query quota table visible | readable | PASS |
| 2 | `python -c "from comp.framework.query_schema import validate_queries_file; validate_queries_file('comp/framework/templates/QUERY_MATRIX.yaml.template')"` | exit 0, no error | validates or expected-missing | PASS |
| 2 | `python -m pytest comp/framework/tests/test_benchmark_sop.py -v` | 5 passed | all pass exit 0 | PASS |
| 3 | `ls comp/framework/templates/` | 4 template files listed | 4 files | PASS |

## Acceptance Criteria

| AC | Status |
|----|--------|
| 1. SOP <=200 lines, maps 7 steps 1:1 | PASS (192 lines) |
| 2. 4 templates under comp/framework/templates/ | PASS |
| 3. Goodhart guards at >=3 steps | PASS (G2 at Steps 0, 1; G3 at Step 4; G5 at Step 3; G1 at Step 5; G4 at Step 6; G6 at Step 7) |
| 4. 5-dimension quota guidance present | PASS (quota table: 30/30/20/14/6) |
| 5. CTO spot-check checklist, 7 items | PASS |
| 6. validate_queries_file() accepts populated template (pytest) | PASS (5 tests) |
| 7. Session log Compiler Tools section | PASS (this doc) |
| 8. MCP COMPLETE to COO | PENDING (next) |

## Notes

- `counterfactual` tag is defined in SOP quota table (6%) but not in `TAG_VOCAB` in query_schema.py. The template uses only valid tags (simple_fact, single_hop, cross_surface). Pre-flagging to CTO: SOP references counterfactual as a 5th dimension per QUALITATIVE_FRAMEWORK but TAG_VOCAB has only 4 tags. DS lanes will hit a schema error when they try to tag counterfactual queries. Recommend CTO/COO file a follow-up TO to add `counterfactual` to TAG_VOCAB.
- validate_queries_file is now the canonical SOP entry point; load_queries remains the internal workhorse.
