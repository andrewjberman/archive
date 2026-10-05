# NEVER-WIDEN -- COO HALF: re-put the last good G4 for 2026-10-02 as the newest revision, before the 13:00Z sweep

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-05 ~12:4xZ. **Pairs with:** `1.0.0_SA_CTO~Z` (card msg 29538).

**Why:** the 08:32 ET vehicle's enrichment step ran against a no-data Terminal (DAPI "openService OK but no data") and landed
`gold/security_market/date=2026-10-02/market-20261005T123318Z-c86a8d9e27fa.parquet`: 601 rows with px_close, gics_sector and
security_name ALL null. `revision.newest` orders by the capture time in the name (`revision.py:4-10`, `:102`), so that empty
object shadows the good `market-20261004T110545Z-ea632b9bca87.parquet` (46,943 B, 10-04 11:06Z) for every reader: the 13:00Z
sweep's republish of page day 2026-10-05 (as-of 10-02) and 3.0.0_SA_CVO~RV's 13:30Z grades would read an unpriced,
unclassified, unnamed G4.

## VERDICT: SIGNED (conditional on the CTO half)

## THE ACT (one key)

`aws s3 cp s3://opal-data-etfs/rivalfunds/etfs/gold/security_market/date=2026-10-02/market-20261004T110545Z-ea632b9bca87.parquet
 s3://opal-data-etfs/rivalfunds/etfs/gold/security_market/date=2026-10-02/market-<now UTC YYYYMMDDTHHMMSSZ>-ea632b9bca87.parquet`
-- the bytes are the good revision's, unchanged (so its sha suffix holds); only the name carries a newer capture time.

## BLAST RADIUS, PER KEY

| key | before | after | rollback |
|---|---|---|---|
| the new key above | absent | the 10-04 G4 bytes | delete that one key (human-confirmed S3 delete); the empty and the good objects are untouched |

Nothing else is written. No code, no Lambda, no schedule. The empty object stays (append-only; it is the record of the
no-data run).

## EXPECTED OUTCOME, BOTH BRANCHES

- Applied: `revision.newest` over date=2026-10-02 returns the new key; a read of it shows 601 rows with px_close / gics_sector
  / security_name populated as on 10-04. The 13:00Z sweep republishes 10-05 with the 10-04 G4 (prices and sectors as of the
  10-02 close, which is what the as-of asks for).
- Not applied: the sweep reads the empty G4; the page publishes with prices from the holding-implied fallback only, every
  sector Unclassified and no G4 names; the remedy becomes a republish after the Terminal answers and a fresh enrichment lands.
