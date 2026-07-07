# Task Order: NFRA_SCTY_PREMCP P2 -- PREMCP P2 residual -- network-isolation + broker review (the last PREMCP leg after L2-403)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-scty_premcp-p2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-07-07</date>
    <status>pending</status>
    <dispatch_state>WRITTEN-NOT-DISPATCHED (wind-down 2026-07-07; Andrew directed decomposition materialized before device reboot; dispatch on restart per the allocation-map in the session handoff /log)</dispatch_state>
    <gate_note>CTO-DEFERRED until P1-phase-1 (L2-403) closes. Sequences after the L2-403 human-OAuth gate.</gate_note>
  </metadata>

  <objective>PREMCP P2 (network isolation + broker review), the CTO-deferred residual after P1 (6 controls + WAF all certed). Scope + close as the last PREMCP leg.</objective>

  <requirements>
    <requirement id="1">network-isolation posture specified + CTO-gated</requirement>
    <requirement id="2">broker review complete</requirement>
    <requirement id="3">CVO certs the P2 controls live</requirement>
  </requirements>
</task_order>
```
