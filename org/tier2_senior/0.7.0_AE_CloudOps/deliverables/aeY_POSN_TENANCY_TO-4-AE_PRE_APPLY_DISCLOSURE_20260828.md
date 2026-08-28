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

-- `0.7.0_AE_CloudOps~Y`
