<task_order>
  <metadata>
    <id>1.3.0_DS_CompLearns-2026-04-16-comp-learns-014-graph-builder</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>1.3.0_DS_CompLearns</issued_to>
    <date>2026-04-16</date>
    <status>complete</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — integration gate for subtype records; unblocks .017</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_ARCHITECTURE.md @ 8df31d86 (v3 — authoritative; v2 c963ced5 superseded)</ref>
    <ref type="prd_section">§5.2 GraphBuilder contract + BuildResult, §5.3 conflict resolution policy (R1-R5), §4.1-§4.4 IR schema (graph-as-directory; Graph.__eq__ manifest-agnostic)</ref>
  </references>

  <objective>
    Implement Graph Builder v0 per §5.2 + §5.3. Consumes `list[SubtypeRecord]`; produces `BuildResult(graph, ambiguity_sidecar, conflicts_sidecar, summary)`.

    Deliver:
    1. `comp/graph_builder/build.py` — main `build()` entry.
    2. `comp/graph_builder/canonicalize.py` — NodeRef resolution via `ir/node_ids.py`.
    3. `comp/graph_builder/dedup.py` — (subject, predicate, object, sorted-conditions, sorted-attributes) equivalence → single edge; provenance unions.
    4. `comp/graph_builder/conditions.py` — materialize ConditionNode objects from repeated ConditionRefs; dedupe by (kind, key, operator, value).
    5. `comp/graph_builder/ambiguity.py` — unresolved-candidate records → `ambiguity_sidecar`.
    6. **`comp/graph_builder/conflicts.py` — conflict resolution policy per §5.3 (ALL FIVE RULES R1-R5) + `ConflictedEdge` sidecar emission + bench-surfacing of `conflict_fraction`.**
    7. `comp/graph_builder/diff.py` — `GraphDiff` function per §5.2.
    8. `comp/graph_builder/summary.py` — GraphSummary with per-kind counts + heuristic/ambiguous/conflict fractions.

    Explicitly out of scope: graph querying (lives in bench + targets/*/compiler.py), graph persistence beyond ir/serializers.py, LLM-driven edge inference.
  </objective>

  <scope>
    <files>
      <file action="create">comp/graph_builder/build.py</file>
      <file action="create">comp/graph_builder/canonicalize.py</file>
      <file action="create">comp/graph_builder/dedup.py</file>
      <file action="create">comp/graph_builder/conditions.py</file>
      <file action="create">comp/graph_builder/ambiguity.py</file>
      <file action="create">comp/graph_builder/conflicts.py</file>
      <file action="create">comp/graph_builder/diff.py</file>
      <file action="create">comp/graph_builder/summary.py</file>
      <file action="create">comp/graph_builder/tests/test_build_dedup.py</file>
      <file action="create">comp/graph_builder/tests/test_diff.py</file>
      <file action="create">comp/graph_builder/tests/test_conflict_policy.py</file>
      <file action="create">comp/graph_builder/tests/test_conflict_sidecar_schema.py</file>
      <file action="create">comp/graph_builder/tests/test_summary_fractions.py</file>
      <file action="create">comp/graph_builder/tests/test_end_to_end_httpx.py</file>
      <file action="create">comp/graph_builder/tests/fixtures/ (synthetic multi-subtype fixtures for R1-R5)</file>
    </files>
  </scope>

  <wire_contract>
    ```python
    def build(
        records: Iterable[SubtypeRecord],
        *,
        target_root: Path,
        language_hints: dict[str, str] | None = None,
    ) -> BuildResult:
        # 1. Canonicalize source + target refs.
        # 2. Materialize condition nodes (dedupe).
        # 3. Dedupe records by (subject, predicate, object, sorted-conditions, sorted-attributes).
        # 4. Promote ambiguous records that resolve; rest → ambiguity_sidecar.
        # 5. Detect + resolve conflicts per §5.3 (R1-R5).
        # 6. Emit GraphSummary (per-kind, per-edge-kind, heuristic/ambiguous/conflict fractions).
        # Returns BuildResult(graph, ambiguity_sidecar, conflicts_sidecar, summary).
    ```

    **Conflict resolution rules (§5.3 — deterministic, top-to-bottom):**
    - **R1** Confidence mismatch — `certain` wins over `heuristic`; loser → conflicts_sidecar with `resolution="r1_confidence_win"`.
    - **R2** Both `certain`, both AST-backed, different attribute values on same (source, predicate, target) — merge: union attribute dimensions; if same dimension has contradictory values → fall through to R5.
    - **R3** Both `certain`, different targets for same (source, predicate) — keep both IFF predicate allows multi-target (e.g., `imports` to multiple modules); else R5.
    - **R4** Same confidence, provenance overlap (same file + span) — raise `ConflictingProvenanceError` (build fails; extractor bug).
    - **R5** Contradictory and unresolvable — both routed to conflicts_sidecar with `resolution="elevation_required"`, `winner_idx=None`, `elevated_at=<ISO8601>`; bench penalty applies.

    **Multi-target predicates** (R3 allowance): `imports`, `writes_to`, `reads_from`, `depends_on` allow multiple targets. `grants_permission_to` allows multiple permissions. Other predicates are single-target by default.

    **conflict_fraction = len(conflicts_sidecar) / max(1, len(graph.edges))**. Surfaced via GraphSummary for bench consumption (§6.6 primary_metric penalty).
  </wire_contract>

  <acceptance_criteria>
    1. **Property test — dedup invariant:** `build(records).summary.edges_count == len(canonical_dedup(records))` for synthetic inputs.
    2. **Conflict policy R1-R5 unit tests (test_conflict_policy.py):** each rule has a dedicated fixture producing its trigger; each returns the expected resolution string + winner_idx + conflicts_sidecar entry.
    3. **ConflictedEdge sidecar schema (test_conflict_sidecar_schema.py):** feeding two contradictory `certain` records on same (source, predicate, target) but different attribute values for the same dimension yields one `conflicts_sidecar` entry with `resolution="elevation_required"` (R5 — contradictory attribute dimension) and the bench penalty is applied.
    4. **GraphDiff invariants (test_diff.py):** `diff(g, g)` returns empty GraphDiff; `diff(g, g + 1 edge)` returns GraphDiff with `added_edges` of length 1, `removed_edges` empty, and the correct `kind_deltas` entry. **v3 manifest-agnostic:** `diff(g1, g2)` where g1 and g2 have identical entity streams but different manifests (different `extracted_at` / `compiler_sha`) returns empty GraphDiff — the diff operates on entities only.
    5. **End-to-end httpx (test_end_to_end_httpx.py):** `build(ImportsSubtype().extract(PythonParser().parse_tree(httpx_root)))` produces a non-empty graph. Summary counts match gold counts (from .016) ± 5%. **conflict_fraction == 0 (single-subtype invariant per §5.3).**
    6. **Summary fractions (test_summary_fractions.py):** `heuristic_fraction`, `ambiguous_fraction`, `conflict_fraction` are floats in [0, 1] and algebraically correct against hand-computed synthetic inputs.
    7. `pytest comp/graph_builder/ -v` exits 0.
    8. Session log `## Compiler Tools` reproduces every `<run>` below with observed output + pass/fail vs. `<expect>`.
    9. MCP COMPLETE to 2.0.0_SA_COO~Z with commit hash + httpx graph summary output + conflict_fraction numbers.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>python -c "from comp.graph_builder import GraphBuilder, BuildResult, GraphDiff, ConflictedEdge; from comp.compiler_subtypes.imports import ImportsSubtype; from comp.parsers.python import PythonParser; print('deps ok')"</run>
        <expect>Prints `deps ok`. .011 + .012 + .013 all shipped and importable.</expect>
        <if_mismatch>STOP. Ping COO~Z — a parent TO has not shipped.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/graph_builder/tests/test_conflict_policy.py -v</run>
        <expect>All five rule fixtures exist with documented trigger conditions. Running them should initially fail (no impl); after Phase 2, all pass.</expect>
        <if_mismatch>Author R1-R5 fixtures BEFORE any build() logic. TDD discipline — fixtures first, code second.</if_mismatch>
      </step>
      <step>
        <run>python -c "from comp.compiler_subtypes.records import SubtypeRecord; r = SubtypeRecord(subtype_kind='imports', attributes={'resolution':'static','guard':'unconditional','binding':'resolved'}, source='file:a.py', predicate='imports', target='module:b', confidence='certain', provenance={'parser':'python_libcst','rule_id':'imports.v0','file_ref':'file:a.py','span':(1,1,1,10)}, conditions=[], extracted_at='2026-04-16T00:00:00Z'); print(r.subtype_kind)"</run>
        <expect>Prints `imports`. Dependency check — SubtypeRecord constructs with dimensional attributes cleanly.</expect>
        <if_mismatch>STOP. .011 attribute validator broken or SUBTYPE_DIMENSIONS missing.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>pytest comp/graph_builder/tests/test_conflict_policy.py -v</run>
        <expect>All R1-R5 fixture tests pass. Exit 0.</expect>
        <if_mismatch>Fix conflict resolution logic until all five rules return the documented resolution string. Do NOT commit with any R-rule failing.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/graph_builder/tests/test_diff.py -v</run>
        <expect>`diff(g, g)` returns empty; `diff(g, g + edge)` returns GraphDiff with added_edges of length 1.</expect>
        <if_mismatch>Fix diff logic.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/graph_builder/tests/test_end_to_end_httpx.py -v</run>
        <expect>Builds graph from imports subtype records on httpx. summary.edges_count > 0. conflict_fraction == 0.0.</expect>
        <if_mismatch>If .016 gold has not landed, the ±5% check vs gold is skipped and noted in session log; end-to-end build with conflict_fraction==0 must still pass.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/graph_builder/ -v</run>
        <expect>All tests pass. Exit 0.</expect>
        <if_mismatch>Fix until green.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-xref comp/graph_builder/build.py</run>
        <expect>Module visible; .015 bench + .017 ratchet will consume after they land.</expect>
        <if_mismatch>`comp-build --rebuild` and re-check.</if_mismatch>
      </step>
      <step>
        <run>python -m comp.graph_builder.build --records /tmp/imports_records.jsonl --target-root comp/targets/httpx/ --summary-only</run>
        <expect>Prints GraphSummary: node counts per kind, edge counts per kind, heuristic/ambiguous/conflict fractions. conflict_fraction should be 0.0 on the single-subtype httpx run.</expect>
        <if_mismatch>If conflict_fraction > 0 on single-subtype input, there is a subtle dedup/conflict bug — investigate.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <risks>
    <risk id="R1">Benchmark dishonesty. (Medium/Critical) Mitigation: graph builder operates on records; does not touch gold. Gold-before-code invariant applies to .016 + .013, not .014.</risk>
    <risk id="R3">Subtype explosion. (High/High) Mitigation: builder treats subtype_kind as opaque string; the SUBTYPE_DIMENSIONS controlled vocabulary (from .011) governs what's valid. Builder does NOT add new subtype kinds.</risk>
    <risk id="R4">Scope creep. (High/High) Mitigation: **No graph DB, no LLM edge inference, no query engine.** If you catch yourself building a query interface, STOP — that's bench + compiler.py territory.</risk>
    <risk id="R7">Legacy churn. (Low/Medium) Mitigation: new module. No legacy consumers.</risk>
    <risk id="R10">Silent conflict accumulation. (Medium/High) Mitigation: **§5.3 resolution priority is deterministic and EXHAUSTIVELY tested at Phase 2. R5 elevation_required conflicts are routed to sidecar with winner_idx=None and surfaced via conflict_fraction — never silently merged. Bench penalty per conflict is applied in .015 scoring.**</risk>
  </risks>

  <dependencies>
    <dependency to="COMP_LEARNS.011" status="required">GraphBuilder protocol + BuildResult + ConflictedEdge + GraphDiff dataclasses</dependency>
    <dependency to="COMP_LEARNS.013" status="required">ImportsSubtype — produces the SubtypeRecords this builder consumes for end-to-end test</dependency>
  </dependencies>

  <cross_domain_coordination><none/></cross_domain_coordination>

  <next>On commit + MCP COMPLETE: .017 (~C ratchet) is closer to unblocking. .017 still waits on .015 + .016 + .020 + .021.</next>
</task_order>
