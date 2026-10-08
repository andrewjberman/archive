# IRPT_DASHBD TO-DB-b-39 -- the four non-rounding windows, read and fixed by rule (counts only)

Worker 0.9.0_WK_IRPT_DASHBD~22, round 25 workstream B, cell DB-b-39. The fixes are in `account_activity_lots.py` (4 new tests, 35
passing in all); `account_return_daily.py` and every served producer were imported read-only; S3 was read, never written. The evidence
is `WINDOWS_E1.json` beside this file; `windows_e1.py` regenerates it. No client figure, balance or account number is quoted here.

## What explains the four windows (each read against its lot rows)

- 3 windows were MISSING-TERM in round 24 (a lot's basis above the cash paid). The cause is a wash-sale carry-over: on the open lot,
  `disallowed_loss_amount` equals `cost_basis_unamortized` less `original_cost_basis` on 102 of 102 lots that carry one on the last
  day (2026-10-05); on 2026-09-30, 101 of the 102 lots carrying one have `acquired_date` earlier than `orgpurch_date` (the holding
  period tacked back). That loss had no cash
  behind it, so the lot entered the unrealized book understated by it while the earlier sale had already carried the loss in realized.
  Lots newly opened with such a basis: 1, 4 and 1 in the three windows (the 4 also closed 6 such lots in the window).
- 1 window was OTHER in round 24 (a custodian re-selection). A leg of in-kind shares posts on one day with one selection of lots; the
  next trading day the table shows another selection of the same security (2 lot ids out, 1 in) with the share count unchanged and
  the remaining basis moved. The shares relieved are the leg's on both days, so this is reproduced from the rows,
  not a vendor behaviour left unexplained.
- All 4 are `kind` RULE. None is VENDOR: every cause reproduces from the custodian's rows.

## The two rules (no account id in the producer)

1. A lot whose custodian basis carries a disallowed loss is measured from the cash paid (basis less the loss) on every day it is open
   and where it closes (`basis_source` WASH_SALE_EXCLUDED_BASIS; the custodian's figure stays in `custodian_cost_basis`). An in-kind
   reference takes precedence. A closed lot is linked to the open lot it closed by its opening event and, where the event holds
   several lots, its acquired date (one sale of 0.94 shares was unlinked before this). 2,478 unrealized rows and 9 realized rows
   carry the new source; 0 rows have an absent disallowed figure.
2. After an in-kind departure, a re-selection of the same security's lots within LEG_LAG_DAYS (1) with the shares unchanged, no leg and
   no sale moves the departure gain by the change in the remaining basis. 1 re-selection in the window. Any other basis move with
   shares unchanged is listed (0 in the window).

## The re-run, same 91 accounts and window, LEG_LAG_DAYS 1

| | round 24 | E1 |
|---|---|---|
| graded | 91 | 91 |
| within one cent (passed) | 55 | 58 |
| above one cent (failed) | 36 | 33 |

- The 33 failures are all ROUNDING (gap within 0.05); MISSING-TERM 0 (was 3), OTHER 0 (was 1). The 4 windows' gaps: 3 now tie within
  a cent, 1 sits at 1.07 cents (ROUNDING). No window got larger and no account that passed in round 24 fails.
- Nothing is plugged: the residual of each of the 4 windows after the fix equals the residual round 24's diagnosis left unexplained.

## Controls

- The two rules switched off for the 4 accounts return round 24's four gaps exactly (4 of 4).
- Two runs of the driver over the same days give byte-identical output.
