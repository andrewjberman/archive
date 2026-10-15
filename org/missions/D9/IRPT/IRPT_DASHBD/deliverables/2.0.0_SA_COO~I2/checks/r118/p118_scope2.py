"""IRPT_DASHBD round 118, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the second Orion Scope probe (CTO round-118 analysis, ruling 2).

  DB-i-6 (~306) the SAME household as round 117, the quarter that ended 2026-09-30, the fee flag false then true, the INNER scope body. (i) do the missing account and the series-less group
              appear over the longer span, (ii) does the true-minus-false gap tie to the summed feeAmount, (iii) the cause class of each short account from the position cache and the
              newest fact_positions partition (flags and categories only). If the Q3 pair holds no fee (by fee magnitude), a second pair over 2026-01-01 to 2026-09-30 is allowed (the 4-call cap).
                                                                                                                                                     DBI118-1-AC1
The checker RECOMPUTES from the private raw bodies (sha256 in the record): the household (round 117's rule), each window's Account groups with p117's `groups`, the coverage, the fee
verdict (p117's `verdict_b`, with `NO_FEE_IN_WINDOW` when the flag changes the return and no compared account has a fee above 0), the short accounts and their position days from the cache.

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


P117 = _load("p117_scope", "r117/p117_scope.py")
P114 = P117.P114
Fail, need = P114.Fail, P114.need

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~306/SCOPE_PROBE2_R118.json"
CACHE = P114.PRIV + "0.9.0_WK_IRPT_DASHBD~174/work/positions_daily_cache.parquet"
WINDOWS = {"q3": ("2026-07-01", "2026-09-30"), "ytd": ("2026-01-01", "2026-09-30")}
MAX_CALLS = 4
B2_VERDICTS = ("IGNORED", "NET_WHEN_FALSE", "DIFFERENT_UNTIED", "NO_FEE_IN_WINDOW", "NOT_RUN")
ROLES = ("NO_GROUP", "GROUP_NO_SERIES")
CAUSES = ("NO_POSITIONS_IN_WINDOW", "ACCOUNT_CLASS_EXCLUDED_BY_VENDOR", "NOT_DETERMINED")
STORES = P117.STORES


def verdict_b2(gf, gt):
    v, ncmp, nfee = P117.verdict_b(gf, gt)
    if v == "DIFFERENT_UNTIED" and nfee == 0:
        v = "NO_FEE_IN_WINDOW"
    return v, ncmp, nfee


def coverage(grp, account_ids):
    """(groups_returned, groups_with_series, missing ids, series-less ids) for one response."""
    missing = sorted(set(account_ids) - set(grp))
    sless = sorted(i for i in account_ids if i in grp and (grp[i]["perf"] is None or grp[i]["points"] < 1))
    return len(grp), sum(1 for g in grp.values() if g["perf"] is not None and g["points"] >= 1), missing, sless


def digest(account_id):
    return hashlib.sha256(account_id.encode("utf-8")).hexdigest()


def position_days(account_id, window):
    import pyarrow.compute as pc
    import pyarrow.parquet as pq
    lo, hi = window
    t = pq.read_table(CACHE, columns=["acc", "date"])
    t = t.filter(pc.and_(pc.greater_equal(t["date"], lo), pc.less_equal(t["date"], hi)))
    return sum(1 for a in t["acc"].to_pylist() if P117.key_of(a) == account_id)


def check(root):
    rec = P114.load(root, REC_REL)
    P114.no_identifiers(rec)
    for k in ("served_values_changed", "pushed", "deployed", "files_in_repo_private"):
        need(rec.get(k) is False, "%s must be false" % k)
    r = rec.get("reads", {})
    for k in ("s3_writes", "dynamodb_writes"):
        need(r.get(k) == 0, "reads.%s must be 0" % k)
    need(isinstance(r.get("secret_reads"), int) and 0 <= r["secret_reads"] <= MAX_CALLS, "reads.secret_reads must be an integer within the call cap")
    need(isinstance(rec.get("basis_words"), str) and len(rec["basis_words"]) > 160, "basis_words missing")
    P114.script_clean(root, rec["script"]["file"], rec["script"]["sha256"])
    digest_hh, accounts = P117.household_choice()
    need(rec.get("household_sha256") == digest_hh and rec.get("accounts_in_household") == len(accounts), "household differs from round 117's rule")
    need(rec.get("windows") == {k: {"start": v[0], "end": v[1]} for k, v in WINDOWS.items() if k in rec.get("windows", {})} and "q3" in rec.get("windows", {}), "windows must be q3 (and optionally ytd) exactly as defined")
    calls = rec.get("calls")
    need(isinstance(calls, list) and 1 <= len(calls) <= MAX_CALLS, "calls must be 1 to %d" % MAX_CALLS)
    need(rec.get("calls_made") == len(calls) and r.get("vendor_calls") == len(calls), "calls_made and reads.vendor_calls must equal the calls listed")
    bodies = {}
    for c in calls:
        need(c.get("window") in WINDOWS and c["window"] in rec["windows"], "call window")
        need(c.get("gross_of_fees_flag") in (False, True) and isinstance(c.get("http_status"), int), "call flag or status")
        need(c.get("ok") is (200 <= c["http_status"] < 300), "call ok disagrees with its status")
        if c["ok"]:
            f = c["response_file"]
            need(Path(f["path"]).is_file() and f["path"].replace("\\", "/").startswith(P114.PRIV), "response file absent or outside the private folder")
            need(P114.sha(f["path"]) == f["sha256"], "response file sha256 differs from the record")
            bodies.setdefault((c["window"], c["gross_of_fees_flag"]), json.loads(Path(f["path"]).read_text(encoding="utf-8")))
    need(rec.get("token_store_used") in STORES, "token_store_used")
    # (c)
    any_ok_false = any(c["ok"] and c["gross_of_fees_flag"] is False for c in calls)
    all_refused = all(not c["ok"] for c in calls)
    all_auth = all(c["http_status"] in (401, 403) for c in calls)
    exp_c = "ACCEPTED" if any_ok_false else (("REFUSED" if all_auth else "REQUEST_REJECTED") if all_refused else "NOT_RUN")
    need(rec["c_credential"].get("verdict") == exp_c and rec["c_credential"].get("claim") in P114.CLAIMS, "c_credential differs from the recount (%s)" % exp_c)
    # (i) coverage per window
    cov = rec.get("coverage", {})
    need(sorted(cov) == sorted(rec["windows"]), "coverage must carry exactly the windows run")
    shorts = {}
    for w in rec["windows"]:
        if (w, False) in bodies:
            ngr, nser, miss, sl = coverage(P117.groups(bodies[(w, False)]), accounts)
            e = cov[w]
            need(e.get("account_groups_returned") == ngr and e.get("groups_with_series") == nser, "coverage.%s counts differ from the recount" % w)
            need(sorted(e.get("missing_account_sha256", [])) == sorted(digest(i) for i in miss), "coverage.%s missing accounts differ" % w)
            need(sorted(e.get("series_less_account_sha256", [])) == sorted(digest(i) for i in sl), "coverage.%s series-less accounts differ" % w)
            need(e.get("verdict") == ("ALL_COVERED" if not miss and not sl else "SHORT"), "coverage.%s verdict" % w)
            shorts[w] = ({i: "NO_GROUP" for i in miss}, {i: "GROUP_NO_SERIES" for i in sl})
        else:
            need(cov[w].get("verdict") == "NOT_RUN", "coverage.%s must read NOT_RUN without a flag-false response" % w)
    # (ii) fee verdict: the q3 pair; the ytd pair only when q3 held no fee
    pairs = {}
    for w in rec["windows"]:
        if (w, False) in bodies and (w, True) in bodies:
            pairs[w] = verdict_b2(P117.groups(bodies[(w, False)]), P117.groups(bodies[(w, True)]))
    if "ytd" in rec["windows"]:
        need("q3" in pairs, "a ytd pair needs the q3 pair first")
        need(len(calls) == 4, "a ytd window means all four calls")
    else:
        need(len(calls) <= 2, "without a ytd window at most two calls")
    if not pairs:
        exp_b, pair, ncmp, nfee = "NOT_RUN", None, 0, 0
    else:
        pair = "ytd" if ("ytd" in pairs and pairs["q3"][2] == 0) else next(iter(pairs))
        exp_b, ncmp, nfee = pairs[pair]
    b = rec["b_fee_basis"]
    need(b.get("verdict") == exp_b and b.get("verdict") in B2_VERDICTS and b.get("pair") == pair, "b_fee_basis differs from the recount (%s on %s)" % (exp_b, pair))
    need(b.get("accounts_compared") == ncmp and b.get("accounts_with_fee") == nfee and b.get("claim") in P114.CLAIMS, "b_fee_basis counts or claim differ")
    # (iii) short accounts (the q3 window)
    sa = rec.get("short_accounts")
    need(isinstance(sa, list), "short_accounts must be a list")
    exp_short = {}
    if "q3" in shorts:
        for d_ in shorts["q3"]:
            exp_short.update(d_)
    need(sorted(s["account_sha256"] for s in sa) == sorted(digest(i) for i in exp_short), "short_accounts differ from the q3 recount")
    for s in sa:
        aid = next(i for i in exp_short if digest(i) == s["account_sha256"])
        need(s.get("role") == exp_short[aid] and s.get("role") in ROLES, "short account role")
        need(s.get("position_days_in_window") == position_days(aid, WINDOWS["q3"]), "short account position_days_in_window differs from the cache")
        need(s.get("cause_class") in CAUSES and s.get("claim") in P114.CLAIMS, "short account cause_class or claim")
        for k in ("account_type_class", "registration_class"):
            need(isinstance(s.get(k), str) and 1 <= len(s[k]) <= 40, "short account %s" % k)
        need(isinstance(s.get("words"), str) and len(s["words"]) > 20, "short account words")


def selftest():
    arms = []

    def arm(name, ok):
        arms.append((name, ok))

    def g(gid, perf, fee, startv, points=2):
        pts = [{"factor": 1.001, "feeAmount": fee / points} for _ in range(points)]
        return {"$type": "calculated-group", "grouping": "Account", "groupEntityId": gid,
                "calculations": [{"$type": "calculated-activity", "id": "startValue", "value": startv},
                                 {"$type": "calculated-performance", "performance": perf} if perf is not None else {}, {"series": pts if perf is not None else []}]}
    body = {"calculations": [g(1, 0.01, 0.0, 1000.0), g(2, None, 0.0, 1000.0)]}
    grp = P117.groups(body)
    ngr, nser, miss, sl = coverage(grp, ["1", "2", "3"])
    arm("coverage", (ngr, nser, miss, sl) == (2, 1, ["3"], ["2"]))
    gt = P117.groups({"calculations": [g(1, 0.011, 0.0, 1000.0)]})
    arm("no fee in window", verdict_b2(P117.groups({"calculations": [g(1, 0.01, 0.0, 1000.0)]}), gt)[0] == "NO_FEE_IN_WINDOW")
    gf = P117.groups({"calculations": [g(1, 0.01, 10.0, 1000.0)]})
    gt2 = P117.groups({"calculations": [g(1, 0.02, 10.0, 1000.0)]})
    arm("net when false", verdict_b2(gf, gt2)[0] == "NET_WHEN_FALSE")
    arm("ignored", verdict_b2(gf, gf)[0] == "IGNORED")
    arm("digest", digest("7") == hashlib.sha256(b"7").hexdigest())
    for n, v in arms:
        print(("ok   " if v else "FAIL ") + n)
    return all(v for _, v in arms)


def main(argv):
    if argv and argv[0] == "--selftest":
        sys.exit(0 if selftest() else 1)
    if len(argv) != 2 or argv[1] != "DBI118-1-AC1":
        print("usage: <root> DBI118-1-AC1")
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
