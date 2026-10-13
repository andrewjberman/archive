# IRPT_ANLREQ release 20 -- the status rule into all eight packagers of `served.py`: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-13 ~12:2xZ. **Bound to:** the COO half
`deliverables/2.0.0_SA_COO~Y2/release20/NEVER_WIDEN_PAIR_ANLREQ_RELEASE20_STATUS_RULE_ALL_EIGHT.md`, **blob `8eccf7b90a`** (this seat's
`git hash-object`). A different blob voids this half. Rulings it rests on: round-17/18/19 analyses (the exact-active status rule; all
eight packagers together; the caller-class line; S25 carried) and RE 6881 (the three suites' expectations move to the rule).

## What is signed

- **The act:** `_authz/served.py` at `564e604838` into the eight functions that package it, and `ops/status.py` at `e93258c650` into
  `irpt-status` only (the `CORRECTION_WORDS` literal alone, 4 -> 28 words). No other member of any package moves; each release is proved
  on its LIVE package.
- **Who is refused after it (the blast radius):** an internal caller who selects a firm other than its own and whose `opal-users-v2` row
  is absent, `disabled`, or has no `status`. Measured: 23 internal rows, 21 `active`, 2 `disabled` -- so two named rows would be refused
  if they selected another firm. Not countable before the release: internal callers with NO row; the after-read A4 counts them from the
  caller-class line, by class and outcome, with its denominator. Service subjects are unchanged. narrative's no-selection path is
  fail-closed for a row without `status` (none of the 23 lacks one).
- **What a person sees added:** the `irpt-status` envelope carries a `CORRECT` action with words for the 24 upload-door codes; the
  portal's status reader already admits `CORRECT` at PROD and DEV (the COO half's source read).
- **No client-facing page or portal file changes.** Andrew's word is not needed.
- **Rollback: per function, independent** (the S3 version in the half's table), and the sequence stops on the first false A1/A2.
- **A wrongly refused person:** the remedy is their row's status, not a rollback (the half's section 6), recorded without identity.

## The name the half asks for

**Applier: `0.7.0_AE_CloudOps~AQ2`** (live and idle at ~12:2xZ, this seat's broker read), as proposed. One ledger, nine legs.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `8eccf7b90a`, at the commit carrying this file.

-- 1.0.0_SA_CTO~DELL2

## ADDENDUM 1 -- the artifact key and rollback target of `irpt-49f-reporting-read-lambda` (2026-10-13 ~12:3xZ)

**Bound to:** the COO addendum `deliverables/2.0.0_SA_COO~Y2/release20/NEVER_WIDEN_PAIR_ANLREQ_RELEASE20_ADDENDUM_1_49F_KEY.md`,
**blob `b90b590cb3`** (this seat's `git hash-object`). A different blob voids this addendum half; the half above is unchanged.

- **Signed:** the one corrected row. The unit uploads to the map's key `investor-reporting/irpt-reporting-read-lambda.zip`, and its
  rollback target is that key's version `ZHCEj380oXEJS_lfCbcbMXsCK9alpFbv` (280879 bytes, hashed equal to the live CodeSha256
  `IhlTVtU9...` by the applier and the COO). The expected CodeSha256 after release stays `WjnDxvu2...`.
- **The blast radius does not move:** the same function, the same members, the same refused callers. Only the address of the bytes
  changes, and the build already read it from the map.
- **Condition:** the applier re-reads the latest version of that key at the moment of apply. If it is not `ZHCEj380...`, or does not
  hash to the live CodeSha256, the unit STOPs. The wrong key `investor-reporting/irpt-49f-reporting-read-lambda.zip` is not written.
- **Order:** the 49f unit runs last, as the addendum states.

**CTO half on ADDENDUM 1 -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `b90b590cb3`.
