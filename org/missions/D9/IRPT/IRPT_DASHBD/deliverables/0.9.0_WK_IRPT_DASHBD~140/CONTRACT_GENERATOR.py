"""Generate the round-94 performance report contract and its gap table (DB-b-174, 0.9.0_WK_IRPT_DASHBD~140).

Usage: python -I gen_contract.py <repo_root> <contract_out> <gap_out>
Writes the contract bytes first, then binds the gap table to their sha256.
Counts in the gap table are computed from the members, never typed.
"""
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
CONTRACT_OUT = Path(sys.argv[2])
GAP_OUT = Path(sys.argv[3])

SO = "org/standards/"
AAD = SO + "IRPT_DASHBD_ACCOUNT_ACTIVITY_DAILY_CONTRACT.json"
ARD = SO + "IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
ACD = SO + "IRPT_DASHBD_ACCOUNT_CLASS_DAILY_CONTRACT.json"
LR = SO + "IRPT_DASHBD_ACCOUNT_LOT_REALIZED_CONTRACT.json"
LU = SO + "IRPT_DASHBD_ACCOUNT_LOT_UNREALIZED_DAILY_CONTRACT.json"
CS = SO + "IRPT_DASHBD_CLIENT_SUMMARY_CONTRACT.json"
DIM = SO + "IRPT_DASHBD_DIM_RETURN_METHOD_CONTRACT.json"
SER = SO + "IRPT_DASHBD_SERIES_CONTRACT.json"
SIBLINGS = [AAD, ARD, ACD, LR, LU, CS, DIM, SER]

SECTIONS = [
    {"id": "cover", "title": "Cover", "grain": "household"},
    {"id": "portfolio_overview", "title": "Portfolio Overview", "grain": "household"},
    {"id": "summary_of_portfolio_accounts", "title": "Summary of Portfolio Accounts", "grain": "household and each account"},
    {"id": "holdings_overview", "title": "Holdings Overview", "grain": "household, by class"},
    {"id": "taxable_realized_gain_loss_ytd", "title": "Taxable Realized Gain/Loss Summary, Year To Date", "grain": "account (taxable accounts with realized activity)"},
    {"id": "account_overview", "title": "Account Overview", "grain": "account"},
    {"id": "gain_loss_review_by_account", "title": "Gain/Loss Review by Account, Last 12 Months", "grain": "account, by class"},
    {"id": "disclosure", "title": "Disclosure page", "grain": "not in the baseline export"},
]

# ---- reasons (words only; ABSENT carries no value) ----
R_HH_RETURN = ("A household-grain return is not carried by any sibling contract. Returns do not add across accounts, so the household figure "
               "cannot be folded from the account returns, and no sibling defines a household daily return series. It would come from a household "
               "daily return series built the way the account series is built, as a new contract. The account rows carry each account's own return.")
R_BENCH = ("Opal holds no benchmark return series. None of the sibling contracts carries the four model benchmark returns. It would come from a "
           "benchmark return series contract that does not exist yet; until it does, the cell prints this reason in words and no figure.")
R_MTD = ("Month to date is not a ruled period. The client summary carries quarter to date, year to date, last 12 months and since inception only "
         "(its windows are YTD, QTD, 1Y and SI), and the ruled periods are QTD, YTD, 1Y and SI. The daily terms exist, so a month-to-date window "
         "needs a ruling before a sibling carries it.")
R_HH_NAME = ("The client summary carries ids only, by design: no name and no custodian account number. No sibling holds the household's display name. "
             "It would come from the household's directory entry, which is outside these contracts.")
R_ACCT_LIST = ("The account list needs each account's registration name, and no sibling holds it. The account tables carry the custodian account id, "
               "so the last four digits can be shown once a registration-name source exists. The client summary holds only issued opaque account ids, "
               "which no sibling maps to the custodian id (see open_changes).")
R_OVERVIEW_LINE = ("The household performance line needs a household daily return series, which no sibling carries (household return rule), and the four "
                   "benchmark lines, which no sibling carries (benchmark rule). Each account's own performance line is served from its series object.")
R_DISCLOSURE = ("The baseline export does not include the disclosure page, and no sibling holds its text. The method row carries the GIPS-alignment "
                "statement (the dim_return_method gips_alignment field) that the page will quote; the rest of the text needs its own source.")

