# ADVI_BDPRCE round 1 -- L5 ground truth (2.0.0_SA_COO~K1, 2026-10-13 ~13:1xZ, dell1)

Each line carries its claim: MEASURED (a read this seat ran, with the command class), READ (a file read at the cited line), or NOT-READ (the worker's to establish).

| # | fact | claim | source |
|---|---|---|---|
| 1 | PRD v1.0 @96028a9e53: ratified-text half SIGNED by 3.0.0_SA_CVO, brief half SIGNED (auto, the CRO wrote the brief); status ADMITTED | MEASURED | `python .tools/prd-signoff.py status ADVI_BDPRCE` at 12:5xZ |
| 2 | `project.json`: `dep_stage` PRD, `decompositions` empty, `coo_lane` `2.0.0_SA_COO~K1`, mode lease FULL | MEASURED | `drive-mode.py read`; file read |
| 3 | surprise channel: 0 rows, 0 open, 0 armed | MEASURED | `.tools/comp-surprise --project ADVI_BDPRCE --json` |
| 4 | the sequence lists no row for this project (UNPLACED); its own directive's rules govern | MEASURED | `sequence-check.py --project ADVI_BDPRCE` |
| 5 | `SOURCE_RANK`: scoped_override -2, yahoo_finance -1, transaction_observed 0, linear_interpolation 2, carry_forward 3 | READ | `data/black_diamond/scripts/silver/bd_price_update.py:65-71` |
| 6 | `extract_t1_prices`: median of `|market_value|/|units|` per `asset_name` over the rows given; valid rows need `units` abs > 1e-8, `market_value` != 0, price in (0, 100000) | READ | `bd_price_update.py:327-344` |
| 7 | `load_transactions_for_date` reads `silver/transactions/<day>.parquet` and does not de-duplicate on `transaction_id` | READ | `bd_price_update.py:263-271`; the new-asset loader does at :258-259 |
| 8 | `upsert_canonical` keeps the lowest `SOURCE_RANK` per (date, asset_name); `save_canonical_prices` puts `silver/prices/canonical_prices.parquet`; `save_daily_prices_trigger` puts `silver/prices/<day>.parquet` | READ | `bd_price_update.py:587-640` |
| 9 | B_01 reads every `silver/prices/*.parquet` (daily files and canonical), sorts by date and keeps the first row per asset | READ | `data/black_diamond/scripts/gold/B_01.holdings_lots.py:319-361` |
| 10 | the price bucket for these scripts is `opal-data-bd`; the served 49F home since ADVI_FIRMBKTS act 2 is `opal-data-49financial` (prefixes `advi/`, `gold/`, `irpt/`, `mdpf/`, `_campaign/`, `_code/`; under `advi/49financial/`: `gold/`, `platinum/`) | MEASURED | `s3api list-objects-v2 --delimiter /` on both |
| 11 | `s3://opal-data-bd/silver/prices/canonical_prices.parquet`: versioned; today's versions at 00:15:27Z (105,292,662 B), 04:03:26Z (109,605,884 B) and 04:03:42Z (109,972,952 B), 09:49:32Z and 09:49:48Z, 12:47:50Z and 12:48:05Z. Paired writes about 15 s apart; the pair's first member is the smaller object | MEASURED | `s3api list-object-versions --max-items 8` |
| 12 | `silver/transactions/2026-10-10` .. `-13`: sizes 58,226; 391,262; 35,269; 35,269 bytes, written once per day at ~00:15Z | MEASURED | `s3api list-objects-v2 --prefix silver/transactions/2026-10-1` |
| 13 | the writer identities of the pair in #11 | NOT-READ | BP-a-1 |
| 14 | the served T-1 holdings object key a portal reads for a 49F account, and whether a per-lot row there carries the price's source | NOT-READ | BP-a-4 finds it from the producer chain; BP-a-1 names writers, not the served object |
| 15 | the 603-of-1,610 figure (brief PART VI.3) was measured over the 20 weekday partitions 2026-09-16 to 2026-10-13 by `0.9.0_WK_ADVI_FIRMBKTS~66`; its replica scripts are `pricing_quant_s32_s33.py`, `pricing_quant_s34.py` | READ | brief PART IV.6 and VI.3 |
| 16 | AWS identity of this box's reads: `arn:aws:iam::313476888478:user/cloudops-dell1-agent-user`; reads of `opal-data-bd` succeed | MEASURED | `.tools/aws sts get-caller-identity`; `list-objects-v2` |
| 17 | the rail denies a raw served-prefix listing on `opal-data-49financial` unless a `# rail-checked: <why>` rides the call | MEASURED | the deny, id `20261013T130219Z-89708856` |

Not read by the issuer, by design: the held cells' files (C1 template content beyond the PRD's quotation), the lot-level code of B_01 past :361, the Lambda twin. They belong to the enrichment round that touches them.
