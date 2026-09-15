# NFRA_OPLGTW.TO-OG-a-3: the download browser's own OIDC login

**Worker:** `0.9.0_WK_NFRA_OPLGTW~3` | **Branch:** `wk-nfra_oplgtw-1-3d` (worktree `/c/tmp/wk-oplgtw-1-3d`, cut from
`CLOUD` at `7459929520`, after OG-a-2 merged) | **Commits (LOCAL):**
- `6a4e94d734`: the code, the test module and `BROWSER_PATHS.json`;
- `b2648343dc`: rows W3-S16 .. W3-S21;
- the commit that carries this file, the proof instance and the `<status>` flip.

Nothing was pushed, merged or deployed.

## Read this first: 7 of 7 criteria pass by output

Each criterion's invocation was run verbatim at `6a4e94d734` and read `1 passed`, rc=0. One effect lands outside the
grant: OG-a-2's `test_oga2_ac04` now fails on the two new routes (row W3-S16, ARMED, disarm `2.0.0_SA_COO~O`).

## What was built

| path | what |
|---|---|
| `infra/aws/ec2/opal-gateway/app/browser_oidc.py` (new) | the login, the callback, the cookies, `read_session` / `session_principal` |
| `infra/aws/ec2/opal-gateway/app/server.py` | the import, the 2 `Route` declarations after `/callback`, and 1 auth-model docstring entry |
| `infra/aws/ec2/opal-gateway/tests/test_browser_oidc.py` (new) | `test_oga3_ac01` .. `test_oga3_ac07` |
| `deliverables/0.9.0_WK_NFRA_OPLGTW~3/BROWSER_PATHS.json` | the two exact paths and their methods, for OG-i-3 |

- **Paths:** `GET /schwab/download/login` and `GET /schwab/download/callback` (Starlette also serves HEAD for each).
- **Login:** mints a random state and nonce and seals them, with a return path under `/schwab/download`, in a
  transaction cookie (600 s). It then redirects to the upstream for OpenID scopes only, with the new callback as the
  redirect URI.
- **Callback:** refuses unless the state equals the transaction cookie's, and does so before any code exchange. It
  redeems the code for its own redirect URI and validates the ID token with OG-a-2's
  `token_broker.verify_upstream_id_token` (the principal function reused, not a second one). That checks the
  authorized tenant, the RS256 signature against the tenant's published key, the exact issuer, the audience (client
  id), expiry and this sign-in's nonce. The callback then applies the kill switch and blocklist, and sets the session
  (900 s).
- **Cookies:** `__Secure-` names, Secure, HttpOnly, SameSite=Lax, host-only, `Path=/schwab/download`. They are
  Fernet tokens under a key derived from `FERNET_KEY` for this use only, so a browser cookie can never be read as the
  MCP bridge state or the legacy consent state. SameSite is Lax, not Strict, because the callback is a top-level
  navigation back from the upstream's origin, and a Strict cookie is withheld from it.
- **For OG-x-1:** `session_principal(request)` returns the principal (tid, oid; email for display). It re-checks the
  authorized tenants and principal revocation on every read.
- **Not used:** `identity.py`'s ALB helper and any identity header.

## Criteria (each invocation verbatim at `6a4e94d734`)

| id | verdict | deciding line |
|---|---|---|
| OGA3-AC1 | PASS-by-output | `BROWSER_PATHS.json lists 2 path(s) ...; app routes served by app.browser_oidc 2; browser_oidc.BROWSER_ROUTES 2; all three sets equal; 4 of 4 (path, method) pairs answered` / `1 passed in 1.66s` |
| OGA3-AC2 | PASS-by-output | `refused 400 with no redirect and no session cookie on 4 of 4 arms ...; upstream redemptions for the 3 state arms [0, 0, 0]` / `1 passed in 1.24s` |
| OGA3-AC3 | PASS-by-output | `refused 400, no session cookie, on 3 of 3 arms, each by its own check: InvalidSignatureError; InvalidIssuerError; InvalidAudienceError` / `1 passed in 1.32s` |
| OGA3-AC4 | PASS-by-output | `2 of 2 cookies ... Secure + HttpOnly + SameSite=lax + Path=/schwab/download + no Domain; ... sends the session to 4 of 4 download URLs and to 0 of 10 others` / `1 passed in 1.11s` |
| OGA3-AC5 | PASS-by-output | `MCP OAuth principal key == browser session principal key (True), tid equal True, oid equal True; ... same email, another oid -> another key (True)` / `1 passed in 1.25s` |
| OGA3-AC6 | PASS-by-output | `imports of app/identity.py and references to 4 ALB helper names or the ALB OIDC header 0 ...; controls: app/server.py 4 hit(s), 5 of 5 specimens caught` / `1 passed in 1.08s` |
| OGA3-AC7 | PASS-by-output | `routes at the base 27 (git object 7459929520: 27 declared ...); now 29; added 2; removed 0; changed 0; middleware unchanged` / `1 passed in 1.34s` |

## Controls

- **Mutants** (in-process plugins; the worktree was not touched):
  - the state check disabled: `test_oga3_ac02` fails on the forged-state arm (`('forged state', 302, '')`), 1 failed and 6 passed;
  - the cookies at `Path=/`: `test_oga3_ac04` fails, 1 failed and 6 passed.
- **Egress:** under a plugin that refuses every non-loopback connect and name lookup: `7 passed`, `EGRESS-ATTEMPTS: 0`.
- **Regression census,** one process per module: 13 of 14 modules pass. `test_principal_cutover` reads `1 failed,
  10 passed`, the failure being `test_oga2_ac04` on exactly `['/schwab/download/callback', '/schwab/download/login']`
  (row W3-S16). The known-red `test_identity_scope` read 6 of 6 (row W3-S21). The `test_ogq1_ac02` flake did not
  occur (13 passed).
- **Commit gate:** `OK: pre-commit gate clean for 3 of 3 file(s)`.

## Rows filed (`INVESTIGATION_v1.md` @ `b2648343dc`)

- **W3-S16** OBSERVATION, ARMED (disarm `2.0.0_SA_COO~O`): `test_oga2_ac04`'s `ROUTE_CLASS` lacks the two new paths.
- **W3-S17** OBSERVATION, ARMED (disarm `2.0.0_SA_COO~O`): OGA3-AC7 pins the base table, so the next cell that adds
  a route (OG-x-1, OG-z-1) turns it red.
- **W3-S18** OBSERVATION, INERT: the new endpoints are not in `ratelimit.AUTH_PATHS`.
- **W3-S19** OBSERVATION, INERT: the new callback must be registered as a redirect URI upstream, and no cell names
  that act.
- **W3-S20** OBSERVATION, INERT: no download path is named anywhere, so `/schwab/download` was chosen (from the audit
  test's sentinel URL). This binds OG-x-1.
- **W3-S21** OBSERVATION, INERT: the order's known-red test passed here.

## Proof check

`py -3.12 .tools/proof-of-spec-check.py org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~3/NFRA_OPLGTW.TO-OG-a-3.browser-oidc.proof_of_spec.json OGA3-AC1,OGA3-AC2,OGA3-AC3,OGA3-AC4,OGA3-AC5,OGA3-AC6,OGA3-AC7`:
the exit code is recorded in the final worker report and the commit that carries this file.
