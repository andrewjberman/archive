<task_order>
  <metadata>
    <id>1.1.0_SA_CTO-2026-04-22-comp-learns-stage2-activation</id>
    <issued_by>1.1.0_SA_CTO</issued_by>
    <issued_to>PROGRAM</issued_to>
    <date>2026-04-22</date>
    <status>active</status>
    <project_code>COMP_LEARNS</project_code>
  </metadata>

  <declaration>
    COMP_LEARNS eval-mode Stage 2 is ACTIVE as of 2026-04-22.

    This TO is the explicit CTO authorization required by AUTOMATION_V1 §11 condition 4.
    It is not implicit. It supersedes manual COO bundle inspection as the default eval-mode
    dispatch path effective immediately.
  </declaration>

  <stage2_gate_evidence>
    §11 requires all four conditions satisfied before Stage 2 activation.

    Condition 1 — comp-preflight.py implemented + unit tests passing:
      SATISFIED. Commit f6f29836 (1.4.0_DS, .042). 31 test_preflight cases GREEN.
      Full CLI + 7 checks + CHECK 2b + JSON diagnostic per §5 spec.

    Condition 2 — comp-wave-runner.py --dry-run verified against wave 1 data:
      SATISFIED. Commit 5a44ac87 (1.3.0_DS, .043). 40 test_wave_runner cases GREEN
      including §11 wave-1 dry-run gate. COO re-ran independently; archived at
      comp/results/stage2-gate/wave-1-replay-dryrun.txt. 4-event reconstruction
      matches pilot-wave-1: condition_a before condition_b dependency enforced,
      0 dev / 4 eval / scorer = 2.1.0_SC_CompLearns. Exit 0.

    Condition 3 — COO reviewed automation flow + approved handoff protocol:
      SATISFIED. Commit 1b6380da (2.1.0_SA_COO, .045 COO section). COO approval
      memo at comp/results/stage2-gate/coo-approval-memo.md. Five invariants from
      Stage 1 confirmed preserved: fresh SC session per event, reasoning.md
      mechanically excluded from scorer inputs, COO relay preserved at event
      boundary, verdict integrity (SC commits, wave-runner does not generate),
      SC-authored integrity audit.

    Condition 4 — CTO explicit activation TO:
      SATISFIED. This document.

    CTO independent spot-check (per .045 TO):
      Ran comp-preflight.py manually against comp/tasks/case-002-click-refactor/
      bundles/ds-1.3.0-condition_a in eval mode. Output matches COO captured run
      (preflight-replay.json) exactly: task_packet_present PASS, bundle_complete PASS,
      manifest_computed PASS, doctrine_pinned PASS, worktree_clean FAIL (expected —
      worktree not provisioned; wave-runner provisions before preflight in Stage 2 flow),
      exit 1. Check semantics and JSON structure correct per §5 spec.
  </stage2_gate_evidence>

  <stage2_eval_mode_protocol>
    Default path: comp-wave-runner.py manages eval-mode dispatch. Preflight runs
    automatically before each SC session dispatch. Manual COO full-bundle inspection
    is replaced by preflight JSON verification + worktree provisioning (~30s/event).

    Human relay required on:
      - Any preflight EXIT 1 (DS logs diagnostic, MCPs COO — per §6)
      - First event for any new task (establishing manifest anchor)
      - Cross-model comparison events
      - Any bundle where DS flags anomalies

    All other eval-mode events: auto-route to SC after preflight EXIT 0.
  </stage2_eval_mode_protocol>

  <stage2_dev_mode_note>
    Dev mode was activated independently at .044 ship (comp-dev-loop.py, commits
    0d0dec04 + cc18adf0, 13 test_dev_loop GREEN). This activation does not change
    dev mode — it is already live. Dev mode human-review triggers remain: plateau
    signal, kill switch, budget exhaustion, DS-flagged anomalous result.json.
  </stage2_dev_mode_note>

  <known_gaps>
    1. pilot-wave-1 artifact persistence gap: 7 of 8 pilot-wave-1 bundles not
       materialized in feature_clb HEAD despite 6dcbdf22 audit commit in ancestry.
       Historical 8/8 PASS record is authoritative (audit commit in HEAD ancestry
       confirmed: git merge-base --is-ancestor 6dcbdf22 HEAD = true). Gap is cosmetic
       repo state. NOT gating Stage 2. Recommend separate cleanup TO.

    2. .041 (Case 4 httpx packet) still pending: 1.1.0_DS has not yet shipped Phase 0
       baseline_commit resolution for bl-httpx-002. No Stage 2 eval-mode wave for
       Case 4 until packet.yaml is complete.

    3. 9 pre-existing test failures in comp/bench/ + comp/graph/ unrelated to .042-.044.
       Accepted baseline; separate sweep TO recommended.
  </known_gaps>

  <fallback_conditions>
    Stage 2 eval mode halts and reverts to manual COO inspection if:
    - Preflight generates a false-pass (EXIT 0 on invalid bundle reaching SC)
    - Integrity audit reports a violation post-scoring
    - comp-wave-runner exits non-zero on a live wave event
    - CTO issues explicit HALT via MCP to COO

    Stage 2 exit criterion per §6: 2+ waves with zero eval-mode preflight false-passes
    AND zero integrity violations in the integrity audit. Stage 3 planning begins after.
  </fallback_conditions>

</task_order>
