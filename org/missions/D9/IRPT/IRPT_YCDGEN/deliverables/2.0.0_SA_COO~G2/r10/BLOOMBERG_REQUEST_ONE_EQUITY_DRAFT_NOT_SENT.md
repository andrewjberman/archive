# IRPT_YCDGEN round 10, cell YCD-e-10 -- the data request, WRITTEN and NOT SENT

**By:** `2.0.0_SA_COO~G2`, 2026-10-11, after reading `integrations/bloomberg/READ_HERE.md` in full. The draft is
`BLOOMBERG_REQUEST_ONE_EQUITY_DRAFT_NOT_SENT.json` beside this file, in the key set the demand queue's request files use
(`org/missions/D8/MDPF/MDPF_DEMQUE/requests/`, 9 request files read for the shape). It is NOT in that folder. Nothing has been
asked of the queue, its producer or the Terminal.

## What it asks, when it is sent

One security, `MPC US Equity` (CUSIP 56585A102 by Cottonwood's transactions cache, unconfirmed against Bloomberg), two reference
fields, `CNTRY_OF_DOMICILE` and `GICS_SECTOR_NAME`: 2 cells. Tier 2 (current clients) by Andrew's priority order of 2026-10-08.

## Why one symbol

`1.0.0_SA_CTO~DELL2` msgs 4502 and 4506. The one eligible Cottonwood account of six or more positions reads 76.85% covered by
value today and 91.29% once this one equity has a store row; the other 13 symbols of the sized list are funds and cash.

## What the draft cannot settle

- **Where the answer lands.** A reference answer does not reach the resident. The Overview reads the daily characteristics
  parquet, written for the daily leg's own universe. For the row to exist every day the security joins that universe: an edit
  to `etf_daily_pull.py` at site Z, which READ_HERE.md section 3 says IS a deploy, and which moves served data. Round 11, its
  own pair.
- **Authority.** None yet. The CTO ruled what the request is; nobody has said send.

## What I read in READ_HERE.md that changed this round

Section 4: on a fund ticker the source serves `HB_INDUSTRY_SECTOR_ALLOCATION` (sector weights) and `HB_GEO_CNTRY_ALLOC`, with no
BQL, current-day only, no backfill; `etf_constituents_pull.py:70-71` already pulls both as `sector_allocation` and
`geo_allocation`. My round-10 item 2 said the source gives a fund no sector. That was a reading of the store's columns, not of
the source, and I corrected it to the CTO (msg 4506 withdraws the ruling that rested on it).
