# L8 drain end -- IRPT_BCKEND rounds 106 and 108, workstream ~P (adds to the round 104 packet @9bdc151f84)

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-09 ~12:1xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD |
**Judgment criteria:** 0 | **round-close:** rounds 106 and 108 are both MAY-CLOSE (`round-close-check.py`, orders=1, judgment=0)

## Round 106 (@fdf1c51c1e): 1 of 1 COMPLETE

- **IB-pr-405**, worker `0.9.0_WK_IRPT_BCKEND~268`, drained @6f51e09a79. It was ordered by CTO msg 3088 (IRPT_DASHBD ADDENDUM 9.2 (2)).
  - `analysis-request-read` gains opt-in `include=persist_inputs` with four members: `artifact_id`, `composition_sha256`,
    `retention_policy` and `report_index`. It is re-authorized per request.
  - `svc-custody-statement` gains only that operation, cottonwood-bound.
- **Issuer re-grade: 3 of 3 PASS.**
  - IB106-1-AC1: 20 `persist_inputs` tests.
  - IB106-1-AC2: ops 288 passed and `_authz` 315 passed.
  - IB106-1-AC3: census of 8 artifacts, 26 replay arms, packet.
- The code was reviewed: the `include` set gained one name, and `SVC_CUSTODY_STATEMENT_OPERATIONS` gained one operation.
- **Not released.** Row W268-S2 is disarmed by D2-S45. CTO ADDENDUM 17 (msg 3220) ruled (a), sequenced: irpt-status is built narrow on
  IRPT_ANLREQ release 1's live bytes, AFTER release 1 lands, with each re-pin owned. That release is event-gated on ~Y2.

## Round 108 (@eda099ad29): 1 of 1 COMPLETE

- **IB-pr-407**, worker `0.9.0_WK_IRPT_BCKEND~270`, drained @9c00d0155c. It publishes `include=persist_inputs`:
  - the `routes.json` query text;
  - the `persist_inputs` definition in `OwnedAnalysisRequest.schema.json`, `$ref`'d from the read's response schema;
  - 5 contract tests.
- **Issuer re-grade: 3 of 3 PASS.** The unguarded census passes, and IB-pr-407's own contract tests pass.
- **Row D2-S46:** 9 `_contracts` tests already fail at HEAD from other cells' in-flight work. They are untouched and identical before and
  after this cell.
- **Row D2-S47** resolves D2-S43, since the census passes at HEAD.

## Carried (other rounds, still open)

- **Round 102:** IB-pr-397 is on `~IB2` after 401, under AMENDMENT 3 (duplicate log group dropped, retention 14).
- **Round 103:** IB-pr-401 is applying on `~IB2`. It runs ahead of 397 (CTO 399 half AMENDMENT 1) and is at the enforcer-scope arm.
- **Round 105:** IB-pr-404 has its three keys LANDED and the replay on the uploaded bytes reads 18/18. The after-read is at the 14:15Z fire.
- **Round 107:** IB-pr-406 (49F e56 + CUSIP narrow bundle) is with worker ~269.

**Push state:** LOCAL on box/dell2 (MSTR box-sync pushes).
