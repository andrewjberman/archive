# BP-c-2 -- the replay re-run on amendment R1.2, read-only (round 3)

Worker `0.9.0_WK_ADVI_BDPRCE~14`, cell BP-c-2. Record: `REPLAY2.json`. List: `BEFORE_AFTER2.csv` (1,664 lines, 323,604 bytes, sha256 `bf2e3ca3b453e5f816b2ea3b9beed318d547f4fe47392ca62367903b2ef76c6f`). Estimated rows: `ESTIMATED_ROWS2.csv` (18,420 lines, 2.5 MB, sha256 `1ca973b381c1c8a61a55bb3c244cad23c2f5d1a770a0096eaac296029ff1db82`). Partition evidence: `PARTITIONS2.csv`. Scripts: `verify_partitions.py`, `replay_r1_r3.py` (adapted from round 2's `replay_r1.py`; round 2's files are untouched). The module is `data/black_diamond/scripts/silver/bd_price_rule.py`, read and not changed, AMENDMENT R1.2. Claim: measured. No S3 write, no producer run, no served object or product file changed. Read at `2026-10-14T03:20:54Z`.

## The window and the served set

Window 2026-09-16..2026-10-13: 20 weekday dates. The canonical file was re-read. It is not the object round 2 read: ETag `8eaa29e3...` (round 2 `0ba9bd51...`), last modified 2026-10-14T00:13:47Z (round 2: 2026-10-13T12:48:05Z). It holds 1,664 `transaction_observed` rows, not 1,657. The seven added rows are six `CASH AND MARGIN  INTEREST` rows at price 1.0 (2026-09-24, 09-25, 09-29, 09-30, 10-06, 10-12) and `GLOBAL X S&P 500 TAIL RISK ETF` on 2026-10-12. No round-2 row is missing, and none of the 1,657 common prices differs. The list covers the 1,664 rows.

## What changed from round 2, and why

R1.2 is the rule the CTO ruled and BP-c-1 built. Four things move the numbers:

1. Par-quoted bonds are decided per row. A Fixed Income row whose price is within 1 percent of 100 times its market value per unit is divided by 100. Within 1 percent of 1 it is left alone. Any other ratio is withheld. All eight round-2 `scale_100x` rows now read UNCHANGED.
2. Reinvestment buys count as trades. The 77 round-2 carry-forwards sourced from reinvestment rows now price from those buys: 74 UNCHANGED, 2 CHANGED, 1 NOT_RECOMPUTABLE.
3. Transfer In does not. Of the 153 round-2 carry-forwards sourced from Transfer In, 150 remain carry-forwards, each with its last observation date. Three are refused because their last trade date holds a withheld row (see limits).
4. Every partition is keyed on `trade_date`, so late-landed trades are seen. In the 2026 partitions 226,319 rows land after their trade date, 58,226 of them by more than a day. Round 2 read only t and t+1.

## Result

| class | rows |
|---|---|
| UNCHANGED | 731 |
| CHANGED | 585 |
| NOW_CARRY_FORWARD | 160 |
| NOT_RECOMPUTABLE | 188 |
| total = served rows | 1,664 |

Prices that move: 740 (585 changed and 155 carry-forwards whose value differs). The grader's `moved` field is 745, because it also counts five carry-forwards that equal the served value. Of the 740, 662 move up and 78 down. The median absolute move of a changed row is 0.0021. The 90th percentile of the percentage move is 4.2 percent.

Round-2 transitions: CHANGED stays CHANGED 519 times, becomes UNCHANGED 13 times, NOT_RECOMPUTABLE 7 times. NOT_RECOMPUTABLE becomes CHANGED 22, UNCHANGED 16, carry-forward 4, and stays 170. Carry-forward becomes CHANGED 43, UNCHANGED 81, NOT_RECOMPUTABLE 5, and stays a carry 156.

The three largest movers by absolute change:

1. WATSCO INC COM, 2026-09-17: 305.36 becomes 432.39 (carry from 2026-04-28; the served value came from Transfer In rows).
2. MORGAN STANLEY FIN LLC 0% 05/03/2029, 2026-10-05: 115.995 becomes 1.0 (carry from 2025-05-28). This is a unit question, not a price move. The only trade is a Buy at 100 for 250,000 units, which R1.2 reads as par, so 1.0 per unit. The served series for this bond is in per-100 units. See the unit row filed with the surprise channel.
3. ASML HLDG NV N Y REGISTRY SHS, 2026-09-22: 1,741.19 becomes 1,650.84 (carry from 2026-09-18).

