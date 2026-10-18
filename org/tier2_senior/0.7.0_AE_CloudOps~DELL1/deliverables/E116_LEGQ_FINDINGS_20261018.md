# TO-SC-e116b leg Q findings (0.7.0_AE_CloudOps~DELL1, 2026-10-18 ~06:48Z)

Claim words: `measured` = read this session.

## What ran (measured)
- Runner i-01003b035d2988dfb started 06:47:44Z, SSM online 06:48:13Z, FIRST command `systemctl stop gold-layer-runner` (CommandId eeaec39d-3507-4b09-906e-57ba777401cd, Success, no gold process, no boot-chain step started).
- SECOND command (CommandId 75cf5f38-62e1-4e32-9824-1942a7340bcd): `BD_PLATINUM_MODE=canonical bash /tmp/gold_dispatch.sh --dry-run --single E_18`, script pulled from S3 (box md5 of gold_dispatch.sh 165933f6, of E_18 197eac28), NO --upload. SINGLE-RC=0, wall 4.5s, 0 ERROR lines. The output header carries no `flags: --upload` line (the plan form, CTO msg 7449).
- `etf-classifications` before vs after the single: 11375 items both; 13 seeded present, 9 held-out absent, first 200 sorted keys with `last_updated` identical (E116_LEGQ_TABLE_BEFORE/AFTER_20261018.json, and equal to leg P's).

## The display (measured)
`Held out by the resolution table (real ticker absent from the canonical table): 14` and 14 lines `<ticker>  <name>  -- held out`: the nine named tickers (BALCX, CIMAX, DODBX, FSNQX, HBLFX, JBAWX, KAMIX, PCEF, TRRNX) plus FPE, TRRJX, VTTVX, WTM, XPMIX. `Scheduled-classification candidates: 0`, `Scheduled rows written / refused: 0 / 0`, `Truly unresolved: 109`.

## One figure differs from the order's text
The order expected `Already resolved (in resolution table): 9` "as in the 2026-10-17 23:00Z fire". The single printed 14. Cause, measured: the 23:00Z fire's chain log (gold/logs/chain_full_20261017_230043.log, VersionId t6i.x4cy3PVBMuoCDf5PVCfdMeAxCmCF) loaded `gold/holdings_lots/2026-10-09.parquet` (Already resolved 9, candidates 0, unresolved 72); today's single loaded `gold/holdings_lots/2026-10-16.parquet`. Controlled A/B, same file, plan form, reads only, run locally (`e116_ab_local.py`): the BASE E_18 (md5 f5c03ee6) prints Already resolved 14, candidates 0, written/refused 0/0, unresolved 109; the NEW file prints the same four figures plus the held-out block. So the 14 comes from the input, not the ship. The request's own "Both branches" paragraph covers a block that lists more than nine names because holdings changed. Issuer's grade.

## Runner
The wrapper's own shutdown (SHUTDOWN_ARMED, 2 minutes) returned the instance to stopped (see the ledger).
