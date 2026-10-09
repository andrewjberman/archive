# CB-ag-1 price-basis census (round 33)

READ-ONLY. Class rule written in the script (its own commit) before the first run; see the script docstring.

## 1. The store as it stands

- object: `s3://opal-data-cot/silver/prices/canonical_prices.parquet` (97633099 bytes)
- file vintage (S3 LastModified): 2026-06-09 20:42:16+00:00
- rows: 11291021; tickers: 4003; columns: date, ticker, price, source

| label | rows | tickers |
|---|---|---|
| linear_interpolation | 7831140 | 3994 |
| yahoo_finance | 3396067 | 3580 |
| transaction_observed | 50143 | 567 |
| scoped_override | 12042 | 6 |
| bd_txn_price | 1623 | 3 |
| transaction_observed_capped | 6 | 0 |

- tickers carrying `yahoo_finance` rows: 3580 (distinct normalised keys; raw ticker strings 3580); this run classes 3580
- Yahoo window: 2020-06-27 .. 2026-10-10

## 3. Class per ticker (denominator: 3580 tickers carrying `yahoo_finance` rows)

| class | tickers | share | yahoo_finance rows | linear_interpolation rows |
|---|---|---|---|---|
| as_traded | 175 | 4.9% of 3580 | 63576 | 32880 |
| dividend_adjusted | 2079 | 58.1% of 3580 | 2208536 | 1021549 |
| indistinguishable | 872 | 24.4% of 3580 | 681492 | 339631 |
| mixed | 79 | 2.2% of 3580 | 48488 | 23160 |
| no_yahoo | 109 | 3.0% of 3580 | 80196 | 54535 |
| other | 266 | 7.4% of 3580 | 313779 | 144718 |

no_yahoo reasons: possibly delisted; no timezone found=73; no_overlap=30; possibly delisted; no price data found =6

other reasons: matches_neither=239; no_dividend_window_store_off_close=25; overlap_lt_20=2

### mixed tickers (named)

