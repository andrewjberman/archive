# L8 drain end -- ADVI_COTBKF round 34

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~12:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB34ah1-AC2 and
CB34ah2-AC3; the re-mint's grade opens the CTO's reader gate)

Round 34 was cut as one issuance @9135ec68a8 (`fanout: 2 of 3 chains now, cap 8`) on `1.0.0_SA_CTO~DELL2` ADDENDUM 9 @cf58046f35 (msg
3180). Its follow-ons were cut as rounds 35 (@39c76740e9, drained) and 36 (@35931777b7, running).

| order | item | assignee | state |
|---|---|---|---|
| CB-ah-1 | read-only code trace of `bd_txn_price`'s writer | ~61 | complete @33b729fc1b, drained @248cb44fa0 -- `class=cross_firm` |
| CB-ah-2 | as-traded price basis in the chain; local rebuild and re-grade | ~62 | complete @1fd8b6113f, drained @6df94d0218 |
| CB-ah-3 | SERVED re-mint of the three FWD-3 tables, as-traded, three bonds held | `0.7.0_AE_CloudOps~CB2` | complete; report @20e7c39855; ledger CLOSED (5 legs) |

**Mid-round rulings:**
- **The COO half** was given @64b302f3a8, marked superseded on ADDENDUM 10 (the rewrite sequencing), and reinstated @e075588a6c on the
  CTO half (msg 3271): the held bonds make the re-mint independent of the 38-key rewrite.
- **CB-ah-3 AMENDMENT 1** @513fcb47f3 released the order: apply the issuer's held build AS BUILT. The run_commit is part of the table
  content.
- **CB34ah2-AC2's bar** was re-anchored on the builder's own `FWD3-BUILD daily_rows=` line (to-pipeline-gate GATE ix). The
  `price_basis=as_traded` check is read under AC3.

## The real runs, shared tree, by the issuer

```
BD-TXN-TRACE writer=data/black_diamond/scripts/silver/inject_scoped_overrides.py:136 inputs=3 outputs=1 class=cross_firm
SWEEP-REGRADE ... months_before=3133/838/78622 months_after=3678/293/78622 control_same=False regressions=5 movers_back=155 year_chain_same=True r22_named=25/25 dividend_both=NA price_basis_before=store price_basis_after=as_traded
FWD3-BUILD ... run_commit=6f70d5cc01bb ... absent_months=5 price_basis=as_traded absent_reason=REGRESSED_UNDER_AS_TRADED hold_cusips=3 held_account_days=988
FWD3-VERIFY-TABLE daily_returns     local_rows=1691729  served_rows=1691729  hash_same=True
FWD3-VERIFY-TABLE account_day_value local_rows=21102041 served_rows=21102041 hash_same=True
FWD3-VERIFY-TABLE month_grades      local_rows=82593    served_rows=82593    hash_same=True
FWD3-VERIFY tables=3 match=True
```

The verify was run by this seat at ~12:5xZ. The served versions after the re-mint (`head-object`) are:
- `daily_returns`: `w9j5YeV1LnNIakNlRTBX6jW1.SDHqmJR` (12:41:01Z);
- `account_day_value`: `qIWjLLwCIh_Gx6IblSgyaint2tfJ37pr` (12:41:02Z);
- `month_grades`: `QI5Ks8vQwGTwnc9ekyh.DOsyN8PKN3PB` (12:41:03Z).

The prior versions named in the pair stay retrievable, which is the rollback.

## What the round delivered

**FWD-3 is served on the as-traded basis** (ADDENDUM 8's ruling): the dividend-adjusted closes are replaced by Yahoo `Close` for
911 tickers, with interpolated days re-derived.

| grade | store basis | as-traded |
|---|---|---|
| MATCH | 3,133 | 3,678 |
| DIFF | 838 | 293 |
| UNGRADABLE | 78,622 | 78,622 |

- The round-28 four ABSENT months (B3S728504/06, 2023-05/06) now MATCH.
- SCHB and SCHZ on 2022-10-12 equal the round-31 Yahoo evidence exactly (41.94 / 44.93). Nothing was tuned.
- **5 new regressions read ABSENT** (`REGRESSED_UNDER_AS_TRADED`), each with a named row: D2-S53 0QF878956 2022-03, S54 0QF878956
  2022-08, S55 B3S793726 2026-03, S56 D49151054 2021-07, S57 D49151054 2021-10. Their causes are untraced. The two D49151054 months
  move by about 0.6 pp, the largest.
- **The three 49F bonds are held:** 988 account-days blank, `HELD_SOURCE_UNDER_REVIEW` (CB-ah-1 `cross_firm`; round 35 traced the
  route; round 36 rewrites the cot keys).

**Carried, not decided here:**
- `control_same=False` on the re-grade line is uninvestigated.
- W62-S2: 3,962 interpolated days blank where they lay outside a ticker's Yahoo points. 36 priced holding-days are lost.
- 98 tickers stay on the store price (81 `other`, 17 `no_yahoo`).
- **The CTO's reader gate stays closed** until this round is graded.

**Rows:** W61-S1 (BLOCKING, answered by rounds 35/36), W62-S1, W62-S2, D2-S53..S57. ARMED: 0.

**Round-close check:** REFUSED on the two ungraded judgment criteria, CB34ah1-AC2 and CB34ah2-AC3. Orders 3/3 complete.
