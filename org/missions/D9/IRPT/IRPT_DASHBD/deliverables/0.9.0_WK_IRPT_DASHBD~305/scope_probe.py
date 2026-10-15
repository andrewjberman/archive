"""IRPT_DASHBD round 117, cell DB-i-5 (worker 0.9.0_WK_IRPT_DASHBD~305): the Orion Reporting/Scope probe.

One Inflection household with 2 or more accounts (the lowest-sha256 such household in the private account
dimension), one Scope POST with the Account grouping and calcGrossOfFees false, then true, over 2026-10-01
to 2026-10-13. A vendor READ: no AWS write, no deploy, no push. Each 2xx body is saved to the private folder
only. This script prints verdict words and counts, never a token, an identifier or a figure.

Usage: python -I <this file> <repo_root>
"""
import copy
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

DIM = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~171/ACCOUNT_DIM_DRY_RUN.parquet"
PRIV = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~305/"
START = "2026-10-01"
END = "2026-10-13"
MODULE_DIRS = ("infra/aws/lambda/investor-reporting/performance", "infra/aws/lambda/inf-pipeline/inf-performance-daily")
MAX_CALLS = 4
PACE_S = 6          # at least 5 seconds between calls
RETRY_WAIT_S = 15   # a timeout or a 5xx is retried once per flag after 15 seconds
MIN_REMAINING_S = 120
MAX_BYTES = 16 * 1024 * 1024
CANON_ACCOUNT = "probe-household"


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


def household():
    import pyarrow.parquet as pq
    rows = pq.read_table(DIM, columns=["account_id", "household_id"]).to_pylist()
    hh = {}
    for r in rows:
        a, h = key_of(r["account_id"]), key_of(r["household_id"])
        if a and h:
            hh.setdefault(h, set()).add(a)
    multi = {h: s for h, s in hh.items() if len(s) >= 2}
    if not multi:
        raise SystemExit("no household with 2 or more accounts")
    best = min(multi, key=lambda h: hashlib.sha256(h.encode("utf-8")).hexdigest())
    return best, sorted(multi[best])


def build_bodies(household_id, first_account):
    import orion_selected
    import tenants
    mapping = {"firm_id": tenants._CANONICAL_INF, "canonical_account_id": CANON_ACCOUNT,
               "vendor_account_id": int(first_account), "vendor_household_id": int(household_id)}
    false_body = orion_selected.requests_for(mapping, CANON_ACCOUNT, START, END)
    option = false_body["scope"]["calculations"][0]["contextChange"]["performanceOption"]
    if option.get("calcGrossOfFees") is not False:
        raise SystemExit("fee flag path does not hold calcGrossOfFees false")
    true_body = copy.deepcopy(false_body)
    true_body["scope"]["calculations"][0]["contextChange"]["performanceOption"]["calcGrossOfFees"] = True
    return false_body, true_body, tenants.route_for(tenants._LEGACY_SHORT_ID["INF"]).url("scope")


def _error_code(exc):
    response = getattr(exc, "response", None)
    if isinstance(response, dict):
        return str(response.get("Error", {}).get("Code", ""))
    return ""


def load_token():
    reads = {"secret_reads": 0, "s3_reads": 0}
    import orion_live
    reads["secret_reads"] += 1
    try:
        return orion_live.orion_session_jwt(), "secretsmanager", reads
    except Exception as exc:
        print("secretsmanager read refused: %s %s" % (type(exc).__name__, _error_code(exc)))
    import jwt_freshness
    reads["s3_reads"] += 1
    try:
        return jwt_freshness._load_from_s3(), "s3_copy", reads
    except Exception as exc:
        print("s3 copy read refused: %s %s" % (type(exc).__name__, _error_code(exc)))
        return None, "none", reads


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


def run_calls(url, token, false_body, true_body):
    calls, raws = [], {}
    stop = False
    for flag, body in ((False, false_body), (True, true_body)):
        if stop:
            break
        attempt = 0
        while True:
            if calls:
                time.sleep(RETRY_WAIT_S if attempt else PACE_S)
            status, raw = post(url, token, body)
            ok = 200 <= status < 300
            entry = {"gross_of_fees_flag": flag, "http_status": status, "ok": ok}
            if ok and raw is not None:
                # written at once, so an interrupted run cannot lose a response it already received
                path = PRIV + ("scope_true.json" if flag else "scope_false.json")
                with open(path, "wb") as fh:
                    fh.write(raw)
                entry["response_file"] = {"path": path, "sha256": hashlib.sha256(raw).hexdigest()}
                raws[flag] = raw
            calls.append(entry)
            attempt += 1
            if status in (401, 403):
                stop = True
                break
            retryable = status == 0 or status >= 500
            if retryable and attempt == 1:
                continue
            break
    if len(calls) > MAX_CALLS:
        raise SystemExit("call cap exceeded")
    return calls, raws


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


def verdict_a(grp, account_ids):
    ids = set(grp)
    if not ids:
        return "OTHER_GROUPS"
    if ids == set(account_ids) and all(g["perf"] is not None and g["points"] >= 1 for g in grp.values()):
        return "ONE_GROUP_PER_ACCOUNT"
    if ids < set(account_ids):
        return "FEWER_GROUPS"
    return "OTHER_GROUPS"


