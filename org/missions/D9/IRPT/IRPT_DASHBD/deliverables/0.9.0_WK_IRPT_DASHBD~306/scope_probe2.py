"""IRPT_DASHBD round 118, cell DB-i-6 (worker 0.9.0_WK_IRPT_DASHBD~306): the second Orion Scope probe.

The round-117 household (the lowest-sha256 household with 2 or more accounts in the private account dimension),
one Scope POST per call with the INNER scope body (requests_for(...)["scope"]), the fee flag false then true over
2026-07-01 to 2026-09-30 (q3). A second pair over 2026-01-01 to 2026-09-30 (ytd) is made only when the q3 pair
completed with both 2xx answers and compared no account with a fee above 0. A non-2xx answer stops the run at once.
No retry. Pacing 6 seconds between calls. A read of the newest fact_positions partition through the GET-only
reader gives the account TYPE and REGISTRATION categories of the short accounts; nothing else is read from it.

A vendor READ: no AWS write, no deploy, no push. Each 2xx body is saved to the private folder only. The run prints
verdict words and counts, never a token, an account or household id, or a value. It writes the repo record
(SCOPE_PROBE2_R118.json, in the deliverables folder) with the basis words left for the worker to fill in.

Usage: python -I <this file> <repo_root>
"""
import copy
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ENDPOINT = "https://api.cloud.orionadvisor.com/api/v1/Reporting/Scope"
DIM = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~171/ACCOUNT_DIM_DRY_RUN.parquet"
CACHE = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~174/work/positions_daily_cache.parquet"
PRIV = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~306/"
SCRIPT_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~306/scope_probe2.py"
REC_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~306/SCOPE_PROBE2_R118.json"
R117_HH_SHA = "00328ce57bbc14b33bd6695bc8eb32cdf2fb5f3a7d89ec14a42825e15d39df60"
MODULE_DIRS = ("infra/aws/lambda/investor-reporting/performance", "infra/aws/lambda/inf-pipeline/inf-performance-daily",
               "data/assets/scripts/gold/irpt_reporting/adapters", "lib")
FP_TABLE = "s3://opal-data-assets/orion/inflection/silver/fact_positions"
WINDOWS = {"q3": ("2026-07-01", "2026-09-30"), "ytd": ("2026-01-01", "2026-09-30")}
CANON_ACCOUNT = "probe-household"
PACE_S = 6
MIN_REMAINING_S = 120
MAX_BYTES = 16 * 1024 * 1024
MAX_CALLS = 4
PRIOR_S3_READS = 14     # the two exploration runs of the same partition before this run (7 reads each)
ABSENT = "ABSENT"


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


def verdict_b2(gf, gt):
    v, ncmp, nfee = verdict_b(gf, gt)
    if v == "DIFFERENT_UNTIED" and nfee == 0:
        v = "NO_FEE_IN_WINDOW"
    return v, ncmp, nfee


def coverage(grp, account_ids):
    missing = sorted(set(account_ids) - set(grp))
    sless = sorted(i for i in account_ids if i in grp and (grp[i]["perf"] is None or grp[i]["points"] < 1))
    return len(grp), sum(1 for g in grp.values() if g["perf"] is not None and g["points"] >= 1), missing, sless


def digest(account_id):
    return hashlib.sha256(account_id.encode("utf-8")).hexdigest()


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


def build_bodies(household_id, first_account, window):
    import orion_selected
    import tenants
    start, end = WINDOWS[window]
    mapping = {"firm_id": tenants._CANONICAL_INF, "canonical_account_id": CANON_ACCOUNT,
               "vendor_account_id": int(first_account), "vendor_household_id": int(household_id)}
    wrapper = orion_selected.requests_for(mapping, CANON_ACCOUNT, start, end)
    false_body = wrapper["scope"]
    option = false_body["calculations"][0]["contextChange"]["performanceOption"]
    if option.get("calcGrossOfFees") is not False:
        raise SystemExit("fee flag path does not hold calcGrossOfFees false")
    true_body = copy.deepcopy(false_body)
    true_body["calculations"][0]["contextChange"]["performanceOption"]["calcGrossOfFees"] = True
    url = tenants.route_for(tenants._LEGACY_SHORT_ID["INF"]).url("scope")
    if url != ENDPOINT:
        raise SystemExit("endpoint differs from the one Scope path")
    return false_body, true_body, url


def _error_code(exc):
    response = getattr(exc, "response", None)
    if isinstance(response, dict):
        return str(response.get("Error", {}).get("Code", ""))
    return ""


def load_token():
    """The estate's own Secrets Manager loader only. An IAM refusal is recorded and the run stops (no S3 fallback)."""
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


