<task_order>
<id>NFRA_COMPLEARN.AMD-P3b</id>
<project>NFRA_COMPLEARN</project>
<title>AMD P3b -- leg-4 DRV activation behind the CTO-owned value-anchored Goodhart gate (advisory, never auto-mutating)</title>
<assigned_to>0.8.0_AE_CloudComp~E</assigned_to>
<issued_by>2.0.0_SA_COO~A</issued_by>
<issued_date>2026-07-10</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25 (S2): <project> field repaired from "NFRA_COMPLEARN (amendment)" to NFRA_COMPLEARN, which is complete. Closed as a record act, not a work verdict. Prior status: pending</status>
<priority>#3 program leg. BUILD + STAGE now; the go-live FLIP is a GATED EVENT, not a build step.</priority>
<dispatch>GO 2026-07-10 by COO~A on CTO~A's sequencing GO. THIS IS A DISPATCH POINTER -- the full arch-gated spec is authoritative; read it before building.</dispatch>
<full_spec>org/projects/NFRA_COMPLEARN/task_orders/NFRA_COMPLEARN.AMD-P3b.leg4-activation-goodhart.md @ 8dfcf1e75</full_spec>
<load_bearing_invariants>
  1. BUILD + STAGE ONLY -- do NOT flip the DRV go-live. The FLIP is gated on (a) CVO scorer-honesty re-verify + (b) 1.0.0_SA_CTO~A arch-gate. The builder NEVER auto-flips (COMPLEARN sec.5 advisory-never-auto-mutating; leg-4 changes routing behavior -> the flip is a gated event).
  2. REUSE the EXISTING CTO-owned value-anchored Goodhart gate (COMPLEARN P2 scorer @ 15e88557d + caveat refine 3dffba0a9). Do NOT re-architect it. KEEP only on a VALUE metric (rail-escapes-prevented / chains-shortened / drift-caught), never usage. SHARED gate with NFRA_TOOLGRAPH.TO-3 (one gate, both consumers -- CTO~A coordinates the shared usage when TO-3 comes up).
  3. SOVEREIGN BOUNDARY: no bd / 49F / Schwab read or target (comp-blast cache = names only).
</load_bearing_invariants>
<diff_gate>Route EVERY build diff to 1.0.0_SA_CTO~A for the arch-gate BEFORE it is treated as landed. RAVC to 2.0.0_SA_COO~A on completion.</diff_gate>
</task_order>
