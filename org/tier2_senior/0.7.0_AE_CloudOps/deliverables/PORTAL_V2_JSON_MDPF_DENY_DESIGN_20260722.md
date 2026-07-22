# Deliverable 2 -- `opal-data-portal-v2/json/mdpf/**` protection: DESIGN + EXERCISE PLAN

**Status:** DRAFT. **NOT APPLIED. NOT IN `infra/`** -- deliberately held outside the TF tree so it
cannot be applied by accident. **This property is now LOAD-BEARING, not tidiness:** under the MDPF
planning hold the apply is HELD, and a `.tf` file living in a root is reachable by any untargeted
apply in that root -- the exact hazard class as PART 0's staged CF flip, in a different root.
**It stays out of `infra/` until the advisory releases the apply.**
**Author:** `0.7.0_AE_CloudOps` 2026-07-22 · **Hold:** `org/critical_paths/DO_NOT_DECOMMISSION_portal-v2_json_mdpf_49financial_20260722.md` (@74677ea04)

**GATE STATE (updated 2026-07-22 ~1528Z -- 2 of 3 original blockers RULED):**
| # | blocker | state |
|---|---|---|
| 1 | Andrew -- 07-17 alert-suspension adjacency | **RESOLVED.** Andrew ~1425Z, verbatim: *"THere should be a gate/hook for this, but not an 'Alert' not an SES or something like that."* The 07-17 suspension is on **ALERTS**, not on **GATES/HOOKS**. Test: does it PAGE someone, or does it STOP something? This Deny stops something and pages nobody. |
| 2 | CTO -- lifecycle-limb scope call | **RESOLVED by R5** (`MDPF_CONSOLIDATED_PLAN_20260722.md` @49687d1b2): *"Deliverable 2 includes the `PutLifecycleConfiguration` limb. Routine cleanup arrives as a lifecycle rule far more often than a hand-typed delete; shipping only the easy-to-test half is refused."* **V2 IS IN. Uncommented below.** |
| 3 | CTO/COO -- placement root | **STILL OPEN.** COO ground-truthed a `desired`/source-layout read (`shared-infra`) at 152230Z and explicitly labelled it his read, not a placement instruction. Mine to confirm on the `applied` limb at plan time. |

**APPLY POSTURE:** **HELD** under CTO's narrowed carve-out 1 (@8da5fbfa5, 152205Z): *"the deny's APPLY is
HELD ... Drafting, exercise-design and grounding continue; the apply waits for the advisory."* Andrew's
1425Z settled **whether this exists**, not whether to fire an apply under a planning hold.

---

## HEADLINE: THE SPECIFIED CONTROL CANNOT DO HALF ITS JOB, AND ITS CITED PRECEDENT DOES NOT TRANSFER

The hold doc specifies control #1 as *"S3 bucket-policy DENY on `DeleteObject` / lifecycle-expiry for the
prefix,"* precedent *"the `.parquet`-under-`bronze/` deny (Rule 17a) -- behavior-grade and exercised."*
Both halves of that sentence have a defect. Neither is fatal; both change what gets built.

### Defect 1 -- a bucket policy CANNOT block lifecycle expiry

Lifecycle expiration is performed by the **S3 service itself, not by a calling principal**, so it is never
evaluated against the bucket policy. A `Deny` on `s3:DeleteObject` scoped to `json/mdpf/*` stops principals
and does **not** stop a lifecycle rule from expiring those exact objects.

**So the control as specified would land, exercise GREEN on a denied delete -- a real, passing test -- and
leave the named vector wide open.** Same defect class as the WS-5 `.json` suffix fix this morning: a change
that reads GREEN while the thing it was built to stop still gets through.

**Live state (grounded 2026-07-22 ~13:20Z, `get-bucket-lifecycle-configuration`):**

| rule | status | `Filter.Prefix` | expires current objects? |
|---|---|---|---|
| `expire-noncurrent-versions-14d` | Enabled | `""` (WHOLE BUCKET) | No -- noncurrent versions only |
| `abort-incomplete-mpu-7d` | Enabled | `""` (WHOLE BUCKET) | No |

Nothing is broken today. **But both existing rules are whole-bucket-prefix -- that is the established
lifecycle idiom in this bucket.** A future `Expiration` rule written in the same shape reaches
`json/mdpf/**` **without the string `mdpf` appearing anywhere in the change.** That is what defeats the
ladder's lower rungs specifically: control #3 (the hold doc) only fires for someone who greps the prefix,
and **nobody greps `json/mdpf` while writing a `Filter.Prefix = ""` rule.** The doc's own stated weakness
(*"they will grep the prefix first is an assumption about a PERSON"*) is sharper than it realises -- the
realistic change never mentions the prefix at all.

