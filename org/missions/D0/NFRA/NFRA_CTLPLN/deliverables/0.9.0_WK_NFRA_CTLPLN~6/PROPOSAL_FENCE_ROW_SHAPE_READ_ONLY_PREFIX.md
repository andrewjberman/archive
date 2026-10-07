# Proposal: a registry row shape for a read-only, prefix-scoped fence exemption

Author: 0.9.0_WK_NFRA_CTLPLN~6, NFRA_CTLPLN.TO-CT-d-2 AMENDMENT 3, 2026-10-07. For `1.0.0_SA_CTO` to rule and the registry's lane to land.
This document proposes. It changes no registry file, no module, no `.tf` file and no part of `lib/opal_naming.py`. Every number below
is printed by `infra/aws/terraform/shared-infra/tests/derive_fence_row_shape.py` (run at HEAD of branch `wk-NFRA_CTLPLN-6`).

## 1. Conclusion

- **Can a row carry an action set and a prefix today? No.** Every one of the 29 rows in `infra/logic/registry/exemptions.json` has the
  one key set `arn, principal, reason, signoff_ref`. No row has an action key or a prefix key, and `_about` never mentions either.
- **Worse, the readers would not refuse the new keys: they would ignore them.** The validator, the module and the join check each
  accept a row with extra `actions` and `prefix` keys, and the module renders it as a full admission. Landing such a row before the
  module learns the new keys would admit `cloudops-dell1-agent-user` to the whole bucket, with put (measured, section 3).
- **The shape needed:** two new optional row fields, `actions` and `prefix`, given together or not at all, plus three rendered Deny
  statements per scoped row (sections 6 and 7). Absent both, a row means exactly what it means today.
- **Prefix:** `irpt/<firm>/platinum/holdings/` where `<firm>` is `49financial`, `cottonwood` and `inflection` for the three buckets.
  The repository shows all three (section 5).
- **Proof:** the three statements, rendered by the proposed HCL in a scratch copy of the module, were run through
  `iam simulate-principal-policy` against a scratch bucket document. 25 of 25 arms matched (section 8).

## 2. The row today

`exemptions.json` `_about.row_fields` reads: `principal` (a role name or an ARN); `arn` (the principal's full ARN, written when it is
not the role ARN of its name); `reason`; `signoff_ref`. Measured: 7 bucket keys, 29 rows, one key set, 29 rows with it.
`rows_with_actions=0 rows_with_prefix=0`. Three rows (the `irpt-holdings-role` row under each fenced bucket) say "prefix-scoped" in their
`reason` text; that scope lives in the role's own identity policy, not in a field.

## 3. Every reader, and what an extra key does

`git grep` over tracked files (markdown, jsonl, `org/`, `docs/` excluded) returns 16 live files, all classified; none is unclassified.
There are also 9 frozen battery scripts under `org/` (delivered fixed inputs of finished rounds).

| Role | File : lines | What an extra key does |
|---|---|---|
| validator | `lib/opal_naming.py:529-540` | **Ignored.** Reads `account_id`; per row requires `principal`, `reason`, `signoff_ref` to be non-empty strings; reads no other key. |
| module | `infra/aws/terraform/modules/opal_name/main.tf:90-95` | **Ignored, row rendered as full admission.** `r.arn` / `r.principal` only. |
| join check | `tests/check_dell_fence_join.py:86-99` (`render_arns`) | **Ignored**, same full-admission render. |
| hash | `lib/opal_naming.py:173-184` `registry_hash` | The bytes change, so the hash changes; see the mark note below. |
| consumers | `s3-49financial.tf:141`, `s3-lgic-firm-buckets.tf:162` | Never see a row; they read the module's ARN list. |
| marks | `generated_locals.tf:1`, `opal_name.tftest.hcl:4`, `vectors.json:2` | Carry a hash only; parse nothing. |
| packagers/manifests | `.tools/safe_deploy_core.py:528`, two `build_package.py`, `harvest/lambda_src/build_zip.py:116`, `build-and-upload-scoped-amgt.sh:240`, `lambda-source-map.json`, two `BUILD_MANIFEST.json` | Copy the file; a new key rides along. |

Measured on a scratch copy of the registry in a temporary directory outside the repository (nothing in the repo edited):

- `validate(<scratch dir>)`: refusals 0 for the unchanged copy; 0 with three dell1 rows carrying `actions` and `prefix`; 0 even with
  `actions` a string and `prefix` an integer. Control: the same rows with `reason` removed give 3 refusals, so the scratch directory
  was the one read. `python lib/opal_naming.py validate --registry-dir <scratch>` exits 0 with `VALIDATE: OK`.
