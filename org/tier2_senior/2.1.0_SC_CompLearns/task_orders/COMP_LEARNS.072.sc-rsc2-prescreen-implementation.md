<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-072-sc-rsc2-prescreen-implementation</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>complete</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Stage 3 ship-blocker R-SC-1 P0 + R-SC-2 P1 (parallel with .070/.071/.073)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §2 — Parametric-prior pre-screen; §2.3 — R-SC-2 semantics integration; §2.4 — Wrong|Wrong subtype distinction</ref>
    <ref type="prd_section">§2.5 — Pre-screen output schema (per-question YAML). §10 ship-blocker items: R-SC-1 P0 and R-SC-2 P1.</ref>
    <ref type="r_sc_1">comp/results/dev-click-001/scoring_regime_honesty_note.md — R-SC-1: float grader undocumented behavior + q11 correct-but-unparseable. R-SC-2 extends this to a full semantic label taxonomy.</ref>
    <ref type="cvo_ruling">CVO R-COO-1 / R-SC-2 P1 — pre-screen must consume semantic labels, not raw binary grader output. Wrong|Wrong is not monolithic.</ref>
    <ref type="blocking_note">R-SC-2 required before iter-8 on click (blocking field). Also required before .075 sphinx pre-screen execution.</ref>
  </references>

  <objective>
    Two deliverables in sequence: (Phase 0) file R-SC-2 as a document defining the semantic audit label
    taxonomy; (Phase 1) implement the pre-screen triage logic consuming those labels.

    ## Context

    R-SC-1 (scoring_regime_honesty_note.md) documented the float grader's undocumented load-bearing
    behavior and q11's correct-but-unparseable status. R-SC-2 extends this to a complete semantic label
    taxonomy that the pre-screen and future scoring passes can consume to reason correctly about
    pass/fail classifications.

    Without R-SC-2 labels, the pre-screen triage matrix (§2.2) cannot distinguish "judge gave semantically
    correct answer but grader failed it" from "judge gave genuinely wrong answer." A Wrong|Wrong triage
    under raw grader output could misclassify a format-failure question as a genuine knowledge ceiling.

    ## Phase 0 — File R-SC-2 semantic label taxonomy

    Author the R-SC-2 document at:
    ```
    comp/results/r_sc_2_semantic_labels.md
    ```

    The document must define the five label values used in pre-screen and scoring:

    | Label | Definition |
    |-------|------------|
    | `parseable-correct` | Judge response is parseable by the grader AND semantically correct |
    | `parseable-wrong` | Judge response is parseable AND semantically wrong (genuine knowledge/reasoning failure) |
    | `semantic-correct-but-unparseable` | Judge response conveys the correct answer in free text, but the grader cannot extract it (FORMAT failure, not knowledge failure) |
    | `semantic-wrong-unparseable` | Judge response is unparseable AND semantically wrong |
    | `semantic-ambiguous` | Cannot determine semantic correctness; escalate to human review |

    For each label, document:
    1. The definition (as above)
    2. At least one example from the click q02/q03/q11 experience (can anonymize question content if needed, but reference the qID)
    3. The triage consequence: how this label maps to pre-screen category (see §2.3 mapping below)
    4. Whether the grader output (pass/fail) and the R-SC-2 label can disagree, and what to do when they do

    §2.3 label-to-triage mapping (codified from PRD):
    - `parseable-correct` + zero-shot → SENTINEL indicator
    - `parseable-correct` + full-source → expected (measures nothing if also correct zero-shot)
    - `parseable-wrong` + zero-shot, `parseable-correct` + full-source → INCLUDE (clear retrieval gain)
    - `parseable-wrong` + zero-shot, `parseable-wrong` + full-source → INVESTIGATE (Wrong|Wrong — see subtype)
    - `semantic-correct-but-unparseable` under BOTH regimes → NOT an INVESTIGATE candidate for retrieval; grader-surface fix needed
    - `semantic-ambiguous` → default to INVESTIGATE

    Also document the §2.4 Wrong|Wrong subtype labels:
    - `full_source_overload_candidate` — recoverable under structured compression; pilot_eligible=true
    - `ceiling` — unsolvable for this judge regardless of context; pilot_eligible=false
    - `grader_artifact` — grader surface failure; not a retrieval problem
    - `unresolved` — cannot confidently separate; default is pilot_eligible=true (NOT ceiling)

    The document must be authored by 2.1.0_SC_CompLearns, not synthesized from PRD text.
    Add your own judgment on edge cases encountered in the click run (q02, q11, any others).

    Commit R-SC-2 before proceeding to Phase 1:
    ```bash
    git commit --only \
      --author="2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>" \
      -m "doc(COMP_LEARNS.072): R-SC-2 semantic audit label taxonomy -- pre-screen grading surface" \
      -- comp/results/r_sc_2_semantic_labels.md
    git push origin CLOUD
    ```

    ## Phase 1 — Pre-screen triage logic implementation

    Author a pre-screen implementation document or script that SC will run per target.

    The pre-screen is NOT a fully automated pipeline step — it is an SC-operated procedure that
    produces a structured artifact. The implementation here is the protocol and the output schema,
    not necessarily a Python runner (though a Python helper is acceptable if it reduces manual error).

    Deliver at:
    ```
    comp/results/<target>/prescreen/prescreen_protocol.md
    ```
    (first instantiation will be sphinx — see .074 + .075)

    The protocol must specify:
    1. For each candidate question: run C1 (zero-shot, no context) and run full-source (current compiler v0 or best available for the target). Record grader pass/fail for each.
    2. Apply R-SC-2 semantic labels to each result using the §2.3 mapping.
    3. Classify into triage_category (INCLUDE / SENTINEL / INVESTIGATE) per the §2.2 triage matrix.
    4. For INVESTIGATE: determine investigate_subtype and set pilot_eligible per §2.4 rules.
    5. Emit per-question YAML conforming to §2.5 schema.

    §2.5 per-question output schema (must be emitted exactly):
    ```yaml
    question_id: qXX
    zero_shot_result:
      grader_label: pass | fail
      semantic_label: parseable-correct | parseable-wrong | semantic-correct-but-unparseable | semantic-wrong-unparseable | semantic-ambiguous
    full_source_result:
      grader_label: pass | fail
      semantic_label: <same options>
    triage_category: INCLUDE | SENTINEL | INVESTIGATE
    include_reason: <free text — required if INCLUDE>
    sentinel_reason: <free text — required if SENTINEL>
    investigate_subtype: full_source_overload_candidate | grader_artifact | ceiling | unresolved
    pilot_eligible: true | false
    ```

    Also emit a prescreen_summary.yaml at:
    ```
    comp/results/<target>/prescreen/prescreen_summary.yaml
    ```

    ```yaml
    target: <target>
    date: <ISO8601>
    authored_by: 2.1.0_SC_CompLearns
    question_count: N
    include_count: N
    sentinel_count: N
    investigate_count: N
    pilot_eligible_count: N
    sentinel_review_note: null  # required if sentinel_count == 0
    ```

    Note: the prescreen_protocol.md (methodology) is separate from the per-question YAML output.
    The former is the how; the latter is the what. Both are required artifacts.

    ## Phase 2 — Commit and push

    Commit Phase 1 artifacts (protocol doc, schema spec):
    ```bash
    git commit --only \
      --author="2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>" \
      -m "doc(COMP_LEARNS.072): pre-screen triage protocol (R-SC-1 P0 + R-SC-2 P1) -- §2.5 schema + methodology" \
      -- comp/results/r_sc_2_semantic_labels.md
    git push origin CLOUD
    ```

    Note: the per-question YAML output files are authored in .075 (sphinx pre-screen execution), not here.
    This TO delivers the R-SC-2 taxonomy + prescreen methodology. .075 applies it.

    ## Phase 3 — MCP

    MCP 2.1.0_SA_COO with:
    - R-SC-2 commit sha
    - Protocol commit sha (if separate)
    - Number of label values defined
    - Key edge cases documented (at minimum: q11 from click)
    - Confirmation that prescreen_protocol.md covers §2.5 output schema
    - Whether any label mapping ambiguity was found (flag for CTO if so)

    CC 1.1.0_SA_CTO with same content.
  </objective>

  <compiler_tools_mandate>
    <note>This TO does not modify Python source files. No ds-commit-gate.sh required.
    Commits are doc-only (markdown + YAML schema files).</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Parallel with .070/.071/.073 — no shared artifacts.
      .075 (sphinx pre-screen execution) gates on this TO being complete.
      R-SC-2 unblocks iter-8 on click (blocking field in COMP_LEARNS.json).
      .069 (q02/q11 ablation) also gates on R-SC-2 complete.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/results/r_sc_2_semantic_labels.md authored with 5 label values, definitions, examples, grader-vs-label disagreement handling.
    2. §2.3 label-to-triage mapping documented.
    3. §2.4 Wrong|Wrong subtype labels (full_source_overload_candidate / ceiling / grader_artifact / unresolved) defined with pilot_eligible mapping.
    4. prescreen_protocol.md authored covering C1 + full-source run procedure, R-SC-2 label application, §2.5 per-question output schema.
    5. prescreen_summary.yaml schema defined including sentinel_review_note field.
    6. R-SC-2 committed --only --author=2.1.0_SC_CompLearns before Phase 1 artifacts.
    7. Pushed to CLOUD.
    8. MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO with commit sha(s) + label count + edge cases.
  </acceptance_criteria>

  <dependencies>
    - No gates. Parallelizable with .070/.071/.073.
    - .075 (sphinx pre-screen execution) gates on this TO complete.
    - iter-8 on click (future) gates on R-SC-2 filed.
    - .069 (q02/q11 ablation) gates on R-SC-2 filed.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis in docs or logs.
    - R-SC-2 is YOUR analysis as scorer — not PRD paraphrase. Bring judgment from q02/q11 experience.
    - The protocol document (how to run the pre-screen) is the SC contribution. The per-question YAML
      output is authored in .075. Keep the two roles distinct.
    - If label ambiguity is found that the PRD does not resolve, flag it in the MCP (do not silently
      resolve it without CTO input).
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha(s)
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO
    - session log
  </closeout>
</task_order>
