# Rival Funds: what each chart and table reads, and the owed history sized to it

Issuer 2.0.0_SA_COO~V1, 2026-10-13 ~20:5xZ, on CTO msg 5138 (Andrew: "C1 yes measure that now."). READ ONLY: source files and S3 GETs/LISTs under
`cloudops-dell1-agent-user`; no Bloomberg call, no write to the served store. Page day 2026-10-13, as-of 2026-10-12 (`prev_trading_day`).
Script, re-runnable: `round30_prep/owed_size.py` (same folder). Source: `data/etfs/scripts/rivalfunds/` (`render.py`, `publish_page.py`,
`gold_holding_contribution.py`, `gold_buying_trend.py`, `gold_trade_schedule.py`, `price_series.py`, `history_owed.py`).

## 1. What each component reads

No component reads a FUND-level price: the funds' NAV hook is documented as "none on file" (`gold_holding_contribution.py:28`), and `render.py`,
`publish_page.py`, `gold_holding_contribution.py` and `gold_buying_trend.py` carry no fund price or fund return read (grep over those four, read
beside this table). Every element below is HOLDING-level.

| component (where) | securities | field | earliest date shown |
|---|---|---|---|
| Holding ranking, 30d (best and worst 10, `render.py` `_rank_table`; stage `gold_holding_contribution`) | every holding of the fund that period (all ranked; the table shows 10 and 10) | day total return `DAY_TO_DAY_TOT_RETURN_GROSS_DVDS`, else the close ratio, else the fund's own implied price | 2026-09-12 (as-of minus 30 calendar days) |
| Holding ranking, 90d | same | same | 2026-07-14 |
| Holding ranking, 365d | same | same | 2025-10-12 (first trading day 2025-10-13) |
| Sector ranking, all three periods | sums of the holding returns above | derived, no new field | as the three rows above |
| Buying trend (`gold_buying_trend`) | the fund's holdings | none from the vendor: shares from the fund's own reports; `g4_window` is read for names and parse keys only (`gold_buying_trend.py:313`) | 30d / 90d / 365d as above, needs no owed history |
| Trade list and trade schedule (`gold_trade_schedule`) | the fund's holdings | none from the vendor: `est_price` is the fund's own `market_value / quantity` (`gold_trade_schedule.py:44`) | as above, needs no owed history |
| Security dialog price curve (402 dialogs on the 2026-10-13 page; `price_series.py`, `publish_page._build_charts`) | the holdings that get a dialog: top 10 best and worst of R30 and R365, and the trend's top 10 into and away | the close `px_close` only (no total return); the fund-implied price fills a day with no close | 30d 2026-09-12; 90d 2026-07-14; 365d 2025-10-12 |
| Trade markers on the curve (`trade_markers`) | the same dialog securities | none from the vendor (trades and fund market value) | as the curve |
| Audit page (`render.py` audit list) | the refused (security, day) rows of each fund's R365 security table | derived | 2025-10-12 |
| Dramatic move lookup (`dramatic_move.py`) | a security that moved | the close, within 30 days of the move (`DATE_WINDOW_DAYS`, read at the constant only) | 30 days before the move |

So two things consume owed history: the RANKINGS (the return of every held security on every day a fund held it, total return first) and the
CURVES (the close of each dialog security over the range). Nothing needs a fund's own price.

## 2. The owed set, sized to what the page reads

Live reads, 2026-10-13: owed set from `history_owed.owed(s, "2026-10-13", 365)` = 742 securities x 251 trading dates = **182,394 units** (a unit is
one security on one trading day with no stored close). 13 funds in G1; `ACWI` and `IWM` hold 0 of the 182,394 units, so Z4 changes no cell here.

| need | units | cells at close only | cells at close + total return | runs at 20,000 cells (close + TR) |
|---|---|---|---|---|
| Everything owed today (all 742 securities, all 251 dates) | 182,394 | 182,394 | 364,788 | 19 |
| What the page reads, 365d (rankings' held days plus the curves) | 145,689 | 145,689 | 291,378 | 15 |
| What the page reads, 90d | 34,673 | 34,673 | 69,346 | 4 |
| What the page reads, 30d | 8,924 | 8,924 | 17,848 | 1 |
| Field-matched, 365d: total return on the rankings' held days (123,933) plus the close on the curves' days (89,216) | 123,933 + 89,216 | n/a | 213,149 | 11 |
| Fund-level only (13 funds x 251 dates) | 3,263 | 3,263 | 6,526 | 1; serves NO element above |

Parts of the 145,689: rankings' held days 123,933; curve days 89,216; both 67,460; rankings only 56,473; curves only 21,756.
Per fund, held days owed (a security held by two funds counts for each): BASG 8,049; BIDD 11,090; CGIC 44,653; ETFT 6,025; GQGU 916; IDVZ 7,385;
INEQ 24,654; PCLG 6,151; PFOE 3,994; SCHY 25,243; TSEL 6,476; TXUE 11,844; WCMG 4,247.

## 3. What this does and does not say

- The CTO's "about 185,000 cells, 370,000 with TR" matches the all-owed row (182,394 and 364,788). Its "fund-level only about 9,500" is NOT reproduced:
  13 x 251 is 3,263 units, 6,526 at two fields. Either way a fund-level pull feeds no table or chart.
- The page-read row cuts the all-owed set by 20%, because 36,705 units (182,394 minus 145,689) sit outside every held day and every dialog. The field-matched row is
  the smallest honest figure, if the request can ask a field per unit; if one request asks both fields for each unit, use the close + TR column.
- The 30d slice is one run; 90d is four. The 365d rankings and curves are what the 15 runs buy. Which period must be complete first is Andrew's.
- NOT measured: (1) held days are the day after each fund report that holds the security, which understates a fund whose reports skip a day (the
  contribution carries the latest report forward); (2) 29 of 402 dialog keys did not map to a security id and are not in the curve counts; (3) the
  dramatic-move window was read at its constant only; (4) the securities a fund holds but the 10-13 page does not rank are included in the
  rankings' held days (the stage ranks all of them).
