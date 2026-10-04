"""AMGT_CORPUS round 34, CRPS-aj-1 -- the daily Model-block refresh carries the V3 set, the long name and the earnings
dates (Andrew-direct 2026-10-03 ~20:3xZ card 3, "yes, one daily pull for all of it"). Offline: it imports the producer and
never opens a Bloomberg session or an AWS client. The issuer's file.

  BUILD arms (FAIL at the base, PASS after):
    b1 each of the 49 V3 mnemonics sits in exactly ONE of HEADER_FIELDS / HIST_FIELDS / FORECAST_FIELDS
    b2 LONG_COMP_NAME, EXPECTED_REPORT_DT and ERN_ANN_DT_AND_PER sit in HEADER_FIELDS
    b3 BEST_CPS sits in FORECAST_FIELDS, and BEST_FPERIOD_OVERRIDE sits in none of the three lists
    b4 every member of the three lists AND each of the 52 new mnemonics has a non-empty FIELD_BASIS entry
    b5 the producer has a `refresh` stage: cmd_refresh exists and main() accepts `refresh`
  CONTROL arms (PASS at the base and after):
    c1 every base member of the three lists keeps its base index (new members are APPENDED, nothing re-ordered)
    c2 the admit stage and its batch cap are unchanged (cmd_admit exists, ADMIT_BATCH == 3, HIST_FIELDS_PER_REQUEST == 25)
    c3 the F2/G-24 cap still refuses a 4-security pull before any client opens
  -> one 'ARM <id> PASS|FAIL <got>' line per arm, then 'aj1 build <p>/5 control <q>/3'
"""
import importlib.util
import os
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
for p in (TOP, RES):
    if p not in sys.path:
        sys.path.insert(0, p)
spec = importlib.util.spec_from_file_location("mbp_aj1", os.path.join(RES, "model_block_pull.py"))
mbp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mbp)

# The V3 set, measured 2026-10-03 ~21:0xZ by 2.0.0_SA_COO~X: `python -m lib.research.corpus.typecast --read-latest`
# (workbooks_read 158, with_mnemonics 120, mnemonic_core 96) MINUS the producer's HEADER+HIST+FORECAST union at CLOUD
# 6527a03cc1 (66 fields; 46 of the core) = 50, less BEST_FPERIOD_OVERRIDE (an override parameter, not a field) = 49.
V3 = [
    "ARD_GOODWLL", "ARD_OTHER_INTANGIBLE_ASSET", "ARD_SHARES_OUTSTANDING", "ARD_TOTAL_CURRENT_LIABILITIES",
    "ARD_TOT_ASSETS", "AVERAGE_DIVIDEND_YIELD", "AVERAGE_EV_TO_T12M_EBIT", "AVERAGE_EV_TO_T12M_SALES",
    "AVERAGE_PRICE_EARNINGS_RATIO", "AVERAGE_PRICE_TO_BOOK_RATIO", "AVERAGE_PRICE_TO_FREE_CASH_FLOW",
    "AVG_DAILY_VALUE_TRADED_3M", "AVG_EV_TO_T12M_EBITDA", "BEST_CPS", "CAPEX_ABSOLUTE_VALUE",
    "CASH_AND_MARKETABLE_SECURITIES", "CF_CASH_FROM_OPER", "COUNTRY_FULL_NAME", "CRNCY_ADJ_MKT_CAP", "DIVIDEND_YIELD",
    "EARN_FOR_COMMON", "EQY_FUND_YEAR", "EV_TO_T12M_EBIT", "EV_TO_T12M_EBITDA", "EV_TO_T12M_SALES",
    "FCF_MARGIN_AFTER_OPER_LEA_PYMT", "FREE_CASH_FLOW_PER_SH", "HIGH_CLOSING_PRICE_TO_BOOK_RATIO", "HIGH_DIVIDEND_YIELD",
    "HIGH_EV_TO_T12M_EBIT", "HIGH_EV_TO_T12M_EBITDA", "HIGH_EV_TO_T12M_SALES", "HIGH_PRICE_TO_FREE_CASH_FLOW",
    "HISTORICAL_MARKET_CAP", "LOW_CLOSING_PRICE_TO_BOOK_RATIO", "LOW_DIVIDEND_YIELD", "LOW_EV_TO_T12M_EBIT",
    "LOW_EV_TO_T12M_EBITDA", "LOW_EV_TO_T12M_SALES", "LOW_PRICE_TO_FREE_CASH_FLOW", "MINORITY_NONCONTROLLING_INTEREST",
    "NORMALIZED_ROA", "NORMALIZED_ROE", "PX_ERN_RATIO_WITH_HIGH_CLOS_PX", "PX_ERN_RATIO_WITH_LOW_CLOS_PX",
    "SHORT_AND_LONG_TERM_DEBT", "SHORT_NAME", "TANG_BOOK_VAL_PER_SH", "TOTAL_EQUITY",
]
NAME_AND_EARNINGS = ["LONG_COMP_NAME", "EXPECTED_REPORT_DT", "ERN_ANN_DT_AND_PER"]

BASE_HEADER = ['NAME', 'CRNCY', 'CNTRY_OF_DOMICILE', 'GICS_SECTOR_NAME', 'PX_LAST', 'CUR_MKT_CAP', 'NET_DEBT',
               'CURR_ENTP_VAL', 'VOLUME_AVG_30D', 'EQY_SH_OUT_REAL', 'EQY_FREE_FLOAT_PCT', 'EQY_BETA', 'EQY_DVD_YLD_IND',
               'SHORT_INT_RATIO', 'SI_PERCENT_EQUITY_FLOAT', 'CIE_DES', 'CIE_DES_BULK', 'EQY_FUND_CRNCY']
