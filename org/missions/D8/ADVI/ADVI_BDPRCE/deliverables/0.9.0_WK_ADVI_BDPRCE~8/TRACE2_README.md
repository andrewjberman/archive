# TRACE2_README -- `trace_price_v2.py` (ADVI_BDPRCE BP-b-4, round 2)

Answers "where did this served Financial price come from?" by following the row the SERVED lot carries. Round 1's
`trace_price.py` (BP-a-2) took the daily row on a same-date tie; here the followed row is the candidate whose price
equals the served price, so a daily row with a different value is reported and not followed.

## How to run

    python trace_price_v2.py --asset "<asset_name>" --lot-object <bucket>/<key>@<VersionId> [--out <file.json>]
    python trace_price_v2.py --asset "<asset_name>" --date YYYY-MM-DD --served-price <value> [--bucket opal-data-bd] [--out <file.json>]
    python trace_price_v2.py --self-test

`--lot-object` reads the served client detail object at that VersionId, takes its `data_as_of` as the date and the one
`current_price` it carries for the asset as the served price. The client key is not printed; the record carries its
first 16 hex digits of SHA-256. Needs AWS read credentials (boto3 default chain). `--self-test` needs no AWS.

## What it does

- Gathers the same-date rows for the asset: the row in `silver/prices/<date>.parquet` and the row in
  `silver/prices/canonical_prices.parquet`, each with its VersionId.
- Follows the canonical row when it equals the served price (both equal: canonical is followed and `both_equal` is true).
  Otherwise follows the daily row when it equals it. When neither equals it, `follows_served` is false, `followed_source`
  is null and no rule is traced. It never picks a row silently.
- Traces the followed row with round 1's rule functions (imported from `0.9.0_WK_ADVI_BDPRCE~2/trace_price.py`): the
  as-built recompute from `silver/transactions/<date>.parquet`, `trade_ids` with repeats kept, and `match`.
- Adds `r1_price` only if `data/black_diamond/scripts/silver/bd_price_rule.py` exists in the tree. It does not in this
  tree, so the record says so in `r1_price_module`.

## What it does not do

- It does not fix a rule. The recompute is the rule as built today, with its bugs (no de-duplication on
  `transaction_id` on the daily path).
- It does not know which row the lot's B_01 run chose on a tie. B_01 sorts unstably, so when both rows equal the served
  price the record says "canonical followed by rule" and never claims B_01's pick.
- It does not run a producer, write to S3, or recompute `gold/B_01`. Writes only the `--out` file.
- `linear_interpolation` and yahoo inputs are named, not recomputed; their claim is `absent` where not read.
