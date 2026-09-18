# EN-w-7-r3 result -- R-20's four legacy writers dispositioned

**Cell:** `EN-w-7`, round 3 (DEC-4(ii); R-20/R-25). **Author:** `0.9.0_WK_LGIC_ENFORCE~2`, worktree
`wk-lgic-enforce-3-2`. **Commit:** `ea5edd1fe4` (the disposition file, the exemptions.json row, the
three regenerated `opal_name` module files, and surprise row LGIC_ENFORCE-W2-S12).

## What landed

`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~2/FENCE_WRITER_DISPOSITION.r3.json`
carries one row per R-20 legacy writer:

| role | bucket | disposition |
|---|---|---|
| `irpt-core-firm-49financial` | `opal-data-49financial` | `NOT_A_PRINCIPAL` |
| `irpt-core-firm-inflection` | `opal-data-inf` | `NOT_A_PRINCIPAL` |
| `irpt-core-firm-cottonwood` | `opal-data-cot` | `NOT_A_PRINCIPAL` |
| `demo-transform-runner-ec2-role` | `opal-data-demo` | `EXEMPTED` |

### The three `NOT_A_PRINCIPAL` rows

Each `irpt-core-firm-<id>` role is an IRPT_BCKEND B5 execution-role STUB (`infra/aws/terraform/
investor-reporting/core/roles.tf`), live since 2026-09-10T23:53:54Z. Its ONE attached policy
(`irpt-core-firm-<id>-prefix`, `iam_firm_conditions.tf:26-45`) grants `s3:GetObject`/`PutObject`/
`ListBucket` **only** on `aws_s3_bucket.ycharts` (`firms/<id>/*`) -- a bucket that is not any
`opal-data-*` bucket. No inline policy exists on any of the three (`iam list-role-policies`:
`PolicyNames []`).

CloudTrail evidence, per role: `lookup-events --lookup-attributes AttributeKey=ResourceName
AttributeValue=<role>`, window `2026-09-01T00:00:00Z` to `2026-09-17T23:59:59Z`: **2 of 2** events
total, both `CreateRole`/`AttachRolePolicy` by `Andrew_Berman` at role-mint time -- **0 `AssumeRole`
events**. The role's trust policy (Lambda service assume only) has never been exercised, so no
session under this identity has ever existed to make an S3 call. `aws lambda list-functions
--query "Functions[?contains(Role,'irpt-core-firm')]"`: 0 of N functions reference any of the
three, confirming no compute currently assumes them either.

### The one `EXEMPTED` row

`demo-transform-runner-ec2-role` is NOT a NOT_A_PRINCIPAL candidate: `shared-infra/
demo-transform.tf:99-136` grants it `s3:GetObject`/`PutObject` on `opal-data-demo/platinum/*`
(Sid `ReadWriteDestPlatinumDemo`) plus scoped `DeleteObject`/`ListBucket` -- it is the ADVI_DEMOV1
one-shot demo-bucket populator, reading `opal-data-bd/platinum/**` and writing the pseudonymized
clone to `opal-data-demo/platinum/**`. Added to `infra/logic/registry/exemptions.json
[opal-data-demo]` with this reason. No apply and no never-widen sign-off: `opal-data-demo` carries
no applied fence (round 1 EN-f-2 applied the generated Deny only on `opal-data-49financial`).

**No BLOCKING row is filed for the one-stop sign-off**: no `EXEMPTED` row landed under
`opal-data-49financial` this round, so the never-widen precondition in the order never triggers.

## Acceptance

- **W7R3-AC1** (`w7-writers-dispositioned`): `PASS-W7-WRITERS-DISPOSITIONED` -- 4 of 4 legacy
  writers confirmed against the artifact (exemptions.json presence for the EXEMPTED row; the
  three NOT_A_PRINCIPAL rows' evidence >= 40 chars).
- **W7R3-AC2** (`regress-w7-applied-deny`): `PASS-W7R-APPLIED-DENY-EQUALS-BUILDER` -- live
  `ArnNotLike` 17 entries == builder 17 entries (1 pattern + 16 exemptions), unchanged from the
  cut, because this round added no `opal-data-49financial` exemption.
- **W7R3-AC3**: judgment, for `3.0.0_SA_CVO` at L9. `UNVERIFIABLE-BY-INSTRUMENT` here.

## Surprise row

`LGIC_ENFORCE-W2-S12` (OBSERVATION, ARMED, `disarm_owner` `0.7.0_AE_CloudOps`): `opal-data-demo`
carries no CloudTrail data-event selector at all -- neither the org trail's `ReadOnly` list
(`cloudtrail-organization-trail.tf:46-51`, four buckets, `-demo` absent) nor the served-key
write-trail's `WriteOnly` list (`item2e_served_write_trail.tf:30`, three buckets, `-demo` absent).
The order's prescribed `NOT_A_PRINCIPAL` evidence path (CloudTrail data events) can therefore
never answer true or false for that bucket. It did not block this cell (`demo-transform-runner-
ec2-role` resolved `EXEMPTED` from a direct IAM-grant read, never from CloudTrail) but would block
a future `NOT_A_PRINCIPAL` claim on `opal-data-demo`.

## Not claimed

- No CloudTrail data-event count is offered as evidence for `demo-transform-runner-ec2-role` on
  `opal-data-demo`: none exists to read (see the surprise row above), and none was needed since
  its disposition is `EXEMPTED`, not `NOT_A_PRINCIPAL`.
- No apply, no rename, no edit to `systems.json`/`scopes.json`/`tiers.json`/`resources.json`.
