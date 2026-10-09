# BF-aa-1 retire evidence -- round 12

**Seat:** `0.7.0_AE_CloudOps~DELL1` -- **2026-10-09 ~10:3xZ** -- READ-ONLY IN AWS. No `apply`, no `destroy`, no
`import`, no `state rm`, no `s3 rm`, no `safe-apply`. Nothing in AWS changed.

Order `LGIC_BLANKFIX.TO-BF-aa-1` @6c36e70e0a (verified an ancestor of HEAD before acting), GO from
`2.0.0_SA_COO~B1` msg 2262, acked READ.

---

## The instrument discriminates -- read this before the counts below

`terraform state list` returning nothing with rc=0 is indistinguishable, on its face, from a backend it could not
read. So a POSITIVE CONTROL was run on a root known to hold resources:

```
terraform -chdir=infra/aws/terraform/opal-assets state list   ->  238 addresses
  data.aws_caller_identity.cot_reattempt
  data.aws_caller_identity.current
  data.aws_lambda_layer_version.openpyxl
  ...
```

The same command, same binary, same session prints 238 addresses for a populated root and zero for the two below.
The empty reads are therefore absences in the world, not a silent instrument failure.

---

STATE-LIST canonical-schwab-si2-schedule count=0

```
$ terraform -chdir=infra/aws/terraform/canonical-schwab-si2-schedule init -input=false
  (success; backend s3://opal-313476888478-terraform-state/canonical-schwab-si2-schedule/tfstate)
$ terraform -chdir=infra/aws/terraform/canonical-schwab-si2-schedule state list
  (no output)
rc=0
```

The folder holds `main.tf` and `.terraform.lock.hcl` only. `main.tf` declares `terraform`, `provider` and `locals`
blocks and **zero `resource` blocks**, which is consistent with the empty state rather than merely compatible with it.

AWS-OWNED canonical-schwab-si2-schedule count=0

```
$ comp-find --corpus aws 'canonical-schwab-si2-schedule'
  DENOMINATOR: 0 hit(s) across 2844 aws node(s) scanned [corpus=aws]
  VINTAGE: built from the estate as of 2026-10-09 06:17:57 UTC; stitch manifest 1089b9991c93
  NO HITS. This is a MEASURED zero over 2844 aws node(s) -- not a claim the term is absent from AWS:
  only what the graph MODELS can match.
```

That caveat is the tool's own and is carried here rather than dropped. Two further reads were run because of it:

1. **The schedule this root describes never landed.** Its header specifies `cron(35 8,20 * * ? *)` ->
   SSM RunCommand on the SI2 box. Over 153 EventBridge rules (auto-paginated, denominator printed), **no rule
   carries that cron**.
2. **The re-timing did eventually land, under other names and not from here.** Four live rules name schwab/si2
   with DIFFERENT crons: `canonical-schwab-si2-08242234-daily-pull` `cron(15 10,22 * * ? *)`,
   `canonical-schwab-si2-08335338-daily-pull` `cron(45 9,21 * * ? *)`,
   `schwab-canonical-si2-08403355-pull-daily` `cron(45 10,22 * * ? *)`, plus
   `opal-assets-silver-schwab-sweep-daily`. None is declared by this root (its state is empty), so this root is a
   SUPERSEDED INTENTION. Retiring it removes a never-applied plan, not a control.

The instance the root names in `locals`, `i-0f3d57a97f14727af`, **exists and is running** -- read directly,
`ec2 describe-instances` -> `i-0f3d57a97f14727af running`. It is NOT owned by this root: the root's state is empty,
so it manages zero resources, and a `locals` reference is not ownership. Retiring the folder does not touch it.

REMOTE-STATE canonical-schwab-si2-schedule s3://opal-313476888478-terraform-state/canonical-schwab-si2-schedule/tfstate LEFT

```
$ aws s3api head-object --bucket opal-313476888478-terraform-state \
      --key canonical-schwab-si2-schedule/tfstate
  ContentLength 343    LastModified 2026-08-04T05:12:30+00:00    VersionId G1Hy9VgQTCK_PCTJYWhQQ0eDwLx.ReWR
```

