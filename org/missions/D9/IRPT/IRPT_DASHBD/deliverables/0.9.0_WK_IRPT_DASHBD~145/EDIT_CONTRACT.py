"""DB-b-179 (TO IRPT_DASHBD.TO-DB-b-179, worker 0.9.0_WK_IRPT_DASHBD~145): re-source the 36 window members of the
performance report contract to account_return_daily; version 0.2.0 with the 0.1.0 bytes in lineage.

Run: python -I <this file> <repo_root>. Changes ONLY: contract_version, a new lineage key, and the source of the 36 members.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
CONTRACT = ROOT / "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
RET = "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
V010_SHA = "53fce40546882c90b634decb91ec5176a54ddf3c3b4622270bfc5cc35f66991b"
WINDOWS = ("qtd", "ytd", "last_12_months", "since_inception")

SPAN = {
    "qtd": "the quarter to date window: the trading days after its opening anchor (the last trading day before the first day of the calendar quarter containing as_of) up to and including as_of",
    "ytd": "the year to date window: the trading days after its opening anchor (the last trading day before 1 January of as_of's year) up to and including as_of",
    "last_12_months": "the last 12 months window: the trading days after its opening anchor (the last trading day before the calendar day one year before as_of) up to and including as_of",
    "since_inception": "the since-inception window: the trading days after the account's first valued day up to and including as_of",
}
ANCHOR = {
    "qtd": "the window's opening anchor day (the last trading day before the first day of the calendar quarter containing as_of)",
    "ytd": "the window's opening anchor day (the last trading day before 1 January of as_of's year)",
    "last_12_months": "the window's opening anchor day (the last trading day before the calendar day one year before as_of)",
    "since_inception": "the account's first valued day (its first emitted account_return_daily row, the first day its market_value_eod exists)",
}
NOT_SPANNED = ("an account with no row on its anchor day did not hold a value at the window's start: its term is absent, never zero, "
               "and its window is NOT_SPANNED, so it prints the not-held dash")
FEE = "a gain BEFORE advisory fees (convention.fee_basis_label: the baseline's Net Gain includes fees, so the two are not the same figure)"


def account_fold(w, row):
    if row == "beginning_value":
        return ("market_value_eod of this account on " + ANCHOR[w] + ", the whole-account value at end of day with cash included; "
                + NOT_SPANNED + "; absent, never zero, when that row's day_quality is SOURCE_LAG")
    if row == "ending_value":
        return ("market_value_eod of this account on as_of, the whole-account value at end of day with cash included; absent, never zero, "
                "when there is no row on as_of or as_of's day_quality is SOURCE_LAG")
    if row == "net_additions":
        return ("the sum of external_flow (net external flow, capital-in positive) over this account's rows for " + SPAN[w] + "; each row's carried_days "
                "already folds the flows of a skipped closure into its trading day, so every flow is counted once; absent when any trading day of the window "
                "has no row for this account or a row there is SOURCE_LAG (that day's flow is unknown), never zero")
    if row == "net_gain":
        return ("ending_value minus beginning_value minus net_additions for this account, the three terms above read from the same rows: " + FEE
                + "; absent when any of the three terms is absent; it is a residual and is never plugged to tie")
    if row == "return_cumulative":
        return ("the account's cumulative return over " + SPAN[w] + ": the product of (1 + total_return_daily) over the window's trading days, minus 1, "
                "read from this account's rows. Guard and day rules: a row whose total_return_daily is null (day_quality NOT_MEASURABLE or SOURCE_LAG, "
                "where the geometric link breaks) makes the window ABSENT with the gap date named, never bridged; a row whose guard_state is "
                "GRADED_DISAGREED serves no number (ruling 17), so the window is ABSENT; a row whose day_quality is FLOW_UNRECONCILED or LARGE_FLOW, or whose "
                "guard_state is NOT_GRADED_OUTSIDE_DOMAIN, NOT_GRADED_NO_NEIGHBOUR or GUARD_NOT_REACHED, compounds as served and the window carries that "
                "flag. An account with no row on its anchor day is NOT_SPANNED: its term is absent, its window prints the not-held dash, and its figure "
                "is never a compounding over the part it held")
    raise KeyError(row)


def household_fold(w, row):
    if row == "net_gain":
        return ("sum over the household's accounts of each account's ending_value minus beginning_value minus net_additions over " + SPAN[w] + "; "
                + FEE + "; absent when any account term is absent (document.household_sum_rule), never a partial sum")
    head = "sum over the household's accounts of " + account_fold(w, row)
    return head + "; a household sum is absent when any account term is absent (document.household_sum_rule), never a partial sum"


FIELD = {"beginning_value": "market_value_eod", "ending_value": "market_value_eod", "net_additions": "external_flow",
         "net_gain": "market_value_eod", "return_cumulative": "total_return_daily"}


def plan():
    out = {}
    for w in WINDOWS:
        for r in ("beginning_value", "ending_value", "net_additions", "net_gain"):
            out["pvs.%s.%s" % (w, r)] = {"contract": RET, "field": FIELD[r], "fold": household_fold(w, r)}
            out["avs.%s.%s" % (w, r)] = {"contract": RET, "field": FIELD[r], "fold": account_fold(w, r)}
        out["avs.%s.return_cumulative" % w] = {"contract": RET, "field": FIELD["return_cumulative"], "fold": account_fold(w, "return_cumulative")}
    return out


def counts(members):
    src = sum(1 for m in members if m["source"] != "ABSENT")
    return src, len(members) - src


def main():
    raw = CONTRACT.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == V010_SHA, "base bytes are not the 0.1.0 contract"
    c = json.loads(raw.decode("utf-8"))
    assert c["contract_version"] == "0.1.0" and "lineage" not in c
    new_plan = plan()
    assert len(new_plan) == 36, len(new_plan)
    members = c["members"]
    before = counts(members)
    hit = []
    for m in members:
        if m["id"] in new_plan:
            assert m["source"] != "ABSENT", m["id"]
            m["source"] = new_plan[m["id"]]
            hit.append(m["id"])
    assert sorted(hit) == sorted(new_plan), "not all 36 found"
    after = counts(members)
    out = {}
    for k, v in c.items():
        if k == "contract_version":
            out["contract_version"] = "0.2.0"
            out["lineage"] = [{"contract_version": "0.1.0", "sha256": V010_SHA,
                               "reason": "window figures re-sourced to the account return table"}]
        else:
            out[k] = v
    data = (json.dumps(out, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    CONTRACT.write_bytes(data)
    print("OK: members re-pointed: %d" % len(hit))
    print("before (sourced, absent): %d, %d" % before)
    print("after  (sourced, absent): %d, %d" % after)
    print("new contract bytes: %d sha256 %s" % (len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
