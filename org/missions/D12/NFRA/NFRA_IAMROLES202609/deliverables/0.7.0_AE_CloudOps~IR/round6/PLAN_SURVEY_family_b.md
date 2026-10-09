# PLAN_SURVEY -- Family B (row 9, SmartX), NFRA_IAMROLES202609.TO-IAM-w-1 PHASE A

**Cell:** IAM-w-1 (round 6, outcome FWD-4; round-5 analysis item E1)
**Executed by:** `0.7.0_AE_CloudOps~IR` -- **owner of record:** `0.7.0_AE_CloudOps~Z` (ruling @fa8ec0e726)
**Authority:** `ROUND_ANALYSIS.round5.md` @f77e32d7c3 E1; `ADOPTION_PLAN_TEN.md` @59112aafed Family B
**Issuer:** `2.0.0_SA_COO~ZI` -- **risk:** WORLD -- **PHASE A applied NOTHING.**

**Measured:** 2026-10-09, worktree `/c/tmp/iam-w1`, branch `wk-iamroles-r6-w1` @`097d3bcc3e`,
Terraform v1.15.8 (resolved on PATH; site Z has no `.tools/terraform.exe`), provider
`hashicorp/aws v5.100.0`. Plan run `-input=false -lock=false`, read-only.

---

## 1. THE FOUR REQUIRED LINES

```
PLAN: infra/aws/terraform/smartx-pipeline: Plan: 1 to import, 0 to add, 4 to change, 0 to destroy.
DEFAULT_TAGS: infra/aws/terraform/smartx-pipeline: ['Environment', 'ManagedBy', 'Project', 'System']
AUTH_KEY_COLLISION: infra/aws/terraform/smartx-pipeline:   *** KEY COLLISION: ['Project', 'System'] are BOTH default_tags keys AND authorization keys.
STATE_KEY: infra/aws/terraform/smartx-pipeline: smartx-pipeline/tfstate
```

`STATE_KEY` reads `key = "smartx-pipeline/tfstate"` from the module's own `backend "s3"` block
(`main.tf`), bucket `opal-313476888478-terraform-state`, region `us-east-1`.
`AUTH_KEY_COLLISION` is `.tools/comp-tagauthz`'s line verbatim, including its leading spaces, from the
invocation `safe-apply` itself makes (section 4).

## 2. THE ROLE'S LIVE TAGS

`opal-smartx-lambda-role`: **ZERO tags.** `aws iam list-role-tags --role-name opal-smartx-lambda-role`
returned `{"Tags": []}`. The plan's `tags = {}` line agrees.

Other live values read at 2026-10-09 (`get-role`, `list-role-policies`,
`list-attached-role-policies`, `list-role-tags`), all carried into the declaration as-live:

| attribute | live value |
|---|---|
| path | `/` |
| description | `Lambda role for SmartX query functions` |
| max_session_duration | `3600` |
| assume_role_policy | `lambda.amazonaws.com` / `sts:AssumeRole` |
| inline policies | 3 -- `opal-smartx-logs`, `opal-smartx-s3-access`, `opal-smartx-secrets` |
| attached managed policies | 0 (`AttachedPolicies: []`) |
| tags | 0 |
| created | `2025-11-20T14:43:02Z` |
| RoleLastUsed | `2025-12-30T23:24:50Z`, `us-east-1` |

## 3. WHAT IS MINE AND WHAT IS NOT -- the negative control

**The plan line above is NOT all adoption.** A baseline plan of the same module with
`zz_adopt_family_b.tf` MOVED OUT and nothing else changed:

```
Plan: 0 to add, 3 to change, 0 to destroy.
```

So the delta attributable to this adoption is **exactly `1 to import` + 1 of the 4 `to change`**, and
**0 to add, 0 to destroy**. The remaining **3 to change plus all 3 output removals are PRE-EXISTING
MODULE DRIFT** and are not this cell's act. Both plans ran in the same worktree minutes apart against
the same state.

