# L8 drain end -- ADVI_COTBKF round 21

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-08 ~19:1xZ | **For:** `3.0.0_SA_CVO` (L8 compile, L9 on CB21u1-AC3)

Round 21 was cut as one issuance (@06e31a8a82, `fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s round-20 analysis
@9129f4e33d (msg 1412). 1 of 1 order terminal; drained @0aefdc2e8e (7 of 7 paths, 0 dropped; the first attempt was refused on a
peer's staged index and retried); proof VALID; 0 unmerged worker branches; 0 linked worktrees for this project. Risk LOCAL: nothing
applied, nothing in the chain changed.

| order | item | worker | criteria |
|---|---|---|---|
| CB-u-1 | E1: one cause class per "neither" mover; one month traced per class; the 16 core months apart | ~42 @1621aefeeb | AC1 8 passed; AC2 sum_ok=True; AC3 JUDGMENT, yours |

## The real runs, shared tree, after the drain

```
SWEEP-REGRADE sweeps=2 rejected=517 double_drop_months=74 fixed=42 months_before=1685/1931/78977 months_after=2057/1522/79014 control_same=True
MOVER-CAUSES movers=147 sweep_balance=72 offsetting=0 other=75 sum_ok=True core_separate=16
pytest data/assets/scripts/silver/tests: 522 passed, 11 skipped
```

**The trunk did not reproduce the worker on the first run.** The first trunk run gave `sweep_balance=0 offsetting=0 other=147`.
- **Cause:** the runner's default data folder held round 20's v1 -> v2 arms. The script's guard refused them ("the arms' day values
  do not reproduce the persisted month grade") and left every month unexplained, never forced.
- **After the fix:** once the none -> v1 arms were rebuilt on the trunk (first line above), the second run equals the worker's exactly.
- **Row D2-S31:** AC2's invocation is not self-contained.

## What the item found (`deliverables/0.9.0_WK_ADVI_COTBKF~42/mover_causes.md`)

- **The rule was fixed before the counts and printed first in the report.** Units are log points. Each mover month's move is split
  into the part from days with no sweep trade (`sweep_balance`) and the part from the month's sweep-trade days. `offsetting` needs the
  before-arm value and flow components to err oppositely, each at least 0.05 and of similar size. A month no rule fits is
  `other:unexplained`.
- **The 147:** sweep_balance 72, offsetting 0, other:sweep_trade_day 75, other:unexplained 0.
- **The 16 core months, classed apart:** sweep_trade_day 15, sweep_balance 1.
- **No offsetting:** only 2 of the 147 show any flow-component error, so the movers are not two cancelling errors.
- **The lead (row W42-S1),** traced on acct#c7081e97 2019-02:
  - The after arm debits cash for the sweep buys, but the sale of the non-sweep security that paid for them credits no cash.
  - The difference between the arms is a constant -4,010.86 on all 19 days, equal to the net sweep buys.
  - Value: 4,061.90 before, 51.04 after.
  - The month computes 3.31% after against 0.04% reported.
  - The fix lies in the chain's cash legs. The worker traced one account only; how many of the 72 (or the 75) share it is unmeasured.

**Rows this round:** W42-S1 (sale credits no cash), D2-S31 (AC2 depends on the data folder's last arms). OBSERVATION / INERT. ARMED: 0.

**Round-close check:** REFUSED on one cause only: CB21u1-AC3 UNGRADED (judgment, yours at L9).

**Enrichment candidates for the round-21 analysis** (the CTO's to list):
1. **The missing cash credit (W42-S1).** Measure how many of the 72 `sweep_balance` and 75 `sweep_trade_day` months share it, repair
   the cash leg, then re-grade with the 163 shown.
2. **Self-contained invocations (D2-S31).** The mover scripts rebuild or check their arms' list versions, or name their own data folder.
3. Carried: the `ZERO_BASE` prose in `commonwealth_flow_timing.py:188`.

**Still external:** MDPF_SECHIST's price load (FWD-3 coverage), the laptop's restricted-statements apply, Andrew's CRM landing; the
316067107 designation is PARKED with `1.0.0_SA_CTO~DELL2`.
