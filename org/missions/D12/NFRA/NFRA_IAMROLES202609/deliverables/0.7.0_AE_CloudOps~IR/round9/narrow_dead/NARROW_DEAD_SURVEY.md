# IAM-z-1 PHASE A -- the five dead names: reference census, four acts, four plans

**Seat:** `0.7.0_AE_CloudOps~IR` - **Order:** `NFRA_IAMROLES202609.TO-IAM-z-1` - **Risk:** WORLD
**Read time:** 2026-10-11 22:0xZ - 2026-10-12 00:4xZ. Every live value below was measured in that window.
**Standing (Z-S40):** this survey names its read time; each act re-reads its baseline before it applies.
**Worktree:** `C:/tmp/iam-r9-z1`, branch `wk-iamroles-r9-z1`, cut from `box/sitez` HEAD (verified equal).
**PHASE A committed:** this survey + 10 rollback documents + 1 after-document. **No edit is committed.**

---

## 1. THE REFS BLOCK (step 1)

```
REFS: workspace-sync-lambda-role ajb-workflow: env=0 code=0
REFS: workspace-sync-lambda-role opal-data-portal-s3: env=0 code=0
REFS: infrastructure-ops-lambda-role opal-data-smartx-v2: env=0 code=0
REFS: smartx-exporter-role-20251218220948293500000001 opal-data-smartx-v2: env=0 code=34
REFS: smartx-exporter-role-20251218220948293500000001 opal-data-smartx: env=0 code=12
REFS: smartx-ingestion-lambda-role opal-data-smartx-v2: env=0 code=23
REFS: FredIngestionLambdaRole opal-market-update: env=0 code=2
```

Seven `(role, bucket)` pairs, not five: `opal-data-smartx-v2` is granted on three roles and
`opal-data-smartx` on one, so the five names make seven grants. Code was read through the EC2 manifest's
`source_path` and the Lambda source map's declared `files[]`, never by filename glob.

### Every `env=0` with its cause named, because a bare zero reads as "no problem"

| pair | why env=0 |
|---|---|
| `workspace-sync-lambda-role` x2 | **0 functions on the role.** The env plane is EMPTY, not clean |
| `infrastructure-ops-lambda-role` | **0 functions on the role**; `RoleLastUsed` **None** -- never assumed since creation 2026-02-19 |
| `smartx-exporter-role...` x2 | an **EC2 instance role**: there is no API-visible environment. See the caveat below |
| `smartx-ingestion-lambda-role` | **0 of 3** live env keys reference it (`DISABLE_PORTAL_AUM_TIMESERIES_WRITE`, `DISABLE_PORTAL_AUM_METRICS_WRITE`, `DISABLE_PORTAL_BELL_WRITE`) |
| `FredIngestionLambdaRole` | **0 of 0** keys -- `Environment` reads `null`, `length(...)` = 0 |

> **The `env=0` for the two exporter pairs is the weakest number in this survey and I am not letting it
> stand bare.** An EC2 instance has no environment the AWS API can return, so "env=0" there means *the
> instrument cannot see this plane*, not *there is no reference*. And there **is** one:
> `infra/aws/ec2/smartx-exporter/config/production.env:9` sets `S3_BUCKET=opal-data-smartx-v2`. It is
> counted in `code=34` because `.env` is in the files I read. So for the exporter the honest reading is
> **env=0 on the API plane, 1 reference in a deployed env FILE**, and the `code` figure is carrying it.

**The two roles with no consumer were established, not assumed.** `comp-kuzu` over the served graph:
`MATCH (n:CloudNode) WHERE n.node_type='LAMBDA' AND n.props CONTAINS '<role>' RETURN n.name` returns
**0 rows** for both `workspace-sync-lambda-role` and `infrastructure-ops-lambda-role`. That zero is only
worth something because the **same query shape** returns `opal-smartx-ingestion-pipeline` for
`smartx-ingestion-lambda-role` -- the instrument works, so the 0 is a measurement rather than a
wrong-pattern artifact. (Graph vintage: built 2026-10-11 16:09:59 UTC, manifest `99086e337200`.)

### Positive control per role, as the cell requires

| role | live bucket its own code really uses | found |
|---|---|---|
| `smartx-exporter-role...` | `opal-data-portal-v2` | **15** |
| `smartx-ingestion-lambda-role` | `opal-data-portal-v2`, `opal-data-mdpf` | **29**, **6** |
| `FredIngestionLambdaRole` | `opal-data-portal-v2` | **3** |
| `workspace-sync-lambda-role` | -- | **NONE FOUND -- this plane cannot be read for this role** |
| `infrastructure-ops-lambda-role` | -- | **NONE FOUND -- this plane cannot be read for this role** |

