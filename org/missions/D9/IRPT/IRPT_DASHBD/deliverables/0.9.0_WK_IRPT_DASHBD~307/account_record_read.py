"""IRPT_DASHBD round 119, cell DB-i-7 (worker 0.9.0_WK_IRPT_DASHBD~307) -- Orion's own account record for the account Scope leaves out.

The round-117 household (the lowest-sha256 household with 2 or more accounts in the private account dimension) gives three
roles, resolved from round 118's record and the flag-false Q3 body: `missing` (no Account group in Reporting/Scope over Q3),
`series_less` (a group with no series in Q3) and `present` (the lowest sha256 digest among the accounts with a return and a
daily series). This run reads Orion's own account records over the endpoint the estate's account pull already uses:

  GET 1 newportfolio_active    GET {BASE}/api/v1/Portfolio/Accounts/NewPortfolio, the pull's own params, isActive true.
  GET 2 newportfolio_inactive  the same request with isActive false, ONLY while `missing` is not yet found.
  GET 3 accounts_roster        GET {BASE}/api/v1/Portfolio/Accounts, the pull's params for that call, ONLY while `missing`
                               is still not found.

At most three GETs, PACE_S seconds apart, no retry; any non-2xx ends the run at once and is recorded by status. The session
token comes from the estate's Secrets Manager loader only and is used in the Authorization header only. Each 2xx body is
saved verbatim to the private folder. The repo record carries digests, counts, field names and verdict words only.
Nothing is written to AWS.

Usage: python -I <this file> <repo_root>        the probe (one run; it makes the vendor GETs above)
       python -I <this file> --selftest         the pure helpers on synthetic arms (no vendor call, no file write)
"""
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

BASE = "https://api.cloud.orionadvisor.com"
PRIV = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~307/"
DIM = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~171/ACCOUNT_DIM_DRY_RUN.parquet"
Q3_BODY = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~306/scope_q3_false.json"
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
SCRIPT_REL = D + "0.9.0_WK_IRPT_DASHBD~307/account_record_read.py"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~307/ACCOUNT_RECORD_READ_R119.json"
REC118_REL = D + "0.9.0_WK_IRPT_DASHBD~306/SCOPE_PROBE2_R118.json"
R117_HH_SHA = "00328ce57bbc14b33bd6695bc8eb32cdf2fb5f3a7d89ec14a42825e15d39df60"
MODULE_DIRS = ("infra/aws/lambda/investor-reporting/performance", "infra/aws/lambda/inf-pipeline/inf-performance-daily",
               "data/assets/scripts/gold/irpt_reporting/adapters", "lib")
PACE_S = 6
MIN_REMAINING_S = 120
MAX_GETS = 3
MAX_BYTES = 64 * 1024 * 1024
ROLES = ("missing", "series_less", "present")
RELEVANT_RX = re.compile(r"perf|report|exclud|includ|status|inception|start|end|clos|terminat|activ|model|managed|billing|composite|benchmark|hidden|suppress|skip", re.I)
EXCL_RX = re.compile(r"exclud|includ|suppress|hidden|skip|notreport|noreport|reportable", re.I)
ID_RX = re.compile(r"^(accountid|account_id|id|accountnumber)$", re.I)
MISSING = object()


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def key_of(raw):
    if raw is None:
        return None
    if isinstance(raw, float):
        if raw != raw:
            return None
        if raw.is_integer():
            return str(int(raw))
    if isinstance(raw, int):
        return str(raw)
    text = str(raw).strip()
    return text or None


