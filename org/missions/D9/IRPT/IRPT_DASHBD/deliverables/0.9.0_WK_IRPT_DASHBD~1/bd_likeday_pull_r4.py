"""TO-DB-b-10 -- ONE Black Diamond pull over Opal's gap-free segments, and the like-day tie-out.

Word: Andrew-direct 2026-10-02 ~13:2xZ card 4 (@0abef798f7): the five round-1 accounts, BD's return over each of Opal's
gap-free segments, at most ONE performancePeriod request per mapped account, run ONCE. No performanceSeries, no other call.

Two modes (usage: python bd_likeday_pull_r4.py <repo_root> plan | pull --go):
  plan   OFFLINE. Reads the served reporting gold (S3 reads) and the roster, builds the gap-free segments and the request
         bodies with the estate's own bd_adapter.build_period_request, prints them and writes BD_LIKEDAY_PLAN_R4.json.
         DRY_RUN stays 1 in this mode, so the estate client REFUSES any network call it might attempt.
  pull   LIVE, needs --go. Rebuilds the plan, requires it equal to the written plan, mints the session bearer once, makes at
         most one performancePeriod POST per mapped account, writes the raw responses under <repo_root>/.scratch/r4/raw/
         (a sanitised copy is made separately) and the records. A credential, cookie or token is never written or printed.

The estate client is REUSED, read-only: bd_adapter.build_period_request / parse_period (infra/aws/lambda/investor-reporting/
performance/) and the helpers it loads from opal-assets-bd49f-reporting-pull (load_bd_session, get_clientview_token,
_request). tenants.VERIFICATION_ROUTES is the 49 Financial Black Diamond route (host, paths, session secret id).
"""
import io
import json
import math
import os
import statistics
import sys
import urllib.error
from pathlib import Path

def _REAL(token):
    """Resolve an acct# token to the real account id at run time from the private evidence dir (outside the repo)."""
    import json as _json
    import os as _os
    d = _os.environ.get("IRPT_PRIVATE_EVIDENCE_DIR")
    if not d:
        raise SystemExit("REFUSE: IRPT_PRIVATE_EVIDENCE_DIR is not set; this historical script needs the private account map")
    p = _os.path.join(d, "account_map_49financial.json")
    if not _os.path.isfile(p):
        raise SystemExit("REFUSE: account_map_49financial.json is absent from IRPT_PRIVATE_EVIDENCE_DIR")
    with open(p, encoding="utf-8") as fh:
        m = _json.load(fh)
    if token not in m:
        raise SystemExit("REFUSE: token %s is not in the account map" % token)
    return m[token]


FIVE = [_REAL("acct#89d0916a"), _REAL("acct#f08ffd13"), _REAL("acct#6b914f88"), _REAL("acct#ffa615d2"), _REAL("acct#d0cf6c92")]
WORD = "@0abef798f7 card 4"
MIN_DAYS = 5
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/"


def load_roster(root):
    import boto3
    s3 = boto3.client("s3", region_name="us-east-1")
    o = s3.get_object(Bucket="opal-data-assets", Key="blackdiamond/49f/_ops/taxsma_roster.json")
    accts = json.loads(o["Body"].read())["accounts"]
    return {a["schwab_account"]: a for a in accts}


def read_gold(root):
    """{account: {date_str: total_return_daily or None}} over every served account_return_daily partition."""
    sys.path.insert(0, str(root))
    from lib import opal_naming as on
    import boto3
    import pyarrow.parquet as pq
    s3 = boto3.client("s3", region_name="us-east-1")
    base = on.address("irpt", "49financial", "gold", "account_return_daily", "date=2026-01-01")
    bucket, key = base[len("s3://"):].split("/", 1)
    pref = key.rsplit("/", 1)[0] + "/"
    dates = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=pref, Delimiter="/"):
        for cp in p.get("CommonPrefixes", []):
            seg = cp["Prefix"].rstrip("/").rsplit("/", 1)[1]
            if seg.startswith("date="):
                dates.append(seg[5:])
    dates.sort()
    out = {a: {} for a in FIVE}

    def one(d):
        k = on.address("irpt", "49financial", "gold", "account_return_daily", "date=" + d)
        kb, kk = k[len("s3://"):].split("/", 1)
        body = s3.get_object(Bucket=kb, Key=kk + "/data.parquet")["Body"].read()
        return pq.read_table(io.BytesIO(body)).to_pylist()

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=16) as ex:
        tables = list(ex.map(one, dates))
    for t in tables:
        for r in t:
            a = r["account_id"]
            if a in out:
                v = r["total_return_daily"]
                out[a][r["business_date"]] = None if (v is None or (isinstance(v, float) and math.isnan(v))) else float(v)
    return out, dates