LEFT IN PLACE. Deleting it is Andrew's act and is listed in the report; this cell never touched it.

---

STATE-LIST opal-assets-absence count=0

```
$ terraform -chdir=infra/aws/terraform/opal-assets-absence init -input=false
  (success; backend s3://opal-313476888478-terraform-state/opal-assets-absence/tfstate, encrypt=true)
$ terraform -chdir=infra/aws/terraform/opal-assets-absence state list
  (no output)
rc=0
```

The folder holds `main.tf` only -- `terraform`, `provider` and `locals` blocks, **zero `resource` blocks**.

AWS-OWNED opal-assets-absence count=0

```
$ comp-find --corpus aws 'opal-assets-absence'
  DENOMINATOR: 1 hit(s) across 2844 aws node(s) scanned [corpus=aws]
  [LOG_GROUP] /aws/lambda/opal-assets-absence-check  drift=LIVE-no-DECLARED  src=full-derive
```

**Count is 0 OWNED, and the one hit is named rather than rounded away.** The root's state is empty, so it manages
zero resources; the hit is not ownership. What it is, read directly:

- the function the root names, `opal-assets-absence-check`, **does not exist**:
  `lambda get-function-configuration` -> `ResourceNotFoundException: Function not found:
  arn:aws:lambda:us-east-1:313476888478:function:opal-assets-absence-check`
- its **log group survives the function**: `logs describe-log-groups` ->
  `/aws/lambda/opal-assets-absence-check  storedBytes 4811  retentionInDays None`
- and it is not a husk: `logs describe-log-streams --query length(logStreams)` -> **6**

So the function ran at some point, was removed, and left an orphaned log group with 6 streams, ~4.8 KB and **no
retention policy, i.e. never expiring**, which nothing in the estate declares (`drift=LIVE-no-DECLARED`). It is not
owned by this root and is not a reason to stop the retirement under the refusal clause -- the clause turns on a
non-empty state or a resource OWNED by the root, and neither holds. It IS a real estate finding, and retiring this
folder removes its last documentary trace in the repo, so it is filed as a surprise row rather than left in this
file alone: `LGIC_BLANKFIX-D1-S3`. The order prescribes `LGIC_BLANKFIX-D1-CO1-S<k>`; the live gate refuses only the `CO1` segment -- the `D1` coordinate is REQUIRED for a row filed on dell1, a bare id being the laptop's. The deviation is recorded in the row itself..

REMOTE-STATE opal-assets-absence s3://opal-313476888478-terraform-state/opal-assets-absence/tfstate LEFT

```
$ aws s3api head-object --bucket opal-313476888478-terraform-state --key opal-assets-absence/tfstate
  ContentLength 180    LastModified 2026-07-18T01:17:42+00:00    VersionId Dm9SuGZIxfEG3z7WpyX3eAQk8Gm3CUlt
```

LEFT IN PLACE, same as the other.

---

## Acts left for Andrew

1. Delete `s3://opal-313476888478-terraform-state/canonical-schwab-si2-schedule/tfstate`
   (343 B, VersionId `G1Hy9VgQTCK_PCTJYWhQQ0eDwLx.ReWR`) -- if the state history is no longer wanted.
2. Delete `s3://opal-313476888478-terraform-state/opal-assets-absence/tfstate`
   (180 B, VersionId `Dm9SuGZIxfEG3z7WpyX3eAQk8Gm3CUlt`) -- same.
3. Decide the orphaned log group `/aws/lambda/opal-assets-absence-check` (6 streams, ~4.8 KB, no retention, no
   declaring root, function gone). Not this cell's to delete and not in its grant.

## The three standing conditions

`1.0.0_SA_CTO~DELL1` msg 1821 / ADDENDUM 3 @947dd446e5: **none of the three was touched.** This cell made no send at
all (so (1) and (2) cannot fire), wrote no firm data bucket, never assumed the 49F principal, and moved no 49
Financial data anywhere (3).
