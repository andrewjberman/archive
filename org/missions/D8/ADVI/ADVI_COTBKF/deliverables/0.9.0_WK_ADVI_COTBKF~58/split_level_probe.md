# split level probe (ADVI_COTBKF-D2-S45)

Day 2022-10-12; Yahoo yahoo/yfinance; as_traded = Close x product of splits dated after the day.

| cusip | symbol | symbol source | Close | splits after | factor | as_traded | r28 | r26 | Yahoo split 2024-10-10/11 matches rows |
|---|---|---|---|---|---|---|---|---|---|
| 808524102 | SCHB | delivery transactions Symbol column (most common), as commonwealth_price_need.symbols_of | 13.9800 | 2024-10-11:x3 | 3 | 41.9400 | 39.9906 | 13.3302 | True |
| 808524839 | SCHZ | delivery transactions Symbol column (most common), as commonwealth_price_need.symbols_of | 22.4650 | 2024-10-11:x2 | 2 | 44.9300 | 39.4362 | 19.7181 | True |

Branch (rule in script header, tol 2%): **OTHER**

Key: `s3://opal-data-assets/commonwealth/cottonwood/silver/price_evidence/date=2022-10-12/part-00000.parquet` (written)
