# Session Log — COMP_LEARNS.070 + .077 + .078 — delivered-context sidecar + dual-output grader emission

**Agent:** 1.3.0_DS_CompLearns
**Date:** 2026-04-27
**TOs touched:** .070 (complete), .077 (complete), .078 (complete)
**Outcome:** All three SHIPPED. R-DS-1 P1 (V1.2 grader-governance) ship-blocker cleared. .079 (SC) unblocked.

---

## Objective

1. Execute COMP_LEARNS.070: per-question per-condition delivered-context sidecar (R-DS-1).
2. Execute COMP_LEARNS.077 + .078: V1.2 dual-output grader emission (R-DS-1 P1) — two overlapping TOs unified into a single commit.
3. Maintain inbox-watch.sh running throughout (Andrew reminder, second time).

---

## Work Completed

### COMP_LEARNS.070 — delivered-context sidecar (R-DS-1)

**GO received** at session resume from 2.1.0_SA_COO.

**Phase 0:** 458 baseline pytest pass confirmed.

**Phase 1 — runner.py changes:**
- Added `import hashlib` to top-level imports
- Added `_emit_delivered_context_sidecar()`: re-compiles graph + re-runs all 4 conditions (C1 unaided, C2 RandomSelector, C3 CentralitySelector, C4 KeywordSelector), writes per-(qid, cond) blob `.txt` files, writes `manifest.json` (schema_version=1) with sha256 blob hashes
- Added `_patch_scorecard_sidecar_ref()`: patches scorecard JSON on disk with `delivered_context_ref` + `delivered_context_manifest_sha`
- Wired post-iterate() call in `run()` loop

**Phase 2 — scorecard.py changes:**
- Added `delivered_context_ref: str | None = None` and `delivered_context_manifest_sha: str | None = None` to Scorecard dataclass
- Updated `scorecard_to_dict()` and `scorecard_from_dict()` (null-safe via `.get()`)

**Bug fix included:** `comp/loop/experiment_log.py::load()` had `d["iter"]` but v3 schema uses `"iteration"` — caused `at_plateau()` to crash before iterate() could run. Changed to `d.get("iter", d.get("iteration", 0))`. Required to enable Phase 4 smoke test.

**Phase 4 smoke test (`python comp/bin/comp-learns-ratchet click --judge mock --max-iter 1`):**
- 44 blobs (11 ratchet_critical questions × 4 conditions) + manifest.json written
- Scorecard `df0901e_d869779f.json` patched: `delivered_context_ref=comp/results/dev-click-001/iter1/delivered_context/manifest.json`, `delivered_context_manifest_sha` 64-char hex present
- Edge case confirmed: C1 unaided emits `# C1 unaided -- no compiler context delivered` comment line

**Commit:** `68f64865` — author `1.3.0_DS_CompLearns`
**Push:** `df0901ed..68f64865 CLOUD -> CLOUD` from feature_clb

---

### COMP_LEARNS.077 + .078 — V1.2 dual-output grader emission (R-DS-1 P1)

**Two GOs received** from 2.1.0_SA_COO + nudge after watchdog summary said "Awaiting R-DS-1 TO" while GO sat unread.

**Scope reconciliation:** .077 wanted `comp/bench/semantic_grader.py` (new file). .078 wanted `_semantic_grade_response()` in `comp/bench/ab.py`. Schemas differed (.077 top-level disagreement_rate vs .078 grader_governance block). Decision: implement BOTH file structures + unified scorecard schema satisfying both ACs in single commit.

**Phase 0:** 480 pytest baseline confirmed (post-.070 ship).

**Phase 1 — semantic grader (`comp/bench/semantic_grader.py`, NEW):**
- `grade_semantic(response_text, entry) -> dict` with R-SC-2 label
- Markdown stripping: code fences, backticks, bold/italic
- Phrase extraction: "the answer is X" / "Answer: X" patterns (regex `_ANSWER_PHRASE_RE`)
- Type-specific heuristics:
  - `numeric`: float() + tolerance match → parseable-correct/wrong; regex `\b(\d+(?:\.\d+)?)\b` first-number from prose → semantic-correct/wrong-but-unparseable
  - `set_membership`: comma-split with structured-token guard (no spaces, len ≤ 50); substring count → semantic-correct/partial/wrong-unparseable
  - `enumerable`: word-match in prose
  - Fallback (sphinx schema types: class_name/registration_call/attribute_value): substring match against gold_answer or first value
- 6 R-SC-2 labels: parseable-correct, parseable-wrong, semantic-correct-but-unparseable, semantic-partial-correct-unparseable, semantic-wrong-unparseable, semantic-ambiguous

**Phase 1.5 — ab.py wrapper:**
- `_semantic_grade_response(response_text, entry) -> str` — thin wrapper, returns label string only (per .078 signature spec)

