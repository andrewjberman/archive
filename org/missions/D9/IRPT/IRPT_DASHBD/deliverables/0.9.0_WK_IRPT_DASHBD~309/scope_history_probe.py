"""IRPT_DASHBD round 122, cell DB-i-9 (worker 0.9.0_WK_IRPT_DASHBD~309): the Scope history probe.

Exactly TWO Orion Reporting/Scope POSTs, paced six seconds apart, with NO retry: household A (round 117's household) and
household B (round 120's household). Each POST carries the INNER scope body from orion_selected.requests_for, with
calcGrossOfFees false and a Daily compact breakdown over the household's window: from the earliest non-null accountStartDate
of its accounts in the round-119 roster to 2026-10-13. A 4xx or 5xx answer (or no answer) stops the run at once; a body
over 64 MB stops it as oversize. The POST timeout is 180 seconds.

Per account the run records the state (GROUP_WITH_SERIES, GROUP_NO_SERIES or NO_GROUP), the series points, whether the
chained daily factors reproduce the group's period return, and whether the series length is within one trading day of the
trading days from the account's own start. The record SCOPE_HISTORY_PROBE_R122.json holds digests, counts, verdict words
and timings only. The raw bodies stay in the private folder. The token comes from the estate's own loader and is never
printed, logged or written.

Usage: python -I <this file> <repo_root>
"""
import copy
import datetime as dt
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
PRIV = PRIV_ROOT + "0.9.0_WK_IRPT_DASHBD~309/"
DIM = PRIV_ROOT + "0.9.0_WK_IRPT_DASHBD~171/ACCOUNT_DIM_DRY_RUN.parquet"
ROSTER = PRIV_ROOT + "0.9.0_WK_IRPT_DASHBD~307/get1_newportfolio_active.json"
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
SCRIPT_REL = D + "0.9.0_WK_IRPT_DASHBD~309/scope_history_probe.py"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~309/SCOPE_HISTORY_PROBE_R122.json"
MODULE_DIRS = ("infra/aws/lambda/investor-reporting/performance", "infra/aws/lambda/inf-pipeline/inf-performance-daily",
               "data/assets/scripts/gold/irpt_reporting/adapters", "lib")
END = "2026-10-13"
CANON_ACCOUNT = "probe-household"
CALL_ORDER = ("A", "B")
PACE_S = 6
TIMEOUT_S = 180
MIN_REMAINING_S = 120
MAX_BYTES = 64 * 1024 * 1024
CHAIN_TOL = 1e-6
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


def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


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


def group_series(body):
    """{account id: (perf, [factors])} for the Account groups of one body; factors are the numeric factor values of the descendants."""
    out = {}
    for g in walk(body):
        if g.get("$type") != "calculated-group" or g.get("grouping") != "Account":
            continue
        perf, facs = None, []
        for n in walk(g):
            if n is g:
                continue
            if perf is None and n.get("$type") == "calculated-performance" and is_num(n.get("performance")):
                perf = float(n["performance"])
            if is_num(n.get("factor")):
                facs.append(float(n["factor"]))
        out[key_of(g.get("groupEntityId"))] = (perf, facs)
    return out


def chain_ok(perf, facs):
    if perf is None or not facs:
        return False
    p = 1.0
    for f in facs:
        p *= f
    return abs(p - 1.0 - perf) <= CHAIN_TOL


def trading_days(start, end):
    from lib import trading_calendar as tc
    return len(tc.trading_days_between(dt.date.fromisoformat(start), dt.date.fromisoformat(end)))


def classify(row):
    if row is None:
        return "NOT_IN_ROSTER"
    if row.get("accountStartDate") in (None, ""):
        return "NO_START"
    if row.get("modelName") in (None, ""):
        return "NO_MODEL"
    return "FULL"


def load_world():
    import pyarrow.parquet as pq
    dim = pq.read_table(DIM, columns=["account_id", "household_id"]).to_pylist()
    hh_list, hh_set = {}, {}
    for r in dim:
        a, h = key_of(r["account_id"]), key_of(r["household_id"])
        if a and h:
            hh_list.setdefault(h, []).append(a)
            hh_set.setdefault(h, set()).add(a)
    rows = {}
    for r in json.loads(Path(ROSTER).read_text(encoding="utf-8")):
        if isinstance(r, dict) and key_of(r.get("id")):
            rows[key_of(r["id"])] = r
    return hh_list, hh_set, rows


