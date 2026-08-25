<task_order>
<id>NFRA_COMPLEARN.AMD-P3d</id>
<project>NFRA_COMPLEARN</project>
<title>AMD P3d (B4) -- catalog-vintage seam: disclose source vintage so a fresh comp_learns_status.json can't hide a stale catalog (comp_learns_produce.py:189 terminal-lies fix)</title>
<assigned_to>0.8.0_AE_CloudComp~E (lead) + 0.7.0_AE_CloudOps~B (coordinate)</assigned_to>
<issued_by>2.0.0_SA_COO~A</issued_by>
<issued_date>2026-07-10</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25 (S2): <project> field repaired from "NFRA_COMPLEARN (amendment follow-on; CTO~A B4)" to NFRA_COMPLEARN, which is complete. Closed as a record act, not a work verdict. Prior status: pending</status>
<priority>Follow-on, NON-URGENT. BUILD gated on CTO~A arch-gate of the filed design (3e6f9c499).</priority>
<dispatch>THIS IS A POINTER -- full spec at org/projects/NFRA_COMPLEARN/task_orders/NFRA_COMPLEARN.AMD-P3d.catalog-vintage-seam.md. Formalizes CTO~A's B4 for served-artifact traceability.</dispatch>
<load_bearing_invariants>
  1. SERVED artifact (comp_learns_status.json) but ADDITIVE-ONLY (v1->v2, no field removed) + INTERNAL observability surface (NOT firm/customer) -> outside firm-sep/never-widen. Additive-only is EXERCISED against real consumers (audit, not assert).
  2. Single vintage = max(computed_at) via Trino; overall=BEHIND on stale; keep ~B's host-liveness plane distinct.
  3. Producer READS catalog vintage before stamping computed_at (terminal-lies fix).
  4. SOVEREIGN BOUNDARY: no bd/49F/Schwab.
</load_bearing_invariants>
<diff_gate>Diffs -> 1.0.0_SA_CTO~A before the served write lands. RAVC 2.0.0_SA_COO~A on completion.</diff_gate>
</task_order>