Also grounded: **Versioning = Enabled. Object Lock = NOT CONFIGURED** (`ObjectLockConfigurationNotFoundError`)
-- so the other real anti-expiry control is absent too.

### Defect 2 -- the 17a precedent's safety property does NOT transfer

`opal-assets/monolith.tf:230-231` states it plainly: *"This is the bucket's FIRST policy (live
GetBucketPolicy = NoSuchBucketPolicy) -- a pure ADD, nothing merged, nothing replaced."*

**`opal-data-portal-v2` is not that case. It already HAS a policy**, with two live CloudFront statements:

| Sid | Effect | Principal | Resource |
|---|---|---|---|
| `AllowCloudFrontOAI` | Allow | OAI `EU39UXW7CMSI5` | `opal-data-portal-v2/*` |
| `AllowCloudFrontOACPublicData` | Allow | `cloudfront.amazonaws.com` | `json/*`, `json-tiered/*` (SourceArn `EVTSA9VEHNZVH`) |

**A TF `aws_s3_bucket_policy` resource REPLACES a bucket's ENTIRE policy** -- the same singleton semantics
as the notification config. So declaring one carrying only the Deny would, on first apply, **delete both
CloudFront Allow statements, drop CloudFront's read on `json/*` and `json-tiered/*`, and take the portal
data plane dark -- including the very MDPF artifacts this hold exists to protect.**

> **The control, built naively from its own cited precedent, destroys the thing it protects.**

Confirmed: **no `aws_s3_bucket` or `aws_s3_bucket_policy` resource for `opal-data-portal-v2` exists
anywhere in `infra/aws/terraform/`.** Many roots reference it by ARN in IAM (`mdpf-pipeline`,
`market-overview`, `news-pipeline`, `fred-pipeline`, `globgrph`, `data-refresh`) -- none manages it.
The bucket is console-managed and unowned, exactly the pre-FIRMSEP.02 condition described in
`portal-auth/firm-bucket-cross-ref.tf:8-13`.

---

## THE THREE VECTORS, AND WHAT ACTUALLY CLOSES EACH

| # | vector | closed by | scope |
|---|---|---|---|
| V1 | a principal deletes the objects (console, CLI, script, cleanup sweep) | `Deny s3:DeleteObject` + `s3:DeleteObjectVersion` on `json/mdpf/*` | prefix-scoped, **clean** |
| V2 | a lifecycle `Expiration` rule expires them | `Deny s3:PutLifecycleConfiguration` on the **bucket** | **BUCKET-WIDE -- broader than the hold** |
| V3 | the producer stops writing (frozen input) | nothing here -- this is the DS decouple work item | out of scope |

**V2 WAS A SCOPE DECISION AND IT WAS NOT MINE. IT HAS NOW BEEN RULED: V2 IS IN.**

> **R5 (CTO, `MDPF_CONSOLIDATED_PLAN_20260722.md` @49687d1b2, owner `0.7.0_AE_CloudOps`):**
> *"Deliverable 2 includes the `PutLifecycleConfiguration` limb. Routine cleanup arrives as a lifecycle rule
> far more often than a hand-typed delete; shipping only the easy-to-test half is refused."*

I raised this as a never-widen concern and I stand by having raised it -- **but the ruling is right and my
framing under-weighted the actual threat model.** The realistic deletion of these objects is not a person
typing `delete-object`; it is a whole-bucket `Expiration` rule written by someone who never types the string
`mdpf` at all. **V1 alone closes the rare vector and leaves the common one open**, which is the
GREEN-while-still-open shape this document was written to refuse.

**WHAT TAKING V2 ACTUALLY COSTS -- stated plainly, because it IS broader than the hold:**
`s3:PutLifecycleConfiguration` is bucket-level and **cannot be prefix-scoped.** So this denies *all* lifecycle
management on `opal-data-portal-v2`, a bucket hosting many prefixes and several other pipelines' outputs --
**not just the MDPF prefix.** Two lifecycle rules exist today (`expire-noncurrent-versions-14d`,
`abort-incomplete-mpu-7d`, both whole-bucket) and **neither can be modified while this Deny stands.**

**CONSEQUENCE THAT NEEDS AN OWNER (new open item, CTO):** with `Principal = "*"`, the unlock path is "edit the
bucket policy first, then change lifecycle." That is the intended ratchet -- **the control outlives the person
who knew about it** -- but it means a legitimate future lifecycle change on this bucket has a prerequisite step
and **no named owner today.** An undocumented prerequisite is how a control gets ripped out in a hurry by
someone who reads it as an obstacle rather than a decision. **Name the owner, or the first person who needs a
lifecycle change removes the Deny.**

**Not taken (recorded so the ladder does not imply coverage it lacks):** *Object Lock on the specific objects*
-- narrower than V2, but a materially bigger change (versioning interactions, retention governance, per-object
legal holds), needs its own assessment. **Not costed, NOT closed by this deliverable.**

