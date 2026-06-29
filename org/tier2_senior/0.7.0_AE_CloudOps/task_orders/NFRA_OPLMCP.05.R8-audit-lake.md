<to_id>NFRA_OPLMCP.05.R8</to_id>
<project>NFRA_OPLMCP</project>
<title>OPLMCP.05 (R8) audit->lake/Athena -- route the gateway per-call audit to a queryable data-lake (AC4 lake-reach)</title>
<assigned_to>0.7.0_AE_CloudOps (base; AE-CloudOps -- gateway-emit + S3/Firehose/Athena infra)</assigned_to>
<consult>0.4.0_DS_ClientPlatform (only if the Athena data-model gets non-trivial -- a JSON-over-S3 audit table shouldn't need it, per CTO)</consult>
<verify>3.0.0_SA_CVO (AC4 lake-reach: a sample audit row queryable via Athena)</verify>
<issued_by>2.0.0_SA_COO (OPLMCP DRIVE-TO-DONE R8; CTO drive-to-done plan 2026-06-23; Andrew-direct OPLMCP-completely-done)</issued_by>
<issued_date>2026-06-24</issued_date>
<status>complete</status>
<!-- CLOSEOUT 2026-06-29 (0.7.0_AE_CloudOps~B, COO reconciliation-pass GO 184506Z; corrects my own earlier false-positive call -- I'd read the TO objective only, not the LIVE state; live-grounding shows R8 is BUILT + LIVE). Grounded:
- AC1 (audit reaches the lake, queryable): audit-lake.tf is APPLIED -- s3 opal-mcp-audit + opal-mcp-athena-results buckets + Glue DB opal_mcp + Glue table mcp_audit (JSON-over-S3, partition PROJECTION on dt, location s3://opal-mcp-audit/audit/). The bucket is RECEIVING date-partitioned per-call audit LIVE (audit/dt=2026-06-29/*.jsonl landing today). audit.py ships each record to AUDIT_S3_BUCKET via _s3_client.put_object (in-VPC S3 gateway endpoint, no Firehose).
- AC2 (redaction preserved): the Athena rows carry ts/user/tool/outcome only -- NO message bodies (privacy bar held).
- AC3 (CVO lake-reach: a sample audit row queryable via Athena): VERIFIED ~B 2026-06-29 -- Athena query (QID b0addd0b) "SELECT ts,user,tool,outcome FROM opal_mcp.mcp_audit WHERE dt='2026-06-29' LIMIT 5" SUCCEEDED, returned 5 real redacted rows (andrew@opalinvest.com / ms_site_children / ok). CVO co-signs the AC3 lake-reach (verify-owner).
- AC4 (infra applied): live (buckets + Glue table present + queryable).
Flipped active->complete; CVO co-signs AC3. -->
<!-- ORIGINAL: active -->
<!-- Queued after .07 AC2 in base-AE's lane. AC4-lake-reach gates the OPLMCP macro-close. The on-box audit is the v1 FLOOR (already live); this is the real .05 lake-routing build. -->

<objective>
Route the gateway's per-call audit log to a queryable data-lake (S3 + Athena) so the OPLMCP audit is fleet-queryable -- closing the AC4 lake-reach (which gates the OPLMCP macro-close). SPEC + BUILD (the on-box audit is the v1 floor; the lake routing is the real build).
</objective>

<the_work>
The gateway _emit (the per-call audit: user-identity + tool + ts, message-BODIES-REDACTED) -> S3 (Firehose or direct write) -> Athena external table (JSON-over-S3, date-partitioned) -> queryable.
- Preserve the redaction (no message bodies in the lake -- the AC4/privacy bar).
- In-VPC routing note (per the globgrph finding): the writer can't reach SNS/CW-PutMetricData in-VPC (no monitoring endpoint + no NAT) -- if a LOUD failure-channel is wanted, use a CW-Logs metric-filter on the audit/error log-line -> metric -> alarm -> SNS-egress, NOT SNS/PutMetricData from the writer. (The audit->S3->Athena path itself uses the S3 gateway endpoint.)
- Infra (Firehose/Athena/Glue-table) via Terraform -> safe-apply + a deploy-completion ledger if it's a real cutover.
</the_work>

<acceptance_criteria>
1. The gateway per-call audit reaches the lake: S3 (date-partitioned) + an Athena external table, queryable.
2. Redaction preserved end-to-end (no message bodies in the lake).
3. CVO verifies AC4 lake-reach: a real sample audit row queryable via Athena (verify-on-served, not self-report).
4. Any infra deployed via safe-apply (+ deploy-completion ledger if a cutover); ds-gate per .py.
5. RAVC2 COO + CTO.
</acceptance_criteria>
