# CARD-A P1 slice: the depth cuts for Andrew's card (2.0.0_SA_COO~Q1, 2026-10-13) -- for CTO msg 4921; NO draw

Read only: `card_a_slice.build("P1", ...)` on the merged DQ-t-44 window (box/dell1 @900406e221), the silver transactions for each name's first-trade window, flow dates and `Asset_Type`.
No Yahoo or Bloomberg call, nothing written to a store. CUSIP-level rows: scratchpad `p1_cuts_by_cusip.csv` (counts per CUSIP, no account data, not committed).

**Names:** 609 in P1; 606 priced (FDIC66606, FDIC66853 and the 7-character cash identifier CFNCASH are cash identifiers, not priceable). **Quota rate:** 2,673 cells a day (the history
allowance the quote tool implied for the P1 slice).

## The cuts, cells and days of quota

| `Asset_Type` (transactions) | names | A. every trading day | B. month-ends before 2026-04-22, daily after | C. flow dates + month-ends, everywhere | D. flow dates + month-ends before 2026-04-22, daily after |
|---|---|---|---|---|---|
| Fixed Income | 370 | 398,113 (149 days) | 22,787 (9 days) | 23,134 (9 days) | 26,476 (10 days) |
| Cash Equivalent | 227 | 65,771 (25 days) | 4,386 (2 days) | 7,370 (3 days) | 8,323 (3 days) |
| Alternative Investment | 9 | 4,234 (2 days) | 353 (0 days) | 354 (0 days) | 491 (0 days) |
| **Total** | **606** | **468,118 (175 days)** | **27,526 (10 days)** | **30,858 (12 days)** | **35,290 (13 days)** |

## What the cuts mean and how they were counted

- **A** is the merged builder's own daily window: each name from the later of its first trade and 2012-01-01 to the frontier when held (or its last trade when not). It reads 468,118 here against the
  quote tool's 471,522 for 607 names; the 3,326 cells of CFNCASH and a 78-cell edge difference in counting the last day account for the gap.
- **B** (CTO cut 2) keeps every trading day from 2026-04-22 (where Black Diamond units begin) and, before that date, only the last trading day of each month inside the window.
- **C** (CTO cut 3) keeps only flow dates (a name's own transaction dates, moved to the next trading day when they fall on a non-trading day) plus month-ends, over the whole window.
- **D** is C before 2026-04-22 and daily after, so the recent period matches B's.
- A `month-end` is the last NYSE trading day of the calendar month inside a name's window.

## Caveats, stated plainly

1. **Security type.** The transactions table carries three `Asset_Type` values for these names (Fixed Income, Cash Equivalent, Alternative Investment). It does NOT distinguish bond from
   annuity, SMA sleeve or private fund; mutual funds are a Yahoo type and are not in this set. A six-way split needs a source I have not found for 606 CUSIPs.
2. **Black Diamond units** cover only 179 of these names and 1,944 held days from 2026-06-08, so cuts B and D keep daily draws after 2026-04-22 for every name; they do not remove them.
3. **Month-end sampling** gives a month-end price, not a daily series. Whether the reports behind these names need daily values is Andrew's call; this table only prices the choice.
4. The 2,673 rate is the quote tool's allowance for this slice; it moves with the Bloomberg history ceiling and the 10 percent ad-hoc reserve Andrew set (the rate shown is before that reserve).