WIN = [
    # key, column name in the baseline, label words, client summary key, fold words
    ("qtd", "Quarter To Date", "quarter to date", "QTD",
     "from its opening anchor (the last trading day before the first calendar day of the quarter) to as_of"),
    ("ytd", "Year To Date", "year to date", "YTD",
     "from its opening anchor (the last trading day before 1 January of as_of's year) to as_of"),
    ("last_12_months", "Last 12 Months", "last 12 months", "1Y",
     "from its opening anchor (the last trading day before the calendar day one year before as_of) to as_of"),
    ("since_inception", "Since <inception>", "since inception", "SI",
     "from the account's first_data_date to as_of"),
]
WIN_MTD = ("month_to_date", "Month To Date", "month to date", None,
           "from its opening anchor (the last trading day before the first calendar day of as_of's month) to as_of")

VS_ROWS = [
    ("beginning_value", "Beginning Value"),
    ("net_additions", "Net Additions"),
    ("net_gain", "Net Gain (the baseline footnote says it includes fees)"),
    ("ending_value", "Ending Value"),
    ("return_cumulative", "Return (Cumulative)"),
    ("benchmark_ultra_short_term", "Benchmark: Ultra-Short Term Return (Cumulative)"),
    ("benchmark_short_term", "Benchmark: Short-Term Return (Cumulative)"),
    ("benchmark_intermediate_term", "Benchmark: Intermediate-Term Return (Cumulative)"),
    ("benchmark_long_term", "Benchmark: Long-Term Return (Cumulative)"),
]

members = []


def src(contract, field, fold, also=None):
    d = {"contract": contract, "field": field, "fold": fold}
    if also:
        d["also"] = also
    return d


def absent(reason):
    return {"absent": True, "reason": reason}


def add(mid, section, baseline, label, unit, source):
    m = {"id": mid, "section": section, "baseline": baseline, "label": label, "unit": unit}
    if isinstance(source, dict) and source.get("absent"):
        m["source"] = "ABSENT"
        m["reason"] = source["reason"]
    else:
        m["source"] = source
    members.append(m)


def scope_phrase(scope):
    return "the household's accounts" if scope == "household" else "this account"


def vs_block(scope, section, sec_name, table):
    """Portfolio Value Summary (household) or Account Value Summary (account)."""
    for key, colname, wlabel, cs_key, wfold in WIN:
        for row, rowname in VS_ROWS:
            mid = "%s.%s.%s" % ("pvs" if scope == "household" else "avs", key, row)
            base = "section %s %s, table %s, column %s, row %s" % (
                "1 Portfolio Overview" if scope == "household" else "5 Account Overview", sec_name, table, colname, rowname)
            if row == "beginning_value":
                if scope == "household":
                    fold_b = ("sum over the household's accounts of beginning_value on the window's opening anchor day; a household sum is absent "
                              "when any account term is absent; an account whose anchor day carries NO_PRIOR_VALUE makes the sum absent, never zero")
                else:
                    fold_b = ("beginning_value on the window's opening anchor day for this account; absent where that day carries NO_PRIOR_VALUE, "
                              "never zero")
                s = src(AAD, "beginning_value", fold_b)
                lab = "Beginning value, %s" % wlabel
                add(mid, section, base, lab, "dollars", s)
            elif row == "net_additions":
                if scope == "household":
                    fold = "contributions minus withdrawals, summed over the household's accounts across the window's trading days (%s)" % WIN_FOLD_TEXT(wfold)
                else:
                    fold = "contributions minus withdrawals over the window's trading days (%s)" % WIN_FOLD_TEXT(wfold)
                add(mid, section, base, "Net additions, %s" % wlabel, "dollars",
                    src(AAD, "contributions", fold, also=["withdrawals"]))
            elif row == "net_gain":
                if scope == "household":
                    fold = "realized plus unrealized_change plus income, summed over the household's accounts across the window's trading days (%s); before advisory fees, and income is net of fee and administration cash (see convention.fee_basis_label)" % WIN_FOLD_TEXT(wfold)
                else:
                    fold = "realized plus unrealized_change plus income over the window's trading days (%s); before advisory fees, and income is net of fee and administration cash (see convention.fee_basis_label)" % WIN_FOLD_TEXT(wfold)
                add(mid, section, base, "Net gain before advisory fees, %s" % wlabel, "dollars",
                    src(AAD, "realized", fold, also=["unrealized_change", "income"]))
            elif row == "ending_value":
                if scope == "household":
                    fold = "ending_value on as_of, summed over the household's accounts; the same figure in every window column"
                else:
                    fold = "ending_value on as_of for this account; the same figure in every window column"
                add(mid, section, base, "Ending value (as of the report date)", "dollars",
                    src(AAD, "ending_value", fold))
            elif row == "return_cumulative":
                if scope == "household":
                    add(mid, section, base, "Return, cumulative, before advisory fees, %s" % wlabel, "percent",
                        absent(R_HH_RETURN))
                else:
                    add(mid, section, base, "Return, cumulative, before advisory fees, %s" % wlabel, "percent",
                        src(CS, "windows",
                            "the account entry's windows[%s], the geometric link of the account's daily total return over the window (%s); null, and so absent, where window_status[%s] is NOT_SPANNED or BREAK, never a partial link; cumulative, not annualized" % (
                                cs_key, WIN_FOLD_TEXT(wfold), cs_key),
                            also=["window_status"]))
            else:
                bname = row.replace("benchmark_", "").replace("_", " ")
                add(mid, section, base, "Opal model benchmark, %s, cumulative, %s" % (bname, wlabel), "percent", absent(R_BENCH))


