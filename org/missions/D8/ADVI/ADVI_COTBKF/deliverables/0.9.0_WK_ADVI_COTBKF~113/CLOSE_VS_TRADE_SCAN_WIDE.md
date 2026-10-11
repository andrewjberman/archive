# CB-br-3 -- the close-against-trade scan widened once (round 70, 0.9.0_WK_ADVI_COTBKF~113)

A read-only measurement: no code, test, config or manifest changed; no AWS or network call. Records: `CLOSE_VS_TRADE_SCAN_WIDE.json` (the named keys), `CLOSE_VS_TRADE_SCAN_WIDE.csv` (the 8 CONSTANT_SCALE and STEP securities), `CLOSE_VS_TRADE_SCAN_WIDE_DETAIL.json` (print-type evidence, pair origins, per-store counts).

**Headline.** 8 close series are mis-scaled (6 constant-scale and 2 step: the seven of round 69, all still classed, plus OIEJX, which rests on 3 pairs over 17 days, 2 of them reinvestment prints) -- and that count is a floor: 334 compared securities are still too few to class (209 have a single pair), 44 of the thin ones still carry a pair more than 10 percent off, and 1,700 traded securities have no close in the table at all (1,693 of them held, 974,014 account-days resting on them, every one NOT_MEASURABLE).

## 1. Round 69 reproduced

The round-69 script re-run on the same inputs: 720 securities, 7,979 (cusip, date) pairs; AGREES 315, CONSTANT_SCALE 5, STEP 2, ISOLATED 15, NOISY 37, TOO_FEW 346. Identical. Every pair below carries an origin: `same_date` trade (by/sl), `gap` (nearest close within 3 trading days, day gap kept), or a same-date print of another type (`dvr`, `leu`, `TRCISU`).

## 2. The widenings, each against round 69 alone

| widening | pairs added | of the 346: leave TOO_FEW, into | of the 50 | new securities compared |
|---|---|---|---|---|
| A nearest close, 3 trading days (trade prints) | 42 (gap -1: 4, +1: 14, +2: 14, +3: 10) | 1: AGREES 1 | 0 classed | 2, both TOO_FEW |
| B dvr (reinvested distributions) | 1,801 | 18: AGREES 8, NOISY 8, ISOLATED 1, CONSTANT_SCALE 1 | 9 classed | 8 (3 AGREES, 1 NOISY, 4 TOO_FEW) |
| B leu | 143 | 2: AGREES 2 | 0 | 0 |
| B TRCISU | 20 | 0 (one NOISY becomes AGREES) | 0 | 0 |
| B all three together | 1,964 | 19 | 9 | 8 |
| C same security, another key | 0 (reported, not merged) | 0 | 0 | 0 |
| **A + B together** (gap pairs also taken for dvr: 12 more) | **2,018** | **20: AGREES 10, NOISY 8, ISOLATED 1, CONSTANT_SCALE 1** | **9** | **12 (4 classed, 8 TOO_FEW)** |

**Gap pairs (A).** 54 in all (42 trade, 12 dvr), at most 3 trading days; they sit in 46 securities (AGREES 27, TOO_FEW 15, ISOLATED 2, NOISY 2). They moved one security out of TOO_FEW. The guard (an ISOLATED verdict resting only on gap pairs is set aside) fired 0 times. A gap pair is a small yield because the table holds a security only from its first held day in the served window: 54,226 print dates have no close that day and almost all of them are far earlier than the first stored close.

