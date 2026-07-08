# Task Order: NFRA_SEMCTL FINALIZE -- the loop-close finalization tail (3 non-gating follow-ons -> fully closed)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-08-nfra-semctl-finalize-tail</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>3.0.0_SA_CVO (R4 re-sign) + 2.0.0_SA_COO~B (R4 SoD-land) + 0.7.0_AE_CloudOps (C3-materialize) + 0.4.0_DS_ClientPlatform~B (focused-coupling refinement) + 0.5.0_AE_OpalETL (store coord)</issued_to>
    <date>2026-07-08</date>
    <status>complete -- CLOSED 2026-07-08. All 3 finalize items DONE: (1) R4 @0.4 schema-bump landed (995419d28) + version-owner-signed-off + tool-leg wired (a0528032d); (2) focused-coupling flip to focused_coupling_ratio @0.12 CVO-certed (c5fd9d85f, ordering-preserved + not-tuned); (3) MOTIF C3-materialize DELIBERATE DEPLOY COMPLETE (0.7.0/CloudOps coupled @0.4 pass, ledger 20260708T1807Z OPENED->CLOSED in-session, all 5 legs, NEVER-half-land satisfied): @0.4 derive-image rebuild-from-HEAD (ECR :latest b76cefe6, producers now emit @0.4) + C3+CONTAINS materialize (7 nodes [6 C2Motif+1 C3System semctl] + 36 CONTAINS, 0 unresolved, round-trip verified, comp-kuzu re-finalized = CVO's residual CLOSED) + PROMOTE producer live-emit (0.5.0, PROMOTE CSE @0.4 in iceberg.globgrph.cse -> cse_directive_effectiveness = FEDOBS now SEES the promotion = the R4 raison d'etre delivered). CVO~B independently certed the N=1-clean round-trip; CTO's 4 conditions met. NON-GATING follow-on: CVO~B's C3 node_id collision in DS~B discovery code (N=1 clean today; separate re-rebuild+re-cert when DS~B regenerates the spec).</status>
    <prd_ref>docs/architecture/NFRA_SEMCTL_PRD.md + NFRA_PROMOTE_PRD.md + NFRA_MOTIF_PRD.md</prd_ref>
    <dispatch_state>DISPATCHED 2026-07-08 by COO~B on Andrew's finalize directive. All 3 are non-gating to the (already CLOSED) loop-close acceptance; they complete the tail.</dispatch_state>
    <gate_note>The SEMCTL federated learning loop is CLOSED clean on real data (CVO full-pass 4395c0bb5) + STANDING (CVO c13a73cdd/61ae8c3f1). These 3 follow-ons finalize the tail.</gate_note>
  </metadata>

  <objective>Fully finalize the 3 non-gating loop-close follow-ons so the SEMCTL plane is 100% closed with no open tail.</objective>

  <requirements>
    <requirement id="1" owner="3.0.0_SA_CVO -> 2.0.0_SA_COO~B">R4 GOVERNED SCHEMA-BUMP: the PROPOSED ProducerKind.PROMOTE=\"promote\" 5th-producer emission contract (~D a5271978f, CTO-arch-gated + version-PINNED @0.4). CVO re-signs the schema/enum change -> COO~B SoD-lands the cse_schema.py 0.4 bump (add ProducerKind.PROMOTE; DS~B version-history line cse_schema.py:42; ~D's optional MIGRATION_NOTE docstring; ping ~D at land to retire the trail-record CSE interim -> schema-validated PROMOTE emission + DS~B confirms the coverage-sweep greens). Version-coordinate with DS~B (@0.3 -> 0.4 sequential).</requirement>
    <requirement id="2" owner="0.7.0_AE_CloudOps">MOTIF C3-GRAPH MATERIALIZE: execute DS~B's handed C3+CONTAINS edge spec (541810435) -- store-write the discovered C3 system(s) + CONTAINS edges into the graph via the in-VPC derive/ingest path (same path that materialized the 91 clusters). VERIFY the round-trip (C3 nodes + CONTAINS edges live at canonical HEAD). This is a HEAD-ADVANCING op -> it ALSO exercises + closes CVO's comp-kuzu re-finalize-on-advance residual (the not-yet-exercised advance case). RAVC COO~B + CVO -> CVO certs the materialized round-trip + confirms comp-kuzu re-finalizes to the new HEAD.</requirement>
    <requirement id="3" owner="0.4.0_DS_ClientPlatform~B + 0.5.0_AE_OpalETL">FOCUSED-COUPLING SIGNAL REFINEMENT (CVO signal-quality note): the coupling_ratio can be inflated by BROAD-commit co-appearances (3/6 acceptance-sample shas were broad sweeps; the standing store 107/454 holds raw). Refine the ratio computation to WEIGHT/DISCOUNT broad commits -- e.g. a per-session file-count ceiling or focus-weighting so a focused co-change counts more than a sweeping one. DS~B owns the coupling_ratio (P1 gate); 0.5.0 owns the standing store (raw events stay raw -- the refinement is at the RATIO/gate layer, not the store). NON-BLOCKING (the promotion holds on the focused commits alone, CTO-git-verified); this hardens the signal quality for future candidates. Self-test the refined ratio; RAVC COO~B + CC CTO/CVO.</requirement>
  </requirements>

  <cross_domain_coordination>
    - R4 is a governed cross-plane migration (CTO algebra plane) -- SoD-land pattern (author ~D / arch-gate CTO / re-sign CVO / commit COO~B), same as the 0.3 bump.
    - The C3-materialize round-trip is the CLEAN way to exercise the comp-kuzu re-finalize-on-advance residual (a real HEAD-advance) -- fold the two.
    - The focused-coupling refinement is at the RATIO/gate layer (DS~B P1), NOT the store (0.5.0 keeps raw events) -- correct layering per the standing-loop cert.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. R4: cse_schema.py @0.4 with ProducerKind.PROMOTE landed (CVO re-signed + COO SoD-committed); ~D's schema-validated PROMOTE emission live; coverage-sweep green.
    2. C3-materialize: C3 nodes + CONTAINS edges live at HEAD (round-trip verified, Rule 22); CVO cert; comp-kuzu re-finalize-on-advance residual CLOSED.
    3. Focused-coupling: the ratio discounts broad-commit inflation, self-tested; the acceptance-run promotion (silent-display-fork) still holds under the refined ratio. RAVC COO~B.
  </acceptance_criteria>
</task_order>
```
