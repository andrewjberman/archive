# Task Order: NFRA_COMPILERKIT P2 -- the config compiler (high-yield near-lexical) against the built P1 SDK

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-compilerkit-p2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.8.0_AE_CloudComp~D + 0.4.0_DS~A (recognizers)</issued_to>
    <date>2026-07-07</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_COMPILERKIT is complete; this TO was last touched 2026-07-07, predating the project close 2026-07-07. Closed as a record act, not a work verdict. Prior status: ready</status>
    <dispatch_state>WRITTEN-NOT-DISPATCHED (wind-down 2026-07-07; Andrew directed decomposition materialized before device reboot; dispatch on restart per the allocation-map in the session handoff /log)</dispatch_state>
    <gate_note>COO-RESOLVABLE after P1 (the SDK is built). Owner 0.8.0~D + DS~A.</gate_note>
  </metadata>

  <objective>Add a config-artifact compiler (YAML/TOML/env/tf-vars) as a new recognizer-set on the P1 SDK (comp_recognizer_sdk.py). Additive to the parity-oracle pair. Pure-lexical per CTO #3.</objective>

  <requirements>
    <requirement id="1">config recognizers emit CSE C0/C1 with file:line provenance</requirement>
    <requirement id="2">every node PASSES comp-ladder fidelity_check</requirement>
    <requirement id="3">determinism: an untypable config -> Concept(untyped)+low-confidence, never a guess</requirement>
  </requirements>
</task_order>
```
