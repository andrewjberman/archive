# Size classes - proposal from the size census (PRD v0.20 FWD-26) - 2.0.0_SA_COO~MI, 2026-10-21

Data: SIZE_CENSUS_20261021.json, `size_census.py` @956dcead42d plus the uncompressed-total field, read live 2026-10-21 over the tracked catalog (md5 03d2dbbae1f07b8d4fa5f0eaa73355d6): {"no_prefix": 11, "store_or_non_s3": 5, "template_prefix": 1}
DENOMINATOR: 298 catalog rows; measured 281 rows over 275 locations; skipped 17; errors 0. Read-only: S3 list and parquet footer range reads, no data page.

## What was measured, and the anchors
- Per table: the newest date partition's object count, listed bytes, largest object and, for parquet, the row count AND the footer's uncompressed byte total (the footer is the only part read).
- The gateway's own limits: the over-memory object cap 67,108,864 bytes (64 MiB; `tool_error_over_memory_cap`); the Schwab engine 256 MiB per job and a 12-object / 64 MB source cap (brief F4); the reply bound 50 KB.
- ONE calibration point, not a rule: Orion `fact_transactions` has a footer uncompressed total of 63,087,565 bytes (60.2 MiB) and the gateway's failing read of it was 166,082,568 bytes, a factor of 2.63. Compressed size (32.6 MiB) would have hidden the problem; the footer's uncompressed total is the number to class on.

## Proposed thresholds (the CTO rules them; nothing here is applied)
- **small**: under 8 MiB uncompressed (parquet) or listed bytes (json and other) in the newest partition, and under 1,000,000 rows: answer whole.
- **large**: 8 MiB up to 24 MiB, under 1,000,000 rows: fits the 64 MiB cap even at the observed 2.63 factor (24 MiB x 2.63 = 63.1 MiB); read by column and window, page the answer.
- **very large**: 24 MiB or more, or 1,000,000 rows or more: aggregate or page up front, never read whole (24 MiB x 2.63 is already the cap).
- The 2.63 factor is a single observation; a second measured failure or a controlled read of one more table should confirm or move the 24 MiB line before it is ruled.

## Counts under the proposal (281 measured rows)
- small: 234
- large: 15
- very large: 32
- basis of the class: large on listed bytes: 9; large on uncompressed bytes: 6; small on listed bytes: 81; small on uncompressed bytes: 153; very large on listed bytes: 16; very large on uncompressed bytes: 16
- 'listed' rows are json/other tables (bytes of the listed objects) and 4 parquet tables whose footers were not read (more than 40 objects in the newest partition); for parquet that makes the class a lower bound.

