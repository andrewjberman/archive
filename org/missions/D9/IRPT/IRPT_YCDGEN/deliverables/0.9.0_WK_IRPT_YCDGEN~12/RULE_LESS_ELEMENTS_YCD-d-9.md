# Rule-less Opal-held elements, YCD-d-9

Counted by script from the map and held_data.RULES: map elements 254, Opal-held 158, rule-less 70.

PARTIAL = related data of the same kind is kept, not this figure per security. NOT_SEEN_IN_REPO = the search found nothing; it is not a claim that Opal lacks the data. A family with a mix lists the counts.

| input family | elements | why no rule (held_data) | feedable | best evidence |
|---|---|---|---|---|
| bond_maturity | 17 | bond-sleeve look-through share; no Opal table holds it per holding / a multi-column group needs every column held, and not every column is | PARTIAL | infra/aws/terraform/yang-pipeline/etf-classifications.tf:12 |
| alpha_5y | 1 | no Opal table holds a per-holding alpha | NOT_SEEN_IN_REPO | none |
| asset_allocation | 4 | no asset-class label means cash; a zero cannot be told from an unlabelled holding / a multi-column group needs every column held, and not every column is / no asset-class label means convertible / no asset-class label means preferred | PARTIAL | infra/aws/terraform/yang-pipeline/etf-classifications.tf:7 |
| average_coupon | 1 | no Opal table holds this figure per holding | NOT_SEEN_IN_REPO | none |
| average_price | 1 | no Opal table holds this figure per holding | NOT_SEEN_IN_REPO | none |
| avg_credit | 1 | no Opal table holds this figure per holding | NOT_SEEN_IN_REPO | integrations/bloomberg/pipeline/etf_daily_pull.py:606 |
| beta_5y | 1 | the held beta is Bloomberg's adjusted beta (BETA_ADJ_OVERRIDABLE), not the 5-year beta | PARTIAL | integrations/bloomberg/pipeline/etf_daily_pull.py:607 |
| bond_credit | 8 | bond-sleeve look-through share; no Opal table holds it per holding | NOT_SEEN_IN_REPO | integrations/bloomberg/pipeline/etf_daily_pull.py:606 |
| bond_sector | 7 | bond-sleeve look-through share; no Opal table holds it per holding / a multi-column group needs every column held, and not every column is | PARTIAL | infra/aws/terraform/yang-pipeline/etf-classifications.tf:11 |
| cash_net | 1 | net cash allocation (cash net of shorts) is not held; the asset-class label carries no cash | NOT_SEEN_IN_REPO | none |
| current_yield | 1 | no Opal table holds this figure per holding | NOT_SEEN_IN_REPO | none |
| distribution_yield | 2 | distribution yield is a fund measure; the held field is a stock's indicated dividend yield | PARTIAL | integrations/bloomberg/pipeline/etf_daily_pull.py:606 |
| effective_duration | 1 | bond-sleeve figure; the held duration field (HB_OAS_EFF_DURTN) is empty for every holding the upload's census found, and the sleeve weights need a look-through bond share Opal does not hold | PARTIAL | integrations/bloomberg/pipeline/etf_daily_pull.py:606 |
| level_series | 1 | price history is held for only part of the holdings (a series for the whole portfolio is not buildable) | PARTIAL | integrations/bloomberg/pipeline/etf_daily_pull.py:67 |
| market_cap | 6 | market-cap bucket and style-box shares are vendor-defined look-throughs; Opal holds a market cap and no bucket / a multi-column group needs every column held, and not every column is | PARTIAL | integrations/bloomberg/pipeline/etf_daily_pull.py:621 |
| number_of | 1 | the held count (TOTAL_NUMBER_OF_HOLDINGS_IN_PORT) is a fund's own count, not the portfolio's look-through count | PARTIAL | integrations/bloomberg/pipeline/etf_daily_pull.py:605 |
| of_bond | 1 | no Opal table holds this figure per holding | NOT_SEEN_IN_REPO | integrations/bloomberg/pipeline/etf_daily_pull.py:145 |
| of_stock | 1 | no Opal table holds this figure per holding | NOT_SEEN_IN_REPO | integrations/bloomberg/pipeline/etf_daily_pull.py:145 |
| stock_style | 9 | market-cap bucket and style-box shares are vendor-defined look-throughs; Opal holds a market cap and no bucket | PARTIAL | infra/aws/terraform/yang-pipeline/etf-classifications.tf:8 |
| weighted_avg | 4 | no Opal table holds this figure per holding | NOT_SEEN_IN_REPO 2, PARTIAL 2 | integrations/bloomberg/research/model_block_pull.py:238 |
| yield_to | 1 | no Opal table holds this figure per holding | PARTIAL | infra/aws/lambda/opal-assets/opal-assets-silver-schwab/schwab_schemas.py:386 |
