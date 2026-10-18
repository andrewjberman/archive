# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-42 (round-43 ninth batched release: probe firm pin + Graph host pin)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED on the ask's sections 1-8**, 2026-10-18 ~15:2xZ.

**Bound to:**
- ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-42.md`, sha256
  `cd24609722a88a85efc6968941571107b10f30610c99d883685734f263189822` (re-hashed at signing);
- release `a0c83303ee48c95c16a61c0d5e8bd186b1083b66` on live `922ee425fea4b2cbce2beb8ca7930f3a474d877a` (dell1 ck-3);
- the four dell1 harvest blobs read at 922ee425fe and again at the release: `harvest_research` 845a3416, `harvest_figures` 98bceb90,
  `harvest_identity` f5bc0b80, `harvest_keys` 25b44841.

## What I measured myself

- `git log -1 a0c83303ee`: its parent is `922ee425fe`, the live ref.
- `git diff --stat 922ee425fe a0c83303ee`: 4 files, +253/-10 (`graph.py`, `probe_listener.py`, two tests). No harvest file and no
  `server.py`, `tools.py` or unit change.
- The four harvest blobs at the release are equal to those at the live ref.
- **The `graph.py` diff:**
  - An absolute URL is accepted only as `https`, on host `graph.microsoft.com`, with port absent or 443 and no user-info. It is
    checked in the sink before any client is built.
  - A relative path is prefixed with GRAPH_BASE, so it cannot leave the host.
  - `call` never talks to the login host, so none is allow-listed. That is correct, and narrower than my analysis allowed.
- **The `probe_listener.py` diff:** the lease carries `firm`, matched in full against `^[a-z0-9][a-z0-9_-]{1,63}$`. A lease without a
  valid firm is malformed, which means unarmed. `client_get_transactions` is refused 403 `probe_firm_refused` unless the call's firm
  equals the lease's, before the tool runs. Together with the existing account check, this is the firm-AND-account pin I ruled
  (msg 35695). `etfs_compare_peers` reads public peer tables and carries no firm.

## Accepted

- **Nothing widens.** The listener refuses more, and the Graph client accepts less.
- There is no arming and no SSM write in this order. The served read at Phase B is UNARMED ONLY.
- **The ask's limits are stated honestly:**
  - the pins are measured in a guarded scratch process on a test port;
  - the firm pin is not exercised in the service until OG-ev-7 arms a lease with a firm;
  - the Graph allowed branch is proven by a stub and the 21-site audit, not by a live Graph call.
- **Rollback is the 922ee425fe tree.**

## Conditions of this half

- **CT1 (base):** a live marker other than 922ee425fe at Phase B is a STOP and a re-cut.
- **CT2 (dell1's files):** Phase B prints the host md5 of the four harvest files beside the release's. Any mismatch is a rollback.
- **CT3 (at rest):** no lease parameter exists, and none is written, through the ledger close. The read-back shows `probe_not_armed`
  on the listener. A 200 from `/probe/` is a rollback trigger, as before.
- **CT4 (Graph, served):** the 30-minute read-back counts the Graph-backed tool calls that succeed or fail, and the
  `GraphHostRefused` errors. Any `GraphHostRefused` on an organic call is a row before the ledger closes, because a legitimate
  nextLink must never be refused.
