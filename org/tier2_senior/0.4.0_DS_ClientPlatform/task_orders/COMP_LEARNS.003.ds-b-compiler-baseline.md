<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform~B-2026-04-15-comp-learns-003-compiler-baseline</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- Shipped 2026-04-15 20:30Z. Files: comp/framework/compiler_baseline.py (139 lines), extractor_interface.py, tests/test_compiler_baseline.py (9/9 PASS, 7.05s). Acceptance #3 dispatcher smoke PASS (4/4 SUBCOMMANDS via cc.invoke). Acceptance #4 run_harness honest-zero PASS (queries_run=10, pass_rate=0.0, coverage=0.0, mean_latency_ms>0). Acceptance flex pre-flagged to CTO 20:15Z — baseline CLI matches ~A's shipped compiler_contract (no --repo, no confidence, 4 subcommands incl. rebuild, list-* return arrays) because harness_base IS the interlock consumer. 0.4.0_DS_ClientPlatform~B. -->
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — prevents agent over/under-engineering first iteration</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_COMPILER_BASELINE.md (PRD #3 of 5)</ref>
    <ref type="framework_contract">comp/framework/compiler_contract.py (once PRD #1 ships — CLI spec)</ref>
    <ref type="precedent">autoresearch-master/train.py (single-file agent-editable scaffold — our `compiler_baseline.py` plays this role for code-compilers)</ref>
  </references>

  <objective>
    Ship `comp/framework/compiler_baseline.py` + `comp/framework/extractor_interface.py`. The baseline is a
    single-file Python module (120-180 lines) implementing the CLI contract (`answer`, `list-surfaces`, `list-edges`)
    with honest "I don't know" stubs. Per-target `compiler.py` copies the baseline — NOT imported. Agent edits freely
    in Phase 2.

    Extractor interface is a small protocol: `surfaces()`, `edges(filter)`, `answer(question)`. Optional for v0 but
    stabilizes the interface for Phase 3+ extractor-swap experimentation.

    Purpose: minimum-viable first commit for every target — agent's first iteration is "make one query pass," not "architect from scratch."
  </objective>

  <scope>
    <files>
      <file action="create">comp/framework/compiler_baseline.py</file>
      <file action="create">comp/framework/extractor_interface.py</file>
      <file action="create">comp/framework/tests/test_compiler_baseline.py</file>
    </files>
  </scope>

  <wire_contract>
    `compiler_baseline.py` exposes CLI matching PRD #1 `CompilerContract`:
    - `python compiler_baseline.py answer "question" --repo <_repo_path>` → JSON `{"answer": null, "confidence": 0.0, "latency_ms": N}` (honest empty)
    - `python compiler_baseline.py list-surfaces --repo <_repo_path>` → JSON `{"surfaces": []}` (empty stub)
    - `python compiler_baseline.py list-edges --repo <_repo_path> [--filter surface=X]` → JSON `{"edges": []}`

    `extractor_interface.py` exposes:
    ```python
    from typing import Protocol, Any
    class Extractor(Protocol):
        def surfaces(self) -> list[str]: ...
        def edges(self, filter: dict | None = None) -> list[dict]: ...
        def answer(self, question: str) -> Any | None: ...
    ```

    Contract promise: any target's `compiler.py` that starts from `compiler_baseline.py` passes PRD #1's `compiler_contract.py` dispatch smoke-test out of the box (all queries score FAIL honestly; coverage 0%; latency non-zero).
  </wire_contract>

  <acceptance_criteria>
    1. `compiler_baseline.py` under 180 lines; all 3 CLI subcommands present; JSON output schema-stable.
    2. `extractor_interface.py` defines `Extractor` Protocol.
    3. Smoke test via `comp.framework.compiler_contract` dispatcher: all 3 commands parse + return JSON without crash.
    4. Harness test: running PRD #1 `run_harness(compiler_baseline.py, queries.yaml stub, None)` produces `query_pass_rate=0, coverage_pct=0, mean_latency_ms>0` on ≥10 stub queries (no crashes).
    5. `tests/test_compiler_baseline.py` ≥5 cases; pytest green.
    6. Copy-template doc inline: module-level docstring tells the agent "copy this file to `comp/targets/{target}/compiler.py` and edit freely."
    7. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO Rule 7).
    8. MCP COMPLETE to COO with commit hash + line count + smoke-test JSON output.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>cat /tmp/autoresearch_inspect/autoresearch-master/train.py | head -100</run>
        <expect>Confirms single-file scaffold pattern — all imports + config at top, followed by model + loop. Our baseline mimics single-file + top-level config.</expect>
        <if_mismatch>Re-read autoresearch train.py structure before authoring.</if_mismatch>
      </step>
      <step>
        <run>ls comp/framework/ 2>&amp;1 | grep -E "compiler_contract|harness_base"</run>
        <expect>Both files exist (PRD #1 shipped). Baseline depends on their signatures.</expect>
        <if_mismatch>If not present, STOP — this TO gates on ~A's PRD #1 completion.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>wc -l comp/framework/compiler_baseline.py</run>
        <expect>Between 120 and 180 lines (PRD target).</expect>
        <if_mismatch>If over 180, tighten; if under 120, likely missing honest stubs.</if_mismatch>
      </step>
      <step>
        <run>python comp/framework/compiler_baseline.py answer "test?" --repo /tmp/fake_repo 2>&amp;1 | python -c "import sys, json; print(json.loads(sys.stdin.read()))"</run>
        <expect>JSON parses; keys include `answer, confidence, latency_ms`.</expect>
        <if_mismatch>Output schema broken; fix.</if_mismatch>
      </step>
      <step>
        <run>python -m pytest comp/framework/tests/test_compiler_baseline.py -v</run>
        <expect>All tests pass.</expect>
        <if_mismatch>Fix until green.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>grep -n "copy this file" comp/framework/compiler_baseline.py</run>
        <expect>Docstring explicitly tells future agent how to use this as a template.</expect>
        <if_mismatch>Add the copy-template line; agents need the breadcrumb.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~A" task="COMP_LEARNS.001" status="staged" description="framework CLI contract needed for baseline to implement against"/>
  </dependencies>

  <next>On commit: PRD #2 HTTPX_TARGET (CTO) copies baseline as its starting `compiler.py` template. Phase 2 iteration can fire once engine is built.</next>
</task_order>
