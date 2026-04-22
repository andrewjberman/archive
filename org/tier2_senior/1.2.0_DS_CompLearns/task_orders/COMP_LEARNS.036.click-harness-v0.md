<task_order>
  <metadata>
    <id>1.2.0_DS_CompLearns-2026-04-22-comp-learns-036-click-harness-v0</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.2.0_DS_CompLearns</issued_to>
    <date>2026-04-22</date>
    <status>complete <!-- aabc9fe1 (compiler+tests) + 61c0da75 (repo_pin+gold stubs) — 2026-04-22 --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — gates condition_b Case 2 (Runs 7+8) for both 1.1.0_DS and 1.3.0_DS; blocks pilot completion</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_PARALLELIZATION_V1.md §8 (target harness structure) + §13 (Case 2 click refactor backlog entry)</ref>
    <ref type="existing_target">comp/targets/httpx/ — canonical reference implementation; mirror this structure exactly</ref>
    <ref type="backlog_entry">comp/backlog/bl-click-001.yaml — Case 2 click refactor, archetype: refactor_invariant_preservation, baseline_commit: f80cf4b09fbe36099b7bfc065fbde30d053da46d</ref>
    <ref type="task_packet">comp/tasks/case-002-click-refactor/packet.yaml — SC-authored Case 2 packet; 5 ACs</ref>
  </references>

  <objective>
    Build comp/targets/click/ harness v0 — the click target parallel to comp/targets/httpx/.
    This is a structural scaffold task: create the directory, compiler.py, gold/ stubs, and
    repo_pin.txt. No gold survey execution required. Condition_b Case 2 runs (Runs 7+8) are
    blocked until this harness exists and pytest comp/ passes.

    Explicitly in scope:
    1. comp/targets/click/__init__.py — empty file (package marker).
    2. comp/targets/click/compiler.py — clone httpx compiler.py structure exactly. Change
       module docstring to reference click. compile(target_root: Path) -> Graph. Same
       ImportsSubtype -> GraphBuilder -> Graph pipeline. No logic changes from httpx pattern.
    3. comp/targets/click/repo_pin.txt — single line: f80cf4b09fbe36099b7bfc065fbde30d053da46d
    4. comp/targets/click/gold/ directory with stub files:
       - target_version.txt: placeholder (sha256=pending, computed_at=pending, inputs=pending)
       - ab_questions.yaml: empty list (questions: [])
       - ab_answer_key.yaml: empty list (answers: [])
    5. pytest comp/ -q passes (no regressions). If new tests are needed for the click target
       module, add the minimum required. More likely: no new tests needed — existing suite covers
       the compiler subtype infrastructure.
    6. ds-commit-gate.sh on compiler.py before commit.

    Explicitly out of scope:
    - Running a gold survey against click repo (that is pilot runner scope, not harness scope)
    - Populating ab_questions.yaml or ab_answer_key.yaml with real questions (stub is sufficient)
    - Building comp/targets/click/_repo/ (the DS condition_b runners will clone click at baseline
      commit themselves — the harness only needs compiler.py to be importable and callable)
    - Any changes outside comp/targets/click/
  </objective>

  <acceptance_criteria>
    1. comp/targets/click/__init__.py exists (empty).
    2. comp/targets/click/compiler.py exists; compile(Path) -> Graph importable; ds-commit-gate.sh clean.
    3. comp/targets/click/repo_pin.txt contains f80cf4b09fbe36099b7bfc065fbde30d053da46d.
    4. comp/targets/click/gold/ exists with target_version.txt, ab_questions.yaml, ab_answer_key.yaml (stubs OK).
    5. pytest comp/ -q green (no regressions).
    6. Commit --author=1.2.0_DS_CompLearns; push to CLOUD.
    7. MCP COMPLETE to 2.1.0_SA_COO with commit sha.
  </acceptance_criteria>

  <dependencies>
    - No blocking dependencies. Execute immediately.
    - Unblocks: condition_b Case 2 GO to 1.1.0_DS and 1.3.0_DS (Runs 7+8).
  </dependencies>

  <operational_notes>
    - Operate from feature_clb/ worktree (C:/Users/AndrewBerman/Desktop/feature_clb). Confirm pwd.
    - Reference: comp/targets/httpx/compiler.py is the canonical template — copy and adapt.
    - Do NOT attempt to clone or access the click _repo. The harness only needs to be structurally
      present and importable. Runners will bring their own target source during condition_b execution.
    - ds-commit-gate.sh on compiler.py before commit.
    - Single commit for all files is fine.
  </operational_notes>

  <closeout>
    On completion:
    - commit with --author="1.2.0_DS_CompLearns &lt;1.2.0_DS_CompLearns@opal.agent&gt;"
    - push to CLOUD
    - flip TO status to complete with commit ref
    - MCP COMPLETE to 2.1.0_SA_COO with sha — this triggers Run 7+8 GOs immediately
    - session log under org/tier2_senior/1.2.0_DS_CompLearns/logs/2026-04-22/
  </closeout>
</task_order>
