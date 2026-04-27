<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-069-q02q11-ablation-stub</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SA_COO</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P2 — non-blocking follow-on; gated on .068 result + R-SC-2 (.072 Phase 0) complete</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §11 — Open follow-ons: .069 q02/q11 non-ratchet diagnostic ablation</ref>
    <ref type="r_sc_1">comp/results/dev-click-001/scoring_regime_honesty_note.md — R-SC-1: float grader + q11 correct-but-unparseable. q02/q11 numeric-fact nodes disqualified from ratchet by CVO R-CTO-1.</ref>
    <ref type="cvo_ruling">CVO R-CTO-1 — q02/q11 numeric-fact nodes disqualified as potential answer injection under float(full_response_text) grader. .069 is a non-ratchet diagnostic ONLY.</ref>
    <ref type="iter7_result">comp/dev-bundles/dev-click-001/iter-7/result.json — pending .068 scoring. .069 gates on this result.</ref>
    <ref type="r_sc_2">comp/results/r_sc_2_semantic_labels.md — to be authored in .072 Phase 0. .069 gates on R-SC-2 complete.</ref>
  </references>

  <objective>
    Diagnostic ablation: run click iter-7 compiler WITH q02/q11 numeric-fact nodes added (ablation-only
    compiler variant) under non-ratchet conditions to measure the float grader's sensitivity.
    This is NOT a ratchet iteration — it does NOT affect champion.json or experiment_log.jsonl.

    ## Status

    DEFERRED — this TO is a stub. DO NOT execute until both gates are satisfied:
    1. .068 COMPLETE (iter-7 scoring verdict received)
    2. .072 Phase 0 COMPLETE (R-SC-2 semantic label taxonomy filed)

    COO will author the full TO specification when bandwidth permits after both gates clear.

    ## Scoping note

    Per CVO R-CTO-1, q02/q11 numeric-fact nodes are disqualified from being ratchet-critical evidence
    because float(full_response_text) can trivially extract a numeric answer if the context contains the
    exact value. The diagnostic purpose here is NOT to re-evaluate whether to include them in the ratchet,
    but to measure the FORMAT effect vs. the SEMANTIC effect:

    - Does adding q02/q11 nodes change q02/q11 grader pass/fail? (float extraction test)
    - Do R-SC-2 semantic labels show that q02/q11 are parseable-correct vs. parseable-wrong?
    - Is the q11 correct-but-unparseable diagnosis from R-SC-1 confirmed under iter-7 compiler?

    This is scoring-regime forensics, not a mutation signal. The result informs R-SC-2 labeling
    quality and the format-aware grader upgrade path (if any).

    ## Full TO specification (to be authored after gates clear)

    COO to expand this stub into full phases (pre-run gate, ablation run, R-SC-2 label application,
    report) when .068 verdict + R-SC-2 are both in hand.
  </objective>

  <acceptance_criteria>
    STUB — acceptance criteria to be defined when full TO is authored.
  </acceptance_criteria>

  <dependencies>
    - Gate 1: .068 COMPLETE (iter-7 scoring verdict)
    - Gate 2: .072 Phase 0 COMPLETE (R-SC-2 semantic labels filed)
    - Non-blocking for Stage 3 dispatch.
  </dependencies>

  <operational_notes>
    - This is a stub placeholder only. Do NOT execute.
    - Numbered .069 per Stage 3 PRD §11 ("COO authors when bandwidth permits").
    - Stage 3 ship-blocker TOs are .070-.076; .069 does not block any of them.
  </operational_notes>

  <closeout>
    - Expand stub to full TO when gates clear.
    - Execute and close out after full TO authored.
  </closeout>
</task_order>
