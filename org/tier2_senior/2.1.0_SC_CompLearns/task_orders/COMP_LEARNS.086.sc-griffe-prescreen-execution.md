<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-086-sc-griffe-prescreen-execution</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>staged</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — gates CTO off-ramp ruling and packet authoring dispatch</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §2 — Pre-screen triage matrix; §2.5 — Output schema. §10 ship-blocker: "Path B pre-screen (griffe)"</ref>
    <ref type="prd_section">§7.3 — Path B sequencing. §7.4 — authored-pool guardrail (>=2 families). §11 — V1.2 grader-governance (dual-grader + disagreement).</ref>
    <ref type="sub_prd">docs/architecture/COMP_LEARNS_STAGE3_PATH_B.md V1 ACCEPTED — §6 dispatch sequence Step 3</ref>
    <ref type="question_pool">comp/backlog/benchmark/bl-griffe-001.yaml — authored in COMP_LEARNS.085 (e4dc9246); 16 questions, 4 families (A=5, B=3, C=4, D=4)</ref>
    <ref type="r_sc_2">comp/results/r_sc_2_semantic_labels.md — semantic label taxonomy (6 primary + extended per .078)</ref>
    <ref type="governance">V1.2 §11 grader-governance: dual-grader (exact-match + semantic_grader.py per .077), R-SC-2 labels (.078), per-question disagreement_flag + summary disagreement_rate (.079)</ref>
    <ref type="consumer">CTO off-ramp ruling gates on this TO: INCLUDE >= 5 → packet authoring + 4-condition case dispatch; INCLUDE &lt; 5 → fallback to awkward-array</ref>
  </references>

  <objective>
    Execute the Stage 3 griffe pre-screen: run zero-shot (C1) and full-source for each griffe
    candidate question; apply V1.2/V1.3 dual-grader governance with R-SC-2 labels and
    disagreement tracking; emit per-question YAML + summary; assess off-ramp trigger.

    ## Gate — confirm before proceeding

    COMP_LEARNS.085 COMPLETE — bl-griffe-001.yaml committed at e4dc9246.

    ```bash
    python3 -c "import yaml; qs=yaml.safe_load(open('comp/backlog/benchmark/bl-griffe-001.yaml')); print(len(qs['questions']), 'questions')"
    # Expect: 16
    ```

    ## Phase 0 — Pre-run setup

    Pull CLOUD to get .085 artifact:
    ```bash
    cd /c/Users/AndrewBerman/Desktop/feature_clb
    git pull origin CLOUD --ff-only
    ```

    Read R-SC-2 taxonomy before running:
    ```bash
    cat comp/results/r_sc_2_semantic_labels.md
    ```

    Note on "full-source" for griffe: no griffe-specific compiler exists yet (packet authoring TOs
    will build it post-CTO approval). For this pre-screen, "full-source" = raw Python source content
    of the relevant file(s) from packages/griffelib/src/griffe/_internal/ delivered directly as judge
    context. This is the upper-bound baseline: if even raw source delivery doesn't produce retrieval
    gain, INCLUDE is very unlikely from any compiler. Raw source delivery is consistent with "best
    available compiler output" doctrine for targets without an existing compiler.

    Source delivery mechanic: for each question, read gold_source_file from bl-griffe-001.yaml
    and deliver that file's raw Python content as the compiler context string.

    ANTHROPIC_API_KEY must be set before Phase 1.

    ## Phase 1 — Zero-shot run (C1) for each question

    For each question in bl-griffe-001.yaml:
    - Run judge with NO compiler context (C1 = unaided, zero-shot)
    - Apply exact-match grader → exact_match_label: pass | fail
    - Apply semantic_grader.py → semantic_label + semantic_pass: true | false
    - Record disagreement_flag: true if exact_match_label != semantic_pass result

    ## Phase 2 — Full-source run for each question

    For each question:
    - Deliver raw Python source of gold_source_file as judge context
    - Apply exact-match grader → exact_match_label: pass | fail
    - Apply semantic_grader.py → semantic_label + semantic_pass: true | false
    - Record disagreement_flag

    ## Phase 3 — Apply R-SC-2 labels and triage matrix

    For each question, using zero-shot and full-source results:

    1. Assign R-SC-2 semantic_label to each result per .072 taxonomy:
       - parseable-correct | parseable-wrong | semantic-correct-but-unparseable | semantic-wrong-unparseable | semantic-ambiguous | semantic-partial-correct-unparseable (sixth label per .078)

    2. Apply triage matrix (§2.2), governed by V1.2 semantic-aware triage:
       - Wrong (zero-shot) + Correct (full-source) → INCLUDE — clear retrieval gain
       - Correct (zero-shot) + Correct (full-source) → SENTINEL — prior-dominated
       - Wrong + Wrong → INVESTIGATE (subtype TBD)
       - Correct + Wrong → INVESTIGATE (grader/context-overload artifact)

       For INVESTIGATE subtypes per §2.4 + R-SC-2 labels:
       - Both regimes produce semantic-correct-but-unparseable → grader_artifact, pilot_eligible=false
       - Both regimes produce semantic-partial-correct-unparseable → grader_artifact, pilot_eligible=false
       - Confident ceiling diagnosis → ceiling, pilot_eligible=false
       - Confident full_source_overload_candidate → full_source_overload_candidate, pilot_eligible=true
       - Cannot distinguish → unresolved, pilot_eligible=true (default)

    3. V1.2 governance — triage uses SEMANTIC grader as the governance authority, not just exact-match:
       - If exact-match says fail but semantic says pass (parseable-correct or semantic-correct-but-unparseable): treat as Correct for triage
       - Document every disagreement_flag=true case in MCP so CTO can review triage boundary decisions

    ## Phase 4 — Emit pre-screen artifacts

    Per-question YAML at:
    ```
    comp/results/griffe/prescreen/q&lt;ID&gt;_prescreen.yaml
    ```

    Per-question schema (V1.2/V1.3 — adds disagreement fields vs sphinx .075 schema):
    ```yaml
    question_id: griffe-001
    zero_shot_result:
      exact_match_label: pass | fail
      semantic_label: parseable-correct | parseable-wrong | semantic-correct-but-unparseable | semantic-wrong-unparseable | semantic-ambiguous | semantic-partial-correct-unparseable
      semantic_pass: true | false
      disagreement_flag: true | false
    full_source_result:
      exact_match_label: pass | fail
      semantic_label: &lt;same options&gt;
      semantic_pass: true | false
      disagreement_flag: true | false
    triage_decision: INCLUDE | SENTINEL | INVESTIGATE
    triage_basis: exact_match | semantic_override  # which grader determined triage
    include_reason: &lt;required if INCLUDE&gt;
    sentinel_reason: &lt;required if SENTINEL&gt;
    investigate_subtype: full_source_overload_candidate | grader_artifact | ceiling | unresolved
    pilot_eligible: true | false
    notes: &lt;optional — semantic disagreement details, sixth-label occurrences&gt;
    ```

    Summary at:
    ```
    comp/results/griffe/prescreen/prescreen_summary.yaml
    ```

    ```yaml
    target: griffe
    version: v2.0.0
    date: &lt;ISO8601&gt;
    authored_by: 2.1.0_SC_CompLearns
    question_count: 16
    include_count: N
    sentinel_count: N
    investigate_count: N
    pilot_eligible_count: N
    disagreement_rate: N.NN   # fraction of questions where exact-match != semantic grader
    sentinel_review_note: null  # if sentinel_count > 0; author review note if sentinel_count == 0
    path_b_trigger_1: true | false  # INCLUDE &lt; 5
    path_b_trigger_2: true | false  # SENTINEL &gt; 50% of total
    off_ramp_recommendation: PASS | FALLBACK_AWKWARD_ARRAY  # preliminary, CTO rules
    ```

    ## Phase 5 — Off-ramp preliminary assessment

    Before committing:
    - INCLUDE &lt; 5? → path_b_trigger_1=true; recommend FALLBACK_AWKWARD_ARRAY
    - SENTINEL &gt; 8 (50% of 16)? → path_b_trigger_2=true; flag regardless of INCLUDE count
    - If neither trigger fires: INCLUDE &gt;= 5 and SENTINEL &lt;= 8 → recommend PASS

    Report the off-ramp recommendation in MCP. CTO makes the formal ruling.

    Note: if disagreement_rate is high (&gt; 0.30), flag as a V1.2 governance watch item even if
    triage proceeds to PASS. This informs CTO's quality read on the pool.

    ## Phase 6 — Commit and push

    ```bash
    git add comp/results/griffe/prescreen/
    git commit --only \
      --author="2.1.0_SC_CompLearns &lt;2.1.0_SC_CompLearns@opal.agent&gt;" \
      -m "score(COMP_LEARNS.086): griffe v2.0.0 pre-screen -- N_INCLUDE INCLUDE + N_SENTINEL SENTINEL + N_INVESTIGATE INVESTIGATE" \
      -- comp/results/griffe/prescreen/
    git push origin CLOUD
    ```

    Replace N_INCLUDE, N_SENTINEL, N_INVESTIGATE with actual counts.

    ## Phase 7 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Question count: total / INCLUDE / SENTINEL / INVESTIGATE / pilot_eligible
    - disagreement_rate (fraction)
    - Per-category summary (not per-question)
    - Off-ramp recommendation (PASS or FALLBACK_AWKWARD_ARRAY) with trigger status
    - Investigate subtype breakdown (unresolved / grader_artifact / ceiling / full_source_overload)
    - sentinel_review_note if SENTINEL == 0
    - Any sixth-label (semantic-partial-correct-unparseable) occurrences

    CC 1.1.0_SA_CTO with same content.
  </objective>

  <compiler_tools_mandate>
    <note>No Python source changes. This TO runs the runner (pre-existing) and writes YAML artifacts.
    ds-commit-gate.sh not required. ANTHROPIC_API_KEY must be set before Phase 1.
    comp-build not required. pytest not required.</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Gates on COMP_LEARNS.085 (griffe question pool committed at e4dc9246).
      CTO off-ramp gate follows: CTO reads prescreen_summary.yaml and issues ruling.
      Does NOT gate on any other active TO — this is the sole blocker for Path B progression.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Gate confirmed: comp/backlog/benchmark/bl-griffe-001.yaml present (16 questions).
    2. Zero-shot (C1) judge run completed for all 16 questions in bl-griffe-001.yaml.
    3. Full-source (raw gold_source_file content) judge run completed for all 16 questions.
    4. Both exact-match and semantic grader applied per question (V1.2 dual-grader).
    5. R-SC-2 semantic labels applied to all results (including sixth-label where applicable).
    6. disagreement_flag recorded per question per regime.
    7. Per-question YAML artifacts at comp/results/griffe/prescreen/q&lt;ID&gt;_prescreen.yaml (16 files).
    8. prescreen_summary.yaml written with correct counts + disagreement_rate + off-ramp fields.
    9. sentinel_review_note authored if SENTINEL pool is empty.
    10. Off-ramp recommendation (PASS / FALLBACK) stated in summary + MCP.
    11. Committed --only --author=2.1.0_SC_CompLearns. Pushed to CLOUD.
    12. MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO with commit sha + counts + disagreement_rate + off-ramp rec.
  </acceptance_criteria>

  <dependencies>
    - Gate: COMP_LEARNS.085 COMPLETE (e4dc9246) — bl-griffe-001.yaml available
    - No other active TOs gate this
    - CTO off-ramp ruling gates ON this TO
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - ANTHROPIC_API_KEY must be set. Duration: 2 * 16 = 32 API calls if cache cold.
    - "Full-source" for griffe = raw Python source of gold_source_file delivered as context string.
      No griffe compiler exists yet — raw source IS the upper-bound baseline.
    - Format-aware grader: apply semantic grader before final triage classification. A fail
      from exact-match may be semantic-correct-but-unparseable — check judge response text.
    - If any question produces semantic-ambiguous: flag in MCP, default to INVESTIGATE (§2.3).
    - V1.2 governance note: when exact-match and semantic grader disagree, semantic grader
      governs triage per V1.2 §11. Document every such case — CTO reviews at off-ramp.
    - disagreement_rate &gt; 0.30 is a quality watch item even if triage is PASS.
    - griffe v2.0.0 source path: packages/griffelib/src/griffe/_internal/ (v2 monorepo).
      All gold_source_file values in bl-griffe-001.yaml reference this path. Use the pinned
      v2.0.0 tag when fetching source content for full-source runs.
  </operational_notes>

  <closeout>
    - Flip TO status to complete with commit sha evidence
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO + CC 1.1.0_SA_CTO with commit sha + counts + disagreement_rate + off-ramp
    - Session log
  </closeout>
</task_order>
