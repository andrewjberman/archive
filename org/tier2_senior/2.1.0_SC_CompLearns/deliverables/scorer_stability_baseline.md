# Scorer Stability Baseline Report — httpx / post-.027b runtime

**Role:** 2.1.0_SC_CompLearns  
**Date:** 2026-04-21  
**Target:** httpx (encode/httpx)  
**Target version:** `909ea79f63e9c016e457693b01eb1d1bdc8a7f60fb6fdb9430235e0810e39f0b`  
**Champion compiler_sha:** `3fb8b69`  
**Champion primary_metric:** `0.06635351328309276`  
**Judge regime:** real (`claude-sonnet-4-6`, `benchmark_honest=true`)  
**Runtime commit (Phase 3 close):** `d047496a` (tag: `comp-learns-phase3-closed`)  
**RUNTIME_V1.md reference commit:** landed before the proving sequence; tag `comp-learns-v1-proving-start` at `d27790c1`  
**Scorecard path:** `comp/targets/httpx/scorecards/3fb8b69_909ea79f.json`  
**Baseline produced by:** fresh read of artifacts, commits, and source; no `comp/` edits made

---

## §1 Truth Surface

**Evidence:**
- Target pinned: encode/httpx commit `26d48e0634e6ee9cdc0533996db289ce4b430177` (tag `0.28.1`), per `comp/targets/httpx/SURFACE_INVENTORY.md` and `repo_pin.txt`.
- Gold artifacts frozen in `comp/targets/httpx/gold/`: `imports_gold.jsonl`, `ab_questions.yaml`, `ab_answer_key.yaml`, `GOLD_SURVEY.md`.
- `target_version.txt` records: `sha256=909ea79f63e9...` covering `imports_gold.jsonl + ab_questions.yaml + ab_answer_key.yaml + httpx_source_tree(_repo/httpx/**/*.py)`.
- `compute_target_version()` in `comp/bench/cache.py:234` hashes gold files + source tree into the `target_version` token. Any gold or source change bumps this hash and orphans prior cache entries.
- All 4 Option A+ scorecards carry identical `target_version: 909ea79f...` — confirms inputs were frozen across the proving sequence.

**Verdict: PASS.** Target pinned. Gold artifacts frozen and versioned. Single `target_version` token gates cache invalidation.

---

## §2 Score Identity

**Evidence:**
- `Scorecard` dataclass (`comp/bench/scorecard.py:134`) carries: `target_version`, `compiler_sha`, `judge_mode`, `judge_model_id`, `benchmark_honest`, `compiler_loc`, `cache_provenance`.
- `cache_provenance` (`CacheProvenance` at line 116) carries: `compiler_sha`, `target_version`, `judge_model_id`, `warm_up_entries_written`, `hits_by_selector`, `misses_by_selector`.
- All 4 Option A+ experiment_log entries carry: `schema_version=2`, `judge_mode=real`, `benchmark_honest=true`, `judge_model_id=claude-sonnet-4-6` in `extra`.
- Champion scorecard `3fb8b69_909ea79f.json` confirmed to carry all identity fields.
- **CAVEAT:** `champion.json` does NOT carry `judge_mode` or `benchmark_honest` fields. Current contents: `compiler_sha`, `primary_metric`, `structural_f1`, `compiler_loc`, `scorecard_path`. The champion state can be corroborated via `scorecard_path` pointer to the real-judge scorecard, but the champion file itself has no structural regime guard. Adding `champion.judge_mode` is a v1.1 parking-lot item (see §7).

**Verdict: PASS with caveat.** Scorecards and log entries carry complete score identity. Champion.json lacks judge_mode — a v1.1 item, not blocking because champion was established under real-judge scoring and the scorecard_path is traceable.

---

## §3 Deterministic Core