- AAETX: share_close=0.31 share_adj=0.31 of 354 days (store/Close 0.8983..1.0000)
- AMCFX: share_close=0.27 share_adj=0.00 of 441 days (store/Close 0.7458..1.0000)
- AMIGX: share_close=0.43 share_adj=0.43 of 849 days (store/Close 0.9100..1.0000)
- AMPCX: share_close=0.29 share_adj=0.00 of 412 days (store/Close 0.6877..1.0000)
- AZBAX: share_close=0.52 share_adj=0.52 of 210 days (store/Close 0.9101..1.0182)
- BIOIX: share_close=0.30 share_adj=0.30 of 393 days (store/Close 0.8460..1.0000)
- BREIX: share_close=0.30 share_adj=0.30 of 393 days (store/Close 0.9298..1.0000)
- BSIIX: share_close=0.05 share_adj=0.21 of 1415 days (store/Close 0.7690..1.0010)
- CAFAX: share_close=0.24 share_adj=0.00 of 502 days (store/Close 0.7107..1.0000)
- CEYRX: share_close=0.25 share_adj=0.25 of 477 days (store/Close 0.5965..1.0000)
- CFNAX: share_close=0.23 share_adj=0.00 of 502 days (store/Close 0.7188..1.0000)
- CGNAX: share_close=0.42 share_adj=0.00 of 261 days (store/Close 0.9082..1.0000)
- CLBAX: share_close=0.24 share_adj=0.00 of 502 days (store/Close 0.7668..1.0000)
- CLREX: share_close=0.50 share_adj=0.00 of 244 days (store/Close 0.8955..1.0000)
- CMLAX: share_close=0.23 share_adj=0.00 of 502 days (store/Close 0.7866..1.0000)
- CNGAX: share_close=0.23 share_adj=0.23 of 502 days (store/Close 0.6736..1.0000)
- COSSX: share_close=0.10 share_adj=0.74 of 1176 days (store/Close 0.7471..1.0000)
- CWIAX: share_close=0.20 share_adj=0.00 of 576 days (store/Close 0.7147..1.0000)
- CWMAX: share_close=0.23 share_adj=0.26 of 502 days (store/Close 0.6806..1.0000)
- DAINX: share_close=0.23 share_adj=0.23 of 479 days (store/Close 0.6566..1.0000)
- DBL: share_close=0.30 share_adj=0.00 of 184 days (store/Close 0.9507..1.0000)
- DFEOX: share_close=0.09 share_adj=0.62 of 1404 days (store/Close 0.8408..1.0000)
- DFFVX: share_close=0.14 share_adj=0.26 of 833 days (store/Close 0.9323..1.0000)
- DFQTX: share_close=0.09 share_adj=0.62 of 1404 days (store/Close 0.8105..1.0000)
- DFUSX: share_close=0.11 share_adj=0.22 of 1146 days (store/Close 0.7274..1.0000)
- DFVEX: share_close=0.09 share_adj=0.46 of 1341 days (store/Close 0.7304..1.0000)
- DURPX: share_close=0.14 share_adj=0.70 of 1239 days (store/Close 0.8661..1.0000)
- EMSQX: share_close=0.21 share_adj=0.26 of 503 days (store/Close 0.6771..1.0000)
- ETIEX: share_close=0.77 share_adj=0.77 of 1452 days (store/Close 0.9726..1.0000)
- ETIHX: share_close=0.75 share_adj=0.75 of 1490 days (store/Close 0.7601..1.0000)
- FAGOX: share_close=0.22 share_adj=0.22 of 505 days (store/Close 0.9202..1.0000)
- FBCGX: share_close=0.28 share_adj=0.00 of 643 days (store/Close 0.9726..1.0000)
- FCDIX: share_close=0.20 share_adj=0.63 of 581 days (store/Close 0.9467..1.0000)
- FCVSX: share_close=0.35 share_adj=0.14 of 318 days (store/Close 0.8240..1.0000)
- FEDDX: share_close=0.78 share_adj=0.78 of 153 days (store/Close 0.9391..1.0000)
- FEGRX: share_close=0.34 share_adj=0.34 of 369 days (store/Close 0.8562..1.0061)
- FFFHX: share_close=0.07 share_adj=0.35 of 1468 days (store/Close 0.5587..1.0000)
- FISEX: share_close=0.55 share_adj=0.00 of 203 days (store/Close 0.8386..1.0065)
- FLIAX: share_close=0.62 share_adj=0.62 of 182 days (store/Close 0.8472..1.0000)
- FSMDX: share_close=0.09 share_adj=0.30 of 1215 days (store/Close 0.8708..1.0000)
- FSPCX: share_close=0.11 share_adj=0.28 of 1021 days (store/Close 0.6727..1.0000)
- FSSL: share_close=0.37 share_adj=0.00 of 139 days (store/Close 0.9692..1.0000)
- GOLDX: share_close=0.23 share_adj=0.23 of 460 days (store/Close 0.7895..1.0880)
- GSMCX: share_close=0.27 share_adj=0.28 of 366 days (store/Close 0.7584..1.0200)
- HGICX: share_close=0.36 share_adj=0.36 of 334 days (store/Close 0.7696..1.0000)
- HSRUX: share_close=0.32 share_adj=0.32 of 348 days (store/Close 0.8486..1.0000)
- HWSIX: share_close=0.15 share_adj=0.44 of 849 days (store/Close 0.8272..1.0000)
- JDEAX: share_close=0.75 share_adj=0.75 of 159 days (store/Close 0.9076..1.0034)
- JGVRX: share_close=0.68 share_adj=0.68 of 177 days (store/Close 0.8010..1.0000)
- JHQTX: share_close=0.20 share_adj=0.74 of 1174 days (store/Close 0.9451..1.0005)
- JIGTX: share_close=0.30 share_adj=0.72 of 1203 days (store/Close 0.5379..1.0000)
- JLPSX: share_close=0.34 share_adj=0.34 of 351 days (store/Close 0.9442..1.0033)
- JSMAX: share_close=0.35 share_adj=0.39 of 306 days (store/Close 0.9211..1.0049)
- KBWY: share_close=0.57 share_adj=0.00 of 92 days (store/Close 0.9843..1.0000)
- LBDFX: share_close=0.62 share_adj=0.00 of 74 days (store/Close 0.9895..1.0000)
- LGVAX: share_close=0.37 share_adj=0.37 of 321 days (store/Close 0.8192..1.0000)
- MIDLX: share_close=0.24 share_adj=0.24 of 502 days (store/Close 0.8431..1.0000)
- MIOIX: share_close=0.58 share_adj=0.58 of 1490 days (store/Close 0.7909..1.0636)
- MPAIX: share_close=0.25 share_adj=0.59 of 1489 days (store/Close 0.3225..1.0000)
- MRGAX: share_close=0.27 share_adj=0.27 of 438 days (store/Close 0.6554..1.0000)
- NEXOF: share_close=0.58 share_adj=0.00 of 404 days (store/Close 0.9886..1.0000)
- ODMAX: share_close=0.22 share_adj=0.22 of 549 days (store/Close 0.4103..1.0000)
- PGTAX: share_close=0.79 share_adj=0.79 of 141 days (store/Close 0.7914..1.0000)
- PHYL: share_close=0.69 share_adj=0.00 of 67 days (store/Close 0.9937..1.0000)
- PMJPX: share_close=0.27 share_adj=0.30 of 393 days (store/Close 0.8817..1.0000)
- PNNT: share_close=0.62 share_adj=0.00 of 92 days (store/Close 0.9676..1.0000)
- QDVO: share_close=0.36 share_adj=0.00 of 132 days (store/Close 0.9566..1.0000)
- RYOCX: share_close=0.22 share_adj=0.22 of 500 days (store/Close 0.7978..1.0500)
- SGHC: share_close=0.50 share_adj=0.00 of 484 days (store/Close 0.9328..1.0000)
- SHAPX: share_close=0.26 share_adj=0.26 of 458 days (store/Close 0.6386..1.0000)
- SHSSX: share_close=0.20 share_adj=0.00 of 606 days (store/Close 0.6935..1.0000)
- TEGIX: share_close=0.22 share_adj=0.22 of 547 days (store/Close 0.7756..1.0000)
- TRRJX: share_close=0.48 share_adj=0.48 of 236 days (store/Close 0.9293..1.0000)
- USRAX: share_close=0.27 share_adj=0.27 of 421 days (store/Close 0.7381..1.0000)
- VTHRX: share_close=0.26 share_adj=0.26 of 426 days (store/Close 0.9069..1.0032)
- VTRIX: share_close=0.44 share_adj=0.44 of 263 days (store/Close 0.7157..1.0061)
- VTTHX: share_close=0.08 share_adj=0.25 of 1422 days (store/Close 0.5903..1.0031)
- VTWNX: share_close=0.22 share_adj=0.22 of 507 days (store/Close 0.7548..1.0025)
- YAFIX: share_close=0.32 share_adj=0.32 of 369 days (store/Close 0.6103..1.0000)

