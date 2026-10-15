"""IRPT_DASHBD round 120, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the second-household Scope probe (CTO round-120 analysis, ruling 2).

  DB-i-8 (~308) ONE other Inflection household that holds an account with a NULL accountStartDate and an account with a start date but NO modelName, and no account outside Orion's active
              roster (chosen by the rule below, recomputed here); Scope called twice with the inner body, calcGrossOfFees false: Q3 (2026-07-01 to 2026-09-30) and YTD (2026-01-01 to
              2026-09-30). Does the null-start account have no Scope group, is the no-model account short, and is every other account present with a series?    DBI120-1-AC1

PRE-REGISTERED PREDICTION (from round 119's single household, written before any call): the null-start account has NO group in both windows; the no-model account is not
GROUP_WITH_SERIES in Q3; every other account is GROUP_WITH_SERIES in both windows. The verdict words below say whether each part held; nothing is tuned afterwards.

Selection rule: from the private dimension and the round-119 roster body (GET 1, the pull's NewPortfolio request), a household's accounts are classed NO_START (roster row with a null or empty
accountStartDate), NO_MODEL (a start date, a null or empty modelName), FULL, or NOT_IN_ROSTER. Candidates: households other than round 117's with at least one NO_START, at least one NO_MODEL and
NO NOT_IN_ROSTER account. The household is the candidate whose sha256(str(household_id)) hex digest sorts lowest; its NO_START account and NO_MODEL account are the lowest-digest account of each class.
State of an account in a body: GROUP_WITH_SERIES (a group with a perf and 1 or more points), GROUP_NO_SERIES (a group, no perf or no points), NO_GROUP.

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
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~308/SECOND_HOUSEHOLD_PROBE_R120.json"
REC119_REL = D + "0.9.0_WK_IRPT_DASHBD~307/ACCOUNT_RECORD_READ_R119.json"
ROSTER = P114.PRIV + "0.9.0_WK_IRPT_DASHBD~307/get1_newportfolio_active.json"
WINDOWS = {"q3": ("2026-07-01", "2026-09-30"), "ytd": ("2026-01-01", "2026-09-30")}
MAX_CALLS = 2
CLASSES = ("NO_START", "NO_MODEL", "FULL", "NOT_IN_ROSTER")
STATES = ("GROUP_WITH_SERIES", "GROUP_NO_SERIES", "NO_GROUP")


def dig(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def classify(row):
    if row is None:
        return "NOT_IN_ROSTER"
    if row.get("accountStartDate") in (None, ""):
        return "NO_START"
    if row.get("modelName") in (None, ""):
        return "NO_MODEL"
    return "FULL"


def select(households, rows, exclude_hh):
    """households: {hh: [account ids]}; rows: {account id: roster row}; -> (hh, accounts-class dict, no_start id, no_model id) or None."""
    cands = []
    for h, accts in households.items():
        if h == exclude_hh:
            continue
        cl = {a: classify(rows.get(a)) for a in accts}
        v = list(cl.values())
        if "NO_START" in v and "NO_MODEL" in v and "NOT_IN_ROSTER" not in v:
            cands.append((dig(h), h, cl))
    if not cands:
        return None
    _, h, cl = min(cands)
    ns = min((a for a, c in cl.items() if c == "NO_START"), key=dig)
    nm = min((a for a, c in cl.items() if c == "NO_MODEL"), key=dig)
    return h, cl, ns, nm


def state(grp, aid):
    g = grp.get(aid)
    if g is None:
        return "NO_GROUP"
    return "GROUP_WITH_SERIES" if (g["perf"] is not None and g["points"] >= 1) else "GROUP_NO_SERIES"


def load_world():
    import pyarrow.parquet as pq
    dim = pq.read_table(P117.DIM, columns=["account_id", "household_id"]).to_pylist()
    hh = {}
    for r in dim:
        a, h = P117.key_of(r["account_id"]), P117.key_of(r["household_id"])
        if a and h:
            hh.setdefault(h, []).append(a)
    body = json.loads(Path(ROSTER).read_text(encoding="utf-8"))
    rows = {}
    for r in body:
        if isinstance(r, dict) and P117.key_of(r.get("id")):
            rows[P117.key_of(r["id"])] = r
    r117_hh = min((h for h, a in hh.items() if len(a) >= 2), key=dig)
    return hh, rows, r117_hh


def check(root):
    rec = P114.load(root, REC_REL)
    P114.no_identifiers(rec)
    for k in ("served_values_changed", "pushed", "deployed", "files_in_repo_private"):
        need(rec.get(k) is False, "%s must be false" % k)
    r = rec.get("reads", {})
    for k in ("s3_writes", "dynamodb_writes"):
        need(r.get(k) == 0, "reads.%s must be 0" % k)
    need(isinstance(r.get("secret_reads"), int) and 0 <= r["secret_reads"] <= MAX_CALLS, "reads.secret_reads within the cap")
    need(isinstance(rec.get("basis_words"), str) and len(rec["basis_words"]) > 160, "basis_words missing")
    P114.script_clean(root, rec["script"]["file"], rec["script"]["sha256"])
    hh, rows, r117_hh = load_world()
    sel = select(hh, rows, r117_hh)
    need(sel is not None, "no candidate household exists")
    h, cl, ns, nm = sel
    need(rec.get("household_sha256") == dig(h) and rec.get("accounts_in_household") == len(cl), "household differs from the selection rule")
    need(rec.get("account_classes") == {dig(a) + "": c for a, c in cl.items()}, "account_classes differ from the recount")
    need(rec.get("no_start_account_sha256") == dig(ns) and rec.get("no_model_account_sha256") == dig(nm), "chosen accounts differ from the rule")
    calls = rec.get("calls")
    need(isinstance(calls, list) and 1 <= len(calls) <= MAX_CALLS, "calls must be 1 to %d" % MAX_CALLS)
    need(rec.get("calls_made") == len(calls) and r.get("vendor_calls") == len(calls), "calls_made and reads.vendor_calls must equal the calls listed")
    bodies = {}
    for i, c in enumerate(calls):
        need(c.get("window") == ("q3", "ytd")[i], "call %d must be %s" % (i + 1, ("q3", "ytd")[i]))
        need(c.get("gross_of_fees_flag") is False and isinstance(c.get("http_status"), int), "call flag or status")
        need(c.get("ok") is (200 <= c["http_status"] < 300), "call ok disagrees with its status")
        need(c["ok"] or i == len(calls) - 1, "a failed call must be the last (no retry)")
        if c["ok"]:
            f = c["response_file"]
            need(Path(f["path"]).is_file() and f["path"].replace("\\", "/").startswith(P114.PRIV), "response file absent or outside the private folder")
            need(P114.sha(f["path"]) == f["sha256"], "response file sha256 differs from the record")
            bodies[c["window"]] = json.loads(Path(f["path"]).read_text(encoding="utf-8"))
    need(rec.get("token_store_used") in P117.STORES, "token_store_used")
    exp_c = "ACCEPTED" if bodies else ("REFUSED" if all(c["http_status"] in (401, 403) for c in calls) else "REQUEST_REJECTED")
    need(rec["c_credential"].get("verdict") == exp_c and rec["c_credential"].get("claim") in P114.CLAIMS, "c_credential differs from the recount (%s)" % exp_c)
    states = {}
    for w, b in bodies.items():
        grp = P117.groups(b)
        states[w] = {dig(a): state(grp, a) for a in cl}
    need(rec.get("states") == states, "states differ from the recount")
    # verdicts
    v = rec.get("verdict", {})
    ns_ok = bool(states) and all(states[w][dig(ns)] == "NO_GROUP" for w in states)
    nm_ok = "q3" in states and states["q3"][dig(nm)] != "GROUP_WITH_SERIES"
    others = [a for a in cl if a not in (ns, nm)]
    oth_ok = bool(states) and all(states[w][dig(a)] == "GROUP_WITH_SERIES" for w in states for a in others)
    oth_short = sum(1 for w in states for a in others if states[w][dig(a)] != "GROUP_WITH_SERIES")
    need(v.get("no_start_confirmed") is ns_ok, "verdict.no_start_confirmed differs from the recount (%s)" % ns_ok)
    need(v.get("no_model_confirmed") is nm_ok, "verdict.no_model_confirmed differs from the recount (%s)" % nm_ok)
    need(v.get("others_all_present") is oth_ok and v.get("others_short_cells") == oth_short, "verdict.others differ from the recount")
    need(v.get("claim_upgrade_allowed") is (ns_ok and nm_ok and oth_ok and len(states) == 2), "verdict.claim_upgrade_allowed differs from the recount")
    need(v.get("claim") in P114.CLAIMS, "verdict.claim")


def selftest():
    arms = []

    def arm(name, ok):
        arms.append((name, ok))

    rows = {"1": {"accountStartDate": None, "modelName": "m"}, "2": {"accountStartDate": "d", "modelName": ""}, "3": {"accountStartDate": "d", "modelName": "m"},
            "4": {"accountStartDate": None, "modelName": ""}, "5": {"accountStartDate": "d", "modelName": ""}, "6": {"accountStartDate": "d", "modelName": "m"}}
    arm("classify", [classify(rows[k]) for k in "123"] == ["NO_START", "NO_MODEL", "FULL"] and classify(None) == "NOT_IN_ROSTER")
    hhs = {"A": ["1", "2", "3"], "B": ["4", "5", "6"], "C": ["1", "9", "3"], "R": ["1", "2", "3"]}
    s = select(hhs, rows, "R")
    arm("select excludes R, drops NOT_IN_ROSTER (C), picks lowest digest", s is not None and s[0] == min(("A", "B"), key=dig) and s[0] != "C")
    arm("select none", select({"C": ["1", "9"]}, rows, "R") is None)
    grp = {"1": {"perf": 0.1, "points": 3}, "2": {"perf": None, "points": 0}}
    arm("state", (state(grp, "1"), state(grp, "2"), state(grp, "7")) == ("GROUP_WITH_SERIES", "GROUP_NO_SERIES", "NO_GROUP"))
    for n, v_ in arms:
        print(("ok   " if v_ else "FAIL ") + n)
    return all(v_ for _, v_ in arms)


def main(argv):
    if argv and argv[0] == "--selftest":
        sys.exit(0 if selftest() else 1)
    if len(argv) != 2 or argv[1] != "DBI120-1-AC1":
        print("usage: <root> DBI120-1-AC1")
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