class Run:
    def __init__(self, url, token):
        self.url, self.token = url, token
        self.calls, self.bodies, self.attempted = [], {}, []

    def call(self, window, flag, body):
        if self.calls:
            time.sleep(PACE_S)
        status, raw = post(self.url, self.token, body)
        ok = 200 <= status < 300
        entry = {"window": window, "gross_of_fees_flag": flag, "http_status": status, "ok": ok}
        if ok and raw is not None:
            path = PRIV + "scope_%s_%s.json" % (window, "true" if flag else "false")
            with open(path, "wb") as fh:
                fh.write(raw)
            entry["response_file"] = {"path": path, "sha256": hashlib.sha256(raw).hexdigest()}
            self.bodies[(window, flag)] = json.loads(raw.decode("utf-8"))
        self.calls.append(entry)
        return ok


def class_table(accounts):
    """(accountType, registrationType) per household account, from the newest fact_positions partition (GET only)."""
    from inflection_account_dim import InflectionSilverReader
    rd = InflectionSilverReader()
    name, frame = rd.latest_partition(FP_TABLE)
    wanted = set(accounts)
    seen = {}
    for acc, typ, reg in zip(frame["accountId"], frame["accountType"], frame["registrationType"]):
        k = key_of(acc)
        if k in wanted:
            seen.setdefault(k, set()).add((str(typ).strip(), str(reg).strip()))
    out = {}
    for a in accounts:
        pairs = seen.get(a)
        if not pairs:
            out[a] = (ABSENT, ABSENT)
        elif len(pairs) == 1:
            out[a] = next(iter(pairs))
        else:
            out[a] = ("MULTI", "MULTI")
    return name, out, rd.reads


def position_days(account_id, window):
    import pyarrow.compute as pc
    import pyarrow.parquet as pq
    lo, hi = window
    t = pq.read_table(CACHE, columns=["acc", "date"])
    t = t.filter(pc.and_(pc.greater_equal(t["date"], lo), pc.less_equal(t["date"], hi)))
    return sum(1 for a in t["acc"].to_pylist() if key_of(a) == account_id)


def cause(account_id, days, cls, series_classes):
    if days == 0:
        return "NO_POSITIONS_IN_WINDOW"
    if cls == ABSENT or not series_classes:
        return "NOT_DETERMINED"
    if cls not in series_classes:
        return "ACCOUNT_CLASS_EXCLUDED_BY_VENDOR"
    return "NOT_DETERMINED"