## Very large (32)
| table | location | MiB | basis | rows | class |
|---|---|---|---|---|---|
| harvest_derived_model_block | opal-data-harvest/derived/model_block/ | 965.3 | listed | - | very large |
| harvest_bloomberg_harvest_bronze_article | opal-data-harvest/bloomberg/harvest/bronze/article/ | 963.4 | listed | - | very large |
| opal_data_news_v2_gold_trending_reports | opal-data-news-v2/trending_reports/ | 431.4 | listed | - | very large |
| harvest_wsj_harvest_bronze_article | opal-data-harvest/wsj/harvest/bronze/article/ | 384.1 | listed | - | very large |
| harvest_seeking_alpha_harvest_bronze_news_listing | opal-data-harvest/seeking-alpha/harvest/bronze/news_listing/ | 175.3 | listed | - | very large |
| opal_data_portal_v2_served_security_scanner | opal-data-portal-v2/json/security_scanner/latest/ | 163.6 | listed | - | very large |
| opal_data_inf_silver_transactions | opal-data-inf/silver/transactions/ | 162.5 | uncompressed | 1,526,148 | very large |
| opal_data_assets_silver_commonwealth_cottonwood_account_day_value | opal-data-assets/commonwealth/cottonwood/silver/account_day_value/ | 128.1 | uncompressed | 21,102,041 | very large |
| harvest_amgt_harvest_bronze_research_report_extract | opal-data-harvest/amgt/harvest/bronze/research-report-extract/ | 119.2 | listed | - | very large |
| harvest_seeking_alpha_harvest_bronze_article | opal-data-harvest/seeking-alpha/harvest/bronze/article/ | 96.7 | listed | - | very large |
| opal_data_assets_silver_commonwealth_cottonwood_transactions | opal-data-assets/commonwealth/cottonwood/silver/transactions/ | 72.6 | uncompressed | 1,416,497 | very large |
| harvest_barrons_harvest_bronze_news_listing | opal-data-harvest/barrons/harvest/bronze/news_listing/ | 61.2 | listed | - | very large |
| opal_data_assets_silver_orion_inflection_fact_transactions | opal-data-assets/orion/inflection/silver/fact_transactions/ | 60.2 | uncompressed | 1,526,148 | very large |
| harvest_seeking_alpha_harvest_silver_listing_hit | opal-data-harvest/seeking-alpha/harvest/silver/listing_hit/ | 58.5 | listed | - | very large |
| opal_data_assets_silver_schwab_08242234_fact_rlw | opal-data-assets/schwab/08242234/silver/fact_rlw/ | 56.6 | uncompressed | 383,662 | very large |
| opal_data_assets_silver_schwab_08335338_fact_rly | opal-data-assets/schwab/08335338/silver/fact_rly/ | 49.4 | uncompressed | 327,621 | very large |
| opal_data_assets_silver_schwab_08242234_fact_rly | opal-data-assets/schwab/08242234/silver/fact_rly/ | 48.6 | uncompressed | 324,125 | very large |
| harvest_barrons_harvest_bronze_article | opal-data-harvest/barrons/harvest/bronze/article/ | 43.5 | listed | - | very large |
| opal_data_assets_silver_schwab_08335338_fact_rlu | opal-data-assets/schwab/08335338/silver/fact_rlu/ | 42.4 | uncompressed | 284,476 | very large |
| opal_data_assets_silver_schwab_08242234_fact_rlu | opal-data-assets/schwab/08242234/silver/fact_rlu/ | 42.2 | uncompressed | 282,721 | very large |
| opal_data_assets_silver_yahoo_global_price_history | opal-data-assets/yahoo/global/silver/price_history/ | 39.8 | listed | - | very large |
| opal_data_portal_v2_served_market_overview_tiered | opal-data-portal-v2/json-tiered/market-overview/ | 35.4 | listed | - | very large |
| harvest_bloomberg_harvest_bronze_histdata | opal-data-harvest/bloomberg/harvest/bronze/histdata/ | 33.4 | listed | - | very large |
| opal_data_assets_silver_schwab_08335338_fact_uln | opal-data-assets/schwab/08335338/silver/fact_uln/ | 32.4 | uncompressed | 308,622 | very large |
| opal_data_assets_silver_schwab_08242234_fact_uln | opal-data-assets/schwab/08242234/silver/fact_uln/ | 32.2 | uncompressed | 306,994 | very large |
| harvest_research-dossier | opal-data-harvest/amgt/harvest/gold/research-dossier/ | 27.6 | listed | - | very large |
| harvest_ft_harvest_bronze_article | opal-data-harvest/ft/harvest/bronze/article/ | 27.5 | listed | - | very large |
| opal_data_assets_silver_schwab_08335338_fact_ult | opal-data-assets/schwab/08335338/silver/fact_ult/ | 26.1 | uncompressed | 226,447 | very large |
| opal_data_assets_silver_schwab_08242234_fact_ult | opal-data-assets/schwab/08242234/silver/fact_ult/ | 25.1 | uncompressed | 219,743 | very large |
| opal_data_inf_silver_orion_rest_transactions | opal-data-inf/silver/orion-rest/transactions/ | 23.1 | uncompressed | 1,249,183 | very large |
| opal_data_inf_silver_prices | opal-data-inf/silver/prices/ | 11.9 | uncompressed | 1,479,566 | very large |
| opal_data_assets_silver_commonwealth_cottonwood_daily_returns | opal-data-assets/commonwealth/cottonwood/silver/daily_returns/ | 3.9 | uncompressed | 1,691,729 | very large |

