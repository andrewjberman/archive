<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-068-sc-iter7-click-scoring</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — click dev-loop iter-7 scoring (gates on .067 COMPLETE; now unblocked)</priority>
  </metadata>

  <references>
    <ref type="ds_delivery">.067 COMPLETE — commits f5095ac0 (path fix) + 7ee0859c (compiler v7) pushed CLOUD 20260427T150543Z</ref>
    <ref type="compiler">comp/targets/click/compiler.py — iter-7, class_hierarchy_correction node (Command-perspective NOT-exclusion)</ref>
    <ref type="compiler_content_sha">923071d5 (sha256[:8] of iter-7 compiler.py)</ref>
    <ref type="champion">comp/targets/dev-click-001/champion.json — sha 7beb09b, pm=0.1180, baseline_commit=f80cf4b0</ref>
    <ref type="experiment_log">comp/results/dev-click-001/experiment_log.jsonl — 6 iters [1-6]; path fix in .067 means runner now appends here directly</ref>
    <ref type="h3_baseline">comp/results/dev-click-001/h3_baseline/h3_v2_result.json — 8/11 (minimum 9/11 per R-SC-1); improvable: q02, q03, q11</ref>
    <ref type="iter6_result">comp/dev-bundles/dev-click-001/iter-6/result.json — DISCARD PATTERN C</ref>
    <ref type="r_sc_1">comp/results/dev-click-001/scoring_regime_honesty_note.md — q02/q11 format-variance ambiguity documented</ref>
    <ref type="cto_ruling">1.1.0_SA_CTO 20260427T144011Z — ITER-7 SPEC AMENDMENT P0 — q03-only, Command-perspective NOT-exclusion</ref>
  </references>

  <objective>
    Score iter-7 click compiler mutation (class_hierarchy_correction node) against champion.
    Standard dev-loop scoring run — one ratchet iteration, real judge, full per-selector breakdown.

    ## Context

    1.3.0_DS_CompLearns delivered .067 at commits f5095ac0 + 7ee0859c. The iter-7 compiler
    replaces the iter-6 hierarchy_summary (Group-perspective) with a class_hierarchy_correction
    node (Command-perspective with NOT-exclusion):

      id: "hierarchy_correction:click"
      kind: "class_hierarchy_correction"
      attributes:
        "Command.direct_subclasses": ["_BaseCommand", "Group"]
        "_MultiCommand.parent_class": "Group (NOT a direct Command subclass)"
        "CommandCollection.parent_class": "Group (NOT a direct Command subclass)"

    CTO diagnosis of iter-6 failure: Group-perspective encodes what judge already knows (q04 correct).
    The corrective signal must come from Command's perspective. The NOT-exclusion strings are
    load-bearing for q03 — judge must see that _MultiCommand and CommandCollection are NOT Command's
    direct inheritors.

    Path fix: .067 Phase 0 fixed runner.py so the ratchet now writes experiment_log entries directly
    to comp/results/dev-click-001/experiment_log.jsonl (schema v3). No manual backfill needed this iter.

    R-SC-1 note: q02/q11 failures are format-variance, not semantic error. iter-7 targets q03 only.
    If q02/q11 flip, note it but do not treat as genuine evidence of compiler improvement — see
    comp/results/dev-click-001/scoring_regime_honesty_note.md.

    ## Phase 0 — Pre-run gate

    Pull CLOUD and verify iter-7 compiler commits are present:
    ```bash
    git pull origin CLOUD --ff-only
    git log --oneline -5
    # Expect: 7ee0859c feat(COMP_LEARNS.067): click compiler v7 -- class_hierarchy_correction node
    #          f5095ac0 fix(COMP_LEARNS.067): experiment_log path -- runner resolves v3 log at comp/results/dev-click-001/
    ```

    If 7ee0859c is NOT on HEAD, STOP and MCP COO before proceeding.

    Verify experiment_log has 6 iters (runner path fix now means runner writes here directly):
    ```bash
    python3 -c "import json; rows=[json.loads(l) for l in open('comp/results/dev-click-001/experiment_log.jsonl')]; print(len(rows), [r['iteration'] for r in rows])"
    # Expect: 6 [1, 2, 3, 4, 5, 6]
    ```

    ## Phase 1 — Scoring run

    From feature_clb root:
    ```bash
    python comp/bin/comp-learns-ratchet click \
      --judge real \
      --max-iter 1 \
      --compiler-content-sha 923071d5
    ```

    Expected exit: MAX_ITER (10). Duration: ~2-3 minutes if cache warm; up to ~30 minutes if cold.
    With the path fix, ratchet will append iter-7 directly to comp/results/dev-click-001/experiment_log.jsonl.

    ## Phase 2 — Read scorecard and assess verdict

    After run completes, locate the new scorecard:
    ```bash
    ls -t comp/targets/click/scorecards/ | head -3
    ```

    Read the scorecard JSON. Report:
    - primary_metric (ab_lift overall)
    - Per-selector breakdown: keyword / centrality / random lift values
    - structural_f1, mutation_stability
    - tied_at_best, random_unique_win
    - Verdict: KEEP if ab_lift > champion 0.1180; DISCARD otherwise

    Per-selector protocol: report keyword/centrality/random individually + explicit PATTERN call
    (A=clean lift, B=keyword-only, C=all flat, or NEW=mixed).

    If ab_lift > 0.0 on ANY selector: read the judge responses for any question that flipped
    correct vs H3-v2 baseline. Note specifically whether q03 flipped (the target question).

    R-SC-1 note for flip reporting: if q02 or q11 flip, document the judge response format
    (bare numeric vs verbose) to distinguish genuine improvement from format accident. See
    scoring_regime_honesty_note.md.

    ## Phase 3 — Verify experiment log auto-append

    The path fix in .067 means experiment_log.jsonl should now auto-append without manual backfill.
    Verify after run:
    ```bash
    python3 -c "import json; rows=[json.loads(l) for l in open('comp/results/dev-click-001/experiment_log.jsonl')]; print(len(rows), [r['iteration'] for r in rows])"
    # Expect: 7 [1, 2, 3, 4, 5, 6, 7]
    ```

    If NOT 7 entries: the path fix did not work as expected. Manually backfill per schema_version=3
    format (mirror from iter-6 in the log) and note "manual backfill" in MCP.

    ## Phase 4 — Commit and push

    Commit the result artifacts:
    ```bash
    git add comp/dev-bundles/dev-click-001/iter-7/result.json
    git add comp/results/dev-click-001/experiment_log.jsonl
    git commit --only \
      --author="2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>" \
      -m "score(COMP_LEARNS.068): click iter-7 scoring -- class_hierarchy_correction [VERDICT]" \
      -- comp/dev-bundles/dev-click-001/iter-7/result.json \
         comp/results/dev-click-001/experiment_log.jsonl
    git push origin CLOUD
    ```

    Replace [VERDICT] with KEEP or DISCARD in the commit message.

    ## Phase 5 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Verdict (KEEP / DISCARD)
    - ab_lift value
    - Per-selector breakdown (keyword/centrality/random)
    - PATTERN call
    - Whether q03 flipped (YES/NO) and judge excerpt if YES
    - experiment_log.jsonl status (auto-appended vs manually backfilled)
    - Any q02/q11 flip (format note per R-SC-1 if applicable)

    CC 1.1.0_SA_CTO with same content.
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before run">
      <step>
        <run>git pull origin CLOUD --ff-only &amp;&amp; git log --oneline -3</run>
        <expect>7ee0859c is HEAD or within last 3 commits.</expect>
        <if_mismatch>STOP. MCP COO — commits not on CLOUD.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "import json; rows=[json.loads(l) for l in open('comp/results/dev-click-001/experiment_log.jsonl')]; print(len(rows), [r['iteration'] for r in rows])"</run>
        <expect>6 [1, 2, 3, 4, 5, 6]</expect>
        <if_mismatch>STOP. MCP COO.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after run, before commit">
      <step>
        <run>python3 -c "import json; rows=[json.loads(l) for l in open('comp/results/dev-click-001/experiment_log.jsonl')]; print(len(rows), [r['iteration'] for r in rows])"</run>
        <expect>7 [1, 2, 3, 4, 5, 6, 7] — ratchet auto-appended iter-7 via path fix</expect>
        <if_mismatch>Manually backfill iter-7 entry before committing. Note in MCP.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>python3 -c "import json; rows=[json.loads(l) for l in open('comp/results/dev-click-001/experiment_log.jsonl')]; last=rows[-1]; print('iter-7 verdict:', last.get('verdict'), 'pm:', last.get('primary_metric'))"</run>
        <expect>iter-7 verdict and primary_metric present in log.</expect>
        <if_mismatch>Backfill was incomplete. Fix before MCP.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      No concurrent writers. This TO writes to comp/dev-bundles/dev-click-001/iter-7/ and
      comp/results/dev-click-001/experiment_log.jsonl.
    </note>
    <shared_artifacts>
      comp/results/dev-click-001/experiment_log.jsonl (DS wrote path fix in .067; runner now appends here directly)
    </shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. git pull confirms 7ee0859c on CLOUD before run.
    2. Ratchet run completes exit=MAX_ITER (or THRESHOLD_REACHED if ab_lift >= 1.30).
    3. Scorecard file written to comp/targets/click/scorecards/.
    4. experiment_log.jsonl has 7 iters [1-7] with iter-7 fields complete (schema_version=3).
    5. result.json committed to comp/dev-bundles/dev-click-001/iter-7/ with --author=2.1.0_SC_CompLearns.
    6. Pushed to CLOUD from feature_clb.
    7. MCP 2.1.0_SA_COO with verdict + ab_lift + per-selector breakdown + PATTERN call + q03 flip status.
    8. CC 1.1.0_SA_CTO with same content.
    9. Session log with Compiler Tools section.
  </acceptance_criteria>

  <dependencies>
    - Gate: .067 COMPLETE (7ee0859c on CLOUD). SATISFIED — unblocked.
    - R-SC-2 (semantic-correct-but-unparseable audit label): non-blocking for iter-7, required before iter-8.
    - Iter-8 strategy: gates on this verdict + CTO assessment.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis in code, logs, or commit messages.
    - Do NOT modify compiler.py — scoring run only; DS owns compiler mutations.
    - If ratchet exits PLATEAU before MAX_ITER, that is also a terminal condition — report verdict as DISCARD.
    - ANTHROPIC_API_KEY must be set before running ratchet with --judge real.
    - experiment_log path fix is live — expect auto-append; note if manual backfill required.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha evidence
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO with verdict + ab_lift + per-selector breakdown
    - CC 1.1.0_SA_CTO with same content
    - session log
  </closeout>
</task_order>
