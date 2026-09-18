# NFRA_OPLGTW.TO-OG-x-1 -- the authenticated, filtered CSV download -- result

**Worker:** `0.9.0_WK_NFRA_OPLGTW~5` | **Cut base:** CLOUD @96ed92aa4d | **Cell:** OG-x-1

## What this cell built

- `infra/aws/ec2/opal-gateway/app/integrations/schwab/export.py` (new) -- ticket mint/validate/consume
  (real DynamoDB conditional writes via `app/access_state.py`, exercised against moto in the tests, never
  a hand-rolled stand-in), the CSV formula-escaping writer, and `generate_csv()` orchestrating
  `SchwabService.export_query`.
- `infra/aws/ec2/opal-gateway/app/download_routes.py` (new) -- `GET /schwab/download` (the static page,
  unconditionally served so the page's own script can decide whether a sign-in is needed -- a server-side
  redirect at GET time would drop the ticket, which lives only in the URL fragment) and
  `POST /schwab/download/exchange` (Origin+CSRF checked; `pending` peeks without a session and retains
  only the ticket's own hash; unauthenticated `start:false` peeks metadata without consuming;
  `start:true` atomically consumes, generates+validates the CSV, reauthorizes, then streams it).
- `infra/aws/ec2/opal-gateway/app/static/schwab_download/index.html` (new) -- the one static page + its
  one inline script, hashed into a `script-src 'sha256-...'` CSP computed fresh from the shipped file.
- `infra/aws/ec2/opal-gateway/app/integrations/schwab/integration.py` -- fills the `ticket_issuer` call
  site OG-q-2 left; adds `default_service()` (the one process-wide `SchwabService` the MCP tools and the
  download routes now share) and `SchwabService.export_query` (full grant/scope/catalog/engine parity
  with `schwab_query`, unbounded within the contract's `export_rows`).
- `infra/aws/ec2/opal-gateway/app/server.py` -- two new routes, `/schwab/download` (GET) and
  `/schwab/download/exchange` (POST), as LITERAL string paths (see "route-path form" below).
- `infra/aws/ec2/opal-gateway/tests/test_principal_cutover.py` -- ENTRIES ONLY (ruling 97203 C): two new
  `ROUTE_CLASS` lines, both `"public"`.
- `infra/aws/ec2/opal-gateway/tests/test_schwab_export.py` (new) -- one test per criterion OGX1-AC1..AC27.
- `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~5/DOWNLOAD_PATHS.json` and
  `probes/og_x1.py` (AC29's diff-discriminator probe).

## Route classification (ROUTE_CLASS)

Both new paths are classed `"public"`, the SAME class and the SAME reasoning ruling 97203 A already gave
OG-a-3's `/schwab/download/login` and `/schwab/download/callback`: neither route consults the Gateway's
own Authorization-bearer scheme or the ALB access-layer header at all (their answer is invariant to both),
which is exactly the axis `test_principal_cutover.py`'s public-route arm and
`test_data_entitlement_guard.py`'s else-branch grade. The REAL guard -- OG-a-3's session cookie plus this
cell's own ticket identity/grant/single-use checks -- is independent of that axis and is exercised by
OGX1-AC1..AC16, never by ROUTE_CLASS. Recorded rather than defaulted: the standing rule warns against a
lazy `"public"`, and this entry is reasoned, not assumed.

## Route-path form (a surprise fix, not a design choice)

The route declarations use LITERAL string paths (`Route("/schwab/download", ...)`), not a
`download_routes.export.DOWNLOAD_PAGE_PATH`-style reference. `tests/test_browser_oidc.py`'s AST route-
table reader (`_declared_routes`, outside this cell's `<paths>` grant) resolves ONLY a one-level
`oauth_as.X` / `browser_oidc.X` attribute form or a literal constant; a two-level attribute chain
(`module.submodule.CONSTANT`) is unparseable to it (`AttributeError: 'Attribute' object has no attribute
'id'`), which broke `test_oga3_ac07` on first use. Filed as a surprise row and fixed by using literal
strings, which the SAME reader accepts as `ast.Constant`. Re-verified green after the fix.

## Verification

- `tests/test_schwab_export.py`: 27 of 27 individually (`rc=0`, `1 passed` each) and twice as a whole
  file (`27 passed`, ~9.7-9.9s both times).
- `tests/test_principal_cutover.py` (AC28, `-m "not live"`): `11 passed`.
- `probes/og_x1.py AC29`: `VERDICT: PASS-OGX1-AC29` (diff against cut base 96ed92aa4d is exactly the two
  `ROUTE_CLASS` lines DOWNLOAD_PATHS.json names).
- No-regression spot check on every sibling file that reads `app/server.py`'s route table or imports
  `ROUTE_CLASS`: `tests/test_browser_oidc.py` (7/7) and `tests/test_data_entitlement_guard.py` (12/12),
  both green.
- Mutant control: `export.validate()`'s principal-match check short-circuited, OGX1-AC11 fails as
  expected (`200` instead of `403`), file restored and sha256-verified byte-identical, OGX1-AC11 green
  again.
- `.tools/commit-gate.sh` clean on every `.py` file this order touches.

## Design notes worth citing against the PRD text directly

- **Ticket transport (C5):** the URL fragment only; the stored record is keyed by the SHA-256 of a fresh
  32-byte random secret, never the deterministic `ticket_key` `integration.py`'s `prepare_download`
  computes for cache/audit correlation -- a deterministic key would let two identical requests collide and
  would not meet "random opaque ticket."
- **Metadata without a second redemption (contract `download_metadata`):** the exchange's `start:false`
  (or absent) action reads the ticket and returns its already-non-secret scope (master/dataset/date/
  columns) WITHOUT consuming it; only `start:true` atomically consumes. Both actions share one endpoint
  and one ticket.
- **Pending ticket (C5):** `pending:true` (no session) retains ONLY the ticket's own hash (already its
  storage key -- nothing new is written) in a cookie scoped to `/schwab/download`, and returns the OG-a-3
  login URL with `return_to`. Hashing is one-way by construction, so this is declared a defensive/anti-
  fixation artifact, not an auto-resume mechanism -- see `declared_exclusions` in the proof instance.
- **Reauthorize-then-stream (C5):** `export.reauthorize()` is a SECOND, independent grant-revision read,
  called after the CSV is fully generated and byte-validated and immediately before the response is built
  -- ordering asserted directly in OGX1-AC19 by spying on the call sequence.
- **Never truncate (C5):** `SchwabService.export_query` requests `export_rows + 1` rows so it can tell "at
  the cap" from "over the cap" without ever materializing more than one row past the limit, and refuses
  (never trims) when the true `matched_rows` exceeds the cap; `write_csv` separately refuses (and removes
  the file) over `EXPORT_UTF8_BYTES`.
