"""RIV-d-3 act driver (0.9.0_WK_ETFS_RIVALS~5): the import of both capture sets, in date-ordered chunks, plus the G3 import.

Run from the tree root. Every command takes --sink: `s3` is the act, `local:<dir>` is the rehearsal (a local mirror of the served
state, no served write). It is a driver, not product code: every address, name, event shape and stage is the product modules'.

  counts                              print the capture-file counts (gate 6) and the chunk plan
  mirror <dir>                        mirror the served rivalfunds + issuer state into <dir> (read-only against S3)
  g3 --sink S                         enrichment_bloomberg import over dividends.json (G3 BEFORE any G5, row W3-S13)
  chunk <k> --sink S [--chain]        collector_bloomberg import of chunk k (a batch, a marker). With --chain and a local sink the
                                      downstream stages run in process, as the marker rules would run them in AWS.

The S3 sink wrapper (CachedS3Sink) is the one departure from the product's sink: land_capture asks "is this sha already in this
acquisition partition" by listing the partition and GETting every sidecar, once per capture, and all captures of a census share one or
two acquisition dates, so 937 captures would cost ~440,000 GETs. The wrapper caches sidecar GETs (a sidecar is immutable once written)
and still read-backs every PUT from the wire. Row ETFS_RIVALS-Z-W5-... (surprise channel) records it.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import glob
import json
import pathlib
import subprocess
import sys
import time

RUNTIME = pathlib.Path("C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime")
SETS = (("idvz", RUNTIME / "etfs-rivals-idvz-20260930" / "daily"),
        ("pfoe", RUNTIME / "amgt-reconn-daily-census-20260929"))
DIVIDENDS = RUNTIME / "etfs-rivals-idvz-20260930" / "dividends.json"
CHUNK_DAYS = 60  # requested dates per batch
BUCKET = "opal-data-etfs"
ACT_DAY = "2026-09-30"  # the ET act day


def root() -> pathlib.Path:
    return pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                                       check=True).stdout.strip())


def setup():
    r = root()
    for p in (str(r / "data" / "etfs" / "scripts"), str(r)):
        if p not in sys.path:
            sys.path.insert(0, p)
    return r


def capture_files():
    """{set: [path, ...]} of the dated capture files (YYYY-MM-DD.json) of each census directory."""
    out = {}
    for name, d in SETS:
        out[name] = sorted(pathlib.Path(p) for p in glob.glob(str(d / "20??-??-??.json")))
    return out


def chunks(n_days=CHUNK_DAYS):
    """Date-ordered chunks: [{"k", "dates": [...], "files": [path, ...], "marker_date"}, ...]; one chunk holds every file of
    its requested dates from BOTH sets, so a chunk's G1 dates see every fund of the day."""
    by_date = {}
    for _, files in capture_files().items():
        for f in files:
            by_date.setdefault(f.stem, []).append(f)
    dates = sorted(by_date)
    out = []
    for i in range(0, len(dates), n_days):
        ds = dates[i:i + n_days]
        out.append({"k": len(out), "dates": ds, "files": [f for d in ds for f in sorted(by_date[d])], "marker_date": ds[-1]})
    return out


def cmd_counts(a):
    cf_ = capture_files()
    allf = [f for fs in cf_.values() for f in fs]
    print("capture files (dated *.json, one real Excel BQL response each):")
    for name, d in SETS:
        raw = len(list(d.iterdir()))
        print(f"  {name}: {len(cf_[name])} dated captures ({raw} entries in {d})")
    print(f"  TOTAL {len(allf)} captures to import (order text: 503 + 441 = 944; 503 and 444 are the directory entries, which include run.json, runs.jsonl, coverage files and the basg/gqgu probe folders)")
    ch = chunks(a.days)
    print(f"chunk plan: {len(ch)} batches of <= {a.days} requested dates: " +
          ", ".join(f"#{c['k']}:{c['dates'][0]}..{c['dates'][-1]}({len(c['files'])}f)" for c in ch))
    return 0


def _s3():
    import boto3
    return boto3.client("s3", region_name="us-east-1")


def cmd_mirror(a):
    setup()
    s3 = _s3()
    dest = pathlib.Path(a.dir)
    prefixes = ["issuer-site/etfs/bronze/", "issuer-site/etfs/silver/", "rivalfunds/etfs/gold/", "rivalfunds/etfs/platinum/",
                "rivalfunds/etfs/state/", "bloomberg/etfs/"]
    keys = [o["Key"] for pf in prefixes for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=pf)
            for o in pg.get("Contents", [])]

    def get(k):
        d = dest / BUCKET / k
        d.parent.mkdir(parents=True, exist_ok=True)
        s3.download_file(BUCKET, k, str(d))

    with cf.ThreadPoolExecutor(16) as ex:
        list(ex.map(get, keys))
    print(f"mirrored {len(keys)} objects into {dest}")
    return 0


