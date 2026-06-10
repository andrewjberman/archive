<to_id>NFRA_COMPAWS.SFN-FIX</to_id>
<project>NFRA_COMPAWS</project>
<title>StepFunctions cert fix: SFN-INVOKES-NESTED-GAP (ASL walk misses 17 Lambda invokes nested in 2 Parallel blocks)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (LD-0177 Andrew-direct NFRA staffing; decomposition per CTO dispatch list 174053Z)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>active -- GO (CVO re-cert after)</status>

Fix the ASL walker to descend into Parallel blocks (yang-generate fan-out = 17 missed Lambda invokes). CVO re-certifies the SFN node class after. RAVC2 to COO + CVO.
