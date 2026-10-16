"""IRPT_DASHBD round 132, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: ONE business_date FOR ALL THREE FIRMS (CTO msg 9342, ruling 3).

  DB-f-1801 (~1801) `lib/trading_calendar.py` gains `first_trading_day_on_or_after(date, window=14)` (the first NYSE trading day on or after the date,
                    None when none lies within the window; the calendar's fail-closed coverage error still propagates). The 49 Financial,
                    Cottonwood and Inflection producers each IMPORT it (none re-implements it); business_date is that day for the line's trade
                    date and trade_date keeps the source date as received. A line with no readable trade date, or no trading day in the window,
                    is REFUSED (counted). Each writer refuses a row whose business_date is not the partition day it is written under. The
                    round-131 producer criteria still hold (this checker runs them as a regression leg).
                    DBF132-1-AC2

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import datetime as dt
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r131"))
import p131_cottonwood as base  # noqa: E402  (the round-131 producer checker: helpers and the regression leg)

CONTRACT = base.CONTRACT
CW = base.CW
F49 = base.F49
INF = "data/assets/scripts/gold/irpt_reporting/account_transaction_inflection.py"
LIB = "lib/trading_calendar.py"
LIB_TEST = "lib/tests/test_trading_calendar.py"
FUNCTION = "first_trading_day_on_or_after"
Fail = base.Fail
need = base.need


def calendar(root):
    p = Path(root) / LIB
    need(p.is_file(), "missing " + LIB)
    spec = importlib.util.spec_from_file_location("trading_calendar_under_check", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def source_problems(sources):
    """Each producer imports the shared function and defines no day-roll of its own."""
    pr = []
    for name, text in sources.items():
        if FUNCTION not in text:
            pr.append("%s does not use %s" % (name, FUNCTION))
        if "def _performance_day" in text or "def first_trading_day" in text or "tc.is_trading_day(" in text or "trading_calendar.is_trading_day(" in text:
            pr.append("%s re-implements the day roll (it must call the one function)" % name)
    return pr


def function_problems(tc):
    pr = []
    f = getattr(tc, FUNCTION, None)
    if not callable(f):
        return ["lib/trading_calendar.py has no %s" % FUNCTION]
    cases = ((dt.date(2026, 3, 10), dt.date(2026, 3, 10)), (dt.date(2026, 3, 14), dt.date(2026, 3, 16)), (dt.date(2026, 3, 15), dt.date(2026, 3, 16)),
             (dt.date(2026, 1, 1), dt.date(2026, 1, 2)))
    for given, want in cases:
        got = f(given)
        if got != want:
            pr.append("%s(%s) gave %s, wanted %s" % (FUNCTION, given, got, want))
    if f(dt.date(2026, 3, 14), 1) is not None:
        pr.append("%s must give None when no trading day lies within the window (window 1 from a Saturday)" % FUNCTION)
    if f("2026-03-14") != dt.date(2026, 3, 16):
        pr.append("%s must accept an ISO date string as the calendar's other functions do" % FUNCTION)
    return pr


def ac_all(root):
    root = str(root)
    tc = calendar(root)
    pr = function_problems(tc)
    need(not pr, "; ".join(pr))
    srcs = {n: (Path(root) / p).read_text(encoding="utf-8") for n, p in (("49 Financial", F49), ("Cottonwood", CW), ("Inflection", INF))}
    pr = source_problems(srcs)
    need(not pr, "; ".join(pr))
    base.run_pytest(root, LIB_TEST, 26)
    # the round-131 criteria still hold (the key function, the live domains, the producers' tests: 49 Financial 50, Cottonwood 51)
    base.run_pytest(root, base.F49_TEST, 50)
    base.run_pytest(root, base.CW_TEST, 51)
    base.ac_all(root)
    con = json.loads((Path(root) / CONTRACT).read_text(encoding="utf-8"))
    m49 = base.load_module(root, F49, "account_transaction_49_dates_check")
    mcw = base.load_module(root, CW, "account_transaction_cw_dates_check")
    minf = base.load_module(root, INF, "account_transaction_inf_dates_check")
    fee_cols = tuple(con["fee_basis"]["49financial"]["columns"])
    # 49 Financial: the source business_date is NOT the answer; the rule is
    rows = m49.normalize_trn(base.cw_frame([
        base.line49(fee_cols), base.line49(fee_cols, trade_date="2026-01-03", business_date="2026-01-03"),
        base.line49(fee_cols, trade_date="2026-01-05", business_date="2026-01-06")]), m49.supported_firm())
    got = [(str(r["trade_date"]), str(r["business_date"])) for r in rows]
    need(got == [("2026-01-05", "2026-01-05"), ("2026-01-03", "2026-01-05"), ("2026-01-05", "2026-01-05")],
         "49 Financial: business_date must be the first trading day on or after trade_date whatever the source business_date says, trade_date as received: %s" % (got,))
    try:
        m49.normalize_trn(base.cw_frame([base.line49(fee_cols, trade_date=None)]), m49.supported_firm())
    except SystemExit as e:
        need("trade" in str(e).lower(), "the refusal of a 49 Financial line with no trade_date must name the trade date: %s" % e)
    else:
        raise Fail("49 Financial accepted a line with no trade_date (business_date cannot be derived)")
    # Cottonwood: Saturday trade date rolls to Monday; trade_date as received
    cw = mcw.normalize_trn(base.cw_frame([base.base_row(**{"Trade Date": "2026-03-14"}), base.base_row()]), "cottonwood")
    need([(str(r["trade_date"]), str(r["business_date"])) for r in cw] == [("2026-03-14", "2026-03-16"), ("2026-03-10", "2026-03-10")],
         "Cottonwood: a Saturday trade date rolls business_date to Monday and keeps trade_date")
    # the writers refuse a row under another partition day
    for name, mod, firm, rws, same in (("49 Financial", m49, m49.supported_firm(), rows, "2026-01-05"), ("Cottonwood", mcw, "cottonwood", cw, "2026-03-10")):
        mine = [r for r in rws if str(r["business_date"]) == same]
        res = mod.emit_transaction_day(object(), mine, firm, same, upload=False)
        need(res.get("landed") is False and res.get("rows") == len(mine), "%s: emit_transaction_day(upload=False) must make no call" % name)
        other = [r for r in rws if str(r["business_date"]) != same] or [dict(mine[0], business_date=dt.date(2026, 1, 7))]
        try:
            mod.emit_transaction_day(object(), other, firm, same, upload=False)
        except SystemExit as e:
            need("partition" in str(e).lower(), "%s: the refusal of a row under another partition day must say partition: %s" % (name, e))
        else:
            raise Fail("%s: emit_transaction_day accepted a row whose business_date is not the partition day" % name)
    del minf


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    arm("source-green", source_problems({"a": "x = tc.first_trading_day_on_or_after(d)"}), [])
    arm("source-missing", len(source_problems({"a": "pass"})), 1)
    arm("source-own-roll", len(source_problems({"a": "first_trading_day_on_or_after\ndef _performance_day(x): pass"})), 1)
    arm("source-own-loop", len(source_problems({"a": "first_trading_day_on_or_after\nif tc.is_trading_day(d): pass"})), 1)

    class Cal:
        @staticmethod
        def first_trading_day_on_or_after(d, window=14):
            if isinstance(d, str):
                d = dt.date.fromisoformat(d)
            if window < 3 and d.weekday() >= 5:
                return None
            while d.weekday() >= 5 or d == dt.date(2026, 1, 1):
                d += dt.timedelta(days=1)
            return d

    arm("function-green", function_problems(Cal), [])

    class NoCal:
        pass

    arm("function-missing", function_problems(NoCal), ["lib/trading_calendar.py has no first_trading_day_on_or_after"])
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    if ac != "DBF132-1-AC2":
        print("%s FAIL (unknown criterion)" % ac)
        return 1
    try:
        ac_all(root)
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % ac)
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % ac)
        return 1
    print("%s PASS" % ac)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
