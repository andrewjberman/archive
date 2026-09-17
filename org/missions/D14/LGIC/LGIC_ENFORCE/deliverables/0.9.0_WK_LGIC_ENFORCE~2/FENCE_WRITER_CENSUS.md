# FENCE_WRITER_CENSUS -- who can read or write each firm bucket, and who was seen doing it

**Cell:** `EN-c-2`, LGIC_ENFORCE round 1 (PRD candidate E1, second half; DEC-4 condition (ii)). **Order:**
`task-orders/LGIC_ENFORCE.TO-EN-c-2.fence-writer-census.md`, issued by `2.0.0_SA_COO~G`. **Author:**
`0.9.0_WK_LGIC_ENFORCE~2`, worktree `wk-lgic-enforce-1-2` cut from CLOUD @fd9c9ca174. **PRD:** `prd/LGIC_ENFORCE_PRD.md`
v1.1 @78128f29ea. **Decomposition:** v1.1 @53d221f334, s.0 and s.3a.1.

Nothing live moved. Every AWS read below was read-only, through the `aws` shim.

## 1. The window

- **From `2026-09-14T02:33:09Z`.** That is the commit time of @231cd62ec5 (`2026-09-13T22:33:09-04:00`), which validated
  read logging on the four buckets.
- **To `2026-09-14T20:00:52Z`.** That is the moment the log download began.
- The org trail's newest event in the window is `19:55:00Z`, and CloudTrail delivers log files some minutes after the
  event. So the last minutes before the end may be under-read.
- The first data event on the four buckets inside the window is at `03:02:35Z`. There were 61 further data events on
  2026-09-14 before the window opened; they are not counted.

## 2. What was read, with denominators

| Source | Instrument | Denominator |
|---|---|---|
| Identity policies | `aws iam get-account-authorization-details` (all roles, users and groups, with inline and attached managed policy documents) | 250 roles, 7 users, 1 group, 56 managed policies. `list-roles` (250) and `list-users` (7) agree, and 48 of 48 attached managed-policy ARNs resolve in the dump |
| Bucket policies | `aws s3api get-bucket-policy`, one call per bucket | 4 of 4 buckets |
| Readers | `opal-organization-trail`'s log files, `s3://opal-cloudtrail-logs-313476888478/AWSLogs/313476888478/CloudTrail/us-east-1/2026/09/14/` | 2169 files, 208,398 records, 146,273 S3 data events on the four buckets in the window, 0 of them writes |
| Writers on `platinum/firm/` | `opal-served-key-write-trail`'s log files, `s3://opal-served-key-write-trail-logs/AWSLogs/313476888478/CloudTrail/us-east-1/2026/09/14/` | 112 files, 2333 records, 2333 WriteOnly data events on `platinum/firm/` in the window |
| Terraform source per role | `comp-iam roles` (its `source:` line) | 209 Terraform roles |
| Per-role grant lookup | `comp-iam role <name>`, once per role a grant or belt names | 94 roles, 0 resolved: row `LGIC_ENFORCE-W2-S1` |
| Scope tokens | `org/standards/NAMING_SCHEMA.json` v1.6 | resource grammar `:54-57`, `firm_forms` `:111-116`, `refused_tokens` `:118-121` |

Live selectors, read at the same time:

- **`opal-organization-trail`.** A `ReadOnly` data selector on exactly the four buckets. This matches
  `shared-infra/cloudtrail-organization-trail.tf:46-51` and `:73`.
- **`opal-served-key-write-trail`.** `readOnly=false`, with ARN prefixes on `platinum/firm/` of `opal-data-inf`, `-bd`
  and `-cot` only.

Both trails report `IsLogging: true`. The buckets are all in `us-east-1`, so their data events land in that region's folder.

## 3. What is NOT observed

**Writes outside `platinum/firm/` are not observed.**

- The org trail logs the four buckets' data events `ReadOnly` (`infra/aws/terraform/shared-infra/cloudtrail-organization-trail.tf:73`).
  Its 146,273 in-window data events contain 0 writes. That is the negative control: a write in that set would have
  falsified the reading.
- The only write logging is the served-key trail. It selects `platinum/firm/` on three buckets, and not on
  `opal-data-49financial`. So **no write at all to `opal-data-49financial` is observed**, inside `platinum/firm/` or
  outside it (row `LGIC_ENFORCE-W2-S3`).

**So the writer population is taken from GRANTS** (decomposition s.0, gate G-W). SEEN adds the readers the org trail
records, and the `platinum/firm/` writers the served trail records.

## 4. How each list was built

### GRANTED

Every IAM role or user is included whose inline policies, attached managed policies or group policies carry an **Allow**
statement that meets both of these:

- **Action.** It covers any `s3:` action (or `*`, or a `NotAction` that does not exclude `s3:*`).
- **Resource.** It matches the bucket ARN or an object ARN in it (or a `NotResource` that does not exclude it).

Each row carries the following fields:

- **`grant`.** Every matching statement, as `<inline | managed | AWS-managed> policy <name> stmt[<index>] Sid=<sid>:
  Allow <actions> on <resources>`.
- **`grant_match`.** `literal` when some statement names the bucket, `wildcard` when only a pattern (`*`,
  `arn:aws:s3:::*`, ...) reaches it.
- **`tf_source`.** The role's `.tf` file, from the `comp-iam roles` listing.
- **`comp_iam`.** The `comp-iam role` result.
- **`belts`.** Any Deny statement the same principal carries on the bucket.

The bucket policies add their Allow principals:

- **On `opal-data-bd`, `-inf` and `-cot`:** the CloudFront Origin Access Identity `E139998VWH0PD`
  (`AllowScopedAdvisorOAI`, `s3:GetObject` on the whole bucket), and the service principal `cloudfront.amazonaws.com`
  (`s3:GetObject` on `gold/*`, conditioned on distribution `EVTSA9VEHNZVH`).
- **On `opal-data-49financial`:** none. Its policy's one statement is `DenyForeignFirmPrincipals`, a Deny to
  Principal `*`, and it is recorded under `bucket_policy_deny`.

A wildcard grant still grants. The same 14 principals are granted on all four buckets, and hold only wildcard grants
there, except that on `opal-data-inf` the three users also hold literal ones:

- **AWS service-linked roles:** `AWSServiceRoleForResourceExplorer`, `AWSServiceRoleForSupport`,
  `AWSServiceRoleForTrustedAdvisor`.
- **Human users:** `Andrew_Berman`, `Andrew_Berman_Console`, `Opal_Terminal`. On `opal-data-inf` these three are also
  literal.
- **Platform roles:** `infrastructure-ops-lambda-role`, `infrastructure-snapshot-role`,
  `opal-drift-producer-codebuild-role`, `opal-globgrph-derive-runner-task`, `opal-globgrph-incremental-updater`,
  `opal-news-lambda-role`, `partners-lambda-role`, `security-sweep-dedicated-role`.

### The role-side belts

In this estate's Terraform, a belt is a role-side **explicit Deny**, for example `inf-pipeline/cross-firm-deny.tf:1-28`
and `bd-pipeline/bd-silver-merge.tf:13`.

- A granted principal that also carries one lists it in its `belts` field.
- A principal whose only statement on the bucket is a Deny is recorded under `belt_only`, with its Deny, its `.tf`
  source and its token. It is **not** put under `granted`, because the issuer's `_writers_49` (`check_en.py:535-537`)
  reads every granted row as a writer (row `LGIC_ENFORCE-W2-S4`).

### SEEN

- **Readers.** Every principal in the org trail's S3 data events on the bucket, from the window start on, named by
  `userIdentity`. An assumed role is named by its session issuer's role name; a user by its user name.
- **Writers.** Every principal in the served trail's WriteOnly events on `<bucket>/platinum/firm/`.
- **Evidence.** Each row gives the first and last event in the window (event name, time, request id) and the count
  per event name.
- **The one reader with no identity grant is the CloudFront OAI.** It is recorded as `userIdentity` type `AWSAccount`,
  principalId `AIDAJ3ELLOIDNV4A5IWRG`, accountId `CloudFront`. It reads `opal-data-bd`, `-inf` and `-cot` (`GetObject`)
  and is named here by its OAI principal ARN.
- **Cross-check.** After that mapping, every seen principal is also a granted principal (column "seen not in granted"
  below).

### Tokens

`token` is the firm scope token read from the name by the resource grammar
`{system}-{scope}-{function}[-{qualifier}]-{last}` (`NAMING_SCHEMA.json:54`), splitting on `-` and matching whole
segments only (so `info` is not `inf`). `token_basis` states where it was read. The rules:

- **A firm short form in slot 2 (the scope slot)** gives that token: `49f`, `inf`, `cot` or `demo`.
- **A long form or the refused alias `bd` in slot 2** gives the canonical short form, recorded as `grade.ALIAS`.
- **A firm token in slot 1 (the system slot)** fails the grammar: "a firm in the system slot" is OUT-OF-PATTERN
  (`:133`). The token is `none`, and the basis names the firm token and its slot.
- **A firm token in any other slot** also gives `none`, with the slot named.
- **IAM users** are `none`: `IAM_USER` is NOT GRADED (`:94`).
- **The OAI and the service principal** are `none`: they are AWS-issued identifiers outside the grammar (`:141`).
- **A name that is not kebab-case** (the AWS service-linked roles) is `none`.

So `none` does not mean "no firm". Most firm pipeline roles put the firm first (`inf-gold-layer-ec2-role`,
`bd-exporter-ec2-role`), and the grammar reads no scope from them. The basis keeps the firm token they do carry.

## 5. Findings the order did not ask for, each filed as one row

- **`LGIC_ENFORCE-W2-S1`.** `comp-iam role <name>` resolved 0 of the 94 roles, though `comp-iam roles` lists 79 of
  them. The grant lines therefore come from the live authorization dump.
- **`LGIC_ENFORCE-W2-S2`.** `bd-gold-layer-runner` (PRD `:206`) is not an IAM principal. It is EC2 instance
  `i-01003b035d2988dfb` (stopped), under instance profile `bd-exporter-profile`, which carries `bd-exporter-ec2-role`.
  That role is granted on `opal-data-49financial` by a literal grant, and is seen reading it.
- **`LGIC_ENFORCE-W2-S3`.** No write to `opal-data-49financial` is observed at all. `item2e_served_write_trail.tf:4`
  still reads "PROPOSED -- NOT YET APPLIED", while the trail is live.
- **`LGIC_ENFORCE-W2-S4`.** Belt-only principals and the 49financial bucket-policy Deny are recorded beside `granted`,
  not in it.

## 6. Summary by bucket (generated from the json block below)

| bucket | granted | of which literal | of which wildcard-only | of which bucket policy | belt_only | seen readers | seen platinum/firm/ writers | seen not in granted | granted tokens |
|---|---|---|---|---|---|---|---|---|---|
| opal-data-bd | 46 | 30 | 14 | 2 | 47 | 12 | 1 | 0 | 49f 2, none 44 |
| opal-data-inf | 51 | 38 | 11 | 2 | 18 | 31 | 1 | 0 | inf 2, none 49 |
| opal-data-cot | 30 | 14 | 14 | 2 | 47 | 10 | 1 | 0 | cot 2, none 28 |
| opal-data-49financial | 16 | 2 | 14 | 0 | 13 | 4 | 0 | 0 | none 16 |

## 7. The census

