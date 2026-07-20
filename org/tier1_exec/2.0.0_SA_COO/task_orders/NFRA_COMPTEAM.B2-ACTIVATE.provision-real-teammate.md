# Task Order: NFRA_COMPTEAM B2-ACTIVATE -- provision a REAL non-Andrew teammate (the final activation inch)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-compteam-b2-activate</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>2.0.0_SA_COO + 1.0.0_SA_CTO (Andrew-Directive-gated)</issued_to>
    <date>2026-07-07</date>
    <status>staged</status>
    <reconcile_note>Status corrected 2026-07-20 by 2.0.0_SA_COO (Andrew-direct backlog review): was 'pending' but dispatch_state = WRITTEN-NOT-DISPATCHED, so factually 'staged'. Andrew-policy-gated (provisioning a real non-Andrew teammate = a new access class) and NOT itself a PRD-named deliverable. COMPTEAM A1 (kit) + B1 (surface->source map) are closed; B2 read-partition design is CVO-cleared but the access-control build is not started. NOT active work. DEPRECATE-vs-KEEP-FENCED is Andrew's call -- surfaced 2026-07-20.</reconcile_note>
    <dispatch_state>WRITTEN-NOT-DISPATCHED (wind-down 2026-07-07; Andrew directed decomposition materialized before device reboot; dispatch on restart per the allocation-map in the session handoff /log)</dispatch_state>
    <gate_note>GENUINELY-EXTERNAL: gated on the standing-access-class DIRECTIVE (Andrew, sovereign). Pairs with AGENTBUS-AB-ACTIVATE (SAME Directive).</gate_note>
  </metadata>

  <objective>Provision a real external human principal to the MCP/agent infra with a distributed kit + a live scoped read-partition. This is a NEW ACCESS CLASS.</objective>

  <requirements>
    <requirement id="1">real teammate registered with a kit + a live partition</requirement>
    <requirement id="2">scoped-read enforced live for the new principal</requirement>
  </requirements>
</task_order>
```
