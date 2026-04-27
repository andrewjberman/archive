<task_order>
  <metadata>
    <id>2.1.0_SA_COO-2026-04-27-comp-learns-067-iter7-class-hierarchy-correction</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.3.0_DS_CompLearns</issued_to>
    <date>2026-04-27</date>
    <status>staged</status>
    <hold>GO pending: (1) SC R-SC-1 scoring-regime honesty note filed; (2) this TO committed with q03-only spec amendment. Do NOT begin until GO received from COO.</hold>
    <project_code>COMP_LEARNS</project_code>
    <priority>P0 — click dev-loop iter-7 (CTO P0 spec amendment 20260427T144011Z + CVO R-CTO-1/R-COO-1)</priority>
  </metadata>

  <references>
    <ref type="cto_ruling">1.1.0_SA_CTO 20260427T142454Z — ITER-7 STRATEGY RULING (original, superseded by amendment)</ref>
    <ref type="cto_amendment">1.1.0_SA_CTO 20260427T144011Z — ITER-7 SPEC AMENDMENT P0 — q03-only, answer injection disqualified</ref>
    <ref type="cvo_ruling">org/tier1_exec/3.1.0_SA_CVO/responses/20260427T143500Z_to_1.1.0_SA_CTO_iter6_iter7_review.md</ref>
    <ref type="iter6_result">comp/dev-bundles/dev-click-001/iter-6/result.json — DISCARD, PATTERN C, q03 did not flip</ref>
    <ref type="champion">comp/targets/dev-click-001/champion.json — sha 7beb09b, pm=0.1180, baseline_commit=f80cf4b0</ref>
    <ref type="h3_baseline">comp/results/dev-click-001/h3_baseline/h3_v2_result.json — 8/11; improvable: q02, q03, q11</ref>
    <ref type="iter6_compiler">comp/targets/click/compiler.py at 18563c7a — v6, hierarchy_summary node (Group-perspective, now superseded)</ref>
    <ref type="experiment_log">comp/results/dev-click-001/experiment_log.jsonl — 6 iters [1-6]; path mismatch fix required in Phase 0</ref>
  </references>

  <objective>
    Author iter-7 click compiler mutation: single `class_hierarchy_correction` node targeting q03,
    Command-perspective framing with explicit NOT-exclusion signals.

    ## Ruling context

    Iter-6 (hierarchy_summary, Group-perspective) DISCARD PATTERN C. CTO diagnosis: spec error —
    Group-perspective encodes what the judge already knows (q04 correct). Corrective signal must come
    from Command's perspective: what are Command's DIRECT subclasses, and what are NOT.

    CVO ruling (R-CTO-1, R-COO-1): q02/q11 numeric-fact nodes are answer injection under the current
    grader (float(full_response_text)). Disqualified from ratchet-critical evidence. This TO is
    q03-only. q02/q11 addressed in separate non-ratchet diagnostic ablation (.068) after this iter
    delivers and SC files R-SC-1 honesty note.

    ## Phase 0 — Experiment log path fix (REQUIRED BEFORE iter-7 commit)

    The ratchet runner currently appends to `comp/targets/click/experiment_log.jsonl` (schema v2),
    but the maintained schema v3 log is at `comp/results/dev-click-001/experiment_log.jsonl`.
    SC has been manually backfilling the v3 log each iter. Fix this path mismatch before iter-7.

    Locate the runner config or target spec that controls the experiment_log_path used when
    target=dev-click-001 (or click). The runner.py resolves it as:
        log_path = target_dir / "experiment_log.jsonl"
    where target_dir = comp/targets/dev-click-001/

    The v3 maintained log lives at comp/results/dev-click-001/experiment_log.jsonl.

    Fix: update runner.py or the target's config so experiment_log_path resolves to
    comp/results/dev-click-001/experiment_log.jsonl for the dev-click-001 target.
    Alternatively: symlink or redirect acceptable if cleaner — check with runner.py semantics.

    If the fix touches runner.py: run pytest comp/ --ignore=comp/targets first to confirm no
    regressions from the path change. Keep the fix minimal (1-3 LOC).

    Commit the path fix in the same commit or a preceding commit to the iter-7 mutation.

    ## Phase 1 — Author iter-7 mutation

    **Mutation: class_hierarchy_correction node (iter-7 corrected Option D)**

    Replace the iter-6 `class_hierarchy_summary` node with a `class_hierarchy_correction` node.
    The new node encodes the hierarchy from Command's perspective with explicit exclusion signals.

    Node spec (verbatim from CTO P0 amendment):
    - node_type: "class_hierarchy_correction"
    - Content line 1: Command.direct_subclasses: [_BaseCommand, Group]
    - Content line 2: _MultiCommand.parent_class: Group (NOT a direct Command subclass)
    - Content line 3: CommandCollection.parent_class: Group (NOT a direct Command subclass)

    Implementation notes:
    - Replace the existing hierarchy_summary block in compiler.py with this new node
    - Keep id/kind/canonical_path structure consistent with iter-6 node
    - The parenthetical "NOT a direct Command subclass" is load-bearing — it is the exclusion
      signal the judge needs to distinguish Command's inheritors from Group's inheritors
    - Do NOT add q02/q11 numeric-fact nodes — those are disqualified (CVO R-CTO-1)
    - Do NOT combine with any other mutation — keep this isolated to the single correction node
    - q03 is the only target; this is a corrected Command-perspective fact node, not Group-perspective

    ## Phase 2 — Pre-commit gates

    Run the pre-commit gate:
    ```bash
    .tools/ds-commit-gate.sh comp/targets/click/compiler.py
    ```
    All three checks must exit 0: py_compile, ds-precommit-check.py, ruff.

    If runner.py was touched in Phase 0, also gate it:
    ```bash
    .tools/ds-commit-gate.sh comp/loop/runner.py
    ```

    Then run the comp/ test suite:
    ```bash
    python -m pytest comp/ --ignore=comp/targets -q --tb=short
    ```
    All 458 tests must PASS (or more if you added tests). Zero regressions.

    ## Phase 3 — Commit and push

    Commit the iter-7 mutation (and path fix if in same commit):
    ```bash
    git commit --only \
      --author="1.3.0_DS_CompLearns <1.3.0_DS_CompLearns@opal.agent>" \
      -m "feat(COMP_LEARNS.067): click compiler v7 -- class_hierarchy_correction node (iter-7 q03-only)" \
      -- comp/targets/click/compiler.py \
         comp/results/dev-click-001/experiment_log.jsonl
    ```

    If runner.py path fix is in a separate preceding commit:
    ```bash
    git commit --only \
      --author="1.3.0_DS_CompLearns <1.3.0_DS_CompLearns@opal.agent>" \
      -m "fix(COMP_LEARNS.067): experiment_log path -- runner resolves v3 log at comp/results/dev-click-001/" \
      -- comp/loop/runner.py
    ```

    Push to CLOUD from feature_clb:
    ```bash
    git push origin CLOUD
    ```

    Then MCP COO (2.1.0_SA_COO) with:
    - Commit sha(s)
    - Brief description of what the class_hierarchy_correction node outputs
    - Whether path fix was separate commit or combined
    - Ready-for-scoring flag
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>python -m pytest comp/ --ignore=comp/targets -q --tb=no 2>&amp;1 | tail -3</run>
        <expect>458 passed (or more). Zero failures.</expect>
        <if_mismatch>STOP. Report failure count to COO before proceeding.</if_mismatch>
      </step>
      <step>
        <run>python -c "import json; rows=[json.loads(l) for l in open('comp/results/dev-click-001/experiment_log.jsonl')]; print(len(rows), [r['iteration'] for r in rows])"</run>
        <expect>6 [1, 2, 3, 4, 5, 6]</expect>
        <if_mismatch>Experiment log gap — MCP COO before proceeding.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh comp/targets/click/compiler.py</run>
        <expect>All 3 checks exit 0 (py_compile + ds-precommit-check + ruff).</expect>
        <if_mismatch>STOP. Fix flagged issue. Do not commit until gate exits 0.</if_mismatch>
      </step>
      <step>
        <run>python -m pytest comp/ --ignore=comp/targets -q --tb=short 2>&amp;1 | tail -5</run>
        <expect>458+ passed, 0 failed.</expect>
        <if_mismatch>STOP. Fix regression before committing.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>python -c "import json; rows=[json.loads(l) for l in open('comp/results/dev-click-001/experiment_log.jsonl')]; print(len(rows), [r['iteration'] for r in rows])"</run>
        <expect>6 iters [1-6] still intact. Path fix should not have altered content.</expect>
        <if_mismatch>Path fix broke log continuity. Fix before scoring.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>
      GO is HELD pending CVO/SC R-SC-1 gate. Do not begin until GO received from COO.
      comp/results/dev-click-001/experiment_log.jsonl: DS owns path-fix + iter-7 backfill;
      SC will append iter-7 scoring result after delivery.
    </note>
    <shared_artifacts>comp/results/dev-click-001/ (DS writes; SC scores after DS ready-flag)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Experiment log path mismatch fixed — runner resolves to comp/results/dev-click-001/experiment_log.jsonl for dev-click-001 target.
    2. comp/targets/click/compiler.py modified to replace hierarchy_summary with class_hierarchy_correction node per exact CTO spec (Command.direct_subclasses + NOT-exclusion notes for _MultiCommand, CommandCollection).
    3. No q02/q11 numeric-fact nodes added — q03-only per CVO R-CTO-1.
    4. ds-commit-gate.sh exits 0 on compiler.py (and runner.py if touched).
    5. pytest comp/ --ignore=comp/targets passes 458+ tests, 0 failures.
    6. Commit --only --author=1.3.0_DS_CompLearns scoped to changed files only.
    7. Pushed to CLOUD from feature_clb.
    8. MCP COO with commit sha(s) + node output description + ready-for-scoring flag.
    9. Session log with Compiler Tools section.
  </acceptance_criteria>

  <dependencies>
    - HOLD: GO not dispatched until (1) SC R-SC-1 filed, (2) this TO committed by COO.
    - After DS delivers: SC scores (.067 scoring TO to be authored by COO after GO clears).
    - .068 (q02/q11 diagnostic ablation): separate TO, sequenced after .067 result + SC R-SC-1.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb (COMP_LEARNS worktree).
    - No emojis in code or logs.
    - from __future__ import annotations not required for compiler.py, but run pre-commit gate.
    - Do NOT run the scoring yourself. DS authors, SC scores.
    - Do NOT add q02/q11 nodes — CVO ruling disqualifies them from this iter.
    - The class_hierarchy_correction node replaces (not supplements) the iter-6 hierarchy_summary node.
  </operational_notes>

  <closeout>
    - flip TO status to complete with commit sha evidence
    - git push origin CLOUD from feature_clb
    - MCP COMPLETE to 2.1.0_SA_COO with commit sha + node description + ready flag
    - session log
  </closeout>
</task_order>
