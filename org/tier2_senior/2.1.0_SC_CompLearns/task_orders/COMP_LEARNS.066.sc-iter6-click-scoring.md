<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-066-sc-iter6-click-scoring</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SC_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — click dev-loop iter-6 scoring (gates on .064 COMPLETE; now unblocked)</priority>
  </metadata>

  <references>
    <ref type="ds_delivery">.064 COMPLETE — 1.3.0_DS_CompLearns commit 18563c7a (pushed CLOUD 20260427T140149Z)</ref>
    <ref type="compiler">comp/targets/click/compiler.py — iter-6, class_hierarchy_summary node (Option D)</ref>
    <ref type="compiler_content_sha">ecaf3bc0 (sha256[:8] of iter-6 compiler.py)</ref>
    <ref type="champion">comp/targets/dev-click-001/champion.json — sha 7beb09b, pm=0.1180, baseline_commit=f80cf4b0</ref>
    <ref type="experiment_log">comp/results/dev-click-001/experiment_log.jsonl — 5 iters present [1-5]; iter-6 will be appended by ratchet</ref>
    <ref type="h3_baseline">comp/results/dev-click-001/h3_baseline/h3_v2_result.json — 8/11; improvable: q02, q03, q11</ref>
    <ref type="cto_ruling">1.1.0_SA_CTO session13 20260427T124801Z — Option D targets q03 knowledge error</ref>
    <ref type="iter5_pattern">comp/dev-bundles/dev-click-001/iter-5/result.json — PATTERN C; all selectors flat at 0.0</ref>
  </references>

  <objective>
    Score iter-6 click compiler mutation (class_hierarchy_summary node) against champion.
    Standard dev-loop scoring run — one ratchet iteration, real judge, full per-selector breakdown.

    ## Context

    1.3.0_DS_CompLearns delivered .064 at commit 18563c7a. The iter-6 compiler adds a single
    static fact node to every compile() output:
      id: "hierarchy_summary:click"
      kind: "hierarchy_summary"
      attributes:
        "Group.direct_subclasses": ["_MultiCommand", "CommandCollection"]
        "_BaseCommand.direct_subclasses": ["Group"]

    This is a new mutation family (summary/fact node, not import/class_inherits topology).
    Targets q03: judge error was conflating Group subclasses with direct _BaseCommand inheritors.
    Prior iters 2-5 (import/class_inherits family) all DISCARD with ab_lift=0.0 (PATTERN C confirmed).

    ## Phase 0 — Pre-run gate

    Pull CLOUD and verify iter-6 compiler commit is on CLOUD:
    ```bash
    git pull origin CLOUD --ff-only
    git log --oneline -3
    # Expect: 18563c7a feat(COMP_LEARNS.064): click compiler v6 -- class_hierarchy_summary node
    ```

    If 18563c7a is NOT on HEAD, STOP and MCP COO before proceeding.

    Also verify experiment_log.jsonl has 5 iters:
    ```bash
    python -c "import json; rows=[json.loads(l) for l in open('comp/results/dev-click-001/experiment_log.jsonl')]; print(len(rows), [r['iteration'] for r in rows])"
    # Expect: 5 [1, 2, 3, 4, 5]
    ```

    ## Phase 1 — Scoring run

    From feature_clb root:
    ```bash
    python comp/bin/comp-learns-ratchet dev-click-001 \
      --judge real \
      --max-iter 1 \
      --compiler-content-sha ecaf3bc0
    ```

    Expected exit: MAX_ITER (10). Duration: ~2-3 minutes if cache is warm (all 11 questions
    cached from prior runs); up to ~30 minutes if cold (33 fresh LLM calls).

    The ratchet will auto-append the iter-6 entry to experiment_log.jsonl.

    ## Phase 2 — Read scorecard and assess verdict

    After the run completes, locate the new scorecard:
    ```bash
    ls -t comp/targets/dev-click-001/scorecards/ | head -3
    ```

    Read the scorecard JSON. Report:
    - primary_metric (ab_lift overall)
    - Per-selector breakdown: keyword / centrality / random lift values
    - structural_f1, mutation_stability
    - tied_at_best, random_unique_win
    - Verdict: KEEP if ab_lift > champion 0.1180; DISCARD otherwise

    Per-selector protocol (CTO watch-item from iter-5 retrospective): report keyword/centrality/random
    individually + explicit PATTERN call (A=clean lift, B=keyword-only, C=all flat, or NEW=mixed).

    If ab_lift > 0.0 on ANY selector: read the judge responses for any question that flipped
    correct vs H3-v2 baseline. Note specifically whether q03 flipped (the target question).

    ## Phase 3 — Commit and push

    Commit the result artifacts:
    ```bash
    git add comp/dev-bundles/dev-click-001/iter-6/result.json
    git add comp/results/dev-click-001/experiment_log.jsonl
    git commit --only \
      --author="2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>" \
      -m "score(COMP_LEARNS.066): click iter-6 scoring -- class_hierarchy_summary [VERDICT]" \
      -- comp/dev-bundles/dev-click-001/iter-6/result.json \
         comp/results/dev-click-001/experiment_log.jsonl
    git push origin CLOUD
    ```

    Replace [VERDICT] with KEEP or DISCARD in the commit message.

    Note: experiment_log.jsonl is written by the ratchet runner and must be committed with the
    result.json. If ratchet did not append (cache-only run or error), backfill manually per
    schema_version=3 format (mirror from iter-5 in the log).

    ## Phase 4 — MCP

    MCP 2.1.0_SA_COO with:
    - Commit sha
    - Verdict (KEEP / DISCARD)
    - ab_lift value
    - Per-selector breakdown (keyword/centrality/random)
    - PATTERN call
    - If any question flipped: which QID and judge excerpt for that question
    - experiment_log.jsonl status (auto-appended vs manually backfilled)

    CC 1.1.0_SA_CTO with same content.
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before run">
      <step>
        <run>git pull origin CLOUD --ff-only &amp;&amp; git log --oneline -3</run>
        <expect>18563c7a is HEAD or within last 3 commits.</expect>
        <if_mismatch>STOP. MCP COO — commit not on CLOUD.</if_mismatch>
      </step>
      <step>
        <run>python -c "import json; rows=[json.loads(l) for l in open('comp/results/dev-click-001/experiment_log.jsonl')]; print(len(rows), [r['iteration'] for r in rows])"</run>
        <expect>5 [1, 2, 3, 4, 5]</expect>
        <if_mismatch>STOP. Iter-5 backfill missing. MCP COO.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after run, before commit">
      <step>
        <run>python -c "import json; rows=[json.loads(l) for l in open('comp/results/dev-click-001/experiment_log.jsonl')]; print(len(rows), [r['iteration'] for r in rows])"</run>
        <expect>6 [1, 2, 3, 4, 5, 6] — ratchet appended iter-6</expect>
        <if_mismatch>Manually backfill iter-6 entry before committing.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>python -c "import json; rows=[json.loads(l) for l in open('comp/results/dev-click-001/experiment_log.jsonl')]; last=rows[-1]; print('iter-6 verdict:', last.get('verdict'), 'pm:', last.get('primary_metric'))"</run>
        <expect>iter-6 verdict and primary_metric present in log.</expect>
        <if_mismatch>Backfill was incomplete. Fix before MCP.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      .065 (Option A diagnostic) is concurrent — read-only, no artifact conflict.
      This TO (.066) writes to comp/dev-bundles/dev-click-001/iter-6/ and experiment_log.jsonl.
      No other active writers for these paths.
    </note>
    <shared_artifacts>
      comp/results/dev-click-001/experiment_log.jsonl (DS wrote iter-5 backfill in .064; SC appends iter-6 here)
    </shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. git pull confirms 18563c7a on CLOUD before run.
    2. Ratchet run completes exit=MAX_ITER (or THRESHOLD_REACHED if ab_lift >= 1.30).
    3. Scorecard file written to comp/targets/dev-click-001/scorecards/.
    4. experiment_log.jsonl has 6 iters [1-6] with iter-6 fields complete (schema_version=3).
    5. result.json committed to comp/dev-bundles/dev-click-001/iter-6/ with --author=2.1.0_SC_CompLearns.
    6. Pushed to CLOUD from feature_clb.
    7. MCP 2.1.0_SA_COO with verdict + ab_lift + per-selector breakdown + PATTERN call.
    8. CC 1.1.0_SA_CTO with same content.
    9. Session log with Compiler Tools section.
  </acceptance_criteria>

  <dependencies>
    - Gate: .064 COMPLETE (18563c7a on CLOUD). SATISFIED — unblocked.
    - .065 (Option A diagnostic) — concurrent, no sequencing constraint.
    - Iter-7 strategy (CTO): gates on this verdict + .065 Option A findings.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis in code, logs, or commit messages.
    - Do NOT modify compiler.py — scoring run only; DS owns compiler mutations.
    - If ratchet exits PLATEAU before MAX_ITER, that is also a terminal condition — report verdict as DISCARD.
    - Cache may be partially warm from prior iters. Cache hit reduces LLM calls significantly.
    - ANTHROPIC_API_KEY must be set in environment before running ratchet with --judge real.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha evidence
    - git push origin CLOUD from feature_clb
    - MCP 2.1.0_SA_COO with verdict + ab_lift + per-selector breakdown
    - CC 1.1.0_SA_CTO with same content
    - session log
  </closeout>
</task_order>
