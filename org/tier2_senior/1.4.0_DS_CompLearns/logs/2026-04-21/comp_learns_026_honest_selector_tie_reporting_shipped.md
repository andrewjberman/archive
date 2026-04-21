# 1.4.0_DS_CompLearns — Session Log 2026-04-21

**TO:** COMP_LEARNS.026 (honest-selector-tie-reporting-and-status)
**Outcome:** COMPLETE — commit pending push

---

## Objective

Add `winners_at_best: list[str]` and `random_unique_win: bool` to the downstream_ab
scorecard block, mirror into experiment_log extra, create `render_selector_summary`
chokepoint helper with tie-first rule, and replace the `.023` `--status` stub with the
full derived-view per RUNTIME_V1.md §10.

---

## Work Completed

1. **`comp/bench/scorecard.py`** — Added `winners_at_best` and `random_unique_win` to
   `DownstreamAB`. Updated `_ratchet_critical_to_dict` and `_ratchet_critical_from_dict`
   to emit/load both fields with backward-compat defaults (`[]` / `False`).

2. **`comp/bench/ab.py`** — Replaced `winners_at_max` list with `winners_at_best = sorted(...)`.
   Added `random_unique_win = winners_at_best == ["random"]`. Passed both to `DownstreamAB` return.
   Early-return (no questions) now also carries `winners_at_best=[]` and `random_unique_win=False`.

3. **`comp/loop/ratchet.py`** — Added `winners_at_best` and `random_unique_win` to
   the `extra` dict in `explog.append()`.

4. **`comp/loop/render.py`** (NEW) — Pure-function module with:
   - `render_selector_summary(dab)` — tie-first rule chokepoint; zero `f"best_selector={...}"`
     formatting outside this function.
   - `render_status(target, target_dir, ...)` — full `--status` output: champion / last N
     verdicts with `compare_key` inference / terminal proximity / cache provenance / selectors.
   - All reads from `champion.json`, `experiment_log.jsonl`, `scorecards/*.json`. No writes.

5. **`comp/loop/runner.py`** — Replaced `do_status` stub with a 4-line dispatch to
   `render.render_status`. Added `last_n: int = 5` parameter.

6. **`comp/bin/comp-learns-ratchet`** — Updated `--status` help text; added `--last N` flag
   (default 5); wired to `do_status(args.target, last_n=args.last)`.

7. **`comp/bench/tests/test_selector_tie_reporting.py`** (NEW) — 9 tests covering ACs 1-5, 11,
   plus alphabetical-sort invariant. All pass.

8. **`comp/loop/tests/test_status_render.py`** (NEW) — 7 tests covering ACs 6-10 plus fallback.
   All pass.

9. **`comp/loop/tests/test_runner_cli.py`** — Updated existing `test_status_dispatches_do_status`
   to expect `do_status('httpx', last_n=5)` after the new `--last` flag wiring.

---

## Decisions Made

- `render_selector_summary` falls back to `best_selector` when `winners_at_best` is empty
  (pre-.026 scorecard loaded from JSON) — AC#11 backward-compat.
- `_infer_compare_key` in render.py: delta != 0 → primary_metric; loc_delta != 0 → compiler_loc;
  otherwise structural_f1. Covers all three-key comparison cases without storing compare_key
  in the log (the linter also added a `compare_key_for()` helper in ratchet.py for future use).
- `budget_sec` not displayable from standalone `--status` (no active runner to measure elapsed
  time against) — shows "not measurable outside active runner" in terminal proximity block.
- `--last N` flag is a top-level argument (not bound to the mutually-exclusive mode group)
  so it parses correctly whether or not `--status` is passed; it's silently unused in run mode.

---

## Files Modified

| File | Action |
|------|--------|
| `comp/bench/scorecard.py` | Add `winners_at_best`, `random_unique_win` to `DownstreamAB`; update ser/deser |
| `comp/bench/ab.py` | Compute `winners_at_best` (sorted), `random_unique_win`; pass to `DownstreamAB` |
| `comp/loop/ratchet.py` | Mirror `winners_at_best`, `random_unique_win` into experiment_log extra |
| `comp/loop/render.py` | NEW: `render_selector_summary` + `render_status` (full --status) |
| `comp/loop/runner.py` | Replace `do_status` stub with `render.render_status` dispatch |
| `comp/bin/comp-learns-ratchet` | Add `--last N`; update --status help text |
| `comp/bench/tests/test_selector_tie_reporting.py` | NEW: 9 tests (ACs 1-5, 11, sort invariant) |
| `comp/loop/tests/test_status_render.py` | NEW: 7 tests (ACs 6-10 + fallback) |
| `comp/loop/tests/test_runner_cli.py` | Fix existing test for `last_n=5` kwarg |
| `org/tier2_senior/1.4.0_DS_CompLearns/task_orders/COMP_LEARNS.026.*.md` | status → complete |

---

## Blockers

None.

---

## Current State

COMP_LEARNS.026 complete. `.028` (legacy loop decommission) still blocked on `.027`
(real-judge proving sequence; 1.1.0_DS_CompLearns lane, still pending).

---

## Next Steps

1. Await `.027` completion from 1.1.0_DS_CompLearns — unblocks `.028`.
2. On GO for `.028`: inventory grep, delete legacy surfaces, update docs.

---

## Compiler Tools

| Phase | Run | Expected | Observed | Pass/Fail |
|-------|-----|----------|----------|-----------|
| Before write | N/A — no gold scripts touched; comp-pipescript io not applicable | — | — | N/A |
| Before commit | `ds-commit-gate.sh` on 7 .py files | OK | `OK: pre-commit gate clean for 7 file(s)` | PASS |
| Before commit | `ds-commit-gate.sh` on test_runner_cli.py update | OK | `OK: pre-commit gate clean for 1 file(s)` | PASS |
| Before commit | `pytest comp/ -q --ignore=comp/targets` | 402 passed (pre-fix), then 403 passed | 403 passed in 46.86s | PASS |
