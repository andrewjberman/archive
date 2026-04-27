<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-079-sc-disagreement-emission</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>complete</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — V1.2 grader-governance ship-blocker (§11.3 R-SC-1 P0); gates on .078</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §11.3 SC requirements (R-SC-1 P0): per-question disagreement emission + per-target disagreement rate</ref>
    <ref type="prereq">.078 (1.3.0_DS_CompLearns) — must be complete before this TO executes; provides dual-output grader output format</ref>
    <ref type="rsc2">comp/results/r_sc_2_semantic_labels.md — R-SC-2 label taxonomy (authored .072)</ref>
    <ref type="prescreen_protocol">comp/results/sphinx/prescreen/prescreen_protocol.md — existing per-question schema (§2.5)</ref>
  </references>

  <objective>
    Implement V1.2 §11.3 SC-side grader-governance emission: per-question disagreement labels
    in pre-screen output and target summary disagreement rate.

    ## Gate — Do NOT start until .078 COMPLETE

    .078 (DS dual-output emission) must be committed and pushed before this TO executes.
    Verify:
    ```bash
    git pull origin CLOUD --ff-only
    python3 -c "from comp.bench.ab import _semantic_grade_response; print('OK')"
    ```
    If _semantic_grade_response is absent: MCP COO and hold.

    ## Context

    After .078 ships, the runner emits both exact_pass and semantic_label per trial. SC must
    update the pre-screen triage procedure and per-question YAML schema to:
    1. Consume the semantic_label from runner output (rather than applying labels manually)
    2. Emit a disagreement_flag per question per regime
    3. Add a per-target disagreement rate to prescreen_summary.yaml

    This TO does NOT re-run the sphinx pre-screen. It:
    - Updates the pre-screen protocol document (comp/results/sphinx/prescreen/prescreen_protocol.md)
    - Amends the §2.5 per-question YAML schema to include disagreement fields
    - Provides the updated prescreen_summary.yaml schema with disagreement_rate field
    - Updates prescreen_protocol.md §3 and §4 accordingly

    The actual sphinx pre-screen re-run with dual-output data is a future TO (sphinx revisit
    or Path B target first use of the governance framework).

    ## Phase 0 — Pull .078 and verify

    ```bash
    git pull origin CLOUD --ff-only
    python3 -c "from comp.bench.ab import _semantic_grade_response; print('OK')"
    ```

    ## Phase 1 — Update §2.5 per-question YAML schema

    Amend the per-question YAML schema in prescreen_protocol.md to add disagreement fields:

    ```yaml
    question_id: qXX
    zero_shot_result:
      grader_label: pass | fail              # exact-match output (primary)
      semantic_label: <R-SC-2 label>         # semantic-aware output
      disagreement: true | false             # exact_pass != semantic_says_correct
    full_source_result:
      grader_label: pass | fail
      semantic_label: <R-SC-2 label>
      disagreement: true | false
    triage_category: INCLUDE | SENTINEL | INVESTIGATE
    include_reason: null
    sentinel_reason: null
    investigate_subtype: null
    pilot_eligible: null
    ```

    The `triage_category` now consumes semantic_label, not grader_label, per §2.3.
    Where grader_label=fail and semantic_label=parseable-correct → disagreement=true;
    triage uses semantic_label.

    ## Phase 2 — Update prescreen_summary.yaml schema

    Add disagreement_rate to prescreen_summary.yaml schema:

    ```yaml
    target: <target>
    date: <ISO8601>
    authored_by: 2.1.0_SC_CompLearns
    question_count: N
    include_count: N
    sentinel_count: N
    investigate_count: N
    pilot_eligible_count: N
    sentinel_review_note: null
    path_a_viable: true | false
    path_b_trigger: null | ...
    grader_governance:
      disagreement_count: N          # questions where exact_pass != semantic_correct in any regime
      disagreement_rate: 0.NN        # disagreement_count / (question_count * 2 regimes)
      grader_artifact_count: N       # questions classified grader_artifact in investigate_subtype
    ```

    ## Phase 3 — Update prescreen_protocol.md

    Amend comp/results/sphinx/prescreen/prescreen_protocol.md:
    - §2 Step 3: note that semantic_label is now sourced from runner dual-output (.078),
      not applied manually
    - §3: update per-question YAML schema to include disagreement fields
    - §4: update prescreen_summary.yaml schema to include grader_governance block
    - Add §8: Disagreement Rate Interpretation — when disagreement_rate > 0.5, flag as
      grader_artifact-dominated target; sentinel_review_note is required regardless of
      sentinel_count (signals that SENTINEL pool is masked by exact-match failure, not
      absent by content)

    ## Phase 4 — Commit and push

    ```bash
    git add comp/results/sphinx/prescreen/prescreen_protocol.md
    git commit --only \
      --author="2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>" \
      -m "doc(COMP_LEARNS.079): SC disagreement emission schema -- V1.2 grader-governance per-question + summary" \
      -- comp/results/sphinx/prescreen/prescreen_protocol.md
    git push origin CLOUD
    ```

    ## Phase 5 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Confirmation that disagreement_flag derivation rule matches .078 implementation
    - Whether any schema decision deviated from TO spec (flag for CTO if so)
    - When the schema is ready for use (sphinx revisit or Path B target first pre-screen)
  </objective>

  <compiler_tools_mandate>
    <note>No Python source changes — document/schema update only. ds-commit-gate.sh not required.
    Gate: .078 must be complete before execution.</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      HARD GATE on .078 (DS dual-output). Pull CLOUD and verify _semantic_grade_response before
      starting. If .078 format deviates from what this TO describes, MCP COO before proceeding.
      .080 (grader_artifact subtype split) is parallel — no dependency.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. .078 confirmed complete (python3 import test passes).
    2. Per-question YAML schema updated to include disagreement fields for both regimes.
    3. prescreen_summary.yaml schema updated to include grader_governance block.
    4. prescreen_protocol.md §3/§4 updated; §8 disagreement rate interpretation added.
    5. Committed --only --author=2.1.0_SC_CompLearns. Pushed CLOUD.
    6. MCP 2.1.0_SA_COO with commit sha + schema confirmation.
  </acceptance_criteria>

  <dependencies>
    - HARD GATE: .078 must be complete before execution.
    - .080 is parallel (no dependency).
    - .077 is parallel (no dependency).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - This TO is schema/document only. The actual disagreement data for sphinx questions requires
      re-running the sphinx pre-screen after .078 ships — that is a future TO, not part of .079.
    - If disagreement derivation rule in .078 differs from what this TO describes, flag before
      adopting any different rule — CTO must approve disagreement semantics.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD
    - MCP 2.1.0_SA_COO
    - session log
  </closeout>
</task_order>
