<task_order>
  <metadata>
    <id>ADHC_CLCOMM.TO-4</id>
    <project>ADHC_CLCOMM</project>
    <title>Cross-Channel Agent Comms Architecture Doc — AGENT_COMMS_ARCHITECTURE.md</title>
    <issued_to>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-01</issued_date>
    <status>open</status>
    <priority>P2 — standing work; not blocking any active execution</priority>
    <estimated_effort>0.5d (doc authoring, no code)</estimated_effort>
    <gates_on>ADHC_CLCOMM.TO-3 PASS (COMPLETE 2026-05-01)</gates_on>
  </metadata>

  <context>
    ADHC_CLCOMM.TO-3 (ae-verification-and-close) COMPLETE 2026-05-01. All 9 §7 verification
    tests PASS/ACCEPTED. Channel in active production use. 14 cross-channel architectural
    observations seeded across 3 session logs by AE 0.5.0:

    Observation corpus:
    - obs #1-7:  org/tier2_senior/0.5.0_AE_OpalETL/logs/2026-04-30/adhc_clcomm_001_cl_mcp_scripts.md
    - obs #8-11: org/tier2_senior/0.5.0_AE_OpalETL/logs/2026-04-30/adhc_clcomm_002_feature_clb_integration.md
    - obs #12-14: org/tier2_senior/0.5.0_AE_OpalETL/logs/2026-05-01/adhc_clcomm_003_verification.md
    - synthesis:  org/tier2_senior/0.5.0_AE_OpalETL/logs/2026-04-30/session_wrap.md (12-entry)

    Also notable from TO-3 verification:
    - Both namespaces visible to exec agents (intentional cross-workspace escalation path)
    - deregister_all_stale auth gap for 2.1.x serials (standing backlog item)
    - Pre-TO-2 CL artifact dirs in ajb_workspace/inbox/ (inert, housekeeping backlog)
    - inbox-watch.sh cherry-pick opportunity: COMP eval-exclusion + PPID-filter hardening
      (c471b2fd9 + d26a36492 from 2.1.0_SC_CompLearns) could benefit opal-agent-comms watcher
  </context>

  <objective>
    Author docs/architecture/AGENT_COMMS_ARCHITECTURE.md — canonical cross-channel
    architecture reference covering:
    (1) Two-channel design: opal-agent-comms (port 7800, ajb_workspace) vs
        complearns-agent-comms (port 7801, feature_clb)
    (2) Routing rules: which serials register where, prefix routing in agent-poller.py
    (3) Cross-channel escalation path: why exec agents (CTO/COO) are visible in both
    (4) Inbox-watch invocation rules: generic vs cl-inbox-watch.sh, path requirements,
        PPID-filter behavior, orphan-cleanup hook
    (5) deregister_all_stale auth gap for 2.1.x (document as known limitation)
    (6) Future: cherry-pick plan for COMP eval-exclusion + PPID hardening into opal watcher
    (7) Org/XXX.md updates: cl-* command references, cross-worktree operator rules
  </objective>

  <acceptance_criteria>
    1. docs/architecture/AGENT_COMMS_ARCHITECTURE.md committed on CLOUD under CTO author
    2. All 14 AE 0.5.0 observations addressed (cited or resolved)
    3. Two-channel topology diagram (ASCII) included
    4. deregister_all_stale gap documented as known limitation with remediation path
    5. org/XXX.md updated with cl-inbox-watch.sh references (if not already from TO-2)
    6. RAVC4 to COO from CTO on completion
  </acceptance_criteria>

  <notes>
    Joint CTO+COO deliverable — CTO authors, COO reviews. No code changes. Doc only.
    AE 0.5.0 not needed for execution; observation corpus is the input.
    ADHC_CLCOMM project is already closed — this TO is the final standing-backlog item
    noted in the ADHC_CLCOMM.json lane_note (CTO+COO joint on TO-4).
  </notes>
</task_order>
