<task_order>
  <metadata>
    <id>1.4.0_DS_CompLearns-2026-04-21-comp-learns-026-honest-selector-tie-reporting-and-status</id>
    <issued_by>1.1.0_SA_CTO</issued_by>
    <issued_to>1.4.0_DS_CompLearns</issued_to>
    <date>2026-04-21</date>
    <status>complete</status><!-- commit 53386ec7 — 2026-04-21 -->
    <evidence>
      Shipped: commit 53386ec7 — honest selector tie reporting + full --status (COMP_LEARNS.026).
      Artifacts: comp/bench/scorecard.py (winners_at_best: list[str] + random_unique_win: bool on DownstreamAB; computed in ab.run() alongside existing tied_at_best; serialized with .get() backcompat defaults), comp/loop/ratchet.py (winners_at_best + random_unique_win mirrored into experiment_log extra), comp/loop/render.py (new: render_selector_summary with tie-first rule — winners_at_best shown when tied_at_best=true, random_unique_win flag surfaced; render_status covering champion/verdicts/terminal-phase/last-N-scorecards/selector-tie blocks), comp/loop/runner.py (do_status stub replaced with render_status dispatch; --last N flag default 5 on comp-learns-ratchet CLI), comp/loop/tests/test_selector_tie_reporting.py (9 tests: unique-win, multi-way tie, random-unique-win=True, random-in-tie-not-unique, experiment-log mirror), comp/loop/tests/test_status_render.py (7 tests: status read-only, rendering tie/unique cases, all-six-blocks, no-parallel-state, backward-compat no winners_at_best).
      Validation: AC unique-win path winners_at_best=["selector"], tied_at_best=false PASS. AC multi-way tie winners_at_best sorted alphabetical, tied_at_best=true PASS. AC random-unique-win=True when only random at max lift PASS. AC random-in-tie NOT a unique win (random_unique_win=false when others tie with random) PASS. AC experiment-log mirror extra.winners_at_best == scorecard winners_at_best PASS. AC --status read-only: no file under comp/targets/ modified PASS. AC --status tie rendering shows all tied selectors PASS. AC --status unique rendering shows best_selector PASS. AC --status covers all six blocks (champion/verdicts/terminal-phase/last-N/selector-tie/no-parallel-state) PASS. AC backward-compat: pre-.026 scorecards missing winners_at_best load without error; render_status tolerates empty list PASS. AC pre-commit gate clean PASS. All 403 tests pass.
      Session log: org/tier2_senior/1.4.0_DS_CompLearns/logs/2026-04-21/.
    </evidence>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Phase 2 parallel with .024/.025; completes Phase 2 exit</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_RUNTIME_V1.md §7 (honest selector reporting), §10 (derived status views)</ref>
    <ref type="precedent">comp/bench/ab.py:147-158 — `tied_at_best` already landed; build on it</ref>
    <ref type="runner">comp/bin/comp-learns-ratchet + comp/loop/runner.py (from .023) — `--status` stub lands here</ref>
  </references>

  <objective>
    Stop the selector reporting layer from naming a unique winner when the result is really a tie. Every human-facing summary (including `--status`) must say "tie at best" *before* naming a selector when ties exist. Additionally, promote the `--status` stub from .023 into the full derived-view per PRD §10.

    In scope:
    1. Add `winners_at_best: list[str]` and `random_unique_win: bool` to the downstream_ab scorecard block.
    2. Mirror into experiment_log `extra`.
    3. Keep existing `tied_at_best` and `best_selector` — do not remove.
    4. Add a `render_selector_summary(scorecard) -> str` helper that implements the tie-first rendering rule.
    5. Full `--status` implementation replacing the .023 stub: champion, last N verdicts with compare_key, terminal-condition proximity, cache provenance snapshot, judge_mode + benchmark_honest.

    Out of scope:
    - selector harness redesign (selectors themselves unchanged)
    - dashboard / web UI (no dashboard in v1)
  </objective>

  <scope>
    <files>
      <file action="modify">comp/bench/ab.py (compute winners_at_best + random_unique_win alongside existing tied_at_best)</file>
      <file action="modify">comp/bench/scorecard.py (add fields to downstream_ab block + serializer)</file>
      <file action="modify">comp/loop/ratchet.py (write fields into experiment_log entry extra)</file>
      <file action="modify">comp/loop/runner.py (replace --status stub from .023 with full impl)</file>
      <file action="create">comp/loop/render.py (render_selector_summary + status renderer; pure functions, no IO)</file>
      <file action="create">comp/bench/tests/test_selector_tie_reporting.py</file>
      <file action="create">comp/loop/tests/test_status_render.py</file>
    </files>
  </scope>

  <wire_contract>
    **Computed in `comp/bench/ab.py`** (next to existing `tied_at_best`):
    ```python
    # After selector A/B scoring:
    max_lift = max(s.lift for s in selector_results)
    winners_at_best = sorted([s.name for s in selector_results if s.lift == max_lift])
    tied_at_best = len(winners_at_best) > 1
    random_unique_win = winners_at_best == ["random"]
    # best_selector stays as existing insertion-order pick for backward compat
    ```

    **Scorecard `DownstreamAB` additions** (backward-compatible):
    ```python
    @dataclass
    class DownstreamAB:
        # ... existing ...
        winners_at_best: list[str] = field(default_factory=list)
        random_unique_win: bool = False
        tied_at_best: bool = False  # already landed — kept
    ```
    Serializer emits all three; loader tolerates absence (defaults).

    **Experiment-log mirror** (entry `extra`):
    ```json
    "extra": {
      ...,
      "best_selector": "centrality",
      "winners_at_best": ["centrality", "keyword"],
      "tied_at_best": true,
      "random_unique_win": false,
      ...
    }
    ```

    **Rendering rule** (`comp/loop/render.py`):
    ```python
    def render_selector_summary(dab: DownstreamAB) -> str:
        if dab.tied_at_best:
            winners = ", ".join(dab.winners_at_best)
            return f"tie at best ({len(dab.winners_at_best)}): {winners}"
        line = f"best_selector={dab.winners_at_best[0] if dab.winners_at_best else dab.best_selector}"
        if dab.random_unique_win:
            line += "  [AUDIT: random_unique_win — investigate selector health]"
        return line
    ```
    Rule: any human-facing summary MUST call this helper rather than formatting `best_selector` directly. Grep in runner + status code post-TO should find zero `f"best_selector={...}"` strings outside `render.py`.

    **Full `--status` output** (replaces .023 stub):
    ```
    [comp-learns-ratchet httpx --status]

    champion:
      compiler_sha=13254d0  primary_metric=1.2439  structural_f1=0.5743  compiler_loc=34
      judge_mode=real  benchmark_honest=true  judge_model_id=claude-sonnet-4-6

    last 5 verdicts:
      iter=12  kept       compare_key=primary_metric  Δ+0.0440  sha=27b8233
      iter=11  tied       compare_key=compiler_loc    Δ 0      sha=6c58f0e
      iter=10  discarded  compare_key=primary_metric  Δ-0.0810  sha=e8f2c50
      iter= 9  kept       compare_key=structural_f1   Δ 0      sha=909ea79f
      iter= 8  tied       compare_key=compiler_loc    Δ 0      sha=13254d0

    terminal proximity:
      iters since last KEEP: 1   (plateau-k=5 → 4 to go)
      budget remaining:      11h 17m
      max-iter remaining:    8

    cache provenance (latest run):
      compiler_sha=27b8233  target_version=909ea79f  judge=real
      hits/misses by selector: centrality 42/0  keyword 39/0  random 12/0

    selectors (latest run):
      tie at best (2): centrality, keyword
    ```

    **Derivation rules** (all outputs come from artifacts):
    - champion block: `comp/targets/<target>/champion.json`
    - verdicts: last N entries from `experiment_log.jsonl` (N default 5, configurable `--last N` flag)
    - terminal proximity: computed from runner config (if runner state is accessible — when invoked standalone without a running runner, show "no active runner; max-iter/budget N/A") + experiment log scan
    - cache provenance: latest `scorecards/*.json` by mtime
    - selectors: same latest scorecard, passed through `render_selector_summary`

    **--status never writes**. Read-only.
  </wire_contract>

  <acceptance_criteria>
    1. **Unique-win path**: selector results where one selector strictly beats others → `winners_at_best=["centrality"]`, `tied_at_best=False`, `random_unique_win=False`; `render_selector_summary` returns `"best_selector=centrality"`.
    2. **Multi-way tie**: two selectors tie at max → `winners_at_best=["centrality","keyword"]` (sorted), `tied_at_best=True`; render returns `"tie at best (2): centrality, keyword"`.
    3. **Random unique win (audit flag)**: only `random` at max → `random_unique_win=True`; render returns `"best_selector=random  [AUDIT: random_unique_win — investigate selector health]"`.
    4. **Random in tie is NOT a unique win**: `winners_at_best=["centrality","random"]` → `random_unique_win=False`.
    5. **Experiment-log mirror**: after a mock run, entry `extra.winners_at_best` equals scorecard's `winners_at_best`, and `tied_at_best` matches.
    6. **Status read-only**: `comp-learns-ratchet httpx --status` does not modify any file under `comp/targets/httpx/` (diff before/after is empty).
    7. **Status rendering — tie case**: construct a test fixture with latest scorecard having `tied_at_best=True`; `--status` output contains `"tie at best ("` line BEFORE any `"best_selector="` line (or omits `best_selector=` entirely).
    8. **Status rendering — unique case**: fixture with unique winner; `--status` output contains `"best_selector=<name>"` without a `"tie at best"` prefix.
    9. **Status covers all six blocks**: parseable output has sections for champion / verdicts / terminal proximity / cache provenance / selectors (5 of 6 always visible; judge_mode inline in champion).
    10. **No parallel state**: grep in runner.py + render.py post-TO finds zero references to a `state.json`-style file; all reads are from `champion.json` / `experiment_log.jsonl` / `scorecards/*.json`.
    11. **Backward-compat**: scorecards written pre-.026 (no `winners_at_best`) load without error; `render_selector_summary` falls through to `best_selector` name in that case (no crash).
    12. **Existing tests green**: `pytest comp/ -q` passes.
    13. **Pre-commit gate**: `.tools/ds-commit-gate.sh` passes on every `.py` edit.
  </acceptance_criteria>

  <dependencies>
    - **Blocked by .023** (runner + --status stub)
    - **Cooperates with .024** (judge_mode/benchmark_honest display in status) and **.025** (cache_provenance + compare_key display in status). Status renderer must tolerate absence of any of those fields (older runs) and show a clean fallback.
  </dependencies>

  <operational_notes>
    - Do NOT change `best_selector` semantics. Some existing tests and tooling read it; keep it as the insertion-order pick it already is. The tie-rendering rule handles the honesty problem without breaking the existing field.
    - `winners_at_best` is sorted alphabetically for deterministic output. Rationale: downstream diff tools hate non-deterministic list ordering.
    - `render_selector_summary` is the chokepoint. Any future dashboard or notification system must go through it.
  </operational_notes>

  <closeout>
    - commit with `--author="1.4.0_DS_CompLearns <1.4.0_DS_CompLearns@opal.agent>"`
    - MCP COMPLETE to 1.1.0_SA_CTO + 2.1.0_SA_COO with commit sha + AC checklist
    - flip TO status to `complete` with commit ref
  </closeout>
</task_order>