**Evidence:**
- Structural metrics: `score_against_gold()` in `comp/bench/structural.py` (SHA-256 of frozen gold, AST-based parse) — no wall-clock, no RNG, fully deterministic.
- Primary metric: `comp/bench/primary.py:30` formula `ab_lift * (1 + 0.3 * token_reduction) * mutation_stability * (1 - conflict_penalty)` — deterministic given deterministic inputs.
- Mutation runs: seeded via `per_mutation_seed` dict keys (seed tuples explicit in scorecard).
- Cache-bound scoring: all primary_metric runs go through `ABCache.require_hit()`, which raises on miss rather than falling through to a live LLM call. No fresh non-deterministic calls during primary_metric phase.
- `emitted_at` (wall-clock) explicitly excluded from `Scorecard.__eq__` (`scorecard.py:157`).
- **Proven:** Runs A2 (sha=5db71c6) and A4 (sha=92f5e4c) used different git SHAs but identical `compiler.py` content. Both produced `primary_metric=0.06635351328309276` (bit-exact) with `cache_hits=114`, `cache_misses=0`. Scores are git-sha-independent when compiler content is identical.

**Verdict: PASS.** Deterministic core confirmed by end-to-end proof (A2 vs A4). Time, RNG, and UUIDs are excluded from score-driving paths.

---

## §4 Model-Mediated Scoring

**Evidence:**
- Temperature fixed: `make_cache_key()` in `comp/bench/cache.py:53` appends literal `|temperature=0` to the 9-tuple SHA-256. Any caller that deviates from temperature=0 generates a different key and gets a cache miss.
- Model version fixed: `model_id` and `model_version` are inputs 6 and 7 of the 9-tuple. Swapping model invalidates the cache.
- Selected context identity fixed: `selector_hash`, `selector_version`, `selected_context_token_count` are inputs 4, 5, 8 of the 9-tuple.
- Cache-bound primary_metric: `ABCache.require_hit()` (`comp/bench/cache.py:131`) raises `CacheMissDuringPrimaryMetric` on cache miss. The error message explicitly states "Do NOT fall through to a fresh LLM call — that reintroduces R14 judge drift." Bench halts on miss.
- Mock vs real: `judge_mode` and `benchmark_honest` recorded in every schema_version=2 entry and every scorecard. `_GoldAwareMockJudge` has `model_id="gold-aware-mock"` — clearly distinguishable from real judge.
- All 4 Option A+ runs: `judge_mode=real`, `benchmark_honest=true`, `judge_model_id=claude-sonnet-4-6` in both scorecards and experiment_log entries.

**Verdict: PASS.** Temperature fixed in cache key. Model version fixed in cache key. Primary metric is cache-only. Mock vs real explicitly labeled on every record.

---

## §5 Selector Integrity

**Evidence:**
- Three selectors: `keyword`, `random`, `centrality`. Each has a `version` field used in cache keying (via `selector_version` input to `make_cache_key()`).
- Selection identity: `selector_hash` (computed from selector name, version, selected nodes+edges) is input 4 of the 9-tuple cache key (`comp/bench/ab.py:165`). Selection context is cache-invalidation-relevant.
- Tie representation: `tied_at_best` (bool, True when >=2 selectors share max lift), `winners_at_best` (sorted list of tied selectors), added in `.026` (`scorecard.py:58`).
- Deterministic tie-break: `sorted(per_selector.items(), key=lambda kv: (-kv[1].lift, kv[0]))` in `comp/bench/ab.py:150`. Alphabetical secondary sort: centrality < keyword < random. Prevents insertion-order wins.
- `random_unique_win` flag: `True` only when exactly one selector is at max lift AND that selector is `random`. Guards against degenerate eval where random outperforms structured selectors.
- Selector game detection: `check_selector_game()` imported and called in `ratchet.py:372`. Raises `SelectorGameDetected` if random strictly outperforms structured by >0.1, forcing `Verdict.FORKED`.
- **All 4 Option A+ runs:** `tied_at_best=true`, `random_unique_win=false`. Winners: `["keyword","random"]` (A1/A2/A4), `["centrality","keyword","random"]` (A3, zero-output floor). No selector gaming detected.

**Verdict: PASS.** Selectors versioned. Selection identity in cache key. Ties represented honestly. Random-win guard active.

---

## §6 Formula Simplicity