def main(argv):
    root = Path(argv[0]).resolve() if argv else Path.cwd()
    for d in MODULE_DIRS[:2]:
        sys.path.insert(0, str(root / d))
    for d in MODULE_DIRS[2:]:
        sys.path.append(str(root / d))
    Path(PRIV).mkdir(parents=True, exist_ok=True)
    hh_id, accounts = household()
    hh_sha = digest(hh_id)
    if hh_sha != R117_HH_SHA:
        raise SystemExit("household differs from round 117's household digest")
    false_q3, true_q3, url = build_bodies(hh_id, accounts[0], "q3")
    secret_reads = 1
    token = load_token()
    store = "secretsmanager" if token is not None else "none"
    run = Run(url, token)
    if token is None:
        print("no token: no vendor call made")
    else:
        from jwt_freshness import _decode_jwt_exp
        remaining = _decode_jwt_exp(token) - time.time()
        if remaining < MIN_REMAINING_S:
            print("session near expiry or expired: no vendor call made")
        else:
            # q3 pair: flag false then true; any non-2xx stops the cell at once
            if run.call("q3", False, false_q3) and run.call("q3", True, true_q3):
                gf = groups(run.bodies[("q3", False)])
                gt = groups(run.bodies[("q3", True)])
                _, _, nfee_q3 = verdict_b2(gf, gt)
                if nfee_q3 == 0:
                    ytd_false, ytd_true, _ = build_bodies(hh_id, accounts[0], "ytd")
                    if run.call("ytd", False, ytd_false):
                        run.call("ytd", True, ytd_true)
    token = None
    calls = run.calls
    windows_run = [w for w in WINDOWS if any(c["window"] == w for c in calls)]
    # (c) credential
    any_ok_false = any(c["ok"] and c["gross_of_fees_flag"] is False for c in calls)
    all_refused = all(not c["ok"] for c in calls)
    all_auth = all(c["http_status"] in (401, 403) for c in calls)
    vc = "ACCEPTED" if any_ok_false else (("REFUSED" if all_auth else "REQUEST_REJECTED") if all_refused else "NOT_RUN")
    c_cred = {"verdict": vc, "claim": "absent" if vc == "NOT_RUN" else "measured"}
    # (i) coverage per window run
    cov, shorts_by_window = {}, {}
    for w in windows_run:
        if (w, False) in run.bodies:
            ngr, nser, miss, sl = coverage(groups(run.bodies[(w, False)]), accounts)
            shorts_by_window[w] = ({i: "NO_GROUP" for i in miss}, {i: "GROUP_NO_SERIES" for i in sl})
            cov[w] = {"account_groups_returned": ngr, "groups_with_series": nser,
                      "missing_account_sha256": [digest(i) for i in miss],
                      "series_less_account_sha256": [digest(i) for i in sl],
                      "verdict": "ALL_COVERED" if not miss and not sl else "SHORT"}
        else:
            cov[w] = {"account_groups_returned": 0, "groups_with_series": 0, "missing_account_sha256": [],
                      "series_less_account_sha256": [], "verdict": "NOT_RUN"}
    # (ii) fee basis: the q3 pair, or the ytd pair when it exists
    pairs = {}
    for w in windows_run:
        if (w, False) in run.bodies and (w, True) in run.bodies:
            pairs[w] = verdict_b2(groups(run.bodies[(w, False)]), groups(run.bodies[(w, True)]))
    if not pairs:
        bv, pair, ncmp, nfee = "NOT_RUN", None, 0, 0
    else:
        pair = "ytd" if "ytd" in pairs else "q3"
        bv, ncmp, nfee = pairs[pair]
    b_fee = {"verdict": bv, "pair": pair, "accounts_compared": ncmp, "accounts_with_fee": nfee,
             "claim": "absent" if bv == "NOT_RUN" else "measured"}
    # (iii) short accounts of the q3 window, with the category read and the cause class
    short_accounts, detail = [], []
    if "q3" in shorts_by_window:
        miss_map, sless_map = shorts_by_window["q3"]
        gq = groups(run.bodies[("q3", False)])
        series_ids = {i for i in accounts if i in gq and gq[i]["perf"] is not None and gq[i]["points"] >= 1}
        part_name, classes, run_reads = class_table(accounts)
        series_classes = {classes[i] for i in series_ids}
        for aid, role in list(miss_map.items()) + list(sless_map.items()):
            days = position_days(aid, WINDOWS["q3"])
            cls = classes[aid]
            cz = cause(aid, days, cls, series_classes)
            short_accounts.append({"account_sha256": digest(aid), "role": role,
                                   "position_days_in_window": days,
                                   "account_type_class": cls[0], "registration_class": cls[1],
                                   "cause_class": cz, "claim": "inferred", "words": "PENDING"})
            detail.append((digest(aid)[:12], role, days, cls[0], cls[1], cz))
        fp_partition = part_name
    else:
        run_reads, fp_partition = 0, None
    s3_reads = PRIOR_S3_READS + run_reads
    # the record: one file, the script's own hash, words to be filled by the worker
    rec = {
        "script": {"file": SCRIPT_REL, "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        "household_sha256": hh_sha,
        "accounts_in_household": len(accounts),
        "windows": {w: {"start": WINDOWS[w][0], "end": WINDOWS[w][1]} for w in windows_run},
        "calls": calls,
        "calls_made": len(calls),
        "token_store_used": store,
        "coverage": cov,
        "b_fee_basis": b_fee,
        "c_credential": c_cred,
        "short_accounts": short_accounts,
        "basis_words": "PENDING",
        "reads": {"vendor_calls": len(calls), "s3_writes": 0, "dynamodb_writes": 0,
                  "secret_reads": secret_reads, "s3_reads": s3_reads},
        "files_in_repo_private": False,
        "served_values_changed": False,
        "pushed": False,
        "deployed": False,
    }
    with open(Path(root) / REC_REL, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=2, sort_keys=True)
        fh.write("\n")
    with open(PRIV + "probe2_summary.json", "w", encoding="utf-8") as fh:
        json.dump({"record": rec, "fact_positions_partition": fp_partition}, fh, indent=2, sort_keys=True)
    # verdict words and counts only
    print("household_sha256 %s accounts_in_household %d token_store_used %s" % (hh_sha, len(accounts), store))
    for c in calls:
        print("call window=%s flag=%s http_status=%d ok=%s" % (c["window"], c["gross_of_fees_flag"], c["http_status"], c["ok"]))
    for w in windows_run:
        e = cov[w]
        print("coverage %s verdict=%s groups=%d groups_with_series=%d missing=%d series_less=%d" % (
            w, e["verdict"], e["account_groups_returned"], e["groups_with_series"],
            len(e["missing_account_sha256"]), len(e["series_less_account_sha256"])))
    print("b_fee_basis verdict=%s pair=%s accounts_compared=%d accounts_with_fee=%d" % (bv, pair, ncmp, nfee))
    print("c_credential verdict=%s" % vc)
    for row in detail:
        print("short digest=%s role=%s position_days=%d type=%s registration=%s cause=%s" % row)
    print("fact_positions partition read: %s, reader reads this run %d" % (fp_partition, run_reads))


if __name__ == "__main__":
    main(sys.argv[1:])
