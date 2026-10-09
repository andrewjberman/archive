# 49 Financial tie-out against Black Diamond -- round 4, like day sets

**Cell:** `IRPT_DASHBD.TO-DB-b-10` | **By:** `0.9.0_WK_IRPT_DASHBD~1`, 2026-10-02 | **Word:** @0abef798f7 card 4
**Records:** `TIEOUT_49F_BLACKDIAMOND_R4.json`, `BD_LIKEDAY_PULL_R4.json`, `BD_LIKEDAY_PLAN_R4.json` (the reviewed request bodies), `RAW_BD_PERIOD_<account>.sanitised.json.gz` (the full response, `accountName` replaced; sha256 of the unsanitised bytes in the pull record notes below), script `bd_likeday_pull_r4.py`
**Vendor calls:** 3 performancePeriod requests (one per mapped account), 0 transport retries, 1 session-token mint (see row IRPT_DASHBD-W1-S11), 0 performanceSeries.
**Mapped:** acct#e7ab8585, 0076459710, 0084073310. **Unmapped:** 0035940058 and 0091939812 (no `bd_internal_id` in the roster, status `pending_resolution`; not guessed).

## The table

| account | start | end | Opal linked days | BD daysHeld | like days | Opal TWR | BD TWR | abs_diff |
|---|---|---|---|---|---|---|---|---|
| acct#e7ab8585 | 2026-03-17 | 2026-03-26 | 8 | 8 | yes | -2.6935% | -2.5221% | 0.1714% |
| acct#e7ab8585 | 2026-04-09 | 2026-04-30 | 16 | 16 | yes | -2.8356% | -3.2912% | 0.4555% |
| acct#e7ab8585 | 2026-05-08 | 2026-06-23 | 31 | 31 | yes | -7.1203% | -7.1359% | 0.0157% |
| acct#e7ab8585 | 2026-06-25 | 2026-07-06 | 7 | 7 | yes | +3.4935% | +2.2806% | 1.2130% |
| acct#e7ab8585 | 2026-07-08 | 2026-08-04 | 20 | 20 | yes | +1.1633% | +1.0072% | 0.1561% |
| acct#e7ab8585 | 2026-08-06 | 2026-08-19 | 10 | 10 | yes | +0.4949% | +0.4991% | 0.0042% |
| acct#e7ab8585 | 2026-08-21 | 2026-10-01 | 29 | 29 | yes | -10.0257% | -10.2211% | 0.1954% |
| 0076459710 | 2026-07-09 | 2026-08-04 | 19 | 19 | yes | +5.0098% | +5.0098% | 0.0000% |
| 0076459710 | 2026-08-11 | 2026-08-19 | 7 | 7 | yes | +3.9440% | +4.2747% | 0.3307% |
| 0076459710 | 2026-08-21 | 2026-09-09 | 13 | 13 | yes | +1.7933% | +1.7858% | 0.0076% |
| 0076459710 | 2026-09-16 | 2026-10-01 | 12 | 12 | yes | -6.7067% | -6.5769% | 0.1297% |
| 0084073310 | 2026-03-20 | 2026-08-04 | 94 | 94 | yes | +24.2267% | +23.9661% | 0.2606% |
| 0084073310 | 2026-08-06 | 2026-08-19 | 10 | 10 | yes | +1.8714% | +1.9838% | 0.1124% |
| 0084073310 | 2026-08-21 | 2026-10-01 | 29 | 29 | yes | +6.1779% | +6.8856% | 0.7078% |

**Summary:** 14 pairs, 14 like-day pairs (coverage 14 of 14); over the like-day pairs the median abs_diff is 0.1637% and the max is 1.2130%.

## The paragraph

Each row is one maximal run of consecutive NYSE trading days (`lib/trading_calendar.py`) with a non-null `total_return_daily` in the served reporting gold, at least 5 days long; `opal_twr` is the geometric link of those daily returns. BD was asked for its time-weighted return (Cumulative, net of fees) over exactly those ranges, one request per account. On all 14 pairs BD's `daysHeld` equals Opal's linked-day count, so every pair is a like-day pair and no pair is left out of the median or the max. This record states differences between two series over equal day counts; it does not say which series is right on any row.

Full-response sha256 (unsanitised bytes, first 16 hex): acct#e7ab8585 `9cacaf85e9a483b8`; 0076459710 `a6276efe2c043d7a`; 0084073310 `6c4bff2f216376f8`.
