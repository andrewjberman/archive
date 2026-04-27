<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-075-sc-sphinx-prescreen-execution</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — Stage 3 ship-blocker (gates on .072 + .074; parallel execution gates for .070/.071/.073 not required)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §2 — Pre-screen triage matrix; §2.5 — Output schema. §10 ship-blocker: "Sphinx target pre-screen run (Path A first attempt)"</ref>
    <ref type="prd_section">§7.1 — Sphinx Path A rationale. §3.1 — Empty-pool rules (sentinel_review_note). §7.2 — Path B MANDATORY thresholds.</ref>
    <ref type="r_sc_2">comp/results/r_sc_2_semantic_labels.md — authored in .072 Phase 0; defines semantic label taxonomy consumed here</ref>
    <ref type="prescreen_protocol">comp/results/sphinx/prescreen/prescreen_protocol.md — authored in .072 Phase 1; methodology for this run</ref>
    <ref type="sphinx_questions">comp/targets/sphinx/gold/ab_questions.yaml + ab_answer_key.yaml — authored in .074; provides question pool</ref>
    <ref type="sphinx_compiler">comp/targets/sphinx/compiler.py — v0 imports-only; used as "full-source" baseline for this pre-screen</ref>
    <ref type="consumer">.076 (CTO pre-screen review + off-ramp gate) gates on this TO complete</ref>
  </references>

  <objective>
    Execute the Stage 3 sphinx pre-screen: run zero-shot (C1) and full-source (v0 compiler) for each
    sphinx candidate question; apply R-SC-2 semantic labels; emit per-question triage schema + summary.

    ## Gates — do NOT proceed until both are confirmed

    1. .072 COMPLETE — R-SC-2 semantic label taxonomy filed + prescreen_protocol.md authored
    2. .074 COMPLETE — sphinx question pool (ab_questions.yaml + ab_answer_key.yaml) committed

    Verify before running:
    ```bash
    python3 -c "import yaml; qs=yaml.safe_load(open('comp/targets/sphinx/gold/ab_questions.yaml')); print(len(qs['questions']), 'questions')"
    # Expect: >= 10
    ls comp/results/r_sc_2_semantic_labels.md
    # Expect: file exists
    ```

    ## Phase 0 — Pre-run setup

    Pull CLOUD to get .072 + .074 artifacts:
    ```bash
    git pull origin CLOUD --ff-only
    ```

    Read the R-SC-2 taxonomy before running:
    ```bash
    cat comp/results/r_sc_2_semantic_labels.md
    ```

    Read the pre-screen protocol:
    ```bash
    cat comp/results/sphinx/prescreen/prescreen_protocol.md
    ```
    (authored in .072; if absent, MCP COO — .072 may not be fully complete)

    ## Phase 1 — Zero-shot run (C1) for each question

    For each question in ab_questions.yaml, run the judge in C1 (unaided) mode:
    - No compiler context delivered to judge
    - Use format-aware grader (consistent with R-SC-2 semantics — do NOT use raw binary pass/fail)
    - Record grader_label (pass/fail) and apply R-SC-2 semantic_label

    Use the ratchet runner or equivalent judge harness. ANTHROPIC_API_KEY must be set.

    Duration note: N_questions * 1 call each. With cache hits, warm; cold = N_questions API calls.
    Check if prior click zero-shot runs have cached responses for overlapping question formats.

    ## Phase 2 — Full-source run for each question

    For each question, run the judge with the sphinx compiler v0 full output as context:
    - Use comp/targets/sphinx/compiler.py (imports-only v0) to compile the sphinx target
    - Deliver the full compiled graph as context (no addressing, no selector filtering — full surface)
    - Record grader_label and R-SC-2 semantic_label

    Note: "full-source" in the pre-screen context means the best available compiler output, not raw
    file content. For sphinx at v0, this is the imports subtype graph. This is the Stage 3 baseline;
    a more evolved compiler would produce richer context. Use what's available — the pre-screen result
    is relative to the current compiler state.

    ## Phase 3 — Apply R-SC-2 labels and triage matrix

    For each question, using the zero-shot and full-source results:

    1. Assign semantic_label to each result per R-SC-2 taxonomy (from .072)
    2. Apply triage matrix (§2.2):
       - Wrong (zero-shot) + Correct (full-source) → INCLUDE — clear retrieval gain
       - Correct (zero-shot) + Correct (full-source) → SENTINEL — prior-dominated
       - Wrong + Wrong → INVESTIGATE (subtype TBD per §2.4)
       - Correct + Wrong → INVESTIGATE (grader/context-overload artifact)
    3. For INVESTIGATE: determine investigate_subtype and pilot_eligible per §2.4 + R-SC-2 labels:
       - `semantic-correct-but-unparseable` under both regimes → grader_artifact, pilot_eligible=false
       - Cannot separate ceiling vs. full_source_overload_candidate → unresolved, pilot_eligible=true (default)
       - Confident ceiling diagnosis → ceiling, pilot_eligible=false
       - Confident full-source-overload-candidate → full_source_overload_candidate, pilot_eligible=true

    ## Phase 4 — Emit pre-screen artifacts

    Write per-question YAML (§2.5 schema) to:
    ```
    comp/results/sphinx/prescreen/q<ID>_prescreen.yaml
    ```

    Per-question schema:
    ```yaml
    question_id: q01
    zero_shot_result:
      grader_label: pass | fail
      semantic_label: parseable-correct | parseable-wrong | semantic-correct-but-unparseable | semantic-wrong-unparseable | semantic-ambiguous
    full_source_result:
      grader_label: pass | fail
      semantic_label: <same options>
    triage_category: INCLUDE | SENTINEL | INVESTIGATE
    include_reason: <required if INCLUDE>
    sentinel_reason: <required if SENTINEL>
    investigate_subtype: full_source_overload_candidate | grader_artifact | ceiling | unresolved
    pilot_eligible: true | false
    ```

    Write summary:
    ```
    comp/results/sphinx/prescreen/prescreen_summary.yaml
    ```

    ```yaml
    target: sphinx
    date: <ISO8601>
    authored_by: 2.1.0_SC_CompLearns
    question_count: N
    include_count: N
    sentinel_count: N
    investigate_count: N
    pilot_eligible_count: N
    sentinel_review_note: null  # if sentinel_count > 0, null is correct; if sentinel_count == 0, author a review note
    ```

    ## Phase 5 — Off-ramp preliminary assessment

    Before committing, compute the Path B trigger check:
    - INCLUDE count < 5? (Path B trigger 1)
    - SENTINEL count > 50% of total candidate count? (Path B trigger 2)
    - Note: trigger 3 (INVESTIGATE pilot result) not yet evaluable — that gates on .076 pilot dispatch

    Report the preliminary Path B risk in the MCP. CTO will make the formal ruling in .076.

    ## Phase 6 — Commit and push

    ```bash
    git add comp/results/sphinx/prescreen/
    git commit --only \
      --author="2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>" \
      -m "score(COMP_LEARNS.075): sphinx pre-screen execution -- N_INCLUDE INCLUDE + N_SENTINEL SENTINEL + N_INVESTIGATE INVESTIGATE" \
      -- comp/results/sphinx/prescreen/
    git push origin CLOUD
    ```

    Replace N_INCLUDE, N_SENTINEL, N_INVESTIGATE with actual counts.

    ## Phase 7 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Question count: total / INCLUDE / SENTINEL / INVESTIGATE / pilot_eligible
    - Per-category summary (not per-question — that's in the files)
    - Preliminary Path B risk assessment (triggers 1 and 2)
    - Any INVESTIGATE subtype findings (unresolved count, grader_artifact count)
    - sentinel_review_note if SENTINEL pool is empty
    - R-SC-2 semantic labels encountered (any label types used beyond parseable-correct/parseable-wrong)

    CC 1.1.0_SA_CTO with same content.
  </objective>

  <compiler_tools_mandate>
    <note>No Python source changes. This TO runs the runner (pre-existing) and writes YAML artifacts.
    ds-commit-gate.sh not required. ANTHROPIC_API_KEY must be set before Phase 1.</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Gates on .072 (R-SC-2 + pre-screen protocol) + .074 (sphinx question pool).
      Does NOT gate on .070 (sidecar) or .071 (pilot machinery) — pre-screen predates 4-condition scoring.
      Does NOT gate on .073 (packet schema) — schema is a COO artifact, not a pre-screen prerequisite.
      .076 (CTO off-ramp gate) gates on this TO.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Both gates confirmed before execution: .072 COMPLETE + .074 COMPLETE.
    2. Zero-shot (C1) judge run completed for all N questions in ab_questions.yaml.
    3. Full-source (v0 compiler) judge run completed for all N questions.
    4. R-SC-2 semantic labels applied to all results.
    5. Per-question YAML artifacts emitted at comp/results/sphinx/prescreen/q&lt;ID&gt;_prescreen.yaml for all questions.
    6. prescreen_summary.yaml written with correct counts.
    7. sentinel_review_note authored if SENTINEL pool is empty.
    8. Preliminary Path B risk assessed and reported in MCP.
    9. Committed --only --author=2.1.0_SC_CompLearns. Pushed to CLOUD.
    10. MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO with commit sha + pool counts + Path B risk.
  </acceptance_criteria>

  <dependencies>
    - Gate 1: .072 COMPLETE (R-SC-2 filed + prescreen_protocol.md authored)
    - Gate 2: .074 COMPLETE (sphinx question pool committed)
    - .070/.071/.073 are parallel — do NOT wait for them
    - .076 (CTO off-ramp gate) gates on this TO.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - ANTHROPIC_API_KEY must be set. Duration: 2*N_questions API calls if cache is cold.
    - "Full-source" for sphinx v0 = imports-only compiled graph. This is NOT as rich as what the
      Stage 3 evolved compiler will produce. The pre-screen result is relative to the current
      compiler state. A question that is Wrong|Wrong under v0 might be INCLUDE under a v5 compiler
      — but that is a post-iteration observation, not a pre-screen concern.
    - Format-aware grader: apply R-SC-2 labels before classifying, not after. A fail from the grader
      may be semantic-correct-but-unparseable — check judge response text before assigning triage category.
    - If any question produces a semantic-ambiguous label: flag it in the MCP and default to INVESTIGATE
      per §2.3. Do not silently assign a label you are not confident in.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO with commit sha + pool counts + Path B risk
    - session log
  </closeout>
</task_order>
