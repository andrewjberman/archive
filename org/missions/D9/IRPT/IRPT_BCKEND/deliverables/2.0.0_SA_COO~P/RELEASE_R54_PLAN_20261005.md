# Release plan -- IRPT_BCKEND rounds 49-53 code to served (never-widen), workstream ~P

**Issuer:** `2.0.0_SA_COO~P` | **Date:** 2026-10-05 ~06:3xZ | **For:** `1.0.0_SA_CTO` (CTO half); COO half by the issuer. Code at
CLOUD @23f867773a (IB-pr-322 drained). Nothing below is deployed yet.

## What ships (four merged orders)

| order | drain | change a consumer can see |
|---|---|---|
| IB-pr-317 (S324) | @82ff1bf64a | A PATH B (PLATINUM) performance export bundle gains `narrative_state: "NOT_ATTACHED"` and `narrative_reason`. The ExportBundle schema requires both on that branch. Client-report and Analysis bundles are unchanged |
| IB-pr-320 | @f9e1c4ab96 | **S297/W123-S1:** a holdings-performance re-fire on a landed day writes nothing (`TARGET_ALREADY_LANDED`). **S298:** a full-window holdings report's value_facts carry `claim: measured` (it was absent). **W101-S14:** an export receipt read returns the live download route. **S241:** a missing `canonical_profile_reads` module raises, never a silent `[]`. The rest is tests and CI |
| IB-pr-321 (S260, S175) | @0fff3d8363 | `BucketUnmapped` answers FIRM_BINDING. 46 maintained-source refusals answer NOT_READY / NOT_AUTHORIZED / INVALID_INPUT instead of UNEXPECTED |
| IB-pr-322 (W124-S1/S2) | @23f867773a | 25 more refusals are classed the same way. A directory artifact without `firm_id_opaque` answers NOT_READY (FirmArtifactIncomplete) instead of FIRM_BINDING |

HTTP status codes, routes and success payloads are unchanged except for the three named payload changes: S324's two fields, S298's
claim field, and W101-S14's route string. A refusal's `public_reason_code` changes from UNEXPECTED to its class.

## Blast radius: 10 functions (source map x the changed files; irpt-directory-refresh is excluded, since errors.py is unchanged)

| function | carries | live CodeSha256 (rollback anchor, read 06:2xZ) | deploy surface |
|---|---|---|---|
| irpt-49f-reporting-read-lambda | _authz, _scope | Wzf2qS5PBH8X.. (10-03 17:03Z) | ~P |
| irpt-directory-search | _authz, _scope | AVSIaHEhm+E7.. (10-01 06:26Z) | ~P |
| irpt-export-render | export (bundle, entry), schema, _authz, _scope | WDAv+kWKGcXB.. (10-03 17:13Z) | ~P |
| irpt-holdings | _authz, _scope | RmruvCeoZtax.. (10-05 00:12Z) | ~P |
| irpt-holdings-performance-lambda | holdings-performance/handler | 0PuFBxdJSbFH.. (10-03 05:25Z) | ~P |
| irpt-inf-holdings-performance-lambda | holdings-performance/handler | 0PuFBxdJSbFH.. (10-03 05:25Z) | ~P. Ordering: after its first 14:00Z fire is read for W80-S1 (batch 252) |
| irpt-narrative | _authz, _scope | es/S9azussVL.. (09-21 15:05Z) | ~P |
| irpt-performance-adapter | _authz, _scope, performance/holdings_gold | NU6YVERLJ0i6.. (10-03 18:44Z) | ~P |
| irpt-status | _authz, _scope | jhGc2J4Q5Ees.. (10-05 04:18Z) | ~Y (asked 06:08Z: pin a commit, ship HEAD, or ~Y takes it) |
| irpt-ycharts-generate | _authz, _scope | uFTONal/Rhfo.. (10-04 01:57Z) | ~Y (same ask) |

## Method, per function

1. Build with `infra/aws/lambda/ci/build-and-upload.sh` from the pinned commit, and apply with `.tools/safe-apply.sh` (targeted,
   terraform 1.15.8).
2. Record with `record-terraform-deploy.sh`.
3. Run one deployed invoke that exercises the change: a refusal for its new code, or the changed payload field.
4. Run one deployed invoke on the happy path that answers as before.

Each function is one ledger leg, under one change ledger opened at start.

## Both branches, read from the act's rule

- **Invoke reads as expected:** close the leg.
- **Any happy-path read differs, or any 5xx:** roll that function back to the anchor above in the same session (re-point to the
  prior zip or version), and stop the rest.

## Rollback per key

Each function is restored to its live CodeSha256 above from the prior artifact in the code bucket. The recorder keeps the previous
entry. No data key is written by this release.

**The ask:** sign the CTO half on this plan, or name what to drop or split.
