"""IRPT_DASHBD round 120, cell DB-i-8 (worker 0.9.0_WK_IRPT_DASHBD~308): the second-household Scope probe.

ONE other Inflection household, chosen by the rule below (fixed before any call and recomputed by the checker
p120_second_hh.py): it holds an account with a null accountStartDate (NO_START), an account with a start date and
no modelName (NO_MODEL), and no account outside Orion's active roster. Orion's Reporting/Scope is POSTed exactly
twice with the INNER scope body and calcGrossOfFees false: window q3 (2026-07-01 to 2026-09-30), then window ytd
(2026-01-01 to 2026-09-30). The calls are paced six seconds apart. There is no retry, and any non-2xx answer (or no
answer) stops the run at once.

Selection rule. Each account of the private account dimension is classed from the round-119 roster body: NO_START
(roster row with a null or empty accountStartDate), NO_MODEL (a start date, null or empty modelName), FULL, or
NOT_IN_ROSTER (no roster row). Candidates are the households other than round 117's with at least one NO_START, at
least one NO_MODEL and no NOT_IN_ROSTER account. The household is the candidate whose sha256 of its id (utf-8 hex)
sorts lowest; its NO_START and NO_MODEL accounts are the lowest-digest account of each class.

Prediction, written before any call: the NO_START account has no Scope group in either window; the NO_MODEL account
is not GROUP_WITH_SERIES in q3; every other account is GROUP_WITH_SERIES in both windows.

A vendor READ. No AWS write, no deploy, no push. The session token comes from the estate's own loader and is never
printed, logged or written. Each 2xx body is saved verbatim to the private folder. The run prints counts and verdict
words only. It writes the repo record SECOND_HOUSEHOLD_PROBE_R120.json, whose basis_words field the worker fills in
after reading the results.

Usage: python -I <this file> <repo_root>
"""
import copy
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

ENDPOINT = "https://api.cloud.orionadvisor.com/api/v1/Reporting/Scope"
PRIV_ROOT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/"
DIM = PRIV_ROOT + "0.9.0_WK_IRPT_DASHBD~171/ACCOUNT_DIM_DRY_RUN.parquet"
ROSTER = PRIV_ROOT + "0.9.0_WK_IRPT_DASHBD~307/get1_newportfolio_active.json"
PRIV = PRIV_ROOT + "0.9.0_WK_IRPT_DASHBD~308/"
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
SCRIPT_REL = D + "0.9.0_WK_IRPT_DASHBD~308/second_household_probe.py"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~308/SECOND_HOUSEHOLD_PROBE_R120.json"
R117_REC_REL = D + "0.9.0_WK_IRPT_DASHBD~305/SCOPE_PROBE_R117.json"
MODULE_DIRS = ("infra/aws/lambda/investor-reporting/performance", "infra/aws/lambda/inf-pipeline/inf-performance-daily",
               "data/assets/scripts/gold/irpt_reporting/adapters", "lib")
WINDOWS = {"q3": ("2026-07-01", "2026-09-30"), "ytd": ("2026-01-01", "2026-09-30")}
CALL_ORDER = ("q3", "ytd")
CANON_ACCOUNT = "probe-household"
PACE_S = 6
MIN_REMAINING_S = 120
MAX_BYTES = 16 * 1024 * 1024
STATES = ("GROUP_WITH_SERIES", "GROUP_NO_SERIES", "NO_GROUP")
BASIS_PENDING = "PENDING"


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
    """The Account groups of one response, as the round-117 checker reads them."""
    out = {}
    for g in walk(body):
        if g.get("$type") != "calculated-group" or g.get("grouping") != "Account":
            continue
        gid = key_of(g.get("groupEntityId"))
        perf, points = None, 0
        for n in walk(g):
            if n is g:
                continue
            if perf is None and n.get("$type") == "calculated-performance" and is_num(n.get("performance")):
                perf = float(n["performance"])
            if is_num(n.get("factor")):
                points += 1
        out[gid] = {"perf": perf, "points": points}
    return out


def state(grp, aid):
    g = grp.get(aid)
    if g is None:
        return "NO_GROUP"
    return "GROUP_WITH_SERIES" if (g["perf"] is not None and g["points"] >= 1) else "GROUP_NO_SERIES"


