# PORTING_VERDICT_RECORD -- ADVI_COTBKF CB-ce-2 (round 83), 0.9.0_WK_ADVI_COTBKF~165

Machine record: `PORTING_VERDICT_RECORD.json` (this folder). COO half, DRAFT and unsigned: `NEVER_WIDEN_R83_PORTING_VERDICT_COO_HALF.md`.

**Headline.** The live Yahoo store index has no `porting_verdict` column, so every Yahoo-sourced figure row reads UNVERIFIED and every
other row reads NOT_YAHOO. Nothing was applied, minted, served, uploaded or sent.

| table | rows | wide rule: UNVERIFIED | narrow rule: UNVERIFIED | existing values changed |
|---|---|---|---|---|
| account_day_value (holding-days) | 21,102,041 | 3,709,042 | 3,648,401 | 0 |
| daily_returns (account-days) | 1,691,729 | 669,262 | 658,642 | 0 |
| month_grades (account-months) | 82,593 | 33,217 | 32,232 | 0 on the 9 Month-derived columns, both rules; the 10 Year/InceptionToDate-derived columns NOT_MEASURED (S4) |

- **Wide** = yahoo_finance and linear_interpolation (ruled 10-13). **Narrow** = yahoo_finance.
- **Origin of a price, today.** The per-day file carries the store id only. The source label is read by `pc.read_store` and dropped in
  `security_day_prices` (`commonwealth_daily_valuation.py` HEAD 403-406). The worktree change carries it through.
- **Changed code.** `commonwealth_price_need.py` (verdict reader, three branches, fail-closed), `commonwealth_daily_valuation.py`
  (source per security-day, yahoo_holdings), `commonwealth_fwd3_serve.py` (porting_verdict appended last to the three tables).
- **Tests.** 61 passed, 0 failed across the four files named by the order.
- **Surprise rows.** `ADVI_COTBKF-D2-W165-S1` (origin dropped; rebuilt from caches), `S2` (BLOCKING: month_grades existing values not
  re-derived under the first grant; narrowed by AMENDMENT 1), `S3` (split-factor price differences not replayed offline), `S4` (BLOCKING:
  the granted read covers the Month partition only; the Year and InceptionToDate-derived month_grades columns are NOT measured).
- **Not established.** Branch counts with a verdicts column (no file exists); the ten Year/InceptionToDate-derived month_grades columns; the split replay.