def verdict_b(gf, gt):
    ids = sorted(set(gf) & set(gt))
    pairs = [(gf[i], gt[i]) for i in ids if gf[i]["perf"] is not None and gt[i]["perf"] is not None]
    if not pairs:
        return "NOT_RUN", 0, 0
    if all(abs(t["perf"] - f["perf"]) < 1e-12 for f, t in pairs):
        return "IGNORED", len(pairs), sum(1 for f, _ in pairs if f["fee"] > 0)
    fee_pairs = [(f, t) for f, t in pairs if f["fee"] > 0]
    ties = 0
    for f, t in fee_pairs:
        obs = t["perf"] - f["perf"]
        if f["startv"] is None or f["startv"] <= 0 or obs < 0:
            return "DIFFERENT_UNTIED", len(pairs), len(fee_pairs)
        exp = f["fee"] / f["startv"]
        if abs(obs - exp) <= max(1e-4, 0.25 * abs(exp)):
            ties += 1
        else:
            return "DIFFERENT_UNTIED", len(pairs), len(fee_pairs)
    return ("NET_WHEN_FALSE" if ties >= 1 else "DIFFERENT_UNTIED"), len(pairs), len(fee_pairs)


def verdicts(calls, raws, accounts):
    import_bodies = {flag: json.loads(raw.decode("utf-8")) for flag, raw in raws.items()}
    all_refused = all(not c["ok"] for c in calls)
    if False in import_bodies:
        gf = groups(import_bodies[False])
        va = verdict_a(gf, accounts)
        a = {"verdict": va, "claim": "measured", "account_groups_returned": len(gf),
             "groups_with_daily_series": sum(1 for g in gf.values() if g["points"] >= 1)}
    else:
        va = "REFUSED" if all_refused else "NOT_RUN"
        a = {"verdict": va, "claim": "measured" if va == "REFUSED" else "absent",
             "account_groups_returned": 0, "groups_with_daily_series": 0}
    if False in import_bodies and True in import_bodies:
        vb, ncmp, nfee = verdict_b(groups(import_bodies[False]), groups(import_bodies[True]))
    else:
        vb, ncmp, nfee = "NOT_RUN", 0, 0
    b = {"verdict": vb, "claim": "absent" if vb == "NOT_RUN" else "measured",
         "accounts_compared": ncmp, "accounts_with_fee": nfee}
    any_ok_false = any(c["ok"] and c["gross_of_fees_flag"] is False for c in calls)
    vc = "ACCEPTED" if any_ok_false else ("REFUSED" if all_refused else "NOT_RUN")
    c = {"verdict": vc, "claim": "absent" if vc == "NOT_RUN" else "measured"}
    return a, b, c


def main(argv):
    root = Path(argv[0]).resolve() if argv else Path.cwd()
    for d in MODULE_DIRS:
        sys.path.insert(0, str(root / d))
    os.makedirs(PRIV, exist_ok=True)
    hh_id, accounts = household()
    hh_sha = hashlib.sha256(hh_id.encode("utf-8")).hexdigest()
    false_body, true_body, url = build_bodies(hh_id, accounts[0])
    token, store, reads = load_token()
    calls, raws = [], {}
    if token is None:
        print("no token: no vendor call made")
    else:
        from jwt_freshness import _decode_jwt_exp
        remaining = _decode_jwt_exp(token) - time.time()
        if remaining < MIN_REMAINING_S:
            print("session near expiry or expired: no vendor call made")
        else:
            calls, raws = run_calls(url, token, false_body, true_body)
    token = None
    listed = calls
    a, b, c = verdicts(calls, raws, accounts) if calls else (
        {"verdict": "NOT_RUN", "claim": "absent", "account_groups_returned": 0, "groups_with_daily_series": 0},
        {"verdict": "NOT_RUN", "claim": "absent", "accounts_compared": 0, "accounts_with_fee": 0},
        {"verdict": "NOT_RUN", "claim": "absent"})
    summary = {"household_sha256": hh_sha, "accounts_in_household": len(accounts), "token_store_used": store,
               "reads": reads, "calls": listed, "a_multi_account": a, "b_fee_basis": b, "c_credential": c,
               "script_run": "scope_probe.py"}
    with open(PRIV + "probe_summary.json", "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
    print("household_sha256 %s accounts_in_household %d token_store_used %s" % (hh_sha, len(accounts), store))
    for i, c_ in enumerate(listed, 1):
        print("call %d flag=%s http_status=%d ok=%s" % (i, c_["gross_of_fees_flag"], c_["http_status"], c_["ok"]))
    print("a_multi_account verdict=%s groups=%d groups_with_daily_series=%d" % (
        a["verdict"], a["account_groups_returned"], a["groups_with_daily_series"]))
    print("b_fee_basis verdict=%s accounts_compared=%d accounts_with_fee=%d" % (
        b["verdict"], b["accounts_compared"], b["accounts_with_fee"]))
    print("c_credential verdict=%s" % c["verdict"])


if __name__ == "__main__":
    main(sys.argv[1:])
