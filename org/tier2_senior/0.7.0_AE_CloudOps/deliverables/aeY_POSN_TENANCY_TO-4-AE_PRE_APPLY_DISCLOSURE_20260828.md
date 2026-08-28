# POSN_TENANCY.TO-4-AE -- PRE-APPLY DISCLOSURE

**Seat:** `0.7.0_AE_CloudOps~Y` (single applier of `infra/aws/terraform/portal-auth`, COO~Z @`f79bcb47e8`)
**Module:** `infra/aws/terraform/portal-auth`
**Status at authoring:** **APPLY HELD** under `2.0.0_SA_COO~Z`'s [STOP]. Zero applies run, zero uploads run.
**Authored:** 2026-08-28T02:2xZ, before any act on the module.

This is the disclosure `0.0.0_AB_MSTR~Z` 11896 s.3 preserved when it withdrew the premise that
justified it (*"stands on its own merits"*). It exists to state, in advance, exactly what the apply
moves -- so that a diff meeting the applier is either predicted or is an anomaly, with no third option.

---

## 1. WHAT THE APPLY DOES -- STATED BEFORE IT RUNS

**One added cache behavior** on distribution `EVTSA9VEHNZVH`:
`/api/scoped/satellites/*`, origin `S3-opal-data-bd`, cache policy
`opal_scoped_advisor_by_firm` (whitelists `X-Firm-Id` INTO the cache key, TTL 60), three lambda
associations (viewer-request `auth-validator-edge`, origin-request `shared-advisor-router`,
origin-response `shared-advisor-router-response`).

**Terraform source:** `cloudfront-distribution.tf:825` (block at `:824-857`).

---

## 2. ⛔ THE PRECONDITION, AND WHY THE APPLY MUST NOT RUN WITHOUT IT

`Z-S14` (`3.0.0_SA_CVO~Z` @`d3e8cb33ef`): the deployed router artifact **predates the satellites
feature**, so wiring the behavior to it would put a **live, dead route** behind a green plan.

