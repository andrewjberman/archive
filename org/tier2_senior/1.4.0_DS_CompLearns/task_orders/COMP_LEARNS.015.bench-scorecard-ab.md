<task_order>
  <metadata>
    <id>1.4.0_DS_CompLearns-2026-04-16-comp-learns-015-bench-scorecard-ab</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>1.4.0_DS_CompLearns</issued_to>
    <date>2026-04-16</date>
    <status>staged</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — critical path; bench is the product surface. Fallback owner ~B after .013 closes if ~D capacity-blocked on CN-P1b.</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_ARCHITECTURE.md @ dc839e77 (v4.2 — R1/R3 layer separation + ship-blocker MUST-halt + enforcement-owner paragraph)</ref>
    <ref type="prd_section">§6.1 ratchet-critical vs exploratory split + primary objective function (v3), §6.2 Scorecard schema (v3), §6.3 required benchmark components + §6.3 gold ship-blocker + enforcement-owner paragraph (v4.2), §6.4 A/B LLM protocol + JudgeBackend judge-split (enumerable/set_membership/numeric in ratchet-critical; open-ended → exploratory only), §6.4.1 cached-answer regime (ratchet-critical non-negotiable), §6.5 selector consumption, §6.6 mutation axis consumption, §11.1 R13 + R14</ref>
    <ref type="prd">docs/architecture/COMP_LEARNS_TARGET_CLOSEOUT.md v2.0 (§7.1 .015a decision: inline — no standalone micro-TO; §7.3 AC #7 preserved with 5 fixtures a-e because it maps to the v4 6/6-coverage bug caught during .016)</ref>
    <ref type="amendment">2026-04-21 amendment — AC #7 added + Phase 2 compiler mandate step added for `validate_gold_survey_attestation` per TARGET_CLOSEOUT §8.3. Authored by 1.1.0_SA_CTO. Subsequent ACs shifted 7→8, 8→9, ..., 13→14. MCP target updated 2.0.0_SA_COO~Z → 2.1.0_SA_COO per dyad succession.</ref>
  </references>

  <objective>
    Implement bench scorecard + structural scorer + A/B comparator with **model-agnostic `JudgeBackend` protocol per §6.4 AND v3 ratchet-critical/exploratory scorecard split per §6.1–6.2 AND v3 cached-answer regime per §6.4.1.** Claude Sonnet 4.6 is the v0 backend, NOT hard-wired — backends are pluggable. **Every ratchet-critical LLM call runs at temperature=0 and is served from the on-disk cache; cache-miss during primary_metric computation = benchmark halt, not a fresh LLM call.**

    Deliver:
    1. `comp/bench/structural.py` — precision / recall / F1 computation vs gold JSONL; per-subtype + aggregate. Heuristic records discounted per §5.1 confidence ladder. Output populates `scorecard.ratchet_critical.structural`.
    2. `comp/bench/behavioral.py` — legacy query_pass_rate from framework (thin adapter). Output populates `scorecard.exploratory.behavioral` (informational only; never contributes to primary_metric).
    3. `comp/bench/efficiency.py` — extraction_time (bucketed per §6.1 to kill jitter), graph_size_bytes, peak_memory_mb. Output populates `scorecard.ratchet_critical.efficiency`.
    4. `comp/bench/generalization.py` — held-out target F1 (v0 stub; `unevaluated=true` since we have one target). Output populates `scorecard.exploratory.generalization`.
    5. **`comp/bench/ab.py` — A/B comparator consuming `.020`'s Selector outputs. Populates `scorecard.ratchet_critical.downstream_ab.per_selector` for all 3 selectors; computes `best_selector` + `best_lift`; fires `SelectorGameDetected` when `best_selector=="random"` and `best_lift > 0.1`. All ratchet-critical LLM calls go through the cached-answer regime (§6.4.1); cache-miss during primary_metric computation raises `CacheMissDuringPrimaryMetric` and halts the bench.**
    6. **`comp/bench/judges/base.py` — `JudgeBackend` Protocol with `temperature: float = 0.0` default AND a `ratchet_critical_call(...)` wrapper that asserts `temperature == 0.0` before dispatch.**
    7. **`comp/bench/judges/anthropic.py` — `AnthropicJudge` implementing `JudgeBackend` — claude-sonnet-4-6 v0 backend, uses Anthropic's deterministic-output knobs where available (temperature=0 minimum).**
    8. `comp/bench/judges/mock.py` — deterministic `MockJudge` for tests (keyed response table).
    9. **`comp/bench/primary.py` — primary_metric formula per §6.1 (v3): reads ONLY from `ratchet_critical`; formula = `ab_lift * (1 + α * token_reduction) * mutation_stability * (1 - conflict_penalty)` with α=0.3 default, tiebreaker 1 structural F1, tiebreaker 2 negative-LoC-delta.**
    10. **A/B response caching keyed per §6.4.1 on the full 9-tuple: `(question_text, source_hash, graph_hash, selector_hash, selector_version, model_id, model_version, selected_context_token_count, temperature=0)`. Swapping selector, selector version, model, model version, or selected-context size invalidates cache. target_version bump (from `ab_questions.yaml` / `ab_answer_key.yaml` edits) orphans prior cache entries (not deleted; not used).**
    11. **`comp/bench/ab_answer_key_validator.py` — validates `ab_answer_key.yaml` at load time: every entry in the ratchet-critical pool MUST be `enumerable` / `set_membership` / `numeric`. Free-text / open-ended entries in the ratchet pool = raise `RatchetPoolOpenEndedRejected`. Open-ended is routed to `exploratory` pool only.**

    Explicitly out of scope: selectors themselves (.020), mutation engine itself (.021), adversarial generator (.017 Phase 3), gold authoring (.016), loop ratchet state machine (.017).
  </objective>

  <scope>
    <files>
      <file action="create">comp/bench/structural.py</file>
      <file action="create">comp/bench/behavioral.py</file>
      <file action="create">comp/bench/efficiency.py</file>
      <file action="create">comp/bench/generalization.py</file>
      <file action="create">comp/bench/ab.py</file>
      <file action="create">comp/bench/primary.py</file>
      <file action="create">comp/bench/cache.py (response cache helpers)</file>
      <file action="create">comp/bench/judges/__init__.py</file>
      <file action="create">comp/bench/judges/base.py</file>
      <file action="create">comp/bench/judges/anthropic.py</file>
      <file action="create">comp/bench/judges/mock.py</file>
      <file action="create">comp/bench/ab_answer_key_validator.py</file>
      <file action="create">comp/bench/tests/test_structural_scorer.py</file>
      <file action="create">comp/bench/tests/test_ab_selector_integration.py</file>
      <file action="create">comp/bench/tests/test_judge_protocol.py</file>
      <file action="create">comp/bench/tests/test_selector_game_detected.py</file>
      <file action="create">comp/bench/tests/test_primary_metric.py</file>
      <file action="create">comp/bench/tests/test_cache_key.py</file>
      <file action="create">comp/bench/tests/test_cached_answer_regime.py</file>
      <file action="create">comp/bench/tests/test_ab_answer_key_validator.py</file>
      <file action="create">comp/bench/tests/test_scorecard_eq.py</file>
    </files>
  </scope>

  <wire_contract>
    ```python
    class JudgeBackend(Protocol):
        model_id: str                                # e.g. "claude-sonnet-4-6"
        model_version: str                           # e.g. "claude-sonnet-4-6-20260311" — cache-key input per §6.4.1
        provider: str                                # e.g. "anthropic"

        def ask(
            self,
            system: str,
            user: str,
            *,
            max_tokens: int = 1024,
            temperature: float = 0.0,                # §6.4.1 ratchet-critical default = 0.0
            seed: int | None = None,
        ) -> JudgeResponse:
            """Deterministic under fixed seed where backend supports it."""

        def ratchet_critical_call(self, system: str, user: str, **kwargs) -> JudgeResponse:
            """Wrapper enforcing temperature=0 + provider deterministic-output knobs.
            Raises NonDeterministicRatchetCall if temperature != 0.0 or seed omitted on backends supporting it."""

    @dataclass(frozen=True)
    class JudgeResponse:
        text: str
        tokens_prompt: int
        tokens_completion: int
        model_id: str
        model_version: str
        temperature: float
        latency_ms: int
    ```

    **Scorecard schema (v3 §6.2) — two sections:**
    ```python
    @dataclass
    class Scorecard:
        target: str
        target_version: str                          # hash of frozen target source + gold; bump orphans cache
        compiler_sha: str
        subtypes_enabled: list[str]
        ratchet_critical: RatchetCritical            # contributes to primary_metric
        exploratory: Exploratory                     # reported but NEVER contributes
        primary_metric: float                        # computed from ratchet_critical only
        emitted_at: str                              # metadata; EXCLUDED from __eq__

    @dataclass
    class RatchetCritical:
        structural: Structural                       # precision/recall/F1 vs frozen gold
        efficiency: Efficiency                       # bucketed extraction_time + graph_size_bytes + peak_memory_mb
        conflict_fraction: float
        mutation_stability: MutationStability        # §6.6 — seeded, deterministic
        downstream_ab: DownstreamAB                  # §6.5 — frozen cached-answer regime mandatory

    @dataclass
    class Exploratory:
        behavioral: Behavioral                       # legacy queries.yaml — informational only
        generalization: Generalization               # v0 = unevaluated
        open_ended_judge: OpenEndedJudge | None      # v0 = None
        human_annotations: list[str]
    ```

    `Scorecard.__eq__` compares `ratchet_critical + primary_metric` only. `emitted_at`, `human_annotations`, `exploratory.behavioral.timing` excluded. Two scorecards for same `(target_version, compiler_sha)` MUST compare equal regardless of when they ran.

    **Primary metric (§6.1 v3) — reads ONLY from `ratchet_critical`:**
    ```python
    def primary_metric(s: Scorecard, alpha: float = 0.3) -> float:
        rc = s.ratchet_critical
        ab_lift = rc.downstream_ab.best_lift          # max across selectors per §6.5
        token_reduction = rc.downstream_ab.per_selector[rc.downstream_ab.best_selector].token_reduction_pct
        mutation_stability = rc.mutation_stability.score   # ∈ [0, 1], §6.6 mean across mutations × seeds
        conflict_penalty = min(1.0, 0.02 * rc.downstream_ab_elevation_required_count())
        base = ab_lift * (1.0 + alpha * token_reduction)
        return base * mutation_stability * (1.0 - conflict_penalty)
    # Tiebreaker 1: structural F1.  Tiebreaker 2: negative-LoC-delta.
    ```

    **Cache key (§6.4.1 — 9-tuple, all inputs that shift LLM output):**
    ```python
    cache_key = sha256(
        f"{question_text}|{source_hash}|{graph_hash}|{selector_hash}|{selector_version}|"
        f"{model_id}|{model_version}|{selected_context_token_count}|temperature=0"
    )
    ```
    Stored at `comp/targets/{name}/ab_cache/{cache_key}.json`. **Cache is git-tracked** (diffable, auditable, survives sessions). Prunable via `bench.cache.prune(older_than=N_days)`; never auto-evicted mid-run. `target_version` bump orphans prior entries (not deleted, not used).

    **Cached-answer regime (§6.4.1 — ratchet-critical non-negotiable):**
    1. **Temperature=0 mandatory** on every ratchet-critical LLM call; provider deterministic knobs engaged where available.
    2. **Cache-hit required for primary_metric.** During primary_metric computation, every answer is served from cache. Cache-miss on a ratchet-critical `(question, compiler_sha, selector)` tuple → raise `CacheMissDuringPrimaryMetric` and HALT the bench. Do NOT fall through to a fresh LLM call.
    3. **Cache-miss path (warm-up phase, separate from primary_metric):** when a genuinely new tuple is first evaluated, bench calls LLM ONCE, deterministic-judges via `ab_answer_key`, writes response + cache entry. Warm-up must complete + commit to disk BEFORE scoring starts.
    4. `ab_questions.yaml` / `ab_answer_key.yaml` edits bump `target_version`; prior cache entries are orphans.

    **ab_answer_key validator (§6.4 judge split):** at load time, reject any ratchet-critical pool entry whose answer type is not `enumerable` / `set_membership` / `numeric`. Free-text / open-ended answers in the ratchet pool → raise `RatchetPoolOpenEndedRejected` citing the offending question_id. Open-ended is valid in the exploratory pool only.

    **SelectorGameDetected trigger:** when `scorecard.ratchet_critical.downstream_ab.best_selector == "random"` AND `best_lift > 0.1` — raise `SelectorGameDetected` with scorecard attached; loop halts; CTO notified via experiment_log `fork` entry.

    **Budget guardrail:** hard cap `$50` per target per iteration cycle (applies to warm-up phase only; primary_metric is cache-only), tracked in `comp/bench/cache.py`. Exceeding: log halts + raises `AB_BUDGET_EXCEEDED`.
  </wire_contract>

  <acceptance_criteria>
    1. **Scorecard round-trip (from .011):** verified in integration — `load(dump(scorecard)) == scorecard` with all v0 fields populated on both `ratchet_critical` and `exploratory` sections.
    2. **Scorecard __eq__ discipline (test_scorecard_eq.py):** two scorecards for same `(target_version, compiler_sha)` emitted at different `emitted_at` values AND different `human_annotations` AND different `exploratory.behavioral.timing` MUST compare equal. Changing any `ratchet_critical` field MUST compare unequal.
    3. **Structural scorer tests (test_structural_scorer.py):** F1 on known-good synthetic case = 1.0; F1 on known-bad (zero-overlap records vs gold) < 0.5; precision/recall computed separately per-confidence bucket. Heuristic records discounted in aggregate score. Populates `ratchet_critical.structural` only.
    4. **JudgeBackend protocol (test_judge_protocol.py):** `AnthropicJudge` implements `JudgeBackend`; `MockJudge` returns deterministic outputs for test use; bench code never calls Anthropic SDK directly — only through protocol. `ratchet_critical_call(...)` enforces temperature=0 — raises `NonDeterministicRatchetCall` when passed `temperature=0.7`.
    5. **Cached-answer regime (test_cached_answer_regime.py) — NEW v3:**
       a. `bench.primary_metric(scorecard)` with a pre-populated cache = returns float (no LLM call made).
       b. `bench.primary_metric(scorecard)` with a missing cache entry for any ratchet-critical `(question, compiler_sha, selector)` tuple MUST raise `CacheMissDuringPrimaryMetric` and NOT fall through to a fresh LLM call. Asserted by spying on the MockJudge — call count must be 0 during primary_metric computation.
       c. Warm-up phase (`bench.warm_up_cache(compiler_sha, target, selectors)`) DOES call the judge, writes entries, then `primary_metric` succeeds on the same compiler_sha.
    6. **ab_answer_key validator (test_ab_answer_key_validator.py) — NEW v3:** loading an `ab_answer_key.yaml` where a ratchet-critical entry has answer type `free_text` / `open_ended` MUST raise `RatchetPoolOpenEndedRejected` citing the offending `question_id`. Loading an answer key where all ratchet-critical entries are `enumerable` / `set_membership` / `numeric` MUST load cleanly. Exploratory-pool entries MAY be open-ended.
    7. **Gold survey attestation validator (test_gold_survey_attestation.py) — NEW v4.2 per COMP_LEARNS_TARGET_CLOSEOUT.md §7.1 (inline; `.015a` standalone micro-TO rejected):**
       a. `validate_gold_survey_attestation(target_root: Path)` exists in `ab_answer_key_validator.py` as a public function.
       b. On a fixture where `ab_answer_key.yaml` + `imports_gold.jsonl` show <100% vocabulary coverage for any dimension AND `GOLD_SURVEY.md` lacks a "Dimension Values Not Observed" section, MUST raise `GoldSurveyAttestationMissing` citing the absent dimension value.
       c. On a fixture where `GOLD_SURVEY.md` has the section but lacks a grep command + output for an absent value, MUST raise `GoldSurveyAttestationMissing`.
       d. On the real httpx fixture (present in repo as of `.016` ship at commit `58a52153`), MUST return cleanly — `resolution=dynamic` is documented with reproducible grep evidence.
       e. On a fabricated fixture with 100% vocabulary coverage (every dimension value appears ≥2× in gold), MUST return cleanly WITHOUT requiring a "Dimension Values Not Observed" section.
    8. **A/B with selectors integration (test_ab_selector_integration.py):** given frozen cached responses from 3 fake selectors (seeded fixtures), `bench.ab.run(scorecard, selectors=[random, keyword, centrality])` populates `ratchet_critical.downstream_ab.per_selector` for all 3 selectors; `best_selector` + `best_lift` computed correctly (argmax).
    9. **SelectorGameDetected (test_selector_game_detected.py):** fabricated scorecard where `random` wins with `best_lift=0.15` raises `SelectorGameDetected`; fabricated scorecard where `centrality` wins with `best_lift=0.2` does NOT raise.
    10. **Primary metric (test_primary_metric.py):** primary_metric formula hand-verified against 3 synthetic scorecards with known values; α default = 0.3; reads ONLY from `ratchet_critical`; mutation_stability weight applied; conflict_penalty applied. Identical `(target_version, compiler_sha)` → identical primary_metric value across two bench runs (determinism ratchet).
    11. **Cache key (test_cache_key.py):** every one of the 9 inputs — `question_text, source_hash, graph_hash, selector_hash, selector_version, model_id, model_version, selected_context_token_count, temperature` — independently changes the cache key when perturbed in isolation. Identical inputs → identical key.
    12. `pytest comp/bench/ -v` exits 0.
    13. Session log `## Compiler Tools` reproduces every `<run>` from `<compiler_tools_mandate>` with observed output + pass/fail vs. `<expect>`. Missing rows = REWORK.
    14. MCP COMPLETE to 2.1.0_SA_COO with commit hash + pytest output + sample Scorecard dict showing `ratchet_critical.downstream_ab.per_selector` populated AND demonstrating `Scorecard.__eq__` on two runs of same `(target_version, compiler_sha)` AND a sample `validate_gold_survey_attestation` return on the real httpx fixture.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>python -c "import anthropic; print(anthropic.__version__)"</run>
        <expect>Prints a version — Anthropic SDK available via ADVI_49EXEC.003 layer (shipped `c0a00bcc`) or local install. Phase 1 external block CLEARED per PRD v3 §11.2.</expect>
        <if_mismatch>Flag to COO~Z; proceed on MockJudge + structural scorer + protocol skeleton; ship AnthropicJudge as follow-up sweep.</if_mismatch>
      </step>
      <step>
        <run>python -c "from comp.bench import Scorecard, RatchetCritical, Exploratory, DownstreamAB, MutationStability; from comp.graph_builder import GraphBuilder, BuildResult; print('deps ok')"</run>
        <expect>Prints `deps ok`. .011 exposes v3 Scorecard with `ratchet_critical` + `exploratory` sections (not flat `.adversarial`); .014 exposes GraphBuilder. Import surface confirms v3 schema landed in .011.</expect>
        <if_mismatch>STOP. .011 or .014 has not shipped the v3 schema. Ping COO~Z — likely .011 still on v2 schema (flat `.adversarial`). Do NOT implement against v2 surface.</if_mismatch>
      </step>
      <step>
        <run>python -c "from comp.bench.judges.base import JudgeBackend; from inspect import signature; sig = signature(JudgeBackend.ratchet_critical_call); print('ratchet_critical_call signature:', sig)"</run>
        <expect>Protocol exposes `ratchet_critical_call(system, user, **kwargs)` that enforces temperature=0 (§6.4.1 non-negotiable). Asserts the temperature-0 mandate is wired into the protocol itself, not left to caller discipline.</expect>
        <if_mismatch>STOP. Add the `ratchet_critical_call` wrapper to `JudgeBackend` before implementing `AnthropicJudge`. The temperature-0 guarantee must live at the protocol level per PRD v3 §6.4.1 + R14.</if_mismatch>
      </step>
      <step>
        <run>ls comp/targets/httpx/gold/ab_questions.yaml comp/targets/httpx/gold/ab_answer_key.yaml 2>&amp;1 || echo "gold-not-landed"</run>
        <expect>Either both files exist (landed by .016) OR `gold-not-landed` — in which case Phase 2 A/B-on-real-gold step deferred and noted in session log. Protocol + scorer + validator + cache-regime tests run against fixtures regardless.</expect>
        <if_mismatch>No mismatch — both states are acceptable; log which state you observed.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>pytest comp/bench/tests/test_judge_protocol.py -v</run>
        <expect>JudgeBackend Protocol round-trip passes; MockJudge deterministic; AnthropicJudge constructs; `ratchet_critical_call` raises `NonDeterministicRatchetCall` when passed `temperature=0.7`; exits 0.</expect>
        <if_mismatch>Fix protocol typing + the temperature-0 enforcement wrapper.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/bench/tests/test_cached_answer_regime.py -v</run>
        <expect>primary_metric with pre-populated cache → returns float, judge.call_count==0. primary_metric with missing cache entry for a ratchet-critical tuple → raises `CacheMissDuringPrimaryMetric`. Warm-up phase populates cache; subsequent primary_metric succeeds. Exits 0.</expect>
        <if_mismatch>STOP. The cached-answer regime is the v3 non-negotiable per §6.4.1. Do NOT commit with a fall-through-to-fresh-LLM code path — that reintroduces R14 judge drift.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/bench/tests/test_ab_answer_key_validator.py -v</run>
        <expect>Ratchet-pool open-ended entry → `RatchetPoolOpenEndedRejected` with the offending question_id. All-deterministic ratchet pool → loads cleanly. Exploratory-pool open-ended → permitted. Exits 0.</expect>
        <if_mismatch>Fix validator logic; open-ended answers are §6.4 exploratory-pool-only by type.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/bench/tests/test_scorecard_eq.py -v</run>
        <expect>Two scorecards for same `(target_version, compiler_sha)` with different `emitted_at` + `human_annotations` + `exploratory.behavioral.timing` → `==` equal. Any `ratchet_critical` change → `!=`. Exits 0.</expect>
        <if_mismatch>Fix `Scorecard.__eq__` field exclusion per PRD v3 §6.2.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/bench/tests/test_selector_game_detected.py -v</run>
        <expect>SelectorGameDetected fires on `random` winning >0.1; does NOT fire on structured selector winning. Exits 0.</expect>
        <if_mismatch>Fix the detector's conditional.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/bench/tests/test_cache_key.py -v</run>
        <expect>All 9 inputs (`question_text, source_hash, graph_hash, selector_hash, selector_version, model_id, model_version, selected_context_token_count, temperature`) independently change the key when perturbed. Identical inputs → identical key. Exits 0.</expect>
        <if_mismatch>Fix cache key derivation — missing input = reintroduces R14 drift via unseen prompt shift.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/bench/tests/test_primary_metric.py -v</run>
        <expect>3 synthetic scorecards hand-verified; formula reads ONLY from `ratchet_critical` (test MUST assert `exploratory.behavioral.pass_rate` perturbation does NOT change primary_metric). Determinism ratchet: same `(target_version, compiler_sha)` → identical primary_metric value across two runs. Exits 0.</expect>
        <if_mismatch>Fix the read surface. If exploratory fields leak into primary_metric, R14 is back.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/bench/tests/test_gold_survey_attestation.py -v</run>
        <expect>All five fixtures from AC #7 (a-e) pass: missing-section raise, missing-grep raise, real-httpx clean, fabricated-100%-coverage clean, incomplete-coverage-but-section-present clean. Exit 0. This is the v4.2 ship-blocker enforcement per COMP_LEARNS_TARGET_CLOSEOUT.md §7.1 — cannot be skipped.</expect>
        <if_mismatch>Fix the validator until all fixtures pass. If authoring scope here genuinely overflows the TO estimate at 2x, pre-flag per Rule 7 and the dyad (1.1.0_SA_CTO + 2.1.0_SA_COO) will authorize a standalone .015a at that time — do NOT silently defer.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/bench/ -v</run>
        <expect>All tests pass. Exit 0.</expect>
        <if_mismatch>Fix until green.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-xref comp/bench/ab.py</run>
        <expect>Module visible; .017 ratchet + .020 selectors will consume after they land.</expect>
        <if_mismatch>`comp-build --rebuild` and re-check.</if_mismatch>
      </step>
      <step>
        <run>git diff HEAD~1 -- comp/bench/judges/ | grep -E "^\+.*temperature\s*=\s*[^0]" || echo "temp-0 clean"</run>
        <expect>Prints `temp-0 clean`. No added line introduces a non-zero default temperature on any JudgeBackend call path.</expect>
        <if_mismatch>STOP + revert. Any non-zero temperature default on a ratchet-critical path is a v3 §6.4.1 violation.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <risks>
    <risk id="R1">Benchmark dishonesty — gold authored to match compiler output. (Medium/Critical) Mitigation: structural scorer treats gold as read-only ground truth; never mutates. Ensure scoring does not short-circuit on identity — a compiler that emits gold verbatim should score F1=1.0 but a compiler that emits gold-with-attribute-perturbations should still drop below 1.0.</risk>
    <risk id="R2">A/B metric gaming / selector leakage. (Medium/High) Mitigation: **Cache key includes selector_hash + model_id per §6.4. SelectorGameDetected fork fires on random-wins anomaly. Per-selector reporting in scorecard surfaces when a compiler only wins with one specific selector (attack surface).**</risk>
    <risk id="R3">Subtype explosion. (High/High) Mitigation: bench does not add subtype kinds; structural scorer groups by subtype_kind from SUBTYPE_DIMENSIONS.</risk>
    <risk id="R4">Scope creep. (High/High) Mitigation: **Scorer + A/B + primary_metric + JudgeBackend ONLY.** Selectors are .020. Mutation engine is .021. Loop state machine is .017. If you catch yourself writing a Selector, STOP.</risk>
    <risk id="R7">Legacy churn. (Low/Medium) Mitigation: new modules; behavioral.py is thin adapter over framework/harness_base.</risk>
    <risk id="R8">A/B LLM budget overrun. (Medium/Low) Mitigation: `AB_BUDGET_EXCEEDED` raise at $50/target/cycle; budget tracked in cache.py.</risk>
    <risk id="R9">Selector optimization — compiler + selector co-optimize leaving graph substance behind. (Medium/Critical) Mitigation: **primary_metric uses `best_lift` (max across 3 selectors), not average. SelectorGameDetected flags random-wins. Scorecard emits per-selector block so the compiler can't hide behind one custom selector.**</risk>
    <risk id="R14">**Judge drift across re-runs — non-deterministic LLM output feeding primary_metric makes champion selection drift even when compiler is unchanged.** (Medium/Critical) Mitigation: (a) §6.1 ratchet-critical / exploratory split — primary_metric reads ratchet_critical only; test_primary_metric MUST assert exploratory perturbation does NOT change primary_metric. (b) §6.4.1 cached-answer regime — temperature=0 mandatory (enforced at protocol via `ratchet_critical_call`); cache-hit required during primary_metric (cache-miss → HALT, not fresh LLM); cache git-tracked. (c) §6.4 judge split — ratchet pool rejects open-ended by type via `ab_answer_key_validator.py`; open-ended is exploratory-only. **Determinism ratchet test asserts identical primary_metric across two runs of same `(target_version, compiler_sha)`.** This TO is the primary defense against R14.</risk>
  </risks>

  <dependencies>
    <dependency to="COMP_LEARNS.011" status="required">Scorecard, DownstreamAB, Adversarial dataclasses</dependency>
    <dependency to="COMP_LEARNS.014" status="required">Graph + GraphSummary (for conflict_fraction + structural scoring context)</dependency>
    <dependency to="ADVI_49EXEC.003" status="external-gated">anthropic-sdk-deps Lambda layer (AE 0.6 in flight). **Phase 1 `import anthropic` gate.** Non-Anthropic pieces (structural, protocol, MockJudge, cache, selector integration stubs) are unblocked; AnthropicJudge class ships as a stub until SDK lands.</dependency>
    <dependency to="COMP_LEARNS.020" status="preferred-parallel">Selectors — per_selector integration test uses seeded fake selectors if .020 hasn't landed; swap to real selectors when available.</dependency>
  </dependencies>

  <cross_domain_coordination>
    **.015 Phase 1 — Anthropic SDK availability: UNBLOCKED.** `ADVI_49EXEC.003` (anthropic-sdk-deps layer) shipped `c0a00bcc` 2026-04-16 per PRD v3 §11.2. Proceed on AnthropicJudge directly.

    **Capacity flag:** if ~D is saturated on ADVI_ROLLUP (primary COO's lane), reassign to ~B after .013 closes per §16 item 6. COO~Z (owning this project as of 2026-04-20) re-asserts fallback authority — bench is critical path, do not stall.

    **v3 sweep marker (2026-04-20 COO~Z):** this TO was swept from v2→v3 per CTO checklist 2026-04-16 13:59Z, preserved in COO~Z handoff log `org/tier1_exec/2.0.0_SA_COO/logs/2026-04-16/COO_B_comp_learns_v3_sweep_handoff.md`. Deltas applied: ratchet_critical/exploratory scorecard split (§6.1, §6.2), cached-answer regime (§6.4.1) with `CacheMissDuringPrimaryMetric` + warm-up phase separation, JudgeBackend temperature-0 enforcement via `ratchet_critical_call` wrapper, ab_answer_key validator rejecting open-ended in ratchet pool (§6.4), full 9-tuple cache key, R14 risk added.
  </cross_domain_coordination>

  <next>On commit + MCP COMPLETE to 2.0.0_SA_COO~Z: .017 (~C ratchet) is closer to unblocking. Still waits on .016 + .020 + .021.</next>
</task_order>
