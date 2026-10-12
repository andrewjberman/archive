# IB-pr-464: the performance route's reader, per window and per firm -- accounts with an excluded day, and where those days fall

Base `7c00a44b5a`. READ ONLY. Arm `READER_CODE_OVER_SERVED_GOLD`: the reader's own code (`holdings_gold.calculate`) run locally over the served holdings gold read from S3; NOT the deployed route (see `arm_in_words`). Every landed partition read once: the 49F entry 566, orion 1619. Counts only; no account id is written.

## Answer, leading with the interior counts

**the 49F entry** (interior = `interior_only` + `first_and_interior`, accounts with a figure):
- SI: 222 of 3736 accounts with an excluded day are interior (97 interior only, 125 first and interior); 3336 first day only; 178 with the last row excluded.
- YTD: 98 of 1592 accounts with an excluded day are interior (54 interior only, 44 first and interior); 1380 first day only; 114 with the last row excluded.
- QTD: 1 of 47 accounts with an excluded day are interior (1 interior only, 0 first and interior); 42 first day only; 4 with the last row excluded.
- 1Y: 125 of 2056 accounts with an excluded day are interior (64 interior only, 61 first and interior); 1809 first day only; 122 with the last row excluded.

**orion** (interior = `interior_only` + `first_and_interior`, accounts with a figure):
- SI: 53 of 894 accounts with an excluded day are interior (0 interior only, 53 first and interior); 716 first day only; 125 with the last row excluded.
- YTD: 11 of 200 accounts with an excluded day are interior (4 interior only, 7 first and interior); 84 first day only; 105 with the last row excluded.
- QTD: 0 of 7 accounts with an excluded day are interior (0 interior only, 0 first and interior); 3 first day only; 4 with the last row excluded.
- 1Y: 15 of 240 accounts with an excluded day are interior (5 interior only, 10 first and interior); 110 first day only; 115 with the last row excluded.

**The claim.** The reader gives `claim` `measured` or `inferred`. In the cells below `inferred` appears exactly where the account also carries the `missing_trading_days` absence (a trading day with no partition, holdings_gold.py:288-295), which is orion's; it appears for accounts with an excluded day and for accounts with none alike, and the 49F entry's claim is `measured` for all its accounts in all four windows. An excluded day does not enter the claim: the control account read again with one in-memory day set non-OK keeps its claim in every cell. What names the excluded days is the `excluded_rows` absence, status PARTIAL, which every account with an excluded day carries (49F SI 3736 of 3736; orion SI 894 of 894; all cells, `absences_named` in the JSON) and no account with none carries.

## Windows (named from the code)

`SI`, `YTD`, `QTD`, `1Y`: `infra/aws/lambda/investor-reporting/performance/holdings_gold.py:98-106 (_period_for: SI when start is 1970-01-01, else f49_engine.ruled_period_for) with infra/aws/lambda/investor-reporting/performance/f49_engine.py:44 (RULED_WINDOWS = YTD, QTD, 1Y); any other window refuses (holdings_gold.py:105-106). Each ruled window is taken at the latest landed day by parity_period_returns.period_window; SI is 1970-01-01 to the latest landed day.` Each at the latest landed day (2026-10-08 both entries); the ruled windows start SI 1970-01-01, YTD 2026-01-01, QTD 2026-10-01, 1Y 2025-10-08.

## the 49F entry

| window | read | with excluded day | none | refused | first only | interior only | first+interior | last row | claim (with excluded day) | claim (none) |
|---|---|---|---|---|---|---|---|---|---|---|
| SI | 8916 | 3736 | 3160 | 2020 | 3336 | 97 | 125 | 178 | measured 3736 | measured 3160 |
| YTD | 8126 | 1592 | 5240 | 1294 | 1380 | 54 | 44 | 114 | measured 1592 | measured 5240 |
| QTD | 7621 | 47 | 6675 | 899 | 42 | 1 | 0 | 4 | measured 47 | measured 6675 |
| 1Y | 8334 | 2056 | 4784 | 1494 | 1809 | 64 | 61 | 122 | measured 2056 | measured 4784 |

Excluded days per account (accounts with an excluded day): SI: 1=102, 2=178, 3-5=1083, 6-20=1242, more=1131; YTD: 1=39, 2=99, 3-5=460, 6-20=519, more=475; QTD: 1=13, 2=5, 3-5=29, 6-20=0, more=0; 1Y: 1=55, 2=124, 3-5=612, 6-20=655, more=610

Refusals: SI: holdings account mapping missing or duplicate 1296, holdings gold carries no OK row inside the window 724; YTD: holdings account mapping missing or duplicate 506, holdings gold carries no OK row inside the window 788; QTD: holdings account mapping missing or duplicate 1, holdings gold carries no OK row inside the window 898; 1Y: holdings account mapping missing or duplicate 714, holdings gold carries no OK row inside the window 780

Status values (every partition): ALL-HOLDINGS-EXCLUDED 467, FOLLOWS-DISCONTINUITY 2, IMPLAUSIBLE-RETURN 2, NO-PRIOR-HOLDINGS 413118, NON-POSITIVE-BASE 1596, OK 2841381

## orion

