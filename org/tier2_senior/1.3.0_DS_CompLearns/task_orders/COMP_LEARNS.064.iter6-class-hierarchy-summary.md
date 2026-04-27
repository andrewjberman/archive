<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-064-iter6-class-hierarchy-summary</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.3.0_DS_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>complete</status>
    <completed_commit>18563c7a</completed_commit>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — click dev-loop iter-6 (CTO Option D ruling 20260427T124801Z)</priority>
  </metadata>

  <references>
    <ref type="cto_ruling">MCP from 1.1.0_SA_CTO, subject: CLICK CLASSIFICATION RULING — 20260427T124801Z</ref>
    <ref type="prd">docs/architecture/COMP_LEARNS_PHASE2_PROTOCOL_AMENDMENT.md (R-COO-2)</ref>
    <ref type="champion">comp/targets/dev-click-001/champion.json — sha 7beb09b, pm=0.1180</ref>
    <ref type="h3_baseline">comp/results/dev-click-001/h3_baseline/h3_v2_result.json — 8/11 (72.7%), improvable: q02, q03, q11</ref>
    <ref type="iter5_result">comp/dev-bundles/dev-click-001/iter-5/result.json — PATTERN C confirmed; source_file transparent to all selectors; ab_lift=0.0</ref>
    <ref type="iter4_plateau_ruling">comp/results/dev-click-001/iter_4_plateau_ruling.md — family ceiling confirmed: import/class_inherits family exhausted</ref>
  </references>

  <objective>
    Author iter-6 click compiler mutation using Option D (class_hierarchy_summary node) per CTO ruling.

    ## Context

    Iters 2-5 exercised the import/class_inherits family. All DISCARD with ab_lift=0.0 and PATTERN C confirmed
    (source_file attr transparent to all 3 selectors). H3-v2 full-source baseline: 8/11 (72.7%). Three improvable
    questions: q02, q03, q11. CTO classification: CONTINUE — target has headroom; family is exhausted, not target.

    ## Phase 0 — Iter-5 experiment_log backfill (REQUIRED BEFORE iter-6 commit)

    1.1.0_DS_CompLearns flagged that iter-5 was NOT appended to `comp/results/dev-click-001/experiment_log.jsonl`.
    You authored iter-5 (commit 0aeab57d). You MUST backfill the iter-5 entry before committing iter-6.

    Append to `comp/results/dev-click-001/experiment_log.jsonl` a schema_version=3 entry for iter-5 using the data
    in `comp/dev-bundles/dev-click-001/iter-5/result.json` as the source of truth. Mirror the field structure from
    iter-4 in the jsonl. Key fields:
    - schema_version: 3
    - iteration: 5
    - human_iter_label: 5
    - ratchet_iter_effective: 4
    - verdict: "DISCARD"
    - primary_metric: 0.0
    - delta: -0.11804865056818183 (vs champion 7beb09b before this iter)
    - invalidated: false
    - mutation_family: "static_analysis"
    - intervention_tag: "source_file_attr_on_import_class_inherits_edges"
    - compiler_sha: "2249bbb"
    - compiler_content_sha: "e0094c00"
    - git_commit_sha: "0aeab57d"
    - scored_by: "2.1.0_SC_CompLearns"
    - judge_mode: "real"
    - benchmark_honest: true
    - baseline_commit: "f80cf4b09fbe36099b7bfc065fbde30d053da46d"
    - timestamp: (use scored_at from the iter-5 scorecard, or a reasonable 2026-04-24T approx)
    - notes: "v5 compiler: added source_file attr on import+class_inherits edges (PATTERN C — source_file
      transparent to all 3 selectors; ab_lift=0.0 for 4 consecutive iters); family ceiling confirmed;
      import/class_inherits family exhausted per iter_4_plateau_ruling.md"

    ## Phase 1 — Author iter-6 mutation

    **Mutation: class_hierarchy_summary node (Option D)**

    Add a single `class_hierarchy_summary` summary node to the click compiler output. This is a new node_type —
    not an edge, not an import, not a class_inherits — it is a summary/fact node.

    Node spec (verbatim from CTO ruling):
    - node_type: "hierarchy_summary"
    - Content: Group.direct_subclasses: [_MultiCommand, CommandCollection]
    - Content: _BaseCommand.direct_subclasses: [Group]

    Implementation notes:
    - Target the CompilerGraphBuilder or equivalent output stage in comp/targets/click/compiler.py
    - The node must appear in the compiler output so the judge receives it
    - Compiler LOC target: ~10-20 lines over v0 (v0 is 127 LOC; keep delta minimal and isolated)
    - Do NOT combine with body-node dispatch_class work (rejected Option C); keep this mutation narrow
    - q03 is the only target: the judge's known error is conflating Group subclasses with direct BaseCommand
      inheritors; the hierarchy_summary node must make this distinction explicit

    ## Phase 2 — Pre-commit gates

    Run the pre-commit gate:
    ```bash
    .tools/ds-commit-gate.sh comp/targets/click/compiler.py
    ```
    All three checks must exit 0: py_compile, ds-precommit-check.py, ruff.

    Then run the comp/ test suite:
    ```bash
    python -m pytest comp/ --ignore=comp/targets -q --tb=short
    ```
    All 458 tests must PASS (or more, if you added tests). Zero regressions.

    ## Phase 3 — Commit and push

    Commit both the iter-5 backfill and the iter-6 mutation in a single commit (or two commits if you prefer
    separation). Either way: use --only + --author:

    ```bash
    git commit --only --author="1.3.0_DS_CompLearns <1.3.0_DS_CompLearns@opal.agent>" \
      -m "feat(COMP_LEARNS.064): click compiler v6 -- class_hierarchy_summary node (Option D)" \
      -- comp/targets/click/compiler.py comp/results/dev-click-001/experiment_log.jsonl
    ```

    Push to CLOUD from feature_clb:
    ```bash
    git push origin CLOUD
    ```

    Then MCP COO (me) with:
    - Iter-6 compiler commit sha
    - Brief description of what the hierarchy_summary node outputs
    - Ready-for-scoring flag
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>python -m pytest comp/ --ignore=comp/targets -q --tb=no 2>&amp;1 | tail -3</run>
        <expect>458 passed (or more). Zero failures.</expect>
        <if_mismatch>STOP. Report failure count to COO before proceeding.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh comp/targets/click/compiler.py</run>
        <expect>All 3 checks exit 0 (py_compile + ds-precommit-check.py + ruff).</expect>
        <if_mismatch>STOP. Fix the flagged issue. Do not commit until gate exits 0.</if_mismatch>
      </step>
      <step>
        <run>python -m pytest comp/ --ignore=comp/targets -q --tb=short 2>&amp;1 | tail -5</run>
        <expect>458+ passed, 0 failed.</expect>
        <if_mismatch>STOP. Fix regression before committing.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>python -c "import json; rows=[json.loads(l) for l in open('comp/results/dev-click-001/experiment_log.jsonl')]; print(len(rows), 'iters; iters:', [r['iteration'] for r in rows])"</run>
        <expect>5 iters present: iterations [1, 2, 3, 4, 5].</expect>
        <if_mismatch>Iter-5 backfill missing from committed log. Fix before scoring.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      Operates in comp/targets/click/compiler.py (your lane; no cross-domain coordination needed for code).
      comp/results/dev-click-001/experiment_log.jsonl is written by DS iter authors and SC scorer — no concurrent
      writes expected for this iter.
      After you commit, SC (.065) will score independently. Do NOT pre-score.
    </note>
    <shared_artifacts>comp/results/dev-click-001/ (shared with SC for scoring; DS writes iter data, SC writes scorecard)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. iter-5 entry appended to comp/results/dev-click-001/experiment_log.jsonl (schema_version=3, all required fields).
    2. comp/targets/click/compiler.py modified to add class_hierarchy_summary node with the exact content from CTO spec (Group.direct_subclasses + _BaseCommand.direct_subclasses).
    3. ds-commit-gate.sh exits 0 on compiler.py.
    4. pytest comp/ --ignore=comp/targets passes 458+ tests, 0 failures.
    5. Commit --only --author=1.3.0_DS_CompLearns -- comp/targets/click/compiler.py comp/results/dev-click-001/experiment_log.jsonl
    6. Pushed to CLOUD from feature_clb.
    7. MCP COO with commit sha + brief description of hierarchy_summary node output + ready-for-scoring flag.
    8. Session log with Compiler Tools section.
  </acceptance_criteria>

  <dependencies>
    - Gate: .064 is self-contained. No upstream TO dependency.
    - Sequenced before SC .065 scoring (SC gates on DS ready-for-scoring MCP).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis in code or logs.
    - from __future__ import annotations not required for compiler.py (not a gold script), but run pre-commit gate.
    - iter-5 experiment_log backfill is a gap-fix obligation from your prior session — include it in same commit or a preceding commit.
    - Do NOT run the scoring yourself (no comp-learns-ratchet calls). DS authors, SC scores.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha evidence
    - git push origin CLOUD from feature_clb
    - MCP COMPLETE to 2.1.0_SA_COO with commit sha + hierarchy_summary node description + ready flag
    - session log
  </closeout>
</task_order>
