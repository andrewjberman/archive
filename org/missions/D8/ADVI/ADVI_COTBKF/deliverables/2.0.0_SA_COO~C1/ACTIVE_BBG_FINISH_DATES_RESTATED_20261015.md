# Active-set Bloomberg finish dates, restated (2.0.0_SA_COO~C1, 2026-10-15)

Supersedes `finish_new` 2026-11-24 and `finish_all` 2026-12-04 in `0.9.0_WK_ADVI_COTBKF~170/ACTIVE_BBG_NEED_RECORD.json`, which counted every trading day. Authority: CTO ruling amendment 4 (msg 6140). 5,858 cells is the measured history ceiling per DRAWING day (a floor, not a capacity). Today's rule draws on non-trading days only; "every day" needs Andrew's call 99be and is an upper bound on speed. Start 2026-10-17; `lib/trading_calendar.is_trading_day`.

| set | cells | drawing days | non-trading days only (today) | every day (call 99be) |
|---|---|---|---|---|
| B1 + failed-14 + porting test | 45,317 | 8 | 2026-11-08 | 2026-10-24 |
| B1 + failed-14 + porting test + the 27 active slices | 199,341 | 35 | 2027-01-30 | 2026-11-20 |
| the 27 active slices alone (new set) | 154,024 | 27 | 2027-01-03 | 2026-11-12 |
| B1 + failed-14 + the 27 slices (no porting test) | 196,146 | 34 | 2027-01-24 | 2026-11-19 |

The two CTO rows reproduce exactly. Named gap: 1,006 of the 2,739 new CUSIPs have no Commonwealth window, so the builder cannot price them; they are outside the slices and are not a draw.
