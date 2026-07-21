# Task Order: NFRA_GCONTR closeout -- drive the 5 staged contract rows to ratified + flip advisory->blocking (nothing left to BUILD, ~90% gate-wait)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-gcontr-closeout</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>3.0.0_SA_CVO + 2.0.0_SA_COO + 1.0.0_SA_CTO</issued_to>
    <date>2026-07-07</date>
    <status>cancelled-suspended</status>
    <suspension_note>CANCELLED-as-suspended by 2.0.0_SA_COO~A registry-hygiene sweep 2026-07-21, per NFRA_GCONTR SUSPENDED-INDEFINITE (Andrew-direct sovereign 2026-07-20 ~14:35 ET; verbatim in the project suspend_directive: "Pause GCONTR ... rendered as indefinite/suspended i do not want to fucking hear about it again"). All GCONTR closeout/ratify/flip work is DROPPED-as-suspended -- nothing to drive, do not re-surface. This is the COO pre-existing TO the sweep-brief named as SUPERSEDED.</suspension_note>
    <dispatch_state>WRITTEN-NOT-DISPATCHED (wind-down 2026-07-07; Andrew directed decomposition materialized before device reboot; dispatch on restart per the allocation-map in the session handoff /log)</dispatch_state>
    <gate_note>SEV1 = Andrew (sovereign); SEV2 = CTO+COO (RESOLVABLE now); ramp-flip = CTO (evidence-gated). ~90% gate-wait, ~0% build.</gate_note>
  </metadata>

  <objective>Drive the 5 staged rows (TO-3) to ratified + flip enforcement. Engine + pipescript surface LIVE+verified (TO-2/4/5). SEV1 rows (benchmark/headline/advisor_nna) need Andrew sign-off -> Nessie hash via --load-contracts; SEV2 (peers/aum) need CTO+COO; CTO ramp-flips comp-surface-check Q2 advisory->blocking on low-FP evidence.</objective>

  <requirements>
    <requirement id="1">SEV1 rows Andrew-signed -> real Nessie hash stamped</requirement>
    <requirement id="2">SEV2 rows CTO+COO-signed</requirement>
    <requirement id="3">CTO ramp-flips advisory->blocking (low-FP-gated)</requirement>
    <requirement id="4">BMKAUD synthetic replay caught end-to-end post-flip</requirement>
  </requirements>
</task_order>
```
