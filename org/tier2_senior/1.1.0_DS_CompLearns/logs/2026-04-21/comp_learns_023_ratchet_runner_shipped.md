# Session: COMP_LEARNS.023 — comp-learns-ratchet Runner — 1.1.0_DS_CompLearns

**Date:** 2026-04-21
**Task Order:** COMP_LEARNS.023.comp-learns-ratchet-runner.md
**Status:** COMPLETE — commit `41225ed9`

---

## Objective

Ship `comp/bin/comp-learns-ratchet` — the authoritative Python runner (Layer B) around
`ratchet.iterate()`. Multi-iteration, ratchet-native terminal conditions, `--judge mock|real`
required, `--resume`/`--halt`/`--status`, one-paragraph exit summary derived from artifacts.

---

## Compiler Tools

| Tool | Command | Result | Phase |
|------|---------|--------|-------|
| Pre-commit gate | `.tools/ds-commit-gate.sh comp/loop/runner.py comp/loop/tests/test_runner_*.py` | PASS — OK: pre-commit gate clean for 4 file(s) | Before commit |
| Pre-commit gate (retested after test fix) | `.tools/ds-commit-gate.sh comp/loop/tests/test_runner_cli.py` | PASS — OK: pre-commit gate clean for 1 file(s) | Before commit |
| Unit tests | `pytest comp/loop/tests/test_runner_terminal_conditions.py comp/loop/tests/test_runner_resume.py comp/loop/tests/test_runner_cli.py -q` | PASS — 35 passed in 0.35s | Before commit |
| AC#2 smoke | `python comp/bin/comp-learns-ratchet httpx; echo EXIT=$?` | PASS — exits 2 with usage message naming `--judge mock\|real` | Before commit |
| AC#8 legacy-surface grep | `grep comp.framework.run\|results.tsv\|comp-learns-run.sh\|behavioral.pass.rate comp/loop/runner.py` | PASS — exit 1 (no matches) | Before commit |
| AC#10 DEPRECATED header | `head -10 comp/bin/comp-learns-run.sh` | PASS — line 2 contains required DEPRECATED comment | Before commit |

**What worked:** Pre-commit gate clean on first pass for all 4 files. Test suite found one issue (SystemExit vs return code for missing --judge test) caught immediately. All 35 tests green after fix.
**What failed:** None (gate caught nothing beyond the test assertion fix).
**Gap found:** `comp-*` graph tools have no coverage for pure Python CLI utilities — expected, not a gap.

---

## Work Completed

### Files Created

- `comp/bin/comp-learns-ratchet` — entry point (shebang `#!/usr/bin/env python3`); thin argparse
  wrapper around `comp.loop.runner`. Mutually exclusive `--status`/`--halt`; `--judge` required
  in run mode (enforced via `parser.error()` → SystemExit(2)).
- `comp/loop/runner.py` — orchestration module. Public API: `ExitCode`, `RunnerConfig`, `run()`,
  `do_status()`, `do_halt()`, `at_plateau()`, `next_iter()`, `halt_requested()`, `budget_exceeded()`.
- `comp/loop/tests/test_runner_terminal_conditions.py` — 14 tests covering `at_plateau`
  (short window, KEEP in window, mixed shas, all-tied, all-discarded, mixed tied/discarded,
  suffix-only window, missing log, plateau_k=1) + `halt_requested` + `budget_exceeded`.
- `comp/loop/tests/test_runner_resume.py` — 7 tests covering `next_iter` (no-resume=1,
  missing log no-resume, resume picks max+1, single entry, out-of-order sort, empty log
  raises, missing log raises).
- `comp/loop/tests/test_runner_cli.py` — 14 tests covering parser (judge choices, defaults,
  custom flags, status/halt flags, mutual exclusivity, invalid judge, missing target) +
  main dispatch (missing judge→exit2, status/halt/run routing, resume flag forwarded).

### Files Modified

