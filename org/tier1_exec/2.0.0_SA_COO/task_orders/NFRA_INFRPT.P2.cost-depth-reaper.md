# Task Order: NFRA_INFRPT P2 -- cost-depth section + security triage + snapshot-reaper (STAGED+undriven since ~06-17 -- owner-gap, UNBLOCKED)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-infrpt-p2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-07-07</date>
    <status>ready</status>
    <dispatch_state>WRITTEN-NOT-DISPATCHED (wind-down 2026-07-07; Andrew directed decomposition materialized before device reboot; dispatch on restart per the allocation-map in the session handoff /log)</dispatch_state>
    <gate_note>COO-RESOLVABLE: assign an active lane (the owner-gap is the true blocker, not a dependency). Validate-on-scheduled-nightly.</gate_note>
  </metadata>

  <objective>Cost-depth (per-pipeline $ attribution off the 6 live CE tags + trend/forecast + biggest-movers + EC2 right-size flags) + security triage (trend/top-N-new/Claude briefing) + snapshot-reaper (daily AMI/EBS cleanup + 30d retention). STAGED but undriven since the ~B lane stood down 06-16 + 0.7.0_AE was consumed by PREMCP.</objective>

  <requirements>
    <requirement id="1">per-pipeline $ attribution grounded on the 6 live CE keys</requirement>
    <requirement id="2">snapshot-reaper verified on a SCHEDULED run (no ad-hoc), retention honored</requirement>
    <requirement id="3">false-clean hard-criterion: no section reports 'clean' it hasn't probed</requirement>
    <requirement id="4">CVO verifies on the emitted 13:00 UTC artifact, not rc=0</requirement>
  </requirements>
</task_order>
```