def segments_for(series, tc):
    """Maximal runs of consecutive trading days with a non-null total_return_daily, length >= MIN_DAYS."""
    if not series:
        return []
    days = tc.trading_days_between(min(series), max(series))
    segs, run = [], []
    for d in days:
        v = series.get(d.isoformat())
        if v is None:
            if run:
                segs.append(run)
            run = []
        else:
            run.append(d)
    if run:
        segs.append(run)
    out = []
    for r in segs:
        if len(r) >= MIN_DAYS:
            twr = 1.0
            for d in r:
                twr *= 1.0 + series[d.isoformat()]
            out.append({"start": r[0].isoformat(), "end": r[-1].isoformat(), "opal_linked_days": len(r), "opal_twr": twr - 1.0})
    return out


def build_plan(root):
    sys.path.insert(0, str(root / "lib"))
    import trading_calendar as tc
    perf = str(root / "infra/aws/lambda/investor-reporting/performance")
    sys.path.insert(0, perf)
    import bd_adapter
    from tenants import verification_route_for, _LEGACY_SHORT_ID
    route = verification_route_for(_LEGACY_SHORT_ID["49F"])
    roster = load_roster(root)
    gold, dates = read_gold(root)
    reqs, unmapped = [], []
    for a in FIVE:
        r = roster.get(a)
        bd = (r or {}).get("bd_internal_id")
        if not bd:
            unmapped.append({"account": a, "reason": "no bd_internal_id in taxsma_roster.json (status %s); never guessed"
                             % ((r or {}).get("status", "absent from roster"))})
            continue
        segs = segments_for(gold[a], tc)
        if not segs:
            unmapped.append({"account": a, "reason": "no gap-free segment of >= %d trading days in the served gold" % MIN_DAYS})
            continue
        first, last = segs[0], segs[-1]
        body, _idx = bd_adapter.build_period_request(
            int(bd), first["start"], first["end"], first["start"], int(last["end"][:4]), "Cumulative")
        body["parameters"]["dateRanges"] = [
            {"endDate": s["end"], "name": "Custom", "startDate": s["start"], "type": "Custom"} for s in segs]
        body["parameters"]["asOfDate"]["asOfDate"] = last["end"]
        reqs.append({"account": a, "bd_account": str(bd), "segments": segs, "body": body})
    return {"route": route.describe(), "gold_partitions": len(dates), "gold_first": dates[0], "gold_last": dates[-1],
            "requests": reqs, "unmapped": unmapped}


def _d(s):
    return None if not s else str(s)[:10]


def find_account_node(resp, bd):
    for k in ("levels", "combinedLevels"):
        for lv in resp.get(k) or []:
            st = [lv]
            while st:
                n = st.pop()
                if (n.get("descriptor") or {}).get("level") == "Account" and \
                        str((n.get("accountInfo") or {}).get("accountId")) == str(bd):
                    return n
                st.extend(n.get("levels") or [])
                st.extend(n.get("combinedLevels") or [])
    return None


