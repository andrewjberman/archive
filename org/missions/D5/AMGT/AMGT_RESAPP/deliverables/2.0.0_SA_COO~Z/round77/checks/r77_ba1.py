"""AMGT_RESAPP round 77 -- AMGT-ba-1 checks (FWD-7 data half, CTO round-76 rulings 1-2).

  python r77_ba1.py --crit AC1|AC2|AC3 [--where local|deployed]

AC1 (build, plant): `lib.research.freshness.stale_rule` keys the stale flag ONLY on inputs collected for the name at least
    once; a never-collected input reads not_collected and is never in `stale_inputs`; `keyed_date` is the OLDEST collected
    input's day; the flag and the keyed date never disagree on a row.
AC2 (build, real view): the rule applied to the /freshness view the function serves: over the covered rows, 0 never-collected
    inputs are flagged, 0 rows disagree between flag and keyed date, and the stale and not-stale counts are printed.
AC3 (bound): the route's DEFAULT /freshness rows keep exactly their ten keys (r75 c59 compares those rows; this cell adds a
    module and changes no served row).

Prints PASS/FAIL clause lines and `R77 BA1 <CRIT> SERVED: YES|NO`; exit 0 on YES.
"""
import argparse
import datetime
import importlib
import json
import sys

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
BAR_DAYS = 7
BASE_ROW_KEYS = {"covered", "reason", "name", "security_key", "security_key_basis", "source", "last_refreshed",
                 "per_input", "pack", "rot"}
INPUTS = ("bloomberg", "seekingalpha", "serp", "pack")


def _event(path, query=None):
    return {"rawPath": path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
            "queryStringParameters": query}


def _body(where, path, query=None):
    if where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")
        r = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(_event(path, query)).encode())["Payload"].read())
    else:
        from lib.research.api import scoped_amgt

        r = scoped_amgt.handler(_event(path, query))
    try:
        return r.get("statusCode"), json.loads(r.get("body") or "{}")
    except ValueError:
        return r.get("statusCode"), {}


def _stamp(day):
    return day.strftime("%Y%m%dT000000Z")


def _trading_days_back(today, n):
    from lib import trading_calendar

    day = today
    for _ in range(n):
        day = trading_calendar.prev_trading_day(day)
    return day


def _row(name, bloomberg="NEVER", seekingalpha="NEVER", serp="NEVER", pack="NEVER"):
    return {"covered": True, "reason": None, "name": name, "security_key": name.upper() + "_US_Equity",
            "security_key_basis": "plant", "source": "plant", "last_refreshed": None,
            "per_input": {"bloomberg": bloomberg, "seekingalpha": seekingalpha, "serp": serp}, "pack": pack, "rot": ""}