def pick_households(hh_list, hh_set, rows):
    """A: the lowest-digest household with 2 or more accounts. B: the rule of round 120, excluding A's household."""
    multi = {h: s for h, s in hh_set.items() if len(s) >= 2}
    a_raw = min(multi, key=dig)
    a_accts = sorted(multi[a_raw])
    a_list_raw = min((h for h, a in hh_list.items() if len(a) >= 2), key=dig)
    cands = []
    for h, accts in hh_list.items():
        if h == a_list_raw:
            continue
        cl = {a: classify(rows.get(a)) for a in accts}
        v = set(cl.values())
        if "NO_START" in v and "NO_MODEL" in v and "NOT_IN_ROSTER" not in v:
            cands.append((dig(h), h, cl))
    if not cands:
        raise SystemExit("no candidate household for B")
    _, b_raw, cl = min(cands)
    b_accts = sorted(cl)
    return {"A": (a_raw, a_accts), "B": (b_raw, b_accts)}, len(cands), cl


def window_start(accts, rows):
    starts = [str(rows[a]["accountStartDate"])[:10] for a in accts if a in rows and rows[a].get("accountStartDate") not in (None, "")]
    if not starts:
        raise SystemExit("a household without any roster start date")
    return min(starts)


def build_body(household_raw, first_account, start):
    import orion_selected
    import tenants
    mapping = {"firm_id": tenants._CANONICAL_INF, "canonical_account_id": CANON_ACCOUNT,
               "vendor_account_id": int(first_account), "vendor_household_id": int(household_raw)}
    wrapper = orion_selected.requests_for(mapping, CANON_ACCOUNT, start, END)
    body = wrapper["scope"]
    option = body["calculations"][0]["contextChange"]["performanceOption"]
    if option.get("calcGrossOfFees") is not False:
        raise SystemExit("fee flag path does not hold calcGrossOfFees false")
    url = tenants.route_for(tenants._LEGACY_SHORT_ID["INF"]).url("scope")
    if url != ENDPOINT:
        raise SystemExit("endpoint differs from the one Scope path")
    return copy.deepcopy(body)


def load_token():
    """The estate's own Secrets Manager loader only. A refusal is recorded and no call is made."""
    import orion_live
    try:
        return orion_live.orion_session_jwt()
    except Exception as exc:
        print("secretsmanager read refused: %s" % type(exc).__name__)
        return None


def post(url, token, body):
    """One POST, timed from just before the request to the end of the body read. Status 0 means no HTTP response."""
    data = json.dumps(body, allow_nan=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Accept", "application/json")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", "Session " + token)
    opener = urllib.request.build_opener(_NoRedirect())
    t0 = time.monotonic()
    try:
        with opener.open(req, timeout=TIMEOUT_S) as resp:
            status = int(resp.status)
            raw = resp.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as exc:
        status = int(exc.code)
        exc.close()
        return status, None, None
    except (urllib.error.URLError, OSError):
        return 0, None, None
    return status, raw, time.monotonic() - t0


def run_calls(url, token, bodies):
    """Exactly the calls in CALL_ORDER; a non-2xx answer, no answer or an oversize body stops the run; no retry."""
    calls, raws, timings = [], {}, {}
    for i, lab in enumerate(CALL_ORDER):
        if i:
            time.sleep(PACE_S)
        status, raw, elapsed = post(url, token, bodies[lab])
        ok = 200 <= status < 300
        entry = {"household": lab, "gross_of_fees_flag": False, "http_status": status, "ok": ok}
        if ok and raw is not None and len(raw) > MAX_BYTES:
            entry["oversize"] = True
            entry["oversize_bytes_read"] = len(raw)
            calls.append(entry)
            print("call household=%s http_status=%d oversize" % (lab, status))
            break
        if ok and raw is not None:
            path = PRIV + "hist_%s.json" % lab
            with open(path, "wb") as fh:
                fh.write(raw)
            entry["elapsed_s"] = elapsed
            entry["response_bytes"] = len(raw)
            entry["response_file"] = {"path": path, "sha256": sha_bytes(raw)}
            raws[lab] = raw
            timings[lab] = elapsed
        calls.append(entry)
        print("call household=%s http_status=%d ok=%s" % (lab, status, ok))
        if not ok:
            break
    return calls, raws


