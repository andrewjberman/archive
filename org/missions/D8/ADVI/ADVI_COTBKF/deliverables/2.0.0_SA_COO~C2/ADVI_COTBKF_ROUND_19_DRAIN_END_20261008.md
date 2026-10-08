# L8 drain end -- ADVI_COTBKF round 19

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-08 ~17:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile, L9 on CB19s1-AC3)

Round 19 was cut as one issuance (@c954f11b92, one cell) on `1.0.0_SA_CTO~DELL2`'s round-18 analysis @04b347e9ea (msg 1237,
the ruling "sweep vehicles are cash"). 1 of 1 order terminal and merged; proof VALID; 0 unmerged worker branches; 0 linked
worktrees for this project. Risk LOCAL: nothing applied, nothing served moved.

The dell2 reboot at 16:38Z killed worker ~40 mid-order with uncommitted work. It was respawned into the same worktree at
~17:0xZ and finished from the state it left; no work was redone from scratch and no criterion changed.

| order | item | worker | drain | criteria |
|---|---|---|---|---|
| CB-s-1 | the FDIC sweep is cash: declared list, sweep buys/sells INTERNAL, re-grade | ~40 | @bf424e274b | AC1 8 passed (silver suite 500 passed, 11 skipped); AC2 control_same=True; AC3 JUDGMENT, yours |

## The real run, shared tree, after the drain

```
SWEEP-REGRADE sweeps=2 rejected=517 double_drop_months=74 fixed=42 months_before=1685/1931/78977 months_after=2057/1522/79014 control_same=True
```

Identical to the worker's line. The before arm reproduces round 18's MONTHLY-GRADE exactly (the control on the chain).

## What the item found

- **The declared list** (`commonwealth_sweeps.py`, `SWEEP_LIST_VERSION` sweeps-v1-20261008), source = the vendor's
  `Security_Description` as delivered:
  - FDIC66606 "Bank Deposit Sweep Program" (143,357 transaction rows, 708 accounts)
  - FDIC66853 "Advisory Retirement Sweep Program" (80,939 rows, 391 accounts)
  - CFNCASH stays cash, not a sweep. `commonwealth_crosswalk.is_cash` untouched.
- **Rejected candidates:** 517 of 520 flagged CUSIPs, each with its reason (CD 279, cash-merger wording 61, bank issuer 33,
  money-market fund 22, UIT "Cash" distributions 18, insured munis 4, Pershing government cash management 2, Pacer Cash Cows ETF 1);
  0 flagged CUSIPs unaccounted. **AC3 asks you whether any of these should have been on the list** -- the money-market
  funds and the Pershing cash-management pair are the ones to read.
- **The 74 double-drop months:** reproduced exactly under the value-drop rule (|drop - 2x|flow|| within 1% of |flow| + 0.05).
  42 now MATCH; the rest stay DIFF or go UNGRADABLE (blank, never filled). 68 of 74 pair with a same-day, same-amount sweep
  sale; the other 6 were funded partly by a non-sweep money-market fund (e.g. Fidelity Government Cash Reserves), which stays
  rejected under the ruling.
- **Whole grade:** MATCH 1,685 -> 2,057; DIFF 1,931 -> 1,522; UNGRADABLE 78,977 -> 79,014.
  - Moves: DIFF->MATCH 543, **MATCH->DIFF 163**, DIFF->UNGRADABLE 31, MATCH->UNGRADABLE 10, UNGRADABLE->graded 4.
- **Control:** 642 of 642 graded months of accounts with no listed-sweep row on or before the month are unchanged. The literal
  in-month reading (919 months) moved 158, all in accounts that traded a sweep earlier (the cash leg persists); the report prints
  both readings.

**Rows this round:** D2-S29 (OBSERVATION / INERT) @505036461c -- the 163 MATCH->DIFF months are unexplained. ARMED: 0.

**Round-close check:** `round-close-check.py --project ADVI_COTBKF --round 19` -> REFUSED on one cause only: CB19s1-AC3 UNGRADED
(judgment, yours at L9). Orders 1/1 complete, proofs 1/1 ok.

**Enrichment candidates for the round-19 analysis** (the CTO's to list):
1. Class the 163 MATCH->DIFF months (D2-S29) before the next repair.
2. The 6 money-market-funded withdrawals: whether a non-sweep cash vehicle that pays a withdrawal needs its own ruling.
3. Carried: the `ZERO_BASE` prose in `commonwealth_flow_timing.py:188`.

**Still external:** MDPF_SECHIST's price load (FWD-3 coverage), the laptop's restricted-statements apply, and Andrew's CRM landing.

Deliverables: `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~40/sweep_regrade.md` and the proof instance beside it.
