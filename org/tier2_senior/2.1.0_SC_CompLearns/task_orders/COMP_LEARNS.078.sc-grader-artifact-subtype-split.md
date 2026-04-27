<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-078-sc-grader-artifact-subtype-split</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>complete</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — V1.2 grader-governance ship-blocker (R-SC-2 P1, parallel with .077/.080/.081)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §11.3 — SC grader_artifact subtype split (R-SC-2 P1)</ref>
    <ref type="prior_taxonomy">comp/results/r_sc_2_semantic_labels.md — your R-SC-2 taxonomy (07fbc543); needs subtype amendment</ref>
    <ref type="cvo_ruling">CVO 20260427T200500Z grader-format ruling (e3393b26) + V1.2 PRD (95f8c0d3). Refined Option C governance.</ref>
    <ref type="sphinx_pattern">comp/results/sphinx/prescreen/ — 8 of 10 INVESTIGATE = grader_artifact (semantic-prior unparseable); q01/q07 reclassified by .076 to grader_artifact (format-elicitation gain)</ref>
    <ref type="cto_distinction">.076 ruling deliverable §2 — q01/q07 reclassification rationale; CVO §3 governance reasoning</ref>
  </references>

  <objective>
    Amend r_sc_2_semantic_labels.md to split the single grader_artifact subtype into two distinct
    mechanisms: format-elicitation gain vs semantic-prior unparseable. The split is required because
    these have different downstream interpretations (one is a real behavioral effect outside the program's
    primary retrieval claim; the other is clean SENTINEL).

    ## Context

    The sphinx pre-screen exposed that "grader_artifact" is not monolithic. Two distinct patterns
    surface under exact-match grading both regimes:

    1. **Format-elicitation gain** (sphinx q01/q07 pattern) — judge knows the answer in BOTH zero-shot
       and full-source. Zero-shot wraps in markdown that exact-match cannot parse (fail). Full-source
       changes the answer SHAPE (gives a bare extracted answer that exact-match parses). The full-source
       context did NOT add knowledge — it changed presentation. CTO's .076 ruling: this is NOT a
       genuine retrieval gain and should not count as INCLUDE.

    2. **Semantic-prior unparseable** (sphinx 8-of-10 INVESTIGATE pattern) — judge knows the answer
       in BOTH regimes and wraps in markdown both times. Both fail exact-match grader. Under semantic
       audit, both are correct. This is prior-dominated — clean SENTINEL category.

    Without the split, both patterns label as `grader_artifact` and the program loses signal about
    target characteristics. With the split, grader-format dominance is detectable per-target.

    ## Phase 1 — Author the subtype amendment

    Open `comp/results/r_sc_2_semantic_labels.md` (the existing R-SC-2 taxonomy authored by you at
    07fbc543). Locate the §2.4 Wrong|Wrong subtype section.

    Replace the single `grader_artifact` entry with two entries:

    ### `format_elicitation_gain` (NEW)
    - **Pattern**: zero-shot fails grader exact-match; full-source passes grader exact-match. Under semantic
      audit BOTH responses convey the correct answer. The full-source context changed answer shape (e.g.,
      stripped markdown) without adding knowledge.
    - **Triage decision**: NOT INCLUDE. NOT genuine retrieval gain. Maps to a behavior outside the program's
      primary retrieval claim ("find/localize/act on correct structural context").
    - **pilot_eligible**: false
    - **Example**: sphinx q01, q07 (per .076 ruling)
    - **Open question** (V1.2 §12 follow-on): is the program testing "knowledge delivery to the judge"
      or "gradeable answer production"? Future CVO design cycle item.

    ### `semantic_prior_unparseable` (NEW, replaces vague `grader_artifact`)
    - **Pattern**: BOTH regimes show parseable-correct semantic-aware but parseable-wrong exact-match
      (judge wraps correct answer in markdown both times). Knowledge already present in the parametric
      prior under both regimes.
    - **Triage decision**: SENTINEL (prior-dominated). The judge already knows; compiler context is not
      needed for knowledge.
    - **pilot_eligible**: false
    - **Example**: sphinx 8-of-10 INVESTIGATE under exact-match grader

    Keep these existing subtypes:
    - `full_source_overload_candidate` — recoverable under structured compression; pilot_eligible=true
    - `ceiling` — unsolvable for this judge; pilot_eligible=false
    - `unresolved` — cannot confidently separate; default pilot_eligible=true (NOT ceiling)

    Update the §2.3 label-to-triage mapping table to reference the two new subtypes:
    - `parseable-wrong` zero-shot + `parseable-correct` full-source where semantic audit shows BOTH are
      semantic-correct → `format_elicitation_gain` (NOT INCLUDE)
    - `parseable-wrong` BOTH regimes where semantic audit shows BOTH are semantic-correct →
      `semantic_prior_unparseable` (SENTINEL)
    - `parseable-wrong` BOTH regimes where semantic audit shows BOTH are semantic-wrong →
      `full_source_overload_candidate` or `ceiling` per the existing rules

    ## Phase 2 — Sixth-label amendment (carried over from prior CTO ruling)

    Per CTO ruling 2026-04-27 ~17:00 ET: add a sixth primary label `semantic-partial-correct-unparseable`
    for set responses where the judge gives M of N gold members (1 ≤ M < N) in prose with the rest
    absent (not asserted-wrong). Five deterministic cross-regime subtype rules cover all combinations
    (promote / full_source_overload_candidate / grader_artifact / anomaly / escalate). Multi-trial guard
    (≥4/6 stable coverage) prevents trial-noise mislabeling.

    This amendment was issued before the V1.2 ruling; integrate it now in the same TO so r_sc_2_semantic_labels.md
    reflects both the sixth-label and the subtype-split changes in one consistent state.

    Click q03 retroactively confirmed as `parseable-wrong`, NOT `partial-correct`. Document this
    confirmation in the amendment.

    ## Phase 3 — Commit and push

    ```bash
    git commit --only \
      --author="2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>" \
      -m "doc(COMP_LEARNS.078): R-SC-2 amendments -- subtype split (format_elicitation vs semantic_prior_unparseable) + sixth label" \
      -- comp/results/r_sc_2_semantic_labels.md
    git push origin CLOUD
    ```

    ## Phase 4 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Subtype split applied (2 new subtypes; 1 retired)
    - Sixth label integrated (semantic-partial-correct-unparseable + 5 cross-regime rules + multi-trial guard)
    - Click q03 confirmation noted
    - Updated label count (6 primary + 5 subtypes = 11 named values)

    CC 1.1.0_SA_CTO with same content.
  </objective>

  <compiler_tools_mandate>
    <note>This TO modifies a markdown file only. No ds-commit-gate.sh required.</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Parallel with .077/.080/.081. No shared artifact writes.
      .079 (SC disagreement labels) does NOT gate on this TO directly; both can run in parallel.
      However, both .078 and .079 ship together completes the SC contribution to V1.2 §10 ship-blocker.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. r_sc_2_semantic_labels.md amended with format_elicitation_gain + semantic_prior_unparseable subtypes (replacing single grader_artifact).
    2. §2.3 label-to-triage mapping table updated to reference new subtypes.
    3. Sixth primary label semantic-partial-correct-unparseable added with 5 cross-regime subtype rules + multi-trial guard.
    4. Click q03 confirmation as parseable-wrong (not partial-correct) documented.
    5. Total label count: 6 primary + 5 subtypes = 11 named values.
    6. Committed --only --author=2.1.0_SC_CompLearns. Pushed to CLOUD.
    7. MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO with commit sha + amendment summary.
  </acceptance_criteria>

  <dependencies>
    - No gates. Parallel with .077/.079/.080/.081.
    - V1.2 §10 ship-blocker requires .077 + .078 + .079 jointly complete for any future primary case dispatch.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - This is a doc amendment, not a re-authoring. Preserve existing structure; amend in place.
    - The retired single grader_artifact subtype: the term may still appear in older artifacts (e.g., .075 prescreen YAMLs). Do NOT bulk-edit historical artifacts. New artifacts use the split.
    - Sixth label amendment was originally a separate CTO ruling earlier today (~17:00 ET); it sat unactioned during sphinx prescreen execution. Now consolidated with the subtype split.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO
    - session log
  </closeout>
</task_order>
