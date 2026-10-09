# bond_custodian_price (CB-ak-1)

Read-only. Class rule: see the module docstring (committed first). Sources are Cottonwood's own: the
Commonwealth silver tables and the cot canonical stores. Foreign-label token set: ['49f', '49f:acct:', '49financial', 'acct', 'bbg', 'bd', 'bd49f', 'blackdiamond', 'bloomberg', 'constant', 'data', 'demo', 'derived', 'f', 'f-49f', 'f-inf', 'fir', 'fir_', 'inf', 'inflection', 'mockadv', 'opal', 'opal-data-49financial', 'opal-data-bd', 'opal-data-demo', 'opal-data-inf', 'opal-data-inflection', 'override', 'proxy', 'trade', 'txn', 'yahoo', 'yfinance']

Held days: daily_holdings_table over 1416497 transaction rows: 988 account-days for the 3 CUSIPs (05613L3H2=0, 95000U2D4=988, 651639AX4=0)

## Source A: Commonwealth silver transactions (s3://opal-data-assets/commonwealth/cottonwood/silver/transactions/date=2026-06-23)
table rows 1416497; rows for the 3 CUSIPs 10; price-like columns in the schema: ['Amount', 'Cost_Date']

## Source B: Commonwealth silver positions (s3://opal-data-assets/commonwealth/cottonwood/silver/positions/date=2026-06-23)
table rows 469; rows for the 3 CUSIPs 0; columns ['Advisor_ID', 'AccountNumber', 'Cusip', 'FundCode', 'Symbol', 'Security_Description', 'Quantity', 'LongShort_Indicator', 'Position_Type', 'AsOfDate', 'Account_Status', 'source_zip', 'source_zip_sha256', 'source_file', 'source_line', 'source_record']; price-like columns: []

Performance table (not read for rows): columns are returns/benchmarks per account-period, no security key.

## Source C: cot canonical stores
- silver-canonical-prices: 1 object, 11291021 rows, columns ['date', 'asset_name', 'ticker', 'price', 'source']
-   matched on ticker: 0 rows
- gold-canonical-holdings: bucket opal-data-cot prefix gold/canonical/holdings/: 133 objects listed (paginated)
-   rows scanned 1515703; objects with a CUSIP hit 86
-   column set x47 objects: ['date', 'account_id', 'asset_name', 'units', 'price', 'market_value', 'source', 'bd_units', 'schwab_units', 'ticker']
-   column set x51 objects: ['date', 'account_id', 'asset_name', 'units', 'price', 'market_value', 'source', 'bd_units', 'schwab_units', 'ticker', 'cusip', 'cash_equivalent']
-   column set x35 objects: ['date', 'account_id', 'asset_name', 'units', 'price', 'market_value', 'source', 'bd_units', 'schwab_units', 'ticker', 'cusip', 'cash_equivalent', 'holding_supervised', 'account_supervised']

## 05613L3H2
held account-days 0 on 0 distinct dates (- .. -)

Transactions: 0 rows. By Transaction_Type: {}
Trade rows with Amount and Quantity (abs(Amount)/abs(Quantity)): 0 rows, 0 trade dates, - .. -
Positions rows: 0 (Quantity only; no price field)
cot store rows keyed by this CUSIP: 0

COVERAGE 05613L3H2: held account-days with a counted price on that date 0 of 0; distinct held dates covered 0 of 0
CLASS 05613L3H2 = none

## 95000U2D4
held account-days 988 on 988 distinct dates (2022-06-08 .. 2026-05-15)

Transactions: 10 rows. By Transaction_Type: {"by": 1, "int": 8, "lo": 1}
Trade rows with Amount and Quantity (abs(Amount)/abs(Quantity)): 1 rows, 1 trade dates, 2022-06-08 .. 2022-06-08
  - 2022-06-08 by acct 0QF879090 qty 25000.0 amount 25156.69 px 1.006268 desc Wells Fargo &co Ser Q MTN Call: Make Who
Positions rows: 0 (Quantity only; no price field)
cot store rows keyed by this CUSIP: 172
  - store gold-canonical-holdings field market_value label 'bd_snapshot' status foreign:bd: 86 rows, 86 with price>0, dates 2026-06-08 .. 2026-10-08
  - store gold-canonical-holdings field price label 'bd_snapshot' status foreign:bd: 86 rows, 86 with price>0, dates 2026-06-08 .. 2026-10-08

COVERAGE 95000U2D4: held account-days with a counted price on that date 1 of 988; distinct held dates covered 1 of 988
CLASS 95000U2D4 = trade_only:silver-transactions Amount/Quantity

## 651639AX4
held account-days 0 on 0 distinct dates (- .. -)

Transactions: 0 rows. By Transaction_Type: {}
Trade rows with Amount and Quantity (abs(Amount)/abs(Quantity)): 0 rows, 0 trade dates, - .. -
Positions rows: 0 (Quantity only; no price field)
cot store rows keyed by this CUSIP: 0

COVERAGE 651639AX4: held account-days with a counted price on that date 0 of 0; distinct held dates covered 0 of 0
CLASS 651639AX4 = none

Unread, named: a custodian file the cot code does not name (BLIND per the order's preflight).

BOND-CUSTODIAN-PRICE bonds=3 custodian_reported=0 trade_only=1 none=2