def WIN_FOLD_TEXT(wfold):
    return wfold


def act_block():
    cols = [("beginning_value", "Beginning Value"), ("contributions", "Contributions"), ("withdrawals", "Withdrawals"),
            ("net_gain", "Net Gain *"), ("income", "Income"), ("ending_value", "Ending Value")]
    for row in ("household", "account"):
        for col, colname in cols:
            mid = "act.%s.%s" % (col, row)
            base = "section 2 Summary of Portfolio Accounts, table Activity Summary Last 12 Months, column %s, row %s" % (
                colname, "household" if row == "household" else "each account")
            if row == "household":
                who = "the household's accounts"
            else:
                who = "this account"
            if col == "beginning_value":
                add(mid, "summary_of_portfolio_accounts", base, "Beginning value, last 12 months (%s)" % row, "dollars",
                    src(AAD, "beginning_value", "beginning_value on the last-12-months opening anchor day, %s%s" % (
                        "summed over the household's accounts; absent when any account term is absent" if row == "household" else "for this account", "")))
            elif col == "contributions":
                add(mid, "summary_of_portfolio_accounts", base, "Contributions, last 12 months (%s)" % row, "dollars",
                    src(AAD, "contributions", "sum over %s of the daily contributions across the last-12-months trading days" % who))
            elif col == "withdrawals":
                add(mid, "summary_of_portfolio_accounts", base, "Withdrawals, last 12 months (%s)" % row, "dollars",
                    src(AAD, "withdrawals", "sum over %s of the daily withdrawals (shown as a non-negative amount) across the last-12-months trading days" % who))
            elif col == "net_gain":
                add(mid, "summary_of_portfolio_accounts", base, "Net gain before advisory fees, last 12 months (%s)" % row, "dollars",
                    src(AAD, "realized", "sum over %s of realized plus unrealized_change plus income across the last-12-months trading days; before advisory fees (see convention.fee_basis_label)" % who,
                        also=["unrealized_change", "income"]))
            elif col == "income":
                add(mid, "summary_of_portfolio_accounts", base, "Income recognised on cash receipt, net of fee and administration cash, last 12 months (%s)" % row, "dollars",
                    src(AAD, "income", "sum over %s of income across the last-12-months trading days; income is recognised on cash receipt and is net of fee and administration cash and of withheld tax" % who))
            else:
                add(mid, "summary_of_portfolio_accounts", base, "Ending value, last 12 months end (%s)" % row, "dollars",
                    src(AAD, "ending_value", "ending_value on as_of, %s; cash included" % ("summed over the household's accounts" if row == "household" else "for this account")))