## Schwab (57 tables)
classes: large 4, small 44, very large 9
| table | location | MiB | basis | rows | class |
|---|---|---|---|---|---|
| opal_data_assets_silver_schwab_08242234_dim_asset | opal-data-assets/schwab/08242234/silver/dim_asset/ | 0.2 | uncompressed | 2,191 | small |
| opal_data_assets_silver_schwab_08242234_dim_balance | opal-data-assets/schwab/08242234/silver/dim_balance/ | 0.7 | uncompressed | 7,613 | small |
| opal_data_assets_silver_schwab_08242234_dim_position | opal-data-assets/schwab/08242234/silver/dim_position/ | 3.5 | uncompressed | 106,051 | small |
| opal_data_assets_silver_schwab_08242234_dim_transaction | opal-data-assets/schwab/08242234/silver/dim_transaction/ | 0.2 | uncompressed | 7,133 | small |
| opal_data_assets_silver_schwab_08242234_fact_acc | opal-data-assets/schwab/08242234/silver/fact_acc/ | 1.1 | uncompressed | 7,610 | small |
| opal_data_assets_silver_schwab_08242234_fact_rld | opal-data-assets/schwab/08242234/silver/fact_rld/ | 0.2 | uncompressed | 972 | small |
| opal_data_assets_silver_schwab_08242234_fact_rlu | opal-data-assets/schwab/08242234/silver/fact_rlu/ | 42.2 | uncompressed | 282,721 | very large |
| opal_data_assets_silver_schwab_08242234_fact_rlw | opal-data-assets/schwab/08242234/silver/fact_rlw/ | 56.6 | uncompressed | 383,662 | very large |
| opal_data_assets_silver_schwab_08242234_fact_rly | opal-data-assets/schwab/08242234/silver/fact_rly/ | 48.6 | uncompressed | 324,125 | very large |
| opal_data_assets_silver_schwab_08242234_fact_rps | opal-data-assets/schwab/08242234/silver/fact_rps/ | 4.3 | uncompressed | 106,051 | small |
| opal_data_assets_silver_schwab_08242234_fact_rps_s2 | opal-data-assets/schwab/08242234/silver/fact_rps_s2/ | 0.7 | uncompressed | 7,613 | small |
| opal_data_assets_silver_schwab_08242234_fact_rtu | opal-data-assets/schwab/08242234/silver/fact_rtu/ | 16.9 | uncompressed | 111,948 | large |
| opal_data_assets_silver_schwab_08242234_fact_rty | opal-data-assets/schwab/08242234/silver/fact_rty/ | 17.5 | uncompressed | 113,595 | large |
| opal_data_assets_silver_schwab_08242234_fact_sec | opal-data-assets/schwab/08242234/silver/fact_sec/ | 0.3 | uncompressed | 2,191 | small |
| opal_data_assets_silver_schwab_08242234_fact_trn | opal-data-assets/schwab/08242234/silver/fact_trn/ | 0.6 | uncompressed | 7,133 | small |
| opal_data_assets_silver_schwab_08242234_fact_uln | opal-data-assets/schwab/08242234/silver/fact_uln/ | 32.2 | uncompressed | 306,994 | very large |
| opal_data_assets_silver_schwab_08242234_fact_ult | opal-data-assets/schwab/08242234/silver/fact_ult/ | 25.1 | uncompressed | 219,743 | very large |
| opal_data_assets_silver_schwab_08242234_fact_upn | opal-data-assets/schwab/08242234/silver/fact_upn/ | 2.8 | uncompressed | 65,297 | small |
| opal_data_assets_silver_schwab_08242234_fact_upt | opal-data-assets/schwab/08242234/silver/fact_upt/ | 2.0 | uncompressed | 40,588 | small |
| opal_data_assets_silver_schwab_08335338_dim_asset | opal-data-assets/schwab/08335338/silver/dim_asset/ | 0.3 | uncompressed | 2,501 | small |
| opal_data_assets_silver_schwab_08335338_dim_balance | opal-data-assets/schwab/08335338/silver/dim_balance/ | 0.8 | uncompressed | 7,704 | small |
| opal_data_assets_silver_schwab_08335338_dim_position | opal-data-assets/schwab/08335338/silver/dim_position/ | 3.7 | uncompressed | 110,347 | small |
| opal_data_assets_silver_schwab_08335338_dim_transaction | opal-data-assets/schwab/08335338/silver/dim_transaction/ | 0.2 | uncompressed | 7,183 | small |
| opal_data_assets_silver_schwab_08335338_fact_acc | opal-data-assets/schwab/08335338/silver/fact_acc/ | 1.0 | uncompressed | 7,701 | small |
| opal_data_assets_silver_schwab_08335338_fact_fam | opal-data-assets/schwab/08335338/silver/fact_fam/ | 0.3 | uncompressed | 7,202 | small |
| opal_data_assets_silver_schwab_08335338_fact_rld | opal-data-assets/schwab/08335338/silver/fact_rld/ | 0.2 | uncompressed | 976 | small |
| opal_data_assets_silver_schwab_08335338_fact_rlu | opal-data-assets/schwab/08335338/silver/fact_rlu/ | 42.4 | uncompressed | 284,476 | very large |
| opal_data_assets_silver_schwab_08335338_fact_rly | opal-data-assets/schwab/08335338/silver/fact_rly/ | 49.4 | uncompressed | 327,621 | very large |
| opal_data_assets_silver_schwab_08335338_fact_rps | opal-data-assets/schwab/08335338/silver/fact_rps/ | 4.6 | uncompressed | 110,347 | small |
| opal_data_assets_silver_schwab_08335338_fact_rps_s2 | opal-data-assets/schwab/08335338/silver/fact_rps_s2/ | 0.8 | uncompressed | 7,704 | small |
| opal_data_assets_silver_schwab_08335338_fact_rtu | opal-data-assets/schwab/08335338/silver/fact_rtu/ | 17.0 | uncompressed | 112,496 | large |
| opal_data_assets_silver_schwab_08335338_fact_rty | opal-data-assets/schwab/08335338/silver/fact_rty/ | 18.0 | uncompressed | 115,936 | large |
| opal_data_assets_silver_schwab_08335338_fact_sec | opal-data-assets/schwab/08335338/silver/fact_sec/ | 0.4 | uncompressed | 2,501 | small |
| opal_data_assets_silver_schwab_08335338_fact_slm | opal-data-assets/schwab/08335338/silver/fact_slm/ | 0.3 | uncompressed | 7,651 | small |
| opal_data_assets_silver_schwab_08335338_fact_trn | opal-data-assets/schwab/08335338/silver/fact_trn/ | 0.6 | uncompressed | 7,183 | small |
| opal_data_assets_silver_schwab_08335338_fact_uln | opal-data-assets/schwab/08335338/silver/fact_uln/ | 32.4 | uncompressed | 308,622 | very large |
| opal_data_assets_silver_schwab_08335338_fact_ult | opal-data-assets/schwab/08335338/silver/fact_ult/ | 26.1 | uncompressed | 226,447 | very large |
| opal_data_assets_silver_schwab_08335338_fact_upn | opal-data-assets/schwab/08335338/silver/fact_upn/ | 2.9 | uncompressed | 65,595 | small |
| opal_data_assets_silver_schwab_08335338_fact_upt | opal-data-assets/schwab/08335338/silver/fact_upt/ | 2.2 | uncompressed | 44,584 | small |
| opal_data_assets_silver_schwab_08403355_dim_asset | opal-data-assets/schwab/08403355/silver/dim_asset/ | 0.1 | uncompressed | 635 | small |
| opal_data_assets_silver_schwab_08403355_dim_balance | opal-data-assets/schwab/08403355/silver/dim_balance/ | 0.0 | uncompressed | 30 | small |
| opal_data_assets_silver_schwab_08403355_dim_position | opal-data-assets/schwab/08403355/silver/dim_position/ | 0.1 | uncompressed | 3,920 | small |
| opal_data_assets_silver_schwab_08403355_dim_transaction | opal-data-assets/schwab/08403355/silver/dim_transaction/ | 0.0 | uncompressed | 28 | small |
| opal_data_assets_silver_schwab_08403355_fact_acc | opal-data-assets/schwab/08403355/silver/fact_acc/ | 0.0 | uncompressed | 30 | small |
| opal_data_assets_silver_schwab_08403355_fact_rld | opal-data-assets/schwab/08403355/silver/fact_rld/ | 0.0 | uncompressed | 0 | small |
| opal_data_assets_silver_schwab_08403355_fact_rlu | opal-data-assets/schwab/08403355/silver/fact_rlu/ | 0.0 | uncompressed | 9 | small |
| opal_data_assets_silver_schwab_08403355_fact_rly | opal-data-assets/schwab/08403355/silver/fact_rly/ | 0.5 | uncompressed | 1,892 | small |
| opal_data_assets_silver_schwab_08403355_fact_rps | opal-data-assets/schwab/08403355/silver/fact_rps/ | 0.2 | uncompressed | 3,920 | small |
| opal_data_assets_silver_schwab_08403355_fact_rps_s2 | opal-data-assets/schwab/08403355/silver/fact_rps_s2/ | 0.0 | uncompressed | 30 | small |
| opal_data_assets_silver_schwab_08403355_fact_rtu | opal-data-assets/schwab/08403355/silver/fact_rtu/ | 0.0 | uncompressed | 9 | small |
| opal_data_assets_silver_schwab_08403355_fact_rty | opal-data-assets/schwab/08403355/silver/fact_rty/ | 0.4 | uncompressed | 1,818 | small |
| opal_data_assets_silver_schwab_08403355_fact_sec | opal-data-assets/schwab/08403355/silver/fact_sec/ | 0.1 | uncompressed | 635 | small |
| opal_data_assets_silver_schwab_08403355_fact_trn | opal-data-assets/schwab/08403355/silver/fact_trn/ | 0.0 | uncompressed | 28 | small |
| opal_data_assets_silver_schwab_08403355_fact_uln | opal-data-assets/schwab/08403355/silver/fact_uln/ | 0.0 | uncompressed | 0 | small |
| opal_data_assets_silver_schwab_08403355_fact_ult | opal-data-assets/schwab/08403355/silver/fact_ult/ | 0.8 | uncompressed | 6,108 | small |
| opal_data_assets_silver_schwab_08403355_fact_upn | opal-data-assets/schwab/08403355/silver/fact_upn/ | 0.0 | uncompressed | 0 | small |
| opal_data_assets_silver_schwab_08403355_fact_upt | opal-data-assets/schwab/08403355/silver/fact_upt/ | 0.2 | uncompressed | 3,920 | small |

