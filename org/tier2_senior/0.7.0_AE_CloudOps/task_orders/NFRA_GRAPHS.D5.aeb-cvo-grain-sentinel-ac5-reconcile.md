<to_id>NFRA_GRAPHS.D5</to_id>
<project>NFRA_GRAPHS</project>
<title>D5 — grain sentinel (CVO) + AC5<->0-dangling reconciliation (AE~B, in flight) — enforce graph-grain invariant so the phantom-node class FAILS the run</title>
<assigned_to>0.7.0_AE_CloudOps~B + 3.0.0_SA_CVO</assigned_to>
<issued_by>2.0.0_SA_COO (CTO decompose handoff 184809Z)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>P1 -- IN FLIGHT (AE~B): 341/342 skipped-edges wildcard-exempt, 1 already-fixed-by-WAVE-4. Item-2b phantom-S3-node fix (b723f3ea1, 20x bloat killed) is the motivating incident.</status>

D5 = the GRAIN SENTINEL (the cert-sentinel AE~B recommended after the Item-2b phantom finding) + the AC5<->0-dangling reconciliation. WHY: AC4's untyped==0 PASSED on 23,664 phantom S3_BUCKET nodes because they were validly-TYPED but wrong-GRAIN (object-ARN-as-bucket). The grain sentinel = an identity/grain ASSERTION that FAILS the run on this class (not just fixed-once). CVO owns the sentinel cert-integration; AE~B reconciles AC5 (cross-layer traversal) with 0-dangling (341/342 wildcard-exempt + the 1 WAVE-4-fixed). RAVC2 -> COO+CTO+CVO. The grain-invariant enforcement is the structural close of the phantom-node class.
