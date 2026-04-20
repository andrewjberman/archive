<task_order>
  <metadata>
    <id>0.2.0_DS_CompLearns-2026-04-16-comp-learns-013-imports-subtype</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.2.0_DS_CompLearns</issued_to>
    <date>2026-04-16</date>
    <status>staged</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — inaugural subtype; unblocks .014 (graph builder uses imports records) + .017 (ratchet integration)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_ARCHITECTURE.md @ 8df31d86 (v3 — authoritative; v2 c963ced5 superseded)</ref>
    <ref type="prd_section">§4.5 dimensional subtype ontology, §5.1 SubtypeRecord + determinism rule (no wall-clock) + confidence ladder, §8 v0 inaugural subtype rationale, §11.1 R13 (wall-clock contamination), §12.2 TO .013 mandate (v3 delta)</ref>
  </references>

  <objective>
    Implement the `imports` subtype v0 per §4.5. LibCST-backed. Emits `SubtypeRecord` objects with **dimensional attributes `{resolution, guard, binding}` per §4.5.** Flat-string subtype names like `imports_dynamic` MUST fail validation (enforced by .011's attribute validator).

    Deliver:
    1. `comp/compiler_subtypes/imports.py` — full implementation. Input: `list[ParsedFile]`. Output: `list[SubtypeRecord]` with `subtype_kind="imports"` and all three dimensions populated on every record.
    2. Dimensional-attribute coverage — every record must populate all three dimensions (`resolution`, `guard`, `binding`).
    3. Confidence ladder per §5.1:
       - `certain` — unambiguous AST (plain `import httpx`, `from httpx import _transports`).
       - `ambiguous` — star imports (`from .utils import *`) where the target set has multiple public names.
       - `heuristic` — regex/string-match fallback (not expected in v0 imports; if used, MUST be flagged honestly).
    4. Synthetic fixtures (3-file + dynamic + conditional) that exercise every dimension value.

    Explicitly out of scope: graph builder (.014 consumes these records), gold authoring (.016), scoring (.015). This TO ships the extractor only.
  </objective>

  <scope>
    <files>
      <file action="create">comp/compiler_subtypes/imports.py</file>
      <file action="create">comp/compiler_subtypes/tests/test_imports_synthetic.py</file>
      <file action="create">comp/compiler_subtypes/tests/fixtures/synthetic_3_file/ (minimal 3-file target exercising static/dynamic/conditional/resolved/unresolved)</file>
      <file action="modify">comp/compiler_subtypes/__init__.py (export ImportsSubtype)</file>
    </files>
  </scope>

  <wire_contract>
    ```python
    class ImportsSubtype:
        name = "imports"
        version = "v0"
        kind = "imports"

        def extract(
            self,
            parsed_files: list[ParsedFile],
            *,
            previous_records: list[SubtypeRecord] | None = None,
        ) -> list[SubtypeRecord]:
            """Deterministic, pure function. No side effects.
            Emits SubtypeRecord per import statement, with dimensional attributes:
              - resolution: "static" | "dynamic"
              - guard:      "unconditional" | "conditional"
              - binding:    "resolved" | "unresolved"
            Attributes dict must ONLY contain keys from SUBTYPE_DIMENSIONS["imports"].
            """
    ```

    **Dimension encoding rules (v0):**
    - `resolution=static` — `import X`, `from X import Y`, `from .X import Y` (literal module path).
    - `resolution=dynamic` — `importlib.import_module(...)`, `__import__(...)` calls (AST call patterns).
    - `guard=unconditional` — import at module top level.
    - `guard=conditional` — import inside `if`, `try`, `def`, `class`, or `with` block.
    - `binding=resolved` — target is a specific module/name; e.g., `import httpx`, `from httpx import _transports`.
    - `binding=unresolved` — star import (`from X import *`), dynamic import where target string is not a literal, `from . import X` without lexical resolution.

    Every `SubtypeRecord` includes `provenance: Provenance(parser="python_libcst", rule_id="imports.v0", file_ref=..., span=...)`.

    Downstream .014 consumes these records. Downstream .017 ratchet measures their structural F1 vs .016 gold.
  </wire_contract>

  <acceptance_criteria>
    1. **Attribute validator tests (must pass):**
       - Emitting `subtype_kind="imports_dynamic"` from the extractor MUST raise `InvalidSubtypeKindError` (caught from .011's validator). This is the §4.5 mechanical enforcement.
       - Emitting `attributes={"unknown_dim": "x"}` MUST raise `InvalidAttributeError`.
    2. **v3 determinism tests (R13 mechanical enforcement):**
       - **Byte-identical output on identical input:** call `ImportsSubtype().extract(parsed_files)` twice on the same inputs. `json.dumps([r.__dict__ for r in out1], sort_keys=True) == json.dumps([r.__dict__ for r in out2], sort_keys=True)` (post-dataclass-to-dict normalization). No drift across calls.
       - **SubtypeRecord carries no time fields:** `assert "extracted_at" not in {f.name for f in dataclasses.fields(SubtypeRecord)}`; `assert all("time" not in k.lower() and "_at" not in k for k in record.provenance.keys())`.
    3. **Synthetic fixture test:** `test_synthetic_3_file` fixture covers all `{resolution, guard, binding}` × value combinations. Extractor emits a record for each import with all three dimensions populated.
    4. **Attribute coverage on real httpx:** run against `comp/targets/httpx/httpx/*.py`; produce `/tmp/imports_records.jsonl`; verify `jq -r '.attributes | keys[]' /tmp/imports_records.jsonl | sort -u` equals exactly `binding\nguard\nresolution` (every record has all three dimensions). **No `.extracted_at` in records — per-record jq `.extracted_at // "absent"` returns `absent` for every record.**
    5. **Precision/recall gate vs .016 gold:** on `comp/targets/httpx/`, extractor output compared to `comp/targets/httpx/gold/imports_gold.jsonl` (landed by .016) achieves precision ≥ 0.95, recall ≥ 0.90 on `confidence=certain` records. **If .016 has not shipped when .013 reaches Phase 2, hold — COO~Z coordinates dispatch so .016 lands first or in parallel.**
    6. `pytest comp/compiler_subtypes/ -v` exits 0.
    7. Session log `## Compiler Tools` reproduces every `<run>` below with observed output + pass/fail vs. `<expect>`.
    8. MCP COMPLETE to 2.0.0_SA_COO~Z with commit hash + precision/recall numbers + synthetic-fixture dimension coverage matrix + determinism-test output.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>python -m pytest comp/compiler_subtypes/tests/test_base_validator.py -v</run>
        <expect>All validator tests from .011 pass. Attribute validator is live.</expect>
        <if_mismatch>STOP. .011 has not shipped or is broken. Ping COO~Z.</if_mismatch>
      </step>
      <step>
        <run>python -c "from comp.compiler_subtypes import Subtype, SubtypeRecord; from comp.parsers.python import PythonParser; from comp.ir.kinds import SUBTYPE_DIMENSIONS; print(SUBTYPE_DIMENSIONS['imports'])"</run>
        <expect>Prints the imports dimensions dict — `{'resolution': frozenset(...), 'guard': frozenset(...), 'binding': frozenset(...)}`. Confirms .011 + .012 both shipped and the dimensional vocabulary is as expected.</expect>
        <if_mismatch>STOP. If dimensions are missing or have different keys, surface to CTO — §4.5 spec drift.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/compiler_subtypes/tests/test_imports_synthetic.py::test_synthetic_3_file</run>
        <expect>Synthetic 3-file fixture test exists and passes. Covers static/dynamic, conditional/unconditional, resolved/unresolved.</expect>
        <if_mismatch>Extend fixtures to cover every dimension value before Phase 2.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/compiler_subtypes/tests/test_imports_synthetic.py::test_rejects_flat_string_kind</run>
        <expect>Test asserts that a manufactured SubtypeRecord with `subtype_kind="imports_dynamic"` raises `InvalidSubtypeKindError`. Test passes.</expect>
        <if_mismatch>Add the test. The §4.5 mechanical-enforcement invariant depends on it.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m comp.compiler_subtypes.imports comp/targets/httpx/httpx/ > /tmp/imports_records_1.jsonl &amp;&amp; python -m comp.compiler_subtypes.imports comp/targets/httpx/httpx/ > /tmp/imports_records_2.jsonl &amp;&amp; diff /tmp/imports_records_1.jsonl /tmp/imports_records_2.jsonl &amp;&amp; echo "byte-identical"</run>
        <expect>Prints `byte-identical`. Two extractions on the same source produce byte-identical output. v3 R13 determinism enforcement.</expect>
        <if_mismatch>Extractor non-deterministic. Remove wall-clock/RNG/dict-ordering dependencies. Check that provenance dicts are serialized with `sort_keys=True` and SubtypeRecord has no time fields.</if_mismatch>
      </step>
      <step>
        <run>jq -r '.attributes | keys[]' /tmp/imports_records_1.jsonl | sort -u</run>
        <expect>Output is exactly three lines: `binding`, `guard`, `resolution`. Every record has all three dimensions populated.</expect>
        <if_mismatch>Extractor is under-populating attributes. Fix: every code path that emits SubtypeRecord must populate all three dimensions. This is the §4.5 invariant.</if_mismatch>
      </step>
      <step>
        <run>jq -r '.extracted_at // "absent"' /tmp/imports_records_1.jsonl | sort -u</run>
        <expect>Output is exactly one line: `absent`. No record has an `extracted_at` field (v3 R13).</expect>
        <if_mismatch>Remove `extracted_at` from SubtypeRecord construction. Update .011 dataclass if it still has the field.</if_mismatch>
      </step>
      <step>
        <run>python -m comp.bench.structural --records /tmp/imports_records.jsonl --gold comp/targets/httpx/gold/imports_gold.jsonl --confidence certain</run>
        <expect>Precision ≥ 0.95, recall ≥ 0.90 on certain-confidence records.</expect>
        <if_mismatch>If .016 gold has not landed, defer this step to post-.016 and document in session log. Otherwise, raise precision/recall before commit.</if_mismatch>
      </step>
      <step>
        <run>python -m pytest comp/compiler_subtypes/ -v</run>
        <expect>All tests pass including validator tests + synthetic fixture + real-httpx smoke. Exit 0.</expect>
        <if_mismatch>Fix until green.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-xref comp/compiler_subtypes/imports.py</run>
        <expect>Module visible; when .014 lands, graph_builder consumers will appear.</expect>
        <if_mismatch>`comp-build --rebuild` and re-check.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <risks>
    <risk id="R1">Benchmark dishonesty — extractor authored to match gold. (Medium/Critical) Mitigation: **.016 gold is authored BEFORE this extractor's Phase 2 scoring step (gold-before-code invariant, §8). If ~B reads gold before writing the extractor, that is a QA failure — session log must attest gold was not consulted during extraction logic writing.**</risk>
    <risk id="R3">Subtype explosion. (High/High) Mitigation: **This TO ships exactly ONE subtype kind (`imports`). Variation expressed via dimensional attributes, not flat-string variants. Attribute validator from .011 mechanically enforces. No `imports_dynamic`, no `imports_conditional` — these are attributes, not kinds.**</risk>
    <risk id="R4">Scope creep. (High/High) Mitigation: **`imports` subtype ONLY. No `io`, no `calls`, no `iam`.** If you catch yourself adding a second subtype, STOP.</risk>
    <risk id="R7">Legacy churn. (Low/Medium) Mitigation: new module; legacy extractor_interface is aliased, not broken.</risk>
    <risk id="R13">**Wall-clock contamination — time-valued fields on SubtypeRecord poison dedup/hash/diff. (High without mechanical enforcement / Critical)** Mitigation: **SubtypeRecord has NO `extracted_at` field (per .011 dataclass). provenance dict has no `time`/`_at` keys. Phase 2 determinism test: two extractions on the same source produce byte-identical JSONL.** Per PRD v3 §5.1 + §11.1 R13.</risk>
  </risks>

  <dependencies>
    <dependency to="COMP_LEARNS.011" status="required">Subtype protocol + SubtypeRecord + attribute validator + SUBTYPE_DIMENSIONS["imports"]</dependency>
    <dependency to="COMP_LEARNS.012" status="required">PythonParser + ParsedFile</dependency>
    <dependency to="COMP_LEARNS.016" status="preferred-parallel">httpx gold — needed for Phase 2 precision/recall gate. If .016 not yet landed, Phase 2 precision/recall step deferred until .016 lands; synthetic fixtures still unblocked.</dependency>
  </dependencies>

  <cross_domain_coordination><none/></cross_domain_coordination>

  <next>On commit + MCP COMPLETE: .014 (~C graph builder) unblocks. .017 (~C ratchet integration) waits for .014/.015/.016/.020/.021 to all land.</next>
</task_order>
