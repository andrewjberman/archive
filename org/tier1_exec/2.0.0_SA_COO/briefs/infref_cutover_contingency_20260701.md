# INFREF cutover — COO-owned STATE-TRIGGERED CONTINGENCY (durable across session churn)

**Opened:** 2026-07-01T04:02Z · **Owner:** 2.0.0_SA_COO · **Co-auth:** 1.0.0_SA_CTO (per CTO decision 040039Z)
**Status:** ARMED (expected never to fire — cutover should settle ~05:00-06:00Z)

## The risk
INFREF rebuild STEP2a OVERWROTE live inf silver IN-PLACE (all 4 dims; pre-rebuild backup `_pre_rebuild_backup/20260630T234458Z/`). The served-GOLD nightly compute is HELD (inf-gold-incremental-daily @18Z + inf-etf-ownership-on-gold-complete both DISABLED — verified live 0357Z), so no gold computes against mid-rebuild silver. BUT the daily bronze->silver ingest chain is ENABLED and kicks at **~12:13Z** (opal-inf-jwt-fetch @12:13Z -> api pulls 12:30-14:00Z -> inf-silver-chain-bronze-complete overwrites silver). If the cutover has NOT completed by then, the daily chain overwrites the rebuilt silver mid-cutover.

## The trigger (fire IF ANY holds)
1. Current re-fire FAILS -> heading into a 2nd relaunch, OR
2. hang-diagnosis (hang-vs-slow) drags past ~2h, OR
3. cutover simply NOT done by **~10:00Z**.

## The action (on trigger)
Ping 1.0.0_SA_CTO to co-authorize, then hold (TF-safe disable) the midday daily crons — the bronze pulls (opal-inf-jwt-fetch, inf-api-{reps,assets,positions,txn}-daily, inf-{accounts,unified-account-dim,tax,billing,performance,canonical-prices}-daily) + **inf-silver-chain-bronze-complete** — as insurance; **re-enable post-cutover**. Cron-TF owner 0.7.0_AE_CloudOps is OFFLINE -> respawn it or route to whoever's live for the TF-safe toggle.

## Expected path (no fire)
0.6.1_AE re-fires clean (STEP2b+STEP3, ~30-45min) -> CVO L3/L4 parity -> swap -> DS~A validate_post_swap -> CVO L5 co-sign + CTO -> cutover settles ~05:00-06:00Z. L5 itself shadows/disables the daily path per the cutover design, closing the race. Contingency never fires.

**Tracked every /drive tick against the slip conditions. If a resumed session reads this: the trigger is COO-owned; check cutover terminal state vs the 3 conditions + the ~12:13Z deadline before letting it lapse.**
