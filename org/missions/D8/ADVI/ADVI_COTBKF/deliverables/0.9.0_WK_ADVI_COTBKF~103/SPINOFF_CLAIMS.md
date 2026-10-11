# CB-bp-3 -- the four spin-off events against the custodian's price (round 68, 0.9.0_WK_ADVI_COTBKF~103)

Read-only measurement. No code, config or manifest changed; no vendor and no network call; local caches only. Record: `SPINOFF_CLAIMS.json`.

## 1. Which print is the custodian's, and when it exists
- **Taken as the custodian's print: `cottonwood-gold-canonical-holdings`, source `bd_snapshot`, 2026-06-08 .. 2026-10-06** (564,563 cached rows, one source value). It is the store the build's code names as the custodian mark on a held position (`commonwealth_price_census.py` STORES comment), and its price is the holdings snapshot's reported market value over units (`B_00.canonical_holdings._build_canonical_from_snapshot`), not a vendor close. Limit: the label and the docstring say BD-reported; that it equals the custodian's own number is the code's word.
- **Dates before each event: 0, 0, 0, 0.** The latest event is 2025-10-30; the store's first date is 2026-06-08.
- The silver canonical prices store (2020-06-30 .. 2026-06-09; yahoo_finance 1,386,986, linear_interpolation 749,242, transaction_observed 2,692 rows) is a Yahoo-sourced store (T2 of `build_canonical_prices_v2.py`), keyed by ticker; its raw points equal Yahoo's Adj Close times one constant per ticker. Not the custodian's; reported separately, decides nothing.
- A second candidate: the custodian-delivered trade price, |Amount|/|Quantity| over `by`/`sl` rows (the file has no price field). **Taken as a second candidate, not as the ruling's print** (reasons in the JSON). Its readings are given so the CTO can admit it without a re-measure.

## 2. Claims (the print taken as the custodian's)
| CUSIP | event | factor | held dates before | dates compared | claim |
|---|---|---|---|---|---|
| 00206R102 | 2022-04-11 | 1.324 | 2269 | 0 | UNAPPLIED_NO_HELD_DATE |
| 438516106 | 2025-10-30 | 1.061 | 3162 | 0 | UNAPPLIED_NO_HELD_DATE |
| 460146103 | 2021-10-01 | 1.056 | 2127 | 0 | UNAPPLIED_NO_HELD_DATE |
| 717081103 | 2020-11-17 | 1.054 | 1919 | 0 | UNAPPLIED_NO_HELD_DATE |

## 3. The second candidate (trade price), if admitted
WITHOUT = the served build's close (`r34/after/security_day_price`); WITH = that times the factor (`apply_splits` multiplies a close before the day by the ratio; the pbB1 table equals served x factor on every pre-event date).
| CUSIP | dates compared | WITHOUT: within 0.5% / 2%, median, worst | WITH: within 0.5% / 2%, median, worst | reading |
|---|---|---|---|---|
| 00206R102 | 16 (123 trade dates; 107 precede the price table) | 0 / 0, 0.7573, 0.7491 | 9 / 15, 1.0027, 1.0304 | APPLY |
| 438516106 | 4 | 0 / 4, 0.9880, 0.9842 | 0 / 0, 1.0483, 1.0532 | DO_NOT_APPLY (neither within 0.5%) |
| 460146103 | 4 | 0 / 0, 0.9470, 0.9440 | 4 / 4, 1.0000, 1.0033 | APPLY |
| 717081103 | 1 (one trade, 2020-08-03) | 0 / 0, 0.9445 | 1 / 1, 0.9956 | APPLY on one date |

The silver store's raw points, set beside both reconstructions, fall in no tolerance (WITHOUT median 1.35, 1.12, 1.24, 1.31): a different basis (Adj Close), so no use as a print.

## 4. What the price source is adjusted for
Split-adjusted, not dividend-adjusted (Close); the silver points are dividend-adjusted (Adj Close times a constant). Control: AAPL 4:1, AMZN 20:1, NVDA 4:1 + 10:1 -- Yahoo Close is continuous across the split, the served price before it is Close x the ratio, and served/trade medians are 0.991, 0.9992, 1.0022. For T, IP, PFE Yahoo Close before the event is already scaled down by about the factor (served/trade 0.7573, 0.9470, 0.9445); HON's is not (0.9880). What Yahoo adjusted at each spin-off is inferred, not read.

## 5. Not established
See `not_established` in the record. Notably: the round-67 "independent cottonwood step" (0.8132, 0.9400, 0.9524, 0.9654) equals Yahoo's step divided by the factor to four digits, i.e. the with-factor table's own step; it is not a measurement of the factor. Surprise rows ADVI_COTBKF-D2-W103-S1 and -S2.
