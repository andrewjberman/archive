<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-077-sc-sphinx-q03q05-capped-pilot</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — diagnostic, non-blocking; parallel with .078/.079/.080/.081 (V1.2 R-COO-1 authorization)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_STAGE3.md §11.4 — sphinx q03/q05 narrow pilot scope and caps</ref>
    <ref type="ruling">COMP_LEARNS.076 ruling §6 action sequence — pilot authorized in parallel with grader-governance</ref>
    <ref type="prescreen">comp/results/sphinx/prescreen/ — q03_prescreen.yaml + q05_prescreen.yaml (pilot_eligible=true, unresolved)</ref>
    <ref type="pilot_machinery">comp/loop/runner.py run_pilot() — --pilot mode, N=8, C4+C1 paired conditions</ref>
  </references>

  <objective>
    Run a capped diagnostic pilot on sphinx q03 and q05 — the two questions classified
    INVESTIGATE/unresolved/pilot_eligible=true in the .075 pre-screen.

    ## Scope cap (V1.2 §11.4 R-COO-2 P1 — strictly enforced)

    - Pilot answers ONE diagnostic question: "do q03/q05 show any C4-over-C1 lift worth
      preserving as a design signal?"
    - Pilot does NOT morph into sphinx primary case continuation
    - Pilot does NOT trigger packet authoring or pool preregistration
    - Pilot does NOT override PATH_B_MANDATORY ruling from .076
    - Results are diagnostic only — not promotion evidence

    ## Context

    q03 (StandaloneHTMLBuilder): Judge gives 'Builder' consistently in C1 and full-source.
    The correct answer requires knowing the intermediate HTML builder layer in sphinx's
    inheritance chain. The v0 imports-only compiler has no class hierarchy signal.

    q05 (DocstringSignatureMixin, ModuleLevelDocumenter): Judge gives wrong mixin name
    (DocstringStripSignatureMixin — training data artifact) in C1. Full-source added noise
    (ClassLevelDocumenter for second base class). No class hierarchy from v0 compiler.

    Both are classified semantic-wrong under both C1 and full-source — genuinely wrong, not
    grader_artifact. The v0 sphinx compiler is imports-only; it provides no class hierarchy
    edges. The pilot question is whether the KEYWORD selector's graph retrieval (C4) still
    finds useful context despite compiler limits.

    ## Phase 0 — Pre-pilot gate

    Confirm .079 is NOT required before running the pilot. This pilot uses the existing
    exact-match grader (V1.2 grader-governance has not shipped). SC must apply manual R-SC-2
    semantic labels to the pilot responses as best-effort audit, separate from grader output.

    Verify sphinx compiler is current and target repo is pinned:
    ```bash
    cat comp/targets/sphinx/repo_pin.txt
    # Expect: 36367765fe780f962bba861bf368a765380bbc68
    python3 -c "from comp.targets.sphinx.compiler import compile; print('OK')"
    ```

    ## Phase 1 — Run capped pilot

    ```bash
    cd /c/Users/AndrewBerman/Desktop/feature_clb
    python3 comp/bin/comp-learns-ratchet sphinx \
      --pilot \
      --questions q03,q05 \
      --judge real \
      --n 8
    ```

    Expected output:
    - comp/results/sphinx/pilot/<timestamp>/pilot_q03.json
    - comp/results/sphinx/pilot/<timestamp>/pilot_q05.json
    - comp/results/sphinx/pilot/<timestamp>/pilot_summary.json

    Duration: 2 questions × 8 trials × 2 conditions (C4 + C1) = 32 API calls. ~5–8 min.

    ANTHROPIC_API_KEY: retrieve from AWS Secrets Manager as in prior sessions.

    ## Phase 2 — Apply manual R-SC-2 labels to pilot responses

    Read each trial's response text from the pilot artifact (pilot_q03.json, pilot_q05.json
    contain per-trial response text). Apply R-SC-2 semantic labels manually:
    - Is the response semantic-wrong-unparseable (genuinely wrong answer in prose)?
    - Or semantic-correct-but-unparseable (correct answer in prose but parseable fails)?
    - Exact-match grader result and R-SC-2 label recorded separately

    Since V1.2 dual-output grader (.078) is not yet shipped, this is best-effort manual audit.
    Record distribution: N_parseable-wrong, N_semantic-correct-but-unparseable, N_semantic-wrong-
    unparseable, N_semantic-ambiguous for both C1 and C4 conditions.

    ## Phase 3 — Assess dual-condition gate

    Per PRD §5.2 pilot decision rule:
    - PROMOTE to INCLUDE if C4 success rate >= 5/8 AND (C4 - C1) >= 2
    - DEMOTE (ceiling) if C4 success rate <= 1/8
    - DEMOTE (prior-dominated) if C1 success rate >= 6/8 AND delta <= 0
    - Otherwise: hold INVESTIGATE / diagnostic

    Given that v0 is imports-only with no class hierarchy edges, the prior expectation is
    that C4 will NOT significantly exceed C1 for q03 and q05 (keyword selector cannot
    surface what the compiler did not emit). A null pilot result here is informative:
    it confirms that class_hierarchy compiler mutations are required, not just better
    question selection.

    ## Phase 4 — Author pilot diagnostic note

    Write a brief diagnostic note at:
    comp/results/sphinx/pilot/<timestamp>/pilot_diagnostic_note.md

    Cover:
    1. C4 vs C1 decision rule outcome (PROMOTE / DEMOTE / hold) for each question
    2. R-SC-2 semantic label distribution for both conditions
    3. Whether the pilot result supports class_hierarchy compiler mutation as the
       required next step (consistent with the v0 imports-only limitation)
    4. Reaffirmation that this pilot does NOT advance sphinx toward primary case dispatch

    ## Phase 5 — Commit and push

    ```bash
    git add comp/results/sphinx/pilot/
    git commit --only \
      --author="2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>" \
      -m "pilot(COMP_LEARNS.077): sphinx q03/q05 capped diagnostic -- C4 vs C1 lift assessment" \
      -- comp/results/sphinx/pilot/
    git push origin CLOUD
    ```

    ## Phase 6 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Per-question: C4 successes / C1 successes / delta / decision rule outcome
    - R-SC-2 label distribution (manual audit)
    - Whether the pilot result signals class_hierarchy compiler as the required mutation
    - Restatement: pilot result does NOT change PATH_B_MANDATORY or trigger packet authoring
  </objective>

  <compiler_tools_mandate>
    <note>No Python source changes. Uses existing --pilot mode runner. ds-commit-gate.sh not required.
    ANTHROPIC_API_KEY must be set before Phase 1.</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Parallel with .078/.079/.080/.081 — no shared artifacts.
      Pilot does NOT gate any downstream TO.
      PATH_B_MANDATORY and HOLD on Path B re-selection remain independent of pilot results.
      Pilot result is informational input to CTO/CVO only.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Pilot run completed for q03 and q05 (N=8 per condition per question).
    2. Per-trial response text read and R-SC-2 semantic labels applied manually.
    3. Dual-condition gate evaluated for both questions.
    4. pilot_diagnostic_note.md authored (scope cap reaffirmed, no packet authoring triggered).
    5. Committed --only --author=2.1.0_SC_CompLearns. Pushed CLOUD.
    6. MCP 2.1.0_SA_COO with decision rule outcomes + R-SC-2 distribution + class_hierarchy signal.
  </acceptance_criteria>

  <dependencies>
    - No upstream gate. Can run immediately.
    - Informational dependency: .078/.079/.080 grader-governance work is parallel and does not gate this pilot.
    - .076 ruling is already complete (PATH_B_MANDATORY, q01/q07 reclassified).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis.
    - SCOPE CAP IS HARD: pilot is diagnostic only. No packet authoring, no pool preregistration,
      no sphinx continuation. If C4 shows lift on q03 or q05, the correct action is to flag as
      a design signal in the MCP — not to author a new sphinx iteration.
    - Grader: exact-match only (V1.2 grader-governance not yet shipped). Best-effort manual
      R-SC-2 audit on responses.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO with pilot results
    - session log
  </closeout>
</task_order>
