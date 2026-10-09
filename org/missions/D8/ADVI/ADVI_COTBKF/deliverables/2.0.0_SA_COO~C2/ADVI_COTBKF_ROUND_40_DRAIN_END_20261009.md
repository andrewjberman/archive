# L8 drain end -- ADVI_COTBKF round 40

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~14:2xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB40an1-AC2)

Round 40 was cut as one issuance @8a50861034 (`fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2` ADDENDUM 12 @7d33a8581d (msg
3390), the ruling on D2-S62: the cross-firm test keys on a `source_firm` FIELD, never a token.

| order | item | worker | state |
|---|---|---|---|
| CB-an-1 | `source_firm` on every cot price row, from its input's address via the registry; the rewrite census reads it | ~68 | complete @ff17e59776 (test alone first, eb13fd505d), drained @ba35c04d1c |

## The real runs, shared tree, by the issuer

```
pytest data/cot/scripts/gold/tests/test_canonical_prices_source_firm.py: 5 passed
pytest data/cot/scripts/gold/tests: 36 passed
SOURCE-FIRM-CENSUS keys=38 rows=11671939 cottonwood=0 BREACH=0 absent=11671939 keys_BREACH=0 keys_NOT-CLEAN=38 keys_CLEAN=0
```

The worker's run also gave `data/assets/scripts/silver/tests`: 725 passed, 11 skipped.

## What the round delivered

- **The cot price writer** `build_canonical_prices_v2.py` now stamps `source_firm` after `source` on every row. The firm is resolved
  from the input's bucket and key prefix through the registry (`opal-data-cot` is a bucket alias of the cottonwood scope).
  - An unknown bucket stamps `absent` and is never defaulted.
  - Interpolated rows take their endpoints' firm: `mixed` if the endpoints differ, `absent` if either endpoint is absent.
- **The census on today's 38 keys** reads every row `absent` (`NOT-CLEAN`): the column does not exist yet, as expected. It arrives with
  the next silver-prep, under its own pair (ADDENDUM 12). D2-S62 closes when that run's census reads `cottonwood` with `BREACH=0`.
- **Not deployed.** Shipping `build_canonical_prices_v2.py` to the cot code mirror is a later SERVED cell.

**For the CTO, three points from ~68 (rows W68-S1 and W68-S2):**
1. **Run-time registry dependency (deploy-blocking as is).** The writer needs `lib/opal_naming` and the registry at run time. The gold
   run syncs only `code/gold/` (`gold_dispatch.sh`:497-498), so on that path EVERY row would read `absent` until the registry ships with
   it. The writer WARNs and never claims the own firm, so it is safe but NOT-CLEAN.
   - The deploy cell must ship the registry alongside the script, or the field stays absent in production.
2. **Stamp rule.** The stamp is the firm of the input that supplied the PRICE (transactions for T1, historical_prices for T2). The
   ticker-mapping inputs are resolved and a WARN fires on a mismatch, but they do not change the stamp.
3. **A dead check, not changed:** W68-S1. Step 5b's share-class check filters on `t1_transaction_observed`, a label the writer never
   emits, so the check is a no-op.

**Rows:** W68-S1, W68-S2 (INERT). ARMED: 0.

**Round-close check:** REFUSED on the one ungraded judgment criterion, CB40an1-AC2.

**Also in flight:**
- Round 41 (CB-ao-1, the `_ff_worker` deploy) is RELEASED on both halves @7179ea76bd, on `~CB2`.
- Round 38 (CB-al-2) stays held on IRPT_DASHBD 13.1's sources-fields cell.
