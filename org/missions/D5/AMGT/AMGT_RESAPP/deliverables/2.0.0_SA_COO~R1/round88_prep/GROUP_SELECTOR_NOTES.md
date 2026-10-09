# AMGT_RESAPP round-88 PREP -- row D1-S18, the scoped watchlist route and `selected_tenant` (`2.0.0_SA_COO~R1`, 2026-10-09 ~20:1xZ)

**The row:** GET `/api/scoped/amgt/watchlist` ignores `selected_tenant`; an off-list selector gets 200 with the caller's own list where
other routes refuse it (dell2 `2.0.0_SA_COO~V2` msg 3757, TCKT_VNEXT SA-r-1b run 2 @e2c7f7b25a).

## Measured at HEAD

- `selected_tenant`: 0 occurrences under `lib/research/api/` and 0 under `lib/` (Grep, both scopes). The refusing routes the report
  compares against live outside this function.
- `lib/research/api/scoped_amgt.py:6417-6429` `_firm_id`: the firm is read ONLY from the `x-firm-id` header that `auth-validator-edge`
  injects after verifying the JWT; absent -> 401 (fail closed). Its docstring: "The firm is never read from the path or the body. A client
  cannot name a firm here, so there is no code path on which one firm's request reaches another firm's partition."
- So the 200 is BY DESIGN: the route has no client-selectable tenant at all, and an off-list selector cannot widen what it serves. Not a
  leak (the reporter agrees).

## The call for the round-88 analysis (two branches)

- **A. Dismiss D1-S18** with that reason: the route's tenancy is edge-injected only; a selector parameter is not part of its contract.
- **B. Consistency cell (small, LOCAL + a redeploy):** `scoped_amgt` refuses a request whose `selected_tenant` (query or header, as the
  other routes read it) is present and differs from the edge-injected firm, 403 with a reason; absent selector unchanged. Needs the
  other routes' exact selector contract read first (outside this function -- not yet located) so the refusal matches theirs.

Issuer's recommendation: **A**, unless the portal sends `selected_tenant` to this route and expects the refusal (then B, after reading the
other routes' contract).
