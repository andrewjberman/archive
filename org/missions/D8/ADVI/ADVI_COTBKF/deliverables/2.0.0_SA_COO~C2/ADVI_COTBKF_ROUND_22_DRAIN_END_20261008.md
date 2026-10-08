# L8 drain end -- ADVI_COTBKF round 22

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-08 ~19:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile, L9 on CB22v1-AC3)

Round 22 was cut as one issuance (@386c7f1431, `fanout: 2 of 2 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s round-21 analysis (msg
1449; ruling on D2-S32). 2 of 2 orders terminal and drained; proofs VALID; 0 unmerged worker branches; 0 linked worktrees for this
project. Risk LOCAL: nothing applied.

| order | item | worker | drain | criteria |
|---|---|---|---|---|
| CB-v-1 | E1: cash-leg repair -- a non-sweep sale funding a sweep buy credits cash; re-grade | ~43 | @4839b6f2d2 | AC1 9 passed (mutant: 3 fail); AC2 control_same=True; AC3 JUDGMENT, yours |
| CB-v-2 | E2: mover scripts name their data folder, refuse a list-version mismatch | ~44 | @c0f717a5c9 (first attempt waited on a peer's open merge) | AC1 6 passed; existing mover tests 17 passed |

## The real run, shared tree, after the drains (own `--data-dir`)

```
SWEEP-REGRADE sweeps=2 rejected=517 double_drop_months=8 fixed=0 months_before=2057/1522/79014 months_after=2103/1520/78970 control_same=True
pytest data/assets/scripts/silver/tests: 537 passed, 11 skipped
```

Identical to the worker's line. The arms are v1 with the round-19 cash leg (`r19`) against v1 repaired.

## What the round found

- **The repair** (`commonwealth_sweeps.py`):
  - New `funding_credit_rows`, called from `with_sweep_cash`.
  - It credits CFNCASH, for each account and trade date with a listed-sweep buy, the smaller of (a) the day's non-sweep sale proceeds
    and (b) the day's sweep buy.
  - No account is named. A null Amount credits nothing, and a missing Amount column is refused.
  - The runner selects the rule per arm (`--before-cash-leg` / `--after-cash-leg`); `r19` reproduces round 19's verdict on 163 of 163.
- **The ruling's prediction did not hold: the two classes did NOT collapse together.**

  | movers | back to MATCH |
  |---|---|
  | `sweep_balance` | 25 of 72 |
  | `other:sweep_trade_day` | 0 of 75 |
  | `core` | 0 of 16 |
  | all movers | 25 of 163 |

  - The traced D49141714 2019-02 returned to MATCH; RGY005018 2024-12 is still DIFF (-8.8079 vs -8.02).
  - All 138 remaining movers are named in `deliverables/0.9.0_WK_ADVI_COTBKF~43/sweep_regrade.md`.
- **A second mechanism (row W43-S1):** dividend rows (cash in) fund sweep buys, and fee rows `man`/`fch` (cash out) are paid by sweep
  sales, with no matching cash leg.
  - Of the 122 `neither` movers still DIFF, 94 carry such a row on a sweep-trade day.
  - No non-sweep sale falls on a sweep-trade day inside any of the 147 `neither` months, so the 25 that returned are carried-balance
    months.
- **Regressions:** 23 months moved MATCH -> DIFF between the arms, 19 of them in accounts 0QF879130 and 0QF879352. They are named, and
  their cause is not measured.
- **Whole grade:** MATCH 2,057 -> 2,103; DIFF 1,522 -> 1,520; UNGRADABLE 79,014 -> 78,970. The control is 642 of 642 unchanged.
- **E2:** both mover scripts check the list version recorded in the persisted grades and refuse a mismatch:
  `refused: BEFORE arm records list version sweeps-v1-20261008 but expected none (none)`.
  - `commonwealth_mover_causes.py` now requires `--data-dir`.
  - **Gap (row D2-S33):** the day parquet records no list version, so D2-S31's actual case (right grades, stale day values) still passes
    the check and is caught only by the reproduce guard.

**Rows this round:** W43-S1 (dividend/fee cash legs), D2-S33 (the version check cannot see the day parquet). OBSERVATION / INERT.
ARMED: 0.

**Round-close check:** REFUSED on one cause only: CB22v1-AC3 UNGRADED (judgment, yours at L9). Orders 2/2 complete.

**Enrichment candidates for the round-22 analysis** (the CTO's to list):
1. **The dividend and fee cash legs (W43-S1):** a dividend that funds a sweep buy credits cash; a fee paid by a sweep sale debits cash.
   Re-grade with the 138 remaining movers shown.
2. **The 23 regressions:** cause by month, 19 sit in two accounts.
3. **D2-S33:** the runner stamps the list version and cash-leg rule into the day parquet, and the mover scripts check it.
4. **Carried from the CRO's backfill research** (@e112184d3b, rec 4): a NAME match against the Black Diamond set in the crosswalk,
   before the P3 "gone client" tier is treated as final.
5. Carried: the `ZERO_BASE` prose in `commonwealth_flow_timing.py:188`.

**Parked, owner `~C2`:** the ranked price-need list for the dell1 backfill data-queue project. It is a file at a fixed path with its
key namespace stated, and un-parks when that project's L2 is cut (CTO msg 1495).

**Still external:** the dell1 backfill data queue (Yahoo, Andrew's ~19:1xZ word for the Dell boxes), MDPF_SECHIST's Bloomberg leg, the
laptop's restricted-statements apply, and Andrew's CRM landing. The 316067107 designation is PARKED with `1.0.0_SA_CTO~DELL2`.
