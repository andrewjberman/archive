# ADVI_COTBKF CB-bi-2 -- shared-infra plan proof, round 61

**Seat:** `0.7.0_AE_CloudOps~CB2` | **Order:** `ADVI_COTBKF.TO-CB-bi-2` (AMENDMENT 1 @`6d616df83c`) |
**Ruling proved against:** `1.0.0_SA_CTO~DELL2` @`27ba4d3769`, item 5 | **Date:** 2026-10-11T06:35Z | **Box:** dell2

## VERDICT: STOPPED on step 4. No apply made, and none is proposed.

The selector fix works. The `one()` defect is cleared and the CRM statements themselves are DELTA=0.
But the plan is not 0-change over item 5's named set: **the break-glass role and its inline policy plan to
CREATE**, because they exist only in code and have never been applied. `CB61bi2-AC1` therefore reads
`watched_changed=2` against `<expect>watched_changed=0</expect>` and **FAILS as written**. Step 4 and the
refusal clause both route this to `1.0.0_SA_CTO~DELL2` as a never-widen act, so it is routed and not graded here.

## 1. The `CRM-PLAN` line

```
CRM-PLAN resources=242 watched=12 watched_changed=2 other_changed=2
```

The **watched count is 12, not 0** -- so this is not the failed read the criterion warns about. Stable across
two independent plan runs of the same commit.

## 2. The watched addresses, all 12 of 12, with their actions

| action | address |
|---|---|
| **create** | `aws_iam_role.restricted_breakglass` |
| **create** | `aws_iam_role_policy.restricted_breakglass` |
| no-op | `aws_s3_bucket_policy.lgic_firm["cottonwood"]` |
| no-op | `aws_s3_bucket_policy.lgic_firm["inflection"]` |
| no-op | `aws_s3_bucket.lgic_firm["cottonwood"]` |
| no-op | `aws_s3_bucket.lgic_firm["inflection"]` |
| no-op | `aws_s3_bucket_public_access_block.lgic_firm["cottonwood"]` |
| no-op | `aws_s3_bucket_public_access_block.lgic_firm["inflection"]` |
| no-op | `aws_s3_bucket_server_side_encryption_configuration.lgic_firm["cottonwood"]` |
| no-op | `aws_s3_bucket_server_side_encryption_configuration.lgic_firm["inflection"]` |
| no-op | `aws_s3_bucket_versioning.lgic_firm["cottonwood"]` |
| no-op | `aws_s3_bucket_versioning.lgic_firm["inflection"]` |

**The CRM restricted-prefix statements are not a resource of their own** -- they are inline statements inside
`aws_s3_bucket_policy.lgic_firm["cottonwood"]`, which reads **no-op**. That is the part of item 5 that holds
cleanly: the thing the selector feeds did not move. `data.aws_iam_user.restricted_console` matches the watched
pattern but is a data source, so it appears in no `resource_changes` row -- the preflight's own named BLIND.

## 3. Why the break-glass create is not a resource the selector change moved

Three independent reads, each with a control:

- **terraform state:** 253 rows, **0** match `breakglass`. Positive control on the same state: **10** rows match
  `lgic_firm`. So the instrument reads this state fine; the role is simply not in it.
- **live IAM:** `get-role cloudops-cot-restricted-breakglass-role` -> `NoSuchEntity`. Isolated positive control,
  same credentials: `get-role demo-transform-runner-ec2-role` -> `arn:aws:iam::313476888478:role/demo-transform-runner-ec2-role`.
  ABSENT is therefore the world, not the instrument.
- **in-plan control:** 15 `aws_iam_role` resources in the plan; **14 read no-op** against live. Only
  `restricted_breakglass` reads create.

So the role has never been applied. The create is pre-existing undeployed code from cell `CB-d-4`, not a delta the
selector introduced. **This is material for the CTO, not a conclusion drawn here:** the criterion is written as a
flat `watched_changed=0` and it reads 2, and item 5 names the break-glass role among the resources that must read
0 changes. Whether item 5 is satisfied by "the statements did not move, the role was never deployed" is the CTO's
call. Row `ADVI_COTBKF-D2-S91` carries it.

## 4. The plan's own summary lines