def classify(row):
    if row is None:
        return "NOT_IN_ROSTER"
    if row.get("accountStartDate") in (None, ""):
        return "NO_START"
    if row.get("modelName") in (None, ""):
        return "NO_MODEL"
    return "FULL"


def load_households():
    import pyarrow.parquet as pq
    rows = pq.read_table(DIM, columns=["account_id", "household_id"]).to_pylist()
    hh = {}
    for r in rows:
        a, h = key_of(r["account_id"]), key_of(r["household_id"])
        if a and h:
            hh.setdefault(h, set()).add(a)
    return hh


def load_roster():
    body = json.loads(Path(ROSTER).read_text(encoding="utf-8"))
    rows = {}
    for r in body:
        if isinstance(r, dict) and key_of(r.get("id")):
            rows[key_of(r["id"])] = r
    return rows


def select(hh, rows, exclude_digest):
    """-> ((household, class map, no_start account, no_model account), candidate count) or (None, 0)."""
    cands = []
    for h, accts in hh.items():
        if dig(h) == exclude_digest:
            continue
        cl = {a: classify(rows.get(a)) for a in accts}
        v = set(cl.values())
        if "NO_START" in v and "NO_MODEL" in v and "NOT_IN_ROSTER" not in v:
            cands.append((dig(h), h, cl))
    if not cands:
        return None, 0
    _, h, cl = min(cands)
    ns = min((a for a, c in cl.items() if c == "NO_START"), key=dig)
    nm = min((a for a, c in cl.items() if c == "NO_MODEL"), key=dig)
    return (h, cl, ns, nm), len(cands)


def build_body(household_id, first_account, window):
    import orion_selected
    import tenants
    start, end = WINDOWS[window]
    mapping = {"firm_id": tenants._CANONICAL_INF, "canonical_account_id": CANON_ACCOUNT,
               "vendor_account_id": int(first_account), "vendor_household_id": int(household_id)}
    wrapper = orion_selected.requests_for(mapping, CANON_ACCOUNT, start, end)
    body = wrapper["scope"]
    option = body["calculations"][0]["contextChange"]["performanceOption"]
    if option.get("calcGrossOfFees") is not False:
        raise SystemExit("fee flag path does not hold calcGrossOfFees false")
    url = tenants.route_for(tenants._LEGACY_SHORT_ID["INF"]).url("scope")
    if url != ENDPOINT:
        raise SystemExit("endpoint differs from the one Scope path")
    return copy.deepcopy(body), url


def _error_code(exc):
    response = getattr(exc, "response", None)
    if isinstance(response, dict):
        return str(response.get("Error", {}).get("Code", ""))
    return ""


def load_token():
    """The estate's own Secrets Manager loader only. An IAM refusal is recorded and no call is made."""
    import orion_live
    try:
        return orion_live.orion_session_jwt()
    except Exception as exc:
        print("secretsmanager read refused: %s %s" % (type(exc).__name__, _error_code(exc)))
        return None


def post(url, token, body):
    """One POST. Returns (http_status, raw_bytes_or_None); status 0 means no HTTP response."""
    data = json.dumps(body, allow_nan=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Accept", "application/json")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", "Session " + token)
    opener = urllib.request.build_opener(_NoRedirect())
    try:
        with opener.open(req, timeout=60) as resp:
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


def run_calls(url, token, bodies):
    """Exactly the calls in CALL_ORDER; a non-2xx answer (or none) stops the run; no retry."""
    calls, raws = [], {}
    for i, w in enumerate(CALL_ORDER):
        if i:
            time.sleep(PACE_S)
        status, raw = post(url, token, bodies[w])
        ok = 200 <= status < 300
        entry = {"window": w, "gross_of_fees_flag": False, "http_status": status, "ok": ok}
        if ok and raw is not None:
            path = PRIV + "scope_%s.json" % w
            with open(path, "wb") as fh:
                fh.write(raw)
            entry["response_file"] = {"path": path, "sha256": hashlib.sha256(raw).hexdigest()}
            raws[w] = raw
        calls.append(entry)
        print("call window=%s http_status=%d ok=%s" % (w, status, ok))
        if not ok:
            break
    return calls, raws


