# BD OTP Cross-Firm Fetch Lock — design contract (GATE-B durable concurrency control)

**Author:** 0.6.2_AE_PartnerETL · **Project:** ADVI_BDAPIMIG.P1-DURABLE (GATE-B) · **Date:** 2026-06-29
**Status:** DESIGN for review — COO ruled GATE-B = the lock (not the time-blackout); CTO arch-gates;
gateway-owner (0.7.0/base) lands the gateway code. NOT on the LEG2 critical path (sequence after/alongside).

## Problem (grounded)
One shared OTP mailbox (otp.py:96 `cfg.OTP_MAILBOX` = andrew@opalinvest.com; the per-firm OTP_BEARER
AUTHORIZES the /otp/fetch call but does NOT route to a per-firm mailbox — otp.py:50-72). cot + 49f BD OTP
emails are content-identical (same sender/subject/pattern, only the 6-digit code differs). `window_seconds`
(otp.py:128-131 clamp) bounds STALENESS — it rejects a code outside [since, since+window] — but does NOT
prevent two firms fetching CONCURRENTLY: if a cot code and a 49f code both land inside the same window,
the newest-in-window match (otp.py:124 loop) can return the WRONG firm's code = silent firm-sep break
(NEVER#1). The blackout heuristic was disqualified: (i) cot worst-case OTP-activity span ~15-20min
(3 attempts x ≤300s OTP poll + backoff) >> a happy-path window, and (ii) cot has multiple trigger paths
(cron 0 2 + keepalive rate(15m) + freshness-probe) so its login activity is not single-window.

## Invariant the lock must guarantee
At most ONE firm's BD login may be inside its "OTP send -> OTP fetch" critical section against the shared
mailbox at any time. While firm A holds it, firm B's login cannot trigger an OTP send + fetch that could
read A's code (or vice versa). CANNOT-happen, not unlikely.

## Why a gateway-side-only /otp/fetch lock is INSUFFICIENT (key design point)
The collision is created at CREDENTIAL SUBMIT (when BD sends the OTP into the mailbox), which is BOX-side,
not at the gateway fetch. A lock acquired only inside /otp/fetch can't stop firm B from submitting creds
(injecting a B code into the mailbox) while A is mid-fetch. So the lock must be HELD ACROSS the box's
cred-submit, i.e. acquired BEFORE the box submits credentials and released after the fetch. The lock STATE
lives gateway-side (COO's framing); the box ACQUIRES/RELEASES it via the gateway around its login.

## Contract — 3 gateway endpoints (extend the existing /otp/* capability surface)
All bearer-gated by the SAME static capability bearer the box already holds (otp.py check_bearer), so no
new auth model. Lock state in a single DynamoDB item (conditional-write) keyed to the shared mailbox.

1. POST /otp/acquire  {firm_hint?}  -> {lock_token, expires_at} | 409 LOCK_HELD
   - Conditional-put a global item PK=`otp-lock:<OTP_MAILBOX>` IF not-exists OR expired. Holder = a fresh
     opaque lock_token + the caller's bearer-derived firm id + TTL (default 1200s = 20min worst-case ceiling;
     auto-expiry so a crashed holder never deadlocks). Returns 409 if another live holder exists.
   - The box calls this BEFORE nav/login. On 409 it WAITS-with-jitter and retries up to a bounded deadline
     (e.g. 25min), then loud-fails rc=1 (re-triggers later) — FAIL-CLOSED, never proceeds without the lock.
2. POST /otp/fetch  {sender,subject,since,pattern,window_seconds, lock_token}  -> {code} | 423 NO_LOCK
   - UNCHANGED selection logic (the window clamp stays as defense-in-depth) PLUS: require a valid, live
     lock_token whose holder == this caller's firm. If absent/expired/foreign -> 423 LOCK_REQUIRED, no read.
     This makes a fetch without the held lock impossible (closes the gateway half).
3. POST /otp/release  {lock_token}  -> {released:true}
   - Delete the lock item IF holder==lock_token (idempotent; no-op if already expired). The box calls this
     in a finally-block after fetch (success OR terminal failure) so the lock frees immediately on the
     common fast path (~<2min when the OTP arrives quickly), not held for the full TTL.

## Box-side (thin; the only box change)
run-bd-auto-login.js wraps attemptLogin in: acquire (before cred submit) -> ... -> release (finally).
Re-acquire/extend on each retry attempt by the SAME holder is idempotent (same firm extends its own TTL,
never blocks itself). On acquire-timeout: rc=1 LOUD (the existing OTP_GATEWAY_NO_CODE loud-fail+retry path
already handles a wait/retry, so the trigger lane re-fires later) — no silent wrong-firm mint.

## Fail-closed matrix
- lock DDB unreachable -> acquire fails -> box loud-fails rc=1 (do NOT proceed lock-less).
- /otp/fetch without a live held lock -> 423, no mailbox read.
- holder crashes -> TTL auto-expiry frees the lock (bounded by the 20min ceiling) -> other firm proceeds.
- both firms race /otp/acquire -> conditional-write gives exactly one winner; loser 409 -> waits.

## Firm-sep properties
- Single global lock (keyed to the shared mailbox), NOT per-firm — that is the point (serialize ACROSS firms).
- Each firm still uses its OWN bearer (firm-sep auth) + OWN since/window. The lock adds mutual exclusion on
  the shared resource without sharing any firm secret.
- window_seconds clamp RETAINED as belt-and-suspenders (a second independent guard).

## Scope / sequencing
Gateway code-land = 0.7.0/base (m365-mcp-gateway otp.py + server.py + a DDB table + gw-role DDB IAM).
CTO arch-gates the contract. Box-side acquire/release = my lane (small wrapper/js change). Sequence AFTER
LEG2 proves the mechanism (GATE A); GATE B (unattended 49f enablement) stays HELD until the lock is built
AND proven. COO formalizes the lock + trigger-lane TO.