def holdings_block():
    base_tab = "section 3 Holdings Overview, table Holdings Overview, column %s, row household total"
    add("hold.ending_value", "holdings_overview", base_tab % "Ending Value", "Ending value of the household (as of the report date)", "dollars",
        src(AAD, "ending_value", "sum over the household's accounts of ending_value on as_of, cash included"))
    add("hold.allocation", "holdings_overview", base_tab % "Allocation", "Allocation, each asset class's share of household ending value", "percent",
        src(ACD, "market_value_eod", "each asset class's market_value_eod as a share of the household ending value on as_of; the household total is 100 percent; sub-class shares are not carried (see holdings.rows.class_hierarchy)"))
    wins = [("last_12_months", "Last 12 Months"), ("ytd", "Year To Date"), ("qtd", "Quarter To Date"), ("mtd", "Month To Date"), ("since_inception", "Since <inception>")]
    fold_of = {"last_12_months": WIN[2][4], "ytd": WIN[1][4], "qtd": WIN[0][4], "since_inception": WIN[3][4], "mtd": WIN_MTD[4]}
    lab_of = {"last_12_months": "last 12 months", "ytd": "year to date", "qtd": "quarter to date", "mtd": "month to date", "since_inception": "since inception"}
    for w, colname in wins:
        mid_n = "hold.net_gain_%s" % w
        base_n = base_tab % ("Net Gain / " + colname)
        if w == "mtd":
            add(mid_n, "holdings_overview", base_n, "Net gain before advisory fees, month to date", "dollars", absent(R_MTD))
        else:
            add(mid_n, "holdings_overview", base_n, "Net gain before advisory fees, %s" % lab_of[w], "dollars",
                src(AAD, "realized", "sum over the household's accounts of realized plus unrealized_change plus income across the window's trading days (%s); before advisory fees (see convention.fee_basis_label)" % fold_of[w], also=["unrealized_change", "income"]))
        mid_r = "hold.return_%s" % w
        base_r = base_tab % ("Return / " + colname)
        if w == "mtd":
            add(mid_r, "holdings_overview", base_r, "Return before advisory fees, month to date (household)", "percent",
                absent(R_HH_RETURN + " Month to date is also not a ruled period, so its household return waits on the same ruling as its net gain."))
        else:
            add(mid_r, "holdings_overview", base_r, "Return before advisory fees, %s (household)" % lab_of[w], "percent", absent(R_HH_RETURN))


def trgl_block():
    base = "section 4 Taxable Realized Gain/Loss Summary, Year To Date, column %s (per taxable account with realized activity)"
    fold = "sum over the lots of this account closed in the year to date (closing date on or after 1 January of as_of's year)"
    add("trgl.cost_basis", "taxable_realized_gain_loss_ytd", base % "Cost Basis", "Cost basis of lots closed, year to date", "dollars",
        src(LR, "cost_basis", fold + "; cost_basis as basis_source says"))
    add("trgl.proceeds", "taxable_realized_gain_loss_ytd", base % "Proceeds", "Proceeds of lots closed, year to date", "dollars",
        src(LR, "proceeds", fold + "; proceeds net of the trade's fees"))
    add("trgl.realized_short_term", "taxable_realized_gain_loss_ytd", base % "Realized ST", "Realized gain or loss, short-term, year to date", "dollars",
        src(LR, "realized_gain", fold + " whose holding_term reads short-term", also=["holding_term"]))
    add("trgl.realized_long_term", "taxable_realized_gain_loss_ytd", base % "Realized LT", "Realized gain or loss, long-term, year to date", "dollars",
        src(LR, "realized_gain", fold + " whose holding_term reads long-term", also=["holding_term"]))
    add("trgl.total_realized_gl", "taxable_realized_gain_loss_ytd", base % "Total RGL", "Total realized gain or loss, year to date", "dollars",
        src(LR, "realized_gain", fold + ", short-term and long-term together"))


def glr_block():
    base = "section 6 Gain/Loss Review by Account, Last 12 Months, column %s, row account total"
    add("glr.cost_basis", "gain_loss_review_by_account", base % "Cost Basis", "Cost basis of open lots, account total", "dollars",
        src(LU, "cost_basis", "sum over this account's open lots on as_of of cost_basis, as basis_source says"))
    add("glr.ending_value", "gain_loss_review_by_account", base % "Ending Value", "Ending value of the account, cash included", "dollars",
        src(AAD, "ending_value", "ending_value on as_of for this account"))
    add("glr.total_realized_gl", "gain_loss_review_by_account", base % "Total RGL", "Total realized gain or loss, last 12 months", "dollars",
        src(LR, "realized_gain", "sum over this account's lots closed in the last 12 months of realized_gain"))
    add("glr.total_unrealized_gl", "gain_loss_review_by_account", base % "Total UGL", "Total unrealized gain or loss on open lots", "dollars",
        src(LU, "unrealized_gain", "sum over this account's open lots on as_of of unrealized_gain"))


