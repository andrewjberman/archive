# NEVER-WIDEN ASK -- `OG-ev-10` STEP 2 -- ONE controlled identity refusal against the existing limiter: NO TEST PRINCIPAL EXISTS THAT IS NOT A PERSON'S IDENTITY, so `NOT_EXPOSED` STANDS and there is NO act to sign

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ev-10.round-44-is-the-audit-refusal-write-failing.md` (STEP 2 GO: msg 35864, "if no non-person test principal exists, say so in the ask, and NOT_EXPOSED stands"). STEP 1 (`W/AUDIT_REFUSAL_WRITE.json`, committed): 1413 `POST /mcp` lines since 2026-10-18T19:23:53Z, 0 answered 429, 0 writer WARN lines, 0 `gw_ratelimit` rows over 5568 lake objects, counter exposed by no route: `NOT_EXPOSED`. Nothing has been sent to the gateway for STEP 2.

## 1. What STEP 2 needs, and what exists (read, not guessed)

The limiter is reached only by a request that passes `GuardMiddleware` (`app/server.py`): `_bearer_auth` runs `oauth_as.validate_access_token` and the refusal is keyed on the validated `principal.key` (`<tid>/<oid>`), so the 121st request in 60 seconds needs a **valid gateway access token for one principal**. `validate_access_token` (`app/oauth_as.py`) accepts a token only if all of these hold: (1) the RS256 signature of the gateway's own key, issuer and audience; (2) token version 2 and an immutable `tid`/`oid` pair; (3) the principal's tenant is authorized; (4) **the refresh family named by the token's `fid` is live in the gateway's durable state, bound to the same principal and granting the scope** (a strong read); (5) the kill path (jti, family, principal) is clear. Tokens come only from the OAuth authorization-code flow after an upstream (Microsoft Entra) sign-in, and `issue_access_token` is called from a refresh family.

- **No machine or service principal exists** for `/mcp`: the code has no `client_credentials` grant, no static or test token, and no non-person identity that signs in. Every identity that can hold a valid token is a person's.
- The only other principals in the repo are the **in-process** ones: the listener's fixed probe principal (`app/probe_listener.py`, built in code, never from a token, and served by the loopback listener, which does NOT pass `GuardMiddleware` or the limiter) and the `master`/probe principals this seat builds inside guarded fresh processes. None is a bearer; a request through `/mcp` cannot carry them.
- Producing a bearer for a synthetic principal would need the gateway's signing key (a secret in the service environment) AND a refresh-family record written to the gateway's durable state, plus an authorized tenant. That is minting a credential and writing access state, not "requests only"; the order's bounds (no state write outside the audit lake, no SSM write, no environment change, no use of a person's identity) do not cover it, and I have not tried it.
- The session this seat itself runs in holds an authenticated gateway connection, but it is a person's (`whoami` names a signed-in user). The order forbids it.

**Therefore:** the controlled refusal cannot be made as specified. **`NOT_EXPOSED` stands.** The verdict of `W/AUDIT_REFUSAL_WRITE.json` is unchanged, `controlled_refusal` stays `null`, and the proof instance already committed (`AC1` PASS) stays the record of this cell.

## 2. process-wide state this change touches: none, read

No change is proposed. (I opened `app/server.py`, `app/ratelimit.py`, `app/oauth_as.py` and `app/audit.py` to write section 1.)

## 3. Options for the issuer or the CTO to rule (none is started, none is signed here)

- **(a) Wait for an organic 429 and re-read.** `ev10_step1.py` is read-only and repeatable (about two minutes over a day's lake): run it again after a period of heavy use, or whenever a person reports a rate-limited call. A 429 line in the journal with no `gw_ratelimit` row, or a WARN line, decides `FAILS`; a 429 with a row decides `WRITES`. Cost: none, but it decides only if a 429 ever happens (0 of 1413 in 7 hours).
- **(b) A fresh guarded process calls `ratelimit.record_identity_refusal` with a synthetic principal key against the real audit sink** (the code path after the limiter), then the lake is read within 120 seconds for the row. It would write ONE `gw_ratelimit` object to the audit lake (an S3 write of one small record under a synthetic key such as `00000000-0000-4000-8000-0000000000b3/...`), needs its own ask and three halves, and tests the WRITER (the part Z-W155-S1 doubts), not the middleware path. It does not need a bearer. It would answer "can this process's writer record a row", which is the narrower, decidable question.
- **(c) Withdraw the cell** as undecidable without a test principal, and carry the writer question to whoever next builds a non-person `/mcp` principal.

My recommendation: (a) now, then (b) only if the CTO wants the writer proved before an organic 429.

## 4. Both branches

Nothing is sent, armed, written or released by this ask. If an option is chosen, it needs its own ask and halves.

## 5. Rollback

None needed: no act.

## 6. Triggers

None: no act.

## 7. Gate lines

Files: this ask only (a `W/` document). No product file, no test, no AWS call.

## 8. The three halves

### CTO half (`1.0.0_SA_CTO~Z`)

Nothing to sign: no act is proposed. Read section 1 and rule on options (a), (b) or (c).

### COO half (`2.0.0_SA_COO~O`)

Nothing to sign: no act is proposed. Read section 1 and rule on options (a), (b) or (c).

### CVO half (`3.0.0_SA_CVO~Z`)

Nothing to sign: no act is proposed.
