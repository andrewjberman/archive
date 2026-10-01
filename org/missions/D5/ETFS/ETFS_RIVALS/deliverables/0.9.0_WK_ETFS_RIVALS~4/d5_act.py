"""RIV-d-5 act driver (0.9.0_WK_ETFS_RIVALS~4): GQGU import by marker, Lambda invoke, windowed replay. A driver, not product code:
every address, name, event shape and stage is the product modules'. Run from the tree root.

  bronze                      land the archived GQGU days as issuer bronze (land_bronze fund=GQGU, device identity, S3 read-back)
  markers [--from K]          one fetch-holdings marker per chunk of report dates; waits for the silver + gold markers of each
  invoke <function> '<json>'  synchronous Lambda invoke (prints the request id)
  replay --start S --end E    the canonical-shape Lambda in replay mode, chunked by --days report dates, one batch id per chunk
Nothing here deletes anything.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import time

ARCHIVE = pathlib.Path("C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/amgt-reconn-daily-census-20260929/gqgu")
ACT_DAY = "2026-10-01"
CHUNK = 60


def setup():
    r = pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip())
    for p in (str(r / "data" / "etfs" / "scripts"), str(r)):
        if p not in sys.path:
            sys.path.insert(0, p)
    return r


def days():
    return sorted(p.stem for p in ARCHIVE.glob("????-??-??.json") if p.with_suffix(".txt").exists())


def cmd_bronze(a):
    setup()
    from rivalfunds import collector_issuer, sinks
    s = sinks.S3Sink()
    out, bad = {}, {}
    for d in days():
        side = ARCHIVE / f"{d}.json"
        meta = json.loads(side.read_text(encoding="utf-8"))
        sc = collector_issuer.land_bronze((ARCHIVE / f"{d}.txt").read_bytes(), meta["requested_date"], meta.get("url", ""), s,
                                          captured_at=meta.get("at"), http_status=int(meta.get("http_status", 200)), fund="GQGU")
        out[d] = sc["bronze_uri"]
        if sc.get("status") != "OK":
            bad[d] = sc.get("status")
    pathlib.Path(a.out).write_text(json.dumps({"landed": len(out), "not_ok": bad, "bronze": out}, indent=1), encoding="utf-8")
    print(f"landed {len(out)} days; not OK {bad}; bronze dates {sorted({u.split('date=')[1][:10] for u in out.values()})}")
    return 0 if not bad else 1


def _markers(s, stage, bid):
    from rivalfunds import markers
    return markers.get_marker(stage, ACT_DAY, bid, s)


def cmd_markers(a):
    setup()
    from rivalfunds import markers, sinks
    s = sinks.S3Sink()
    landed = json.loads(pathlib.Path(a.bronze).read_text(encoding="utf-8"))["bronze"]
    ds = sorted(landed)
    chunks = [ds[i:i + CHUNK] for i in range(0, len(ds), CHUNK)]
    print(f"{len(ds)} days, {len(chunks)} chunks")
    for k, ch in enumerate(chunks):
        if k < a.start_at:
            continue
        bid = f"d5-gqgu-{k:02d}"
        outs = [landed[d] for d in ch]
        uri = markers.write_marker("fetch-holdings", ACT_DAY, bid, s,
                                   {"status": "OK", "outputs": outs, "days": {f"GQGU:{d}": "OK" for d in ch}})
        print(f"chunk {k} {ch[0]}..{ch[-1]} ({len(ch)}): marker {uri}", flush=True)
        t0 = time.time()
        want = ("build-silver", "build-canonical-shape", "build-coverage", "build-trade-schedule")
        seen = {}
        while time.time() - t0 < a.wait:
            for st in want:
                if st not in seen:
                    m = _markers(s, st, bid)
                    if m:
                        seen[st] = (m.get("status"), len(m.get("outputs", [])))
            if len(seen) == len(want):
                break
            time.sleep(10)
        print(f"  chain after {time.time() - t0:.0f}s: {seen}", flush=True)
        if "build-silver" not in seen or "build-canonical-shape" not in seen:
            print("  STOP: silver or G1 marker absent")
            return 1
    return 0


def cmd_invoke(a):
    import boto3
    from botocore.config import Config
    lam = boto3.client("lambda", region_name="us-east-1", config=Config(read_timeout=900, connect_timeout=30, retries={"max_attempts": 0}))
    t0 = time.time()
    r = lam.invoke(FunctionName=a.function, InvocationType="RequestResponse", Payload=a.event.encode("utf-8"))
    body = r["Payload"].read().decode("utf-8")
    print(json.dumps({"function": a.function, "request_id": r["ResponseMetadata"]["RequestId"], "status_code": r["StatusCode"],
                      "function_error": r.get("FunctionError"), "seconds": round(time.time() - t0, 1)}))
    print(body[:2500])
    return 0 if r["StatusCode"] == 200 and not r.get("FunctionError") else 1


def cmd_replay(a):
    setup()
    from rivalfunds import homes, silver_bloomberg, sinks
    s = sinks.S3Sink()
    # report dates in scope: the issuer + bloomberg silver partitions in the window (the replay's own scope)
    dates = set()
    for pref in (homes.issuer_silver(""), silver_bloomberg.silver_prefix("")):
        for u in s.list(pref):
            if u.endswith(".parquet") and "date=" in u:
                dates.add(u.split("date=")[1][:10])
    ds = sorted(d for d in dates if a.start <= d <= a.end)
    chunks = [ds[i:i + a.days] for i in range(0, len(ds), a.days)]
    print(f"{len(ds)} report dates in {a.start}..{a.end}, {len(chunks)} chunks")
    results = []
    for k, ch in enumerate(chunks):
        if k < a.start_at:
            continue
        ev = {"date": ACT_DAY, "mode": "replay", "start": ch[0], "end": ch[-1], "batch_id": f"{a.prefix}-{k:02d}"}
        print(f"chunk {k}: {ev}", flush=True)
        ns = argparse.Namespace(function="rivalfunds-build-canonical-shape-lambda", event=json.dumps(ev))
        rc = cmd_invoke(ns)
        results.append((k, rc))
        if rc != 0:
            print("STOP: chunk failed")
            return 1
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("bronze")
    b.add_argument("--out", required=True)
    m = sub.add_parser("markers")
    m.add_argument("--bronze", required=True)
    m.add_argument("--start-at", type=int, default=0)
    m.add_argument("--wait", type=int, default=900)
    i = sub.add_parser("invoke")
    i.add_argument("function")
    i.add_argument("event")
    r = sub.add_parser("replay")
    r.add_argument("--start", required=True)
    r.add_argument("--end", required=True)
    r.add_argument("--days", type=int, default=50)
    r.add_argument("--prefix", default="d5-replay-r4")
    r.add_argument("--start-at", type=int, default=0)
    a = ap.parse_args(argv)
    return {"bronze": cmd_bronze, "markers": cmd_markers, "invoke": cmd_invoke, "replay": cmd_replay}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
