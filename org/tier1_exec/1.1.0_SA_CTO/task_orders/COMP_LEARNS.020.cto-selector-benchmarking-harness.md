<task_order>
  <metadata>
    <id>1.1.0_SA_CTO-2026-04-16-comp-learns-020-selector-benchmarking-harness</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>1.1.0_SA_CTO</issued_to><!-- Transferred 2026-04-21 from 1.0.0_SA_CTO per COMP_LEARNS_TARGET_CLOSEOUT.md §7.2 (dyad ownership split). No scope change — v4.2 PRD §6.5 already fully specifies this TO. -->
    <date>2026-04-16</date>
    <status>staged</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — NEW TO per v2 amendment; gates .015 + .017</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_ARCHITECTURE.md @ c963ced5 (v2)</ref>
    <ref type="prd_section">§6.5 selector benchmarking first-class component, §6.4 A/B protocol + cache key includes selector_hash, §9 bootstrap-vs-target table (selectors row), §12.2 TO .020 three-phase mandate</ref>
    <ref type="amendment">§17 v2 amendment gap #3 (selector attack surface) — this TO closes it</ref>
  </references>

  <objective>
    Implement selector benchmarking harness + 3 v0 selectors per §6.5. **First-class component, not implementation detail.** The graph→LLM-context subset is the real attack surface; without selector discipline we optimize for the selector rather than the graph.

    Deliver:
    1. `comp/bench/selectors/base.py` — `Selector` Protocol + `SelectedContext` dataclass.
    2. `comp/bench/selectors/random.py` — uniform random sample up to token_budget. Deterministic under fixed seed. The floor — any real selector should beat this.
    3. `comp/bench/selectors/keyword.py` — question-keyword → node-name Jaccard; top-k under token_budget. Weak baseline; reveals keyword-leakage attacks.
    4. `comp/bench/selectors/centrality.py` — PageRank-style graph centrality + question-kind-aware filtering (e.g., for "which modules import X?" return modules with `imports` edges into X's neighborhood). Strong baseline; shows structure-aware lift.
    5. `comp/bench/selectors/harness.py` — `run_selectors(question, graph, selectors, budget) -> dict[str, SelectedContext]` — deterministic wiring for bench.ab.run.
    6. Integration with `.015`'s `bench/ab.py` — `scorecard.downstream_ab.per_selector` populated for all 3 selectors.
    7. **SelectorGameDetected fork wired** — when `best_selector == "random"` and `best_lift > 0.1`, `bench.ab.run` raises `SelectorGameDetected`.

    Explicitly out of scope: randomized-seed variants per selector (v0.2 per §6.5), LLM-as-selector (v0.4+), selectors beyond the three specified.
  </objective>

  <scope>
    <files>
      <file action="create">comp/bench/selectors/__init__.py</file>
      <file action="create">comp/bench/selectors/base.py</file>
      <file action="create">comp/bench/selectors/random.py</file>
      <file action="create">comp/bench/selectors/keyword.py</file>
      <file action="create">comp/bench/selectors/centrality.py</file>
      <file action="create">comp/bench/selectors/harness.py</file>
      <file action="create">comp/bench/selectors/tests/test_protocol_roundtrip.py</file>
      <file action="create">comp/bench/selectors/tests/test_random_uniform.py</file>
      <file action="create">comp/bench/selectors/tests/test_keyword_jaccard.py</file>
      <file action="create">comp/bench/selectors/tests/test_centrality_convergence.py</file>
      <file action="create">comp/bench/selectors/tests/test_token_budget_honored.py</file>
      <file action="create">comp/bench/selectors/tests/test_selector_game_fork.py</file>
    </files>
  </scope>

  <wire_contract>
    ```python
    class Selector(Protocol):
        name: str                                    # "random" | "keyword" | "centrality"
        version: str                                 # "v0"

        def select(
            self,
            question: str,
            graph: Graph,
            *,
            token_budget: int,
            seed: int | None = None,
        ) -> SelectedContext: ...

    @dataclass(frozen=True)
    class SelectedContext:
        nodes: list[NodeRef]
        edges: list[EdgeRef]
        conditions: list[NodeRef]
        token_count: int
        rationale: str                               # one-line explanation for auditability
        selector_name: str                           # echoed for cache key
        selector_version: str                        # echoed for cache key
    ```

    **Selector-hash for cache key (§6.4):** `sha256(f"{name}|{version}|{sorted_node_ids}|{sorted_edge_ids}")`. Changes with selector identity OR with its specific selection for a given question/graph.

    **Harness integration:**
    ```python
    def run_selectors(
        question: str,
        graph: Graph,
        selectors: list[Selector],
        *,
        token_budget: int,
    ) -> dict[str, SelectedContext]:
        return {s.name: s.select(question, graph, token_budget=token_budget) for s in selectors}
    ```

    **SelectorGameDetected fork (§6.5):** wired into `bench/ab.py`:
    ```python
    if scorecard.downstream_ab.best_selector == "random" and scorecard.downstream_ab.best_lift > 0.1:
        raise SelectorGameDetected(scorecard=scorecard, message="Random selector wins >0.1 lift — bench is broken; fork to CTO")
    ```
  </wire_contract>

  <acceptance_criteria>
    1. **Protocol roundtrip (test_protocol_roundtrip.py):** all 3 selectors implement `Selector` Protocol; `select()` returns `SelectedContext` with `selector_name` + `selector_version` populated.
    2. **Determinism:** given fixed `seed`, each selector returns the same `SelectedContext` across runs on the same graph + question.
    3. **Random uniform (test_random_uniform.py):** over 1000 runs with different seeds, `random.select()` samples approximately uniformly from graph nodes (per-node selection frequency within expected binomial CI).
    4. **Keyword Jaccard (test_keyword_jaccard.py):** given question `"foo bar"` and nodes `{"foo_module", "bar_module", "zzz_module"}`, top-k returns `foo_module` and `bar_module` before `zzz_module`.
    5. **Centrality convergence (test_centrality_convergence.py):** PageRank computation converges on a small synthetic graph (N=10) within 50 iterations; centrality scores are normalized to [0, 1] and sum to ≈1.
    6. **Token budget honored (test_token_budget_honored.py):** for each selector, output `SelectedContext.token_count ≤ token_budget`. Measured via a deterministic token counter (tiktoken or heuristic).
    7. **SelectorGameDetected fork (test_selector_game_fork.py):** fabricated scorecard where random wins >0.1 raises; fabricated scorecard where centrality wins >0.1 does NOT raise.
    8. **Integration with .015 bench/ab.py:** `bench.ab.run(scorecard, selectors=[random, keyword, centrality])` populates `scorecard.downstream_ab.per_selector` with all 3 keys and computes `best_selector` + `best_lift`.
    9. `pytest comp/bench/selectors/ -v` exits 0.
    10. Session log `## Compiler Tools` reproduces every `<run>` below with observed output + pass/fail vs. `<expect>`.
    11. MCP COMPLETE to 2.0.0_SA_COO~B with commit hash + pytest output + sample SelectedContext from each selector on the httpx graph.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>python -c "from comp.bench import Scorecard, DownstreamAB; print('deps ok')"</run>
        <expect>Prints `deps ok`. .011 contracts available.</expect>
        <if_mismatch>STOP. .011 has not shipped. Ping COO~B.</if_mismatch>
      </step>
      <step>
        <run>grep -c "class SelectorGameDetected" comp/bench/ab.py 2>/dev/null || echo 0</run>
        <expect>1 if .015 has shipped, 0 if not yet. If 0, this TO adds the exception class alongside the selector implementations and arranges the import path so .015 consumes it.</expect>
        <if_mismatch>No mismatch — both states handled.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>pytest comp/bench/selectors/tests/test_protocol_roundtrip.py -v</run>
        <expect>All 3 selectors satisfy the Protocol; `SelectedContext` round-trips.</expect>
        <if_mismatch>Fix Protocol conformance.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/bench/selectors/tests/test_selector_game_fork.py -v</run>
        <expect>Fork fires on fabricated random-wins fixture; does NOT fire on structured-selector-wins fixture.</expect>
        <if_mismatch>Fix the conditional.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/bench/selectors/ -v</run>
        <expect>All tests pass. Exit 0.</expect>
        <if_mismatch>Fix until green.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-xref comp/bench/selectors/</run>
        <expect>Module visible; .015 + .017 consume after they land.</expect>
        <if_mismatch>`comp-build --rebuild` and re-check.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <risks>
    <risk id="R1">Benchmark dishonesty. (Medium/Critical) Mitigation: selectors are deterministic; selector_hash in A/B cache key prevents stale-cache reuse across selector changes.</risk>
    <risk id="R2">A/B metric gaming / selector leakage. (Medium/High) Mitigation: **per-selector reporting in scorecard (from .015). SelectorGameDetected fork wired here. Random as floor.**</risk>
    <risk id="R3">Subtype explosion. (High/High) Mitigation: selectors operate on graph-level; do not touch subtype_kind vocabulary.</risk>
    <risk id="R4">Scope creep. (High/High) Mitigation: **Three selectors ONLY — random, keyword, centrality. No LLM selector. No randomized-seed variants (v0.2). If you catch yourself adding a 4th selector, STOP.**</risk>
    <risk id="R7">Legacy churn. (Low/Medium) Mitigation: new module; no legacy consumers.</risk>
    <risk id="R9">Selector optimization / compiler+selector co-adaptation. (Medium/Critical) Mitigation: **primary_metric uses `best_lift` (max across 3 selectors), not average. This TO is the structural defense against R9.**</risk>
  </risks>

  <dependencies>
    <dependency to="COMP_LEARNS.011" status="required">Scorecard.DownstreamAB + SelectorAB dataclasses</dependency>
  </dependencies>

  <cross_domain_coordination><none/></cross_domain_coordination>

  <next>On commit + MCP COMPLETE: .015 per_selector integration unblocks; .017 end-to-end scoring has 3 selectors live.</next>
</task_order>
