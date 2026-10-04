"""TO-DB-b-20 -- the ONE Black Diamond population pull over Opal's gap-free segments (E3 / P-5): its script and its OFFLINE plan.

Word: Andrew-direct 2026-10-04 ~22:0xZ card 2 (@66f1e98e98): ONE performancePeriod pull across every 49 Financial account in the
served reporting gold, scoped to Opal's gap-free segments, graded against 0.35 pp, no second pull. Run shape ruled by
1.0.0_SA_CTO RULINGS batch 245 (msg 105012): one run, one bearer, about 2 requests/s, abort on the first non-transient error, one
transient retry, no credential in any log, responses landed at the builder's address.

Fork of the round-4 script (bd_likeday_pull_r4.py). Usage: python bd_population_pull_e3.py <repo_root> plan | pull --go
  plan   OFFLINE. Reads the served reporting gold and the xref silver (S3 reads only), maps each Schwab account to its Black
         Diamond internal id by the resolver's tier-1 rule (taxsma_resolver.py:8-9, int(bd_account_id[3:]), no vendor call),
         builds the gap-free segments and request bodies with the estate's bd_adapter.build_period_request, and writes
         BD_POPULATION_PLAN_E3.json. DRY_RUN stays 1: the estate client refuses any network call. vendor_calls is 0.
  pull   LIVE, needs --go, and is NEVER run by the worker that built it. Refuses unless: --go is given; no pull record
         (BD_POPULATION_PULL_E3.json) exists (no second pull); E3_SHAPE_RULING.json exists beside this file and names the CTO
         ruling id, the pace and the abort rule; the rebuilt plan equals the written plan (hash). Then it mints the bearer once,
         paces the requests, sends each account exactly once, lands each raw response at the builder's address, and writes the
         pull record. A credential, cookie or token is never written or printed.
"""
import hashlib
import io
import json
import math
import os
import sys
import time
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

WORD = "66f1e98e98 card 2"
MIN_DAYS = 5
HERE = Path(__file__).resolve().parent
PLAN_NAME = "BD_POPULATION_PLAN_E3.json"
PULL_NAME = "BD_POPULATION_PULL_E3.json"
RULING_NAME = "E3_SHAPE_RULING.json"
XREF_BUCKET = "opal-data-assets"
XREF_PREFIX = "blackdiamond/49f/silver/dim_account_xref/"
TRANSIENT_HTTP = (429, 502, 503, 504)


def _address(on, pull, acct_id):
    return on.address("blackdiamond", "49financial", "bronze", "reporting_performance", "pull=" + pull,
                      object="acct=%s.json" % acct_id)


def normalize_schwab(acct):
    """The estate's exact key (taxsma_registry.normalize_schwab): digits only, zero-padded to 10, else None (never fuzzy)."""
    s = str(acct).strip().replace("-", "")
    if not s.isdigit() or len(s) > 10:
        return None
    return s.zfill(10)


def load_xref():
    """{schwab_account_id: [bd_account_id, ...]} over every row of the newest dim_account_xref partition, plus its key."""
    import boto3
    import pyarrow.parquet as pq
    s3 = boto3.client("s3", region_name="us-east-1")
    keys = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=XREF_BUCKET, Prefix=XREF_PREFIX):
        keys += [o["Key"] for o in p.get("Contents", []) if o["Key"].endswith("data.parquet")]
    if not keys:
        raise SystemExit("ERROR: no dim_account_xref data.parquet under s3://%s/%s" % (XREF_BUCKET, XREF_PREFIX))
    key = max(keys)
    body = s3.get_object(Bucket=XREF_BUCKET, Key=key)["Body"].read()
    rows = pq.read_table(io.BytesIO(body), columns=["schwab_account_id", "bd_account_id"]).to_pylist()
    out = {}
    for r in rows:
        out.setdefault(str(r["schwab_account_id"]), []).append(str(r["bd_account_id"]).strip())
    return out, key


def map_account(acct, xref):
    """(bd_internal_id | None, reason | None). The resolver's tier-1 rule, exact, fail-loud, never guessed."""
    k = normalize_schwab(acct)
    if k is None:
        return None, "account id %r is not a 10-digit-or-shorter all-digit Schwab number; never guessed" % acct
    hits = xref.get(k, [])
    if not hits:
        return None, "not in dim_account_xref (tier-1 exhausted; tier-2/3 need an egress word, none used); never guessed"
    if len(hits) > 1:
        return None, "%d xref rows for this account (exact must be 1); refusing to pick one" % len(hits)
    bd = hits[0]
    if len(bd) < 4 or not (bd[0] == "z" and bd[1:3].isdigit() and bd[3:].isdigit()):
        return None, "bd_account_id %r is not the z<NN><digits> shape; refusing to derive an id by guessing" % bd
    return int(bd[3:]), None


