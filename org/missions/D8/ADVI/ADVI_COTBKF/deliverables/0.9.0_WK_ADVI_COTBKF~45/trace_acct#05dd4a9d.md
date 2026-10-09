# Trace of one acct#05dd4a9d month (2023-05) before any change (AMENDMENT 1)

Written and committed BEFORE the rule is changed. Sources: silver transactions as the chain reads them (1,416,497 rows, with Amount),
the r19 and repaired arms of the real run (account_day_value, daily holdings). r19 = round 19's cash legs; repaired = + the funding credit.

## The month

acct#05dd4a9d 2023-05: reported 0.07 pct, r19 MATCH, repaired DIFF (computed 0.0027). Account value on 2023-05-02: r19 1,827.91 (CFNCASH
115.28 + FDIC66606 1,712.63); repaired 34,506.86 (CFNCASH 32,794.23 + FDIC66606 1,712.63). The 2023 sweep interest is about 1.2 dollars
a month (dvr 0.93 on 2023-05-31), which is 0.07 pct of 1,8xx and 0.003 pct of 34,5xx: the r19 level is the level the vendor's return
was made on. The value is blank (account day incomplete) until 2022-07-18, so the level of every later day is set by the CFNCASH
quantity carried from the history.

## The three credit days of the account (2021-07-16, 2021-07-20, 2022-07-18)

| day | stock sales S | sweep buy B | credit min(S,B) | vendor CFNCASH row | sweep sale | CFNCASH qty end of day r19 / repaired |
|---|---|---|---|---|---|---|
| 2021-07-16 | 13,000.00 (38147X705) | 13,000.00 | 13,000.00 | lo 12,788.22 | sl FDIC66606 12,788.22 | 412,475.71 / 425,475.71 (day before 425,475.71) |
| 2021-07-20 | 10,000.00 (38147X705) | 10,000.00 | 10,000.00 | lo 10,000.00 | sl FDIC66606 10,000.00 | 402,475.71 / 425,475.71 |
| 2022-07-18 | 24,560.55 (five securities) | 9,678.95 (6,183.93 + 3,495.02) | 9,678.95 | lo 7,034.39 | sl FDIC66606 7,034.39 | 14,299.98 / 46,978.93 (day before 23,978.93 / 46,978.93) |

Per day the cash rows are: sweep buy -> LIX -B; sweep sale -> LOX +sale; (repaired only) credit LOX +min(S,B); vendor `lo` -(withdrawal).
On 2021-07-16 under repaired: -13,000 + 12,788.22 + 13,000 - 12,788.22 = 0 (the stock moves into the sweep, the sweep pays the
withdrawal); under r19 the CFNCASH line falls by 13,000. The first complete day is 2022-07-18: r19 17,640.53, repaired 50,319.48;
the difference 32,678.95 = 13,000 + 10,000 + 9,678.95, the three credits, and it is carried unchanged to 2023-05 (34,506.86 - 1,827.91 =
32,679.0 with the same 1,712.63 sweep). The 13 months (2023-05, 06, 08, 09, 11, 12, 2024-02, 03, 05, 06, 08, 09, 11) are the months with a
gradable return whose level carries those 32,678.95.

## What the vendor posts in this account

From 2022-07-18 to 2023-06-30 every sweep sale of FDIC66606 (32 rows, 174,694.92) has a CFNCASH `lo` of the same quantity on the same
day (41 `lo` rows, 173,984.23, the extra rows pairing 3,000 + 8,000 with one 11,000 sale); the one contribution (li CFNCASH 150,000.00 on 2022-09-16)
sits beside a sweep buy of 150,000.00; the three `man` rows (-710.69) beside sweep sales of the same size. The vendor books the cash legs of the
account's sweep trading itself, on its own CFNCASH rows. The 2022-07-20 sweep buy (14,881.60, T+1 of the 24,560.55 sale) has no CFNCASH row.

## The general condition that would clear the 13, stated before any change

On every one of the 13's credit days the account's CFNCASH line carries a vendor row whose quantity equals a same-day listed-sweep SALE
(the vendor's own cash leg of the sweep trade). Candidate rule (one rule, every account, over row types): the funding credit is not applied on
a day on which a CFNCASH row of any type equals a same-day sweep sale quantity (CARRY_TOL). Measured on the 2,703 credit days of list v1: 310
carry any CFNCASH row; 32 carry one equal to a same-day sweep sale (lo 25, man 6, li/lo/trfi/trfo 1), against which the wider "any CFNCASH
row" condition would drop 310 (130 of them contribution `li` rows that are cash INTO the account).

It is shipped only if the real run keeps round 22's 25 movers MATCH and the control unchanged; otherwise the order's refusal clause applies.

## Measured after the change (same AC2 invocation; list v1 both arms; control 642 of 642 in every run)

| conditions in the rule | credit days kept of 2,703 | months_after (MATCH/DIFF/UNGRADABLE) | regressions | movers_back (round-19 movers MATCH) |
|---|---|---|---|---|
| round 22 `repaired` (none) | 2,703 | 2103/1520/78970 | 23 | 25 |
| (b) as built | 2,703 | 2103/1520/78970 | 23 | 25 |
| (a) + (b), the order as amended | not counted | 2045/1538/79010 | 14 | 0 |
| (b) + (c), no (a) (scratch driver, not shipped) | 2,671 | 2116/1507/78970 | 10 | 25 |
| (a) + (b) + (c), SHIPPED as `conditional` | 793 | 2058/1525/79010 | 1 | 0 |

(c) clears all 13 of acct#05dd4a9d and keeps the 25 (b)+(c): it is shipped. (a) clears 9 of the other 10 but loses all 25 round-22 recovered movers:
every credit day of the 25's five accounts (acct#5aa91f68, acct#ab0c6781, acct#cce589ab, D49141608, D49141714) sold a security with no price the day before,
exactly as the 9 did, so "valued the day before" does not separate the 9 from the 25. The one month left is acct#57e741a5 2025-07: the sold
security is the money-market fund 316067107 (priced), four credit days (4,871.60 / 4,711.88 / 1,514.07 / 778.15 = 11,875.70) pass every
condition; r19 value on 2025-07-31 9,816.72, with the credits 21,692.42 (the difference 11,875.70); reported 0.12 pct, r19 matches, the
credited base gives 0.0535.
