# THREE_EQUITIES -- round 80 CB-cb-1 (row ADVI_COTBKF-D2-W152-S1)

Worker: 0.9.0_WK_ADVI_COTBKF~155. Record: `THREE_EQUITIES.json` (same folder). No code, config or served copy changed.

## Same-hour clause (first)

APH (CUSIP 032095101) is held on 48 SERVED minted days (2025-02-11 to 2025-04-21; 1 account; 48 account-days).
The served close equals the build on every one of them, and the build is 0.5035 to 0.5048 of the store on those
days and 0.487 of the price paid on the nearest sale (65.2875 on 2025-04-22). It is not in the 47 early partitions.
Filed as row ADVI_COTBKF-D2-W155-S1 (BLOCKING, ARMED, disarm owner 2.0.0_SA_COO~C2).

## The five securities off 1.0 (last common day, build over store)

| ticker | kind | build/store | held days (minted) | held days (47 partitions) | served price |
|---|---|---|---|---|---|
| APH | Equity | 0.5000 | 48 | 0 | build |
| CTVA | Equity | 0.1500 | 400 | 0 | build |
| HON | Equity | 1.0488 | 3315 | 9 | minted: build; partitions: store |
| KLAC | Equity | 0.1000 | 191 | 0 | absent (no close or value) |
| SCCO | Equity | 0.9881 | 263 | 0 | absent (no close or value) |

Threshold 0.1 percent: 5 of 1263 off, 1258 within. Thresholds of 0.1 percent and 0.001 agree on the count.

## Price paid (custodian trades, amount over units)

- CTVA: four sales 2020-07 to 2026-02. Store is 0.948 to 0.990 of the price paid; build is 0.147 to 0.152 on every one. The store matches.
- APH: one sale 65.29 (2025-04-22). Store 0.967 of it on the nearest held day; build 0.487. The store matches.
- HON: five trades with both series. 2023-04-27 to 2025-02-12 (four): build 0.984 to 0.993, store 0.885 to 0.914. 2026-02-04: store 0.9986, build 1.0525. The price paid does not decide one side for all dates.
- KLAC and SCCO: the held days end (2020-05-28 and 2014-04-22) before any build or store row exists. No price-paid test on a held day.

## Steps and split dates

- No vendor split date is on disk. The cache files carry Date, Close, Adj Close only; the build split plan is not in `r34/after/`; the split store was not read (not in the grant). `vendor_splits` is empty for that reason.
- Build over store, every overlap day: no step equals a split ratio (none within 1 percent of 1/k or k for k = 2..50). The APH ratio is flat near 0.5 from 2021-01-08 to 2026-06-05, with no step at the 2024-06 window. CTVA falls from 0.1603 to 0.1500 through small steps. HON falls from 1.1726 to 1.0488 through about 22 steps of 0.5 percent. KLAC is flat near 0.1; SCCO is near 1.0 with small steps.

## Cause

`not_established` for all five. No step equals a split ratio, so no `double_scaling` is named and `widens_c_basis` is false.
The price paid puts the store on the correct side for CTVA and APH; it does not decide HON; KLAC and SCCO are untestable on a held day.

## Other rows

- ADVI_COTBKF-D2-W155-S2: split plan absent from `r34/after/`; no split events in the cache.
- ADVI_COTBKF-D2-W155-S3: minted copy (32 HON days, 3 accounts, build price) and 47 partitions (9 days, 2 accounts, store price) disagree in the window (ARMED, disarm owner 2.0.0_SA_COO~C2).
- ADVI_COTBKF-D2-W155-S4: build steps after the store's last day (APH 2026-09-04 0.5171; CTVA 2026-10-02 0.1535; KLAC 2026-09-04 1.0774).

## Reads made (remote)

1. `head-object` on `silver/prices/canonical_prices.parquet`, current version (returned VersionId 76.rgWIXYdLNsXSwrXvyuEmaEtfr9y98, ContentLength 97443387). One earlier `head-object` with the version id given without its `76.` prefix returned 400 Bad Request.
2. `get-object` on the same key at version 76.rgWIXYdLNsXSwrXvyuEmaEtfr9y98 into `.scratch/cb1/`. Byte length 97443387 = expected.
3. `get-object` on `gold/canonical/holdings/<date>.parquet` for 2026-04-22 to 2026-06-07 (47 objects; 2026-06-03 fetched twice in the first test). Read whole into `.scratch/cb1/parts/` (never committed); only rows whose asset_name matched the five names were used; no account id or value was printed.

No vendor call, no listing, no write, no delete.