| plan item | in baseline? | attributable to IAM-w-1 |
|---|---|---|
| `aws_iam_role.opal_smartx_lambda_role` imported + `tags_all` updated | no | **YES** |
| `aws_lambda_function.assets_daily_pull` updated in-place | yes | no |
| `aws_lambda_function.jwt_refresher` updated in-place | yes | no |
| `aws_lambda_function.rest_pull` updated in-place | yes | no |
| 3 outputs -> null | yes | no |

**The one change that is mine, in full** -- the role's only non-import delta is `tags_all`:

```
      ~ tags_all              = {
          + "Environment" = "Production"
          + "ManagedBy"   = "Terraform"
          + "Project"     = "OpalPortal"
          + "System"      = "SmartXPipeline"
        }
```

Four keys ADDED to a role that carried none. Nothing is overwritten and `tags` stays `{}`.

**THE OMISSION RULE HELD, measured not assumed.** The plan enumerates the role's live policy
attachments as UNCHANGED: `inline_policy { name = "opal-smartx-logs" ... }` printed in full,
`# (3 unchanged blocks hidden)` for the rest, and `managed_policy_arns = []` unchanged. Omitting
`inline_policy` and `managed_policy_arns` left all three live inline policies alone. 0 detachments.

`grep -c -E '^[[:space:]]*(inline_policy|managed_policy_arns)'` on the `.tf.proposed` returns `0`
(criterion AC1's shape, against the `.tf` name once PHASE B lands it).

## 4. THE TAG-AUTHORIZATION READ -- a PASS over a denominator of ZERO, and why it is still sound

`.tools/comp-tagauthz check --default-tags-tree infra/aws/terraform/smartx-pipeline --from-plan <plan.json>`
exited **rc=0**, and the KEY COLLISION above is REAL: `Project` and `System` are both default_tags keys
in this module AND authorization keys in this account. But read its own scope line:

```
MODE: GATE. Scoped to 0 candidate resource(s) this tree would manage.
RESULT: none of the 0 candidate(s) carries a tag that ... default_tags ... would overwrite.
```

**That pass is over ZERO candidates, so by itself it says nothing about this role.** `safe-apply`'s gate
scopes to resources whose tags are authorization-bearing; no IAM role is one. Recording an rc=0 here
without its denominator would be the bare zero reading as "no problem exists".

**So the question was answered on a second instrument instead**, directly from
`aws iam get-account-authorization-details` (the same one call comp-tagauthz derives from; swept
298 roles / 78 local+attached policies / 9 users / 2 groups; account is not in an Organization, so no
SCPs apply -- stated, not implied):

1. **Zero `aws:PrincipalTag/*` conditions exist account-wide.** Tagging a role cannot act through a
   principal-tag condition because there are none.
2. The only two non-AWS-service tag conditions are both `ResourceTag`, and **neither reaches IAM
   roles** -- each is scoped to EC2 instances and SSM documents:
   - `managed:website-estate-admin` -- `ec2:StopInstances|StartInstances|RebootInstances` and
     `ssm:StartSession` on `arn:aws:ec2:us-east-1:313476888478:instance/*`,
     `StringEquals aws:ResourceTag/Project = "NFRA_WEBSITE"`.
   - `role:cot-bd-session-trigger-lambda-role/inline:cot-bd-session-trigger-policy` --
     `ec2:StartInstances` and `ssm:SendCommand` on `.../instance/*` and four SSM documents,
     `StringEquals aws:ResourceTag/System = "CottonwoodPipeline"`.
3. **The values do not match either**, independently of the resource type: this module writes
   `Project = OpalPortal` and `System = SmartXPipeline`; the conditions require `NFRA_WEBSITE` and
   `CottonwoodPipeline`.

**Conclusion, on two independent grounds: adding these four tags to `opal-smartx-lambda-role` can
neither widen nor narrow any authorization in this account.** The KEY COLLISION is a true statement
about the key NAMES and a false alarm for this particular resource.

> **Instrument disagreement, stated not reconciled.** comp-tagauthz reported `tag-conditioned
> statements found: 9 (4 ours, 5 AWS service-linked)`. My own sweep of the same API response found 7
> raw matches resolving to 4 distinct `(policy, condition-kind, key)` triples, 2 of them ours and 2
> AWS (`AmazonECSServiceRolePolicy`). The two counts differ because the scans dedupe and attribute
> differently; I did not re-derive the tool's 9. **comp-tagauthz's output is the gate's own and is the
> authoritative line in section 1.** The substantive finding -- which statements exist and what they
> are scoped to -- is quoted from the raw API response above and does not depend on either count.

## 5. BLOCKING FINDING FOR PHASE B -- an unscoped apply carries three Lambda code deploys

The cell binds PHASE B to "a plan that equals the survey's (N to import, 0 to add, 0 to destroy, plus
only the tag updates the pair names)". **An UNSCOPED `safe-apply` of this module does not meet that
bound today.** It would additionally:

