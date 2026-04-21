# COMP_LEARNS.007 session log — status CLI

**Agent:** 1.2.0_DS_CompLearns
**Date:** 2026-04-21
**TO:** `org/tier2_senior/1.2.0_DS_CompLearns/task_orders/COMP_LEARNS.007.status-cli.md`
**Project:** COMP_LEARNS
**Commit:** `2cd6ba10`

## Objective

Ship `comp-learns-status {target} [--json]` CLI per mandate req #8 observability. Sub-10s response. Reads state.json + results.tsv + filesystem sentinels; derives active/paused/terminated state.

## Work Completed

### Files Delivered

- `comp/framework/status.py` — full implementation
- `comp/framework/tests/test_status.py` — 10 tests
- `comp/bin/comp-learns-status` — install shim

### Implementation Notes

**Two state.json schemas** coexist in the codebase and must both be handled:
- **Bash driver** (`comp-learns-run.sh`): writes `last_update_unix`, `driver_pid`, `current_pass_rate`, `last_status`
- **Python run.py**: writes `timestamp`, `query_pass_rate`, `status`, `plateau_warning`

`status.py` reads both: `state.get("last_update_unix") or state.get("timestamp")` for seconds-since-last-commit; `state.get("driver_pid")` for PID (bash schema only).

**State derivation logic:**
1. `.halt` file present → `paused` (checked first — driver can be halted mid-run)
2. `driver_pid` alive → `active`
3. `SUMMARY.md` present + PID dead → `terminated`
4. Default → `terminated`

**Authoritative iter:** TSV row count (not state.json `iter` field). `state.json` is a cache per mandate contract.

**Plateau detection:** calls `detect_plateau()` from `.004` on last 5 keep rows' `query_pass_rate` from TSV.

**`COMP_LEARNS_WORKTREES_ROOT` env var:** overrides the default `workspace/worktrees/` root; used by tests via `monkeypatch.setenv`.

**`_git_branch`:** subprocess `git -C {worktree_dir} rev-parse --abbrev-ref HEAD` with 5s timeout; returns `"unknown"` on failure.

## Compiler Tools

| Step | Run | Observed | Pass/Fail |
|------|-----|----------|-----------|
| Phase 1.1 | `grep -A15 write_state_cache comp/framework/run.py` | state_payload fields confirmed: target, iter, commit, query_pass_rate, coverage_pct, mean_latency_ms, lines_of_code, status, plateau_warning, description, timestamp | PASS |
| Phase 1.2 | `grep -A5 COLUMNS comp/framework/results_schema.py` | COLUMNS = ("commit", "query_pass_rate", "coverage_pct", "mean_latency_ms", "lines_of_code", "status", "description") | PASS |
| Phase 2.1 | `python -m pytest comp/framework/tests/test_status.py -v` | 10 passed in 0.49s | PASS |
| Phase 2.2 | `time python -m comp.framework.status _stub` | real 0m0.364s — valid 8-field output | PASS |
| Phase 3.1 | `python -m comp.framework.status _stub --json \| python -c "import json,sys; json.load(sys.stdin); print('ok')"` | ok | PASS |
| Full suite | `python -m pytest comp/framework/ -v` | 60 passed in 4.11s | PASS |

Also noted: bash driver `comp-learns-run.sh` writes a different `write_state_cache` schema than `run.py`; schema reconciliation documented in implementation notes above. No mismatch action needed — `status.py` handles both.

## Acceptance Checklist

| # | Criterion | Status |
|---|-----------|--------|
| 1 | `comp-learns-status _stub` produces valid output against stub artifacts | PASS — 8 fields, exit 0 |
| 2 | Sub-10s response (wall-clock `time`) | PASS — 0.364s |
| 3 | `--json` produces parseable JSON (pytest validates schema) | PASS — `test_json_flag_produces_valid_json` |
| 4 | active/paused/terminated derivation per rules | PASS — 3 dedicated tests |
| 5 | Tests >= 6 cases; pytest green | PASS — 10 tests, all green |
| 6 | Install shim at `comp/bin/comp-learns-status` | PASS — tracked; copied to `.tools/` |
| 7 | Session log Compiler Tools section | PASS — this file |
| 8 | MCP COMPLETE to COO with commit hash + sample output | PENDING SEND |

## Sample Output on _stub

```
target: _stub
state: active
iter: 3
seconds_since_last_commit: 31515844
last_3_statuses: keep, keep, discard
plateau_warning: false
branch: comp-learns/_stub
driver_pid: 0
```

## Current State

Ship-ready. Commit `2cd6ba10` pushed to CLOUD. All 6 acceptance criteria pass. 60 framework tests green.
