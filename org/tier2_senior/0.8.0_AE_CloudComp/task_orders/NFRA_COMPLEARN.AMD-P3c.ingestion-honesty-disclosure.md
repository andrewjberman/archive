<task_order>
<id>NFRA_COMPLEARN.AMD-P3c</id>
<correction date="2026-07-10" by="CTO~A arch-gate; COO~A path-grounded">NOT DAYLIGHT-HELD. comp_log_auto.py lives at org/modules/graph/comp_log_auto.py (NOT .tools/; .tools/comp_log_auto.py confirmed ABSENT), so this leg is NOT subject to the .tools/**->BASE_EXEC daylight hold. ALL "daylight-held / land-only-in-daylight / BASE_EXEC" language below is SUPERSEDED: P3c LANDS after commit-gate + landing-verify, no BASE_EXEC handoff.</correction>
<project>NFRA_COMPLEARN</project>
<title>AMD P3c -- ingestion honesty: comp_log_auto disclosure (a dropped emission DISCLOSED, not swallowed; R5/R7)</title>
<assigned_to>0.8.0_AE_CloudComp~E</assigned_to>
<issued_by>2.0.0_SA_COO~A</issued_by>
<issued_date>2026-07-10</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25 (S2): <project> field repaired from "NFRA_COMPLEARN (amendment)" to NFRA_COMPLEARN, which is complete. Closed as a record act, not a work verdict. Prior status: pending</status>
<priority>#3 program leg. DESIGN + STAGE now; the enforcer EDIT lands only in daylight.</priority>
<dispatch>GO 2026-07-10 by COO~A on CTO~A's sequencing GO. THIS IS A DISPATCH POINTER -- the full arch-gated spec is authoritative; read it before building.</dispatch>
<full_spec>org/projects/NFRA_COMPLEARN/task_orders/NFRA_COMPLEARN.AMD-P3c.ingestion-honesty-disclosure.md @ 8dfcf1e75</full_spec>
<load_bearing_invariants>
  1. DESIGN + STAGE the comp_log_auto disclosure now (a dropped emission DISCLOSED via count/marker, not swallowed by try/except pass). The enforcer EDIT to comp_log_auto is DAYLIGHT-HELD (.tools/**->BASE_EXEC) -- LAND only in daylight, do not land the edit now.
  2. EXERCISED, not asserted (AC-L3c): prove it by FORCING a write failure and observing the disclosure -- a passing assertion never mutated has never been tested.
  3. SOVEREIGN BOUNDARY: no bd / 49F / Schwab read or target.
</load_bearing_invariants>
<diff_gate>Route the design/diff to 1.0.0_SA_CTO~A for the arch-gate BEFORE the edit lands. RAVC to 2.0.0_SA_COO~A on completion.</diff_gate>
</task_order>
