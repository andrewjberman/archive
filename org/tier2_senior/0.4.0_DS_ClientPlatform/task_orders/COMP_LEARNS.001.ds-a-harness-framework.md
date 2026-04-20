<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform~A-2026-04-15-comp-learns-001-harness-framework</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- COO flip 2026-04-16. ~A shipped comp/framework/ harness skeleton 43e3225e (PRD #1 of 5) + elapsed_ms diagnostic 714d43a9. Framework foundational; unblocks #2/#3/#4/#5. -->
    <evidence>
      Shipped: commits 43e3225e (comp/framework/ harness skeleton — PRD #1 of 5) and 714d43a9 (QueryResult.elapsed_ms diagnostic add per CTO).
      Artifacts: comp/framework/harness_base.py, comp/framework/query_schema.py, comp/framework/compiler_contract.py, comp/framework/results_schema.py, comp/framework/tests/smoke.py, comp/framework/tests/test_harness_base.py, comp/README.md.
      Validation: pytest comp/framework/ passes — 6+ cases (happy path, compiler-crash, subprocess-timeout, malformed-yaml, duplicate-id, missing-answer). Smoke test instantiates all four pieces with a 3-query fake target and reports green.
      Session log: org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-15/.
    </evidence>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — foundational; unblocks 2 + 4</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_HARNESS_FRAMEWORK.md (PRD #1 of 5)</ref>
    <ref type="doctrine">docs/architecture/COMP_LEARNS_QUALITATIVE_FRAMEWORK.md (CTO benchmark epistemics)</ref>
    <ref type="mandate">docs/architecture/COMP_LEARNS_OPERATIONAL_MANDATE.md (8 non-negotiables for COO engine)</ref>
    <ref type="precedent">autoresearch-master/prepare.py (fixed-constants-never-modified pattern — our harness_base.py plays this role)</ref>
  </references>

  <objective>
    Build reusable harness skeleton `comp/framework/` that every per-target harness consumes. Enforces:
    1. Fixed query schema (`query_schema.py`)
    2. Fixed scoring protocol — `query_pass_rate`, `coverage_pct`, `mean_latency_ms`, per-query PASS/FAIL
    3. Fixed compiler CLI contract (`answer`, `list-surfaces`, `list-edges`) via subprocess dispatch
    4. Fixed `results.tsv` schema

    Per PRD: every target's `harness.py` collapses to ~10-line wrapper calling `run_harness(compiler_path, queries_path, answers_module)` from `comp/framework/harness_base.py`. Validation of `queries.yaml` happens at load. Drift across targets is structurally impossible.

    Scope NOT in this TO: the orchestrator loop (PRD #4), per-target queries (PRD #2), compiler baseline (PRD #3). Framework only.
  </objective>

  <scope>
    <files>
      <file action="create">comp/framework/__init__.py</file>
      <file action="create">comp/framework/harness_base.py</file>
      <file action="create">comp/framework/query_schema.py</file>
      <file action="create">comp/framework/compiler_contract.py</file>
      <file action="create">comp/framework/results_schema.py</file>
      <file action="create">comp/framework/tests/test_harness_base.py (minimum-viable)</file>
    </files>
  </scope>

  <wire_contract>
    Exports from `comp.framework`:
    - `run_harness(compiler_path: Path, queries_path: Path, answers_module: ModuleType | None) -> HarnessResult`
    - `HarnessResult` dataclass: `query_pass_rate, coverage_pct, mean_latency_ms, per_query: list[QueryResult]`
    - `QueryResult` dataclass: `id, status (PASS|FAIL|ERROR), observed, expected, latency_ms`
    - `Query` schema (pydantic or dataclass): `id, question, answer_kind, answer, ground_truth_method, tags`
    - `CompilerContract` CLI spec: `answer <question>`, `list-surfaces`, `list-edges [--filter surface=...]`

    Downstream consumers: PRD #2 HTTPX_TARGET (ships first target's harness.py + queries.yaml + answers.py); PRD #3 COMPILER_BASELINE (ships compiler_v0.py template); PRD #4 LOOP_ORCHESTRATOR (consumes HarnessResult). Harness_base signature is the interlock — do not change post-ship without a new PRD.
  </wire_contract>

  <acceptance_criteria>
    1. `comp/framework/harness_base.py` runs a queries.yaml + subprocess-dispatched compiler and emits HarnessResult. Subprocess timeout 30s default (configurable via arg).
    2. `query_schema.py` validates a fixture yaml (good + 3 bad cases) — rejects on missing required fields, unknown answer_kind, duplicate ids.
    3. `compiler_contract.py` runs against a stub compiler (echo-back stub) and correctly parses all 3 CLI commands.
    4. `results_schema.py` exports the TSV column list + append-discipline helper (atomic append via `flock` to avoid multi-target concurrency races per MANDATE req #6).
    5. `tests/test_harness_base.py` runs under `pytest` with a bundled fixture and passes; at least 6 test cases covering: happy path, compiler crash, compiler timeout, schema violation, answer mismatch, empty queries.
    6. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO Rule 7 locked 2026-04-15).
    7. MCP COMPLETE to COO with commit hash + test output + sample HarnessResult dict.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>ls comp/ 2>&amp;1 || echo "empty"</run>
        <expect>`comp/` exists (walkthrough just created it) OR confirms no prior framework files to conflict with.</expect>
        <if_mismatch>If existing framework files present, STOP and surface to COO — walkthrough may have landed partial scaffolding.</if_mismatch>
      </step>
      <step>
        <run>cat /tmp/autoresearch_inspect/autoresearch-master/prepare.py | head -60</run>
        <expect>Confirms fixed-constants-pattern that harness_base.py inherits (TIME_BUDGET, MAX_SEQ_LEN style — our equivalent: subprocess_timeout, default scoring thresholds as module constants, NOT function args).</expect>
        <if_mismatch>Re-read autoresearch README for pattern clarification.</if_mismatch>
      </step>
      <step>
        <run>grep -rn "pydantic\|dataclass" comp/ 2>&amp;1 || echo "none"</run>
        <expect>Empty — no existing preferred dependency choice. Pick dataclass (stdlib, no new dep) unless pydantic already in an adjacent project's requirements.</expect>
        <if_mismatch>If pydantic already in use, use it for schema validation.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m pytest comp/framework/tests/test_harness_base.py -v</run>
        <expect>All 6+ tests pass. Exit 0.</expect>
        <if_mismatch>Fix until green. Do NOT skip tests.</if_mismatch>
      </step>
      <step>
        <run>python -m mypy comp/framework/ --strict (if mypy available) OR python -c "import comp.framework; print(comp.framework.__all__)"</run>
        <expect>No type errors; public API surface clean.</expect>
        <if_mismatch>Tighten types before commit.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>python -c "from comp.framework import run_harness, Query, HarnessResult, QueryResult; print('ok')"</run>
        <expect>"ok" — public API importable from `comp.framework` top-level.</expect>
        <if_mismatch>__init__.py re-exports missing; fix.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>None. Foundational; unblocks PRDs #2 + #4.</dependencies>

  <next>On commit: PRD #2 HTTPX_TARGET (CTO-authored, solo) can start. PRD #4 LOOP_ORCHESTRATOR can draft against stable framework signature.</next>
</task_order>