For the last two there is no control because there is no code to read, and I say so rather than printing
a 0 that looks like coverage. Their evidence is the graph query plus `RoleLastUsed`, not a census.

---

## 2. THE FINDING THAT CHANGES AN ACT: `opal-data-smartx` IS A LIVE DYNAMODB TABLE

`comp-find --corpus aws 'opal-data-smartx'` -> **1 hit across 2891 aws nodes**, band `DYNAMODB_TABLE=1`:

```
[DYNAMODB_TABLE] opal-data-smartx   drift=LIVE-no-DECLARED  src=full-derive
  arn:aws:dynamodb:us-east-1:313476888478:table/opal-data-smartx   {"billing_mode": "PAY_PER_REQUEST", ...}
```

So the name is **dead as an S3 bucket and live as a DynamoDB table**. Two consequences:

**(a) `code=12` for that pair splits 10 DynamoDB / 2 S3, and the 2 are documentation.** Classified per hit:

| class | n | what they are |
|---|---|---|
| DYNAMODB | **10** | `DYNAMODB_TABLE = "opal-data-smartx"` in 7 scripts, plus `os.environ.get('DYNAMODB_TABLE', 'opal-data-smartx')`, a `load_historical_timeseries_from_dynamodb` default, and a `print(" DynamoDB table: opal-data-smartx ...")` |
| S3 | **2** | both inside docstrings: a usage line `python generate_smartx_timeseries_and_metrics.py --bucket opal-data-smartx...` and `S3_BUCKET: S3 bucket containing consolidated data (default: opal-data-smartx)` |

**A merged `code=12` would read as "this role still uses the dead bucket twelve times."** It does not. It
uses a live table ten times and documents an old bucket twice. z-1's act is scoped to *S3 bucket ARNs*,
so removing `arn:aws:s3:::opal-data-smartx` and `/*` breaks **nothing** in this code.

**(b) `aws_iam_role_policy.ingestion_dynamodb` ("smartx-dynamodb-access") MUST NOT BE TOUCHED.** Its one
statement grants six DynamoDB actions on
`arn:aws:dynamodb:${local.region}:${local.account_id}:table/opal-data-smartx`
(`smartx-pipeline/iam.tf:93`). A name-based narrowing would have deleted a grant on a live table and
broken the smartx ingestion pipeline. It is **absent from both plans below**, which is the check that
proves it is untouched rather than the claim that it is.

`opal-data-smartx` is also a strict **prefix** of `opal-data-smartx-v2`, so a naive count of the shorter
name double-counts every hit of the longer one. Every regex here carries a right boundary that rejects
`-v2`; an earlier loop of mine without it reported `opal-data-smartx x1` inside
`infrastructure-ops-permissions`, which is really the single `opal-data-smartx-v2/*` ARN counted twice
under two names. **The cell's grant list is correct and my first reading of it was not.**

---

## 3. THE FIVE NAMES, RE-READ LIVE (step 2)

`s3api get-bucket-location` per name, reading the error **CODE** (not a HEAD status -- the x-2 lesson):

| name | rc | code |
|---|---|---|
| `ajb-workflow` | 254 | `NoSuchBucket` |
| `opal-data-portal-s3` | 254 | `NoSuchBucket` |
| `opal-data-smartx-v2` | 254 | `NoSuchBucket` |
| `opal-market-update` | 254 | `NoSuchBucket` |
| `opal-data-smartx` | 254 | `NoSuchBucket` |
| **control** `opal-data-portal-v2` | **0** | -- |
| **control** `opal-data-bd` | **0** | -- |

All five absent as S3 buckets; two live controls return rc=0 in the same run, so the 254s are the world
and not a broken credential.

**Rollback documents saved** to `.../round9/narrow_dead/` -- **10 files**, every policy on all four roles,
including the five I must not touch (so a rollback restores the whole role, not just the edited policy):

| file | stmt | ARN |
|---|---|---|
| `ROLLBACK_workspace-sync-lambda-role_workspace-sync-permissions.json` | 10 | 19 |
| `ROLLBACK_infrastructure-ops-lambda-role_infrastructure-ops-permissions.json` | 13 | 15 |
| `ROLLBACK_smartx-exporter-role-...-s3-access.json` | 3 | 6 |
| `ROLLBACK_smartx-exporter-role-...-{ecr-access,lambda-invoke,secrets-access,self-shutdown}.json` | 2,1,2,1 | 2,1,4,1 |
| `ROLLBACK_smartx-ingestion-lambda-role_smartx-s3-access.json` | 2 | 6 |
| `ROLLBACK_smartx-ingestion-lambda-role_smartx-dynamodb-access.json` | 1 | 1 |
| `ROLLBACK_FredIngestionLambdaRole_S3Access.json` | 1 | 2 |