| run | rc | summary |
|---|---|---|
| refreshing (the criterion's artifact) | **1** | `Plan: 4 to add, 0 to change, 1 to destroy.` |
| `-refresh=false`, same commit | **0** | `Plan: 2 to add, 0 to change, 0 to destroy.` |

## 5. The control of step 2 -- RUN HERE, not cited from site Z

Detached control worktree `C:/dev/wk-cotbkf-bi2ctl` at the branch's base `28fbb42d46`. At that commit
**`terraform init` itself fails, rc=1**:

```
Error: Invalid function argument

  on s3-lgic-firm-buckets.tf line 197, in locals:
 197:   lgic_crm_scope  = one([for k, s in local.lgic_managed_firm_buckets : s if length(lookup(s, "masters", [])) > 0])
    |
    | while calling one(list)
    | local.lgic_managed_firm_buckets is object with 2 attributes

Invalid value for "list" parameter: must be a list, set, or tuple value with
either zero or one elements.
```

Two notes for the record. First, the failure is at **`init`**, earlier than the ruling's "init and plan" phrasing
implies -- so the defect never reaches a plan at all. Second, the selected set is **2**, not the 3 the ruling
counts: only two FIRM rows are *managed* by this root (cottonwood, inflection), and both carry `masters`. Two is
still more than one, so `one()` fails either way; the ruling's conclusion is unaffected.

## 6. Every other planned change, by address

2 of 2, and **neither is drift**:

- `aws_s3_bucket.opalinvest_portal` -- create (plan also prints `has been deleted`)
- `aws_s3_bucket_server_side_encryption_configuration.opalinvest_portal` -- must be replaced

Both are **artifacts of this box's credentials**, not of the estate. The plan carries exactly 2 `Error:` blocks,
both naming `User: arn:aws:iam::313476888478:user/cloudops-dell2-agent-user`:

- `cur:ListTagsForResource` on `arn:aws:cur:us-east-1:313476888478:definition/opal-cur` (400 AccessDeniedException)
- `s3:GetBucketPublicAccessBlock` on `arn:aws:s3:::opalinvest-portal` (403 AccessDenied)

**The bucket exists.** `head-bucket opalinvest-portal` -> **403 Forbidden**; `head-bucket` on a deliberately
nonexistent name -> **404 Not Found**. The two codes discriminate, so `has been deleted` is false. `list-objects-v2`
on the same bucket -> `AccessDenied` on `s3:ListBucket`, the second missing grant. And at the same commit,
`plan -refresh=false` drops both changes entirely -- which is what identifies them as refresh output.

> **An apply of the refreshing plan from this box would try to recreate a live bucket and replace its SSE config.**
> Row `ADVI_COTBKF-D2-S92` files this ARMED, owner `1.0.0_SA_CTO~DELL2`. It is not disarmed by this seat: the
> disarm is either the two IAM grants on the dell2 agent user, or a standing rule that shared-infra is not
> planned-for-apply from dell2, and both are the CTO's. Until then the sound read of this root on this box is
> `plan -refresh=false`, and **no shared-infra plan taken on dell2 is an apply instrument.**

## 7. Did `init` download anything?

**Yes.** At `84457822bb`: `Installed hashicorp/aws v5.100.0 (unauthenticated)`, reusing the version in the lock
file. No `.terraform` existed for this root in any checkout on this box beforehand. The download was permitted and
nothing was worked around, so step 1's STOP condition did not fire. The backend (`s3`, key `shared-infra/tfstate`)
configured successfully and 4 modules initialized.

## 8. Bounds honoured

No `terraform apply`. No state verb -- `terraform state list` is a read. No AWS write. No push, no merge of
`wk-ADVI_COTBKF-88`. `C:/dev/wk-cotbkf-80` was confirmed at `84457822bb` before `init` and not otherwise touched
(`init` created a gitignored `.terraform/` there). Plan files and their JSON live outside the repo at
`C:/dev/_cotbkf_private_evidence_20261009/r61/`. `<status>` was NOT flipped: the acceptance was not met.

## 9. One declared departure: the row ids

The face prescribes `ADVI_COTBKF-D2-WCB2-S<k>`. Measured at HEAD against the live `SURPRISE_ID_RE`
(`.tools/proof-of-spec-check.py:1212`): `ADVI_COTBKF-D2-WCB2-S2` is **REJECTED**, `ADVI_COTBKF-D2-S91` **PARSES**.
Row `ADVI_COTBKF-D2-WCB2-S1` already records this exact wall and filed in the project's non-worker namespace for
the same reason; these rows follow that precedent as **`D2-S91`** and **`D2-S92`** rather than being renamed
silently or left unfiled. The fix is the issuer's, in the clause or in the regex.

## Evidence files (outside the repo, as the face requires)

`C:/dev/_cotbkf_private_evidence_20261009/r61/`

| file | bytes | what it is |
|---|---|---|
| `shared_infra_plan.json` | 1,212,652 | the criterion's artifact (refreshing plan, JSON) |
| `shared_infra.tfplan` | 201,499 | its plan file |
| `branch_plan_refresh.txt` | 35,385 | full stdout of the refreshing plan, both errors |
| `shared_infra_plan_norefresh.json` | 1,208,525 | `-refresh=false` plan, JSON |
| `shared_infra_norefresh.tfplan` | 200,786 | its plan file |
| `branch_plan_norefresh.txt` | 5,919 | full stdout, rc=0 |
| `ctl_init.txt` | 782 | the step-2 control, `one()` error verbatim |
| `ctl_plan.txt` | 468 | control plan (plugins absent -- init never completed) |
| `state_list.txt` | 12,353 | 253 state rows, the breakglass/lgic_firm denominators |
