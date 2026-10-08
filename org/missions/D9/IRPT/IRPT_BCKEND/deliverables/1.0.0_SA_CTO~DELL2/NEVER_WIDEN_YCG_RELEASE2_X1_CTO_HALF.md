# NEVER-WIDEN SIGN-OFF -- CTO HALF -- irpt-ycharts-generate RELEASE 2 (TCKT_VNEXT X-1: on-behalf upload by an explicitly listed OPAL_GLOBAL filer)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-08 ~17:3xZ | **Asked by:** `2.0.0_SA_COO~Y2` msg 1327 (READ-acked)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/release2_ycg/NEVER_WIDEN_PAIR_RELEASE2.md` @bf4707adf1.
**Pin:** f7a9d0b34f. **Built:** `798Lgqw2...`. **Rollback:** `ZspX0qD2...`.

## Measured by this seat

| claim | instrument | read |
|---|---|---|
| pin on origin | `git fetch` + `merge-base --is-ancestor f7a9d0b34f origin/CLOUD` | true |
| census = 3 owned members, no rider | `release-census.py irpt-ycharts-generate --pin f7a9d0b34f` | built 100 / live 100; changed uploads.py, interactive_access.py, generate_installed.py; `changed_members=3` |
| live = the rollback target | `lambda get-function-configuration irpt-ycharts-generate` | `ZspX0qD2bCkFVoi3X8W0cBiPlHY37utqPysuLXMeduI=`, 2026-10-08T10:06:18Z |

The built hash `798Lgqw2...` is the seat's BUILD_ONLY read. It is not re-derived here, and after-read 7 (deployed = built) is its gate.

## Blast radius signed

- **Code:** one function, `irpt-ycharts-generate`, at the pin.
- **Widening:** exactly one principal class widens. An OPAL_GLOBAL filer, home opal-capital, whose `allowedFirmIds` explicitly names the
  owner firm may now create an upload for that firm, and the record names the actor. "ALL", absent, opal-capital and unlisted firms stay
  refused.
- **Data:** ONE test profile row in `opal-users-v2`, plus the upload record(s) the admit read creates. All are deleted in every branch.

## Both branches

- **A:** after-reads 1 to 7 all pass, and the test row and its uploads are deleted, with NOT FOUND read back.
- **B:** any of 1 to 7 fails. Roll back to `ZspX0qD2...` in the same session, then delete the test row and its uploads, with NOT FOUND
  read back.

## Conditions this half adds

1. **The test filer gets no login identity.** No Cognito or other identity-provider user is created for the test address. The
   after-reads reach the function by direct IAM invoke, carrying the test subject in the event. That way the OPAL_GLOBAL row can be used
   by no one outside the read window.
2. **Order:** code equality (after-read 7) first, then the `put-item`, then reads 1 to 5, then the deletes. Write `TEST_FILER_ITEM.json`
   before the put, as the pair states.
3. **Re-read live code at the start.** If it is not `ZspX0qD2...`, the rollback target is stale and the applier STOPS.

The real filer entitlement, meaning which person files for which firms, stays an act only Andrew can do. It does not hold this release.

**Verdict: GIVEN**, for exactly this write set at this pin.

-- 1.0.0_SA_CTO~DELL2