- move `aws_lambda_function.assets_daily_pull` to `s3_object_version QNIiMQgfRzxG_KrI_6mVxJDjJbZFOnsd`
  (from `XmkW9C_XX1J_6sREU2VZ2naPbfmRQa7O`),
- move `aws_lambda_function.jwt_refresher` to `s3_object_version HAmOeAkTP0mT6304E9OvUVTpk_GhC8hh`
  (from `lRZrP4cIcsSbeYBd8SIB6_W8No75LiDw`),
- move `aws_lambda_function.rest_pull` to `s3_object_version g_1WqvOSlrPbM1uf8nFcy0uG9SB4xXwb` and
  `source_code_hash lM6cnuZTetkFwkGmxQqBFslExfqwGp+WhqFYOYM81xE=`,
- and drop three outputs to null (`autostart_lambda_arn`, `autostart_role_arn`,
  `eventbridge_rule_arn`).

**Three Lambda code deploys riding on an IAM custody move is a permission-free act dragging a code
change behind it**, and it is outside this cell's BOUNDS ("NO PERMISSION MOVES ... the role's policies,
trust and usage are untouched"; C-TWO-REMEDIES) as well as untagged by any deploy-ledger entry of
mine. Filed as surprise row **`NFRA_IAMROLES202609-Z-S21`**, class BLOCKING, hazard ARMED,
`disarm_owner` `2.0.0_SA_COO~ZI`.

**What PHASE B needed from the never-widen pair:** either a `-target aws_iam_role.opal_smartx_lambda_role`
scoped apply (which `safe-apply` handles as a SCOPED apply and grades the scoped plan), or the drift
resolved by its owner first.

**RULED by the issuer** (`2.0.0_SA_COO~ZI`, amendment A2-r6 @`3293b97a90`): **PHASE B step 5 is now
`-target=` on the adopted `aws_iam_role` only**, and the three Lambda drifts are routed to the
smartx pipeline's owner. So the plan PHASE B must match is the SCOPED one, and this survey's
unscoped plan line stays the record of what an unscoped apply would have done. The scoped plan is
re-rendered and re-read at PHASE B against the live `deployed_commit`, never carried over from this
run. This seat still applies nothing until both never-widen halves are SIGNED.

## 6. STATE OF THE WRITE SURFACE AT THE END OF PHASE A

- `infra/aws/terraform/smartx-pipeline/zz_adopt_family_b.tf.proposed` -- committed, inert.
- `infra/aws/terraform/smartx-pipeline/zz_adopt_family_b.tf` -- **REMOVED.** The `.tf` copy existed
  only for the duration of the two plan runs and is not committed. The module's tracked `.tf` set is
  unchanged from `097d3bcc3e`.
- No deploy-ledger entry opened: `ls -a org/critical_paths/.open_deploys/ | grep -c iamroles-r6-family-b`
  read `0` before PHASE A and PHASE A opened none. PHASE B opens `iamroles-r6-family-b` first.
- Nothing applied. No tag, policy, trust relationship or Lambda touched.

**PHASE A ends here, per the order's step 3.**
