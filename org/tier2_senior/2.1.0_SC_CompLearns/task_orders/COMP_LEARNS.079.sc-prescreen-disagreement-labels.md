<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-079-sc-prescreen-disagreement-labels</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — V1.2 grader-governance ship-blocker (R-SC-1 P0, gates on .077)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §11.3 — SC pre-screen and target summary emission (R-SC-1 P0)</ref>
    <ref type="prd_section">§11.1 — Disagreement rate as first-class runtime metric. §10 ship-blocker — V1.2 governance binding for any future primary case.</ref>
    <ref type="ds_dependency">.077 (1.3.0_DS dual-output emission) — provides scorecard fields this TO consumes</ref>
    <ref type="prior_protocol">comp/results/sphinx/prescreen/prescreen_protocol.md — your existing pre-screen methodology (4806174b); needs disagreement-labels extension</ref>
    <ref type="prior_artifacts">comp/results/sphinx/prescreen/q*_prescreen.yaml — existing per-Q schema; extend with disagreement_flag</ref>
  </references>

  <objective>
    Extend pre-screen output schema to emit per-question disagreement labels and per-target summary
    aggregated disagreement rate. Update prescreen_protocol.md with the new fields. The disagreement
    rate becomes a first-class metric on every pre-screen run, not a post-hoc audit.

    ## Context

    V1.2 §11.1 makes disagreement between exact-match and semantic graders a first-class runtime metric.
    Per CVO §1: without this, the project keeps discovering grader-artifact dominance only through ad-hoc
    closeout memos. Sphinx pre-screen forced this discovery; we don't want to repeat the discovery cycle
    on every target.

    .077 (1.3.0_DS dual-output emission) provides the scorecard fields. This TO consumes them in
    pre-screen output and methodology.

    ## Gate — do NOT proceed until confirmed

    .077 COMPLETE — 1.3.0_DS dual-output emission shipped; scorecard JSON contains:
    - per-response `graders.exact_match` + `graders.semantic` + `graders.disagreement_flag`
    - summary `disagreement_rate` + `disagreement_count` + `total_responses`

    Verify before running:
    ```bash
    python3 -c "
    import json, glob
    sc_files = sorted(glob.glob('comp/targets/click/scorecards/*.json'))
    if not sc_files:
        print('NO SCORECARDS FOUND')
    else:
        sc = json.load(open(sc_files[-1]))
        print('disagreement_rate:', sc.get('disagreement_rate', 'MISSING'))
        print('graders block:', 'graders' in str(sc) or 'per_question_graders' in str(sc))
    "
    ```

    ## Phase 1 — Extend per-question prescreen YAML schema

    Update prescreen_protocol.md §2.5 schema to include disagreement fields:

    ```yaml
    question_id: q01
    zero_shot_result:
      grader_label_exact_match: pass | fail
      grader_label_semantic: pass | fail
      semantic_label: parseable-correct | parseable-wrong | semantic-correct-but-unparseable | semantic-wrong-unparseable | semantic-partial-correct-unparseable | semantic-ambiguous
      disagreement_flag: bool
    full_source_result:
      grader_label_exact_match: pass | fail
      grader_label_semantic: pass | fail
      semantic_label: <same options>
      disagreement_flag: bool
    triage_category: INCLUDE | SENTINEL | INVESTIGATE
    triage_decision_under: exact_match | semantic | both_agree
    include_reason: <required if INCLUDE>
    sentinel_reason: <required if SENTINEL>
    investigate_subtype: full_source_overload_candidate | format_elicitation_gain | semantic_prior_unparseable | ceiling | unresolved
    pilot_eligible: true | false
    ```

    Note the `triage_decision_under` field — captures whether the triage decision changes depending on
    which grader output is consulted. Per V1.2 §11.1, semantic-aware governs triage; exact-match preserved
    for ratchet primary metric.

    ## Phase 2 — Extend prescreen_summary.yaml schema

    Add disagreement aggregate fields:

    ```yaml
    target: <target>
    date: <ISO8601>
    authored_by: 2.1.0_SC_CompLearns
    question_count: N
    include_count: N
    sentinel_count: N
    investigate_count: N
    pilot_eligible_count: N
    disagreement_rate_zero_shot: 0.XX     # NEW
    disagreement_rate_full_source: 0.XX   # NEW
    disagreement_rate_overall: 0.XX       # NEW (combined)
    disagreement_dominated_target: bool   # NEW: true if disagreement_rate_overall > 0.5
    sentinel_review_note: <optional, required if sentinel_count == 0>
    path_a_viable: bool
    path_b_trigger: null | include_too_small | sentinel_majority | investigate_pilot_failed
    answer_key_schema_note: <optional, target-specific>
    ```

    The `disagreement_dominated_target` flag: if more than 50% of responses disagree between graders,
    the target is grader-format dominated and requires special handling (sphinx is exactly this).

    ## Phase 3 — Update prescreen_protocol.md methodology

    Document the procedure for applying disagreement labels:

    1. After running C1 (zero-shot) and full-source for each question, read the scorecard's per-response
       graders block (post-.077 schema).
    2. For each (q, condition) response:
       - Record exact_match and semantic grader_label values
       - Record semantic_label per R-SC-2 taxonomy (with the .078 subtype split)
       - Set disagreement_flag = (exact_match.graded != semantic.graded)
    3. Apply triage matrix using SEMANTIC grading output (per V1.2 §11.1 governance — semantic governs
       triage; exact-match is preserved for ratchet metric).
    4. Aggregate disagreement counts to compute summary fields.

    Add a §3 "Disagreement Interpretation" section to prescreen_protocol.md:
    - High zero-shot disagreement + low full-source disagreement → format-elicitation effect (sphinx q01/q07)
    - High disagreement under BOTH regimes → semantic-prior-unparseable dominance (sphinx 8-of-10)
    - Low disagreement under both regimes → grader is well-matched to target's response shape
    - Recommend disagreement_dominated_target (>50%) triggers a target-fit review before primary scoring

    ## Phase 4 — Backfill sphinx pre-screen with disagreement labels (optional but recommended)

    Re-process the existing sphinx prescreen YAMLs to add disagreement_flag fields where derivable.
    Since 0.077 dual-grader was not yet shipped during the .075 run, the disagreement labels for sphinx
    must be reconstructed from your manual semantic audit (the prescreen_summary.yaml sentinel_review_note
    documents that ~8 of 12 zero-shot responses were semantic-correct-but-unparseable, etc.).

    If backfill is high-effort: document the gap in prescreen_summary.yaml (a `backfill_note` field
    explaining sphinx pre-screen predates V1.2 governance) and skip. The next pre-screen run will have
    full disagreement instrumentation natively.

    ## Phase 5 — Commit and push

    ```bash
    git commit --only \
      --author="2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>" \
      -m "doc(COMP_LEARNS.079): pre-screen disagreement labels (R-SC-1 P0) -- per-Q + summary disagreement_rate" \
      -- comp/results/sphinx/prescreen/prescreen_protocol.md \
         comp/results/sphinx/prescreen/prescreen_summary.yaml
    # Add per-Q YAMLs to pathspec if backfilled
    git push origin CLOUD
    ```

    ## Phase 6 — MCP

    MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO with:
    - Commit sha
    - Schema changes summary (per-Q fields added; summary aggregate fields added)
    - Whether sphinx prescreen was backfilled or marked with backfill_note
    - Confirmation that V1.2 §10 ship-blocker SC contribution complete (.078 + .079 jointly close it)
  </objective>

  <compiler_tools_mandate>
    <note>This TO modifies markdown + YAML files only. No ds-commit-gate.sh required.</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Gates on .077 (DS dual-output emission). .078 (subtype split) is parallel; integrate the new
      subtypes (format_elicitation_gain, semantic_prior_unparseable) into the protocol where they appear.
      Path B target re-selection sub-PRD authoring (COO) gates on .077 + .078 + .079 jointly complete.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. .077 confirmed COMPLETE before execution.
    2. prescreen_protocol.md §2.5 per-question schema extended with grader_label_exact_match + grader_label_semantic + disagreement_flag + triage_decision_under fields.
    3. prescreen_summary.yaml schema extended with disagreement_rate_zero_shot + disagreement_rate_full_source + disagreement_rate_overall + disagreement_dominated_target fields.
    4. prescreen_protocol.md §3 Disagreement Interpretation section authored.
    5. Triage decisions use SEMANTIC grading (per V1.2 §11.1 governance).
    6. Sphinx prescreen artifacts either backfilled OR marked with backfill_note documenting V1.2 predate.
    7. Committed --only --author=2.1.0_SC_CompLearns. Pushed to CLOUD.
    8. MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO with commit sha + schema summary.
  </acceptance_criteria>

  <dependencies>
    - GATE: .077 COMPLETE (1.3.0_DS dual-output scorecard fields shipped).
    - Parallel with .078 (subtype split) and .080 (sphinx schema fix) and .081 (sphinx q03/q05 pilot).
    - V1.2 §10 ship-blocker for primary case dispatch requires .077 + .078 + .079 jointly complete.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - DO NOT change the ratchet primary metric or champion selection logic — that's DS lane (.077 already preserves exact-match primacy).
    - Triage decisions under semantic-aware grading become the new norm. Backward compatibility with prior pre-screen results: existing artifacts (sphinx q*_prescreen.yaml) used exact-match-only labels; the protocol amendment notes this transition.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO
    - session log
  </closeout>
</task_order>
