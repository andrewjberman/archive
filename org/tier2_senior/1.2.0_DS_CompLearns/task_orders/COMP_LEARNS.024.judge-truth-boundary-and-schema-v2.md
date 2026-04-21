<task_order>
  <metadata>
    <id>1.2.0_DS_CompLearns-2026-04-21-comp-learns-024-judge-truth-boundary-and-schema-v2</id>
    <issued_by>1.1.0_SA_CTO</issued_by>
    <issued_to>1.2.0_DS_CompLearns</issued_to>
    <date>2026-04-21</date>
    <status>complete</status><!-- commit 506a9466 — 2026-04-21 -->
    <evidence>
      Shipped: commit 506a9466 — judge truth boundary + schema v2 (COMP_LEARNS.024).
      Artifacts: comp/bench/scorecard.py (judge_mode + benchmark_honest fields, serialized, excluded from __eq__), comp/loop/experiment_log.py (schema_version/judge_mode/benchmark_honest on ExperimentEntry; load_entries() v1-normalizer; derive_benchmark_honest(); strict-mode check in append()), comp/loop/ratchet.py (judge_mode + benchmark_honest kwargs on iterate(); entry_schema_version logic), comp/bench/judges/anthropic.py (credentials_resolved field set from ANTHROPIC_API_KEY at __post_init__).
      Tests: comp/bench/tests/test_scorecard_judge_mode.py (9 tests: round-trip mock/real, absent field defaults, __eq__ exclusion, credentials_resolved via monkeypatch), comp/loop/tests/test_experiment_log_schema_v2.py (13 tests: round-trip, v1 normalization, strict-mode failure x2, derive_benchmark_honest x5, mixed v1+v2), comp/bench/tests/test_scorecard_roundtrip.py (3 new assertions: round-trip preserves judge_mode/benchmark_honest, absent fields yield defaults). 30 new tests; 125 total passing.
      Validation: AC#1 scorecard round-trip PASS. AC#2 experiment-log round-trip schema_version=2 PASS. AC#3 v1 entry tolerance (normalized schema_version=1, judge_mode="", benchmark_honest=False) PASS. AC#4 strict-mode failure raises ValueError mentioning "judge_mode" PASS. AC#5 mock run emits benchmark_honest=false via direct iterate() with judge_mode="mock" PASS. AC#6 real run guard test exists with @pytest.mark.skipif (no credentials in CI — by design). AC#7 credentials_resolved set from env var PASS. AC#8 __eq__ unchanged — scorecards differing only in judge_mode are == PASS. AC#9 only load_entries() branches on schema_version (grep confirmed). AC#10 125/125 existing tests green. AC#11 pre-commit gate clean on all .py edits.
      Runner plumbing: comp/loop/runner.py .023 call to iterate() updated to pass judge_mode=cfg.judge_mode + benchmark_honest=derive_benchmark_honest(cfg.judge_mode, judge).
      Session log: org/tier2_senior/1.2.0_DS_CompLearns/logs/2026-04-21/comp_learns_024_judge_truth_boundary_shipped.md.
    </evidence>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Phase 2 parallel with .025/.026; required for .027</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_RUNTIME_V1.md §5 (judge truth boundary), §9 (schema versioning)</ref>
    <ref type="schema">comp/bench/scorecard.py::Scorecard (already has `judge_model_id` since validator #2)</ref>
    <ref type="schema">comp/loop/experiment_log.py::ExperimentEntry (add `schema_version`, `judge_mode`, `benchmark_honest`)</ref>
  </references>

  <objective>
    Make judge identity operationally meaningful and versioned. Today `judge_model_id` exists on scorecards but whether a run is benchmark-significant is inferred from model-ID strings. This TO makes `benchmark_honest` the single filter between demo and evidence, and stamps every new experiment-log entry with `schema_version: 2` so pre/post-tightening entries stop looking interchangeable.

    In scope:
    1. Add `judge_mode: "mock"|"real"` and `benchmark_honest: bool` to `Scorecard` and to experiment-log entries.
    2. Propagate from runner (.023) → iterate() → scorecard + experiment log.
    3. Add `schema_version: 2` to new experiment-log entries.
    4. Add loader `load_entries(path) -> list[dict]` that normalizes v1 entries into v2 shape (fill defaults; never branch on version downstream).
    5. Strict-mode check: any v2 entry missing a v2-mandatory field fails validation — runner fails closed before writing.

    Out of scope:
    - compare explainability fields (.025)
    - selector tie reporting (.026)
    - cache_provenance block (.025)
  </objective>

  <scope>
    <files>
      <file action="modify">comp/bench/scorecard.py</file>
      <file action="modify">comp/loop/experiment_log.py</file>
      <file action="modify">comp/loop/ratchet.py (plumb judge_mode + benchmark_honest through iterate signature + scorecard/experiment-log writes)</file>
      <file action="modify">comp/loop/runner.py (.023 output: pass judge_mode + benchmark_honest to iterate)</file>
      <file action="create">comp/loop/tests/test_experiment_log_schema_v2.py</file>
      <file action="create">comp/bench/tests/test_scorecard_judge_mode.py</file>
      <file action="modify">comp/bench/tests/test_scorecard_roundtrip.py (add round-trip assertions for new fields)</file>
    </files>
  </scope>

  <wire_contract>
    **Scorecard fields** (additive — do NOT remove anything):
    ```python
    @dataclass
    class Scorecard:
        # ... existing fields ...
        judge_mode: str = ""          # "mock" | "real" — empty default only for backcompat loads
        benchmark_honest: bool = False
    ```

    Serialization: include both fields in `scorecard_to_dict`. Loader tolerates absence → defaults above.

    `__eq__` rule: `judge_mode` and `benchmark_honest` are **NOT** in `__eq__` — same `(target_version, compiler_sha, ratchet_critical, primary_metric)` is still structurally equal regardless of run class. Rationale matches existing `judge_model_id` exclusion (scorecard.py:135).

    **Experiment-log entry fields** (additive):
    ```python
    @dataclass
    class ExperimentEntry:
        # ... existing fields ...
        schema_version: int = 2       # NEW entries always 2; v1 entries have no field (loader fills 1)
        judge_mode: str = ""
        benchmark_honest: bool = False
    ```

    Written JSON shape:
    ```json
    {
      "schema_version": 2,
      "iter": 9,
      "compiler_sha": "13254d0",
      "primary_metric": 1.2439,
      "judge_mode": "real",
      "benchmark_honest": true,
      "timestamp": "2026-04-22T14:00:00Z",
      "verdict": "kept",
      "delta": 0.0,
      "loc_delta": 0,
      "notes": "...",
      "extra": { "judge_model_id": "claude-sonnet-4-6", ... }
    }
    ```

    **benchmark_honest derivation rule** (the only place this is computed):
    ```python
    def derive_benchmark_honest(judge_mode: str, judge_instance) -> bool:
        if judge_mode != "real":
            return False
        # real-judge path requires the judge to advertise credential resolution
        return getattr(judge_instance, "credentials_resolved", False) is True
    ```
    `AnthropicJudge` must expose `credentials_resolved: bool` (true after env-var/secret check at init). `MockJudge` does not set the attr → `getattr` default false → `benchmark_honest=false`. This TO adds the attribute on `AnthropicJudge` if missing.

    **Loader contract** (`comp/loop/experiment_log.py`):
    ```python
    def load_entries(path: Path) -> list[dict]:
        """Load JSONL experiment log, normalizing v1 entries into v2 shape.
        Downstream readers consume the normalized dicts and never branch on schema_version."""
        out = []
        for line in path.read_text().splitlines():
            if not line.strip(): continue
            d = json.loads(line)
            if "schema_version" not in d:
                # v1: fill v2 defaults
                d["schema_version"] = 1
                d.setdefault("judge_mode", "")
                d.setdefault("benchmark_honest", False)
                # (compare_key + before-snapshots come from .025; keep absent here)
            out.append(d)
        return out
    ```

    **Strict-mode write check** (new entries only):
    ```python
    def append(path, entry: ExperimentEntry) -> None:
        if entry.schema_version == 2:
            if entry.judge_mode not in ("mock", "real"):
                raise ValueError(f"v2 entry requires judge_mode mock|real, got {entry.judge_mode!r}")
            # benchmark_honest is bool — type-checked by dataclass
        # ... existing write logic ...
    ```

    **iterate() signature change**:
    Add parameters `judge_mode: str` and `benchmark_honest: bool` to `iterate()`. Both flow through to scorecard + experiment entry writes. Parameters are keyword-only (placement after existing kwargs in ratchet.py:213).

    Runner (.023 landed) must pass `judge_mode=cfg.judge_mode` and `benchmark_honest=derive_benchmark_honest(...)` on every iterate() call.
  </wire_contract>

  <acceptance_criteria>
    1. **Scorecard round-trip**: serialize → deserialize preserves `judge_mode` + `benchmark_honest` exactly. Loaders of pre-.024 scorecard JSON (absent fields) yield defaults `""` / `False`.
    2. **Experiment-log round-trip**: new entry written with `schema_version=2` loads via `load_entries` with all fields intact.
    3. **v1 entry tolerance**: hand-crafted v1 JSONL (lacking schema_version, judge_mode, benchmark_honest) loads successfully; normalized entries have `schema_version=1`, `judge_mode=""`, `benchmark_honest=False`.
    4. **Strict-mode failure**: attempting to `append()` a `schema_version=2` entry with `judge_mode=""` raises `ValueError`; test asserts the exception message mentions "judge_mode".
    5. **Mock run emits honest=false**: run `comp-learns-ratchet httpx --judge mock --max-iter 1` (requires .023 landed — coordinate). Resulting experiment-log entry has `judge_mode="mock"`, `benchmark_honest=false`, `schema_version=2`. Scorecard JSON on disk has matching fields.
    6. **Real run emits honest=true** (only assertable once credentials exist; guard test with `@pytest.mark.skipif(not credentials_available)`): entry has `judge_mode="real"`, `benchmark_honest=true`.
    7. **AnthropicJudge credentials_resolved**: `comp/bench/judges/anthropic.py` exposes `credentials_resolved: bool` set during `__init__` based on API key presence. Test with a stubbed key → True; with env var unset → False.
    8. **__eq__ unchanged**: two scorecards differing only in `judge_mode` are still `==`. Round-trip test covers this.
    9. **Downstream readers normalized**: grep `schema_version` in repo post-TO; only `experiment_log.py::load_entries` branches on it. `ratchet.py`, runner, status helpers never check schema_version directly.
    10. **Existing tests green**: `pytest comp/loop/tests/ comp/bench/tests/ -q` passes.
    11. **Pre-commit gate**: `.tools/ds-commit-gate.sh` passes on every `.py` edit (CLAUDE.md rule 14).
  </acceptance_criteria>

  <dependencies>
    - **Blocked by .023** (needs the runner signature to plumb through). Can begin implementation on a branch before .023 lands if using `iterate()` directly in tests.
  </dependencies>

  <operational_notes>
    - Do NOT migrate existing v1 entries in `comp/targets/httpx/experiment_log.jsonl`. They stay as-is; loader handles them.
    - `judge_mode` empty string is reserved for "unknown / pre-v2". Do not use it as a third category.
    - Any doc that references "how to tell if a run is real" after this TO must point readers at `benchmark_honest` — not at model ID strings.
  </operational_notes>

  <closeout>
    On completion:
    - commit with `--author="1.2.0_DS_CompLearns <1.2.0_DS_CompLearns@opal.agent>"`
    - MCP COMPLETE to 1.1.0_SA_CTO + 2.1.0_SA_COO with commit sha + AC checklist
    - flip TO status to `complete` with commit ref
  </closeout>
</task_order>
