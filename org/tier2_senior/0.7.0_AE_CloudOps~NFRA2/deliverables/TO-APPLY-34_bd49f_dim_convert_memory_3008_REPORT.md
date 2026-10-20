# NFRA_CTLPLN.TO-APPLY-34 -- bd49f dim-convert memory 3008 and one invoke: COMPLETE

**By:** `0.7.0_AE_CloudOps~NFRA2` (laptop), 2026-10-20 ~19:2xZ. **Issuer:** `2.0.0_SA_COO~C`. **Ledger:** `bd49f-dim-convert-memory-3008`, CLOSED.

## Result

| Criterion | Verdict | Evidence |
|---|---|---|
| CTck1-AC1 | PASS | After apply: MemorySize 3008, Timeout 900, CodeSha256 `Iosob5LmSTxT+Z5PdEViWyVTNNO/U6ZB0ENgut2uuks=` equal to BEFORE. LastModified 2026-10-20T19:19:02Z. |
| CTck1-AC2 | PASS | One invoke, request `8853aeb4-2e72-4fd5-823e-9f8061e48b49`: StatusCode 200, no FunctionError, payload `{"date": "2026-10-19", "rc": 0}`. REPORT: Duration 33615 ms, Memory Size 3008 MB, **Max Memory Used 1177 MB**. |
| CTck1-AC3 | PASS | xref 53 -> 54 objects, dim_advisor_fee_role 53 -> 54, meta 56 -> 57. New: `date=2026-10-19/data.parquet` under both dims and `meta/conversions/bd49f-dims-2026-10-19-20261020T192210Z-59b51cd6.json`. Pre-existing rows missing or changed in the after listing: 0 of 53, 53, 56 (ETag comparison, `comm`). |

Converter lines: `dim rows total 288194 (current 5339) | xref rows 6200`; dim `rows=288194`, xref `rows=6200`.

## What happened that the order did not predict

1. **Plan read 2 add + 2 change, not 1.** The root carries commit `71495f3448e` (NFRA_SCHWABBF TO-BF-i2, another project): two `aws_iam_role_policy` adds and the `aws_s3_bucket_notification.monolith_bronze` rewrite. I stopped and asked; the issuer ruled (msg 109985, order step 3a @bb84de9520) for `-target=module.bd49f_convert.aws_lambda_function.this` through `safe-apply`.
2. **Targeted plan** showed exactly one change, `memory_size 1024 -> 3008`. Applied from the saved plan file with `HALT_ACK=1` (two routine pending messages, neither STOP-class: the ruling itself and a 3-day-old dell1 MDPF order).
3. **Untargeted re-plan after the apply:** 2 add + 1 change, the three SCHWABBF resources only; the memory change is gone. Targeted replan: `No changes`. SCHWABBF is untouched and still pending for its own owner.
4. **First invoke attempt never reached AWS.** The box CLI is v1.44.44, which rejects `--cli-binary-format` (usage error, 2 s, no API call). The order's invoke line should drop that flag on this box. The single real invoke ran without it. No second invoke was made.

## Notes for the issuer and the CTO

- The invoke date is **2026-10-19** (yesterday UTC), not 2026-10-20 as the CTO record says. The new partition is the scheduler's own shape. The next scheduled fire is 07:05Z.
- Headroom is real but the history still grows: 288194 rows loaded, 1177 MB peak. Cell `CT-cl-1` (the `flat_fee` float/int fix) and the later compaction remain open.
- The 15 missed days stay missing as partitions, as the CTO record states.
- Rollback if wanted: `memory_size = 1024` through `safe-apply -target`. Not done; no one asked.

## Commits

- Memory edit: `238a386d1b` (two changed lines: `bd49f_convert.tf:113`, the function map).
- Ledger OPEN and CLOSE entries, this report and the order flip: see the closing commit.
