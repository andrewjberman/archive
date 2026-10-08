# L8 drain end -- IRPT_BCKEND round 72, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-07 ~21:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD (IB-pr-355, 357, 358;
nothing deployed here) and LOCAL (IB-pr-356, portal)

**Cut from:**
- CTO ruling msg 973 (row W162-S1, option (a): the custody report read);
- CTO ruling msg 998 (row IRPT_YCDGEN-S16: the F1 stop);
- the issuer's ruling on row W163-S1 (the upload door's reader).

Issuance @f9b9472ee6, decomposition section 65. **Judgment criteria:** 0 in all four orders.

## The orders

| order | slot | drain | result |
|---|---|---|---|
| IB-pr-355 custody report read route | ~164 | @5c3067c649 | `GET /api/scoped/investor-reporting/custody-report/{reportId}` (operation custody-report-read on irpt-export-render), authorized by `retained_export.resolve`. The routes.json row is added. IB72-1-AC1 PASS (export 22, census 9); IB72-1-AC2 PASS after AMENDMENT 1 (see below). Flipped complete by the issuer @6eca7b8ae4. |
| IB-pr-356 print page reads and mounts the custody report | ~165 | @85c56b2381 (workspace); portal @b3fedfea on `wk-IRPT_BCKEND-165-portal` (CTO DEV review asked) | The client op, the manifest, resolveBundle and PrintEntry mount ClientReportDocument; an unknown kind is still refused with 0 requests. IB72-2-AC1 PASS (15 pass) and IB72-2-AC2 PASS, re-run by the issuer in the worker's worktree. Supersedes IB-pr-353. |
| IB-pr-357 response_envelope drops internal_correlation_id | ~166 | @c246d6a180 | IB72-3-AC1 PASS at HEAD (envelope 4; census 9); the pin test failed before the fix. |
| IB-pr-358 upload door passes the profile reader | ~166 (re-seated) | @c246d6a180 | `compose_upload` in reports/generate_installed.py passes `CanonicalProfileReaders.get_user`, memoized once per request. IB72-4-AC1 PASS at HEAD (26 passed). |

## Issuer defects and corrections on the record

1. **AC2 check defect (row W164-S3).** IB72-1-AC2 sliced the ROUTES dict at the first `}`, which is the brace inside `{exportId}`. Fixed
   by AMENDMENT 1 @169e6c8150, which also adds `custody_read.py` to the export build list (row W164-S1).
2. **Release premise.** The ruling first held that "any build ships both". A census at the bytes showed four staged rows hold old blobs
   (served.py, generate_installed.py, uploads.py, interactive_access.py), so a build at HEAD shipped none of IB-pr-357/354/358 or
   IB-yr-631. Record @7e28cd9ec5. The CTO split the release (msg 1091):
   - **Release 1:** IB-pr-357, pin 1b5afe6a49. The served.py row is re-pinned for irpt-ycharts-generate only. The census at the pin
     is 20 members, served.py built 7cc704 = IB-pr-357; rider IB-pr-326.
   - **Release 2:** X-1, after its own re-pin.
3. **Re-seat.** A finished worker could not be resumed, so slot ~166 was re-seated cold for IB-pr-358 with IB-pr-357's commits as
   inherited state.

## Rows

| row | what it records |
|---|---|
| W164-S1 | Disarmed: the build-list line was added @169e6c8150. |
| W164-S2 | INERT. |
| W164-S3 | The issuer's defect, fixed. |
| W165-S1 | INERT: the read sits outside parseIrEnvelope. |
| W165-S2 | ARMED, disarm owner ~P2: the bun full suite rewrites contracts/wire/*.ts; restored, nothing staged. |
| W165-S3 | INERT. |

## Still open

- **Release 1** (irpt-ycharts-generate at 1b5afe6a49): ~Y2 deploys under the pair, with the three E-Y4 legs; Andrew's F1 retry
  follows.
- **The custody route** (IB-pr-351, 352, 355) releases under its own pair naming the route and every principal class.
- **The portal** IB-pr-356 waits on CTO review, then lands on DEV.
- **Push state:** LOCAL at the time of writing.