**Print types (B).** Rule: on the 315 securities classed AGREES, close over |Amount|/|Quantity| on same-date pairs must have a median within 2 percent of 1 and at least 90 percent of pairs within 5 percent, over at least 15 pairs; a print other than by/sl also needs summed Quantity >= 0.05 (Quantity is rounded to 3 decimals; without this guard WAB's 0.001-0.002-share reinvestments imply prices of 60 to 320 and make a false NOISY security).

| type | pairs on AGREES securities | median ratio | within 2% | within 5% | verdict |
|---|---|---|---|---|---|
| sl / by (baseline) | 3,437 / 2,514 | 1.0009 / 0.9997 | 94.7% / 92.5% | 99.4% / 98.7% | the round-69 trades |
| dvr | 1,141 (71 securities) | 1.0000 | 91.7% | 99.3% | ADMITTED |
| leu | 133 (64) | 1.0014 | 79.7% | 99.3% | ADMITTED (median and 5% test; its tails are wider than dvr's) |
| TRCISU | 18 (17) | 0.9971 | 100% | 100% | ADMITTED (small) |
| li | 868 (219) | 1.2315 | 7.6% | 16.1% | REJECTED |
| ci | 69 (18) | 1.0633 | 18.8% | 39.1% | REJECTED |
| LISU | 31 (18) | 1.0072 | 41.9% | 51.6% | REJECTED (median at 1, spread wide) |
| trfi | 23 (20) | 1.1978 | 0% | 4.3% | REJECTED |
| lica | 17 (16) | 1.2012 | 5.9% | 17.6% | REJECTED |
| acca | 5 (5) | 24.5 | 0% | 0% | REJECTED |
| licar, TRFIR | 4, 3 | 0.98, 1.00 | | | NOT ADMITTED (too few to show) |
| lo, loca, trfo, trco, QA | | | | | no price (zero or no Amount) |
| dv, dvlt, dvst, DVX, frntax, roy, misc, int, ftax | | | | | Amount without Quantity: no price |
| LICASU, accal, ac, DVRX, cs, ileu, si, ss, trci | 0 | | | | NOT TESTABLE (no pair on an AGREES security) |

**Where the 20 go.** AGREES 10 (MELI, RING, BND, ROK, PTTAX, SWAGX, AMCFX, VBTLX, VBR, FXNAX); NOISY 8 (CWGIX, AWSHX, NEWFX, WGIFX, WMFFX, AMRMX, FINFX, CPXIX); ISOLATED 1 (VTSAX: 11 reinvestment pairs at 1.000, two trade pairs at 1.128 and 0.953); CONSTANT_SCALE 1 (OIEJX). The 12 newly compared securities: AMCPX NOISY, FEMKX, FSSNX, MHYIX AGREES, 8 still TOO_FEW.

**The 50.** 9 are now classed: NOISY 7 (WMFFX, NEWFX, WGIFX, AMRMX, FINFX, CWGIX, AWSHX), ISOLATED 1 (VTSAX), CONSTANT_SCALE 1 (OIEJX). 41 are still thin. Adding the 3 newly compared securities that carry a beyond-10-percent pair, **44** thin securities still carry such a pair. All gains come from reinvestment prints; the nearest-close rule classed none of the 50.

**(C).** In the transactions each CUSIP lists exactly one Symbol (0 of 4,634 list two), so a CUSIP whose ticker changed cannot be seen; 103 tickers are claimed by more than one CUSIP. Of the 346, 2 are touched (GDX and GE, each claimed by two CUSIPs); none of the other claimants has a close in the table, so there is nothing to merge. Touched: 2 of 346, 0 of the 50.

**The seven keep their class** in every widening: BALCX CONSTANT_SCALE 0.758, T STEP 0.7578, XLB 0.502, MMM STEP 0.8418, AMBFX 0.7676, FDX 0.811, CTVA 0.1513 (factors move by at most 0.004).

## 3. The post-widening table

| class | round 69 | after widening |
|---|---|---|
| AGREES | 315 | 329 |
| CONSTANT_SCALE | 5 | 6 |
| STEP | 2 | 2 |
| ISOLATED | 15 | 16 |
| NOISY | 37 | 45 |
| TOO_FEW | 346 | 334 (326 of the 346 and 8 newly compared) |
| securities / pairs | 720 / 7,979 | 732 / 9,997 |

Pairs by class in the final scan (same-date trade / dvr / leu / TRCISU / gap): CONSTANT_SCALE 37 pairs (28 / 9 / 0 / 0 / 0); STEP 55 (49 / 3 / 3 / 0 / 0); ISOLATED 1,438 (1,153 / 276 / 3 / 3 / 3); NOISY 1,032 (740 / 288 / 1 / 0 / 3); AGREES 6,976 (5,583 / 1,213 / 132 / 16 / 32); TOO_FEW 459 (426 / 12 / 4 / 1 / 16). TOO_FEW securities have 1 pair (209) or 2 (125).

| ticker | class | factor | span (wrong side) | pairs: same-date / other print / gap | priced holding-days wrong | measured account-days | new |
|---|---|---|---|---|---|---|---|
| BALCX | CONSTANT_SCALE | 0.758 | 2022-05-09..2023-03-01 | 11 / 3 dvr / 0 | 428 | 426 | no |
| T | STEP | 0.7578 until 2022-01-10, then 1.00 from 2022-06-02 | 2020-07-16..2022-01-10 | 42 / 6 (3 dvr, 3 leu) / 0 over both sides | 3,062 (588 in the gap) | 28 | no |
| XLB | CONSTANT_SCALE | 0.502 | 2020-11-19..2023-11-22 | 4 / 0 / 0 | 608 | 16 | no |
| MMM | STEP | 0.8418 until 2024-01-09, then 1.00 from 2025-02-18 | 2021-12-16..2024-01-09 | 7 / 0 / 0 over both sides | 3,524 (1,384 in the gap) | 0 | no |
| AMBFX | CONSTANT_SCALE | 0.7676 | 2023-12-13..2024-11-27 | 3 / 4 dvr / 0 | 504 | 0 | no |
| FDX | CONSTANT_SCALE | 0.811 | 2021-10-19..2025-10-10 | 5 / 0 / 0 | 170 | 0 | no |
| CTVA | CONSTANT_SCALE | 0.1513 | 2020-07-23..2026-02-18 | 4 / 0 / 0 | 115 | 0 | no |
| OIEJX | CONSTANT_SCALE | 0.6408 | 2021-11-29..2021-12-16 | 1 / 2 dvr / 0 | 19 | 0 | **yes** |

Reach: 8,430 priced holding-days (8,411 + 19) and **470 measured account-days** (distinct; unchanged from round 69: the new one adds none). No new security rests on gap pairs; the one new security rests on two reinvestment prints and one trade.

**Hand-read.** I read the ratio series of: OIEJX (0.621 dvr 2021-11-29, 0.641 dvr 2021-12-14, 0.642 trade 2021-12-16: three pairs over 17 days); the added pairs of BALCX, AMBFX and T (dvr and leu ratios 0.74-0.77, and T's two leu pairs of 2024 at 1.026 and 1.003, on the agreeing side); and all 9 newly NOISY series and the newly ISOLATED one: 11 new series in full, plus 3 of the original seven for their added pairs. The nine NOISY series (AMCPX, AMRMX, CWGIX, WGIFX, CPXIX, FINFX, NEWFX, AWSHX, WMFFX) are not scales: each starts at a ratio of 0.47 to 0.84 in 2020-2023 and rises in jumps at distribution dates to about 1.00 by 2025-2026 (WGIFX 0.686 -> 1.004; WMFFX 0.648 -> 0.998), the shape of a dividend-adjusted close. OIEJX's 3 pairs cannot tell a scale from the start of such a ramp; it is counted, and reported as resting on reinvestment prints.

## 4. The 1,700 with no close

By kind: Equity 807, Mutual Fund 711, ETF 66, Mutual Fund (Closed End) 59, Unit Investment Trust 57. **1,693 are held** on some date in the served table (Equity 800; the 7 not held are Equity): 4,221,264 holding rows, **974,014 distinct account-days**, none priced, **all 974,014 NOT_MEASURABLE** (61.5 percent of the 1,584,413 NOT_MEASURABLE account-days in the returns table of 1,691,729). By kind, holding rows: Mutual Fund 2,884,391, Equity 1,127,732, Closed End 87,961, ETF 80,834, UIT 40,346.

Is it an absence or an unmade join? **Mostly absence.** Across the six local store caches (two are empty), counting a row under (i) the CUSIP, (ii) the transactions' ticker, including a ticker another CUSIP claims: no CUSIP row for any of the 1,700 (the gold and rivalfunds caches carry CUSIP-keyed rows, none of these); no row under any ticker claimed by one CUSIP only (1,460 securities); **90 have a row only under a multiply-claimed ticker** (149 of the 1,609 with a ticker have one): gold cache 49, silver cache 81, bbg testpull cache 8 (the three overlap). 91 of the 1,700 have no ticker in the transactions. **1,610 have no price row under any key.** Of the 90, 28 have a ticker row on days they are held (232,676 holding rows, 224,842 account-days), and 47 have another claimant CUSIP with a close in the table. Whether such a row prices the security: on dates the security traded, the silver row agrees with the traded price within 5 percent for 6 of 25 that overlap, the bbg row 1 of 2. So the join the build refuses recovers at most 90 of 1,700 (28 with held days), and only if each row is shown to price the right CUSIP.

## 5. Fixed income

753 traded, 180 in the table. **Unit: fraction of par on both sides.** The 180 securities' closes have median 1.03 (5th to 95th percentile 0.985 to 1.12; 179 of 180 securities between 0.8 and 1.2; none near 100); the 186 trade dates of the same securities carry |Amount|/|Quantity| with median 1.07 (0.998 to 1.183), Quantity a par amount (median 35,000), so no times-100 factor. **Not classed:** the closes are the gold snapshot store only, 14,131 rows from 2026-06-08 to 2026-10-06, while every trade is on or before 2026-05-05 (nearest 34 days): 0 pairs within 3 trading days, so there is no FI table. Diagnostic only: 10 securities have a close within 90 days of a trade and the ratio is 0.983 to 1.015 (median 0.9997); accrued interest's small bias is not visible at that resolution.

## 6. Not established

See `not_established` in the JSON. In short: why any ratio is what it is; whether OIEJX is a scale or the start of a ramp; how many AGREES funds carry the ramp on dates not seen; the 334 and 44 cannot be shrunk further from custodian rows because the table starts at the first held day; the 1,610 are an absence in the six local caches, not a statement about the live stores; ticker changes are not visible in the transactions; fixed income has no pair; reach is counted, not valued; the Quantity >= 0.05 guard on non-trade prints is this scan's own rule.
