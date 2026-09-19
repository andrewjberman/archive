# IB-rtf-7 result: step 4 attempted with every credential this seat holds, 1 identity, 2 of 2 denied

**Order:** `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtf-7.step-4-attempted-by-every-credential-the-seat-holds.md` @4ee8426c72
**Seat:** `0.7.0_AE_CloudOps~V`, worktree `/c/tmp/wk-irpt-6-ae1`, branch `wk-irpt_bckend-6-ae1`
**Authority:** Andrew-direct 2026-09-19 ~06:3xZ (record `org/tier1_exec/2.0.0_SA_COO~B/deliverables/ANDREW_DIRECT_20260919_063xZ_STEP4_BUCKET_POLICY_AE_ATTEMPT_THEN_PROCEED.md` @e4126c5e57)
**Command set:** fixed by the issuer's nudge (2.0.0_SA_COO~B, this session): `sts get-caller-identity`, then `s3api delete-bucket-policy` per bucket. A `get-bucket-policy` read-back runs only after a delete succeeds, and none did.

## R64-AC1: FAIL by output

The run that decides it is `battery_ib_rtf_7.py` at 2026-09-19T08:01:41Z, worktree HEAD af4902cc98. It ran under ledger entry `irpt-bckend-ib-rtf-7-step4-bucket-policy`, which was opened at 08:00:09Z with its sentinel committed @af4902cc98 before the attempt, and closed at 08:02:22Z.

| identity (N = 1) | bucket | rc | response, verbatim |
|---|---|---|---|
| `arn:aws:iam::313476888478:user/Andrew_Berman` | `opal-data-inflection` | 255 | `An error occurred (AccessDenied) when calling the DeleteBucketPolicy operation: User: arn:aws:iam::313476888478:user/Andrew_Berman is not authorized to perform: s3:DeleteBucketPolicy on resource: "arn:aws:s3:::opal-data-inflection" with an explicit deny in a resource-based policy` |
| `arn:aws:iam::313476888478:user/Andrew_Berman` | `opal-data-cottonwood` | 255 | `An error occurred (AccessDenied) when calling the DeleteBucketPolicy operation: User: arn:aws:iam::313476888478:user/Andrew_Berman is not authorized to perform: s3:DeleteBucketPolicy on resource: "arn:aws:s3:::opal-data-cottonwood" with an explicit deny in a resource-based policy` |

- Attempts: 2 of 2 (2N, N = 1). Succeeded: 0 of 2. AccessDenied: 2 of 2. Other failures: 0 of 2.
- NoSuchBucketPolicy: 0 of 2. No read-back was taken because no delete succeeded.
- Nothing changed on either bucket, and nothing else was attempted on either one.

**Carry line, verbatim:** *"step 4 -- Andrew at the console when next present; 1 identities tried, 2 of 2 denied"*

IB-rtf-5 stays staged behind step 4. Under Andrew's word ("if they cant for whatever reason, proceed and note it for later"), the round proceeds.

## R64-AC2: JUDGMENT, recorded for 3.0.0_SA_CVO and not self-graded

**What the live fence structurally admits.** The fence's source is `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf:142-171 @4ee8426c72`. It holds one statement: `Effect: Deny`, `Principal: "*"`, `Action: "s3:*"` on the bucket and its objects, with the condition `ArnNotLike aws:PrincipalArn = concat(fence_patterns[firm], fence_exemption_arns[bucket])` (`:158-164 @4ee8426c72`).

- A request is exempt from the Deny only when its principal ARN matches the firm's role pattern or an exemption ARN. At the 2026-09-18 apply the exemption list was empty (rows W3-S43/S45), so the only principals the live policy admits are those matching the firm's role pattern.
- Every other IAM principal hits an explicit deny: IAM users, every other role, and administrator identities. In AWS evaluation an explicit deny overrides any Allow, so no identity-based policy can win against it.
- The denial text shows which layer refused. It says "with an explicit deny in a resource-based policy". A missing IAM grant would say "because no identity-based policy allows". So the attempts reached S3 and the bucket policy refused them.
- I did not read the live policy's bytes. `get-bucket-policy` is inside the same Deny and outside the nudge's command set, so the empty-exemption state is taken from rows W3-S43/S45, not re-measured here.

**Why root alone gets through.** The bucket-owning account's root user is not an IAM principal the policy can bind for policy management. S3 lets the owner account's root user get, put and delete a bucket policy even when that policy denies it, as a recovery path so a bucket can always be unlocked. `Principal: "*"` therefore reaches every IAM identity and never reaches the recovery path. Only the console, or root credentials, which no seat holds, can remove it. That is the carry to Andrew.

**Proposal for 1.0.0_SA_CTO / 4.0.0_SA_CRO (not built here): a break-glass exemption that exists from birth.** The lockout happened because the first apply attached a fence whose exemption set did not contain the principal doing the applying. Two possible shapes:

1. A **registry contract rule**: every fence's exemption set is non-empty from its first row and always contains one named Opal operator break-glass identity. That identity is never a firm principal, which keeps the cross-firm bound.
2. An **apply-time precondition**: the plan refuses a bucket policy whose `ArnNotLike` set does not match the applying caller's ARN (or its assumed-role source), so an apply cannot lock out its own applier.

Either removes the class. The second also covers a later edit that shrinks the set. Who owns the contract and the gate is for the CTO/CRO to decide.

**What the seat could not try, and why:**

- The account root user. No seat holds its credentials, and adding root to any list is excluded by Andrew's word.
- Any role assumption that needs a new grant. That is out of scope under the face's bounds.
- Other local profiles. The box has exactly one, `[default]`. That count comes from the section-header lines of `~/.aws/config` and `~/.aws/credentials`, read before the issuer's nudge; no values were printed. `aws configure list-profiles` does not exist on this box's CLI v1.44.44 (row IRPT_BCKEND-S84).
- Credentials held on other devices or fabrics. This seat does not hold them.
- The console. Andrew is remote.

## Rows filed

- `IRPT_BCKEND-S83`: OBSERVATION, INERT. The face's `A-S<k>` id form is refused by the gate and the schema, so the rows use the seat form.
- `IRPT_BCKEND-S84`: OBSERVATION, INERT. `configure list-profiles` is absent on CLI v1, and the nudge's N = 1 identity set is recorded, along with what was read before the nudge.
- `IRPT_BCKEND-S85`: OBSERVATION, INERT. The ledger tool has no NO-CHANGE close status, so NO-CHANGE is carried in each leg's proof.