def extra_block():
    add("cover.household_name", "cover", "section 0 Cover, household name line", "Household name", "text", absent(R_HH_NAME))
    add("cover.account_list", "cover", "section 0 Cover, Accounts list, each as registration name then masked number",
        "Accounts, each with its registration name and last four digits", "text", absent(R_ACCT_LIST))
    add("cover.as_of_date", "cover", "section 0 Cover, As of line", "As of date", "text",
        src(CS, "as_of", "the newest as_of among the account entries, as YYYY-MM-DD"))
    add("overview.chart.allocation_by_asset_class", "portfolio_overview", "section 1(a) chart Allocation by Asset Class (household)",
        "Allocation by asset class (household)", "series",
        src(ACD, "market_value_eod", "each asset class's share of household market value on each day, by Opal's asset-class enumeration; sub-class segments are not carried (see document.row_dimensions.class_hierarchy)"))
    add("overview.chart.portfolio_performance_last_12_months", "portfolio_overview", "section 1(b) chart Portfolio Performance Last 12 Months (household, portfolio line and four benchmark lines)",
        "Household performance, last 12 months, with benchmark lines", "series", absent(R_OVERVIEW_LINE))
    add("accounts.chart.allocation_by_account", "summary_of_portfolio_accounts", "section 2(a) chart Allocation by Account (household)",
        "Allocation by account (household)", "series",
        src(AAD, "ending_value", "each account's share of the household ending_value on each day, by account_id"))
    add("accounts.chart.ending_value_and_net_additions_last_12_months", "summary_of_portfolio_accounts",
        "section 2(b) chart Ending Value and Net Additions Last 12 Months (household)",
        "Ending value and net additions, last 12 months (household)", "series",
        src(AAD, "ending_value", "daily ending_value summed over the household's accounts across the last 12 months; net additions is contributions minus withdrawals summed the same way", also=["contributions", "withdrawals"]))
    add("holdings.rows.class_hierarchy", "holdings_overview", "section 3 Holdings Overview, row labels: class, then sub-class (the baseline's class hierarchy)",
        "Class rows, then sub-class rows", "text",
        src(ACD, "asset_class", "class level only: Opal's asset-class enumeration (seven values, unclassified included) from account_class_daily; the baseline's sub-class rows are not carried, so the sub-class cell of each row is absent with its reason (see document.row_dimensions.class_hierarchy)"))
    add("convention.fee_basis_label", "portfolio_overview", "section 1 and section 5 footnote: '*Net Gain includes Fees' and the conventions note",
        "Returns and gains are before advisory fees. The baseline's Net Gain includes fees, so the two are not the same figure. Income is net of fee and administration cash and of withheld tax.",
        "text", src(DIM, "fee_basis", "the served fee basis is GROSS_ONLY (returns and gains are gross of advisory fees); the label words print beside every Opal return and gain column and beside every baseline Net Gain column"))
    add("convention.inception_per_household_and_account", "portfolio_overview", "section 1 and section 5 column heading 'Since <inception date>' and the conventions note",
        "Since-inception column is headed with that household's or that account's inception date", "text",
        src(CS, "first_data_date", "per account: the account's first_data_date; per household: the earliest first_data_date among its accounts; never a firm-wide date"))
    add("convention.not_held_for_entire_period", "portfolio_overview", "section 1 and section 5 footnote: 'Not held for the entire period'",
        "Footnote: not held for the entire period (a window the account did not span prints a dash with this footnote)", "text",
        src(CS, "window_status", "a window whose window_status is NOT_SPANNED for an account prints the dash and this footnote in place of a figure"))
    add("disclosure.page", "disclosure", "disclosure page (not in the baseline export): every page says the report is incomplete without it",
        "Disclosure page", "text", absent(R_DISCLOSURE))


# build in checker order
vs_block("household", "portfolio_overview", "Portfolio Value Summary", "Portfolio Value Summary")
act_block()
holdings_block()
trgl_block()
vs_block("account", "account_overview", "Account Value Summary", "Account Value Summary")
glr_block()
extra_block()

