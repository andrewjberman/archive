# IRPT_DASHBD round 91, workstream B -- drain-end and FWD-8 grade (issuer 2.0.0_SA_COO~D2, 2026-10-13 ~17:0xZ)

**One cell, LOCAL:** `DB-b-171` (~137), order `IRPT_DASHBD.TO-DB-b-171.ledger-rows-behind-the-23-differing-days` (issued @f7c008ad8d), status `complete`, round-close `verdict=MAY-CLOSE` (`round-close-check --project IRPT_DASHBD --round 91`: orders=1, judgment=0).
Drained @09d0ebc99a. On the CTO's ROUND-91 ANALYSIS @3a44c65c3e section 3 and msg 7032. S3 GET/LIST only; zero vendor calls; no served byte moved; counts, multiples, offsets and sizes only.

## What the cell found

- **Rows read:** Black Diamond's landed transactions, 925 rows over 1,878 partitions (all columns, the seven accounts, each differing day and five calendar days either side); the served side, 261 rows over 269 partitions, from the custody transactions store the gold producer's source declaration names (found by the worker through `comp-read`). No denial. Stored-table control: 122 of 122 window days match.
- **Rule before the read:** `RULE_LEDGER.md` committed alone (e90aabb4cb) before any ledger row of the seven was opened.
- **Result:** all 23 differing days UNEXPLAINED under the CTO's closed list (`BD_INCOME_PER_LOT`, `DUPLICATE_ROW`, `BOOKING_DATE_DIFFERS`, `MISSING_IN_LEDGER`); all 7 uncorrected windows miss; **0 of 7 windows re-close**. Per account (differing days): 9, 2, 1, 1, 7, 1, 2. Row `IRPT_DASHBD-D2-W137-S1` (BLOCKING, hazard INERT).
- **Reproduced by this seat:** the drained module re-run from fresh S3 reads gives the same per-account counts, the same summary and the same row counts (925 and 261) as the committed record. This seat read the rule addendum and the module's header, not the module's 503 lines.
- **A defect in the rule as written, found by the worker, handled by its own clause:** the `BD_INCOME_PER_LOT` test demanded two distinct transaction identifiers among the income rows, but a per-lot split is several rows of one transaction (9 of the 12 multiple-income days carry one identifier). The rule file is untouched; a dated `RULE_LEDGER_ADDENDUM.md` (0adf9dd5db) states READING B (test: at least two income rows whose sum is a whole multiple k of the served income). **Reading A (as written) is the record; Reading B was measured only in the worker's private folder by a copy of the module differing in that one clause: it takes no day either.** The disposition of the two readings is the CTO's.
- **The worker's measured pattern (not a reason, not verified by this seat):** 12 of the 23 days carry Black Diamond income that is a whole multiple (3x: 1 day, 4x: 6, 5x: 4, 6x: 1) of the served income, over 3 to 25 income rows each, none a single row; on 8 of those 12 the day gap equals minus the served income over the prior day's value, to within 0.01 pp; with the per-lot clause removed, the Black Diamond-side correction closes none of the 12.
- **One variance from the analysis, stated:** the analysis said to read "through IRPT's existing per-account call". Black Diamond's transactions for these accounts are already landed in S3 (the store the earlier tie-out cells read), so this cell made no vendor call (decomposition section 93, decision b). The issuer's own pull of round 90 stays the only vendor read.

## FWD-8 grade (PRD 11b as the CTO read it in the round-91 analysis, ruling 1)

| segment group (90 stored segments, 86 accounts) | window grain (0.35 pp, `BD_DEFAULT`) | day grain |
|---|---|---|
| 76 flow-bearing segments | agree | not graded one by one |
| 5 flow segments + 2 no-flow segments | disagree; reason stated and the window re-closes when corrected | met (a window reason that re-closes the window meets the day clause; ruling 1) |
| **7 flow segments, one in each of 7 accounts** | disagree; no window-grain reason | **23 differing days; no reason from the round-90 list and none from the ledger-row list; all 7 windows open** |

**Grade: FWD-8 is NOT REALIZED for those 7 accounts; met for the other 79.** Per the CTO's item 3, the 7 come back to the CTO by count with the per-day table (per account: days differing 9, 2, 1, 1, 7, 1, 2; the UNEXPLAINED offsets and sizes are in `LEDGER_ROWS_23_DAYS.json`, e.g. sizes from about 0.03 pp to about 32 pp). What a served day shows when it cannot be supported (FWD-8's first clause) is then the CTO's to rule.
The label and guard clauses are not re-graded here (cited as in rounds 89 and 90; the C-LABEL switch is IRPT_BCKEND's page).

## Open

- **Ledger leg L7 (mine), carried:** the first scheduled fire after the thresholds swap, 2026-10-14 11:41Z, `checks/l5/l5b_read.py` @88d74f1a63; ledger `irpt-dashbd-thresholds-swap-20261013` stays OPEN until then.
- **For the CTO:** the two readings of reason 1; the 7 accounts; whether a further read (a vendor read of Black Diamond's own transaction listing for those 23 days, or a ruling that the daily series is not a valid oracle at day grain) is wanted. This seat chose none.
- **Push state:** this seat's commits are LOCAL on box/dell2.

-- 2.0.0_SA_COO~D2
