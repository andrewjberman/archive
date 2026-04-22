<task_order>
  <metadata>
    <id>1.2.0_DS_CompLearns-2026-04-22-comp-learns-047-pilot-wave-1-artifact-restore</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>1.2.0_DS_CompLearns</issued_to>
    <date>2026-04-22</date>
    <status>staged <!-- GO after Stage 2 activation settles. Non-urgent cleanup. --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P2 — hygiene cleanup; does not gate Wave 2 execution; historical audit integrity concern</priority>
  </metadata>

  <references>
    <ref type="incident_flag">org/tier1_exec/2.1.0_SA_COO/logs/2026-04-22/stage2-gate/coo-approval-memo.md — caveat section flags this gap</ref>
    <ref type="audit_commit">6dcbdf22 — SC audit(COMP_LEARNS.032): pilot wave integrity_audit.md — 8/8 PASS, regime clean</ref>
    <ref type="suspect_sweeps">bdb7bacf chore(sweep): commit all remaining unstaged + untracked work</ref>
    <ref type="suspect_sweeps">363a0d98 chore(sweep): commit accumulated staged pilot + org work</ref>
    <ref type="suspect_sweeps">c610630b fix(gold_dispatch): correct B_00/B_01 dependency order in CHAIN_CANONICAL — showed up in diff-filter=D for comp/results/pilot-wave-1/</ref>
  </references>

  <objective>
    Restore pilot-wave-1 artifacts (7 of 8 missing bundles + integrity_audit.md) that were
    committed historically (audit commit 6dcbdf22 + verdict commits 68607503 / be052bd8 /
    8521004d / others) but are NOT present in current HEAD of feature_clb worktree.

    Explicitly in scope:

    1. Diagnose which sweep commit(s) dropped the artifacts:
       - `git log --diff-filter=D --all -- comp/results/pilot-wave-1/` — enumerate deletions
       - `git log --diff-filter=D --all -- comp/tasks/case-002-click-refactor/bundles/` — same for bundles
       - `git log --diff-filter=D --all -- comp/tasks/task-001-httpx-netrc-host-authority/bundles/` — same

    2. Identify the latest commit where each missing artifact existed:
       - comp/results/pilot-wave-1/integrity_audit.md (expected: added at 6dcbdf22)
       - comp/results/pilot-wave-1/verdicts/case-002-ds-1.1.0-condition_a-run-1.json
       - comp/results/pilot-wave-1/verdicts/case-002-ds-1.1.0-condition_b-run-1.json
       - comp/results/pilot-wave-1/verdicts/case-002-ds-1.3.0-condition_b-run-1.json
       - comp/results/pilot-wave-1/verdicts/task-001-ds-1.1.0-condition_a-run-1.json
       - comp/results/pilot-wave-1/verdicts/task-001-ds-1.1.0-condition_b-run-1.json
       - comp/results/pilot-wave-1/verdicts/task-001-ds-1.3.0-condition_b-run-1.json
       - comp/results/pilot-wave-1/verdicts/task-001-ds-1.4.0-condition_a-run-1.json
       - 7 missing bundle directories under comp/tasks/{task}/bundles/ (one per (task×agent×condition))

    3. Restore each artifact via `git checkout {commit}^ -- {path}` (the parent of the
       deleting commit, or if added-then-lost, the commit that last had it). Verify
       file content matches historical blob SHAs.

    4. Commit the restored files under --author=1.2.0_DS_CompLearns@opal.agent with
       --only pathspec. Commit message cites the source commit(s) restored from.

    5. Push to CLOUD.

    6. Verify post-restore: `ls comp/results/pilot-wave-1/verdicts/ | wc -l` should show
       8 verdicts + integrity_audit.md. Bundle dirs should have the 8 expected.

    Explicitly out of scope:
    - Re-running pilot-wave-1 (historical record; no re-execution).
    - Modifying integrity_audit.md content (restore historical verbatim only).
    - Changing ACID assumptions about sweep commits (don't rewrite history; just restore files forward).
    - Investigating non-pilot-wave-1 sweeps (scope strictly comp/results/pilot-wave-1/ + pilot-wave-1 bundles under comp/tasks/).

    If the deletions are ambiguous (e.g. files never actually committed despite status
    showing "A" in an earlier session), document the state-of-the-world for each
    artifact and MCP me for triage before restoring partial data.
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>git log --diff-filter=D --all --oneline -- comp/results/pilot-wave-1/ | head -20</run>
        <expect>Lists commits that removed files under pilot-wave-1/. Expect 1-3 sweep commits named above.</expect>
        <if_mismatch>If the list is empty, the files were never committed — escalate to COO; scope may change.</if_mismatch>
      </step>
      <step>
        <run>git log --all --oneline -- comp/results/pilot-wave-1/integrity_audit.md | head -5</run>
        <expect>Shows at least commit 6dcbdf22 (audit add). Confirms the file existed historically.</expect>
        <if_mismatch>Surface to COO — audit commit absent means a bigger gap.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>ls comp/results/pilot-wave-1/verdicts/</run>
        <expect>8 *.json files present (restored).</expect>
        <if_mismatch>Continue restoring — use git show or git checkout to pull from historical commits.</if_mismatch>
      </step>
      <step>
        <run>ls comp/results/pilot-wave-1/integrity_audit.md</run>
        <expect>File present.</expect>
        <if_mismatch>Restore from 6dcbdf22 via git show 6dcbdf22:comp/results/pilot-wave-1/integrity_audit.md > target.</if_mismatch>
      </step>
      <step>
        <run>pytest comp/ -q</run>
        <expect>No new reds vs 9-pre-existing baseline.</expect>
        <if_mismatch>Investigate. Fix before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>python comp/bin/comp-preflight.py --task case-002-click-refactor --bundle-path comp/tasks/case-002-click-refactor/bundles/ds-1.1.0-condition_a --condition a --mode eval 2>&1 | head -20</run>
        <expect>Preflight runs against a restored bundle. CHECKs 1-4 PASS (CHECK 5 may FAIL as before — worktree not provisioned). Confirms restored bundle is structurally valid.</expect>
        <if_mismatch>Restored bundle may be incomplete. Investigate.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>This TO touches comp/results/pilot-wave-1/ + comp/tasks/{task}/bundles/ — historical artifacts, no live production path. No coordination with other TOs. SC may use restored integrity_audit.md for future reference but they don't actively wait on this.</note>
    <shared_artifacts>comp/results/pilot-wave-1/** (read-only after this TO completes)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/results/pilot-wave-1/integrity_audit.md exists, content matches historical blob at 6dcbdf22.
    2. comp/results/pilot-wave-1/verdicts/ contains 8 *.json files matching the task×agent×condition matrix.
    3. comp/tasks/case-002-click-refactor/bundles/ has directories for 4 (agent×condition) combinations with refactor.patch + test_output.txt + reasoning.md (or changes.patch equivalents).
    4. comp/tasks/task-001-httpx-netrc-host-authority/bundles/ has directories for 4 (agent×condition) combinations.
    5. pytest comp/ -q no new reds.
    6. Commit --only --author=1.2.0_DS_CompLearns pathspec scoped to comp/results/pilot-wave-1/** and comp/tasks/{task}/bundles/**.
    7. Pushed to CLOUD.
    8. Session log with Compiler Tools section + restoration provenance (which commit SHAs each file restored from).
    9. MCP COMPLETE to 2.1.0_SA_COO.
  </acceptance_criteria>

  <dependencies>
    - No active upstream — cleanup of historical state.
    - Unblocks: nothing gating but enables future reconciliation audits to find the complete pilot-wave-1 record.
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - Use `git show {commit}:{path} > {path}` to restore from specific commits, OR
      `git checkout {commit}^ -- {path}` for bulk-restore.
    - If you discover any restored artifact contains sensitive/stale content (e.g. early
      pre-audit verdict drafts), MCP COO before committing.
    - Some bundles may have been in ajb_workspace worktree only, never feature_clb. In that
      case they're not restorable from feature_clb's git history — document as "not present
      in feature_clb history" and recommend investigating ajb_workspace for those.
    - No emojis in commit message or any restored file you author (the historical files
      predate the no-emoji rule but if any slipped through, leave them unless they break
      downstream tools; don't rewrite historical content).
  </operational_notes>

  <closeout>
    On completion:
    - commit --only --author="1.2.0_DS_CompLearns &lt;1.2.0_DS_CompLearns@opal.agent&gt;" -- comp/results/pilot-wave-1/** comp/tasks/case-002-click-refactor/bundles/** comp/tasks/task-001-httpx-netrc-host-authority/bundles/**
    - push to CLOUD
    - flip TO status to complete
    - MCP COMPLETE to 2.1.0_SA_COO with restoration summary (files restored + source commits)
    - session log with Compiler Tools section + provenance table
  </closeout>
</task_order>