def dig(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and x == x


def walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def groups(body):
    """The Account groups of one Scope response: id, perf, points (numeric factors), fee sum, startv."""
    out = {}
    for g in walk(body):
        if g.get("$type") != "calculated-group" or g.get("grouping") != "Account":
            continue
        gid = key_of(g.get("groupEntityId"))
        perf, points, fee, startv = None, 0, 0.0, None
        for n in walk(g):
            if n is g:
                continue
            if perf is None and n.get("$type") == "calculated-performance" and is_num(n.get("performance")):
                perf = float(n["performance"])
            if is_num(n.get("factor")):
                points += 1
            if is_num(n.get("feeAmount")):
                fee += float(n["feeAmount"])
            if startv is None and n.get("$type") == "calculated-activity" and n.get("id") == "startValue" and is_num(n.get("value")):
                startv = float(n["value"])
        out[gid] = {"perf": perf, "points": points, "fee": fee, "startv": startv}
    return out


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


def rows_of(body):
    """The roster rows: the list the body is, or the first list the body holds."""
    if isinstance(body, dict):
        return next((v for v in body.values() if isinstance(v, list)), [])
    return body if isinstance(body, list) else []


def find_record(rows, id_key, account_id):
    for r in rows:
        if isinstance(r, dict) and key_of(r.get(id_key)) == account_id:
            return r
    return None


def id_candidates(rows):
    names = set()
    for r in rows:
        if isinstance(r, dict):
            names.update(k for k in r if ID_RX.match(k))
    return sorted(names, key=lambda k: (k != "accountId", k != "id", k))


def choose_key(rows, present_id):
    """The id field: the first candidate name under which the known present account is found; else the first candidate."""
    cands = id_candidates(rows)
    for k in cands:
        if find_record(rows, k, present_id) is not None:
            return k
    return cands[0] if cands else None


def compare(a, c):
    fa, fc = flatten(a), flatten(c)
    paths = sorted(set(fa) | set(fc))
    diff = [p for p in paths if fa.get(p, MISSING) != fc.get(p, MISSING)]
    rel = [p for p in diff if RELEVANT_RX.search(p)]
    excl = [p for p in rel if EXCL_RX.search(p)]
    bools = {p: [fa[p], fc[p]] for p in rel if p in fa and p in fc and isinstance(fa[p], (bool, type(None))) and isinstance(fc[p], (bool, type(None)))}
    verdict = "FLAG_DIFFERS" if excl else ("STATUS_OR_DATE_DIFFERS" if rel else "NONE_VISIBLE")
    return {"differing_paths_total": len(diff), "relevant_paths": rel, "exclusion_type_paths": excl, "bool_values": bools, "verdict": verdict}


def read_roles(root):
    """The household and the three account roles, from round 118's record, the private dimension and the flag-false Q3 body."""
    import pyarrow.parquet as pq
    r118 = json.loads((Path(root) / REC118_REL).read_text(encoding="utf-8"))
    q3 = r118["coverage"]["q3"]
    if len(q3["missing_account_sha256"]) != 1 or len(q3["series_less_account_sha256"]) != 1:
        raise SystemExit("round 118 q3 must name one missing and one series-less account")
    hh = {}
    for r in pq.read_table(DIM, columns=["account_id", "household_id"]).to_pylist():
        a, h = key_of(r["account_id"]), key_of(r["household_id"])
        if a and h:
            hh.setdefault(h, set()).add(a)
    multi = {h: s for h, s in hh.items() if len(s) >= 2}
    best = min(multi, key=dig)
    hh_sha = dig(best)
    if hh_sha != R117_HH_SHA:
        raise SystemExit("household differs from round 117's household digest")
    accounts = sorted(multi[best])
    by = {dig(a): a for a in accounts}
    grp = groups(json.loads(Path(Q3_BODY).read_text(encoding="utf-8")))
    ok = sorted(a for a in accounts if a in grp and grp[a]["perf"] is not None and grp[a]["points"] >= 1)
    if not ok:
        raise SystemExit("no present account in the q3 body")
    roles = {"missing": by[q3["missing_account_sha256"][0]],
             "series_less": by[q3["series_less_account_sha256"][0]],
             "present": min(ok, key=dig)}
    return hh_sha, roles, len(accounts)


def load_token():
    """The estate's own Secrets Manager loader only. A refusal is printed by class and code, and the run stops."""
    import orion_live
    try:
        return orion_live.orion_session_jwt()
    except Exception as exc:
        response = getattr(exc, "response", None)
        code = str(response.get("Error", {}).get("Code", "")) if isinstance(response, dict) else ""
        print("secretsmanager read refused: %s %s" % (type(exc).__name__, code))
        return None


def headers(token, app_path):
    return {
        "Authorization": "Session " + token,
        "App": "OrionConnect",
        "AppPath": app_path,
        "BrowserSessionId": str(uuid.uuid4()),
        "Origin": BASE,
        "Referer": BASE + "/orionconnectapp/",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/147.0.0.0 Safari/537.36",
    }


def request_spec(kind):
    """The pull's own request for each kind: path, query params and the AppPath header."""
    if kind == "newportfolio_active":
        return "/api/v1/Portfolio/Accounts/NewPortfolio", {"$top": "50000", "createdDateStart": "01/01/1970", "isActive": "true", "newAccountFilter": ""}, "/portfolio/accounts/newportfolio"
    if kind == "newportfolio_inactive":
        return "/api/v1/Portfolio/Accounts/NewPortfolio", {"$top": "50000", "createdDateStart": "01/01/1970", "isActive": "false", "newAccountFilter": ""}, "/portfolio/accounts/newportfolio"
    return "/api/v1/Portfolio/Accounts", {"top": "50000"}, "/portfolio/accounts"


def get(kind, token):
    """One GET. Returns (http_status, raw_bytes_or_None); status 0 means no HTTP response. No redirect is followed."""
    path, params, app_path = request_spec(kind)
    req = urllib.request.Request(BASE + path + "?" + urllib.parse.urlencode(params), method="GET")
    for k, v in headers(token, app_path).items():
        req.add_header(k, v)
    opener = urllib.request.build_opener(_NoRedirect())
    try:
        with opener.open(req, timeout=180) as resp:
            status = int(resp.status)
            raw = resp.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as exc:
        status = int(exc.code)
        exc.close()
        return status, None
    except (urllib.error.URLError, OSError):
        return 0, None
    if len(raw) > MAX_BYTES:
        raise SystemExit("response oversize: refused")
    return status, raw


def run_gets(token, roles):
    """The GETs in order; a later GET only while `missing` is not found; a non-2xx ends the run (no retry)."""
    kinds = ("newportfolio_active", "newportfolio_inactive", "accounts_roster")
    found, gets, prev_start = {}, [], None
    for n, kind in enumerate(kinds, start=1):
        if prev_start is not None:
            time.sleep(PACE_S)
        start = time.time()
        gap = "none" if prev_start is None else "%.1f" % (start - prev_start)
        prev_start = start
        status, raw = get(kind, token)
        ok = 200 <= status < 300
        if not ok or raw is None:
            gets.append({"kind": kind, "http_status": status, "ok": False})
            print("GET %d kind=%s http_status=%d ok=False gap_s=%s (run stops)" % (n, kind, status, gap))
            break
        path = PRIV + "get%d_%s.json" % (n, kind)
        Path(path).write_bytes(raw)
        rows = rows_of(json.loads(raw.decode("utf-8")))
        key = choose_key(rows, roles["present"])
        if key is None:
            raise SystemExit("get %d: no account id field among the row names (body saved, run stopped)" % n)
        pres = {}
        for role in ROLES:
            row = find_record(rows, key, roles[role])
            pres[role] = row is not None
            if row is not None and role not in found:
                found[role] = row
        gets.append({"kind": kind, "http_status": status, "ok": True, "rows": len(rows), "account_id_key": key,
                     "presence": pres, "response_file": {"path": path, "sha256": hashlib.sha256(raw).hexdigest()}})
        print("GET %d kind=%s http_status=%d ok=True rows=%d id_key=%s gap_s=%s presence=%s" % (
            n, kind, status, len(rows), key, gap, json.dumps(pres, sort_keys=True)))
        if pres["missing"]:
            break
    return gets, found


def comparisons(found):
    out = {}
    for name, role in (("missing_vs_present", "missing"), ("series_less_vs_present", "series_less")):
        if role in found and "present" in found:
            out[name] = compare(found[role], found["present"])
        else:
            out[name] = {"differing_paths_total": 0, "relevant_paths": [], "exclusion_type_paths": [], "bool_values": {}, "verdict": "NOT_AVAILABLE"}
    return out


def credential(gets):
    if any(g["ok"] for g in gets):
        verdict = "ACCEPTED"
    elif all(g["http_status"] in (401, 403) for g in gets):
        verdict = "REFUSED"
    else:
        verdict = "REQUEST_REJECTED"
    return {"verdict": verdict, "claim": "measured"}


def selftest():
    arms = []

    def arm(name, ok):
        arms.append((name, bool(ok)))

    a = {"accountId": 1, "status": "Active", "isExcludedFromPerformance": True, "inceptionDate": "2020-01-01", "name": "x", "nested": {"reportingFlag": False}}
    c = {"accountId": 2, "status": "Active", "isExcludedFromPerformance": False, "inceptionDate": "2020-01-01", "name": "y", "nested": {"reportingFlag": False}}
    r = compare(a, c)
    arm("flag differs", r["verdict"] == "FLAG_DIFFERS" and r["exclusion_type_paths"] == ["isExcludedFromPerformance"] and r["bool_values"] == {"isExcludedFromPerformance": [True, False]})
    arm("identity and name are not relevant", "accountId" not in r["relevant_paths"] and "name" not in r["relevant_paths"] and r["differing_paths_total"] == 3)
    arm("status differs", compare(dict(c, status="Closed"), c)["verdict"] == "STATUS_OR_DATE_DIFFERS")
    arm("none visible", compare(dict(c, name="z"), c)["verdict"] == "NONE_VISIBLE")
    rows = [{"accountId": 5.0, "id": 9}, {"accountId": 7, "id": 3}]
    arm("find_record", find_record(rows, "accountId", "7") == rows[1] and find_record(rows, "accountId", "8") is None)
    arm("choose_key prefers accountId", choose_key(rows, "7") == "accountId")
    arm("choose_key falls back to id", choose_key([{"id": 4, "name": "q"}], "9") == "id")
    arm("choose_key none", choose_key([{"name": "q"}], "9") is None)
    arm("rows_of holds a list", rows_of({"total": 2, "items": rows}) == rows and rows_of(rows) == rows)
    arm("flatten", flatten({"a": [{"b": 1}], "c": 2}) == {"a[0].b": 1, "c": 2})
    arm("credential", credential([{"ok": False, "http_status": 401}, {"ok": False, "http_status": 401}])["verdict"] == "REFUSED" and credential([{"ok": False, "http_status": 400}])["verdict"] == "REQUEST_REJECTED")
    arm("request_spec isActive", request_spec("newportfolio_inactive")[1]["isActive"] == "false" and request_spec("accounts_roster")[0] == "/api/v1/Portfolio/Accounts")
    for n, v in arms:
        print(("ok   " if v else "FAIL ") + n)
    return all(v for _, v in arms)


def main(argv):
    if argv and argv[0] == "--selftest":
        sys.exit(0 if selftest() else 1)
    if len(argv) != 1:
        print("usage: <repo_root>  |  --selftest")
        sys.exit(2)
    root = Path(argv[0]).resolve()
    for d in MODULE_DIRS[:2]:
        sys.path.insert(0, str(root / d))
    for d in MODULE_DIRS[2:]:
        sys.path.append(str(root / d))
    Path(PRIV).mkdir(parents=True, exist_ok=True)
    hh_sha, roles, n_accounts = read_roles(root)
    print("roles resolved: %d; household accounts: %d" % (len(roles), n_accounts))
    token = load_token()
    if token is None:
        print("no token: no vendor call made")
        sys.exit(3)
    from jwt_freshness import _decode_jwt_exp
    if _decode_jwt_exp(token) - time.time() < MIN_REMAINING_S:
        token = None
        print("session near expiry or expired: no vendor call made")
        sys.exit(3)
    gets, found = run_gets(token, roles)
    token = None
    made = len(gets)
    rec = {
        "script": {"file": SCRIPT_REL, "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        "household_sha256": hh_sha,
        "roles_sha256": {"missing_sha256": dig(roles["missing"]), "series_less_sha256": dig(roles["series_less"]), "present_sha256": dig(roles["present"])},
        "gets": gets,
        "gets_made": made,
        "comparisons": comparisons(found),
        "missing_account_found": "missing" in found,
        "c_credential": credential(gets),
        "basis_words": "PENDING",
        "reads": {"vendor_calls": made, "s3_writes": 0, "dynamodb_writes": 0, "secret_reads": 1, "s3_reads": 0},
        "files_in_repo_private": False,
        "served_values_changed": False,
        "pushed": False,
        "deployed": False,
    }
    with open(root / REC_REL, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print("missing_account_found=%s gets_made=%d credential=%s" % ("missing" in found, made, rec["c_credential"]["verdict"]))
    for name, e in rec["comparisons"].items():
        print("%s verdict=%s differing_paths_total=%d exclusion_type_paths=%d" % (name, e["verdict"], e["differing_paths_total"], len(e["exclusion_type_paths"])))


if __name__ == "__main__":
    main(sys.argv[1:])
