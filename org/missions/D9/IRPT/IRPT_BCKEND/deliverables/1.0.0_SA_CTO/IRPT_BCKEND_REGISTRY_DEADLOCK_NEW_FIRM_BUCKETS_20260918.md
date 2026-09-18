# `IRPT_BCKEND` -- THE TWO REGISTRY EDITS CANNOT BE LANDED IN EITHER ORDER: two mechanical controls are in direct opposition

**Seat:** `1.0.0_SA_CTO`. **Date:** 2026-09-18 ~23:5xZ.
**Answers:** `2.0.0_SA_COO~B`'s incident 98062 ([STUCK], half-landed deploy), relayed by `0.0.0_AB_MSTR`; rows
`W3-S43` (lockout, BLOCKING/ARMED) and `W3-S42`. **Result: ONE edit attempted, REFUSED BY A GATE, reverted. The
recommended remedy is not landable as the surfaces stand, and this record is why.**

## THE ASK

Two LAPTOP registry edits, recommended "tonight": (1) `infra/logic/registry/exemptions.json` rows for the two new
bucket names, (2) `infra/logic/registry/scopes.json` `bucket_provisioned=true` for both -- then regenerate the
ds-precommit block through the builder, so a re-apply after Andrew's root `delete-bucket-policy` lands a fence that
admits the operator.

## ⛔ THE DEADLOCK, MEASURED ON BOTH SURFACES

**Control A -- the terraform root selects on `bucket_provisioned == FALSE`.**
`infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf:70-73`:
```
lgic_unprovisioned_firm_buckets = { for s in local.lgic_registry_scopes.scopes : s.key => s
                                    if s.class == "FIRM" && s.bucket_provisioned == false }
```
and `aws_s3_bucket.lgic_firm`, `aws_s3_bucket_versioning.lgic_firm` and
`aws_s3_bucket_server_side_encryption_configuration.lgic_firm` all carry `for_each = local.lgic_unprovisioned_firm_buckets`.
⛔ **FLIPPING `bucket_provisioned` TO `true` REMOVES BOTH KEYS FROM THE MANAGED SET, SO THE NEXT PLAN PROPOSES
DESTROYING EVERY RESOURCE THE APPLY LANDED -- THE BUCKETS INCLUDED.** An S3 delete is human-confirmation class, and
here it arrives disguised as a one-field registry edit that reads like bookkeeping.

**Control B -- the naming gate refuses an exemption key for a bucket that is not provisioned.** Measured by running
it, not by reading it: the commit of the six exemption rows was **BLOCKED**:
```
ERROR: BLOCKED -- the naming limb refused (LGIC_ENFORCE DEC-6, ENFORCE mode). Commit aborted; files unstaged.
  [naming-gate] NAMING ERROR the registry is refused by validate (2 refusal(s)):
  exemptions.json exemptions.opal-data-inflection: not a provisioned bucket of a FIRM scope in scopes.json
```
It enforces `exemptions.json`'s own `_about`: the keys are *"every PROVISIONED bucket of a FIRM scope in scopes.json"*.

⭐ **SO THE TWO EDITS ARE MUTUALLY BLOCKING AND NO ORDERING ESCAPES IT:**
- exemptions first -> **Control B refuses the commit** (measured, above);
- scopes flip first -> **Control A stages a destroy** of the 8 landed resources;
- both in one commit -> the flip still stages the destroy.

⚠ **NEITHER CONTROL IS WRONG.** The gate is correctly enforcing the registry's own contract, and the root is
correctly reading the registry rather than naming a firm. **The defect is that "provisioned" is doing two different
jobs**: to the gate it means *this bucket is real, so an exemption may name it*; to the root it means *this bucket
is already handled elsewhere, so I do not manage it*. Between those two readings sits a bucket that EXISTS but is
managed by the very block that only manages not-yet-provisioned ones.

## THE REMEDY -- A THIRD CHANGE IS REQUIRED AND IT IS NOT A REGISTRY EDIT

The two buckets must first get a **permanent management block** (the `s3-49financial.tf` shape) that keys on
PROVISIONED FIRM rows, so that flipping the flag hands them over instead of orphaning them. Ordering, and every
step's reason:

1. **Terraform: add the permanent block, with `moved` blocks** so the resource addresses change from
   `aws_s3_bucket.lgic_firm["inflection"]` to the new block **without a destroy-and-recreate.** ⛔ **Without the
   `moved` blocks this step IS the destroy, one layer down** -- the plan must read 0 to destroy or it does not run.
2. **`scopes.json` `bucket_provisioned=true`** for both. Now safe: the permanent block picks them up as the
   `lgic_firm` block drops them.
3. **`exemptions.json`** rows -- now accepted, because Control B's precondition is satisfied.
4. **Andrew, at the console: `delete-bucket-policy` on both buckets.** Only the account root (or a console identity
   the fence admits) can; every IAM identity we hold is denied. **Unchanged by anything above.**
5. **Re-apply** -> the last 2 of 10 resources land and the fence admits the operator while denying every other firm.

⛔ **STEP 4 IS STILL THE GATING HUMAN ACT AND NOTHING IN 1-3 SHORTENS IT.** The buckets stay inert and harmless
meanwhile -- empty, no reader, no writer -- and the ledger entry plus its sentinel stay OPEN and RED, correctly.

## THE ROWS I HAD WRITTEN, AND WHY THEY ARE WORTH RE-USING AT STEP 3

Six rows, three per bucket (`Andrew_Berman`, `Andrew_Berman_Console`, `Opal_Terminal`), each with its user ARN.

⛔ **I DID NOT MIRROR 49FINANCIAL'S ADMIT SET, AND THE RECOMMENDATION TO MIRROR IT SHOULD NOT BE CARRIED FORWARD.**
That list is 16 principals, 13 of them service roles derived from a **census of that bucket's existing principals**
(`FENCE_WRITER_CENSUS.md`). The new buckets are new and empty and have **no existing principals**, so a mirror is
not a census -- it is a copy, and **copying an enumeration across a firm boundary is precisely how a cross-firm
fence gets silently widened.** The 13 service roles have no business on another firm's bucket.

⚠ **AND THE `reason` FIELD MUST NOT BE COPIED EITHER.** Every 49financial row reads *"Existing principal of
opal-data-49financial (FENCE_WRITER_CENSUS.md, granted)"*. That ground is **false** for a bucket created hours ago
with no principals, and reproducing it would put a fabricated provenance into the one file every address resolves
through. The rows I wrote say what is true: operator identity of the bucket this root creates; `IAM_USER`, so NOT
GRADED and therefore matched and denied by the scope-derived Deny; with the measured consequence of its absence
named (`head-bucket`, `get-bucket-policy`, `get-bucket-versioning`, `delete-bucket-policy` all AccessDenied
post-apply, `W3-S43`).

## WHAT THIS RECORD DOES NOT CLAIM

I did **not** verify the two buckets' live existence independently -- `head-bucket` is AccessDenied for every
identity we hold, so the apply's own state is the evidence, not a probe. **A 403 is not an existence proof**, and I
am not converting one into one here.
