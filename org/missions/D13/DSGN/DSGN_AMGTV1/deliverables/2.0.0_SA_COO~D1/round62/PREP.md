# DSGN_AMGTV1 round 62 -- prep (2.0.0_SA_COO~D1, 2026-10-09 ~10:2xZ)

Carried from the round-61 close (@252ca10073, CTO msg 2234, CVO `ADJUDICATION_v34.md`), for the cut once the CTO's round-61 analysis
lands. Read at portal DEV `9b06f6ed`.

1. **The price line breaks at every day with no close.** `components/TimelinePanel.tsx:667-676` draws the price `Line` with
   `connectNulls={false}`. The spine has a day for every calendar day, so the line breaks at every weekend and holiday; on a nine-month
   spine it reads as dashes. Fix: `connectNulls`. `withPrices` keeps those days at `null`, so the chart draws the join and no value is
   placed on the day.
2. **The price axis has no label** (`TimelinePanel.tsx:641-649`); the left axis reads "Articles per day". Fix: a label naming the
   closing price. No currency is served on `price_series`, so the label names none.
3. **The walk names one security with no stored prices** (CVO, the `TO-AV-zzm-2` AC3 carry). The round-61 walk saw only names with
   prices, so the one sentence (`data-timeline-price-absent`) was never seen rendered. The next close walk picks a name outside the
   stored price history (95 tickers, gg-5).

Check: `round62/checks/r62.cjs`, dry-run at DEV `9b06f6ed` 2 of 4 (ONE LINE and THE AXIS SAYS WHAT IT IS FAIL as expected; NOTHING
INVENTED holds as the guard; PLANTED passes). Items 1-2 are one repair cell, LOCAL, cut as LF (row `DSGN_AMGTV1-D1-S1`).