**Evidence:**
- Formula (`comp/bench/primary.py:30`): `pm = ab_lift * (1 + 0.3 * token_reduction) * mutation_stability * (1 - conflict_penalty)`
  - `ab_lift` = best selector's answer-question lift (fraction correct on ratchet_critical pool)
  - `token_reduction` = best selector's `token_reduction_pct` (fraction of max-budget tokens saved)
  - `mutation_stability` = `MutationStabilityReport.aggregate` (0..1)
  - `conflict_penalty` = `min(1.0, conflict_fraction)` (0..1)
  - `alpha = 0.3` (hardcoded default)
- Range is [0.0, 1.3] at alpha=0.3 — NOT capped at 1.0 by design (token efficiency bonus can push past 1.0). Documented in primary.py docstring. Reviewed per DS Flag 1, CTO accepted doc-only resolution.
- **Verification:** champion 3fb8b69 scorecard: `ab_lift=0.05263`, `token_reduction=0.8824` (keyword), `mutation_stability=0.9968`, `conflict_fraction=0.0` → `base = 0.05263 * 1.2647 = 0.06657`, `pm = 0.06657 * 0.9968 = 0.06635`. Matches stored `primary_metric=0.06635351328309276`.
- Each component independently inspectable: structural_f1 is a separate field, best_lift is in downstream_ab, mutation_stability is in mutation_stability.aggregate.
- Tiebreakers explicit: §6.1 v3 — primary_metric → structural_f1 → negative loc_delta. Implemented in `ratchet.py:432-448` `_compare()`. `compare_key` field records which key decided verdict in experiment_log.
- Reconstruction example from log alone (Run A3): `verdict=discarded` ← `compare_key=primary_metric` ← `candidate_pm=0.0 < champion_pm_before=0.0664`. No source reading required.

**Verdict: PASS.** Formula is 4-factor, each factor inspectable. Tiebreakers explicit and implemented. Verdicts reconstructable from artifacts.

---

## §7 Champion / Compare Semantics

**Evidence:**
- Three-key compare order: primary_metric → structural_f1 → compiler_loc (smaller wins), implemented in `ratchet.py:432-448`. `TIED` verdict when all three are exactly equal — champion NOT updated (ratchet.py:474-475 comment: "TIED means no strict improvement").
- Compare reasons emitted: `compare_key` field in every experiment_log entry's `extra` block. A1/A2/A4 show `compare_key=primary_metric` (A1 empty champion) or `compare_key=compiler_loc` (A2/A4 pm-tied → fell through to loc tiebreaker).
- Ties handled: A2 (TIED, loc tiebreaker) and A4 (TIED, loc tiebreaker) both left champion at sha=3fb8b69 unchanged. Audit confirmed champion.json consistent with last KEEP across all four runs.
- Tie-does-not-rewrite: pre-.027 bug was TIED updating champion.json silently. Fixed per validator finding #4. Current implementation: REVERT/TIED/FORK → champion.json intentionally unchanged.
- `champion_v0_mock.json` preserved as separate archive artifact (sha=53386ec, pm=1.2439 mock-judge) — the mock baseline is separated from the live champion. Live champion.json is real-judge only.
- **KNOWN ITEM — mock/real divergence:** The `.027` proving run discovered the mock-established champion (pm=1.2439 set by gold-aware-mock) was incommensurable with real-judge scoring (pm=0.0664 on same compiler). CTO ruled Option A+ — wipe champion.json + fresh real-judge baseline. Entries 10-13 VOIDed and annotated in experiment_log. This fully resolves the immediate divergence operationally.
- **CAVEAT — v1.1 parking-lot:** `champion.json` lacks a `judge_mode` field. A future agent that reads champion.json cannot structurally verify whether it was established under mock or real scoring — it must trace `scorecard_path` to confirm. CTO leans toward adding `champion.judge_mode` as a v1.1 item. This SC endorses that position: the Option A+ reset resolved the problem operationally for Phase 3, but the structural gap remains.

**Verdict: PASS with caveat.** Compare semantics fully implemented. Option A+ reset closed the mock/real divergence. Caveat: champion.json lacks judge_mode — v1.1 parking-lot item, not blocking Phase 3 close.

---

## §8 Artifact Authority

