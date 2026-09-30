# MDPF_SECCLASS.TO-SC-t1 -- BD classifier reads the canonical table -- result

**Worker:** `0.9.0_WK_MDPF_SECCLASS~3`, worktree `wk-MDPF_SECCLASS-3`.

## What changed

`data/black_diamond/scripts/gold/lib/etf_classifier.py` no longer scans `bd-securities`. It imports
`infra/aws/lambda/v2_portal/_shared/etf_classifications_dynamodb.ETFClassifier` by extending
`sys.path` with `Path(__file__).resolve().parents[5] / infra/aws/lambda/v2_portal/_shared` -- the same
extended-import-path pattern `data/assets/scripts/gold/build_satellites_registry.py:load_classifier()`
already uses one path-depth shallower -- and wraps it. `classify()` now does ONE thing: a direct
ticker lookup against `etf-classifications` (344 rows), returning the row's `asset_class` VERBATIM
(no hedge->alternatives fold). Layers 2 (name-alias), 3 (name-pattern regex) and 4 (ticker-shape
guess) are removed. A ticker the table lacks returns `''` (`ETFClassifier.UNKNOWN`), the same falsy
signal every existing reader (`C_06`, `D_03`, `D_04`, `E_25`) already tests for. `resolve_ticker`
always returns `None` (no name_aliases in the canonical source). The BD `CASH_USD` override is
unchanged. The public API (`instance`, `classify`, `get_sub_asset_class`, `resolve_ticker`) is kept;
`client=` is an injection seam for tests.

## Tests (SC1-t1-AC1)

`data/black_diamond/scripts/gold/tests/test_etf_classifier_canonical.py`, 11 cases on a hand-rolled
stub client (no live AWS): GLD/PHYS/VXX land as the table will hold them, an unseen ticker and a
name-pattern-matching name both come back `''` (never a guess), `resolve_ticker` always `None`,
`CASH_USD` unchanged, and a real-wiring test (`monkeypatch` on the shared module's `boto3.resource`)
proves construction requests `etf-classifications` ONLY, never `bd-securities`.

```
python -m pytest data/black_diamond/scripts/gold/tests/test_etf_classifier_canonical.py -q -p no:cacheprovider
11 passed in 0.22s
```

## Census (SC1-t1-AC2)

Classified BD's latest OPEN holdings (`s3://opal-data-bd/gold/holdings_lots/2026-09-25.parquet`, the
day `E_18.detect_new_securities.get_latest_parquet_key` reads; 3,992 distinct open (ticker, asset_name)
pairs) with the BEFORE classifier (CLOUD @c1e9b60e63bf535d3c9bc148c0e612f824b51684: `bd-securities`
scan, 10,929 rows, layers 1-4) and the AFTER classifier (this commit: `etf-classifications`, 344 rows,
one layer, no fold, no guess). Written to
`org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R1_BD_RESOLUTION_CENSUS_20260929.json`:

- `holdings`: 3992. `before_layers`: layer1_ticker=2344, layer2_name_alias=1647, unclassified=1.
  `after_layers`: canonical_table=293, unclassified=3699.
- `moved`: 3880 (every one listed in `moves`), `unclassified`: 3699 -- large and EXPECTED (the
  canonical table covers few BD tickers today; SC-k-1's backfill is what closes this).
- `bd_securities_reads_after`: 0. `guessed_after`: 0.
- GLD: before `(alternatives, Gold)` -> after `(commodities, Metals)`.
- VXX: before `(alternatives, Volatility)` -> after `(structured, Hedge)`.
- PHYS: before `(alternatives, Gold)` -> after `('', '')` -- **the canonical `etf-classifications`
  table does not carry a PHYS row today** (live scan confirmed, 344 rows, GLD and VXX present, PHYS
  absent; PHYS exists only in the legacy `bd-securities` table). This is the library correctly
  reporting an honest miss, not a defect in the code under test.

## SC1-t1-AC2 -- BLOCKING, recorded FAIL

```
python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R1_CHECKS/r1_bd_resolution_census.py
NOT-CENSUSED: PHYS lands {'asset_class': '', 'sub_asset': ''}, placed ('commodities', 'Metals')
rc=1
```

The check (and SC-k-1's sibling `r1_backfill_census.py` PINNED set) both assume GLD, PHYS and VXX
already carry canonical rows. Live measured state shows PHYS does not. Per the refusal clause, this
is NOT weakened to pass: filed as `MDPF_SECCLASS-W3-S1` (BLOCKING, ARMED, disarm owner
`2.0.0_SA_COO~M`) in `org/missions/D8/MDPF/MDPF_SECCLASS/surprise-channel/investigations/INVESTIGATION_v1.md`.
A second row, `MDPF_SECCLASS-W3-S2` (OBSERVATION, ARMED), notes that removing layers 2-4 also drops
the private `_ticker_map`/`_name_map` attributes `build_bd_assets_dim.py:156` reads directly for a
diagnostic print -- no production impact today (this order is LOCAL build + record, no deploy), but
a break for that reader's next real run, owned by SC-t-2/SC-t-3.

Because SC1-t1-AC2 does not PASS-by-output, this task order's `<status>` is NOT flipped to
`complete`.
