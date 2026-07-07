# Task Order: NFRA_AGENTBUS S3 -- broker adapter -- the 5-control choke point + tool_activity meter (SIMULATED-only, governance-fenced)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-agentbus-s3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps (RE-LANED from DE)</issued_to>
    <date>2026-07-07</date>
    <status>pending</status>
    <dispatch_state>WRITTEN-NOT-DISPATCHED (wind-down 2026-07-07; Andrew directed decomposition materialized before device reboot; dispatch on restart per the allocation-map in the session handoff /log)</dispatch_state>
    <gate_note>RE-LANE to AE/CloudOps (backend-infra, NOT portal; DE-park was a lane-accident; 0.7.0_AE built S2 live). REAL dependency = COMPTEAM-A's strip-list/sig-root -> sequences after COMPTEAM-A (the keystone). SIMULATED-only is in-scope under Andrew-direct-auth.</gate_note>
  </metadata>

  <objective>Adapter over the existing opal-agent-comms broker <-> the SQS bus (S2 built live): signed from_employee+from_agent attribution off COMPTEAM's signature-root (C3); egress strip via COMPTEAM's strip-list (C4); ACTION-vs-DATA classifier -> SCTY authz gate (C2, tier-model live); propose-only inbound default (C5); app-layer meter -> tool_activity (append, not fork). GOVERNANCE-FENCE: single-tenant-simulated only, no live cross-principal wiring.</objective>

  <requirements>
    <requirement id="1">forged/absent signature REJECTED</requirement>
    <requirement id="2">planted secret redacted/blocked</requirement>
    <requirement id="3">ACTION-request without SCTY entitlement DENIED; DATA-share flows read-only</requirement>
    <requirement id="4">every message appears in tool_activity</requirement>
  </requirements>
</task_order>
```
