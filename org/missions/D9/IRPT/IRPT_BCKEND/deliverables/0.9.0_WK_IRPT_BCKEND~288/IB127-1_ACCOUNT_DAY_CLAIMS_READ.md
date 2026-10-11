# IB127-1 -- the per account-day date-basis claim, counted (read only, counts only)

Author `0.9.0_WK_IRPT_BCKEND~288`, 2026-10-11. For the CTO (msgs 4825, 4833). Data: `IB127-1_account_day_claims.json`. Instruments: `ib429_fetch.py`, `ib429_claims.py` (copied from IB-pr-427 and extended). S3 reads only. No account id, balance or position value is in any file here.

**The paragraph asked for.** To stamp a claim on day D the instrument needs four things: the account's Cottonwood holdings partition for D, the Schwab anchor's close for D, the anchor's close for the prior trading day, and the trading calendar (a static table in the repo). It also reads yesterday's stamped claim for the serving rule. The Cottonwood partition for D is the last to land: about 11:46 UTC on the next calendar day, about two hours after the anchor's close for D (about 09:46 UTC). Over 85 graded days (2026-06-10 to 2026-10-09) there are 76,796 account-days. 45,247 read OWN_DATE, 425 PRIOR_CLOSE and 31,124 (40.5 percent) NOT_GRADED. The rule as written serves 43,932 of 75,796 eligible account-days and **blanks 31,864, which is 42.0 percent**; 403 of 999 accounts are never served. The alternative (an account-day is good when it reads OWN_DATE or has nothing to grade) **blanks 18,931, which is 25.0 percent**; 169 accounts are never served. Counted on only the two ungradeable kinds the order names, the alternative blanks 10,825, which is 14.3 percent (see "A class I added").

## The claims (one per account-day, 85 days, 1,000 accounts)

Rule: any moved row at neither close makes the day NOT_GRADED; else any prior-close row makes it PRIOR_CLOSE (a day with own and prior rows and no neither row is PRIOR_CLOSE); else any moved row, all at the own close, makes it OWN_DATE; else NOT_GRADED. Every account in a graded partition has a claim; none is dropped.

| claim | account-days | share |
|---|---|---|
| OWN_DATE | 45,247 | 58.9% |
| PRIOR_CLOSE | 425 | 0.6% |
| NOT_GRADED | 31,124 | 40.5% |
| all | 76,796 | |

Mixed account-days: 8 hold both own and prior rows (all PRIOR_CLOSE). 788 hold a neither row beside own or prior rows; the rule makes them NOT_GRADED.

| NOT_GRADED reason | account-days |
|---|---|
| no_moved_security | 30,201 |
| neither_row | 923 |

## NOT_GRADED, split (AMENDMENT 1)

A NOT_GRADED day is `ungradeable` if it holds a priced security the instrument cannot grade; otherwise `nothing_to_grade`. A day with both kinds is ungradeable, named by the first that applies: neither_row, outside_anchor, no_cusip, negative_position.

| side | class | account-days |
|---|---|---|
| nothing_to_grade (13,636) | cash and rows with no price | 12,685 |
| | rows with no price only | 928 |
| | cash, unmoved securities and rows with no price | 23 |
| ungradeable (17,488) | outside_anchor (priced, the anchor lacks it) | 8,380 |
| | no_cusip (valued row, no CUSIP) | 7,930 |
| | neither_row (moved row at neither close) | 923 |
| | negative_position (Units and value below zero) | 255 |

"Rows with no price" are rows with Units and Market Value null or zero. Of the 386 accounts with no moved row on any day: 136 hold a valued row with no CUSIP on some day, 131 hold a security outside the anchor, 3 a negative position, 110 hold only cash and rows with no price, 6 only rows with no price. 146 accounts are NOT_GRADED and ungradeable on every day they appear; 116 are NOT_GRADED and nothing-to-grade on every day.

## The serving rule

Eligible: present today and on the prior graded day. First day: 2026-06-10's prior partition (2026-06-09) is ungraded and has no claim, so the 707 account-days of 2026-06-10 are not eligible and are outside these counts (still claimed above). Counted instead as eligible and blank, the as-written share would be 42.6 percent. 293 later account-days are not eligible because the account was absent the prior day.

| | as written | alternative | alternative, two kinds only |
|---|---|---|---|
| eligible | 75,796 | 75,796 | 75,796 |
| served | 43,932 | 56,865 | 64,971 |
| blank | 31,864 | 18,931 | 10,825 |
| blank share | 42.0% | 25.0% | 14.3% |
| blank: today PRIOR_CLOSE | 422 | 422 | 422 |
| blank: today NOT_GRADED / ungradeable | 30,601 | 17,181 | 9,120 |
| blank: yesterday PRIOR_CLOSE | 101 | 102 | 102 |
| blank: yesterday NOT_GRADED / ungradeable | 740 | 1,226 | 1,181 |
| accounts never / always / sometimes served (999) | 403 / 142 / 454 | 169 / 286 / 544 | 47 / 425 / 527 |

Reasons are taken in the order today PRIOR_CLOSE, today not graded, yesterday PRIOR_CLOSE, yesterday not graded. The alternative is NOT the rule in force.

## A class I added

The order lists ungradeable kinds outside_anchor and neither_row "or any other reason you meet". I met two: valued rows with no CUSIP (Units and Market Value above zero, 11,837 rows across the 91 partitions read, not cash-flagged) and negative positions (Units and Market Value below zero, 4,084 rows, same basis). The instrument's price filter (CUSIP present, Units above zero) leaves both out, so it cannot grade them, and either could sit on the wrong date. I counted them ungradeable. The right-hand column above shows the alternative without them. Cash-flagged rows (Cash Equivalent = true) count as cash even when priced and outside the anchor (2,263 nothing-to-grade account-days hold one).

## Daily needs of the instrument

| input | from | exists by |
|---|---|---|
| Cottonwood partition, day D (CUSIP, Market Value, Units, AccountID; Cash Equivalent for the split) | blackdiamond_z09 silver positions, `date=D/` | 11:46 UTC next day, last 8 days: **last to land** |
| Anchor close, day D | Schwab silver dim_position, `date=D/` | 09:46 UTC next day, about 119 minutes earlier |
| Anchor close and Cottonwood partition, prior day | same prefixes, `date=p` | already in place |
| Trading calendar | `lib/trading_calendar.py`, static to 2027 | no landing time |
| Prior-day claim | the instrument's own output for p | stamped a cycle earlier; none for 2026-06-09 |

Times are object last-modified times (list only). Over all 85 days the Cottonwood partition was later on 62 and the anchor on 23; a rewrite moves an old day's time.

## Control and reconciliation

Planted fixture (4 days, 4 accounts: one prior-close day, one neither row, cash-only, unmoved, outside-anchor, no-CUSIP and negative-position days): the planted counts equal the counts read, for the claims, both splits, the rule as written, the alternative and the two-kinds alternative. Reconciliation with IB-pr-427: exact. Moved rows 583,996, prior 3,278, neither 1,903, own 578,815; 85 days; 1,000 accounts; 386 with no moved row.

## Not measured

- Why a security is outside the anchor, why a row has no CUSIP, or what those positions are worth (no value was read out).
- Whether an OWN_DATE day also holds an ungradeable row; it is claimed OWN_DATE.
- When the gold runs or what it does when an input is late; no schedule or log was read.
- 2026-06-09 and any day outside 2026-06-09 to 2026-10-09.
- Which rule is right. This read counts and proposes nothing.