def _day_of(value):
    text = str(value or "")
    if len(text) >= 8 and text[:8].isdigit():
        return "{0}-{1}-{2}".format(text[:4], text[4:6], text[6:8])
    return text[:10] if len(text) >= 10 and text[4:5] == "-" else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print("{0} {1} {2}".format("PASS" if cond else "FAIL", name, detail))

    def verdict():
        yes = bool(ok) and all(ok)
        print("R77 BA1 {0} SERVED: {1}".format(a.crit, "YES" if yes else "NO"))
        return 0 if yes else 1

    if a.crit == "AC3":
        code, view = _body(a.where, PREFIX + "/freshness")
        rows = view.get("rows") or []
        odd = [sorted(set(r) ^ BASE_ROW_KEYS) for r in rows if set(r) != BASE_ROW_KEYS]
        print("   default /freshness: status {0}; rows {1}; rows off the ten-key set {2} e.g. {3}".format(
            code, len(rows), len(odd), odd[:1]))
        clause("C1 the default /freshness rows keep exactly their ten keys", code == 200 and rows and not odd,
               "{0} of {1}".format(len(rows) - len(odd), len(rows)))
        return verdict()

    try:
        stale_rule = importlib.import_module("lib.research.freshness.stale_rule")
    except Exception as err:  # noqa: BLE001 -- absent at the base: the build check FAILS here
        clause("C0 lib.research.freshness.stale_rule imports", False, "{0}: {1}".format(type(err).__name__, err))
        return verdict()

    today = datetime.date.today()
    if a.crit == "AC1":
        from lib import trading_calendar

        today = trading_calendar.prev_trading_day(today + datetime.timedelta(days=1))  # today, or the last trading day
        fresh, old, older = _stamp(_trading_days_back(today, 1)), _stamp(_trading_days_back(today, 9)), \
            _stamp(_trading_days_back(today, 20))
        edge7, edge8 = _stamp(_trading_days_back(today, BAR_DAYS)), _stamp(_trading_days_back(today, BAR_DAYS + 1))
        plants = {
            "a": _row("alpha", bloomberg=fresh, pack=fresh),                       # two collected, both fresh
            "b": _row("bravo", bloomberg=old),                                     # one collected, old
            "c": _row("charlie"),                                                  # nothing collected
            "d": _row("delta", bloomberg=fresh, seekingalpha=older, pack=old),     # oldest of three decides
            "e": _row("echo", bloomberg=edge7),                                    # exactly 7 trading days: current
            "f": _row("foxtrot", bloomberg=edge8),                                 # 8 trading days: stale
        }
        out = {k: stale_rule.annotate_row(dict(v), today) for k, v in plants.items()}
        for key in sorted(out):
            r = out[key]
            print("   plant {0}: stale {1}; stale_inputs {2}; keyed_date {3}; inputs {4}".format(
                key, r.get("stale"), r.get("stale_inputs"), r.get("keyed_date"),
                {i: (r.get("inputs") or {}).get(i, {}).get("state") for i in INPUTS}))
        a_, b_, c_, d_, e_, f_ = (out[k] for k in "abcdef")
        clause("C1 a name whose collected inputs are all current is not stale, and its never-collected inputs read "
               "not_collected", a_.get("stale") is False and not a_.get("stale_inputs")
               and (a_.get("inputs") or {}).get("seekingalpha", {}).get("state") == "not_collected"
               and (a_.get("inputs") or {}).get("serp", {}).get("state") == "not_collected")
        clause("C2 an old collected input flags the row and names itself", b_.get("stale") is True
               and b_.get("stale_inputs") == ["bloomberg"] and b_.get("keyed_date") == _day_of(old))
        clause("C3 a name with nothing collected is not stale, has no keyed date and says why in plain words",
               c_.get("stale") is False and c_.get("keyed_date") is None and not c_.get("stale_inputs")
               and isinstance(c_.get("stale_reason"), str) and len(c_.get("stale_reason")) > 10)
        clause("C4 the keyed date is the OLDEST collected input's day", d_.get("keyed_date") == _day_of(older)
               and d_.get("stale") is True and sorted(d_.get("stale_inputs") or []) == ["pack", "seekingalpha"])
        clause("C5 the line is 7 trading days: 7 is current, 8 is stale", e_.get("stale") is False
               and f_.get("stale") is True)
        untouched = all(set(plants[k]) == BASE_ROW_KEYS for k in plants)
        clause("C6 the source row is not changed in place", untouched)
        return verdict()

    code, view = _body(a.where, PREFIX + "/freshness")
    rows = [r for r in (view.get("rows") or []) if r.get("covered")]
    marked = [stale_rule.annotate_row(dict(r), today) for r in rows]
    never_flagged, disagree = [], []
    from lib import trading_calendar

    for src, r in zip(rows, marked):
        stamps = dict(src.get("per_input") or {})
        stamps["pack"] = src.get("pack")
        for name in r.get("stale_inputs") or []:
            if _day_of(stamps.get(name)) is None:
                never_flagged.append((r.get("security_key"), name))
        keyed = r.get("keyed_date")
        if keyed:
            after = datetime.date.fromisoformat(keyed) + datetime.timedelta(days=1)
            age = len(trading_calendar.trading_days_between(after, today)) if after <= today else 0
            if bool(r.get("stale")) != (age > BAR_DAYS):
                disagree.append((r.get("security_key"), keyed, age, r.get("stale")))
        elif r.get("stale"):
            disagree.append((r.get("security_key"), None, None, True))
    stale_n = sum(1 for r in marked if r.get("stale"))
    print("   {0} view: status {1}; covered rows {2}; stale {3}; not stale {4}; never-collected inputs flagged {5}; "
          "flag/date disagreements {6} e.g. {7}".format(a.where, code, len(marked), stale_n, len(marked) - stale_n,
                                                       len(never_flagged), len(disagree), (never_flagged + disagree)[:2]))
    clause("C1 no never-collected input is flagged on any covered row", code == 200 and marked and not never_flagged,
           "{0}".format(len(never_flagged)))
    clause("C2 the flag and the keyed date agree on every covered row", marked and not disagree, "{0}".format(len(disagree)))
    clause("C3 every covered row is annotated (stale is a boolean)", marked
           and all(isinstance(r.get("stale"), bool) for r in marked), "{0}".format(len(marked)))
    return verdict()


if __name__ == "__main__":
    sys.exit(main())
