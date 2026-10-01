# DENOMINATION CENSUS -- AMGT_CORPUS round 25, CRPS-aa-1 (0.9.0_WK_AMGT_CORPUS~1)

Population: 73 figures on 25 securities (BP/NG excluded under Z-S64; the -SLASH- twin keys of both are excluded too).

Every class is decided by a stated read on the newest served block; nothing is assumed from a field name and no FX rate is invented.

## Counts by mnemonic and class

| mnemonic | quote | reporting | UNRESOLVED |
|---|---|---|---|
| CUR_MKT_CAP | 12 | 5 | 8 |
| NET_DEBT | 0 | 5 | 20 |
| CURR_ENTP_VAL | 0 | 10 | 13 |

## Method

- **market_cap_read**: CUR_MKT_CAP / (PX_LAST x EQY_SH_OUT_REAL), all three from the same block; for a GBp quote PX_LAST is divided by 100 (pence to pounds, a definitional subunit, not FX). A ratio of 1 within 0.2% decides the value is in the quote currency's major unit; anything else is UNRESOLVED (never an FX-scaled guess).
- **identity_read**: CURR_ENTP_VAL ~ CUR_MKT_CAP/1e6 + NET_DEBT under four EV-side/ND-side hypotheses (QQ, RR, RQ, QR), tolerance +/-12%; the market cap is converted to the reporting currency only with a factor f implied by the block's own Bloomberg dimensionless ratios (PX_TO_BOOK_RATIO x BOOK_VAL_PER_SH / PX_LAST agreeing within 3% with PE_RATIO x IS_EPS / PX_LAST at the latest FY carrying all four). No external FX rate is used and none is invented.
- **side_rule**: A side (quote or reporting) is decided for a figure only if the best hypothesis residual with it is within 12% and the best residual with the other side is beyond 24%.
- **no_factor_rule**: With no block-implied factor, the all-quote identity holding does NOT decide (a same-magnitude reporting currency is not excluded); the identity failing plus the EV tracking read (header EV / (CURRENT_EV_TO_T12M_EBITDA x EBITDA) over the price ratio, within 12%) decides EV only.
- **gbp_note**: For quote GBp: a value measured in GBP (the major unit) has no label in the two-class vocabulary: it is 'reporting' only where the reporting currency is GBP; otherwise UNRESOLVED.

## Figures