# ---- the document ----
DOCUMENT = {
    "shape": ("One filled report per household. A filled report is one JSON object with: household {household_ref, as_of, accounts (one entry per "
              "account of the household, in account_id order)}; windows (the five windows below, each with its start rule); values, an object keyed by "
              "member id with exactly one entry per member in members; rows, the variable rows (one per account, and the class rows under each account "
              "and under the household). A value is a number, a text, or {\"absent\": \"<reason in words>\"}. A member whose source is ABSENT always "
              "holds the absent form, never zero and never a default. Units follow each member's unit: dollars as whole dollars with thousands "
              "separators; percent from the decimal fraction to one decimal place; text as written; series as the list the chart reads. The sample builder "
              "writes this object from the sibling contracts named in each member's source; the tab and the export read it by member id and print every "
              "absent form as its words. Neither the tab nor the export derives a figure from another source."),
    "row_dimensions": {
        "account": {
            "order": "the household's accounts in account_id order; one row per account, labelled with its registration name and last four digits (the registration name is absent, so the label carries the absent form until a name source exists)",
            "sources": {"account_id": "account_activity_daily account_id (custodian account form)"},
            "grain": "account"
        },
        "class_hierarchy": {
            "levels": ["class", "sub_class"],
            "class_level": "Opal's asset-class enumeration from account_class_daily asset_class (seven values: cash, fixed_income, equity, structured, alternatives, commodities, unclassified), in the baseline's printed class order where a baseline class has an Opal counterpart",
            "sub_class_level": "ABSENT. The baseline's sub-class rows (for example the large-cap, mid-cap, international, municipal and high-yield rows) are not carried by any sibling; each sub-class cell holds the absent form with the reason in words. A class with no holding prints a dash, which is an absent form, never zero.",
            "grain": "household by class (holdings overview) and account by class (gain/loss review)"
        }
    },
    "windows": {
        "quarter_to_date": {"column": "Quarter To Date", "start_rule": "the first calendar day of the calendar quarter containing as_of (1 January, 1 April, 1 July or 1 October)", "opening_anchor": "the last trading day before the start day, from lib/trading_calendar.py", "client_summary_key": "QTD"},
        "year_to_date": {"column": "Year To Date", "start_rule": "1 January of as_of's year", "opening_anchor": "the last trading day before 1 January, from lib/trading_calendar.py", "client_summary_key": "YTD"},
        "last_12_months": {"column": "Last 12 Months", "start_rule": "the calendar day one year before as_of", "opening_anchor": "the last trading day before that calendar day, from lib/trading_calendar.py", "client_summary_key": "1Y"},
        "month_to_date": {"column": "Month To Date", "start_rule": "the first calendar day of as_of's month", "opening_anchor": "the last trading day before that day, from lib/trading_calendar.py", "client_summary_key": None, "served": False, "reason": "not a ruled period: no sibling carries it; the month-to-date members are absent"},
        "since_inception": {"column": "Since <inception>", "start_rule": "the account's first_data_date (the household's inception is the earliest first_data_date among its accounts)", "opening_anchor": "none: the window opens on first_data_date", "client_summary_key": "SI", "annualization": "the baseline annualizes since inception past one year; the served since-inception return is cumulative and is printed as cumulative; annualization is not in any sibling"}
    },
    "household_sum_rule": "a household figure built by summing accounts is absent when any contributing account term is absent; a partial sum is never printed as the household figure",
    "footnotes": {
        "not_held_for_entire_period": "a window whose figure is absent because the account did not span it (window_status NOT_SPANNED) prints a dash with the footnote 'Not held for the entire period' in place of the figure (member convention.not_held_for_entire_period)",
        "inception_per_household_and_account": "the since-inception column is headed with the inception date of that household or that account (member convention.inception_per_household_and_account)",
        "fee_basis": "the fee-basis words in convention.fee_basis_label print beside every Opal return and gain column and beside every baseline Net Gain column, so the two are never silently matched"
    },
    "section_order": [s["id"] for s in SECTIONS],
    "absent_rule": "ABSENT is never zero. A member with source ABSENT carries {\"absent\": reason} in values and prints the reason in words; a window with no measured figure prints its absent form, and a window the account did not span prints the not-held dash"
}

