# Task Order: NFRA_CMTQUE TO-5F -- contamination-guard retire + worker-side ds-gate re-assert

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-cmtque-to-5f</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-07-07</date>
    <status>ready</status>
    <dispatch_state>WRITTEN-NOT-DISPATCHED (wind-down 2026-07-07; Andrew directed decomposition materialized before device reboot; dispatch on restart per the allocation-map in the session handoff /log)</dispatch_state>
    <gate_note>COO-RESOLVABLE now, no window. Owner 0.7.0~B.</gate_note>
  </metadata>

  <objective>Remove the commit-mutex v2 baseline/contamination apparatus (safe-commit.sh:196-339) from the queue path; worker re-asserts ds-gate; prove the workflows/-class sensitive leak still fail-closes IN THE WORKER (the 07-02 near-miss).</objective>

  <requirements>
    <requirement id="1">selftest case-2 green (already)</requirement>
    <requirement id="2">owned-paths-lane rejection exercised in the worker path</requirement>
    <requirement id="3">non-compiling .py rejection exercised in the worker path</requirement>
    <requirement id="4">legacy apparatus removed from the queue path</requirement>
  </requirements>
</task_order>
```
