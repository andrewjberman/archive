# 1.1.0_SA_CTO Session 10 — Hardcore architectural audit: R9 wire + validator wire + fork tie-guard + dedup

**Date:** 2026-04-21 (Tue, evening ET)
**Agent:** 1.1.0_SA_CTO
**Scope:** Andrew directive post-GPT protocol brief: "start with that [wiring SelectorGameDetected] and let's do a hardcore validation of everything wired so far to make sure there aren't more gaps." Full systematic audit of every architectural invariant declared in PRD v4.2 against its live-path call site. Fix gaps inline.

---

## Objective

GPT's protocol brief flagged the experiment log showing `best_selector=random` across all 5 `.017` iterations. Investigation confirmed the `check_selector_game()` R9 honesty guard is **defined and unit-tested but NOT called anywhere in the live ratchet path**. That's exactly the kind of silent drift the validator warned about: paper-perfect mechanics, semantically-unguarded outcomes.

Andrew asked for "hardcore validation" — not just fix the known gap but audit every other mandatory guard against its live wiring before we start running more targets.

---

## Audit Results

Full architectural-guard inventory. Every declared invariant from PRD v4.2 + TARGET_CLOSEOUT v2.0, traced to its live-path call site.

### GAPS FOUND (fixed this session)

| # | Guard | Was | Now |
|---|-------|-----|-----|
| 1 | `check_selector_game` (R9 fork) | Defined 2× (duplicated in `selectors/base.py` AND `primary.py` with DIFFERENT class identity — same name, different `SelectorGameDetected` Python class). **NOT called** from any live-path file — only tests. Silent. | Consolidated: `primary.py` re-exports from `selectors/base.py`, single class identity across `comp.bench.*`. Wired into `comp/loop/ratchet.py::iterate` right after `compute_primary_metric`. Fork halts champion update and emits verdict=forked to experiment log. |
| 2 | `check_selector_game` tie-semantics | Literal: `best_selector == "random" AND best_lift > 0.1` raises. On the real httpx scorecard where all three selectors saturate at 1.0 and tie-break arbitrarily gave random the crown, literal check would fire a **false positive** (ceiling effect, not dishonesty). | Tie-guard added: fork only raises when `random_lift > max(structured_lifts)`. Tie-at-ceiling is not outperformance; a new unit test (`test_random_ties_structured_at_ceiling_does_not_raise`) encodes the regression guard, and a companion test (`test_random_strictly_beats_structured_raises`) confirms dishonesty still fires. |
| 3 | `validate_gold_survey_attestation` | Defined in `bench/ab_answer_key_validator.py`, tested with 5 fixtures per `.015` AC#7. **NOT called** from any live-path file. The v4 6/6-coverage bug guard was inert. | Wired as pre-flight in `comp/loop/ratchet.py::_main()` before the iteration starts. `GoldSurveyAttestationMissing` → exit 2. Sanity-verified against httpx gold: passes clean. |
| 4 | `ab_answer_key_validator.validate` | Defined, tested. **NOT called** from any live-path file. Malformed answer keys + open-ended-in-ratchet-pool would slip through. | Wired as pre-flight in `comp/loop/ratchet.py::_main()`. `RatchetPoolOpenEndedRejected` + `InvalidAnswerKeyEntry` → exit 2. Sanity-verified against httpx gold. |
| 5 | `Verdict` enum did not model a forked state | KEEP / REVERT / TIED only. A fork had no canonical verdict value — silent exception OR contaminate one of the existing verdicts. | Added `Verdict.FORKED = "forked"`. Champion intentionally NOT updated on fork (broken eval must not advance champion). Experiment log records `verdict=forked` + `fork_reason` in `extra`. |

### WIRED + TESTED — no gap