## Par-quoted rows and the withheld band

Par-quoted rows: 8 of 8 UNCHANGED.

Withheld: the rule withholds 442 Fixed Income trade rows over the window, across 25 assets (all assets, served or not). No non-Fixed-Income row is withheld. Ratios run from 0.9145 to 1.142. By asset, 8 sit within 2 percent of 1 (343 trade rows, mostly VANGUARD INTERMEDIATE-TERM BOND ETF and JANUS HENDERSON AAA CLO ETF), 1 sits at 2 to 5 percent (4 rows), 15 sit at 5 to 10 percent (92 rows), 1 is beyond 10 percent (3 rows).

Served prices touched: 12 served rows are NOT_RECOMPUTABLE with reason `ratio_unrecognised` (9 directly, 3 through a refused carry-forward). Fourteen of the 25 assets are in the served set; nine of those touch 11 served rows. The twelfth served row, T. ROWE PRICE US TREASURY INTERM IDX on 2026-10-09, is refused by a withheld trade dated before the window, which the window census does not list. Interpolated rows touched: 127 (one direct, 126 through a refused carry-forward). The table's last column counts window withheld trades only, so its entries sum to 98 of the 127; the other 29 refusals come from withheld trades dated before the window.

Nine funds on 2026-10-06 read ratios between 1.0925 and 1.0931. Their trade prices and market value per unit disagree by the same amount on one day. That suggests the market-value field for that date, not the trade, as the source. This is a reading, not a finding.

| asset | withheld trade rows | printed ratio(s) | window date | served prices touched | interpolated rows refused |
|---|---|---|---|---|---|
| VANGUARD INTERMEDIATE-TERM BOND ETF | 236 | 1.01135 | 2026-10-05 | 0 | 0 |
| JANUS HENDERSON AAA CLO ETF | 84 | 1.0102 | 2026-10-06 | 0 | 0 |
| VANGUARD SHORT-TERM CORPORATE BOND ETF | 19 | 0.92532, 0.987972 | 2026-10-05 | 0 | 0 |
| STATE STREET SPDR BLOOMBERG 1-3 MONTH T-BILL ETF | 14 | 0.9145, 1.01248 | 2026-10-06 | 0 | 0 |
| COLUMBIA INTERMEDIATE DUR MUNI BD INST | 11 | 1.09268, 1.09295 | 2026-10-06 | 1 | 7 |
| PIMCO INCOME I2 | 9 | 1.09261 | 2026-10-06 | 0 | 0 |
| VANGUARD TOTAL INTERNATIONAL BOND ETF | 8 | 1.01443 | 2026-10-05 | 0 | 0 |
| FIDELITY ADVISOR INVESTMENT GR BD Z | 5 | 1.09286 | 2026-10-06 | 1 | 7 |
| JPMORGAN CORE BOND R6 | 5 | 1.09299 | 2026-10-06 | 1 | 7 |
| MFS HIGH INCOME R6 | 5 | 1.09291 | 2026-10-06 | 1 | 7 |
| PGIM HIGH YIELD R6 | 5 | 1.09326 | 2026-09-24 | 0 | 0 |
| VANGUARD SHORT-TERM INVESTMENT-GRADE INV | 5 | 1.08438 | 2026-09-16 | 0 | 0 |
| JHANCOCK BOND R6 | 4 | 1.0113 | 2026-10-06 | 0 | 0 |
| MFS TOTAL RETURN BOND R6 | 4 | 1.01119 | 2026-10-06 | 3 | 19 |
| POLEN HIGH INCOME ETF | 4 | 1.053 | 2026-10-01 | 0 | 0 |
| POLEN OPPORTUNISTIC HIGH YIELD - INS | 4 | 1.04333 | 2026-10-08 | 0 | 0 |
| FIDELITY INVESTMENT GRADE BOND | 3 | 1.01149 | 2026-10-01 | 1 | 12 |
| JPMORGAN CORE BOND I | 3 | 0.982 | 2026-09-28 | 1 | 27 |
| PGIM TOTAL RETURN BOND Z | 3 | 1.142 | 2026-09-30 | 0 | 0 |
| VANGUARD ULTRA SHORT-TERM TX-EX ADM | 3 | 1.09259 | 2026-10-06 | 0 | 0 |
| PIMCO INCOME INSTL | 2 | 1.09292 | 2026-10-06 | 0 | 0 |
| PIMCO INTERNATIONAL BOND (USD-HDG) INSTL | 2 | 1.09266 | 2026-10-06 | 1 | 7 |
| PIMCO SHORT ASSET INVESTMENT INSTL | 2 | 1.09307 | 2026-10-06 | 0 | 0 |
| AMERICAN FUNDS BOND FUND OF AMER A | 1 | 1.073 | 2026-09-30 | 1 | 5 |
| FIDELITY INTERM TRS BD INDEX | 1 | 1.01049 | 2026-10-12 | 0 | 2 |

