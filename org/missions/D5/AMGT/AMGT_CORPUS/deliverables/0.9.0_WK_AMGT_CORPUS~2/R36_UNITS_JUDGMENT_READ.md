# R36 units judgment read (CRPS-al-3), 0.9.0_WK_AMGT_CORPUS~2

Read through `lib.research.api.scoped_amgt.read_model_block(<key>)` on 2026-10-04 (read only). Newest served block per name:
- `derived/model_block/BA_US_Equity/20261004T195644Z/model_block.json` (currencies: quote USD, reporting USD, mixed False)
- `derived/model_block/TSM_US_Equity/20261004T195814Z/model_block.json` (currencies: quote USD, reporting TWD, mixed True, converted False)
- `derived/model_block/SAP_GY_Equity/20261004T195805Z/model_block.json` (currencies: quote EUR, reporting EUR, mixed False)

Members chosen (one per family, same across names where a figure exists): SHORT_NAME, EXPECTED_REPORT_DT, EQY_FUND_YEAR,
NORMALIZED_ROE, TOTAL_EQUITY, IS_SH_FOR_DILUTED_EPS, IS_EPS, EV_TO_T12M_EBITDA. Value is the header value, else the newest fiscal year.

## 1. Family table

| family | security_key | mnemonic | served unit | served value | basis words | verdict |
|---|---|---|---|---|---|---|
| TEXT | BA_US_Equity | SHORT_NAME | TEXT (string field) | BOEING CO/THE | short (abbreviated) name of the issuer | RIGHT |
| TEXT | TSM_US_Equity | SHORT_NAME | TEXT (string field) | TAIWAN SEMIC-ADR | short (abbreviated) name of the issuer | RIGHT |
| TEXT | SAP_GY_Equity | SHORT_NAME | TEXT (string field) | SAP SE | short (abbreviated) name of the issuer | RIGHT |
| DATE | BA_US_Equity | EXPECTED_REPORT_DT | DATE (ISO yyyy-mm-dd) | 2026-10-27 | date of next expected earnings report | RIGHT |
| DATE | TSM_US_Equity | EXPECTED_REPORT_DT | DATE (ISO yyyy-mm-dd) | 2026-10-15 | date of next expected earnings report | RIGHT |
| DATE | SAP_GY_Equity | EXPECTED_REPORT_DT | DATE (ISO yyyy-mm-dd) | 2026-10-21 | date of next expected earnings report | RIGHT |
| YEAR | BA_US_Equity | EQY_FUND_YEAR | no figure served (UNRESOLVED, absent) | none | fiscal year of the fundamentals, a year number | CANNOT-TELL |
| YEAR | TSM_US_Equity | EQY_FUND_YEAR | no figure served (UNRESOLVED, absent) | none | fiscal year of the fundamentals, a year number | CANNOT-TELL |
| YEAR | SAP_GY_Equity | EQY_FUND_YEAR | no figure served (UNRESOLVED, absent) | none | fiscal year of the fundamentals, a year number | CANNOT-TELL |
| PERCENT | BA_US_Equity | NORMALIZED_ROE | PERCENT | 941.5759 (FY2018, newest of 3) | normalized return on equity, percent | RIGHT |
| PERCENT | TSM_US_Equity | NORMALIZED_ROE | PERCENT | 35.5298 (FY2025) | normalized return on equity, percent | RIGHT |
| PERCENT | SAP_GY_Equity | NORMALIZED_ROE | PERCENT | 15.9666 (FY2025) | normalized return on equity, percent | RIGHT |
| ABSOLUTE_OR_MILLIONS | BA_US_Equity | TOTAL_EQUITY | MILLIONS | 5457.0 (FY2025) | total equity incl. minority, millions of reporting currency | RIGHT |
| ABSOLUTE_OR_MILLIONS | TSM_US_Equity | TOTAL_EQUITY | MILLIONS | 5460795.283 (FY2025) | total equity incl. minority, millions of reporting currency | RIGHT |
| ABSOLUTE_OR_MILLIONS | SAP_GY_Equity | TOTAL_EQUITY | MILLIONS | 45073.0 (FY2025) | total equity incl. minority, millions of reporting currency | RIGHT |
| SHARE_COUNT_MILLIONS | BA_US_Equity | IS_SH_FOR_DILUTED_EPS | MILLIONS (share count) | 762.3 (FY2025) | weighted-average diluted shares, millions of shares | RIGHT |
| SHARE_COUNT_MILLIONS | TSM_US_Equity | IS_SH_FOR_DILUTED_EPS | no figure served | none | weighted-average diluted shares, millions of shares | CANNOT-TELL |
| SHARE_COUNT_MILLIONS | SAP_GY_Equity | IS_SH_FOR_DILUTED_EPS | MILLIONS (share count) | 1175.0 (FY2025) | weighted-average diluted shares, millions of shares | RIGHT |
| PER_SHARE | BA_US_Equity | IS_EPS | PER SHARE (local trading/reporting currency) | 2.49 (FY2025) | reported earnings per share | RIGHT |
| PER_SHARE | TSM_US_Equity | IS_EPS | no figure served | none | reported earnings per share | CANNOT-TELL |
| PER_SHARE | SAP_GY_Equity | IS_EPS | PER SHARE (local trading/reporting currency) | 6.14 (FY2025) | reported earnings per share | RIGHT |
| RATIO | BA_US_Equity | EV_TO_T12M_EBITDA | RATIO (dimensionless multiple) | 30.0787 (FY2025) | enterprise value / trailing-twelve-month EBITDA | RIGHT |
| RATIO | TSM_US_Equity | EV_TO_T12M_EBITDA | RATIO (dimensionless multiple) | 14.5693 (FY2025) | enterprise value / trailing-twelve-month EBITDA | RIGHT |
| RATIO | SAP_GY_Equity | EV_TO_T12M_EBITDA | RATIO (dimensionless multiple) | 22.1108 (FY2025) | enterprise value / trailing-twelve-month EBITDA | RIGHT |

