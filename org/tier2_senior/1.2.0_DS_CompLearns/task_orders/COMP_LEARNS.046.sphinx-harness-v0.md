<task_order>
  <metadata>
    <id>1.2.0_DS_CompLearns-2026-04-22-comp-learns-046-sphinx-harness-v0</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.2.0_DS_CompLearns</issued_to>
    <date>2026-04-22</date>
    <status>pending <!-- GO'd on dispatch --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — prerequisite for .040 (Case 3 packet); .040 cannot begin until this ships</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_BACKLOG_V1.md §6 (source hierarchy — SWE-bench filter) + §7 (Case 3 = sphinx approved by CTO)</ref>
    <ref type="backlog_entry">comp/backlog/benchmark/bl-sweb-002.yaml — sphinx-doc__sphinx-10449, baseline_commit 36367765fe780f962bba861bf368a765380bbc68</ref>
    <ref type="precedent">comp/targets/click/ (built by 1.2.0_DS in .036) — canonical reference structure; mirror</ref>
    <ref type="precedent">comp/targets/httpx/ — canonical template for compiler.py</ref>
    <ref type="cto_decision">MCP 1.1.0_SA_CTO 20260422T approximately 1720Z — ".046 as a dedicated sphinx harness-authoring TO. Route to 1.2.0_DS"</ref>
  </references>

  <objective>
    Build comp/targets/sphinx/ harness v0 — the sphinx target parallel to comp/targets/httpx/
    and comp/targets/click/. This is a structural scaffold task: create the directory,
    compiler.py, gold/ stubs, and repo_pin.txt. No gold survey execution required.

    Explicitly in scope:

    1. comp/targets/sphinx/__init__.py — empty file (package marker).

    2. comp/targets/sphinx/compiler.py — clone comp/targets/click/compiler.py structure
       exactly (or httpx/compiler.py, whichever you find cleaner). Change module docstring
       to reference sphinx. `compile(target_root: Path) -> Graph`. Same
       ImportsSubtype → GraphBuilder → Graph pipeline. No logic changes from the existing
       pattern.

    3. comp/targets/sphinx/repo_pin.txt — single line:
       `36367765fe780f962bba861bf368a765380bbc68`
       (matches bl-sweb-002.yaml baseline_commit; matches SWE-bench sphinx-doc__sphinx-10449 base_commit)

    4. comp/targets/sphinx/gold/ directory with stub files (mirror click):
       - target_version.txt: placeholder (sha256=pending, computed_at=pending, inputs=pending)
       - ab_questions.yaml: empty list (questions: [])
       - ab_answer_key.yaml: empty list (answers: [])
       - test_compiler_sphinx.py: minimal smoke test that compile(Path) returns a Graph
         (mirror test_compiler_click.py if present in gold/)

    5. pytest comp/ -q passes (no regressions). No new tests required beyond the smoke test
       in gold/. Existing compiler/subtype infrastructure tests should continue to pass.

    6. ds-commit-gate.sh on compiler.py + any Python file before commit.

    Explicitly out of scope:
    - Running a gold survey against sphinx repo (pilot runner scope, not harness scope).
    - Populating ab_questions.yaml or ab_answer_key.yaml with real questions (stub is sufficient
      for this TO; .040 + downstream may populate).
    - Building comp/targets/sphinx/_repo/ (the DS condition_b runners will clone sphinx at
      baseline_commit themselves — harness only needs compiler.py to be importable + callable).
    - Any changes outside comp/targets/sphinx/.
    - Exposing gold patch content (SWE-bench `patch` or `test_patch` fields — CTO-held).
    - Modifying bl-sweb-002.yaml or BACKLOG.md — those are already in place.
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-build</run>
        <expect>Clean rebuild.</expect>
        <if_mismatch>Surface to COO — likely concurrent edit. Do not proceed.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/ -q</run>
        <expect>Baseline GREEN (the 9 pre-existing reds are accepted baseline; document count before start).</expect>
        <if_mismatch>If NEW reds appear relative to the 9 baseline, rebase on current CLOUD + investigate before starting.</if_mismatch>
      </step>
      <step>
        <run>ls comp/targets/click/ comp/targets/httpx/</run>
        <expect>Both harnesses present with compiler.py + gold/ subtree — confirms template availability.</expect>
        <if_mismatch>Investigate; templates must be present before mirroring.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -c "from comp.targets.sphinx.compiler import compile; print('import ok')"</run>
        <expect>Prints "import ok" — confirms package + compile() importable.</expect>
        <if_mismatch>Fix import path / __init__.py / compiler.py before commit.</if_mismatch>
      </step>
      <step>
        <run>cat comp/targets/sphinx/repo_pin.txt</run>
        <expect>Single line: 36367765fe780f962bba861bf368a765380bbc68</expect>
        <if_mismatch>Correct the pin.</if_mismatch>
      </step>
      <step>
        <run>ls comp/targets/sphinx/gold/</run>
        <expect>target_version.txt + ab_questions.yaml + ab_answer_key.yaml + test_compiler_sphinx.py all present.</expect>
        <if_mismatch>Add missing files per scope item 4.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh comp/targets/sphinx/compiler.py comp/targets/sphinx/__init__.py comp/targets/sphinx/gold/test_compiler_sphinx.py</run>
        <expect>Exit 0 — py_compile clean + AST undefined-name scanner clean.</expect>
        <if_mismatch>STOP. Fix each issue. Do not commit until clean.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/ -q</run>
        <expect>No NEW reds vs Phase 1 baseline. Pre-existing 9 reds unchanged.</expect>
        <if_mismatch>Investigate + fix.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-build</run>
        <expect>Clean rebuild post-commit.</expect>
        <if_mismatch>Surface to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>.040 (Case 3 task packet, 1.3.0_DS) directly depends on this harness. Once .046 ships, I GO .040 to 1.3.0. .040's TO already references comp/targets/sphinx/ as a prerequisite (see .040 operational_notes). Do NOT touch comp/tasks/case-003-* — that is 1.3.0's scope under .040. This TO only builds the target harness.</note>
    <shared_artifacts>comp/targets/sphinx/** (created by this TO); referenced read-only by .040 + downstream Case 3 runners</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/targets/sphinx/__init__.py exists (empty).
    2. comp/targets/sphinx/compiler.py exists; `from comp.targets.sphinx.compiler import compile` works; ds-commit-gate.sh clean.
    3. comp/targets/sphinx/repo_pin.txt contains exactly `36367765fe780f962bba861bf368a765380bbc68`.
    4. comp/targets/sphinx/gold/ exists with target_version.txt + ab_questions.yaml + ab_answer_key.yaml + test_compiler_sphinx.py (all stubs acceptable).
    5. pytest comp/ -q: no NEW reds vs baseline (9 pre-existing accepted).
    6. Commit --only --author=1.2.0_DS_CompLearns@opal.agent -- comp/targets/sphinx/**
    7. Pushed to CLOUD.
    8. Session log at org/tier2_senior/1.2.0_DS_CompLearns/logs/2026-04-22/ with Compiler Tools section.
    9. MCP COMPLETE to 2.1.0_SA_COO with commit sha — authorizes .040 (Case 3 packet) GO to 1.3.0_DS.
  </acceptance_criteria>

  <dependencies>
    - No blocking upstream — .039 shipped, bl-sweb-002 approved, baseline_commit resolved.
    - Unblocks: .040 (Case 3 packet authoring by 1.3.0_DS).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb. Confirm pwd.
    - Mirror comp/targets/click/compiler.py (your prior .036 work) — familiar ground.
    - sphinx is a substantially larger repo than httpx/click; that's fine for the harness
      scaffold since we're not compiling sphinx at this TO — just making comp.targets.sphinx
      a valid importable package with a compile(Path) signature.
    - Do NOT clone sphinx's _repo/ as part of this TO. The harness is structural only.
    - If the click template has no test_compiler_click.py in gold/, use httpx/gold/ as the
      reference. If neither has one, mirror the minimal smoke-test pattern from any existing
      target's gold/ subtree.
    - No emojis anywhere (CLAUDE.md Code Quality).
  </operational_notes>

  <closeout>
    On completion:
    - commit with --only --author="1.2.0_DS_CompLearns &lt;1.2.0_DS_CompLearns@opal.agent&gt;" -- comp/targets/sphinx/...
    - push to CLOUD
    - flip TO status to complete with commit ref
    - MCP COMPLETE to 2.1.0_SA_COO with sha — this triggers .040 GO immediately
    - session log with Compiler Tools section
  </closeout>
</task_order>
