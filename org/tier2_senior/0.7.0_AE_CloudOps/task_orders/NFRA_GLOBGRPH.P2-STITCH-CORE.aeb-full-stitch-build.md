<to_id>NFRA_GLOBGRPH.P2-STITCH-CORE</to_id>
<project>NFRA_GLOBGRPH</project>
<title>GLOBGRPH P2-STITCH-core full build: L1 portal AST extractor -> stitch-edge derive -> kuzu load -> AC5 traversal done-gate</title>
<assigned_to>0.7.0_AE_CloudOps~B</assigned_to>
<issued_by>2.0.0_SA_COO (Andrew reallocation 2026-06-11 ~1825Z — base-AE offline, AE~B owns P2-STITCH + Nessie/Fargate)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>active -- DISPATCHED to AE~B (inbox 182910Z; Andrew confirms received, AE~B heads-down). FULLY UNBLOCKED (CTO comp-aws v3.x final 53816378a schema + 514d433d8 comp-platinum firm-vocab). Base-AE's prior P2-STITCH ownership retired (Andrew direct).</status>

CONTEXT: Andrew took base-AE (0.7.0) offline (DTAFLP P1/COTETL/§8/trade-recon all done+verified) + reallocated the full GLOBGRPH P2-STITCH-core to AE~B, which he brought online for the parallel Nessie/Fargate infra layer. The stitch<->infra coordination is now INTRA-LANE (AE~B owns both) -> removes the cross-lane collision risk that surfaced earlier (P2-STITCH deliverable lands in CTO's then-locked NFRA_COMPAWS_SCHEMA.md; CTO's expansion is now DONE so the schema is frozen/stable).

BUILD (multi-component, sequence + RAVC2 per component):
1. L1 portal AST extractor (portal-side; CTO-cleared parallel-safe, NOT his locked files).
2. stitch-edge derive -> stitch to the FINAL comp-aws schema 53816378a; the P2 stitch-vocab lands in NFRA_COMPAWS_SCHEMA.md (schema now frozen).
3. kuzu load (stitched graph into Kuzu) -- align with AE~B's Nessie/Fargate graph-runtime/substrate work.
4. AC5 traversal = the BINDING done-gate (CVO certifies the cross-layer traversal that proves the stitch).

UNBLOCKED BY: CTO comp-aws v3.x final 53816378a (schema + INVOKES/IAM/API_GW/S3 edges) + 514d433d8 (comp-platinum firm-parameterized trace graph — stops confidently-wrong cross-firm ADVI traces). RAVC2 each component -> COO+CTO; AC5 -> CVO done-gate. Flag COO for any CTO stitch-vocab ruling or Nessie/Fargate-vs-stitch collision.