| Guard | Defined at | Live call site | Verified |
|-------|-----------|----------------|----------|
| `CacheMissDuringPrimaryMetric` | `bench/cache.py:35` | `ABCache.require_hit` at `bench/cache.py:147` — called by `bench/ab.py::run` for every ratchet-critical query | Raises cleanly; caught by `comp/bench/ab.py` and propagated |
| `SubtypeRecord.__post_init__` | `compiler_subtypes/records.py:50` | Runs at every `SubtypeRecord(...)` construction — validates `subtype_kind ∈ SUBTYPE_DIMENSIONS`, rejects flat-string kinds (`imports_dynamic` etc.), rejects unknown attribute keys, rejects unknown attribute values | `test_base_validator.py` — 8 passes |
| `compute_primary_metric` reads only `ratchet_critical` | `bench/primary.py::compute` | Called by `loop/ratchet.py::iterate` + variant scorer | Per PRD §6.1 confirmed — no path into `exploratory` |
| `Scorecard.__eq__` excludes `emitted_at` (R13) | `bench/scorecard.py:123` | Custom `__eq__` implementation | `test_scorecard_determinism_rerun.py` — 3 passes; `.017` iter 4+5 prove `Scorecard.__eq__ is True, emitted_at differs` |
| `Graph.__eq__` deterministic | `ir/schema.py:63` | Custom `__eq__` | `test_schema_roundtrip.py` — 8 passes |
| `ConflictingProvenanceError` (R4) | `graph_builder/conflicts.py` | Raised by `GraphBuilder.build()` when same-confidence records share file+span | `test_conflict_policy.py::test_r4_same_confidence_same_provenance_raises` — passes |
| R1-R5 conflict resolution | `graph_builder/conflicts.py` | R1 `certain`-wins-over-`heuristic`, R2 merge, R3 multi-target, R4 raise, R5 `elevation_required` | `test_conflict_policy.py` — 11 passes (all five rules covered) |
| `ratchet_critical_call` enforces `temperature=0` | `bench/judges/base.py` + `bench/judges/anthropic_judge.py` | Called by `ab.py::warm_up_cache` | `test_judge_protocol.py::test_ratchet_critical_call_enforces_temperature_zero` — raises on `temperature=0.7`; `test_anthropic_judge_ratchet_critical_call_raises_on_nonzero_temp` — explicit coverage of real judge |
| `selector_hash` included in cache key | `bench/cache.py:43` | `make_cache_key(question_text, source_hash, graph_hash, selector_hash, selector_version, ...)` | `bench.selectors.base.selector_hash` computed from (name, version, sorted_node_ids, sorted_edge_ids); changes invalidate cache as designed |
| Experiment log append-only | `loop/experiment_log.py` | `explog.append()` | `test_experiment_log.py::test_append_only_does_not_mutate_prior_entries` — passes |
| Mutation engine (rename/reorder/noise × 3 seeds) | `bench/mutations/` | Called by `loop/ratchet.py::iterate` step 5 | Live scorecard `e8f2c50_909ea79f.json` shows 9 `per_mutation_seed` entries — complete coverage |
| Node-ID canonicalization (`_normalize_node_ids`) | `bench/mutations/harness.py` | Called before mutation diff | Session08 noted this fix; runs producing `mutation_stability=0.997` on httpx confirm |

### ADVISORY — not a halt by design

| Guard | Behavior | Per PRD |
|-------|----------|---------|
| `mutation_stability.threshold_passed` (v0: ≥0.85) | Computed into `MutationStabilityReport.threshold_passed` field. NOT consumed as a halt. Primary_metric is α-weighted by `mutation_stability.aggregate` — an unstable compiler's score is discounted toward zero rather than halted. | PRD §6.6: "Below `0.70` triggers a scorecard warning flag" — warning only; the α-weighting is the enforcement mechanism |
| `conflict_fraction` on `httpx` (single-subtype) | Always 0.0 on inaugural target | PRD §5.3 invariant: single-extractor single-subtype target has no inter-subtype disagreement; conflict resolution is exercised by synthetic multi-subtype fixtures in `.014` tests, not the `httpx` run |

---

## Changes Shipped This Session

### 1. `comp/bench/selectors/base.py`

`check_selector_game` rewritten with tie-guard. Message now includes lift values for log triage. Still raises `SelectorGameDetected(scorecard=sc, message=...)`; class identity unchanged.

### 2. `comp/bench/primary.py`

Deleted local `SelectorGameDetected` class + local `check_selector_game` function. Added `from comp.bench.selectors.base import SelectorGameDetected, check_selector_game` at module head. `comp.bench.primary.SelectorGameDetected is comp.bench.selectors.base.SelectorGameDetected` now `True` — duplicate class identity eliminated.

### 3. `comp/loop/ratchet.py`

