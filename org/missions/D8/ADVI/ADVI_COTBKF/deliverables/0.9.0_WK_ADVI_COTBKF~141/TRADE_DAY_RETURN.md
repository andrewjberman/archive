# TRADE_DAY_RETURN -- the return on trade days across every account (round 76, CB-bx-4)

Measurement on local copies, by arithmetic on the served table. Nothing was built, fetched or read from a bucket. No account id, amount, quantity, value, flow or return is in this folder; counts, basis points, tickers and dates only.

## The quantity, written first (2026-10-11T22:47:16Z, before it was computed on any row)

Served return on day t with the account's previous row s: `ret_t = (V_t - F_t + A_t) / V_s - 1`, V = shares x served close, a purchase or sale internal.

- **Purchase** of |q| shares for cash |c|: the table values the new shares at |q| x close_t; at what was paid they are worth |c|. `delta_V = |c| - |q| x close_t`, `delta_ret = delta_V / V_s`. Positive = the served return is too low. Several funds in one account-day: the terms are summed, then divided by V_s once. A fund with no served close that day is `no_close`: counted, not computed.
- **Sale**: the sold shares are gone from V_t and the cash is in it, so V_t does not depend on the fund's close on t. The mis-valuation of the sold shares sits in V_s (the carried holding), which this item does not revalue. The sale's trade term on its day is **zero**. Sale days enter the population and the by-kind count and add 0 bp; they never enter the over-10bp count alone. Round 75's 3 sale days with LOWER returns came from the full two-build comparison, where the holding at s was revalued; that is outside this quantity.
- **Not revalued:** the holding carried at the served close. This is the TRADE term only.
- **Floor:** counted when |delta_ret| > 10 bp (headline); > 1 bp reported beside it.

## Control (before the count)

On round 75's 12 purchase days the term reproduces `q x (p1_t - p0_t) / V_s` on **12 of 12** (agreement within the larger of 5 percent or 1 bp; ratio 0.99994 to 1.00004; 41.5 to 51.6 bp on ten days, 881.7 and 882.0 bp on two). The definitions differ in one place: round 75 values the new shares at the UNADJUSTED vendor close p1; here they are valued at the price paid (cash over shares), which equals p1 within 1 percent on 12 of 12. Against round 75's other split, the q part `Pred - Pred_h` of the two-build prediction, it agrees on 2 of 12 (the two days where that part is the whole change): that part is a difference of two builds that nets the holding and the denominator. Against the observed round 74 two-build change, the term is 0.9989 to 1.0037 of it.

## Population (every denominator)

| step | trade account-days |
|---|---|
| a by or sl unit of a fund among the 270 series, amount present, quantity >= 0.05 sh (91,495 rows; 38 rows dropped by the guard; 247 of the 270 series have a trade row) | **15,103** (in 928 accounts) |
| no unit has a served close | 8,929 (`no_close`) |
| with a served close | 6,174 (in 544 accounts) |
| measured (return present, V_s present and positive) | **31** (in 13 accounts) |
| blank, with a close | **6,143**: UNPRICED 6,136; DVR_CLOSE_STEP 6; FIRST_DAY 1; no row in the table at all 0 |

15,103 = 31 measured + 6,143 blank + 8,929 no_close. The 91,040 units (account, day, fund, kind) split 14,250 with a close and 76,790 without; on the 31 measured days no unit lacks a close. By kind of day: purchase-only 4,863, sale-only 3,941, both 6,299 (all 15,103); the 31 measured are 17 purchase, 14 sale, 0 both.

## The number

**16 of the 31 measured trade account-days change by more than 10 basis points** when the trade is valued at what was paid (also 16 over 1 bp). Bands: 10-50 bp: 9; 50-200 bp: 5; over 200 bp: 2 (sum 16). All 16 are served-return-too-LOW (0 too high). By kind: purchase 16 of 17, sale 0 of 14 (the sale term is zero). By year (changed of measured): 2021 3/4, 2022 9/11, 2023 2/3, 2025 2/7, 2026 0/6. By price fit (served close / price paid): within 1 percent 0 of 7; 1 to 5 percent 0 of 1; 5 to 20 percent 2 of 6; over 20 percent off 14 of 17 -- so none of the changes is fee-sized. The 19 moved funds: 12 of 17; all other funds: 4 of 14. Largest: **882.0 bp**, 2025-10-24, FCNTX. The changes sit in **4 accounts** and **3 funds** (4 funds counting a second purchase unit on a changed day). Sanity: the 12 purchase days are inside the 16 (12 of 12); 3 of round 74's 9 changed accounts are among the 4.

## Blank days, apart (never added to the headline)

Of the 6,143 blank trade account-days with a close, 13 cannot be evaluated (1 with no previous row, 12 with no valued position at the previous row). Literal rule (V_s = sum of the valued positions at s): 6,130 evaluable, 1,591 over 10 bp (452 / 565 / 574 in the bands). That figure is an upper figure, not a measurement: on an UNPRICED day most positions are unvalued, V_s is a partial sum and the ratio is inflated. Strict rule (every position at s valued): 122 evaluable, **46 over 10 bp** (9 / 20 / 17). The 8,929 no_close days cannot be evaluated here.

## Headline

16 of 31 measured trade account-days change by more than 10 basis points when the trade is valued at what was paid. This is the trade term only: the carried holding is not revalued, and a sale adds nothing on its day. The 6,143 blank trade account-days are counted apart; the 8,929 with no served close are not computed.

## Not established

See `not_established` in TRADE_DAY_RETURN.json. In short: the measured set is 31 of 15,103 account-days (accounts holding an unpriced position never measure, and most trades have no stored close), so the count describes where the served table is priced and not the other 15,072 account-days; the term is first-order and not a rebuilt return; the price paid includes any load; the fund series outside the 270 are not in the population.