- `terraform console` on a scratch copy of the module reading the scratch registry: `local.fence_exemption_arns` holds the dell1 ARN
  under 3 of 3 buckets. The extra keys are ignored and the row becomes a full admission.
- `check_dell_fence_join.render_arns` on the scratch rows: the dell1 ARN is in the rendered list of 3 of 3 buckets.
- Totals for the last line: `extra_key_ignored=3 extra_key_refused=0`.

**Mark note (a finding, outside the ask).** `registry_hash` over `exemptions.json` + `scopes.json` is `9641c8676ad38b19` now and was
`7cf7580cda2303a3` before commit `e7ac51a04c` (the dell2 rows). `generated_locals.tf:1` still carries `7cf7580cda2303a3`. The same hash
covers `vectors.json` and `opal_name.tftest.hcl`. Any row landed in `exemptions.json` moves these marks, so the three dell1 rows need a
restamp by the generator (`python lib/opal_naming.py generate ...`); the dell2 rows already do. Row `NFRA_CTLPLN-W6-S4` records it.

## 4. The fences, and what plain admission would give

Both fences are one `DenyForeignFirmPrincipals` statement: `Effect Deny, Principal *, Action s3:*`, resource the bucket and `bucket/*`,
condition `ArnNotLike aws:PrincipalArn` over `concat(fence_patterns, fence_exemption_arns[bucket], ...)`:
`s3-49financial.tf:129-145` (list built at :139-143, the exemption terms at :141) and `s3-lgic-firm-buckets.tf:150-166` (list built at
:160-163, exemption terms at :162, one `for_each` resource for the two other buckets). A principal in the list is outside the Deny's
condition, so it gains everything the fence denied, on the whole bucket, limited only by its own identity policy. The statement
grants nothing itself.

dell1's own policies (`nfra-ctlpln-identity`: group deploy, create and respol documents, plus the per-user bus document) allow, on
`arn:aws:s3:::opal-*` and `opal-*/*`: `s3:GetObject`, `GetObjectVersion`, **`PutObject`**, `ListBucket`, `GetBucketLocation`,
`ListBucketVersions`, `GetBucket*` (`dell_deploy_policy.json` stmt `S3ObjectsOnOpalBuckets`), and `PutObjectTagging` and bucket-level
tagging and configuration puts (`dell_create_policy.json` stmt `CreateUpdateTagS3OnOpalBuckets`). It denies `DeleteObject*`,
`DeleteBucket*` and `PutLifecycleConfiguration` on `opal-data-*` (`DenyS3DeletesOnProductionData`) and `s3:PutBucketPolicy`
(`DenyResourcePolicyWrites`). The evaluator agrees on plain admission (cottonwood, scratch document = saved policy + dell1 in the list):
get allowed, **put allowed**, put outside the prefix allowed, list allowed, delete explicitDeny. **So plain admission is not read-only.**

## 5. The prefix

`irpt/<firm>/platinum/holdings/`, with `<firm>` the scope's `long` form in `infra/logic/registry/scopes.json`, from the builder
`lib/opal_naming.key("irpt", <firm>, "platinum", "holdings", "date=...")`:

| bucket | `<firm>` token | prefix |
|---|---|---|
| `opal-data-49financial` | `49financial` | `irpt/49financial/platinum/holdings/` |
| `opal-data-cottonwood` | `cottonwood` | `irpt/cottonwood/platinum/holdings/` |
| `opal-data-inflection` | `inflection` | `irpt/inflection/platinum/holdings/` |

Where the repository writes it: `infra/aws/terraform/investor-reporting/holdings/main.tf:75,77` (`${holdings_source}/${f.long}/platinum/holdings/...`,
`holdings_source` = the systems.json key `irpt`); the writer builds the address through the same builder
(`infra/aws/lambda/investor-reporting/holdings/publication.py:136-141`, table `holdings`); the `irpt-holdings-role` rows in
`exemptions.json` (:111, :146, :178) name the same path for each bucket. The test fixture
`intake/tests/test_custody_interpreter_firms.py:92` pairs the firm token `inflection` with a legacy bucket name, so the key path
token for `inflection` is read from the registry and the writer, not from that fixture. A QA run writes table `holdings_qa`; the
trailing slash of the prefix excludes it. No bucket was listed and no object read.

## 6. THE ROW SHAPE NEEDED

Two new optional fields on an `exemptions.json` row:

