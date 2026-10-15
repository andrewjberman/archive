# MCPINDEX silver table rows at merge 66f8ea1466: 216 rows (entity | row id | layer | read_tool | retired | firm_scope | bucket | key_template)

dynamodb_dynamodb_market_updates | c-4143696ffe2b | dynamodb | GAP:NFRA_OPLGTW | live | opal-internal-only | none (DynamoDB us-east-1) | none
dynamodb_dynamodb_opal_harvest_articles | c-5f47990a71d1 | dynamodb | GAP:NFRA_OPLGTW | live | opal-internal-only | none (DynamoDB us-east-1) | none
dynamodb_dynamodb_opal_harvest_security_metrics | c-9de236f72cbb | dynamodb | GAP:NFRA_OPLGTW | live | opal-internal-only | none (DynamoDB us-east-1) | none
dynamodb_dynamodb_opal_keyword_intelligence | c-d133c63fb4d8 | dynamodb | GAP:NFRA_OPLGTW | live | opal-internal-only | none (DynamoDB us-east-1) | none
dynamodb_dynamodb_opal_news_articles | c-008bf8d002bc | dynamodb | GAP:NFRA_OPLGTW | live | opal-internal-only | none (DynamoDB us-east-1, account 313476888478) | none
dynamodb_dynamodb_opal_news_trending_daily | c-9513ddfd2d6c | dynamodb | GAP:NFRA_OPLGTW | live | opal-internal-only | none (DynamoDB us-east-1) | none
dynamodb_dynamodb_seeking_alpha_article_urls | c-f661a436dee5 | dynamodb | GAP:NFRA_OPLGTW | live | opal-internal-only | none (DynamoDB us-east-1) | none
dynamodb_dynamodb_semantic_news_trending_daily | c-c05b122bef10 | dynamodb | GAP:NFRA_OPLGTW | live | opal-internal-only | none (DynamoDB us-east-1) | none
dynamodb_opal_tickets | c-2cb42abec4ad | dynamodb | GAP:NFRA_OPLGTW | live | opal-internal-only | dynamodb (not opal-data-portal-v2) | n/a -- table opal-tickets
dynamodb_opal_trade_submissions | c-3f7960fedf6f | dynamodb | GAP:NFRA_OPLGTW | live | opal-internal-only | dynamodb + s3://opal-data-trade-submissions (not opal-data-portal-v2) | n/a -- table opal-trade-submissions; files at opal-data-trade-submissions/{submissions,parquet}/
opal_data_assets_silver_49f_dim_account_xref | c-068b87add1de | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/49f/silver/dim_account_xref/
opal_data_assets_silver_49f_dim_advisor_fee_role | c-f09e2adb7b7f | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/49f/silver/dim_advisor_fee_role/
opal_data_assets_silver_49f_fact_bd_allocation | c-46a7da843940 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/49f/silver/fact_bd_allocation/
opal_data_assets_silver_49f_fact_taxsma_report | c-bea1c1455a89 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/49f/silver/fact_taxsma_report/
opal_data_assets_silver_49financial_allocations_silver_legacy | c-971931790dc6 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | null | silver/allocations/<d>.parquet
opal_data_assets_silver_49financial_assets_silver_legacy | c-a14c8a96ed2d | silver | GAP:NFRA_OPLGTW | live | firm-scoped | null | silver/assets/<d>.parquet
opal_data_assets_silver_49financial_fact_insurance_insurancerelationshiplist_export | c-2d8cb9f11e0c | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/49financial/silver/fact_insurance_insurancerelationshiplist_export/
opal_data_assets_silver_49financial_fact_insurance_relationshipaccountdetailsearch | c-93b122ff409d | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/49financial/silver/fact_insurance_relationshipaccountdetailsearch/
opal_data_assets_silver_49financial_fact_insurance_relationshipdetail | c-4e95c17c2fdf | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/49financial/silver/fact_insurance_relationshipdetail/
opal_data_assets_silver_49financial_fees_silver_legacy | c-bcb135da3897 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | null | silver/fees/<d>.parquet
opal_data_assets_silver_49financial_prices_silver_legacy | c-3337de310b4a | silver | GAP:NFRA_OPLGTW | live | firm-scoped | null | silver/prices/<d>.parquet
opal_data_assets_silver_49financial_realized_silver_legacy | c-d8a200d181a1 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | null | silver/realized/<d>.parquet
opal_data_assets_silver_49financial_single_file_silver_legacy | c-d17d9b52d456 | silver | GAP:NFRA_OPLGTW | RETIRED | firm-scoped | opal-data-assets | blackdiamond/49financial/silver_legacy/_single_file/
opal_data_assets_silver_49financial_transactions_enriched_silver_legacy | c-7ab7e7195cf4 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | null | silver/transactions_enriched/date=<d>/data.parquet
opal_data_assets_silver_49financial_transactions_silver_legacy | c-9702a0209e11 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | null | silver/transactions/<d>.parquet
opal_data_assets_silver_49financial_unrealized_silver_legacy | c-33f8ae6563b5 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | null | silver/unrealized/<d>.parquet
opal_data_assets_silver_commonwealth_cottonwood_account_day_value | c-f2cc47419174 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | commonwealth/cottonwood/silver/account_day_value/
opal_data_assets_silver_commonwealth_cottonwood_account_links | c-23e863ccc55e | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | commonwealth/cottonwood/silver/account_links/
opal_data_assets_silver_commonwealth_cottonwood_coverage | c-4b12209c93df | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | commonwealth/cottonwood/silver/coverage/
opal_data_assets_silver_commonwealth_cottonwood_crosswalk | c-2738e2f54011 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | commonwealth/cottonwood/silver/crosswalk/
opal_data_assets_silver_commonwealth_cottonwood_daily_returns | c-e28664493b67 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | commonwealth/cottonwood/silver/daily_returns/
opal_data_assets_silver_commonwealth_cottonwood_document_index | c-6f536d623cf5 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | commonwealth/cottonwood/silver/document_index/
opal_data_assets_silver_commonwealth_cottonwood_documents | c-3d628107358d | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | commonwealth/cottonwood/silver/documents/
opal_data_assets_silver_commonwealth_cottonwood_month_grades | c-40e88fdf5735 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | commonwealth/cottonwood/silver/month_grades/
opal_data_assets_silver_commonwealth_cottonwood_performance | c-da4f579f70df | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | commonwealth/cottonwood/silver/performance/
opal_data_assets_silver_commonwealth_cottonwood_positions | c-fe97cbadee58 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | commonwealth/cottonwood/silver/positions/
opal_data_assets_silver_commonwealth_cottonwood_price_evidence | c-3f517fc2fab7 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | commonwealth/cottonwood/silver/price_evidence/
opal_data_assets_silver_commonwealth_cottonwood_transactions | c-59badf831c6b | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | commonwealth/cottonwood/silver/transactions/
opal_data_assets_silver_cottonwood_fact_allocations | c-cb0bf9114572 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/cottonwood/silver/fact_allocations/
opal_data_assets_silver_cottonwood_fact_allocations_s2 | c-6bf0e4f9e062 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/cottonwood/silver/fact_allocations_s2/
opal_data_assets_silver_cottonwood_fact_holdings | c-831f78936cbc | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/cottonwood/silver/fact_holdings/
opal_data_assets_silver_cottonwood_fact_holdings_s2 | c-9b2ef4d58efe | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/cottonwood/silver/fact_holdings_s2/
opal_data_assets_silver_cottonwood_fact_model_assignment | c-d0b89683d3a6 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/cottonwood/silver/fact_model_assignment/
opal_data_assets_silver_cottonwood_fact_model_blend | c-0943508aab88 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/cottonwood/silver/fact_model_blend/
opal_data_assets_silver_cottonwood_fact_model_definition | c-fd4fb3d1fcb1 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/cottonwood/silver/fact_model_definition/
opal_data_assets_silver_cottonwood_fact_model_roster | c-f246861e133b | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/cottonwood/silver/fact_model_roster/
opal_data_assets_silver_cottonwood_fact_realized | c-bb5ebb0fbbac | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/cottonwood/silver/fact_realized/
opal_data_assets_silver_cottonwood_fact_realized_s2 | c-39672f3e83d0 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/cottonwood/silver/fact_realized_s2/
opal_data_assets_silver_cottonwood_fact_transactions | c-9917b00882bc | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/cottonwood/silver/fact_transactions/
opal_data_assets_silver_cottonwood_fact_transactions_s2 | c-dcf29e598561 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/cottonwood/silver/fact_transactions_s2/
opal_data_assets_silver_cottonwood_fact_unrealized | c-0e84a90b9641 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/cottonwood/silver/fact_unrealized/
opal_data_assets_silver_cottonwood_fact_unrealized_s2 | c-df478a4f3835 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | blackdiamond/cottonwood/silver/fact_unrealized_s2/
opal_data_assets_silver_eclipse_inflection_fact_model_composition | c-bbd4f6140ad6 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | eclipse/inflection/silver/fact_model_composition/
opal_data_assets_silver_eclipse_inflection_fact_models | c-3a6ef0dbe4cd | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | eclipse/inflection/silver/fact_models/
opal_data_assets_silver_eclipse_inflection_fact_portfolios_full | c-fc6a1328bb3d | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | eclipse/inflection/silver/fact_portfolios_full/
opal_data_assets_silver_eclipse_inflection_fact_portfolios_simple | c-f8e09ce8baf1 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | eclipse/inflection/silver/fact_portfolios_simple/
opal_data_assets_silver_gateway_global_taxsma_workbook | c-814530e9c561 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | gateway/global/silver/taxsma_workbook/
opal_data_assets_silver_orion_4698_account_performance_gross | c-f239f09c2fe1 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | orion/4698/silver/account_performance_gross/
opal_data_assets_silver_orion_inflection_fact_assets | c-d3176e6b1404 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | orion/inflection/silver/fact_assets/
opal_data_assets_silver_orion_inflection_fact_performance | c-576bc07d5790 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | orion/inflection/silver/fact_performance/
opal_data_assets_silver_orion_inflection_fact_positions | c-5cde759e5343 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | orion/inflection/silver/fact_positions/
opal_data_assets_silver_orion_inflection_fact_transactions | c-32b7fec53660 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | orion/inflection/silver/fact_transactions/
opal_data_assets_silver_pathfinder_pfde_fact_dailynav | c-736aa032d8e3 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | pathfinder/PFDE/silver/fact_dailynav/
opal_data_assets_silver_pathfinder_pfde_fact_holdings | c-71acf83124bf | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | pathfinder/PFDE/silver/fact_holdings/
opal_data_assets_silver_pathfinder_pfoe_fact_dailynav | c-07de6c102300 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | pathfinder/PFOE/silver/fact_dailynav/
opal_data_assets_silver_pathfinder_pfoe_fact_holdings | c-c7e6a6a851ff | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | pathfinder/PFOE/silver/fact_holdings/
opal_data_assets_silver_schwab_08242234_fact_acc | c-becfdddc34cb | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08242234/silver/fact_acc/
opal_data_assets_silver_schwab_08242234_fact_rld | c-be959e776ba3 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08242234/silver/fact_rld/
opal_data_assets_silver_schwab_08242234_fact_rlu | c-fc283bf6b74e | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08242234/silver/fact_rlu/
opal_data_assets_silver_schwab_08242234_fact_rlw | c-3328458ad957 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08242234/silver/fact_rlw/
opal_data_assets_silver_schwab_08242234_fact_rly | c-345509217363 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08242234/silver/fact_rly/
opal_data_assets_silver_schwab_08242234_fact_rps | c-bbe6b1c2f09c | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08242234/silver/fact_rps/
opal_data_assets_silver_schwab_08242234_fact_rps_s2 | c-89970814b79c | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08242234/silver/fact_rps_s2/
opal_data_assets_silver_schwab_08242234_fact_rtu | c-bda84bed7a76 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08242234/silver/fact_rtu/
opal_data_assets_silver_schwab_08242234_fact_rty | c-b6960191e8a6 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08242234/silver/fact_rty/
opal_data_assets_silver_schwab_08242234_fact_sec | c-c5505048940e | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08242234/silver/fact_sec/
opal_data_assets_silver_schwab_08242234_fact_trn | c-32c0f62978db | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08242234/silver/fact_trn/
opal_data_assets_silver_schwab_08242234_fact_uln | c-dc5128fad1b8 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08242234/silver/fact_uln/
opal_data_assets_silver_schwab_08242234_fact_ult | c-5bb6c482b754 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08242234/silver/fact_ult/
opal_data_assets_silver_schwab_08242234_fact_upn | c-400ca90b2f01 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08242234/silver/fact_upn/
opal_data_assets_silver_schwab_08242234_fact_upt | c-d07b0eaf1dc0 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08242234/silver/fact_upt/
opal_data_assets_silver_schwab_08335338_fact_acc | c-834f0cb1890a | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_acc/
opal_data_assets_silver_schwab_08335338_fact_fam | c-a8121d906e8c | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_fam/
opal_data_assets_silver_schwab_08335338_fact_rld | c-8707eb0f2089 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_rld/
opal_data_assets_silver_schwab_08335338_fact_rlu | c-ec9059c5cdb5 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_rlu/
opal_data_assets_silver_schwab_08335338_fact_rly | c-c42814432bac | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_rly/
opal_data_assets_silver_schwab_08335338_fact_rps | c-d226f704ccce | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_rps/
opal_data_assets_silver_schwab_08335338_fact_rps_s2 | c-ea14f9f131c8 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_rps_s2/
opal_data_assets_silver_schwab_08335338_fact_rtu | c-80721725583d | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_rtu/
opal_data_assets_silver_schwab_08335338_fact_rty | c-a1f8ab359dd2 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_rty/
opal_data_assets_silver_schwab_08335338_fact_sec | c-d90dc0946e91 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_sec/
opal_data_assets_silver_schwab_08335338_fact_slm | c-cca07f67c7d7 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_slm/
opal_data_assets_silver_schwab_08335338_fact_trn | c-a066a0f21196 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_trn/
opal_data_assets_silver_schwab_08335338_fact_uln | c-4eaeb5c8d01d | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_uln/
opal_data_assets_silver_schwab_08335338_fact_ult | c-0f279457582d | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_ult/
opal_data_assets_silver_schwab_08335338_fact_upn | c-ed0da9f50bf9 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_upn/
opal_data_assets_silver_schwab_08335338_fact_upt | c-d638c9baffd0 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08335338/silver/fact_upt/
opal_data_assets_silver_schwab_08403355_fact_acc | c-84522b84b9e9 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08403355/silver/fact_acc/
opal_data_assets_silver_schwab_08403355_fact_rld | c-e957819e3f35 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08403355/silver/fact_rld/
opal_data_assets_silver_schwab_08403355_fact_rlu | c-844308f958f5 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08403355/silver/fact_rlu/
opal_data_assets_silver_schwab_08403355_fact_rly | c-65d0b60855d0 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08403355/silver/fact_rly/
opal_data_assets_silver_schwab_08403355_fact_rps | c-9615a74e5795 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08403355/silver/fact_rps/
opal_data_assets_silver_schwab_08403355_fact_rps_s2 | c-bf4432bb5a39 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08403355/silver/fact_rps_s2/
opal_data_assets_silver_schwab_08403355_fact_rtu | c-170379e95b79 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08403355/silver/fact_rtu/
opal_data_assets_silver_schwab_08403355_fact_rty | c-8faa4391019c | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08403355/silver/fact_rty/
opal_data_assets_silver_schwab_08403355_fact_sec | c-21d902b09057 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08403355/silver/fact_sec/
opal_data_assets_silver_schwab_08403355_fact_trn | c-1b2905207f22 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08403355/silver/fact_trn/
opal_data_assets_silver_schwab_08403355_fact_uln | c-73c0403ec460 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08403355/silver/fact_uln/
opal_data_assets_silver_schwab_08403355_fact_ult | c-859c6ab90323 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08403355/silver/fact_ult/
opal_data_assets_silver_schwab_08403355_fact_upn | c-1f066340d1ba | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08403355/silver/fact_upn/
opal_data_assets_silver_schwab_08403355_fact_upt | c-6dc27e0a29f2 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | schwab/08403355/silver/fact_upt/
opal_data_assets_silver_smartx_allocation_positions_draft | c-397fc94ec3c6 | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-assets | smartx/platform/silver/allocation_positions/
opal_data_assets_silver_smartx_allocation_valuation_draft | c-55c26c656fa1 | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-assets | smartx/platform/silver/allocation_valuation/
opal_data_assets_silver_smartx_fact_account_allocations | c-ff70229eb5e4 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | smartx/platform/silver/fact_account_allocations/
opal_data_assets_silver_smartx_fact_account_detail | c-5353cf6079b4 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | smartx/platform/silver/fact_account_detail/
opal_data_assets_silver_smartx_fact_allocation_account_map | c-b18254523fde | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | smartx/platform/silver/fact_allocation_account_map/
opal_data_assets_silver_smartx_fact_allocation_positions | c-98bc4f8c892b | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | smartx/platform/silver/fact_allocation_positions/
opal_data_assets_silver_smartx_fact_allocation_valuation | c-c272a074490e | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | smartx/platform/silver/fact_allocation_valuation/
opal_data_assets_silver_smartx_fact_model_allocation_roster | c-a659bf0c7384 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | smartx/platform/silver/fact_model_allocation_roster/
opal_data_assets_silver_smartx_fact_model_aum_daily | c-07918576485b | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-assets | smartx/platform/silver/fact_model_aum_daily/
opal_data_assets_silver_smartx_fact_model_changerequests | c-27120c920e98 | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-assets | smartx/platform/silver/fact_model_changerequests/
opal_data_assets_silver_smartx_fact_model_holdings | c-9b40dd7fb102 | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-assets | smartx/platform/silver/fact_model_holdings/
opal_data_assets_silver_smartx_fact_model_performance | c-899f0f426bbd | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-assets | smartx/platform/silver/fact_model_performance/
opal_data_assets_silver_smartx_fact_nonzerosleeve | c-12ecc02b42f9 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | smartx/platform/silver/fact_nonzerosleeve/
opal_data_assets_silver_trueshares_divz_fact_holdings | c-6b2a91a2b1ba | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | trueshares/DIVZ/silver/fact_holdings/
opal_data_assets_silver_trueshares_divz_fact_netassets_page | c-6aa636837e86 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | trueshares/DIVZ/silver/fact_netassets_page/
opal_data_assets_silver_trueshares_idvz_fact_holdings | c-841c185cfe13 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | trueshares/IDVZ/silver/fact_holdings/
opal_data_assets_silver_trueshares_idvz_fact_netassets_page | c-9f76449220b1 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-assets | trueshares/IDVZ/silver/fact_netassets_page/
opal_data_assets_silver_yahoo_global_price_history | c-1c3389a99aab | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-assets | yahoo/global/silver/price_history/
opal_data_etfs_config_etf_universe | c-826b59ec58da | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | config/etf_universe.json
opal_data_etfs_gold_book | c-fc3803f3ed55 | gold | etfs_get_positioning | live | opal-internal-only | opal-data-etfs | gold/book/date={YYYY-MM-DD}/book.parquet
opal_data_etfs_gold_buying_trend | c-661f9bbafd36 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | rivalfunds/etfs/gold/buying_trend/date={D}/<part>.parquet
opal_data_etfs_gold_canonical_shape | c-c2e3b838dd34 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | rivalfunds/etfs/gold/canonical_shape/date={D}/<part>.parquet
opal_data_etfs_gold_corporate_actions | c-9cb4120aa590 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | rivalfunds/etfs/gold/corporate_actions/date={D}/<part>.parquet
opal_data_etfs_gold_daily_partner_ownership | c-ff1f33b6ca1d | gold | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-etfs | daily/{partner}/{YYYY-MM-DD}.json
opal_data_etfs_gold_flow_reconciliation | c-16b066d81943 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | rivalfunds/etfs/gold/flow_reconciliation/date={D}/<part>.parquet
opal_data_etfs_gold_holding | c-7113cef03772 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | gold/holding/date={YYYY-MM-DD}/holding.parquet
opal_data_etfs_gold_holding_contribution | c-136a54d516b0 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | rivalfunds/etfs/gold/holding_contribution/date={D}/<part>.parquet
opal_data_etfs_gold_holdings_coverage | c-1b6f6b25d324 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | rivalfunds/etfs/gold/holdings_coverage/date={D}/<part>.parquet
opal_data_etfs_gold_input_census | c-8c722856f550 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | rivalfunds/etfs/gold/input_census/date={D}/<part>.parquet
opal_data_etfs_gold_mdpf_new_securities | c-b6326c5a36a4 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | mdpf/etfs/gold/new_securities/date={D}/new_securities.json
opal_data_etfs_gold_peer_group_map | c-97afd86d5d02 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | rivalfunds/etfs/gold/peer_group_map/date={D}/<part>.parquet
opal_data_etfs_gold_research_hypotheses | c-cf75738b9be9 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | rivalfunds/etfs/gold/research_hypotheses/date={D}/<part>.parquet
opal_data_etfs_gold_security_market | c-fa02110e7004 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | rivalfunds/etfs/gold/security_market/date={D}/<part>.parquet
opal_data_etfs_gold_security_names | c-912b16998f5c | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | rivalfunds/etfs/gold/security_names/date={D}/<part>.parquet
opal_data_etfs_gold_security_universe | c-ef8e5499a53e | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | rivalfunds/etfs/gold/security_universe/date={D}/<part>.parquet
opal_data_etfs_gold_trade_schedule | c-27cfedd352a5 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | rivalfunds/etfs/gold/trade_schedule/date={D}/<part>.parquet
opal_data_etfs_platinum_etf_ownership_dashboard | c-9156b2c365de | platinum | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-etfs | platinum/etf_ownership_dashboard.json
opal_data_etfs_platinum_monthly_ownership_report | c-e01461a48c79 | platinum | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-etfs | platinum/reports/{YYYY-MM}/
opal_data_etfs_platinum_rivalfunds_page | c-6b8e81cab3bf | platinum | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | rivalfunds/etfs/platinum/page/date={D}/{index.html,manifest.json,audit}
opal_data_etfs_silver_bbg_characteristics | c-479c053f0e37 | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | bbg/{YYYY-MM-DD as_of}/characteristics.parquet
opal_data_etfs_silver_bbg_constituents_issuer_fill | c-ad97ceb698c3 | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | bbg/{YYYY-MM-DD as_of}/constituents/constituents_issuer_fill.parquet
opal_data_etfs_silver_bbg_derived_geo_allocation | c-9467dd2bdcda | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | bbg/{YYYY-MM-DD as_of}/constituents/derived_geo_allocation.parquet
opal_data_etfs_silver_bbg_derived_sector_allocation | c-1e34f2e046cd | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | bbg/{YYYY-MM-DD as_of}/constituents/derived_sector_allocation.parquet
opal_data_etfs_silver_bbg_derived_summary | c-e8ccd6e27b97 | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | bbg/{YYYY-MM-DD as_of}/constituents/derived_summary.parquet
opal_data_etfs_silver_bbg_fund_daily | c-18fb67b97cce | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | bbg/{YYYY-MM-DD as_of}/fund_daily.parquet
opal_data_etfs_silver_bbg_history_topup | c-a58377a63dca | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | bbg/{YYYY-MM-DD as_of}/history_topup.parquet
opal_data_etfs_silver_bloomberg_etf_holdings | c-cc1a71b9de7d | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | bloomberg/etfs/silver/holdings/date={D}/{FUND}-{batch}.parquet
opal_data_etfs_silver_bloomberg_history_gaps | c-9d38d11f7924 | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | bloomberg/etfs/silver/history_gaps/as_of={D}/gap_record.json
opal_data_etfs_silver_etf_history_csv | c-17776d4388b2 | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | etf_history.csv
opal_data_etfs_silver_holdings | c-a7871a05f171 | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | silver/holdings/{YYYY-MM-DD}.parquet
opal_data_etfs_silver_issuer_site_holdings | c-37591f249cdd | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | issuer-site/etfs/silver/holdings/date={D}/{issuer}-{batch}.parquet
opal_data_etfs_silver_netassets | c-22d23348fecb | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | silver/netassets/{YYYY-MM-DD}.parquet
opal_data_etfs_silver_netassets_daily | c-f040a4641168 | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | silver/netassets_daily.parquet
opal_data_etfs_silver_snapshots | c-45a8877abcc6 | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-etfs | snapshots/snapshot_{YYYY-MM-DD}.json
opal_data_mdpf_feeds_etf_net_assets | c-78ac4cc17f7f | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-mdpf | mdpf/feeds/etf_net_assets/
opal_data_mdpf_feeds_model_aua_positions_49financial | c-196ff79bae06 | silver | GAP:NFRA_OPLGTW | RETIRED | firm-scoped | opal-data-mdpf | mdpf/feeds/model_aua_positions/49financial/
opal_data_mdpf_feeds_model_aua_positions_inflection | c-0a6e44470158 | silver | GAP:NFRA_OPLGTW | RETIRED | firm-scoped | opal-data-mdpf | mdpf/feeds/model_aua_positions/inflection/
opal_data_mdpf_feeds_model_composition | c-759e6e36ccb7 | silver | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-mdpf | mdpf/feeds/model_composition/<firm>/
opal_data_mdpf_feeds_non_model_aua | c-84f5c4c77081 | silver | GAP:NFRA_OPLGTW | RETIRED | firm-scoped | opal-data-mdpf | mdpf/feeds/non_model_aua/<firm>/
opal_data_mdpf_feeds_partner_held_etf_49financial | c-1c09ce5c4a9e | silver | GAP:NFRA_OPLGTW | RETIRED | firm-scoped | opal-data-mdpf | mdpf/feeds/partner_held_etf/49financial/
opal_data_mdpf_gold_ai_classified_securities | c-2ac840b20449 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-mdpf | mdpf/global/gold/ai_classified_securities/date=<YYYY-MM-DD>/index.json
opal_data_news_av_silver_seeking_alpha | c-40bf707f1bd6 | silver | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-news-av | seeking-alpha/{news,analysis}/
opal_data_news_v2_gold_semantic_clusters | c-2d2da10a2528 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-news-v2 | semantic_clusters/
opal_data_news_v2_gold_trending_reports | c-b925ca57deb4 | gold | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-news-v2 | trending_reports/
opal_data_portal_v2_platinum_advi_49financial_perfrp | c-1db3c93b1ae0 | platinum | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-portal-v2 | platinum/advi/49financial/perfrp_{book_advisor,gainloss_account,gainloss_relationship}.json
opal_data_portal_v2_platinum_advi_49financial_twins | c-cf4e62d5b3c4 | platinum | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-portal-v2 | platinum/advi/49financial/{mix_summary,leaderboard,ownership_map,timeseries_overview,cumulative_chart,clients-tab-slim,timeseries_chart,timeseries_chart_full,partner_analytics_quarterly,partner_analytics_annual}.json + _manifests/
opal_data_portal_v2_platinum_etfs_positioning_data | c-b55d6853bf0f | platinum | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | platinum/etfs/positioning_data.json (+ _manifests/)
opal_data_portal_v2_platinum_mdpf_account_distribution | c-6d9e3b7857e6 | platinum | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-portal-v2 | platinum/mdpf/{scope}/account-distribution.json
opal_data_portal_v2_platinum_mdpf_aggregate_aua_timeseries | c-cd7f4962b398 | platinum | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-portal-v2 | platinum/mdpf/{scope}/aggregate-aua-timeseries.json
opal_data_portal_v2_platinum_mdpf_aum_metrics | c-e6f9a7a1607e | platinum | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-portal-v2 | platinum/mdpf/{scope}/aum-metrics.json
opal_data_portal_v2_platinum_mdpf_category_views | c-5902fd256409 | platinum | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-portal-v2 | platinum/mdpf/{scope}/category-views.json
opal_data_portal_v2_platinum_mdpf_cottonwood_account_units | c-ea8574648ef4 | platinum | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-portal-v2 | platinum/mdpf/cottonwood/account-units.json
opal_data_portal_v2_platinum_mdpf_manifests_and_archive | c-efe717f6c230 | platinum | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-portal-v2 | platinum/mdpf/{_manifests/,archive/}
opal_data_portal_v2_platinum_mdpf_non_model_assets | c-9505c3517893 | platinum | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | platinum/mdpf/global/non-model-assets.json
opal_data_portal_v2_served_allocation_summary | c-0327f7206c46 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/positioning/allocation_summary.json
opal_data_portal_v2_served_benchmark_returns | c-74105180cb8e | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/benchmarks/benchmark_returns.json
opal_data_portal_v2_served_cma_assumptions | c-147c0a0a4ab8 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/capital-markets/assumptions.json
opal_data_portal_v2_served_cma_views | c-1778833ca208 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/capital-markets/views.json
opal_data_portal_v2_served_correlation_data | c-82b2ae9cf720 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/correlations/correlation_data.json
opal_data_portal_v2_served_etf_returns | c-4d5bcd2a8226 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/benchmarks/etf_returns.json
opal_data_portal_v2_served_factor_tilts | c-dd0416e0f769 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/factor-tilts/{tier1-snapshot,tier2-spreads,tier3-timeseries}.json
opal_data_portal_v2_served_holdings_attribution_data | c-1988578911ae | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/positioning/holdings_attribution_data.json
opal_data_portal_v2_served_keyword_history | c-0b9dea331995 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/sentiment/keyword-history-{articles,summary}/{keyword}.json
opal_data_portal_v2_served_macro_data | c-a880cac23d65 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/macro/macro_data.json (+ macro_data_fred.json)
opal_data_portal_v2_served_macro_timeseries | c-0e0ede7b9f52 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/macro/timeseries/{slug}.json
opal_data_portal_v2_served_market_all_returns_legacy | c-02f9f4af122f | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/market/all_returns.json
opal_data_portal_v2_served_market_overview_tiered | c-fdeb68d84789 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json-tiered/market-overview/{summary/all-returns.json, rsi-summary.json, rsi-details-{equities,fixedIncome,commodities}.json, timeseries/{ticker}.json, details/{ticker}.json}
opal_data_portal_v2_served_market_regime | c-095929ce1904 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/market/market-regime.json (+ market-regime-history.json)
opal_data_portal_v2_served_model_portfolio_benchmarks | c-563154f16918 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/benchmarks/model_portfolio_benchmarks.json
opal_data_portal_v2_served_model_portfolio_timeseries | c-3b7d2331c5c4 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/benchmarks/model_portfolio_timeseries.json
opal_data_portal_v2_served_model_portfolios_views | c-50fb9755cb8e | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/model_portfolios/views/{by_assetclass,by_period}/*.json + latest/manifest/summary.json
opal_data_portal_v2_served_news_trending_and_sentiment | c-11e0ad30e7be | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/trending/latest.json; json/sentiment/{fear-greed-index,keyword-sentiments}.json; json/sentiment/keyword-history-{summary,articles}/; json/semantic-trending/latest.json; sentiment/ (legacy)
opal_data_portal_v2_served_opal_aggregate | c-0d5e4eb86d97 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/positioning/opal_aggregate.json
opal_data_portal_v2_served_peer_performance | c-8e9c92c8e765 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/peers/peer_performance.json
opal_data_portal_v2_served_pipeline_manifest | c-7311a8d44d42 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/latest/manifest.json (+ json/latest/{data_pkl,model_pkl,attribution_excel,peer_excel,cma_excel}.json)
opal_data_portal_v2_served_portfolios_legacy | c-f125af5a6726 | served | GAP:NFRA_OPLGTW | live | firm-scoped | opal-data-portal-v2 | json/portfolios/{aum-metrics,account-distribution,aum-timeseries}.json + json/portfolios/<firm>/account-distribution.json
opal_data_portal_v2_served_positioning_data | c-ffc5cfb35125 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/positioning/positioning_data.json
opal_data_portal_v2_served_risk_premium_data | c-70f0bfd04e98 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/valuation/risk_premium_data.json
opal_data_portal_v2_served_security_scanner | c-c8831dfc514d | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/security_scanner/latest/{factor_metadata.json, universes/{universe}/{universe_data,scanner_data}.json}
opal_data_portal_v2_served_sentiment_singletons | c-f5d0be208a76 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/sentiment/{fear-greed-index,keyword-sentiments}.json
opal_data_portal_v2_served_smartx_model_performance | c-91aa67970f7b | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/benchmarks/_smartx_model_{daily,monthly}.json
opal_data_portal_v2_served_trending_latest | c-3a11e22b6be6 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/trending/latest.json
opal_data_portal_v2_served_valuation_data | c-a488fb56cfcf | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/valuation/valuation_data.json
opal_data_portal_v2_served_volatility_data | c-57158a96fbf2 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/macro/volatility_data.json (+ vix_data.json)
opal_data_portal_v2_served_yield_curve_fred | c-a4ce22e18787 | served | GAP:NFRA_OPLGTW | live | opal-internal-only | opal-data-portal-v2 | json/macro/yield_curve_fred.json
