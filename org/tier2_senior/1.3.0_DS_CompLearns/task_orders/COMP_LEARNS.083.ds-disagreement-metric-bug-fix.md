<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-083-ds-disagreement-metric-bug-fix</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.3.0_DS_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — CVO Q1 V1.2 acceptance gate; blocks V1.2→V1.3 PRD sync + Path B sub-PRD authoring</priority>
  </metadata>

  <references>
    <ref type="cto_brief">CTO MCP 20260427T20:50Z to COO -- "CVO P0 BUG FIX -- disagreement metric semantics (.077 follow-on)"</ref>
    <ref type="cvo_ruling">CVO ruling: V1.2 NOT fully closed pending disagreement-metric semantics fix. Per Andrew direction, sequencing: .083 fix → V1.2→V1.3 PRD sync (CTO) → Path B sub-PRD authoring (COO).</ref>
    <ref type="prior_work">.077 (dbb30c32) -- your dual-output grader emission shipped 494 tests; this TO is a narrow follow-on bug fix</ref>
    <ref type="bug_locations">comp/loop/runner.py lines 300, 585-587 (narrow disagreement formula); line 595 (correct semantic_correct counter); line 590 (downstream sidecar.semantic.graded record)</ref>
  </references>

  <objective>
    Fix the disagreement-metric semantics bug at runner.py emission sites. The bug treats
    `semantic-correct-but-unparseable` as semantically wrong for the disagreement flag, which
    contradicts the runner's own correct definition at line 595 and the V1.2 motivating examples
    (click q11, sphinx 8-of-10).

    This is ~10-15 lines + 1 new test. Fast turnaround.

    ## Phase 0 — Pre-fix gate

    ```bash
    python -m pytest comp/ --ignore=comp/targets -q --tb=no 2>&1 | tail -3
    # Expect: 494 passed (post-.077 baseline). Zero failures.
    ```

    ## Phase 1 — Refactor: extract helper

    Add to comp/loop/runner.py (or wherever fits cleanly — top of file or shared utility module):

    ```python
    def _semantic_grade_correct(label: str) -> bool:
        """Source of truth for semantic-aware grading correctness.

        A response is semantically correct if the judge produced the right answer,
        whether or not the exact-match grader could parse it. Used to compute the
        disagreement flag against exact-match grader output.
        """
        return label in {"parseable-correct", "semantic-correct-but-unparseable"}
    ```

    ## Phase 2 — Apply at all emission sites

    **Line 300 (pilot path):** replace
    ```python
    disagreement = (exact_pass and semantic_label != "parseable-correct") or (
        not exact_pass and semantic_label == "parseable-correct")
    ```
    with
    ```python
    semantic_grade_correct = _semantic_grade_correct(semantic_label)
    disagreement = (exact_pass != semantic_grade_correct)
    ```

    **Lines 585-587 (sidecar/scorecard path):** same replacement.

    **Line 595 (semantic_correct counter):** route through helper:
    ```python
    semantic_correct += int(_semantic_grade_correct(semantic_label))
    ```
    (behavior preserved; consistency improved)

    **Line 590 (sidecar `semantic.graded` field):** sanity-check that the recorded value matches
    `semantic_grade_correct(label)` directly. The CTO brief notes: "Under the buggy narrow rule,
    semantic-correct-but-unparseable + exact_fail records graded=False (wrong). The fix to the
    disagreement rule automatically corrects this downstream because `not disagreement →
    graded=exact_pass` is only meaningful when both graders agree."

    Verify by reading the code path carefully. If line 590 still produces incorrect values for
    semantic-correct-but-unparseable + exact_fail after the line 585 fix, replace with direct
    `semantic_grade_correct` value:
    ```python
    "semantic": {"graded": _semantic_grade_correct(semantic_label), ...}
    ```

    ## Phase 3 — Add runtime test

    Per Andrew direction (tighten beyond unit grader behavior): test that exercises the FULL
    runner emission path with the canonical click q11 pattern.

    Place at: `comp/loop/tests/test_grader_governance_emission.py`

    Test scenario: exact_fail + semantic_label="semantic-correct-but-unparseable"

    Verify:
    1. Emitted disagreement flag is True
    2. Sidecar entry's `semantic.graded` is True
    3. grader_governance counters increment `semantic_aware_correct`
    4. `disagreement_count` increments

    Use mocks/stubs as needed to avoid full ratchet run; the test must exercise the emission
    code path that produces these fields.

    ## Phase 4 — Pre-commit gate

    ```bash
    .tools/ds-commit-gate.sh comp/loop/runner.py
    # If new test file: .tools/ds-commit-gate.sh comp/loop/tests/test_grader_governance_emission.py
    ```

    ```bash
    python -m pytest comp/ --ignore=comp/targets -q --tb=short 2>&1 | tail -5
    # Expect: 494+ passed (494 baseline + new test). 0 failures.
    ```

    ## Phase 5 — Commit and push

    ```bash
    git commit --only \
      --author="1.3.0_DS_CompLearns <1.3.0_DS_CompLearns@opal.agent>" \
      -m "fix(COMP_LEARNS.083): disagreement metric semantics -- semantic-correct-but-unparseable counts as semantically correct (CVO P0)" \
      -- comp/loop/runner.py \
         comp/loop/tests/test_grader_governance_emission.py
    git push origin CLOUD
    ```

    ## Phase 6 — MCP

    MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO with:
    - Commit sha
    - Confirmation: helper extracted, all 4 sites consistent
    - Test count (494+ baseline + new runtime test)
    - Sample test output confirming the click q11 / sphinx 8-of-10 pattern produces the right disagreement flag now

    ## Historical data NOT re-run (per CTO brief)

    - .082 pilot artifacts (sphinx q03/q05): all responses parseable-wrong, correct disagreement
      under buggy rule too. No re-pilot.
    - dev-click-001/iter1 sidecar: smoke artifact, not benchmark. No re-run.
    - SC .075 sphinx pre-screen: did not use the runner.py emission path. No re-prescreen.
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>python -m pytest comp/ --ignore=comp/targets -q --tb=no 2>&amp;1 | tail -3</run>
        <expect>494 passed. Zero failures.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh comp/loop/runner.py</run>
        <expect>All 3 checks exit 0.</expect>
      </step>
      <step>
        <run>python -m pytest comp/ --ignore=comp/targets -q --tb=short 2>&amp;1 | tail -5</run>
        <expect>494+ passed (with new runtime test). 0 failures.</expect>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    1. _semantic_grade_correct(label) helper extracted as source of truth.
    2. All four emission sites (lines ~300, ~585-587, ~590, ~595) consistent: route through helper.
    3. Disagreement formula: disagreement = (exact_pass != _semantic_grade_correct(semantic_label)).
    4. New runtime test in comp/loop/tests/test_grader_governance_emission.py covering canonical click q11 pattern (exact_fail + semantic-correct-but-unparseable).
    5. ds-commit-gate.sh exits 0.
    6. pytest 494+ baseline + new runtime test, 0 failures.
    7. Committed --only --author=1.3.0_DS_CompLearns. Pushed to CLOUD.
    8. MCP COO + CC CTO with commit sha + test confirmation.
  </acceptance_criteria>

  <dependencies>
    - GATE: blocks V1.2→V1.3 PRD sync (CTO) and Path B sub-PRD authoring (COO).
    - CVO Q1 V1.2 acceptance: P0 NOT-ACCEPTED → P0 ACCEPTED upon merge.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - Narrow scope. ~10-15 LOC + 1 test. Fast turnaround expected.
    - Do NOT change exact-match grader behavior or champion selection logic.
    - Do NOT introduce a new label or change R-SC-2 taxonomy semantics.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO with commit sha + test confirmation
    - session log
  </closeout>
</task_order>
