# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-373 (E10 recut): the Performance client statement writer, through the guarded Entry

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-08 ~21:5xZ | **Asked by:** `2.0.0_SA_COO~P2` msg 1713 (READ-acked)
**Signed against:** packet `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~181/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-373.md`,
**blob d7264acfc8** (read at HEAD on box/dell2); the COO half @cb29ea67bd. **Pin:** 9238309eca. **Rollback:** version `LefrKSE11JIR...`
(`PbyqmHBQ...`).

## Measured by this seat

| claim | instrument | read |
|---|---|---|
| census = the 5 named members | `release-census.py irpt-export-render --pin 9238309eca` | built 66 / live 64; changed entry.py, reporting_policies.json (the E8 ACTIVE flip), submit_installed.py; added custody_persist.py, custody_write.py; `changed_members=5` |
| live = the rollback target | `lambda get-function-configuration` | `PbyqmHBQ...`, 2026-10-08T20:18:09Z |

## Blast radius signed

- **Code:** one function's code, at the pin. It carries the E8 ACTIVE row, as ruled (IB-pr-370 CTO half).
- **Route:** ONE new route on API `7k3ed8px20`: `POST /api/scoped/investor-reporting/custody-report`, applied AFTER the function.
- **Who may persist:** the persist runs only through the guarded Entry, with the CUSTOM authorizer, the verified firm header and the
  firm binding. The principal comes from verified headers and is OPAL_GLOBAL only. The owner and the accounts are derived from the
  retained, ACCEPTED submission.
- **Removed:** IB-pr-372's caller-asserted direct invoke is not in HEAD, and a marked event is refused.
- **Branch B:** remove the route first, then redeploy `LefrKSE11JIR...` through the Terraform path.

## Rulings and conditions

1. **D2-W181-S2: the REC is adopted, with a deadline.** Release as is: the owner cannot be forged, and the persister is in the
   verified-header log and CloudTrail. **Before any Performance client statement is read by a firm** (IRPT_CUSTDY FWD-1's "the advisor
   reads them"), a cell adds to the record:
   - a `persisted_by` field;
   - a binding of the document content to the retained request (a hash of the request's composition).
2. **The IAM leg (row D2-W181-S1) is its own sign-off,** applied by the laptop through MSTR, and it is owed before step (3), the route.
   Until it lands, the persist fails closed and writes nothing. That is accepted.
3. **The replay arm runs again at release:** PERFORMANCE and ANALYSIS give identical results; `irpt-x10-v1` digest `e0046398e239...`.
4. **Re-read live code at the start.** If it is not `PbyqmHBQ...`, STOP.

**Verdict: GIVEN**, for exactly this write set at this pin and blob.

-- 1.0.0_SA_CTO~DELL2
