# NFRA_OPLGTW.TO-OG-a-2: principal cutover result

**Worker:** `0.9.0_WK_NFRA_OPLGTW~3` | **Branch:** `wk-nfra_oplgtw-1-3c` (worktree `/c/tmp/wk-oplgtw-1-3c`, cut from
`CLOUD` at `3f94e0a024`) | **Commits (LOCAL):** `d02e73c272` code and tests; `5f47166b4b` surprise rows W3-S7..S12; and the
commit carrying this file, the proof instance and the `complete` flip. Nothing was pushed, merged or deployed.

## Read this first: an order bound is breached (row W3-S7, BLOCKING, ARMED)

All 11 criteria pass by output. One bound does not hold: **"`tests/test_oauth_durable.py` stays green"** fails, and it
cannot hold as the order is written.

- **Durable fixture:** that file's fixture replaces the upstream seam with a fake that returns only an email. No
  immutable principal can come back from its sign-in, so the cutover's bridge refuses it (fail closed, no network).
  14 of its 18 tests fail at the callback.
- **Two further tests:** `test_jwt_cve_lock.py::test_control_valid_token_accepted` and
  `test_schwab_audit.py::test_ogo1_ac06` mint a family-less access token for an email and expect it accepted. That is
  the legacy token OGA2-AC4 must reject.
- **Why no fix was possible here:** the three files are outside `<paths>`, and the order forbids editing an existing
  test. Any code path that made them pass would be the email or legacy authorization that C1 removes.

The flip below follows the order's mechanical rule (checker rc 0 and every mechanical criterion PASS-by-output). The
row carries the breach to the issuer.

## Premises re-grounded (base `3f94e0a024`)

- `token_broker.py:139,151,169`: the sign-in, the code redemption and the bridge redemption all requested `GRAPH_SCOPES`.
- `token_broker.py:173-175`: the identity was preferred_username/email/upn.
- `context.py:6-14`: the context stored only the email.
- `server.py:110`: raised `insufficient_scope` with 403.
- `server.py:85-93` (`_mcp_unauthorized`): rendered every OAuthError as 401.
- Route declarations `server.py:757-790`: 26 Route + 1 Mount = 27, matching the L4 read.

## What changed (`d02e73c272`)