---

## 4. THE FOUR ACTS (step 3)

### ACT 1 -- `shared-infra` (Terraform): `aws_iam_role_policy.infrastructure_ops_permissions`

Declared `shared-infra/iam_legacy.tf:62-85`; the `S3InfraWrite` statement is one line. Edit removes one
ARN from its `Resource` list. Targeted plan, graded from `show -json`:

```
PLAN: shared-infra: 2 resource_changes, histogram {no-op: 1, update: 1}, 0 to destroy
  update aws_iam_role_policy.infrastructure_ops_permissions
    attributes that move: 1 -> ['policy']          <- only the document; no role, name or tag
    statements 13 -> 13                            <- no statement added or dropped
    ARNs 15 -> 14   REMOVED 1, ADDED 0
      - [S3InfraWrite] arn:aws:s3:::opal-data-smartx-v2/*   DEAD-S3
    Sids removed: []   added: []
```
**Untargeted beside it:** `245 resource_changes, {no-op: 244, update: 1}` -- the 1 being this same change.
Statements that would become EMPTY: **none** (`S3InfraWrite` keeps `opal-infrastructure-snapshots/*` and
`opal-data-portal-v2/infrastructure/*`).

### ACT 2 -- `smartx-pipeline` (Terraform): `ec2_s3_access` + `ingestion_s3`

```
PLAN: smartx-pipeline: 4 resource_changes, histogram {no-op: 2, update: 2}, 0 to destroy
  update aws_iam_role_policy.ec2_s3_access      (s3-access, on smartx-exporter-role)
    attributes that move: 1 -> ['policy']
    statements 3 -> 1
    ARNs 6 -> 2   REMOVED 4, ADDED 0
      - [SmartXDataReadWrite] arn:aws:s3:::opal-data-smartx-v2     DEAD-S3
      - [SmartXDataReadWrite] arn:aws:s3:::opal-data-smartx-v2/*   DEAD-S3
      - [SmartXLegacyRead]    arn:aws:s3:::opal-data-smartx        DEAD-S3
      - [SmartXLegacyRead]    arn:aws:s3:::opal-data-smartx/*      DEAD-S3
    Sids removed: ['SmartXDataReadWrite', 'SmartXLegacyRead']   added: []   kept: ['PortalViewsSync']
  update aws_iam_role_policy.ingestion_s3       (smartx-s3-access, on smartx-ingestion-lambda-role)
    attributes that move: 1 -> ['policy']
    statements 2 -> 2
    ARNs 6 -> 4   REMOVED 2, ADDED 0
      - arn:aws:s3:::opal-data-smartx-v2     DEAD-S3
      - arn:aws:s3:::opal-data-smartx-v2/*   DEAD-S3
    Sids kept: ['MdpfFeedReadForDistribution']
```
**Untargeted beside it:** `47 resource_changes, {no-op: 45, update: 2}`, 0 to destroy.

**STATEMENTS THAT WOULD BECOME EMPTY -- named as the cell requires: TWO.**
`SmartXDataReadWrite` (2 of 2 ARNs dead) and `SmartXLegacyRead` (2 of 2 dead). Both go entirely, so
`s3-access` drops from 3 statements to 1 and the exporter role keeps only `PortalViewsSync`. Nothing else
on the role changes: `ecr-access`, `lambda-invoke`, `secrets-access` and `self-shutdown` are absent from
the plan, and so is `ingestion_dynamodb`.

### ACT 3 -- `workspace-sync-lambda-role` (IAM-API: `put-role-policy`)

