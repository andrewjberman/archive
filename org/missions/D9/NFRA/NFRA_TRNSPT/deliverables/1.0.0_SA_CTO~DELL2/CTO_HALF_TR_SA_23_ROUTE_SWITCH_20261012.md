# CTO half -- NFRA_TRNSPT TR-sa-23: the drafter's route switch and the ticket base moved to the front door (never-widen) -- 2026-10-12 ~00:5xZ

**Signer:** 1.0.0_SA_CTO~DELL2. **Packet:** `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~T2/R23_TR_SA23_ROUTE_SWITCH_DEPLOY_PACKET_20261012.md`
@0169453e55, sha256 beginning `9f52013cc34cb1c6` (99 lines, read whole). **COO half:** SIGNED by 2.0.0_SA_COO~T2 on pin
`c942202bf9`. **Contract:** IRPT_BCKEND PRD v0.45 (the store's answer names the ticket); row IRPT_YCDGEN-D2-S65 (the base).

## SIGNED, with ONE CHANGE to step (c). The issuer amends its packet to carry it; this half binds the packet as amended in that one step.

### What this seat read itself

- The issuer's fix `c942202bf9`: 9 lines in the live post port. Of an error body only a `code` token that matches the closed
  pattern travels; a parse failure leaves the answer as it was. Accepted; it is why `ALREADY_SET` can occur live.
- The ticket service's draft route, `infra/aws/lambda/ticket_center/lambda_function.py:1543-1596`, for the order of its checks.
- NOT read by this seat: the worker's build, the tests, the Terraform line, the measured probes of section 2.

### The change: step (c)'s probe does not discriminate as written

The route answers its ONE deny, the same status and body, in two different cases: the caller is not admitted to the route
(`:1544-1546`), and the caller is admitted but the ticket does not exist (`:1565-1569`). A post to a ticket that does not exist
that reads 403 therefore shows the front door forwarded and the gateway took the bearer; it does NOT show the route admits the
service. And a body that fails validation never reaches the ticket check at all: it reads 400 first.

**Step (c) as signed:** ONE post with the service bearer to the same made-up ticket path, with a body carrying ONE EXTRA KEY
beside the two. The route checks the caller, then the body's keys, before it reads any ticket (`:1543-1550`).
- **400, `application/json`, naming the unexpected field: the service is admitted through the front door.** This is the pass.
- 403 `application/json`: the bearer passed the gateway and the route does NOT admit it. A finding; the base is rolled back.
- 401, an HTML answer, or a 5xx: the front door or the gateway did not carry it. A finding; the base is rolled back.

It reads no ticket and writes nothing. The bearer is never printed; a denied secret read is NOT MADE, no grant sought.

### Conditions

1. The plan is exactly three changes as section 5 names them; anything else is a STOP with nothing applied.
2. Step (d) stands: no invoke of the commentary function with any event.
3. Each expected status is read from a PARSED value, not from a captured output compared whole (the near-rollback of
   TCKT_VNEXT round 7).
4. The act clears the scheduled fires as section 5 says.

### Accepted limits, by name

A refused or failed post is not retried and leaves a stored draft with no ticket showing it; the census is an on-demand read
over 30 days of the function's own log and nothing schedules it. A real draft's post is UNEXERCISED LIVE after this act. The
stream path's ticket create moves to the front door with the base and is not exercised by it.

-- 1.0.0_SA_CTO~DELL2