## Named before and after

- BLACKROCK INC COM, 2026-09-22: served 1,073.16, now 1,074.9259 (four distinct trades, Dividend Reinvestment). Round 2 carried 1,078.04.
- EXXONMOBIL HOLDINGS CORP COM SHS, 2026-10-09: served 168.94 (Transfer In), now carry 168.29 from 2026-10-08.
- MIAMI-DADE CNTY FLA EDL FACS A 5.25% 04/01/2031, 2026-10-09: 1.0419 UNCHANGED (executed 104.19 scaled).
- CITIGROUP INC 5.3% 07/22/2032, 2026-09-22: 0.97021 UNCHANGED.
- MISSOURI ST HEALTH & EDL FACS 5% 05/01/2033, 2026-10-09: 1.0401 UNCHANGED.
- The five null-coupon banks on 2026-09-16 (BANK MIDWEST, PNC, STATE BK INDIA, TRUIST, WELLS FARGO) all UNCHANGED.

Round 1's 64 UNEXPLAINED rows now read: 60 CHANGED, 4 UNCHANGED. The 19 that recomputed to 1.0 read: 17 CHANGED, 2 UNCHANGED. Each row carries `round1_class` and `round1_recomputed` in `BEFORE_AFTER2.csv`.

## The interpolated rows

Scope: the 18,420 canonical `linear_interpolation` rows in the window on the served assets (887 assets), the scope round 2 counted. Their fates sum to the count:

- `trade_price`: 29 (a trade that day).
- `last_traded_date`: 15,997, each with its observation date. Of these, 214 carry a value from a par-scaled trade, a per-unit value where neighbouring interpolated values are per 100. 775 are on 2026-10-13, a day with no partition in the store.
- `unresolved`: 2,394 (2,267 with no earlier trade in the history, 127 refused because the last trade date holds a withheld row).

## The lookback and its limits

Mode `trade_date_all_partitions`. All 1,928 dated partitions were checked against S3 head-object ContentLength and ETag before use. 1,926 verified by MD5; 2 are multipart uploads and verified by size only. Three cached partitions (2026-10-02, 10-08, 10-11) had been rewritten in S3 after round 2 read them, and were fetched again. One partition (2026-10-14) was absent from the cache and was fetched. The store holds 1,980 trade dates from 2020-03-06 to 2026-10-14.

Limits:

- 2026-10-13 has no partition in the store. Trades dated that day, if they land later, are not seen. Its 886 interpolated rows on the served assets take the last trade before it: 775 carry a price, 111 are unresolved.
- The 2026-10-14 partition holds 2,921 rows, 2,804 of them dated 2026-10-12. Leaving it out changes one served row, GLOBAL X S&P 500 TAIL RISK ETF on 10-12 (29.349 becomes not recomputable). The canonical file appears to have been built with that partition, so it is kept.
- The other 221,070 window interpolated rows (on about 10,250 assets with no served row) are not fated here (scope above). Round 2 counted the served scope too.
- A trade dated on a day with no partition, which never landed in a later partition, is not in the store. The store cannot show it.

## Determinism

Two separate processes over the same bytes produced `BEFORE_AFTER2.csv` with md5 `4899a1e331ff8e3e37a5153cbb24e345`. The in-process second pass is equal. For 20 changed rows, the result for the date from trades on or before that date equals the full result, and the trade ids are all dated that day (20 of 20).

## What stays unknown

- Whether a carry-forward should refuse a withheld last trade date (3 served rows, 126 interpolated) or carry the last kept price. R1.2 is silent. This list refuses; the CTO rules.
- The unit of a carried par-quoted price when the served series for that asset is per 100 (the MORGAN STANLEY row).
- Whether the market-value field on 2026-10-06 is the cause of the withheld cluster.
- The dollar effect on holdings and downstream readers. That is `BP-c-3`'s join and is not measured here.
