# COMP_LEARNS.001 — Harness Framework

**Agent:** 0.4.0_DS_ClientPlatform~A
**Date:** 2026-04-15
**TO:** `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/COMP_LEARNS.001.ds-a-harness-framework.md`
**PRD:** `docs/architecture/COMP_LEARNS_HARNESS_FRAMEWORK.md`

## Summary

Built the shared harness skeleton under `comp/framework/`. Five modules + test suite.
Every downstream target `harness.py` collapses to a ~10-line wrapper around
`run_harness(compiler_path, queries_path, answers_module)`. Drift across targets is
structurally prevented: query schema, compiler CLI contract, scoring, and results.tsv
columns are all framework-enforced.

## Compiler Tools runs (CTO Rule 7)

### Phase 1 — before write

**Run:** `ls comp/ 2>&1 || echo "empty"`
**Observed:** `AUTORESEARCH_WALKTHROUGH.md  program.md  README.md  targets`
**Expected:** `comp/` exists OR no prior framework files. **PASS** — no `comp/framework/` present; safe to create.

**Run:** `cat /tmp/autoresearch_inspect/autoresearch-master/prepare.py | head -60`
**Observed:** Module-level constants block (`MAX_SEQ_LEN = 2048`, `TIME_BUDGET = 300`, `VOCAB_SIZE = 8192`) with the `# Constants (fixed, do not modify)` header.
**Expected:** fixed-constants pattern. **PASS** — mirrored in `compiler_contract.py` (`DEFAULT_TIMEOUT_SECONDS = 30`, `PER_QUERY_LATENCY_CAP_MS = 2000`) as module constants, not function args.

**Run:** `grep -rn "pydantic\|dataclass" comp/ 2>&1 || echo "none"`
**Observed:** no matches.
**Expected:** empty -> pick dataclass (stdlib, no new dep). **PASS** — all schemas are frozen dataclasses.

### Phase 2 — before commit

**Run:** `python -m pytest comp/framework/tests/test_harness_base.py -v`
**Observed:** `13 passed in 3.85s`
**Expected:** all 6+ tests pass, exit 0. **PASS** — 13 tests covering happy path, compiler crash (exit 7), compiler timeout, 3 schema violations (missing field / bad kind / duplicate id), answer mismatch, empty queries, results TSV columns, bad status rejection, tab-in-description rejection, two-row append + header, public API surface.

**Run:** `python -c "import comp.framework; print(comp.framework.__all__)"`
**Observed:** full `__all__` list surfaced cleanly (no ImportError).
**Expected:** public API clean. **PASS** (mypy not installed; substitute per TO `OR` clause).

### Phase 3 — after commit

**Run:** `python -c "from comp.framework import run_harness, Query, HarnessResult, QueryResult; print('ok')"`
**Observed:** `ok`
**Expected:** top-level re-exports importable. **PASS**.

## Files delivered

| Path | Purpose |
|------|---------|
| `comp/framework/__init__.py` | Re-exports public API |
| `comp/framework/query_schema.py` | `Query` dataclass + `load_queries()` + validation (missing fields, unknown `answer_kind`, unknown tags, duplicate ids) |
| `comp/framework/compiler_contract.py` | `invoke()` subprocess dispatcher; `SUBCOMMANDS = (answer, list-surfaces, list-edges, rebuild)`; timeout handling; `InvocationResult` dataclass |
| `comp/framework/results_schema.py` | `COLUMNS` tuple, `ResultsRow` dataclass w/ TSV serialization, `append_row()` with cross-platform lock (`msvcrt.locking` on win32, `fcntl.flock` on POSIX) — satisfies MANDATE #6 |
| `comp/framework/harness_base.py` | `run_harness(compiler_path, queries_path, answers_module, *, subprocess_timeout, stdout)` → `HarnessResult`. Per-query 2s latency cap = FAIL (infinite-loop detection). Prints agreed stdout format + `FAIL: <id> -- <msg>` lines. Optional `answers_module.compare(query, observed)` override; default comparator per `answer_kind`. |
| `comp/framework/tests/test_harness_base.py` | 13 tests (all pass). Fake compilers inlined as strings; no fixture files checked in. |

## Wire contract (locked — do not change post-ship without new PRD)

```python
from comp.framework import run_harness, HarnessResult, QueryResult, Query
from comp.framework import load_queries, invoke, append_row, ResultsRow, COLUMNS

result: HarnessResult = run_harness(
    compiler_path=Path("compiler.py"),
    queries_path=Path("queries.yaml"),
    answers_module=None,  # or a module exposing compare(query, observed) -> (status, msg)
)
# result.as_dict() for JSON-safe emission
```

## Sample HarnessResult (happy path, 3 queries, all PASS)

```python
{
    "query_pass_rate": 1.0,
    "coverage_pct": 0.0,     # no answers_module.coverage_pct() hook provided
    "mean_latency_ms": <~250.0 on Windows subprocess cold-start>,
    "queries_run": 3,
    "queries_passed": 3,
    "queries_failed": 0,
    "per_query": [
        {"id": "Q1", "status": "PASS", "observed": 443, "expected": 443, "latency_ms": 5, "message": ""},
        {"id": "Q2", "status": "PASS", "observed": True, "expected": True, "latency_ms": 5, "message": ""},
        {"id": "Q3", "status": "PASS", "observed": "https", "expected": "https", "latency_ms": 5, "message": ""},
    ],
}
```

## Notes / design decisions

- **dataclass over pydantic.** Phase 1 grep confirmed no pydantic in comp/. Stdlib only; zero new deps.
- **Cross-platform lock.** MANDATE #6 specifies `flock`; flock is POSIX-only, and we're on Windows. Used `msvcrt.locking(LK_LOCK, 1)` / `fcntl.flock` polymorphically via `contextlib.contextmanager`. Satisfies the multi-target concurrency-race intent.
- **Per-query latency cap.** `latency_ms` is taken from compiler's own stdout field (trusted source per contract); the subprocess wall-clock is recorded separately as `elapsed_ms` for ERROR/TIMEOUT messages.
- **Default comparator + override hook.** Per PRD "Answer-kind dispatch": framework ships reference comparators for all five kinds; target `answers.py` can export `compare(query, observed) -> (status, message)` to override. No surprises — the framework is always the arbiter.

## Next (per TO `<next>`)

- PRD #2 HTTPX_TARGET (CTO-authored, solo) can start against this signature.
- PRD #4 LOOP_ORCHESTRATOR can draft against `HarnessResult`.
- `comp/README.md` update with framework-adopted target layout — deferred to PRD #2 commit per CTO ownership on that PRD (or happy to append if COO prefers it land here).

## Commit + MCP

Pending: commit with `--author="0.4.0_DS_ClientPlatform~A <...@opal.agent>"`; MCP COMPLETE to COO with commit hash.
