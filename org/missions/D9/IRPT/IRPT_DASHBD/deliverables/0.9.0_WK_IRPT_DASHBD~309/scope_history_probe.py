"""IRPT_DASHBD round 122, cell DB-i-9 (worker 0.9.0_WK_IRPT_DASHBD~309): the Scope history probe.

Exactly TWO Orion Reporting/Scope POSTs, paced six seconds apart, with NO retry: household A (round 117's household) and
household B (round 120's household). Each POST carries the INNER scope body from orion_selected.requests_for, with
calcGrossOfFees false and a Daily compact breakdown over the household's window: from the earliest non-null accountStartDate
of its accounts in the round-119 roster to 2026-10-13. A 4xx or 5xx answer (or no answer) stops the run at once; a body
over 64 MB stops it as oversize. The POST timeout is 180 seconds.

Mode 1 (default, one live run): the two calls above, the saved 2xx bodies, the record.
Mode 2 (--recompute): NO vendor call. It re-measures the saved private bodies (hist_A.json, hist_B.json, verified by the
sha256 in the record) with the amended rules and rewrites the record; the calls, timings, bytes and the bound stay as measured.

Amended rules (issuer amendment 1 on the worker's rows S2 and S3): the compact breakdown is basedOn Calendar, so a series
has one point per calendar day. Per account with a series: span_days (first to last endDate, inclusive), gap_breaks,
contiguous (no gap and points equal span_days), chain_cumulative_bp (|prod(factor) - 1 - perf| x 1e4). Up to 365 days the
summary is the cumulative return (chain_matches when chain_cumulative_bp <= 0.01). Over 365 days Orion annualizes the summary,
so annualized_residual_bp = |prod(factor)^(365/span_days) - 1 - perf| x 1e4 and annualization_explains when it is at most 10.0.

The record SCOPE_HISTORY_PROBE_R122.json holds digests, counts, verdict words and timings only. The raw bodies stay in the
private folder. The token comes from the estate's own loader and is never printed, logged or written.

Usage: python -I <this file> <repo_root>              (the two live calls)
       python -I <this file> <repo_root> --recompute  (no vendor call; re-measures the saved bodies)
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
ANNUAL_DAYS = 365
ANNUAL_TOL_BP = 10.0
CHAIN_TOL_BP = 0.01
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


def _day(s):
    s = str(s)
    if "/" in s:
        return dt.datetime.strptime(s[:10], "%m/%d/%Y").date()
    return dt.date.fromisoformat(s[:10])


def group_series(body):
    """{account id: (perf, [factors], [endDates])} for the Account groups of one body, in document order."""
    out = {}
    for g in walk(body):
        if g.get("$type") != "calculated-group" or g.get("grouping") != "Account":
            continue
        perf, facs, ends = None, [], []
        for n in walk(g):
            if n is g:
                continue
            if perf is None and n.get("$type") == "calculated-performance" and is_num(n.get("performance")):
                perf = float(n["performance"])
            if is_num(n.get("factor")):
                facs.append(float(n["factor"]))
                ends.append(n.get("endDate"))
        out[key_of(g.get("groupEntityId"))] = (perf, facs, ends)
    return out


def series_measures(perf, facs, ends):
    """(span_days, gap_breaks, contiguous, chain_cumulative_bp, annualized_residual_bp or None); None when the group has no series."""
    if perf is None or not facs:
        return None
    ds = [_day(e) for e in ends]
    span = (ds[-1] - ds[0]).days + 1
    gaps = sum(1 for a, b in zip(ds, ds[1:]) if (b - a).days > 1)
    chain = 1.0
    for f in facs:
        chain *= f
    cum = abs(chain - 1.0 - perf) * 1e4
    ann = round(abs(chain ** (ANNUAL_DAYS / float(span)) - 1.0 - perf) * 1e4, 1) if span > ANNUAL_DAYS and chain > 0 else None
    return span, gaps, (gaps == 0 and len(facs) == span), round(cum, 2), ann


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
    calls, raws = [], {}
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
        calls.append(entry)
        print("call household=%s http_status=%d ok=%s" % (lab, status, ok))
        if not ok:
            break
    return calls, raws


def account_entries(body, accts, rows):
    """One entry per account of a household, in order of account_sha256, under the amended rules."""
    gs = group_series(body)
    out = []
    for a in accts:
        if a not in gs:
            out.append({"account_sha256": dig(a), "state": "NO_GROUP", "points": 0})
            continue
        perf, facs, ends = gs[a]
        m = series_measures(perf, facs, ends)
        if m is None:
            out.append({"account_sha256": dig(a), "state": "GROUP_NO_SERIES", "points": len(facs)})
            continue
        span, gaps, contiguous, cum, ann = m
        e = {"account_sha256": dig(a), "state": "GROUP_WITH_SERIES", "points": len(facs), "span_days": span,
             "gap_breaks": gaps, "contiguous": contiguous, "chain_cumulative_bp": cum}
        if span <= ANNUAL_DAYS:
            e["chain_matches"] = cum <= CHAIN_TOL_BP
        else:
            e["annualized_residual_bp"] = ann
            e["annualization_explains"] = ann is not None and ann <= ANNUAL_TOL_BP
        out.append(e)
    out.sort(key=lambda e: e["account_sha256"])
    return out


def verdict_of(allexp):
    series = [e for e in allexp if e["state"] == "GROUP_WITH_SERIES"]
    return {"all_accounts_with_series": all(e["state"] == "GROUP_WITH_SERIES" for e in allexp),
            "series_contiguous_all": all(e["contiguous"] for e in series),
            "short_series_chain_matches_all": all(e["chain_matches"] for e in series if "chain_matches" in e),
            "long_series_annualization_explains_all": all(e["annualization_explains"] for e in series if "annualization_explains" in e)}


def measure(hhs, windows, rows, raws):
    """Households (for the record) and the verdict, from the saved 2xx bodies only."""
    households, allexp = {}, []
    for lab in CALL_ORDER:
        if lab not in raws:
            continue
        raw_id, accts = hhs[lab]
        body = json.loads(raws[lab].decode("utf-8"))
        entries = account_entries(body, accts, rows)
        households[lab] = {"household_sha256": dig(raw_id), "window_start_sha256": dig(windows[lab]), "accounts": entries}
        allexp.extend(entries)
    return households, verdict_of(allexp)


def credential_of(calls):
    if not calls:
        return "REQUEST_REJECTED"
    if any(c["ok"] for c in calls):
        return "ACCEPTED"
    if all(c["http_status"] in (401, 403) for c in calls):
        return "REFUSED"
    return "REQUEST_REJECTED"


def bound_of(hh_list, rows, calls):
    universe = sum(1 for accts in hh_list.values() if any(a in rows for a in accts))
    ok = [c for c in calls if c["ok"] and "elapsed_s" in c]
    if not ok:
        return {"households_in_universe": universe, "requests": universe, "seconds_max": None, "bytes_max": None}
    return {"households_in_universe": universe, "requests": universe,
            "seconds_max": universe * max(float(c["elapsed_s"]) for c in ok),
            "bytes_max": universe * max(int(c["response_bytes"]) for c in ok)}


def start_offsets(hhs, rows, raws):
    """Counts only, for basis_words: per series account, days from the roster start to the first point, and the span against the calendar days."""
    rep = {}
    for lab in CALL_ORDER:
        if lab not in raws:
            continue
        raw_id, accts = hhs[lab]
        gs = group_series(json.loads(raws[lab].decode("utf-8")))
        rows_out = []
        for a in accts:
            if a not in gs or gs[a][0] is None or not gs[a][1]:
                continue
            perf, facs, ends = gs[a]
            start = _day(rows[a]["accountStartDate"])
            first = _day(ends[0])
            span = series_measures(perf, facs, ends)[0]
            cal = (dt.date.fromisoformat(END) - start).days + 1
            rows_out.append({"offset_days": (first - start).days, "calendar_days_from_start": cal, "span_days": span, "points": len(facs)})
        rep[lab] = rows_out
    return rep


def write_record(root, rec):
    with open(root / REC_REL, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=2, sort_keys=True)
        fh.write("\n")


def script_entry():
    return {"file": SCRIPT_REL, "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def print_summary(hhs_meas, verdict, cred, store, ncalls):
    for lab in CALL_ORDER:
        if lab in hhs_meas:
            print("accounts %s %s" % (lab, dict(Counter(e["state"] for e in hhs_meas[lab]["accounts"]))))
    print("verdict %s" % json.dumps(verdict, sort_keys=True))
    print("c_credential verdict=%s token_store_used=%s calls_made=%d" % (cred, store, ncalls))


def recompute(root):
    """No vendor call: re-measure the saved 2xx bodies with the amended rules; calls, timings, bytes and the bound are kept."""
    rec = json.loads((root / REC_REL).read_text(encoding="utf-8"))
    hh_list, hh_set, rows = load_world()
    hhs, _, _ = pick_households(hh_list, hh_set, rows)
    windows = {lab: window_start(hhs[lab][1], rows) for lab in CALL_ORDER}
    raws = {}
    for c in rec["calls"]:
        if c["ok"]:
            f = c["response_file"]
            raw = Path(f["path"]).read_bytes()
            if sha_bytes(raw) != f["sha256"] or len(raw) != c["response_bytes"]:
                raise SystemExit("saved body differs from the record")
            raws[c["household"]] = raw
    households, verdict = measure(hhs, windows, rows, raws)
    bound = bound_of(hh_list, rows, rec["calls"])
    if bound != rec["bound"]:
        raise SystemExit("bound differs from the stored bound (not rewritten)")
    rec["script"] = script_entry()
    rec["households"] = households
    rec["verdict"] = verdict
    rec["c_credential"] = {"verdict": credential_of(rec["calls"]), "claim": "measured"}
    write_record(root, rec)
    print("recomputed from saved bodies: %s" % ",".join(sorted(raws)))
    print_summary(households, verdict, rec["c_credential"]["verdict"], rec["token_store_used"], len(rec["calls"]))
    for lab, rows_out in start_offsets(hhs, rows, raws).items():
        print("offsets %s %s" % (lab, json.dumps(rows_out, sort_keys=True)))


def live(root):
    Path(PRIV).mkdir(parents=True, exist_ok=True)
    hh_list, hh_set, rows = load_world()
    hhs, ncand, cl_b = pick_households(hh_list, hh_set, rows)
    windows, bodies = {}, {}
    for lab in CALL_ORDER:
        raw_id, accts = hhs[lab]
        windows[lab] = window_start(accts, rows)
        bodies[lab] = build_body(raw_id, accts[0], windows[lab])
    print("candidates_b %d accounts_a %d accounts_b %d" % (ncand, len(hhs["A"][1]), len(hhs["B"][1])))
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
    households, verdict = measure(hhs, windows, rows, raws)
    rec = {
        "script": script_entry(),
        "calls": calls,
        "calls_made": len(calls),
        "token_store_used": store,
        "households": households,
        "verdict": verdict,
        "bound": bound_of(hh_list, rows, calls),
        "c_credential": {"verdict": credential_of(calls), "claim": "measured"},
        "basis_words": BASIS_PENDING,
        "reads": {"vendor_calls": len(calls), "s3_writes": 0, "dynamodb_writes": 0,
                  "secret_reads": secret_reads, "s3_reads": 0},
        "files_in_repo_private": False,
        "served_values_changed": False,
        "pushed": False,
        "deployed": False,
    }
    write_record(root, rec)
    print_summary(households, verdict, rec["c_credential"]["verdict"], store, len(calls))


def main(argv):
    root = Path(argv[0]).resolve() if argv else Path.cwd()
    for d in MODULE_DIRS[:2]:
        sys.path.insert(0, str(root / d))
    for d in MODULE_DIRS[2:]:
        sys.path.append(str(root / d))
    sys.path.append(str(root))
    if "--recompute" in argv[1:]:
        recompute(root)
    else:
        live(root)


if __name__ == "__main__":
    main(sys.argv[1:])
