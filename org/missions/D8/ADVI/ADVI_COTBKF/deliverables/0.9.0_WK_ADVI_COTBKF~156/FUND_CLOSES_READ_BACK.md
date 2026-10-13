# CB-cb-2 -- the 15 funds' closes as dell1 landed them, read back (round 80, 0.9.0_WK_ADVI_COTBKF~156)

Generated 2026-10-13T13:00Z. Counts, tickers, dates, prices and ratios only; no account identifier, amount, quantity or balance. Record: `FUND_CLOSES_READ_BACK.json`; per fund: `FUND_CLOSES_READ_BACK.csv`. Nothing was re-priced, re-minted, served or written; remote reads are read-only.

**Headline.** Dell1's lander drew 7 of the 15 funds (PCBIX, SGIIX, GFFFX, FOCPX, FCNTX, DISVX, DFLVX). The 8 rejected funds (VEIRX, ABNFX, PRILX, BALCX, AGTHX, NFFFX, MEIIX, VGHAX) have no object and are `not_landed`. Of the 20,718 held trading days, 5,730 carry a non-null as-traded close (27.7 percent) and 14,988 are absent. PCBIX, SGIIX, DISVX and DFLVX are present on every held day; GFFFX, FOCPX and FCNTX hold only 2026-04-14 to 2026-10-09 (122, 56 and 85 present). Every fund has trade units on the round-76 basis (5 to 1,596 each), so the premise of 14 funds with trades is not what the round-76 record shows (see not_established). On dell1's column the round-76 test classes 4 funds passes (PCBIX, SGIIX, DISVX, DFLVX; 3,975 of 4,324 read units within 1 percent), FCNTX too_few (1 unit), GFFFX and FOCPX no_trade_row (every trade pre-dates 2026-04-14), and 8 not_landed; none fails. Round 76 classed all 15 fails on the served close.

## Where the closes are (as named)

`price_store.s3_root()` returns `s3://opal-data-assets/yahoo/global/silver/price_history`. One object set per CUSIP under `cusip=<CUSIP>/`; `index/index.parquet` is the store index (326 CUSIPs; the 7 landed funds are in it, the 8 rejected are not). The order's `s3://` prefix is already in the return value, so it was not added twice.

## Held trading days present, per fund

| ticker | in store | rows | first | last | held trading days | present | absent |
|---|---|---|---|---|---|---|---|
| VEIRX | no | 0 | | | 1177 | 0 | 1177 |
| PCBIX | yes | 2331 | 2017-07-05 | 2026-10-12 | 1283 | 1283 | 0 |
| ABNFX | no | 0 | | | 1520 | 0 | 1520 |
| SGIIX | yes | 3347 | 2013-06-21 | 2026-10-12 | 1535 | 1535 | 0 |
| GFFFX | yes | 125 | 2026-04-14 | 2026-10-09 | 1571 | 122 | 1449 |
| FOCPX | yes | 125 | 2026-04-14 | 2026-10-09 | 1499 | 56 | 1443 |
| FCNTX | yes | 125 | 2026-04-14 | 2026-10-09 | 1528 | 85 | 1443 |
| PRILX | no | 0 | | | 1121 | 0 | 1121 |
| BALCX | no | 0 | | | 1036 | 0 | 1036 |
| AGTHX | no | 0 | | | 1563 | 0 | 1563 |
| DISVX | yes | 1498 | 2020-07-06 | 2026-06-22 | 1242 | 1242 | 0 |
| DFLVX | yes | 1498 | 2020-07-06 | 2026-06-22 | 1407 | 1407 | 0 |
| NFFFX | no | 0 | | | 1227 | 0 | 1227 |
| MEIIX | no | 0 | | | 1568 | 0 | 1568 |
| VGHAX | no | 0 | | | 1441 | 0 | 1441 |
| **total** | **7** | | | | **20718** | **5730** | **14988** |

Missing ranges per fund are in `by_fund[].missing_ranges` of the JSON. The held-day counts reproduce round 80's `held_covered_by_cache` exactly, fund by fund.

## The test (round 76, unchanged)

Quoted in full as `test` in the JSON (`FUNDS_BY_TRADES.json` `rule.text`, written 2026-10-11T23:07:58Z). Minimum 5 decisive units on 3 days; pass line 0.10 fail share; fails above 0.50; 180-day guard; charge-sized excuse at 34.15 dollars. The instrument was run on round 76's population first: all 15 funds reproduce round 76's per-fund unit counts, decisive, failing, unresolved, distinct days and class (0 mismatches).

## Trades, on dell1's column beside round 76's store class

| ticker | read units (dell1) | within 1 percent | class from dell1 | class from store, round 76 |
|---|---|---|---|---|
| PCBIX | 3814 | 3469 | passes | fails |
| SGIIX | 493 | 489 | passes | fails |
| DISVX | 8 | 8 | passes | fails |
| DFLVX | 8 | 8 | passes | fails |
| FCNTX | 1 | 1 | too_few | fails |
| GFFFX | 0 | 0 | no_trade_row | fails |
| FOCPX | 0 | 0 | no_trade_row | fails |
| eight not landed | 0 | 0 | not_landed | fails |

## Splits

Funds with a split inside the back-fill: 0 of 15. The split-undone property rests on dell1's word alone for these funds: on every row where both fields are present, `close_served` equals `as_traded_close`, and the two vendor split events in the landed objects (FOCPX 2018-05-11 and FCNTX 2018-08-10, ratio 10.0) fall before every held day and before the objects' first rows. The split arm was not tested and is not claimed as passed.

## Not established

See `not_established` in the JSON: the 14-versus-15 premise and VGHAX (round 80 calls it too_few on the cache close; round 76 on the store close, 5 of 5 fail); the fallback NYSE calendar (`pandas_market_calendars` absent); presence is a read of dell1's object, not a check of its prices; why three objects start on 2026-04-14; dell1's `close_served` differs from round 76's served close on most common dates for the four passing funds; no advisor or firm filter was applied or inspected on the custodian cache.
