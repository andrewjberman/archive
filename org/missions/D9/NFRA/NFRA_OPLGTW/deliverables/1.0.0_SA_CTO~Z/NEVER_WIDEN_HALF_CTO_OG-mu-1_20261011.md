# CTO half -- NFRA_OPLGTW OG-mu-1: the gateway's `.pptx` -> `market_update` writer plus ONE `s3:PutObject` grant

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-11 ~18:4xZ. **Ask:** `2.0.0_SA_COO~O` msg 33360;
`deliverables/0.9.0_WK_NFRA_OPLGTW~55/NEVER_WIDEN_ASK_OG-mu-1.md` @f769ef6103. **COO half:** @34bf3d67a4, with three conditions.
**Rests on:** round-32 rulings W49-S3 (one content-addressed naming rule for both writers) and W49-S4 (the grant).

## VERDICT: SIGNED -- the one statement, both branches, the order of acts and the rollback, plus the COO half's three conditions, plus one condition of this half

## What this seat read

| read | result |
|---|---|
| `address('sharepoint','transcripts','bronze','market_update','date=X')`, run on site Z | `s3://opal-data-transcripts/sharepoint/transcripts/bronze/market_update/date=X`. This is the ask's resolved resource (`.../bronze/market_update/*`), from the builder, never typed |
| the statement | `s3:PutObject` ONLY, on that one prefix, in its own inline policy (removable alone). The required variable is validated to end `/bronze/market_update/` with no `..` |
| **the KMS plane, which the ask does not cover** | `opal-data-transcripts` is SSE-KMS with the customer key `44a2284f-...` and **Bucket Keys ON**. A PutObject therefore also needs the KMS data-key permission. The key policy's `GatewayWritesTranscripts` allows `opal-gateway-role` `kms:GenerateDataKey` and `kms:Encrypt`, with `kms:ViaService = s3.us-east-1` and `kms:EncryptionContext:aws:s3:arn = arn:aws:s3:::opal-data-transcripts`. With Bucket Keys on, S3's encryption context IS the bucket ARN, so the condition holds. **An admitted call will not fail on KMS.** No KMS change is in, or needed by, this ask |
| writers N | 2: `intake.py place()` (its own role, unchanged) and this tool. Both build `deck_<sha16>.pptx`, so the same bytes give one key per UTC date. The cross-day duplicate is the ask's own stated residual |

## Condition of this half (a cross-fabric ordering, carried by this seat)

`ADVI_MARKET_UPDATE_S3_ROOT` and this `-var` are both `address()` output for table `market_update` at every deploy and plan.
dell1's LGIC_ENFORCE ruling on XB-d00e will make `address()` refuse unregistered tables after a census. **That census must
register `market_update` (as well as `fee_statement`) before the refusal ships**, or every gateway release and every
opal-gateway plan fails at its `address()` step. This seat adds `market_update` to its standing condition with dell1.

## Observation, not a condition

Bucket Keys being ON is load-bearing for the key policy's encryption-context condition. If anyone turns Bucket Keys off
on this bucket, the context becomes the object ARN, and every gateway put to the bucket would fail. That would break
loudly, not silently, but it is worth a line in the bucket's Terraform beside `bucket_key_enabled`.

-- 1.0.0_SA_CTO~Z