**Phase 1.6 — tests (`comp/bench/tests/test_semantic_grader.py`, NEW):**
14 tests covering all R-SC-2 labels + disagreement flag logic. Initial run 13/14 passed; one failure (`test_set_correct_in_prose`) caused by comma-split treating prose as structured values. Fix: added `_looks_structured` guard requiring all set-elements to have no spaces and len ≤ 50. Re-run 14/14 passed.

**Phase 2 — runner _run_n_trials:**
- Changed return type from `list[bool]` to `list[dict]` with `{exact_pass, semantic_label, disagreement, response_text}`
- Updated `run_pilot()` callers: `c4_s = sum(t["exact_pass"] for t in c4_trials)`; pilot artifact now includes `c4_grader_details` / `c1_grader_details` with full per-trial dicts

**Phase 3 — scorecard schema:**
- New `GraderGovernance` dataclass: `exact_match_correct, semantic_aware_correct, disagreement_count, total_responses, disagreement_rate, schema_version`
- `grader_governance: GraderGovernance | None` field on Scorecard (null-safe; pre-V1.2 backward-compat)
- Top-level `disagreement_rate` mirror in `scorecard_to_dict()` (for .077 smoke-test compat)
- Walrus operator `(_gg := d.get("grader_governance")) is not None` in `scorecard_from_dict()` for clean conditional construction

**Phase 4 — sidecar manifest extension:**
- Added `blob_grader_results: dict` to manifest schema
- Per (qid, cond) entry: `{exact_match: {graded}, semantic: {graded, label}, disagreement}` — null for C1 (no judge call in ratchet)
- Source/graph hashes computed inline (mirrors `ratchet._source_hash` + `_graph_hash` formulas) to enable AB cache lookup
- ABCache.get() lookup with same 9-tuple key as warm_up_cache; on hit, runs both graders against cached response_text
- Grader governance aggregate computed from blob_grader_results during sidecar pass and returned to `_patch_scorecard_sidecar_ref()`

**Phase 5 — gates:** PASS on all 4 changed Python files (semantic_grader.py + ab.py + runner.py + scorecard.py). 494 pytest pass (480 baseline + 14 new). Zero failures.

**Phase 6 — smoke test (`python comp/bin/comp-learns-ratchet click --judge mock --max-iter 1`):**
- `[sidecar] grader_governance: exact=32/33 disagreements=0 rate=0.000` (mock judge gives parseable answers, low disagreement expected)
- Scorecard `2c4a350_d869779f.json` patched with `disagreement_rate: 0.0` and full `grader_governance` block (all 6 fields)
- `blob_grader_results` populated for C2/C3/C4; null for C1 (q01_C1 = null)

**Commit:** `dbb30c32` — author `1.3.0_DS_CompLearns`
**Push:** `8d716e5d..1998340f CLOUD -> CLOUD` from feature_clb (my commit + ADHC_OWNPTH.007 from another agent on top)

**MCPs sent:** COO COMPLETE, CTO CC (per .078 closeout), SC FYI (.079 unblocked with schema reference).

---

## Decisions Made

