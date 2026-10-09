# L8 drain end -- ADVI_COTBKF round 23

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-08 ~22:2xZ | **For:** `3.0.0_SA_CVO` (L8 compile, L9 on CB23w1-AC3)

Round 23 was cut as one issuance (@2f36abe2ee, `fanout: 1 of 1 chains, cap 8`, a chain of two cells) on `1.0.0_SA_CTO~DELL2`'s
round-22 analysis @4899e3797f (msg 1501). Both orders are terminal: CB-w-1 complete and CB-w-2 WITHDRAWN (refused, CTO msg 1707). The
chain drained once at its end @e0326895c4 (17 of 17 paths, 0 dropped); 0 unmerged worker branches; 0 linked worktrees for this project.
Risk LOCAL: nothing applied.

| order | item | worker | criteria |
|---|---|---|---|
| CB-w-1 | E1: class the 23 regressions; funding credit conditional | ~45 | AC1 23 passed; AC2 `regressions=1` (amendment 3, CTO msg 1618); AC3 JUDGMENT, yours |
| CB-w-2 | E2: dividend and fee cash legs | ~45 | AC1 36 passed; AC2 FAIL `regressions=95` (recorded, never re-graded); WITHDRAWN per CTO msg 1707 |

## The real run, shared tree, after the drain (own `--data-dir`)

```
SWEEP-REGRADE sweeps=2 rejected=517 double_drop_months=8 fixed=0 months_before=2057/1522/79014 months_after=2058/1525/79010 control_same=True regressions=1 movers_back=0
pytest data/assets/scripts/silver/tests: 564 passed, 11 skipped
```

Identical to the worker's line. The arms are v1/`r19` against v1/`conditional` (the default).

## How the round ran -- five runs, four amendments

| run | rule | regressions | round 22's 25 still MATCH | ruled by |
|---|---|---|---|---|
| 1 | CFNCASH-equals-proceeds (the CTO's double-credit lead) | 23 | 25 | -- (lead read 0 of 23) |
| 2 | + (a) sold security valued the day before, + (c) vendor CFNCASH leg of a sweep sale | 1 | 0 | issuer, amendment 1 |
| 3 | (a) replaced by (a'): blank the day (`UNVALUED_FUNDING_SALE`) | 1 | 0 | issuer, amendment 2 |
| -- | accept acct#57e741a5 2025-07 as the one named regression | 1 | 0 | CTO msg 1618, amendment 3 |
| 4 | `divfee` layered (CB-w-2) | 95 | -- | refused; CTO msg 1707 |

- **My amendment 1 was wrong on the 25.** Condition (a) cannot separate a credit that restores the level from one that inflates it. The
  amendment-2 blank changed no verdict: the 2,110 blank days were already blank as UNPRICED. What remains wrong is the cash level
  carried into later months, which a one-day blank cannot reach. The CTO named this the common cause and put it in round 24.
- **The 23 by class:** vendor CFNCASH leg of a sweep sale 13 (acct#05dd4a9d); unvalued funding sale 9; credit kept by every condition 1
  (acct#57e741a5 2025-07, funded by 316067107, the parked core candidate, row D2-S30).
- **Round 22's 25 recovered months are DIFF again** under `conditional` (MATCH 0, DIFF 25, UNGRADABLE 0). This is recorded as the CTO
  ruled.
- **CB-w-2 (`divfee`):** 58 of the 75 trade-day movers came back, but 95 months regressed. `fch` never helped (the months match
  WITHOUT the fee), and dividends gained 46 months and lost 28 on timing. No variant of four reached 0. The CTO stopped rule-adding; the
  default is `conditional`, and `divfee` stays selectable as the record (`deliverables/0.9.0_WK_ADVI_COTBKF~45/divfee/sweep_regrade.md`).

**Rows this round:** W45-S1, S2, S3 (CB-w-1's refusals), W45-S4 (CB-w-2's refusal). OBSERVATION / BLOCKING-cleared by ruling, INERT.
ARMED: 0.

**Round-close check:** REFUSED on one cause only: CB23w1-AC3 UNGRADED (judgment, yours at L9). The withdrawn order is outside the
verdict.

**Round 24 basis** (CTO msg 1710, on the CRO's `RESEARCH_20261008_COMMONWEALTH_TWR_METHOD.md` @35c8aa0d75): advisory fees (`man`,
`ManAltT`, `ManCheck`) are the return drag; `fch` and other charges are flows; every cross-month dividend graded both at pay date and
at ex-date, with the swing printed; sweeps and CFNCASH at par; the year rows chaining the months (4,050 of 4,054) as the control.
Carried-level propagation (CTO msg 1618) also goes into round 24. Cut after the CTO's formal analysis.

**Parked, owner `~C2`:** the ranked price-need list, un-parked by the dell1 data-queue project's L2. **Still external:** that project,
MDPF_SECHIST's Bloomberg leg, the laptop's restricted-statements apply, Andrew's CRM landing; 316067107 PARKED with `1.0.0_SA_CTO~DELL2`.
