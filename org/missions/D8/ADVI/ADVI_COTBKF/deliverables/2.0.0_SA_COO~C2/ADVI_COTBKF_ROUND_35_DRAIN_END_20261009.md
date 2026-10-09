# L8 drain end -- ADVI_COTBKF round 35

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~12:1xZ | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB35ai1-AC2)

Round 35 was cut as one issuance @39c76740e9 (`fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2` ADDENDUM 9.1 @3093730512 (msg
3188). Round 34 is still open: CB-ah-1 and CB-ah-2 are drained, and CB-ah-3 is held on the pair.

| order | item | worker | state |
|---|---|---|---|
| CB-ai-1 | read-only provenance of the 49F `bd_txn_price` rows in `opal-data-cot` | ~63 | complete @d322d04fcd (rule commit 5c79b91853 first), drained @381f92da9e |

## The real run, shared tree, after the drain

```
BD-TXN-PROVENANCE keys_scanned=7797 keys_with_rows=38 earliest=silver/prices/2026-04-14.parquet@2026-06-09T20:42:15Z class=shared_builder_run
```

The issuer's run matches the worker's except `keys_scanned`: 7,797 vs 7,790. The bucket is live and grew by 7 keys between the two runs.
The hits, the earliest key and the class are the same.

## What the round found

**Route: `shared_builder_run`.** On 2026-06-09 at ~20:42Z, the cot gold run (SSM doc in `infra/aws/terraform/cot-pipeline/ssm.tf`, which
exports `BD_S3_BUCKET=opal-data-cot`) ran a price builder that still auto-chained 49F's `inject_scoped_overrides`. It wrote 49F's
three bond constants into cot's price lineage. Each file has a single version.
- **Code history:**
  - That auto-chain was in the shared builder at the time (64b6b9d65a) and in the cot seed's first commit (6b0be4337e, 2026-06-10).
  - It was removed by 319a716cb4 (2026-06-12, "cot does NOT run a scoped-override inject step").
  - No live cot code path remains at HEAD.
- **Where the rows sit:** 38 cot keys.
  - 37 daily files `silver/prices/2026-04-14.parquet` .. `2026-06-05.parquet` carry 3 rows each, written 2026-06-09T20:42:15Z.
  - `silver/prices/canonical_prices.parquet` carries 1,623 rows, written 20:42:16Z.
  - The full key/version/size table is section 5 of `deliverables/0.9.0_WK_ADVI_COTBKF~63/bd_txn_provenance.md`.

**For Andrew, via the CTO -- the removal is an S3 act, not a seat's:**
- Every one of the 38 keys is a FULL price file. The daily files are ~280 KB each, holding every ticker's price for that day. Only 3
  rows in each, and 1,623 in the store, are 49F's.
- Deleting the keys would delete Cottonwood's own prices with them. The clean removal is a REWRITE of each key without the label rows:
  a served move, under a never-widen pair, with the prior versions as the rollback.
- Which (rewrite or delete) is Andrew's call. Nothing is deleted or rewritten.
- The as-traded rebuild already excludes the three bonds (`--hold-cusips`, COO half @0071b97a83).

**Disclosure (row W63-S1):**
- The worker's run 1 detector over-matched. It read two docstring lines as live code and counted files written 1 s before the store
  as prior carriers, giving `live_cot_path`.
- The worker corrected the DETECTOR (ast-parse that skips docstrings and comments; a 60 s prior-carrier window), not the class rule
  committed at 5c79b91853, and re-ran.
- The S3 read set was narrowed to price, backup, seed and snapshot keys after a 550 s timeout; the output says so.
- Reading the seed commit as the builder "in force" at the write is the worker's inference, flagged.

**Re-source.** CTO 9.1 item 2: re-price the three bonds from Cottonwood's own source of record (Yahoo as-traded). They are corporate
bonds (BNP 05613L3H2, WFC 4.15% 2029, NEM 2.8% 2029). Yahoo carries no bond CUSIP series; the equity tickers are what mis-routed
them originally. A re-source has no Yahoo path. Until one exists, they stay HELD (blank, `HELD_SOURCE_UNDER_REVIEW`). This needs a
ruling.

**Rows:** W63-S1 (INERT). ARMED: 0.

**Round-close check:** REFUSED on the one ungraded judgment criterion, CB35ai1-AC2.
