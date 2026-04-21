# COMP_LEARNS.019 -- Visualization CLI

**Agent:** 1.1.0_DS_CompLearns
**Date:** 2026-04-21
**TO:** `org/tier2_senior/1.1.0_DS_CompLearns/task_orders/COMP_LEARNS.019.visualization-cli.md`
**Commit:** `22889582`

## Objective

Pretty-print helpers for scorecards + experiment_log, wired as subcommands of `comp-learns-run.sh`.

## Work Completed

4 files (3 created, 1 modified):
- `comp/bin/show_scorecard.py` -- reads latest scorecard JSON, prints structured ASCII table per wire contract
- `comp/bin/show_log.py` -- tails experiment_log.jsonl with KEEP/DISCARD/TIE verdict prefixes
- `comp/bin/show_diff.py` -- metric-level diff between two scorecard JSONs (structural, AB, mutation, subtype deltas)
- `comp/bin/comp-learns-run.sh` -- wired `--show-scorecard`, `--show-log [--last N]`, `--show-diff A B` flags

Note on `--show-diff`: scorecard artifacts do not embed full Graph objects (node/edge lists), so diff is computed from available metrics (structural f1/precision/recall deltas, mutation_stability by type, per-selector AB shifts, subtype set changes). This is the maximum fidelity available from on-disk artifacts without re-running the compiler.

## Compiler Tools

| Phase | Run | Observed | Expected | Result |
|-------|-----|----------|----------|--------|
| 1 | `ls comp/targets/httpx/scorecards/*.json comp/targets/httpx/experiment_log.jsonl` | 2 scorecards + log listed | both present | PASS |
| 2 | `bash comp/bin/comp-learns-run.sh httpx --show-scorecard \| head -30` | 12-line scorecard table, correct format | per wire contract | PASS |
| 2 | ASCII pipe check | `ascii-ok` | `ascii-ok` | PASS |
| 2 | `bash comp/bin/comp-learns-run.sh httpx --show-log --last 2` | iter=4 TIE + iter=5 TIE with delta/sha | last 2 entries | PASS |
| 3 | `bash comp/bin/comp-learns-run.sh httpx --show-scorecard && echo EXIT=$?` | scorecard + EXIT=0 | EXIT=0 | PASS |

## Acceptance Criteria

| AC | Status |
|----|--------|
| 1. `--show-scorecard` prints per wire contract | PASS |
| 2. `--show-log --last 5` tails experiment_log | PASS |
| 3. `--show-diff A B` prints diff summary | PASS |
| 4. No emoji / ASCII-only verified | PASS |
| 5. Exit 0 on missing scorecard/log | PASS |
| 6. Session log Compiler Tools section | PASS (this doc) |
| 7. MCP COMPLETE to COO | PENDING (next) |

## Sample Outputs

**--show-scorecard:**
```
=== Scorecard: httpx @ e8f2c50 2026-04-21 17:56:48 ===
Primary metric:  1.2439
Subtypes:        imports
Structural:      p=0.40 r=1.00 f1=0.5743
Behavioral:      not evaluated
Efficiency:      extract=<1s graph=0B mem=0MB
Downstream AB:   best=random lift=+1.00 tokens_reduced=83%
  - centrality   lift=+1.00  tokens_reduced=83%
  - keyword      lift=+1.00  tokens_reduced=88%
  - random       lift=+1.00  tokens_reduced=83%
Adversarial:     mutation_stability=1.00 (noise=1.00  rename=0.99  reorder=1.00)
Conflict frac:   0.000
```

**--show-log --last 2:**
```
iter=4   TIE     primary=+1.2439  delta=+1.2439  sha=e8f2c50  [adversarial_variants=0]
iter=5   TIE     primary=+1.2439  delta=+0.0000  sha=e8f2c50  [adversarial_variants=0]
```

**--show-diff 6c58f0e_909ea79f.json e8f2c50_909ea79f.json:**
```
=== GraphDiff: 6c58f0e -> e8f2c50 ===
primary_metric:    0.0000 -> 1.2439  (+1.2439)
structural.f1      0.5743 -> 0.5743  (+0.0000)
mutation_stability:0.0000 -> 0.9968  (+0.9968)
  mutation.noise   0.00 -> 1.00  (+1.00)
  mutation.rename  0.00 -> 0.99  (+0.99)
  ...
```
