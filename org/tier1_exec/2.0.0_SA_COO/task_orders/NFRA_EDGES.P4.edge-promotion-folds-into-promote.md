# Task Order: NFRA_EDGES P4 -- EDGE-PROMOTION folds into NFRA_PROMOTE (a new ProducerKind, NOT a new mechanism)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-08-nfra-edges-p4-promote-fold</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.5.0_AE_OpalETL / 0.4.0_DS_ClientPlatform~B (NFRA_PROMOTE lane) + 1.0.0_SA_CTO (governed-migration ratify) | CVO cert</issued_to>
    <date>2026-07-08</date>
    <status>staged -- SCOPED OUT of NFRA_EDGES core; tracked as an NFRA_PROMOTE extension. GO after P1-P3 land (PRD SS8 Q1 lean: reification first, promotion is the capstone). Gated on P1-P3 + NFRA_PROMOTE coordination.</status>
    <prd_ref>docs/architecture/NFRA_EDGES_PRD.md (SS3-P4, SS5 Q3-folds-into-PROMOTE, SS8 Q1-timing) + NFRA_PROMOTE_PRD.md</prd_ref>
    <gate_note>Edge-promotion is NOT a new mechanism -- a validated edge-motif promotes via the EXISTING NFRA_PROMOTE 5-invariant gate as a NEW ProducerKind (like the R4 @0.4 ProducerKind.PROMOTE governed bump). This TO tracks the fold; it lands in the NFRA_PROMOTE plane.</gate_note>
  </metadata>

  <objective>Fold edge-motif promotion into NFRA_PROMOTE as a new ProducerKind (governed schema bump, like R4 @0.4), so a validated recurring edge-motif promotes through the existing 5-invariant gate (measure-before-promote / human-ratify / anti-Goodhart / reversible / inspectable) -- NO new gate, NO new mechanism.</objective>

  <requirements>
    <requirement id="1">NEW ProducerKind for edge-motif promotion via the GOVERNED schema-bump pattern (author -> CTO-arch-gate -> CVO-re-sign -> COO SoD-land the cse_schema bump, same SoD as R4 @0.4 ProducerKind.PROMOTE). NOT a new gate -- the edge-motif rides the existing 5-invariant PROMOTE gate.</requirement>
    <requirement id="2">the promoted edge-motif inherits AC4 (collision-safe node_id, unique-by-construction) + AC5 (snapshot_ts / CloudNode-conform / freshness-covered) from P1-P3 -- the promotion does not re-open the collision or freshness discipline.</requirement>
    <requirement id="3">measure-before-promote (the coupling/recurrence signal for the edge-motif) + reversible (auto-demote on degradation) apply unchanged -- the edge-motif is a promotion candidate like a node-motif.</requirement>
    <requirement id="4">TIMING (SS8 Q1): GO after P1-P3 land (the reification + subgraph must exist before an edge-motif can promote). Coordinate with the NFRA_PROMOTE plane owner -- it's a PROMOTE extension, tracked there.</requirement>
  </requirements>

  <acceptance_criteria>
    1. A validated recurring edge-motif promotes via the existing NFRA_PROMOTE 5-invariant gate as a new ProducerKind (governed bump, CTO-ratified + CVO-re-signed + COO SoD-landed); the 5 invariants BITE on an edge-motif candidate.
    2. Reversible (promote -> degrade -> auto-demote) proven on an edge-motif; AC4/AC5 inherited. CVO cert. RAVC COO~B + the NFRA_PROMOTE owner.
  </acceptance_criteria>
</task_order>
```
