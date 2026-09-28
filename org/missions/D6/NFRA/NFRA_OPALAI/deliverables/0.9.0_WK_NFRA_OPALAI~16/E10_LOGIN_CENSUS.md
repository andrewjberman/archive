# E10 -- census of the legacy `/login` GUI consent (OA-e-10, worker 0.9.0_WK_NFRA_OPALAI~16)

LOGIN_USES: 0
WINDOW: 2026-07-14..2026-09-28
SOURCE: `sudo journalctl -u opal-gateway --no-pager -o cat | grep -cE '"[A-Z]+ /login([? ]|HTTP)'` over SSM on i-07dccb1615503ac99 (AWS-RunShellScript, run 2026-09-28 ~21:50Z), and the same count over `_COMM=uvicorn` (every unit, both service names)
DEPENDENTS: 1
BRANCH: NARROW

No email, token, bearer or cache content appears in this file. The host's `.env` was read only to derive the cache FILE NAME of each server-held identity (sha256 of the lower-cased value, as `token_broker._cache_path` does) and to test that the file exists.

## LOGIN_USES and WINDOW, measured

- The journal ACTUALLY covers 2026-07-14T09:48:50Z (first uvicorn line, boot -2) to 2026-09-28T21:51Z (measured; the whole
  journal is 838.1M, 3 boots: 07-14..08-21, 08-21..09-18, 09-18..now).
- Two unit names sit in that span: `m365-mcp-gateway.service` (320,575 uvicorn lines, 07-14..~08-15) and
  `opal-gateway.service` (551,417 lines, from 2026-08-15T03:02:10Z, the rename). The face's command
  (`-u opal-gateway`) reads only the second: **0** `/login` requests. The all-unit `_COMM=uvicorn` read over the full span
  also reads **0**.
- A substring-only count for `/login` in the `opal-gateway` unit returns 7, every one `GET /schwab/download/login` answered
  404: a different route (`browser_oidc.LOGIN_PATH`), not this cell. Both counts are reported so the 0 is not a
  pattern artefact. `app/browser_oidc.py` is NOT on the `/login` path and was not edited.
- Go-live of the MCP `/authorize` sign-in: registered in git at `63e61ca77b` (2026-06-23, "gateway OAuth-AS facade
  (Model-B) ... authored, UNAPPLIED"); the durable rewrite that gave it its current constant is `51b0f7d823` (2026-09-15).
  The first `GET /authorize` in the journal is 2026-07-15, the latest 2026-09-25 (an access-log read, unfiltered by status).
- **The journal does NOT reach back to the go-live commit**: it starts 2026-07-14, 21 days after `63e61ca77b`. LOGIN_USES = 0
  is therefore a count over 2026-07-14..2026-09-28 (76 days), not since the commit. The 21 days before the journal are
  unmeasured. Those dates are not recoverable from this host.
- For comparison in the same journal: 14 `GET /callback` lines (bridge and legacy are not distinguishable in an access
  line).

## DEPENDENTS -- server-held identities that read the email-keyed cache `/login` writes

The email-keyed cache (`token_broker._email_owner(email)` -> `<sha256(email)>.bin`) is written in exactly one place:
`token_broker.redeem_consent` (`token_broker.py:360`), reached only from the legacy branch of `callback()` on a state minted by
`/login`. The bridge (`redeem_code_for_principal`, `token_broker.py:331`) writes only `principal:<tid>/<oid>`. `get_token(email)` on a
request that carries no principal (or a principal whose email differs) reads the email-keyed file
(`_cache_owner_for`, `token_broker.py:159`); `_save_cache` only re-writes the same owner after a silent refresh.

Callers of `get_token(<email>)`:

| caller | identity | reads |
|---|---|---|
| `otp.py:122,153` (`/otp/fetch`, `/otp/health`, `server.py:~690-730`) | `OTP_MAILBOX` | email-keyed cache |
| `ms_ingest.py:114,207` (`/ms/sites`, `/ms/site_children`, `/ms/onedrive_children`, `/ms/search`, `/ms/health`; `server.py:~760-830`) | `MS_INGEST_IDENTITY` | email-keyed cache |
| `server.py:628` (`/teams/poll`), `tools.py:106`, `taxsma_workbook.py:313`, `opal_portal/integration.py:219` | the request's own principal | principal-keyed cache (the request calls `set_current_principal` first) -- NOT dependents |

`/otp/*` and `/ms/*` are capability-bearer routes: they call `set_current_principal` nowhere, so their `get_token` always
resolves to the email-keyed file.

DEPENDENTS = **1 distinct server-held identity, on 2 routes**:

1. The identity configured as `OTP_MAILBOX` and as `MS_INGEST_IDENTITY` (the same value in both, measured on the host:
   both hash to cache file `7b1bca22c953247e...bin`, which exists, size 13,132 bytes, last written 2026-09-28 20:32Z by a
   silent refresh). Routes: `/otp/fetch` + `/otp/health` (the bd-auto-login box's OTP, and the EventBridge liveness
   probe) and `/ms/*` (the nightly globgrph derive, its liveness probe). Why a dependent: **the cache can be (re)minted
   ONLY through `/login` + the legacy `/callback`.** No other path writes an email-keyed file: the bridge sign-in writes the
   principal's cache, which an `/otp` or `/ms` request never reads (no principal in context); no bootstrap script or ops
   tool in `infra/aws/ec2/opal-gateway` writes a cache. Today the file is live (refreshing), so nothing needs `/login`
   right now, but a lapsed refresh token (the "SPOF" the `/otp/health` and `/ms/health` probes exist to catch) has
   `/login` as its only recovery.

Count rule: the DEPENDENTS number counts distinct identities (cache files), so the OTP and MS routes are ONE identity.
Host cache directory: 6 files in total; only `7b1bca22...` corresponds to a configured server-held identity (file names
and mtimes only; the other 5 are not attributable from names and are not counted).

## BRANCH: NARROW -- what was built

DEPENDENTS is 1, so the route is NARROWED, not removed: `/login` admits only the identities in
`{OTP_MAILBOX, MS_INGEST_IDENTITY}` (existing settings, lower-cased and stripped; no new config key), fails closed when both
are empty, and answers any other caller 403 before `make_state` or `build_consent_url` runs
(`server.py:450-470`). The `:199` access-layer arm, the OG-e-2 email-deny guard, the legacy `callback()` branch and all
`/sprint*` handling are unchanged. Nothing is deployed.
