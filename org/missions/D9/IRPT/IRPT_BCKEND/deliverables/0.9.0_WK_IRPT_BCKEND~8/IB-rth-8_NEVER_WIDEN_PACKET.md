# THE NEVER-WIDEN PACKET -- `IRPT_BCKEND.TO-IB-rth-8`: clear the four tainted `lgic_firm` resources

**Drafted by:** `0.9.0_WK_IRPT_BCKEND~8`. **Date:** 2026-09-21. **Governing order:**
`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rth-8.clear-the-four-tainted-lgic-firm-resources-under-never-widen.md`.
**This packet is NOT a sign-off.** It states the act's blast radius, the measured replace window and
rollback for CTO+COO to read and SIGN (CLAUDE.md NEVER-1, CTO+COO) as separate half-files under
`org/tier1_exec/1.0.0_SA_CTO/deliverables/` and `org/tier1_exec/2.0.0_SA_COO~<lane>/deliverables/`,
each naming THIS packet's blob hash at HEAD, before arm (c) of the governing order runs.

## 0. WHERE THIS STANDS -- IB-rth-7's measurement, re-confirmed independently this session

`IB-rth-7`'s worker (`0.9.0_WK_IRPT_BCKEND~7`, @`cabb11ced3`) found a fresh `terraform plan` on
`infra/aws/terraform/shared-infra` reading `4 to add, 0 to change, 4 to destroy` -- NOT `0/0/0` -- with
`aws_s3_bucket_policy.lgic_firm["inflection"/"cottonwood"]` and
`aws_s3_bucket_versioning.lgic_firm[same]` TAINTED, leftover from the 2026-09-18 half-landed apply
(row `IRPT_BCKEND-W3-S45`). Filed as `IRPT_BCKEND-W7-S2` (ARMED, disarm_owner `2.0.0_SA_COO~B`).

**Re-run fresh this session** (`.tools/terraform.exe init` + `plan -out=... ` + `show -json`,
`infra/aws/terraform/shared-infra`): **identical result** -- `Plan: 4 to add, 0 to change, 4 to
destroy.`, the same four resource addresses tainted, `action_reason: "replace_because_tainted"` on
all four. 242 total `resource_changes` in the root's plan; **238 no-op, 4 replace, 0 elsewhere** --
`demo`/`49financial` resources (15 of the 242) all read `no-op`.

## 1. THE EXACT BLAST RADIUS -- ONLY THESE FOUR, BOTH FIRMS, NOTHING ELSE

| resource | key | actions (structured plan JSON) | action_reason |
|---|---|---|---|
| `aws_s3_bucket_policy.lgic_firm` | `"inflection"` | `["delete","create"]` | `replace_because_tainted` |
| `aws_s3_bucket_policy.lgic_firm` | `"cottonwood"` | `["delete","create"]` | `replace_because_tainted` |
| `aws_s3_bucket_versioning.lgic_firm` | `"inflection"` | `["delete","create"]` | `replace_because_tainted` |
| `aws_s3_bucket_versioning.lgic_firm` | `"cottonwood"` | `["delete","create"]` | `replace_because_tainted` |

**Measured (not inferred): the destroy is forced PURELY by the TAINT marker, not by any attribute
needing replacement.** For both `aws_s3_bucket_policy` resources, the plan's `change.before` and
`change.after` policy documents are **byte-identical** (confirmed by independent sha256 comparison,
normalized JSON): `opal-data-inflection` both hash to `2d90b2f1a01b...`, `opal-data-cottonwood` both
hash to `b095cbbfe657...`. The live `get-bucket-policy` read (a separate AWS CLI call, not the
Terraform refresh) matches both of those hashes exactly. **So this replace will delete and then
recreate the SAME already-correct policy document (the CRO's console PUT, msg 99124) -- no content
change, purely a state-mechanics clear of the taint.**

**Nothing outside these four resources moves.** 238 of 242 resources in the root's plan are `no-op`;
the 15 `demo`/`49financial` resources present in the root (IAM role/profile/policy + the two buckets'
own controls) are ALL `no-op`. A plan showing anything else at apply time is a STOP per the governing
order's own BOUNDS -- arm (c) re-checks this immediately before applying, not just at packet-draft
time.

## 2. THE MEASURED WINDOW

**`aws_s3_bucket_policy` (both buckets): the bucket sits with NO explicit Deny policy for an interval
during the apply.** Basis and confidence: the AWS provider's `aws_s3_bucket_policy` resource has no
in-place-update-from-taint path -- a tainted resource is unconditionally destroyed then recreated. The
provider's Delete operation for this resource type is understood (from documented, stable, long-lived
CRUD behavior of a resource with a 1:1 API mapping -- `Create` = `PutBucketPolicy`, `Delete` =
`DeleteBucketPolicy`, no other verb touches this object) to call `s3:DeleteBucketPolicy`, which removes
the ENTIRE policy document (there being only one policy per bucket, not per-statement), before the
`Create` step's `PutBucketPolicy` re-attaches it. **CONFIDENCE: MODERATE-HIGH on the CRUD mapping
itself (a single-purpose resource, two AWS API calls, no ambiguity in which does what); NOT
independently re-verified against the provider's Go source in this environment** -- only the vendored
compiled binary is available locally (`.tools/terraform.exe`, provider cached at
`C:\Users\AndrewBerman\.terraform.d\plugin-cache`, no source, no decompile attempted), and no live
vendor/network fetch was performed (none is authorized for this act). This read is consistent with the
CTO's own framing of the same question in `IB-rtf-5`'s CTO half (@`89fecc6686`), which posed exactly
this mechanism as the expected one.

