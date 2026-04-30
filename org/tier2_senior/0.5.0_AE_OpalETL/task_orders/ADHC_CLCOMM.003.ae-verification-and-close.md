<task_order>
  <metadata>
    <id>ADHC_CLCOMM.003.ae-verification-and-close</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-04-30</date>
    <status>staged</status>
    <project_code>ADHC_CLCOMM</project_code>
    <prd_ref>docs/architecture/ADHC_CLCOMM.md §6 + §7 verification checklist</prd_ref>
    <effort>~1-2 hours (mostly verification + smoke testing)</effort>
    <gates_on>ADHC_CLCOMM.002 RAVC4 (feature_clb wire-up shipped on COMP branch).</gates_on>
    <gates_for>Project closure (3-step atomic close after RAVC4 ACK)</gates_for>
  </metadata>

  <objective>
    Run the §7 verification checklist (9 concrete tests) to confirm the isolated `complearns-agent-comms` channel is actually isolated from `opal-agent-comms` in practice — not just in spec. Smoke testing requires a fresh Claude Code session in feature_clb (MCP config loads at session-start). AE coordinates with Andrew on when to launch the fresh session OR documents the verification protocol Andrew can run.

    On clean PASS: project closes via 3-step atomic close (JSON status → complete + REGISTRY row move + PRD Status update). On any FAIL: triage + small follow-on TO if needed.
  </objective>

  <compiler_tools_mandate>
    <phase_1_before_verify>
      - Read PRD §6 (gotchas) and §7 (verification checklist) end-to-end.
      - Confirm TO-1 + TO-2 commits are pushed and merged into the appropriate branches (CLOUD + COMP).
      - Confirm `feature_clb/org/mcp/cl_inbox/` does NOT exist yet (will be auto-created on first server start per PRD §6).
      - Coordinate with Andrew: is now a good time to launch a fresh feature_clb session for smoke testing, OR should AE document the verification protocol for Andrew to run when convenient?
    </phase_1_before_verify>
    <phase_2_verification>
      Run the 9 tests in PRD §7 in order:
      1. `mcp__complearns-agent-comms__register_agent` tool available (not `mcp__opal-agent-comms__*`)
      2. `register_agent("2.1.0_SA_COO", ...)` returns broker port 7801, not 7800
      3. `cl-check-inbox 2.1.0_SA_COO` looks in `feature_clb/org/mcp/cl_inbox/`, not `ajb_workspace/org/mcp/inbox/`
      4. `cl-inbox-watch 2.1.0_SA_COO` watches `feature_clb/org/mcp/cl_inbox/2.1.0_SA_COO/`
      5. Send test message CL→CL; verify it lands in `cl_inbox/` not `inbox/`
      6. Open concurrent `ajb_workspace` Claude Code session; verify messages sent there do NOT appear in `cl_inbox/`
      7. `deregister_agent` called by `2.1.0_SA_COO` succeeds (auth check passes for 2.1.x prefix per TO-1's widening)
      8. `cl_broker.db` is created in `feature_clb/org/mcp/`, not `ajb_workspace/org/mcp/`
      9. `agent-poller.py` polls port 7801 (the §6 hidden dependency — verifies TO-1's channel-routing decision works)

      Document each test's outcome (PASS/FAIL/N/A with rationale) in the session log.
    </phase_2_verification>
    <phase_3_after_verify>
      - On all-PASS: author the 3-step closure commit OR MCP COO to drive the closure (COO handles JSON+REGISTRY; CTO handles PRD Status line).
      - On any FAIL: file a small follow-on TO scoped to the specific failure. If failure is structural (e.g., agent-poller.py routing logic broken), MCP CTO immediately for triage.
      - Append session-log entry to `org/compiler-tools-log.md`.
    </phase_3_after_verify>
  </compiler_tools_mandate>

  <scope>
    1. Coordinate with Andrew on smoke-test timing (fresh feature_clb session).
    2. Run §7 verification checklist (9 tests). Document each.
    3. On PASS: close project via 3-step atomic.
    4. On FAIL: triage + file follow-on if structural.

    **No new code in this TO** — pure verification + closure.

    **Cross-channel architecture observations** — final pass: append a section "Cross-channel architecture observations" to the session log capturing any pattern surfaced during smoke-testing or the verification flow that should generalize. Combined with TO-1 + TO-2 observation sections, this becomes the input corpus for TO-4 (architecture doc) authoring.

    **TO-4 dispatch trigger:** on TO-3 PASS + project close, MCP CTO with: "TO-3 verification PASS + project closed; ready for TO-4 architecture doc authoring." CTO+COO co-author TO-4 from the three session logs.

    Author: `0.5.0_AE_OpalETL <0.5.0_AE_OpalETL@opal.agent>` for any commits (e.g., session log). 3-step closure routing per Closure Discipline (CTO PRD Status line; COO JSON+REGISTRY).

    **Note on project closure semantics:** project does NOT fully close on TO-3 PASS — TO-4 (architecture doc) is the final wave. Project closes when TO-4 ships. TO-3 closure is "Phase 1 verification COMPLETE; Phase 2 (architectural codification) in flight."
  </scope>

  <acceptance_criteria>
    1. All 9 §7 verification tests run + outcome documented.
    2. Inbox isolation empirically confirmed: messages sent on opal-agent-comms do NOT appear in `cl_inbox/`; messages sent on complearns-agent-comms do NOT appear in `inbox/`.
    3. agent-poller.py channel-routing decision (from TO-1) verified in practice — broker push channel notifications reach CL agents on port 7801.
    4. Project closed via 3-step atomic OR follow-on TO filed for any FAIL.
    5. RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with: 9-test outcome table + closure status.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT skip any of the 9 §7 tests — partial verification = unknown isolation. The whole point of the project is the isolation working in practice, not just on paper.</rule>
    <rule>Do NOT close the project on partial PASS without explicit CTO ack on the FAIL classification (e.g., "this fail is acceptable because X").</rule>
    <rule>Do NOT smoke-test from the current session — fresh session required.</rule>
  </do_not>

  <deliverables>
    <deliverable type="document">Session log with 9-test outcome table</deliverable>
    <deliverable type="closure">3-step atomic close commit OR follow-on TO if FAIL</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with verification outcomes + closure status</deliverable>
  </deliverables>
</task_order>
