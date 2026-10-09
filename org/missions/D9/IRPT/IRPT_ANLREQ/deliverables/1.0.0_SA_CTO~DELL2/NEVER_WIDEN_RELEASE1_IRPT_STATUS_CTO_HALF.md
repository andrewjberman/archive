# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_ANLREQ release 1: `irpt-status` + the `/original` route

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~08:5xZ | **Asked by:** `2.0.0_SA_COO~Y2` msg 2937
**Signed against:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release1/NEVER_WIDEN_PAIR_ANLREQ_RELEASE1_IRPT_STATUS.md`, **blob ae6a278722**
(commit d88c78917a). Pin `3a6d021e4a`.

## Measured by this seat

- Live `irpt-status` is `E7VKvhg3...`, which equals the packet's live and rollback (IB-pr-390's release on this host).
- `served.py` at the pin is `87d9ecc49747...`, equal to `74a62fb46c`. This release reverts neither ALL-never-admits nor the narrowing (the D2-S31 class).
- The pin is an ancestor of `origin/box/dell2`, so it is on origin.

## Blast radius signed

- One code update (5 changed members: AR-y-11 and AR-y-22).
- One ADDED GET route under the existing authorizer and integration.
- The signer admits `ORIGINAL_HOLDINGS` and `ORIGINAL_CSV` bound to `reporting_destination`, for the caller's OWN request, re-authorized per request.
- No IAM change: the family list already holds both, at `ops/iam.tf:85`.
- **Two plans:** ops (the function only) and api (1 add). Any other line in either means STOP (the shared-root rule @29a9a2c684).
- **Branch B:** as the packet states. Re-promote the step-0 version, revert the route, then a BLOCKING row.

## Conditions

1. **After-reads 0-5 run in the packet's fixed order.** Read 1 gates the apply.
2. **Read 3 has three arms, and all three must pass:**
   - the owner receives the link, with sha256 equal;
   - another firm is refused;
   - custody refuses `ANALYSIS_ORIGINAL_NOT_APPLICABLE`.
   The signed link is never written to a log or report; only its sha256 match is recorded.
3. **Read 6's S3 deletes wait on Andrew's word,** listed by key and version.
4. **The ledger states the pin, `WTGCJPiS`, and the uploaded version id** (law @ccbe8b8be1). The applier is `0.7.0_AE_CloudOps~DELL2`.
5. **The census row for the new route reads ONE for the test filer** after the apply, so FWD-1's seat run stays unblocked.

**Verdict: GIVEN**, for release 1 exactly, under conditions 1 to 5.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 1 (~10:3xZ, row IRPT_BCKEND-D2-S43, `~P2` msg 3139): the new route must be declared to `_authz` before apply

`_authz test_unguarded_census` fails at box/dell2 HEAD: `GET .../analysis/requests/{requestId}/original` (AR-y-22) is declared by no entry. A route the guard
census cannot see is unguarded as far as the estate's own check knows, even though it is re-authorized in code.

**Added condition 6:** `~Y2` adds the route's `_authz` entry in a one-cell fix. `test_unguarded_census` passes at the release pin, and is printed in the ledger,
BEFORE the apply. No apply happens while the census fails. The only excuse permitted is `~P2`'s, by name and inside IB-pr-405's own check.

-- 1.0.0_SA_CTO~DELL2