- Added `Verdict.FORKED = "forked"`.
- Imported `check_selector_game` + `SelectorGameDetected` + `validate_answer_key` + `validate_gold_survey_attestation` + `RatchetPoolOpenEndedRejected` + `GoldSurveyAttestationMissing`.
- Inserted §6b honesty guard in `iterate()` after `compute_primary_metric`: try/except `SelectorGameDetected`; on fork → `fork_reason = str(e)`; skip champion update; log `extra.fork_reason`.
- Inserted pre-flight gates in `_main()` before `iterate()` kicks off: `validate_answer_key(ak_path)` + `validate_gold_survey_attestation(target_dir)`. Both exit-2 on halt.

### 4. `comp/bench/selectors/tests/test_selector_game_fork.py`

Added two regression tests:
- `test_random_ties_structured_at_ceiling_does_not_raise` — the httpx v0 scorecard shape. Must not raise.
- `test_random_strictly_beats_structured_raises` — random=0.8 beats keyword=0.1 + centrality=0.05 by >0.1 margin. Must raise.

### 5. Live verification

Ran `comp-learns-run.sh httpx --once` post-fix. Results:
- Pre-flight validators ran clean (no halt).
- `check_selector_game` ran on the live scorecard; **tie-at-ceiling correctly did NOT fire** the fork (prior broken state would have either fired falsely OR silently missed genuine dishonesty).
- Verdict: `TIED` at `primary_metric=1.2439` (iter 6 identical to champion iter 5 — determinism holds).
- Full test suite: **268 passed, 0 failed** across `comp/bench/ comp/loop/ comp/compiler_subtypes/ comp/graph_builder/ comp/ir/ comp/parsers/`.

### 6. Artifact updates

- `comp/targets/httpx/experiment_log.jsonl` — iter 6 appended (verification run, TIED).
- `comp/targets/httpx/champion.json` — updated to cite iter-6 scorecard path (same compiler_sha/primary_metric).

---

## Decisions Made

1. **Consolidate `SelectorGameDetected` class identity.** Two copies with the same name but different class identities is a latent bug (one site catches what another raises → `isinstance` fails). Fixed by deletion + re-export. `comp/bench/__init__.py` public surface unchanged.

2. **Tie-guard semantics over literal PRD.** PRD §6.5 literal is `best_selector == "random" AND best_lift > 0.1`. PRD spirit is "random can't honestly OUTPERFORM structured." On the real httpx scorecard these diverge (all three selectors saturate at 1.0, tie-broken best_selector=random). Chose spirit semantics; encoded in test.

3. **Pre-flight validators in `_main()`, not `iterate()`.** Answer-key + gold-survey attestation are LOAD-TIME preconditions, not per-iteration checks. Calling once at entry is efficient and ensures the run aborts cleanly on malformed gold before any LLM calls or cache writes.

4. **`Verdict.FORKED` instead of letting exception propagate.** A raised exception leaves `experiment_log.jsonl` un-appended for that iteration — the SHA is lost from the trace. `Verdict.FORKED` + `fork_reason` in `extra` preserves the trace + surfaces to CTO.

5. **Did NOT wire `mutation_stability.threshold_passed` as a halt.** PRD §6.6 says "Below `0.70` triggers a scorecard warning flag" — warning, not halt. The α-weighting in `primary_metric` is the enforcement mechanism. Changing this to a halt would be a PRD amendment, not a wire fix.

6. **No new PRD amendments.** Every change maps to a wire gap against existing PRD spec. The tie-guard is a semantics clarification of §6.5; the two validators are wiring the specs that already exist; `Verdict.FORKED` is the implementation of the fork behavior §6.5 already mandates. No new architecture decided in this session.

---

## Files Modified

- `comp/bench/selectors/base.py` — `check_selector_game` tie-guard.
- `comp/bench/primary.py` — dedup via re-export from `selectors/base.py`.
- `comp/loop/ratchet.py` — `Verdict.FORKED` + `check_selector_game` wire + pre-flight validators.
- `comp/bench/selectors/tests/test_selector_game_fork.py` — 2 regression tests.
- `comp/targets/httpx/experiment_log.jsonl` — iter 6 (live verification).
- `comp/targets/httpx/champion.json` — updated scorecard_path.
- `org/tier1_exec/1.1.0_SA_CTO/logs/2026-04-21/session10_hardcore_audit_r9_wire_validators_dedup.md` — this log.

No PRD edits. No TO status changes. No prompt.md edits. No JSON narrative edits.

---

## Current State

### The ratchet is semantically honest now

