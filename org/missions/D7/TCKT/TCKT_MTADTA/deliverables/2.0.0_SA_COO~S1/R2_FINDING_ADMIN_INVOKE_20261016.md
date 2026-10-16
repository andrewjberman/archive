# TCKT_MTADTA round 2 -- finding: an IAM administrator can invoke the door, so neither "non-members are refused" nor the MFA gate binds one

**By:** 2.0.0_SA_COO~S1, 2026-10-16 ~08:5xZ, from reads taken after `0.7.0_AE_CloudOps~TM1` applied the `trino` root (measured, live, read-only).

## What was measured

1. `r2_check_r1.py applied` -> `R1-APPLIED-OK aliases=collector,member`: the root is applied.
2. `aws lambda invoke --function-name globgrph-trino-access-lambda --qualifier member --payload e30=` as `cloudops-dell1-agent-user` (an IAM user in no group)
   -> `StatusCode 200`; the door answered `{"ok": false, "error": "op is not served on this alias"}`. The same user invoked the `collector` alias, rc=0.
   **The invoke itself was not refused.** The door's own op gate answered, which is the only thing between that user and `get_day`.
3. `aws s3api get-object` on the cursor key as the same user -> `NoSuchKey` (the key does not exist yet), not `AccessDenied`.
   `iam simulate-principal-policy` for that user and action against the LIVE bucket policy -> `explicitDeny`. So the Deny is correct; the probe on a
   missing key does not discriminate. The probe needs an object that exists (the first clean fire writes the cursor).

## Why (the mechanism)

Same-account IAM: a principal is allowed if ANY of its identity policy or the resource's policy allows, unless something EXPLICITLY denies. The group policy grants
invoke to the group, and `aws_lambda_permission` grants it to the collector role, but neither is a Deny. `cloudops-dell1-agent-user` (and any administrator, and the
laptop agents' `Andrew_Berman`) already holds `lambda:InvokeFunction` through its own policy. So "only the group's members may invoke" is true of principals with
no other grant and false of every administrator. Likewise the CTO's MFA ruling on call 0017 (the group policy requires `aws:MultiFactorAuthPresent`) conditions
only the group's grant: an administrator's own policy has no such condition. S3 is different: the bucket policy carries an explicit Deny, so a direct read is refused
(simulated `explicitDeny`).

## What the door still enforces for an administrator who invokes it

On the `member` alias: `get_day` (any of the eight's day), `get_state`, `list_state`, `derive_silver`. On the `collector` alias: `put`, `derive_silver`, the cursor read. So an
administrator can read the eight's metadata through the `member` alias with no MFA. That is PRD C-RESIDUAL (2) in a wider form than it is written (it names only principals
that can EDIT the policies).

## Options (the CTO's to rule; the issuer does not take them)

(a) A Deny that binds administrators: a Lambda resource-policy statement `Effect: Deny, Principal: *` on each alias with `BoolIfExists aws:MultiFactorAuthPresent = false`,
with the collector role carved out of the `collector` alias's statement by `aws:PrincipalArn`. `aws lambda put-resource-policy` exists in the CLI; the Terraform provider's
`aws_lambda_permission` cannot express a Deny, so this is an AWS-CLI act or a different resource. Not verified live: nothing was written.
(b) Accept and state it: the residual list gains "every principal whose own policy allows invoking the door (all IAM administrators, the dell agent users, the laptop agents)",
and FWD-8's refusal criteria change to "a principal with no invoke grant of its own is refused", which the box identity cannot demonstrate because it holds one.
(c) A different door: a function URL with IAM auth does not change this; a separate AWS account (the later Organization project) does.

## What this changes in the orders

`TO-MD-r1` AC2 (`r2_check_r1.py refusals`) demands that the box identity's invoke of the `member` and `collector` aliases be refused; with the mechanism above it cannot be
under the built root. The GetObject probe there must run against an existing key. The issuer holds `TO-MD-r2` staged until the CTO rules.