Why, one sentence per group:
- TEXT: three strings, each an abbreviated issuer name, no number involved.
- DATE: three ISO yyyy-mm-dd strings, all after the read date 2026-10-04 (a next expected report), matching the basis text.
- YEAR: EQY_FUND_YEAR is in no header, no fiscal row and the unresolved list carries no served value on any of the three names, so the YEAR placement is untested (a block lookup returned none).
- PERCENT: unit PERCENT agrees with the definition; cross-read EARN_FOR_COMMON / TOTAL_EQUITY gives SAP 7161/45073 = 15.9 (served 15.97) and TSM 1717883/5460795 = 31.5 (served 35.5, Bloomberg's own normalization); BA 941.6 for FY2018 is a very large percent on a FY2018 equity of 410 million, the percent scale holds.
- ABSOLUTE_OR_MILLIONS: millions agree with the basis text and the magnitudes: SAP 45,073 million EUR, BA 5,457 million USD, TSM 5.46 million million TWD (5.46 trillion TWD) with EARN_FOR_COMMON 1.72 trillion TWD giving the ROE above.
- SHARE_COUNT_MILLIONS: BA 762.3 against EQY_SH_OUT_REAL 790.4 million and SAP 1175 against 1228.5 million are the same order in millions; TSM lands no diluted share figure so it cannot be told (no value).
- PER_SHARE: BA 2.49 on net income 2235 / 762.3 = 2.93 (EPS after preferred/other adjustments, same scale) and SAP 6.14 on 7161 / 1175 = 6.09 both read as per-share amounts; TSM lands no per-share figure among the 52 or IS_EPS, so it cannot be told.
- RATIO: BA 30.08 against EV 184,627 / EBITDA 6,752 = 27.3 and SAP 22.11 against 225,333 / 10,928 = 20.6 are multiples in the right range; TSM 14.57 is a dimensionless multiple whose scale cannot be reproduced to the decimal from served TWD/USD figures but is of the right order (RIGHT on unit and magnitude, not on exact reproduction).

## 2. Currency section -- TSM_US_Equity

Block `currencies` entry: quote USD, reporting TWD, mixed True, converted False. This entry is correct (an ADR quoted in USD whose
filings are in TWD; EQY_FUND_CRNCY served TWD, CRNCY served USD).

TSM carries 167 figures of the 52 round-34 mnemonics (23 mnemonics landed; 29 of the 52 have none on this name). Every one of the 167
carries `currency` null and `currency_basis` "invariant". Graded by what the number is:
- 75 RIGHT: TEXT 3 (SHORT_NAME, COUNTRY_FULL_NAME, LONG_COMP_NAME), DATE 2 (EXPECTED_REPORT_DT, ERN_ANN_DT_AND_PER), PERCENT 30
  (FCF_MARGIN_AFTER_OPER_LEA_PYMT, NORMALIZED_ROA, NORMALIZED_ROE x 10 years), RATIO 40 (EV_TO_T12M_EBIT, EV_TO_T12M_EBITDA,
  EV_TO_T12M_SALES, LOW_PRICE_TO_FREE_CASH_FLOW x 10 years). Dimensionless or non-monetary: no currency is the right label.
- 92 WRONG: monetary figures that carry no currency label although the block is mixed.
  - 90 statement figures in TWD (ARD_TOTAL_CURRENT_LIABILITIES, ARD_TOT_ASSETS, CAPEX_ABSOLUTE_VALUE, CASH_AND_MARKETABLE_SECURITIES,
    CF_CASH_FROM_OPER, EARN_FOR_COMMON, MINORITY_NONCONTROLLING_INTEREST, SHORT_AND_LONG_TERM_DEBT, TOTAL_EQUITY x 10 years) read
    currency null / invariant; they should be TWD (reporting, EQY_FUND_CRNCY). Evidence the mechanism exists: 60 other TSM MILLIONS
    statement figures (e.g. EBITDA FY2025 2,624,188 million) carry `currency` TWD, basis "reporting (EQY_FUND_CRNCY)".
  - 1 CRNCY_ADJ_MKT_CAP (2,452,061 million = CUR_MKT_CAP 2,452,061,183,866 / 1e6, a price-based figure) null; should be USD (quote). CUR_MKT_CAP
    itself carries USD, basis quote (CRNCY).
  - 1 AVG_DAILY_VALUE_TRADED_3M (4,907,136,000, a traded value in the trading currency) null; should be USD (quote).
- 0 CANNOT-TELL.

The block-level `currencies` entry is right; the 92 figure-level labels are missing, so a consumer of the figure alone cannot tell TWD
from USD on a mixed block.

CURRENCY TSM_US_Equity figures 167 labelled 167 right 75 wrong 92 cannot-tell 0

## 3. Closing note

- WRONG in the family table: 0. CANNOT-TELL: 5 (YEAR x 3 absent everywhere; SHARE_COUNT_MILLIONS and PER_SHARE on TSM, no figure).
  RIGHT: 19. Totals RIGHT 19 / WRONG 0 / CANNOT-TELL 5 over 24 rows.
- WRONG in the currency section: 92 of 167 TSM figures (see above), touching the ABSOLUTE_OR_MILLIONS family (monetary figures of the
  52). BA and SAP carry the same null label on their monetary figures of the 52 (BA: 125 MILLIONS + 23 PER SHARE + 1 ABSOLUTE with
  `currency` null; the block is single-currency there, so the label is incomplete but not misleading).
- What it would take: the currency-basis assignment in the producer/classifier for the 52 monetary mnemonics (statement lines
  reporting-currency; HISTORICAL_MARKET_CAP, CRNCY_ADJ_MKT_CAP, AVG_DAILY_VALUE_TRADED_3M quote-currency), the way the older
  MILLIONS fields already get it, then a re-derive of the 96 blocks. Filed as row AMGT_CORPUS-Z-W2-S20.
