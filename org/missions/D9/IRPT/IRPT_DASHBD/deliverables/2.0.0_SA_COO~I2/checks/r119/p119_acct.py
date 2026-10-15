"""IRPT_DASHBD round 119, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- Orion's own account record for the account Scope omits (CTO round-119 analysis, ruling 2).

  DB-i-7 (~307) at most 3 paced GETs of the endpoint the estate's pull already uses for accounts (GET /api/v1/Portfolio/Accounts/NewPortfolio, then, only while the missing account is still not
              found, the same endpoint with isActive=false, then GET /api/v1/Portfolio/Accounts): find the missing account, the series-less account and one present account of the round-117
              household, compare every performance-relevant field of their records, and name which differ, as verdict words only. A vendor READ: nothing is written.   DBI119-1-AC1

The checker RECOMPUTES from the saved private response bodies (sha256 in the record): the three accounts by round 118's record, the account records found in each body, the presence of each
account in each GET, and every comparison (flattened field paths; a path is performance-relevant by RELEVANT_RX, exclusion-type by EXCL_RX). It never calls the vendor.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]         the pure helpers on synthetic arms
"""
import hashlib
import importlib.util
import json
import re
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
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~307/ACCOUNT_RECORD_READ_R119.json"
REC118_REL = D + "0.9.0_WK_IRPT_DASHBD~306/SCOPE_PROBE2_R118.json"
Q3_BODY = P114.PRIV + "0.9.0_WK_IRPT_DASHBD~306/scope_q3_false.json"
MAX_GETS = 3
RELEVANT_RX = re.compile(r"perf|report|exclud|includ|status|inception|start|end|clos|terminat|activ|model|managed|billing|composite|benchmark|hidden|suppress|skip", re.I)
EXCL_RX = re.compile(r"exclud|includ|suppress|hidden|skip|notreport|noreport|reportable", re.I)
ENDPOINTS = {"newportfolio_active": ("/api/v1/Portfolio/Accounts/NewPortfolio", "true"),
             "newportfolio_inactive": ("/api/v1/Portfolio/Accounts/NewPortfolio", "false"),
             "accounts_roster": ("/api/v1/Portfolio/Accounts", None)}
ORDER = ("newportfolio_active", "newportfolio_inactive", "accounts_roster")
VERDICTS = ("FLAG_DIFFERS", "STATUS_OR_DATE_DIFFERS", "NONE_VISIBLE", "NOT_AVAILABLE")
MISSING = object()


def flatten(node, prefix=""):
    out = {}
    if isinstance(node, dict):
        for k, v in node.items():
            out.update(flatten(v, prefix + "." + str(k) if prefix else str(k)))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out.update(flatten(v, "%s[%d]" % (prefix, i)))
    else:
        out[prefix] = node
    return out


def find_record(body, id_key, account_id):
    """The row of a roster body (a list, or a dict holding a list) whose id_key equals the account id; None when absent."""
    if isinstance(body, dict):
        rows = next((v for v in body.values() if isinstance(v, list)), [])
    else:
        rows = body if isinstance(body, list) else []
    for r in rows:
        if isinstance(r, dict) and P117.key_of(r.get(id_key)) == account_id:
            return r
    return None


def compare(a, c):
    fa, fc = flatten(a), flatten(c)
    paths = sorted(set(fa) | set(fc))
    diff = [p for p in paths if fa.get(p, MISSING) != fc.get(p, MISSING)]
    rel = [p for p in diff if RELEVANT_RX.search(p)]
    excl = [p for p in rel if EXCL_RX.search(p)]
    bools = {p: [fa[p], fc[p]] for p in rel if p in fa and p in fc and isinstance(fa[p], (bool, type(None))) and isinstance(fc[p], (bool, type(None)))}
    verdict = "FLAG_DIFFERS" if excl else ("STATUS_OR_DATE_DIFFERS" if rel else "NONE_VISIBLE")
    return {"differing_paths_total": len(diff), "relevant_paths": rel, "exclusion_type_paths": excl, "bool_values": bools, "verdict": verdict}


def roles_from_round118(root):
    r118 = P114.load(root, REC118_REL)
    q3 = r118["coverage"]["q3"]
    need(len(q3["missing_account_sha256"]) == 1 and len(q3["series_less_account_sha256"]) == 1, "round 118 q3 must name exactly one missing and one series-less account")
    digest_hh, accounts = P117.household_choice()
    by = {hashlib.sha256(a.encode("utf-8")).hexdigest(): a for a in accounts}
    body = json.loads(Path(Q3_BODY).read_text(encoding="utf-8"))
    grp = P117.groups(body)
    ok = sorted(a for a in accounts if a in grp and grp[a]["perf"] is not None and grp[a]["points"] >= 1)
    need(ok, "no present account in the q3 body")
    present = min(ok, key=lambda a: hashlib.sha256(a.encode("utf-8")).hexdigest())
    return {"missing": by[q3["missing_account_sha256"][0]], "series_less": by[q3["series_less_account_sha256"][0]], "present": present}, digest_hh


