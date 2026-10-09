# CB-as-1 split literal removal (0.9.0_WK_ADVI_COTBKF~72)

Path per key: REGISTRY. `legacy_address()` can express both keys, so no R20 departure and no R20 draft are needed.

| key | before | after |
|---|---|---|
| PFX | `'/'.join(['silver','pri'+'ces'])+'/'` = `silver/prices/` | `legacy_address(OWN + "-silver-prices-prefix")` row, bucket opal-data-cot = `silver/prices/` |
| PIN_KEY | `'/'.join(['code','gold','scopes'+'.json'])` = `code/gold/scopes.json` | `legacy_address(OWN + "-code-gold-scopes-pin")` row = `code/gold/scopes.json` |

Keys before and after printed from the imported module: identical (`'silver/prices/' 'code/gold/scopes.json' opal-data-cot`).
Registry: two rows appended to infra/logic/registry/legacy_addresses.json; `python lib/opal_naming.py validate` OK (54 system, 14 scope, 0 warnings); no generated carrier regenerated.
Registry evidence fields say the store was NOT re-listed by this worker (no AWS act).
First commit attempt was refused by the naming gate because the row names carried the firm token typed; fixed by composing from OWN (as the existing script does), no bypass.

Tests: no_split_literals 1 failed at base (f317f82c20, 4 ast hits), 1 passed after. Silver suite: 749 passed, 11 skipped.
Other files (row ADVI_COTBKF-D2-W72-S1): commonwealth_bd_txn_provenance.py 2 sites, data/cot/scripts/gold/build_canonical_prices_v2.py 1 site, other 36 files 0. Unchanged.
Commits: f317f82c20 (test alone), c904299ad5 (fix).

SPLIT-LITERALS script=0 path=registry other_files=2
