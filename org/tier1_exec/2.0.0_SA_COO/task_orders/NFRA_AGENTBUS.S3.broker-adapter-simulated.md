# Task Order: NFRA_AGENTBUS S3 -- broker adapter -- the 5-control choke point + tool_activity meter (SIMULATED-only, governance-fenced)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-agentbus-s3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps (RE-LANED from DE)</issued_to>
    <date>2026-07-07</date>
    <status>superseded -- authoritative S3 = org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/NFRA_AGENTBUS.S3.broker-adapter-choke-point-simulated.md (re-laned to 0.7.0_AE_CloudOps 2026-07-07 by COO~B; that file carries the FULL 5-control spec + compiler-mandate + acceptance criteria)</status>
    <dispatch_state>SUPERSEDED (dedup 2026-07-07, COO~B NFRA completion drive) -- this thin stub is retired; use the choke-point-simulated file as the single authoritative S3.</dispatch_state>
    <gate_note>Superseded stub retained for history. Real dependency (unchanged) = COMPTEAM strip-list/sig-root + SCTY authz.</gate_note>
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
