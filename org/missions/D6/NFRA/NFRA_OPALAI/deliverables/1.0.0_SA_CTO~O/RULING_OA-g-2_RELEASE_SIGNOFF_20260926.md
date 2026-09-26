# OA-g-2 -- never-widen sign-off, CTO half (1.0.0_SA_CTO~O, 2026-09-26 ~14:0xZ)

**Act:** the opal-gateway narrow release in `NFRA_OPALAI.TO-OA-g-2.portal-grant-release`, announced in
`deliverables/0.9.0_WK_NFRA_OPALAI~9/ANNOUNCE_OA-g-2.md` (drained @3f0798fdd0). Deployer `0.9.0_WK_NFRA_OPALAI~9`,
issuer `2.0.0_SA_COO~O`, one deployer at a time (@75117e60d6).
**Authority for this half:** Andrew's self-drive arming term, "Served output still moves only under a never-widen
sign-off (CTO half + a second, non-acting half)" (record `ANDREW_DIRECT_20260926_03xxZ_SELF_DRIVE_O_FABRIC.md`).
**Second half owed:** a non-acting seat, `3.0.0_SA_CVO~O`. The issuer and the deployer are acting seats.

## Blast radius (read from the release diff, `git diff c5f8099440 df724ef284 -- infra/aws/ec2/opal-gateway`)
- Base: c5f8099440, resolved by content (3 of 3 named files, SSM command a3708411). Release commit df724ef284.
- 5 files, 411 insertions / 18 deletions; 290 of the insertions are `tests/test_portal_grant.py`. Served code:
  `app/data_entitlement.py`, `app/asker_scope.py`, `app/admin_grants.py`, `ops/schwab_entitlement_admin.py`.
- **What may change:** a data_entitlement record MAY now carry `portal_channels`. With it (and an empty Schwab half)
  the grant is PORTAL-ONLY: it admits no Schwab tool (`portal_only` returns `frozenset()`), and `opal_asker_query`
  serves a catalog key only if the key's own `_channel` is granted, after the calling identity's catalog_gate verdict.
  Never wider than either side.
- **What may NOT change:** every record WITHOUT `portal_channels` parses exactly as v1.1. That is the code's own rule at
  the parse (`set(raw) in (SCOPE_DIMENSIONS, SCOPE_DIMENSIONS | {portal_channels})`; the Schwab half keeps its
  non-empty checks), at the asker path (the channel check runs only `if access.grant.scope.portal_channels`), and at
  the read-back (the key is added only when non-empty). The tool list is untouched; the 46 = 46 guard must hold.
  `identity_scope` is not in the diff.

## Both branches, read from the producer's rule
- **Today's table (no record carries `portal_channels`):** every existing grant takes the unchanged v1.1 path, so
  **DELTA = 0** on every served answer at GO. The release adds a capability and moves no one.
- **After a portal-only record is written:** only that person's asker answers change, narrowed to the granted
  channels. That write is OA-g-3 (Alyssa Keith, portal figures), Andrew's call 2
  (`ANDREW_DIRECT_20260926_022xZ_CTO_O_OPEN_CALLS_1_TO_6_ANSWERED.md`). It is a separate act with its own order.
  This half does not sign it.

## Writers of the named property (NEVER-1: count them), added 2026-09-26 ~18:4xZ
**N = 1.** The only site that puts `portal_channels` into a STORED record is the operator admin command,
`ops/schwab_entitlement_admin.py:274-275` (it writes the field only when the scope carries it). That command
refuses the field unless the contract declares `portal_grant`, and refuses channels the catalog does not hold
(`:192-199`). `app/admin_grants.py:105-107` builds the `get_grant` read-back response, so it is not a writer.
Every other hit in `infra/aws/ec2/opal-gateway` is parse, enforcement or tests. Counted by `3.0.0_SA_CVO~Z`
(file msg 20260926T183500Z, 53 hits); the two cited ranges were re-read here at HEAD.
**So "no record carries `portal_channels` today" is a bounded property, not a moment:** it can change only when
someone deliberately runs that command, which is OA-g-3's act, not this one.

## Rollback, per key
- Code: redeploy the base artifact `opal-gateway-c5f8099440.tar.gz` through the same release script (the 90-second
  health rollback does this on its own if /health fails). The manifest record reverts with it.
- Data: none written by this act.

## Guards required at GO
The release script's .env render check; the 90-second health rollback; the MCP tool list unchanged (46 = 46); the
NEVER-2 ledger `nfra-opalai-portal-grant-gateway` opened before the upload and closed after. The BLOCKING row
Z-W9-S3 (5 files vs the face's 4) is dispositioned by the issuer before GO. The fifth file, `app/admin_grants.py`,
is read above and moves only the read-back of a grant that carries `portal_channels`.

**CTO half: SIGNED**, for the act above as bounded here, by `1.0.0_SA_CTO~O`.
