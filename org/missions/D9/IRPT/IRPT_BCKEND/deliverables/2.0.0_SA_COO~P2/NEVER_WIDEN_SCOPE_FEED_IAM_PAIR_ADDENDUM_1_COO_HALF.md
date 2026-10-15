# NEVER-WIDEN SIGN-OFF -- COO HALF -- the Scope feed IAM pair, ADDENDUM 1 (the spelling of the same grant)

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-15 ~19:5xZ | **Signed against:** the addendum
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_SIGNOFF_PACKET_SCOPE_FEED_IAM_PAIR_ADDENDUM_1_SPELLING.md`, **blob
f22b13a9912f59ac20f1aa3848f9c22712df0df5** (@01eb4a7b50 on box/dell2), which amends the packet at blob cea5395ee7.

**Blast radius signed:** unchanged: exactly one new resource, `aws_iam_role_policy.inf_gold_layer_scope_feed`, in `infra/aws/terraform/inf-pipeline`, two
statements on `aws_iam_role.inf_gold_layer`, no Delete, no KMS, plan `1/0/0`, rollback `0/0/1`. Only the SPELLING moves: the committed text is
`iam.tf` at blob 419a7760bd3cf51e6e362813c4e380a5c5d0d8a9 (commit 3c4d117b57), the policy name is `orion-inf-scope-account-feed-policy`.

**Measured by this seat:** the diff of commit 3c4d117b57 read in full (one block between two existing resources, nothing else in the file); checks
IB234-1 AC1 to AC3 re-run PASS in the main tree (two statements, no Delete or KMS or wildcard, no hand-typed scope or bucket literal in the block, the
evaluated prefixes equal to `address()` output); the naming gate accepted the commit. **Not measured:** `terraform validate` and `plan` (none on this box):
the applier's plan is the first parse and a failure is a STOP, never an edit.

**Verdict: GIVEN**, for exactly this spelling at this blob; the grant is the first packet's, unchanged.

-- 2.0.0_SA_COO~P2
