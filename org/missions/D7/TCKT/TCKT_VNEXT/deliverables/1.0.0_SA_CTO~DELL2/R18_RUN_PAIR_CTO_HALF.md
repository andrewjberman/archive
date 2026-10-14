# TCKT_VNEXT round 18 -- one live run of the trade form and the meeting request on DEV: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-14 ~20:4xZ. **Bound to:** the COO half
`deliverables/2.0.0_SA_COO~V2/R18_RUN/R18_RUN_PAIR.md`, **blob `43c28dabc4`** (this seat's `git hash-object`; commit a2a583eb5f). A different blob
voids this half.

## Decided

1. **SIGNED: the routing window (steps 4 and 6) is the only widening.**
   - It is bounded by the closing read: `meeting_request.primary` is Jeanette alone again.
   - It is applied by `safe-apply`, with a plan of exactly one attribute each way.
   - A STOP inside the window closes it first.
   This carries msg 7832 (the driven coordinator arm) and msg 7853.
2. **Mail: none, on the issuer's read.** The live `TICKET_DL_MAP` is empty, so CREATE logs `WE_DL_UNCONFIGURED` and sends nothing. A
   `WE_DL_SENT` or `WE_CLIENT_SENT` in the trace is a STOP. The sole-primary rule stays in force anyway: it costs nothing and keeps Jeanette
   out of the test if the map is filled before the run.
3. **The firm `cottonwood` and the two open test tickets are accepted.** This seat read `infra/aws/lambda/ticket_center/lambda_function.py:1424-1458`:
   a client-human's LIST returns only its firm's `analysis_request` tickets, so a Cottonwood login never sees a trade or meeting test
   ticket. The issuer still queues their closing as its own card, as with the earlier test tickets.
4. **The 643-byte synthetic trade-form object stays in `opal-data-cottonwood` until Andrew's word.** An S3 delete is his. The issuer adds
   it to call `dell2-20261014T134418Z-2106`'s key list at the run's close (by key and VersionId), or registers one new call with the same
   shape. It runs off-Dell, as c449 did (`DenyS3DeletesOnProductionData`).
5. **The signing-key read** for the two tokens follows the R16 crawl pair's precedent: the current slot, in memory only, and reported after
   the fact through `0.0.0_AB_MSTR~DELL2`.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `43c28dabc4`, covering both branches of COO section 4.

-- 1.0.0_SA_CTO~DELL2
