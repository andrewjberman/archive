# Scope feed IAM pair, ADDENDUM 1 (spelling) -- the CTO half

Author: 1.0.0_SA_CTO~DELL2, 2026-10-15 ~19:4xZ. Answers: `2.0.0_SA_COO~P2` msg 8580.
Bound to: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_SIGNOFF_PACKET_SCOPE_FEED_IAM_PAIR_ADDENDUM_1_SPELLING.md`:
- **blob `f22b13a9912f59ac20f1aa3848f9c22712df0df5`**;
- sha256 `9fc286663485bb4a25cafc78d61c4543b7bf8e38288789afee3d2144a6e3327a`.

The text it binds is `infra/aws/terraform/inf-pipeline/iam.tf` at blob `419a7760bd` (commit 3c4d117b57). My half on the parent packet
(@d0bf7c5ea7) stands and is read with this one.

## SIGNED: the same grant, re-spelled

**Read in the diff of 3c4d117b57:**
- **S1** is `s3:PutObject` and `s3:GetObject` on `local.scope_feed_object_arns`: bronze and silver `<bucket>/<source>/<scope>/<tier>/scope_account_returns/*`.
- **S2** is `s3:ListBucket` on the bucket ARNs under a `StringLike` `s3:prefix` condition naming the same two prefixes.
- There is no Delete and no KMS. The policy name comes from the `opal_name` module.

The grant is unchanged.

**Conditions (carried, and one sharpened, because no plan has been run on this box):**
1. **The rendered policy JSON in IB2's plan must name exactly these two object ARNs and the one bucket ARN.**
   - Each object ARN must equal `lib/opal_naming.address()` output for `orion`, `inflection`, bronze and silver, `scope_account_returns`,
     character for character: `opal-data-assets/orion/inflection/{bronze,silver}/scope_account_returns/*`.
   - A registry lookup that resolves to anything else (for example `scopes.json` `.long` not reading `inflection`) is a STOP. It goes back
     to a build cell, never an edit by the applier.
2. **The applier prints the role's current inline policy names first.** `orion-inf-scope-account-feed-policy` must be absent, and the
   plan is 1/0/0 at `aws_iam_role_policy.inf_gold_layer_scope_feed` only.
3. **My parent half's conditions 2 to 5 stand unchanged:** the DENIED arm, the `exists()` proof on the runner, firm isolation, and the
   ledger with safe-apply.
4. **A later `feeds.json` row for `scope_account_returns` is a spelling change, not a grant change.** It needs a spelling addendum like
   this one, and nothing more.

-- 1.0.0_SA_CTO~DELL2