```json
{
 "window": {
  "start": "2026-09-14T02:33:09Z",
  "end": "2026-09-14T20:00:52Z"
 },
 "unobserved_writes": "Writes outside platinum/firm/ are not observed, because the org trail logs these four buckets' S3 data events ReadOnly (infra/aws/terraform/shared-infra/cloudtrail-organization-trail.tf:73) and the only write logging, opal-served-key-write-trail, is WriteOnly on platinum/firm/ of opal-data-bd, -inf and -cot alone (globgrph/item2e_served_write_trail.tf:30-31), so no write at all to opal-data-49financial is observed and the writer population is taken from grants.",
 "sources": {
  "grants": "aws iam get-account-authorization-details, read-only, 2026-09-14 ~19:57Z: 250 roles, 7 users, 1 group, 56 managed policies (list-roles 250 and list-users 7 agree; 48 of 48 attached managed policy ARNs resolved)",
  "bucket_policies": "aws s3api get-bucket-policy on each of the four buckets, read-only, 2026-09-14 ~19:55Z",
  "org_trail": "opal-organization-trail, s3://opal-cloudtrail-logs-313476888478/AWSLogs/313476888478/CloudTrail/us-east-1/2026/09/14/: 2169 files, 208398 records, 146273 S3 data events on the four buckets in the window, 0 of them writes",
  "served_write_trail": "opal-served-key-write-trail, s3://opal-served-key-write-trail-logs/AWSLogs/313476888478/CloudTrail/us-east-1/2026/09/14/: 112 files, 2333 records, 2333 WriteOnly data events on platinum/firm/ in the window",
  "comp_iam": "comp-iam role <name> for every role named by a grant or a belt (Terraform plane only)",
  "tokens": "org/standards/NAMING_SCHEMA.json v1.6 resource grammar (:54-57), firm_forms (:111-116), refused_tokens (:118-121)"
 },
 "buckets": {
  "opal-data-bd": {
   "granted": [
    {
     "principal": "AWSServiceRoleForResourceExplorer",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/aws-service-role/resource-explorer-2.amazonaws.com/AWSServiceRoleForResourceExplorer",
     "grant": "AWS-managed policy AWSResourceExplorerServiceRolePolicy stmt[3] Sid=ResourceInventoryAccess: Allow s3:GetBucketLocation,s3:ListAccessPoints,s3:ListAllMyBuckets,s3:ListBucket,s3:ListMultiRegionAccessPoints,s3:ListStorageLensConfigurations,s3:ListStorageLensGroups on * (wildcard) | AWS-managed policy AWSResourceExplorerServiceRolePolicy stmt[4] Sid=PermissionsForReadGetResources: Allow s3:GetAccelerateConfiguration,s3:GetAccessGrant,s3:GetAccessGrantsInstance,s3:GetAccessGrantsLocation,s3:GetAnalyticsConfiguration,s3:GetBucketAbac,s3:GetBucketAcl,s3:GetBucketCORS,s3:GetBucketLogging,s3:GetBucketMetadataTableConfiguration,s3:GetBucketNotification,s3:GetBucketObjectLockConfiguration,s3:GetBucketOwnershipControls,s3:GetBucketPolicy,s3:GetBucketPublicAccessBlock,s3:GetBucketTagging,s3:GetBucketVersioning,s3:GetBucketWebsite,s3:GetEncryptionConfiguration,s3:GetIntelligentTieringConfiguration,s3:GetInventoryConfiguration,s3:GetLifecycleConfiguration,s3:GetMetricsConfiguration,s3:GetReplicationConfiguration,s3:GetStorageLensGroup,s3:ListAccessGrants,s3:ListAccessGrantsInstances,s3:ListTagsForResource on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role AWSServiceRoleForResourceExplorer: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "none",
     "token_basis": "not kebab-case: the resource grammar does not hold, no firm token"
    },
    {
     "principal": "AWSServiceRoleForSupport",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/aws-service-role/support.amazonaws.com/AWSServiceRoleForSupport",
     "grant": "AWS-managed policy AWSSupportServiceRolePolicy stmt[4] Sid=AWSSupportActionsGroup3: Allow s3:describeJob,s3:describeMultiRegionAccessPointOperation,s3:getAccelerateConfiguration,s3:getAccessGrant,s3:getAccessGrantsInstance,s3:getAccessGrantsInstanceResourcePolicy,s3:getAccessGrantsLocation,s3:getAccessPoint,s3:getAccessPointConfigurationForObjectLambda,s3:getAccessPointForObjectLambda,s3:getAccessPointPolicy,s3:getAccessPointPolicyForObjectLambda,s3:getAccessPointPolicyStatus,s3:getAccessPointPolicyStatusForObjectLambda,s3:getAccountPublicAccessBlock,s3:getAnalyticsConfiguration,s3:getBucketAcl,s3:getBucketCORS,s3:getBucketLocation,s3:getBucketLogging,s3:getBucketNotification,s3:getBucketObjectLockConfiguration,s3:getBucketOwnershipControls,s3:getBucketPolicy,s3:getBucketPolicyStatus,s3:getBucketPublicAccessBlock,s3:getBucketRequestPayment,s3:getBucketVersioning,s3:getBucketWebsite,s3:getEncryptionConfiguration,s3:getIntelligentTieringConfiguration,s3:getInventoryConfiguration,s3:getLifecycleConfiguration,s3:getMetricsConfiguration,s3:getMultiRegionAccessPoint,s3:getMultiRegionAccessPointPolicy,s3:getMultiRegionAccessPointPolicyStatus,s3:getMultiRegionAccessPointRoutes,s3:getObjectAcl,s3:getObjectLegalHold,s3:getObjectRetention,s3:getReplicationConfiguration,s3:getStorageLensConfiguration,s3:listAccessGrants,s3:listAccessGrantsInstances,s3:listAccessGrantsLocations,s3:listAccessPoints,s3:listAccessPointsForObjectLambda,s3:listAllMyBuckets,s3:listBucket,s3:listBucketMultipartUploads,s3:listBucketVersions,s3:listJobs,s3:listMultipartUploadParts,s3:listMultiRegionAccessPoints,s3:listStorageLensConfigurations on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role AWSServiceRoleForSupport: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "none",
     "token_basis": "not kebab-case: the resource grammar does not hold, no firm token"
    },
    {
     "principal": "AWSServiceRoleForTrustedAdvisor",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/aws-service-role/trustedadvisor.amazonaws.com/AWSServiceRoleForTrustedAdvisor",
     "grant": "AWS-managed policy AWSTrustedAdvisorServiceRolePolicy stmt[0] Sid=TrustedAdvisorServiceRolePermissions: Allow s3:GetAccountPublicAccessBlock,s3:GetBucketAcl,s3:GetBucketPolicy,s3:GetBucketPolicyStatus,s3:GetBucketLocation,s3:GetBucketLogging,s3:GetBucketVersioning,s3:GetBucketPublicAccessBlock,s3:GetLifecycleConfiguration,s3:ListBucket,s3:ListAllMyBuckets on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role AWSServiceRoleForTrustedAdvisor: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "none",
     "token_basis": "not kebab-case: the resource grammar does not hold, no firm token"
    },
    {
     "principal": "bd-49f-fees-runner-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/bd-49f-fees-runner-role",
     "grant": "inline policy bd-49f-fees-runner-policy stmt[1] Sid=ReadBdCode: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/code/* (literal) | inline policy bd-49f-fees-runner-policy stmt[2] Sid=FeesBronzeSilverReadWrite: Allow s3:GetObject,s3:PutObject on arn:aws:s3:::opal-data-bd/bronze/fees/*,arn:aws:s3:::opal-data-bd/silver/fees/* (literal) | inline policy bd-49f-fees-runner-policy stmt[3] Sid=ListFeesPrefixes: Allow s3:ListBucket on arn:aws:s3:::opal-data-bd (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/bd-pipeline/bd-49f-interim.tf",
     "comp_iam": "comp-iam role bd-49f-fees-runner-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read; also carries '49f' in slot 2"
    },
    {
     "principal": "bd-49f-runner-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/bd-49f-runner-role",
     "grant": "inline policy bd-49f-runner-policy stmt[1] Sid=ReadBdBronzeCodeAndTemplates: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/code/bronze/* (literal) | inline policy bd-49f-runner-policy stmt[2] Sid=LandBdForwardfill: Allow s3:GetObject,s3:PutObject on arn:aws:s3:::opal-data-bd/forwardfill_v2/* (literal) | inline policy bd-49f-runner-policy stmt[3] Sid=EmitBdBronzeSentinel: Allow s3:PutObject on arn:aws:s3:::opal-data-bd/bronze/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/bd-pipeline/bd-49f-interim.tf",
     "comp_iam": "comp-iam role bd-49f-runner-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read; also carries '49f' in slot 2"
    },
    {
     "principal": "bd-49f-session-trigger-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/bd-49f-session-trigger-role",
     "grant": "inline policy bd-49f-session-trigger-policy stmt[5] Sid=ModeMarker: Allow s3:PutObject,s3:GetObject on arn:aws:s3:::opal-data-bd/blackdiamond/49f/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/bd-pipeline/bd-49f-session-chain.tf",
     "comp_iam": "comp-iam role bd-49f-session-trigger-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read; also carries '49f' in slot 2"
    },
    {
     "principal": "bd-allocation-checker-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/bd-allocation-checker-lambda-role",
     "grant": "inline policy bd-allocation-checker-permissions stmt[0] Sid=S3ReadAccess: Allow s3:GetObject,s3:HeadObject,s3:ListBucket on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/bd-pipeline/iam.tf",
     "comp_iam": "comp-iam role bd-allocation-checker-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "bd-allocation-processor-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/bd-allocation-processor-role",
     "grant": "inline policy s3-access stmt[0]: Allow s3:GetObject,s3:PutObject,s3:HeadObject,s3:ListBucket on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/bd-pipeline/iam.tf",
     "comp_iam": "comp-iam role bd-allocation-processor-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "bd-daily-trigger-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/bd-daily-trigger-lambda-role",
     "grant": "inline policy bd-s3-access stmt[0]: Allow s3:ListBucket,s3:GetObject,s3:PutObject on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/bd-pipeline/iam.tf",
     "comp_iam": "comp-iam role bd-daily-trigger-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "bd-exporter-ec2-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/bd-exporter-ec2-role",
     "grant": "inline policy s3-access stmt[0] Sid=BDDataBucket: Allow s3:PutObject,s3:GetObject,s3:ListBucket,s3:HeadObject,s3:DeleteObject,s3:CopyObject on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/ec2/bd-exporter/terraform/main.tf",
     "comp_iam": "comp-iam role bd-exporter-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "bd-gold-detail-generator-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/bd-gold-detail-generator-role",
     "grant": "inline policy bd-gold-detail-s3-access stmt[0]: Allow s3:GetObject,s3:PutObject,s3:ListBucket on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/bd-pipeline/iam.tf",
     "comp_iam": "comp-iam role bd-gold-detail-generator-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "bd-gold-layer-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/bd-gold-layer-lambda-role",
     "grant": "inline policy bd-s3-scoped stmt[0]: Allow s3:GetObject,s3:PutObject,s3:DeleteObject on arn:aws:s3:::opal-data-bd/* (literal) | inline policy bd-s3-scoped stmt[1]: Allow s3:ListBucket on arn:aws:s3:::opal-data-bd (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/bd-pipeline/iam.tf",
     "comp_iam": "comp-iam role bd-gold-layer-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "bd-merge-daily-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/bd-merge-daily-lambda-role",
     "grant": "inline policy bd-merge-daily-policy stmt[0]: Allow s3:GetObject,s3:PutObject,s3:ListBucket on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "grant_match": "literal",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role bd-merge-daily-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "bd-pipeline-task-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/bd-pipeline-task-role",
     "grant": "inline policy BDPipelineTaskPolicy stmt[0]: Allow s3:GetObject,s3:PutObject,s3:ListBucket,s3:DeleteObject on arn:aws:s3:::opal-data-bd/*,arn:aws:s3:::opal-data-bd (literal)",
     "grant_match": "literal",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role bd-pipeline-task-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "bd-processor-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/bd-processor-lambda-role",
     "grant": "inline policy bd-s3-readwrite stmt[0] Sid=S3BDFullAccess: Allow s3:GetObject,s3:PutObject,s3:DeleteObject,s3:ListBucket on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/bd-pipeline/iam.tf",
     "comp_iam": "comp-iam role bd-processor-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "bd-silver-merge-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/bd-silver-merge-role",
     "grant": "inline policy bd-silver-merge-policy stmt[0] Sid=ReadBdSilverAndBronzeCode: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/code/* (literal) | inline policy bd-silver-merge-policy stmt[1] Sid=ReadBdForwardfillBronze: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/forwardfill_v2/* (literal) | inline policy bd-silver-merge-policy stmt[2] Sid=ReadWriteBdSilver: Allow s3:GetObject,s3:PutObject on arn:aws:s3:::opal-data-bd/silver/* (literal) | inline policy bd-silver-merge-policy stmt[3] Sid=ListBdBucket: Allow s3:ListBucket on arn:aws:s3:::opal-data-bd (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/bd-pipeline/bd-silver-merge.tf",
     "comp_iam": "comp-iam role bd-silver-merge-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "demo-transform-runner-ec2-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/demo-transform-runner-ec2-role",
     "grant": "inline policy demo-transform-runner-s3-scoped stmt[0] Sid=ReadSourcePlatinumBd: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/platinum/* (literal) | inline policy demo-transform-runner-s3-scoped stmt[1] Sid=ListSourcePlatinumBd: Allow s3:ListBucket on arn:aws:s3:::opal-data-bd (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/shared-infra/demo-transform.tf",
     "comp_iam": "comp-iam role demo-transform-runner-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'demo' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "exec-summary-generator-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/exec-summary-generator-role",
     "grant": "inline policy exec-summary-generator-policy stmt[0] Sid=PlatinumReadAdvisors: Allow s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-bd/platinum/advisors/* (literal) | inline policy exec-summary-generator-policy stmt[1] Sid=PlatinumReadLeaderboards: Allow s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-bd/platinum/leaderboards/* (literal) | inline policy exec-summary-generator-policy stmt[2] Sid=PlatinumListBucket: Allow s3:ListBucket on arn:aws:s3:::opal-data-bd (literal, conditioned) | inline policy exec-summary-generator-policy stmt[3] Sid=PlatinumWriteExecSummary: Allow s3:PutObject,s3:PutObjectAcl on arn:aws:s3:::opal-data-bd/platinum/advisors/*/exec_summary.json (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/exec-summary/iam.tf",
     "comp_iam": "comp-iam role exec-summary-generator-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "gldinc-ss4c-canary-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/gldinc-ss4c-canary-role",
     "grant": "inline policy gldinc-ss4c-canary-policy stmt[0] Sid=ReadLoadFlowsCache: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/gold/_state/load_flows/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/bd-pipeline/gldinc-ss4c.tf",
     "comp_iam": "comp-iam role gldinc-ss4c-canary-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "infrastructure-ops-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/infrastructure-ops-lambda-role",
     "grant": "inline policy infrastructure-ops-permissions stmt[4] Sid=S3BucketEnumeration: Allow s3:ListAllMyBuckets,s3:GetBucketVersioning,s3:GetBucketEncryption,s3:GetBucketLocation,s3:GetBucketPolicy on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/shared-infra/iam_legacy.tf",
     "comp_iam": "comp-iam role infrastructure-ops-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "infrastructure-snapshot-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/infrastructure-snapshot-role",
     "grant": "inline policy InfrastructureSnapshotPolicy stmt[6] Sid=S3BucketRead: Allow s3:ListAllMyBuckets,s3:GetBucketVersioning,s3:GetBucketEncryption on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/shared-infra/iam_legacy.tf",
     "comp_iam": "comp-iam role infrastructure-snapshot-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "irpt-directory-refresh-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/irpt-directory-refresh-role",
     "grant": "inline policy irpt-directory-refresh-policy stmt[0] Sid=ReadFirmDirectoryPrefixOnly: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/investor-reporting/directory/* (literal) | inline policy irpt-directory-refresh-policy stmt[1] Sid=WriteRefreshManifestsOnly: Allow s3:PutObject on arn:aws:s3:::opal-data-bd/investor-reporting/directory/_refresh/* (literal) | inline policy irpt-directory-refresh-policy stmt[2] Sid=ListExactlyWhatItMayAlreadyRead: Allow s3:ListBucket on arn:aws:s3:::opal-data-bd (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/investor-reporting/directory/schedule.tf",
     "comp_iam": "comp-iam role irpt-directory-refresh-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "irpt-directory-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/irpt-directory-role",
     "grant": "inline policy irpt-directory-policy stmt[0] Sid=ReadFirmDirectoryPrefixOnly: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/investor-reporting/directory/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/investor-reporting/directory/iam.tf",
     "comp_iam": "comp-iam role irpt-directory-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "irpt-holdings-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/irpt-holdings-role",
     "grant": "inline policy irpt-holdings-firm-read stmt[0] Sid=ReadTheProductOnly: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/investor-reporting/* (literal) | inline policy irpt-holdings-firm-read stmt[1] Sid=ListUnderTheProductPrefixOnly: Allow s3:ListBucket on arn:aws:s3:::opal-data-bd (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/investor-reporting/holdings/iam.tf",
     "comp_iam": "comp-iam role irpt-holdings-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "irpt-status-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/irpt-status-role",
     "grant": "inline policy irpt-status-policy stmt[0] Sid=ReadFirmDirectoryPrefixOnly: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/investor-reporting/directory/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/investor-reporting/ops/iam.tf",
     "comp_iam": "comp-iam role irpt-status-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "lambda-edge-execution-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/lambda-edge-execution-role",
     "grant": "inline policy lambda-edge-ownership-map-read stmt[0]: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/platinum/*/ownership_map.json (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/portal-auth/iam.tf",
     "comp_iam": "comp-iam role lambda-edge-execution-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "lambda-execution-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/lambda-execution-role",
     "grant": "inline policy S3Access stmt[0]: Allow s3:GetObject,s3:PutObject,s3:ListBucket on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/shared-infra/lambda-execution-role.tf",
     "comp_iam": "comp-iam role lambda-execution-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [
      "inline policy cross-firm-bucket-write-deny stmt[0] Sid=DenyCrossFirmBucketWrites: Deny s3:Put*,s3:Delete* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)"
     ],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "mdpf-daily-runner-ec2-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/mdpf-daily-runner-ec2-role",
     "grant": "inline policy mdpf-runner-scoped stmt[4] Sid=BdReadWSD2WSE: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/schwab/silver/rps/*,arn:aws:s3:::opal-data-bd/silver/allocations/*,arn:aws:s3:::opal-data-bd/silver/fees/*,arn:aws:s3:::opal-data-bd/gold/aua_certification/* (literal) | inline policy mdpf-runner-scoped stmt[5] Sid=BdListScoped: Allow s3:ListBucket on arn:aws:s3:::opal-data-bd (literal, conditioned) | inline policy mdpf-runner-scoped stmt[31] Sid=IrptDirectoryFirmDestWrite: Allow s3:PutObject,s3:GetObject on arn:aws:s3:::opal-data-bd/investor-reporting/directory/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/mdpf-pipeline/iam.tf",
     "comp_iam": "comp-iam role mdpf-daily-runner-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "mdpf-feeder-trigger-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/mdpf-feeder-trigger-role",
     "grant": "inline policy mdpf-feeder-trigger stmt[4] Sid=FeederInputPrecheckRead: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/schwab/silver/rps/* (literal) | inline policy mdpf-feeder-trigger stmt[5] Sid=FeederInputPrecheckListForNotFoundSemantics: Allow s3:ListBucket on arn:aws:s3:::opal-data-bd (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/mdpf-pipeline/feeder-trigger.tf",
     "comp_iam": "comp-iam role mdpf-feeder-trigger-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-49f-served-guard",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-49f-served-guard",
     "grant": "inline policy ServedKeyGuardS3 stmt[0] Sid=ReadAndRestoreServedKey: Allow s3:GetObject,s3:GetObjectVersion,s3:PutObject on arn:aws:s3:::opal-data-bd/platinum/firm/header_metrics.json (literal) | inline policy ServedKeyGuardS3 stmt[1] Sid=QuarantineCopyWrite: Allow s3:PutObject on arn:aws:s3:::opal-data-bd/_quarantine/served-guard/* (literal) | inline policy ServedKeyGuardS3 stmt[2] Sid=ListServedKeyVersions: Allow s3:ListBucket,s3:ListBucketVersions on arn:aws:s3:::opal-data-bd (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-49f-served-guard: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "49f",
     "token_basis": "scope slot (slot 2) carries the short form '49f'; last slot 'guard' is not a kind"
    },
    {
     "principal": "opal-advi-stitch-landing-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-advi-stitch-landing-role",
     "grant": "inline policy opal-advi-stitch-landing-scoped stmt[0] Sid=ReadDeclaredSourceScopeSet: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/backfill_v2/*,arn:aws:s3:::opal-data-bd/forwardfill_v2/*,arn:aws:s3:::opal-data-bd/silver/*,arn:aws:s3:::opal-data-bd/gold/canonical/performance/*,arn:aws:s3:::opal-data-bd/gold/canonical/nna/*,arn:aws:s3:::opal-data-bd/gold/canonical/holdings/* (literal) | inline policy opal-advi-stitch-landing-scoped stmt[2] Sid=ListSourceScopeSetOnly: Allow s3:ListBucket,s3:ListBucketMultipartUploads on arn:aws:s3:::opal-data-bd (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/opal-assets/advi_stitch_landing.tf",
     "comp_iam": "comp-iam role opal-advi-stitch-landing-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-drift-producer-codebuild-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-drift-producer-codebuild-role",
     "grant": "AWS-managed policy ReadOnlyAccess stmt[1] Sid=ReadOnlyActionsGroup2: Allow s3:DescribeJob,s3:Get*,s3:List* on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/shared-infra/drift-producer.tf",
     "comp_iam": "comp-iam role opal-drift-producer-codebuild-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [
      "inline policy DriftProducerWritesAndDataDeny stmt[5] Sid=DenyFirmDataObjectReads: Deny s3:GetObject,s3:GetObjectVersion on arn:aws:s3:::opal-data-*/* (wildcard)"
     ],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-globgrph-derive-runner-task",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-globgrph-derive-runner-task",
     "grant": "inline policy DeriveRunnerAccountDescribe stmt[0] Sid=AccountWideReadOnly: Allow s3:GetBucketPolicy,s3:GetBucketVersioning,s3:GetBucketLocation,s3:ListAllMyBuckets on * (wildcard) | inline policy DeriveRunnerBucketNotificationRead stmt[0] Sid=BucketNotificationRead: Allow s3:GetBucketNotification on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/globgrph/item2a.tf",
     "comp_iam": "comp-iam role opal-globgrph-derive-runner-task: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-globgrph-incremental-updater",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-globgrph-incremental-updater",
     "grant": "inline policy BoundedDeriveReadOnly stmt[0] Sid=BoundedDeriveReadOnly: Allow s3:GetBucketPolicy,s3:GetBucketVersioning,s3:GetBucketLocation,s3:ListAllMyBuckets on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/globgrph/iam.tf",
     "comp_iam": "comp-iam role opal-globgrph-incremental-updater: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared); last slot 'updater' is not a kind"
    },
    {
     "principal": "opal-news-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-news-lambda-role",
     "grant": "AWS-managed policy AmazonS3ReadOnlyAccess stmt[0]: Allow s3:Get*,s3:List*,s3:Describe* on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/news-pipeline/iam.tf",
     "comp_iam": "comp-iam role opal-news-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [
      "inline policy cross-firm-bucket-read-deny stmt[0] Sid=DenyCrossFirmBucketReads: Deny s3:Get*,s3:List* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)"
     ],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-portal-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-portal-lambda-role",
     "grant": "inline policy MonitorDataFreshnessRead stmt[5] Sid=MonitorBdServedObjectRead: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/* (literal) | inline policy MonitorDataFreshnessRead stmt[6] Sid=MonitorBdServedBucketList: Allow s3:ListBucket on arn:aws:s3:::opal-data-bd (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf",
     "comp_iam": "comp-iam role opal-portal-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "partners-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/partners-lambda-role",
     "grant": "inline policy partners-lambda-permissions stmt[0] Sid=ReadPartnerBuckets: Allow s3:GetObject,s3:ListBucket on arn:aws:s3:::opal-data-*,arn:aws:s3:::opal-data-*/* (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/partners-api/iam.tf",
     "comp_iam": "comp-iam role partners-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "security-sweep-dedicated-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/security-sweep-dedicated-role",
     "grant": "inline policy SecuritySweepComprehensive stmt[0] Sid=SecuritySweepReadPermissions: Allow s3:ListAllMyBuckets,s3:GetBucketPublicAccessBlock,s3:GetBucketAcl,s3:GetBucketEncryption,s3:GetBucketVersioning,s3:GetBucketLogging,s3:GetBucketPolicy,s3:ListBucket on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/security-ops/iam.tf",
     "comp_iam": "comp-iam role security-sweep-dedicated-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "smartx-jwt-refresher-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/smartx-jwt-refresher-role",
     "grant": "inline policy smartx-jwt-refresher-access stmt[2] Sid=WriteJWTToS3: Allow s3:PutObject on arn:aws:s3:::opal-data-bd/smartx/jwt/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/smartx-pipeline/rest-pull-iam.tf",
     "comp_iam": "comp-iam role smartx-jwt-refresher-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "smartx-rest-pull-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/smartx-rest-pull-role",
     "grant": "inline policy smartx-rest-pull-access stmt[0] Sid=ReadParkedJWT: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/smartx/jwt/* (literal) | inline policy smartx-rest-pull-access stmt[1] Sid=WriteRawBronze: Allow s3:PutObject on arn:aws:s3:::opal-data-bd/smartx/raw/*,arn:aws:s3:::opal-data-bd/smartx/bronze/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/smartx-pipeline/rest-pull-iam.tf",
     "comp_iam": "comp-iam role smartx-rest-pull-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "wsd-49f-partner-held-etf-daily-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/wsd-49f-partner-held-etf-daily-role",
     "grant": "inline policy wsd-49f-partner-held-etf-daily stmt[0] Sid=ReadRpsSilver: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/schwab/silver/rps/* (literal) | inline policy wsd-49f-partner-held-etf-daily stmt[1] Sid=ListRpsPartitions: Allow s3:ListBucket on arn:aws:s3:::opal-data-bd (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/mdpf-pipeline/wp5-feeder-schedules.tf",
     "comp_iam": "comp-iam role wsd-49f-partner-held-etf-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "49f",
     "token_basis": "scope slot (slot 2) carries the short form '49f'"
    },
    {
     "principal": "Andrew_Berman",
     "kind": "user",
     "arn": "arn:aws:iam::313476888478:user/Andrew_Berman",
     "grant": "group AdministratorAccessOpalCapital AWS-managed policy AdministratorAccess stmt[0]: Allow * on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role: n/a (IAM user)",
     "belts": [],
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "Andrew_Berman_Console",
     "kind": "user",
     "arn": "arn:aws:iam::313476888478:user/Andrew_Berman_Console",
     "grant": "group AdministratorAccessOpalCapital AWS-managed policy AdministratorAccess stmt[0]: Allow * on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role: n/a (IAM user)",
     "belts": [],
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "Opal_Terminal",
     "kind": "user",
     "arn": "arn:aws:iam::313476888478:user/Opal_Terminal",
     "grant": "group AdministratorAccessOpalCapital AWS-managed policy AdministratorAccess stmt[0]: Allow * on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role: n/a (IAM user)",
     "belts": [],
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E139998VWH0PD",
     "kind": "oai",
     "arn": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E139998VWH0PD",
     "grant": "bucket policy opal-data-bd Sid=AllowScopedAdvisorOAI: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/*",
     "grant_match": "literal",
     "tf_source": "bucket policy (live read)",
     "comp_iam": "comp-iam role: n/a (not an IAM role)",
     "belts": [],
     "token": "none",
     "token_basis": "AWS-issued identifier: outside the grammar (NAMING_SCHEMA.json not_covered)"
    },
    {
     "principal": "cloudfront.amazonaws.com",
     "kind": "service",
     "arn": "cloudfront.amazonaws.com",
     "grant": "bucket policy opal-data-bd Sid=AllowCloudFrontOACReadGold: Allow s3:GetObject on arn:aws:s3:::opal-data-bd/gold/* (Condition AWS:SourceArn = distribution EVTSA9VEHNZVH)",
     "grant_match": "literal",
     "tf_source": "bucket policy (live read)",
     "comp_iam": "comp-iam role: n/a (not an IAM role)",
     "belts": [],
     "token": "none",
     "token_basis": "AWS-issued identifier: outside the grammar (NAMING_SCHEMA.json not_covered)"
    }
   ],
   "seen": [
    {
     "principal": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E139998VWH0PD",
     "kind": "oai",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (userIdentity type AWSAccount, principalId AIDAJ3ELLOIDNV4A5IWRG, accountId CloudFront): first GetObject 2026-09-14T14:27:35Z requestID HN7T8XR448SXEBNJ; last GetObject 2026-09-14T19:54:14Z requestID RB4MGY4SADJC0MHB; 233 event(s) in window: GetObject x233",
     "in_granted": true,
     "token": "none",
     "token_basis": "AWS-issued identifier: outside the grammar (NAMING_SCHEMA.json not_covered)"
    },
    {
     "principal": "Andrew_Berman",
     "kind": "user",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:user/Andrew_Berman): first ListObjects 2026-09-14T03:09:03Z requestID HE460JR68XRRE4Z4; last ListObjects 2026-09-14T19:09:05Z requestID AJP54FE4TC5KGYD5; 38 event(s) in window: ListObjects x38",
     "in_granted": true,
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "Andrew_Berman_Console",
     "kind": "user",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:user/Andrew_Berman_Console): first HeadBucket 2026-09-14T17:16:24Z requestID 7JFAVWEFPH829YYW; last HeadBucket 2026-09-14T17:16:24Z requestID 7JFAVWEFPH829YYW; 1 event(s) in window: HeadBucket x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "bd-exporter-ec2-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/bd-exporter-ec2-role): first GetObject 2026-09-14T04:00:40Z requestID TSXZZ3S2FDYRD81R; last GetObject 2026-09-14T14:01:48Z requestID 1P9YB50YMEJKEVCH; 112646 event(s) in window: GetObject x112330, HeadObject x27, ListObjects x289",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "gldinc-ss4c-canary-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/gldinc-ss4c-canary-role): first GetObject 2026-09-14T06:30:14Z requestID XBD12T65C93F0KG8; last GetObject 2026-09-14T06:30:21Z requestID G925DE00D0EN1ZVS; 2 event(s) in window: GetObject x2",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "irpt-directory-refresh-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/irpt-directory-refresh-role): first ListObjects 2026-09-14T13:00:31Z requestID JYFW8CG00ZBKP9TT; last ListObjects 2026-09-14T13:00:31Z requestID JYFW8CG00ZBKP9TT; 2 event(s) in window: GetObject x1, ListObjects x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "mdpf-daily-runner-ec2-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/mdpf-daily-runner-ec2-role): first GetObject 2026-09-14T12:52:57Z requestID ESA84ZZNDHCNAWQF; last GetObject 2026-09-14T12:54:15Z requestID 7PVZRQ036FR98PYZ; 5 event(s) in window: GetObject x3, ListObjects x2",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "mdpf-feeder-trigger-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/mdpf-feeder-trigger-role): first HeadObject 2026-09-14T12:52:10Z requestID M2RSX1XTMQXBEJRM; last HeadObject 2026-09-14T12:52:10Z requestID M2RSX1XTMQXBEJRM; 1 event(s) in window: HeadObject x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-49f-served-guard",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/opal-49f-served-guard): first GetObject 2026-09-14T05:35:37Z requestID HEPW9YKFEGN9C5MS; last GetObject 2026-09-14T05:35:37Z requestID HEPW9YKFEGN9C5MS; 2 event(s) in window: GetObject x1, ListObjectVersions x1",
     "in_granted": true,
     "token": "49f",
     "token_basis": "scope slot (slot 2) carries the short form '49f'; last slot 'guard' is not a kind"
    },
    {
     "principal": "opal-portal-lambda-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/opal-portal-lambda-role): first HeadObject 2026-09-14T13:01:42Z requestID 9R2KX747ZJD7CRGB; last HeadObject 2026-09-14T13:02:11Z requestID GV7GARVA7Y75Y7VQ; 46 event(s) in window: HeadObject x17, ListObjects x29",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "partners-lambda-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/partners-lambda-role): first GetObject 2026-09-14T14:27:42Z requestID QPH7F2VQZJ9BYK17; last GetObject 2026-09-14T19:54:14Z requestID RB4M89BWPEBA9DG0; 33 event(s) in window: GetObject x33",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "smartx-rest-pull-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/smartx-rest-pull-role): first GetObject 2026-09-14T13:15:30Z requestID XEDG3RHB9JWPD6H7; last GetObject 2026-09-14T13:15:30Z requestID XEDG3RHB9JWPD6H7; 1 event(s) in window: GetObject x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "bd-exporter-ec2-role",
     "kind": "role",
     "observed": "write platinum/firm/",
     "evidence": "opal-served-key-write-trail WriteOnly data event (arn:aws:iam::313476888478:role/bd-exporter-ec2-role): first PutObject 2026-09-14T05:27:31Z requestID RB54KRTS819ZR49C; last PutObject 2026-09-14T05:51:55Z requestID YAHZ81735MZRD9NT; 15 event(s) in window: CopyObject x1, PutObject x14",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    }
   ],
   "belt_only": [
    {
     "principal": "bd-cot-keepalive-role",
     "kind": "role",
     "belt": "inline policy bd-cot-keepalive-policy stmt[3] Sid=DenyBdPlane: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/cot-pipeline/cot-detection-layer.tf",
     "comp_iam": "comp-iam role bd-cot-keepalive-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read; also carries 'cot' in slot 2"
    },
    {
     "principal": "cot-exporter-ec2-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/cot-pipeline/iam.tf",
     "comp_iam": "comp-iam role cot-exporter-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "cot-gold-layer-ec2-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/cot-pipeline/iam.tf",
     "comp_iam": "comp-iam role cot-gold-layer-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "cot-rebalancer-runner-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/opal-assets/cot_rebalancer_runner.tf",
     "comp_iam": "comp-iam role cot-rebalancer-runner-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "cot-satellites-registry-producer-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/cot-pipeline/satellites-registry-producer.tf",
     "comp_iam": "comp-iam role cot-satellites-registry-producer-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-accounts-v2-daily-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-accounts-v2-daily.tf",
     "comp_iam": "comp-iam role inf-accounts-v2-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-assets-v2-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-api-assets-v2.tf",
     "comp_iam": "comp-iam role inf-api-assets-v2-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-positions-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-api-positions.tf",
     "comp_iam": "comp-iam role inf-api-positions-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-reps-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-api-reps.tf",
     "comp_iam": "comp-iam role inf-api-reps-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-txn-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-api-txn.tf",
     "comp_iam": "comp-iam role inf-api-txn-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-assets-trigger-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-assets-trigger-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-billing-daily-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-billing-daily.tf",
     "comp_iam": "comp-iam role inf-billing-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-bronze-runner-ec2-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf",
     "comp_iam": "comp-iam role inf-bronze-runner-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-bronze-trigger-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-bronze-trigger-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-ec2-launch-monitor-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-ec2-launch-monitor.tf",
     "comp_iam": "comp-iam role inf-ec2-launch-monitor-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-ec2-retry-launch-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-ec2-retry-launch.tf",
     "comp_iam": "comp-iam role inf-ec2-retry-launch-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-etf-ownership-daily-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-etf-ownership-daily.tf",
     "comp_iam": "comp-iam role inf-etf-ownership-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-eventbridge-ssm-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-eventbridge-ssm-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-exporter-ec2-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-exporter-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-gold-layer-ec2-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-gold-layer-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-gold-layer-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-gold-layer-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-gold-qa-runner-ec2-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-gold-qa-runner.tf",
     "comp_iam": "comp-iam role inf-gold-qa-runner-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-gold-trigger-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-gold-trigger-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-jwt-trigger-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-jwt-trigger-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-nna-partition-checker-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-nna-partition-checker.tf",
     "comp_iam": "comp-iam role inf-nna-partition-checker-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-otp-relay-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/lambda-otp-relay.tf",
     "comp_iam": "comp-iam role inf-otp-relay-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-performance-daily-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-performance-daily.tf",
     "comp_iam": "comp-iam role inf-performance-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-silver-aggregator-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-silver-aggregator-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-silver-chain-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-silver-chain.tf",
     "comp_iam": "comp-iam role inf-silver-chain-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-tax-daily-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-tax-daily.tf",
     "comp_iam": "comp-iam role inf-tax-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-unified-account-dim-daily-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-unified-account-dim-daily.tf",
     "comp_iam": "comp-iam role inf-unified-account-dim-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "opal-assets-bd49f-daily-pull-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/opal-assets/bd49f_pull.tf",
     "comp_iam": "comp-iam role opal-assets-bd49f-daily-pull-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-bd49f-reporting-pull-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/opal-assets/bd49f_reporting_pull.tf",
     "comp_iam": "comp-iam role opal-assets-bd49f-reporting-pull-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-ingest-router-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/opal-assets/router_iam.tf",
     "comp_iam": "comp-iam role opal-assets-ingest-router-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-mdpf-portal-publisher-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/opal-assets/mdpf_portal_publisher.tf",
     "comp_iam": "comp-iam role opal-assets-mdpf-portal-publisher-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-bd49finsurance-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-bd49finsurance-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-blackdiamond-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-blackdiamond-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-eclipse-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-eclipse-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-etf-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-etf-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-orion-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-orion-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-schwab-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-schwab-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-smartx-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-smartx-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-inf-served-guard",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-inf-served-guard: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "inf",
     "token_basis": "scope slot (slot 2) carries the short form 'inf'; last slot 'guard' is not a kind"
    },
    {
     "principal": "opal-inf-value-parity",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/inf-value-parity/inf_value_parity.tf",
     "comp_iam": "comp-iam role opal-inf-value-parity: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "inf",
     "token_basis": "scope slot (slot 2) carries the short form 'inf'; last slot 'parity' is not a kind"
    },
    {
     "principal": "opal-schwab-monolith-remap-role",
     "kind": "role",
     "belt": "inline policy opal-schwab-monolith-remap-inline stmt[2] Sid=DenyBdPlane: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/canonical-schwab-ec2/monolith-iam.tf",
     "comp_iam": "comp-iam role opal-schwab-monolith-remap-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "quartz-si2-spike-role",
     "kind": "role",
     "belt": "inline policy quartz-si2-spike-inline stmt[3] Sid=DenyBdPlane: Deny s3:* on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/canonical-schwab-ec2/iam.tf",
     "comp_iam": "comp-iam role quartz-si2-spike-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "smartx-assets-pull-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-bd,arn:aws:s3:::opal-data-bd/* (literal)",
     "tf_source": "infra/aws/terraform/smartx-pipeline/assets-pull-iam.tf",
     "comp_iam": "comp-iam role smartx-assets-pull-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    }
   ],
   "denominators": {
    "granted": 46,
    "seen": 13,
    "belt_only": 47
   }
  },
  "opal-data-inf": {
   "granted": [
    {
     "principal": "AWSServiceRoleForResourceExplorer",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/aws-service-role/resource-explorer-2.amazonaws.com/AWSServiceRoleForResourceExplorer",
     "grant": "AWS-managed policy AWSResourceExplorerServiceRolePolicy stmt[3] Sid=ResourceInventoryAccess: Allow s3:GetBucketLocation,s3:ListAccessPoints,s3:ListAllMyBuckets,s3:ListBucket,s3:ListMultiRegionAccessPoints,s3:ListStorageLensConfigurations,s3:ListStorageLensGroups on * (wildcard) | AWS-managed policy AWSResourceExplorerServiceRolePolicy stmt[4] Sid=PermissionsForReadGetResources: Allow s3:GetAccelerateConfiguration,s3:GetAccessGrant,s3:GetAccessGrantsInstance,s3:GetAccessGrantsLocation,s3:GetAnalyticsConfiguration,s3:GetBucketAbac,s3:GetBucketAcl,s3:GetBucketCORS,s3:GetBucketLogging,s3:GetBucketMetadataTableConfiguration,s3:GetBucketNotification,s3:GetBucketObjectLockConfiguration,s3:GetBucketOwnershipControls,s3:GetBucketPolicy,s3:GetBucketPublicAccessBlock,s3:GetBucketTagging,s3:GetBucketVersioning,s3:GetBucketWebsite,s3:GetEncryptionConfiguration,s3:GetIntelligentTieringConfiguration,s3:GetInventoryConfiguration,s3:GetLifecycleConfiguration,s3:GetMetricsConfiguration,s3:GetReplicationConfiguration,s3:GetStorageLensGroup,s3:ListAccessGrants,s3:ListAccessGrantsInstances,s3:ListTagsForResource on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role AWSServiceRoleForResourceExplorer: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "none",
     "token_basis": "not kebab-case: the resource grammar does not hold, no firm token"
    },
    {
     "principal": "AWSServiceRoleForSupport",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/aws-service-role/support.amazonaws.com/AWSServiceRoleForSupport",
     "grant": "AWS-managed policy AWSSupportServiceRolePolicy stmt[4] Sid=AWSSupportActionsGroup3: Allow s3:describeJob,s3:describeMultiRegionAccessPointOperation,s3:getAccelerateConfiguration,s3:getAccessGrant,s3:getAccessGrantsInstance,s3:getAccessGrantsInstanceResourcePolicy,s3:getAccessGrantsLocation,s3:getAccessPoint,s3:getAccessPointConfigurationForObjectLambda,s3:getAccessPointForObjectLambda,s3:getAccessPointPolicy,s3:getAccessPointPolicyForObjectLambda,s3:getAccessPointPolicyStatus,s3:getAccessPointPolicyStatusForObjectLambda,s3:getAccountPublicAccessBlock,s3:getAnalyticsConfiguration,s3:getBucketAcl,s3:getBucketCORS,s3:getBucketLocation,s3:getBucketLogging,s3:getBucketNotification,s3:getBucketObjectLockConfiguration,s3:getBucketOwnershipControls,s3:getBucketPolicy,s3:getBucketPolicyStatus,s3:getBucketPublicAccessBlock,s3:getBucketRequestPayment,s3:getBucketVersioning,s3:getBucketWebsite,s3:getEncryptionConfiguration,s3:getIntelligentTieringConfiguration,s3:getInventoryConfiguration,s3:getLifecycleConfiguration,s3:getMetricsConfiguration,s3:getMultiRegionAccessPoint,s3:getMultiRegionAccessPointPolicy,s3:getMultiRegionAccessPointPolicyStatus,s3:getMultiRegionAccessPointRoutes,s3:getObjectAcl,s3:getObjectLegalHold,s3:getObjectRetention,s3:getReplicationConfiguration,s3:getStorageLensConfiguration,s3:listAccessGrants,s3:listAccessGrantsInstances,s3:listAccessGrantsLocations,s3:listAccessPoints,s3:listAccessPointsForObjectLambda,s3:listAllMyBuckets,s3:listBucket,s3:listBucketMultipartUploads,s3:listBucketVersions,s3:listJobs,s3:listMultipartUploadParts,s3:listMultiRegionAccessPoints,s3:listStorageLensConfigurations on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role AWSServiceRoleForSupport: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "none",
     "token_basis": "not kebab-case: the resource grammar does not hold, no firm token"
    },
    {
     "principal": "AWSServiceRoleForTrustedAdvisor",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/aws-service-role/trustedadvisor.amazonaws.com/AWSServiceRoleForTrustedAdvisor",
     "grant": "AWS-managed policy AWSTrustedAdvisorServiceRolePolicy stmt[0] Sid=TrustedAdvisorServiceRolePermissions: Allow s3:GetAccountPublicAccessBlock,s3:GetBucketAcl,s3:GetBucketPolicy,s3:GetBucketPolicyStatus,s3:GetBucketLocation,s3:GetBucketLogging,s3:GetBucketVersioning,s3:GetBucketPublicAccessBlock,s3:GetLifecycleConfiguration,s3:ListBucket,s3:ListAllMyBuckets on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role AWSServiceRoleForTrustedAdvisor: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "none",
     "token_basis": "not kebab-case: the resource grammar does not hold, no firm token"
    },
    {
     "principal": "bd-exporter-ec2-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/bd-exporter-ec2-role",
     "grant": "inline policy advi-49f-chain-access stmt[4] Sid=AdviChainAssetTruthUnionInfPositionsReadTransitional: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/silver/api_dims/positions_mv/* (literal) | inline policy advi-49f-chain-access stmt[5] Sid=AdviChainAssetTruthUnionInfListScopedTransitional: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/ec2/bd-exporter/terraform/main.tf",
     "comp_iam": "comp-iam role bd-exporter-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-accounts-v2-daily-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-accounts-v2-daily-role",
     "grant": "inline policy s3-accounts-v2 stmt[0] Sid=JwtRead: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/orion/jwt/current.json (literal) | inline policy s3-accounts-v2 stmt[1] Sid=HhRepMappingBronzeRead: Allow s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/bronze/orion-api-v2/*/household_rep_mapping.json (literal) | inline policy s3-accounts-v2 stmt[2] Sid=BronzeNewPortfolioWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/bronze/orion-api/*/new_portfolio_accounts.json (literal) | inline policy s3-accounts-v2 stmt[3] Sid=BronzeAccountsRosterWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/bronze/orion-api/*/accounts_roster.json,arn:aws:s3:::opal-data-inf/bronze/orion-api/*/accounts_roster_marker.json (literal) | inline policy s3-accounts-v2 stmt[4] Sid=SilverAccountsV2Write: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/silver/api_dims/accounts_v2/* (literal) | inline policy s3-accounts-v2 stmt[5] Sid=SilverCompleteSentinelWrite: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/silver/_silver_complete/*/accounts_v2.json (literal) | inline policy s3-accounts-v2 stmt[6] Sid=BucketList: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-accounts-v2-daily.tf",
     "comp_iam": "comp-iam role inf-accounts-v2-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-assets-v2-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-api-assets-v2-lambda-role",
     "grant": "inline policy s3-assets-v2 stmt[0] Sid=JwtRead: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/orion/jwt/current.json (literal) | inline policy s3-assets-v2 stmt[1] Sid=HhRepMapRead: Allow s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/silver/api_dims/household_rep_mapping/* (literal) | inline policy s3-assets-v2 stmt[2] Sid=BronzeAssetsReadWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/bronze/assets/* (literal) | inline policy s3-assets-v2 stmt[3] Sid=SilverAssetsV2Write: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/silver/assets_v2/* (literal) | inline policy s3-assets-v2 stmt[4] Sid=SilverCompleteSentinelWrite: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/silver/_silver_complete/*/assets_v2.json (literal) | inline policy s3-assets-v2 stmt[5] Sid=RateLimiterState: Allow s3:GetObject,s3:PutObject on arn:aws:s3:::opal-data-inf/orion/rate_limit_state_assets_v2.json (literal) | inline policy s3-assets-v2 stmt[6] Sid=BucketList: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-api-assets-v2.tf",
     "comp_iam": "comp-iam role inf-api-assets-v2-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-eclipse-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-api-eclipse-role",
     "grant": "inline policy inf-api-eclipse-scoped stmt[1] Sid=WriteEclipseStagingBronzeOnly: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/bronze/eclipse_qa/* (literal) | inline policy inf-api-eclipse-scoped stmt[2] Sid=ListEclipseStagingPrefix: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/br1-eclipse-rehome.tf",
     "comp_iam": "comp-iam role inf-api-eclipse-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-positions-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-api-positions-role",
     "grant": "inline policy s3-positions stmt[0] Sid=JwtRead: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/orion/jwt/current.json (literal) | inline policy s3-positions stmt[1] Sid=HhRepMapRead: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/silver/api_dims/household_rep_mapping/* (literal) | inline policy s3-positions stmt[2] Sid=BronzePositionsWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/bronze/positions/* (literal) | inline policy s3-positions stmt[3] Sid=SilverPositionsMvWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/silver/api_dims/positions_mv/* (literal) | inline policy s3-positions stmt[4] Sid=SilverCompleteSentinelWrite: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/silver/_silver_complete/*/positions_daily.json (literal) | inline policy s3-positions stmt[5] Sid=RateLimiterState: Allow s3:GetObject,s3:PutObject on arn:aws:s3:::opal-data-inf/orion/rate_limit_state_positions_mv.json (literal) | inline policy s3-positions stmt[6] Sid=BucketList: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-api-positions.tf",
     "comp_iam": "comp-iam role inf-api-positions-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-reps-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-api-reps-role",
     "grant": "inline policy s3-reps stmt[0] Sid=JwtRead: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/orion/jwt/current.json (literal) | inline policy s3-reps stmt[1] Sid=BronzeRepsWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/bronze/orion-api-v2/* (literal) | inline policy s3-reps stmt[2] Sid=SilverRepsWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/silver/api_dims/representatives/* (literal) | inline policy s3-reps stmt[3] Sid=SilverHhRepMapWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/silver/api_dims/household_rep_mapping/* (literal) | inline policy s3-reps stmt[4] Sid=SilverCompleteSentinelWrite: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/silver/_silver_complete/*/representatives.json (literal) | inline policy s3-reps stmt[5] Sid=RateLimiterState: Allow s3:GetObject,s3:PutObject on arn:aws:s3:::opal-data-inf/orion/rate_limit_state_reps.json (literal) | inline policy s3-reps stmt[6] Sid=BucketList: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-api-reps.tf",
     "comp_iam": "comp-iam role inf-api-reps-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-txn-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-api-txn-role",
     "grant": "inline policy s3-txn stmt[0] Sid=JwtRead: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/orion/jwt/current.json (literal) | inline policy s3-txn stmt[1] Sid=BronzeTxnWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/bronze/orion-api/*/transactions.csv (literal) | inline policy s3-txn stmt[2] Sid=SilverTxnWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/silver/transactions/* (literal) | inline policy s3-txn stmt[3] Sid=SilverCompleteSentinelWrite: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/silver/_silver_complete/*/transactions.json (literal) | inline policy s3-txn stmt[4] Sid=BucketList: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-api-txn.tf",
     "comp_iam": "comp-iam role inf-api-txn-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-billing-daily-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-billing-daily-role",
     "grant": "inline policy s3-billing stmt[0] Sid=JwtRead: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/orion/jwt/current.json (literal) | inline policy s3-billing stmt[1] Sid=BronzeBillingWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/bronze/orion-api/*/billing.csv (literal) | inline policy s3-billing stmt[2] Sid=SilverCompleteSentinelWrite: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/silver/_silver_complete/*/billing.json (literal) | inline policy s3-billing stmt[3] Sid=BucketList: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-billing-daily.tf",
     "comp_iam": "comp-iam role inf-billing-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-bronze-complete-emitter-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-bronze-complete-emitter-role",
     "grant": "inline policy inf-bronze-complete-emitter-scoped stmt[0] Sid=ListOrionApiBronze: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned) | inline policy inf-bronze-complete-emitter-scoped stmt[1] Sid=PutSentinelUnderOrionApiBronze: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/bronze/orion-api/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/br1-eclipse-rehome.tf",
     "comp_iam": "comp-iam role inf-bronze-complete-emitter-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-bronze-runner-ec2-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-bronze-runner-ec2-role",
     "grant": "inline policy bronze-modemarker-rw stmt[0] Sid=BronzeModemarkerAccess: Allow s3:GetObject,s3:PutObject,s3:DeleteObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/orion/bronze-trigger-mode.json (literal) | inline policy s3-rate-limit-state stmt[0] Sid=RateLimiterStateRW: Allow s3:GetObject,s3:PutObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/orion/rate_limit_state_* (literal) | inline policy s3-scoped-inf stmt[0] Sid=ReadJwt: Allow s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/orion/jwt/*,arn:aws:s3:::opal-data-inf/orion/bronze-trigger-mode.json (literal) | inline policy s3-scoped-inf stmt[1] Sid=ReadCode: Allow s3:GetObject,s3:ListBucket on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/code/bronze-runner/*,arn:aws:s3:::opal-data-inf/code/bronze/* (literal) | inline policy s3-scoped-inf stmt[2] Sid=WriteBronze: Allow s3:GetObject,s3:PutObject,s3:HeadObject,s3:DeleteObject on arn:aws:s3:::opal-data-inf/bronze/orion-api/*,arn:aws:s3:::opal-data-inf/bronze/orion-api-v2/*,arn:aws:s3:::opal-data-inf/bronze/positions/*,arn:aws:s3:::opal-data-inf/bronze/assets/*,arn:aws:s3:::opal-data-inf/bronze/transactions/*,arn:aws:s3:::opal-data-inf/bronze/performance/*,arn:aws:s3:::opal-data-inf/bronze/logs/inf-bronze-runner/*,arn:aws:s3:::opal-data-inf/orion/backfill_progress_*,arn:aws:s3:::opal-data-inf/orion/rate_limit_state_* (literal) | inline policy s3-scoped-inf stmt[3] Sid=ReadSilverInputDims: Allow s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/silver/api_dims/household_rep_mapping/*,arn:aws:s3:::opal-data-inf/silver/api_dims/household/*,arn:aws:s3:::opal-data-inf/silver/api_dims/accounts_v2/* (literal) | inline policy s3-scoped-inf stmt[4] Sid=WriteSilver: Allow s3:GetObject,s3:PutObject,s3:HeadObject,s3:DeleteObject on arn:aws:s3:::opal-data-inf/silver/api_dims/positions_mv/*,arn:aws:s3:::opal-data-inf/silver/assets_v2/*,arn:aws:s3:::opal-data-inf/silver/transactions/*,arn:aws:s3:::opal-data-inf/silver/performance/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf",
     "comp_iam": "comp-iam role inf-bronze-runner-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-bronze-trigger-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-bronze-trigger-lambda-role",
     "grant": "inline policy inf-bronze-trigger-policy stmt[2] Sid=WriteBronzeModeMarker: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/orion/bronze-trigger-mode.json (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-bronze-trigger-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-etf-ownership-daily-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-etf-ownership-daily-role",
     "grant": "inline policy s3-etf-ownership stmt[0] Sid=ReadOwnFirmHoldings: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/gold/canonical/holdings_* (literal) | inline policy s3-etf-ownership stmt[6] Sid=ListInfHoldings: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-etf-ownership-daily.tf",
     "comp_iam": "comp-iam role inf-etf-ownership-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-exporter-ec2-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-exporter-ec2-role",
     "grant": "inline policy s3-scoped-inf-exporter stmt[0] Sid=BronzeOrionRW: Allow s3:PutObject,s3:GetObject,s3:DeleteObject,s3:HeadObject,s3:ListBucket on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/bronze/orion/*,arn:aws:s3:::opal-data-inf/otp/*,arn:aws:s3:::opal-data-inf/orion/jwt/*,arn:aws:s3:::opal-data-inf/orion/browser-profile/*,arn:aws:s3:::opal-data-inf/eclipse/browser-profile/*,arn:aws:s3:::opal-data-inf/code/exporter/*,arn:aws:s3:::opal-data-inf/gold/logs/inf-exporter/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-exporter-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-gold-layer-ec2-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-gold-layer-ec2-role",
     "grant": "inline policy s3-scoped-inf stmt[0] Sid=InfDataBucket: Allow s3:GetObject,s3:PutObject,s3:DeleteObject,s3:HeadObject,s3:ListBucket on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-gold-layer-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-gold-layer-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-gold-layer-lambda-role",
     "grant": "inline policy inf-s3-scoped stmt[0]: Allow s3:GetObject,s3:PutObject,s3:DeleteObject on arn:aws:s3:::opal-data-inf/* (literal) | inline policy inf-s3-scoped stmt[1]: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-gold-layer-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-gold-qa-runner-ec2-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-gold-qa-runner-ec2-role",
     "grant": "inline policy s3-qa-scoped stmt[0] Sid=ReadGoldRunnerInputs: Allow s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/silver/*,arn:aws:s3:::opal-data-inf/gold/canonical/*,arn:aws:s3:::opal-data-inf/gold/views/*,arn:aws:s3:::opal-data-inf/gold/timeseries/*,arn:aws:s3:::opal-data-inf/gold/dimensions/*,arn:aws:s3:::opal-data-inf/gold/holdings/*,arn:aws:s3:::opal-data-inf/code/gold/*,arn:aws:s3:::opal-data-inf/code/silver/*,arn:aws:s3:::opal-data-inf/code/bronze/*,arn:aws:s3:::opal-data-inf/code/manual_api/*,arn:aws:s3:::opal-data-inf/bronze/*,arn:aws:s3:::opal-data-inf/platinum/advisors/* (literal) | inline policy s3-qa-scoped stmt[1] Sid=WriteQAArtifacts: Allow s3:PutObject,s3:GetObject,s3:DeleteObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/qa/*,arn:aws:s3:::opal-data-inf/gold/logs/inf-gold-qa-runner/*,arn:aws:s3:::opal-data-inf/silver/assets_v2/*,arn:aws:s3:::opal-data-inf/silver/api_dims/assets/* (literal) | inline policy s3-qa-scoped stmt[2] Sid=BucketList: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-gold-qa-runner.tf",
     "comp_iam": "comp-iam role inf-gold-qa-runner-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [
      "inline policy s3-qa-scoped stmt[3] Sid=DenyPlatinumWrites: Deny s3:PutObject,s3:DeleteObject on arn:aws:s3:::opal-data-inf/platinum/* (literal)"
     ],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-gold-trigger-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-gold-trigger-lambda-role",
     "grant": "inline policy inf-gold-trigger-policy stmt[5] Sid=DispatchLockRW: Allow s3:GetObject,s3:PutObject,s3:DeleteObject on arn:aws:s3:::opal-data-inf/gold/dispatch-lock.json (literal) | inline policy inf-gold-trigger-policy stmt[6] Sid=DispatchLockBucketList: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-gold-trigger-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-jwt-trigger-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-jwt-trigger-lambda-role",
     "grant": "inline policy inf-jwt-trigger-policy stmt[2] Sid=WriteModeMarker: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/orion/jwt/trigger-mode.json (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-jwt-trigger-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-nna-partition-checker-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-nna-partition-checker-lambda-role",
     "grant": "inline policy inf-nna-partition-checker-scoped stmt[0] Sid=ReadCanonicalNnaArtifact: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/platinum/firm/advisor_nna_canonical.json (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-nna-partition-checker.tf",
     "comp_iam": "comp-iam role inf-nna-partition-checker-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-otp-relay-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-otp-relay-lambda-role",
     "grant": "inline policy s3-otp-rw stmt[0] Sid=OtpPrefixRW: Allow s3:PutObject,s3:GetObject,s3:DeleteObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/otp/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/lambda-otp-relay.tf",
     "comp_iam": "comp-iam role inf-otp-relay-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-performance-daily-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-performance-daily-role",
     "grant": "inline policy s3-performance stmt[0] Sid=JwtRead: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/orion/jwt/current.json (literal) | inline policy s3-performance stmt[1] Sid=BronzePerformanceCsvWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/bronze/orion-api/*/performance_dim.csv (literal) | inline policy s3-performance stmt[2] Sid=BronzePerformanceSkipWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/bronze/orion-api/*/performance_dim_SKIP.json (literal) | inline policy s3-performance stmt[3] Sid=SilverCompleteSentinelWrite: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/silver/_silver_complete/*/performance.json (literal) | inline policy s3-performance stmt[4] Sid=BucketList: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-performance-daily.tf",
     "comp_iam": "comp-iam role inf-performance-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-silver-aggregator-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-silver-aggregator-lambda-role",
     "grant": "inline policy inf-silver-aggregator-policy stmt[0] Sid=ListSentinels: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned) | inline policy inf-silver-aggregator-policy stmt[1] Sid=ReadSentinels: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/silver/_silver_complete/* (literal) | inline policy inf-silver-aggregator-policy stmt[2] Sid=WriteFiredMarker: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/silver/_silver_complete/*/_AGGREGATOR_FIRED.json (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-silver-aggregator-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-silver-chain-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-silver-chain-lambda-role",
     "grant": "inline policy inf-silver-chain-s3 stmt[0] Sid=BronzeReadOnly: Allow s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/bronze/orion-api/* (literal) | inline policy inf-silver-chain-s3 stmt[1] Sid=SilverWriteAndChainSummary: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/silver/api_dims/* (literal) | inline policy inf-silver-chain-s3 stmt[2] Sid=BucketList: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-silver-chain.tf",
     "comp_iam": "comp-iam role inf-silver-chain-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-tax-daily-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-tax-daily-role",
     "grant": "inline policy s3-tax stmt[0] Sid=JwtRead: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/orion/jwt/current.json (literal) | inline policy s3-tax stmt[1] Sid=BronzeTaxUnrealizedWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/bronze/orion-api/*/tax_unrealized.csv (literal) | inline policy s3-tax stmt[2] Sid=BronzeTaxRealizedWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/bronze/orion-api/*/tax_realized.csv (literal) | inline policy s3-tax stmt[3] Sid=SilverCompleteSentinelWrite: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/silver/_silver_complete/*/tax.json (literal) | inline policy s3-tax stmt[4] Sid=BucketList: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-tax-daily.tf",
     "comp_iam": "comp-iam role inf-tax-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-unified-account-dim-daily-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/inf-unified-account-dim-daily-role",
     "grant": "inline policy s3-unified-account-dim stmt[0] Sid=JwtRead: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/orion/jwt/current.json (literal) | inline policy s3-unified-account-dim stmt[1] Sid=BronzeUnifiedAccountDimWrite: Allow s3:PutObject,s3:GetObject,s3:HeadObject on arn:aws:s3:::opal-data-inf/bronze/orion-api/*/unified_account_dim.csv (literal) | inline policy s3-unified-account-dim stmt[2] Sid=SilverCompleteSentinelWrite: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/silver/_silver_complete/*/unified_account_dim.json (literal) | inline policy s3-unified-account-dim stmt[3] Sid=BucketList: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-unified-account-dim-daily.tf",
     "comp_iam": "comp-iam role inf-unified-account-dim-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "infrastructure-ops-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/infrastructure-ops-lambda-role",
     "grant": "inline policy infrastructure-ops-permissions stmt[4] Sid=S3BucketEnumeration: Allow s3:ListAllMyBuckets,s3:GetBucketVersioning,s3:GetBucketEncryption,s3:GetBucketLocation,s3:GetBucketPolicy on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/shared-infra/iam_legacy.tf",
     "comp_iam": "comp-iam role infrastructure-ops-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "infrastructure-snapshot-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/infrastructure-snapshot-role",
     "grant": "inline policy InfrastructureSnapshotPolicy stmt[6] Sid=S3BucketRead: Allow s3:ListAllMyBuckets,s3:GetBucketVersioning,s3:GetBucketEncryption on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/shared-infra/iam_legacy.tf",
     "comp_iam": "comp-iam role infrastructure-snapshot-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "irpt-directory-refresh-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/irpt-directory-refresh-role",
     "grant": "inline policy irpt-directory-refresh-policy stmt[0] Sid=ReadFirmDirectoryPrefixOnly: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/investor-reporting/directory/* (literal) | inline policy irpt-directory-refresh-policy stmt[1] Sid=WriteRefreshManifestsOnly: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/investor-reporting/directory/_refresh/* (literal) | inline policy irpt-directory-refresh-policy stmt[2] Sid=ListExactlyWhatItMayAlreadyRead: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/investor-reporting/directory/schedule.tf",
     "comp_iam": "comp-iam role irpt-directory-refresh-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "irpt-directory-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/irpt-directory-role",
     "grant": "inline policy irpt-directory-policy stmt[0] Sid=ReadFirmDirectoryPrefixOnly: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/investor-reporting/directory/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/investor-reporting/directory/iam.tf",
     "comp_iam": "comp-iam role irpt-directory-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "irpt-holdings-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/irpt-holdings-role",
     "grant": "inline policy irpt-holdings-firm-read stmt[0] Sid=ReadTheProductOnly: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/investor-reporting/* (literal) | inline policy irpt-holdings-firm-read stmt[1] Sid=ListUnderTheProductPrefixOnly: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/investor-reporting/holdings/iam.tf",
     "comp_iam": "comp-iam role irpt-holdings-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "irpt-status-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/irpt-status-role",
     "grant": "inline policy irpt-status-policy stmt[0] Sid=ReadFirmDirectoryPrefixOnly: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/investor-reporting/directory/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/investor-reporting/ops/iam.tf",
     "comp_iam": "comp-iam role irpt-status-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "mdpf-daily-runner-ec2-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/mdpf-daily-runner-ec2-role",
     "grant": "inline policy mdpf-runner-scoped stmt[13] Sid=InfEclipseReadLegacyEmit: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/gold/eclipse/*,arn:aws:s3:::opal-data-inf/silver/eclipse/* (literal) | inline policy mdpf-runner-scoped stmt[14] Sid=InfClientPerfReadWSC: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/gold/timeseries/client_performance.parquet (literal) | inline policy mdpf-runner-scoped stmt[15] Sid=OrionJwtReadStage0Bronze: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/orion/jwt/* (literal) | inline policy mdpf-runner-scoped stmt[16] Sid=InfEclipseListScoped: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned) | inline policy mdpf-runner-scoped stmt[17] Sid=InfAccountsV2ListScoped: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned) | inline policy mdpf-runner-scoped stmt[18] Sid=InfAccountsV2Read: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/silver/api_dims/accounts_v2/* (literal) | inline policy mdpf-runner-scoped stmt[29] Sid=IrptDirectoryInfDimsRead: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/silver/api_dims/representatives/*,arn:aws:s3:::opal-data-inf/silver/api_dims/household_rep_mapping/* (literal) | inline policy mdpf-runner-scoped stmt[30] Sid=IrptDirectoryInfDimsListScoped: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned) | inline policy mdpf-runner-scoped stmt[31] Sid=IrptDirectoryFirmDestWrite: Allow s3:PutObject,s3:GetObject on arn:aws:s3:::opal-data-inf/investor-reporting/directory/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/mdpf-pipeline/iam.tf",
     "comp_iam": "comp-iam role mdpf-daily-runner-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "mdpf-feeder-trigger-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/mdpf-feeder-trigger-role",
     "grant": "inline policy mdpf-feeder-trigger stmt[4] Sid=FeederInputPrecheckRead: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/gold/eclipse/*/_meta/gold_complete.json (literal) | inline policy mdpf-feeder-trigger stmt[5] Sid=FeederInputPrecheckListForNotFoundSemantics: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/mdpf-pipeline/feeder-trigger.tf",
     "comp_iam": "comp-iam role mdpf-feeder-trigger-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-ingest-router-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-assets-ingest-router-role",
     "grant": "inline policy opal-assets-ingest-router-read-sources stmt[1] Sid=ReadSrcOpalDataInf: Allow s3:GetObject,s3:GetObjectVersion on arn:aws:s3:::opal-data-inf/bronze/* (literal) | inline policy opal-assets-ingest-router-read-sources stmt[3] Sid=ListSrcOpalDataInf: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/opal-assets/router_iam.tf",
     "comp_iam": "comp-iam role opal-assets-ingest-router-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [
      "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard)",
      "managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal)",
      "managed policy opal-assets-one-way-fan-in-fence stmt[2] Sid=DenyInfGoldSentinelAbsolutely: Deny s3:* on arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json (literal)"
     ],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-drift-producer-codebuild-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-drift-producer-codebuild-role",
     "grant": "AWS-managed policy ReadOnlyAccess stmt[1] Sid=ReadOnlyActionsGroup2: Allow s3:DescribeJob,s3:Get*,s3:List* on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/shared-infra/drift-producer.tf",
     "comp_iam": "comp-iam role opal-drift-producer-codebuild-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [
      "inline policy DriftProducerWritesAndDataDeny stmt[5] Sid=DenyFirmDataObjectReads: Deny s3:GetObject,s3:GetObjectVersion on arn:aws:s3:::opal-data-*/* (wildcard)"
     ],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-globgrph-derive-runner-task",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-globgrph-derive-runner-task",
     "grant": "inline policy DeriveRunnerAccountDescribe stmt[0] Sid=AccountWideReadOnly: Allow s3:GetBucketPolicy,s3:GetBucketVersioning,s3:GetBucketLocation,s3:ListAllMyBuckets on * (wildcard) | inline policy DeriveRunnerBucketNotificationRead stmt[0] Sid=BucketNotificationRead: Allow s3:GetBucketNotification on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/globgrph/item2a.tf",
     "comp_iam": "comp-iam role opal-globgrph-derive-runner-task: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-globgrph-incremental-updater",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-globgrph-incremental-updater",
     "grant": "inline policy BoundedDeriveReadOnly stmt[0] Sid=BoundedDeriveReadOnly: Allow s3:GetBucketPolicy,s3:GetBucketVersioning,s3:GetBucketLocation,s3:ListAllMyBuckets on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/globgrph/iam.tf",
     "comp_iam": "comp-iam role opal-globgrph-incremental-updater: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared); last slot 'updater' is not a kind"
    },
    {
     "principal": "opal-inf-served-guard",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-inf-served-guard",
     "grant": "inline policy ServedKeyGuardS3 stmt[0] Sid=ReadAndRestoreServedKey: Allow s3:GetObject,s3:GetObjectVersion,s3:PutObject on arn:aws:s3:::opal-data-inf/platinum/firm/header_metrics.json (literal) | inline policy ServedKeyGuardS3 stmt[1] Sid=QuarantineCopyWrite: Allow s3:PutObject on arn:aws:s3:::opal-data-inf/_quarantine/served-guard/* (literal) | inline policy ServedKeyGuardS3 stmt[2] Sid=ListServedKeyVersions: Allow s3:ListBucket,s3:ListBucketVersions on arn:aws:s3:::opal-data-inf (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-inf-served-guard: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "inf",
     "token_basis": "scope slot (slot 2) carries the short form 'inf'; last slot 'guard' is not a kind"
    },
    {
     "principal": "opal-inf-value-parity",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-inf-value-parity",
     "grant": "inline policy InfServedAndSourceRead stmt[0] Sid=InfServedAndPositionsMvRead: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/platinum/firm/header_metrics.json,arn:aws:s3:::opal-data-inf/silver/api_dims/positions_mv/snapshot_date=*/data.parquet (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/inf-value-parity/inf_value_parity.tf",
     "comp_iam": "comp-iam role opal-inf-value-parity: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "inf",
     "token_basis": "scope slot (slot 2) carries the short form 'inf'; last slot 'parity' is not a kind"
    },
    {
     "principal": "opal-news-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-news-lambda-role",
     "grant": "AWS-managed policy AmazonS3ReadOnlyAccess stmt[0]: Allow s3:Get*,s3:List*,s3:Describe* on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/news-pipeline/iam.tf",
     "comp_iam": "comp-iam role opal-news-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [
      "inline policy cross-firm-bucket-read-deny stmt[0] Sid=DenyCrossFirmBucketReads: Deny s3:Get*,s3:List* on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal)"
     ],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-portal-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-portal-lambda-role",
     "grant": "inline policy MonitorDataFreshnessRead stmt[0] Sid=MonitorInfServedObjectRead: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/* (literal) | inline policy MonitorDataFreshnessRead stmt[1] Sid=MonitorInfServedBucketList: Allow s3:ListBucket on arn:aws:s3:::opal-data-inf (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf",
     "comp_iam": "comp-iam role opal-portal-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "partners-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/partners-lambda-role",
     "grant": "inline policy partners-lambda-permissions stmt[0] Sid=ReadPartnerBuckets: Allow s3:GetObject,s3:ListBucket on arn:aws:s3:::opal-data-*,arn:aws:s3:::opal-data-*/* (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/partners-api/iam.tf",
     "comp_iam": "comp-iam role partners-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "security-sweep-dedicated-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/security-sweep-dedicated-role",
     "grant": "inline policy SecuritySweepComprehensive stmt[0] Sid=SecuritySweepReadPermissions: Allow s3:ListAllMyBuckets,s3:GetBucketPublicAccessBlock,s3:GetBucketAcl,s3:GetBucketEncryption,s3:GetBucketVersioning,s3:GetBucketLogging,s3:GetBucketPolicy,s3:ListBucket on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/security-ops/iam.tf",
     "comp_iam": "comp-iam role security-sweep-dedicated-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "Andrew_Berman",
     "kind": "user",
     "arn": "arn:aws:iam::313476888478:user/Andrew_Berman",
     "grant": "managed policy inf-andrew-otp-write stmt[0] Sid=OTPRelay: Allow s3:PutObject,s3:GetObject,s3:DeleteObject on arn:aws:s3:::opal-data-inf/otp/* (literal) | group AdministratorAccessOpalCapital AWS-managed policy AdministratorAccess stmt[0]: Allow * on * (wildcard)",
     "grant_match": "literal",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role: n/a (IAM user)",
     "belts": [],
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "Andrew_Berman_Console",
     "kind": "user",
     "arn": "arn:aws:iam::313476888478:user/Andrew_Berman_Console",
     "grant": "managed policy inf-andrew-otp-write stmt[0] Sid=OTPRelay: Allow s3:PutObject,s3:GetObject,s3:DeleteObject on arn:aws:s3:::opal-data-inf/otp/* (literal) | group AdministratorAccessOpalCapital AWS-managed policy AdministratorAccess stmt[0]: Allow * on * (wildcard)",
     "grant_match": "literal",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role: n/a (IAM user)",
     "belts": [],
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "Opal_Terminal",
     "kind": "user",
     "arn": "arn:aws:iam::313476888478:user/Opal_Terminal",
     "grant": "managed policy inf-andrew-otp-write stmt[0] Sid=OTPRelay: Allow s3:PutObject,s3:GetObject,s3:DeleteObject on arn:aws:s3:::opal-data-inf/otp/* (literal) | group AdministratorAccessOpalCapital AWS-managed policy AdministratorAccess stmt[0]: Allow * on * (wildcard)",
     "grant_match": "literal",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role: n/a (IAM user)",
     "belts": [],
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E139998VWH0PD",
     "kind": "oai",
     "arn": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E139998VWH0PD",
     "grant": "bucket policy opal-data-inf Sid=AllowScopedAdvisorOAI: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/*",
     "grant_match": "literal",
     "tf_source": "bucket policy (live read)",
     "comp_iam": "comp-iam role: n/a (not an IAM role)",
     "belts": [],
     "token": "none",
     "token_basis": "AWS-issued identifier: outside the grammar (NAMING_SCHEMA.json not_covered)"
    },
    {
     "principal": "cloudfront.amazonaws.com",
     "kind": "service",
     "arn": "cloudfront.amazonaws.com",
     "grant": "bucket policy opal-data-inf Sid=AllowCFDistributionGold: Allow s3:GetObject on arn:aws:s3:::opal-data-inf/gold/* (Condition AWS:SourceArn = distribution EVTSA9VEHNZVH)",
     "grant_match": "literal",
     "tf_source": "bucket policy (live read)",
     "comp_iam": "comp-iam role: n/a (not an IAM role)",
     "belts": [],
     "token": "none",
     "token_basis": "AWS-issued identifier: outside the grammar (NAMING_SCHEMA.json not_covered)"
    }
   ],
   "seen": [
    {
     "principal": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E139998VWH0PD",
     "kind": "oai",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (userIdentity type AWSAccount, principalId AIDAJ3ELLOIDNV4A5IWRG, accountId CloudFront): first GetObject 2026-09-14T16:55:14Z requestID 1BTHDSEWNYE1T94S; last GetObject 2026-09-14T19:35:30Z requestID 0HVTH9BP7VSKT659; 123 event(s) in window: GetObject x123",
     "in_granted": true,
     "token": "none",
     "token_basis": "AWS-issued identifier: outside the grammar (NAMING_SCHEMA.json not_covered)"
    },
    {
     "principal": "Andrew_Berman",
     "kind": "user",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:user/Andrew_Berman): first ListObjects 2026-09-14T03:09:02Z requestID S7ZBPNC9J2YR040A; last ListObjects 2026-09-14T19:09:03Z requestID R5WH8RKA90TT7XMP; 68 event(s) in window: ListObjects x68",
     "in_granted": true,
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "Andrew_Berman_Console",
     "kind": "user",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:user/Andrew_Berman_Console): first HeadBucket 2026-09-14T17:16:25Z requestID 8K5A1ZBK1R35Z6XP; last HeadBucket 2026-09-14T17:16:25Z requestID 8K5A1ZBK1R35Z6XP; 1 event(s) in window: HeadBucket x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "bd-exporter-ec2-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/bd-exporter-ec2-role): first GetObject 2026-09-14T12:47:31Z requestID ZK5AHDKT3EF3SENP; last GetObject 2026-09-14T12:47:31Z requestID ZK5AHDKT3EF3SENP; 4 event(s) in window: GetObject x1, ListObjects x3",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-accounts-v2-daily-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-accounts-v2-daily-role): first GetObject 2026-09-14T11:07:28Z requestID DSHTDSCT7YNQ7YYS; last GetObject 2026-09-14T11:07:29Z requestID WG2R8JZFEAM7FX4H; 3 event(s) in window: GetObject x2, HeadObject x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-assets-v2-lambda-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-api-assets-v2-lambda-role): first GetObject 2026-09-14T11:17:26Z requestID B6CNQGSCHS95BT5D; last HeadObject 2026-09-14T11:20:33Z requestID MKB6J5WFBQPKN04K; 7 event(s) in window: GetObject x4, HeadObject x2, ListObjects x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-positions-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-api-positions-role): first GetObject 2026-09-14T11:22:53Z requestID WT6W8J8374XD0224; last GetObject 2026-09-14T11:25:11Z requestID NHR9ZD4GWR6S89W7; 6 event(s) in window: GetObject x4, HeadObject x1, ListObjects x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-reps-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-api-reps-role): first GetObject 2026-09-14T11:02:21Z requestID ZN31TQY7C9AJAN44; last GetObject 2026-09-14T11:02:21Z requestID ZN31TQY7C9AJAN44; 1 event(s) in window: GetObject x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-txn-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-api-txn-role): first GetObject 2026-09-14T11:32:30Z requestID Z8XATP4ZH5Y3TY3P; last GetObject 2026-09-14T11:32:30Z requestID Z8XATP4ZH5Y3TY3P; 1 event(s) in window: GetObject x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-billing-daily-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-billing-daily-role): first GetObject 2026-09-14T14:22:35Z requestID WKQCD0V608Q198ZM; last HeadObject 2026-09-14T14:24:22Z requestID 2KT5K8JJTW1SD1P5; 2 event(s) in window: GetObject x1, HeadObject x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-bronze-complete-emitter-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-bronze-complete-emitter-role): first ListObjects 2026-09-14T14:43:16Z requestID 0K9ASD1VF135GSTC; last ListObjects 2026-09-14T14:43:16Z requestID 0K9ASD1VF135GSTC; 1 event(s) in window: ListObjects x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-bronze-runner-ec2-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-bronze-runner-ec2-role): first GetObject 2026-09-14T11:15:38Z requestID ABCS5W4BNBY3ZRBZ; last HeadObject 2026-09-14T11:17:57Z requestID Q7KMTM6RBKJ8XTMA; 16 event(s) in window: GetObject x9, HeadObject x5, ListObjects x2",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-etf-ownership-daily-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-etf-ownership-daily-role): first ListObjects 2026-09-14T15:00:38Z requestID EZGKQJPM9EMZ250Z; last GetObject 2026-09-14T15:00:40Z requestID G8AS9BVK0FXS8591; 4 event(s) in window: GetObject x1, ListObjects x3",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-exporter-ec2-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-exporter-ec2-role): first ListObjects 2026-09-14T09:50:54Z requestID MHKZV2S9H7CGNYAT; last GetObject 2026-09-14T09:50:57Z requestID 45YP91GGZBTDRGNQ; 2 event(s) in window: GetObject x1, ListObjects x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-gold-layer-ec2-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-gold-layer-ec2-role): first HeadObject 2026-09-14T11:18:10Z requestID 946SPRH2J8Q1H74C; last ListObjects 2026-09-14T12:31:11Z requestID VMPTVVS2MV1J8C6R; 27600 event(s) in window: GetObject x27476, HeadObject x25, ListObjects x99",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-gold-trigger-lambda-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-gold-trigger-lambda-role): first GetObject 2026-09-14T11:32:56Z requestID B96VQKZRNNEEH7VM; last GetObject 2026-09-14T11:32:56Z requestID B96VQKZRNNEEH7VM; 1 event(s) in window: GetObject x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-nna-partition-checker-lambda-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-nna-partition-checker-lambda-role): first GetObject 2026-09-14T19:30:41Z requestID 34BZADA0TRV83CRN; last GetObject 2026-09-14T19:30:41Z requestID 34BZADA0TRV83CRN; 1 event(s) in window: GetObject x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-otp-relay-lambda-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-otp-relay-lambda-role): first GetObject 2026-09-14T09:50:58Z requestID BZ4WQFMTYJ0ZVH52; last GetObject 2026-09-14T09:51:18Z requestID DCRKZVVG252HPZDP; 3 event(s) in window: GetObject x3",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-performance-daily-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-performance-daily-role): first GetObject 2026-09-14T14:27:07Z requestID G3AGHH1SS0WJWSFS; last HeadObject 2026-09-14T14:28:14Z requestID TBQZTN4DWYYKJ62Z; 2 event(s) in window: GetObject x1, HeadObject x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-silver-aggregator-lambda-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-silver-aggregator-lambda-role): first HeadObject 2026-09-14T11:02:34Z requestID XQZTC946JY2ZT7ED; last ListObjects 2026-09-14T14:28:16Z requestID ZAZ1GRKSR0FDJ2D1; 26 event(s) in window: GetObject x7, HeadObject x10, ListObjects x9",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-silver-chain-lambda-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-silver-chain-lambda-role): first GetObject 2026-09-14T11:18:02Z requestID 2W5KRHT2QTJT8YH1; last GetObject 2026-09-14T11:18:04Z requestID MD401WN8K7Y88WH3; 10 event(s) in window: GetObject x9, HeadObject x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-tax-daily-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-tax-daily-role): first GetObject 2026-09-14T13:42:33Z requestID TBC5FRKSXVRCN0ND; last HeadObject 2026-09-14T13:43:55Z requestID 45SE2HZR2J96CDMS; 3 event(s) in window: GetObject x1, HeadObject x2",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-unified-account-dim-daily-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/inf-unified-account-dim-daily-role): first GetObject 2026-09-14T13:27:31Z requestID NAMHAS61BJJ7CZST; last HeadObject 2026-09-14T13:29:42Z requestID 1CEF0BFF252WH9SV; 2 event(s) in window: GetObject x1, HeadObject x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "irpt-directory-refresh-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/irpt-directory-refresh-role): first GetObject 2026-09-14T13:00:32Z requestID MVMXZ76CDJ2N2BXR; last GetObject 2026-09-14T13:00:32Z requestID MVMXZ76CDJ2N2BXR; 2 event(s) in window: GetObject x1, ListObjects x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "mdpf-daily-runner-ec2-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/mdpf-daily-runner-ec2-role): first HeadObject 2026-09-14T12:52:53Z requestID E4Q3C9PYT16Y2KKF; last GetObject 2026-09-14T12:52:58Z requestID Y5TRYCS9CMJKJ71S; 7 event(s) in window: GetObject x4, HeadObject x1, ListObjects x2",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "mdpf-feeder-trigger-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/mdpf-feeder-trigger-role): first HeadObject 2026-09-14T12:52:09Z requestID ZTVQ97F1W2JSTFNH; last HeadObject 2026-09-14T12:52:09Z requestID ZTVQ97F1W2JSTFNH; 1 event(s) in window: HeadObject x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-ingest-router-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/opal-assets-ingest-router-role): first ListObjects 2026-09-14T13:05:17Z requestID ZCV03RQZPQZR2BC0; last GetObject 2026-09-14T13:05:29Z requestID NWARPX0RJ2X83BG9; 31 event(s) in window: GetObject x17, ListObjects x14",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-drift-producer-codebuild-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/opal-drift-producer-codebuild-role): first HeadBucket 2026-09-14T06:38:27Z requestID JDZ94TZP2VKQSKV4; last HeadBucket 2026-09-14T06:38:28Z requestID T5DVQTDCKY4VFBZF; 2 event(s) in window: HeadBucket x2",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-inf-value-parity",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/opal-inf-value-parity): first GetObject 2026-09-14T03:16:26Z requestID Y8JVGE63VK0MPCMT; last GetObject 2026-09-14T19:16:29Z requestID P58Z4XFZ9P74HM8E; 51 event(s) in window: GetObject x34, HeadObject x17",
     "in_granted": true,
     "token": "inf",
     "token_basis": "scope slot (slot 2) carries the short form 'inf'; last slot 'parity' is not a kind"
    },
    {
     "principal": "opal-portal-lambda-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/opal-portal-lambda-role): first ListObjects 2026-09-14T13:01:54Z requestID FB1QWA40Q8FNXFSZ; last HeadObject 2026-09-14T13:02:10Z requestID XTBJG7E24R7SS8GS; 55 event(s) in window: HeadObject x13, ListObjects x42",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "partners-lambda-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/partners-lambda-role): first GetObject 2026-09-14T16:55:15Z requestID 6ACKK5ZT60SW6ZQC; last GetObject 2026-09-14T19:35:30Z requestID 0HVJQPB69QWPJYHN; 36 event(s) in window: GetObject x36",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "inf-gold-layer-ec2-role",
     "kind": "role",
     "observed": "write platinum/firm/",
     "evidence": "opal-served-key-write-trail WriteOnly data event (arn:aws:iam::313476888478:role/inf-gold-layer-ec2-role): first PutObject 2026-09-14T11:52:07Z requestID T9FWXRPS87F6GW9Z; last PutObject 2026-09-14T12:11:56Z requestID C61H5ZHY76MBPEW2; 2303 event(s) in window: PutObject x2303",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    }
   ],
   "belt_only": [
    {
     "principal": "cot-exporter-ec2-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal)",
     "tf_source": "infra/aws/terraform/cot-pipeline/iam.tf",
     "comp_iam": "comp-iam role cot-exporter-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "cot-gold-layer-ec2-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal)",
     "tf_source": "infra/aws/terraform/cot-pipeline/iam.tf",
     "comp_iam": "comp-iam role cot-gold-layer-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "cot-rebalancer-runner-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal) | managed policy opal-assets-one-way-fan-in-fence stmt[2] Sid=DenyInfGoldSentinelAbsolutely: Deny s3:* on arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json (literal)",
     "tf_source": "infra/aws/terraform/opal-assets/cot_rebalancer_runner.tf",
     "comp_iam": "comp-iam role cot-rebalancer-runner-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "cot-satellites-registry-producer-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal)",
     "tf_source": "infra/aws/terraform/cot-pipeline/satellites-registry-producer.tf",
     "comp_iam": "comp-iam role cot-satellites-registry-producer-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "lambda-execution-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-write-deny stmt[0] Sid=DenyCrossFirmBucketWrites: Deny s3:Put*,s3:Delete* on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal)",
     "tf_source": "infra/aws/terraform/shared-infra/lambda-execution-role.tf",
     "comp_iam": "comp-iam role lambda-execution-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-bd49f-daily-pull-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal) | managed policy opal-assets-one-way-fan-in-fence stmt[2] Sid=DenyInfGoldSentinelAbsolutely: Deny s3:* on arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json (literal)",
     "tf_source": "infra/aws/terraform/opal-assets/bd49f_pull.tf",
     "comp_iam": "comp-iam role opal-assets-bd49f-daily-pull-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-bd49f-reporting-pull-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal) | managed policy opal-assets-one-way-fan-in-fence stmt[2] Sid=DenyInfGoldSentinelAbsolutely: Deny s3:* on arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json (literal)",
     "tf_source": "infra/aws/terraform/opal-assets/bd49f_reporting_pull.tf",
     "comp_iam": "comp-iam role opal-assets-bd49f-reporting-pull-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-mdpf-portal-publisher-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal) | managed policy opal-assets-one-way-fan-in-fence stmt[2] Sid=DenyInfGoldSentinelAbsolutely: Deny s3:* on arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json (literal)",
     "tf_source": "infra/aws/terraform/opal-assets/mdpf_portal_publisher.tf",
     "comp_iam": "comp-iam role opal-assets-mdpf-portal-publisher-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-bd49finsurance-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal) | managed policy opal-assets-one-way-fan-in-fence stmt[2] Sid=DenyInfGoldSentinelAbsolutely: Deny s3:* on arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-bd49finsurance-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-blackdiamond-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal) | managed policy opal-assets-one-way-fan-in-fence stmt[2] Sid=DenyInfGoldSentinelAbsolutely: Deny s3:* on arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-blackdiamond-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-eclipse-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal) | managed policy opal-assets-one-way-fan-in-fence stmt[2] Sid=DenyInfGoldSentinelAbsolutely: Deny s3:* on arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-eclipse-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-etf-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal) | managed policy opal-assets-one-way-fan-in-fence stmt[2] Sid=DenyInfGoldSentinelAbsolutely: Deny s3:* on arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-etf-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-orion-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal) | managed policy opal-assets-one-way-fan-in-fence stmt[2] Sid=DenyInfGoldSentinelAbsolutely: Deny s3:* on arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-orion-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-schwab-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal) | managed policy opal-assets-one-way-fan-in-fence stmt[2] Sid=DenyInfGoldSentinelAbsolutely: Deny s3:* on arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-schwab-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-smartx-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal) | managed policy opal-assets-one-way-fan-in-fence stmt[2] Sid=DenyInfGoldSentinelAbsolutely: Deny s3:* on arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-smartx-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-schwab-monolith-remap-role",
     "kind": "role",
     "belt": "inline policy opal-schwab-monolith-remap-inline stmt[4] Sid=DenyInfPlane: Deny s3:* on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal)",
     "tf_source": "infra/aws/terraform/canonical-schwab-ec2/monolith-iam.tf",
     "comp_iam": "comp-iam role opal-schwab-monolith-remap-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "quartz-si2-spike-role",
     "kind": "role",
     "belt": "inline policy quartz-si2-spike-inline stmt[5] Sid=DenyInfPlane: Deny s3:* on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal)",
     "tf_source": "infra/aws/terraform/canonical-schwab-ec2/iam.tf",
     "comp_iam": "comp-iam role quartz-si2-spike-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "smartx-assets-pull-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-inf,arn:aws:s3:::opal-data-inf/* (literal) | managed policy opal-assets-one-way-fan-in-fence stmt[2] Sid=DenyInfGoldSentinelAbsolutely: Deny s3:* on arn:aws:s3:::opal-data-inf/gold/meta/pipeline-complete.json (literal)",
     "tf_source": "infra/aws/terraform/smartx-pipeline/assets-pull-iam.tf",
     "comp_iam": "comp-iam role smartx-assets-pull-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    }
   ],
   "denominators": {
    "granted": 51,
    "seen": 32,
    "belt_only": 18
   }
  },
  "opal-data-cot": {
   "granted": [
    {
     "principal": "AWSServiceRoleForResourceExplorer",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/aws-service-role/resource-explorer-2.amazonaws.com/AWSServiceRoleForResourceExplorer",
     "grant": "AWS-managed policy AWSResourceExplorerServiceRolePolicy stmt[3] Sid=ResourceInventoryAccess: Allow s3:GetBucketLocation,s3:ListAccessPoints,s3:ListAllMyBuckets,s3:ListBucket,s3:ListMultiRegionAccessPoints,s3:ListStorageLensConfigurations,s3:ListStorageLensGroups on * (wildcard) | AWS-managed policy AWSResourceExplorerServiceRolePolicy stmt[4] Sid=PermissionsForReadGetResources: Allow s3:GetAccelerateConfiguration,s3:GetAccessGrant,s3:GetAccessGrantsInstance,s3:GetAccessGrantsLocation,s3:GetAnalyticsConfiguration,s3:GetBucketAbac,s3:GetBucketAcl,s3:GetBucketCORS,s3:GetBucketLogging,s3:GetBucketMetadataTableConfiguration,s3:GetBucketNotification,s3:GetBucketObjectLockConfiguration,s3:GetBucketOwnershipControls,s3:GetBucketPolicy,s3:GetBucketPublicAccessBlock,s3:GetBucketTagging,s3:GetBucketVersioning,s3:GetBucketWebsite,s3:GetEncryptionConfiguration,s3:GetIntelligentTieringConfiguration,s3:GetInventoryConfiguration,s3:GetLifecycleConfiguration,s3:GetMetricsConfiguration,s3:GetReplicationConfiguration,s3:GetStorageLensGroup,s3:ListAccessGrants,s3:ListAccessGrantsInstances,s3:ListTagsForResource on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role AWSServiceRoleForResourceExplorer: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "none",
     "token_basis": "not kebab-case: the resource grammar does not hold, no firm token"
    },
    {
     "principal": "AWSServiceRoleForSupport",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/aws-service-role/support.amazonaws.com/AWSServiceRoleForSupport",
     "grant": "AWS-managed policy AWSSupportServiceRolePolicy stmt[4] Sid=AWSSupportActionsGroup3: Allow s3:describeJob,s3:describeMultiRegionAccessPointOperation,s3:getAccelerateConfiguration,s3:getAccessGrant,s3:getAccessGrantsInstance,s3:getAccessGrantsInstanceResourcePolicy,s3:getAccessGrantsLocation,s3:getAccessPoint,s3:getAccessPointConfigurationForObjectLambda,s3:getAccessPointForObjectLambda,s3:getAccessPointPolicy,s3:getAccessPointPolicyForObjectLambda,s3:getAccessPointPolicyStatus,s3:getAccessPointPolicyStatusForObjectLambda,s3:getAccountPublicAccessBlock,s3:getAnalyticsConfiguration,s3:getBucketAcl,s3:getBucketCORS,s3:getBucketLocation,s3:getBucketLogging,s3:getBucketNotification,s3:getBucketObjectLockConfiguration,s3:getBucketOwnershipControls,s3:getBucketPolicy,s3:getBucketPolicyStatus,s3:getBucketPublicAccessBlock,s3:getBucketRequestPayment,s3:getBucketVersioning,s3:getBucketWebsite,s3:getEncryptionConfiguration,s3:getIntelligentTieringConfiguration,s3:getInventoryConfiguration,s3:getLifecycleConfiguration,s3:getMetricsConfiguration,s3:getMultiRegionAccessPoint,s3:getMultiRegionAccessPointPolicy,s3:getMultiRegionAccessPointPolicyStatus,s3:getMultiRegionAccessPointRoutes,s3:getObjectAcl,s3:getObjectLegalHold,s3:getObjectRetention,s3:getReplicationConfiguration,s3:getStorageLensConfiguration,s3:listAccessGrants,s3:listAccessGrantsInstances,s3:listAccessGrantsLocations,s3:listAccessPoints,s3:listAccessPointsForObjectLambda,s3:listAllMyBuckets,s3:listBucket,s3:listBucketMultipartUploads,s3:listBucketVersions,s3:listJobs,s3:listMultipartUploadParts,s3:listMultiRegionAccessPoints,s3:listStorageLensConfigurations on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role AWSServiceRoleForSupport: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "none",
     "token_basis": "not kebab-case: the resource grammar does not hold, no firm token"
    },
    {
     "principal": "AWSServiceRoleForTrustedAdvisor",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/aws-service-role/trustedadvisor.amazonaws.com/AWSServiceRoleForTrustedAdvisor",
     "grant": "AWS-managed policy AWSTrustedAdvisorServiceRolePolicy stmt[0] Sid=TrustedAdvisorServiceRolePermissions: Allow s3:GetAccountPublicAccessBlock,s3:GetBucketAcl,s3:GetBucketPolicy,s3:GetBucketPolicyStatus,s3:GetBucketLocation,s3:GetBucketLogging,s3:GetBucketVersioning,s3:GetBucketPublicAccessBlock,s3:GetLifecycleConfiguration,s3:ListBucket,s3:ListAllMyBuckets on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role AWSServiceRoleForTrustedAdvisor: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "none",
     "token_basis": "not kebab-case: the resource grammar does not hold, no firm token"
    },
    {
     "principal": "cot-bd-session-trigger-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/cot-bd-session-trigger-lambda-role",
     "grant": "inline policy cot-bd-session-trigger-policy stmt[2] Sid=WriteModeMarker: Allow s3:PutObject on arn:aws:s3:::opal-data-cot/blackdiamond/cot/session-trigger-mode.json (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/cot-pipeline/iam.tf",
     "comp_iam": "comp-iam role cot-bd-session-trigger-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read; also carries 'bd' in slot 2"
    },
    {
     "principal": "cot-etf-ownership-daily-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/cot-etf-ownership-daily-role",
     "grant": "inline policy s3-etf-ownership stmt[0] Sid=ReadOwnFirmHoldings: Allow s3:GetObject on arn:aws:s3:::opal-data-cot/gold/canonical/holdings/* (literal) | inline policy s3-etf-ownership stmt[6] Sid=ListCotHoldings: Allow s3:ListBucket on arn:aws:s3:::opal-data-cot (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/cot-pipeline/cot-etf-ownership-daily.tf",
     "comp_iam": "comp-iam role cot-etf-ownership-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "cot-exporter-ec2-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/cot-exporter-ec2-role",
     "grant": "inline policy cot-exporter-policy stmt[0] Sid=CotDataReadWrite: Allow s3:GetObject,s3:PutObject,s3:DeleteObject,s3:ListBucket on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/cot-pipeline/iam.tf",
     "comp_iam": "comp-iam role cot-exporter-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "cot-gold-layer-ec2-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/cot-gold-layer-ec2-role",
     "grant": "inline policy s3-scoped-cot stmt[0] Sid=CotDataReadWrite: Allow s3:GetObject,s3:PutObject,s3:DeleteObject,s3:ListBucket on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/cot-pipeline/iam.tf",
     "comp_iam": "comp-iam role cot-gold-layer-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "cot-satellites-registry-producer-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/cot-satellites-registry-producer-role",
     "grant": "inline policy s3-read-cot-bronze-write-cot-platinum stmt[1] Sid=WriteSatellitesRegistry: Allow s3:PutObject on arn:aws:s3:::opal-data-cot/platinum/satellites/registry.json (literal) | inline policy s3-read-cot-bronze-write-cot-platinum stmt[2] Sid=WriteSatellitesHoldings: Allow s3:PutObject on arn:aws:s3:::opal-data-cot/platinum/satellites/holdings.json (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/cot-pipeline/satellites-registry-producer.tf",
     "comp_iam": "comp-iam role cot-satellites-registry-producer-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "infrastructure-ops-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/infrastructure-ops-lambda-role",
     "grant": "inline policy infrastructure-ops-permissions stmt[4] Sid=S3BucketEnumeration: Allow s3:ListAllMyBuckets,s3:GetBucketVersioning,s3:GetBucketEncryption,s3:GetBucketLocation,s3:GetBucketPolicy on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/shared-infra/iam_legacy.tf",
     "comp_iam": "comp-iam role infrastructure-ops-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "infrastructure-snapshot-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/infrastructure-snapshot-role",
     "grant": "inline policy InfrastructureSnapshotPolicy stmt[6] Sid=S3BucketRead: Allow s3:ListAllMyBuckets,s3:GetBucketVersioning,s3:GetBucketEncryption on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/shared-infra/iam_legacy.tf",
     "comp_iam": "comp-iam role infrastructure-snapshot-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "irpt-directory-refresh-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/irpt-directory-refresh-role",
     "grant": "inline policy irpt-directory-refresh-policy stmt[0] Sid=ReadFirmDirectoryPrefixOnly: Allow s3:GetObject on arn:aws:s3:::opal-data-cot/investor-reporting/directory/* (literal) | inline policy irpt-directory-refresh-policy stmt[1] Sid=WriteRefreshManifestsOnly: Allow s3:PutObject on arn:aws:s3:::opal-data-cot/investor-reporting/directory/_refresh/* (literal) | inline policy irpt-directory-refresh-policy stmt[2] Sid=ListExactlyWhatItMayAlreadyRead: Allow s3:ListBucket on arn:aws:s3:::opal-data-cot (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/investor-reporting/directory/schedule.tf",
     "comp_iam": "comp-iam role irpt-directory-refresh-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "irpt-directory-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/irpt-directory-role",
     "grant": "inline policy irpt-directory-policy stmt[0] Sid=ReadFirmDirectoryPrefixOnly: Allow s3:GetObject on arn:aws:s3:::opal-data-cot/investor-reporting/directory/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/investor-reporting/directory/iam.tf",
     "comp_iam": "comp-iam role irpt-directory-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "irpt-holdings-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/irpt-holdings-role",
     "grant": "inline policy irpt-holdings-firm-read stmt[0] Sid=ReadTheProductOnly: Allow s3:GetObject on arn:aws:s3:::opal-data-cot/investor-reporting/* (literal) | inline policy irpt-holdings-firm-read stmt[1] Sid=ListUnderTheProductPrefixOnly: Allow s3:ListBucket on arn:aws:s3:::opal-data-cot (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/investor-reporting/holdings/iam.tf",
     "comp_iam": "comp-iam role irpt-holdings-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "irpt-status-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/irpt-status-role",
     "grant": "inline policy irpt-status-policy stmt[0] Sid=ReadFirmDirectoryPrefixOnly: Allow s3:GetObject on arn:aws:s3:::opal-data-cot/investor-reporting/directory/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/investor-reporting/ops/iam.tf",
     "comp_iam": "comp-iam role irpt-status-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "mdpf-daily-runner-ec2-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/mdpf-daily-runner-ec2-role",
     "grant": "inline policy mdpf-runner-scoped stmt[31] Sid=IrptDirectoryFirmDestWrite: Allow s3:PutObject,s3:GetObject on arn:aws:s3:::opal-data-cot/investor-reporting/directory/* (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/mdpf-pipeline/iam.tf",
     "comp_iam": "comp-iam role mdpf-daily-runner-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-ingest-router-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-assets-ingest-router-role",
     "grant": "inline policy opal-assets-ingest-router-read-sources stmt[0] Sid=ReadSrcOpalDataCot: Allow s3:GetObject,s3:GetObjectVersion on arn:aws:s3:::opal-data-cot/forwardfill_v2/*,arn:aws:s3:::opal-data-cot/code/bronze/templates/* (literal) | inline policy opal-assets-ingest-router-read-sources stmt[2] Sid=ListSrcOpalDataCot: Allow s3:ListBucket on arn:aws:s3:::opal-data-cot (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/opal-assets/router_iam.tf",
     "comp_iam": "comp-iam role opal-assets-ingest-router-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [
      "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard)",
      "managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)"
     ],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-cot-served-guard",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-cot-served-guard",
     "grant": "inline policy ServedKeyGuardS3 stmt[0] Sid=ReadAndRestoreServedKey: Allow s3:GetObject,s3:GetObjectVersion,s3:PutObject on arn:aws:s3:::opal-data-cot/platinum/firm/header_metrics.json (literal) | inline policy ServedKeyGuardS3 stmt[1] Sid=QuarantineCopyWrite: Allow s3:PutObject on arn:aws:s3:::opal-data-cot/_quarantine/served-guard/* (literal) | inline policy ServedKeyGuardS3 stmt[2] Sid=ListServedKeyVersions: Allow s3:ListBucket,s3:ListBucketVersions on arn:aws:s3:::opal-data-cot (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-cot-served-guard: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "cot",
     "token_basis": "scope slot (slot 2) carries the short form 'cot'; last slot 'guard' is not a kind"
    },
    {
     "principal": "opal-cot-value-parity",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-cot-value-parity",
     "grant": "inline policy CotServedAndSourceRead stmt[0] Sid=CotServedAndAnchorRead: Allow s3:GetObject on arn:aws:s3:::opal-data-cot/platinum/firm/header_metrics.json,arn:aws:s3:::opal-data-cot/silver/holdings/*.parquet (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/cot-value-parity/cot_value_parity.tf",
     "comp_iam": "comp-iam role opal-cot-value-parity: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "cot",
     "token_basis": "scope slot (slot 2) carries the short form 'cot'; last slot 'parity' is not a kind"
    },
    {
     "principal": "opal-drift-producer-codebuild-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-drift-producer-codebuild-role",
     "grant": "AWS-managed policy ReadOnlyAccess stmt[1] Sid=ReadOnlyActionsGroup2: Allow s3:DescribeJob,s3:Get*,s3:List* on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/shared-infra/drift-producer.tf",
     "comp_iam": "comp-iam role opal-drift-producer-codebuild-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [
      "inline policy DriftProducerWritesAndDataDeny stmt[5] Sid=DenyFirmDataObjectReads: Deny s3:GetObject,s3:GetObjectVersion on arn:aws:s3:::opal-data-*/* (wildcard)"
     ],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-globgrph-derive-runner-task",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-globgrph-derive-runner-task",
     "grant": "inline policy DeriveRunnerAccountDescribe stmt[0] Sid=AccountWideReadOnly: Allow s3:GetBucketPolicy,s3:GetBucketVersioning,s3:GetBucketLocation,s3:ListAllMyBuckets on * (wildcard) | inline policy DeriveRunnerBucketNotificationRead stmt[0] Sid=BucketNotificationRead: Allow s3:GetBucketNotification on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/globgrph/item2a.tf",
     "comp_iam": "comp-iam role opal-globgrph-derive-runner-task: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-globgrph-incremental-updater",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-globgrph-incremental-updater",
     "grant": "inline policy BoundedDeriveReadOnly stmt[0] Sid=BoundedDeriveReadOnly: Allow s3:GetBucketPolicy,s3:GetBucketVersioning,s3:GetBucketLocation,s3:ListAllMyBuckets on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/globgrph/iam.tf",
     "comp_iam": "comp-iam role opal-globgrph-incremental-updater: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared); last slot 'updater' is not a kind"
    },
    {
     "principal": "opal-news-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-news-lambda-role",
     "grant": "AWS-managed policy AmazonS3ReadOnlyAccess stmt[0]: Allow s3:Get*,s3:List*,s3:Describe* on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/news-pipeline/iam.tf",
     "comp_iam": "comp-iam role opal-news-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [
      "inline policy cross-firm-bucket-read-deny stmt[0] Sid=DenyCrossFirmBucketReads: Deny s3:Get*,s3:List* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)"
     ],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-portal-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-portal-lambda-role",
     "grant": "inline policy MonitorDataFreshnessRead stmt[2] Sid=MonitorCotPartitionList: Allow s3:ListBucket on arn:aws:s3:::opal-data-cot (literal)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf",
     "comp_iam": "comp-iam role opal-portal-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "partners-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/partners-lambda-role",
     "grant": "inline policy partners-lambda-permissions stmt[0] Sid=ReadPartnerBuckets: Allow s3:GetObject,s3:ListBucket on arn:aws:s3:::opal-data-*,arn:aws:s3:::opal-data-*/* (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/partners-api/iam.tf",
     "comp_iam": "comp-iam role partners-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "security-sweep-dedicated-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/security-sweep-dedicated-role",
     "grant": "inline policy SecuritySweepComprehensive stmt[0] Sid=SecuritySweepReadPermissions: Allow s3:ListAllMyBuckets,s3:GetBucketPublicAccessBlock,s3:GetBucketAcl,s3:GetBucketEncryption,s3:GetBucketVersioning,s3:GetBucketLogging,s3:GetBucketPolicy,s3:ListBucket on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/security-ops/iam.tf",
     "comp_iam": "comp-iam role security-sweep-dedicated-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "Andrew_Berman",
     "kind": "user",
     "arn": "arn:aws:iam::313476888478:user/Andrew_Berman",
     "grant": "group AdministratorAccessOpalCapital AWS-managed policy AdministratorAccess stmt[0]: Allow * on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role: n/a (IAM user)",
     "belts": [],
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "Andrew_Berman_Console",
     "kind": "user",
     "arn": "arn:aws:iam::313476888478:user/Andrew_Berman_Console",
     "grant": "group AdministratorAccessOpalCapital AWS-managed policy AdministratorAccess stmt[0]: Allow * on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role: n/a (IAM user)",
     "belts": [],
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "Opal_Terminal",
     "kind": "user",
     "arn": "arn:aws:iam::313476888478:user/Opal_Terminal",
     "grant": "group AdministratorAccessOpalCapital AWS-managed policy AdministratorAccess stmt[0]: Allow * on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role: n/a (IAM user)",
     "belts": [],
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E139998VWH0PD",
     "kind": "oai",
     "arn": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E139998VWH0PD",
     "grant": "bucket policy opal-data-cot Sid=AllowScopedAdvisorOAI: Allow s3:GetObject on arn:aws:s3:::opal-data-cot/*",
     "grant_match": "literal",
     "tf_source": "bucket policy (live read)",
     "comp_iam": "comp-iam role: n/a (not an IAM role)",
     "belts": [],
     "token": "none",
     "token_basis": "AWS-issued identifier: outside the grammar (NAMING_SCHEMA.json not_covered)"
    },
    {
     "principal": "cloudfront.amazonaws.com",
     "kind": "service",
     "arn": "cloudfront.amazonaws.com",
     "grant": "bucket policy opal-data-cot Sid=AllowCloudFrontOACReadGold: Allow s3:GetObject on arn:aws:s3:::opal-data-cot/gold/* (Condition AWS:SourceArn = distribution EVTSA9VEHNZVH)",
     "grant_match": "literal",
     "tf_source": "bucket policy (live read)",
     "comp_iam": "comp-iam role: n/a (not an IAM role)",
     "belts": [],
     "token": "none",
     "token_basis": "AWS-issued identifier: outside the grammar (NAMING_SCHEMA.json not_covered)"
    }
   ],
   "seen": [
    {
     "principal": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E139998VWH0PD",
     "kind": "oai",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (userIdentity type AWSAccount, principalId AIDAJ3ELLOIDNV4A5IWRG, accountId CloudFront): first GetObject 2026-09-14T14:56:13Z requestID TR3MT2JAFVJ151SC; last GetObject 2026-09-14T19:51:00Z requestID XVWY7AZS05ZAJB15; 80 event(s) in window: GetObject x80",
     "in_granted": true,
     "token": "none",
     "token_basis": "AWS-issued identifier: outside the grammar (NAMING_SCHEMA.json not_covered)"
    },
    {
     "principal": "Andrew_Berman",
     "kind": "user",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:user/Andrew_Berman): first HeadObject 2026-09-14T16:39:53Z requestID BX6ZFC24X5PNBHJH; last GetObject 2026-09-14T19:55:00Z requestID 6X0VJ6G7FX59G49D; 25 event(s) in window: GetObject x5, HeadBucket x4, HeadObject x11, ListObjects x5",
     "in_granted": true,
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "Andrew_Berman_Console",
     "kind": "user",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:user/Andrew_Berman_Console): first HeadBucket 2026-09-14T17:16:24Z requestID 7JFDZC5TY24KDATJ; last HeadBucket 2026-09-14T17:16:24Z requestID 7JFDZC5TY24KDATJ; 1 event(s) in window: HeadBucket x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "cot-exporter-ec2-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/cot-exporter-ec2-role): first HeadObject 2026-09-14T11:31:04Z requestID V7W86XDJHDRH1PKD; last GetObject 2026-09-14T11:36:57Z requestID 2VV45S443HJ28EAZ; 4796 event(s) in window: GetObject x4206, HeadObject x531, ListObjects x59",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "irpt-directory-refresh-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/irpt-directory-refresh-role): first ListObjects 2026-09-14T13:00:31Z requestID JYFZMRCPDDGHCQ7D; last ListObjects 2026-09-14T13:00:31Z requestID JYFZMRCPDDGHCQ7D; 2 event(s) in window: GetObject x1, ListObjects x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-ingest-router-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/opal-assets-ingest-router-role): first ListObjects 2026-09-14T11:45:52Z requestID M7YD5RKKEHPH5J9Q; last ListObjects 2026-09-14T11:45:55Z requestID XZN44KT0E9T932WM; 10 event(s) in window: GetObject x8, ListObjects x2",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-cot-served-guard",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/opal-cot-served-guard): first ListObjectVersions 2026-09-14T11:36:58Z requestID 2XKSWJWD8W6BZWC0; last ListObjectVersions 2026-09-14T11:36:58Z requestID 2XKSWJWD8W6BZWC0; 2 event(s) in window: GetObject x1, ListObjectVersions x1",
     "in_granted": true,
     "token": "cot",
     "token_basis": "scope slot (slot 2) carries the short form 'cot'; last slot 'guard' is not a kind"
    },
    {
     "principal": "opal-cot-value-parity",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/opal-cot-value-parity): first GetObject 2026-09-14T03:02:35Z requestID 7XBSDB7EXAPDKX58; last GetObject 2026-09-14T19:02:38Z requestID BZTERV57GHQMCRFS; 51 event(s) in window: GetObject x34, HeadObject x17",
     "in_granted": true,
     "token": "cot",
     "token_basis": "scope slot (slot 2) carries the short form 'cot'; last slot 'parity' is not a kind"
    },
    {
     "principal": "opal-drift-producer-codebuild-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/opal-drift-producer-codebuild-role): first HeadBucket 2026-09-14T06:34:03Z requestID K90KVHNHGRMTGY62; last HeadBucket 2026-09-14T06:34:03Z requestID K90KVHNHGRMTGY62; 2 event(s) in window: HeadBucket x2",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-portal-lambda-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/opal-portal-lambda-role): first ListObjects 2026-09-14T13:02:11Z requestID GV7PKXWY98PDKB4E; last ListObjects 2026-09-14T13:02:11Z requestID GV7PKXWY98PDKB4E; 11 event(s) in window: HeadObject x3, ListObjects x8",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "cot-exporter-ec2-role",
     "kind": "role",
     "observed": "write platinum/firm/",
     "evidence": "opal-served-key-write-trail WriteOnly data event (arn:aws:iam::313476888478:role/cot-exporter-ec2-role): first PutObject 2026-09-14T11:35:56Z requestID HVH3E13MMBGFK4ZD; last PutObject 2026-09-14T11:36:56Z requestID N8EV3DJMN8770CVC; 15 event(s) in window: PutObject x15",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    }
   ],
   "belt_only": [
    {
     "principal": "bd-49f-fees-runner-role",
     "kind": "role",
     "belt": "inline policy bd-49f-fees-runner-policy stmt[4] Sid=DenyCotPlane: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/bd-pipeline/bd-49f-interim.tf",
     "comp_iam": "comp-iam role bd-49f-fees-runner-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read; also carries '49f' in slot 2"
    },
    {
     "principal": "bd-49f-runner-role",
     "kind": "role",
     "belt": "inline policy bd-49f-runner-policy stmt[4] Sid=DenyCotPlane: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/bd-pipeline/bd-49f-interim.tf",
     "comp_iam": "comp-iam role bd-49f-runner-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read; also carries '49f' in slot 2"
    },
    {
     "principal": "bd-exporter-ec2-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmCotBucket: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/ec2/bd-exporter/terraform/main.tf",
     "comp_iam": "comp-iam role bd-exporter-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "bd-silver-merge-role",
     "kind": "role",
     "belt": "inline policy bd-silver-merge-policy stmt[5] Sid=DenyCotPlane: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/bd-pipeline/bd-silver-merge.tf",
     "comp_iam": "comp-iam role bd-silver-merge-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "cot-rebalancer-runner-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/opal-assets/cot_rebalancer_runner.tf",
     "comp_iam": "comp-iam role cot-rebalancer-runner-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-accounts-v2-daily-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-accounts-v2-daily.tf",
     "comp_iam": "comp-iam role inf-accounts-v2-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-assets-v2-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-api-assets-v2.tf",
     "comp_iam": "comp-iam role inf-api-assets-v2-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-positions-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-api-positions.tf",
     "comp_iam": "comp-iam role inf-api-positions-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-reps-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-api-reps.tf",
     "comp_iam": "comp-iam role inf-api-reps-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-api-txn-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-api-txn.tf",
     "comp_iam": "comp-iam role inf-api-txn-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-assets-trigger-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-assets-trigger-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-billing-daily-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-billing-daily.tf",
     "comp_iam": "comp-iam role inf-billing-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-bronze-runner-ec2-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf",
     "comp_iam": "comp-iam role inf-bronze-runner-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-bronze-trigger-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-bronze-trigger-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-ec2-launch-monitor-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-ec2-launch-monitor.tf",
     "comp_iam": "comp-iam role inf-ec2-launch-monitor-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-ec2-retry-launch-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-ec2-retry-launch.tf",
     "comp_iam": "comp-iam role inf-ec2-retry-launch-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-etf-ownership-daily-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-etf-ownership-daily.tf",
     "comp_iam": "comp-iam role inf-etf-ownership-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-eventbridge-ssm-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-eventbridge-ssm-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-exporter-ec2-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-exporter-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-gold-layer-ec2-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-gold-layer-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-gold-layer-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-gold-layer-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-gold-qa-runner-ec2-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-gold-qa-runner.tf",
     "comp_iam": "comp-iam role inf-gold-qa-runner-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-gold-trigger-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-gold-trigger-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-jwt-trigger-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-jwt-trigger-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-nna-partition-checker-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-nna-partition-checker.tf",
     "comp_iam": "comp-iam role inf-nna-partition-checker-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-otp-relay-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/lambda-otp-relay.tf",
     "comp_iam": "comp-iam role inf-otp-relay-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-performance-daily-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-performance-daily.tf",
     "comp_iam": "comp-iam role inf-performance-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-silver-aggregator-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/iam.tf",
     "comp_iam": "comp-iam role inf-silver-aggregator-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-silver-chain-lambda-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-silver-chain.tf",
     "comp_iam": "comp-iam role inf-silver-chain-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-tax-daily-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-tax-daily.tf",
     "comp_iam": "comp-iam role inf-tax-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "inf-unified-account-dim-daily-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-pipeline/inf-unified-account-dim-daily.tf",
     "comp_iam": "comp-iam role inf-unified-account-dim-daily-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'inf' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "lambda-execution-role",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-write-deny stmt[0] Sid=DenyCrossFirmBucketWrites: Deny s3:Put*,s3:Delete* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/shared-infra/lambda-execution-role.tf",
     "comp_iam": "comp-iam role lambda-execution-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-bd49f-daily-pull-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/opal-assets/bd49f_pull.tf",
     "comp_iam": "comp-iam role opal-assets-bd49f-daily-pull-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-bd49f-reporting-pull-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/opal-assets/bd49f_reporting_pull.tf",
     "comp_iam": "comp-iam role opal-assets-bd49f-reporting-pull-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-mdpf-portal-publisher-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/opal-assets/mdpf_portal_publisher.tf",
     "comp_iam": "comp-iam role opal-assets-mdpf-portal-publisher-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-bd49finsurance-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-bd49finsurance-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-blackdiamond-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-blackdiamond-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-eclipse-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-eclipse-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-etf-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-etf-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-orion-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-orion-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-schwab-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-schwab-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-smartx-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-smartx-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-inf-served-guard",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-inf-served-guard: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "inf",
     "token_basis": "scope slot (slot 2) carries the short form 'inf'; last slot 'guard' is not a kind"
    },
    {
     "principal": "opal-inf-value-parity",
     "kind": "role",
     "belt": "inline policy cross-firm-bucket-deny stmt[0] Sid=DenyCrossFirmBuckets: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/inf-value-parity/inf_value_parity.tf",
     "comp_iam": "comp-iam role opal-inf-value-parity: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "inf",
     "token_basis": "scope slot (slot 2) carries the short form 'inf'; last slot 'parity' is not a kind"
    },
    {
     "principal": "opal-schwab-monolith-remap-role",
     "kind": "role",
     "belt": "inline policy opal-schwab-monolith-remap-inline stmt[3] Sid=DenyCotPlane: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/canonical-schwab-ec2/monolith-iam.tf",
     "comp_iam": "comp-iam role opal-schwab-monolith-remap-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "quartz-si2-spike-role",
     "kind": "role",
     "belt": "inline policy quartz-si2-spike-inline stmt[4] Sid=DenyCotPlane: Deny s3:* on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/canonical-schwab-ec2/iam.tf",
     "comp_iam": "comp-iam role quartz-si2-spike-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "smartx-assets-pull-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard) | managed policy opal-assets-one-way-fan-in-fence stmt[1] Sid=DenyMutationOnEnumeratedSourceBuckets: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on arn:aws:s3:::opal-data-cot,arn:aws:s3:::opal-data-cot/* (literal)",
     "tf_source": "infra/aws/terraform/smartx-pipeline/assets-pull-iam.tf",
     "comp_iam": "comp-iam role smartx-assets-pull-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    }
   ],
   "denominators": {
    "granted": 30,
    "seen": 11,
    "belt_only": 47
   }
  },
  "opal-data-49financial": {
   "granted": [
    {
     "principal": "AWSServiceRoleForResourceExplorer",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/aws-service-role/resource-explorer-2.amazonaws.com/AWSServiceRoleForResourceExplorer",
     "grant": "AWS-managed policy AWSResourceExplorerServiceRolePolicy stmt[3] Sid=ResourceInventoryAccess: Allow s3:GetBucketLocation,s3:ListAccessPoints,s3:ListAllMyBuckets,s3:ListBucket,s3:ListMultiRegionAccessPoints,s3:ListStorageLensConfigurations,s3:ListStorageLensGroups on * (wildcard) | AWS-managed policy AWSResourceExplorerServiceRolePolicy stmt[4] Sid=PermissionsForReadGetResources: Allow s3:GetAccelerateConfiguration,s3:GetAccessGrant,s3:GetAccessGrantsInstance,s3:GetAccessGrantsLocation,s3:GetAnalyticsConfiguration,s3:GetBucketAbac,s3:GetBucketAcl,s3:GetBucketCORS,s3:GetBucketLogging,s3:GetBucketMetadataTableConfiguration,s3:GetBucketNotification,s3:GetBucketObjectLockConfiguration,s3:GetBucketOwnershipControls,s3:GetBucketPolicy,s3:GetBucketPublicAccessBlock,s3:GetBucketTagging,s3:GetBucketVersioning,s3:GetBucketWebsite,s3:GetEncryptionConfiguration,s3:GetIntelligentTieringConfiguration,s3:GetInventoryConfiguration,s3:GetLifecycleConfiguration,s3:GetMetricsConfiguration,s3:GetReplicationConfiguration,s3:GetStorageLensGroup,s3:ListAccessGrants,s3:ListAccessGrantsInstances,s3:ListTagsForResource on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role AWSServiceRoleForResourceExplorer: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "none",
     "token_basis": "not kebab-case: the resource grammar does not hold, no firm token"
    },
    {
     "principal": "AWSServiceRoleForSupport",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/aws-service-role/support.amazonaws.com/AWSServiceRoleForSupport",
     "grant": "AWS-managed policy AWSSupportServiceRolePolicy stmt[4] Sid=AWSSupportActionsGroup3: Allow s3:describeJob,s3:describeMultiRegionAccessPointOperation,s3:getAccelerateConfiguration,s3:getAccessGrant,s3:getAccessGrantsInstance,s3:getAccessGrantsInstanceResourcePolicy,s3:getAccessGrantsLocation,s3:getAccessPoint,s3:getAccessPointConfigurationForObjectLambda,s3:getAccessPointForObjectLambda,s3:getAccessPointPolicy,s3:getAccessPointPolicyForObjectLambda,s3:getAccessPointPolicyStatus,s3:getAccessPointPolicyStatusForObjectLambda,s3:getAccountPublicAccessBlock,s3:getAnalyticsConfiguration,s3:getBucketAcl,s3:getBucketCORS,s3:getBucketLocation,s3:getBucketLogging,s3:getBucketNotification,s3:getBucketObjectLockConfiguration,s3:getBucketOwnershipControls,s3:getBucketPolicy,s3:getBucketPolicyStatus,s3:getBucketPublicAccessBlock,s3:getBucketRequestPayment,s3:getBucketVersioning,s3:getBucketWebsite,s3:getEncryptionConfiguration,s3:getIntelligentTieringConfiguration,s3:getInventoryConfiguration,s3:getLifecycleConfiguration,s3:getMetricsConfiguration,s3:getMultiRegionAccessPoint,s3:getMultiRegionAccessPointPolicy,s3:getMultiRegionAccessPointPolicyStatus,s3:getMultiRegionAccessPointRoutes,s3:getObjectAcl,s3:getObjectLegalHold,s3:getObjectRetention,s3:getReplicationConfiguration,s3:getStorageLensConfiguration,s3:listAccessGrants,s3:listAccessGrantsInstances,s3:listAccessGrantsLocations,s3:listAccessPoints,s3:listAccessPointsForObjectLambda,s3:listAllMyBuckets,s3:listBucket,s3:listBucketMultipartUploads,s3:listBucketVersions,s3:listJobs,s3:listMultipartUploadParts,s3:listMultiRegionAccessPoints,s3:listStorageLensConfigurations on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role AWSServiceRoleForSupport: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "none",
     "token_basis": "not kebab-case: the resource grammar does not hold, no firm token"
    },
    {
     "principal": "AWSServiceRoleForTrustedAdvisor",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/aws-service-role/trustedadvisor.amazonaws.com/AWSServiceRoleForTrustedAdvisor",
     "grant": "AWS-managed policy AWSTrustedAdvisorServiceRolePolicy stmt[0] Sid=TrustedAdvisorServiceRolePermissions: Allow s3:GetAccountPublicAccessBlock,s3:GetBucketAcl,s3:GetBucketPolicy,s3:GetBucketPolicyStatus,s3:GetBucketLocation,s3:GetBucketLogging,s3:GetBucketVersioning,s3:GetBucketPublicAccessBlock,s3:GetLifecycleConfiguration,s3:ListBucket,s3:ListAllMyBuckets on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role AWSServiceRoleForTrustedAdvisor: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "belts": [],
     "token": "none",
     "token_basis": "not kebab-case: the resource grammar does not hold, no firm token"
    },
    {
     "principal": "bd-exporter-ec2-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/bd-exporter-ec2-role",
     "grant": "inline policy advi-49f-chain-access stmt[8] Sid=AdviChainGoldRW: Allow s3:GetObject,s3:PutObject on arn:aws:s3:::opal-data-49financial/gold/advi/* (literal) | inline policy advi-49f-chain-access stmt[9] Sid=AdviChainCodeRead: Allow s3:GetObject on arn:aws:s3:::opal-data-49financial/_code/* (literal) | inline policy advi-49f-chain-access stmt[10] Sid=AdviChain49fListScoped: Allow s3:ListBucket on arn:aws:s3:::opal-data-49financial (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/ec2/bd-exporter/terraform/main.tf",
     "comp_iam": "comp-iam role bd-exporter-ec2-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "infrastructure-ops-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/infrastructure-ops-lambda-role",
     "grant": "inline policy infrastructure-ops-permissions stmt[4] Sid=S3BucketEnumeration: Allow s3:ListAllMyBuckets,s3:GetBucketVersioning,s3:GetBucketEncryption,s3:GetBucketLocation,s3:GetBucketPolicy on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/shared-infra/iam_legacy.tf",
     "comp_iam": "comp-iam role infrastructure-ops-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "infrastructure-snapshot-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/infrastructure-snapshot-role",
     "grant": "inline policy InfrastructureSnapshotPolicy stmt[6] Sid=S3BucketRead: Allow s3:ListAllMyBuckets,s3:GetBucketVersioning,s3:GetBucketEncryption on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/shared-infra/iam_legacy.tf",
     "comp_iam": "comp-iam role infrastructure-snapshot-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-advi-stitch-landing-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-advi-stitch-landing-role",
     "grant": "inline policy opal-advi-stitch-landing-scoped stmt[1] Sid=WriteTheThreeLandingPrefixesOnly: Allow s3:PutObject,s3:AbortMultipartUpload,s3:ListMultipartUploadParts on arn:aws:s3:::opal-data-49financial/gold/advi/reference/bd_legacy_* (literal) | inline policy opal-advi-stitch-landing-scoped stmt[4] Sid=ListReferenceLandingOnly: Allow s3:ListBucket,s3:ListBucketMultipartUploads on arn:aws:s3:::opal-data-49financial (literal, conditioned)",
     "grant_match": "literal",
     "tf_source": "infra/aws/terraform/opal-assets/advi_stitch_landing.tf",
     "comp_iam": "comp-iam role opal-advi-stitch-landing-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-drift-producer-codebuild-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-drift-producer-codebuild-role",
     "grant": "AWS-managed policy ReadOnlyAccess stmt[1] Sid=ReadOnlyActionsGroup2: Allow s3:DescribeJob,s3:Get*,s3:List* on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/shared-infra/drift-producer.tf",
     "comp_iam": "comp-iam role opal-drift-producer-codebuild-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [
      "inline policy DriftProducerWritesAndDataDeny stmt[5] Sid=DenyFirmDataObjectReads: Deny s3:GetObject,s3:GetObjectVersion on arn:aws:s3:::opal-data-*/* (wildcard)"
     ],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-globgrph-derive-runner-task",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-globgrph-derive-runner-task",
     "grant": "inline policy DeriveRunnerAccountDescribe stmt[0] Sid=AccountWideReadOnly: Allow s3:GetBucketPolicy,s3:GetBucketVersioning,s3:GetBucketLocation,s3:ListAllMyBuckets on * (wildcard) | inline policy DeriveRunnerBucketNotificationRead stmt[0] Sid=BucketNotificationRead: Allow s3:GetBucketNotification on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/globgrph/item2a.tf",
     "comp_iam": "comp-iam role opal-globgrph-derive-runner-task: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-globgrph-incremental-updater",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-globgrph-incremental-updater",
     "grant": "inline policy BoundedDeriveReadOnly stmt[0] Sid=BoundedDeriveReadOnly: Allow s3:GetBucketPolicy,s3:GetBucketVersioning,s3:GetBucketLocation,s3:ListAllMyBuckets on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/globgrph/iam.tf",
     "comp_iam": "comp-iam role opal-globgrph-incremental-updater: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared); last slot 'updater' is not a kind"
    },
    {
     "principal": "opal-news-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/opal-news-lambda-role",
     "grant": "AWS-managed policy AmazonS3ReadOnlyAccess stmt[0]: Allow s3:Get*,s3:List*,s3:Describe* on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/news-pipeline/iam.tf",
     "comp_iam": "comp-iam role opal-news-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "partners-lambda-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/partners-lambda-role",
     "grant": "inline policy partners-lambda-permissions stmt[0] Sid=ReadPartnerBuckets: Allow s3:GetObject,s3:ListBucket on arn:aws:s3:::opal-data-*,arn:aws:s3:::opal-data-*/* (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/partners-api/iam.tf",
     "comp_iam": "comp-iam role partners-lambda-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "security-sweep-dedicated-role",
     "kind": "role",
     "arn": "arn:aws:iam::313476888478:role/security-sweep-dedicated-role",
     "grant": "inline policy SecuritySweepComprehensive stmt[0] Sid=SecuritySweepReadPermissions: Allow s3:ListAllMyBuckets,s3:GetBucketPublicAccessBlock,s3:GetBucketAcl,s3:GetBucketEncryption,s3:GetBucketVersioning,s3:GetBucketLogging,s3:GetBucketPolicy,s3:ListBucket on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "infra/aws/terraform/security-ops/iam.tf",
     "comp_iam": "comp-iam role security-sweep-dedicated-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "belts": [],
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "Andrew_Berman",
     "kind": "user",
     "arn": "arn:aws:iam::313476888478:user/Andrew_Berman",
     "grant": "group AdministratorAccessOpalCapital AWS-managed policy AdministratorAccess stmt[0]: Allow * on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role: n/a (IAM user)",
     "belts": [],
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "Andrew_Berman_Console",
     "kind": "user",
     "arn": "arn:aws:iam::313476888478:user/Andrew_Berman_Console",
     "grant": "group AdministratorAccessOpalCapital AWS-managed policy AdministratorAccess stmt[0]: Allow * on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role: n/a (IAM user)",
     "belts": [],
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "Opal_Terminal",
     "kind": "user",
     "arn": "arn:aws:iam::313476888478:user/Opal_Terminal",
     "grant": "group AdministratorAccessOpalCapital AWS-managed policy AdministratorAccess stmt[0]: Allow * on * (wildcard)",
     "grant_match": "wildcard",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role: n/a (IAM user)",
     "belts": [],
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    }
   ],
   "seen": [
    {
     "principal": "Andrew_Berman",
     "kind": "user",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:user/Andrew_Berman): first ListObjects 2026-09-14T14:14:37Z requestID 3V5GNE06TWSJT4KX; last ListObjects 2026-09-14T14:18:06Z requestID XAR6ZXTW824D0AQA; 2 event(s) in window: ListObjects x2",
     "in_granted": true,
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "Andrew_Berman_Console",
     "kind": "user",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:user/Andrew_Berman_Console): first HeadBucket 2026-09-14T17:16:24Z requestID 7JF3A1DBNQBJD681; last HeadBucket 2026-09-14T17:16:24Z requestID 7JF3A1DBNQBJD681; 1 event(s) in window: HeadBucket x1",
     "in_granted": true,
     "token": "none",
     "token_basis": "IAM_USER: NOT GRADED (NAMING_SCHEMA.json types_not_graded_by_kind.IAM_USER)"
    },
    {
     "principal": "bd-exporter-ec2-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/bd-exporter-ec2-role): first ListObjects 2026-09-14T12:45:42Z requestID ZC30ESN5JGNF9KRZ; last HeadObject 2026-09-14T12:47:47Z requestID N475KNP071GJC7PN; 206 event(s) in window: GetObject x136, HeadObject x33, ListObjects x37",
     "in_granted": true,
     "token": "none",
     "token_basis": "firm token 'bd' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "opal-drift-producer-codebuild-role",
     "kind": "role",
     "observed": "read",
     "evidence": "opal-organization-trail ReadOnly data event (arn:aws:iam::313476888478:role/opal-drift-producer-codebuild-role): first HeadBucket 2026-09-14T06:46:01Z requestID 1NB9WKXR6CYPJQJ8; last HeadBucket 2026-09-14T06:46:01Z requestID 1NB9WKXR6CYPJQJ8; 2 event(s) in window: HeadBucket x2",
     "in_granted": true,
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    }
   ],
   "belt_only": [
    {
     "principal": "cot-rebalancer-runner-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard)",
     "tf_source": "infra/aws/terraform/opal-assets/cot_rebalancer_runner.tf",
     "comp_iam": "comp-iam role cot-rebalancer-runner-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "firm token 'cot' in the SYSTEM slot (slot 1): 'a firm in the system slot' fails the grammar (grade.OUT-OF-PATTERN), so no scope slot is read"
    },
    {
     "principal": "opal-assets-bd49f-daily-pull-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard)",
     "tf_source": "infra/aws/terraform/opal-assets/bd49f_pull.tf",
     "comp_iam": "comp-iam role opal-assets-bd49f-daily-pull-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-bd49f-reporting-pull-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard)",
     "tf_source": "infra/aws/terraform/opal-assets/bd49f_reporting_pull.tf",
     "comp_iam": "comp-iam role opal-assets-bd49f-reporting-pull-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-ingest-router-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard)",
     "tf_source": "infra/aws/terraform/opal-assets/router_iam.tf",
     "comp_iam": "comp-iam role opal-assets-ingest-router-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-mdpf-portal-publisher-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard)",
     "tf_source": "infra/aws/terraform/opal-assets/mdpf_portal_publisher.tf",
     "comp_iam": "comp-iam role opal-assets-mdpf-portal-publisher-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-bd49finsurance-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-bd49finsurance-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-blackdiamond-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-blackdiamond-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-eclipse-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-eclipse-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-etf-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-etf-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-orion-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-orion-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-schwab-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-schwab-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "opal-assets-silver-smartx-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard)",
     "tf_source": "none in comp-iam's Terraform plane",
     "comp_iam": "comp-iam role opal-assets-silver-smartx-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: no",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    },
    {
     "principal": "smartx-assets-pull-role",
     "kind": "role",
     "belt": "managed policy opal-assets-one-way-fan-in-fence stmt[0] Sid=DenyAnyS3MutationOutsideMonolith: Deny s3:PutObject,s3:PutObjectAcl,s3:PutObjectTagging,s3:PutObjectVersionAcl,s3:DeleteObject,s3:DeleteObjectVersion,s3:DeleteObjectTagging,s3:AbortMultipartUpload,s3:RestoreObject on NotResource:arn:aws:s3:::opal-data-assets,arn:aws:s3:::opal-data-assets/* (wildcard)",
     "tf_source": "infra/aws/terraform/smartx-pipeline/assets-pull-iam.tf",
     "comp_iam": "comp-iam role smartx-assets-pull-role: 'No role matching' (row LGIC_ENFORCE-W2-S1); comp-iam roles lists it: yes",
     "token": "none",
     "token_basis": "no firm token in any slot (a shared resource carries no scope token: resource.scope_when_shared)"
    }
   ],
   "denominators": {
    "granted": 16,
    "seen": 4,
    "belt_only": 13
   },
   "bucket_policy_deny": "bucket policy opal-data-49financial Sid=DenyForeignFirmPrincipals: Deny s3:* on the bucket and its objects to Principal '*' where aws:PrincipalArn ArnLike role/cot-*, role/inf-*, role/mdpf-*, role/opal-assets-mdpf-* (infra/aws/terraform/shared-infra/s3-49financial.tf DenyForeignFirmPrincipals). It names no principal it grants, so it contributes no granted row."
  }
 }
}
```