| field | type | meaning |
|---|---|---|
| `actions` | non-empty list of strings | the S3 actions the exemption is limited to |
| `prefix` | string | the key prefix the exemption is limited to |

**Defaults.** Both absent = today's meaning (whole bucket, every action). Every existing row is unchanged byte for byte.

**Validator rule** (an addition to `validate()` beside :536-540; prototyped in `derive_fence_row_shape.py` `scoped_rule`, which accepts
the three rows below and refuses both controls):

1. `actions` and `prefix` come together or not at all.
2. `actions` is drawn from the closed read set `s3:GetObject`, `s3:GetObjectVersion`, `s3:ListBucket`, `s3:ListBucketVersions`. A write
   action is refused: this proposal proves no rendering for one.
3. `prefix` is a literal key prefix: ends in `/`, does not start with `/`, contains no `*` or `?`.
4. The row names ONE principal by its exact ARN (`arn` present, or `principal` an ARN), no `*` or `?`: the statements below match it
   with `ArnLike`, so a wildcard would widen them.
5. The prefix's second path segment is the `long` form of the bucket's firm scope. This is what stops a prefix of one firm riding on
   another firm's bucket: the cross-firm law enforced at the registry.
6. A principal has at most one row per bucket (an unscoped and a scoped row for one principal are refused as a duplicate).

## 7. What each fence must render for a scoped row

The row still renders into `fence_exemption_arns` (the user MUST be in the admitted list, or the fence's Deny still applies to it). In
addition, three Deny statements per scoped row are appended to the bucket policy. Rendered for the cottonwood bucket and the dell1 row
(this JSON is `terraform console` output of the proposed HCL, run on a scratch copy of the module):

```json
[
  {
    "Sid": "DenyScopedExemption1AnyOtherAction",
    "Effect": "Deny",
    "Principal": "*",
    "NotAction": ["s3:GetObject", "s3:ListBucket"],
    "Resource": ["arn:aws:s3:::opal-data-cottonwood", "arn:aws:s3:::opal-data-cottonwood/*"],
    "Condition": {"ArnLike": {"aws:PrincipalArn": ["arn:aws:iam::313476888478:user/cloudops-dell1-agent-user"]}}
  },
  {
    "Sid": "DenyScopedExemption1ObjectsOutsidePrefix",
    "Effect": "Deny",
    "Principal": "*",
    "Action": ["s3:GetObject"],
    "NotResource": ["arn:aws:s3:::opal-data-cottonwood/irpt/cottonwood/platinum/holdings/*"],
    "Condition": {"ArnLike": {"aws:PrincipalArn": ["arn:aws:iam::313476888478:user/cloudops-dell1-agent-user"]}}
  },
  {
    "Sid": "DenyScopedExemption1ListingOutsidePrefix",
    "Effect": "Deny",
    "Principal": "*",
    "Action": ["s3:ListBucket"],
    "Resource": ["arn:aws:s3:::opal-data-cottonwood"],
    "Condition": {
      "ArnLike": {"aws:PrincipalArn": ["arn:aws:iam::313476888478:user/cloudops-dell1-agent-user"]},
      "StringNotLike": {"s3:prefix": ["irpt/cottonwood/platinum/holdings/*"]}
    }
  }
]
```

**Why three statements, and `NotAction` plus `NotResource`.** `s3:ListBucket` is a bucket-level action: its resource is the bucket ARN
and the prefix is tested with the `s3:prefix` condition key. `s3:GetObject` is object-level: its resource is `bucket/key`. A single
`NotResource` Deny cannot serve both: the bucket ARN is outside `bucket/<prefix>*`, so it would deny every list, and leaving the bucket
ARN in `NotResource` would exempt every bucket-level action from the Deny. `s3:prefix` does not exist on a `GetObject` request, so a
`StringNotLike` on it would deny every get. A statement carries `Action` or `NotAction`, never both, so "everything but these two" and
"these two, outside their scope" cannot share one statement. The form is the one `s3-49financial.tf:147-176` already uses for the
performance adapter role (`DenyPerformanceAdapterAnyOtherAction`, `...ReadsOutside...`, `...ListingOutside...`); that precedent types
the role and prefix in the `.tf`, this proposal renders them from the row. The strict two-statement form the ruling's wording suggests
is therefore not reachable without the third.

The `Action` / `NotResource` and `Action` / list statements are rendered only when the row's `actions` hold an object-level or a
bucket-level action respectively. The statement names are `DenyScopedExemption<N>...`, N the position of the row among the bucket's
scoped rows (1-based); adding a second scoped row to a bucket later adds N=2 and leaves N=1 unchanged.

## 8. Proof with the simulator

Scratch document per bucket = the bucket's SAVED live policy from `tests/dell_fence_census.json` (generated by
`dell_fence_census.py --live` earlier today; a saved copy, not the live policy; it predates the dell2 applies) + the rendered admitted list
(`fence_exemption_arns`, so dell1 and dell2 added) + the rendered statements. Identity side: `iam simulate-principal-policy` evaluates the
user's live attached policies (the matched identity statement is `cloudops-dell-agent-deploy-policy`); it was not diffed against the
repo copies of those documents. Cottonwood is the primary bucket (full arm set, with a plain-admission control column); the other two
buckets run the five core arms plus dell2.

