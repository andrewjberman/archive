# L8 drain end -- ADVI_COTBKF round 17

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-08 ~00:3xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

Round 17 was cut as one issuance (@1690130138, `fanout: 2 of 2 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s round-16 analysis
@8b6829c89f (msg 1100). 3 of 3 orders terminal and merged; proofs VALID; 0 unmerged worker branches; 0 linked worktrees for this
project.

| order | item | worker | drain | criteria |
|---|---|---|---|---|
| CB-q-3 | E3 page counts | ~36 | @b4018f97a0 | VALID: AC1 5 passed; AC2 below |
| CB-q-1 | E2 zero-Amount transfers | ~35 | @02c971e765 (chain end) | VALID: AC1 10 passed; AC2 below; AC3 JUDGMENT, for the CVO |
| CB-q-2 | E1 flow timing | ~35 (fresh session; the first could not be resumed) | @02c971e765 | VALID: AC1 8 passed; AC2 below |

Both drains conflicted only on the append-only channel. Each was resolved as HEAD plus the branch's appended rows, after checking
that the branch only appended and that no row id collided. `safe-merge --continue` graded the result.

## The real runs, shared tree, after the drains

```
PAGE-COUNTS documents=11119 counted=11087 unreadable=32 listing_none=10085 listing_zero=1034 listing_positive=0 cause=absent
DAILY-VALUATION accounts=1533 account_days=1691729 complete=132132 holding_days=22547096 priced=6560170 blank=1559597 sources=...
DAILY-RETURNS account_days=1691729 computed=127396 blank=1564333 flow_types=61 of 61 zero_amount=20403 valued=5017 blank_no_price=15386
MONTHLY-GRADE months=82593 match=1973 diff=2264 ungradable=78356 tolerance_pct=0.05
```

The worker's side-by-side (`deliverables/0.9.0_WK_ADVI_COTBKF~35/flow_timing.md`):
`FLOW-TIMING flow_months=937 end_match=242 start_match=241 end_diff_median=6.3111 start_diff_median=6.6653 control_months=2676 control_same=True chosen=end`

## What each item found

- **E3, page counts (D2-S26 answered).** The cause is that the listings never carry a page count: 10,085 have no field or a
  non-number, 1,034 carry "0", 0 carry a positive count. The index copies only that field. Read from the PDFs themselves:
  - 11,087 of 11,119 documents counted;
  - 32 unreadable, each null with its reason (31 not a PDF, 1 encrypted).

  Row W36-S1: 13 REPR listings hold a non-number. **The served index is unchanged.** Filling it means making the index builder read
  pages from the PDF, then re-applying under a never-widen pair. That is the next item.
- **E2, zero-Amount transfers (D2-S27 answered).** Of 20,403 zero-Amount flow rows, 5,017 are now valued at quantity x the same-day
  close and 15,386 stay blank for no price. On today's prices only 6 months move from UNGRADABLE to graded, all DIFF (row W35-S1).
  The worked month for the CVO: acct#e29efebe 2025-09, an `lo` of 21 shares at 508.037384, which went from UNGRADABLE to DIFF
  (0.7664 against a reported 0.84).
- **E1, flow timing (D2-S28 answered: timing is not the cause).** Start and end of day differ by one MATCH on 937 flow months.
  The no-flow control is identical under both. End is kept.
  - **Tax withholding moved to INTERNAL.** With `ftax`/`stax` (4,324 rows) internal, flow-month MATCH rises 216 -> 242. MATCH over
    all months rises 1,947 -> 1,973.
  - **Row W35-S2.** The start rule blanks a non-positive base. 26,903 days follow a negative prior-day value (short positions or a
    negative cash sweep), which the end rule computes. Whether a negative base should read blank under end too is the CTO's ruling.

**Flow months still mostly DIFF** (242 of 937 MATCH, median |diff| 6.3 points), while no-flow months MATCH 1,440 of 2,676 (median
0.32). Timing and tax are ruled out. What remains: a flow's size, a type the FLOW table treats as internal, or Commonwealth's own
flow method. An account-level read of a few DIFF flow months against their transactions would name which.

**Rows this round** (all OBSERVATION / INERT): W35-S1, W35-S2, W36-S1. ARMED: 0.

**Enrichment candidates for the round-17 analysis** (the CTO's to list):
1. **Page counts into the served index.** The builder reads pages from the PDF, then the index is re-applied (SERVED, never-widen
   pair).
2. **Flow-month DIFFs.** Trace 5-10 DIFF flow months against their transactions and name the cause.
3. **The negative-base ruling** (W35-S2).

**Still external:** MDPF_SECHIST's price load (FWD-3 coverage), the laptop's restricted-statements apply, and Andrew's CRM landing.
