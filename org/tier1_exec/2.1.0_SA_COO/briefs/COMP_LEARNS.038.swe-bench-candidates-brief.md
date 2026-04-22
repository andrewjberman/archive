# COMP_LEARNS.038 — SWE-bench Verified Case 3 Candidates (COO execution brief)

**Owner:** 2.1.0_SA_COO (self-execution, no external DS TO)
**Date authored:** 2026-04-22
**Gate:** .037 (backlog dual-lane rebuild) COMPLETE — need comp/backlog/benchmark/ directory to exist before committing candidates
**Downstream gate:** .039 (CTO approves 1 of the 3 candidates; also authors Case 4 + dev seeds)

## Purpose

Per BACKLOG_V1 §7 + handoff session13, COO downloads SWE-bench Verified, filters to
Python repos with `harness_relevance >= 3` + `aided_unaided_safe = true`, proposes 3
Case 3 candidates as `bl-sweb-*.yaml` entries in `comp/backlog/benchmark/`.

## Constraint (§7)

Case 3 MUST NOT be from httpx or click (target familiarity bias — pilot wave 1 already
covered both).

## Execution steps

1. Verify .037 COMPLETE (directory + schema landed); confirm comp/backlog/benchmark/ exists.

2. Download SWE-bench Verified:
   ```python
   from datasets import load_dataset
   ds = load_dataset("SWE-bench/SWE-bench_Verified")
   ```
   Filter to language=python. ~500 instances expected.

3. Apply COMP_LEARNS filters per BACKLOG_V1 §6:
   - Python only
   - Publicly cloneable with pinnable commits (all SWE-bench verified are)
   - Test suite runs in <5 min (check `test_cmd` + prior CI signals if available)
   - `harness_relevance >= 3` (judgment call per case — needs the bug to be plausibly
     findable via compiler-graph edge traversal; rate 1-5 per §3 + §5 archetype fit)
   - `aided_unaided_safe = true` (the comparison must not be confounded — e.g. bugs
     whose gold patch is primarily a prose/docs change are NOT aided-unaided-safe)
   - NOT httpx, NOT click

4. Rank candidates by expected harness leverage (Archetype A or D preferred — both
   stress compiler edge resolution cleanly).

5. Pick top 3. Author 3 `bl-sweb-{NNN}.yaml` files in `comp/backlog/benchmark/` with
   status: candidate. Each file must include ALL §3 required fields:
   - case_id: bl-sweb-001, bl-sweb-002, bl-sweb-003
   - lane: benchmark
   - swe_bench_id: SWE-bench instance_id
   - baseline_commit: SWE-bench base_commit
   - target: repo name (e.g. "psf/requests")
   - archetype: A or D (pick best fit per §5)
   - measurement_axes: per archetype
   - harness_relevance: 3, 4, or 5
   - aided_unaided_safe: true
   - ac_type: test_suite
   - status: candidate
   - notes: why this case, what archetype-specific behavior it exercises

6. Append rows to comp/backlog/BACKLOG.md index (3 new benchmark rows).

7. Commit + push. Author = 2.1.0_SA_COO.

8. MCP CTO for .039 lane — here are the 3 candidates, please approve ONE + author
   Case 4 + dev seeds.

## Success criteria (self-gate)

- 3 bl-sweb-*.yaml files exist in comp/backlog/benchmark/, all status: candidate
- BACKLOG.md index updated with 3 rows
- MCP to CTO sent
- Commit pushed to CLOUD with --only pathspec scoped to comp/backlog/benchmark/** + BACKLOG.md

## Out of scope

- Choosing Case 3 (CTO picks 1 of 3 in .039)
- Authoring task packet (.040 by 1.3.0_DS after CTO approval)
- Authoring harness for the chosen repo (separate TO if the target repo doesn't
  already have a comp/targets/ harness — likely needed; flag to CTO in the .039 MCP)
- Exposing `patch` or `test_patch` fields from SWE-bench (gold data, CTO-held)

## Compiler tools log

`comp-build` + `pytest comp/ -q` at start (baseline) + end (no regression).
Append to org/compiler-tools-log.md.

## Notes

- If local HuggingFace cache isn't set up, first run: `huggingface-cli login` (Andrew
  must have done this previously; if not, MCP him; this is the one step I cannot
  autonomously bootstrap).
- SWE-bench Verified is ~500 Python instances; filtering to harness_relevance>=3 +
  aided_unaided_safe will likely shortlist 30-80. Pick top 3 by archetype fit, not
  just highest harness_relevance.
- Archetype D (cross-module) cases are rarer in SWE-bench — prioritize if present.
- Do NOT commit the downloaded dataset (parquet files). Read-only consumption.
