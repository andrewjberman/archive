# SEGMENT PERIOD LABEL READ -- AMGT_RESAPP round 78 (CTO msg 31077)

1. Of 76 names with stored revenue segment rows: matched 72, unmatched 4, no-block 0 (sum 76).
2. Re-pull: Period 1 is not labelled by its own sum for 4 names (unmatched 4 + no-block 0). In 4 of those 4 a LATER period matches a stored year at the offset that puts Period 1 on the newest stored fiscal year, so their Period 1 is incomplete or empty rather than a different year; 0 have no such evidence. Of the 72 matched, 72 matched the NEWEST stored fiscal year and 0 an earlier one (matched years: FY2025 x62, FY2026 x10).
3. Period 2 test on the 72 matched names (Period 2 level-1 sum vs the stored fiscal year one before the matched one): holds 71, does not hold 1, cannot tell 0.

Measured 2026-10-07T15:13:52Z by `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_read_segment_period_label.py`. Control AMD_US_Equity: matched on fiscal year 2025, P1 level-1 sum 34639.000 -- OK.

## What was read

- Segment table: `s3://opal-data-harvest/bloomberg/harvest/bronze/segments/security_key=<partition>/<stamp>.json`, 85 partitions listed, 76 with a non-empty `response.PG_REVENUE`, 9 without. Per name the NEWEST object carrying revenue rows.
- Model block: the page's reader `lib.research.api.scoped_amgt._read_model_block_pool` -- the newest `s3://opal-data-harvest/derived/model_block/<security_key>/<stamp>/model_block.json`; rows `figures[]` with `scope == fiscal_year_line_item` and `mnemonic == SALES_REV_TURN`; fields `fiscal_year` (a calendar-year string) and `value`.
- Scale: `unit` values seen on those rows: `MILLIONS` x76. Currency: a revenue row carries no currency field of its own (only `currency_caveat`, non-null on 21 names); the block's header carries `EQY_FUND_CRNCY` (the fundamentals currency, column `fund ccy`, present on 76 of 76 names) and `CRNCY` (the trading currency, column `trade ccy`). The two differ on 23 names. Fund-currency counts: BRL x3, CAD x1, CHF x2, CNY x1, EUR x14, GBP x7, INR x1, JPY x3, MXN x2, PHP x1, SGD x1, TWD x2, USD x38.
- Match rule: |P1 level-1 sum / stored year - 1| <= 0.005. A cell with |value| < 1e-06 is absent.

## Per name (76)

