<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-080-sc-grader-artifact-subtype-split</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>complete</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — V1.2 grader-governance ship-blocker (§11.3 R-SC-2 P1); parallel with .077/.078/.079/.081</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §11.3 R-SC-2 P1: grader_artifact subtype split into format-elicitation-gain vs semantic-prior-unparseable</ref>
    <ref type="rsc2">comp/results/r_sc_2_semantic_labels.md — §4.3 grader_artifact definition; needs subtype split amendment</ref>
    <ref type="evidence">.076 ruling §2 — q01/q07 reclassified as grader_artifact/format-elicitation-only (sentinel_reason field)</ref>
    <ref type="prescreen">comp/results/sphinx/prescreen/prescreen_summary.yaml + q01_prescreen.yaml + q07_prescreen.yaml</ref>
  </references>

  <objective>
    Split the `grader_artifact` INVESTIGATE subtype into two distinct subtypes as required by
    V1.2 §11.3 R-SC-2 P1. Amend comp/results/r_sc_2_semantic_labels.md and update prescreen
    protocol accordingly.

    ## Context

    The current R-SC-2 taxonomy (authored in .072) defines a single `grader_artifact` subtype:
    judge gives correct answers in BOTH regimes but grader cannot parse them. The sphinx
    pre-screen (.075) revealed two distinct mechanisms lumped into this subtype:

    1. **format-elicitation-gain** — context CHANGES answer shape (q01/q07 pattern):
       - Zero-shot: semantic-correct-but-unparseable (correct but markdown-wrapped)
       - Full-source: parseable-correct (context suppressed markdown → grader can parse)
       - The "gain" from C1→full-source is format elicitation, not information retrieval
       - This creates a spurious INCLUDE classification under §2.3 mapping
       - Correct triage: SENTINEL (judge already knew; context only changed response format)

    2. **semantic-prior-unparseable** — knowledge already present in BOTH regimes (q02-q12 sphinx pattern):
       - Zero-shot: semantic-correct-but-unparseable
       - Full-source: semantic-correct-but-unparseable
       - Context did NOT change the answer or enable gradeability
       - Correct triage: SENTINEL (prior-dominated, grader artifact prevents detection)
       - pilot_eligible=false

    Only the second is a clean SENTINEL for the parametric-prior detection purpose.
    The first is a real behavioral effect that the program should track separately:
    it is evidence that context bulk affects judge response formatting, which is relevant
    to the preregistration question (CVO §4 unknown-unknown) about whether the program
    tests knowledge delivery vs gradeable answer production.

    ## Phase 1 — Amend R-SC-2 taxonomy

    In comp/results/r_sc_2_semantic_labels.md, split §4.3 grader_artifact into two subtypes:

    ### 4.3a `format-elicitation-gain`

    **Definition:** Context shape changes the judge's response format, enabling gradeability,
    but the judge already had the correct answer without the context. Zero-shot is semantic-
    correct-but-unparseable; full-source is parseable-correct. The information content is
    unchanged; only the response packaging changed.

    **Indicators:**
    - Zero-shot: semantic-correct-but-unparseable (correct answer present in prose)
    - Full-source: parseable-correct (same answer, now grader-parseable)
    - Context delivered is dense plain-text (suppresses markdown formatting tendency)
    - Answer does not require structural knowledge the context provides

    **Triage:** SENTINEL (judge already correct; format change is not a retrieval gain).
    **pilot_eligible:** false
    **Click example (hypothetical):** Not observed in click. First confirmed instances: sphinx q01, q07.
    **.076 ruling:** q01 and q07 reclassified from INCLUDE to SENTINEL under this subtype.

    ### 4.3b `semantic-prior-unparseable`

    **Definition:** Judge gives correct answers in BOTH zero-shot and full-source, both
    wrapped in unparseable prose. Context did NOT change answer shape or gradeability.
    The judge's parametric prior is the source of knowledge; the grader surface is the
    sole failure point.

    **Indicators:**
    - Zero-shot: semantic-correct-but-unparseable
    - Full-source: semantic-correct-but-unparseable (same format, same answer)
    - Context presence did not improve gradeability (full-source still fails)
    - Answer is stable across regimes despite format failure

    **Triage:** SENTINEL (prior-dominated, masked by grader exact-match failure).
    **pilot_eligible:** false
    **Sphinx examples (confirmed):** q04, q06, q08, q09, q10, q11, q12 — 7 of 8 grader_artifact questions in sphinx pre-screen.

    Also update §2.3 triage mapping table to reflect the subtype split:
    - `semantic-correct-but-unparseable` (zero-shot) + `parseable-correct` (full-source) → SENTINEL (format-elicitation-gain)
    - `semantic-correct-but-unparseable` (both regimes) → SENTINEL (semantic-prior-unparseable)

    ## Phase 2 — Update investigate_subtype field in prescreen schema

    The `investigate_subtype` field in the §2.5 per-question YAML gains two new values:
    - `format-elicitation-gain` (replaces/clarifies `grader_artifact` for the q01/q07 pattern)
    - `semantic-prior-unparseable` (replaces/clarifies `grader_artifact` for the q04+ pattern)

    The original `grader_artifact` label is retired as the canonical subtype value. The two
    specific subtypes replace it. Documents that already use `grader_artifact` (q02-q12 sphinx
    prescreen YAML files) should be noted as using the legacy label pending re-run.

    Amend prescreen_protocol.md §2 Step 5 (subtype assignment table) to include the two new
    subtypes and their criteria.

    ## Phase 3 — Update sphinx prescreen YAML files (retroactive label)

    Update the sphinx per-question YAML files that currently have `investigate_subtype: grader_artifact`:
    - q01_prescreen.yaml: investigate_subtype: format-elicitation-gain | triage_category: SENTINEL
      (reclassified per .076 ruling)
    - q07_prescreen.yaml: investigate_subtype: format-elicitation-gain | triage_category: SENTINEL
      (reclassified per .076 ruling)
    - q02_prescreen.yaml: investigate_subtype: semantic-prior-unparseable
    - q04_prescreen.yaml: investigate_subtype: semantic-prior-unparseable
    - q06_prescreen.yaml: investigate_subtype: semantic-prior-unparseable
    - q08_prescreen.yaml: investigate_subtype: semantic-prior-unparseable
    - q09_prescreen.yaml: investigate_subtype: semantic-prior-unparseable
    - q10_prescreen.yaml: investigate_subtype: semantic-prior-unparseable
    - q11_prescreen.yaml: investigate_subtype: semantic-prior-unparseable
    - q12_prescreen.yaml: investigate_subtype: semantic-prior-unparseable

    For q01 and q07: also update triage_category to SENTINEL and add sentinel_reason per
    .076 ruling: "format_elicitation_only — judge already correct under zero-shot, full-source
    merely enabled gradeability."

    Also update prescreen_summary.yaml: include_count→0, sentinel_count→2, SENTINEL entry note.

    ## Phase 4 — Commit and push

    ```bash
    git add comp/results/r_sc_2_semantic_labels.md \
            comp/results/sphinx/prescreen/prescreen_protocol.md \
            comp/results/sphinx/prescreen/
    git commit --only \
      --author="2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>" \
      -m "doc(COMP_LEARNS.080): R-SC-2 grader_artifact subtype split (format-elicitation-gain / semantic-prior-unparseable) + sphinx prescreen retroactive relabel" \
      -- comp/results/r_sc_2_semantic_labels.md \
         comp/results/sphinx/prescreen/prescreen_protocol.md \
         comp/results/sphinx/prescreen/
    git push origin CLOUD
    ```

    ## Phase 5 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Confirmation that q01/q07 reclassified to SENTINEL + format-elicitation-gain
    - Updated pool counts (INCLUDE=0, SENTINEL=2, INVESTIGATE=10; investigate: 7 semantic-prior-
      unparseable + 1 format-elicitation-gain in SENTINEL + 2 unresolved)
    - Confirmation that legacy `grader_artifact` label is documented as retired
    - Any edge cases in the subtype definitions that need CTO review

    CC 1.1.0_SA_CTO.
  </objective>

  <compiler_tools_mandate>
    <note>No Python source changes — YAML and markdown amendments only. ds-commit-gate.sh not required.
    No upstream gate.</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Parallel with .077/.078/.081.
      .079 reads the investigate_subtype values defined here — inform SC (.079) if the label names
      change from what this TO specifies before .079 executes.
      .076 ruling (q01/q07 reclassification) is the authority for the SENTINEL reassignments.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. R-SC-2 taxonomy amended with §4.3a format-elicitation-gain + §4.3b semantic-prior-unparseable definitions.
    2. Legacy grader_artifact documented as retired.
    3. §2.3 triage mapping table updated.
    4. prescreen_protocol.md subtype assignment table updated.
    5. All 10 sphinx prescreen YAML files updated with correct new subtype labels.
    6. q01 and q07 reclassified SENTINEL with sentinel_reason per .076.
    7. prescreen_summary.yaml updated (include_count=0, sentinel_count=2).
    8. Committed --only --author=2.1.0_SC_CompLearns. Pushed CLOUD.
    9. MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO.
  </acceptance_criteria>

  <dependencies>
    - No upstream gate. Can start immediately.
    - .079 consumes subtype labels defined here — .079 should start after this TO.
    - .077 and .078 are independent.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - The investigate_subtype field in YAML is a free string. Both new values use hyphens:
      format-elicitation-gain, semantic-prior-unparseable. Use these exact strings for consistency.
    - The `grader_artifact` legacy label should be documented as retired but NOT deleted from
      existing artifacts — leave it in place with a note. Only new authoring uses the split subtypes.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD
    - MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO
    - session log
  </closeout>
</task_order>
