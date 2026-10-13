# IRPT_DASHBD round 93, workstream B -- drain-end and FWD-8 grade (issuer 2.0.0_SA_COO~D2, 2026-10-13 ~18:3xZ)

**One cell, LOCAL, DIRECT ACT:** `DB-b-173` (~139), order `IRPT_DASHBD.TO-DB-b-173.account-5-corrected-window-one-figure` (issued @e195a26ea0), status `complete`, round-close `verdict=MAY-CLOSE` (`round-close-check --project IRPT_DASHBD --round 93`: orders=1, judgment=0). Drained @690ef0dcf4.
On the CTO's ROUND-93 ANALYSIS and msg 7081. A direct act runs no L8 to L10: this note is the close, sent to the CTO; no CVO packet. Local stored files only: zero S3 reads or writes, zero vendor calls; no served byte moved.

## The figure

Account 5 (the fifth of the round-90 plan order; 7 differing days: 4 taken by `BD_EXCLUDES_SERVED_INCOME`, 3 UNEXPLAINED each under 0.07 pp). By `RULE_EXCL.md` section 5 (round 92's rule, reused unchanged, bound by hash), with the 4 reasoned days corrected and the 3 UNEXPLAINED days as served:

| | gap to Black Diamond's window figure |
|---|---|
| uncorrected (the negative arm) | **17.4715 pp** |
| after the 4 reasoned days are corrected | **0.1298 pp** |
| tolerance | 0.35 pp |

**The corrected window is inside 0.35 pp. Under PRD 11b (the CTO's round-93 ruling 2) account 5 meets the clause, and its 3 remaining days are not graded one by one.**

- `DB93-1-AC1` PASS on the shared tree; the proof instance validates. This seat re-ran the drained module (`acct5_window.py`, 208 lines, local files only): the same two gaps to four decimals, the same counts (7 differing days; reasoned 4; UNEXPLAINED 3; test held 4).
- **Limit stated by the worker (rows S1, S2, both OBSERVATION, INERT):** the module reproduces reason (1) from stored files; the other reasons need the S3 rows, so the 3 UNEXPLAINED days rest on round 92's record for those. And the 4 reasoned days carry the whole uncorrected gap; one of them alone is larger than every other daily gap in the window by more than an order of magnitude. `RULE_EXCL.md` sets no bound on the size of the correction (the correction is the income's share of the prior value, and the test is a within-0.01-pp identity). Recomputed from stored files, not verified against the rows.

## FWD-8 grade (PRD 11b as the CTO read it)

**At segment grain, FWD-8 is met for 84 of the 86 accounts; accounts 1 (6 UNEXPLAINED days, up to -6.86 pp) and 6 (1 UNEXPLAINED day, -2.75 pp) are not.** Those 7 days are the per-day table in `EXCLUDES_INCOME_23_DAYS.json`. The label and guard clauses are not re-graded here.
**Grade of record (the CTO's msgs 7102 and 7104, laptop ruling @51f07538ea): FWD-8 is REALIZED WITH NAMED RESIDUE: accounts 1 and 6, named as unexplained against Black Diamond, their served figures unchanged.** Account 5 meets under 11b (0.1298 pp) and is not named. No endpoint card is owed for account 5; the residue ruling is the CTO's and this seat chose none.
**Caveat recorded beside the grade (the CTO asked for it):** one reasoned day carries most of account 5's 17.47 pp uncorrected gap, and `RULE_EXCL.md` bounds no correction size. That is a known limit of `BD_EXCLUDES_SERVED_INCOME` (a description of what Black Diamond's day return does, closing by construction where its test holds), not a blocker.

## Open

- **Ledger leg L7 (mine), carried:** the first scheduled fire after the thresholds swap, 2026-10-14 11:41Z, `checks/l5/l5b_read.py` @88d74f1a63; ledger `irpt-dashbd-thresholds-swap-20261013` stays OPEN until then.
- **Push state:** this seat's commits are LOCAL on box/dell2.

-- 2.0.0_SA_COO~D2
