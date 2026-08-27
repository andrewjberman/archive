# ADVI_INSURE.TO-A1-AE leg deploy -- the IAM gap, measured on the live primitive

**Seat:** `0.6.0_AE_PartnerETL` · **Raised:** 2026-08-27 ~16:5xZ · **Against:** COO GO 76139 + deploy
ruling 76180 · **Status:** BLOCKING the deploy act; remedy named below; NOT applied.

## The finding

`insurance_leg.py` lands bronze at

    blackdiamond/49financial/bronze/insurance_{surface}/{pull_date}/insurance_{surface}_{disc}.json

The execution role `opal-assets-bd49f-reporting-pull-role` grants `s3:PutObject` on exactly one
prefix (`bd49f_reporting_pull.tf:71`):

    arn:aws:s3:::opal-data-assets/blackdiamond/49f/bronze/reporting_*

`49financial` is not `49f`, and `reporting_*` is not `insurance_*`. **Two independent misses on one
resource string.**

## Coverage -- all FOUR policies on the role, not a sample

| # | policy | S3 Allow? |
|---|---|---|
| 1 | `AWSLambdaBasicExecutionRole` (managed) | no (logs) |
| 2 | `one_way_fan_in_fence` | **Deny-only** -- all 4 statements are `Effect = "Deny"` |
| 3 | `bd49f_reporting_io` (inline) | **the only S3 Allow**; `49f/bronze/reporting_*` + two GetObject paths |
| 4 | `bd49f_reporting_secret` (inline) | no (secretsmanager) |

So the block is the **absence of an Allow**, not the presence of a Deny. The fence is not the
obstacle and must not be loosened.

## Live-primitive evidence (COO condition b method: simulate-principal-policy, ONE --resource-arns, separate positive control)

| arm | action / resource | decision |
|---|---|---|
| **1 -- the claim** | `s3:PutObject` on the leg's ACTUAL landing key | **implicitDeny** |
| **2 -- positive control** | `s3:PutObject` on the granted `49f/bronze/reporting_*` key | **allowed** |
| **3** | `s3:ListBucket` w/ `s3:prefix` = the insurance prefix (the leg's own 13c listing-verify) | **implicitDeny** |

Arm 2 is what makes arms 1 and 3 mean anything -- the instrument returns `allowed` when the grant
exists, so `implicitDeny` is a real absence and not a broken probe.

## Why the prior "EXERCISED" evidence did not catch this

AC1's evidence records a genuine live landing (`exportResultID 282397`, 13,089 bytes,
ListObjectsV2-verified). That run did not execute under this role -- it ran under a local principal.
**It is complete evidence about the CODE and zero evidence about the ROLE.** DESIRED != APPLIED !=
EXERCISED, and the exercised half was exercised as a different subject.

The code-side guard shows the same drift from the other direction: `_ALLOWED_49F_ROOTS` at
`insurance_leg.py:62` was **widened to admit both spellings** (`49financial/` and `49f/`) when the
Ruling-1 tree was minted. The IAM statement that actually enforces firm separation was not widened
with it. **The guard that is prose was updated; the guard that is enforcement was not.**

## Proposed remedy -- scope-exact, mirroring the existing tightness

Add to `bd49f_reporting_io` (NOT a widening of the fence, NOT a whole-tree grant):

```hcl
{
  Sid    = "WriteAndVerifyInsuranceBronze"
  Effect = "Allow"
  Action = ["s3:PutObject", "s3:GetObject"]
  Resource = "arn:aws:s3:::${local.monolith_bucket}/blackdiamond/49financial/bronze/insurance_*"
},
```

and extend the existing `ListOwnReportingBronze` condition prefix list with:

```hcl
"blackdiamond/49financial/bronze/insurance_*"
```

Deliberate properties: stays inside the monolith bucket (fence-compatible); `insurance_*`-scoped so
it cannot write the reporting tree or any sibling; no `s3:Delete*`; keeps `GetObject` for the
read-back verify only.

## What I did NOT do, and why

Did not apply, and did not open the change-management ledger. COO 76180 discipline 5 says do not
open the ledger until the act can run uninterrupted; an unresolved IAM question means it cannot.
Opening it first would manufacture exactly the half-landed deploy NEVER#6 forbids.
