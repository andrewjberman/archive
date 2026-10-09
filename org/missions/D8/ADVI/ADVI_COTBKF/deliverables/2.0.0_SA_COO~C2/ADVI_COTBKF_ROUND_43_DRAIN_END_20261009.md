# L8 drain end -- ADVI_COTBKF round 43

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~14:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB43aq1-AC2)

Round 43 was cut as one issuance @8148110fb6 (`fanout: 1 of 1 chains, cap 8`) on IRPT_DASHBD ADDENDUM 13.1 and `2.0.0_SA_COO~D2` msg
3452 (TO-DB-b-96 @ce9f482be0).

| order | item | worker | state |
|---|---|---|---|
| CB-aq-1 | Cottonwood's channel entry in `sources.json`; adapter `return_basis=TWR`; local rebuild | ~70 | complete @90b2e493b4 (rule commit d41d82a633 first), drained @9a7eaa849a |

## The real run, shared tree, by the issuer

```
ARD-COTTONWOOD-R43 days=3325 rows=1691729 return_basis_twr=107316 manifest_fields_absent=0 producer_tests=102
issuer rebuild vs the worker's committed manifest: day_files 3325 / 3325, identical sha256 = True
```

## What the round delivered

- **One entry** was added to IRPT_DASHBD's `sources.json`: `_commonwealth_delivery`.
  - `registry_key` z09 resolves to Cottonwood through `lookup()`, and there is no firm token.
  - `valuation_source=positions_x_as_traded_close`, `fee_treatment=net_of_fees`, `price_basis=as_traded`.
  - Nothing else in the file changed.
- **The producer's compute path skips it.** The underscore prefix is the producer's existing structural switch: `declared_sources()`
  still reads `['schwab_08335338']`, and `source_entry()` refuses the key.
  - The handler's one-source guard sees the same single source as before. The adapter refuses to run if the entry is ever listed as a
    source.
  - IRPT_DASHBD's producer tests give 102 passed; the reporting-gold handler tests give 86 passed.
- **The rebuild:** 3,325 days and 1,691,729 rows. 107,316 measured rows read `TWR`; the blank rows read `NOT_MEASURABLE`.
  - Every one of the 3,325 day manifests carries the three method fields: 0 of 9,975 absent.
  - The `method` text states the declared fields and no custodian or gross claim.

**Open, asked of the CTO (msg ~14:44Z), and it gates the CB-al-2 mint -- row W70-S1:**
- The producer's `build_manifest()` writes `method_version: 2`, the custodian-equity method row, into EVERY manifest, whatever the
  source entry says.
- Cottonwood's rows carry `method_version` NULL, so the manifests show version 2 beside positions-based method fields.
- Either it is accepted at the mint, or IRPT_DASHBD's producer is changed first. That code is not this lane's.

**Note:** the `sources.json` edit reaches no deployed Lambda until IRPT_DASHBD redeploys, because the handler packages it by
`staged_from` pins.

**Rows:** W70-S1 (INERT). ARMED: 0.

**Round-close check:** REFUSED on the one ungraded judgment criterion, CB43aq1-AC2.
