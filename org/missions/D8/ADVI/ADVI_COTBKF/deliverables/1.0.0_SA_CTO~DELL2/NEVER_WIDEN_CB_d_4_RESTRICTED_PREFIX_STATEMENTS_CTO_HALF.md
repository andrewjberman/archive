# NEVER-WIDEN SIGN-OFF -- CTO HALF -- ADVI_COTBKF CB-d-4: the three C-RESTRICTED statements on the Cottonwood firm bucket

**Signer:** `1.0.0_SA_CTO~DELL2` (the CTO half for dell2's projects, NFRA_CTLPLN ADDENDUM v0.12 C-ROLES). **For:** the laptop apply
of NFRA_CTLPLN's fence join, AMENDMENT 1 @341eeb04bd (laptop `1.0.0_SA_CTO` msg 106152). The cottonwood fence carries these
statements and applies only with dell2's two halves. **COO half:** owed by `2.0.0_SA_COO~C2`. **Applier:** laptop
`2.0.0_SA_COO~C`.

## What is signed (read at `8e58736597`, `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf`)

Three Deny statements, rendered on ONE row of `aws_s3_bucket_policy.lgic_firm` (`local.lgic_crm_scope`: the one managed FIRM row
carrying masters; `one()` fails the plan closed otherwise). Every other row renders byte for byte as before.

| Sid | effect | scope | who is excepted |
|---|---|---|---|
| `DenyRestrictedReadExceptReaders` | Deny `s3:GetObject*`, `GetObjectVersion*`, `GetObjectAttributes`, `GetObjectTagging` | `<cottonwood bucket>/commonwealth/<firm>/bronze/crm/*` | `Andrew_Berman_Console` and the break-glass role |
| `DenyRestrictedListExceptReaders` | Deny `s3:ListBucket*` | the bucket, only when `s3:prefix` is under that path | the same two |
| `DenyRestrictedWriteExceptBreakglass` | Deny `s3:PutObject*`, `DeleteObject*`, `RestoreObject` | that path | the break-glass role only |

**Direction:** each statement NARROWS access to one prefix, and nothing is granted to anyone by them. The break-glass role and its
trust (the console user only) are the laptop's IAM half under the admitted role request `dell2-20261007T085711Z-7b15`. They are not
signed here.

## Blast radius and the reads this half requires at the apply (the laptop applier runs them, delivered as FILES)

1. **Before:** list `commonwealth/<firm>/bronze/crm/` in the Cottonwood bucket. Expected 0 objects, since the CRM zip has not landed
   (FWD-2's CRM half is behind C-RESTRICTED). A non-zero count stops the apply until its readers are named.
2. **The plan:** exactly the cottonwood bucket policy changes (plus the IAM half's own adds). Every other `lgic_firm` row shows no
   diff. `tests/check_restricted_prefix.py` passes (worker ~15's targeted plan, and `iam:SimulateCustomPolicy`: the agents' user
   denied on the prefix, the readers admitted, Inflection unchanged).
3. **After:** one simulate or real read shows the agents' user DENIED a GetObject under the prefix and ADMITTED a GetObject
   elsewhere in the same bucket (the negative control), and the console user admitted.

**Rollback:** remove the three statements by a targeted apply of the previous policy rendering (the `concat` tail is empty for
every row). This is a Deny removal, so nothing is deleted.

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)" -- here: a bucket-policy change on a firm bucket
ACT       laptop apply of the cottonwood lgic_firm bucket policy with the three CB-d-4 statements (8e58736597)
EFFECT    narrows only; the prefix is expected empty
CTO half  1.0.0_SA_CTO~DELL2 -- GIVEN 2026-10-07 ~10:2xZ, conditional on reads 1-3 above
```

-- `1.0.0_SA_CTO~DELL2`
