# NFRA_OPLGTW.TO-OG-a-1 -- durable OAuth: result

**Worker:** `0.9.0_WK_NFRA_OPLGTW~3` | **Branch:** `wk-nfra_oplgtw-1-3b` (worktree `/c/tmp/wk-oplgtw-1-3b`, cut from
`CLOUD` at `8d8b221ee6`) | **Commits (LOCAL):** `51b0f7d823` code and tests, `4daf5659fa` surprise rows, and the
commit carrying this file, the proof instance and the `complete` flip. Nothing was pushed, merged or deployed.

## What changed

`infra/aws/ec2/opal-gateway/app/oauth_as.py` -- every piece of OAuth state goes through `app/access_state.py`
(OG-d-1). The process-local `_clients` / `_pending` / `_codes` dicts are gone (the AST check in AC13/AC14 finds 0
module-level mutable stores).

| record | key | lifetime | rule |
|---|---|---|---|
| client | `RUNTIME#client#<client_id>` | none (row W3-S5) | DCR JSON; each redirect is exactly `https://claude.ai/api/mcp/auth_callback` or an http loopback URI, else the whole registration is refused |
| pending authorization | `RUNTIME#pending_auth#<arid>` | 600 s logical | bound to client, redirect, state, S256 challenge, scope, resource and a nonce the Fernet bridge state also carries; consumed conditionally at the callback |
| code | `RUNTIME#code#<sha256(code)>` | 60 s logical | issued client_id required; exact redirect; bound resource; S256 verifier (a failed verifier burns the code); consumed in the same transaction that installs the family; a replay revokes that family |
| refresh family | head `RUNTIME#refresh#<fid>`, generations `RUNTIME#refresh#<fid>#g<n>` | 30 d absolute, 7 d idle, recorded on the head and checked logically | token `ogr1.<fid>.<n>.<256-bit secret>`, stored only as SHA-256; one conditional TransactWriteItems (Update head, Update g<n> consumed, Put g<n+1>) per rotation; a concurrent loser fails the head condition and gets invalid_grant; a consumed token of the family presented again revokes the family; scope only narrows, and a reduction is recorded |

Also in `oauth_as.py`:
- Access tokens last 900 s (contract `access_token_seconds`) and carry the family id as `fid`.
- `principal_key(email)` is the one function OG-a-2 changes to the tid/oid principal.
- Authorize accepts only a registered client (the old unregistered-loopback branch is removed, so such a client must reconnect) and a registered redirect: the hosted callback as an exact string, a loopback redirect on any port (RFC 8252 s7.3).
- Only the advertised resource is accepted (an absent resource means the advertised one), at authorize and at both grants.
- The metadata documents are built from `enforced_configuration()`, the same values the handlers enforce.
- A store failure, or an unreadable revocation list, answers 503 `temporarily_unavailable`; there is no stateless branch. The JWT refresh functions are removed (row W3-S3).
- The existing kill path still applies at refresh: the jti deny-list (matched against the family id), the user cutoff and the blocklist.

`app/server.py`:
- `/register` accepts JSON only and `/token` form encoding only.
- register, authorize, callback and token run their blocking work on a dedicated 16-thread pool under the C1 budgets (10 s auth, 30 s refresh) and answer 503 when a budget elapses.
- The callback resumes the durable pending authorization first and asks the upstream who the user is only after that record is found.
- OAuth route paths come from the `oauth_as` constants.
- Refusal pages are HTML-escaped.
- The single-worker guard stays, and its message now names the in-process rate limiter as the reason.

`tests/test_oauth_durable.py` -- `test_oga1_ac01` .. `test_oga1_ac18`, all offline:
- moto 5.2.3 sits behind a per-request lock, which models DynamoDB's request serialization.
- The upstream is a local issuer whose RSA key is generated at test time.
- The Fernet key is generated at test time.
- Fake AWS credentials and an empty config are forced.
- The real Starlette app runs in-process, with the per-IP rate limiter off and every flat-file control pointed at `tmp_path`.

## Criteria (each invocation run verbatim, after the last edit to the test file)

