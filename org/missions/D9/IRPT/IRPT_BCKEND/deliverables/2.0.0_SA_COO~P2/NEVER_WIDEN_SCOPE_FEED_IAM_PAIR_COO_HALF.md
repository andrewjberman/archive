# NEVER-WIDEN SIGN-OFF -- COO HALF -- the Scope account feed's IAM pair (put on two prefixes of opal-data-assets)

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-15 ~19:0xZ | **Signed against:** packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_SIGNOFF_PACKET_SCOPE_FEED_IAM_PAIR.md`, **blob
cea5395ee74000806a28ab8eca32156e0af94639** (@95d8c864dd on box/dell2).

**Blast radius signed:** exactly one new resource, `aws_iam_role_policy.inf_gold_layer_scope_feed`, in the root
`infra/aws/terraform/inf-pipeline`. Two statements on `aws_iam_role.inf_gold_layer` and nothing else: S1 `s3:PutObject` and
`s3:GetObject` on `opal-data-assets/orion/inflection/{bronze,silver}/scope_account_returns/*`; S2 `s3:ListBucket` on the bucket under an
`s3:prefix` condition naming the same two prefixes. No Delete, no KMS. The plan is `1/0/0`; the rollback is the same resource removed
(`0/0/1`).

**Measured by this seat:** the feed's write path (`write_day`: an existence read, then a put; never an overwrite or a delete); the
bucket encryption is AES256; the bucket policy's only Deny (`DenyParquetUnderBronze17a`) does not match the feed's keys; the two
prefixes are `address()` output, printed in the packet.

**Branch A** grants nothing reachable until IB-pr-596 runs, and only on the two feed prefixes. **Branch B** is today's fail-closed
state. A refusal after the apply is a STOP and a row, never a widening.

**Verdict: GIVEN**, for exactly this resource and these two statements at this blob.

-- 2.0.0_SA_COO~P2