def make_sink(spec):
    """'s3' -> CachedS3Sink; 'local:<dir>' -> the product's local sink."""
    setup()
    from rivalfunds import sinks
    if spec != "s3":
        return sinks.get_sink(spec)

    class CachedS3Sink(sinks.S3Sink):
        """S3Sink with sidecar GETs cached. PUT still reads back from the wire (the cache is bypassed for the read-back)."""

        def __init__(self):
            super().__init__()
            self.cache = {}

        def get(self, uri):
            if uri.endswith(".sidecar.json") and uri in self.cache:
                return self.cache[uri]
            data = super().get(uri)
            if uri.endswith(".sidecar.json"):
                self.cache[uri] = data
            return data

        def put(self, uri, data, content_type=None):
            bucket, key = sinks.split_uri(uri)
            kw = {"ContentType": content_type} if content_type else {}
            self.client.put_object(Bucket=bucket, Key=key, Body=data, **kw)
            back = sinks.S3Sink.get(self, uri)  # the wire, never the cache
            if back != data:
                raise sinks.ReadBackError(f"read-back mismatch on {uri}")
            if uri.endswith(".sidecar.json"):
                self.cache[uri] = data
            return uri

    return CachedS3Sink()


def cmd_g3(a):
    setup()
    from rivalfunds import enrichment_bloomberg as eb
    s = make_sink(a.sink)
    ev = {"mode": "import", "dividends_json": str(DIVIDENDS), "batch_id": a.batch_id, "sink": s}
    t0 = time.time()
    res = eb.handler_entry(ev)
    print(json.dumps({k: res[k] for k in ("status", "batch_id", "outputs", "marker", "detail")}, default=str)[:1500])
    print(f"seconds={time.time() - t0:.1f}")
    return 0 if res["status"] == "OK" else 1


def cmd_chunk(a):
    setup()
    from rivalfunds import collector_bloomberg as cb
    from rivalfunds import silver_bloomberg, sweep
    ch = chunks(a.days)
    c = ch[a.k]
    s = make_sink(a.sink)
    bid = f"import-r2-{c['k']:02d}"
    # every batch's marker partitions on the ACT day (not the batch's own last date): the chain's publish-page then writes its page
    # under the act day's partition (revisions kept) and never mints a historical page the gateway's archive would list
    mdate = a.act_day
    ev = {"mode": "import", "captures": [str(f) for f in c["files"]], "date": mdate, "batch_id": bid, "sink": s}
    t0 = time.time()
    res = cb.handler_entry(ev)
    print(f"chunk {c['k']} {c['dates'][0]}..{c['dates'][-1]}: import status={res['status']} files={len(c['files'])} "
          f"outputs={len(res['outputs'])} marker={res['marker']} seconds={time.time() - t0:.1f}")
    if res["status"] not in ("OK", "PARTIAL") or not res["marker"]:
        print(json.dumps(res["detail"], default=str)[:1500])
        return 1
    if a.chain and a.sink.startswith("local:"):
        evd = {"date": mdate, "mode": "daily", "batch_id": bid, "sink": a.sink}
        t1 = time.time()
        sv = silver_bloomberg.handler_entry(dict(evd))
        print(f"  silver status={sv['status']} outputs={len(sv['outputs'])} marker={bool(sv['marker'])} seconds={time.time() - t1:.1f}")
        if not sv["marker"]:
            print(json.dumps(sv["detail"], default=str)[:1500])
            return 1
        t2 = time.time()
        g = sweep.run_gold_chain(dict(evd))
        print(f"  gold chain status={g['status']} outputs={len(g['outputs'])} detail={g['detail']} seconds={time.time() - t2:.1f}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("counts")
    c.add_argument("--days", type=int, default=CHUNK_DAYS)
    m = sub.add_parser("mirror")
    m.add_argument("dir")
    g = sub.add_parser("g3")
    g.add_argument("--sink", required=True)
    g.add_argument("--batch-id", default="import-r2-g3")
    k = sub.add_parser("chunk")
    k.add_argument("k", type=int)
    k.add_argument("--sink", required=True)
    k.add_argument("--days", type=int, default=CHUNK_DAYS)
    k.add_argument("--chain", action="store_true")
    k.add_argument("--act-day", default=ACT_DAY)
    a = ap.parse_args(argv)
    return {"counts": cmd_counts, "mirror": cmd_mirror, "g3": cmd_g3, "chunk": cmd_chunk}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
