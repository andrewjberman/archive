"""IRPT_DASHBD round 122, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the Scope history probe (CTO round-118 ADDENDUM 2, msg 8455).

  DB-i-9 (~309) TWO Scope calls, inner body, calcGrossOfFees false, Daily frequency, window = the household's earliest Orion account start date to 2026-10-13: one call for round 117's
              household (A), one for round 120's household (B). They measure, per household, the series length of every account, the call time, the response size, whether a group's
              chained daily factors reproduce Orion's own period return, and whether the series is as long as the trading days since the account's own start; from them the one-time
              backfill's request, time and size bound for the whole universe.                                                              DBI122-1-AC1

The checker RECOMPUTES from the saved private bodies (sha256 in the record): the two households by the earlier rules, each window start (the earliest non-null accountStartDate among the
household's accounts in the round-119 roster body, as a sha256 of the ISO string), each account's group, series points, chain check and completeness, and the universe bound. It never
calls the vendor. Call times are recorded by the worker (claim measured) and cannot be recomputed.

  Series basis (measured, round 122): the compact Daily breakdown is basedOn Calendar, so a series has one point per CALENDAR day and no gaps. Amended rules (issuer error on the first
  cut, which graded completeness in trading days and chained every series against the summary): per account with a series,
    span_days = days from the first point's endDate to the last's, inclusive; gap_breaks = consecutive endDates more than 1 day apart; contiguous = gap_breaks == 0 and points == span_days;
    chain_cumulative_bp = |prod(factor) - 1 - perf| * 1e4; for span_days <= 365 the summary perf is the cumulative return and chain_matches = chain_cumulative_bp <= 0.01;
    for span_days > 365 Orion ANNUALIZES the summary (annualize is on), so annualized_residual_bp = |prod(factor)^(365/span_days) - 1 - perf| * 1e4 is recorded (rounded to 0.1)
    and annualization_explains = annualized_residual_bp <= 10.0 (a stated reading tolerance for the 365-day convention; the residuals themselves are the finding).

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


def _day(s):
    import datetime as dt
    s = str(s)
    if "/" in s:
        return dt.datetime.strptime(s[:10], "%m/%d/%Y").date()
    return dt.date.fromisoformat(s[:10])


def group_series(body):
    """{account id: (perf, [factors], [end dates])} for the Account groups of one body (document order)."""
    out = {}
    for g in walk(body):
        if g.get("$type") != "calculated-group" or g.get("grouping") != "Account":
            continue
        perf, facs, ends = None, [], []
        for n in walk(g):
            if n is g:
                continue
            if perf is None and n.get("$type") == "calculated-performance" and P117._num(n.get("performance")):
                perf = float(n["performance"])
            if P117._num(n.get("factor")):
                facs.append(float(n["factor"]))
                ends.append(n.get("endDate"))
        out[P117.key_of(g.get("groupEntityId"))] = (perf, facs, ends)
    return out


def series_measures(perf, facs, ends):
    """(span_days, gap_breaks, contiguous, chain_cumulative_bp, annualized_residual_bp or None) for one group's series; None when it has no series."""
    if perf is None or not facs:
        return None
    ds = [_day(e) for e in ends]
    span = (ds[-1] - ds[0]).days + 1
    gaps = sum(1 for a, b in zip(ds, ds[1:]) if (b - a).days > 1)
    chain = 1.0
    for f in facs:
        chain *= f
    cum = abs(chain - 1.0 - perf) * 1e4
    ann = round(abs(chain ** (365.0 / span) - 1.0 - perf) * 1e4, 1) if span > 365 and chain > 0 else None
    return span, gaps, (gaps == 0 and len(facs) == span), round(cum, 2), ann


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
    allexp_holder = []
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
                exp.append({"account_sha256": P120.dig(a), "state": "NO_GROUP", "points": 0})
                continue
            perf, facs, ends = gs[a]
            m = series_measures(perf, facs, ends)
            if m is None:
                exp.append({"account_sha256": P120.dig(a), "state": "GROUP_NO_SERIES", "points": len(facs)})
                continue
            span, gaps, contiguous, cum, ann = m
            e = {"account_sha256": P120.dig(a), "state": "GROUP_WITH_SERIES", "points": len(facs), "span_days": span, "gap_breaks": gaps, "contiguous": contiguous,
                 "chain_cumulative_bp": cum}
            if span <= 365:
                e["chain_matches"] = cum <= 0.01
            else:
                e["annualized_residual_bp"] = ann
                e["annualization_explains"] = ann is not None and ann <= 10.0
            exp.append(e)
        exp.sort(key=lambda e: e["account_sha256"])
        need(meas[lab].get("accounts") == exp, "household %s per-account measurements differ from the recount" % lab)
        allexp = locals().get("allexp", []) + exp
        allexp_holder.extend(exp)
    exp_c = "ACCEPTED" if any_ok else ("REFUSED" if all(c["http_status"] in (401, 403) for c in calls) else "REQUEST_REJECTED")
    need(rec.get("c_credential", {}).get("verdict") == exp_c, "c_credential differs from the recount (%s)" % exp_c)
    series = [e for e in allexp_holder if e["state"] == "GROUP_WITH_SERIES"]
    exp_v = {"all_accounts_with_series": all(e["state"] == "GROUP_WITH_SERIES" for e in allexp_holder),
             "series_contiguous_all": all(e["contiguous"] for e in series),
             "short_series_chain_matches_all": all(e["chain_matches"] for e in series if "chain_matches" in e),
             "long_series_annualization_explains_all": all(e["annualization_explains"] for e in series if "annualization_explains" in e)}
    need(rec.get("verdict") == exp_v, "verdict differs from the recount (%s)" % exp_v)
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
                                               {"series": [{"factor": 1.01, "endDate": "10/01/2026"}, {"factor": 1.02, "endDate": "10/02/2026"}]}]}]}
    gs = group_series(body)
    arm("group_series", list(gs) == ["7"] and gs["7"][1] == [1.01, 1.02] and gs["7"][2] == ["10/01/2026", "10/02/2026"])
    m = series_measures(*gs["7"])
    arm("short series: contiguous, chain exact", m[0] == 2 and m[1] == 0 and m[2] is True and m[3] <= 0.01 and m[4] is None)
    gap = series_measures(0.0302, [1.01, 1.02], ["10/01/2026", "10/04/2026"])
    arm("a gap breaks contiguity", gap[1] == 1 and gap[2] is False)
    import datetime as _dt
    days = [_dt.date.fromordinal(739000 + k).isoformat() for k in range(400)]
    long_ = series_measures((1.0001 ** 400) ** (365.0 / 400) - 1.0, [1.0001] * 400, days)
    arm("long series: summary is annualized, cumulative differs, annualized residual ~0", long_[0] == 400 and long_[3] > 0.01 and long_[4] is not None and long_[4] <= 0.1)
    arm("none for no series", series_measures(None, [], []) is None)
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
