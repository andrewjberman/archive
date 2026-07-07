# Task Order: NFRA_AGENTBUS S4 -- CVO independent live re-verify of all 5 controls on the simulated proof

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-agentbus-s4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>3.0.0_SA_CVO~B</issued_to>
    <date>2026-07-07</date>
    <status>superseded -- authoritative S4 = org/tier1_exec/3.0.0_SA_CVO/task_orders/NFRA_AGENTBUS.S4.cvo-live-verification-simulated-proof.md (CVO~B working copy; control-1 partition already independently re-verified 1/5, controls 2-5 gated on S3)</status>
    <dispatch_state>SUPERSEDED (dedup 2026-07-07, COO~B NFRA completion drive) -- this thin stub is retired; the CVO-dir proof file is the single authoritative S4.</dispatch_state>
    <gate_note>Follows S3. Superseded stub retained for history.</gate_note>
  </metadata>

  <objective>The §6 acceptance run on live state (partition-scoped, attribution-signed, strip-fail-closed, action-authz-enforced) + the intra-fleet opal-agent-comms regression.</objective>

  <requirements>
    <requirement id="1">all 5 controls exercised on live AWS/adapter state, never self-report (Rule 22/22a)</requirement>
    <requirement id="2">intra-fleet broker regression clean</requirement>
  </requirements>
</task_order>
```
