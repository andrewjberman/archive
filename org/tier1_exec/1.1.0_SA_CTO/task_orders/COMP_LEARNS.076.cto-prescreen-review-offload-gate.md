<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-076-cto-prescreen-review-offload-gate</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.1.0_SA_CTO</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Stage 3 ship-blocker: final gate before primary case dispatch (gates on .075)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §10 — Ship-blocker checklist items 7+8+9: "Sphinx target pre-screen run", "Pre-screen result reviewed; INCLUDE/SENTINEL/INVESTIGATE pools preregistered", "Off-ramp gate evaluated"</ref>
    <ref type="prd_section">§3.1 — Empty-pool rules; §3.3 — Reporting discipline; §7.2 — Path B MANDATORY thresholds; §7.3 — Path B sequencing.</ref>
    <ref type="prescreen_result">comp/results/sphinx/prescreen/ — per-question YAML + prescreen_summary.yaml (authored in .075)</ref>
    <ref type="packet_template">comp/dispatch/stage3_packet_manifest_template.yaml — authored in .073; used for pool preregistration</ref>
    <ref type="path_b_criteria">comp/dispatch/stage3_dispatch_criteria.md — Path B MANDATORY thresholds (authored in .073)</ref>
    <ref type="dispatch_gate">§10 checklist requires this review before Stage 3 primary case dispatch. No primary scoring run begins until this TO closes with CTO GO ruling.</ref>
  </references>

  <objective>
    Review the sphinx pre-screen result; preregister INCLUDE/SENTINEL/INVESTIGATE pools in the packet
    manifest; rule on Path A pass vs. Path B mandatory; authorize Stage 3 primary case dispatch or
    pause for target re-selection.

    ## Gate — do NOT proceed until confirmed

    .075 COMPLETE — sphinx pre-screen execution committed and MCP received.

    Verify:
    ```bash
    ls comp/results/sphinx/prescreen/prescreen_summary.yaml
    python3 -c "import yaml; s=yaml.safe_load(open('comp/results/sphinx/prescreen/prescreen_summary.yaml')); print('INCLUDE:', s['include_count'], 'SENTINEL:', s['sentinel_count'], 'INVESTIGATE:', s['investigate_count'])"
    ```

    ## Phase 1 — Pre-screen result review

    Read all per-question YAML artifacts:
    ```bash
    ls comp/results/sphinx/prescreen/
    # Read each q*_prescreen.yaml
    ```

    Review checklist:
    1. Are all questions triaged? No question should be missing a triage_category.
    2. Are SENTINEL assignments defensible? Check sentinel_reason for each SENTINEL question.
    3. Are INVESTIGATE assignments defensible? Check investigate_subtype and pilot_eligible assignments.
    4. Is there a sentinel_review_note if SENTINEL pool is empty?
    5. Are any R-SC-2 label assignments questionable? (Flag but do not re-run SC.)
    6. Are INCLUDE questions genuinely measurement-room? (Wrong zero-shot, Correct full-source.)

    ## Phase 2 — Off-ramp gate evaluation

    Apply the Path B MANDATORY thresholds from comp/dispatch/stage3_dispatch_criteria.md:
    - **Trigger 1**: INCLUDE count < 5 after pre-screen?
    - **Trigger 2**: SENTINEL count > 50% of total candidate question count?
    - **Trigger 3** (partial, evaluated after pilot): INVESTIGATE pilot_eligible_count > 0 AND
      preliminary expectation that pilot will NOT promote enough questions to bring INCLUDE to >= 5?
      (Trigger 3 is fully evaluable only after pilot runs — make a preliminary call here.)

    If ANY trigger is met: Path B MANDATORY. Do not proceed to pool preregistration.
    If NO trigger is met: Path A PASS. Proceed to Phase 3.

    ## Phase 3 (Path A only) — INCLUDE/SENTINEL pool preregistration

    Copy the stage3_packet_manifest_template.yaml:
    ```bash
    cp comp/dispatch/stage3_packet_manifest_template.yaml \
       comp/dispatch/sphinx_stage3_packet_manifest.yaml
    ```

    Fill in:
    - `packet_id: stage3-sphinx-001`
    - `target: sphinx`
    - `compiler_content_sha`: sha256[:8] of comp/targets/sphinx/compiler.py at current HEAD
    - `include_pool.question_ids`: list of all INCLUDE question IDs from pre-screen
    - `sentinel_pool.question_ids`: list of all SENTINEL question IDs from pre-screen
    - `sentinel_pool.sentinel_review_note`: SC's review note if sentinel pool is empty (from .075)
    - `investigate_questions_count`: count of INVESTIGATE questions
    - `pilot_eligible_count`: count of pilot_eligible=true questions
    - `pilot_status`: "pending" if pilot_eligible_count > 0; "not_required" if 0
    - `preregistration_timestamp`: ISO8601 timestamp now
    - `preregistration_reviewers`: ["1.1.0_SA_CTO", "2.1.0_SA_COO"]
    - `dispatch_path: path_a`

    Note: INVESTIGATE questions are NOT in the INCLUDE or SENTINEL pool yet. They remain in INVESTIGATE
    pending pilot results (if pilot_eligible_count > 0) OR are demoted to SENTINEL if ceiling/grader_artifact.
    Update `sentinel_pool.question_ids` to include any INVESTIGATE questions with pilot_eligible=false.

    ## Phase 4 — Ruling commit

    ```bash
    git add comp/dispatch/sphinx_stage3_packet_manifest.yaml
    git commit --only \
      --author="1.1.0_SA_CTO <1.1.0_SA_CTO@opal.agent>" \
      -m "review(COMP_LEARNS.076): sphinx pre-screen review + off-ramp gate -- PATH_A_PASS or PATH_B_MANDATORY -- N_INCLUDE INCLUDE / N_SENTINEL SENTINEL / N_INVESTIGATE INVESTIGATE" \
      -- comp/dispatch/sphinx_stage3_packet_manifest.yaml \
         comp/results/sphinx/prescreen/prescreen_summary.yaml
    git push origin CLOUD
    ```

    Replace PATH_A_PASS/PATH_B_MANDATORY and counts in the commit message.

    ## Phase 5 — Dispatch authorization (Path A) or Pause (Path B)

    **If PATH_A_PASS:**
    - If pilot_eligible_count == 0: GO for primary case dispatch authorized. MCP COO with GO ruling.
    - If pilot_eligible_count > 0: PILOT REQUIRED before primary case dispatch. MCP COO with pilot GO
      (COO will dispatch pilot execution TO using the .071 machinery).

    **If PATH_B_MANDATORY:**
    - HOLD primary case dispatch. MCP COO with PATH_B ruling and specific trigger that fired.
    - COO will author a target re-selection sub-PRD per §7.3.

    ## Phase 6 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Off-ramp ruling: PATH_A_PASS or PATH_B_MANDATORY
    - If PATH_A_PASS: INCLUDE / SENTINEL / INVESTIGATE pool counts; pilot required (yes/no)
    - If PATH_B_MANDATORY: which trigger(s) fired + counts
    - Any review findings (SENTINEL defensibility issues, label concerns)
    - Packet manifest file path (if Path A)
  </objective>

  <compiler_tools_mandate>
    <note>No Python source changes. YAML manifest fills and review. No ds-commit-gate.sh required.</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Gates on .075 COMPLETE.
      PATH_A_PASS + pilot_eligible_count==0 → COO dispatches Stage 3 primary case.
      PATH_A_PASS + pilot_eligible_count>0 → COO dispatches pilot execution (using .071 machinery).
      PATH_B_MANDATORY → COO authors target re-selection sub-PRD; Stage 3 dispatch paused.
      All three outcomes flow through COO before any primary case is dispatched.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Gate confirmed: .075 COMPLETE; prescreen_summary.yaml present.
    2. All per-question YAML artifacts reviewed; findings documented in commit/MCP.
    3. Off-ramp gate evaluated against all three Path B MANDATORY thresholds.
    4. Ruling issued: PATH_A_PASS or PATH_B_MANDATORY (no ambiguous outcomes).
    5. If PATH_A_PASS: sphinx_stage3_packet_manifest.yaml committed with INCLUDE/SENTINEL pools preregistered, preregistration_timestamp set, both reviewers listed.
    6. If PATH_B_MANDATORY: specific trigger(s) documented; primary case dispatch on hold.
    7. Committed --only --author=1.1.0_SA_CTO. Pushed to CLOUD.
    8. MCP 2.1.0_SA_COO with ruling + pool counts (or trigger reason).
  </acceptance_criteria>

  <dependencies>
    - Gate: .075 COMPLETE (sphinx pre-screen execution).
    - .073 COMPLETE (packet manifest template) needed for Phase 3. .073 is parallel with .075 — should be complete by the time .075 delivers.
    - Stage 3 primary case dispatch gates on this TO closing with PATH_A_PASS.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - Do NOT re-run the pre-screen judge if results look unexpected. Review and flag in MCP; SC owns
      any re-run decision.
    - Preregistration is a LOCK: once INCLUDE/SENTINEL pools are committed to the manifest, they cannot
      be changed during iteration. Flag any pools you are uncertain about BEFORE committing — re-classify
      the question and re-run pre-screen if needed (back to .075).
    - If pilot_eligible_count > 0: the INVESTIGATE questions remain in INVESTIGATE state in the manifest.
      They are NOT in the INCLUDE pool until pilot promotes them. COO will dispatch pilot after this
      TO closes.
    - If .073 is not yet complete when .075 delivers: use the template fields from §3.1 of the PRD
      directly to construct the manifest. .073 provides a clean YAML template; the fields are defined
      in the PRD if the template is late.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha + ruling
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO with ruling + pool counts
    - session log
  </closeout>
</task_order>
