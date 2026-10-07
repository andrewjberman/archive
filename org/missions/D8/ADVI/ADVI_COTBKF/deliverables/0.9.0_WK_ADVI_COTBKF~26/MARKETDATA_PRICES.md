# Commonwealth marketdata price output, round 10 CB-j-1 (2026-10-07T12:20Z)

Located: writer `historical-prices-scheduler`, bucket `opal-data-bd`, prefix `silver/historical_prices.parquet`. bucket: source default of env BD_S3_BUCKET at data/black_diamond/scripts/silver/fetch_historical_prices_yfinance.py (the function sets no BD_S3_BUCKET); key: constant HISTORICAL_PRICES_KEY used by an upload call (data/black_diamond/scripts/silver/fetch_historical_prices_yfinance.py).

Grade: **BARRED** (BARRED, firm `49financial`, plane `alias`). Calls made under a BARRED bucket (counted by a client wrapper): 0. Nothing was invoked, written or sent to a vendor.

Counts (need 9388961 security-days; a BARRED or NOT_FOUND store is not censused): securities 0, security-days 0, gain over the six stores 0 securities / 0 security-days.

## What was read

- `historical-prices-yfinance`: configuration not found: ResourceNotFoundException; env keys none; source none found
- `historical-prices-scheduler`: configuration found; env keys none; source infra/aws/lambda/historical-prices-scheduler/lambda_function.py, data/black_diamond/scripts/silver/fetch_historical_prices_yfinance.py
