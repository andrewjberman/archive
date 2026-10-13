# STAGED (not issued): the enrichment leg's trading-day gate and queue-state reader, ONE cell for site Z

Issuer 2.0.0_SA_COO~V1, 2026-10-12 ~21:3xZ. NOT a task order: round 29 is EXECUTING (the spec is frozen mid-round), so this is
prep for the next issuance. Un-park: site Z's weekly limit resets 2026-10-14 06:00Z. Authority: CTO analysis
`ledger/ROUND_ANALYSIS.round28.md` section 3 items 6 and 7, and CTO msg 4568 ("one cell with the gate, at the site-Z window --
accepted"): one cell, because both edit `data/etfs/scripts/rivalfunds/enrichment_bloomberg.py` and deploy only at site Z.

## The cell (proposed id RIV-xe-1)

1. **Trading-day gate** (analysis 2.3). The vehicle's enrichment leg runs on TRADING days only, read from
   `lib/trading_calendar.py` (`is_trading_day`). On a non-trading day it prints ONE line beginning `SKIP:` and exits 0, so the
   vehicle's exit line reads a skip and never `97` or `95`. Measured cause: 2026-10-10 (a Saturday) exited 97 because the
   MON-FRI daily Lambda had not built G1 for the previous trading day before the leg looked; 2026-10-11 (a Sunday) exited 95 on
   a signed-out Terminal. How `round28/tw1_j1_read.py` classifies a `SKIP:` run (it keys on a STEP line and an exit code other than 97) is NOT read here: set it, with a check, in the issuance that cuts this cell.
2. **Queue-state reader** (row D1-S2; CTO ruling at round 22 ADDENDUM 7, XA-20261009T033809Z-8c1a condition 1). Before each
   history-owed draw the leg reads the standing request's `state` at the builder address
   `s3://opal-data-assets/bloomberg/global/silver/request_state/request=ETFS_RIVALS-HISTORY-OWED-DAILY/state.json`
   (`lib.opal_naming.address("bloomberg","global","silver","request_state","request=ETFS_RIVALS-HISTORY-OWED-DAILY","state.json")`;
   recorded in `org/missions/D8/MDPF/MDPF_DEMQUE/requests/ETFS_RIVALS-HISTORY-OWED-DAILY.json`, writer DQ-t-16 complete). Three
   arms, the CTO's: `active` draws as today; `paused` (or `stopped`) draws ZERO rows and logs one line naming the state; an
   unreadable or absent state draws ZERO and logs that it could not be read (fails closed, never draws on a failed read).
3. **Checks to write and dry-run before the cut:** the gate's arms (a trading day runs the leg; a Saturday, a Sunday and an NYSE
   holiday print `SKIP:` and exit 0; the calendar source is `lib/trading_calendar.py`, never a typed date list) and the reader's
   three arms with an injected state reader (no S3 in the check).
4. **Bounds:** the switch (`RIVALFUNDS_HISTORY_OWED`) is NOT set by this cell; the switch-on is its own act under the pair.
   No Bloomberg call in any check.

## Deploy and pair

A site-Z producer change: `1.0.0_SA_CTO~Z`'s never-widen half, applied by `0.7.0_AE_CloudOps~ZV` (a site-bound act, via a
crossbox ORDER; the manager commits the record, MSTR lane). Not under Andrew's no-modify order (that covers
`integrations/bloomberg/pipeline/` and the vehicle scripts; this file is in `data/etfs/scripts/rivalfunds/`).

## Also staged for the same window

C-S85's clock advance (the CVO's compile carries it; it needs site Z's file, one writer).

## Window class (Andrew-direct 2026-10-13, CTO msg 4886, ADDENDUM 1 to `ANDREW_DIRECT_20261013_141xZ_BACKFILL_FLOOR_2012_AND_EARLIEST_CLIENT_RECORD.md`)

The standing request `ETFS_RIVALS-HISTORY-OWED-DAILY` is re-declared NON-CLIENT with a 365-day window by the CTO and Q1 (re-priced at the queue before its
next draw); a request that asks beyond its class window is refused at the queue. The producer already asks 365 days back from the page day
(`history_owed.owed(s, day, window_days=365)`, `enrichment_bloomberg.py` reads it through `_history_owed`), so this cell changes no window. Its checks
carry one arm: the owed set's earliest date is not before `page_day - 365` (the 2012-01-01 floor binds both classes).
