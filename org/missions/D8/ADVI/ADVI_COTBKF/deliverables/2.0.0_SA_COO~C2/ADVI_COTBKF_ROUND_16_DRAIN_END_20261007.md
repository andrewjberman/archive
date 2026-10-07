# L8 drain end -- ADVI_COTBKF round 16

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-07 ~20:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

Round 16 was cut as one issuance (@b76a9b5088, `fanout: 3 of 3 chains, cap 8`) on `1.0.0_SA_CTO~DELL2` msg 999 (yes to pulling FWD-3
steps 2-4 forward, built against stub prices). 3 of 3 orders terminal and merged; proofs VALID; 0 unmerged worker branches; 0 linked
worktrees for this project.

| order | worker | drain | criteria (worker's run) |
|---|---|---|---|
| CB-p-1 daily valuation | ~32 | @b07434a3f5 | VALID: AC1 11 passed; AC2 real run (below) |
| CB-p-2 daily return + FLOW table | ~33 | @319769d04e | VALID: AC1 13 passed; AC2 `DAILY-RETURNS account_days=3 computed=2 blank=1 flow_types=61 of 61 stub=True` |
| CB-p-3 monthly grade | ~34 | @9884c4bd5d | VALID: AC1 8 passed; AC2 `MONTHLY-GRADE months=3 match=1 diff=1 ungradable=1 tolerance_pct=0.05 stub=True` |

The ~32 drain conflicted only on the append-only channel; resolved as HEAD plus the W32-S1 row appended (git had split it across the
W33 rows), graded by `safe-merge --continue`.

## The round's real run: the whole chain on Opal's data, shared tree, after the drain

```
DAILY-VALUATION accounts=1533 account_days=1691729 complete=132132 holding_days=22547096 priced=6560170 blank=1559597 sources=cottonwood-silver-canonical-prices,cottonwood-gold-canonical-holdings,etfs-bbg-testpull-ticker-history,cash-at-par
DAILY-RETURNS account_days=1691729 computed=127300 blank=1564429 flow_types=61 of 61
MONTHLY-GRADE months=82593 match=1947 diff=2284 ungradable=78362 tolerance_pct=0.05
```

Identical to the issuer's earlier run from the three worktrees. The tolerance (0.05 percentage points) was fixed in the order and in
code before either run.

**What it says.**
- **Prices are the binding gap.** Only 7.8% of account-days are fully priced (29.1% of holding-days), so 92.6% of months are
  UNGRADABLE: every one has a blank day, and none is filled. Blank reasons: UNPRICED 1,560,217; ZERO_BASE 2,578; FIRST_DAY 1,533;
  FLOW_UNVALUED 101.
- **Where a month is fully priced, the chain works without flows.** Of 4,231 graded months over 280 accounts, the 3,093 with no
  external flow MATCH 1,675 times (median |diff| of the DIFFs 0.35 points).
- **Flow months are off.** 866 of 1,138 flow months DIFF, median |diff| 7.4 points (row D2-S28): the flow convention or a flow class,
  not the prices.
- **Amount census (answers W33-S1).** Amount is unsigned on the in/out types and negative on ftax/stax, so the worker's direction x
  |Amount| is right. But security transfers mostly carry Amount 0 (lo 18,157; trco 147 of 147), so after the price load those days
  would blank (row D2-S27).

**Rows.** New this round, all OBSERVATION / INERT:
- W32-S1: the census reader drops the price column; within-store price conflicts are left unpriced.
- W33-S1: the sign of Amount (answered by the census above).
- W33-S2: Amount was absent from the shared loader projection.
- D2-S27: zero-Amount security transfers.
- D2-S28: flow months DIFF.

ARMED: 0.

**Enrichment candidates for the round-16 analysis** (the CTO's to list):
1. Value a zero-Amount security flow at quantity x the same-day close (D2-S27).
2. Grade flow months under start-of-day vs end-of-day flows and tax withholding internal; keep the better convention (D2-S28).
3. The page-count gap in the document index (D2-S26).

**Still external:**
- MDPF_SECHIST's price load: the FWD-3 real run then needs only `--sechist <prefix>` on step 2.
- The laptop's restricted-statements apply, then Andrew's CRM landing (FWD-2, FWD-4, FWD-7).
