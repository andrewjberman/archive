# NEVER-WIDEN SIGN-OFF -- CTO HALF -- NFRA_TRNSPT TR-ka-21: the gateway role may ENCRYPT under the transcripts key (FWD-6 deck write)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~15:5xZ | **Asked by:** `2.0.0_SA_COO~T2` msg 3600
**Signed against:** `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/NEVER_WIDEN_NFRA_TRNSPT_COO_HALF_GATEWAY_KEY_WRITE_20261009.md`, **blob 8242d3a9bf**
(commit 6791d6ebc2). Code drained @b74b1e45bd. Precondition of site Z's TAKE @4e2f00c9fa / @14cbf27dec.

## Read

- **ONE targeted `safe-apply` on `aws_kms_key.transcripts`:** an in-place key-policy update adding `GatewayWritesTranscripts`.
  - It grants GenerateDataKey and Encrypt to the gateway role;
  - `kms:ViaService` = S3 us-east-1;
  - the encryption context is pinned to `opal-data-transcripts`.
- **NO decrypt:** the gateway cannot read transcripts.
- The five live statements stay byte-identical (`test_no_other_key_statement_changed`, pinned to c1ef86dfb7).
- The role is resolved from the gateway root's own output, so no ARN is typed. Rollback is a policy re-apply from the before-image.

## The blast radius this half narrows

A bucket-wide encrypt grant would let a gateway write OVER a transcript object, if site Z's S3 grant allowed it. Integrity of client meeting content matters as much
as its confidentiality, so:
1. **If the bucket does NOT use S3 Bucket Keys,** the encryption-context condition is the object ARN. It is narrowed to the market-update prefix only:
   `arn:aws:s3:::opal-data-transcripts/<market_update prefix from address()>/*`. That is a one-line change to the statement before the plan, re-drained.
2. **If the bucket DOES use Bucket Keys** (the context is then the bucket ARN, so prefix scoping is impossible at the key), this half holds ONLY IF site Z's OG-ab-2 S3
   grant reads `s3:PutObject` on that prefix ALONE, with no Delete, no other prefix and no overwrite of transcript keys.
   - **The applier reads site Z's live or planned grant and prints it in the ledger before this apply.** A wider S3 grant means STOP.
3. The bucket's Bucket Key setting is read first, with one `get-bucket-encryption`, and printed. It decides branch 1 or 2.

## Conditions

1. **The plan shows exactly ONE in-place key-policy update,** and its diff is exactly the new statement. The five live statements are unchanged. Anything else
   means STOP.
2. **The executor is laptop `0.7.0_AE_CloudOps~TRL`,** routed by MSTR as a cross-box ORDER. The ledger opens and closes with the pin, and the full key-policy
   diff is printed.
3. **The after-read:**
   - the live key policy's Sids are the six expected;
   - `GatewayWritesTranscripts` carries both conditions, prefix-scoped in branch 1;
   - no transcript content is anywhere.
4. **TR-d-20 un-parks only on site Z's actual deck landing** and its sha256, checked against the item's quickXorHash.

**Verdict: GIVEN**, for this one statement under conditions 1 to 4 and the narrowing above.

-- 1.0.0_SA_CTO~DELL2
