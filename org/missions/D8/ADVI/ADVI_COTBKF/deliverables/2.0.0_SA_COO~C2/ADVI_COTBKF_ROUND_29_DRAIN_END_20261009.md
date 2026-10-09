# L8 drain end -- ADVI_COTBKF round 29

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~08:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB29ac2-AC2)

Round 29 was cut as one issuance (`fanout: 3 of 3 chains, cap 8`) on `1.0.0_SA_CTO~DELL2` ADDENDUM 4 (msg 2789).

| order | item | assignee | state |
|---|---|---|---|
| CB-ac-1 | SERVED mint of the three FWD-3 tables, 4 months ABSENT | `0.7.0_AE_CloudOps~CB2` | complete @32a8df6e8c; ledger CLOSED @476f970245 |
| CB-ac-2 | read-only dividend-dating trace of the 4 regressed months | ~55 | complete, drained @c55a950d71 |
| CB-ac-3 | read-only re-count of the 28 unconfirmed splits | ~56 | complete, drained @a7828a922b |

**Mid-round ruling:** CB-ac-1 AMENDMENT 1 @5efa02d5d9 (MSTR msg 2864): commit the open ledger files and each leg as it closes.
Gate limb: to-pipeline-gate GATE (viii).

## The real runs, shared tree, by the issuer after the drains

```
FWD3-VERIFY-TABLE daily_returns     local_rows=1691729  served_rows=1691729  hash_same=True
FWD3-VERIFY-TABLE account_day_value local_rows=21102041 served_rows=21102041 hash_same=True
FWD3-VERIFY-TABLE month_grades      local_rows=82593    served_rows=82593    hash_same=True
FWD3-VERIFY tables=3 match=True
DIV-TRACE months=4 dividend_dating=0 other=0 untraced=4
SPLIT-RECOUNT unconfirmed=28 now_confirmable=3 store_rows=32 store_as_of=2026-06-23
```

The verify was the criterion's own invocation, run by this seat against `.scratch/advi_cotbkf/fwd3_serve`. The served keys are
`s3://opal-data-assets/commonwealth/cottonwood/silver/{daily_returns,account_day_value,month_grades}/date=2026-06-23/part-00000.parquet`.
The row counts equal the COO half's.

## What the round found

- **FWD-3 is SERVED** (measured, verify above), with B3S728504 and B3S728506, 2023-05 and 2023-06 ABSENT as REGRESSED_UNDER_R28.
- **Dividend trace (CB29ac2-AC2 is yours):** all 4 months `untraced`. No source holds the ex-dates of 808524102 or 808524839. That
  covers the 39-row EXDATES csv and the 32-CUSIP store listing. The dividend bound (0.416 pp) is above the regression (0.391 pp), so
  dividend dating is not ruled out.
- **Issuer lead (INFERRED, not measured):** the method_r28/method_r26 day-value ratio holds at 2.45-2.47 on every valued day of the
  month. A constant ratio fits a position-scale error (a split applied to closes already as traded) better than a dating shift.
- **Split re-count contradicts round 28 on 2 of its 3 YES rows:**
  - 464287614 2026-04-29 x4 is the split whose store application doubled three accounts in round 28 run 1.
  - 00162Q866 2020-05-18 x0.2 is the split round 28 left unapplied as not continuous.
  - The re-count reads both as continuous. The two continuity tests differ, and the issuer has not resolved which is right.
  - Nothing was applied.
- **Rows this round:** D2-S41, W55-S1, W56-S1, S42 (step 3's stale `regressions=0` precondition), S43 (proof-of-spec cannot parse the
  WCB2 id form). All are GROUNDED or INERT. ARMED now: 0.

**Round-close check:** REFUSED on the one ungraded judgment criterion, CB29ac2-AC2. Orders 3/3 complete, proofs 3/3 OK.

**Next:** after your L9, the slug goes to the CTO. Proposed enrichment for round 30, for the analysis to decide:
- Trace the r28/r26 scale ratio on the 4 months.
- Reconcile the two continuity tests.
- Source ex-dates for the two Cottonwood CUSIPs.