**Evidence:**
- One authoritative scorecard family: `comp/targets/httpx/scorecards/{sha7}_{tv8}.json`. Filename scheme is deterministic: `ratchet.py:403-406`. No parallel scorecard family.
- One authoritative experiment log: `comp/targets/httpx/experiment_log.jsonl` (append-only JSONL, `experiment_log.py:53`). No secondary summary maintained in parallel.
- One authoritative champion state: `comp/targets/httpx/champion.json`. `champion_v0_mock.json` is a preserved archive artifact (the voided mock baseline) — it is not consulted by any runtime code path.
- Legacy surface decommission: .028 Phase 2 legacy artifact decommission (commits `5622dad4 + 09f7e798`) removed prior-cycle scorecard paths and secondary log formats. Reference: TO `COMP_LEARNS.028` inventory report.

**Verdict: PASS.** Single authoritative artifact family for each artifact type. Secondary summaries not maintained in parallel. Legacy paths decommissioned in .028.

---

## §9 Schema Discipline

**Evidence:**
- `schema_version` field on every experiment_log entry. v1 entries (pre-.024) lack `judge_mode` and `benchmark_honest`. v2 entries require `judge_mode in ("mock","real")` or `append()` raises (`experiment_log.py:57-61`).
- Backward compat on read: `load_entries()` in `experiment_log.py:83` normalizes v1 entries by filling `judge_mode=""` and `benchmark_honest=False` defaults. Downstream readers consume normalized dicts without branching on `schema_version`.
- Scorecard backward compat: `scorecard_from_dict()` uses `.get()` with defaults for newer fields: `judge_model_id=""`, `compiler_loc=0`, `judge_mode=""`, `benchmark_honest=False`, `cache_provenance=None`. Pre-.025 scorecards readable with correct defaults.
- `tied_at_best`, `winners_at_best`, `random_unique_win` added in .026 with backward-compat defaults in `scorecard_from_dict()` (`.get()` pattern).
- All 4 Option A+ scorecards: `schema_version=2` (implicit in scorecard structure via presence of `judge_mode` field).
- The 8 pre-v2 experiment_log entries (iters 1-8) are readable with normalized defaults. They are not benchmark evidence (no `judge_mode`) but are preserved as audit trail.

**Verdict: PASS.** Schema versioned. Old entries readable. Pre- and post-tightening evidence distinguishable via `schema_version` and `benchmark_honest`.

---

## §10 Reproducibility Proof

Five required demonstrations mapped to actual runs:

**Demonstration 1 — Same compiler, same target, same scorer regime, rerun → identical score.**
- Baseline: Run A1 (sha=3fb8b69, pm=0.06635351328309276, real judge).
- Rerun: Run A2 (sha=5db71c6, same compiler.py content, pm=0.06635351328309276, cache_hits=114, cache_misses=0).
- pm bit-exact. Cache served all 114 entries. No fresh LLM calls.
- Evidence: `experiment_log.jsonl` entries timestamped 20:29 (A1) and 20:30 (A2); scorecards `3fb8b69_909ea79f.json` and `5db71c6_909ea79f.json`.
- **PASS.**

**Demonstration 2 — Same logical compiler content under different git SHA → expected cache/score behavior.**
- sha=3fb8b69, sha=5db71c6, sha=92f5e4c: three different git SHAs, identical compiler.py content.
- All three: cache_hits=114, cache_misses=0, pm=0.06635351328309276 (bit-exact across A1/A2/A4).
- Cache is content-addressed via `source_hash = SHA-256(compiler.py content)`. Git SHA is irrelevant.
- Evidence: PROVING_SEQUENCE_R1_R5.md Q3 analysis; experiment_log entries for A1/A2/A4.
- **PASS.** Content-addressed cache identity confirmed end-to-end.

**Demonstration 3 — Induced regression → lower score and correct compare outcome.**
- Run A3 (sha=08fa88b, empty-graph compiler): pm=0.0, cache_hits=57, cache_misses=57 (new adversarial variants warmed).
- compare_key=primary_metric (0.0 < 0.0664 = champion). Verdict=DISCARD. Champion unchanged at sha=3fb8b69.
- Evidence: `experiment_log.jsonl` entry timestamped 20:36; scorecard `08fa88b_909ea79f.json`.
- **PASS.**

