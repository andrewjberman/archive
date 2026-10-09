# L8 drain end -- ADVI_COTBKF round 26

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~02:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile, L9 on three judgment criteria)

Round 26 was cut as one issuance (@fa87b0ca99, `fanout: 2 of 2 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s analysis ADDENDUM 1 (msg 2113).
3 of 3 orders terminal; drains @a9aca322b9 (CB-z-3) and @718291c2c7 (CB-z-1 -> CB-z-2); 0 unmerged worker branches; 0 linked worktrees
for this project. Risk LOCAL: nothing applied.

| order | item | worker | criteria |
|---|---|---|---|
| CB-z-1 | E2: ASF sourced or NO-SOURCE | ~48 | AC1 15 passed; AC2 `regressions=0`; AC3 JUDGMENT, yours |
| CB-z-2 | E1: `method_r26` the default; the non-MATCH census | ~48 | AC1 18 passed; **AC2 FAIL `unexplained=512`**, closed per CTO msg 2213 and NOT amended; AC3 JUDGMENT, yours |
| CB-z-3 | E3: endpoint read, one row per FWD | ~49 | AC1 `fwd_rows=9`; AC2 JUDGMENT, yours |

**Rulings mid-round:**
- **Row W48-S1, ARMED, disarmed the same turn.** The default flip turned one test red, in a file outside CB-z-2's grant. The grant was
  widened @4a4088de98 and the one-line fix landed @1d4ceec9d0 (suite 659 passed, 0 failed; record row W48-S3).
- **CB-z-2's AC2.** It went to the CTO, who ruled "close, graded NOT MET". The closure is recorded @fd2f680497.

## The real runs, shared tree, after the drains (own `--data-dir`)

```
SWEEP-REGRADE ... months_before=3098/886/78609 months_after=3098/886/78609 control_same=True regressions=0 movers_back=138 year_chain_same=True r22_named=25/25
NONMATCH-CENSUS total=82593 match=3098 diff=886 ungradable=78609 classes=10 unexplained=512
pytest data/assets/scripts/silver/tests: 659 passed, 11 skipped
endpoint read (CB26z3-AC1 re-run): fwd_rows=9, realized=4
```

All four are identical to the workers'. The before arm is `method_r25`; the after arm is the new default `method_r26`, equal to it because
ASF is NO-SOURCE.

## What the round found

- **ASF: NO-SOURCE.** There are 6 rows, all in one account (acct#8e3fbc63), dated 2019-01-18..22, netting to 0.00. 3 pair with a same-day
  `ManAltF` reversal; 3 pair with nothing. The CRO's research names ASF on 0 lines. The rule (a document, or every row paired) was fixed
  before the run, so ASF stays internal.
- **The census of all 82,593 graded months:** MATCH 3,098 (3.75%).
  - UNGRADABLE 78,609, every one classed: UNPRICED 74,846, FIRST_DAY 1,533, NON_POSITIVE_BASE 1,173, NO_REPORTED_RETURN 878,
    NO_DAILY_RETURNS 116, REPORTED_SPAN 63.
  - DIFF 886: SWEEP_CASH_LEG 190, INCOME 154, CLIENT_FLOW 30, **unexplained 512**. The 512 are named. In 478 of them no posting
    category's exposure reaches the month's difference; 34 hold no driver row. Valuation-side causes (price, holdings, carried level) are
    the lead.
  - **The dominant fact:** 94.2% of everything that does not match is UNPRICED. Price coverage, not method, now bounds FWD-3.
- **The endpoint read: 4 of 9 REALIZED.** Each row's instrument was run now (`ENDPOINT_READ_20261009.md`):
  - REALIZED: FWD-1 (account history read, traced to the zip), FWD-5 (documents found and opened as PDF), FWD-6 (the coverage
    statement), FWD-8 (the crosswalk: 1,533 rows, 471 MATCHED, every row with a rule or reason).
  - NOT: FWD-2 (the CRM zip is not in the store), FWD-3 (no daily-returns table served), FWD-4 (no CRM tables), FWD-7 (the
    restricted-prefix proof not exercised), FWD-9 (no single read returns a client across a renumbering).
  - **This corrects the "6 of 9" carried since the CTO's round-15 analysis.**
  - Row W49-S1: the local daily-returns file the worker found grades 1,685 MATCH, a stale round-18 output. Nothing is served.
- **Bounds slip (worker ~49, self-reported):** one `manifest.json` was copied to its scratch folder before it switched to streaming
  reads. It was uncommitted and removed with the worktree.

**Rows this round:** W48-S1 (ARMED -> disarmed), W48-S2 (the 512), W48-S3 (S1's fix), W49-S1 (no served returns; stale local file).
ARMED now: 0.

**Round-close check:** REFUSED on three causes, all judgment and yours at L9: CB26z1-AC3, CB26z2-AC3, CB26z3-AC2.

**Round 27, already ruled** (CTO msg 2213):
- E1: trace the 512.
- E2: file the price input for UNPRICED (74,846 months) with dell1's MDPF_DEMQUE queue. Owner `~C2`; a parked hop, never a wait.
- E3: a cell serving FWD-3, which no cell serves today.
