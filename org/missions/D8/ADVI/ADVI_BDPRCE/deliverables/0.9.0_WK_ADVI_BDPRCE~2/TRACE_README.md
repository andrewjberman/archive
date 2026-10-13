# TRACE_README -- `trace_price.py` (ADVI_BDPRCE BP-a-2)

Answers "where did this served Financial price come from?" for one (asset, date): the served row(s), the rule
that produced the price, the transaction ids it was computed from, and a recompute with a match flag.

## How to run

    python trace_price.py --asset "<asset_name>" --date YYYY-MM-DD [--out <file.json>]
    python trace_price.py --date latest --first-transaction-observed [--out <file.json>]
    python trace_price.py --self-test

Needs AWS read credentials for bucket `opal-data-bd` (boto3 default chain). `--self-test` needs no AWS.
The pipeline source is found by walking up from the script to `data/black_diamond/scripts/silver/bd_price_update.py`;
`MAX_UNIT_PRICE`, `SOURCE_RANK` and `_SCOPED_PRICE_OVERRIDES` are parsed from it with `ast`, never copied.

## What it does

- Reads `silver/prices/<date>.parquet` and `silver/prices/canonical_prices.parquet` for the asset, with each
  object's VersionId, and names the row that `gold/B_01` keeps. Two rows on one date are reported as a TIE.
- Names the rule by the served `source`, with file:line citations into `bd_price_update.py`.
- For `transaction_observed`, reads `silver/transactions/<date>.parquet` and applies the rule's filters
  (`extract_t1_prices:335-341`). It lists every `transaction_id` used (repeats kept), `rows_used`,
  `distinct_trade_ids`, `median_distinct` (informational), and `recomputed_price` (the median over ALL rows, as
  the rule does today). `match` is `abs(recomputed - served) <= 1e-6 * max(1, abs(served))`.
- For other sources, `trade_ids` is `[]`, `recomputed_price` is null, `match` is false, and `rule` names the input
  (yahoo close in `silver/historical_prices.parquet`; last canonical row for carry_forward).
- `--date latest` takes the newest daily file. With `--first-transaction-observed` it walks daily files newest
  first and takes the first `transaction_observed` row that traces to a trade. The `selection` block counts what
  it skipped (`skipped_without_trades` and its parts). It is never silent about a walk-back.
- Reads in memory. Writes only the `--out` file. Prints no account, client or advisor field.

## What it does not do

- It does not fix a rule. It reproduces today's rule, bugs included (no de-duplication on `transaction_id` on the
  daily path), and states where a row written by the backfill path would differ (that path de-duplicates).
- It does not read lots, run a producer, write to S3, or recompute `gold/B_01`. The B_01 pick is an emulation of
  the two objects for one date, not a run of B_01.
- A same-date tie pick is a stable-sort emulation (daily first). B_01 uses an unstable sort, so its pick between
  tied rows is not guaranteed and this tool never claims it is.
- `linear_interpolation` and yahoo inputs are named, not recomputed; their claim is `absent` where not read.
