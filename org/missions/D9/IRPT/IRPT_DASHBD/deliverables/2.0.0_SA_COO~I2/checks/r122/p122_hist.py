"""IRPT_DASHBD round 122, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the Scope history probe (CTO round-118 ADDENDUM 2, msg 8455).

  DB-i-9 (~309) TWO Scope calls, inner body, calcGrossOfFees false, Daily frequency, window = the household's earliest Orion account start date to 2026-10-13: one call for round 117's
              household (A), one for round 120's household (B). They measure, per household, the series length of every account, the call time, the response size, whether a group's
              chained daily factors reproduce Orion's own period return, and whether the series is as long as the trading days since the account's own start; from them the one-time
              backfill's request, time and size bound for the whole universe.                                                              DBI122-1-AC1

The checker RECOMPUTES from the saved private bodies (sha256 in the record): the two households by the earlier rules, each window start (the earliest non-null accountStartDate among the
household's accounts in the round-119 roster body, as a sha256 of the ISO string), each account's group, series points, chain check and completeness, and the universe bound. It never
calls the vendor. Call times are recorded by the worker (claim measured) and cannot be recomputed.

  chain_matches: |prod(factor of the group's series points) - 1 - perf| <= 1e-6  (perf = the summary decimal fraction, factors = 1 + percent/100 per day, compact breakdown)
  complete: points >= the number of NYSE trading days from the account's own accountStartDate (inclusive) to 2026-10-13 minus 1, and <= that number plus 1

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]         the pure helpers on synthetic arms
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P120 = _load("p120_second_hh", "r120/p120_second_hh.py")
P117 = P120.P117
P114 = P117.P114
Fail, need = P114.Fail, P114.need

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~309/SCOPE_HISTORY_PROBE_R122.json"
END = "2026-10-13"
MAX_CALLS = 2
CHAIN_TOL = 1e-6


def walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def group_series(body):
    """{account id: (perf, [factors])} for the Account groups of one body (factors = numeric `factor` of every descendant, in document order)."""
    out = {}
    for g in walk(body):
        if g.get("$type") != "calculated-group" or g.get("grouping") != "Account":
            continue
        perf, facs = None, []
        for n in walk(g):
            if n is g:
                continue
            if perf is None and n.get("$type") == "calculated-performance" and P117._num(n.get("performance")):
                perf = float(n["performance"])
            if P117._num(n.get("factor")):
                facs.append(float(n["factor"]))
        out[P117.key_of(g.get("groupEntityId"))] = (perf, facs)
    return out


def chain_ok(perf, facs):
    if perf is None or not facs:
        return False
    p = 1.0
    for f in facs:
        p *= f
    return abs(p - 1.0 - perf) <= CHAIN_TOL


def trading_days(start, end):
    import datetime as dt
    from lib import trading_calendar as tc
    return len(tc.trading_days_between(dt.date.fromisoformat(start), dt.date.fromisoformat(end)))


def complete_ok(points, start, end=END):
    n = trading_days(start, end)
    return n - 1 <= points <= n + 1


def check(root):
    sys.path.insert(0, str(Path(root)))
    rec = P114.load(root, REC_REL)
    P114.no_identifiers(rec)
    for k in ("served_values_changed", "pushed", "deployed", "files_in_repo_private"):
        need(rec.get(k) is False, "%s must be false" % k)
    r = rec.get("reads", {})
    for k in ("s3_writes", "dynamodb_writes"):
        need(r.get(k) == 0, "reads.%s must be 0" % k)
    need(isinstance(r.get("secret_reads"), int) and 0 <= r["secret_reads"] <= MAX_CALLS, "reads.secret_reads within the cap")
    need(isinstance(rec.get("basis_words"), str) and len(rec["basis_words"]) > 200, "basis_words missing")
    P114.script_clean(root, rec["script"]["file"], rec["script"]["sha256"])
    hh, rows, r117_hh = P120.load_world()
    digest_a, accts_a = P117.household_choice()
    sel = P120.select(hh, rows, r117_hh)
    need(sel is not None, "no second household")
    hb, clb, _ns, _nm = sel
    households = {"A": (digest_a, sorted(accts_a)), "B": (P120.dig(hb), sorted(clb))}
    calls = rec.get("calls")
    need(isinstance(calls, list) and 1 <= len(calls) <= MAX_CALLS, "calls must be 1 to %d" % MAX_CALLS)
    need(rec.get("calls_made") == len(calls) and r.get("vendor_calls") == len(calls), "calls_made and reads.vendor_calls must equal the calls listed")
    need(rec.get("token_store_used") in P117.STORES, "token_store_used")
    meas = rec.get("households", {})
    max_s, max_b, any_ok = 0.0, 0, False
    all_present, all_chain, all_complete = True, True, True
    for i, c in enumerate(calls):
        lab = ("A", "B")[i]
        need(c.get("household") == lab, "call %d must be household %s" % (i + 1, lab))
        need(c.get("gross_of_fees_flag") is False and isinstance(c.get("http_status"), int), "call flag or status")
        need(c.get("ok") is (200 <= c["http_status"] < 300), "call ok disagrees with its status")
        need(c["ok"] or i == len(calls) - 1, "a failed call must be the last (no retry)")
        if not c["ok"]:
            continue
        any_ok = True
        f = c["response_file"]
        need(Path(f["path"]).is_file() and f["path"].replace("\\", "/").startswith(P114.PRIV), "response file absent or outside the private folder")
        need(P114.sha(f["path"]) == f["sha256"], "response file sha256 differs from the record")
        need(c.get("response_bytes") == Path(f["path"]).stat().st_size, "response_bytes differs from the file size")
        need(isinstance(c.get("elapsed_s"), (int, float)) and c["elapsed_s"] >= 0, "elapsed_s")
        max_s, max_b = max(max_s, float(c["elapsed_s"])), max(max_b, int(c["response_bytes"]))
        digest, accts = households[lab]
        starts = [str(rows[a]["accountStartDate"])[:10] for a in accts if a in rows and rows[a].get("accountStartDate") not in (None, "")]
        need(starts, "household %s has no start date in the roster" % lab)
        need(meas.get(lab, {}).get("household_sha256") == digest, "household %s differs from its rule" % lab)
        need(meas[lab].get("window_start_sha256") == hashlib.sha256(min(starts).encode("utf-8")).hexdigest(), "household %s window start differs from the rule" % lab)
        body = json.loads(Path(f["path"]).read_text(encoding="utf-8"))
        gs = group_series(body)
        exp = []
        for a in accts:
            if a not in gs:
                exp.append({"account_sha256": P120.dig(a), "state": "NO_GROUP", "points": 0, "chain_matches": False, "complete": False})
                continue
            perf, facs = gs[a]
            has = perf is not None and len(facs) >= 1
            start = str(rows[a]["accountStartDate"])[:10] if a in rows and rows[a].get("accountStartDate") not in (None, "") else None
            exp.append({"account_sha256": P120.dig(a), "state": "GROUP_WITH_SERIES" if has else "GROUP_NO_SERIES", "points": len(facs),
                        "chain_matches": chain_ok(perf, facs), "complete": bool(has and start and complete_ok(len(facs), start))})
        exp.sort(key=lambda e: e["account_sha256"])
        need(meas[lab].get("accounts") == exp, "household %s per-account measurements differ from the recount" % lab)
        for e in exp:
            if e["state"] == "GROUP_WITH_SERIES":
                all_chain = all_chain and e["chain_matches"]
                all_complete = all_complete and e["complete"]
            else:
                all_present = False
    exp_c = "ACCEPTED" if any_ok else ("REFUSED" if all(c["http_status"] in (401, 403) for c in calls) else "REQUEST_REJECTED")
    need(rec.get("c_credential", {}).get("verdict") == exp_c, "c_credential differs from the recount (%s)" % exp_c)
    v = rec.get("verdict", {})
    need(v.get("all_accounts_with_series") is all_present and v.get("chain_matches_all") is all_chain and v.get("series_complete_all") is all_complete, "verdict differs from the recount")
    # the universe bound
    if any_ok:
        hh_in_roster = sum(1 for accts in hh.values() if any(a in rows for a in accts))
        b = rec.get("bound", {})
        need(b.get("households_in_universe") == hh_in_roster and b.get("requests") == hh_in_roster, "bound.households_in_universe or requests differs from the recount (%d)" % hh_in_roster)
        need(abs(b.get("seconds_max", -1) - hh_in_roster * max_s) <= 1e-6 * max(1.0, hh_in_roster * max_s), "bound.seconds_max differs from requests x the slowest call")
        need(b.get("bytes_max") == hh_in_roster * max_b, "bound.bytes_max differs from requests x the largest response")


def selftest():
    arms = []

    def arm(name, ok):
        arms.append((name, ok))

    body = {"calculations": [{"$type": "calculated-group", "grouping": "Account", "groupEntityId": 7,
                              "calculations": [{"$type": "calculated-performance", "performance": 0.0302},
                                               {"series": [{"factor": 1.01}, {"factor": 1.02}]}]}]}
    gs = group_series(body)
    arm("group_series", list(gs) == ["7"] and gs["7"][1] == [1.01, 1.02] and abs(gs["7"][0] - 0.0302) < 1e-12)
    arm("chain ok", chain_ok(0.0302, [1.01, 1.02]))
    arm("chain off", not chain_ok(0.04, [1.01, 1.02]) and not chain_ok(None, [1.01]) and not chain_ok(0.1, []))
    arm("complete uses the calendar", trading_days("2026-10-01", "2026-10-13") == 9 and complete_ok(9, "2026-10-01") and not complete_ok(5, "2026-10-01"))
    for n, v in arms:
        print(("ok   " if v else "FAIL ") + n)
    return all(v for _, v in arms)


def main(argv):
    if argv and argv[0] == "--selftest":
        root = argv[1] if len(argv) > 1 else str(HERE.parents[7])
        sys.path.insert(0, str(Path(root)))
        sys.exit(0 if selftest() else 1)
    if len(argv) != 2 or argv[1] != "DBI122-1-AC1":
        print("usage: <root> DBI122-1-AC1")
        sys.exit(2)
    try:
        check(argv[0])
    except Fail as e:
        print("%s FAIL: %s" % (argv[1], e))
        print("%s FAIL" % argv[1])
        sys.exit(1)
    except Exception as e:  # a checker error is a FAIL, never a pass
        print("%s FAIL: checker error %s: %s" % (argv[1], type(e).__name__, e))
        print("%s FAIL" % argv[1])
        sys.exit(1)
    print("%s PASS" % argv[1])


if __name__ == "__main__":
    main(sys.argv[1:])
