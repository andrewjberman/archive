<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform~D-2026-04-16-comp-learns-021-mutation-engine</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-16</date>
    <status>staged</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — NEW TO per v2 amendment; gates .015 + .017. Fallback owner ~B if ~D capacity-blocked on CN-P1b.</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_ARCHITECTURE.md @ 8df31d86 (v3 — peer review invariant-breakage fixes)</ref>
    <ref type="prd_section">§6.2 Scorecard schema v3 (`ratchet_critical.mutation_stability` path), §6.6 mutation engine v0 core (promoted from v0.3-deferred), §7.5 active adversarial sub-loop, §9 bootstrap-vs-target table (mutation now v0 core), §11.1 R13 (wall-clock contamination — determinism required), §12.2 TO .021 three-phase mandate</ref>
    <ref type="amendment">§17 v2 amendment gap #4 (gold is not the sole honesty mechanism) — this TO closes it</ref>
  </references>

  <objective>
    Implement mutation engine v0 per §6.6. **Promoted from v0.3-deferred to v0 core.** Gold alone does not scale past 3-5 targets; mutation-based validation is the property-testing analog and scales to many targets.

    **Premise:** if a compiler claims `A imports B` in pristine httpx, and we rename `B` to `B2` throughout the source, the compiler should claim `A imports B2` in mutated source. The EDGE is invariant to the rename; only the NODE ID changes.

    Deliver:
    1. `comp/bench/mutations/base.py` — `MutationEngine` Protocol + `MutatedTarget` dataclass.
    2. `comp/bench/mutations/rename.py` — LibCST-backed identifier rename (module names, function names, class names). Scope-aware rebinding; preserves parse-cleanness + import-resolvability.
    3. `comp/bench/mutations/reorder.py` — statement-order shuffle within each module; only within semantically-independent groups (preserves semantics).
    4. `comp/bench/mutations/noise.py` — inserts syntactically-valid but semantically-dead code (unused imports, dead functions, literal-only expressions).
    5. `comp/bench/mutations/harness.py` — `run_mutation_suite(compiler, target_root, seeds=[1,2,3]) -> MutationStabilityReport`.
    6. Integration with `.015`'s v3 scorecard — populates `scorecard.ratchet_critical.mutation_stability` per §6.2 (v3 path, not v2 flat `.adversarial`). The v3 promotion put `mutation_stability` inside `ratchet_critical` — it contributes directly to primary_metric.
    7. **Pytest suite on `comp/framework/` as self-target** — mutation engine validates itself against a known target; stability ≥ 0.85 passes.
    8. **Byte-identical determinism (NEW v3 per R13):** for a given `seed`, `M.mutate(target_root, seed=42)` called twice MUST produce byte-identical `mutated_root` trees + identical `id_mapping` dicts + identical `mutation_log`. Mutation outputs participate in ratchet scoring; non-determinism poisons `scorecard.__eq__` and corrupts champion selection across re-runs.

    Explicitly out of scope: structural-equivalence mutations (v1.0), semantic-preserve mutations beyond rename/reorder/noise (v1.0), LLM-generated mutations (v0.4+), adversarial generator active-sub-loop (.017 Phase 3 consumes this engine but owns the sub-loop wiring).
  </objective>

  <scope>
    <files>
      <file action="create">comp/bench/mutations/__init__.py</file>
      <file action="create">comp/bench/mutations/base.py</file>
      <file action="create">comp/bench/mutations/rename.py</file>
      <file action="create">comp/bench/mutations/reorder.py</file>
      <file action="create">comp/bench/mutations/noise.py</file>
      <file action="create">comp/bench/mutations/harness.py</file>
      <file action="create">comp/bench/mutations/tests/test_protocol_roundtrip.py</file>
      <file action="create">comp/bench/mutations/tests/test_rename_preserves_parse.py</file>
      <file action="create">comp/bench/mutations/tests/test_rename_preserves_imports.py</file>
      <file action="create">comp/bench/mutations/tests/test_reorder_semantic_preserve.py</file>
      <file action="create">comp/bench/mutations/tests/test_noise_does_not_add_real_edges.py</file>
      <file action="create">comp/bench/mutations/tests/test_harness_self_target.py (mutation engine against comp/framework/)</file>
      <file action="create">comp/bench/mutations/tests/test_stability_threshold_gate.py</file>
      <file action="create">comp/bench/mutations/tests/test_mutation_byte_identical_determinism.py</file>
    </files>
  </scope>

  <wire_contract>
    ```python
    class MutationEngine(Protocol):
        name: str                                    # "rename" | "reorder" | "noise"
        version: str                                 # "v0"

        def mutate(self, target_root: Path, seed: int) -> MutatedTarget: ...

    @dataclass(frozen=True)
    class MutatedTarget:
        mutated_root: Path
        id_mapping: dict[str, str]                   # orig NodeRef.id → mutated NodeRef.id (for rename; identity for reorder/noise)
        mutation_count: int
        mutation_log: list[dict]                     # per-mutation detail (kind, location, before, after)

    @dataclass
    class MutationStabilityReport:
        per_mutation_seed: dict[tuple[str, int], float]   # {("rename", 1): 0.92, ...}
        aggregate: float                                  # mean across all 9 runs (3 mutations × 3 seeds)
        threshold_passed: bool                            # aggregate ≥ 0.85
    ```

    **Bench integration recipe (§6.6 + v3 §6.2 paths):**
    1. Extract graph from pristine target → `graph_pristine`.
    2. For each M in `{rename, reorder, noise}` × seed in `{1, 2, 3}`:
       a. `mutated = M.mutate(target_root, seed)`
       b. `graph_mutated = extract(compiler, mutated.mutated_root)`
       c. Translate `graph_mutated` node IDs back via `mutated.id_mapping` → `graph_translated`
       d. `diff = GraphBuilder.diff(graph_pristine, graph_translated)`
       e. `score[M.name][seed] = 1 - (|diff.added_edges| + |diff.removed_edges|) / max(1, len(graph_pristine.edges))`
    3. `scorecard.ratchet_critical.mutation_stability = MutationStability(score=mean(score), per_mutation_seed=..., per_failure={})` — v3 path per §6.2.

    **Determinism (NEW v3 per R13):** for every engine `M`, `M.mutate(target_root, seed=42)` called twice MUST produce identical `MutatedTarget` outputs. Specifically:
    - `mutated_root` tree: `find mutated_root -type f | xargs sha256sum` identical across runs.
    - `id_mapping`: dict equality (same keys, same values).
    - `mutation_log`: list equality (same order, same entries).
    **Disallowed inside `mutate`:** `time.time()`, `uuid.uuid4()`, `random.random()` (without seed parameter), filesystem-ordering dependencies, any network call. Only `random.Random(seed)` or `hashlib`-derived randomness is acceptable.

    **v0 pass threshold:** `mutation_stability ≥ 0.85` on `imports` subtype against httpx. Lower scores are acceptable in experiment_log (loop may still improve a low-stability compiler), but `< 0.70` triggers a scorecard warning flag.

    **Active-adversarial interface (§7.5):** `.017` will call `adversarial.generate(failure)` which wraps `MutationEngine.mutate()` with failure-targeting. This TO does NOT build the active sub-loop — it builds the engine that the sub-loop wraps.
  </wire_contract>

  <acceptance_criteria>
    1. **Protocol roundtrip (test_protocol_roundtrip.py):** all 3 engines implement `MutationEngine` Protocol.
    2. **Rename preserves parse (test_rename_preserves_parse.py):** for 10 sample httpx modules + `comp/framework/` modules, `python -c "import ast; ast.parse(open(path).read())"` passes on the mutated source. No syntax errors.
    3. **Rename preserves imports (test_rename_preserves_imports.py):** for `comp/framework/` self-target, all `from X import Y` statements in mutated source resolve to valid modules in the mutated tree. LibCST scope-aware rebinding.
    4. **Reorder semantic preserve (test_reorder_semantic_preserve.py):** for seeded reorders, `ast.parse(mutated).body` still contains the same set of top-level statements (no dropped statements). Semantically-dependent sequences (e.g., `x = 1; print(x)` must remain in order) are preserved.
    5. **Noise does not add real edges (test_noise_does_not_add_real_edges.py):** run compiler against noisy-mutated target. Extracted edges should equal edges from pristine target (no new real `imports` edges introduced by noise, since noise is dead code).
    6. **Byte-identical determinism (test_mutation_byte_identical_determinism.py) — NEW v3, R13 direct defense:** for each of `rename`, `reorder`, `noise`, call `M.mutate(target_root, seed=42)` twice into two separate temp dirs. Assert:
       - `sha256sum(run1/**) == sha256sum(run2/**)` — mutated file trees byte-identical.
       - `mutated_1.id_mapping == mutated_2.id_mapping`.
       - `mutated_1.mutation_log == mutated_2.mutation_log`.
       - `mutated_1.mutation_count == mutated_2.mutation_count`.
       Additionally, assert `M.mutate(target_root, seed=1) != M.mutate(target_root, seed=2)` at the tree-hash level (different seeds must actually produce different outputs — no silent seed-ignoring).
    7. **Self-target stability (test_harness_self_target.py):** `run_mutation_suite(ImportsSubtype_compiler, target_root="comp/framework/", seeds=[1,2,3])` produces `MutationStabilityReport` with `aggregate ≥ 0.85`. **This is the v0 pass threshold for the mutation engine itself.**
    8. **Stability threshold gate (test_stability_threshold_gate.py):** `report.threshold_passed == True` when aggregate ≥ 0.85; `False` when < 0.85.
    9. **Integration with .015 bench:** `scorecard.ratchet_critical.mutation_stability` populated correctly (v3 path, not flat `.adversarial`) after `run_mutation_suite` returns. Value contributes to primary_metric.
    10. `pytest comp/bench/mutations/ -v` exits 0.
    11. Session log `## Compiler Tools` reproduces every `<run>` from `<compiler_tools_mandate>` with observed output + pass/fail vs. `<expect>`. Missing rows = REWORK.
    12. MCP COMPLETE to 2.0.0_SA_COO~Z with commit hash + pytest output + self-target MutationStabilityReport numbers + byte-identical determinism test output.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>python -c "import libcst; from comp.parsers.python import PythonParser; from comp.graph_builder import GraphBuilder, GraphDiff; from comp.bench import Scorecard, RatchetCritical, MutationStability; print('deps ok')"</run>
        <expect>Prints `deps ok`. .011 exposes v3 `RatchetCritical` + `MutationStability` dataclasses (not flat v2 `.Adversarial`); .012 parser shipped.</expect>
        <if_mismatch>STOP. Parent TO missing OR still on v2 schema. Ping COO~Z — do NOT implement against flat `.adversarial` path.</if_mismatch>
      </step>
      <step>
        <run>ls comp/framework/*.py | head -5</run>
        <expect>Multiple .py files present — the self-target for mutation engine testing.</expect>
        <if_mismatch>`comp/framework/` empty or missing — .001 regression. Ping COO~Z.</if_mismatch>
      </step>
      <step>
        <run>python -c "import libcst.metadata; print(libcst.metadata.ScopeProvider.__name__)"</run>
        <expect>Prints `ScopeProvider`. LibCST metadata resolvers available — required for scope-aware rename rewrites.</expect>
        <if_mismatch>LibCST version too old — needs ≥ 0.4.x. Surface to AE 0.7.</if_mismatch>
      </step>
      <step>
        <run>grep -rnE "time\.time\(\)|uuid\.uuid4\(\)|random\.(random|randint|choice|shuffle)\(" comp/bench/mutations/ 2>/dev/null || echo "no-raw-nondet-sources"</run>
        <expect>Prints `no-raw-nondet-sources` OR only lines wrapped by a `random.Random(seed)` instance. **R13 discipline:** no wall-clock / uuid / unseeded-random calls in mutation code paths.</expect>
        <if_mismatch>STOP. Non-determinism source in mutation engine = scorecard __eq__ will fail across re-runs = R13 poisoning ratchet_critical. Fix before Phase 2.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>pytest comp/bench/mutations/tests/test_mutation_byte_identical_determinism.py -v</run>
        <expect>All 3 engines (rename, reorder, noise) produce byte-identical output across two calls with `seed=42`. Different seeds produce different outputs. Exits 0.</expect>
        <if_mismatch>STOP. Determinism failure is R13 critical — mutation output poisons scorecard.__eq__ and corrupts champion selection across re-runs. Diagnose with `diff -r run1/ run2/`; find the wall-clock / unseeded-random source.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/bench/mutations/tests/test_rename_preserves_parse.py -v</run>
        <expect>All rename mutations produce parseable Python on 10+ sample modules.</expect>
        <if_mismatch>R11 failure — rename breaks parse-cleanness. Fix LibCST rewrite scope handling.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/bench/mutations/tests/test_rename_preserves_imports.py -v</run>
        <expect>Rename on `comp/framework/` produces resolvable imports. LibCST scope-aware rebinding works.</expect>
        <if_mismatch>Fix scope resolution.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/bench/mutations/tests/test_harness_self_target.py -v</run>
        <expect>Self-target stability aggregate ≥ 0.85 on `comp/framework/`. Threshold passed.</expect>
        <if_mismatch>Either stabilize the mutation engine (preferred) OR surface to COO~Z with numbers if the self-target simply has too few imports for stability to be reliable (pivot to `comp/targets/httpx/httpx/` as self-target).</if_mismatch>
      </step>
      <step>
        <run>pytest comp/bench/mutations/ -v</run>
        <expect>All tests pass. Exit 0.</expect>
        <if_mismatch>Fix until green.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-xref comp/bench/mutations/</run>
        <expect>Module visible; .015 scorecard integration + .017 active-adversarial sub-loop consume after they land.</expect>
        <if_mismatch>`comp-build --rebuild` and re-check.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <risks>
    <risk id="R1">Benchmark dishonesty — gold authored to match compiler output. (Medium/Critical) Mitigation: **Mutation engine IS the second line of defense against biased gold. Gold can be biased; mutation invariance cannot be biased by author system-knowledge. §6.6 promotes mutation to v0 core for exactly this reason.**</risk>
    <risk id="R2">A/B metric gaming. (Medium/High) Mitigation: mutation invariance is not gameable without actually understanding the target — primary_metric α-weighted by mutation_stability per §6.6.</risk>
    <risk id="R3">Subtype explosion. (High/High) Mitigation: mutation engine operates on source code; does not touch subtype_kind vocabulary.</risk>
    <risk id="R4">Scope creep. (High/High) Mitigation: **Three mutation kinds ONLY — rename / reorder / noise. No structural-equivalence, no semantic-preserve mutations beyond these, no LLM-generated mutations. Active-adversarial sub-loop wiring is .017's responsibility, not this TO's.**</risk>
    <risk id="R7">Legacy churn. (Low/Medium) Mitigation: new module; does not modify `comp/framework/` (only READS it for self-target testing, writes to temp dir).</risk>
    <risk id="R11">**Mutation engine produces semantically-broken targets. (Medium/Medium)** Mitigation: **Mutations MUST preserve parse-cleanness + import-resolvability. LibCST scope-aware rebinding for rename. `reorder` only within semantically-independent groups. `noise` additions are dead code by construction. Phase 2 tests (test_rename_preserves_parse.py + test_rename_preserves_imports.py) enforce this.**</risk>
    <risk id="R12">Passive loop too slow. (Low after amendment/High) Mitigation: this TO provides the engine; .017 wraps it in the active sub-loop.</risk>
    <risk id="R13">**Wall-clock contamination — non-deterministic mutation output poisons scorecard __eq__ + corrupts champion selection across re-runs. (High without mechanical enforcement / Critical)** Mitigation: (a) Phase 1 grep scan rejects raw `time.time()` / `uuid.uuid4()` / unseeded `random` calls in mutation code. (b) Phase 2 `test_mutation_byte_identical_determinism.py` asserts two calls with `seed=42` produce byte-identical output for every engine. (c) Disallowed primitives documented in wire_contract. This is the direct defense — mutation output participates in ratchet scoring via `ratchet_critical.mutation_stability`; any non-determinism here leaks directly into primary_metric drift.</risk>
  </risks>

  <dependencies>
    <dependency to="COMP_LEARNS.011" status="required">GraphDiff + v3 Scorecard + RatchetCritical + MutationStability dataclasses (not flat v2 `.Adversarial`)</dependency>
    <dependency to="COMP_LEARNS.012" status="required">PythonParser (for LibCST scope-aware rewrites)</dependency>
  </dependencies>

  <cross_domain_coordination>
    **v3 sweep marker (2026-04-20 COO~Z):** swept from v2→v3 per CTO checklist 2026-04-16 13:59Z (preserved in ~B handoff log). Deltas applied: scorecard path updated to `ratchet_critical.mutation_stability` per §6.2 (v3 promoted mutation into the ratchet-critical section, not flat `.adversarial`); byte-identical determinism test (`test_mutation_byte_identical_determinism`) as direct R13 defense (mutation output participates in ratchet scoring; non-determinism leaks into primary_metric drift); Phase 1 grep scan rejects wall-clock / uuid / unseeded-random sources; disallowed primitives listed in wire_contract; R13 risk added.

    **Capacity flag:** if ~D is saturated by CN-P1b on ADVI_ROLLUP (primary COO's lane), reassign this TO to ~B per §16 item 6 fallback. COO~Z re-asserts fallback authority — **bench is critical path, do not stall.** If CN-P1b runs long, ~B picks this up after .013 closes.
  </cross_domain_coordination>

  <next>On commit + MCP COMPLETE to 2.0.0_SA_COO~Z: .015 `scorecard.ratchet_critical.mutation_stability` integration has real numbers. .017 active-adversarial sub-loop has a mutation engine to wrap + determinism to rely on.</next>
</task_order>