def check(root):
    rec = P114.load(root, REC_REL)
    P114.no_identifiers(rec)
    for k in ("served_values_changed", "pushed", "deployed", "files_in_repo_private"):
        need(rec.get(k) is False, "%s must be false" % k)
    r = rec.get("reads", {})
    for k in ("s3_writes", "dynamodb_writes"):
        need(r.get(k) == 0, "reads.%s must be 0" % k)
    need(isinstance(r.get("secret_reads"), int) and 0 <= r["secret_reads"] <= MAX_GETS, "reads.secret_reads within the cap")
    need(isinstance(rec.get("basis_words"), str) and len(rec["basis_words"]) > 160, "basis_words missing")
    P114.script_clean(root, rec["script"]["file"], rec["script"]["sha256"])
    roles, digest_hh = roles_from_round118(root)
    need(rec.get("household_sha256") == digest_hh, "household differs from round 117's rule")
    need(rec.get("roles_sha256") == {k + "_sha256": hashlib.sha256(v.encode("utf-8")).hexdigest() for k, v in roles.items()}, "roles_sha256 differ from round 118's record")
    gets = rec.get("gets")
    need(isinstance(gets, list) and 1 <= len(gets) <= MAX_GETS, "gets must be 1 to %d" % MAX_GETS)
    need(rec.get("gets_made") == len(gets) and r.get("vendor_calls") == len(gets), "gets_made and reads.vendor_calls must equal the gets listed")
    bodies, presence, recs = [], [], {}
    for n, g in enumerate(gets):
        need(g.get("kind") == ORDER[n], "get %d must be %s" % (n + 1, ORDER[n]))
        need(isinstance(g.get("http_status"), int) and g.get("ok") is (200 <= g["http_status"] < 300), "get ok disagrees with its status")
        need(g["ok"] or n == len(gets) - 1, "a failed get must be the last (no retry, stop on any 4xx or 5xx)")
        if not g["ok"]:
            presence.append(None)
            continue
        f = g["response_file"]
        need(Path(f["path"]).is_file() and f["path"].replace("\\", "/").startswith(P114.PRIV), "response file absent or outside the private folder")
        need(P114.sha(f["path"]) == f["sha256"], "response file sha256 differs from the record")
        body = json.loads(Path(f["path"]).read_text(encoding="utf-8"))
        key = g.get("account_id_key")
        need(isinstance(key, str) and key, "get %d account_id_key" % (n + 1))
        found = {role: find_record(body, key, aid) for role, aid in roles.items()}
        pres = {role: found[role] is not None for role in roles}
        need(g.get("presence") == pres, "get %d presence differs from the recount (%s)" % (n + 1, pres))
        for role in roles:
            if found[role] is not None and role not in recs:
                recs[role] = found[role]
        presence.append(pres)
        bodies.append(body)
    # the conditional gets: the next get happens only while the missing account is still not found
    for n in range(len(gets) - 1):
        need(presence[n] is not None and not presence[n]["missing"], "get %d was followed by another although the missing account was already found" % (n + 1))
    if len(gets) < MAX_GETS and gets[-1]["ok"]:
        need(presence[-1]["missing"], "the read stopped before the missing account was found and before the last get")
    # comparisons
    comp = rec.get("comparisons", {})
    for name, role in (("missing_vs_present", "missing"), ("series_less_vs_present", "series_less")):
        e = comp.get(name)
        need(isinstance(e, dict), "comparison %s missing" % name)
        if role in recs and "present" in recs:
            exp = compare(recs[role], recs["present"])
            need({k: e.get(k) for k in exp} == exp, "comparison %s differs from the recount" % name)
        else:
            need(e.get("verdict") == "NOT_AVAILABLE", "comparison %s must read NOT_AVAILABLE when a record was not found" % name)
    need(rec["c_credential"].get("verdict") in ("ACCEPTED", "REFUSED", "REQUEST_REJECTED", "NOT_RUN") and rec["c_credential"].get("claim") in P114.CLAIMS, "c_credential")
    exp_c = "ACCEPTED" if any(g["ok"] for g in gets) else ("REFUSED" if all(g["http_status"] in (401, 403) for g in gets) else "REQUEST_REJECTED")
    need(rec["c_credential"]["verdict"] == exp_c, "c_credential differs from the recount (%s)" % exp_c)
    need(rec.get("missing_account_found") is ("missing" in recs), "missing_account_found differs from the recount")


def selftest():
    arms = []

    def arm(name, ok):
        arms.append((name, ok))

    a = {"accountId": 1, "status": "Active", "isExcludedFromPerformance": True, "inceptionDate": "2020-01-01", "name": "x", "nested": {"reportingFlag": False}}
    c = {"accountId": 2, "status": "Active", "isExcludedFromPerformance": False, "inceptionDate": "2020-01-01", "name": "y", "nested": {"reportingFlag": False}}
    r = compare(a, c)
    arm("flag differs", r["verdict"] == "FLAG_DIFFERS" and r["exclusion_type_paths"] == ["isExcludedFromPerformance"] and r["bool_values"] == {"isExcludedFromPerformance": [True, False]})
    arm("identity and name are not relevant", "accountId" not in r["relevant_paths"] and "name" not in r["relevant_paths"] and r["differing_paths_total"] == 3)
    d = dict(c, status="Closed")
    arm("status differs", compare(d, c)["verdict"] == "STATUS_OR_DATE_DIFFERS")
    arm("none visible", compare(dict(c, name="z"), c)["verdict"] == "NONE_VISIBLE")
    arm("find_record", find_record([{"accountId": 5.0}, {"accountId": 7}], "accountId", "7") == {"accountId": 7} and find_record([{"accountId": 5}], "accountId", "7") is None)
    arm("flatten", flatten({"a": [{"b": 1}], "c": 2}) == {"a[0].b": 1, "c": 2})
    for n, v in arms:
        print(("ok   " if v else "FAIL ") + n)
    return all(v for _, v in arms)


def main(argv):
    if argv and argv[0] == "--selftest":
        sys.exit(0 if selftest() else 1)
    if len(argv) != 2 or argv[1] != "DBI119-1-AC1":
        print("usage: <root> DBI119-1-AC1")
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
