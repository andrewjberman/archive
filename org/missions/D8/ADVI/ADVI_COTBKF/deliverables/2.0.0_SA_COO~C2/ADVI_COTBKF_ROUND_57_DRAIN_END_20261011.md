# L8 drain end -- ADVI_COTBKF round 57

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~05:2xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB57be1-AC2)

**Counts, hashes, file-and-line citations and reason codes only.** No client account id appears here.

Round 57 was cut as one issuance @25cee5b5d8 on `1.0.0_SA_CTO~DELL2` msg 4061: one read-only measurement, whether a bond's stored
close carries accrued interest for Cottonwood's bond holdings. It does not repeat IRPT_DASHBD.TO-DB-b-116 (@2f0664fab0).

| order | item | assignee | state |
|---|---|---|---|
| CB-be-1 | bond close: clean or dirty; is method row 3's income basis true for bond rows | ~84 | complete @fcea2d04b1, drained @e54f2086f5 |

## The real run, shared tree at e54f2086f5, by the issuer

```
BOND-ACCRUAL-RECORD verdict=DIRTY income_basis_for_bonds=FALSE bonds=0 measured_days=0 sawtooth=81/86 evidence_rows=14
test_cotbkf_no_account_ids.py: 474 tracked files, 0 hits -- 1 passed (the record and its .md are inside this scope)
```

**The issuer re-ran the record's own check line and the id test. It did NOT recompute any count below; they are the worker's.**

## For L9 (CB57be1-AC2, judgment), from ~84's record

Record: `deliverables/0.9.0_WK_ADVI_COTBKF~84/BOND_ACCRUAL_MEASURE.json` and `.md`.

- **Verdict DIRTY, on the coupon-date fall only.** Of 86 testable bonds, 81 fall by 0.6 to 1.4 half-coupons within 4 days of the
  coupon date (median 1.00). Negative arm: 5 of 42 bonds with no coupon date in the window show a fall that large.
  - 184 of 778 Fixed Income CUSIPs have a stored close; 86 were testable; 42 had no coupon date in the window, 53 had no parseable
    coupon or maturity, 3 are zero coupon.
  - The accrual climb between coupons is NOT resolved (slope 0.00046, se 0.00202, against 0.00274 predicted).
  - No field name or documentation string says clean or dirty; the store's rows are labelled `bd_snapshot`.
- **`income_basis_for_bonds` FALSE:** the coupon sits in the price before the pay date, so `cash_when_received` is not true for a
  bond priced from this store.
- **No measured row is affected today.** 0 of 107,316 measured account-days hold a Fixed Income CUSIP. All 141,555 account-days
  that hold one are blank: UNPRICED 141,379, FIRST_DAY 125, DVR_CLOSE_STEP 51.
- **The held set is wider than its list.** 16 Fixed Income CUSIPs are held on the 988 held account-days; the hold list names 3
  (row ADVI_COTBKF-D2-W84-S1).
- **Where value is computed:** `commonwealth_daily_valuation.py:444` (quantity times stored close, merged at `:440`); no par factor
  and no accrued term.

**Not read by the worker, by its own statement:** the gold store's `market_value` and any custodian accrued-interest field; a coupon
cash posting inside the bond-price window (cash interest rows end 2026-06-01). The settling read it names is one bond across one
coupon date in the served store, which is an S3 read outside this order.

**Carried, not decided here:**
- What the CB-al-2 pair may state: the measured rows hold no bond, so the stamp's income basis is not contradicted by any row being
  minted; a bond day that later becomes priced from this store would be. That is the CTO's ruling to make on this record.
- The CB-al-2 pair (the mint and the `dim_return_method` row-3 write) is not re-cut yet.

**Round-close check:** REFUSED on CB57be1-AC2, which is ungraded (yours). Orders 1/1 complete.
