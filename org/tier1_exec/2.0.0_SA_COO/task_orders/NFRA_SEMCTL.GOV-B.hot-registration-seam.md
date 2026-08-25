# Task Order: NFRA_SEMCTL GOV-B -- the promoted-recognizer -> LIVE-compiler HOT-REGISTRATION seam (named in COMPILERKIT + PROMOTE)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-semctl-gov-b</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.8.0_AE (COMPILERKIT registry) + 0.4.0_DS/AE (PROMOTE materializer)</issued_to>
    <date>2026-07-07</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_SEMCTL is complete; this TO was last touched 2026-07-07, predating the project close 2026-07-18. Closed as a record act, not a work verdict. Prior status: ready</status>
    <dispatch_state>WRITTEN-NOT-DISPATCHED (wind-down 2026-07-07; Andrew directed decomposition materialized before device reboot; dispatch on restart per the allocation-map in the session handoff /log)</dispatch_state>
    <gate_note>COO-RESOLVABLE (COMPILERKIT registry side ready now; PROMOTE materializer side gated on PROMOTE-P1). Governance item (b).</gate_note>
  </metadata>

  <objective>The seam where a PROMOTE-materialized recognizer hot-registers into the live COMPILERKIT compiler. comp_recognizer_sdk.py already surfaces PROMOTE_SEAM as a named critical-surface; wire the registry side (COMPILERKIT) + the materializer side (PROMOTE).</objective>

  <requirements>
    <requirement id="1">PROMOTE materializer produces a recognizer that hot-registers into the live registry</requirement>
    <requirement id="2">the seam is a named critical-surface (comp-surface-check watched)</requirement>
    <requirement id="3">reversible (a bad promotion can be hot-de-registered)</requirement>
  </requirements>
</task_order>
```