---

## DRAFT TF (V1, plus V2 shown but commented -- **NOT APPLIED**)

**Placement is an open question (CTO/COO):** the bucket is unmanaged, so this needs a home.
`portal-auth` already carries the read-only cross-ref pattern for firm buckets, but it is the live
serving-path root that was rolled back this morning -- I would rather not add an unrelated policy resource
there. A dedicated small root, or `shared-infra`, is safer. **Flagging, not deciding.**

```hcl
# ---------------------------------------------------------------------------
# opal-data-portal-v2 bucket policy -- TAKES OWNERSHIP of a previously
# console-managed policy. The two Allow statements below are REPRODUCED
# VERBATIM from live state (GetBucketPolicy, 2026-07-22 ~13:19Z). They are NOT
# new grants and NOT a widening -- omitting either one drops CloudFront's read
# on json/* and takes the portal data plane dark.
# THE PLAN MUST SHOW EXACTLY ONE ADDED STATEMENT AND ZERO REMOVED.
# Hold: DO_NOT_DECOMMISSION_portal-v2_json_mdpf_49financial_20260722.md @74677ea04
# ---------------------------------------------------------------------------
resource "aws_s3_bucket_policy" "portal_v2" {
  bucket = "opal-data-portal-v2"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # ---- REPRODUCED VERBATIM FROM LIVE STATE -- DO NOT EDIT ----
      {
        Sid       = "AllowCloudFrontOAI"
        Effect    = "Allow"
        Principal = { AWS = "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity EU39UXW7CMSI5" }
        Action    = "s3:GetObject"
        Resource  = "arn:aws:s3:::opal-data-portal-v2/*"
      },
      {
        Sid       = "AllowCloudFrontOACPublicData"
        Effect    = "Allow"
        Principal = { Service = "cloudfront.amazonaws.com" }
        Action    = "s3:GetObject"
        Resource = [
          "arn:aws:s3:::opal-data-portal-v2/json/*",
          "arn:aws:s3:::opal-data-portal-v2/json-tiered/*",
        ]
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = "arn:aws:cloudfront::313476888478:distribution/EVTSA9VEHNZVH"
          }
        }
      },

      # ---- THE ONLY NEW STATEMENT (V1) ----
      {
        # The MDPF revamp producer reads json/mdpf/49financial/aggregate-aua-timeseries.json
        # as a LIVE BUILD-TIME INPUT (dim_mdpf_aggregate_aua_timeseries.py:476-500, wired :812).
        # Deleting it silently breaks-or-FREEZES 49F account counts, and a frozen count is
        # indistinguishable from a stable roster -- nothing detects it. Deny > prose.
        # NOTE: this does NOT stop lifecycle expiry (service-performed, not principal-performed).
        # That is vector V2 and is NOT closed by this statement. See the design doc.
        Sid       = "DenyDeleteMdpfProducerInputHold20260722"
        Effect    = "Deny"
        Principal = "*"
        Action    = ["s3:DeleteObject", "s3:DeleteObjectVersion"]
        Resource  = "arn:aws:s3:::opal-data-portal-v2/json/mdpf/*"
      },

      # ---- V2 -- RULED IN BY R5. BUCKET-WIDE, NOT PREFIX-SCOPED. READ THE COST NOTE. ----
      {
        # Closes the vector V1 cannot: a lifecycle Expiration rule expires these objects
        # WITHOUT the string "mdpf" appearing anywhere in the change. Lifecycle expiry is
        # SERVICE-performed, never evaluated against a principal, so no prefix-scoped Deny
        # on DeleteObject can reach it.
        # DELIBERATELY BROADER THAN THE HOLD: s3:PutLifecycleConfiguration is a BUCKET-level
        # action and CANNOT be prefix-scoped. This freezes ALL lifecycle management on
        # opal-data-portal-v2, including the two existing whole-bucket rules
        # (expire-noncurrent-versions-14d, abort-incomplete-mpu-7d).
        # A legitimate future lifecycle change MUST edit this policy first. That prerequisite
        # needs a NAMED OWNER -- see "CONSEQUENCE THAT NEEDS AN OWNER" above.
        Sid       = "DenyLifecycleChangesProtectingMdpfHold20260722"
        Effect    = "Deny"
        Principal = "*"
        Action    = ["s3:PutLifecycleConfiguration"]
        Resource  = "arn:aws:s3:::opal-data-portal-v2"
      },
    ]
  })
}
```

> **NOTE THE TWO `Resource` SHAPES AND DO NOT "TIDY" THEM.** V1 targets `.../opal-data-portal-v2/*` (the
> OBJECTS); V2 targets `arn:aws:s3:::opal-data-portal-v2` (the BUCKET itself, no trailing `/*`). A bucket-level
> action against an object ARN matches nothing and the Deny silently never fires -- **a GREEN apply protecting
> nothing.** This is the same wrong-axis class as `comp-iam` reporting `[GRANTED]` on `(action)` while the real
> call fails on `(action, resource)`.

