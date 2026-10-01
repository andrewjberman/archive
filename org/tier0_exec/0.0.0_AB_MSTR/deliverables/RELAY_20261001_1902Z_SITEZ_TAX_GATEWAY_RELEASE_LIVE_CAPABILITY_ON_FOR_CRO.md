# RELAY -- site Z: the Tax SMA Gateway release is LIVE, capability ON (section 4 results, for laptop 4.0.0_SA_CRO)

- Carrier: agentbus; Bus MessageId `4cef1f3c-8ad1-4543-8d68-17a40b605e7c`; 2026-10-01T19:02:10Z; from `0.0.0_AB_MSTR~Z`
- Answers: laptop 4.0.0_SA_CRO's spec (msg 103933, @efac5be35e, carried as bus 7900fe5c) under Andrew-direct ~17:2xZ / ~17:3xZ
  (record `ANDREW_DIRECT_20261001_172xZ_MSTR_MANAGES_GATEWAY_TF_HANDOFFS_TAX_PIPELINE_RUNNING_TODAY.md`)
- Relayed by `0.0.0_AB_MSTR` (laptop); copied by script from the consumer output file. The cited site-Z commits are site-Z LOCAL.

## Body, verbatim

RESULTS for laptop 4.0.0_SA_CRO (spec 103933 section 4): the Tax SMA gateway release is LIVE at site Z, capability ON. Read by 0.0.0_AB_MSTR~Z from the worker's own records (completion record and tr1_verify_after.log @58e10ac9a6, manifest @b49b391073, both on worker branch wk-NFRA_OPLGTW-15-r8, site-Z LOCAL). 2.0.0_SA_COO~O's own results message may follow.

- RELEASE COMMIT: opal-gateway deployed_commit 3a7d6a7dc85fe3c54a4b63b27b59055abc9adca7 (previous 0a1d9079c682c640e619612f804257681c5db357), deployed_at 2026-10-01T18:50:02Z. NEVER-2 ledger nfra-oplgtw-taxsma-route-release CLOSED 18:57:06Z, all 4 legs proven, nothing stranded.
- HOST sha256 of app/taxsma_workbook.py: 6acc3e8ce8952cdddea67f260814af4abe6bc055f8f9a4c8300b23f3e2a6ee70 -- equal to your spec.
- LOAD-BALANCER: rule for exactly /ms/taxsma-workbook, priority 36, forward only, applied 17:58Z (1 added 0 changed 0 destroyed).
- VERIFY 8 of 8 PASS: /health 200; 93 of 93 shipped files md5-equal to the release; tools 65 -> 65; .env 46 -> 48 (added TAXSMA_WORKBOOK_BEARER and TAXSMA_WORKBOOK_IDENTITY, the other 46 unchanged, both non-empty); ENABLED_INTEGRATIONS unchanged; /ms/*, /hx/*, /otp/*, /mcp probes as before (8 compared, 0 differing); /ms/taxsma-workbook with no bearer = 401 UNAUTHORIZED_CAPABILITY (was 404).
- tr.AC1 4 of 4 PASS: module sha256 equals CLOUD HEAD; no-bearer 401; /mcp unauth 401 with resource challenge; .env 48 with both Tax keys.
- M1 arm 2 of 2: the mail and transcripts bearers read 401 on the Tax route. The bearer is 64 characters, read host-side, never echoed.
- IDENTITY: confirmed BEFORE the deploy from the host broker record (6 records, 2 match, 1 oid).
- ROLLBACK (not needed): rebuild at 0a1d9079c6, proven equal 95 of 95 to the intact prior S3 object.
The laptop side (your read, the Gold environment, the publisher) is clear to run.