| id | verdict | deciding output |
|---|---|---|
| OGA1-AC1 | PASS-by-output | `1 passed` -- accepted 7 of 7 registered forms, refused 11 of 11 unregistered |
| OGA1-AC2 | PASS-by-output | `1 passed` -- 11 of 11 hosted/malformed refused, 0 client records written |
| OGA1-AC3 | PASS-by-output | `1 passed` -- same code: no client_id 400, other client 400, issued client_id 200 |
| OGA1-AC4 | PASS-by-output | `1 passed` -- 4 of 4 unregistered refused, 0 upstream hops, 0 pending |
| OGA1-AC5 | PASS-by-output | `1 passed` -- other resource 400 at authorize, code exchange and refresh |
| OGA1-AC6 | PASS-by-output | `1 passed` -- plain/absent 400; wrong verifier and plain trick 400; S256 200 |
| OGA1-AC7 | PASS-by-output | `1 passed` -- second redemption 400 invalid_grant; family revoked |
| OGA1-AC8 | PASS-by-output | `1 passed` -- 1 write call, transact_write_items, 3 of 3 items conditional |
| OGA1-AC9 | PASS-by-output | `1 passed` -- reuse 400, family revoked, newest 400; control 200 |
| OGA1-AC10 | PASS-by-output | `1 passed` -- 8 concurrent: 1 x 200, 7 x 400 invalid_grant, 1 successor |
| OGA1-AC11 | PASS-by-output | `1 passed` -- broader 400 invalid_scope; narrower recorded; never re-broadened |
| OGA1-AC12 | PASS-by-output | `1 passed` -- 900 / 2592000 / 604800; expiry refused with the record present |
| OGA1-AC13 | PASS-by-output | `1 passed` -- resume 302 with the original state; 3 of 3 lost arms restart_login, 0 identity lookups |
| OGA1-AC14 | PASS-by-output | `1 passed` -- 307 after restart; control over an empty table 400 invalid_client |
| OGA1-AC15 | PASS-by-output | `1 passed` -- failing store 503 x 4, legacy 400; healthy: the same code and token 200 |
| OGA1-AC16 | PASS-by-output | `1 passed` -- 13 of 13 fields equal the enforced configuration; 5 of 5 probes refused |
| OGA1-AC17 | PASS-by-output | `1 passed` -- JSON token exchange 400 invalid_request; form 200 |
| OGA1-AC18 | PASS-by-output | `1 passed` -- 96 responses, max 0.740 s auth / 0.851 s refresh; overrun 503 in 0.32 s |
| OGA1-AC19 | PASS-by-output | `108 passed, 1 deselected, 34 subtests passed in 22.74s`, rc=0 (base: 90 passed, 1 deselected) |

## Controls

- **Base discrimination** (a second instrument): the new tests run against the pre-change `oauth_as.py` and
  `server.py`, taken from `git archive 8d8b221ee6` into `.scratch/base`. Result: `18 failed`. 15 fail on behaviour
  and 3 on a missing contract constant or function.
- **Mutant**: an authorization code made redeemable twice. Result: `1 failed, 1 passed` (AC7 fails at
  `200 == 400`; AC1 passes). The restored file's sha256 is `dd3f9663...`, equal to HEAD's blob.
- **Determinism**: the whole file run twice gives `18 passed` both times. 3 lines differ: a random client_id, the
  AC18 timings and the wall clock.

## How the whole suite first went red

The AC19 invocation first printed `1 failed, 107 passed` twice; the failing test was `test_oga1_ac18`, which
passes alone. Pairing AC18 with each of the other 10 modules isolated `test_ratelimit.py`. With diagnostics the
failure printed `(201, 200, 1.507, 1.581)`: a 0.3 s `asyncio.wait_for` never timed out. The cause is
`tests/test_ratelimit.py:20`, which replaces `time.monotonic` for the whole process at import, so asyncio's loop
clock stops. The OG-a-1 fixture now restores the builtin for each of its own tests, and monkeypatch puts the fake
back afterwards; `test_ratelimit.py` is untouched. After the guard, the pair gives `7 passed` and the suite gives
`108 passed`. Row NFRA_OPLGTW-W3-S6.

## Decisions the order did not make (each is a row or an exclusion)

- The legacy refresh JWT is refused now, because keeping it would be the stateless branch C1 forbids -- row W3-S3.
- Lifetimes come from the contract, which leaves config.py's two TTL knobs dead -- row W3-S4.
- Client records carry no lifetime -- row W3-S5.
- A concurrent loser (its transaction condition failed) gets invalid_grant WITHOUT revoking the family. A token
  shown to be consumed, i.e. whose generation record hash matches and which is no longer current, revokes the
  family. An unknown token gets invalid_grant without revoking, so a caller who knows only a family id cannot
  revoke a user's session.
- At authorize, unknown scopes are dropped (a partial grant, RFC 6749 s3.3); a request naming only unknown scopes
  is invalid_scope. At refresh, any scope outside the family's is invalid_scope (RFC 6749 s6).
- `code_challenge_method` must be present and S256. The old handler defaulted an absent method to S256; RFC 7636
  defaults it to plain, which is refused.

## Proof check

`py -3.12 .tools/proof-of-spec-check.py <instance> OGA1-AC1,...,OGA1-AC19`. The first run printed `INVALID (rc=1)`,
one violation: the AC11 row's output_evidence omitted the `1 passed in 1.44s` / `rc=0` lines, a transcription
miss (the log `.scratch/ac11.log` has them). After the correction it printed `proof-of-spec-check | structural=jsonschema | acceptance rows=19 |
violations=0` ... `VALID (rc=0)`. Artifacts: 4 of 4 resolved at their pins, content-resolved by their `introduces` tokens.
Surprises: 4 of 4 entries resolve to a channel row.

## Rows filed

NFRA_OPLGTW-W3-S3, -S4, -S5, -S6: all OBSERVATION, INERT; committed at `4daf5659fa` (surprise-row-gate: 4 new of 8,
OK).

## Not done (declared exclusions in the proof)

- The live table and IAM (OG-i-1).
- The tid/oid principal, legacy access-JWT rejection, the family check on protected requests and the reconnect notice (OG-a-2).
- An HTTP logout or revocation endpoint (none exists and no criterion names one; `revoke_family()` and the operator lists cover revocation).
- A two-OS-process restart (moto server mode needs flask, which is not installed).
- Edits to `config.py` or `test_ratelimit.py` (outside the grant).
- Deploy, push or merge.

The suite run from the workspace root appends to an untracked `audit.jsonl` at the worktree root. It is not
committed, and no tracked file is modified.