Cottonwood, `s3:prefix` passed as a context entry:

| arm | plain admission | with statements | deciding policy |
|---|---|---|---|
| 1 dell1 `GetObject` under the prefix | allowed | **allowed** | identity |
| 2 dell1 `GetObject` outside the prefix | allowed | **explicitDeny** | Resource Policy |
| 3 dell1 `PutObject` under the prefix | allowed | **explicitDeny** | Resource Policy |
| 4 dell1 `ListBucket`, `s3:prefix` = the prefix | allowed | **allowed** | identity |
| 5 dell1 `ListBucket`, no `s3:prefix` | allowed | **explicitDeny** | Resource Policy |
| 5b `ListBucket`, `s3:prefix` a date partition under it | allowed | allowed | |
| 5c `ListBucket`, `s3:prefix` outside | allowed | explicitDeny | Resource Policy |
| 5f `ListBucket`, `s3:prefix` = empty string | allowed | explicitDeny | Resource Policy |
| 5d `GetObject` on another firm's holdings key | allowed | explicitDeny | Resource Policy |
| 5e `GetObjectVersion` under the prefix | allowed | explicitDeny | Resource Policy |
| 6 dell2 (unscoped row) `GetObject` outside | allowed | allowed | unchanged |
| 6b dell2 `PutObject` | allowed | allowed | unchanged |
| 6c dell2 `ListBucket`, no prefix | allowed | allowed | unchanged |

The 49financial and inflection scratch documents give the same decisions on arms 1-6 (25 of 25 arms matched in all). The
49financial document already carries three adapter-role Deny statements; they do not interact.

**What the simulator could not show.** (a) It takes `s3:prefix` as a value the caller supplies; it does not derive it from a real
list request. I passed the key absent (arm 5) and as the empty string (5f); both are refused, which covers the two ways real S3 can
present a list with no prefix, but the real request path was not exercised (no bucket listing was permitted). (b) It does not evaluate
organization policies or object ACLs. (c) It cannot show that a real `get-object` under the prefix returns bytes; the post-apply
read-back (get under the prefix succeeds, get outside and a put are refused) is the live test, and needs one real object and the
apply, both outside this pass.

**Consequence of "get and list only".** dell1 is refused `GetBucketLocation`, `GetBucketPolicy`, `HeadBucket` without a prefix (it is
`ListBucket` without `s3:prefix`), `GetObjectVersion`, `ListBucketVersions`, tagging, and every other S3 action on these buckets. A
client that heads the bucket or lists its root will be refused; one that lists with `Prefix=irpt/<firm>/platinum/holdings/` and reads
under it works. A Terraform plan on dell1 touching these buckets would be refused their bucket reads. If the CTO wants
`s3:GetBucketLocation` added to the permitted set, it is an `actions` entry plus one line in the validator's closed set.

## 9. The three rows as they would be written

Under the keys of the three fenced buckets, appended after each bucket's last row (existing rows unchanged). The `signoff_ref` paths
are PROPOSED names following the dell2 rows' pattern; the issuer fixes them, as for dell2.

```json
{
  "principal": "cloudops-dell1-agent-user",
  "arn": "arn:aws:iam::313476888478:user/cloudops-dell1-agent-user",
  "reason": "The dell1 box's agent identity; reads irpt/cottonwood/platinum/holdings/* in opal-data-cottonwood and nothing else, s3:GetObject and s3:ListBucket only (its own policy allows put on opal-*, so this row carries the scope); NFRA_CTLPLN CT-d-2 AMENDMENT 3; CTO msg 106185.",
  "signoff_ref": "org/critical_paths/change_management/ entry slug nfra-ctlpln-dell1-fence-join-scoped-laptop-20261007 (opened at the apply); COO half org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL1_FENCE_JOIN_SCOPED_20261007.md; CTO half org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL1_FENCE_JOIN_SCOPED_20261007.md",
  "actions": ["s3:GetObject", "s3:ListBucket"],
  "prefix": "irpt/cottonwood/platinum/holdings/"
}
```