## Orion (5 tables)
classes: small 4, very large 1
| table | location | MiB | basis | rows | class |
|---|---|---|---|---|---|
| opal_data_assets_silver_orion_4698_account_performance_gross | opal-data-assets/orion/4698/silver/account_performance_gross/ | 0.1 | uncompressed | 3,129 | small |
| opal_data_assets_silver_orion_inflection_fact_assets | opal-data-assets/orion/inflection/silver/fact_assets/ | 1.9 | uncompressed | 37,026 | small |
| opal_data_assets_silver_orion_inflection_fact_performance | opal-data-assets/orion/inflection/silver/fact_performance/ | 4.5 | uncompressed | 485,176 | small |
| opal_data_assets_silver_orion_inflection_fact_positions | opal-data-assets/orion/inflection/silver/fact_positions/ | 1.9 | uncompressed | 37,026 | small |
| opal_data_assets_silver_orion_inflection_fact_transactions | opal-data-assets/orion/inflection/silver/fact_transactions/ | 60.2 | uncompressed | 1,526,148 | very large |

## Cottonwood Black Diamond (14 tables)
classes: small 14
| table | location | MiB | basis | rows | class |
|---|---|---|---|---|---|
| opal_data_assets_silver_cottonwood_fact_allocations | opal-data-assets/blackdiamond/cottonwood/silver/fact_allocations/ | 0.1 | uncompressed | 1,539 | small |
| opal_data_assets_silver_cottonwood_fact_allocations_s2 | opal-data-assets/blackdiamond/cottonwood/silver/fact_allocations_s2/ | 0.0 | uncompressed | 5 | small |
| opal_data_assets_silver_cottonwood_fact_holdings | opal-data-assets/blackdiamond/cottonwood/silver/fact_holdings/ | 0.7 | uncompressed | 22,623 | small |
| opal_data_assets_silver_cottonwood_fact_holdings_s2 | opal-data-assets/blackdiamond/cottonwood/silver/fact_holdings_s2/ | 0.0 | uncompressed | 5 | small |
| opal_data_assets_silver_cottonwood_fact_model_assignment | opal-data-assets/blackdiamond/cottonwood/silver/fact_model_assignment/ | 0.1 | uncompressed | 1,008 | small |
| opal_data_assets_silver_cottonwood_fact_model_blend | opal-data-assets/blackdiamond/cottonwood/silver/fact_model_blend/ | 0.0 | uncompressed | 132 | small |
| opal_data_assets_silver_cottonwood_fact_model_definition | opal-data-assets/blackdiamond/cottonwood/silver/fact_model_definition/ | 0.0 | uncompressed | 1,754 | small |
| opal_data_assets_silver_cottonwood_fact_model_roster | opal-data-assets/blackdiamond/cottonwood/silver/fact_model_roster/ | 0.0 | uncompressed | 74 | small |
| opal_data_assets_silver_cottonwood_fact_realized | opal-data-assets/blackdiamond/cottonwood/silver/fact_realized/ | 0.1 | uncompressed | 3,163 | small |
| opal_data_assets_silver_cottonwood_fact_realized_s2 | opal-data-assets/blackdiamond/cottonwood/silver/fact_realized_s2/ | 0.0 | uncompressed | 5 | small |
| opal_data_assets_silver_cottonwood_fact_transactions | opal-data-assets/blackdiamond/cottonwood/silver/fact_transactions/ | 0.5 | uncompressed | 7,311 | small |
| opal_data_assets_silver_cottonwood_fact_transactions_s2 | opal-data-assets/blackdiamond/cottonwood/silver/fact_transactions_s2/ | 0.0 | uncompressed | 5 | small |
| opal_data_assets_silver_cottonwood_fact_unrealized | opal-data-assets/blackdiamond/cottonwood/silver/fact_unrealized/ | 2.8 | uncompressed | 61,730 | small |
| opal_data_assets_silver_cottonwood_fact_unrealized_s2 | opal-data-assets/blackdiamond/cottonwood/silver/fact_unrealized_s2/ | 0.0 | uncompressed | 5 | small |

## What this proposal does not decide
- The thresholds (8 MiB, 24 MiB, 1,000,000 rows) and whether the class is stored in the catalog row, the tool_index entry or a separate file: the CTO's ruling, and PRD v0.20's ratified-text half is unsigned.
- That 2.63 holds beyond Orion `fact_transactions`; that one partition is representative of a table over time (the census reads the NEWEST partition only); a size class for a table that is read across a window of partitions (fees and transactions read a window).
- Tables whose newest partition holds hundreds or thousands of small objects (several harvest bronze tables, for example 3,000 objects of 0.4 MiB or less) are very large by listed bytes, but their cost to a reader is the object count; the census records objects_in_newest and the proposal classes on bytes and rows only.
- The plain-words meaning and the folder of each table: they already sit in the catalog rows (`business_meaning`, `prefix`); this file adds only the size field.