| module | change |
|---|---|
| `app/context.py` | `Principal(tid, oid, email)`; `principal_key(tid, oid)` = `<tid>/<oid>` (canonical GUIDs) is the authorization identity; email is display metadata; `authorized_tenants()` = `TENANT_ID`, fail closed when unset |
| `app/token_broker.py` | the bridge asks the upstream for OpenID scopes only; the callback validates the ID token (authorized tenant before any key fetch, RS256 against the tenant's published key, exact issuer, audience = client id, expiry, the nonce derived from the sign-in's own state, GUID tid/oid); Graph tools acquire their delegated token silently from the principal's cache when they run; the legacy `/login` consent writes both caches (row W3-S10); an unconfigured upstream fails closed before any network call |
| `app/oauth_as.py` | codes, families and access tokens bind the principal; tokens carry `tver`=2, `tid`, `oid`, `sub`=`<tid>/<oid>`, `email`, `fid`; `validate_access_token` refuses a legacy token while its exp is valid, an unauthorized tenant, and a family that is not live now, is bound to another principal or no longer grants the token's scope; then the kill path. Pre-cutover codes and families answer `invalid_grant` |
| `app/server.py` | `/mcp`, `/teams/poll`, `/query/v0` take their principal only from the validated token; 401 with the resource challenge (no error code when the credential is missing, `error="invalid_token"` when invalid), 403 `insufficient_scope` with `scope=`, 503 when state is unreadable; rate limit keyed by principal |
| `app/revocation.py` | `is_principal_revoked` (a principal-key line revokes one principal; an email line only adds denial); a family id on the jti list revokes that family's access tokens; `revoke_principal` CLI |
| `tests/test_principal_cutover.py` | `test_oga2_ac01` .. `test_oga2_ac11`, offline: local issuer with a generated key behind a fake MSAL client (the gateway's own validation runs against it), moto behind a lock, a Graph recorder, the real app with its lifespan |

`app/identity.py` is unchanged. The `/mcp` path never reads it, and the access-layer helper is outside this cell's
criteria.

## Criteria (each invocation run verbatim, after the last edit to the test file)

| id | verdict | deciding output |
|---|---|---|
| OGA2-AC1 | PASS-by-output | `1 passed`: tver 2, tid, oid, sub=`<tid>/<oid>`, display email, fid; context Principal; a renamed email keeps the same principal and cache |
| OGA2-AC2 | PASS-by-output | `1 passed`: sign-in and redemption asked `['email']`, 0 of 17 Graph scopes, 0 Graph tokens; tools/list 200 |
| OGA2-AC3 | PASS-by-output | `1 passed`: whoami acquires the delegated token silently at the 8 read-only tier scopes; refused acquisition gives needs_login |
| OGA2-AC4 | PASS-by-output | `1 passed`: 27 declarations (26 Route, 1 Mount); legacy refused on 19 of 19 protected routes; live-family legacy 3 of 3 refused, current 3 of 3 accepted; 8 of 8 public unchanged |
| OGA2-AC5 | PASS-by-output | `1 passed`: JWT refresh and pre-cutover family both 400 invalid_grant; the current family 200 |
| OGA2-AC6 | PASS-by-output | `1 passed`: reuse (x2), logout and operator revocation 401; live 200 |
| OGA2-AC7 | PASS-by-output | `1 passed`: 11 forged headers plus query/body; 4 of 4 arms carry the token's principal; no token gives 401 |
| OGA2-AC8 | PASS-by-output | `1 passed`: B on A's family 401; B's Graph token is B's; A revoked by principal, so A 401 and B 200 |
| OGA2-AC9 | PASS-by-output | `1 passed`: unauthorized-tenant sign-in 400, 0 codes, 0 key lookups; a de-authorized tenant's token 401, refresh invalid_grant |
| OGA2-AC10 | PASS-by-output | `1 passed`: 18 of 18: missing 401 bare challenge, invalid 401 `error="invalid_token"`, no scope 403 `insufficient_scope`, full 200 |
| OGA2-AC11 | PASS-by-output | `1 passed`: policy and Graph denials are tool errors in a 200 with no challenge and no login; REST Graph 403 gives 502; the token still works |

AC4's first run failed on `/ms/site_children`, which answers 400 before its credential check (row W3-S11). The census
now sends well-formed parameters, and AC4 was re-run verbatim after that edit.

## Regression census (a second instrument: every other Gateway module, one process each)

The one-process whole suite hangs at base (rc 124 at 300 s, row W3-S12), so each module ran in its own process with
`-m "not live" -k "not test_scoped_deny_by_default"`.

| module | base `3f94e0a024` | build `d02e73c272` |
|---|---|---|
| test_access_state | 7 passed | 7 passed |
| test_attachment_tools | 5 passed | 5 passed |
| test_identity_scope | 5 passed, 1 deselected | 5 passed, 1 deselected |
| test_jwt_cve_lock | 6 passed | **1 failed**, 5 passed (W3-S7) |
| test_min_tier_gate | 3 passed | 3 passed |
| test_oauth_durable | 18 passed | **14 failed**, 4 passed (W3-S7) |
| test_ratelimit | 6 passed | 6 passed |
| test_schwab_audit | 7 passed | **1 failed**, 6 passed (W3-S7) |
| test_schwab_engine | 13 passed | 1 failed, 12 passed: `test_ogq1_ac02` lag bar under box load; re-run 2 of 2 PASS alternating with base 2 of 2 (W3-S12) |
| test_sprint_view | 8 passed | 8 passed |
| test_ssavail_contract | 8 passed | 8 passed |
| test_teams_format | 35 passed, 34 subtests | 35 passed, 34 subtests |

Egress census: the durable file plus this cell's file, run under a socket-and-DNS-refusing plugin, printed
`EGRESS-ATTEMPTS: 0`. The durable sign-ins that now fail are refused before any network call.

## Controls

- **Mutant:** in an archive of HEAD (the worktree untouched), `validate_access_token`'s family status check was removed.
  Result: `1 failed, 1 passed`. AC6 failed (a revoked family's token served tools/list); AC2 passed. FIRED-AS-EXPECTED.
- **Determinism:** the whole file twice. Both runs gave `11 passed`, and only the wall-clock line differs. STABLE.

## Rows filed (`5f47166b4b`)

| id | class | hazard | subject |
|---|---|---|---|
| NFRA_OPLGTW-W3-S7 | BLOCKING | ARMED (2.0.0_SA_COO~O) | 16 existing tests assert the removed behaviour; order bound breached |
| NFRA_OPLGTW-W3-S8 | OBSERVATION | INERT | tool-layer denials come back with MCP isError false |
| NFRA_OPLGTW-W3-S9 | OBSERVATION | ARMED (2.0.0_SA_COO~O) | tier, allowlist, min-tier and catalog still key on the display email |
| NFRA_OPLGTW-W3-S10 | OBSERVATION | INERT | `/login` consent route changed too; first Graph token from an OpenID-only sign-in |
| NFRA_OPLGTW-W3-S11 | OBSERVATION | INERT | `/ms/site_children` validates parameters before its credential |
| NFRA_OPLGTW-W3-S12 | OBSERVATION | INERT | the one-process Gateway suite hangs at base |

## Side effects outside the grant

- **Gateway `audit.jsonl` (tracked):** a scratch probe run from the Gateway directory appended one line (217 bytes) to
  `infra/aws/ec2/opal-gateway/audit.jsonl` through the default `AUDIT_PATH`. That line was removed, and
  `git diff --quiet` on the file reads equal to HEAD. Nothing of it was committed.
- **Root `audit.jsonl` (untracked):** the same default path produced an untracked `audit.jsonl` at the worktree root. It
  is not committed and is left for the worktree's removal.
