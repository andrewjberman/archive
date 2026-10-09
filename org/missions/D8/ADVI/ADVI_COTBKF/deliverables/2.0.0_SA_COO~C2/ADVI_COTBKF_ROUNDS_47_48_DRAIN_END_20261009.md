# L8 drain end -- ADVI_COTBKF rounds 47 and 48

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~15:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile; no judgment criterion in
either round)

| round | order | item | worker | state |
|---|---|---|---|---|
| 47 | CB-au-1 | Cottonwood's sources entry declares `method_version` 3; rebuild through IRPT_DASHBD's changed producer | ~74 | complete @c1624bf45d (rule commit f043506a7c first), drained @9c6b230812 |
| 48 | CB-av-1 | sweep the remaining split key literals onto `legacy_addresses` rows; grep every COTBKF script | ~75 | complete @fb3c7cc171 (test alone first, de5122fd9a), drained @5432796246 |

Cut on: round 47, `~D2` msg 3564 (TO-DB-b-102 @e18a26ad12); round 48, CTO ADDENDUM 20 @3a563d35b1. Round 48's risk is WORLD per
the gate floor (a registry path).

## The real runs, by the issuer

```
ARD-COTTONWOOD-R47 days=3325 manifests_mv3=3325/3325 rows_mv3=1691729 producer_tests=106 handler_tests=86
issuer rebuild vs ~74's committed manifest: day_files 3325 / 3325 identical sha256 = True
target prefix s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/ = 0 keys; positive control irpt/ first page = 3
pytest test_cotbkf_no_split_key_literals.py: 1 passed (files scanned: 39; split key literals: 0)
python lib/opal_naming.py validate: OK, 0 warning(s), registry@16d471aea9868a4d
ROUND-CLOSE round=47 MAY-CLOSE; round=48 MAY-CLOSE
```

## What the rounds delivered

**Round 47:**
- `_commonwealth_delivery` carries `method_version: 3` (`positions_based`), one key.
- Every one of the 3,325 day manifests and all 1,691,729 rows read 3. The three valuation fields are present.
- IRPT_DASHBD's producer gives 106 passed and its handler 86 passed. The producer and handler are unedited.
- The adapter also needed a change: it had hard-coded a null `method_version`, and now reads it from the entry.
- Disclosure: the worker's first `sed` hit the wrong line of `sources.json`. It reverted that uncommitted edit before committing, and
  the committed diff is the one line.
- **This content is now ready for round 38's CB-al-2 mint.** The mint waits only on its apply path (round 49, ~76, running) and its
  pair.

**Round 48:**
- 0 split key literals across the 39 files scanned, with the keys unchanged: `silver/prices/`,
  `silver/prices/canonical_prices.parquet`, `silver/transactions/`, `silver/historical_prices.parquet` and `code/gold/`.
- Three `legacy_addresses` rows added, and `validate` is OK.
- A third site the order did not name (the writer's `CODE_PREFIX`) was caught by the test and swept.

**Rows:**
- **W75-S1:** the writer now imports `lib/opal_naming` at module level, and the cot code mirror does not carry it.
- **D2-S72 @bcb4fe262c (BLOCKING, INERT), filed by the issuer:** the LIVE `B_00` (round 41) imports `opal_naming` inside
  `_ff_worker`, and the mirror carries no `opal_naming` and no `NAMING_SCHEMA.json` anywhere under `code/`.
  - So the gold run would raise ImportError the day `schwab/silver/rps/` fills. It is latent today (rps is empty).
  - The same gap blocks the writer redeploy that ADDENDUM 21 rules.
  - Asked of the CTO, with the issuer's recommendation: resolve the own firm from the pinned `scopes.json` beside each script, with no
    run-time `opal_naming` import.

ARMED: 0.
