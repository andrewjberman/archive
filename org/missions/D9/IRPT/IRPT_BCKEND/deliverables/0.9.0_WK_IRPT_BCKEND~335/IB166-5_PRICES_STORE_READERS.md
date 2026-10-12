# IB166-5 -- readers of the landed prices store (IRPT_BCKEND.TO-IB-pr-480, worker 0.9.0_WK_IRPT_BCKEND~335)

**Verdict: NO_READER.** Nothing under `infra/aws/lambda/investor-reporting/` reads the store, so no served figure depends on it. Base `4650422c34`. Record: `IB166-5_prices_store_readers.json`.

Store: `opal-data-cot`, `silver/prices/canonical_prices.parquet` (registry key `cottonwood-silver-canonical-prices`).

## Census

- 664 tracked files searched under the service (all file types), 0 with a hit for `canonical_prices`, `cottonwood-silver-canonical`, `silver/prices`, `silver_prices`.
- Positive control, same Grep method: the writer `data/cot/scripts/gold/build_canonical_prices_v2.py` returns its own lines (21, 30, 39, 40, 898). The bucket name `opal-data-cot` returns hits under the service (directory tests, `tenants.py:22,164`, and the substring in `opal-data-cottonwood`), so the method sees a bucket hit; none addresses the prices key.

## Near misses (not readers)

- `performance/tenants.py:164`: the Cottonwood route labels data plane `opal-data-cot/forwardfill_v2/`; used by `describe`, `route_key`, `separation_report` only, no S3 read bound to it.
- `performance/holdings_gold.py:109-146` and `installed.py:76-92`: read the per-firm `holdings_performance_daily` gold, not the store. `PRICE_MISSING` is the producer's rule.
- `intake/upload_resolution.py:112,133`: `resolve_prices` is `SHARES_PRICE_SOURCE_NOT_COMPOSED`; other bindings are tests.
- `holdings-performance/handler.py:61`: packages the gold producer (outside the tree); 0 hits for the store terms in its folder.

## Consequence

The retirement of the store as a source is a line in the record: no reader needs a `held` answer or a replacement source.

## Not established

The packaged producer's and the gold's upstream price inputs (not traced); runtime-assembled addresses; layers and portal; live bundles; no test run. Detail in the JSON.

## Bounds

Functions invoked, sign-ins, AWS writes, accounts, figures, vendor requests: 0. No AWS call at all.