def read_gold(root):
    """({account: {date_str: total_return_daily or None}}, dates) over every served account_return_daily partition."""
    sys.path.insert(0, str(root))
    from lib import opal_naming as on
    import boto3
    import pyarrow.parquet as pq
    from botocore.config import Config
    s3 = boto3.client("s3", region_name="us-east-1", config=Config(
        read_timeout=60, retries={"max_attempts": 8, "mode": "standard"}, max_pool_connections=16))
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
    if not dates:
        raise SystemExit("ERROR: no served account_return_daily partitions under s3://%s/%s" % (bucket, pref))
    out = {}

    def one(d):
        k = on.address("irpt", "49financial", "gold", "account_return_daily", "date=" + d)
        kb, kk = k[len("s3://"):].split("/", 1)
        for attempt in range(6):  # body reads are outside botocore's retry; an S3 READ is safe to repeat
            try:
                body = s3.get_object(Bucket=kb, Key=kk + "/data.parquet")["Body"].read()
                break
            except Exception:
                if attempt == 5:
                    raise
                time.sleep(2 * (attempt + 1))
        return pq.read_table(io.BytesIO(body)).to_pylist()

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=8) as ex:
        tables = list(ex.map(one, dates))
    for t in tables:
        for r in t:
            v = r["total_return_daily"]
            out.setdefault(r["account_id"], {})[r["business_date"]] = \
                None if (v is None or (isinstance(v, float) and math.isnan(v))) else float(v)
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
    sys.path.insert(0, str(root))
    from lib import opal_naming as on
    perf = str(root / "infra/aws/lambda/investor-reporting/performance")
    sys.path.insert(0, perf)
    import bd_adapter
    from tenants import verification_route_for, _LEGACY_SHORT_ID
    route = verification_route_for(_LEGACY_SHORT_ID["49F"])
    xref, xref_key = load_xref()
    gold, dates = read_gold(root)
    accounts = sorted(gold)
    reqs, unmapped, mapped, no_seg, seg_counts = [], [], [], [], {}
    by_bd = {}
    resolved = {}
    for a in accounts:
        bd, why = map_account(a, xref)
        if bd is None:
            unmapped.append({"account": a, "reason": why})
        else:
            resolved[a] = bd
            by_bd.setdefault(bd, []).append(a)
    for bd, accs in by_bd.items():  # two accounts onto one internal id would share one landing key: never guess which
        if len(accs) > 1:
            for a in accs:
                del resolved[a]
                unmapped.append({"account": a, "reason": "bd internal id %d is shared by %d gold accounts; refusing to guess" % (bd, len(accs))})
    unmapped.sort(key=lambda u: u["account"])
    for a in accounts:
        if a not in resolved:
            continue
        bd = resolved[a]
        mapped.append({"account": a, "bd_internal_id": bd})
        segs = segments_for(gold[a], tc)
        seg_counts[a] = len(segs)
        if not segs:
            no_seg.append({"account": a, "reason": "mapped, but no gap-free segment of >= %d trading days in the served gold" % MIN_DAYS})
            continue
        first, last = segs[0], segs[-1]
        body, _idx = bd_adapter.build_period_request(
            int(bd), first["start"], first["end"], first["start"], int(last["end"][:4]), "Cumulative")
        body["parameters"]["dateRanges"] = [
            {"endDate": s["end"], "name": "Custom", "startDate": s["start"], "type": "Custom"} for s in segs]
        body["parameters"]["asOfDate"]["asOfDate"] = last["end"]
        reqs.append({"account": a, "bd_account": str(bd), "segments": segs, "body": body,
                     "landing_key_pattern": _address(on, "<YYYYMMDD>", bd)})
    sha = hashlib.sha256(json.dumps([r["body"] for r in reqs], sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    return {"word": WORD, "dry_run": 1, "vendor_calls": 0, "route": route.describe(),
            "gold_partitions": len(dates), "gold_first": dates[0], "gold_last": dates[-1], "xref_partition": xref_key,
            "accounts_total": len(accounts), "mapped": len(mapped), "unmapped": unmapped,
            "mapped_without_segment": no_seg, "requests": len(reqs), "request_bodies_sha256": sha,
            "segment_counts": seg_counts, "landing_template": _address(on, "<YYYYMMDD>", "<bd_internal_id>"),
            "request_list": reqs}


def _d(s):
    return None if not s else str(s)[:10]


def _canon(plan):
    return json.loads(json.dumps(plan, sort_keys=True))


def refusal_checks(out_dir, argv):
    """Every refusal that needs no network. Returns the parsed shape ruling."""
    if len(argv) < 3 or argv[2] != "pull" or "--go" not in argv:
        raise SystemExit("ERROR: live mode needs: pull --go")
    if (out_dir / PULL_NAME).exists():
        raise SystemExit("ERROR: a pull record %s already exists; no second pull" % PULL_NAME)
    rp = out_dir / RULING_NAME
    if not rp.is_file():
        raise SystemExit("ERROR: %s missing beside the script; the CTO's shape ruling is required" % RULING_NAME)
    ruling = json.loads(rp.read_text(encoding="utf-8"))
    for k in ("ruling_id", "pace_rps", "abort_rule"):
        if not ruling.get(k):
            raise SystemExit("ERROR: %s must name %s" % (RULING_NAME, k))
    float(ruling["pace_rps"])
    return ruling


def main(argv=None):
    argv = list(sys.argv if argv is None else argv)
    root = Path(argv[1]).resolve()
    mode = argv[2] if len(argv) > 2 else ""
    out_dir = HERE
    if mode == "plan":
        os.environ["DRY_RUN"] = "1"
        plan = build_plan(root)
        (out_dir / PLAN_NAME).write_text(json.dumps(plan, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print("gold partitions %d (%s..%s); xref %s" % (plan["gold_partitions"], plan["gold_first"], plan["gold_last"], plan["xref_partition"]))
        print("accounts_total %d mapped %d unmapped %d requests %d vendor_calls %d" % (
            plan["accounts_total"], plan["mapped"], len(plan["unmapped"]), plan["requests"], plan["vendor_calls"]))
        print("request_bodies_sha256", plan["request_bodies_sha256"])
        for u in plan["unmapped"]:
            print("UNMAPPED", u["account"], u["reason"])
        return 0
    ruling = refusal_checks(out_dir, argv)
    pp = out_dir / PLAN_NAME
    if not pp.is_file():
        raise SystemExit("ERROR: no written plan %s; run plan first" % PLAN_NAME)
    written = json.loads(pp.read_text(encoding="utf-8"))
    os.environ["DRY_RUN"] = "1"
    plan = build_plan(root)
    if _canon(plan) != written:
        raise SystemExit("ERROR: the live plan hash differs from the reviewed plan; refusing to call")
    if len(plan["request_list"]) != plan["requests"] or plan["requests"] > plan["mapped"]:
        raise SystemExit("ERROR: request count does not match the plan")
    # The estate client refuses egress while DRY_RUN=1; lift it only here, after every refusal passed.
    os.environ["DRY_RUN"] = "0"
    import bd_adapter
    h = bd_adapter.load_bd_helpers(force=True)
    if h.DRY_RUN:
        raise SystemExit("ERROR: helper still DRY")
    import boto3
    sys.path.insert(0, str(root))
    from lib import opal_naming as on
    s3 = boto3.client("s3", region_name="us-east-1")
    path = plan["route"]["paths"]["performancePeriod"]
    pull_date = datetime.now(timezone.utc).strftime("%Y%m%d")
    interval = 1.0 / float(ruling["pace_rps"])
    cookie = h.load_bd_session()
    token = h.get_clientview_token(cookie)
    retries_left = 1
    records, aborted, last_t = [], None, 0.0
    seen = set()
    for r in plan["request_list"]:
        if r["account"] in seen:
            raise SystemExit("ERROR: account %s requested twice" % r["account"])
        seen.add(r["account"])
        wait = last_t + interval - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        rec = {"account": r["account"], "bd_account": r["bd_account"], "ranges": len(r["segments"])}
        while True:
            last_t = time.monotonic()
            try:
                payload = h._request("POST", path, token=token, body=r["body"], raw=True)
                rec["http_status"] = 200
                try:  # a landing failure is non-transient and is recorded, so the pull record always exists after a call
                    json.loads(payload)
                    addr = _address(on, pull_date, r["bd_account"])
                    bkt, key = addr[len("s3://"):].split("/", 1)
                    s3.put_object(Bucket=bkt, Key=key, Body=payload, ContentType="application/json")
                    rec["landed"] = addr
                except Exception as e:
                    rec["error"] = "landing: %s" % type(e).__name__
                    aborted = rec["error"]
                break
            except RuntimeError as e:  # HTTP error from the estate client; only the status code is kept, never the body
                msg = str(e)
                status = int(msg.split("HTTP ")[1].split(":")[0]) if "HTTP " in msg else -1
                rec.update({"http_status": status, "error": "HTTP %d" % status})
                if status in TRANSIENT_HTTP and retries_left > 0:
                    retries_left -= 1
                    rec["retried"] = True
                    time.sleep(interval)
                    continue
                aborted = rec["error"]
                break
            except (urllib.error.URLError, OSError, TimeoutError) as e:  # transport error
                rec.update({"http_status": 0, "error": "transport: %s" % type(e).__name__})
                if retries_left > 0:
                    retries_left -= 1
                    rec["retried"] = True
                    time.sleep(interval)
                    continue
                aborted = rec["error"]
                break
        records.append(rec)
        if aborted:
            break
    pull = {"word": WORD, "endpoint": "performancePeriod", "ruling_id": ruling["ruling_id"], "pace_rps": ruling["pace_rps"],
            "pull_date": pull_date, "session_token_mints": 1, "requests_planned": plan["requests"],
            "vendor_calls": len(records), "aborted": aborted, "retries_used": 1 - retries_left,
            "plan_sha256": plan["request_bodies_sha256"], "records": records, "unmapped": plan["unmapped"]}
    (out_dir / PULL_NAME).write_text(json.dumps(pull, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"vendor_calls": pull["vendor_calls"], "aborted": aborted, "retries_used": pull["retries_used"],
                      "landed": sum(1 for x in records if x.get("landed"))}, indent=1))
    return 1 if aborted else 0


if __name__ == "__main__":
    sys.exit(main())