| security_key | class | L1 rows | P1 absent | P1 level-1 sum | matched FY | newest FY | nearest FY | nearest value | ratio | fund ccy / trade ccy | P2 test | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1299_HK_Equity | matched | 1 | 0 | 42379.000 | 2025 | 2025 | 2025 | 42379.000 | 1.00000 | USD / HKD | HOLDS | - |
| 2317_TT_Equity | matched | 5 | 0 | 8103105.000 | 2025 | 2025 | 2025 | 8103104.763 | 1.00000 | TWD / TWD | HOLDS | - |
| 8035_JP_Equity | matched | 3 | 2 | 2443533.000 | 2026 | 2026 | 2026 | 2443533.000 | 1.00000 | JPY / JPY | HOLDS | - |
| 8766_JP_Equity | unmatched | 6 | 0 | 8336718.000 | - | 2026 | 2026 | 7668839.000 | 1.08709 | JPY / JPY | - | 6 of 6 level-1 rows carry a Period 1 value; later periods matching a stored year: P2=FY2025, P3=FY2024, P4=FY2023, P5=FY2022 (consistent with Period 1 = the newest stored year FY2026) |
| 9433_JP_Equity | matched | 3 | 0 | 6071915.000 | 2026 | 2026 | 2026 | 6071915.000 | 1.00000 | JPY / JPY | HOLDS | - |
| 992_HK_Equity | matched | 4 | 0 | 83074.555 | 2026 | 2026 | 2026 | 83074.555 | 1.00000 | USD / HKD | HOLDS | - |
| ADBE_US_Equity | matched | 3 | 0 | 23769.000 | 2025 | 2025 | 2025 | 23769.000 | 1.00000 | USD / USD | HOLDS | - |
| AI_FP_Equity | matched | 4 | 2 | 26940.200 | 2025 | 2025 | 2025 | 26940.000 | 1.00001 | EUR / EUR | HOLDS | - |
| AMD_US_Equity | matched | 4 | 1 | 34639.000 | 2025 | 2025 | 2025 | 34639.000 | 1.00000 | USD / USD | DOES_NOT_HOLD | P2 16136.000 vs FY2024 25785.000, ratio 0.62579, 2 of 4 level-1 rows carry a Period 2 value |
| AMXB_MM_Equity | unmatched | 4 | 4 | - | - | 2025 | - | - | - | MXN / MXN | - | no level-1 row carries a Period 1 value; later periods matching a stored year: P2=FY2024, P3=FY2023, P4=FY2022, P5=FY2021 (consistent with Period 1 = the newest stored year FY2025) |
| ASML_NA_Equity | matched | 2 | 0 | 32667.300 | 2025 | 2025 | 2025 | 32667.300 | 1.00000 | EUR / EUR | HOLDS | - |
| AZN_LN_Equity | matched | 9 | 1 | 58739.000 | 2025 | 2025 | 2025 | 58739.000 | 1.00000 | USD / GBp | HOLDS | - |
| BATS_LN_Equity | matched | 3 | 0 | 25610.000 | 2025 | 2025 | 2025 | 25610.000 | 1.00000 | GBP / GBp | HOLDS | - |
| BBSE3_BZ_Equity | matched | 4 | 1 | 6197.561 | 2025 | 2025 | 2025 | 6197.561 | 1.00000 | BRL / BRL | HOLDS | - |
| BP/_LN_Equity | matched | 4 | 0 | 189335.000 | 2025 | 2025 | 2025 | 189335.000 | 1.00000 | USD / GBp | HOLDS | - |
| BZLFY_US_Equity | matched | 1 | 0 | 11845.400 | 2025 | 2025 | 2025 | 11845.400 | 1.00000 | GBP / USD | HOLDS | - |
| CDNS_US_Equity | matched | 1 | 0 | 5296.759 | 2025 | 2025 | 2025 | 5296.759 | 1.00000 | USD / USD | HOLDS | - |
| CELH_US_Equity | matched | 1 | 0 | 2515.269 | 2025 | 2025 | 2025 | 2515.269 | 1.00000 | USD / USD | HOLDS | - |
| CLX_US_Equity | matched | 5 | 1 | 6720.000 | 2026 | 2026 | 2026 | 6720.000 | 1.00000 | USD / USD | HOLDS | - |
| CNR_CN_Equity | matched | 2 | 0 | 17304.000 | 2025 | 2025 | 2025 | 17304.000 | 1.00000 | CAD / CAD | HOLDS | - |
| CPA_US_Equity | matched | 1 | 0 | 3617.822 | 2025 | 2025 | 2025 | 3617.822 | 1.00000 | USD / USD | HOLDS | - |
| ENEL_IM_Equity | matched | 9 | 3 | 78057.000 | 2025 | 2025 | 2025 | 78057.000 | 1.00000 | EUR / EUR | HOLDS | - |
| GOOGL_US_Equity | matched | 4 | 0 | 402836.000 | 2025 | 2025 | 2025 | 402836.000 | 1.00000 | USD / USD | HOLDS | - |
| GPN_US_Equity | matched | 8 | 4 | 7705.000 | 2025 | 2025 | 2025 | 7705.878 | 0.99989 | USD / USD | HOLDS | - |
| GSK_LN_Equity | matched | 1 | 0 | 32667.000 | 2025 | 2025 | 2025 | 32667.000 | 1.00000 | GBP / GBp | HOLDS | - |
| HEI_US_Equity | matched | 3 | 0 | 4485.044 | 2025 | 2025 | 2025 | 4485.044 | 1.00000 | USD / USD | HOLDS | - |
| IBE_SM_Equity | matched | 5 | 0 | 44076.000 | 2025 | 2025 | 2025 | 44076.000 | 1.00000 | EUR / EUR | HOLDS | - |
| ICICIBC_IN_Equity | matched | 9 | 1 | 3121183.593 | 2026 | 2026 | 2026 | 3121183.593 | 1.00000 | INR / INR | HOLDS | - |
| ICT_PM_Equity | matched | 1 | 0 | 3234.704 | 2025 | 2025 | 2025 | 3234.704 | 1.00000 | USD / PHP | HOLDS | - |
| IDXX_US_Equity | matched | 4 | 0 | 4303.702 | 2025 | 2025 | 2025 | 4303.702 | 1.00000 | USD / USD | HOLDS | - |
| IMB_LN_Equity | matched | 4 | 2 | 32171.000 | 2025 | 2025 | 2025 | 32171.000 | 1.00000 | GBP / GBp | HOLDS | - |
| ISRG_US_Equity | matched | 2 | 0 | 10064.700 | 2025 | 2025 | 2025 | 10064.700 | 1.00000 | USD / USD | HOLDS | - |
| JD_US_Equity | matched | 4 | 0 | 1309085.000 | 2025 | 2025 | 2025 | 1309085.000 | 1.00000 | CNY / USD | HOLDS | - |
| KPN_NA_Equity | matched | 6 | 0 | 5796.000 | 2025 | 2025 | 2025 | 5797.000 | 0.99983 | EUR / EUR | HOLDS | - |
| LLY_US_Equity | matched | 5 | 0 | 65179.000 | 2025 | 2025 | 2025 | 65179.000 | 1.00000 | USD / USD | HOLDS | - |
| MA_US_Equity | matched | 2 | 1 | 32791.000 | 2025 | 2025 | 2025 | 32791.000 | 1.00000 | USD / USD | HOLDS | - |
| MELI_US_Equity | matched | 2 | 0 | 28893.000 | 2025 | 2025 | 2025 | 28893.000 | 1.00000 | USD / USD | HOLDS | - |
| MER_PM_Equity | matched | 3 | 1 | 497325.000 | 2025 | 2025 | 2025 | 497325.000 | 1.00000 | PHP / PHP | HOLDS | - |
| ML_FP_Equity | matched | 3 | 0 | 25992.000 | 2025 | 2025 | 2025 | 25992.000 | 1.00000 | EUR / EUR | HOLDS | - |
| MNST_US_Equity | matched | 5 | 1 | 8294.343 | 2025 | 2025 | 2025 | 8294.343 | 1.00000 | USD / USD | HOLDS | - |
| MSCI_US_Equity | matched | 4 | 0 | 3134.459 | 2025 | 2025 | 2025 | 3134.459 | 1.00000 | USD / USD | HOLDS | - |
| NESN_SW_Equity | matched | 12 | 6 | 89885.000 | 2025 | 2025 | 2025 | 89885.000 | 1.00000 | CHF / CHF | HOLDS | - |
| NFLX_US_Equity | matched | 3 | 2 | 45183.036 | 2025 | 2025 | 2025 | 45183.036 | 1.00000 | USD / USD | HOLDS | - |
| NG/_LN_Equity | matched | 7 | 2 | 17687.000 | 2026 | 2026 | 2026 | 17687.000 | 1.00000 | GBP / GBp | HOLDS | - |
| NKE_US_Equity | matched | 3 | 0 | 46398.000 | 2026 | 2026 | 2026 | 46398.000 | 1.00000 | USD / USD | HOLDS | - |
| NOKIA_FH_Equity | matched | 10 | 5 | 19889.000 | 2025 | 2025 | 2025 | 19889.000 | 1.00000 | EUR / EUR | HOLDS | - |
| NOVN_SW_Equity | matched | 4 | 2 | 56674.000 | 2025 | 2025 | 2025 | 56674.000 | 1.00000 | USD / CHF | HOLDS | - |
| NOW_US_Equity | matched | 1 | 0 | 13278.000 | 2025 | 2025 | 2025 | 13278.000 | 1.00000 | USD / USD | HOLDS | - |
| OMAB_MM_Equity | matched | 3 | 0 | 15964.414 | 2025 | 2025 | 2025 | 15964.414 | 1.00000 | MXN / MXN | HOLDS | - |
| ORA_FP_Equity | matched | 2 | 0 | 40397.000 | 2025 | 2025 | 2025 | 40397.000 | 1.00000 | EUR / EUR | HOLDS | - |
| PBR_US_Equity | matched | 4 | 0 | 497549.000 | 2025 | 2025 | 2025 | 497549.000 | 1.00000 | BRL / USD | HOLDS | - |
| PWR_US_Equity | matched | 2 | 0 | 28479.697 | 2025 | 2025 | 2025 | 28479.697 | 1.00000 | USD / USD | HOLDS | - |
| QXO_US_Equity | matched | 2 | 1 | 6842.200 | 2025 | 2025 | 2025 | 6842.200 | 1.00000 | USD / USD | HOLDS | - |
| RIO_LN_Equity | unmatched | 15 | 15 | - | - | 2025 | - | - | - | USD / GBp | - | no level-1 row carries a Period 1 value; later periods matching a stored year: P3=FY2023, P4=FY2022 (consistent with Period 1 = the newest stored year FY2025) |
| RKT_LN_Equity | matched | 4 | 1 | 14205.000 | 2025 | 2025 | 2025 | 14205.000 | 1.00000 | GBP / GBp | HOLDS | - |
| RMS_FP_Equity | matched | 8 | 0 | 16002.000 | 2025 | 2025 | 2025 | 16002.000 | 1.00000 | EUR / EUR | HOLDS | - |
| ROG_SW_Equity | matched | 2 | 0 | 61516.000 | 2025 | 2025 | 2025 | 61516.000 | 1.00000 | CHF / CHF | HOLDS | - |
| RWE_GR_Equity | matched | 3 | 1 | 17628.000 | 2025 | 2025 | 2025 | 17628.000 | 1.00000 | EUR / EUR | HOLDS | - |
| SAN_FP_Equity | unmatched | 6 | 5 | 43626.000 | - | 2025 | 2024 | 44286.000 | 0.98510 | EUR / EUR | - | 1 of 6 level-1 rows carry a Period 1 value; later periods matching a stored year: P2=FY2024, P3=FY2023 (consistent with Period 1 = the newest stored year FY2025) |
| SHOP_CN_Equity | matched | 2 | 0 | 11556.000 | 2025 | 2025 | 2025 | 11556.000 | 1.00000 | USD / CAD | HOLDS | - |
| SLB_US_Equity | matched | 9 | 3 | 35708.000 | 2025 | 2025 | 2025 | 35708.000 | 1.00000 | USD / USD | HOLDS | - |
| SNPS_US_Equity | matched | 3 | 0 | 7054.178 | 2025 | 2025 | 2025 | 7054.178 | 1.00000 | USD / USD | HOLDS | - |
| SPOT_US_Equity | matched | 2 | 0 | 17186.000 | 2025 | 2025 | 2025 | 17186.000 | 1.00000 | EUR / USD | HOLDS | - |
| SSE_LN_Equity | matched | 12 | 5 | 10186.500 | 2026 | 2026 | 2026 | 10186.500 | 1.00000 | GBP / GBp | HOLDS | - |
| ST_SP_Equity | matched | 10 | 5 | 14260.600 | 2026 | 2026 | 2026 | 14260.600 | 1.00000 | SGD / SGD | HOLDS | - |
| TSM_US_Equity | matched | 2 | 0 | 3809054.272 | 2025 | 2025 | 2025 | 3809054.272 | 1.00000 | TWD / USD | HOLDS | - |
| TTE_FP_Equity | matched | 8 | 1 | 182344.000 | 2025 | 2025 | 2025 | 182344.000 | 1.00000 | USD / EUR | HOLDS | - |
| UBER_US_Equity | matched | 4 | 1 | 52017.000 | 2025 | 2025 | 2025 | 52017.000 | 1.00000 | USD / USD | HOLDS | - |
| ULVR_LN_Equity | matched | 5 | 1 | 50503.000 | 2025 | 2025 | 2025 | 50503.000 | 1.00000 | EUR / GBp | HOLDS | - |
| UNH_US_Equity | matched | 4 | 1 | 447567.000 | 2025 | 2025 | 2025 | 447567.000 | 1.00000 | USD / USD | HOLDS | - |
| UNVGY_US_Equity | matched | 4 | 0 | 12507.000 | 2025 | 2025 | 2025 | 12507.000 | 1.00000 | EUR / USD | HOLDS | - |
| VIVT3_BZ_Equity | matched | 4 | 3 | 59595.000 | 2025 | 2025 | 2025 | 59595.000 | 1.00000 | BRL / BRL | HOLDS | - |
| V_US_Equity | matched | 5 | 0 | 40000.000 | 2025 | 2025 | 2025 | 40000.000 | 1.00000 | USD / USD | HOLDS | - |
| WDAY_US_Equity | matched | 2 | 0 | 9552.000 | 2026 | 2026 | 2026 | 9552.000 | 1.00000 | USD / USD | HOLDS | - |
| ZTS_US_Equity | matched | 3 | 0 | 9467.000 | 2025 | 2025 | 2025 | 9467.000 | 1.00000 | USD / USD | HOLDS | - |
| ZURN_SW_Equity | matched | 5 | 0 | 69793.000 | 2025 | 2025 | 2025 | 69793.000 | 1.00000 | USD / CHF | HOLDS | - |