**`aws_s3_bucket_versioning` (both buckets): UNCERTAIN, stated as such rather than assumed either way.**
AWS has no "delete versioning" API -- status is binary Enabled/Suspended for the life of a bucket. Two
behaviors are plausible for the provider's Delete step on a tainted replace and this worker cannot
settle which from the plan JSON, the CLI, or the vendored binary alone: (a) a no-op, state-only
reconciliation (Terraform removes the resource from its own state/graph without issuing any mutating
AWS call, because there is no way to truly "unset" versioning and some provider versions treat destroy
of this resource as non-mutating for exactly that reason); or (b) an actual `PutBucketVersioning`
call setting `Suspended` as part of the destroy step, immediately followed by the create step's
`PutBucketVersioning` re-setting `Enabled`. **CONFIDENCE: LOW on which of (a)/(b) is live-true without
either reading the provider's source or observing an actual apply's CloudTrail trail; this packet does
not assume one.**

**Sequencing -- per-resource or all four in one batch:** read from `s3-lgic-firm-buckets.tf` directly
(not inferred): `aws_s3_bucket_versioning.lgic_firm` and `aws_s3_bucket_policy.lgic_firm` carry NO
`depends_on` on each other (the policy resource's only `depends_on` is on
`aws_s3_bucket_public_access_block.lgic_firm`, an unrelated already-existing, non-tainted resource).
Terraform applies resources with no dependency edge between them CONCURRENTLY (default parallelism).
**So the four replacements are NOT guaranteed to be serialized relative to each other** -- inflection's
policy-window and inflection's versioning-window (and cottonwood's) may overlap in time. **Within any
ONE resource's own replace, its delete step completes before its own create step begins** -- that
ordering is a Terraform invariant for a single resource's replace and is not in question.

## 3. THE CONSEQUENCE, GIVEN BOTH BUCKETS HOLD 0 KEYS

**Re-measured this session, both buckets, both instruments (Terraform's own refresh AND a direct
`list-objects-v2` call): 0 keys, `opal-data-inflection` and `opal-data-cottonwood`.** So:

- **No data exposure is possible during the policy window** -- there is nothing in either bucket to
  read, copy or delete, regardless of which principal could act during the gap.
- **Stated plainly, per the governing order's own text: this is a compliance/security STATE regardless
  of whether data exists.** During the delete-to-create gap, the bucket carries no explicit Deny on
  foreign-firm principals. This does NOT by itself grant access -- S3 access still requires an ALLOW
  from IAM (or from this now-absent bucket policy, which was Deny-only and never carried an ALLOW
  statement) -- so the practical exposure during the window is bounded to whatever IAM ALREADY grants
  independently of this fence, which the fence exists to override with an explicit Deny. No new grant
  is created by the gap; an existing IAM grant not overridden by the (temporarily absent) Deny is the
  only thing that could act, and 0 keys means there is nothing for it to act ON.
- **Versioning window:** moot in consequence either way (no-op or Suspend-then-Enable) given 0 keys --
  no object exists to lose version history on, and the create step re-sets `Enabled` regardless.

## 4. ROLLBACK

**If anything reads wrong post-replace** (policy sha256 mismatch, non-zero keys found, versioning not
`Enabled`, a re-plan not reading `0/0/0`, or `terraform state list` showing a tainted resource): re-apply
the fence policy immediately via a fresh `.tools/safe-apply.sh` run on the same root -- the declared
configuration is unchanged by this act (the `after` policy is byte-identical to the current live
policy), so a re-apply converges to the same already-correct state. **No data can have been lost since
none exists** (0 keys, both buckets, both before and after). The rollback path does not depend on any
exemption beyond the three already in `infra/logic/registry/exemptions.json` for both buckets
(`Andrew_Berman`, `Andrew_Berman_Console`, `Opal_Terminal`) -- the applying identity for this session
(`arn:aws:iam::313476888478:user/Andrew_Berman`) is confirmed 1 of 3 exempted on BOTH buckets, so a
rollback apply run under the same identity is not itself blocked by the fence it is restoring.

## 5. WHAT THIS PACKET DOES NOT COVER

- Any object write to either bucket; any reader/writer/runner/env change; any legacy prefix; any
  resource outside the four named (`aws_s3_bucket_policy.lgic_firm[...]`,
  `aws_s3_bucket_versioning.lgic_firm[...]`, both firms).
- `-target` is never used by this act.
- Ledger leg L4 (the host negative control) -- left exactly as `IB-rth-7` left it, UNEXERCISED, host
  stopped; not this cell's to force, not this packet's to cover.
- Any edit to `fence_patterns()`, `exemptions.json`, or `scopes.json`.
- The judgment question (whether this class of taint-clear should use `terraform import` instead of
  replace in future) -- that is `R85-AC3`, for `3.0.0_SA_CVO`, not decided here.

---

**Both never-widen halves (CTO + COO) sign referencing THIS packet's blob hash at HEAD, naming s.1-s.4
above, before arm (c) of the governing order runs.** If either half is not obtained this pass, per the
governing order's own text (matching `IB-rtf-5`'s precedent exactly): that is an honest STOP, the order
stays open on `R85-AC1` alone, and this packet remains the complete and correct record of what is owed.
