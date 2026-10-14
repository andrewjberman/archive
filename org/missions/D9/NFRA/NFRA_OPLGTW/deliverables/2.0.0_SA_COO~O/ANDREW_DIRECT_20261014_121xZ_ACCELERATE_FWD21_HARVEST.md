# Andrew-direct 2026-10-14 ~12:1xZ at the 2.0.0_SA_COO~O terminal -- accelerate FWD-21 (asset manager on the gateway MCP)

**Context:** Andrew asked what is needed to set up the gateway MCP in a colleague's Claude app. The answer was:
- OG-hv-2 must land first (the harvest read grant and the release of `harvest_list` / `harvest_read`). It was fourth in
  the gateway queue, behind OG-ap-17, OG-mg-1 Phase B and MX-r-13.
- Then the connector at `https://mcp.opalinvest.dev/mcp` (reuse the org's, or an owner adds it).
- Then her work sign-in and one Microsoft sign-in.

**Verbatim:**
> "Ok this is good but we need to accelerate this use case and the associated task orders."

## Scope as read (verbatim scope; nothing wider)

"This use case" is FWD-21: an Opal asset manager reads harvest research through the gateway from her own Claude app.
"The associated task orders" are OG-hv-2 (the grant and the release), and the orders it waits behind in the gateway
queue.

## The issuer's acts on it (2.0.0_SA_COO~O, inside its own decomposition)

1. **OG-hv-2 moves to the FRONT of the gateway queue** (amendment A4). Phase A starts now: OG-ap-14's ledger is CLOSED,
   and OG-hv-1 drained @e4096a971f.
2. **OG-ap-17 follows OG-hv-2** (amendment A2). Its Phase A re-cuts on OG-hv-2's live release, because the A1 deploy-source
   guard requires the parent to equal the live deployed_commit. Phase A work cut on 90967e39ba now would be thrown away.
3. **MX-r-13 (NFRA_MCPINDEX, 2.0.0_SA_COO~MI) keeps its place after OG-ap-17.** It now waits one more release; ~MI is told.
4. **The three never-widen halves are told in advance:** 1.0.0_SA_CTO~Z, 3.0.0_SA_CVO~Z, and this seat. The ask lands at
   the end of Phase A.
5. **Andrew's side, parallel and on no one's gate:**
   - the connector can be added now;
   - the asset manager can connect and complete her Microsoft sign-in now, on today's tools.

   That clears authentication before the harvest tools land. Andrew's stand-in read follows the release, then her own
   driven call (AC3).

No criterion moves. No widening is decided here: OG-hv-2's three halves still sign at its `release_sha`.
