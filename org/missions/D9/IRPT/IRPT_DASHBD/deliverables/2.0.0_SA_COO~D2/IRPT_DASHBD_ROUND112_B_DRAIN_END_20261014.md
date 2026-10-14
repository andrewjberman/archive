# IRPT_DASHBD round 112 (the CTO's round-111 L10 answer, msg 7868), workstream B -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-14 ~23:0xZ)

**Two orders, both drained; nothing served moved, nothing written to AWS, nothing deployed; counts, hashes and words only in the repo; the client gold, the household table and every record's inputs stay in the private folder `C:/dev/_irpt_private_evidence_20261009/`.** Issued @c33edfe326. Drained: `DB-b-228` (~183, @6c1eff2aa6) and `DB-b-227` (~182, @06670d9e5a). On the landed tree `DB112-1-AC1` and `DB112-2-AC1` PASS, and so do the three round-111 criteria, the five round-110 criteria and the 14 earlier live criteria. `round-close-check` reads **MAY-CLOSE** (2 orders complete, 2 proof instances VALID, 0 judgment criteria: this round has nothing for the CVO to grade by eye). Push state: `c33edfe326`, `6c1eff2aa6` and my amendment `3503188d92` are ON origin box/dell2 (fetch read, origin @3503188d92); the merge `06670d9e5a` and this packet are LOCAL until the box-sync takes them.

## What the cells found

- **`DB-b-227` (the SOURCE_BREAK rule for household windows, no imputation):** a pure function `household_window_result` in the round-111 module, and the contract's `window_rule`. A window that holds an unmeasured account day returns no figure and the absent form `SOURCE_BREAK` with the CTO's words ("Account <k> of <N> has no measured return on <days> in this period, so the household return for this period is not shown."; the account with the most unmeasured days is named, the lowest position on a tie); a day on which the household has no row at all has its own words; a household that did not exist at the window's start, or whose window holds no day, takes `INSUFFICIENT_HISTORY` (two sets of words). A planted gap renders the words, never a figure; a fill-in mutant fails 5 of 20 tests. Applied to all 4013 households of the 49 Financial firm (the driver reproduces round 111's table row for row: 1,704,799 rows, 0 differing). Per window, figure / SOURCE_BREAK (account, no row) / INSUFFICIENT_HISTORY: QTD 3814 / 194, 1 / 4; YTD 2027 / 1329, 1 / 656; last 12 months 1765 / 1319, 1 / 928; since inception 1449 / 2563, 0 / 1. The 4 + 656 + 928 + 1 insufficient-history households did not exist at their window's start (or have no day yet), which is true to the data.
- **`DB-b-228` (the household-None cause read):** of the households that are SOURCE_BREAK, by the first cause found: closed or stopped before as_of, a null account return, a gap inside the account's life, or a household with no row: QTD 195 (159 / 35 / 0 / 1), YTD 1330 (145 / 1184 / 0 / 1), last 12 months 1320 (132 / 1187 / 0 / 1), since inception 2563 (159 / 2404 / 0 / 0). **The unmeasured account-days are 56,311: `NOT_MEASURABLE` 50,299, `FLOW_UNRECONCILED` 6,005, no row 7.** Every cause names one producer, `data/assets/scripts/gold/irpt_reporting/account_return_daily.py`, which is this project's own: the days it marks not served (the geometric link breaks with a stated gap) are what null the household windows. **One date is the largest single cause: 2026-04-21 breaks 861 households' since-inception windows (825 YTD, 781 last 12 months)**; the next are 2026-07-02 (182 households) and the as_of day itself (160, accounts whose rows stop before it). 570 of 570 partitions read; the rebuilt daily table equals round 111's on every household-day.

## What this seat read for itself

I re-ran each criterion in the worker's tree and on the landed tree, re-validated each proof instance, scanned the changed files for identifier-length digit runs (hashes, a private path and a commit pin only) and checked that the checker's independent recount from the private table (4013 households per window) equals the record's counts. I did not open the cause record's top dates against the account gold myself. No pages (no render this round). **Not a grade.**

## Issuer errors this round (mine, disclosed)

`DB-b-227` first returned a figure of 0 for a household whose only row date is the as_of day (no day in its since-inception window): found by the cause read, amended on `W183-S1` (row `D2-S47`) to `INSUFFICIENT_HISTORY` in words; the order's criterion line still says "three words forms" while step 6 and the check require four (the worker followed step 6 and the check).

## Rows held (owners named)

`W183-S1` ruled and `W183-S2` disarmed in `D2-S47` (the commit gate's client-data check could not run on dell2 because its hashed account-id list is absent: no worker commit this round was checked against it; this seat's identifier scans stand in). `W182-S1` (ARMED, owner 0.0.0_AB_MSTR): the same gate gap, infrastructure. No ARMED row has a dark owner.

## What goes to the CTO (one ask, in the slug)

The largest single cause of the household None windows is one producer event in this project's own `account_return_daily.py`: 861 households on 2026-04-21 (and `NOT_MEASURABLE` is 89 percent of the unmeasured days). May the next cell be a READ of that date's `NOT_MEASURABLE` rows by cause (a position with no price, a flow that does not reconcile, a source missing), before any repair, since a repair would move served numbers and needs a never-widen pair? Carried as data facts: the three round-111 findings still stand (the account-number field, the household tie-out outside-range counts, the households' table is private and nothing sources the report from it yet).

## What this does to the FWD outcomes

Inputs to `FWD-2` and `FWD-21`: neither is met. The 49 Financial household return now has a stated rule for what prints: a figure for 3814 of 4013 households this quarter, 2027 this year, 1765 over 12 months and 1449 since inception, and in words, never a fill-in, for the rest; the report contract's household return members for 49 Financial stay ABSENT until the table is accepted and the contract sources them. Grading is the CTO's at L10.

## Open

**Andrew:** the as-of approval row `dell2-20261014T195533Z-90a9` (client-facing) and call a252 (the 49 Financial disclosure file). **This seat:** `DB-b-183` L3, the first scheduled D_04 run after the 12:08:39Z upload (a one-shot wake at 23:20Z is set).

-- 2.0.0_SA_COO~D2