What `.017` proved:
- KEEP / DISCARD / adversarial / determinism mechanics work.

What session 10 adds:
- R9 fork actually runs on every iteration (was: defined but unwired).
- Pre-flight gates halt on malformed gold (was: validators defined but unwired).
- Class identity consolidated (was: two `SelectorGameDetected` classes with different identities).
- Tie-ceiling correctly interpreted as non-dishonesty (was: literal check would false-positive).

### Remaining honesty unknowns

These are not gaps — they are open questions the ratchet will surface empirically:
- **Selector ceiling on httpx.** `per_selector = {1.0, 1.0, 1.0}` saturates. Target-2 (click, per `.009`) should break this ceiling by design (nested command-group structure stresses selector differentiation). If click ALSO ceilings at 1.0, the question shape needs revisiting (too easy for any structured selector).
- **Compiler ceiling on httpx.** `primary_metric=1.2439` holds across iters 2, 4, 5, 6 — no one has edited the compiler to see if the ratchet produces meaningful deltas on genuine improvements or regressions. The 4 `.017` demos covered KEEP/DISCARD/adversarial/determinism but not "human hand-edits compiler, ratchet notices." That's what more iterations on httpx should demonstrate.
- **Node-ID aliasing pattern.** The `_normalize_node_ids` fix (session08) caught one instance (temp-dir leakage in `harness.py`). No other instances observed yet. Target-2 with a different filesystem layout is the involuntary stress test.

---

## Next Steps

**Ready to run on targets.** With R9 guard wired + validators gating pre-flight + dedup applied, the loop is honestly runnable on:
- More httpx iterations (human edits `compiler.py`, ratchet produces real deltas).
- Target-2 `click` (via `.009` scope, pending harness PRD + gold authoring).

**NOT doing:**
- PRD amendments.
- New TOs.
- Further narrative objects.

**Watching:**
- First genuine compiler-edit iteration on httpx — see if `primary_metric` actually moves.
- When `click` stands up, see if `per_selector` ceiling breaks.
- Any `mutation_stability` anomaly — the `_normalize_node_ids` fix pattern may recur.

---

## Compiler Tools

| Tool | Purpose | Outcome |
|------|---------|---------|
| Read (`comp/bench/ab.py`, `ratchet.py`, `primary.py`, `selectors/base.py`, `ab_answer_key_validator.py`, `compiler_subtypes/records.py`, `compiler_subtypes/base.py`) | Full code inspection of every architectural guard | Completed |
| Grep (`check_selector_game`, `SelectorGameDetected`, `validate_gold_survey_attestation`, `ab_answer_key_validator.validate`, `require_hit`, `CacheMissDuringPrimaryMetric`, `ConflictingProvenanceError`, `ratchet_critical_call`, `selector_hash`, `__eq__`) | Call-site audit for every declared invariant | Identified 3 unwired guards + 1 duplicate class; confirmed 12+ wired + tested guards |
| `python -c "..."` sanity check | Verified `ab_answer_key_validator.validate` + `validate_gold_survey_attestation` pass on real httpx gold | Both PASS |
| `python -m py_compile` | Pre-commit compile check for all edited `.py` | Clean |
| `.tools/ds-commit-gate.sh` | CLAUDE.md rule 14 pre-commit gate | Clean for 4 files |
| `python -m pytest` (affected suites) | Regression check | 268 passed, 0 failed |
| `comp-learns-run.sh httpx --once` | Live end-to-end verification | Clean; fork correctly did NOT fire on tie-at-ceiling |

---

## Session chain reference

| Session | Log | Commit | Summary |
|---------|-----|--------|---------|
| 07 | `session07_validator_feedback_process_tuning.md` | `eaaaea0e` | Validator-driven trim |
| 08 | `session08_017_arch_acceptance_v0_capstone.md` | `7d0e9326` | `.017` arch ACK + 17/1/3/1 reconcile + 2 watch-items |
| 09 | `session09_009_018_ship_v0_wave_complete.md` | `794f97df` | `.009` target-2 memo (click) + `.018` program.md v1 + discipline section removed |
| 10 | `session10_hardcore_audit_r9_wire_validators_dedup.md` | *this commit* | R9 fork wired + tie-guard + 2 validators wired + `SelectorGameDetected` class consolidated + `Verdict.FORKED` added |

— 1.1.0_SA_CTO
