# NEVER-WIDEN SIGN-OFF -- COO HALF -- ADVI_COTBKF C-RESTRICTED: the three restricted-prefix statements in the Cottonwood fence apply

**Signer:** `2.0.0_SA_COO~C2` (ADVI_COTBKF's issuing lane, dell2). **Counterpart:** `1.0.0_SA_CTO~DELL2` (CTO half). **For:** laptop
`2.0.0_SA_COO~C`, who cuts the laptop apply of the Cottonwood fence (laptop `1.0.0_SA_CTO` msg 106152, relayed by `0.0.0_AB_MSTR~DELL2`
msg 339; fence join AMENDMENT 1 @341eeb04bd). **Code:** `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf` as merged @85d8b5f20f
(worker build 8e58736597), lines 177-275. **Register:** X15 (`infra/logic/06_CONFORMANCE_LEDGER.md:149`), Andrew-acknowledged.
**Write-in:** `org/devices/role_requests/dell2/dell2-20261007T085711Z-7b15.json` (ADMITTED on conditions, laptop msg 106095).

## 1. WHAT THIS HALF SIGNS -- ONLY the ADVI_COTBKF statements; the fence join's own statements are not this half's

| item | where (file line at @85d8b5f20f) | effect | rollback |
|---|---|---|---|
| `DenyRestrictedReadExceptReaders` | `:205-211` | Deny `s3:GetObject*`, `GetObjectVersion*`, `GetObjectAttributes`, `GetObjectTagging` on `opal-data-cottonwood/commonwealth/cottonwood/bronze/crm/*` for every principal except the console user and the break-glass role | revert the statement's row in the `.tf`, `safe-apply` targeted on `aws_s3_bucket_policy.lgic_firm` |
| `DenyRestrictedListExceptReaders` | `:212-222` | Deny `s3:ListBucket*` on the bucket where `s3:prefix` is under that prefix, same two exceptions | same |
| `DenyRestrictedWriteExceptBreakglass` | `:223-230` | Deny `s3:PutObject*`, `DeleteObject*`, `RestoreObject` under the prefix for every principal except the break-glass role | same |
| role `cloudops-cot-restricted-breakglass-role` + inline policy `restricted-prefix-get-put-list` | `:236-275` (trust `:248-257`: the console user only) | a NEW role; Get, Put and List on the prefix only | `terraform destroy -target` the role and its policy |
| anything else in the fence apply | -- | **NOT SIGNED here** (the fence join's dell2 statements carry their own halves) | -- |

**Writers of the property (the Cottonwood bucket policy): N = 1** -- the one `for_each` `aws_s3_bucket_policy.lgic_firm` in this file;
the three statements ride only the Cottonwood row (`:167-169`). **Data under the prefix today: none** -- X15 measured `commonwealth/`
empty in `opal-data-cottonwood` (2026-10-07 ~04:3xZ), and the laptop's two-level listing at 09:25Z (row S15) shows only `irpt/` and
`mdpf/`. So the statements deny access to an empty prefix: no existing reader loses anything.

## 2. EXPECTED OUTCOME, BOTH BRANCHES

- **A:** the targeted plan shows exactly the three statements added to the Cottonwood policy (plus whatever the fence join's own halves
  cover) and the role with its inline policy created; `python infra/aws/terraform/shared-infra/tests/check_restricted_prefix.py` run
  IMMEDIATELY before the apply prints its RESTRICTED-CHECK line passing (CB4d4-AC1; terraform is absent on dell2, row S7, so it runs on the
  laptop); after the apply, X15's bound (2): one read refused from an agent identity, one allowed through the group. Only then does the
  single CRM landing happen, by Andrew through the role, on his word.
- **B:** any plan line on the three statements or the role beyond the rows above, the check failing, or the post-apply refused/allowed
  pair not both observed: the half does not cover the act; revert the rows and re-apply; no CRM byte is written.

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)"
ACT       the Cottonwood bucket policy gains 3 Deny statements on commonwealth/cottonwood/bronze/crm/; one new break-glass role
SCOPE     ADVI_COTBKF's statements only; the fence join's statements are signed in their own halves
N         1 writer of the policy (aws_s3_bucket_policy.lgic_firm); the prefix holds 0 objects
COO half  2.0.0_SA_COO~C2 -- GIVEN 2026-10-07 ~10:3xZ
CTO half  1.0.0_SA_CTO~DELL2 -- owed
```

-- `2.0.0_SA_COO~C2`

## AMENDMENT 1 -- 2026-10-07 ~11:2xZ, matching the CTO half's AMENDMENT 1 (@b4073b7bf2, laptop 106173)

The same Cottonwood policy update also carries NFRA_CTLPLN CT-d-2's dell2 principal line. **This half's scope is unchanged** -- the three
ADVI_COTBKF statements and the break-glass role; CT-d-2's line is signed in that project's own halves. This half now also requires, in
Branch A, that the plan touch exactly the three statements plus that one line (any other change is Branch B), and that the after-read
include one refused read on `commonwealth/cottonwood/bronze/crm/` by `cloudops-dell2-agent-user` (the dell2 identity admitted to the
bucket by CT-d-2 is still denied on the restricted prefix). COO half for this amendment: `2.0.0_SA_COO~C2`, GIVEN 2026-10-07 ~11:2xZ.

## AMENDMENT 2 -- 2026-10-07 ~12:0xZ: STATEMENTS ONLY; the break-glass role is a separate act

Laptop `1.0.0_SA_CTO` 106207 (relayed as msgs 461, 464): `0.7.0_AE_CloudOps~E` stopped TO-APPLY-5 at step 0 and applied nothing
(`org/tier2_senior/0.7.0_AE_CloudOps~E/deliverables/STEP0_CONFLICT_READ_TO-APPLY-5_20261007.md` @316e1e5f98), because section 1's role row
and Branch A's "the role with its inline policy created" contradicted both CTO halves, which void on any role line.

**This half now signs STATEMENTS ONLY**, and supersedes section 1's role row and Branch A's role clause:
- **Signed:** the three Deny statements (`DenyRestrictedReadExceptReaders`, `DenyRestrictedListExceptReaders`,
  `DenyRestrictedWriteExceptBreakglass`) in the Cottonwood row of `aws_s3_bucket_policy.lgic_firm`, plus CT-d-2's dell2 principal line
  (signed in its own halves). The statements name the break-glass role's ARN, derived from its builder name; the role need not exist for
  the policy to apply, and until it does, only the console user reads the prefix (the prefix holds 0 objects).
- **Not signed here:** `aws_iam_role.restricted_breakglass` and `aws_iam_role_policy.restricted_breakglass`. They are their own act under
  the admitted role request `dell2-20261007T085711Z-7b15` (laptop 106095), with their own pair.
- **Branch A:** the targeted plan touches exactly the three statements plus CT-d-2's line and NO role resource; CB4d4-AC1's policy limb
  passes immediately before the apply; after it, one read on `commonwealth/cottonwood/bronze/crm/` by `cloudops-dell2-agent-user` is
  refused. **Branch B:** a role line or any other change in the plan -- stop, apply nothing.

COO half for this amendment: `2.0.0_SA_COO~C2`, GIVEN 2026-10-07 ~12:0xZ.
