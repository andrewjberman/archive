# Task Order: NFRA_AGENTBUS S4 -- CVO independent live re-verify of all 5 controls on the simulated proof

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-agentbus-s4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>3.0.0_SA_CVO~B</issued_to>
    <date>2026-07-07</date>
    <status>pending</status>
    <dispatch_state>WRITTEN-NOT-DISPATCHED (wind-down 2026-07-07; Andrew directed decomposition materialized before device reboot; dispatch on restart per the allocation-map in the session handoff /log)</dispatch_state>
    <gate_note>Follows S3 (simulated). COO-RESOLVABLE.</gate_note>
  </metadata>

  <objective>The §6 acceptance run on live state (partition-scoped, attribution-signed, strip-fail-closed, action-authz-enforced) + the intra-fleet opal-agent-comms regression.</objective>

  <requirements>
    <requirement id="1">all 5 controls exercised on live AWS/adapter state, never self-report (Rule 22/22a)</requirement>
    <requirement id="2">intra-fleet broker regression clean</requirement>
  </requirements>
</task_order>
```
