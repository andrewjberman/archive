# IB153-1 (IB-pr-457) -- the date-basis producer's design as a read

A READ, NOT A BUILD. Base 1bce31df72. Counts only; the entry is named by its key, blackdiamond_z09. Data: `IB153-1_producer_design_read.json`; driver `ib153_count.py` (every grade comes from `data/assets/scripts/gold/irpt_reporting/date_basis_grading.py`). Nothing edited, built, served or proposed as an order.

## What is served today
1. Nothing carries a date basis for this entry (measured). `date_basis_claim`, `PER_ACCOUNT_DAY`, `date_basis_witnesses` and `ungradeable_kinds` have 0 hits in `data/assets/scripts`, `infra/` and `docs/contracts`; the only `date_basis` is the prospect envelope's, a different member. The entry declares `partition_close` OWN_DATE, basis inferred (`sources.json:168`), not PER_ACCOUNT_DAY.
2. The holdings gold has 20 columns and none is a claim (`holdings_performance.py:248`). Its manifest carries the declared partition-level close (`:1157`). The record shows 75 partitions landed by a one-off run to 2026-09-25 (held; not re-listed). The performance route composes holdings sources for two other firms only (`installed.py:68`, measured), so it does not serve this entry's returns today.

## Where the module would be called
3. Only `holdings_performance.py:1065` (via `holdings-performance/handler.py:149`) holds this entry's partitions. It has NO schedule for this entry (measured: the two scheduled fires name the other two entries; the first-witness one is 07:30 America/New_York, described live, ENABLED).
4. The reporting-gold producers (`account_return_daily.py:993` and the class, activity and lot producers) read no partition of this entry; they are consumers (07:41 America/New_York).
5. Landings (S3 LastModified, 22 partitions since 2026-09-10): anchor next day 09:46Z (21 of 22); the entry's partition next day 11:46Z (19 of 22; 3 landed 3 to 5 days after the date). 07:30 America/New_York is 11:30Z in daylight time, 16 minutes before the partition (measured arithmetic). Earlier partitions show later last writes (46 of 69 and 23 of 64), so these are steady-state times, not a history.
6. The site lacks: the first witness's closes (another entry), the bars, the security types, the prior day's claim, and a write path for a day already landed (the handler writes new keys only, `handler.py:105`).

## Where each input lives
7. Rows: the entry's silver partitions, already read by the producer (measured). Closes: the first-witness entry's silver, next day 09:46Z. Types: the transactions table beside the holdings, read by measurement scripts only (121 partitions, 1,042,552 rows).
8. The second witness's bars exist only as run-time Yahoo fetches into a local directory (`commonwealth_price_basis_census.py:200`; `read_yahoo_close` reads that directory only, `commonwealth_daily_valuation.py:229`). No scheduled producer lands them. A landed prices store with yahoo-labelled points exists, but it is not shown to hold the unadjusted Close (the census classes some tickers dividend_adjusted or mixed), and its schedule was not read. A run-time fetch from a producer is a design fact: egress from a Lambda, a rate limit stops a pass, and a ticker with no bars means no grade (7 of 878 here).

## Consumers (found by subtraction)
9. 38 files name the gold or reach it by its table constant: 14 consumers, 8 writers, 16 neither (34 by the table string, then 4 more by the module name and `TABLE_DAILY`: a name search is not a census of readers; it first missed `holdings_comparison.py`). The portal checkout (dbeb6764, another checkout) names the gold in 0 files; the pages that render the route's returns were not classified.
10. Key policies (measured): the route reader (`holdings_gold.py:153`) ignores an added column, SKIPS a non-OK day and chains the rest with a partial absence rather than refusing (`:246`, `:314`), and raises on an OK row with a null return (`:259`). The guard read (`account_return_daily.py:1016`) and the comparison (`holdings_comparison.py:223`) key on status OK. How a blank day is written decides whether the route serves it.

## The count (computed by the product module, 85 days, 300 securities)
11. Security-days the guard grades and the rule (window 40, floor 20) does not: 272 = 54 for short history only + 218 for the repeat rule (all 218 on a full window of 39 comparisons). Reproduces IB-pr-454's record.
12. 4 securities were ever short of 20 compared days. 26 account-days are blank only for short history (freed 12195 with the floor, 12221 without; blank 33340 against 33325 of 75796).
13. Newly held: the floor reads the bars, not the holdings (`date_basis_grading.py:189`). Of 70 securities first held inside the run, 68 met the floor on the day first held; 2 are blank for their first window, both securities that began trading inside the run. 3 securities began trading inside the run and stay ungraded for short history for 16, 17 and 19 days.

## Open design questions (the addendum must answer; the JSON gives what would settle each)
Bars source and failure mode; who writes the claim after a day has landed; how a blank is written for the route; the run time against late landings; the prior day's claim; where the types live; the declaration vocabulary and the gold's contract file (none found); the members carried; route composition and role grants for this entry's firm; packaging.

## Not established
The gold's live extent; any schedule outside Terraform; the portal pages' behaviour; whether the landed prices store is as-traded; Lambda egress to Yahoo; whether LastModified is first landing; the count outside the 85 days; the `irpt-holdings` snapshot lambdas; `retained.py`.
