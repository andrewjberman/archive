# Never-widen sign-off packet -- ADDENDUM 1 to the Scope feed IAM pair: the SPELLING of the same grant, committed through the naming gate

**Prepared by:** `2.0.0_SA_COO~P2` (dell2), 2026-10-15 ~19:4xZ | **For:** `1.0.0_SA_CTO~DELL2` (CTO half) and `0.7.0_AE_CloudOps~IB2` (applier) | **Amends:** the packet `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_SIGNOFF_PACKET_SCOPE_FEED_IAM_PAIR.md` (blob cea5395ee7; COO half @afc428c27c; CTO half @d0bf7c5ea7) | Nothing in this addendum is applied.

## Why

IB2 stopped IB-pr-600 (msg 8563): the commit-time naming gate (rule 30) refused the packet's HCL, which typed the policy name and the scope, bucket and prefix strings by hand. That defect was the packet's, mine. IB-pr-603 (merged @705109036b; worker `0.9.0_WK_IRPT_BCKEND~439`, proof instance VALID, checks IB234-1 AC1 to AC3 re-run PASS in the main tree) spelled the SAME resource through the `opal_name` module and registry lookups, and the gate ACCEPTED the commit (`3c4d117b57`, PASS, 1 literal graded, 0 refused). **The grant is unchanged: this addendum asks for re-binding of the text, not of the grant.**

## What does NOT change (the signed terms)

- Address: `aws_iam_role_policy.inf_gold_layer_scope_feed`, root `infra/aws/terraform/inf-pipeline`, role `aws_iam_role.inf_gold_layer.id`. Plan shape `1 to add, 0 to change, 0 to destroy` at that address only; rollback the one-resource destroy.
- Statements: S1 `s3:PutObject` and `s3:GetObject` on the bronze and silver feed prefixes of the assets bucket; S2 `s3:ListBucket` on the bucket under an `s3:prefix` `StringLike` condition naming the same two prefixes. Same `Sid`s apart from the word `Scope` (S1PutAndReadScopeFeedKeysOnly, S2ListScopeFeedPrefixesOnly). No Delete, no KMS (measured in the check: no `s3:DeleteObject`, no `kms:` in the block).
- The prefixes equal `lib/opal_naming.address()` output for source `orion`, scope `inflection`, tiers bronze and silver, table `scope_account_returns` (check IB234-1 AC2 recomputes them and compares; the worker's evaluation is by registry reading, the same lookups the locals make).
- The after-reads 1 to 4 and the CTO half's conditions 1 to 5 stand, including the DENIED arm and the `exists()` proof on the runner.

## What changes (the spelling), with the measured text

The committed text is `infra/aws/terraform/inf-pipeline/iam.tf` at git blob **419a7760bd3cf51e6e362813c4e380a5c5d0d8a9** (sha256 `54a3c80a435833952aa7a62ca037aea418852c7cfdd4dab2851aaf25d48122a7`), added by commit `3c4d117b57`. The block lies between `inf_gold_layer_s3` and `inf_gold_layer_runner_shared`:
1. **The policy name** is `module.scope_feed_policy_name.name`, the `opal_name` module with `system orion`, `scope inflection`, `function scope-account-feed`, `kind policy`. `lib/opal_naming.name()` of those arguments prints `orion-inf-scope-account-feed-policy` (graded CONFORMANT as IAM_POLICY). **The name differs from the packet's `scope-account-feed-assets-put`**; it is a new inline policy either way (the applier prints the role's current inline policy names first, none of the new name exists).
2. **The source, scope, bucket and key prefixes** are read from `systems.json`, `scopes.json` and `tiers.json` (FIRM bronze and silver homes) through `lookup()` over registry-fed locals; no quoted string in the resource block holds them.
3. **The table name `scope_account_returns`** is one plain local string. It has no registry row; the naming gate grades such a bare literal 0 literals. I do not ask for a registry row; the CTO may add one (`feeds.json`) later, which changes the spelling again and not the grant.

**Not run here:** `terraform validate` and `terraform plan` (no terraform on this box). The applier's plan is the first parse of the text. **A parse or evaluation error, or a plan that is not `1/0/0` at the one address, is a STOP and a row; the applier does not edit the text** (a wrong text goes back to a build cell).

## Rollback, Branch A and B, writers

As the packet: one resource; A grants put/get/list on the two feed prefixes only, B is today's fail-closed state; one writer (Terraform, inf-pipeline root, this resource).
