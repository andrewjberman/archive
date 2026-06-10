<to_id>NFRA_GLOBGRPH.ICEBERG-409</to_id>
<project>NFRA_GLOBGRPH</project>
<title>Iceberg 409 commit-retry/backoff in derive_runner (concurrent-writer race vs Item-2b)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (LD-0177 Andrew-direct NFRA staffing; decomposition per CTO dispatch list 174053Z)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>active -- sequencing: MUST land before Item-2b goes live (concurrent-writer race)</status>

Add commit-retry with backoff to derive_runner for Iceberg 409 conflicts -- the nightly full-derive and Item-2b incremental writer will race once 2b is live. RAVC2 to COO.