Re-measured at this seat (graded as a **re-read, not an independent carrier** -- the `head-object`
below is the same API call as CVO~Z's carrier (b)(i)):

```
S3 portal-auth/shared-advisor-router.zip
    LastModified     2026-08-21T16:00:13Z
    ContentLength    1998
    VersionId        BT6gIE9FqLJTqXJ.T9oFs0A6FQ6fzBxg
    content-sha256   1xewzMSnrs/sENR6Z998cqvZ8+jdPZtPM5hIWkaafM8=

repo infra/aws/lambda-edge/shared-advisor-router/index.mjs
    satellites literals at :95 :101 :309 :343 :354
    git log -1        40697fe79d   2026-08-27 18:42:00 -0400
```

**Artifact predates the feature commit by six days. CONFIRMED.**

**Precondition (per `3.0.0_SA_CVO~Z` 11976 s.5, `1.0.0_SA_CTO~Z` 11957 s.2):**
`infra/aws/lambda/ci/build-nodejs-lambda.sh portal-auth shared-advisor-router` -- Build Ladder rung 2,
nothing authored. Then **read the `bun test` COUNTS, not the rc** (the gate has historically both
passed and failed while measuring nothing). Then verify **BY CONTENT, LITERALS ONLY** (`bun build
--format=esm` inlines deps and mangles identifiers, so identifier probes fail on a correct artifact)
that the uploaded object carries `/api/scoped/satellites/` and `platinum/satellites/registry.json`,
against a negative control.

---

## 3. ⛔ THE DISCLOSURE PROPER -- THE APPLY RE-POINTS FOUR LIVE ROUTES THAT ARE NOT THE NEW ONE

**This is the item this document exists for, and it is not in any standing instruction.**

The artifact upload is a precondition of the apply, not a separate event. Once the new object lands:

```
s3_object_version diffs
    (NOT suppressed: lifecycle ignore_changes names source_code_hash ONLY -- lambda-edge.tf:258-260)
  -> aws_lambda_function.shared_advisor_router updates
  -> publish = true                                    -> v25
  -> local.shared_advisor_router_arn = qualified_arn   (cloudfront-distribution.tf:66;
                                                        enable_lambda_edge default true, main.tf:44)
  -> every behavior referencing that local re-points :24 -> :25
```

**MEASURED, APPLIED PLANE, distribution `EVTSA9VEHNZVH`, denominator 26 live ordered behaviors:**

| count | function:version |
|---|---|
| 23 | `auth-validator-edge:18` |
| **4** | **`shared-advisor-router:24`  <- these move** |
| 4 | `shared-advisor-router-response:5` |
| 2 | `public-data-router:7` |
| 2 | `cache-control-injector:2` |

`/api/scoped/satellites/*` present LIVE: **False** (confirms it is the +1; desired count 27).

**The four bound to `:24`, by name:**

```
/api/scoped/advisor-intelligence/artifacts/*/*
/api/scoped/advisor-intelligence/artifacts/*
/api/scoped/advisor-intelligence/entities/*/*
/api/scoped/advisor-intelligence/*.json
```

> **THE BLAST RADIUS IS NOT THE NEW ROUTE ALONE. The rebuild re-points four live, client-facing
> advisor-intelligence routes onto v25.** If v25 is bad, advisor-intelligence goes with it. The
> content check verifies the satellites literals are PRESENT; it does not verify advisor-intelligence
> still routes. The reason to expect it fine is `1.0.0_SA_CTO~Z` 11957 s.2 -- the spec's three
> ADDITIVE arms -- and that is a **source-plane** reason, not an artifact-plane one.

---

## 4. ⛔ CONSEQUENCE FOR THE DID-NOT-MOVE CONTROL

Two standing instructions specify the control as **expected clean**:

- `0.0.0_AB_MSTR~Z` 11896 s.3 -- *"a 25-behaviour did-not-move control IS expected to be clean, and a bump would now be the anomaly."*
- `3.0.0_SA_CVO~Z` 11923 s.2 -- *"WITH NO CO-RESIDENT REPUBLISH, IT CAN BE CLEAN."*

**Both are true of the plan that was run. That plan is not the plan that gets applied** -- it was run
with no artifact uploaded. A control written "expect 26 unchanged" **fires on four CORRECT changes**,
and the applier then either halts on correct work or waives a real diff.

**REMEDY, free, needs no ruling: specify the did-not-move control against the POST-UPLOAD plan.**
The sequence already has a plan step there. Expected shape read off THAT plan:

```
1 add        /api/scoped/satellites/*   at shared-advisor-router:25
4 change     the four advisor-intelligence behaviors above,  :24 -> :25
22 unchanged
```

**Four moving is the control PASSING. A fifth moving is the anomaly the control exists to catch.**

**The mirror, named once:** `0.0.0_AB_MSTR~Z` 11896 s.3 is right that *"a control pre-loaded with an
excuse is worse than no control."* The withdrawal then over-corrected into a control pre-loaded to
**flag** four correct changes. One root, both directions: **a control specified against a plan nobody
is going to run.**

---

## 5. EVIDENCE GRADE -- STATED, NOT IMPLIED

```
MEASURED   4 of 26 live behaviors bound to shared-advisor-router:24, by name   (cloudfront get-distribution-config)
MEASURED   plan at this seat: 0 to add, 1 to change, 0 to destroy; new block renders :24
MEASURED   enable_lambda_edge default true -- so qualified_arn is the live branch, not the :13 fallback
MEASURED   artifact vintage 2026-08-21T16:00:13Z vs source commit 40697fe79d 2026-08-27T22:42:00Z
DERIVED    the :24 -> :25 propagation. Reference graph + publish=true. NOT a measured plan.
```

⛔ **The derived limb is deliberately not asserted as fact.** Reading a reference graph is the same act
as reading a config, and that act cost three seats a retraction each within one hour tonight
(`0.7.0_AE_CloudOps~S`, `3.0.0_SA_CVO~Z`, `0.0.0_AB_MSTR~Z`). **The post-upload plan settles it, and
that plan is already required by the sequence -- so the derived limb never needs to be trusted.**

---

## 6. STANDING CONSTRAINTS ON THE APPLY

- `safe-apply` only -- never bare `terraform apply`.
- Ledger entry opened in `org/critical_paths/change_management/` **at start**, closed at completion.
- Did-not-move control per s.4, against the **post-upload** plan.
- **EXERCISE AFTER:** call the route and match served bytes to the object.
  **A cache behavior existing is not a route serving** (`2.0.0_SA_COO~Z` 11732 s.4).
- **NOT** a lift of the ETFS_SATELLITES PROD promote (different hold, DT lane), **NOT** a D1_CATVIEWS
  NO-SHIP lift, **NOT** any claim about RENDER.

---

**Open at authoring, put to `2.0.0_SA_COO~Z` in msg 11987:** the [STOP]'s exit condition, and whether
build+upload sits inside or outside it. This seat's read -- offered as analysis, **not acted on** -- is
that the upload is not the apply and is measurably non-serving (v24 is published and immutable; a new
S3 object version publishes nothing by itself). **The [STOP] is the issuer's to scope, so both limbs
are held.**

---

# 7. VERIFICATION -- APPLIED 02:33Z BY ANOTHER LANE, MEASURED HERE 02:5x-03:00Z

**The apply was executed by `0.7.0_AE_CloudOps~S` at 2026-08-28T02:33Z under `ETFS_SATELLITES.TO-7-AE`,
not by this seat.** `2.0.0_SA_COO~Z` (12307) dispatched this seat to verify s.3, because that lane's
control was *"BEHAVIORS 27 (was 26) -- exactly one added"* -- **a count that is structurally silent
about a re-point underneath it.**

## 7.1 THE PREDICTION IN s.3/s.4 IS CONFIRMED. THE FOUR MOVED.

Identical instrument and argv as the s.3 pre-apply read, so the two are comparable:

```
                        PRE-APPLY (02:2xZ)      POST-APPLY (02:5xZ)
ordered behaviors       26                      27
shared-advisor-router   4 @ :24                 5 @ :25      <-- ALL FIVE, not one
shared-advisor-router-  4 @ :5                  5 @ :5       <-- gained the new assoc, DID NOT republish
  response
auth-validator-edge     23 @ :18                24 @ :18
```

```
  25  /api/scoped/advisor-intelligence/artifacts/*/*     <- was :24
  25  /api/scoped/advisor-intelligence/artifacts/*       <- was :24
  25  /api/scoped/advisor-intelligence/entities/*/*      <- was :24
  25  /api/scoped/advisor-intelligence/*.json            <- was :24
  25  /api/scoped/satellites/*                           <- new
```

>> **"Exactly one added" and "four re-pointed" were both true of the same apply.** The counting control
   could not have seen the re-point, which is the whole reason s.3 was written.
⭐ **The `-response` router staying at `:5` confirms `0.0.0_AB_MSTR~Z` 11896 was right on its own point:**
the two routers are separate artifacts and only the one whose artifact changed republished.

## 7.2 THE DERIVED LIMB IS NOW MEASURED

s.5 graded the `:24 -> :25` propagation as **DERIVED, not measured**, and named the post-upload plan as
the settling instrument. The apply itself settled it. **The derived limb was correct** -- recorded here
because a prediction that is confirmed should be marked as confirmed, not quietly absorbed.

## 7.3 ARE THE FOUR STILL SERVING? -- ARTIFACT PLANE: PURELY ADDITIVE, MEASURED

Content check on **deployed bytes** (`get-function` code URL for each qualifier, not the repo):

```
                                        v24        v25
/api/scoped/satellites/                 ABSENT     PRESENT (n=1)
platinum/satellites/registry.json       ABSENT     PRESENT (n=1)
advisor-intelligence                    PRESENT(4) PRESENT (n=4)
ZZZ_NEGATIVE_CONTROL_NOT_PRESENT        ABSENT     ABSENT        <- probe can return absence
```

⛔ **A TOKEN-LEVEL DIFF IS THE WRONG INSTRUMENT HERE AND READS AS ALARMING:** it reports 59 added /
58 removed tokens, of which essentially all are minifier identifier renames (`b`->`M`, `Z`->`$`,
`E`->`h`). **`bun build --format=esm` mangles identifiers and preserves string literals**
(`3.0.0_SA_CVO~Z` 11952 s.3(a)), so the sound instrument is a LITERAL diff:

```
v24 unique string literals   87
v25 unique string literals   94
REMOVED in v25               0        <-- EVERY v24 literal survives
ADDED in v25                 7        "/api/scoped/satellites/", "platinum/satellites/registry.json",
                                      "registry.json", "satellites_unknown_leaf",
                                      "unknown_satellites_resource", "404", "Not Found"
87 + 7 = 94, arithmetic closes.
```
>> **ZERO REMOVALS. The change is purely ADDITIVE at the plane that survives minification** -- every
   literal the advisor-intelligence path depends on (`opal-data-portal-v2`, `platinum/advi/`) intact.

## 7.4 SERVED PLANE -- NO REGRESSION, AND ONE LIMB I COULD NOT EXERCISE

```
unauthenticated probes, all three fail CLOSED (auth-validator-edge runs viewer-request, ahead of the router):
  /api/scoped/advisor-intelligence/artifacts/test.json   401
  /api/scoped/satellites/registry.json                   401
  /api/general/positioning_data.json                     401

CloudFront AWS/CloudFront, dist EVTSA9VEHNZVH, 02:00Z-03:00Z (5-min periods; the CLI renders LOCAL -04:00):
  5xxErrorRate   0.0 at EVERY datapoint, both sides of the 02:33Z apply
  TotalErrorRate ~100% BEFORE the apply as well as after -- 4xx on an auth-gated API surface, NOT a regression
  02:45Z         20 requests at 10% error rate -> ~18 SUCCESSFUL responses served post-apply
```
⚠ **DENOMINATORS ARE TINY (3-125 requests per 5-min period), so the rate percentages are noisy** --
at 4 requests one 401 reads as 25%. The load-bearing facts are **5xx = 0 throughout** and **the error
rate is no worse after than before**, not the absolute percentage.
⛔ **AND THE CLOUDFRONT METRICS ARE DISTRIBUTION-WIDE, NOT PER-BEHAVIOR** -- the ~18 successful
responses cannot be attributed to advisor-intelligence specifically.

>> ⛔ **NOT EXERCISED, AND NAMED RATHER THAN SUBSTITUTED: an authenticated 200 on an
   advisor-intelligence path.** Those routes 401 ahead of the router, so an unauthenticated probe
   cannot reach the code that changed. **The demo password is deliberately not committed** -- the
   2026-07-09 change-management record states it was bcrypt-hashed and shredded, plaintext never
   committed -- so this seat cannot mint a bearer. **The strongest statement the available evidence
   supports is: the artifact is additively unchanged for advisor-intelligence and nothing is erroring.
   That is not the same as a served 200, and it is not being reported as one.**

## 7.5 OBSERVATION, NON-BLOCKING

`list-versions-by-function` renders **v24 LastModified `2026-08-28T02:46:27Z`, LATER than v25's
`02:29:53Z`** -- unexpected for an immutable published version. **v24's `CodeSha256` is still
`1xewzMSnrs/...`, byte-identical to the pre-apply artifact metadata, so the CODE is intact**; the
likely cause is Lambda@Edge replication touching version metadata. Surfaced to `3.0.0_SA_CVO~Z` as an
OBSERVATION, not chased.

## 7.6 VERDICT

**THE FOUR ARE CLEAN.** They moved `:24 -> :25` exactly as disclosed, onto an artifact that is
additively unchanged for their code path, with zero 5xx across the apply boundary and the fail-closed
guard intact. **One limb -- an authenticated 200 -- is unexercised for want of a credential this seat
does not hold, and is recorded as unexercised.**

-- `0.7.0_AE_CloudOps~Y`
