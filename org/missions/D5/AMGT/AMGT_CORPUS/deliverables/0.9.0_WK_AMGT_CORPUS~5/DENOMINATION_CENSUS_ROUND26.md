# DENOMINATION CENSUS -- AMGT_CORPUS round 26, CRPS-ab-5 (0.9.0_WK_AMGT_CORPUS~5)

Population: 6 figures on 2 securities (BP/ LN Equity, NG/ LN Equity; read at the encoded keys BP-SLASH-_LN_Equity and NG-SLASH-_LN_Equity). Extends round 25 (`0.9.0_WK_AMGT_CORPUS~1/DENOMINATION_CENSUS_ROUND25.json`) to the two names it excluded.

Every class is decided by a stated read on the newest served block; nothing is assumed from a field name and no FX rate is invented. The `measurement` text of every figure is in the JSON beside this file.

## Counts by mnemonic and class

| mnemonic | quote | reporting | UNRESOLVED |
|---|---|---|---|
| CUR_MKT_CAP | 0 | 1 | 1 |
| NET_DEBT | 0 | 1 | 1 |
| CURR_ENTP_VAL | 0 | 2 | 0 |

## Method

- **market_cap_read**: CUR_MKT_CAP / (PX_LAST x EQY_SH_OUT_REAL), all three from the same block; for a GBp quote PX_LAST is divided by 100 (pence to pounds, a definitional subunit, not FX). A ratio of 1 within 0.2% decides the value is in the quote currency's major unit; anything else is UNRESOLVED (never an FX-scaled guess).
- **identity_read**: CURR_ENTP_VAL ~ CUR_MKT_CAP/1e6 + NET_DEBT under four EV-side/ND-side hypotheses (QQ, RR, RQ, QR), tolerance +/-12%; the market cap is converted to the reporting currency only with a factor f implied by the block's own Bloomberg dimensionless ratios (PX_TO_BOOK_RATIO x BOOK_VAL_PER_SH / PX_LAST agreeing within 3% with PE_RATIO x IS_EPS / PX_LAST at the latest FY carrying all four). No external FX rate is used and none is invented.
- **side_rule**: A side (quote or reporting) is decided for a figure only if the best hypothesis residual with it is within 12% and the best residual with the other side is beyond 24%.
- **gbp_note**: For quote GBp: a value measured in GBP (the major unit) has no label in the two-class vocabulary: it is 'reporting' only where the reporting currency is GBP; otherwise UNRESOLVED.

## Figures

| security_key | mnemonic | quote/reporting | class | deciding read |
|---|---|---|---|---|
| BP-SLASH-_LN_Equity | CUR_MKT_CAP | GBp/USD | UNRESOLVED | value/(PX_LAST/100 x shares)=1.00000: GBP, neither GBp nor USD |
| BP-SLASH-_LN_Equity | NET_DEBT | GBp/USD | UNRESOLVED | identity best residual 1.9% (quote-major side) vs 9.9% (reporting side): sides not separated |
| BP-SLASH-_LN_Equity | CURR_ENTP_VAL | GBp/USD | reporting | identity best residual 1.9% reporting side vs 37.1% quote side: USD decided |
| NG-SLASH-_LN_Equity | CUR_MKT_CAP | GBp/GBP | reporting | value/(PX_LAST/100 x shares)=1.00000: GBP == reporting GBP |
| NG-SLASH-_LN_Equity | NET_DEBT | GBp/GBP | reporting | identity residual +0.03% in GBP-major unit; quote-major == reporting |
| NG-SLASH-_LN_Equity | CURR_ENTP_VAL | GBp/GBP | reporting | identity residual +0.03% in GBP-major unit; quote-major == reporting |
