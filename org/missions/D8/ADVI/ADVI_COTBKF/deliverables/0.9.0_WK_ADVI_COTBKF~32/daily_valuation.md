# Daily valuation per account (CB-p-1)

Each holding of step 1 is valued at that day's close (quantity x price); no price is carried from another day. An account-day is complete only when every holding on it has a price, and only a complete day has a value; all others are blank. A day holding nothing is complete with value 0.0. Cash (FDIC*, CFNCASH) is priced at 1.0. Where two stores price the same security-day the earlier store wins; a security-day whose rows disagree inside its winning store is unpriced.

- accounts: 1533
- account_days: 1691729
- complete: 132132 (7.81%)
- blank: 1559597
- holding_days (non-zero account, day, cusip): 22547096
- priced holding_days: 6560170 (29.10%)
- sources that priced at least one holding: cottonwood-silver-canonical-prices, cottonwood-gold-canonical-holdings, etfs-bbg-testpull-ticker-history, cash-at-par
- price rows disagreeing inside a store's own security-day (security-days left unpriced), by store: cottonwood-gold-canonical-holdings=2204, cottonwood-silver-canonical-prices=3753, etfs-bbg-fund-daily=0, etfs-bbg-testpull-ticker-history=0, portal-canon-return-daily-values=0, rivalfunds-etfs-gold-security-market=0

## Coverage by year

| year | account_days | complete | complete % | holding_days | priced | priced % |
|---|---|---|---|---|---|---|
| 2013 | 44557 | 6476 | 14.53 | 642282 | 41657 | 6.49 |
| 2014 | 80070 | 9515 | 11.88 | 1190842 | 74721 | 6.27 |
| 2015 | 89566 | 6938 | 7.75 | 1286893 | 83745 | 6.51 |
| 2016 | 93656 | 7016 | 7.49 | 1187413 | 160770 | 13.54 |
| 2017 | 101591 | 7228 | 7.11 | 1220581 | 181550 | 14.87 |
| 2018 | 112253 | 6358 | 5.66 | 1357973 | 201354 | 14.83 |
| 2019 | 120183 | 5270 | 4.38 | 1510208 | 215934 | 14.30 |
| 2020 | 134756 | 5893 | 4.37 | 1657348 | 364847 | 22.01 |
| 2021 | 149792 | 8217 | 5.49 | 1868901 | 677251 | 36.24 |
| 2022 | 159910 | 11183 | 6.99 | 2055291 | 853814 | 41.54 |
| 2023 | 168755 | 13845 | 8.20 | 2295917 | 962373 | 41.92 |
| 2024 | 175301 | 15625 | 8.91 | 2633460 | 1182273 | 44.89 |
| 2025 | 180949 | 16017 | 8.85 | 2585848 | 1095545 | 42.37 |
| 2026 | 80390 | 12551 | 15.61 | 1054139 | 464336 | 44.05 |

## Top unpriced securities by holding-days

4372 securities have at least one unpriced holding-day; the top 25:

| cusip | unpriced holding_days |
|---|---|
| 552985863 | 622724 |
| 4812C0381 | 568949 |
| 277907200 | 562245 |
| 149498107 | 394428 |
| 14064D865 | 384280 |
| 92647K309 | 382869 |
| 13161T401 | 375936 |
| 77958B402 | 350813 |
| 693390882 | 305643 |
| 09251M504 | 286153 |
| 316146356 | 283333 |
| 302544101 | 273900 |
| 31635V729 | 266708 |
| 31423A689 | 266019 |
| 31635V679 | 264296 |
| 316146315 | 238425 |
| 30254T643 | 215137 |
| 722005220 | 214939 |
| 74253Q747 | 209975 |
| 277902698 | 207145 |
| 543916464 | 167402 |
| 4812A1373 | 159021 |
| 746745405 | 158978 |
| 74440B405 | 142389 |
| 131649774 | 140490 |

Blind spot: corporate actions the transactions do not record; a price the stores do not hold is blank, never inferred.
