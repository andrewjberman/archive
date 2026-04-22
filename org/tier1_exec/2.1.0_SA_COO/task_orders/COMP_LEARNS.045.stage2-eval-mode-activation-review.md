<task_order>
  <metadata>
    <id>2.1.0_SA_COO-and-1.1.0_SA_CTO-2026-04-22-comp-learns-045-stage2-eval-mode-activation-review</id>
    <issued_by>2.1.0_SA_COO</issued_by>
    <issued_to>2.1.0_SA_COO + 1.1.0_SA_CTO (joint)</issued_to>
    <date>2026-04-22</date>
    <status>complete <!-- COO section 1b6380da (stage2-gate/ 4 artifacts + APPROVE memo). CTO section 1773f087 (STAGE2-ACTIVATION TO). Stage 2 eval-mode LIVE 2026-04-22. --></status>
    <project_code>COMP_LEARNS</project_code>
    <priority>P1 — gates Stage 2 EVAL-MODE activation; dev mode activates independently after .044 (does NOT wait for this)</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/COMP_LEARNS_AUTOMATION_V1.md §11 (Stage 2 gate condition) + §10 (eval-mode invariants) + §13 (TO decomposition)</ref>
    <ref type="prerequisite_tos">.042 (comp-preflight.py) + .043 (comp-wave-runner.py) both COMPLETE</ref>
    <ref type="prerequisite_data">comp/results/pilot-wave-1/ — Stage 1 reference data for dry-run reconstruction</ref>
  </references>

  <objective>
    Explicit joint gate for Stage 2 EVAL-MODE activation. AUTOMATION_V1 §11 names four
    conditions; this TO verifies all four and produces the CTO-signed authorization that
    activates eval-mode auto-routing for future waves.

    Note: Dev mode (per §11) may activate independently of this TO once .044 ships. This
    TO gates EVAL MODE ONLY.

    Explicitly in scope:

    ## COO section (2.1.0_SA_COO owns)

    1. Run `comp-wave-runner --wave-config wave-1-replay.yaml --dry-run`:
       - Verify output reconstructs the pilot wave 1 event sequence (2 tasks × 2
         conditions × agents) accurately
       - Output archived to comp/results/stage2-gate/wave-1-replay-dryrun.txt

    2. Run `comp-preflight` against every pilot-wave-1 bundle under
       comp/results/pilot-wave-1/bundles/:
       - Eval mode, all 8 bundles
       - Document exit codes + diagnostic JSON to
         comp/results/stage2-gate/preflight-replay.json
       - Eight runs should all EXIT 0 (or document precisely why a wave-1 bundle fails
         today's preflight — reveals a regression in the stored artifacts)

    3. Review `comp-preflight` + `comp-wave-runner` unit test status:
       - pytest comp/tests/test_preflight.py -v → all PASS
       - pytest comp/tests/test_wave_runner.py -v → all PASS
       - Document in comp/results/stage2-gate/unit-test-status.md

    4. Handoff protocol review:
       - Manual review of how eval-mode dispatch flow diverges from Stage 1 (per
         AUTOMATION_V1 §6 eval-mode diagram)
       - Specific attention to the COO relay reduction: COO now verifies preflight JSON
         + provisions SC session (~30s), vs Stage 1 full manual bundle inspection
       - Confirm §10 invariants preserved: fresh SC session per event + reasoning.md
         excluded from scorer inputs + COO relay preserved + verdict attribution + SC-
         authored integrity audit
       - Write COO approval memo: comp/results/stage2-gate/coo-approval-memo.md — one
         page, cites the four §11 gate conditions, documents dry-run evidence, approves
         or declines

    5. MCP CTO with the full stage2-gate/ bundle for activation authorization review.

    ## CTO section (1.1.0_SA_CTO owns)

    1. Review COO-approval-memo.md + dry-run artifacts.

    2. Independent spot-check: run one random eval-mode preflight against a current
       bundle to confirm the tool behaves as specified.

    3. If approved: author explicit activation TO at
       org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.STAGE2-ACTIVATION.md
       - TO declares Stage 2 eval mode ACTIVE as of the TO's commit date
       - Names the specific wave config format (wave-N.yaml) that becomes the canonical
         dispatch mechanism for eval-mode events going forward
       - Names the fallback conditions that revert to Stage 1 manual (preflight EXIT 1,
         first event of new task, cross-model event, DS-flagged anomaly — per §6)

    4. If declined: document the specific §11 condition not satisfied; cycle back to COO
       with a gap-closure TO.

    Explicitly out of scope:
    - Running an actual eval-mode Wave 2 event (that happens AFTER this TO signs off).
    - Dev-mode activation (independent; gated on .044 ship only).
    - Stage 3 (audit-sampled) design — deferred per §14.
    - Cross-model wave activation (not in Wave 2 scope).
  </objective>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>pytest comp/tests/test_preflight.py comp/tests/test_wave_runner.py -v</run>
        <expect>Both test suites GREEN — confirms .042 + .043 both shipped + stable.</expect>
        <if_mismatch>STOP. One of the prerequisites has regressed. Fix before starting activation review.</if_mismatch>
      </step>
      <step>
        <run>ls comp/results/pilot-wave-1/</run>
        <expect>bundles/ + verdicts/ + integrity_audit.md present — needed for dry-run replay.</expect>
        <if_mismatch>STOP — pilot wave 1 data missing.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>ls comp/results/stage2-gate/</run>
        <expect>wave-1-replay-dryrun.txt + preflight-replay.json + unit-test-status.md + coo-approval-memo.md all present.</expect>
        <if_mismatch>Re-run whichever step is missing.</if_mismatch>
      </step>
      <step>
        <run>cat comp/results/stage2-gate/coo-approval-memo.md | head -5</run>
        <expect>Approval memo starts with clear APPROVE or DECLINE verdict.</expect>
        <if_mismatch>Re-author memo with explicit verdict line.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>git log --author="1.1.0_SA_CTO" --oneline -5</run>
        <expect>Most recent CTO commit is the Stage 2 activation authorization TO (or a declined gap-closure TO).</expect>
        <if_mismatch>Wait for CTO authorization ship before flipping this TO to complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <note>Joint TO — COO authors the gate artifacts; CTO reviews + authorizes. Neither
    party ships the other's deliverable. If CTO declines activation, COO authors
    gap-closure TO to the appropriate DS agent (preflight edge case, wave-runner bug,
    etc.) before re-requesting activation.</note>
    <shared_artifacts>comp/results/stage2-gate/** (COO writes, CTO reads); org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.STAGE2-ACTIVATION.md (CTO writes)</shared_artifacts>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. comp/results/stage2-gate/wave-1-replay-dryrun.txt — dry-run output reconstructs pilot wave 1 event sequence.
    2. comp/results/stage2-gate/preflight-replay.json — all 8 pilot-wave-1 bundles preflight-checked + exit codes documented.
    3. comp/results/stage2-gate/unit-test-status.md — .042 + .043 unit tests GREEN confirmed.
    4. comp/results/stage2-gate/coo-approval-memo.md — COO explicit APPROVE or DECLINE with §11 four-condition evidence.
    5. CTO review evidence: MCP acknowledgment + independent spot-check logged.
    6. On CTO APPROVE: org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.STAGE2-ACTIVATION.md exists, authored by CTO, declaring eval-mode Stage 2 ACTIVE.
    7. On CTO DECLINE: gap-closure TO authored by COO, specific to the failing §11 condition.
    8. Commits under respective authors; --only pathspec scoped to comp/results/stage2-gate/** + TO files.
    9. Pushed to CLOUD.
    10. Joint session log entries: COO at org/tier1_exec/2.1.0_SA_COO/logs/{date}/ ; CTO at org/tier1_exec/1.1.0_SA_CTO/logs/{date}/.
  </acceptance_criteria>

  <dependencies>
    - Gate: .042 (comp-preflight.py) COMPLETE and merged.
    - Gate: .043 (comp-wave-runner.py) COMPLETE and merged.
    - Parallel / independent: .044 (comp-dev-loop.py) may have activated dev mode already; this TO is eval-mode-only.
    - Blocks: formal Stage 2 eval-mode wave events (e.g. Wave 2 benchmark scoring on Cases 3 + 4).
  </dependencies>

  <operational_notes>
    - Operate from /c/Users/AndrewBerman/Desktop/feature_clb.
    - COO portion can proceed as soon as .042 + .043 are both COMPLETE; do not wait
      for pilot-wave-2 data (this TO gates wave 2 eval, so it precedes wave 2 dispatch).
    - CTO independent spot-check: CTO chooses ONE random bundle (wave-1 OR a fresh
      synthetic) and runs preflight manually — this is the "independent" arm of the §11
      review (COO runs the replay; CTO runs one at random).
    - §11 is stronger than a rubber-stamp: the explicit CTO authorization TO is the
      authoritative activation signal. Do NOT treat .043 ship as implicit authorization
      (per CTO handoff constraint 3).
    - Dev mode is independent — if dev-mode iterations are running via comp-dev-loop.py
      already at the time of this gate, that is expected and does not affect the eval
      activation review.
    - No emojis in memos / logs.
  </operational_notes>

  <closeout>
    On APPROVE completion:
    - COO commits comp/results/stage2-gate/** under --author="2.1.0_SA_COO" --only pathspec
    - COO flips this TO to complete with commit ref
    - CTO commits the activation TO separately under --author="1.1.0_SA_CTO"
    - Both push to CLOUD
    - Joint MCP to Andrew: Stage 2 eval-mode ACTIVE as of {date}, authorized by .STAGE2-ACTIVATION
    - Session logs with Compiler Tools sections

    On DECLINE completion:
    - COO flips this TO to complete with DECLINE verdict; authors gap-closure TO to appropriate DS
    - Re-request activation after gap closes (this TO re-opens or a .045b follows)
  </closeout>
</task_order>
