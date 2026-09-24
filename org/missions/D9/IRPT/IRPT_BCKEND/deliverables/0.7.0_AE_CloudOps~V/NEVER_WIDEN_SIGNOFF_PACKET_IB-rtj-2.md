# NEVER-WIDEN SIGN-OFF PACKET -- IB-rtj-2: the L4 bounded test principal, created, exercised, destroyed

**For:** `1.0.0_SA_CTO` and `4.0.0_SA_CRO` (CTO ruling 99312 CALL 1: "two halves, CTO + CRO (the CloudOps~V
precedent)"). **Prepared by:** `0.7.0_AE_CloudOps~V`, 2026-09-22 ~00:5xZ. **Order:**
`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtj-2.the-l4-bounded-test-principal-created-exercised-destroyed.md`.
**Nothing is applied by this packet. STOP until both halves are at HEAD naming this file's blob.**

A half signs the blast radius and the rollback. This act's rollback IS its own last step (the destroy),
which is why the destroy and its verification are named here as part of the act.

---

## 1. THE PRINCIPAL, EXACTLY (Terraform root `infra/aws/terraform/investor-reporting/l4-fence-probe/`, its own state key)

**Role name:** `irpt-fence-probe-l4-role` = `lib/opal_naming.py name("irpt", None, "fence-probe", "role", "l4")`
(builder output, Rule 30; the builder refuses the scope tokens `inf`/`cot` inside a function or qualifier).
**Inline policy name:** `irpt-fence-probe-l4-policy` = `name("irpt", None, "fence-probe", "policy", "l4")`.
**max_session_duration:** 3600.

