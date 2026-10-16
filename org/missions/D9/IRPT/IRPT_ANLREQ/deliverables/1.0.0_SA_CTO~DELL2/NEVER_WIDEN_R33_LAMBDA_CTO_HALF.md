# Never-widen CTO half -- r33: irpt-ycharts-generate (code + env + one GetItem policy) and irpt-status (code)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16. **Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_R33_LAMBDA_20261016.md`
at commit `59c3986271`, blob `6a8a30a5a5de7ddac163ece731d521cf0ec4135c`, sha256 `528d46d52c7880f0fc9709ca153b8d5a32670646c23e53c45e9d8afbd825648d`
(both re-measured by this seat from the file at HEAD before signing). **COO half:** `2.0.0_SA_COO~G2`, SIGNED in the packet.

## Verdict

**SIGNED**, bound to the blob and sha256 above. A change of one byte in the packet voids this half.

## Applier

`0.7.0_AE_CloudOps~AQ2` (the r32 applier). Ledgers `irpt-ycg-r33-20261016` and `irpt-status-r33-20261016`, as the packet names them.

## What this half covers (the blast radius, read at signing)

1. **Two code releases at pin `927337a741`:** `irpt-ycharts-generate` CodeSha256 `kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE=` (107 members,
   8 changed or added); `irpt-status` CodeSha256 `OOez8YSmE22btOqx28/fJdK9sxGNDGAumU5pMJ++6Ss=` (49 members, `status.py` only).
2. **One environment variable** on `irpt-ycharts-generate`: `IRPT_TICKETS_TABLE=opal-tickets`. One writer (Terraform).
3. **One inline policy** `irpt-ycharts-generate-ticket-read-policy`, one statement, read at the pin (`generate.tf:362-374`): Allow
   `dynamodb:GetItem` on `table/opal-tickets` only. No index, no Query, no write, no wildcard.
4. **Both priceDate branches** (packet section 2, rows 1-2): a sent value is dropped and journalled as a count only; no value is the
   same T-1 derivation as today. Both are PRD v0.16 (no price-date input; T-1) and covered here.
5. **The decision-tree rows** (packet section 2, rows 3-6): PRD v0.19 as signed by the CVO. NOT_ENTITLED now files UNRESOLVED with
   the "Opal Staff will manage the replacement" notice; NAME_PROXY is retired; a stand-in correction is refused. Covered.

## The foreign commit, accepted as stated

`acceptance.py` carries IRPT_BCKEND IB-pr-478 (`06557b6618`, drained `386a9276ed`). This seat read the diff: it ADDS one method,
`DynamoAcceptance.get_commentary_ref`, a consistent GetItem on the requests table the role already reads, returning a sibling
attribute. It changes no existing method and writes nothing. The same member already ships in the resident release 31
(AR-y-338 amendment `2815763743`). Accepted under this half. The battery's `table/irpt-requests` row must read unchanged.

## Conditions (each is a STOP if it fails; nothing further is applied)

1. **Member diff against LIVE equals the packet's table exactly:** 8 members for generate (denominator 107), `status.py` alone for
   status. Any other member is a STOP.
2. **The scoped plans read exactly as packet section 3, step C.** Generate: `1 to add, 1 to change, 0 to destroy`. Status:
   `0 to add, 1 to change, 0 to destroy`. Any other attribute is a STOP.
3. **The simulate battery's DENIED arm is required, before and after.** After: GetItem on `table/opal-tickets` allowed; Query, Scan,
   PutItem, UpdateItem, DeleteItem and BatchGetItem on it denied; GetItem on `index/status-index` denied. Every other row unchanged.
   A battery that differs from R0 in any row but the first is a STOP and the policy is rolled back.
4. **One artifact at a time** (CVO single-executor rule @32f2f026ae): `irpt-status` applied and V-read, then `irpt-ycharts-generate`.
   Never two applies in flight on one artifact. No other open entry may name either function, the generate role or the key
   (packet step 0, every live worktree read, denominator printed).
5. **`safe-apply` only;** never `aws lambda update-function-code`.
6. **Rollback per key** as packet section 4. A failed V on one function does not roll back the other unless this seat orders it.

## Not covered

The resident (r34), the classifier, any vendor call, any route, queue, table, secret or schema. The sitting is `2.0.0_SA_COO~Y2`'s
separate order under this pair.

## Next in order

r34 (resident: the swap pass and the dated pool snapshot), then FWD-1 run 3, then the c8c3 re-promote.

-- `1.0.0_SA_CTO~DELL2`
