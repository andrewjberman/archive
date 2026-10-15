# READERS_RECORD -- ADVI_COTBKF.TO-CB-ci-2 (round 87)

Searched commit: `b773d5864a7ee4db1c368e379560897d5915f185` (box/dell1). Record: `READERS_RECORD.json` beside this file.

Counts: readers=49; feeds_account_value=4; ranks_or_reports=15; feeds_other=3; not_a_reader=26; unread=1; gaps=4.

Gaps (FEEDS_ACCOUNT_VALUE without use_class): `data/assets/scripts/silver/commonwealth_daily_valuation.py` L574; `data/assets/scripts/silver/commonwealth_daily_valuation.py` L329; `data/assets/scripts/silver/commonwealth_sweep_regrade.py` L1602; `data/assets/scripts/silver/commonwealth_fwd3_serve.py` L687.

## Tokens

| token | files |
|---|---|
| `price_history` | 13 |
| `yahoo/global` | 0 |
| `price_store` | 42 |
| `demque_index` | 2 |
| `index.parquet` | 20 |
| `porting_verdict` | 9 |
| `use_class` | 7 |
| `as_traded_close` | 53 |
| `yahoo` | 158 |

## Readers

| file | line | class | filters_on | fails_closed | note |
|---|---|---|---|---|---|
| `data/assets/scripts/silver/commonwealth_daily_valuation.py` | 574 | FEEDS_ACCOUNT_VALUE | none | not_applicable | Yahoo store splits.parquet per CUSIP at the named as_of instant (SPLIT_STORE); applied as split factors to closes (apply_splits). |
| `data/assets/scripts/silver/commonwealth_daily_valuation.py` | 329 | FEEDS_ACCOUNT_VALUE | none | false | As-traded close read from a ticker-keyed Yahoo Close cache (not the CUSIP store); a missing file keeps the store points, no exclusion. |
| `data/assets/scripts/silver/commonwealth_sweep_regrade.py` | 1602 | FEEDS_ACCOUNT_VALUE | none | not_applicable | Calls dv.load_store_splits for the before and after arms; routes the Yahoo Close cache to valuation at L1562-1616. |
| `data/assets/scripts/silver/commonwealth_fwd3_serve.py` | 687 | FEEDS_ACCOUNT_VALUE | porting_verdict | false | Reads the Yahoo index for porting_verdict labels on account-day rows only; no row is excluded, an unreadable index labels UNVERIFIED and keeps the value. |
| `data/assets/scripts/silver/commonwealth_price_need.py` | 394 | RANKS_OR_REPORTS | valid_range, porting_verdict, use_class | true | Need list ranked from the index; use_class (CB-ci-1, landed at this HEAD) excludes an active-set NOT_FOR_ACTIVE security from coverage and fails closed; values no account. |
| `data/assets/scripts/silver/commonwealth_div_dating_trace.py` | 117 | RANKS_OR_REPORTS | none | not_applicable | Dividend-dating trace report; calls dv.load_store_splits; writes no account value. |
| `data/assets/scripts/silver/commonwealth_split_recount.py` | 47 | RANKS_OR_REPORTS | none | not_applicable | Read-only re-count of unconfirmed splits; reads the store index (L47), splits (L59) and prices (L67); applies nothing. |
| `data/mdpf/scripts/demque/batch_equality.py` | 79 | RANKS_OR_REPORTS | none | not_applicable | Equality-proof report of the batched pull; index read L79, prices and splits L80-89. |
| `data/mdpf/scripts/demque/batch_pull.py` | 187 | RANKS_OR_REPORTS | none | not_applicable | Takes the head of the index to pick names for a batched Yahoo pull (a need list). |
| `data/mdpf/scripts/demque/extend_frontier.py` | 337 | RANKS_OR_REPORTS | valid_range | not_applicable | Index valid_to read to list names needing a standing extension request. |
| `data/mdpf/scripts/demque/incremental_equal.py` | 527 | RANKS_OR_REPORTS | none | not_applicable | Equality-proof report of the incremental path; store reads at L455-464. |
| `data/mdpf/scripts/demque/incremental_plan.py` | 56 | RANKS_OR_REPORTS | none | not_applicable | Read-only plan of the incremental draw over the served index; splits read L43-46. |
| `data/mdpf/scripts/demque/inactive_set.py` | 187 | RANKS_OR_REPORTS | none | not_applicable | Index read for symbol strings only; builds the inactive-only CUSIP list for Yahoo pulls; its filter is V2 membership, not a store field. |
| `data/mdpf/scripts/demque/lock_cause.py` | 150 | RANKS_OR_REPORTS | none | not_applicable | Measures the cause of each re-draw lock rejection; prices L150, lock L176. |
| `data/mdpf/scripts/demque/p1_coverage.py` | 232 | RANKS_OR_REPORTS | valid_range | not_applicable | Read-only CARD-A coverage measurement from the index valid_from and valid_to. |
| `data/mdpf/scripts/demque/porting_test.py` | 273 | RANKS_OR_REPORTS | none | not_applicable | Reads the index to build the Bloomberg porting-test request JSON; writes no price. |
| `data/mdpf/scripts/demque/priority_gate.py` | 172 | RANKS_OR_REPORTS | none | not_applicable | Index read for the priority gate's name list. |
| `data/mdpf/scripts/demque/redraw_stale.py` | 52 | RANKS_OR_REPORTS | none | not_applicable | Reads each name's prices.parquet and lock.json (read only) to list stale served files. |
| `data/mdpf/scripts/demque/secclass_sync.py` | 186 | RANKS_OR_REPORTS | none | not_applicable | Read-only class-sync report; index read L186 and L207, lock.json L213. |
| `infra/aws/lambda/investor-reporting/ycharts/research/price_adapter_demque.py` | 79 | FEEDS_OTHER | valid_range | true | Security-level total-return series for the ycharts price chain (prices L97); no account caller in this checkout, only its tests. |
| `data/mdpf/scripts/demque/daily_draw.py` | 118 | FEEDS_OTHER | none | not_applicable | Reads a name's stored prices, lock, splits and dividends to append; writes the store itself (write_incremental). |
| `data/mdpf/scripts/demque/hold_lock_records.py` | 50 | FEEDS_OTHER | claim | not_applicable | Reads lock.json claim and writes claim held with a reason; the claim is a store field, not a price. |
| `data/assets/scripts/analysis/commonwealth_price_census.py` | 59 | UNREAD | none | not_applicable | STORES[0] canonical-prices carries yahoo_finance rows read by valuation; the writer is not in the census, so Yahoo-store provenance is UNREAD. |
| `data/assets/scripts/silver/commonwealth_base_close_trace.py` | 88 | NOT_A_READER | none | not_applicable | Reads the chain's canonical store (SPEC) and live yfinance (L96); not the Yahoo store. |
| `data/assets/scripts/silver/commonwealth_price_basis_census.py` | 252 | NOT_A_READER | none | not_applicable | Live yfinance census (L252); writes the Yahoo Close cache that valuation L329 reads; no store read. |
| `data/assets/scripts/silver/commonwealth_split_level_probe.py` | 66 | NOT_A_READER | none | not_applicable | Live yfinance split probe for one day; not the store. |
| `data/assets/scripts/silver/commonwealth_cot_price_rewrite.py` | 109 | NOT_A_READER | none | not_applicable | Live Yahoo bond calls and a rewrite of another store's rows; no read of the Yahoo store. |
| `data/assets/scripts/silver/commonwealth_bond_custodian_price.py` | 44 | NOT_A_READER | none | not_applicable | The string yahoo appears only in a label set. |
| `data/assets/scripts/silver/commonwealth_daily_returns.py` | 1 | NOT_A_READER | none | not_applicable | Zero store, Yahoo and cache tokens; priced frames arrive from the valuation. |
| `data/assets/scripts/silver/commonwealth_daily_holdings.py` | 1 | NOT_A_READER | none | not_applicable | Zero store, Yahoo and cache tokens. |
| `data/assets/scripts/silver/commonwealth_account_return_daily.py` | 131 | NOT_A_READER | none | not_applicable | ARD mint: imports the gold producer (zero tokens) and reads valuation output only; downstream of the valuation's reads. |
| `data/assets/scripts/silver/cotbkf_active_bbg_need.py` | 38 | NOT_A_READER | none | not_applicable | Reads the B1 and failed-14 request files and the V2 set; no store or index read. |
| `data/assets/scripts/silver/commonwealth_document_index.py` | 55 | NOT_A_READER | none | not_applicable | Its index.parquet is the document index, not the Yahoo index. |
| `data/assets/scripts/analysis/commonwealth_price_store_scan.py` | 55 | NOT_A_READER | none | not_applicable | Default prefix is the Cottonwood reporting tree (irpt/...), not the Yahoo store address. |
| `data/assets/scripts/analysis/commonwealth_price_need_file.py` | 39 | NOT_A_READER | none | not_applicable | Yahoo appears as an asset-class source label; no price is read. |
| `data/assets/scripts/gold/irpt_reporting/date_basis_grading.py` | 47 | NOT_A_READER | none | not_applicable | Grades days from bars passed in; no store or index read in this file. |
| `data/assets/scripts/gold/irpt_reporting/second_witness_guard.py` | 37 | NOT_A_READER | none | not_applicable | Pure guard over bars passed in; no read. |
| `data/mdpf/scripts/silver/security_series_writer.py` | 119 | NOT_A_READER | none | not_applicable | Writer, off unless switch is True; consumes rows passed in; no store read. |
| `data/mdpf/scripts/silver/security_identity_map.py` | 73 | NOT_A_READER | none | not_applicable | Takes lock rows as an argument; no store read in this file. |
| `data/mdpf/scripts/demque/yahoo_pull.py` | 1 | NOT_A_READER | none | not_applicable | Live Yahoo puller; no read of the store or index. |
| `data/mdpf/scripts/demque/tr_column.py` | 45 | NOT_A_READER | none | not_applicable | Money-market guard reading a local csv; no store read. |
| `lib/research/price/price_history.py` | 33 | NOT_A_READER | none | not_applicable | Bloomberg price_history_px_last reader; not Yahoo. |
| `lib/research/api/scoped_amgt.py` | 7401 | NOT_A_READER | none | not_applicable | Imports the Bloomberg price-history loader; not Yahoo. |
| `lib/research/harvest/timeline_api.py` | 372 | NOT_A_READER | none | not_applicable | Mentions the Bloomberg price_history_px_last table in a source label. |
| `integrations/bloomberg/research/price_series_persist.py` | 44 | NOT_A_READER | none | not_applicable | Bloomberg table constant; not Yahoo. |
| `data/cot/scripts/gold/lib/s3_layout.py` | 138 | NOT_A_READER | none | not_applicable | Layout constant for synthetic positions index; not the Yahoo index. |
| `data/black_diamond/scripts/gold/lib/s3_layout.py` | 183 | NOT_A_READER | none | not_applicable | Layout constant for synthetic positions index; not the Yahoo index. |
| `data/assets/scripts/gold/irpt_reporting/sources.json` | 126 | NOT_A_READER | none | not_applicable | Configuration label valuation_source; no read. |
| `data/assets/scripts/gold/runners_49f/d00_census_out.json` | 1 | NOT_A_READER | none | not_applicable | A stored census output containing the token; not code. |

