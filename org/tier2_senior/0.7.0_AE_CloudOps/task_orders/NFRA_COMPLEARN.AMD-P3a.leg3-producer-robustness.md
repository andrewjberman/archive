<task_order>
<id>NFRA_COMPLEARN.AMD-P3a</id>
<project>NFRA_COMPLEARN</project>
<title>AMD P3a -- leg-3 producer robustness + HARD freshness gate + "make the nightly-Fargate emit claim TRUE or DELETE it"</title>
<assigned_to>0.7.0_AE_CloudOps~B</assigned_to>
<issued_by>2.0.0_SA_COO~A</issued_by>
<issued_date>2026-07-10</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25 (S2): <project> field repaired from "NFRA_COMPLEARN (amendment)" to NFRA_COMPLEARN, which is complete. Closed as a record act, not a work verdict. Prior status: pending</status>
<priority>#3 program leg, NON-URGENT / LAST -- leads behind the 0.8.0 P1 foundations. CloudOps infra.</priority>
<dispatch>GO 2026-07-10 by COO~A. 0.7.0_AE_CloudOps~B is Andrew-cleared as OURS (base + ~A remain Andrew's -- OFF-LIMITS). THIS IS A DISPATCH POINTER -- the full arch-gated spec is authoritative; read it before building.</dispatch>
<full_spec>org/projects/NFRA_COMPLEARN/task_orders/NFRA_COMPLEARN.AMD-P3a.leg3-producer-robustness.md @ 8dfcf1e75</full_spec>
<load_bearing_invariants>
  1. "MAKE THE CLAIM TRUE OR DELETE IT": no comment may assert a nightly Fargate emit that does not run. Either stand up the actual scheduled invoker (located/verified LIVE) or DELETE the claim.
  2. FRESHNESS IS A HARD GATE, EXERCISED by going stale: prove it by letting tool_activity go stale and observing the alarm/block -- not a comment (AC-L3a). Every host-only source DISCLOSED with an alarm; no source silently absent from the cloud catalog (AC-L3b).
  3. Per-source decision: cloud-ship (EventBridge->Fargate, gold-run pattern) for git-tracked sources vs explicit-host-local-with-alarm for the irreducibly host-only ones.
  4. SOVEREIGN BOUNDARY: no bd / 49F / Schwab read or target (comp-blast cache = names only).
</load_bearing_invariants>
<diff_gate>Route EVERY build diff to 1.0.0_SA_CTO~A for the arch-gate BEFORE it is treated as landed. RAVC to 2.0.0_SA_COO~A on completion.</diff_gate>
</task_order>
