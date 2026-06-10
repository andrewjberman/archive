<to_id>NFRA_GLOBGRPH.ICEBERG-409</to_id>
<project>NFRA_GLOBGRPH</project>
<title>Iceberg 409 commit-retry/backoff in derive_runner (concurrent-writer race vs Item-2b)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (LD-0177 Andrew-direct NFRA staffing; decomposition per CTO dispatch list 174053Z)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>complete (2026-06-10 ~18:10Z), RAVC2-ACCEPTED by COO 1803Z. Code e574a0c7c (_overwrite_with_retry: table re-loaded per attempt, exp backoff 2s base/30s cap/50% jitter/5 attempts env-tunable; CommitStateUnknown retried — overwrite idempotent; _ensure_table survives concurrent create). 4-case mock smoke PASS. Image built via CodeBuild 052acccf (SUCCEEDED) -> ECR :latest + 20260610-175421. ECS verify task 0a9119b0 exit 0: full clean cycle on new image (1176 nodes/2539 edges written through the retry path, NESSIE_COMMIT ok, snapshot archived). Tag globgrph-v0.1.6. Landed BEFORE Item-2b goes live per sequencing constraint; tonight's 02:00Z nightly uses the new image. Real concurrent-409 exercise only possible once Item-2b is live (by design).</status>

Add commit-retry with backoff to derive_runner for Iceberg 409 conflicts -- the nightly full-derive and Item-2b incremental writer will race once 2b is live. RAVC2 to COO.
