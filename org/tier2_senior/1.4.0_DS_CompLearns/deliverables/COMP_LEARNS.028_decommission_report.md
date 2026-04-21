# COMP_LEARNS.028 — Legacy Loop Decommission Report

**Author:** 1.4.0_DS_CompLearns  
**Date:** 2026-04-21  
**TO:** COMP_LEARNS.028 (legacy-loop-decommission)  
**Phase:** 1 — Inventory (pre-deletion audit trail)

---

## Inventory Grep

Surfaces scanned: `comp/`, `docs/`, `org/`  
Patterns: `comp-learns-run\.sh`, `comp\.framework\.run`, `from comp\.framework import run`, `results\.tsv`, `COMP_LEARNS_OPERATIONAL_MANDATE`

### Binary Files / Entry Points

| File | Line | Reference | Disposition |
|------|------|-----------|-------------|
| `comp/bin/comp-learns-run.sh` | entire | Legacy bash driver (486 lines); DEPRECATED header at line 2; quarantine gate at line 127 requiring `--legacy` flag; delegates `--once` to `comp.loop.ratchet`; `--legacy` mode invokes `comp.framework.run` | DELETE |
| `comp/bin/comp-learns-run` | line 43 | `exec "${PYTHON}" -m comp.framework.run "$@"` — thin forwarder | DELETE |
| `comp/bin/comp-learns-status` | line 33 | `exec "${PYTHON}" -m comp.framework.status "$@"` — thin forwarder | DELETE (superseded by `comp-learns-ratchet --status`) |

### comp/framework/ Python Modules

| File | Live non-legacy callers outside framework? | Disposition |
|------|------------------------------------------|-------------|
| `comp/framework/run.py` | None | DELETE |
| `comp/framework/results_schema.py` | None (only `comp/framework/tests/test_status.py`) | DELETE |
| `comp/framework/plateau.py` | None (only `comp/framework/status.py`) | DELETE |
| `comp/framework/status.py` | None (only `comp/framework/tests/test_status.py`) | DELETE |
| `comp/framework/branch_guard.py` | None (only `comp/framework/tests/test_branch_guard.py`) | DELETE |
| `comp/framework/compiler_baseline.py` | None (only `comp/framework/tests/test_compiler_baseline.py`) | DELETE |
| `comp/framework/compiler_contract.py` | None (only `comp/framework/tests/test_compiler_baseline.py`) | DELETE |
| `comp/framework/extractor_interface.py` | None (only `comp/framework/tests/test_compiler_baseline.py`) | DELETE |
| `comp/framework/query_schema.py` | None (only `comp/framework/tests/test_benchmark_sop.py`) | DELETE |
| `comp/framework/harness_base.py` | YES — `comp/bench/behavioral.py:22` deferred import; `comp/loop/ratchet.py:31` imports `score_from_harness_result` from behavioral | **KEEP** (Layer-A behavioral harness, live non-legacy caller) |
| `comp/framework/__init__.py` | Required for package | **KEEP** (minimal; framework package needed while harness_base.py lives here) |

### comp/framework/tests/

| File | Disposition |
|------|-------------|
| `comp/framework/tests/test_status.py` | DELETE (tests deleted module) |
| `comp/framework/tests/test_plateau.py` | DELETE |
| `comp/framework/tests/test_harness_base.py` | DELETE (tests live module, but test file has no coverage value post-decommission; harness_base itself stays) |
| `comp/framework/tests/test_compiler_baseline.py` | DELETE |
| `comp/framework/tests/test_branch_guard.py` | DELETE |
| `comp/framework/tests/test_benchmark_sop.py` | DELETE |
| `comp/framework/tests/__init__.py` | DELETE (empty package file) |

### results.tsv

`find comp/targets -name "results.tsv"` → **empty** (no results.tsv files exist on disk). No action needed.

### Docs (Phase 3 — HOLD)

| File | Reference | Disposition (Phase 3 — HOLD until .027b) |
|------|-----------|------------------------------------------|
| `comp/OPERATING.md` | All examples reference `comp-learns-run.sh` | Rewrite to use `comp-learns-ratchet` |
| `comp/README.md` | `results.tsv` reference in target dir diagram | Remove reference |
| `comp/prompts/iter.md` | `python -m comp.framework.run`, `results.tsv` | Update to `comp-learns-ratchet` + `experiment_log.jsonl` |
| `comp/prompts/README.md` | `comp-learns-run.sh` driver reference | Update |
| `docs/architecture/COMP_LEARNS_OPERATIONAL_MANDATE.md` | Entire doc describes v0 bash-driver loop | Prepend HISTORICAL header |
| `docs/architecture/COMP_LEARNS_LOOP_ORCHESTRATOR.md` | Entire doc describes v0 loop orchestration | Prepend HISTORICAL header |
| `org/tier2_senior/1.*_DS_CompLearns/prompt.md` | Potential `comp-learns-run` references | Grep + replace with `comp-learns-ratchet` |

### comp/AUTORESEARCH_WALKTHROUGH.md

Multiple references to `results.tsv`, `comp/bin/comp-learns-run.sh`, `comp.framework.run`. This is an architectural walkthrough doc — historical context, not active guidance. Disposition: **leave as-is** (same as `org/*/logs/` — history, not instructions). Doc accurately describes the v0 design Karpathy walkthrough; value is preserved.

---

## Unique Behaviors in comp-learns-run.sh NOT in comp-learns-ratchet

### At Phase 2 commit:
- `--show-scorecard`, `--show-log`, `--show-diff` subcommands: **MIGRATED** — added as `--show-scorecard`, `--show-log`, `--show-diff` flags to `comp-learns-ratchet` (thin dispatch to existing `comp/bin/show_*.py` modules; no logic rewrite). COO disposition: option (a).

### Dropped with legacy loop (not gaps):
- Git worktree isolation for parallel target runs (`--legacy` mode only)
- SIGTERM handler + SUMMARY.md generation (`--legacy` mode only)
- Per-iteration `flock` + `ulimit -v` + `timeout` resource capping (`--legacy` mode only)
- `state.json` cache writes (superseded by `champion.json` + `experiment_log.jsonl`)

---

## No QUARANTINE path needed

All deleted surfaces have clean delete paths — no live non-legacy code will break. `comp/framework/harness_base.py` survives at its existing path.

---

## Phase Boundaries

| Phase | Status | Gate |
|-------|--------|------|
| 0 — Inventory grep | DONE | pre-work |
| 1 — Inventory commit (this doc) | DONE | CTO + COO GO 2026-04-21 |
| 2 — DELETE execution + show_* migration | IN PROGRESS | same GO |
| 3 — Doc migration + HISTORICAL headers | HOLD | .027b closes green |
| 4 — RUNTIME_V1.md "Realized" + COMP_LEARNS.json | HOLD | .027b closes green |
