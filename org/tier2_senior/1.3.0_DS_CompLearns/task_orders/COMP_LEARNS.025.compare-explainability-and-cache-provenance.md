<task_order>
  <metadata>
    <id>1.3.0_DS_CompLearns-2026-04-21-comp-learns-025-compare-explainability-and-cache-provenance</id>
    <issued_by>1.1.0_SA_CTO</issued_by>
    <issued_to>1.3.0_DS_CompLearns</issued_to>
    <date>2026-04-21</date>
    <status>complete</status><!-- e7a12a12 (cache.py/tests/log); core scorecard/ratchet/ab changes co-landed in 53386ec7 by parallel .026 agent -->
    <evidence>
      Shipped: commit e7a12a12 (primary: cache.py, tests, session log) + co-landed scorecard/ratchet/ab changes in 53386ec7 by 1.4.0_DS parallel agent.
      Artifacts: comp/bench/scorecard.py (CacheProvenance dataclass with compiler_sha/target_version/judge_model_id/warm_up_entries_written/hits_by_selector/misses_by_selector; scorecard_to_dict/from_dict round-trip; loader tolerates null), comp/bench/cache.py (per-selector hit/miss counters; hits_by_selector + misses_by_selector properties; selector_name threaded through get() + require_hit()), comp/loop/ratchet.py (compare_key_for() module-level fn making every KEEP/DISCARD/TIED/FORKED verdict reconstructable from experiment_log extra alone; _compiler_loc() refined to non-empty non-comment lines only; 9 new extra fields: compare_key, candidate/champion_primary_metric/structural_f1/compiler_loc before/after, cache_hits, cache_misses), comp/bench/__init__.py (exports), plus tests.
      Tests: 22 new tests; 198 total passing. Test files cover compare_key_for() four cases (primary_metric KEEP, structural_f1 KEEP, compiler_loc KEEP, FORKED), snapshot values, no-champion case, refined LoC (non-empty non-comment lines), cache_provenance round-trip, non-breaking loader for pre-.025 scorecards.
      Validation: AC compare_key correctness — four cases (primary_metric KEEP, structural_f1 KEEP, compiler_loc KEEP, SelectorGame FORKED) PASS. AC snapshot values match champion.json["primary_metric"] at entry time PASS. AC no-champion case produces all champion_*_before=null PASS. AC refined LoC counts non-empty non-comment lines only PASS. AC loc_delta uses refined count PASS. AC cache_provenance populated after mock run (hits_by_selector + misses_by_selector) PASS. AC cache-hits mirror experiment_log entry extra.cache_hits == sum(cache_provenance.hits_by_selector.values()) PASS. AC primary-metric phase zero misses (cache-hit-only re-run path, misses==0) PASS. AC non-breaking loader: pre-.025 scorecards missing cache_provenance load without error PASS. AC existing tests 198/198 green PASS.
      Session log: org/tier2_senior/1.3.0_DS_CompLearns/logs/2026-04-21/.
    </evidence>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Phase 2 parallel with .024/.026; required for .027</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_RUNTIME_V1.md §6 (compare explainability), §8 (cache integrity)</ref>
    <ref type="engine">comp/loop/ratchet.py — compare-and-keep logic (lines ~340+, champion update block)</ref>
    <ref type="schema">comp/bench/scorecard.py — where to attach cache_provenance block</ref>
  </references>

  <objective>
    Make every KEEP / TIED / DISCARD / FORKED verdict reconstructable from artifacts alone, and make the cache inspectable enough to tell whether a benchmark result was driven by warm-up, cache reuse, or actual model variance.

    In scope:
    1. Add compare-explainability fields to `experiment_log` entry `extra`: `compare_key`, `candidate_primary_metric`, `champion_primary_metric_before`, `candidate_structural_f1`, `champion_structural_f1_before`, `candidate_compiler_loc`, `champion_compiler_loc_before`.
    2. Refine `compiler_loc` definition: non-empty, non-comment Python lines in the authoritative compiler surface. Replace raw-line-count implementation.
    3. Add `cache_provenance` block to scorecard summary: `compiler_sha`, `target_version`, `judge_model_id`, `warm_up_entries_written`, `hits_by_selector`, `misses_by_selector`.
    4. Mirror `cache_hits` + `cache_misses` scalars into experiment_log `extra` for log-only audits.

    Out of scope:
    - `judge_mode`/`benchmark_honest`/`schema_version` (.024)
    - `winners_at_best` / selector tie rendering (.026)
  </objective>

  <scope>
    <files>
      <file action="modify">comp/loop/ratchet.py</file>
      <file action="modify">comp/bench/scorecard.py</file>
      <file action="modify">comp/bench/ab.py (expose hits_by_selector / misses_by_selector from warm_up_cache + ab_run)</file>
      <file action="modify">comp/bench/cache.py (counter instrumentation — no semantic change)</file>
      <file action="create">comp/loop/tests/test_compare_explainability.py</file>
      <file action="create">comp/bench/tests/test_cache_provenance.py</file>
      <file action="create">comp/bench/tests/test_compiler_loc_refined.py</file>
    </files>
  </scope>

  <wire_contract>
    **Compare explainability fields** — go into `experiment_log` entry `extra` (not top-level; keeps root schema small):
    ```json
    "extra": {
      "compare_key": "primary_metric",  // "primary_metric" | "structural_f1" | "compiler_loc" | "fork"
      "candidate_primary_metric": 1.2439,
      "champion_primary_metric_before": 1.2000,
      "candidate_structural_f1": 0.5743,
      "champion_structural_f1_before": 0.5600,
      "candidate_compiler_loc": 34,
      "champion_compiler_loc_before": 38,
      ...existing extra keys...
    }
    ```

    **Snapshot-timing rule**: `*_before` values are the champion's state *as read at the start of the iteration's compare* (i.e. from `champion.json` immediately before the verdict is computed). If there is no champion yet, all `champion_*_before` fields are `null` (JSON) / `None` (Python).

    **compare_key derivation rule** (matches existing verdict logic in ratchet.py, made explicit):
    ```python
    def compare_key_for(verdict: Verdict, candidate: Scorecard, champion: dict | None) -> str:
        if verdict == Verdict.FORKED:
            return "fork"
        if champion is None:
            return "primary_metric"  # first entry always keeps
        cand_pm = candidate.primary_metric
        champ_pm = champion["primary_metric"]
        if cand_pm != champ_pm:
            return "primary_metric"
        cand_f1 = candidate.ratchet_critical.structural.f1
        champ_f1 = champion.get("structural_f1", 0.0)
        if cand_f1 != champ_f1:
            return "structural_f1"
        return "compiler_loc"  # final tiebreak; may still tie → TIED verdict
    ```
    Place in `comp/loop/ratchet.py` near `_compare_and_update_champion` helper. Unit-tested directly.

    **Refined `compiler_loc` definition**:
    ```python
    def _compiler_loc(compiler_py_path: Optional[Path]) -> int:
        """Non-empty, non-comment Python lines in the authoritative compiler surface.
        Pure stdlib: no AST parse, no complexity score. Tiebreak input only."""
        if compiler_py_path is None or not compiler_py_path.exists():
            return 0
        count = 0
        for raw in compiler_py_path.read_text(encoding="utf-8").splitlines():
            stripped = raw.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                continue
            count += 1
        return count
    ```
    Replaces existing implementation at `ratchet.py:102`. Docstring-only lines (inside `"""..."""`) count as code — the simpler heuristic is fine for tiebreak; we are not building a maintainability index (PRD §6).

    **cache_provenance block** on scorecard:
    ```python
    @dataclass
    class CacheProvenance:
        compiler_sha: str
        target_version: str
        judge_model_id: str
        warm_up_entries_written: int
        hits_by_selector: dict[str, int]
        misses_by_selector: dict[str, int]

    @dataclass
    class Scorecard:
        # ... existing ...
        cache_provenance: CacheProvenance | None = None  # optional until all emission sites populate
    ```
    Serialize as nested JSON object. Loader tolerates `null` / absent → `None`.

    **Experiment-log mirror** (in `extra`):
    ```json
    "extra": {
      ...,
      "cache_hits": 123,
      "cache_misses": 0
    }
    ```
    Sums across selectors; individual-selector breakdown stays on the scorecard only.

    **ABCache instrumentation** (`comp/bench/cache.py`):
    - increment a per-selector hit counter on cache-hit read
    - increment a per-selector miss counter on cache-miss (which should happen only in warm-up, never in primary-metric phase)
    - expose `ABCache.hits_by_selector -> dict[str, int]` and `.misses_by_selector -> dict[str, int]`
    - zero the counters when `ABCache` is instantiated (no cross-iteration leakage — each iterate() constructs its own)
  </wire_contract>

  <acceptance_criteria>
    1. **compare_key correctness — four cases**:
       - candidate beats champion on primary_metric → `compare_key="primary_metric"`, verdict KEEP
       - candidate ties on primary_metric, beats on structural_f1 → `compare_key="structural_f1"`, verdict KEEP
       - candidate ties on both, beats on compiler_loc (lower) → `compare_key="compiler_loc"`, verdict KEEP
       - SelectorGame detected → `compare_key="fork"`, verdict FORKED
       Each case is a unit test in `test_compare_explainability.py`.
    2. **Snapshot values match**: `champion_primary_metric_before` in the new entry equals `champion.json["primary_metric"]` as it was before the iteration wrote a new champion. Test by asserting against a pre-read champion dict.
    3. **No-champion case**: first iteration on an empty target produces entry with all `champion_*_before` fields null; `compare_key="primary_metric"`.
    4. **Refined LoC**: test fixture compiler.py with mix of blank lines, comment-only lines, and code lines; `_compiler_loc` returns only the code-line count. Edge case: file with only comments returns 0.
    5. **LoC in experiment log**: `loc_delta` field continues to work; uses the refined count. Regression check: running an existing httpx compiler post-refinement may produce a different absolute `compiler_loc` than pre-TO — that is expected, but subsequent iterations on the same compiler must produce stable values.
    6. **Cache provenance populated**: run `comp-learns-ratchet httpx --judge mock --max-iter 1`; resulting scorecard JSON has a non-null `cache_provenance` block with all six fields populated. `hits_by_selector` keys match the active selector set.
    7. **Cache-hits mirror**: experiment_log entry `extra.cache_hits` equals `sum(cache_provenance.hits_by_selector.values())`. Same for misses.
    8. **Primary-metric phase zero misses**: in the cache-hit-only re-run path (§11 run #2 regime), `misses_by_selector` is all zeros across selectors. Test with a fixture where warm-up has already populated cache.
    9. **Non-breaking loader**: scorecards written pre-TO (missing `cache_provenance`) load without error; the loaded dataclass has `cache_provenance=None`.
    10. **Existing tests green**: `pytest comp/loop/tests/ comp/bench/tests/ -q` passes.
    11. **Pre-commit gate**: `.tools/ds-commit-gate.sh` passes on every `.py` edit.
  </acceptance_criteria>

  <dependencies>
    - **Blocked by .023** (needs runner surface to call through).
    - Parallel with .024 and .026. If .024 merges first, `extra` dict may already have `judge_model_id` key — do not conflict with it.
  </dependencies>

  <operational_notes>
    - Do NOT backfill compare explainability into existing experiment_log entries — they stay as-is; the loader (.024) returns them normalized but without compare fields. Downstream readers must check for field presence.
    - The LoC refinement changes the absolute number slightly. This is acceptable: ratchet compare uses the value at decision time, not historical consistency.
    - Keep the cache_provenance JSON compact — no pretty-printing that explodes scorecard file size.
  </operational_notes>

  <closeout>
    - commit with `--author="1.3.0_DS_CompLearns <1.3.0_DS_CompLearns@opal.agent>"`
    - MCP COMPLETE to 1.1.0_SA_CTO + 2.1.0_SA_COO with commit sha + AC checklist
    - flip TO status to `complete` with commit ref
  </closeout>
</task_order>
