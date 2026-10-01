# OG-lt-1 -- stored sign-in lifetime (READ only)

Verdict: GE_1_DAY. observed_unattended_hours = 1126.87 (about 46.9 days), claim class `measured`, a LOWER BOUND on the lifetime.

## What was read

- Store: the Fernet-encrypted MSAL cache file the broker reads for the machine identity (`token_broker._cache_path(email-lowercased)` = `<TOKEN_CACHE_DIR>/sha256(owner).bin`, dir `/opt/opal-gateway/.token_cache`). Fields used: `RefreshToken.last_modification_time`, `AccessToken.cached_at`, and an 8-hex hash prefix of the refresh token (to prove rotation). No token, refresh token or blob was printed or moved.
- Before the on-demand refresh: refresh-token last modification 2026-10-01T02:03:06Z (the service's own most recent silent refresh).
- On demand: one refresh through the broker's own path with `force_refresh=True` (a plain `get_token` may answer from a still-valid cached access token and prove nothing). Outcome `OK` at 2026-10-01T02:15:06Z; the refresh-token hash prefix changed (d6e8db46 to 1e29f9bc) and its last modification moved to 02:15:07Z, so a real server-side refresh and rotation occurred.
- Last interactive sign-in: the MSAL cache holds NO interactive-sign-in timestamp (only the last refresh write). It is INFERRED from the gateway audit log (`/opt/opal-gateway/audit.jsonl`, rows for this identity, 62,391 rows): the identity's last three `needs_login` rows are all on 2026-08-15 (last 03:21:57Z) and the first non-`needs_login` row follows at 03:23:06Z. The interactive consent therefore fell between 03:21:57Z and 03:23:06Z; 03:23:06Z is used, which makes the span the smaller (lower-bound-safe) figure. Claim class of that timestamp: inferred, within about 70 seconds.

## Computation

1126.87 h = 2026-10-01T02:15:07Z minus 2026-08-15T03:23:06Z. At least 24 h, so GE_1_DAY. The refresh chain has been continuous since (the identity's audit rows are `ok` through 2026-10-01T02:12Z with no later `needs_login`).

## What it cannot see

- The identity platform's refresh-token policy (inactivity window, conditional-access or sign-in-frequency limits, revocation) is not readable from the host. The span is a floor: the token was still good at 1126.87 h, not proof of when it would lapse.
- The chain stayed alive partly because the gateway refreshes it continuously (about hourly access-token use from the polling route); a schedule that went quiet for the policy's inactivity window could lapse it, which this measurement does not bound.
- The interactive time is inferred from the audit log, not recorded in the store.
- Every refresh rotates the stored refresh token; the one on-demand refresh rewrote the cache file through the broker's own `_save_cache` (the normal behaviour of every get_token).