## Not established

- BLIND by design (comp-adversary RUN): the census counts files by literal token. yahoo/global has 0 hits because every reader builds the address with opal_naming.address(); a reader that builds it from other parts, or reads through an intermediate file or table, is not matched by any token.
- Direct readers only: consumers of valuation outputs (account_day_value, returns, the ARD mint, fwd3 tables, reports) are not classed as readers. A Yahoo price that enters the valuation is carried downstream without a further read here.
- UNREAD: the canonical-prices store (commonwealth_price_census.py STORES[0], L59) carries yahoo_finance-labelled rows that valuation reads as the primary price input. Its writer is not among the census hits; whether those rows originate in the Yahoo store is not established.
- The Yahoo Close cache (valuation L241 and L329) is ticker-keyed. Its CUSIP-to-ticker mapping, and whether use_class can be applied to it, is not traced. Its writer (commonwealth_price_basis_census.py, live yfinance into a scratch cache) is classed NOT_A_READER here.
- The use_class column is read from the index in code (price_store.index, CB-ci-1 readers). Whether the index now served in S3 carries the column is not read: no S3 call was made.
- Callers of price_adapter_demque (the price_source chain) are not traced beyond this checkout's tests; its FEEDS_OTHER class rests on that.
- Other-firm Yahoo pipelines (data/black_diamond, data/cot, data/inf, lib and infra fetchers) read their own yfinance pulls and do not use the Yahoo store address; they are outside the store definition and are not classed one by one.
- The searched tree is the box/dell1 HEAD b773d5864a (the base checkout's working tree at search time). The base HEAD moved from 6a557f1206 during this run; the census was re-run at b773d5864a and its per-token file lists matched except use_class (commonwealth_price_need.py added).
- No account number, name or dollar value was read or written. The active-set file was not opened.