**Demonstration 4 — Tie case → tie handling behaves exactly as policy says.**
- Runs A2 and A4: pm=0.0664 tied with champion, f1 tied (0.5743), loc tied (26). compare_key=compiler_loc.
- Verdict=TIED. Champion.json not updated (sha=3fb8b69 throughout). TIED does not rewrite champion.
- Evidence: ratchet.py:474-475 "TIED means no strict improvement"; experiment_log entries 20:30 (A2) and 20:38 (A4).
- **PASS.**

**Demonstration 5 — Real-judge proving run → benchmark-honest path works end to end.**
- Run A1 (sha=3fb8b69, judge_mode=real, benchmark_honest=true, judge_model_id=claude-sonnet-4-6): pm=0.0664, verdict=KEEP on empty champion.
- This was the first real-judge entry written to champion.json. Full AB pipeline executed: warm-up (cache pre-populated by VOID'd runs) → primary_metric (cache-only, 114 hits, 0 misses) → structural scoring → mutation stability → scorecard emitted → champion updated.
- **Note on warm_up_entries_written=0 (A1):** AC#2 expected warm_up_entries_written > 0 for run #1 of the proving sequence. Actual: 0, because the AB cache was pre-warmed by the VOID'd runs (d87377a sha, same compiler.py content). The cache infrastructure is working correctly — this is a sequence-setup condition, not a runtime defect. A cold-cache run would require cache wipe (outside TO scope).
- Evidence: scorecard `3fb8b69_909ea79f.json`; experiment_log entry 20:29.
- **PASS (PARTIAL AC#2: warm_up_entries_written=0 due to pre-warming; infrastructure correct).**

**Overall Reproducibility Verdict: PASS.** All 5 demonstrations satisfied. Stability is proven from end-to-end runs, not unit tests alone.

---

## §11 Benchmark Honesty Flag

**Evidence:**
- Every schema_version=2 entry in experiment_log carries `benchmark_honest` field. All 4 Option A+ entries: `benchmark_honest=true`.
- All 4 Option A+ scorecards: `benchmark_honest=true`.
- VOID'd entries (10-13, timestamps 20:00-20:21): `benchmark_honest=true` (real judge was used) but annotated with VOID in `notes` field: "VOID: mock-vs-real divergence — champion_pm_before=1.2439 set by mock judge; real-judge scoring is incommensurable; these entries do not constitute proving-sequence evidence." The honesty flag correctly labels the run class; the VOID annotation is a separate evidentiary layer.
- Pre-v2 entries (iters 1-9, schema_version=1 or missing): `benchmark_honest` defaults to `False` on read — correct, they predate the honesty gate and used mock scoring.
- `champion_v0_mock.json` (benchmark_honest=False) is clearly named and stored separately from `champion.json` (benchmark_honest=True). No confusion path.
- `derive_benchmark_honest()` in `experiment_log.py:42` is the single derivation point: `judge_mode=="real"` AND `judge.credentials_resolved==True`. Downstream readers use stored field, never recompute.

**Verdict: PASS.** Every emitted score carries `benchmark_honest`. Real vs mock is unambiguous. VOID annotations add evidentiary layer on top of the honesty flag. Single derivation point.

---

## §12 Undocumented Load-Bearing Surfaces

Explicit pass conducted by reading `comp/bench/cache.py`, `comp/bench/ab.py`, `comp/bench/scorecard.py`, `comp/loop/ratchet.py`, `comp/loop/experiment_log.py`, and `comp/bench/primary.py`.

### Finding 1 (KNOWN — elevated as required): Content-addressed AB cache identity

- Cache key is SHA-256 of 9-tuple: `question_text|source_hash|graph_hash|selector_hash|selector_version|model_id|model_version|selected_context_token_count|temperature=0`.
- `source_hash` = `SHA-256(compiler.py content)[:16]` — content-hash of the compiler, NOT git SHA. Computed in `ratchet.py:273-274` (`_source_hash(compiler_py_path)`).
- **Effect:** logically equivalent compilers at different git SHAs share cached judge responses regardless of commit sha. Proven: A1 (sha=3fb8b69), A2 (sha=5db71c6), A4 (sha=92f5e4c) all share same 114 cache entries because compiler.py content is identical.
- **Load-bearing:** any future run that touches only org docs (no compiler.py edit) will get full cache hits from prior runs. This is correct behavior — but operators who expect "new commit = cold cache" will be surprised.
- **Documentation gap:** this behavior is mentioned only in `cache.py` docstring and PROVING_SEQUENCE_R1_R5.md Q3 analysis. Not in COMP_LEARNS_ARCHITECTURE.md or RUNTIME_V1.md.
- **Recommendation:** add one-line note to architecture doc §6.4.1: "cache identity is content-addressed on compiler.py byte content, not git sha."

### Finding 2 (NEW): ABCache constructor path double-nesting

- `ABCache.__init__` receives a `target_dir` parameter and creates `self._root = Path(target_dir) / "ab_cache"`.
- `ratchet.py:_main()` passes `cache_dir=target_dir / "ab_cache"` to `iterate()`.
- `iterate()` calls `ABCache(cache_dir)` = `ABCache(target_dir / "ab_cache")`.
- Actual cache files live at: `comp/targets/{name}/ab_cache/ab_cache/{key}.json` — double-nested.
- `ab.py` docstring says: "Stored at `comp/targets/{name}/ab_cache/{cache_key}.json`" — this is WRONG by one level.
- **Confirmed:** `ls comp/targets/httpx/ab_cache/` in ajb_workspace shows 1 entry (`ab_cache/` subdirectory). `ls comp/targets/httpx/ab_cache/ab_cache/` shows 342 cache JSON files.
- **Load-bearing:** any operator reading the docstring to locate cache files will look in the wrong directory. Pruning, auditing, or cold-starting the cache requires knowing the actual `ab_cache/ab_cache/` path.
- **Recommendation:** either fix `ABCache.__init__` parameter name (rename `target_dir` → `cache_dir` and remove the `/ab_cache` suffix) or fix the docstring. Both together.

### Finding 3 (NEW): AB cache is documented as git-tracked but is not git-tracked

- `ab.py` docstring (line 4): "Cache is git-tracked (diffable, auditable, survives sessions)."
- **Evidence:** `feature_clb` worktree (same CLOUD branch as `ajb_workspace`) shows 0 entries in `comp/targets/httpx/ab_cache/`. `ajb_workspace` has 342 entries in the nested path. If the cache were git-tracked, both worktrees would have it (same branch, same committed state).
- **Conclusion:** AB cache is a runtime artifact, not git-tracked. It survives sessions within the same filesystem (ajb_workspace), but is NOT shared across worktrees and is NOT in the git history.
- **Load-bearing:** operators who assume the cache "survives sessions" will be surprised when running from a fresh worktree (like feature_clb) — all 114 primary_metric entries will be cache misses → warm-up phase will make real API calls → potential cost exceedance under $50 budget cap. Phase 3 avoided this because the proving sequence ran in ajb_workspace throughout.
- **Recommendation:** update docstring to "Cache is a runtime artifact (not git-tracked). Survives sessions within the same filesystem directory. Fresh worktrees start cold." Also: confirm whether `.gitignore` explicitly excludes `ab_cache/` or whether the directory simply was never committed.

### Finding 4 (NEW): Scorecard.__eq__ excludes judge_model_id and judge_mode

- `scorecard.py:157-168`: `__eq__` compares only `target_version`, `compiler_sha`, `ratchet_critical`, `primary_metric`. Both `judge_model_id` and `judge_mode` are explicitly excluded (comment at line 159: "two scorecards from the same (target_version, compiler_sha, ratchet_critical, primary_metric) are equal regardless of judge").
- **Effect:** if a future run uses a different model (e.g., claude-opus-4) but produces identical structural outputs, the scorecards compare as equal. Operators who use `==` to check "is this the same result?" cannot distinguish same-content results from different judge regimes.
- **Load-bearing:** callers who need judge identity must use `scorecard.judge_model_id` directly, not `==`. This is intentional but undocumented as a constraint on callers.
- **Recommendation:** add a docstring note to `Scorecard.__eq__` warning callers that judge identity is intentionally excluded from equality.

**Summary of §12 findings:** 1 known item elevated (content-addressed cache), 3 new items found (path double-nesting, cache not git-tracked, __eq__ excludes judge identity). None are blocking for Phase 3 close; all should be addressed before parallel-regime scoring begins.

---

## §13 Minimal Exit Bar

Seven-line checklist per `prompt.md §5`:

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Frozen truth surface exists | PASS — target pinned, gold frozen, target_version versioned (§1) |
| 2 | Score identity is complete | PASS with caveat — scorecard carries full identity; champion.json lacks judge_mode (v1.1) (§2) |
| 3 | Deterministic core is proven | PASS — bit-exact reproducibility proven A2 vs A4 (§3) |
| 4 | Model-mediated path is cache-bound and labeled | PASS — require_hit() halts on miss; benchmark_honest on every record (§4/§11) |
| 5 | Compare semantics are fully implemented | PASS — 3-key compare, TIED non-rewrite, fork detection (§6/§7) |
| 6 | Artifacts are authoritative | PASS — single scorecard family, single log, single champion (§8) |
| 7 | One end-to-end real proving run passes | PASS — A1 (3fb8b69, real judge, benchmark_honest=true, KEEP) (§10 Demo 5) |

Parallel-regime additions (PARALLELIZATION_V1 onward — §4.13/§4.14/§4.15):
| 8 | Context isolation verified (§4.13) | NOT-YET-APPLICABLE — pre-parallel regime, sequential scoring only |
| 9 | Comparability class labeled (§4.15) | NOT-YET-APPLICABLE — no comparison events to evaluate yet |
| 10 | Scoring context manifest emitted and hash-recorded | NOT-YET-APPLICABLE — pre-parallel regime |

**All 7 sequential criteria: PASS.** Items 8-10 not applicable until PARALLELIZATION_V1 is operationalized.

---

## §14 Recommendation

**YELLOW**

The scorer is stable for Phase 3 and Phase 4 evaluation use. All 7 Minimal Exit Bar criteria pass. All 5 reproducibility demonstrations pass. Benchmark-honest path proven end-to-end.

Two caveats prevent GREEN:
1. `champion.json` lacks `judge_mode` — a v1.1 structural gap. Operationally closed by Option A+ reset; structurally open. CTO and SC both lean toward adding `champion.judge_mode` as a v1.1 item.
2. Three new §12 findings (cache path nesting, cache not git-tracked, `__eq__` excludes judge identity) must be documented before parallel-regime scoring begins, as the parallel regime will involve fresh-worktree operations and cross-run comparisons where these gaps become blocking.

No RED findings. Phase exit is permitted with caveats documented here.

---

## §15 Re-open Triggers Currently Armed

Six conditions that auto-trigger a fresh SC review. Status as of 2026-04-21:

| Trigger | Status | What would fire it |
|---------|--------|--------------------|
| Cache identity changes | ARMED (LOW) | Any change to `make_cache_key()` inputs or the 9-tuple formula. Finding 2 (path nesting) should be fixed without touching keying logic; if it is, this trigger does not fire. |
| Compare semantics changes | ARMED (MEDIUM) | The v1.1 `champion.judge_mode` addition changes champion state schema and compare logic. This WILL fire when v1.1 ships. |
| Judge backend changes | ARMED (LOW) | Any model upgrade from `claude-sonnet-4-6` invalidates all 342 cache entries (model_id in cache key). Anticipated when Sonnet is retired. |
| Selector semantics changes | ARMED (LOW) | Adding a 4th selector, changing `selector_version`, or changing `_WARM_UP_BUDGET_TOKENS` would change selector_hash inputs. No near-term indicator. |
| Champion-state changes | ARMED (MEDIUM) | `champion.judge_mode` addition (v1.1) directly modifies champion state schema. Must trigger SC re-review of §7 specifically. |
| Target-version / schema changes | LOW | No gold or source changes planned for httpx v0.28.1. Any gold edit bumps target_version and orphans cache. |

**Near-term highest risk:** v1.1 `champion.judge_mode` addition triggers both "compare semantics" and "champion-state" conditions. SC review scope for that trigger: §2, §7, and Minimal Exit Bar item 2.

---

*Baseline produced: 2026-04-21. Runtime boundary: post-.027b (commit d047496a, tag comp-learns-phase3-closed). This document is the canonical reference for all future runtime/scoring change diffs.*
