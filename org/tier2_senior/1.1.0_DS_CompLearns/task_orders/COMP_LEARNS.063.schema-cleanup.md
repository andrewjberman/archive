<task_order>
  <metadata>
    <id>1.1.0_DS_CompLearns-2026-04-24-comp-learns-063-schema-cleanup</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.1.0_DS_CompLearns</issued_to>
    <date>2026-04-24</date>
    <status>pending</status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — must land before iter-3 result recording; dispatched via MCP 20260424T180449Z</priority>
  </metadata>

  <references>
    <ref type="cvo_review">org/tier1_exec/3.1.0_SA_CVO/responses/20260424T181500Z_to_1.1.0_SA_CTO_iter_2_ad_hoc_review.md</ref>
    <ref type="cto_surfaced">CTO MCP 20260424T180325Z — R-CTO-1 + R-CTO-2 + R-COO-1</ref>
    <ref type="parent_to">COMP_LEARNS.060 Phase 1 — iter-3 step (d) blocked until this lands</ref>
    <ref type="champion_ruling">COO ruling 20260424T174044Z — champion Option (a): overwrite dev-click-001/champion.json with v0 baseline 0.1180</ref>
  </references>

  <objective>
    Fix two P0 schema issues surfaced by CVO ad-hoc review of iter-2, plus apply champion
    alignment ruling. Must complete before running .060 iter-3 step (d) loop iteration.

    ## R-CTO-1 — Iteration accounting split

    result.json writes `iter=2` (human label) but experiment_log writes `iter=1` (effective
    ratchet iter after invalidation). Diverged. Fix: add two named fields to both schemas:
    - `human_iter_label` (int): sequential human-assigned iteration number (1=first mutation
      attempt, 2=second, 3=third — includes invalidated iters)
    - `ratchet_iter_effective` (int or null): effective ratchet iteration count excluding
      invalidated iters. Invalidated iters = null. iter-2 = 1 (first valid measurement).
      iter-3 = 2 (second valid measurement if scored normally).

    ## R-CTO-2 — compiler_sha split

    `compiler_sha` is overloaded: DS sends mutation commit sha; ratchet.py:600 auto-fills
    `git rev-parse HEAD` (workspace HEAD at scoring time). These diverged in iter-2:
    - DS mutation commit: f781b51d
    - ratchet auto-fill at scoring: 3edd0e62

    Fix: split into two fields across result.json, experiment_log, and scorecard schemas:
    - `compiler_content_sha`: the mutation commit sha DS authored (DS passes this explicitly)
    - `git_commit_sha`: workspace HEAD at scoring time (ratchet.py auto-fills via git rev-parse HEAD)

    ## Champion alignment (per COO ruling 20260424T174044Z)

    Overwrite comp/targets/dev-click-001/champion.json:
    {
      "compiler_sha": "7beb09b",
      "primary_metric": 0.11804865056818183,
      "baseline_commit": "f80cf4b09fbe36099b7bfc065fbde30d053da46d",
      "iteration": 0,
      "timestamp": "2026-04-24T16:30:10Z"
    }

    ## What to change

    ### comp/loop/ratchet.py
    - Line ~600: rename auto-filled SHA field from `compiler_sha` to `git_commit_sha`
    - Add `--compiler-content-sha` CLI argument (passed by SC when invoking ratchet)
    - Write both `compiler_content_sha` and `git_commit_sha` to result.json output
    - Add `human_iter_label` and `ratchet_iter_effective` to result.json output (passed
      as CLI args or derived from caller context)

    ### comp/results/dev-click-001/experiment_log.jsonl
    Retroactive backfill (rename only, no deletions — audit trail preserved):
    - iter-1 entry: add human_iter_label=1, ratchet_iter_effective=null (invalidated),
      compiler_content_sha=79ff544a, git_commit_sha=e3a7d0ff
    - iter-2 entry: add human_iter_label=2, ratchet_iter_effective=1,
      compiler_content_sha=f781b51d, git_commit_sha=3edd0e62

    ### comp/dev-bundles/dev-click-001/iter-3/result.json (after SC places it)
    Backfill before consuming in step (d):
    - compiler_content_sha=2ce75763 (iter-3 mutation commit)
    - git_commit_sha: read from result.json if present; otherwise set to SC's scoring
      commit sha (check git log --author=2.1.0_SC_CompLearns -1)
    - human_iter_label=3, ratchet_iter_effective=2

    ### comp/targets/dev-click-001/champion.json
    Overwrite per Option (a) ruling above.

    ## Timing
    BEFORE step (d) for iter-3. SC is scoring right now — apply backfills to iter-3
    result.json after SC places it, then immediately proceed to step (d) and experiment_log
    recording using the new schema.

    Explicitly out of scope:
    - R-CTO-3 (soft routing-alert on random_unique_win) — P1, separate queue
    - Any other ratchet.py logic changes
    - Touching iter-1/iter-2 result.json files (backfill experiment_log entries only)
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="after ratchet.py edit, before commit">
      <step>
        <run>python -m py_compile comp/loop/ratchet.py</run>
        <expect>Exit 0</expect>
        <if_mismatch>Fix syntax before commit.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh comp/loop/ratchet.py</run>
        <expect>Exit 0</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    1. ratchet.py py_compile + ds-commit-gate clean.
    2. iter-3 result.json has compiler_content_sha + git_commit_sha + human_iter_label=3 + ratchet_iter_effective=2.
    3. experiment_log.jsonl iter-1 + iter-2 entries have all four new fields (backfilled).
    4. champion.json corrected to v0 baseline 0.1180.
    5. Commit --only --author="1.1.0_DS_CompLearns &lt;1.1.0_DS_CompLearns@opal.agent&gt;" -- all changed files.
    6. Pushed to CLOUD.
    7. MCP COMPLETE to 2.1.0_SA_COO with commit sha before proceeding to step (d).
  </acceptance_criteria>

  <dependencies>
    - No prerequisites beyond SC placing iter-3 result.json (for the result.json backfill step).
    - Blocks: .060 iter-3 step (d) loop iteration.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - Dispatched via MCP 20260424T180449Z; this file is the formal TO record.
    - No emojis.
  </operational_notes>

  <closeout>
    - commit --only --author="1.1.0_DS_CompLearns &lt;1.1.0_DS_CompLearns@opal.agent&gt;" -- comp/loop/ratchet.py comp/results/dev-click-001/experiment_log.jsonl comp/dev-bundles/dev-click-001/iter-3/result.json comp/targets/dev-click-001/champion.json
    - push to CLOUD
    - flip TO status complete with commit sha
    - MCP COMPLETE to 2.1.0_SA_COO
  </closeout>
</task_order>
