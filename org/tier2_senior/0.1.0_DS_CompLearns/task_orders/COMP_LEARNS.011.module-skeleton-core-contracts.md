<task_order>
  <metadata>
    <id>0.1.0_DS_CompLearns-2026-04-16-comp-learns-011-module-skeleton-core-contracts</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.1.0_DS_CompLearns</issued_to>
    <date>2026-04-16</date>
    <status>staged</status><!-- REVERT 2026-04-20T17:59Z by COO~Z. Prior pending-flip at 17:55Z (commit 2f7d06d7) was out of lane scope — today's ~Z session is scoped to ~Z agents only per Andrew directive; dispatch across to base DS~A lane was incorrect. TO stays staged; dep-graph eyeballed clean by CTO~Z (PRD §3 module layout: zero-in-edge root, no cycles, blast radius matches) and v3 sweep authoring complete, so whenever the base lane picks this up it's dispatch-ready. -->
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — critical path; unblocks .012/.013/.014/.015/.016/.020/.021</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_ARCHITECTURE.md @ commit 8df31d86 (v3 — authoritative; v2 c963ced5 superseded)</ref>
    <ref type="prd_section">§3 module layout, §4.1-§4.5 IR schema + dimensional ontology + artifact_pattern NodeKind + determinism rule (no wall-clock fields), §4.3 graph-as-directory (manifest.json + entity JSONL streams), §5.1 SubtypeRecord (no extracted_at), §5.2 GraphBuilder contract, §5.3 conflict resolution policy, §6.1 ratchet_critical vs exploratory split, §6.2 Scorecard schema (RatchetCritical + Exploratory dataclasses), §6.5 selector axes, §6.6 mutation axis, §7.1 loop state</ref>
    <ref type="predecessor_prd">docs/architecture/COMP_LEARNS_HARNESS_FRAMEWORK.md (PRD #1 — .001 complete, 43e3225e+714d43a9)</ref>
    <ref type="precedent">comp/framework/extractor_interface.py (evolves into compiler_subtypes/base.py per §3)</ref>
  </references>

  <objective>
    Ship module skeleton + core contracts for the six-concern structural inference system per PRD v3 §3. This is the foundational TO for the .011-.021 wave; every downstream TO plugs into the contracts defined here.

    **v3 delta:** (1) `artifact_pattern` NodeKind added; (2) graph is a DIRECTORY (manifest.json + entity JSONL streams); (3) SubtypeRecord carries NO wall-clock fields (`extracted_at` removed); (4) `file` NodeKind drops `last_modified`; (5) Scorecard split into `RatchetCritical` + `Exploratory` dataclasses; (6) `Graph.__eq__` and `Scorecard.__eq__` manifest-agnostic / metadata-agnostic.

    Deliver, with empty-but-typed implementations where the full implementation lands in a downstream TO:
    1. `comp/ir/` — schema.py (Node/Edge/ConditionNode dataclasses with dimensional-attributes support per §4.5, **`artifact_pattern` NodeKind with `scheme` + `normalized_pattern` + `placeholder_names` + optional `concrete_example`**, **no `last_modified` on file**), node_ids.py (canonical ID generation incl. artifact_pattern scheme), kinds.py (NodeKind/EdgeKind/SUBTYPE_DIMENSIONS controlled vocabularies; EdgeKind `writes_to`/`reads_from` allow `artifact_pattern` targets), serializers.py (**graph-as-directory: manifest.json writer + entity JSONL streams + load/dump roundtrip on entities; manifest.json excluded from `Graph.__eq__`**).
    2. `comp/compiler_subtypes/base.py` — Subtype protocol + **SubtypeRecord dataclass per §5.1 (v3): NO `extracted_at` field, NO wall-clock anywhere on the record. provenance is deterministic (parser, rule_id, file_ref, span).** Attribute validator enforced: subtype_kind must be drawn from closed set; attributes keys must be drawn from ir/kinds.py::SUBTYPE_DIMENSIONS[subtype_kind]; flat-string subtype names like `imports_dynamic` MUST raise `InvalidSubtypeKindError`.
    3. `comp/graph_builder/base.py` — GraphBuilder Protocol + BuildResult + GraphDiff + ConflictedEdge sidecar dataclass per §5.2 + §5.3 (class definitions + stub implementations; full build/dedup/conflict logic ships in .014). **Graph.__eq__ compares entity streams only (nodes + edges + conditions); manifest excluded.**
    4. `comp/bench/scorecard.py` — **Scorecard split per §6.2 (v3): `RatchetCritical` + `Exploratory` sub-dataclasses. `primary_metric` is computed from `ratchet_critical` only. `emitted_at` is scorecard metadata and NOT used in `__eq__`.** `RatchetCritical` contains structural + efficiency + conflict_fraction + mutation_stability + downstream_ab. `Exploratory` contains behavioral + generalization + open_ended_judge + human_annotations. `DownstreamAB.per_selector` per §6.5 with 3 v0 selector keys. Round-trip serializer.
    5. `comp/loop/experiment_log.py` — append-only JSONL logger per §7.4.
    6. `comp/parsers/base.py` — Parser protocol + ParsedFile dataclass stub (full LibCST impl in .012).
    7. `framework/extractor_interface.py` alias-then-rename per R7 mitigation — preserve old contract shape with deprecation comment; ensure Track A ~A/B/C lanes do not break (comp-blast evidence in PRD §10 confirms 0 external consumers).

    Explicitly out of scope: full imports subtype extraction (.013), full Python parser (.012), full graph builder (.014), full bench comparator (.015), gold authoring (.016), selectors (.020), mutation engine (.021). This TO builds the SLOTS; the implementations drop into them.
  </objective>

  <scope>
    <files>
      <file action="create">comp/ir/__init__.py</file>
      <file action="create">comp/ir/schema.py</file>
      <file action="create">comp/ir/node_ids.py</file>
      <file action="create">comp/ir/kinds.py</file>
      <file action="create">comp/ir/serializers.py</file>
      <file action="create">comp/ir/tests/test_schema_roundtrip.py</file>
      <file action="create">comp/ir/tests/test_node_ids.py</file>
      <file action="create">comp/compiler_subtypes/__init__.py</file>
      <file action="create">comp/compiler_subtypes/base.py</file>
      <file action="create">comp/compiler_subtypes/records.py</file>
      <file action="create">comp/compiler_subtypes/tests/test_base_validator.py</file>
      <file action="create">comp/graph_builder/__init__.py</file>
      <file action="create">comp/graph_builder/base.py</file>
      <file action="create">comp/graph_builder/tests/test_contracts.py</file>
      <file action="create">comp/bench/__init__.py</file>
      <file action="create">comp/bench/scorecard.py</file>
      <file action="create">comp/bench/tests/test_scorecard_roundtrip.py</file>
      <file action="create">comp/loop/__init__.py</file>
      <file action="create">comp/loop/experiment_log.py</file>
      <file action="create">comp/loop/tests/test_experiment_log.py</file>
      <file action="create">comp/parsers/__init__.py</file>
      <file action="create">comp/parsers/base.py</file>
      <file action="modify">comp/framework/extractor_interface.py (deprecation comment + alias to compiler_subtypes.base)</file>
    </files>
  </scope>

  <wire_contract>
    **SUBTYPE_DIMENSIONS (ir/kinds.py) — v0 closed set per §4.5:**
    ```python
    SUBTYPE_DIMENSIONS: dict[str, dict[str, frozenset[str]]] = {
        "imports": {
            "resolution": frozenset({"static", "dynamic"}),
            "guard":      frozenset({"unconditional", "conditional"}),
            "binding":    frozenset({"resolved", "unresolved"}),
        },
        # io/iam dimensions are v0.1+ per §4.5 — do NOT add flat-string kinds here
    }
    ```

    **NodeKind `artifact_pattern` (v3 new) per §4.2:** required fields `scheme` (`"s3"|"file"|"gcs"|...`), `normalized_pattern` (e.g. `opal-data-bd/gold/canonical/{name}/{date}.parquet`), `placeholder_names` (list of placeholder strings). Optional: `concrete_example`. Canonical ID scheme: `artifact_pattern:{scheme}:{normalized_pattern}`. EdgeKind `writes_to` / `reads_from` now allow `artifact_pattern` as target (alongside `file` and `resource`).

    **Graph-as-directory wire format per §4.3 (v3):**
    ```
    {graph_dir}/
    ├── manifest.json          # schema_version, compiler_sha, extracted_at, target, file mapping, subtypes_enabled, mutation_lineage
    ├── nodes.jsonl            # one node per line, no headers — deterministic
    ├── edges.jsonl            # one edge per line, no headers — deterministic
    └── conditions.jsonl       # one condition per line, no headers — deterministic
    ```
    `manifest.json` is the ONLY place wall-clock time appears (`extracted_at`). Entity JSONL streams are byte-identical for identical `(source_files, compiler_sha, subtypes_enabled)` inputs. `Graph.__eq__` compares nodes+edges+conditions ONLY; manifest is run metadata.

    **SubtypeRecord (compiler_subtypes/records.py) per §5.1 v3 — frozen dataclass** with `subtype_kind`, `attributes: dict[str, str]`, `source: NodeRef`, `predicate: EdgeKind`, `target: str | NodeRef`, `confidence: Literal["certain","ambiguous","heuristic"]`, `provenance: Provenance` (deterministic: parser, rule_id, file_ref, span; NO wall-clock), `conditions: list[ConditionRef]`. **NO `extracted_at` field — v3 determinism rule (§5.1).** Run metadata (when extracted, by which compiler SHA) lives in `manifest.json`, not on records.

    **Attribute validator (compiler_subtypes/base.py)** — called at SubtypeRecord construction time:
    - If `subtype_kind not in SUBTYPE_DIMENSIONS` → raise `InvalidSubtypeKindError` (message must show the bad value; e.g. `imports_dynamic` is rejected with guidance to use `attributes={"resolution":"dynamic"}` instead).
    - If any `attributes.keys() - SUBTYPE_DIMENSIONS[subtype_kind].keys()` → raise `InvalidAttributeError`.
    - If any `attributes[k] not in SUBTYPE_DIMENSIONS[subtype_kind][k]` → raise `InvalidAttributeValueError`.

    **ConflictedEdge (graph_builder/base.py) per §5.3** — frozen dataclass with `subject`, `predicate`, `candidates: list[SubtypeRecord]`, `resolution: Literal["r1_confidence_win","r2_merged","r3_multi_target","elevation_required"]`, `winner_idx: int | None`, `elevated_at: str | None`.

    **BuildResult (graph_builder/base.py) per §5.2** — `graph: Graph`, `ambiguity_sidecar: list[AmbiguousEdge]`, `conflicts_sidecar: list[ConflictedEdge]`, `summary: GraphSummary` (per-kind + per-edge counts + heuristic/ambiguous/conflict fractions).

    **Scorecard (bench/scorecard.py) per §6.2 v3 — split into RatchetCritical + Exploratory:**
    ```python
    @dataclass
    class Scorecard:
        target: str                                     # "httpx"
        target_version: str                             # hash of frozen target source + gold (cache-invalidation key)
        compiler_sha: str
        subtypes_enabled: list[str]
        ratchet_critical: RatchetCritical               # contributes to primary_metric
        exploratory: Exploratory                        # reported but never contributes
        primary_metric: float                           # computed from ratchet_critical only
        emitted_at: str                                 # metadata; NOT in __eq__

    @dataclass
    class RatchetCritical:
        structural: Structural                          # precision/recall/F1 vs frozen gold
        efficiency: Efficiency                          # extraction_time (bucketed), graph_size_bytes, peak_memory_mb
        conflict_fraction: float                        # from §5.3
        mutation_stability: MutationStability           # from §6.6 — seeded, deterministic
        downstream_ab: DownstreamAB                     # frozen cached-answer regime mandatory (§6.4.1)

    @dataclass
    class Exploratory:
        behavioral: Behavioral                          # queries.yaml pass rate — informational only
        generalization: Generalization                  # held-out targets; v0 = unevaluated=True
        open_ended_judge: OpenEndedJudge | None         # future LLM-majority-of-three; v0 = None
        human_annotations: list[str]                    # rationales / notes

    @dataclass
    class DownstreamAB:
        per_selector: dict[str, SelectorAB]             # key in {"random","keyword","centrality"} at v0
        best_selector: str
        best_lift: float
    ```
    **Scorecard.__eq__:** compares `target_version + compiler_sha + ratchet_critical + primary_metric`. Excludes `emitted_at`, `exploratory.human_annotations`, efficiency timing jitter. Two scorecards for same `(target_version, compiler_sha)` MUST compare equal regardless of when they ran.

    **GraphDiff (graph_builder/base.py) per §5.2** — `added_nodes`, `removed_nodes`, `added_edges`, `removed_edges`, `kind_deltas: dict[str, int]`.

    Downstream consumers:
    - .012 consumes `parsers/base.py::Parser` + `ParsedFile`
    - .013 consumes `compiler_subtypes/base.py::Subtype` + `SubtypeRecord` + SUBTYPE_DIMENSIONS["imports"]
    - .014 consumes `graph_builder/base.py::GraphBuilder`, `ConflictedEdge`, `BuildResult`, `GraphDiff`
    - .015 consumes `bench/scorecard.py::Scorecard`, `DownstreamAB`, `Adversarial`
    - .020 populates `DownstreamAB.per_selector`
    - .021 populates `Adversarial.mutation_stability`
    - .017 wires all of the above end-to-end

    **Do not change these signatures post-ship without a PRD amendment.** They are the interlock for .012-.021.
  </wire_contract>

  <acceptance_criteria>
    1. Every file listed in `<scope>` exists; `python -c "from comp.ir import Node, Edge, ConditionNode; from comp.ir.kinds import SUBTYPE_DIMENSIONS; from comp.compiler_subtypes import Subtype, SubtypeRecord; from comp.graph_builder import GraphBuilder, BuildResult, GraphDiff, ConflictedEdge; from comp.bench import Scorecard, DownstreamAB, Adversarial; from comp.loop import experiment_log; from comp.parsers import Parser, ParsedFile; print('ok')"` prints `ok`.
    2. **Attribute validator tests (compiler_subtypes/tests/test_base_validator.py):**
       - `SubtypeRecord(subtype_kind="imports_dynamic", ...)` raises `InvalidSubtypeKindError`.
       - `SubtypeRecord(subtype_kind="imports", attributes={"unknown_dim": "x"}, ...)` raises `InvalidAttributeError`.
       - `SubtypeRecord(subtype_kind="imports", attributes={"resolution": "bogus"}, ...)` raises `InvalidAttributeValueError`.
       - `SubtypeRecord(subtype_kind="imports", attributes={"resolution":"static","guard":"unconditional","binding":"resolved"}, ...)` constructs cleanly.
       - **v3 determinism test: SubtypeRecord has no wall-clock fields.** `assert "extracted_at" not in {f.name for f in dataclasses.fields(SubtypeRecord)}`; all `provenance` keys deterministic (parser, rule_id, file_ref, span only).
    3. **IR entity-stream round-trip test (ir/tests/test_schema_roundtrip.py):** `load(dump(graph)) == graph` on a synthetic 3-node/3-edge/1-condition fixture — **compares entity streams only; manifest excluded from `__eq__`**. A second `dump()` on the same source produces byte-identical `nodes.jsonl`+`edges.jsonl`+`conditions.jsonl` (manifest `extracted_at` differs, which is expected).
    4. **artifact_pattern NodeKind test (ir/tests/test_schema_roundtrip.py):** constructing an `artifact_pattern` node with `scheme="s3"`, `normalized_pattern="opal-data-bd/gold/canonical/{name}/{date}.parquet"`, `placeholder_names=["name","date"]` round-trips through JSONL. Canonical ID is `artifact_pattern:s3:opal-data-bd/gold/canonical/{name}/{date}.parquet`.
    5. **Node ID canonicalization (ir/tests/test_node_ids.py):** duplicate (kind, canonical_path) with different provenance raises; all §4.4 examples produce the documented canonical form (including `artifact_pattern`).
    6. **Scorecard round-trip (bench/tests/test_scorecard_roundtrip.py):** `load(dump(scorecard)) == scorecard` with `ratchet_critical` + `exploratory` populated; `per_selector` populated for all 3 v0 selector keys (stub SelectorAB values). **Scorecard.__eq__ test:** two scorecards with identical `(target_version, compiler_sha, ratchet_critical, primary_metric)` but different `emitted_at` compare equal.
    7. **Graph directory test (ir/tests/test_schema_roundtrip.py):** `dump(graph, tmp_dir)` creates `manifest.json + nodes.jsonl + edges.jsonl + conditions.jsonl`; `load(tmp_dir) == graph`. Manifest.json has schema_version + compiler_sha + extracted_at + target + subtypes_enabled fields.
    8. **Experiment log test (loop/tests/test_experiment_log.py):** append-only semantics verified — writing entry N does not mutate entries 1..N-1; load returns list ordered by iter.
    9. **GraphBuilder contract test (graph_builder/tests/test_contracts.py):** `GraphBuilder` protocol satisfiable by a no-op stub; `ConflictedEdge` dataclass round-trips; `GraphDiff(empty, empty) == GraphDiff(empty_lists)`. **Graph.__eq__ manifest-agnostic:** two Graph objects with same entities but different manifests compare equal.
    10. **All existing framework tests still pass:** `python -m pytest comp/framework/ comp/ir/ comp/compiler_subtypes/ comp/graph_builder/ comp/bench/ comp/loop/ comp/parsers/ -v` exits 0.
    11. **R7 (legacy churn):** `python -c "from comp.framework.extractor_interface import *; print('ok')"` still prints `ok` (alias, not hard break). `comp-blast comp/framework/extractor_interface` shows 0 new breakage vs baseline.
    12. **R13 (wall-clock contamination) mechanical enforcement:** `python -c "import dataclasses; from comp.compiler_subtypes.records import SubtypeRecord; from comp.ir.schema import Node; assert 'extracted_at' not in {f.name for f in dataclasses.fields(SubtypeRecord)}; assert 'last_modified' not in {f.name for f in dataclasses.fields(Node)}; print('no-wallclock-on-records')"` prints `no-wallclock-on-records`.
    13. Session log includes a `## Compiler Tools` section reproducing every `<run>` from `<compiler_tools_mandate>` below with observed output and explicit pass/fail vs. `<expect>`. **Missing rows = REWORK.**
    14. MCP COMPLETE to 2.0.0_SA_COO~Z with commit hash + test output summary + `python -c "...public-API import..."` one-liner output.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-xref comp/framework/compiler_contract.py</run>
        <expect>1 consumer (comp/framework/run.py). No external consumers outside comp/framework/.</expect>
        <if_mismatch>STOP. If new consumers appeared, surface to COO — the alias-then-rename approach may need to expand scope to update them.</if_mismatch>
      </step>
      <step>
        <run>comp-blast comp/framework/extractor_interface</run>
        <expect>0 external consumers today (per PRD §10 evidence). Safe to evolve into compiler_subtypes/base.py.</expect>
        <if_mismatch>STOP. If external consumers appear, do NOT rename — keep alias permanent until consumers are migrated as a separate TO.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m pytest comp/ -v</run>
        <expect>All existing framework tests pass + new contract tests pass. Exit 0.</expect>
        <if_mismatch>Fix until green. Do NOT skip tests. Do NOT commit with failing tests.</if_mismatch>
      </step>
      <step>
        <run>python -c "from comp.ir import Node, Edge, ConditionNode; from comp.ir.kinds import SUBTYPE_DIMENSIONS, NodeKind; from comp.compiler_subtypes import Subtype, SubtypeRecord; from comp.graph_builder import GraphBuilder, BuildResult, GraphDiff, ConflictedEdge; from comp.bench import Scorecard, RatchetCritical, Exploratory, DownstreamAB, MutationStability; from comp.loop import experiment_log; from comp.parsers import Parser, ParsedFile; print('ok')"</run>
        <expect>Prints "ok". All public contracts importable from package-root. Scorecard exposes RatchetCritical + Exploratory (v3 split).</expect>
        <if_mismatch>__init__.py re-exports missing; fix before commit.</if_mismatch>
      </step>
      <step>
        <run>python -c "import dataclasses; from comp.compiler_subtypes.records import SubtypeRecord; from comp.ir.schema import Node; sr_fields={f.name for f in dataclasses.fields(SubtypeRecord)}; assert 'extracted_at' not in sr_fields, f'v3 violation: SubtypeRecord has extracted_at: {sr_fields}'; print('no-extracted_at ok')"</run>
        <expect>Prints `no-extracted_at ok`. v3 R13 mitigation: SubtypeRecord has no wall-clock fields.</expect>
        <if_mismatch>Remove `extracted_at` from SubtypeRecord. v3 §5.1 determinism rule.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-xref comp/ir/schema.py</run>
        <expect>New module visible in compiler-tools index (may be empty until .012-.015 land).</expect>
        <if_mismatch>If comp-xref can't find the new module, run `comp-build --rebuild` first, then re-check.</if_mismatch>
      </step>
      <step>
        <run>comp-blast comp/framework/extractor_interface</run>
        <expect>0 new breakage vs Phase 1 baseline — alias preserved.</expect>
        <if_mismatch>Surface to COO. R7 mitigation failed — the alias is not honoring the legacy contract shape.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <risks>
    <risk id="R1">Benchmark dishonesty — gold authored to match compiler output. (Medium/Critical) Mitigation: this TO does NOT touch gold; attribute validator + mutation engine (downstream) are structural defenses.</risk>
    <risk id="R3">Subtype explosion — flat-string taxonomy fragments combinatorially. (High/High) Mitigation: **Closed by §4.5 dimensional ontology. This TO mechanically enforces it — attribute validator in subtype base raises on `imports_dynamic`-style flat-string variants.**</risk>
    <risk id="R4">Scope creep — this briefing can become a 6-month project. (High/High) Mitigation: **This TO builds SLOTS only. No full parser, no full subtype, no full builder. If you catch yourself implementing downstream logic, STOP and surface to COO.**</risk>
    <risk id="R7">Legacy framework churn breaks Track A. (Low/Medium) Mitigation: alias-then-rename on extractor_interface.py with deprecation comment; Phase 1 + Phase 3 comp-blast confirm 0 consumer breakage.</risk>
    <risk id="R13">**Wall-clock contamination — time-valued fields on deterministic records poison dedup/hash/diff and corrupt champion selection across re-runs. (High without mechanical enforcement / Critical)** Mitigation: **this TO is the mechanical enforcement point.** SubtypeRecord has NO `extracted_at` field; `Node` file kind has NO `last_modified` field. Acceptance Criterion 12 validates via dataclass introspection. Timestamps live only in `manifest.json` / `experiment_log.jsonl` / `scorecard.emitted_at` — none in `__eq__`.</risk>
    <risk id="R14">**Judge drift across re-runs. (Medium/Critical)** Relevant: Scorecard split (ratchet_critical vs exploratory) is shipped here. `Scorecard.__eq__` discipline excludes metadata so the split is mechanically correct. Full judge-caching logic ships in .015.</risk>
  </risks>

  <dependencies>None. Foundational for .012/.013/.014/.015/.016/.020/.021.</dependencies>

  <cross_domain_coordination><none/></cross_domain_coordination>

  <next>On commit + MCP COMPLETE: COO~Z dispatches .012 (~A Python parser) + .020 (CTO selector harness) + .016 (CTO httpx gold) in parallel. .013/.014/.015/.021 unblock as their additional parents land.</next>
</task_order>