### implied vintage of dividend_adjusted tickers (latest carried dividend step, by month; 2079 tickers)

- 2021-12: 2
- 2022-08: 1
- 2023-09: 2
- 2023-11: 1
- 2024-03: 2
- 2024-04: 1
- 2024-05: 2
- 2024-06: 3
- 2024-08: 3
- 2024-09: 2
- 2024-11: 2
- 2024-12: 14
- 2025-01: 3
- 2025-02: 6
- 2025-03: 22
- 2025-04: 22
- 2025-05: 48
- 2025-06: 19
- 2025-07: 18
- 2025-08: 23
- 2025-09: 9
- 2025-10: 9
- 2025-11: 12
- 2025-12: 230
- 2026-01: 103
- 2026-02: 363
- 2026-03: 985
- 2026-04: 168
- 2026-05: 3
- none: 1

Per-ticker detail: `price_basis_census.csv`.

## 4. What rests on adjusted prices

- store rows (yahoo_finance + linear_interpolation) of dividend_adjusted and mixed tickers: 3301733 of 11227207 (29.4%); tickers 2158 of 3580 with yahoo_finance rows
  - yahoo_finance: 2257024 of 3396067
  - linear_interpolation: 1044709 of 7831140
- served account_day_value: `s3://opal-data-assets/commonwealth/cottonwood/silver/account_day_value/date=2026-06-23/part-00000.parquet` (LastModified 2026-10-09 08:09:27+00:00); 21102041 rows; price_source values {'nan': 15987184, 'cottonwood-silver-canonical-prices': 3744124, 'cash-at-par': 1363846, 'etfs-bbg-testpull-ticker-history': 4229, 'cottonwood-gold-canonical-holdings': 2658}
- cusip -> store ticker as the chain resolves it: 1263 of 4634 universe securities; 867 CUSIPs map to an adjusted ticker
- account-days (distinct account, date) with at least one holding priced from a dividend_adjusted or mixed ticker (price_source = the store, close not null): **638948 of 1669040** (38.3%)
- accounts touched: 688 of 1528; months touched: 73 of 159; account-months touched: 31249 of 81718
- months touched: 2020-06, 2020-07, 2020-08, 2020-09, 2020-10, 2020-11, 2020-12, 2021-01, 2021-02, 2021-03, 2021-04, 2021-05, 2021-06, 2021-07, 2021-08, 2021-09, 2021-10, 2021-11, 2021-12, 2022-01, 2022-02, 2022-03, 2022-04, 2022-05, 2022-06, 2022-07, 2022-08, 2022-09, 2022-10, 2022-11, 2022-12, 2023-01, 2023-02, 2023-03, 2023-04, 2023-05, 2023-06, 2023-07, 2023-08, 2023-09, 2023-10, 2023-11, 2023-12, 2024-01, 2024-02, 2024-03, 2024-04, 2024-05, 2024-06, 2024-07, 2024-08, 2024-09, 2024-10, 2024-11, 2024-12, 2025-01, 2025-02, 2025-03, 2025-04, 2025-05, 2025-06, 2025-07, 2025-08, 2025-09, 2025-10, 2025-11, 2025-12, 2026-01, 2026-02, 2026-03, 2026-04, 2026-05, 2026-06