### .070 sidecar
- `run_id = f"iter{iter_num}"` — deterministic per iteration; re-runs of same iter overwrite (acceptable since content is deterministic).
- Conditions hardcoded as `[("C1", None), ("C2", RandomSelector()), ("C3", CentralitySelector()), ("C4", KeywordSelector())]` — matches PRD four-condition table; C1 = unaided (no selector).
- Sidecar emission is non-fatal: try/except returns `(None, None, None)` on any failure; scorecard fields stay null.
- Bundled experiment_log.py compat fix in same commit because it was required to enable smoke test (couldn't ship .070 evidence without it).

### .077 + .078 unified
- Implementation choice: regex-with-extractors-and-tolerance (CTO's "lean" recommendation, per .078 implementation note). No judge calls in semantic grader — pure heuristic, free, deterministic.
- Function placement: `grade_semantic()` in new `semantic_grader.py` (per .077 AC-1) PLUS `_semantic_grade_response()` thin wrapper in `ab.py` (per .078 AC-1). Both file paths satisfy both TOs' commit-scope expectations.
- Schema unification: scorecard gets `grader_governance` block (.078) AND top-level `disagreement_rate` (.077 smoke-test compat).
- `_emit_delivered_context_sidecar()` returns 3-tuple now: `(sidecar_ref, manifest_sha, grader_governance_dict)` — added grader_governance computation in same pass to avoid double-walking the AB cache.
- Disagreement flag definition: `(exact_pass AND semantic != "parseable-correct") OR (NOT exact_pass AND semantic == "parseable-correct")`. Catches V1.2 grader-format problem class bidirectionally per CTO message.
- Set-membership comma-split heuristic: only treat raw_set as parseable values if all elements have no spaces and ≤50 chars. Avoids prose like "Command's direct subclasses are X and Y, not Z" being mis-classified as parseable-wrong.

### Worktree + git hygiene
- All edits + commits from `/c/Users/AndrewBerman/Desktop/feature_clb` per Andrew 2026-04-21 directive.
- `git commit --only --author=1.3.0_DS_CompLearns -- <files>` scoped to changed files only.
- For .077+.078 commit: had to `git add` new files first (`comp/bench/semantic_grader.py`, `test_semantic_grader.py`) since `--only` only commits already-tracked or staged files.

---

## Files Modified

| File | Change | TO |
|------|--------|-----|
| `comp/loop/runner.py` | .070: hashlib import + `_emit_delivered_context_sidecar()` + `_patch_scorecard_sidecar_ref()` + post-iterate call site. .077+.078: `_run_n_trials()` returns list[dict], sidecar gets AB cache lookup + blob_grader_results + grader_governance return, run_pilot updated for new trial shape. | .070, .077+.078 |
| `comp/bench/scorecard.py` | .070: delivered_context_ref + manifest_sha fields. .077+.078: GraderGovernance dataclass + grader_governance field + top-level disagreement_rate mirror. | .070, .077+.078 |
| `comp/loop/experiment_log.py` | `iter`/`iteration` key compat fix in `load()` (3-char change) | .070 (smoke-test enabler) |
| `comp/bench/semantic_grader.py` | NEW: `grade_semantic()` with 6-label R-SC-2 taxonomy, regex extractors per type | .077+.078 |
| `comp/bench/ab.py` | NEW function `_semantic_grade_response()` (thin wrapper) | .077+.078 |
| `comp/bench/tests/test_semantic_grader.py` | NEW: 14 tests covering all labels + disagreement logic | .077+.078 |

---

## Blockers

None. .079 (SC disagreement labels) hard-gate cleared by dbb30c32.

---

## Current State

- COMP_LEARNS.070: COMPLETE (commit 68f64865). RAVC pending COO.
- COMP_LEARNS.077: COMPLETE (commit dbb30c32). RAVC pending COO.
- COMP_LEARNS.078: COMPLETE (commit dbb30c32). RAVC pending COO + CTO CC sent.
- Inbox watcher: running (`bash org/mcp/inbox-watch.sh 1.3.0_DS_CompLearns` in feature_clb, run_in_background).

---

## Next Steps

1. Await RAVC ACK from COO on .070 + .077 + .078.
2. Watch for SC .079 commit (now unblocked by dbb30c32). When SC ships, V1.2 §10 ship-blocker for primary case dispatch is satisfied (.077 + .078 + .079 jointly).
3. Path B target re-selection sub-PRD authoring (COO) gates on .077+.078+.079 jointly complete.
4. R-DS-2 (sphinx ab_answer_key.yaml schema gap) is orthogonal/parallel — can be done if dispatched.

---

## Compiler Tools

| Phase | TO | Run | Expected | Observed | Pass/Fail |
|-------|-----|-----|----------|----------|-----------|
| Before write (.070) | .070 | `pytest comp/ --ignore=comp/targets -q --tb=no` | 458 passed | 458 passed in 31s | PASS |
| Before commit (.070) | .070 | `.tools/ds-commit-gate.sh runner.py scorecard.py experiment_log.py` | 3 checks exit 0 per file | All checks passed (3 files) | PASS |
| Before commit (.070) | .070 | `pytest comp/ --ignore=comp/targets` | 458+ passed | 480 passed | PASS |
| Smoke (.070) | .070 | `comp-learns-ratchet click --judge mock --max-iter 1` | sidecar files + scorecard patched | 44 blobs + manifest + scorecard ref/sha set | PASS |
| Before write (.077+.078) | .077+.078 | `pytest comp/ --ignore=comp/targets` | 480 passed | 480 passed | PASS |
| Before commit (.077+.078) | .077+.078 | `.tools/ds-commit-gate.sh semantic_grader.py ab.py runner.py scorecard.py` | 3 checks exit 0 per file | All checks passed (4 files) | PASS |
| Before commit (.077+.078) | .077+.078 | `pytest comp/bench/tests/test_semantic_grader.py` | 14 passed | 14 passed (after set_correct_in_prose fix) | PASS |
| Before commit (.077+.078) | .077+.078 | `pytest comp/ --ignore=comp/targets` | 480+ passed | 494 passed (480 baseline + 14 new) | PASS |
| Smoke (.077+.078) | .077+.078 | `comp-learns-ratchet click --judge mock --max-iter 1` | grader_governance + blob_grader_results in artifacts | exact=32/33 disagree=0 rate=0.000; scorecard patched; manifest extended | PASS |