def main(argv):
    root = Path(argv[0]).resolve() if argv else Path.cwd()
    for d in MODULE_DIRS[:2]:
        sys.path.insert(0, str(root / d))
    for d in MODULE_DIRS[2:]:
        sys.path.append(str(root / d))
    Path(PRIV).mkdir(parents=True, exist_ok=True)
    hh = load_households()
    rows = load_roster()
    r117 = json.loads((root / R117_REC_REL).read_text(encoding="utf-8"))["household_sha256"]
    sel, ncand = select(hh, rows, r117)
    if sel is None:
        raise SystemExit("no candidate household exists")
    h, cl, ns, nm = sel
    accounts = sorted(cl)
    first = accounts[0]
    body_q3, url = build_body(h, first, "q3")
    body_ytd, _ = build_body(h, first, "ytd")
    print("candidates %d household_sha256 %s accounts_in_household %d" % (ncand, dig(h), len(accounts)))
    print("account classes %s" % dict(Counter(cl.values())))
    secret_reads = 1
    token = load_token()
    store = "secretsmanager" if token is not None else "none"
    calls, raws = [], {}
    if token is None:
        print("no token: no vendor call made")
    else:
        from jwt_freshness import _decode_jwt_exp
        remaining = _decode_jwt_exp(token) - time.time()
        if remaining < MIN_REMAINING_S:
            print("session near expiry or expired: no vendor call made")
        else:
            calls, raws = run_calls(url, token, {"q3": body_q3, "ytd": body_ytd})
    token = None
    bodies = {w: json.loads(raw.decode("utf-8")) for w, raw in raws.items()}
    states = {}
    for w in CALL_ORDER:
        if w in bodies:
            grp = groups(bodies[w])
            states[w] = {dig(a): state(grp, a) for a in accounts}
    # verdicts (the checker applies the same rules)
    ns_d, nm_d = dig(ns), dig(nm)
    others = [a for a in accounts if a not in (ns, nm)]
    ns_ok = bool(states) and all(states[w][ns_d] == "NO_GROUP" for w in states)
    nm_ok = bool("q3" in states and states["q3"][nm_d] != "GROUP_WITH_SERIES")
    oth_ok = bool(states) and all(states[w][dig(a)] == "GROUP_WITH_SERIES" for w in states for a in others)
    oth_short = sum(1 for w in states for a in others if states[w][dig(a)] != "GROUP_WITH_SERIES")
    claim_ok = bool(ns_ok and nm_ok and oth_ok and len(states) == 2)
    if not calls:
        cred = "NOT_RUN"
    elif bodies:
        cred = "ACCEPTED"
    elif all(c["http_status"] in (401, 403) for c in calls):
        cred = "REFUSED"
    else:
        cred = "REQUEST_REJECTED"
    rec = {
        "script": {"file": SCRIPT_REL, "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        "household_sha256": dig(h),
        "accounts_in_household": len(accounts),
        "account_classes": {dig(a): cl[a] for a in accounts},
        "no_start_account_sha256": ns_d,
        "no_model_account_sha256": nm_d,
        "calls": calls,
        "calls_made": len(calls),
        "token_store_used": store,
        "states": states,
        "verdict": {
            "no_start_confirmed": ns_ok,
            "no_model_confirmed": nm_ok,
            "others_all_present": oth_ok,
            "others_short_cells": oth_short,
            "claim_upgrade_allowed": claim_ok,
            "claim": "measured",
        },
        "c_credential": {"verdict": cred, "claim": "measured" if calls else "absent"},
        "basis_words": BASIS_PENDING,
        "reads": {"vendor_calls": len(calls), "s3_writes": 0, "dynamodb_writes": 0,
                  "secret_reads": secret_reads, "s3_reads": 0},
        "files_in_repo_private": False,
        "served_values_changed": False,
        "pushed": False,
        "deployed": False,
    }
    with open(root / REC_REL, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=2, sort_keys=True)
        fh.write("\n")
    # verdict words and counts only
    for w in CALL_ORDER:
        if w in states:
            print("states %s %s" % (w, dict(Counter(states[w].values()))))
    print("verdict no_start_confirmed=%s no_model_confirmed=%s others_all_present=%s others_short_cells=%d claim_upgrade_allowed=%s" % (
        ns_ok, nm_ok, oth_ok, oth_short, claim_ok))
    print("c_credential verdict=%s token_store_used=%s" % (cred, store))


if __name__ == "__main__":
    main(sys.argv[1:])
