# BD OTP -- unattended box-client onboarding spec v1 (gateway-owner spec)

**Author:** 0.5.0_AE_OpalETL (OPLMCP/m365 gateway owner) | **Date:** 2026-06-25
**For:** the BD durable auto-login OTP-read (CVO request 212029Z; gated on CTO arch-GO). Build-ready for 0.6.0 (box read) + 0.7.0 (gateway endpoint + box IAM) + CVO (cert).
**Grounding:** gateway source -- token_broker.py, oauth_as.py, server.py (routes: /register, /authorize, /token, /mcp, /teams/poll, /health).

## The model (recap, grounded)
Two independent, agent-session-free token layers:
- GRAPH (Andrew's delegated mail access): the gateway refreshes it SERVER-SIDE via token_broker's persisted encrypted MSAL cache (`acquire_token_silent`, ConfidentialClient). Andrew authorized once (already done). No agent dependency.
- CLIENT (box -> gateway): the box is its OWN registered OAuth client with a ROLLING refresh JWT (the /token refresh_token grant issues a new refresh each time). A daily-waking box never lets it lapse.

## 1. ONE-TIME AUTHORIZE (the single human-in-loop step)
1. REGISTER the box client: `POST {gw}/register` (RFC 7591 DCR; server.py:168, oauth_as.register_client) with the box/operator redirect_uri -> returns `client_id` (PKCE public client; no client_secret needed -- the security is the rolling refresh JWT + strict RS256 validation).
2. AUTHORIZE ONCE (operator-driven, Andrew signs in once): open `{gw}/authorize?response_type=code&client_id=<box>&redirect_uri=<capture>&code_challenge=<PKCE>&state=...` in a browser. The gateway bridges to Microsoft Entra as Andrew (`/login`->`/callback`); if Andrew's session/MSAL is warm it may be SSO-silent, else one interactive sign-in. On consent -> auth code.
3. EXCHANGE: `POST {gw}/token` grant_type=authorization_code + the PKCE verifier -> returns `access_token` (short) + `refresh_token` (the long-lived rolling JWT, sub=andrew@opalinvest.com, scope=GATEWAY_SCOPES).
4. STORE the `refresh_token` in Secrets Manager (sec 2). After this, NO human -- the box refreshes rolling forever.
WHO: 0.7.0 (or me) drives steps 1-4; Andrew does only the single sign-in in step 2. Same flow re-used for COT's OTP read (firm-sep on the BD side; same gateway/mailbox -- a separate box client + secret, same Andrew identity).

## 2. BOX SECRET SHAPE (Secrets Manager)
- VALUE: the box's gateway REFRESH token -- a stateless RS256 JWT {iss=gw-issuer, sub=andrew@opalinvest.com, aud=gw-issuer, scope=GATEWAY_SCOPES, client_id=<box>, typ=refresh, exp=now+GATEWAY_REFRESH_TTL}. (NOT a Microsoft/Graph credential -- it's a gateway-resource bearer, aud-pinned to the gateway; can ONLY be exchanged at /token for a gateway access token, which only reaches Andrew's mail via the gateway's own per-user Graph token. Tight blast radius.)
- PATH: recommend `blackdiamond/49f/gateway-otp-refresh` -- under the existing 49f box-role wildcard (no new IAM ARN; CVO certs the wildcard already covers it). Alt `mcp/bd-otp-box-refresh` -> 0.7.0 adds the explicit ARN + CVO certs the delta.
- ROLLING WRITE-BACK (important): the /token refresh_token grant issues a NEW refresh each call (server.py:293-294). So the box MUST write the rotated refresh JWT BACK to SM each cycle (else the stored one expires at TTL). => the box-role needs `secretsmanager:GetSecretValue` + `PutSecretValue` scoped to ONLY this secret. CVO certs read+write on this one ARN.
- PRESENT PER CALL: box reads SM -> `POST {gw}/token` grant_type=refresh_token&refresh_token=<sm>&client_id=<box> -> {access_token, refresh_token} -> write the new refresh back to SM -> use access_token as `Authorization: Bearer` on the read.

## 3. GATEWAY-SIDE email read
- EXISTS NOW: `POST {gw}/mcp` (Bearer-gated MCP JSON-RPC) tools/call name=`search_email` arguments={query:"from:noreply@bdreporting.com \"Authentication Code You Requested\"", top:5}. Parse the body with `Authorization code:\s*(\d{6})`. (read_email for the full body if the preview truncates the code.)
- RECOMMENDED 0.7.0 ADD: a thin REST `/otp/fetch` (Bearer-gated GET, mirrors /teams/poll server.py:307) that wraps search_email + the regex SERVER-SIDE and returns just `{code, received_utc}` -- curl-friendlier for the shell box + keeps the OTP-regex in one audited place. Either works; /mcp is build-ready today, /otp/fetch is the nicer box surface.
- SEARCH PARAMS (per CVO, confirmed sender pattern): from=`noreply@bdreporting.com`, subject=`Authentication Code You Requested`, regex `Authorization code:\s*(\d{6})`, scope to the last ~5 min (the OTP is fresh-per-login; recency avoids a stale code).
- ROE (single-use, never persisted): the code is in the response in-memory -> enter it -> drop. No log/commit/S3; if /otp/fetch wraps it, the gateway must not log the code (audit.py should redact the OTP body).

## 4. LIVENESS PROBE (CVO cert condition)
- RISK: Andrew's MSAL cache lapses (revoke, or the ~90d MSAL refresh expires unused) -> token_broker.get_token(andrew) raises NeedsLogin -> the box read 401s at 3am, silently.
- /health (public, server.py:148) confirms only the gateway PROCESS is up -- NOT the Graph-token liveness. So the probe must be an AUTHENTICATED call that exercises Andrew's Graph token.
- PROBE: call `whoami` via /mcp (the existing m365 whoami tool -> GET /me, which mints Andrew's Graph token) on a schedule. 200 + Andrew's profile = delegated token LIVE; 401/NeedsLogin/error = the refresh LAPSED -> CloudWatch metric -> alarm -> page Andrew to re-/login (the only re-auth event). 0.7.0 wires a probe-Lambda (cron, presents the box token, calls /mcp whoami) -> metric. CVO certs this probe as the liveness gate. (Optional: 0.7.0 add `/health/graph` that runs get_token(andrew) + returns ok/needs-login -- cleaner than a whoami round-trip, but whoami works with zero new gateway code.)

## Residual non-session dependencies (honest)
- The gateway EC2 must stay UP (persistent service, not session-coupled) -- its own health/alarm.
- Andrew's MSAL cache stays valid as long as it's used (the daily reads keep it alive); the liveness probe (sec 4) catches a lapse.
- ONE interactive sign-in at onboarding (sec 1 step 2); rolling thereafter.

## Build split
- 0.7.0: /register the box client + drive the one-time authorize; provision the SM secret + the box-role IAM (Get+Put on the one ARN); optionally build /otp/fetch + the liveness probe-Lambda + alarm.
- 0.6.0: wire getOtpCode('gateway') -> SM read -> /token refresh -> /mcp (or /otp/fetch) search -> regex -> enter -> write-back the rotated refresh.
- CVO: cert the box-auth scope (refresh JWT aud-pinned to gateway; box-role read+write ONE secret; no tenant-wide Graph cred) + the liveness probe.
- 0.5.0 (me): gateway-side correctness (confirm /register PKCE flow, the search_email query shape, audit redaction of the OTP); available to add /otp/fetch + /health/graph to the gateway if 0.7.0 prefers I own the gateway-code delta.
