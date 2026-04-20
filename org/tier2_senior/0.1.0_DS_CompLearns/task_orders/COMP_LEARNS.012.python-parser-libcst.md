<task_order>
  <metadata>
    <id>0.1.0_DS_CompLearns-2026-04-16-comp-learns-012-python-parser-libcst</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.1.0_DS_CompLearns</issued_to>
    <date>2026-04-16</date>
    <status>staged</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — enables .013 (imports subtype) + .021 (mutation engine)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_ARCHITECTURE.md @ c963ced5 (v2)</ref>
    <ref type="prd_section">§3 module layout (parsers/), §4.1-§4.4 IR schema, §5.1 ParsedFile consumption contract</ref>
    <ref type="blocker">§11.2 — LibCST dependency policy (Lambda Layer vs local venv) — AE 0.7.0_AE_CloudOps decides at Phase 1</ref>
  </references>

  <objective>
    Implement the Python parser for the structural inference system per §3. LibCST-backed. Produces the `ParsedFile` objects consumed by .013 (imports subtype) and .021 (mutation engine).

    Deliver:
    1. `comp/parsers/python.py` — full LibCST implementation of `Parser` protocol from .011.
    2. `ParsedFile` dataclass populated: file path, language tag, LibCST `Module` tree, content hash, optional source span lookups.
    3. Round-trip property: `parse(source).to_source() == source` on ≥10 sampled `httpx` modules.
    4. Parse error handling: bad Python → `ParseError` with file + line; does not crash the pipeline.

    Explicitly out of scope: Tree-sitter universal fallback (v0.2+ per §9), TS/Go/HCL parsers (v1.0 per §9), the `imports` subtype extraction (.013 — consumes this parser).
  </objective>

  <scope>
    <files>
      <file action="create">comp/parsers/python.py</file>
      <file action="create">comp/parsers/tests/test_python_parser.py</file>
      <file action="create">comp/parsers/tests/fixtures/ (sampled httpx module copies for round-trip)</file>
      <file action="modify">comp/parsers/__init__.py (export PythonParser)</file>
    </files>
  </scope>

  <wire_contract>
    ```python
    class PythonParser:
        name = "python_libcst"
        version = "v0"
        language = "python"

        def parse(self, path: Path) -> ParsedFile:
            """Deterministic. No network. No side effects.
            Returns ParsedFile with:
              - path: Path
              - language: str ("python")
              - cst: libcst.Module
              - content_hash: str (sha256 of source bytes)
              - source: str (raw source for round-trip)
            Raises ParseError(path, line, message) on invalid Python.
            """
    ```

    Downstream .013 uses `parsed_file.cst` and walks `ImportFrom` / `Import` nodes.
    Downstream .021 uses `parsed_file.cst` for scope-aware LibCST rewrites.
  </wire_contract>

  <acceptance_criteria>
    1. `PythonParser().parse(path)` produces a ParsedFile on every `.py` file in `comp/targets/httpx/httpx/*.py` without exception (except known-invalid fixture files in tests/).
    2. **Round-trip invariant:** on ≥10 sampled httpx modules, `parser.parse(path).source == parser.parse(path).cst.code` (LibCST preserves source exactly).
    3. `ParseError` raised with file path + line number on a hand-crafted invalid Python fixture (e.g., `def (: pass`).
    4. `parsed_file.content_hash` is stable across runs on the same input bytes.
    5. `pytest comp/parsers/ -v` exits 0.
    6. Session log `## Compiler Tools` reproduces every `<run>` below with observed output + pass/fail vs. `<expect>`.
    7. MCP COMPLETE to 2.0.0_SA_COO~Z with commit hash + pytest output + round-trip test count (should be ≥10).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>python -c "import libcst; print(libcst.__version__)"</run>
        <expect>Prints a version. Confirms LibCST is importable in the venv. If ImportError, surface to AE 0.7 — LibCST dependency policy (layer vs local venv per §11.2) must be resolved before writing code.</expect>
        <if_mismatch>STOP. MCP AE 0.7.0_AE_CloudOps: "COMP_LEARNS.012 blocked on LibCST dependency policy — layer or local venv? Preference: layer." Wait for decision.</if_mismatch>
      </step>
      <step>
        <run>ls comp/parsers/base.py comp/ir/schema.py</run>
        <expect>Both files exist (output of .011). Parser protocol + ParsedFile dataclass importable.</expect>
        <if_mismatch>STOP. .011 has not shipped. Ping COO~Z — .012 dep graph is wrong.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m pytest comp/parsers/ -v</run>
        <expect>All tests pass including the ≥10-httpx-module round-trip test. Exit 0.</expect>
        <if_mismatch>Fix until green. Do NOT commit with failing tests.</if_mismatch>
      </step>
      <step>
        <run>python -c "from comp.parsers.python import PythonParser; p = PythonParser(); import pathlib; f = p.parse(pathlib.Path('comp/targets/httpx/httpx/__init__.py')); print(f.language, f.content_hash[:8], len(f.source))"</run>
        <expect>Prints `python &lt;hash8&gt; &lt;nonzero&gt;`. Parser works end-to-end against a real httpx module.</expect>
        <if_mismatch>Debug parse path; ensure httpx target source is present.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-xref comp/parsers/python.py</run>
        <expect>Module visible in compiler-tools index. 0 consumers yet (.013/.021 consume after they land).</expect>
        <if_mismatch>Run `comp-build --rebuild` and re-check.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <risks>
    <risk id="R1">Benchmark dishonesty. (Medium/Critical) Mitigation: parser is deterministic; no gold interaction.</risk>
    <risk id="R3">Subtype explosion. (High/High) Mitigation: parser emits ParsedFile only; does NOT emit subtype records. Subtype validation is .013's responsibility.</risk>
    <risk id="R4">Scope creep. (High/High) Mitigation: **Python only. No Tree-sitter. No TS/Go/HCL.** If you catch yourself reaching for universal parsing, STOP.</risk>
    <risk id="R7">Legacy churn. (Low/Medium) Mitigation: new module, no legacy consumers to break.</risk>
    <risk id="R11">Mutation engine producing semantically-broken targets. (Medium/Medium) — Relevant: .021 depends on this parser for scope-aware rewrites. Ensure LibCST metadata resolvers (ScopeProvider, ParentNodeProvider) are available in the parser's output or accessible from the CST, so .021 can use them without re-parsing.</risk>
  </risks>

  <dependencies>
    <dependency to="COMP_LEARNS.011" status="required">Parser protocol + ParsedFile dataclass</dependency>
  </dependencies>

  <cross_domain_coordination>
    **.012 Phase 1 — LibCST dependency policy gate.** AE 0.7.0_AE_CloudOps must decide Lambda Layer vs local venv before implementation begins. Preference: Lambda Layer if LibCST is used by Lambda code; local venv otherwise. **COO~Z has pre-flagged this to AE 0.7 at .012 dispatch.** If AE 0.7 response is not in inbox when ~A reaches Phase 1, ~A pings AE 0.7 directly and holds until answered.
  </cross_domain_coordination>

  <next>On commit + MCP COMPLETE: .013 (~B imports subtype) and .021 (~D mutation engine) unblock.</next>
</task_order>
