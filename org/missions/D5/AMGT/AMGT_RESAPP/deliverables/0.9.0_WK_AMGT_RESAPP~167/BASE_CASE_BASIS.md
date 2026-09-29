# AMGT_RESAPP round 46 -- AMGT-uu-1 -- the Base-case basis table (AC4 judgment input)

Worker 0.9.0_WK_AMGT_RESAPP~167. Served `/thesis` `model.cases.base` read at 2026-09-29T02:31Z-02:32:17Z off deployed CodeSha256 `CtIvirvMTG47vvgBGmouk3GrTNKPjPIPx/6ovB+EAOM=`. Twin of `BASE_CASE_BASIS.json`. **M = 70** live-library names of 95 have a Base case with status SERVED (the other 25 are ABSENT with a served reason).

Recorded for the L9 reader, no verdict: the judgment asks, for each served Base case, whether both inputs name the adjusted basis and whether the value reads as a plausible price beside px_last.

## Served basis objects (verbatim; identical on every row)

Distinct served objects over the 70 rows: consensus_eps.basis 1, trailing_median_pe.basis 1, formula 1.

- **A. consensus_eps.basis** = mnemonic `BEST_EPS`; definition: "Bloomberg consensus (BEST) estimate of earnings per share for the overridden fiscal period."
- **B. trailing_median_pe.basis** = mnemonic `PX_LAST / IS_COMP_EPS_ADJUSTED`; definition: "Fiscal-year closing price (PX_LAST, the security's trading currency, brought to the EPS unit) divided by Bloomberg's adjusted (comparable) earnings per share (IS_COMP_EPS_ADJUSTED), joined on fiscal_year; the median over the closed fiscal years carrying both with adjusted EPS above zero."
- **F. formula** = "adjusted consensus EPS (FY1) x adjusted trailing-median P/E (PX_LAST / IS_COMP_EPS_ADJUSTED)"

Derived by this worker (substring 'adjust' in the served text, not served): A names adjusted on 0 of 70 rows; B names adjusted on 70 of 70; the formula string names adjusted twice on 70 of 70.

Ratio to px_last over the 70 rows: min 0.5124, median 1.1399, max 2.9835; served band [0.33, 3.0]; rows outside the band: 0.

## Table

Columns: EPS = FY1 BEST_EPS as served; PE = trailing median P/E as served; basis columns A/B refer to the verbatim objects above (all 70 rows carry them unchanged); window = the served list of fiscal years, n = its count; value = base_value; ratio = base_value / px_last.