| window | read | with excluded day | none | refused | first only | interior only | first+interior | last row | claim (with excluded day) | claim (none) |
|---|---|---|---|---|---|---|---|---|---|---|
| SI | 979 | 894 | 32 | 53 | 716 | 0 | 53 | 125 | inferred 144, measured 750 | inferred 32 |
| YTD | 979 | 200 | 706 | 73 | 84 | 4 | 7 | 105 | inferred 124, measured 76 | inferred 32, measured 674 |
| QTD | 979 | 7 | 798 | 174 | 3 | 0 | 0 | 4 | measured 7 | measured 798 |
| 1Y | 979 | 240 | 676 | 63 | 110 | 5 | 10 | 115 | inferred 134, measured 106 | inferred 32, measured 644 |

Excluded days per account (accounts with an excluded day): SI: 1=1, 2=4, 3-5=12, 6-20=9, more=868; YTD: 1=3, 2=4, 3-5=13, 6-20=23, more=157; QTD: 1=1, 2=0, 3-5=6, 6-20=0, more=0; 1Y: 1=2, 2=4, 3-5=12, 6-20=20, more=202

Refusals: SI: holdings gold carries no OK row inside the window 53; YTD: holdings gold carries no OK row inside the window 73; QTD: holdings gold carries no OK row inside the window 174; 1Y: holdings gold carries no OK row inside the window 63

Status values (every partition): NON-POSITIVE-BASE 575039, OK 855536

## What a non-OK row means (producer)

- **the 49F entry:** One function writes both entries' status (holdings_performance.py:869-874, np.select over three conditions; the vocabulary and its reasons at :171-242). The 49F entry's gold holds six tokens (status_values). NO-PRIOR-HOLDINGS (first condition :869, assigned :873: held_count == 0 and cash_value == 0) is a day with no return BY CONSTRUCTION: the account held no position and no cash on the prior trading day, so there is no base (the account's first day, or a day after it held nothing); it is the commonest non-OK token by far. ALL-HOLDINGS-EXCLUDED (:870-871, :873) and NON-POSITIVE-BASE (:872, :874) are days whose return COULD NOT BE COMPUTED (every prior-day holding lacked an identifier or a price, or the basket was zero or below). IMPLAUSIBLE-RETURN (:881-884) is a day whose return WAS computed and then withheld because it fell outside -100% to +100%, and FOLLOWS-DISCONTINUITY (:949-953) is the day after one, withheld although its own arithmetic may be ordinary. daily_return is null on every non-OK row (:876-877, :884, :953).
- **orion:** Same function and lines. Orion's gold holds only OK and NON-POSITIVE-BASE (status_values): its non-OK row is the third np.select condition at holdings_performance.py:872 (account_value <= 0, assigned :874): the basket (non-negative holding value plus positive cash) at t-1 was zero or below, so the return over it is undefined and the producer writes no return (:876-877). It is a day whose return could not be computed over a zero or negative base; orion's gold holds no NO-PRIOR-HOLDINGS row, so no non-OK row in this entry is a first day with no base, and none is a withheld computed return.

## Position rule

Per account, take its rows inside the window in date order and call a row OK or non-OK by its status (the reader's own test, holdings_gold.py:246). The account has an excluded day when the reader returns a figure and days_excluded is 1 or more. last_day_involved: the account's LAST row in the window is non-OK (whatever else). Otherwise, with its first OK row as the dividing point: first_day_only: every non-OK row comes before the first OK row (a leading run of one or more days, e.g. an account not yet funded); interior_only: every non-OK row lies after the first OK row and before the last row (a day between OK days, chained across); first_and_interior: non-OK rows both before the first OK row and between OK days. The four classes are exclusive and cover the accounts with an excluded day. A refused account (no OK row at all, or an account the reader cannot map) is not placed.

## Control

For each cell the driver reads one account whose every row in the window is OK (the first such account holding the window's fullest set of rows) through the reader's calculate(), and the same account again with ONE of its in-window rows set to NON-POSITIVE-BASE in memory only (the cache is never written back; nothing is written to AWS). see `control.per_cell` in the JSON: the unmodified account returns a figure with days_excluded 0 and the claim every account with no excluded day in that cell gets (claim_the_reader_gives_accounts_with_none); the mutated copy returns days_excluded 1 and the same claim value, which is the finding itself. Transport check (stand-in vs the reader's own source class, 50 accounts each): 49F SI 50 of 50 identical; 49F YTD 50 of 50 identical; orion SI 50 of 50 identical; orion YTD 50 of 50 identical.

## Not established

- the deployed route's own answer: the deployed package's bytes, dependencies, mapping loader, authorization and response envelope were not exercised (no Lambda invoked, no sign-in)
- the gold was read once, at the time of this run; a later partition may land and move the windows
- why a given account's day is non-OK beyond the status token: the producer's inputs (prices, identifiers) were not read
- the transport check covers a sample of 50 accounts on the windows listed in transport_check, not every account and window
- whether the accounts the reader refuses (no OK row in the window, or absent from the latest partition so not mappable) are ones the route would serve at all: the route's own scope and permitted set were not applied
- the account-level meaning of last_day_involved (an account that exited, or a late data fault) was not separated

Zeros: functions invoked 0, sign-ins 0, AWS writes 0, accounts written 0.
