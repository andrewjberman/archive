# IRPT_DASHBD round 92, workstream B -- drain-end and FWD-8 grade (issuer 2.0.0_SA_COO~D2, 2026-10-13 ~18:0xZ)

**One cell, LOCAL:** `DB-b-172` (~138), order `IRPT_DASHBD.TO-DB-b-172.bd-excludes-served-income-over-the-23-days` (issued @983ff0292d), status `complete`, round-close `verdict=MAY-CLOSE` (`round-close-check --project IRPT_DASHBD --round 92`: orders=1, judgment=0).
Drained @ab1112493b. On the CTO's ROUND-92 ANALYSIS @a862a037f3 section 3 and msg 7063. S3 GET/LIST only (the same two stores as round 91: 925 Black Diamond rows, 261 served rows); zero vendor calls; no served byte moved; counts, multiples, offsets and sizes only.

## What the cell found

- **Rule before the read:** `RULE_EXCL.md` committed alone (d8a3f1fa58) before any computation on the 23 days. Closed list, in order: `BD_EXCLUDES_SERVED_INCOME`, `BD_INCOME_PER_LOT` (Reading B, the CTO's reading of record), `DUPLICATE_ROW`, `BOOKING_DATE_DIFFERS`, `MISSING_IN_LEDGER`, `UNEXPLAINED`.
- **The new test holds on 13 of the 23 days, not 8.** Round 91's 8 were counted over the 12 whole-multiple-income days; this count is over all 23. `round91_pattern_8_days_confirmed` is false: a finding, not a failure. All 13 days where the test holds were taken (the correction brings each within 0.01 pp). Reasons 2 to 5 take 0 days in every account.
- **Per account (plan order; days differing: taken by the new reason / UNEXPLAINED; window):** 1: 9: 3/6, open; 2: 2: 2/0, closed; 3: 1: 1/0, closed; 4: 1: 1/0, closed; 5: 7: 4/3, open; 6: 1: 0/1, open; 7: 2: 2/0, closed. **4 windows re-close with a stated reason; 3 stay open.** The negative arm holds: all 7 uncorrected windows miss 0.35 pp.
- **The 3 open accounts, UNEXPLAINED days (offset from the segment start / size):** account 1: 0/+0.045, 5/-6.858, 6/-0.044, 10/-2.392, 12/+0.031, 17/-3.843 pp; account 5: 0/+0.060, 9/+0.044, 10/+0.025 pp (all three under 0.07 pp); account 6: 0/-2.745 pp. Row `IRPT_DASHBD-D2-W138-S1` (BLOCKING, hazard INERT). The record does not separate "a day is UNEXPLAINED" from "the window numerically misses": a window is closed only when no day is UNEXPLAINED and it re-closes.
- **Reproduced by this seat:** the drained module re-run from fresh S3 reads gives the same per-account counts, summary and `test_held_days` (13) as the committed record; the stored-table control reads 122 of 122 window days. This seat read `RULE_EXCL.md` in full and the module's output, not the module's source line by line.
- **What the new reason is, stated plainly (the issuer's reading, for the CTO):** `BD_EXCLUDES_SERVED_INCOME`'s test and its correction are one identity (the gap equals minus the served income over the prior value; the correction subtracts it), so a day where the test holds closes by construction. What carries information is that the test holds on 13 days and that 4 whole windows then re-close. It DESCRIBES what Black Diamond's day return does; it does not say why. The evidence multiples (income in Black Diamond's own rows over the served income, from the worker's report) are 1 on all 5 days of accounts 2, 3 and 7 and 3 on account 4's day (4 on 3 days of account 1, 5 on 4 days of account 5): so on at least those 5 days Black Diamond's own ledger carries the same income as ours and its day return still omits it.

## FWD-8 grade (PRD 11b as the CTO read it in the round-91 analysis, ruling 1)

| segment group (90 stored segments, 86 accounts) | window grain (0.35 pp, `BD_DEFAULT`) | day grain |
|---|---|---|
| 76 flow-bearing segments | agree | not graded one by one |
| 5 flow segments + 2 no-flow segments | disagree; reason stated and the window re-closes when corrected | met (ruling 1) |
| **4 of the 7 open windows (accounts 2, 3, 4, 7 of the round-90 list)** | disagree | **met: every differing day carries `BD_EXCLUDES_SERVED_INCOME` and the window re-closes** |
| **3 of the 7 (accounts 1, 5, 6 of the round-90 list)** | disagree | **not met: 10 UNEXPLAINED days** |

**Grade: FWD-8 is NOT REALIZED for 3 accounts; met for the other 83.** Per the CTO's item 3, those 3 accounts' days come back to the CTO once more with the per-day table (above and `EXCLUDES_INCOME_23_DAYS.json`), and the next ruling is on the ENDPOINT, not another read: whether FWD-8 is accepted with those accounts named as known oracle gaps. That changes a DONE WHEN, so it is the CTO's to carry to Andrew as a card; this seat chose none.
The label and guard clauses are not re-graded here (cited as in rounds 89 to 91; the C-LABEL switch is IRPT_BCKEND's page).

## Open

- **Ledger leg L7 (mine), carried:** the first scheduled fire after the thresholds swap, 2026-10-14 11:41Z, `checks/l5/l5b_read.py` @88d74f1a63; ledger `irpt-dashbd-thresholds-swap-20261013` stays OPEN until then.
- **For the CTO:** the endpoint decision on the 3 accounts; whether `BD_EXCLUDES_SERVED_INCOME` (a description of Black Diamond's behaviour, closing by construction where its test holds) is accepted as a "stated reason" under FWD-8; account 5's three tiny days.
- **Push state:** this seat's commits are LOCAL on box/dell2.

-- 2.0.0_SA_COO~D2
