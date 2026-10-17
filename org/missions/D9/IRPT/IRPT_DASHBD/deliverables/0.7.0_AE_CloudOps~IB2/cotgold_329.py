"""IRPT_DASHBD TO-DB-b-329 (applier 0.7.0_AE_CloudOps~IB2): the Cottonwood 2026-07-27 gold rewrite and republish: the reads, the events and the record.

  python cotgold_329.py gates | before | dry | rewrite | prewrite | pubdry | canary | full | after | compile

Every event is ONE synchronous invoke (never retried here). Account ids live in memory only; an account is named by the first 12 hex of the sha256 of its id.
Counts, digests, hashes and words only are printed or written.
"""
import base64
import datetime as dt
import hashlib
import io
import json
import re
import sys
from pathlib import Path

import boto3
from botocore.config import Config

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cotc0_318 as c0  # noqa: E402
import fill328 as f  # noqa: E402  (git, open_legs_on_surface, invoke shape)

HERE = Path(__file__).resolve().parent
STATE = HERE / "state329"
ROOT = c0.ROOT
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
PACKET = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_GOLD_REWRITE_20260727_AND_REPUBLISH.md"
COO_HALF = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_COTTONWOOD_GOLD_REWRITE_20260727_AND_REPUBLISH_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_GOLD_REWRITE_20260727_AND_REPUBLISH_CTO_HALF.md"
PACKET_SHA = "8596f43f1d0f06ba3944da6640c490c19e8440bc3426ec367f32e550b6b9252e"
SLUG = "irpt-dashbd-cottonwood-gold-rewrite-20260727-and-republish-20261017"
DAY, NEXT_DAY, FULL_DAY = "2026-07-27", "2026-07-28", "2026-07-21"
GOLD_FN, PUB_FN = "irpt-cot-account-return-daily-lambda", "irpt-cot-reporting-publish-lambda"
GOLD_CODE, PUB_CODE = "+iYXakKx7zhK33lv6W0jDAY1QsLYUNqNCuHHIA7owD0=", "vYNB1EBTU2qEIINxTnhYQBBBEHBYFId7lllrIJM3YRE="
BUCKET, GOLD_PREFIX, PUB_PREFIX = "opal-data-cottonwood", "irpt/cottonwood/gold/account_return_daily/", "irpt/cottonwood/platinum/reporting/"
SCHEDS = {"account_return_daily": "irpt-cot-account-return-daily-daily", "publish_daily": "irpt-cot-reporting-publish-daily"}
SURFACE = (GOLD_FN, PUB_FN, "irpt/cottonwood/gold/account_return_daily", "irpt/cottonwood/platinum/reporting")
MOVABLE = ("total_return_daily", "day_quality", "return_basis")
s3 = boto3.client("s3", region_name="us-east-1")
sch = boto3.client("scheduler", region_name="us-east-1")
lam_cfg = boto3.client("lambda", region_name="us-east-1")
LAM = boto3.client("lambda", region_name="us-east-1", config=Config(read_timeout=900, connect_timeout=15, retries={"max_attempts": 0, "mode": "standard"}))


def save(name, obj):
    STATE.mkdir(exist_ok=True)
    (STATE / name).write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="ascii")


def load(name):
    return json.loads((STATE / name).read_text(encoding="ascii"))


def d12(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def gold_objects():
    """Every parquet object of the gold table: [(key, version_count)] and the versions overall."""
    keys = {}
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=GOLD_PREFIX):
        for v in pg.get("Versions", []):
            if v["Key"].endswith(".parquet"):
                keys[v["Key"]] = keys.get(v["Key"], 0) + 1
    return keys


def parquet_rows(key, vid=None):
    import pyarrow.parquet as pq
    kw = {"Bucket": BUCKET, "Key": key}
    if vid:
        kw["VersionId"] = vid
    return pq.ParquetFile(io.BytesIO(s3.get_object(**kw)["Body"].read())).metadata.num_rows


def day_object(day):
    out = [o["Key"] for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=GOLD_PREFIX + "date=%s/" % day) for o in pg.get("Contents", []) if o["Key"].endswith(".parquet")]
    return out


def day_versions(key):
    vs = [v for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=key) for v in pg.get("Versions", []) if v["Key"] == key]
    return sorted(vs, key=lambda v: v["LastModified"], reverse=True)