def main():
    root = Path(sys.argv[1]).resolve()
    mode = sys.argv[2]
    out_dir = root / D
    if mode == "plan":
        os.environ["DRY_RUN"] = "1"
        plan = build_plan(root)
        (out_dir / "BD_LIKEDAY_PLAN_R4.json").write_text(json.dumps(plan, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print("gold partitions %d (%s..%s)" % (plan["gold_partitions"], plan["gold_first"], plan["gold_last"]))
        for r in plan["requests"]:
            print("REQUEST", r["account"], "bd", r["bd_account"], "ranges", len(r["body"]["parameters"]["dateRanges"]))
            for s in r["segments"]:
                print("   ", s["start"], s["end"], s["opal_linked_days"], "%.6f" % s["opal_twr"])
        for u in plan["unmapped"]:
            print("UNMAPPED", u["account"], u["reason"])
        return
    if mode != "pull" or "--go" not in sys.argv:
        raise SystemExit("ERROR: live mode needs: pull --go")
    plan = build_plan(root)
    written = json.loads((out_dir / "BD_LIKEDAY_PLAN_R4.json").read_text(encoding="utf-8"))
    if json.loads(json.dumps(plan, sort_keys=True)) != written:
        raise SystemExit("ERROR: the live plan differs from the reviewed plan; refusing to call")
    if len(plan["requests"]) > 5:
        raise SystemExit("ERROR: more than 5 requests")
    # The estate client refuses egress while DRY_RUN=1; lift it only here, after the plan is verified equal.
    os.environ["DRY_RUN"] = "0"
    import bd_adapter
    h = bd_adapter.load_bd_helpers(force=True)
    if h.DRY_RUN:
        raise SystemExit("ERROR: helper still DRY")
    path = plan["route"]["paths"]["performancePeriod"]
    raw_dir = root / ".scratch" / "r4" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    cookie = h.load_bd_session()
    token = h.get_clientview_token(cookie)
    retries_left = 1
    records, pairs = [], []
    for r in plan["requests"]:
        status, resp, err = None, None, None
        while True:
            try:
                payload = h._request("POST", path, token=token, body=r["body"], raw=True)
                status, resp = 200, json.loads(payload)
                (raw_dir / ("RAW_BD_PERIOD_%s.json" % r["account"])).write_bytes(payload)
                break
            except RuntimeError as e:  # HTTP error from the estate client: record the status, no retry
                msg = str(e)
                status = int(msg.split("HTTP ")[1].split(":")[0]) if "HTTP " in msg else -1
                err = msg[:160]
                break
            except (urllib.error.URLError, OSError, TimeoutError) as e:  # transport error: one retry in the whole run
                err = "transport: %s" % type(e).__name__
                if retries_left > 0:
                    retries_left -= 1
                    records.append({"account": r["account"], "retry": 1})
                    continue
                status = 0
                break
        rec = {"account": r["account"], "bd_account": r["bd_account"],
               "ranges": [{"start": s["start"], "end": s["end"]} for s in r["segments"]], "http_status": status}
        if err:
            rec["error"] = err
        records.append(rec)
        node = find_account_node(resp, r["bd_account"]) if resp else None
        pts = {}
        if node:
            for p in node.get("dateRangePoints") or []:
                dr = p.get("dateRange") or {}
                pts[(_d(dr.get("startDate")), _d(dr.get("endDate")))] = p
        for s in r["segments"]:
            p = pts.get((s["start"], s["end"]))
            twr = (p or {}).get("timeWeightedReturns") or {}
            bd_twr, held = twr.get("return"), twr.get("daysHeld")
            if held is None and p:
                held = p.get("daysHeld")
            like = held is not None and int(held) == s["opal_linked_days"]
            pair = {"account": r["account"], "bd_account": r["bd_account"], "start": s["start"], "end": s["end"],
                    "opal_linked_days": s["opal_linked_days"], "bd_days_held": held, "like_days": bool(like),
                    "opal_twr": s["opal_twr"], "bd_twr": bd_twr,
                    "abs_diff": (abs(s["opal_twr"] - bd_twr) if (bd_twr is not None) else None)}
            if p is None:
                pair["note"] = "BD returned no dateRangePoint for this exact range"
            pairs.append(pair)
    reqs = [x for x in records if "retry" not in x]
    retries = sum(1 for x in records if "retry" in x)
    pull = {"word": WORD, "endpoint": "performancePeriod", "accounts_in_scope": FIVE, "requests": reqs,
            "vendor_calls": len(reqs), "transport_retries": retries, "session_token_mints": 1,
            "unmapped": plan["unmapped"]}
    (out_dir / "BD_LIKEDAY_PULL_R4.json").write_text(json.dumps(pull, indent=1) + "\n", encoding="utf-8")
    liked = [p for p in pairs if p["like_days"]]
    diffs = sorted(p["abs_diff"] for p in liked)
    summary = {"pairs": len(pairs), "like_day_pairs": len(liked), "unlike_day_pairs": len(pairs) - len(liked),
               "coverage_like_over_all": "%d of %d" % (len(liked), len(pairs)),
               "median_abs_diff": statistics.median(diffs) if diffs else None,
               "max_abs_diff": max(diffs) if diffs else None}
    tie = {"pairs": pairs, "like_day_pairs": len(liked), "summary": summary}
    (out_dir / "TIEOUT_49F_BLACKDIAMOND_R4.json").write_text(json.dumps(tie, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"vendor_calls": pull["vendor_calls"], "retries": retries,
                      "statuses": [(x["account"], x["http_status"]) for x in reqs], "summary": summary}, indent=1))


if __name__ == "__main__":
    main()