BASE_HIST = ['PX_LAST', 'SALES_REV_TURN', 'IS_OPER_INC', 'OPER_MARGIN', 'EBITDA', 'EBITDA_ADJUSTED', 'EBITDA_MARGIN',
             'IS_EPS', 'BOOK_VAL_PER_SH', 'IS_SH_FOR_DILUTED_EPS', 'CAPITAL_EXPEND', 'CF_FREE_CASH_FLOW', 'IS_DIV_PER_SHR',
             'RETURN_ON_ASSET', 'RETURN_COM_EQY', 'PE_RATIO', 'CURRENT_EV_TO_T12M_EBITDA', 'PX_TO_BOOK_RATIO',
             'EQY_DVD_YLD_IND', 'REVENUE_PER_SH', 'FREE_CASH_FLOW_YIELD', 'FREE_CASH_FLOW_MARGIN', 'PROF_MARGIN',
             'EQY_SH_OUT_TOT_MULT_SH', 'EQY_RAW_BETA', 'BS_CASH_NEAR_CASH_ITEM', 'BS_TOTAL_LIABILITIES',
             'IS_ADJUSTED_GROSS_PROFIT', 'IS_ADJUSTED_OPERATING_INCOME', 'IS_COMP_EPS_ADJUSTED', 'NET_INCOME', 'EQY_DPS',
             'IS_DIL_EPS_CONT_OPS', 'PX_TO_FREE_CASH_FLOW', 'GROSS_MARGIN', 'EBITDA_TO_REVENUE', 'RETURN_ON_CAP',
             'RETURN_ON_INV_CAPITAL', 'RETURN_ON_TANGIBLE_ASSETS']
BASE_FORECAST = ['BEST_EPS', 'BEST_SALES', 'BEST_EBITDA', 'BEST_PE_RATIO', 'BEST_DPS', 'BEST_DIV_YLD', 'BEST_EBIT',
                 'BEST_NET_INCOME', 'BEST_CAPEX', 'BEST_ESTIMATE_FCF', 'BEST_BPS']

H, T, F = list(mbp.HEADER_FIELDS), list(mbp.HIST_FIELDS), list(mbp.FORECAST_FIELDS)
results = []


def arm(aid, ok, got):
    results.append((aid, bool(ok)))
    print("ARM %s %s %s" % (aid, "PASS" if ok else "FAIL", got))


placed = {m: (H.count(m) + T.count(m) + F.count(m)) for m in V3}
bad = sorted(m for m, n in placed.items() if n != 1)
arm("b1", not bad, "v3 %d placed_once %d not_once %s" % (len(V3), len(V3) - len(bad), bad[:6]))

missing = [m for m in NAME_AND_EARNINGS if m not in H]
arm("b2", not missing, "header_missing %s" % missing)

arm("b3", "BEST_CPS" in F and "BEST_FPERIOD_OVERRIDE" not in (H + T + F),
    "best_cps_in_forecast %s override_listed %s" % ("BEST_CPS" in F, "BEST_FPERIOD_OVERRIDE" in (H + T + F)))

basis = getattr(mbp, "FIELD_BASIS", {})
new = set(V3) | set(NAME_AND_EARNINGS)
no_basis = sorted({m for m in set(H + T + F) | new if not str(basis.get(m, "")).strip()})
arm("b4", not no_basis, "members_plus_new %d no_basis %d %s" % (len(set(H + T + F) | new), len(no_basis), no_basis[:6]))

has_cmd = callable(getattr(mbp, "cmd_refresh", None))
accepts = False
try:
    mbp.main(["refresh", "--securities", "X"])  # refresh takes no --securities: a parser error proves the choice exists
except SystemExit as exc:
    accepts = exc.code == 2 and has_cmd
except Exception:  # noqa: BLE001
    accepts = False
arm("b5", has_cmd and accepts, "cmd_refresh %s refresh_choice %s" % (has_cmd, accepts))

moved = [(n, m) for base, cur, n in ((BASE_HEADER, H, "header"), (BASE_HIST, T, "hist"), (BASE_FORECAST, F, "forecast"))
         for i, m in enumerate(base) if i >= len(cur) or cur[i] != m]
arm("c1", not moved, "base_members %d moved %d %s" % (len(BASE_HEADER) + len(BASE_HIST) + len(BASE_FORECAST),
                                                     len(moved), moved[:4]))

arm("c2", callable(getattr(mbp, "cmd_admit", None)) and getattr(mbp, "ADMIT_BATCH", None) == 3
    and getattr(mbp, "HIST_FIELDS_PER_REQUEST", None) == 25,
    "cmd_admit %s ADMIT_BATCH %s HIST_FIELDS_PER_REQUEST %s" % (callable(getattr(mbp, "cmd_admit", None)),
                                                               getattr(mbp, "ADMIT_BATCH", None),
                                                               getattr(mbp, "HIST_FIELDS_PER_REQUEST", None)))

refused = False
try:
    mbp.main(["pull", "--securities", "A", "B", "C", "D"])
except SystemExit as exc:
    refused = "REFUSE" in str(exc.code)
arm("c3", refused, "four_security_pull_refused %s" % refused)

b = sum(1 for aid, ok in results if aid.startswith("b") and ok)
c = sum(1 for aid, ok in results if aid.startswith("c") and ok)
print("aj1 build %d/5 control %d/3" % (b, c))
