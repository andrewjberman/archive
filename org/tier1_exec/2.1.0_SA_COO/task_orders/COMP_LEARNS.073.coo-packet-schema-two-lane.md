<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-073-coo-packet-schema-two-lane</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SA_COO</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Stage 3 ship-blocker R-COO-1 + R-COO-2 (parallel with .070/.071/.072)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §3 — Two-lane question partition (R-COO-1); §7 — Target selection Path A/B (R-COO-2)</ref>
    <ref type="prd_section">§3.1 — Empty-pool rules (asymmetric: INCLUDE empty = hard reject; SENTINEL empty = allowed with sentinel_review_note). §3.2 — Why preregister both pools. §10 — Ship-blocker items R-COO-1 + R-COO-2.</ref>
    <ref type="prd_section_7">§7.2 — Path B MANDATORY thresholds: &lt; 5 INCLUDE questions OR SENTINEL > 50% OR INVESTIGATE pilot fails. §7.3 — Path B requires separate sub-PRD; iteration does not begin against unselected fallback.</ref>
    <ref type="prior_packet_format">comp/tasks/ — prior task packet format (Archetype D, case-003-sphinx-autodoc-typehints); Stage 3 uses a new packet schema with INCLUDE/SENTINEL pools</ref>
  </references>

  <objective>
    Author the Stage 3 dispatch packet manifest schema and dispatch criteria document. These are the
    structural artifacts that COO uses to preregister question pools before primary case dispatch.

    ## Context

    Stage 3 introduces two structural changes to the packet format:
    1. **Two-lane question partition** (R-COO-1): packets must carry INCLUDE and SENTINEL pools,
       preregistered before iteration begins. Both pools are written into the packet manifest before
       any scored run, and the empty-pool rules (asymmetric) govern whether a packet can be dispatched.
    2. **Path A/B dispatch criteria** (R-COO-2): the dispatch packet must document the Path A default
       (sphinx) and the three Path B trigger thresholds, so CTO can evaluate the off-ramp gate at §10
       checkpoint 8.

    ## Phase 1 — Stage 3 packet manifest template

    Author the Stage 3 packet manifest schema at:
    ```
    comp/dispatch/stage3_packet_manifest_template.yaml
    ```

    The template is a YAML file with all fields and inline comments explaining each. Required fields:

    ```yaml
    # Stage 3 packet manifest — template v1
    schema_version: 3
    packet_id: <unique string, e.g. "stage3-sphinx-001">
    target: <target identifier, e.g. "sphinx">
    compiler_content_sha: <sha256[:8] of compiler.py at preregistration time>
    preregistration_timestamp: null  # ISO8601; set when pools are locked by CTO + COO
    preregistration_reviewers: []  # ["1.1.0_SA_CTO", "2.1.0_SA_COO"]

    # Two-lane question partition (R-COO-1)
    include_pool:
      question_ids: []  # Populated from pre-screen INCLUDE + promoted INVESTIGATE questions
      # MUST be non-empty. Empty include_pool = packet rejected from dispatch queue.

    sentinel_pool:
      question_ids: []  # Populated from pre-screen SENTINEL + demoted INVESTIGATE questions
      sentinel_review_note: null
      # If sentinel_pool.question_ids is empty, sentinel_review_note MUST be non-null.
      # sentinel_review_note authored by SC, reviewed by CTO at §10 ship-blocker checkpoint.

    # Path A/B dispatch (R-COO-2)
    dispatch_path: path_a  # path_a | path_b_mandatory
    path_b_trigger_reason: null  # Required if dispatch_path = path_b_mandatory

    # Pilot status (filled after INVESTIGATE pilot runs, if any)
    investigate_questions_count: 0
    pilot_eligible_count: 0
    pilot_status: not_required  # not_required | pending | complete
    pilot_artifact_path: null  # comp/results/<target>/pilot/<timestamp>/pilot_summary.json

    # Primary case metadata (filled at dispatch)
    conditions: [C1, C2, C3, C4]  # All four required from first scored run
    dispatch_timestamp: null
    dispatch_authorized_by: null  # "1.1.0_SA_CTO"
    ```

    ## Phase 2 — Dispatch criteria document

    Author:
    ```
    comp/dispatch/stage3_dispatch_criteria.md
    ```

    Document:
    1. **INCLUDE pool gate**: INCLUDE must be non-empty before dispatch. If empty after pre-screen
       and pilot, Path B evaluation is mandatory.
    2. **SENTINEL pool gate**: SENTINEL may be empty ONLY with a non-null sentinel_review_note authored
       by SC and reviewed by CTO. Empty sentinel with null note = packet rejected.
    3. **Path A default (sphinx)**: sphinx is the Stage 3 primary target per §7.1.
    4. **Path B MANDATORY triggers** (any one is sufficient):
       - INCLUDE pool < 5 questions after pre-screen + pilot
       - SENTINEL pool > 50% of total candidate question count
       - INVESTIGATE pilot (post-pilot) fails to produce any promoted questions AND INCLUDE pool < 5
    5. **Path B process**: dispatch pauses; COO authors a target re-selection sub-PRD; iteration does
       not begin against an unselected fallback target.
    6. **Four-condition requirement**: all Stage 3 primary case runs MUST dispatch C1+C2+C3+C4 from
       the first scored run. No Stage 2-style C1+C2-only dispatch.
    7. **Preregistration lock**: once CTO + COO sign off on INCLUDE/SENTINEL pools, the partition is
       locked. No retroactive pool changes during iteration.

    ## Phase 3 — Directory creation + commit

    Ensure the comp/dispatch/ directory exists (create if not present — it is a new directory).

    ```bash
    git add comp/dispatch/stage3_packet_manifest_template.yaml \
            comp/dispatch/stage3_dispatch_criteria.md
    git commit --only \
      --author="2.1.0_SA_COO <2.1.0_SA_COO@opal.agent>" \
      -m "doc(COMP_LEARNS.073): Stage 3 packet schema (R-COO-1 + R-COO-2) -- two-lane partition template + dispatch criteria" \
      -- comp/dispatch/stage3_packet_manifest_template.yaml \
         comp/dispatch/stage3_dispatch_criteria.md
    git push origin CLOUD
    ```

    ## Phase 4 — MCP

    MCP 1.1.0_SA_CTO with:
    - Commit sha
    - comp/dispatch/ path confirmed
    - Key schema fields: include_pool, sentinel_pool, sentinel_review_note, dispatch_path, pilot_status
    - Path B MANDATORY thresholds as specified
    - Ready for .075 (sphinx pre-screen) + .076 (off-ramp gate review)
  </objective>

  <compiler_tools_mandate>
    <note>This TO does not modify Python source files. No ds-commit-gate.sh required.
    Commits are doc/schema only (YAML template + markdown).</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Parallel with .070/.071/.072.
      .076 (CTO pre-screen review + off-ramp gate) consumes the packet manifest template to preregister
      INCLUDE/SENTINEL pools. Ensure template is clean and reviewable before .076 runs.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/dispatch/ directory created.
    2. stage3_packet_manifest_template.yaml authored with schema_version=3, include_pool, sentinel_pool (with sentinel_review_note), dispatch_path, pilot_status fields and inline comments.
    3. stage3_dispatch_criteria.md documents 7 dispatch criteria including INCLUDE empty = hard reject, SENTINEL empty + review note = allowed, Path B mandatory thresholds (3 triggers), 4-condition requirement, preregistration lock.
    4. Committed --only --author=2.1.0_SA_COO. Pushed to CLOUD.
    5. MCP 1.1.0_SA_CTO with commit sha + key fields confirmed.
  </acceptance_criteria>

  <dependencies>
    - No gates. Parallelizable with .070/.071/.072.
    - .076 (CTO off-ramp gate) consumes the packet manifest template.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - The comp/dispatch/ directory is NEW — it does not exist yet. Create it before committing.
    - Schema YAML should be directly usable as a template: an operator copies it, fills in the nulls,
      and the result is a valid packet manifest for Stage 3 dispatch.
    - The sentinel_review_note field in the template must be clearly documented as REQUIRED when
      sentinel_pool.question_ids is empty — this is the asymmetric empty-pool rule from CVO V1.1 review.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD from feature_clb
    - MCP 1.1.0_SA_CTO with commit sha + schema confirmed
    - session log
  </closeout>
</task_order>
