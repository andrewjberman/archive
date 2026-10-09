# L8 drain end -- ADVI_COTBKF round 45

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~15:2xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB45as1-AC2)

Round 45 was cut as one issuance @e4af0a89d2 (`fanout: 1 of 1 chains, cap 8`; risk WORLD per the gate floor for an
`infra/logic/registry` path) on `1.0.0_SA_CTO~DELL2` ADDENDUM 17 @809d6830ac (msg 3519, D2-S67).

| order | item | worker | state |
|---|---|---|---|
| CB-as-1 | remove the split key literals from `commonwealth_cot_price_rewrite.py` | ~72 | complete @845411827e (test alone first, f317f82c20), drained @406d47b088 |

## The real runs, shared tree, by the issuer

```
pytest test_cot_price_rewrite_no_split_literals.py + test_cot_price_rewrite_pin_check.py: 4 passed
python lib/opal_naming.py validate: OK 54 system row(s), 14 scope row(s), 0 warning(s) at registry@f936f6350cc5c404 over all 13 registry file(s)
```

## What the round delivered

- **Both keys come from the registry,** with no split literal and no R20 departure. `legacy_address()` expresses both legacy shapes, so
  two rows were added to `infra/logic/registry/legacy_addresses.json`:
  - `<own>-silver-prices-prefix` -> `silver/prices/`;
  - `<own>-code-gold-scopes-pin` -> `code/gold/scopes.json`.
  The bucket is `opal-data-cot`. The row names are composed from the module's `OWN`, and there is no firm token.
- **The keys are unchanged** before and after (printed from the imported module).
- **Tests:** the new test failed at the base (4 ast hits at :76 and :251) and passes now. The silver suite gives 749 passed, 11
  skipped.
- **Disclosure:** the worker's first commit typed the firm token in the row names, and the naming gate refused it. It was fixed with no
  bypass. The rows' `evidence` fields say the objects were not re-listed (no AWS act).

**Counted, not changed (row W72-S1, the ruling named only this script):**
- `commonwealth_bd_txn_provenance.py` has 2 sites. `:37` is the same `silver/prices` key; `:103` is a regex fragment.
- The cot writer has 1 site (`:65`, `'/'.join(['silver', ''])`).
- 38 files were scanned and 2 carry the pattern. Whether to sweep them is the CTO's call. The writer's site falls inside round 46's
  file.

**Rows:** W72-S1 (INERT). ARMED: 0.

**Round-close check:** REFUSED on the one ungraded judgment criterion, CB45as1-AC2.

**Also:** round 46 (CB-at-1, writer input resolution) was spawned on this drain (~73), as its dependency required.