def series_counts():
    prefixes = []
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PUB_PREFIX, Delimiter="/"):
        prefixes += [c["Prefix"] for c in pg.get("CommonPrefixes", []) if "/account=" in c["Prefix"]]
    vers = 0
    keys = set()
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=PUB_PREFIX):
        for v in pg.get("Versions", []):
            vers += 1
            keys.add(v["Key"])
    return len(prefixes), len(keys), vers, sorted(prefixes)


def scheds():
    return {k: sch.get_schedule(Name=n)["State"] for k, n in SCHEDS.items()}


def gold_totals():
    objs = gold_objects()
    total = 0
    for k in objs:
        total += parquet_rows(k)
    return len(objs), sum(objs.values()), total


def cmd_gates():
    sha = hashlib.sha256((ROOT / PACKET).read_bytes()).hexdigest()
    coo, cto = (ROOT / COO_HALF).read_text(encoding="utf-8"), (ROOT / CTO_HALF).read_text(encoding="utf-8")
    coo_ok, cto_ok = "SIGNED" in coo and PACKET_SHA in coo, "SIGNED" in cto and PACKET_SHA[:8] in cto
    f.SURFACE, f.SLUG = SURFACE, SLUG
    nw, nfiles, found = f.open_legs_on_surface()
    g, p = lam_cfg.get_function_configuration(FunctionName=GOLD_FN), lam_cfg.get_function_configuration(FunctionName=PUB_FN)
    sc = scheds()
    key = day_object(DAY)
    live_ok = (g["CodeSha256"] == GOLD_CODE and p["CodeSha256"] == PUB_CODE and sc == {"account_return_daily": "ENABLED", "publish_daily": "DISABLED"} and len(key) == 1 and parquet_rows(key[0]) == 3)
    print("GATES packet_sha_ok=%s coo=%s cto=%s" % (sha == PACKET_SHA, coo_ok, cto_ok))
    print("GATES worktrees_read=%d marker_files_read=%d open_legs_on_this_surface=%d %s" % (nw, nfiles, len(found), found))
    print("GATES live: gold_code_ok=%s pub_code_ok=%s schedules=%s day_objects=%d day_rows=%s -> live_matches_packet=%s" % (g["CodeSha256"] == GOLD_CODE, p["CodeSha256"] == PUB_CODE, sc, len(key), parquet_rows(key[0]) if key else None, live_ok))
    save("gates.json", {"packet_sha256": sha, "coo_half_signed": coo_ok, "cto_half_signed": cto_ok, "one_change_at_a_time": {"worktrees_read": nw, "open_markers_naming_this_surface": len(found)}, "live_matches_packet": bool(live_ok)})
    return 0 if (sha == PACKET_SHA and coo_ok and cto_ok and not found and live_ok) else 3


def cmd_before():
    key = day_object(DAY)[0]
    vs = day_versions(key)
    full = day_object(FULL_DAY)
    nobj, nver, total = gold_totals()
    prefixes, sobj, sver, _ = series_counts()
    parts = {k.split("/")[-2] for k in gold_objects()}
    out = {"day_rows": parquet_rows(key), "day_objects": 1, "day_versions": len(vs), "full_day_rows": parquet_rows(full[0]) if full else None, "gold_total_rows": total, "partitions": len(parts),
           "series_prefixes": prefixes, "series_objects": sobj, "series_versions": sver, "gold_code_sha256": lam_cfg.get_function_configuration(FunctionName=GOLD_FN)["CodeSha256"],
           "publish_code_sha256": lam_cfg.get_function_configuration(FunctionName=PUB_FN)["CodeSha256"], "schedules": scheds()}
    save("before.json", out)
    save("before_gold_layout.json", {"gold_objects": nobj, "gold_versions": nver, "per_partition_versions": {k.split("/")[-2]: v for k, v in gold_objects().items()}})
    print("BEFORE", json.dumps(out, sort_keys=True), "| gold parquet objects %d versions %d (denominator printed)" % (nobj, nver))
    return 0