## 5. Provenance of the other source labels (row ADVI_COTBKF-D2-S48)

### label `transaction_observed`: 50143 rows across 567 tickers

| ticker | rows | first date | last date | min price | max price |
|---|---|---|---|---|---|
|  CTRM | 2 | 2022-04-05 | 2022-05-19 | 1.7700 | 1.8900 |
| 88E | 5 | 2022-05-03 | 2024-02-15 | 0.0033 | 0.0099 |
| AAFXX | 16 | 2025-02-13 | 2026-06-01 | 1.0000 | 1.0000 |
| AAPL | 1 | 2026-04-14 | 2026-04-14 | 258.4817 | 258.4817 |
| AAU | 2 | 2024-02-16 | 2025-01-10 | 0.0502 | 0.1351 |
| AAWW | 127 | 2021-01-26 | 2022-10-31 | 55.6711 | 101.1400 |
| ABB | 28 | 2021-12-03 | 2026-05-19 | 27.8930 | 106.8775 |
| ABML | 2 | 2022-07-27 | 2023-07-20 | 0.6133 | 0.6880 |
| ACCD | 2 | 2021-12-06 | 2021-12-07 | 25.2600 | 26.6952 |
| ACSG | 359 | 2023-04-21 | 2025-09-08 | 62.6252 | 112.4818 |
| ADAP | 2 | 2023-06-02 | 2025-06-10 | 0.2715 | 1.0800 |
| AGG | 1 | 2026-04-14 | 2026-04-14 | 99.8305 | 99.8305 |
| AGII | 112 | 2021-01-26 | 2023-04-14 | 22.1078 | 61.2700 |
| AGR | 4 | 2024-05-16 | 2024-10-23 | 35.7896 | 37.5300 |
| AHONY | 4 | 2025-04-24 | 2025-07-23 | 40.6388 | 41.2350 |
| AIG.PRA | 2 | 2021-11-08 | 2021-11-24 | 26.9006 | 27.2850 |
| AJG | 1 | 2026-04-14 | 2026-04-14 | 222.4400 | 222.4400 |
| AL | 1 | 2026-04-10 | 2026-04-10 | 65.0000 | 65.0000 |
| ALA | 3 | 2023-08-18 | 2026-01-09 | 19.3625 | 29.3479 |
| ALE | 5 | 2023-10-02 | 2025-04-14 | 50.9389 | 64.8183 |
| ALPN | 1 | 2022-04-22 | 2022-04-22 | 8.5200 | 8.5200 |
| ALSDF | 3 | 2024-02-16 | 2025-01-13 | 12.7300 | 19.1195 |
| ALXN | 1 | 2020-10-20 | 2020-10-20 | 124.2485 | 124.2485 |
| AMD | 1 | 2026-04-14 | 2026-04-14 | 254.4596 | 254.4596 |
| AMED | 5 | 2024-02-16 | 2025-07-21 | 91.1907 | 97.8200 |
| AMNT | 1 | 2026-06-05 | 2026-06-05 | 22.8744 | 22.8744 |
| AMRS | 4 | 2021-02-08 | 2022-05-05 | 3.5451 | 21.8864 |
| AMZN | 1 | 2026-04-14 | 2026-04-14 | 239.8900 | 239.8900 |
| ANAT | 168 | 2021-01-26 | 2023-10-24 | 27.4400 | 53.7344 |
| ANSS | 8 | 2020-10-20 | 2025-07-18 | 1.0000 | 333.8950 |
| APDN | 2 | 2022-05-31 | 2022-06-03 | 1.2218 | 1.2900 |
| APH | 1 | 2026-04-14 | 2026-04-14 | 147.9264 | 147.9264 |
| APHA | 2 | 2021-05-05 | 2021-05-07 | 13.4350 | 13.4351 |
| APTX | 2 | 2023-02-06 | 2023-02-07 | 0.6000 | 0.6459 |
| AQUA | 4 | 2022-07-20 | 2024-08-16 | 7.1100 | 11.7200 |
| ARBKF | 3 | 2023-09-07 | 2025-01-10 | 0.0588 | 1.3800 |
| ARC | 2 | 2023-08-18 | 2026-01-09 | 15.1786 | 16.6859 |
| ARCH | 4 | 2023-06-23 | 2024-01-02 | 111.4800 | 167.5271 |
| ARNC | 3 | 2020-07-20 | 2023-04-13 | 16.2500 | 25.6500 |
| ARVL | 3 | 2022-11-04 | 2023-03-24 | 0.1476 | 0.6534 |
(527 more tickers not listed)