## Names with no revenue rows (9, outside the 76)

- 8306_JP_Equity (1 object(s) read)
- 8316_JP_Equity (1 object(s) read)
- 939_HK_Equity (1 object(s) read)
- BNP_FP_Equity (1 object(s) read)
- HSBA_LN_Equity (1 object(s) read)
- ISP_IM_Equity (1 object(s) read)
- KOFUBL_MM_Equity (1 object(s) read)
- UBSG_SW_Equity (1 object(s) read)
- WALMEX*_MM_Equity (1 object(s) read)

## NOT MEASURED

- The CURRENCY of a segment value. The segment object carries no currency field; a match within 0.5 percent shows the two stored numbers agree, and the model block states its revenue is in millions of the reporting currency with header EQY_FUND_CRNCY naming it, so the segment currency is inferred from the match, not read. That EQY_FUND_CRNCY is the currency of the SALES_REV_TURN rows is the block's own definition, not something this read tested.
- A match by coincidence. The GBp trading names differ from pounds by 100x, which no match could hide, but two adjacent fiscal years within 0.5 percent of each other were not screened for.
- The fiscal-year END DATE. The model block labels a year by a calendar-year string (`fiscal_year`); no period-end date was read here, so 'FY2025' for a name with a non-December year end is the block's label, not a date.
- Why an unmatched name is unmatched. The ratio and the other-period hits are printed; no cause was tested (restatement, a hierarchy with two level-1 trees, a newer fiscal year in one store than the other).
- PG_OPERATING_INCOME and every other segment list: only PG_REVENUE was compared.
- Periods 3, 4 and 5: the second pass tested Period 2 only.
- Bloomberg itself: no live call was made; AMD is the only name whose Period 1 was probed live (by the issuer, earlier today), and this read reproduces that one from stored data.