def invoke(fn, payload):
    t = c0.now_utc()
    resp = LAM.invoke(FunctionName=fn, InvocationType="RequestResponse", LogType="Tail", Payload=json.dumps(payload).encode("utf-8"))
    body = json.loads(resp["Payload"].read().decode("utf-8"))
    ltxt = base64.b64decode(resp.get("LogResult", "")).decode("utf-8", "replace") if resp.get("LogResult") else ""
    m = re.search(r"Duration: ([0-9.]+) ms.*?Memory Size: (\d+) MB\s+Max Memory Used: (\d+) MB", ltxt, re.S)
    rep = {"duration_s": round(float(m.group(1)) / 1000.0, 1) if m else None, "max_memory_mb": int(m.group(3)) if m else None}
    fl = {"timed_out": "Task timed out" in ltxt, "access_denied": "AccessDenied" in ltxt, "function_error": resp.get("FunctionError"), "request_id": resp["ResponseMetadata"]["RequestId"], "invoked_utc": t}
    return body, rep, fl


def shape(body):
    """Keys and short scalar values of a response, for reading its structure (the gold and publish responses carry counts)."""
    if not isinstance(body, dict):
        return type(body).__name__
    return {k: (v if isinstance(v, (int, float, bool, type(None))) or (isinstance(v, str) and len(v) < 60) else "%s[%d]" % (type(v).__name__, len(v)) if hasattr(v, "__len__") else type(v).__name__) for k, v in body.items()}


def weekday_window():
    tt = dt.datetime.now(dt.timezone.utc)
    return tt.weekday() < 5 and dt.time(12, 5) <= tt.time() <= dt.time(13, 15)


def event_result(body):
    """The one day's result of a rewrite response: (ok, days, held, rows). The rows are read from results[DAY]; its structure is printed as keys and counts."""
    res = (body.get("results") or {}).get(DAY)
    rows = None
    if isinstance(res, dict):
        for k in ("rows", "row_count", "n_rows", "written_rows"):
            if isinstance(res.get(k), int):
                rows = res[k]
                break
    elif isinstance(res, int):
        rows = res
    return body.get("ok"), body.get("days"), body.get("held"), rows, (shape(res) if res is not None else None)


def cmd_dry():
    first = STATE / "dry_invoke.json"
    if (STATE / "dry.json").exists():
        print("REFUSED: the dry run is already recorded")
        return 2
    if first.exists() and not (STATE / "dry_invoke_first.json").exists():
        first.rename(STATE / "dry_invoke_first.json")  # the first dry run's rows were not kept (only the response shape): disclosed in the record
    if weekday_window():
        print("STOP: inside the weekday fire window")
        return 3
    go0 = gold_objects()
    body, rep, fl = invoke(GOLD_FN, {"rewrite": {"start": DAY, "end": DAY}, "dry_run": True})
    go1 = gold_objects()
    ok, days, held, rows, rshape = event_result(body)
    rec = {"ok": ok, "days": days, "held": held, "rows": rows, "gold_objects_before": len(go0), "gold_objects_after": len(go1), "gold_versions_before": sum(go0.values()), "gold_versions_after": sum(go1.values())}
    save("dry_invoke.json", {"body_shape": shape(body), "result_shape": rshape, "report": rep, "flags": fl, "record": rec})
    print("DRY record=%s result_shape=%s report=%s flags=%s" % (json.dumps(rec, sort_keys=True), json.dumps(rshape, sort_keys=True), rep, {k: v for k, v in fl.items() if k in ("timed_out", "access_denied", "function_error")}))
    problems = []
    if fl["timed_out"] or fl["access_denied"] or fl["function_error"] or (rep["max_memory_mb"] or 0) > 819 or (rep["duration_s"] or 0) > 600:
        problems.append("timeout, AccessDenied, error, memory above 819 MB or duration above 600 s")
    if held != 0 or days != [DAY] or ok is not True or rows is None or not 840 <= rows <= 920:
        problems.append("held/days/ok/rows outside the band (840 to 920)")
    if rec["gold_objects_before"] != rec["gold_objects_after"] or rec["gold_versions_before"] != rec["gold_versions_after"]:
        problems.append("gold objects or versions moved on a dry run")
    print("DRY PROBLEMS:", problems or "none")
    if not problems:
        save("dry.json", rec)
    return 0 if not problems else 3


if __name__ == "__main__":
    c = sys.argv[1]
    fn = {"gates": cmd_gates, "before": cmd_before, "dry": cmd_dry}
    sys.exit(fn[c]())