| security_key | mnemonic | quote/reporting | class |
|---|---|---|---|
| 1299_HK_Equity | CUR_MKT_CAP | HKD/USD | quote |
| 1299_HK_Equity | NET_DEBT | HKD/USD | UNRESOLVED |
| 1299_HK_Equity | CURR_ENTP_VAL | HKD/USD | reporting |
| 939_HK_Equity | CUR_MKT_CAP | HKD/CNY | UNRESOLVED |
| 939_HK_Equity | NET_DEBT | HKD/CNY | UNRESOLVED |
| 992_HK_Equity | CUR_MKT_CAP | HKD/USD | quote |
| 992_HK_Equity | NET_DEBT | HKD/USD | UNRESOLVED |
| 992_HK_Equity | CURR_ENTP_VAL | HKD/USD | UNRESOLVED |
| AZN_LN_Equity | CUR_MKT_CAP | GBp/USD | UNRESOLVED |
| AZN_LN_Equity | NET_DEBT | GBp/USD | UNRESOLVED |
| AZN_LN_Equity | CURR_ENTP_VAL | GBp/USD | reporting |
| BABA_US_Equity | CUR_MKT_CAP | USD/CNY | quote |
| BABA_US_Equity | NET_DEBT | USD/CNY | UNRESOLVED |
| BABA_US_Equity | CURR_ENTP_VAL | USD/CNY | UNRESOLVED |
| BATS_LN_Equity | CUR_MKT_CAP | GBp/GBP | reporting |
| BATS_LN_Equity | NET_DEBT | GBp/GBP | reporting |
| BATS_LN_Equity | CURR_ENTP_VAL | GBp/GBP | reporting |
| BZLFY_US_Equity | CUR_MKT_CAP | USD/GBP | quote |
| BZLFY_US_Equity | NET_DEBT | USD/GBP | UNRESOLVED |
| BZLFY_US_Equity | CURR_ENTP_VAL | USD/GBP | UNRESOLVED |
| GSK_LN_Equity | CUR_MKT_CAP | GBp/GBP | reporting |
| GSK_LN_Equity | NET_DEBT | GBp/GBP | reporting |
| GSK_LN_Equity | CURR_ENTP_VAL | GBp/GBP | reporting |
| HSBA_LN_Equity | CUR_MKT_CAP | GBp/USD | UNRESOLVED |
| HSBA_LN_Equity | NET_DEBT | GBp/USD | UNRESOLVED |
| ICT_PM_Equity | CUR_MKT_CAP | PHP/USD | quote |
| ICT_PM_Equity | NET_DEBT | PHP/USD | UNRESOLVED |
| ICT_PM_Equity | CURR_ENTP_VAL | PHP/USD | reporting |
| IMB_LN_Equity | CUR_MKT_CAP | GBp/GBP | reporting |
| IMB_LN_Equity | NET_DEBT | GBp/GBP | reporting |
| IMB_LN_Equity | CURR_ENTP_VAL | GBp/GBP | reporting |
| JD_US_Equity | CUR_MKT_CAP | USD/CNY | UNRESOLVED |
| JD_US_Equity | NET_DEBT | USD/CNY | UNRESOLVED |
| JD_US_Equity | CURR_ENTP_VAL | USD/CNY | UNRESOLVED |
| NOVN_SW_Equity | CUR_MKT_CAP | CHF/USD | quote |
| NOVN_SW_Equity | NET_DEBT | CHF/USD | UNRESOLVED |
| NOVN_SW_Equity | CURR_ENTP_VAL | CHF/USD | reporting |
| PBR_US_Equity | CUR_MKT_CAP | USD/BRL | UNRESOLVED |
| PBR_US_Equity | NET_DEBT | USD/BRL | UNRESOLVED |
| PBR_US_Equity | CURR_ENTP_VAL | USD/BRL | UNRESOLVED |
| RIO_LN_Equity | CUR_MKT_CAP | GBp/USD | UNRESOLVED |
| RIO_LN_Equity | NET_DEBT | GBp/USD | UNRESOLVED |
| RIO_LN_Equity | CURR_ENTP_VAL | GBp/USD | UNRESOLVED |
| RKT_LN_Equity | CUR_MKT_CAP | GBp/GBP | reporting |
| RKT_LN_Equity | NET_DEBT | GBp/GBP | reporting |
| RKT_LN_Equity | CURR_ENTP_VAL | GBp/GBP | reporting |
| SHOP_CN_Equity | CUR_MKT_CAP | CAD/USD | UNRESOLVED |
| SHOP_CN_Equity | NET_DEBT | CAD/USD | UNRESOLVED |
| SHOP_CN_Equity | CURR_ENTP_VAL | CAD/USD | UNRESOLVED |
| SPOT_US_Equity | CUR_MKT_CAP | USD/EUR | quote |
| SPOT_US_Equity | NET_DEBT | USD/EUR | UNRESOLVED |
| SPOT_US_Equity | CURR_ENTP_VAL | USD/EUR | UNRESOLVED |
| SSE_LN_Equity | CUR_MKT_CAP | GBp/GBP | reporting |
| SSE_LN_Equity | NET_DEBT | GBp/GBP | reporting |
| SSE_LN_Equity | CURR_ENTP_VAL | GBp/GBP | reporting |
| TSM_US_Equity | CUR_MKT_CAP | USD/TWD | quote |
| TSM_US_Equity | NET_DEBT | USD/TWD | UNRESOLVED |
| TSM_US_Equity | CURR_ENTP_VAL | USD/TWD | UNRESOLVED |
| TTE_FP_Equity | CUR_MKT_CAP | EUR/USD | quote |
| TTE_FP_Equity | NET_DEBT | EUR/USD | UNRESOLVED |
| TTE_FP_Equity | CURR_ENTP_VAL | EUR/USD | UNRESOLVED |
| UBSG_SW_Equity | CUR_MKT_CAP | CHF/USD | quote |
| UBSG_SW_Equity | NET_DEBT | CHF/USD | UNRESOLVED |
| UBSG_SW_Equity | CURR_ENTP_VAL | CHF/USD | reporting |
| ULVR_LN_Equity | CUR_MKT_CAP | GBp/EUR | UNRESOLVED |
| ULVR_LN_Equity | NET_DEBT | GBp/EUR | UNRESOLVED |
| ULVR_LN_Equity | CURR_ENTP_VAL | GBp/EUR | UNRESOLVED |
| UNVGY_US_Equity | CUR_MKT_CAP | USD/EUR | quote |
| UNVGY_US_Equity | NET_DEBT | USD/EUR | UNRESOLVED |
| UNVGY_US_Equity | CURR_ENTP_VAL | USD/EUR | UNRESOLVED |
| ZURN_SW_Equity | CUR_MKT_CAP | CHF/USD | quote |
| ZURN_SW_Equity | NET_DEBT | CHF/USD | UNRESOLVED |
| ZURN_SW_Equity | CURR_ENTP_VAL | CHF/USD | UNRESOLVED |

The `measurement` text of every figure is in the JSON beside this file (one entry per figure, the read that decided it).
