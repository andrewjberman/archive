# INFREF cutover — COO-owned STATE-TRIGGERED CONTINGENCY (durable across session churn)

**Opened:** 2026-07-01T04:02Z · **Owner:** 2.0.0_SA_COO · **Co-auth:** 1.0.0_SA_CTO (per CTO decision 040039Z)
**Status:** ARMED (expected never to fire — cutover should settle ~05:00-06:00Z)

## The risk
INFREF rebuild STEP2a OVERWROTE live inf silver IN-PLACE (all 4 dims; pre-rebuild backup `_pre_rebuild_backup/20260630T234458Z/`). The served-GOLD nightly compute is HELD (inf-gold-incremental-daily @18Z + inf-etf-ownership-on-gold-complete both DISABLED — verified live 0357Z), so no gold computes against mid-rebuild silver. BUT the daily bronze->silver ingest chain is ENABLED and kicks at **~12:13Z** (opal-inf-jwt-fetch @12:13Z -> api pulls 12:30-14:00Z -> inf-silver-chain-bronze-complete overwrites silver). If the cutover has NOT completed by then, the daily chain overwrites the rebuilt silver mid-cutover.

## The trigger (fire IF ANY holds)
1. **INTRACTABLE repeat failure** — a re-fire fails AGAIN on a NEW reason with no tractable known-fix (NOT any trivial known-fix re-fire; CTO-refined 042537Z — the original "2nd relaunch" wording meant intractability, not re-fire count), OR
2. hang-diagnosis (hang-vs-slow) drags past ~2h, OR
3. cutover simply NOT done by **~10:00Z**.

## The action (on trigger)
Ping 1.0.0_SA_CTO to co-authorize, then hold (TF-safe disable) the midday daily crons — the bronze pulls (opal-inf-jwt-fetch, inf-api-{reps,assets,positions,txn}-daily, inf-{accounts,unified-account-dim,tax,billing,performance,canonical-prices}-daily) + **inf-silver-chain-bronze-complete** — as insurance; **re-enable post-cutover**. Cron-TF owner 0.7.0_AE_CloudOps is OFFLINE -> respawn it or route to whoever's live for the TF-safe toggle.

## Expected path (no fire)
0.6.1_AE re-fires clean (STEP2b+STEP3, ~30-45min) -> CVO L3/L4 parity -> swap -> DS~A validate_post_swap -> CVO L5 co-sign + CTO -> cutover settles ~05:00-06:00Z. L5 itself shadows/disables the daily path per the cutover design, closing the race. Contingency never fires.

**Tracked every /drive tick against the slip conditions. If a resumed session reads this: the trigger is COO-owned; check cutover terminal state vs the 3 conditions + the ~12:13Z deadline before letting it lapse.**

## Checkpoint log
- **04:23Z — CHECKPOINT 1 (re-fire f7bdc4a8 FAILED #4):** literal "2nd relaunch" condition MET, but evaluated NOT-SLIPPING -> hold NOT fired (CTO co-auth pinged 042243Z-ish). Rationale: the 4h-ceiling TIMEOUT FIX WORKED (ran 18min, past the 2h wall); STEP2b-tail GREEN -> **silver FULLY REBUILT (expensive ~105min BANKED)**; failure was a trivial arg-contract bug (orion-gold-dispatch.sh --stage rejects --run-date on date-agnostic steps), NOT timeout/hang/data; DS~A handed 0.6.1 the fix (drop --run-date); next re-fire = STEP3-only-FAST; ~8h margin to 12:13Z. Served UNTOUCHED. RE-EVAL at next checkpoint IF the STEP3-only re-fire ALSO fails OR not staged-clean by ~10:00Z.