Repo search `git grep -n -F transaction_observed -- '*.py' '*.json'` (rc=0), 63 hit(s), file:line:

- `data/black_diamond/scripts/gold/E_00.decompose_aua_gap.py:13:  3. By price tier: T1 (transaction_observed), T2 (yahoo_finance),`
- `data/black_diamond/scripts/gold/E_05.gap_by_pricing_source.py:190:        ('transaction_observed', 'T1 (TRANSACTION_OBSERVED)'),`
- `data/black_diamond/scripts/gold/E_06.trace_asset_pricing.py:85:    # for each asset, find the max date where source is yahoo_finance or transaction_observed`
- `data/black_diamond/scripts/gold/E_06.trace_asset_pricing.py:88:        canon_full['source'].isin(['yahoo_finance', 'transaction_observed']) &`
- `data/black_diamond/scripts/gold/E_06.trace_asset_pricing.py:190:    for src in ['yahoo_finance', 'transaction_observed', 'linear_interpolation',`
- `data/black_diamond/scripts/gold/E_14.audit_existing_mappings.py:80:        (canon['source'] == 'transaction_observed') &`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:17:                            T1: transaction_observed`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:255:    # Rows still rewritten are flagged with source='transaction_observed_capped'`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:403:      T1 (transaction_observed) is primary -- only price source available.`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:427:        source[t1_fill] = 'transaction_observed'`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:428:        source[t1_fill & t1_capped] = 'transaction_observed_capped'`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:433:        source[price.notna()] = 'transaction_observed'`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:434:        source[price.notna() & t1_capped] = 'transaction_observed_capped'`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:437:    t1_mask = source.isin(['transaction_observed', 'transaction_observed_capped'])`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:486:    The 4-tier canonical pipeline (transaction_observed / yahoo_finance /`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:551:    print(f"  T1 (transaction_observed): {t1_count:,} / {len(spine):,} "`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:620:    t1_rows = canonical[canonical['source'] == 't1_transaction_observed']`
- `data/black_diamond/scripts/gold/lib/nna_flows.py:48:    'transaction_observed', 'yahoo_finance', 'linear_interpolation',`
- `data/black_diamond/scripts/silver/bd_price_update.py:68:    'transaction_observed':  0,`
- `data/black_diamond/scripts/silver/bd_price_update.py:425:    Scoped overrides (deliberate corrections) -> Yahoo (tickered) -> T1 (transaction_observed) -> T3 (carry_forward).`
- `data/black_diamond/scripts/silver/bd_price_update.py:464:            price, source = t1_prices[asset_name], 'transaction_observed'`
- `data/black_diamond/scripts/silver/bd_price_update.py:483:            f"T1={(df['source']=='transaction_observed').sum()}, "`
- `data/black_diamond/scripts/silver/bd_price_update.py:555:                price_series[d],  source_series[d] = t1,  'transaction_observed'`
- `data/cot/scripts/gold/E_00.decompose_aua_gap.py:13:  3. By price tier: T1 (transaction_observed), T2 (yahoo_finance),`
- `data/cot/scripts/gold/build_canonical_prices_v2.py:17:                            T1: transaction_observed`
- (38 more hits not listed)

### label `scoped_override`: 12042 rows across 6 tickers

| ticker | rows | first date | last date | min price | max price |
|---|---|---|---|---|---|
| BAC_MBS_0602 | 5332 | 2006-01-02 | 2026-06-09 | 201.5700 | 201.5700 |
| DEST_INTL_I | 179 | 2025-10-02 | 2026-06-09 | 13.3000 | 13.3000 |
| DEST_LCAP_I | 179 | 2025-10-02 | 2026-06-09 | 13.3000 | 13.3000 |
| JPM_STRUCT_0029 | 565 | 2024-04-10 | 2026-06-09 | 2.5500 | 2.5500 |
| WALDROP_DAF | 715 | 2023-09-13 | 2026-06-09 | 1.9500 | 1.9500 |
| WF_MBS_0715 | 5072 | 2007-01-01 | 2026-06-09 | 7.1200 | 7.1200 |

Repo search `git grep -n -F scoped_override -- '*.py' '*.json'` (rc=0), 128 hit(s), file:line:

- `data/black_diamond/scripts/gold/B_01.holdings_lots.py:2305:      T1     price_quality in {rps_injection, scoped_override}                -- external unit authority, protected`
- `data/black_diamond/scripts/gold/B_01.holdings_lots.py:2331:    HIGH_CONF = {'rps_injection', 'scoped_override',`
- `data/black_diamond/scripts/gold/B_01.holdings_lots.py:2933:    # Protected: rps_injection, scoped_override, synthetic_injection, T3 with`
- `data/black_diamond/scripts/gold/aua_overrides.json:2:  "_description": "AUA valuation overrides for 05_build_client_performance.py. RC6 ghost account exclusions only. RC1/RC2 mispriced assets are fixe`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:22:  6b. Auto-chain       -> inject_scoped_overrides.py --upload  (enforced in code)`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:68:    Path(__file__).resolve().parent.parent / 'silver' / 'inject_scoped_overrides.py'`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:482:def _run_inject_scoped_overrides():`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:494:        print(f"\nERROR: inject_scoped_overrides.py not found at {INJECT_OVERRIDES_SCRIPT}")`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:496:        print("ERROR: run inject_scoped_overrides.py --upload manually to repair, "`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:511:        print(f"\nFATAL: inject_scoped_overrides.py (PROD) exited {e.returncode}")`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:670:        _run_inject_scoped_overrides()`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:689:        help='Skip auto-chained inject_scoped_overrides.py post-step. '`
- `data/black_diamond/scripts/silver/bd_price_update.py:62:# scoped_override is highest â€” deliberate corrections for assets whose ticker`
- `data/black_diamond/scripts/silver/bd_price_update.py:66:    'scoped_override':      -2,`
- `data/black_diamond/scripts/silver/bd_price_update.py:80:# This is the SINGLE SOURCE OF TRUTH.  inject_scoped_overrides.py reads`
- `data/black_diamond/scripts/silver/bd_price_update.py:449:                         'source': 'scoped_override'})`
- `data/black_diamond/scripts/silver/bd_price_update.py:482:            f"(override={(df['source']=='scoped_override').sum()}, "`
- `data/black_diamond/scripts/silver/inject_scoped_overrides.py:14:Source tag: 'scoped_override' -- distinguishable from all other sources in`
- `data/black_diamond/scripts/silver/inject_scoped_overrides.py:30:  2. Removes any existing 'scoped_override' rows (idempotent)`
- `data/black_diamond/scripts/silver/inject_scoped_overrides.py:35:    python inject_scoped_overrides.py --dry-run     # show what would change`
- `data/black_diamond/scripts/silver/inject_scoped_overrides.py:36:    python inject_scoped_overrides.py --upload       # inject and upload`
- `data/black_diamond/scripts/silver/inject_scoped_overrides.py:56:SOURCE_TAG = "scoped_override"`
- `data/black_diamond/scripts/silver/inject_scoped_overrides.py:61:# treats identically to scoped_override for the remove-and-replace cycle.`
- `data/black_diamond/scripts/silver/inject_scoped_overrides.py:213:    Remove existing scoped_override rows, then remove any rows for overridden`
- `data/black_diamond/scripts/silver/scoped_price_exceptions.json:2:  "_description": "CUSIP-keyed scoped-exceptions blocklist. Hard-overrides canonical_prices for listed CUSIPs so Yahoo can NEVER re-pri`
- (103 more hits not listed)

### label `bd_txn_price`: 1623 rows across 3 tickers

| ticker | rows | first date | last date | min price | max price |
|---|---|---|---|---|---|
| CUSIP_05613L3H2 | 431 | 2024-10-15 | 2026-06-09 | 1.0188 | 1.0188 |
| CUSIP_651639AX4 | 572 | 2024-04-01 | 2026-06-09 | 0.9037 | 0.9037 |
| CUSIP_95000U2D4 | 620 | 2024-01-24 | 2026-06-09 | 0.9804 | 0.9804 |

Repo search `git grep -n -F bd_txn_price -- '*.py' '*.json'` (rc=0), 8 hit(s), file:line:

- `data/black_diamond/scripts/gold/B_01.holdings_lots.py:2307:      A      T3 (linear_interp / bd_txn_price / other) with cusip IN`
- `data/black_diamond/scripts/silver/inject_scoped_overrides.py:60:# Emits source=<force_source> rows (e.g. 'bd_txn_price'), which this script`
- `data/black_diamond/scripts/silver/inject_scoped_overrides.py:124:    entry's force_source (e.g. 'bd_txn_price'), NOT the generic SOURCE_TAG;`
- `data/black_diamond/scripts/silver/inject_scoped_overrides.py:136:        src = exc.get("force_source", "bd_txn_price")`
- `data/black_diamond/scripts/silver/scoped_price_exceptions.json:10:      "force_source": "bd_txn_price",`
- `data/black_diamond/scripts/silver/scoped_price_exceptions.json:18:      "force_source": "bd_txn_price",`
- `data/black_diamond/scripts/silver/scoped_price_exceptions.json:26:      "force_source": "bd_txn_price",`
- `data/cot/scripts/gold/B_01.holdings_lots.py:2263:      A      T3 (linear_interp / bd_txn_price / other) with cusip IN`

### label `transaction_observed_capped`: 6 rows across 0 tickers

| ticker | rows | first date | last date | min price | max price |
|---|---|---|---|---|---|

Repo search `git grep -n -F transaction_observed_capped -- '*.py' '*.json'` (rc=0), 15 hit(s), file:line:

- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:255:    # Rows still rewritten are flagged with source='transaction_observed_capped'`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:428:        source[t1_fill & t1_capped] = 'transaction_observed_capped'`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:434:        source[price.notna() & t1_capped] = 'transaction_observed_capped'`
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py:437:    t1_mask = source.isin(['transaction_observed', 'transaction_observed_capped'])`
- `data/cot/scripts/gold/build_canonical_prices_v2.py:247:    # Rows still rewritten are flagged with source='transaction_observed_capped'`
- `data/cot/scripts/gold/build_canonical_prices_v2.py:420:        source[t1_fill & t1_capped] = 'transaction_observed_capped'`
- `data/cot/scripts/gold/build_canonical_prices_v2.py:426:        source[price.notna() & t1_capped] = 'transaction_observed_capped'`
- `data/cot/scripts/gold/build_canonical_prices_v2.py:429:    t1_mask = source.isin(['transaction_observed', 'transaction_observed_capped'])`
- `data/inf/scripts/gold/INF_build_canonical_prices.py:278:        source[t1_fill & t1_capped] = 'transaction_observed_capped'`
- `data/inf/scripts/gold/INF_build_canonical_prices.py:283:        source[price.notna() & t1_capped] = 'transaction_observed_capped'`
- `data/inf/scripts/gold/INF_build_canonical_prices.py:286:    t1_mask = source.isin(['transaction_observed', 'transaction_observed_capped'])`
- `data/inf/scripts/gold/INF_build_canonical_prices.py:465:                                              'transaction_observed_capped', 'price_override'])`
- `org/modules/graph/comp_honesty.py:386:                            "producer_labels": ["transaction_observed", "transaction_observed_capped"]}})`
- `org/modules/graph/comp_honesty.py:394:                            "producer_labels": ["transaction_observed", "transaction_observed_capped"]},`
- `org/projects/ADVI_GLDRST.json:44:  "phase": "REOPENED 2026-04-10 for v2 canonical_prices follow-up. Original restructure (19/22 TOs) remains complete. .021 SHIPPED (source-tag transaction_observed_cap`


PRICE-BASIS tickers=3580 as_traded=175 dividend_adjusted=2079 indistinguishable=872 mixed=79 no_yahoo=109 other=266 yahoo_calls=72 adv_days_on_adjusted=638948/1669040