The other two rows differ only in the bucket named in `reason` and in `prefix`: `irpt/49financial/platinum/holdings/` under
`opal-data-49financial`, `irpt/inflection/platinum/holdings/` under `opal-data-inflection`. The script prints all three in full.

## 10. Lines that would change (by reading)

| File | Lines | Change |
|---|---|---|
| `infra/aws/terraform/modules/opal_name/main.tf` | after :96 | add the `locals` block `fence_scoped_rows`, `fence_scoped_principal`, `fence_scoped_statements` (the HCL held in `derive_fence_row_shape.py` `PROPOSED_HCL`; `terraform validate` on a scratch copy: Success) |
| `infra/aws/terraform/modules/opal_name/main.tf` | after :101 | add `output "fence_scoped_statements"`. Lines :89-96 and :98-101 are unchanged: scoped rows keep rendering into `fence_exemption_arns`. |
| `infra/aws/terraform/shared-infra/s3-49financial.tf` | :127 and :177 | `Statement = [ ... ]` becomes `Statement = concat([ ... ], module.opal_name.fence_scoped_statements[aws_s3_bucket.opal_data_49financial.bucket])` |
| `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf` | :149-170 | a third argument to the existing `concat(`, after :169: `lookup(module.opal_name.fence_scoped_statements, aws_s3_bucket.lgic_firm[each.key].bucket, [])` |
| `lib/opal_naming.py` | beside :536-540 | the validator rule of section 6; a constant for the closed action set beside :54-:60 |
| `lib/opal_naming.py` generator | `_gen_locals` :1003-1029 | no change (nothing generated is added); a regenerate restamps the marks of `generated_locals.tf:1`, `vectors.json:2`, `opal_name.tftest.hcl:4` |
| `infra/logic/registry/exemptions.json` | `_about.row_fields` :4 | add the two optional fields to the text; then the three rows |

## 11. What the plan for each bucket would show (by reading; no plan was run)

After the module and the two `.tf` edits and the three rows, per bucket: one `aws_s3_bucket_policy` updated in place (`~`), no resource
added or destroyed: `aws_s3_bucket_policy.opal_data_49financial`, `aws_s3_bucket_policy.lgic_firm["cottonwood"]`,
`aws_s3_bucket_policy.lgic_firm["inflection"]`. In each policy: the `DenyForeignFirmPrincipals` condition list gains one entry (the dell1
ARN) and `Statement` gains three entries, `DenyScopedExemption1AnyOtherAction`, `...ObjectsOutsidePrefix`, `...ListingOutsidePrefix`.
The computation (module rule against the saved documents, dell2 entry set aside) is printed by the script. The order stated for this
pass says two of the three live policies changed since the census by one admitted principal each; the live policies were not read, so
a real plan may show that entry too. Policy size stays far under the 20,480-byte bucket-policy limit (the saved documents are 2,513
bytes for 49financial and 501 for each of the others; the three statements for one row are 954 bytes compact).

## 12. Landing order, and the alternative that cannot fail open

**Hazard (measured, section 3):** a scoped row read by a reader that does not know the new fields is read as a full admission. The
module today is such a reader. The order therefore is: (1) the module's new locals and output, and the two `.tf` edits, in one apply
that carries no scoped row (plan: no change); (2) the validator rule; (3) the three rows and the restamp, in the same apply that
renders their statements. A reviewer should reject any plan that shows the dell1 ARN in a `DenyForeignFirmPrincipals` list without the
three `DenyScopedExemption1...` statements beside it. The extended join check should assert that pairing on the rendered document.

**Alternative (B), not proposed but offered for the ruling:** a sibling top-level key `scoped_exemptions` (per bucket, the same row plus
`actions` and `prefix`) read only by the new module code. An unaware reader never sees it, so landing the rows early fails closed (dell1
stays denied). Cost: a second array to validate and to render into the admitted list, and the fence's `concat` gains a second ARN
source. Option A (this proposal) matches the CTO's wording ("an exemptions.json row carry an action set and a prefix") and needs
fewer lines; B removes the order dependence.

## 13. Not done, by bound

No registry, module, `.tf` or `lib/` file was edited. No `terraform plan` or apply. No listing of any firm bucket, no object read. The
AWS calls were `sts get-caller-identity` and `iam simulate-principal-policy`. Terraform was run only as `init -backend=false`,
`validate` and `console` inside temporary directories outside the repository.
