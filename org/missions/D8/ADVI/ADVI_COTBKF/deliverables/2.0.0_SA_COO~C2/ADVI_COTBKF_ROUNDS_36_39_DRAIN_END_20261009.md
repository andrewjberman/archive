# L8 drain end -- ADVI_COTBKF rounds 36 and 39

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~14:0xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB36aj1-AC2 and
CB39am1-AC2)

Two rounds are terminal and packed together. Round 38 stays open: CB-al-2 is HELD on row W66-S1, disarmed by S63 @5eaa4b6191, with the
producer gap routed to the CTO. Round 40 (`source_firm`, ~68) is running.

| round | order | item | assignee | state |
|---|---|---|---|---|
| 36 | CB-aj-1 | build the 38 cot price files without the 49F rows; per-key diff; writer census | ~64 | complete, drained @370c142ec0 |
| 36 | CB-aj-2 | write them as new versions under a pair | `0.7.0_AE_CloudOps~CB2` | complete; report @e5eb80c75f; ledger CLOSED (5 legs) |
| 39 | CB-am-1 | cot gold `_ff_worker` stamps a claim on every carried price; never carries a foreign-firm price | ~67 | complete @440ee24cba (test alone first, f8b656af51), drained @88e7452955 |

## The real runs, shared tree, by the issuer

```
COT-PRICE-REWRITE keys=38 rows_removed=1734 rows_repriced=0 other_rows_identical=True bonds_priced=0/3 writers=7 scheduled=0
COT-PRICE-REWRITE-VERIFY keys=38 match=38/38
pytest data/cot/scripts/gold/tests/test_b00_ff_carry_claim.py: 3 passed
pytest data/cot/scripts/gold/tests: 31 passed
```

The verify is the issuer's own read of the 38 served keys against the manifest, at ~14:0xZ.

## What the rounds delivered

**Round 36 -- 49 Financial's rows are out of Cottonwood's price store** (CTO ADDENDUM 10: rewrite, not delete).
- 38 keys in `opal-data-cot` carry new versions. 1,734 rows were removed: 111 across 37 daily files, and 1,623 in the store.
- Every other row is byte-identical (38/38). No bond-specific Yahoo series exists, so the three bonds now read UNPRICED.
- All 38 prior versions are kept and retrievable; deleting them is Andrew's act.
- The pair's conditions:
  - 1 per key: met.
  - 2: MET per the CTO half AMENDMENT 1 @fa3cabc1ea; D2-S60 disarmed.
  - 3: MET (`B_00` gives NaN on a price miss; the next gold run moves 99 account-days of the Wells Fargo bond to NaN).
  - 5: met.
- **Condition 4 is the issuer's watch item:** at the next manual silver-prep, 0 rows may come from any 49F input for the three CUSIPs.
  A re-injection reopens D2-S52.

**Round 39 -- the carry-forward is no longer silent.** `_ff_worker` (+25/-1 lines, nothing else changed) stamps every row with:
- `price_basis` (`same_day` / `carried_forward` / `not_carried_foreign_source`);
- `price_source_date`;
- `source_firm`, carried from the prior row, reading `absent` when the prior has none.

A prior price whose `source_firm` is present and is not Cottonwood is never carried; its price is NaN, never zero. The firm key comes
from `opal_naming.lookup`, because the naming gate refused typed tokens. The rule keys on the FIELD per ADDENDUM 12. **Not deployed:** shipping
the gold script to the cot code mirror is a later SERVED cell under its own pair.

**Disclosures:**
- ~67's test-alone commit lacked some names in its exec namespace (`np`, `os`, `sys`, `__file__`), fixed in the change commit. The
  test-alone commit still failed at the base for the intended reason (KeyError `price_basis`).
- ~67 notes that a cash-like asset with a foreign prior reads null after `price_holdings` forces 1.0.
- ~64's runs 1-2 hit a key-parse and a census over-match, fixed before the recorded run 3. The Yahoo rule and the diff rule are
  unchanged.

**Rows:** W64-S1 (BLOCKING; the bonds' source, ruled by the CTO and measured in round 37 as UNPRICED), W64-S2. ARMED: 0.

**Round-close checks:** rounds 36 and 39 are each REFUSED on their one ungraded judgment criterion (CB36aj1-AC2, CB39am1-AC2).