No Terraform declaration (the cell's own reading, confirmed). Before/after document diff instead of a plan:

```
statements 10 -> 10   dropped-as-EMPTY: none
ARNs 19 -> 15   removed 4, all from the single Sid S3Access:
  - arn:aws:s3:::ajb-workflow          - arn:aws:s3:::ajb-workflow/*
  - arn:aws:s3:::opal-data-portal-s3   - arn:aws:s3:::opal-data-portal-s3/*
S3Access keeps arn:aws:s3:::opal-data-news-av and /*; actions on every surviving statement unchanged: True
residual dead-name hits in the AFTER document: {ajb-workflow: 0, opal-data-portal-s3: 0, opal-market-update: 0}
```
After-document written to `.../narrow_dead/AFTER_workspace-sync-lambda-role_workspace-sync-permissions.json`
(2887 bytes). `RoleLastUsed 2025-12-30T19:10:42Z` -- not assumed in 9.5 months.

### ACT 4 -- `FredIngestionLambdaRole` / `S3Access` (IAM-API: **`delete-role-policy`**)

```
statements 1 -> 0   dropped-as-EMPTY: ['(no Sid)']
ARNs 2 -> 0   removed 2:  arn:aws:s3:::opal-market-update/*   arn:aws:s3:::opal-market-update
```
**Both of its ARNs are the dead bucket, so narrowing empties the whole document.** An empty `Statement`
list is not a valid policy, so the act is **`aws iam delete-role-policy`**, not `put-role-policy`, and
**no after-document is written** -- there is nothing valid to write. The cell anticipated this
(*"The opal-market-update grant may be a console inline policy: then it is an IAM-API act"*): confirmed,
`grep -c S3Access fred-pipeline/iam.tf` = **0** against a positive control of **4** declared
`aws_iam_role_policy` blocks in that 4887-byte file, two of them this same role's. The issuer has already
ruled this act `delete-role-policy S3Access` (msg 33404).

> **An instrument trap I hit here and had to re-derive.** My first pass read a rollback file that an
> earlier capture had written in the **wrapped** `get-role-policy` shape
> (`{RoleName, PolicyName, PolicyDocument}`) rather than the unwrapped document. `doc.get('Statement')`
> found nothing, so the script reported `statements 0 -> 0, ARNs removed 0` and then printed the verdict
> *"the whole document would be empty -> delete-role-policy"*. **The conclusion was right and its
> derivation was vacuous** -- it came from reading zero statements, not from finding one statement whose
> two ARNs are both dead. Re-captured with `--query PolicyDocument`, added a shape guard that refuses a
> wrapped response and refuses zero statements in a live policy, and re-derived: 1 statement, 2 of 2 ARNs
> dead. A wrong shape against a real parser returns a real-looking number, and here it returned a
> real-looking *sentence*.

---

## 5. A CELL PREMISE THAT IS NOW STALE: `-target` IS NOT LOAD-BEARING IN EITHER MODULE

The cell says *"shared-infra carries the never-applied restricted_breakglass adds, so -target is
load-bearing."* That was true in round 7, when my own `PLAN_SURVEY_family_c.md:262-263` recorded
`aws_iam_role.restricted_breakglass will be created` and `aws_iam_role_policy.restricted_breakglass will
be created` as **2 adds NOT SIGNED**. It is no longer true:

- `terraform state list` now holds **both** addresses (`aws_iam_role.restricted_breakglass`,
  `aws_iam_role_policy.restricted_breakglass`) among 256.
- The role exists **live**: `get-role cloudops-cot-restricted-breakglass-role` -> created
  **2026-10-11T09:05:05Z**, `RoleLastUsed None`.
- It was applied **today** by another project: `ADVI_COTBKF` workers `~89`/`~88`, commits `a62599efc4`
  and `31263d7d3a` on `shared-infra/s3-lgic-firm-buckets.tf`.
- The untargeted plan confirms it: **244 no-op + my 1 update**, zero adds.

So the hazard the cell cites was closed about 14 hours before I read it. **Both** modules are converged
(shared-infra 244/245 no-op, smartx-pipeline 45/47 no-op), so `-target` here is belt-and-braces, exactly
as it was in z-6's fred-pipeline. **I will still use `-target`, because BOUNDS require it** -- but I am
not citing it as a control that is doing work, because a control believed in the place it is idle is how
one gets trusted in the place it is actually needed.

---

## 6. BROKEN FEATURES THE GRANTS WERE HIDING (the cell's explicit instruction)

> *"A reference found is NOT a reason to keep the grant: it is a broken feature the grant hides. Narrow
> anyway, and file the reference as its own surprise row naming the function."*

Two consumers hold **live, non-comment S3 references to the 404 `opal-data-smartx-v2`**:

| consumer | S3 refs | the sharpest examples |
|---|---|---|
| **EC2 `smartx-exporter`** (role `smartx-exporter-role-2025...`) | **30** of 34 | `config/production.env:9 S3_BUCKET=opal-data-smartx-v2`; `run-all-portfolios.sh:184,201,204` do `aws s3 ls/cp s3://opal-data-smartx-v2/exports/`; `scripts/post-export.sh:84` writes `consolidated/smartx_allocations.parquet`; `S3_BUCKET = "opal-data-smartx-v2"` hardcoded in 8+ scripts |
| **Lambda `opal-smartx-ingestion-pipeline`** (role `smartx-ingestion-lambda-role`) | **14** of 23 | `lambda_function.py:32` sets `os.environ['SMARTX_S3_BUCKET'] = 'opal-data-smartx-v2'` **in code**; `:123` `consolidate.S3_BUCKET = 'opal-data-smartx-v2'`; `config.py:208`, `consolidate_smartx_to_parquet.py:40`, `precompute_views.py:38`, `aggregate_smartx_by_transaction_dates.py:38` (`s3.download_file('opal-data-smartx-v2', ...)`), `parquet_path_fix.py:16` |

These are not documentation: they are assignments and API calls against a bucket that returns
`NoSuchBucket`. The grants are not what makes them work -- nothing makes them work. **Filed as row
Z-S51**, naming both consumers. The narrowing proceeds per the cell.

Supporting evidence that the chain is already dead rather than merely broken-on-paper:
`smartx-exporter-role` `RoleLastUsed 2026-06-01T14:16:37Z` (4.3 months) and
`smartx-ingestion-lambda-role` `2026-08-14T11:30:40Z` (~2 months). Two of the Lambda's own comments say
so in its source: `compute_account_distribution.py:61` calls it *"dead smartx-exporter parquet"* and
`:83` *"Legacy output (deprecated...)"*.

---

## 7. THE LIFECYCLE ON A 404 BUCKET (the note the cell asks for; not this cell's act)

`infra/aws/terraform/smartx-v2-bucket-lifecycle/main.tf:33-34` declares

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "opal_data_smartx_v2" {
  bucket = "opal-data-smartx-v2"
```

a whole Terraform **module** whose only purpose is a 14-day noncurrent-version expiry rule on a bucket
that reads `NoSuchBucket`. Recorded as the cell instructs and **not acted on** -- it is neither an IAM
grant nor in my `<paths>`. I did not read its state (the module needs its own `terraform init`, which is
work outside this cell for a fact that changes nothing I do). Folded into row Z-S51 so the module is
named with an owner rather than left as a line in a survey.

---

## 8. WHAT PHASE A DID AND DID NOT DO

**Did:** the 7-line reference census with a classified breakdown and a positive control per readable
role; five live re-reads with two controls; 10 rollback documents; the four acts' edits in my own
worktree (uncommitted); four plans (2 targeted + 2 untargeted) graded per attribute, per Sid and per ARN
from `show -json`; the two IAM-API before/after diffs; `terraform fmt` on both edited files.

**fmt:** `smartx-pipeline` rc=0. `shared-infra` rc=3, but **the deviation is not mine** -- the flagged
files are `cross-firm-secret-deny.tf`, `drift-producer.tf`, `infra-monitor.tf`,
`lambda-execution-role.tf`, `s3-49financial.tf`, `secrets-unowned.tf`, the **same six** at HEAD in the
shared tree, and `terraform fmt -check iam_legacy.tf` alone reads **rc=0**.

**Edit shape:** 2 files, 1 insertion, 29 deletions, 3 hunks; 7 lines containing `arn:aws:s3` removed and
1 added (ACT 1 rewrites its single-line `Resource` list, which holds 3 ARNs). Residual dead-name census
in the two edited files: all five names **0**, except `opal-data-smartx` = **1** in
`smartx-pipeline/iam.tf` -- which is the **DynamoDB** ARN at `:93`, correctly untouched. Positive
control `opal-data-portal-v2` = 1 and 5 respectively.

**Did NOT:** apply anything, call `put-role-policy` or `delete-role-policy`, open a NEVER-2 entry, commit
any edit, or touch `ingestion_dynamodb` / the four other exporter policies / the lifecycle module. No AWS
write of any kind.

**PHASE B needs ONE PAIR PER ACT** (`ledger/NEVER_WIDEN_ROUND9_Z-1_<ACT>_{COO,CTO}_HALF.md`), and the
cell orders write-bearing names first with `opal-data-smartx` last. On the measurements above that
ordering is: ACT 4 (Fred, delete -- already ruled to follow z-6, which has landed), ACT 3
(workspace-sync, write), ACT 1 (shared-infra, write), then ACT 2 -- whose `SmartXLegacyRead` is the
read-only `opal-data-smartx` statement and so is the last thing to go.