def account_entries(body, accts, rows):
    gs = group_series(body)
    out = []
    for a in accts:
        if a not in gs:
            out.append({"account_sha256": dig(a), "state": "NO_GROUP", "points": 0, "chain_matches": False, "complete": False})
            continue
        perf, facs = gs[a]
        has = perf is not None and len(facs) >= 1
        start = str(rows[a]["accountStartDate"])[:10] if a in rows and rows[a].get("accountStartDate") not in (None, "") else None
        complete = False
        if has and start:
            n = trading_days(start, END)
            complete = n - 1 <= len(facs) <= n + 1
        out.append({"account_sha256": dig(a), "state": "GROUP_WITH_SERIES" if has else "GROUP_NO_SERIES",
                    "points": len(facs), "chain_matches": chain_ok(perf, facs), "complete": complete})
    out.sort(key=lambda e: e["account_sha256"])
    return out


def main(argv):
    root = Path(argv[0]).resolve() if argv else Path.cwd()
    for d in MODULE_DIRS[:2]:
        sys.path.insert(0, str(root / d))
    for d in MODULE_DIRS[2:]:
        sys.path.append(str(root / d))
    sys.path.append(str(root))
    Path(PRIV).mkdir(parents=True, exist_ok=True)
    hh_list, hh_set, rows = load_world()
    hhs, ncand, cl_b = pick_households(hh_list, hh_set, rows)
    windows, accts_of, bodies = {}, {}, {}
    for lab in CALL_ORDER:
        raw_id, accts = hhs[lab]
        accts_of[lab] = accts
        windows[lab] = window_start(accts, rows)
        bodies[lab] = build_body(raw_id, accts[0], windows[lab])
    print("candidates_b %d accounts_a %d accounts_b %d" % (ncand, len(accts_of["A"]), len(accts_of["B"])))
    print("b account classes %s" % dict(Counter(cl_b.values())))
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
            calls, raws = run_calls(ENDPOINT, token, bodies)
    token = None
    households, timings_ok, bytes_ok = {}, [], []
    all_present, all_chain, all_complete = True, True, True
    for c in calls:
        lab = c["household"]
        if not c["ok"] or lab not in raws:
            continue
        timings_ok.append(float(c["elapsed_s"]))
        bytes_ok.append(int(c["response_bytes"]))
        body = json.loads(raws[lab].decode("utf-8"))
        raw_id, accts = hhs[lab]
        entries = account_entries(body, accts, rows)
        households[lab] = {"household_sha256": dig(raw_id), "window_start_sha256": dig(windows[lab]), "accounts": entries}
        for e in entries:
            if e["state"] == "GROUP_WITH_SERIES":
                all_chain = all_chain and e["chain_matches"]
                all_complete = all_complete and e["complete"]
            else:
                all_present = False
    any_ok = bool(timings_ok)
    if not calls:
        cred = "REQUEST_REJECTED"
    elif any_ok:
        cred = "ACCEPTED"
    elif all(c["http_status"] in (401, 403) for c in calls):
        cred = "REFUSED"
    else:
        cred = "REQUEST_REJECTED"
    if any_ok:
        universe = sum(1 for accts in hh_list.values() if any(a in rows for a in accts))
        bound = {"households_in_universe": universe, "requests": universe,
                 "seconds_max": universe * max(timings_ok), "bytes_max": universe * max(bytes_ok)}
    else:
        universe = sum(1 for accts in hh_list.values() if any(a in rows for a in accts))
        bound = {"households_in_universe": universe, "requests": universe, "seconds_max": None, "bytes_max": None}
    rec = {
        "script": {"file": SCRIPT_REL, "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        "calls": calls,
        "calls_made": len(calls),
        "token_store_used": store,
        "households": households,
        "verdict": {"all_accounts_with_series": all_present,
                    "chain_matches_all": all_chain,
                    "series_complete_all": all_complete},
        "bound": bound,
        "c_credential": {"verdict": cred, "claim": "measured"},
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
    for lab in CALL_ORDER:
        if lab in households:
            states = Counter(e["state"] for e in households[lab]["accounts"])
            print("states %s %s" % (lab, dict(states)))
    print("verdict all_accounts_with_series=%s chain_matches_all=%s series_complete_all=%s" % (
        rec["verdict"]["all_accounts_with_series"], rec["verdict"]["chain_matches_all"], rec["verdict"]["series_complete_all"]))
    print("c_credential verdict=%s token_store_used=%s calls_made=%d" % (cred, store, len(calls)))


if __name__ == "__main__":
    main(sys.argv[1:])