**Permission policy -- its ENTIRE grant (the saved plan's `after`, printed verbatim):**
```json
{"Statement": [{"Action": "s3:ListBucket", "Effect": "Allow", "Resource": ["arn:aws:s3:::opal-data-inflection", "arn:aws:s3:::opal-data-cottonwood", "arn:aws:s3:::opal-313476888478-lambda-artifacts"], "Sid": "ListBucketOnlyThreeBuckets"}], "Version": "2012-10-17"}
```
One action, three bucket ARNs, no object ARN, no wildcard, no attached managed policy. The two fenced bucket names
are READ FROM THE REGISTRY, not typed. The naming gate refused typed firm tokens twice, as bucket literals and then as
map keys (LGIC_ENFORCE DEC-6). The root now uses EXACTLY the selector `shared-infra/s3-lgic-firm-buckets.tf`
manages those buckets by: `infra/logic/registry/scopes.json` FIRM rows whose `bucket_managed_by ==
"s3-lgic-firm-buckets.tf"`. Evaluated today it yields `opal-data-inflection` and `opal-data-cottonwood`, and nothing
else (49financial and demo carry no such field). A `precondition` refuses the plan if that selector ever yields a
count other than 2, so a registry edit cannot silently widen the signed grant. The plan's rendered policy is
byte-identical to the JSON above.

**Trust policy (who may exercise it) -- exactly one principal, the operator user that runs the arms:**
```json
{"Statement": [{"Action": "sts:AssumeRole", "Effect": "Allow", "Principal": {"AWS": "arn:aws:iam::313476888478:user/Andrew_Berman"}, "Sid": "OperatorAssumeOnly"}], "Version": "2012-10-17"}
```

**Plan (read-only, taken 2026-09-22 ~00:5xZ from the committed files):** `Plan: 2 to add, 0 to change, 0 to destroy.`
-- `aws_iam_role.l4_fence_probe` create, `aws_iam_role_policy.l4_fence_probe_listbucket` create. Nothing else.
`terraform validate` clean, `fmt -check` clean. Pre-state: `iam get-role --role-name irpt-fence-probe-l4-role` ->
`NoSuchEntity` (does not exist today).

## 2. NON-EXEMPT, PROVEN AGAINST BOTH LIVE `ArnNotLike` LISTS (read fresh 2026-09-22 ~00:4xZ)

Both buckets carry ONE statement, `DenyForeignFirmPrincipals`: Deny `s3:*` on the bucket and `/*` unless
`aws:PrincipalArn` is `ArnNotLike`-excluded. The lists, verbatim:

| `arn:aws:iam::313476888478:role/irpt-fence-probe-l4-role` vs | opal-data-inflection | opal-data-cottonwood |
|---|---|---|
| `role/*-inf-*` (inflection) / `role/*-cot-*` (cottonwood) | no match | no match |
| `user/Andrew_Berman` | no match | no match |
| `user/Andrew_Berman_Console` | no match | no match |
| `user/Opal_Terminal` | no match | no match |

**0 of 4 entries match, on both buckets.** For an assumed-role session `aws:PrincipalArn` is the ROLE ARN, so the fence
applies to it. Matcher positive control: `role/irpt-inf-x-role` vs `role/*-inf-*` -> MATCH (the instrument can say yes).

**The control bucket, `opal-313476888478-lambda-artifacts`:** its whole bucket policy is one `Allow`
(`PortalCISurfaceCheckGet`: `user/github-actions-portal`, `s3:GetObject` on `surface-check/latest/*`). No Deny, no firm
fence. So the role's identity grant alone decides `ListBucket` there. That bucket holds Lambda code zips; a listing
reveals key names only.

## 3. THE SEQUENCE (every step printed into the result)

1. **Ledger** opened and committed BEFORE any apply (role name, both policies, and this destroy-and-verify sequence in it).
2. **Apply:** `terraform plan -out` (must be EXACTLY the 2 creates above) -> `.tools/safe-apply.sh apply <that planfile>`.
3. **Assume:** `sts assume-role` as `user/Andrew_Berman`; print the session's ARN.
4. **POSITIVE ARM:** `list-objects-v2` on the control under the role session -> must SUCCEED (wire result printed).
5. **NEGATIVE ARMS, 2 of 2:** `list-objects-v2` on `opal-data-inflection` and on `opal-data-cottonwood` under the SAME
   session -> both must be `AccessDenied`, each ATTRIBUTED by S3's own error context. S3 names the policy type in
   the message: `... with an explicit deny in a resource-based policy` (the fence) versus `... because no
   identity-based policy allows ...` (nothing grants it). CloudTrail is consulted if a data-event trail covers
   these buckets; otherwise the S3 error context is the attribution the face admits.
6. **ATTRIBUTION CONTROL (added here, needs your eye):** `list-objects-v2` under the same session on
   `opal-data-assets`, a bucket the role is NOT granted and whose policy does not deny `ListBucket`. Expected:
   `AccessDenied ... because no identity-based policy allows`. This shows the error context really distinguishes the
   two causes, so the arm-5 wording is evidence and not decoration. It is an attempt, not a grant; it reads and
   writes nothing.
7. **DESTROY:** `terraform plan -destroy -out` (must be EXACTLY the 2 deletions) -> `.tools/safe-apply.sh apply <that
   destroy planfile>`, in the SAME session.
8. **VERIFY:** `aws iam get-role --role-name irpt-fence-probe-l4-role` -> must return `NoSuchEntity`, printed verbatim.
9. **REMOVE THE DECLARATION:** delete the root's `.tf` files in the same session and commit. A destroyed resource
   whose declaration survives is recreated by the next apply (`safe-apply.sh`'s own tombstone note). Then close the ledger.

## 4. BLAST RADIUS, BOTH BRANCHES

- **What exists, and for how long:** one IAM role plus one inline policy, for the minutes between steps 2 and 7. It can
  be assumed only by `user/Andrew_Berman`, which already holds far broader access (the AdministratorAccessOpalCapital
  group), so no new person or service gains any capability. Its grant is `ListBucket` on 3 buckets. No served
  output, no bucket policy, no exemption list, no other principal is touched.
- **BRANCH EXPECTED (the fence holds):** arm 4 succeeds, arms 5 deny with the resource-based wording 2 of 2, arm 6
  denies with the identity-based wording. That discriminates the fence, and closes leg L4 of
  `org/critical_paths/change_management/20260918T1949Z_irpt-bckend-ib-rte-3-lgic-firm-buckets_deploy_completion.md`.
  That leg's owner is `2.0.0_SA_COO~B` (CTO 99312), and the substitute method is the one CALL 1 names.
- **BRANCH THE FENCE LEAKS (a fenced bucket LISTS for this role):** it is a FINDING, filed as a BLOCKING row. Both
  buckets hold 0 keys today, so the exposure is an empty listing. The role is destroyed in the same way;
  nothing is re-tried or widened.
- **BRANCH THE POSITIVE ARM FAILS:** the instrument, the assumption or the grant is broken. The negative arms are
  NOT read as meaningful; destroy, verify, file a row, and the order stays open.
- **Rollback of the whole act:** steps 7-9. If the apply fails part-way (role created, policy not), the same destroy
  plan removes whatever state holds, then `get-role` verifies. NEVER-2: nothing is left half-landed at session end.

## 5. WHAT THIS PACKET DOES NOT COVER

Any other principal; any bucket-policy or exemption edit (this cell reads the fence and never changes it); any grant
surviving the session.

## 6. WHAT THE HALVES SIGN AGAINST

This file's committed blob (named in the commit that lands it), the two policies above verbatim, and the role name
`irpt-fence-probe-l4-role`.
