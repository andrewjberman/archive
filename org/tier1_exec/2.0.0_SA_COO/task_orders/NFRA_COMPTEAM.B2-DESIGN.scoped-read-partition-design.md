# Task Order: NFRA_COMPTEAM B2-DESIGN -- scoped read-partition DESIGN over the shared graph (binds the LIVE tier-model)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-compteam-b2-design</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.8.0_AE (graph) + SCTY-coord</issued_to>
    <date>2026-07-07</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_COMPTEAM, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: ready</status>
    <dispatch_state>WRITTEN-NOT-DISPATCHED (wind-down 2026-07-07; Andrew directed decomposition materialized before device reboot; dispatch on restart per the allocation-map in the session handoff /log)</dispatch_state>
    <gate_note>COO-RESOLVABLE -- designs against a LIVE interface (tier-model certified 07-01). Not an Andrew gate.</gate_note>
  </metadata>

  <objective>Per-team/per-surface read-partition design over kuzu/nessie/iceberg, read-slices off B1's map (B1 CLOSED, CTO-gated 965c0a8c1), binding to the SCTY user-type-tier + read-only-scope entitlement (the tier-model is ALREADY LIVE-CERTIFIED 07-01, CVO 4/4).</objective>

  <requirements>
    <requirement id="1">every PanelCluster maps to a served source (from B1)</requirement>
    <requirement id="2">a partition reads its slice + is DENIED cross-team/cross-surface</requirement>
    <requirement id="3">scope resolves off SCTY-verified identity, fail-closed on unverified</requirement>
  </requirements>
</task_order>
```
