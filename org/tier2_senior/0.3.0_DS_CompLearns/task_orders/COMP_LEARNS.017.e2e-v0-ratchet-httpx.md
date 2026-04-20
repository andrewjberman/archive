<task_order>
  <metadata>
    <id>0.3.0_DS_CompLearns-2026-04-16-comp-learns-017-e2e-v0-ratchet-httpx</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.3.0_DS_CompLearns</issued_to>
    <date>2026-04-16</date>
    <status>staged</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — integration gate; all prior parents must land first</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_ARCHITECTURE.md @ 8df31d86 (v3 — peer review invariant-breakage fixes)</ref>
    <ref type="prd_section">§6.1 ratchet-critical vs exploratory split, §6.2 Scorecard schema (v3) + __eq__ discipline, §6.4.1 cached-answer regime (warm-up phase vs primary_metric computation), §7.1-§7.5 loop contract + active adversarial sub-loop, §8 v0 exit criterion, §11.1 R13 + R14, §12.2 TO .017 three-phase mandate (KEEP + DISCARD + active-adversarial + determinism-re-run)</ref>
    <ref type="predecessor_prd">docs/architecture/COMP_LEARNS_LOOP_ORCHESTRATOR.md (PRD #4 — .004 complete at e657c232; bash driver in place)</ref>
  </references>

  <objective>
    Wire the v0 end-to-end ratchet on `httpx` under the v3 scorecard contract (§6.2 RC/Exp split) and §6.4.1 cached-answer regime. This is the integration gate — all prior scaffolding from .011-.016 + .020 + .021 must land before this TO executes.

    Deliver:
    1. `comp/targets/httpx/compiler.py` — minimal subtype-invoker. Calls `ImportsSubtype().extract(parsed_files)` → `GraphBuilder().build(records)` → v3 Scorecard emission with `ratchet_critical` + `exploratory` sections populated per §6.2. Returns scorecard-shaped JSON via the existing PRD #3 CLI contract.
    2. `comp/loop/ratchet.py` — keep/revert state machine per §7.1. Two-phase scoring: **(a) warm-up phase** — call `bench.warm_up_cache(compiler_sha, target, selectors)` to populate the on-disk cache for any new `(question, compiler_sha, selector)` tuples; **(b) primary_metric computation** — reads ratchet_critical only; every LLM answer served from cache; cache-miss → `CacheMissDuringPrimaryMetric` halt per §6.4.1. Consumes v3 Scorecard; appends to experiment_log; manages champion SHA.
    3. `comp/loop/failure_miner.py` — extracts failure patterns from `ratchet_critical` fields (structural misses, mutation stability drops, per-selector A/B imbalance). Exploratory fields do NOT drive failure mining for ratchet decisions.
    4. `comp/loop/propose.py` — **null proposer for v0** (human edits compiler.py; propose returns a handoff-to-human marker).
    5. `comp/loop/adversarial.py` — **`AdversarialGenerator` protocol per §7.5.** Active sub-loop: failure → targeted variants (N=10 capped, 3 failures/iter cap) → re-test inside current iteration.
    6. `comp-learns-run.sh httpx --once` wired to execute one full iteration end-to-end (warm-up → primary_metric → compare → KEEP/REVERT → log).
    7. **Demonstrated on httpx:** one KEEP cycle + one DISCARD cycle (induced regression) + active-adversarial sub-loop on ≥1 failure + **determinism re-run proving Scorecard __eq__ on same `(target_version, compiler_sha)` across two bench runs.** All four must land in the same session log with commit SHAs.

    Explicitly out of scope: LLM proposer (v0.4 per §9), generalization F1 (v0.2 per §9), loop continuation beyond 2 iterations in this TO's acceptance (the bash driver continues iterating after .017 ships; we just prove the mechanics work).
  </objective>

  <scope>
    <files>
      <file action="create">comp/targets/httpx/compiler.py</file>
      <file action="create">comp/loop/ratchet.py</file>
      <file action="create">comp/loop/failure_miner.py</file>
      <file action="create">comp/loop/propose.py</file>
      <file action="create">comp/loop/adversarial.py</file>
      <file action="create">comp/loop/tests/test_ratchet_keep.py</file>
      <file action="create">comp/loop/tests/test_ratchet_discard.py</file>
      <file action="create">comp/loop/tests/test_adversarial_subloop.py</file>
      <file action="create">comp/loop/tests/test_scorecard_determinism_rerun.py</file>
      <file action="modify">comp/bin/comp-learns-run.sh (wire --once flag to new ratchet + scorecard emission)</file>
      <file action="create">comp/targets/httpx/scorecards/ (directory; first two scorecards land on iter 1 + iter 2)</file>
      <file action="create">comp/targets/httpx/experiment_log.jsonl</file>
    </files>
  </scope>

  <wire_contract>
    **Ratchet state machine (loop/ratchet.py) per §7.1-§7.2 + §6.4.1:**
    ```python
    def iterate(target: str) -> IterationResult:
        candidate_sha = git_head(worktree)
        target_version = compute_target_version(f"comp/targets/{target}/")

        # (a) Warm-up phase — populate cache for any new (question, compiler_sha, selector) tuples.
        # This is the ONLY place ratchet-critical LLM calls happen; temperature=0 enforced at protocol.
        # Budget guard: $50/target/cycle (cache.py).
        bench.warm_up_cache(
            compiler_sha=candidate_sha,
            target=target,
            selectors=["random", "keyword", "centrality"],
        )

        # (b) Primary-metric computation — cache-only; cache-miss raises CacheMissDuringPrimaryMetric + HALT.
        candidate_scorecard = bench.score(candidate_sha, target, target_version=target_version)

        # Active adversarial sub-loop (§7.5) — failure mining reads ratchet_critical only.
        failures = failure_miner.extract(candidate_scorecard.ratchet_critical)
        for failure in failures[:3]:  # cap 3 failures/iter
            variants = adversarial.generate(failure, target_root, budget=10)
            for variant in variants:
                variant_scorecard = bench.score(candidate_sha, variant.mutated_root, target_version=target_version)
                candidate_scorecard.ratchet_critical.mutation_stability.per_failure[failure.id].append(variant_scorecard.brief())

        champion_scorecard = bench.load_champion_scorecard(target)
        verdict = compare(candidate_scorecard, champion_scorecard)   # reads scorecard.primary_metric only

        if verdict == KEEP:
            champion = candidate
            experiment_log.record(iter=N, verdict="kept", primary_metric=..., delta=..., notes=...)
        elif verdict == REVERT:
            git_checkout(champion)
            experiment_log.record(iter=N, verdict="discarded", primary_metric=..., delta=..., notes=...)
        else:
            experiment_log.record(iter=N, verdict="tied", ...)

        return IterationResult(verdict, candidate_scorecard, failures)
    ```

    **Failure miner (loop/failure_miner.py):**
    - Input: Scorecard.
    - Output: `list[Failure]` — patterns like "missed dynamic imports in httpx/_transports/*.py" (per-module recall drops), "per-selector A/B imbalance", "mutation stability drop on rename seeds {2,3}".
    - Each Failure has `id`, `kind`, `target_location`, `expected`, `observed`, `severity`.

    **AdversarialGenerator (loop/adversarial.py):**
    - `generate(failure, target_root, budget=10)` → `list[MutatedTarget]` stressing the same failure class.
    - For an "imports" failure at `httpx/_transports/default.py`, generate rename variants of the specific module names involved.
    - Budget: 10 variants per failure × 3 failures = 30 variant-extractions per iteration (compute-only; no LLM cost).

    **Propose (loop/propose.py) — v0 null proposer:**
    ```python
    def propose(champion_sha: str, recent_failures: list[Failure], log: ExperimentLog) -> ProposalResult:
        return ProposalResult(mode="human_edit_handoff", candidate_sha=None, notes="v0: human edits compiler.py on branch; run --once to iterate")
    ```
  </wire_contract>

  <acceptance_criteria>
    1. **Phase 2 — end-to-end iteration runs:** `comp-learns-run httpx --once` executes without error. experiment_log.jsonl gets one entry. v3 Scorecard JSON file committed to `comp/targets/httpx/scorecards/{sha_short}_{target_version_short}.json`. Scorecard has both `ratchet_critical` and `exploratory` sections populated per §6.2; `primary_metric` is computed from `ratchet_critical` only.
    2. **Scorecard schema split (NEW v3):** `scorecard.ratchet_critical.downstream_ab.per_selector` has entries for random + keyword + centrality; `scorecard.ratchet_critical.mutation_stability.score` is a float; `scorecard.ratchet_critical.conflict_fraction == 0.0`; `scorecard.exploratory.behavioral` is populated (informational) and does NOT affect primary_metric (proven via test_primary_metric.py in .015).
    3. **Phase 3 KEEP cycle:** initial `compiler.py` produces `scorecard_A` with `primary_metric > 0` over empty-graph baseline; ratchet records KEEP; `experiment_log.jsonl` entry 1 has `"verdict":"kept"`. Commit SHA recorded in session log.
    4. **Phase 3 DISCARD cycle (induced regression):** deliberately edit `compiler.py` to emit strictly worse output (drop all `dynamic` attribute detection so dynamic imports are missed). Re-run `comp-learns-run httpx --once`. Verify:
       - `scorecard_B.primary_metric < scorecard_A.primary_metric`.
       - Ratchet records DISCARD.
       - `git rev-parse HEAD` returns champion SHA (the pre-regression one).
       - `experiment_log.jsonl` entry 2 has `"verdict":"discarded"`.
       - **Both cycle commit SHAs captured in session log.**
    5. **Phase 3 Active adversarial demonstration:** run at least one iteration where `failure_miner` surfaces a failure and `adversarial.generate()` produces ≥1 targeted variant. Variant scorecard appended to `scorecard.ratchet_critical.mutation_stability.per_failure[failure.id]`. **Prove §7.5 sub-loop is live, not dormant.**
    6. **Phase 3 Determinism re-run (NEW v3) — R13/R14 proof:** after the KEEP cycle lands scorecard_A at `sha_A`, run `comp-learns-run httpx --once` a SECOND time against the SAME `(target_version, compiler_sha)` (no compiler edit, no target edit; cache already warm). Load both scorecards and assert `scorecard_A_run1 == scorecard_A_run2` using `Scorecard.__eq__` from .011/.015. Equal-by-__eq__ proves ratchet_critical + primary_metric are byte-identical across runs. `emitted_at` MUST differ (different timestamps) but MUST NOT affect __eq__. This is the direct test that R14 judge drift is closed.
    7. `pytest comp/loop/ -v` exits 0 (includes test_ratchet_keep, test_ratchet_discard, test_adversarial_subloop, **test_scorecard_determinism_rerun**).
    8. **Scorecard A + Scorecard B both show populated `ratchet_critical.downstream_ab.per_selector`** (from .020) with random, keyword, centrality. Random-wins does NOT fire `SelectorGameDetected` on the honest httpx run (centrality should win; else investigate).
    9. **Scorecard A `ratchet_critical.mutation_stability.score ≥ 0.85`** on the `imports` subtype (from .021's integration).
    10. **Cached-answer regime live (NEW v3):** during Phase 2, verify by spy/log that `bench.warm_up_cache()` was called for any new `(question, compiler_sha, selector)` tuples AND the subsequent `bench.score()` primary_metric path made ZERO fresh LLM calls — every answer served from cache. Any `CacheMissDuringPrimaryMetric` raise during normal operation = TO rework.
    11. Session log `## Compiler Tools` reproduces every `<run>` from `<compiler_tools_mandate>` with observed output + pass/fail vs. `<expect>`. Missing rows = REWORK.
    12. MCP COMPLETE to 2.0.0_SA_COO~Z with KEEP commit SHA + DISCARD commit SHA + scorecard_A + scorecard_B JSON dumps + experiment_log.jsonl first two entries + one adversarial sub-loop entry + **determinism-re-run proof (both scorecard paths + `__eq__` assertion passing)**.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>python -c "from comp.ir import Node, Edge; from comp.compiler_subtypes.imports import ImportsSubtype; from comp.graph_builder import GraphBuilder; from comp.bench import Scorecard; from comp.bench.ab import run_ab; from comp.bench.primary import primary_metric; from comp.parsers.python import PythonParser; print('all-deps-ok')"</run>
        <expect>Prints `all-deps-ok`. All seven parent TOs (.011-.016 + .020 + .021) have shipped.</expect>
        <if_mismatch>STOP. Identify missing parent(s) and ping COO~Z. Do NOT proceed to wire the ratchet against stub dependencies — that defeats integration testing.</if_mismatch>
      </step>
      <step>
        <run>ls comp/targets/httpx/gold/imports_gold.jsonl comp/targets/httpx/gold/ab_questions.yaml comp/targets/httpx/gold/ab_answer_key.yaml</run>
        <expect>All three gold artifacts present (landed by .016).</expect>
        <if_mismatch>STOP. .016 has not shipped. Ping COO~Z + CTO.</if_mismatch>
      </step>
      <step>
        <run>python -c "from comp.loop.adversarial import AdversarialGenerator; print('adv-ok')"</run>
        <expect>Prints `adv-ok`. AdversarialGenerator protocol importable (shipping in this TO).</expect>
        <if_mismatch>If this fails in Phase 1, it's expected — you haven't written it yet. Skip this step before code lands.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bash comp/bin/comp-learns-run.sh httpx --once</run>
        <expect>Runs one full iteration (warm-up → primary_metric → compare → log). Exits 0. Creates one v3 Scorecard JSON in `comp/targets/httpx/scorecards/{sha_short}_{target_version_short}.json`. Appends one line to `comp/targets/httpx/experiment_log.jsonl` with `"verdict":"kept"`. Scorecard JSON contains populated `ratchet_critical.downstream_ab.per_selector` (3 selectors) + `ratchet_critical.mutation_stability.score` (float ≥ 0.85) + `ratchet_critical.conflict_fraction == 0.0` + `exploratory.behavioral` populated (informational).</expect>
        <if_mismatch>Debug the iteration. If per_selector empty, .015 + .020 wiring broken. If mutation_stability 0.0, .021 wiring broken. If conflict_fraction > 0, .014 wiring broken. If scorecard still has flat `.adversarial` (v2 schema), .011/.015 did not land the v3 split — ping COO~Z.</if_mismatch>
      </step>
      <step>
        <run>jq '.primary_metric, (.ratchet_critical | keys), (.exploratory | keys)' comp/targets/httpx/scorecards/*.json | tail -10</run>
        <expect>Prints a float for primary_metric, a list containing `["conflict_fraction","downstream_ab","efficiency","mutation_stability","structural"]` (sorted) for ratchet_critical keys, and a list containing `["behavioral","generalization","human_annotations","open_ended_judge"]` for exploratory keys.</expect>
        <if_mismatch>Scorecard schema does not match v3 §6.2. Do NOT commit with v2-flat schema.</if_mismatch>
      </step>
      <step>
        <run># Induce regression, re-run
#   1. git commit a deliberate regression to compiler.py (drop dynamic-attribute emission)
#   2. bash comp/bin/comp-learns-run.sh httpx --once
#   3. git log --oneline -3
</run>
        <expect>Second iteration's experiment_log entry has `"verdict":"discarded"`; HEAD is back to the pre-regression SHA (champion); scorecard_B.primary_metric &lt; scorecard_A.primary_metric.</expect>
        <if_mismatch>DISCARD semantics broken. Debug `compare.primary_metric` + `ratchet.revert` logic.</if_mismatch>
      </step>
      <step>
        <run>jq '.ratchet_critical.mutation_stability.per_failure | keys | length' comp/targets/httpx/scorecards/*.json | tail -1</run>
        <expect>≥ 1 — active-adversarial sub-loop fired on at least one failure.</expect>
        <if_mismatch>§7.5 sub-loop dormant. Debug failure_miner.extract() + adversarial.generate() wiring. If `.ratchet_critical.mutation_stability.per_failure` is absent, .011 did not ship the v3 schema — ping COO~Z.</if_mismatch>
      </step>
      <step>
        <run># Determinism re-run (R13 + R14 direct proof):
#   1. bash comp/bin/comp-learns-run.sh httpx --once    # run 2 — same (target_version, compiler_sha), cache already warm
#   2. pytest comp/loop/tests/test_scorecard_determinism_rerun.py -v
</run>
        <expect>Second run completes without making any fresh LLM call (cache already warm; warm_up_cache is a no-op). `test_scorecard_determinism_rerun` loads scorecard_A_run1 + scorecard_A_run2, asserts `scorecard_A_run1 == scorecard_A_run2` via `Scorecard.__eq__`, asserts `scorecard_A_run1.emitted_at != scorecard_A_run2.emitted_at`. Exits 0.</expect>
        <if_mismatch>STOP. __eq__ failure = R13 wall-clock contamination or R14 judge drift leaked into ratchet_critical. Diagnose via `diff <(jq -S . scorecard_A_run1.json) <(jq -S . scorecard_A_run2.json)` — any non-metadata diff is the leak.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/loop/ -v</run>
        <expect>All loop tests pass (including test_scorecard_determinism_rerun). Exit 0.</expect>
        <if_mismatch>Fix until green.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>ls comp/targets/httpx/scorecards/ | wc -l</run>
        <expect>≥ 2 — two scorecards from KEEP + DISCARD cycles.</expect>
        <if_mismatch>Missing scorecard files — check ratchet's scorecard emission path.</if_mismatch>
      </step>
      <step>
        <run>wc -l comp/targets/httpx/experiment_log.jsonl</run>
        <expect>≥ 2 lines (one per cycle).</expect>
        <if_mismatch>Experiment log broken. Check append-only discipline.</if_mismatch>
      </step>
      <step>
        <run>jq '.verdict' comp/targets/httpx/experiment_log.jsonl</run>
        <expect>First line prints `"kept"`. Second line prints `"discarded"`. Order matters — KEEP must precede DISCARD per PRD §12.2.</expect>
        <if_mismatch>Surface to COO~Z — verdict sequence is not as expected.</if_mismatch>
      </step>
      <step>
        <run>comp-blast comp/targets/httpx/compiler.py</run>
        <expect>Blast radius surfaces the bench + loop modules as consumers. No unexpected consumers elsewhere.</expect>
        <if_mismatch>Investigate unexpected consumers.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <risks>
    <risk id="R1">Benchmark dishonesty — gold authored to match compiler output. (Medium/Critical) Mitigation: gold-before-code invariant upheld by .016 attestation; induced-regression DISCARD cycle proves the bench distinguishes honest from dishonest compilers; mutation engine (.021) is the second line of defense.</risk>
    <risk id="R2">A/B metric gaming / selector leakage. (Medium/High) Mitigation: per-selector reporting in scorecard; SelectorGameDetected fork wired in .015; .017 proves the wiring on real httpx (centrality should win honestly).</risk>
    <risk id="R3">Subtype explosion. (High/High) Mitigation: .017 ships only `imports` subtype in compiler.py. Does NOT add new subtype kinds.</risk>
    <risk id="R4">Scope creep. (High/High) Mitigation: **Two cycles (KEEP + DISCARD) + one adversarial sub-loop ONLY. No LLM proposer, no generalization, no perturbation suite beyond what .021 shipped.**</risk>
    <risk id="R7">Legacy churn. (Low/Medium) Mitigation: `comp/bin/comp-learns-run.sh` is modified but the legacy bash driver contract is preserved; Track B continues to work.</risk>
    <risk id="R11">Mutation engine producing semantically-broken targets. (Medium/Medium) Mitigation: .021 has its own pytest suite on `comp/framework/`; .017 relies on that test having passed. If .017 fires mutations that break httpx semantics, that's a .021 regression — surface to COO~Z.</risk>
    <risk id="R12">Passive loop too slow. (Low after amendment/High) Mitigation: **§7.5 active adversarial sub-loop demonstrated inside the SAME iteration. Failure → targeted variants → re-test — proven at .017 Phase 3.**</risk>
    <risk id="R13">**Wall-clock contamination — time fields leaking into ratchet_critical poison __eq__ + corrupt champion selection across re-runs. (High without mechanical enforcement / Critical)** Mitigation: Phase 2 determinism re-run test asserts `scorecard.__eq__` holds across two runs of same `(target_version, compiler_sha)` with different `emitted_at`. Any __eq__ failure on identical inputs is the smoking gun — fix before commit.</risk>
    <risk id="R14">**Judge drift across re-runs — non-deterministic LLM output feeding primary_metric makes champion selection drift. (Medium/Critical)** Mitigation: ratchet calls `bench.warm_up_cache` (separate from primary_metric) to populate the §6.4.1 cache; `bench.score`'s primary_metric path is cache-only (raises `CacheMissDuringPrimaryMetric` on miss — HALT, no fall-through). Temperature=0 enforced at JudgeBackend protocol via `ratchet_critical_call` wrapper. Determinism re-run test (Phase 2) is the direct proof the regime holds.</risk>
  </risks>

  <dependencies>
    <dependency to="COMP_LEARNS.011" status="required">All core contracts (Scorecard, GraphBuilder, Subtype, Parser)</dependency>
    <dependency to="COMP_LEARNS.013" status="required">ImportsSubtype extractor</dependency>
    <dependency to="COMP_LEARNS.014" status="required">GraphBuilder implementation + GraphDiff</dependency>
    <dependency to="COMP_LEARNS.015" status="required">Structural scorer + A/B + JudgeBackend + primary_metric</dependency>
    <dependency to="COMP_LEARNS.016" status="required">httpx gold (imports + ab_questions + ab_answer_key)</dependency>
    <dependency to="COMP_LEARNS.020" status="required">3 Selectors (random, keyword, centrality) — scorecard per_selector populated</dependency>
    <dependency to="COMP_LEARNS.021" status="required">Mutation engine — scorecard adversarial.mutation_stability populated</dependency>
    <dependency to="COMP_LEARNS.012" status="transitive">PythonParser (via .013 and .021)</dependency>
  </dependencies>

  <cross_domain_coordination>
    **v3 sweep marker (2026-04-20 COO~Z):** swept from v2→v3 per CTO checklist 2026-04-16 13:59Z (preserved in ~B handoff log). Deltas applied: scorecard path updates to `ratchet_critical.*` throughout ratchet state machine, wire_contract + mandates; warm-up-vs-primary_metric two-phase split per §6.4.1; determinism re-run test (`test_scorecard_determinism_rerun`) as direct R13+R14 proof; Phase 2 schema-assert step guards against v2-flat scorecard slipping in; cached-answer regime live-check (zero fresh LLM calls during primary_metric); R13 + R14 risks added.

    **Lane coordination:** this TO is the integration gate — it depends on .011 + .013 + .014 + .015 + .016 + .020 + .021 ALL shipping their v3 surfaces. If any parent lands on v2 schema, this TO cannot proceed. Ping COO~Z immediately on any v2-contract surface encountered in Phase 1.
  </cross_domain_coordination>

  <next>On commit + MCP COMPLETE to 2.0.0_SA_COO~Z: .018 (CTO program.md v1.0) + .019 (optional viz CLI) unblock. Project moves toward v0.1 (second subtype, second target, or LLM proposer). v0 exit criterion (§8) satisfied when .017 ships.</next>
</task_order>