| security_key | cur | EPS (FY1) | EPS basis | PE (median) | PE basis | window (n) | value | px_last | ratio |
|---|---|---|---|---|---|---|---|---|---|
| 2317_TT_Equity | TWD | 18.575 | A | 10.6308601224646 | B | 2016-2025 (n=10) | 197.46822677477994 | 250.5 | 0.7883 |
| 8035_JP_Equity | JPY | 1686.102 | A | 20.44646081611259 | B | 2017-2026 (n=10) | 34474.81847496908 | 55850.0 | 0.6173 |
| 8306_JP_Equity | JPY | 252.375 | A | 10.173023618684638 | B | 2017-2026 (n=10) | 2567.416835765536 | 3700.0 | 0.6939 |
| 8316_JP_Equity | JPY | 479.00800000000004 | A | 8.806356740783102 | B | 2017-2026 (n=10) | 4218.315329689032 | 6893.0 | 0.6120 |
| 8766_JP_Equity | JPY | 503.337 | A | 13.670400250646196 | B | 2017,2018,2019,2020,2021,2022,2023,2024,2026 (n=9) | 6880.818250959504 | 7987.0 | 0.8615 |
| 9433_JP_Equity | JPY | 200.028 | A | 11.907107073108602 | B | 2017,2018,2019,2020,2021,2022,2024,2025,2026 (n=9) | 2381.7548136197674 | 3017.0 | 0.7894 |
| AI_FP_Equity | EUR | 6.41 | A | 25.60181086452922 | B | 2016-2025 (n=10) | 164.1076076416323 | 168.12 | 0.9761 |
| AMD_US_Equity | USD | 7.472 | A | 55.62641509433962 | B | 2017-2025 (n=9) | 415.64057358490567 | 630.63 | 0.6591 |
| AMXB_MM_Equity | MXN | 1.551 | A | 14.857142857142858 | B | 2017-2025 (n=9) | 23.04342857142857 | 19.6 | 1.1757 |
| ASML_NA_Equity | EUR | 38.058 | A | 35.465051651357385 | B | 2016-2025 (n=10) | 1349.7289357473594 | 1503.2 | 0.8979 |
| BATS_LN_Equity | GBp | 3.614 | A | 8.639379556495212 | B | 2016-2025 (n=10) | 3122.2717717173696 | 4243.0 | 0.7359 |
| BBSE3_BZ_Equity | BRL | 4.438 | A | 12.45227942095568 | B | 2016-2025 (n=10) | 55.2632160702013 | 38.77 | 1.4254 |
| BNP_FP_Equity | EUR | 11.707 | A | 8.859080138075878 | B | 2016-2025 (n=10) | 103.71325117645432 | 98.43 | 1.0537 |
| CDNS_US_Equity | USD | 8.146 | A | 39.32668798194471 | B | 2016,2017,2018,2019,2021,2022,2023,2024,2025 (n=9) | 320.35520030092164 | 322.0 | 0.9949 |
| CLX_US_Equity | USD | 5.812 | A | 23.44536387404905 | B | 2017-2026 (n=10) | 136.26445483597308 | 81.8 | 1.6658 |
| CNR_CN_Equity | CAD | 8.152000000000001 | A | 20.665349007874905 | B | 2016-2025 (n=10) | 168.46392511219625 | 169.57 | 0.9935 |
| COST_US_Equity | USD | 22.722 | A | 33.00874326400762 | B | 2017-2026 (n=10) | 750.0246644447811 | 896.48 | 0.8366 |
| CPA_US_Equity | USD | 15.663 | A | 12.072085889570552 | B | 2016,2017,2018,2019,2021,2022,2023,2024,2025 (n=9) | 189.08508128834356 | 128.83 | 1.4677 |
| ENEL_IM_Equity | EUR | 0.725 | A | 12.78299996721788 | B | 2016-2025 (n=10) | 9.267674976232962 | 8.821 | 1.0506 |
| GOOGL_US_Equity | USD | 18.943 | A | 27.007861986193596 | B | 2016-2025 (n=10) | 511.6099296044653 | 343.92 | 1.4876 |
| GPN_US_Equity | USD | 13.648 | A | 16.566176470588236 | B | 2017-2025 (n=9) | 226.09517647058823 | 85.31 | 2.6503 |
| GSK_LN_Equity | GBp | 1.79 | A | 10.198849069974065 | B | 2016-2025 (n=10) | 1825.5939835253578 | 1877.0 | 0.9726 |
| HAL_US_Equity | USD | 2.344 | A | 18.30232558139535 | B | 2017-2025 (n=9) | 42.9006511627907 | 32.76 | 1.3095 |
| HD_US_Equity | USD | 15.055 | A | 22.511969944115513 | B | 2017-2026 (n=10) | 338.917707508659 | 292.18 | 1.1600 |
| HEI_US_Equity | USD | 6.316 | A | 48.73841961852861 | B | 2017-2025 (n=9) | 307.83185831062667 | 306.33 | 1.0049 |
| IBE_SM_Equity | EUR | 1.014 | A | 16.406518710286864 | B | 2016-2025 (n=10) | 16.63620997223088 | 20.25 | 0.8215 |
| ICICIBC_IN_Equity | INR | 87.905 | A | 18.930182632096916 | B | 2017-2026 (n=10) | 1664.0577042744794 | 1329.6 | 1.2515 |
| IDXX_US_Equity | USD | 14.801 | A | 52.45647662734818 | B | 2016-2025 (n=10) | 776.4083105613804 | 513.39 | 1.5123 |
| IMB_LN_Equity | GBp | 3.334 | A | 7.473836160230964 | B | 2017-2025 (n=9) | 2491.7769758210034 | 2475.0 | 1.0068 |
| INTU_US_Equity | USD | 22.958000000000002 | A | 32.23346307598601 | B | 2017-2026 (n=10) | 740.0158452984869 | 277.13 | 2.6703 |
| ISP_IM_Equity | EUR | 0.592 | A | 7.944910195803869 | B | 2016-2025 (n=10) | 4.70338683591589 | 6.724 | 0.6995 |
| ISRG_US_Equity | USD | 10.769 | A | 57.890514841259154 | B | 2016-2025 (n=10) | 623.4229543255199 | 399.52 | 1.5604 |
| KMB_US_Equity | USD | 7.371 | A | 18.710022944637544 | B | 2016-2025 (n=10) | 137.91157912492335 | 97.22 | 1.4186 |
| KOFUBL_MM_Equity | MXN | 12.16 | A | 17.84076080984428 | B | 2016-2025 (n=10) | 216.94365144770646 | 192.82 | 1.1251 |
| KPN_NA_Equity | EUR | 0.23700000000000002 | A | 18.409562655789713 | B | 2016-2025 (n=10) | 4.363066349422162 | 3.957 | 1.1026 |
| LLY_US_Equity | USD | 36.593 | A | 27.805211985456435 | B | 2016-2025 (n=10) | 1017.4761221838074 | 1183.46 | 0.8597 |
| MA_US_Equity | USD | 19.933 | A | 34.1750891664341 | B | 2016-2025 (n=10) | 681.2120523545309 | 566.08 | 1.2034 |
| MELI_US_Equity | USD | 38.144 | A | 80.7574511819116 | B | 2016,2017,2021,2022,2023,2024,2025 (n=7) | 3080.412217882836 | 1754.13 | 1.7561 |
| MER_PM_Equity | PHP | 47.048 | A | 14.25709316676793 | B | 2016-2025 (n=10) | 670.7677193100976 | 453.0 | 1.4807 |
| ML_FP_Equity | EUR | 2.629 | A | 12.043694376179532 | B | 2016-2025 (n=10) | 31.66287251497599 | 33.5 | 0.9452 |
| MNST_US_Equity | USD | 1.156 | A | 37.294048203694615 | B | 2016-2025 (n=10) | 43.11191972347097 | 42.67 | 1.0104 |
| MSCI_US_Equity | USD | 19.697 | A | 39.7822021085322 | B | 2016-2025 (n=10) | 783.5900349317587 | 556.08 | 1.4091 |
| NESN_SW_Equity | CHF | 4.455 | A | 21.903063725490195 | B | 2016-2025 (n=10) | 97.57814889705882 | 77.94 | 1.2520 |
| NFLX_US_Equity | USD | 3.517 | A | 60.84136502095709 | B | 2016-2025 (n=10) | 213.97908077870608 | 71.72 | 2.9835 |
| NG/_LN_Equity | GBp | 0.897 | A | 14.472797100070178 | B | 2017-2026 (n=10) | 1298.209899876295 | 1135.5 | 1.1433 |
| NKE_US_Equity | USD | 1.678 | A | 35.62920679967894 | B | 2017-2026 (n=10) | 59.78580900986126 | 35.99 | 1.6612 |
| NOKIA_FH_Equity | EUR | 0.343 | A | 13.550524475524474 | B | 2016-2025 (n=10) | 4.647829895104895 | 9.07 | 0.5124 |
| NOW_US_Equity | USD | 4.067 | A | 76.15660919540231 | B | 2019-2025 (n=7) | 309.7289295977012 | 137.78 | 2.2480 |
| NU_US_Equity | USD | 0.881 | A | 33.820544051969144 | B | 2021-2025 (n=5) | 29.795899309784815 | 13.56 | 2.1973 |
| OMAB_MM_Equity | MXN | 15.865 | A | 16.024965496549655 | B | 2018-2025 (n=8) | 254.23607760276028 | 223.03 | 1.1399 |
| ORA_FP_Equity | EUR | 1.26 | A | 16.259303271740972 | B | 2016-2025 (n=10) | 20.486722122393626 | 14.015 | 1.4618 |
| PWR_US_Equity | USD | 16.692 | A | 23.29786541791097 | B | 2016-2025 (n=10) | 388.8879695557699 | 649.13 | 0.5991 |
| QXO_US_Equity | USD | 0.27 | A | 49.585300017700156 | B | 2017,2018,2019,2020,2024,2025 (n=6) | 13.388031004779043 | 12.26 | 1.0920 |
| RKT_LN_Equity | GBp | 3.371 | A | 17.626154077394652 | B | 2016-2025 (n=10) | 5941.776539489737 | 4923.0 | 1.2069 |
| RMS_FP_Equity | EUR | 44.424 | A | 46.225182852634816 | B | 2016-2025 (n=10) | 2053.507523045449 | 1354.5 | 1.5161 |
| RWE_GR_Equity | EUR | 3.019 | A | 11.637877163603864 | B | 2016-2025 (n=10) | 35.13475115692007 | 59.38 | 0.5917 |
| SAN_FP_Equity | EUR | 8.6 | A | 13.261482915979599 | B | 2016-2025 (n=10) | 114.04875307742455 | 72.1 | 1.5818 |
| SAP_GY_Equity | EUR | 7.12 | A | 22.416952998053112 | B | 2016-2025 (n=10) | 159.60870534613815 | 184.18 | 0.8666 |
| SLB_US_Equity | USD | 2.49 | A | 23.960686639908257 | B | 2016-2025 (n=10) | 59.662109733371565 | 51.43 | 1.1601 |
| SNPS_US_Equity | USD | 15.118 | A | 30.968210717529516 | B | 2017-2025 (n=9) | 468.1774096276112 | 424.91 | 1.1018 |
| SSE_LN_Equity | GBp | 1.843 | A | 13.275126393175416 | B | 2017-2026 (n=10) | 2446.605794262229 | 2475.0 | 0.9885 |
| ST_SP_Equity | SGD | 0.19 | A | 19.572340534847278 | B | 2017-2026 (n=10) | 3.7187447016209827 | 4.24 | 0.8771 |
| UBER_US_Equity | USD | 3.322 | A | 37.85378098525259 | B | 2023-2025 (n=3) | 125.7502604330091 | 69.22 | 1.8167 |
| UNH_US_Equity | USD | 19.855 | A | 20.482547791932983 | B | 2016-2025 (n=10) | 406.68098640882937 | 376.59 | 1.0799 |
| VIVT3_BZ_Equity | BRL | 2.4290000000000003 | A | 15.2954286856891 | B | 2016-2025 (n=10) | 37.15259627753883 | 30.41 | 1.2217 |
| VLO_US_Equity | USD | 48.449 | A | 15.343072573044298 | B | 2016,2017,2018,2019,2021,2022,2023,2024,2025 (n=9) | 743.3565230914231 | 382.86 | 1.9416 |
| V_US_Equity | USD | 13.224 | A | 25.905472636815922 | B | 2017-2025 (n=9) | 342.57397014925374 | 367.98 | 0.9310 |
| WALMEX*_MM_Equity | MXN | 3.013 | A | 24.23724233989953 | B | 2016-2025 (n=10) | 73.02681117011728 | 45.92 | 1.5903 |
| WDAY_US_Equity | USD | 11.088000000000001 | A | 45.96978021978022 | B | 2022-2026 (n=5) | 509.7129230769231 | 190.99 | 2.6688 |
| ZTS_US_Equity | USD | 6.206 | A | 30.023702185792352 | B | 2016-2025 (n=10) | 186.32709576502734 | 70.27 | 2.6516 |