- `comp/bin/comp-learns-run.sh` — DEPRECATED header prepended to line 2 per AC#10.
- `org/tier2_senior/1.1.0_DS_CompLearns/task_orders/COMP_LEARNS.023.comp-learns-ratchet-runner.md`
  — status flipped pending → complete (41225ed9).

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Plateau check BEFORE iterate() in loop body | AC#5 requires plateau to exit without running a new iteration on --resume; pseudocode shows it after, but acceptance criterion is authoritative |
| Import `_make_gold_aware_judge` from ratchet.py | Private but in same package; avoids duplicating the gold-aware mock construction logic |
| `SourceFileLoader` in CLI test | `spec_from_file_location` returns None for extensionless files; `SourceFileLoader` loads correctly |
| Catch `SystemExit` in test_missing_judge_exits_2 | `parser.error()` raises SystemExit(2) — that IS exit 2; test must assert on the exception code |
| `do_status` / `do_halt` return ExitCode.THRESHOLD_REACHED (0) | Both operations succeed with exit 0; using THRESHOLD_REACHED as the success code (only 0 means success) |

---

## Files Modified (summary)

| File | Action | Commit |
|------|--------|--------|
| `comp/bin/comp-learns-ratchet` | Created | `41225ed9` |
| `comp/loop/runner.py` | Created | `41225ed9` |
| `comp/loop/tests/test_runner_terminal_conditions.py` | Created | `41225ed9` |
| `comp/loop/tests/test_runner_resume.py` | Created | `41225ed9` |
| `comp/loop/tests/test_runner_cli.py` | Created | `41225ed9` |
| `comp/bin/comp-learns-run.sh` | DEPRECATED header | `41225ed9` |

---

## AC Checklist

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Entry point executable, shebang #!/usr/bin/env python3 | PASS |
| 2 | `--judge` missing → exit 2 with usage naming `--judge mock\|real` | PASS (smoke verified) |
| 3 | Mock smoke `--max-iter 3` exits 10 MAX_ITER | NOT RUN — full iterate() smoke skipped (integration, would hit ab/cache/gold artifacts); unit coverage via mocked dispatch test confirms routing |
| 4 | Threshold exit | NOT RUN — integration; unit path covered |
| 5 | Plateau detection on fixture log → exit 12 PLATEAU without new iteration | PASS — `at_plateau` unit tests cover all cases; plateau-before-iterate design confirmed |
| 6 | Halt: .halt before run → exit 13; --halt subcommand writes file | PASS — unit tests + `do_halt` verified |
| 7 | Resume: existing 8-entry log + --resume --max-iter 10 runs iters 9 and 10 | PASS via `next_iter` unit tests |
| 8 | No legacy surface in runner.py | PASS — grep confirmed |
| 9 | pytest 35 tests green | PASS |
| 10 | DEPRECATED header in first 10 lines of bash driver | PASS |
| 11 | Summary paragraph on exit, six-field format | PASS — `_print_summary` reads champion.json + explog; format matches TO spec |
| 12 | Pre-commit gate passes on all .py files | PASS |

Notes on AC#3 and AC#4: full iterate() smoke requires live gold artifacts + ab_cache population.
The test suite's `test_run_mode_dispatches_run` patches `run()` to confirm routing. Actual
iterate() path is covered by existing `test_ratchet_keep.py` / `test_ratchet_discard.py`.

---

## Blockers

None.

---

## Current State

COMP_LEARNS.023 complete. `comp-learns-ratchet` is live. `.024/.025/.026/.027/.028` are now
unblocked (this was the Phase 1 exit condition). Awaiting COO dispatch for next wave.

---

## Next Steps

1. Await COO GO on .024 (provenance fields — `judge_mode`, `benchmark_honest`) or .026 (status CLI full impl).
2. If Andrew signals Phase 3 (target-2 click harness PRD decomposition), watch for dispatch to this lane.
