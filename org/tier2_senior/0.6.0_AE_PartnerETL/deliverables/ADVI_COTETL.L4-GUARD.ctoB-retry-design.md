# ADVI_COTETL.L4-GUARD CTO-B — retry-on-login-failure (pre-staged design)

**Owner:** 0.6.0_AE_PartnerETL · **Status:** PRE-STAGED (design only; not built).
**Timing:** FAST-FOLLOW per CTO ruling 145308Z (catastrophic-safety floor already met without it) —
becomes a HARD pre-activation gate ONLY if CVO rules clause-6c requires IN-RUN self-heal (CTO asking CVO).
**Build gate:** touches the SHARED firm-parameterized `bd_49f_auto_login.js` (affects 49F too) ->
CTO arch sign-off ON THE DIFF + 0.7.0 coordination BEFORE deploy. S3->box (Rule 12).

## Why this is fast-follow, not a gate (the safety floor that already holds)
A wrong/stale OTP today fails LOUD, not silent (source-grounded):
- `otpEntered` guard (L267, L358-364) blocks re-reading the consumed code; a wrong code never reaches
  LOGGED_IN -> loop exhausts MAX_STEPS -> `rc=1` (L415), `.bd.identity` NOT written, session NOT advanced.
- => PIECE-1 keepalive(401) + freshness-probe + served-aua-stale all fire. SILENT re-freeze is impossible.
- CVO clause-6 (a 200-mint can ONLY come from cot's own code) + gateway recency+~120s window => silent
  WRONG-firm 200 is impossible.
CTO-B only improves RECOVERY LATENCY (next-cycle -> in-run) on the RARE 49F-code-in-cot-window edge.

## Design (CTO confirmed arch-SOUND 145308Z)
Wrap the existing perceive-act login loop in an OUTER retry:

```
const MAX_LOGIN_ATTEMPTS = parseInt(process.env.BD_MAX_LOGIN_ATTEMPTS || '3', 10);
for (let attempt = 1; attempt <= MAX_LOGIN_ATTEMPTS; attempt++) {
  // RESET per-attempt state so a fresh OTP is fetched (NEVER the stale one):
  otpSent = false; otpEntered = false;
  const loginStart = Date.now();          // fresh anchor -> getOtpCode fetches the NEW code only
  // ... existing nav + perceive-act loop, sets rc ...
  if (rc === 0) break;                     // success
  if (attempt < MAX_LOGIN_ATTEMPTS) {
    const backoffMs = BASE_BACKOFF_MS * Math.pow(2, attempt - 1); // retry-storm guard
    log(`login attempt ${attempt} failed rc=${rc} -> backoff ${backoffMs}ms + re-trigger fresh OTP`);
    await sleep(backoffMs);
    // re-nav fresh: new browser context (avoid a poisoned page/cookie carry-over)
  }
}
```

### CRITICAL guards (CTO-flagged)
1. **Retry-storm guard** — `MAX_LOGIN_ATTEMPTS` cap (default 3) + EXPONENTIAL backoff. A genuinely-dead
   session (bad creds, BD outage, account lock) must NOT hammer BD login (lockout / abuse-flag risk).
   After cap exhaustion: exit `rc=1` LOUD (PIECE-1 fires) — same terminal state as today, just later.
2. **Fresh `loginStart` per attempt** — the OTP time-window anchor MUST advance each attempt so
   `getOtpCode(loginStart)` (gateway adapter, `since`) fetches the attempt's OWN fresh code, never the
   stale prior one. This is the whole point — a retry that re-reads the stale code is a no-op.
3. **Fresh browser context per attempt** — re-`newContext()` so a poisoned/half-authed page or a stale
   cookie from the failed attempt doesn't carry over and mask a clean re-login.
4. **Firm-sep unaffected** — purely control-flow; no secret-id or path change. Both firms inherit it
   identically (env-tunable cap via `BD_MAX_LOGIN_ATTEMPTS`; 49F can set =1 to preserve current behavior
   until 0.7.0 opts in).
5. **BD device-trust interaction** — each fresh attempt re-checks "Remember My Device"; verify the retry
   doesn't burn device-trust state. (Test on the cot box; 49F deploy only after 0.7.0 signs off.)

## CVO clause-6c contingency
- If CVO accepts **next-cycle-recovery** (02:30 re-run re-attempts with a fresh code = recovers, not a
  hang) as satisfying 6c -> retry stays fast-follow; activation proceeds on the rest of the bar.
- If CVO requires **in-run self-heal** -> this becomes a HARD pre-activation gate; build + CTO-sign-off +
  0.7.0-coord + deploy BEFORE the 02:00 re-point.

## Build checklist (when triggered)
- [ ] Implement the outer loop + 5 guards in `bd_49f_auto_login.js`.
- [ ] `BD_MAX_LOGIN_ATTEMPTS` (default 3) + `BD_LOGIN_BACKOFF_MS` (default e.g. 5000) env, documented in both secret-ids.env templates.
- [ ] CTO arch sign-off on the DIFF (shared script).
- [ ] 0.7.0 coordination (49F inherits the script; 49F sets cap=1 until they opt in).
- [ ] py/js lint + local dry-run; deploy cot box first (S3->box), e2e the 6c self-heal, THEN 49F on 0.7.0 GO.
- [ ] Deploy ledger; tag.