**`Principal = "*"` + `Deny` denies everyone including the account root and me.** That is intended for V1
(nothing should be deleting these) and is the 17a shape. It also means **removal requires a policy edit** --
which is the point: the control outlives the person who knew about it.

---

## EXERCISE PLAN -- behaviour-grade, and built so it CANNOT pass vacuously (Rule 22a)

The gap this hold protects was found by a positive control; the control that closes it gets one too.

| # | test | expected | why it is not vacuous |
|---|---|---|---|
| 1 | `delete-object` on a **throwaway** key under `json/mdpf/` | **AccessDenied naming the policy** | the real, denied path |
| 2 | **ISOLATED POSITIVE CONTROL, SEPARATE INVOCATION** -- same delete against a key **outside** `json/mdpf/` | **SUCCEEDS** | proves the test CAN fail, i.e. the deny is doing the work and not a blanket refusal |
| 3 | **V2 limb, on a SCRATCH BUCKET -- never on portal-v2. NOW MANDATORY (R5), not conditional.** | `PutLifecycleConfiguration` **DENIED** with the policy; same call **SUCCEEDS** without it | exercises the lifecycle limb behaviour-grade **without a live-estate mutation and without waiting a day for an expiry to fire** |
| 3b | **V2 wrong-axis mutant, scratch bucket** -- same Deny written against the OBJECT ARN (`.../opal-data-portal-v2/*`) instead of the BUCKET ARN | `PutLifecycleConfiguration` **SUCCEEDS** (Deny never matches) | **proves the ARN shape is load-bearing.** Without this, a V2 statement that silently matches nothing passes tests 1-4 unchanged -- a GREEN apply protecting nothing |
| 4 | CloudFront still serves `json/mdpf/...` post-apply (curl a real served key) | **200** | proves the reproduced Allow statements survived -- **the outage check for Defect 2** |

**Rule 22a compliance:** test 2 runs as a **separate invocation**, never batched with test 1 (a control
batched with its target is corrupted by its own presence). **If I exercised only test 1 I would be
certifying a control whose second limb I never tested** -- which is precisely the WS-5 `.json` mistake in
a different costume.

**Test 4 is not optional.** Defect 2 means the plausible failure of this deliverable is not "the Deny
didn't work" but "the Deny worked and I dropped a CloudFront grant." The exercise must cover the failure
mode the *change* introduces, not only the one it *prevents*.

---

## OPEN ITEMS BEFORE APPLY

**THE APPLY ITSELF IS HELD** pending Andrew's fabric-wide MDPF advisory (CTO narrowed carve-out 1,
@8da5fbfa5). Items 1-2 are ruled; the rest are live.

1. [x] **Andrew** -- 07-17 alert-suspension adjacency. **RULED ~1425Z:** *"THere should be a gate/hook for
       this, but not an 'Alert' not an SES or something like that."* Gates/hooks in scope; alerts suspended.
       This Deny stops something and pages nobody. Surfaced rather than assumed, which was correct.
2. [x] **CTO** -- V2 scope call. **RULED by R5: the `PutLifecycleConfiguration` limb is IN.** Uncommented above.
3. [ ] **CTO** -- placement: which TF root owns a policy for a previously unmanaged bucket. COO's `desired`
       read is `shared-infra`; **that is my starting hypothesis, not my conclusion.** I confirm on the
       `applied` limb by reading the plan, not by trusting the root name.
4. [ ] **CTO (NEW, raised by R5)** -- **name the owner of the lifecycle-unlock path.** V2 means a legitimate
       future lifecycle change on this bucket must edit the policy first. An unowned prerequisite gets ripped
       out by whoever first reads it as an obstacle.
5. [ ] Plan must show **exactly TWO added statements (V1 + V2), zero removed/changed.** *(Was "exactly one"
       before R5 -- updated deliberately; the acceptance count is part of the control.)* A plan that is not
       pure-add is out of scope and I stop.
6. [ ] Source-map entry (Rule 4) + tag after 0-diff (Rule 6). `safe-apply` only (Rule 18), never bare.
7. [ ] Update `pipeline_inventory.xml` post-0-diff, and correct its Known Issue #9 (`opal-data-portal-v2`
       not in TF) if this lands -- it would be partially resolved.

**DO NOT MOVE THIS FILE'S HCL INTO `infra/` UNTIL THE APPLY IS RELEASED.** A `.tf` in a root is reachable by
any untargeted apply in that root. Keeping it here is the same discipline PART 0 rule 1 enforces on
`portal-auth` -- staged-but-unapplied code in a live root is indistinguishable from drift to everyone who
did not stage it.
