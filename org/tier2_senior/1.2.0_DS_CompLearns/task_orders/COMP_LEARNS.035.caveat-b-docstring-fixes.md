<task_order>
  <metadata>
    <id>1.2.0_DS_CompLearns-2026-04-21-comp-learns-035-caveat-b-docstring-fixes</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.2.0_DS_CompLearns</issued_to>
    <date>2026-04-21</date>
    <status>complete <!-- f33b2c16 — 2026-04-21 --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — must ship before .032 pilot operationalization; parallel to .030/.031; do NOT block on .030</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_PARALLELIZATION_V1.md §6 (Scorecard.__eq__ constraint) + §8 (ABCache path + git-tracking) — v1.2 at f5be0e7a</ref>
    <ref type="sc_finding">COMP_LEARNS.029 scorer-stability baseline — YELLOW caveats B1/B2/B3 (04e192c5)</ref>
    <ref type="cto_direction">1.1.0_SA_CTO MCP 20260421T220923Z — Track 2 code fixes, 3 docstring edits, no logic change</ref>
  </references>

  <objective>
    Fix three incorrect docstrings in comp/bench/ that misrepresent load-bearing runtime contracts
    discovered by SC in the .029 baseline. No logic changes — docstring corrections only.

    All three are in files you authored or extended in .024 (scorecard.py) and .015/.024 (ab.py).
    You know these files cold. This is a 3-edit, 1-commit task.

    Explicitly in scope:
    1. comp/bench/ab.py — fix ABCache double-nesting docstring: actual path is ab_cache/ab_cache/{key}.json (double-nested), not ab_cache/{key}.json. Find the docstring that describes the cache path and correct it.
    2. comp/bench/ab.py or comp/bench/cache.py — fix "git-tracked" claim: the AB cache is NOT git-tracked. Fresh worktrees start cold and require 114 warm-up API calls for httpx. Find and remove or correct any docstring claim that the cache is git-tracked or pre-populated.
    3. comp/bench/scorecard.py — fix Scorecard.__eq__ docstring: __eq__ excludes judge_model_id AND judge_mode from equality comparison. This constraint is currently undocumented. Add a docstring note naming both excluded fields explicitly and stating why (provenance metadata, not behavioral identity).

    Explicitly out of scope:
    - Any logic changes
    - New tests (existing test suite verifies no regression)
    - Any file outside comp/bench/ab.py, comp/bench/cache.py, comp/bench/scorecard.py
  </objective>

  <acceptance_criteria>
    1. comp/bench/ab.py or comp/bench/cache.py: ABCache path documented as ab_cache/ab_cache/{key}.json (double-nested). Prior incorrect path claim removed or corrected.
    2. comp/bench/ab.py or comp/bench/cache.py: "git-tracked" or equivalent claim removed or corrected to state cache is NOT git-tracked; fresh worktrees start cold.
    3. comp/bench/scorecard.py: Scorecard.__eq__ docstring names judge_model_id AND judge_mode as excluded fields with rationale.
    4. pytest comp/bench/ -q green (no logic changed, should be trivially true).
    5. ds-commit-gate passes on all edited .py files.
    6. Commit --author=1.2.0_DS_CompLearns; push to CLOUD.
    7. MCP COMPLETE to 2.1.0_SA_COO with commit sha + 3-item checklist.
  </acceptance_criteria>

  <dependencies>
    - .033 must complete first (same lane — process sequentially).
    - Does NOT require .030 to complete. Ship independently, in parallel with .030/.031.
    - Must ship before .032 pilot operationalization.
  </dependencies>

  <operational_notes>
    - Operate from feature_clb/ worktree. Confirm pwd before first edit.
    - Read comp/bench/ab.py, comp/bench/cache.py, comp/bench/scorecard.py fully before editing — locate the exact docstrings to fix.
    - ds-commit-gate.sh on all edited .py files before commit.
    - Single commit for all 3 fixes is fine (they are logically related).
    - If you cannot locate the "git-tracked" claim verbatim, search for related language (e.g., "tracked", "committed", "versioned", "repo"). If no such claim exists in docstrings (it may be in a comment only), document that finding in the session log and skip that specific edit.
  </operational_notes>

  <closeout>
    On completion:
    - commit with --author="1.2.0_DS_CompLearns &lt;1.2.0_DS_CompLearns@opal.agent&gt;"
    - flip TO status to complete with commit ref
    - MCP COMPLETE to 2.1.0_SA_COO with sha + 3-item checklist
    - session log under org/tier2_senior/1.2.0_DS_CompLearns/logs/2026-04-21/
  </closeout>
</task_order>