CONTRACT = {
    "contract_version": "0.1.0",
    "project": "IRPT_DASHBD",
    "prd": "org/missions/D9/IRPT/IRPT_DASHBD/prd/IRPT_DASHBD_PRD.md",
    "prd_contracts": ["C-SERVE", "C-SEAM", "C-LABEL", "C-HONESTY"],
    "writer": "the sample builder (IRPT_DASHBD.TO-DB-b-175, 0.9.0_WK_IRPT_DASHBD~141) writes filled values keyed by member id, from the sibling contracts each member's source names; no other writer",
    "reader": "the Performance tab (IRPT_DASHBD.TO-DB-b-176) and the export document (IRPT_DASHBD.TO-DB-b-177), both in the section order below; neither derives a figure from another source",
    "authored_by": "0.9.0_WK_IRPT_DASHBD~140",
    "authored_under": "IRPT_DASHBD.TO-DB-b-174 under round 94 (ROUND-94 ANALYSIS item 1, PRD v0.14, FWD-21). The report's structure is read from the round-94 baseline structure note, which is held outside the repo's contract set and names the report only by its structure. Vendor-agnostic: the report is one Opal Shape, and the baseline is named only as 'the baseline'.",
    "siblings": list(SIBLINGS),
    "vendor_agnostic": "nothing in this file names a vendor or a custodian; a member's label is the report's own words, never a sibling's field name",
    "sections": SECTIONS,
    "document": DOCUMENT,
    "members": members,
    "change_rule": "a member whose source changes names the new field in the sibling's own versioned edit; a derivation the siblings do not carry (a household return series, a benchmark series, a month-to-date window, the registration name, the disclosure text) is a new field or a new contract before this contract sources it, and the contract changes by a version bump with the gap table re-bound to its bytes",
    "read_rule": "values are read by member id; an ABSENT member prints its reason in words; a figure is never derived from a source this contract does not name; the fee-basis words print beside every Opal return and gain figure and every baseline Net Gain figure",
    "open_changes": [
        "the household return series and the household daily return: a new contract (household return rule); until then the household return members are ABSENT",
        "the four model benchmark return series: a new contract (benchmark rule); until then the benchmark members are ABSENT",
        "month to date: a ruling is needed before a sibling carries it; until then the month-to-date members are ABSENT",
        "the registration names and the disclosure text: no sibling holds them; the cover, account rows and disclosure page print absent forms",
        "the since-inception convention: the baseline's conventions note says since inception is annualized past one year, while its Portfolio Value Summary row reads Return (Cumulative); the served figure is cumulative and is printed as cumulative until a ruling says otherwise",
        "the account id spaces: the client summary holds issued opaque account ids, while the account tables key on the custodian account id; no sibling maps one to the other, so the masked account number on the cover cannot come from the summary alone"
    ]
}


def main():
    raw = (json.dumps(CONTRACT, indent=2, ensure_ascii=True) + "\n").encode("ascii")
    CONTRACT_OUT.write_bytes(raw)
    sha = hashlib.sha256(raw).hexdigest()
    n = len(members)
    absent_n = sum(1 for m in members if m["source"] == "ABSENT")
    by_sec = {}
    for s in SECTIONS:
        ms = [m for m in members if m["section"] == s["id"]]
        a = sum(1 for m in ms if m["source"] == "ABSENT")
        by_sec[s["id"]] = {"members": len(ms), "sourced": len(ms) - a, "absent": a}
    gap = {
        "contract_sha256": sha,
        "totals": {"members": n, "sourced": n - absent_n, "absent": absent_n},
        "by_section": by_sec,
        "vendor_free": True,
        "baseline_cells_required": n,
        "fwd20_map_folded": True,
        "sibling_contracts_read": list(SIBLINGS),
        "reads": {"vendor_calls": 0, "s3_reads": 0, "s3_writes": 0, "secret_reads": 0},
        "served_values_changed": False,
    }
    GAP_OUT.write_bytes((json.dumps(gap, indent=2, ensure_ascii=True) + "\n").encode("ascii"))
    print("members %d sourced %d absent %d sha256_prefix_bytes %d" % (n, n - absent_n, absent_n, len(raw)))
    for k, v in by_sec.items():
        print(k, v)


if __name__ == "__main__":
    main()
