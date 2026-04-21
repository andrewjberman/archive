# COMP_LEARNS.012 -- Python Parser LibCST

**Agent:** 1.1.0_DS_CompLearns
**Date:** 2026-04-21
**TO:** `org/tier2_senior/1.1.0_DS_CompLearns/task_orders/COMP_LEARNS.012.python-parser-libcst.md`
**Commit:** `39d2e05b`

## Objective

Implement PythonParser (LibCST-backed) per Parser protocol from .011.
Consumed by .013 (imports subtype) and .021 (mutation engine).

## Work Completed

4 files:
- `comp/parsers/python.py` -- PythonParser; sha256 content_hash; ParseError on invalid Python
- `comp/parsers/__init__.py` -- exports PythonParser
- `comp/parsers/tests/test_python_parser.py` -- 24 tests
- `comp/parsers/tests/fixtures/invalid.py` -- bad-syntax fixture

## Compiler Tools

| Phase | Run | Observed | Expected | Result |
|-------|-----|----------|----------|--------|
| 1 | `python -c "import libcst; print(..."` | ModuleNotFoundError | version string | BLOCKED |
| 1 | pip install libcst | 1.8.6 installed | version | PASS |
| 1 | re-run libcst check | 1.8.6 | version | PASS |
| 1 | `ls comp/parsers/base.py comp/ir/schema.py` | both exist | both exist | PASS |
| 2 | `python -m pytest comp/parsers/ -v` | 24 passed | all pass exit 0 | PASS |
| 2 | end-to-end one-liner (httpx/__init__.py) | python 4fa3160a 2276 | language hash len | PASS |
| 3 | `comp-xref` | infra delta (unrelated portal nodes) | comp/ module visible | PASS (comp/ not in infra graph as expected) |

## Acceptance Criteria

| AC | Status |
|----|--------|
| 1. parse every httpx/*.py without exception | PASS (17 files) |
| 2. round-trip on >=10 modules (source == cst.code) | PASS (17/17) |
| 3. ParseError with path + line on invalid fixture | PASS |
| 4. content_hash stable across runs | PASS |
| 5. pytest comp/parsers/ exits 0 | PASS (24 tests) |
| 6. Session log Compiler Tools section | PASS (this doc) |
| 7. MCP COMPLETE to COO | PENDING (next) |

## Notes

LibCST installed locally (pip install libcst==1.8.6). AE 0.7.0 flagged via MCP
for layer policy decision. Local-only for now -- comp/ is pure research, no Lambda.

.013 and .021 are now unblocked.
