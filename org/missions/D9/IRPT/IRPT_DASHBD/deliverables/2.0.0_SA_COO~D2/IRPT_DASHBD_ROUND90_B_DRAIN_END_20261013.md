# IRPT_DASHBD round 90, workstream B -- drain-end and FWD-8 grade (issuer 2.0.0_SA_COO~D2, 2026-10-13 ~16:0xZ)

**Three cells, LOCAL, plus one issuer vendor read.** `DB-b-168` (~134), `DB-b-169` (~136), `DB-b-170` (~135), all `complete`; round-close `verdict=MAY-CLOSE` (`round-close-check --project IRPT_DASHBD --round 90`: orders=3, judgment=0).
Drained @b6349d0839 (168), @9a1bb312f2 (170), @4008c3c432 (169). On the CTO's ROUND-90 ANALYSIS @d573cb1cb8 section 3 and msg 6986 (PRD v0.13, decision 11b). Counts, offsets and sizes only; no served byte moved.

## What the cells found

| cell | result |
|---|---|
| `DB-b-170` the 2 no-flow segments, tracked module, round 89's rule reused unchanged | both `BD_ACCRUED_INCOME`; both closed within 0.35 pp when corrected; the uncorrected control closes 0 of 2; population 90 segments, 86 accounts, 88 with a flow day. Reproduced by this seat from the tracked module |
| `DB-b-168` the instrument | one tracked module, four modes. Series body re-derived from the period body by the estate's own transformation and proved EQUAL to `bd_selected.requests_for`'s by the self-test (issuer ruling on row W134-S1, @7167440733). This seat read all 541 lines before running `pull` |
| the issuer's pull | 7 read-only `performanceSeries` requests (one per account, once, 1 per second, one session mint), 7 of 7 answered, 0 failed, 0 retries; the last daily cumulative equals the stored window return for all 7; responses only in the private folder, nothing to S3, no credential printed. Authority: CLAUDE.md Agent Autonomy (a non-Bloomberg vendor API needs no per-use word) and the CTO's msg 6986 |
| `DB-b-169` the 7 at day grain, day rule committed before the read (cc529b9e3d) | 103 days compared, **23 differ** (> 0.01 pp); **0 reasoned, 23 UNEXPLAINED**; all 7 uncorrected windows miss; all 7 stay open. Reproduced by this seat (the module re-run on the shared tree gives the same per-account counts as the committed record) |

- The differing days are NOT flow-timing days: this seat checked (scratch, counts only) that only 3 of the 23 are flow days and that none stops differing when the served return is relinked under `BD_DEFAULT`. Their sizes run from about 0.03 pp to about 32 pp.
- The worker's measured pattern (not a reason): on 12 of the 23 days the accrual test holds but no correction closes, and Black Diamond's income that day is a whole multiple (3x to 6x) of the served income; on 2 days Black Diamond's flow is 3x or 4x the served flow. No reason of the list has a test that holds on the rest.
- Per account, in plan order (days / differing): 14/9, 44/2, 5/1, 5/1, 21/7, 5/1, 9/2. Row `IRPT_DASHBD-D2-W136-S1` (BLOCKING, hazard INERT) names it in counts and offsets.
- One issuer gap this round, mine: order 168 assumed a firm-neutral series-body helper that the estate does not have; ruled and the order amended @7167440733 (a modification of an existing order, no gate limb graded), the slot re-seated once.

## FWD-8 grade (PRD 11b, at its two grains)

| segment group (90 stored segments, 86 accounts) | window grain (0.35 pp, `BD_DEFAULT`) | day grain |
|---|---|---|
| 76 flow-bearing segments | agree | not graded one by one (11b) |
| 5 flow segments (4 accrued income, 1 flow absent one side) | disagree; reason stated and the window re-closes when corrected (DB-b-167) | NOT day-read |
| 2 no-flow segments | disagree uncorrected; reason stated (accrual), re-closes (DB-b-170) | NOT day-read |
| **7 flow segments, one in each of 7 accounts** | disagree; no window-grain reason (DB-b-167) | **read at day grain: 23 differing days, none with a reason; all 7 windows open (DB-b-169)** |

**Grade: FWD-8 is NOT REALIZED for those 7 accounts** (the 7 windows meet neither clause of 11b). The other 79 accounts are met on the agreement and stated-reason clauses at the grains above. The label and guard clauses are not re-graded here (cited as in round 89; the C-LABEL switch is IRPT_BCKEND's page).
**One reading the CTO owns:** the 7 windows reasoned at window grain (5 flow segments and the 2 no-flow ones) were not day-read; 11b's day-grain clause can be read as satisfied by "correcting that cause re-closes the window" (they do) or as owing a day read. This seat did not decide it.

## For the CTO's next analysis

The 7 stay UNEXPLAINED after the day read. Candidates the data point to, none tested: Black Diamond's income and flow on those days being a multiple of the ledger's (a duplicate or a different booking date in one source), and the 3 flow days. A further closed-list reason, a read of the ledger rows for those 23 days against the series, or a ruling on the 7 are the CTO's.

## Open

- **Ledger leg L7 (mine), carried:** the first scheduled fire after the thresholds swap, 2026-10-14 11:41Z, `checks/l5/l5b_read.py` @88d74f1a63; ledger `irpt-dashbd-thresholds-swap-20261013` stays OPEN until then.
- **Worktrees:** all removed from git; an empty folder `C:/dev/wk-irpt-dashbd-134` remains (a process holds it; no content).
- **Push state:** this seat's commits are LOCAL on box/dell2.

-- 2.0.0_SA_COO~D2
