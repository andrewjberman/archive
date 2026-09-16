# LGIC_ENFORCE fence on opal-data-49financial -- the sign-off packet (EN-f-1)

**Author:** `0.9.0_WK_LGIC_ENFORCE~1`, task order `LGIC_ENFORCE.TO-EN-f-1` (cell EN-f-1; PRD candidate E5, first
half; DEC-4). **What this packet asks for:** the never-widen sign-off (NEVER #1, gate G-E) of `1.0.0_SA_CTO` and
`2.0.0_SA_COO~G` on the act EN-f-2 performs: one `safe-apply` of `infra/aws/terraform/shared-infra/`.

**This cell applied nothing.** The live policy was read (`aws s3api get-bucket-policy`) and a read-only plan was
run (`plan -lock=false`, as `arn:aws:iam::313476888478:user/Andrew_Berman`).

| Carrier | Path |
|---|---|
| Ledger entry (the SIGNOFF lines go here) | `org/critical_paths/change_management/20260915T0334Z_lgic-enforce-fence-49financial_deploy_completion.md` |
| Ledger sentinel | `org/critical_paths/.open_deploys/lgic-enforce-fence-49financial.json` |
| Rollback: the prior policy, verbatim | `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/FENCE_PRIOR_POLICY.json` |
| The plan (`terraform show -json`) | `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/fence_plan.json` |
| The authored change | ledger leg L1's commit: `s3-49financial.tf`, `lgic-enforce-fence-probes.tf`, `exemptions.json`, `modules/opal_name/` |

## 1. The act's blast radius -- what the apply MAY touch

The plan printed `Plan: 6 to add, 1 to change, 0 to destroy`. Of 238 resource changes, 231 are no-op and 7 are not.

| # | Address | Action | Touches |
|---|---|---|---|
| 1 | `aws_s3_bucket_policy.opal_data_49financial` | update in place | the bucket policy of `opal-data-49financial`: the bucket ARN and every object key under it (`/*`) |
| 2 | `aws_iam_role.lgic_fence_probe["49f"]` | create | IAM role `mdpf-49f-fenceprobe-role` |
| 3 | `aws_iam_role.lgic_fence_probe["cot"]` | create | IAM role `mdpf-cot-fenceprobe-role` |
| 4 | `aws_iam_role.lgic_fence_probe["unscoped"]` | create | IAM role `mdpf-fenceprobe-role` |
| 5-7 | `aws_iam_role_policy.lgic_fence_probe_read[...]` | create | one inline policy per probe role: `s3:GetObject`, `s3:ListBucket` on `opal-data-49financial` and `/*` only |

The probe roles trust `arn:aws:iam::313476888478:root` (`sts:AssumeRole`), so an account principal can run the
probes. Nothing else moves: no other bucket, no other role, no object, no data.

**The policy, before** (live; equal to the plan's `before`, compared as parsed JSON):
Deny `s3:*` to `Principal: *` where `aws:PrincipalArn` is **ArnLike** one of four typed patterns: `role/cot-*`,
`role/inf-*`, `role/mdpf-*`, `role/opal-assets-mdpf-*`. Everyone else was not denied.

**The policy, after** (the plan's `after`): Deny `s3:*` to `Principal: *` where `aws:PrincipalArn` is
**ArnNotLike** every one of 17 values: 1 derived pattern plus 16 exemption ARNs. Neither list is typed in the
`.tf`.
- `arn:aws:iam::313476888478:role/*-49f-*` -- `module.opal_name.fence_patterns["49financial"]`, generated from the registry
- the 16 ARNs of `infra/logic/registry/exemptions.json` under `opal-data-49financial` (`module.opal_name.fence_exemption_arns`)

## 2. Every principal whose access changes, per key

The Deny covers the bucket ARN and every object key (`/*`) identically. So for each principal below, the change
is the same at every key of `opal-data-49financial`: ListBucket and bucket configuration, and every object under
every prefix. The partition is by (denied before?, denied after?). The census population is
`FENCE_WRITER_CENSUS.md` (EN-c-2): 16 principals of `opal-data-49financial`, 16 granted and 4 of them seen reading
in the window.

### 2a. Not denied before, not denied after: UNCHANGED (the 16 exempt principals)

Each has a row in `exemptions.json` with its reason and a `signoff_ref` naming the ledger entry above.
`fence_patterns("49financial")` matches none of them; the checker printed `16 of 16 COVERED` (F1-AC1).

| Principal | Kind | What it holds on this bucket (census grant) | Seen in window |
|---|---|---|---|
| `bd-exporter-ec2-role` | role | inline `advi-49f-chain-access`: GetObject/PutObject `gold/advi/*`, GetObject `_code` | read, 206 events |
| `opal-advi-stitch-landing-role` | role | inline `opal-advi-stitch-landing-scoped`: PutObject on three `gold/advi/reference/bd_legacy_*` landing prefixes | no |
| `partners-lambda-role` | role | inline: GetObject, ListBucket on `opal-data-*` (wildcard) | no |
| `opal-news-lambda-role` | role | AWS-managed AmazonS3ReadOnlyAccess (wildcard) | no |
| `opal-drift-producer-codebuild-role` | role | AWS-managed ReadOnlyAccess (wildcard); its own belt denies object reads on `opal-data-*/*` | read, 2 HeadBucket |
| `infrastructure-ops-lambda-role` | role | bucket enumeration (versioning, encryption, location, policy) on `*` | no |
| `infrastructure-snapshot-role` | role | ListAllMyBuckets, versioning, encryption on `*` | no |
| `opal-globgrph-derive-runner-task` | role | bucket policy, versioning, location, notification reads on `*` | no |
| `opal-globgrph-incremental-updater` | role | bucket policy, versioning, location on `*` | no |
| `security-sweep-dedicated-role` | role | bucket posture reads, ListBucket on `*` | no |
| `AWSServiceRoleForResourceExplorer` | service-linked role | AWS-managed: bucket location, ListBucket on `*` | no |
| `AWSServiceRoleForSupport` | service-linked role | AWS-managed: describe and get actions on `*` | no |
| `AWSServiceRoleForTrustedAdvisor` | service-linked role | AWS-managed: bucket ACL, policy and posture reads on `*` | no |
| `Andrew_Berman` | IAM user | AdministratorAccess (group) | read, 2 ListObjects |
| `Andrew_Berman_Console` | IAM user | AdministratorAccess (group) | read, 1 HeadBucket |
| `Opal_Terminal` | IAM user | AdministratorAccess (group) | no |

`bd-gold-layer-runner`, named by the template's comment (`s3-49financial.tf:74-77`), is not an IAM principal in the
census. The comment places it "under bd-exporter-profile", which is `bd-exporter-ec2-role`: exempt, above.

### 2b. Denied before, denied after: UNCHANGED

This is every role matching `role/cot-*`, `role/inf-*`, `role/mdpf-*` or `role/opal-assets-mdpf-*` whose name
does not also carry `-49f-` and which is not exempt. The census `belt_only` list names 13 roles with role-side
belts and no grant here, among them `cot-rebalancer-runner-role` and `opal-assets-mdpf-portal-publisher-role`.
Also here: the two new probes `mdpf-cot-fenceprobe-role` and `mdpf-fenceprobe-role`. Both are created by this
act and denied from birth, which is what their arms prove.

### 2c. Denied before, NOT denied after: WIDENS

This is a role matching an old pattern AND `role/*-49f-*` (for example `mdpf-49f-*`, `cot-49f-*`, `inf-49f-*`,
`opal-assets-mdpf-49f-*`), or an exempt principal matching an old pattern.
- **Existing principals: none.** No census principal matches `*-49f-*`, and none of the 16 exempt principals
  matches an old pattern.
- **Created by this act: `mdpf-49f-fenceprobe-role`.** Its only grant is its inline read (GetObject, ListBucket)
  on this bucket, and it is removed at ledger leg L4.
- **A FUTURE role carrying the scope slot `49f` is no longer denied by this bucket policy.** That is the fence's
  intent (DEC-4 i). It still needs an identity grant to reach anything.

### 2d. Not denied before, DENIED after: NARROWS

This is every principal not in 2a, not matching `*-49f-*`, and not in an old pattern. It includes every other
IAM role and IAM user in the account. Two further members:
- **The account root** (`arn:aws:iam::313476888478:root`). It is not in the list, so it loses object and bucket
  access. S3 still lets the root user delete or replace a bucket policy that denies it, and that is the last
  recovery route (section 3).
- **Any request whose context carries no `aws:PrincipalArn`.** Under a negated condition operator, a missing key
  evaluates true, so the Deny applies. That covers an AWS service principal acting as itself, and an anonymous
  request (already refused by the bucket's public access block).

**What the narrowing costs:** a principal here loses real access only if an identity policy allowed it before.
The census found 16 such principals, and all 16 are in 2a. A principal with no grant goes from implicit deny to
explicit deny, which is no effective change. **Its limit, stated:** the census takes writers from grants, because
writes to this bucket are not logged (`FENCE_WRITER_CENSUS.md` `unobserved_writes`). A principal whose access
comes from a grant the census did not see would lose access here. Section 4 branch B covers that.

## 3. The rollback, per touched resource

| Resource | Rollback | Who can run it after the apply |
|---|---|---|
| bucket policy (every key) | Primary: revert the policy lines of the L1 commit and `safe-apply`. Emergency: `aws s3api put-bucket-policy --bucket opal-data-49financial --policy file://org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/FENCE_PRIOR_POLICY.json`, then land the revert so the next plan is 0-diff | Any 2a principal allowed to write bucket policies: the three administrator users. Last resort: the account root, which S3 always lets delete or replace a bucket policy |
| the 3 probe roles and 3 inline policies | Remove them: delete `lgic-enforce-fence-probes.tf` and `safe-apply` (ledger L4), or `aws iam delete-role-policy` then `delete-role` for each. They hold no data | Any IAM administrator; the bucket policy does not govern IAM |
| `exemptions.json` rows, module output | `git revert` of the L1 commit; nothing on the live plane reads them except through the policy | Any seat on the branch |

**The applying identity must be in 2a.** The plan ran as `user/Andrew_Berman`, which is exempt. If EN-f-2
applies as any identity outside the list, that identity loses read access to this bucket's policy the moment the
apply lands. Its next plan, and a Terraform rollback, then fail, and only an exempt principal or the root user
can recover.

## 4. Both branches

- **Branch A, the apply lands whole.** The fence is live, and the four probe arms run (ledger L3, `FENCE_PROBES.md`):
  - `mdpf-49f-fenceprobe-role` ALLOWED;
  - `mdpf-cot-fenceprobe-role` DENIED;
  - `mdpf-fenceprobe-role` DENIED;
  - an exempt principal ALLOWED.

  If an arm reads otherwise, the fence is wrong: roll back the policy (section 3) and keep the ledger OPEN.
  Then L4 removes the probes, and a re-plan must be 0-diff apart from that removal.
- **Branch B, an existing principal loses access after the apply** (an AccessDenied on a 2a principal, or on one
  the census missed). Roll back the policy from `FENCE_PRIOR_POLICY.json`, and add the principal's exemption row
  with its own sign-off before re-applying.
- **Branch C, the apply lands in part.**
  - If the policy is refused (for example `MalformedPolicy`) and the roles are created, the fence is unchanged.
    Remove the roles (L4); the ledger stays OPEN.
  - If the policy lands and a role fails, the fence is live without its proof. Either re-run the apply for the
    roles, or roll back the policy. It is never left live and unproven: NEVER #2 and this ledger's L3.
- **Branch D, the apply never runs** (a sign-off refused). Nothing live moves. Close the ledger SUPERSEDED or
  ABANDONED with its reason; the L1 commit reverts cleanly.

## 5. What is not claimed

- No principal was probed. A policy simulation was not used (DEC-4: it does not evaluate a resource policy).
  The probes are EN-f-2's.
- The partition above uses the census population and the plan. It is not a sweep of every IAM principal in the
  account. 2d is written as the complement, "everyone else", because the fence is deny-by-default.
- The SIGNOFF lines are the two seats' acts. This author wrote neither.
