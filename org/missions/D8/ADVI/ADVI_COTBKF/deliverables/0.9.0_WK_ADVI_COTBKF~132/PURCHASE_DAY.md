# Purchase-day reading, tested under a rule written first (ADVI_COTBKF.TO-CB-bw-1, round 75)

Measurement on the two local builds of round 74 (baseline = served table, variant = 19 validated funds on the unadjusted close). No code changed, nothing built, fetched or served. Counts, basis points (bp), tickers and ratios only; no account id or account value.

**Rule written first:** 2026-10-11T22:04:03Z, before any return was recomputed (full text in `PURCHASE_DAY.json`, key `rule`). Formula: ret_t = (V_t - F_t + A_t) / V_s - 1, a purchase is internal, V = shares x close. Prediction: V_t moves by (h_s + q)(p1_t - p0_t), V_s by h_s(p1_s - p0_s). Tolerance: 5 percent of the prediction or 0.1 bp, whichever is larger. Reading `confirmed` only if the q-term prediction explains at least 75 percent of purchase days, the holding-only prediction (q = 0) explains at most 25 percent, and the holding-only prediction explains at least 75 percent of the changed days over 10 bp that have no trade row.

**Set.** 1,575 changed account-days at a floor of 1e-9, 1,577 at 1e-12. 37 of them carry a share-moving row in a moved fund (same 37 at both floors). The reviewer's count is reproduced: 22 of the 96 over 10 bp (12 purchases all higher, 2 sales both lower, 8 reinvestments of which 7 lower); 74 have no row.

**Recomputation.** The return recomputed from each build's value, previous value, flow (and the owed-elsewhere fee term, none on these days) equals the build's own return on 1,577 of 1,577 days (largest gap 4.4e-16), 37 of 37 trade days.

| kind of row | days | under 1 bp | 1 to 10 bp | over 10 bp | confirmed | refuted | undecided | higher / lower | holding-only explains |
|---|---|---|---|---|---|---|---|---|---|
| purchase (by) | 12 | 0 | 0 | 12 | 12 | 0 | 0 | 12 / 0 | 0 of 12 |
| sale (sl) | 3 | 0 | 1 | 2 | 3 | 0 | 0 | 0 / 3 | 0 of 3 |
| reinvestment (dvr) | 20 | 4 | 8 | 8 | 20 | 0 | 0 | 9 / 11 | 4 of 20 |
| transfer (in-kind lo) | 2 | 2 | 0 | 0 | 2 | 0 | 0 | 0 / 2 | 0 of 2 |
| all | 37 | 6 | 9 | 22 | 37 | 0 | 0 | 21 / 16 | 4 of 37 |

Control: the holding-only prediction explains 1,540 of 1,540 changed days with no trade row, 74 of 74 over 10 bp.

**What the formula predicts.** Purchase: the q term (new shares at the variant close minus the baseline close) is positive on all 12 (32 to 882 bp; 100 percent of the change on the 2 first purchases of a fund in the account, 75 to 76 percent on the other 10; the rest is the carried holding's weight, 10 to 13 bp). Reinvestment: positive q term on 16 of 20 (median 3.8 bp), negative carried-holding term on 17 of 20 (median -14.8 bp), their sum matches the observed change on 20 of 20, so 11 lower and 9 higher is predicted, not an exception. Sales: both terms negative.

**Share of the total absolute change** over the 1,577 days that sits on the 37 trade days: 40.2 percent (purchases 35.8, reinvestments 3.9, sales 0.5, transfers 0.0002); 58.0 percent of the part over 10 bp.

**Which close makes the shares bought worth the cash paid** (|Quantity| x close / |Amount|, row day):

| close | 12 set purchase days: median, within 1 percent | all 936 purchase rows of the 19 funds with a close: median, within 1 percent |
|---|---|---|
| baseline (dividend-adjusted) | 0.76, 0 of 12 | 0.65, 0.3 percent |
| unadjusted | 1.0000, 12 of 12 | 0.997, 73.7 percent |

With the previous trading day's close the unadjusted fit is 11 of 12 (all rows 72.6 percent), with the next day's 9 of 12 (70.3 percent); the baseline stays at 0 of 12 on all three. 183 of the 1,119 purchase rows have no close on the day in the tables read.

**Reading under the rule: `confirmed`** (12 of 12 purchase days confirmed, holding-only 0 of 12, control 74 of 74).

Not established: the agreement is arithmetic (value = shares x close) and holds on every changed day, so it shows where the change sits, not that the unadjusted close is right for every fund; 26 percent of all purchase rows do not fit the unadjusted close within 1 percent (unexplained, not examined); 19 validated funds only; the ex-date step on reinvestment days was not separately measured.
