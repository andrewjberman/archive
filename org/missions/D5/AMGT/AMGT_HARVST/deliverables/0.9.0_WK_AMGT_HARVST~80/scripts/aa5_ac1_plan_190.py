"""HVST-aa-5 AC1: pre-run PLAN of listing pages per publisher per name over the 190 names.
NO request to any publisher, NO S3 write. Runs the collector's own `plan` command
(python -m lib.opal_data_harvest plan --security-json <name> --publishers <p> --floor 2026-01-01 --with-watermark)
in-process (main() with argv) under a socket guard that records every host resolved and refuses any
non-AWS host. S3 GET/LIST only (watermark; stored SA listings for MEASURED basis)."""
import contextlib
import importlib.util
import io
import json
import os
import socket
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
sys.path.insert(0, str(ROOT))
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True

HOSTS = []
PUB_BLOCKED = []
_real_gai = socket.getaddrinfo


def _guard(host, *a, **k):
    h = str(host)
    HOSTS.append(h)
    if not (h.endswith("amazonaws.com") or h.endswith("amazonaws.com.cn") or h in ("localhost", "127.0.0.1")
            or h.startswith("169.254.")):
        PUB_BLOCKED.append(h)
        raise OSError("aa5 guard: non-AWS host refused: " + h)
    return _real_gai(host, *a, **k)


socket.getaddrinfo = _guard

import boto3  # noqa: E402
import lib.research.harvest.store as store  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "n5", ROOT / "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~59/scripts/n5_ac1_backfill_plan.py")
n5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n5)
from lib.opal_data_harvest import __main__ as coll  # noqa: E402

DELIV = ROOT / "org/missions/D5/AMGT/AMGT_HARVST/deliverables"
UNIVERSE = DELIV / "0.9.0_WK_AMGT_HARVST~46/securities.universe.json"
OUT = DELIV / "0.9.0_WK_AMGT_HARVST~80/aa5_plan_190.json"
PUBS = ["bbg", "wsj", "ft", "barrons", "sa"]
LENOVO_KEY = "992_HK_Equity"

client = boto3.client("s3", region_name="us-east-1")
held = n5.stored_listings(client)
cache = {}
real = store.silver_latest


def memo(source, table, fields, client=None):
    k = (source, table, tuple(fields))
    if k not in cache:
        cache[k] = real(source, table, fields, client=client or boto3.client("s3", region_name="us-east-1"))
    return cache[k]


store.silver_latest = memo

universe = [s for s in json.loads(UNIVERSE.read_text(encoding="utf-8")) if s["key"] != LENOVO_KEY]
assert len(universe) == 190, len(universe)
tmp = Path(tempfile.mkdtemp())
names = []
per_pub = {p: {"pages": 0, "measured": 0, "default": 0} for p in PUBS}
for sec in universe:
    (tmp / "s.json").write_text(json.dumps(sec), encoding="utf-8")
    row = {"key": sec["key"], "publishers": {}}
    for pub in PUBS:
        sys.argv = ["opal_data_harvest", "plan", "--security-json", str(tmp / "s.json"), "--publishers", pub,
                    "--floor", "2026-01-01", "--with-watermark"]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = coll.main()
        assert rc == 0
        line = json.loads(buf.getvalue().splitlines()[0])
        cap = line["planned_listing_pages"]
        pages, basis = cap, "DEFAULT"
        if pub == "sa":
            for method, q in n5.candidate_queries(pub, sec):
                h = held.get((pub, n5.sha(q)))
                if h:
                    meta = h[1]["sa_meta"] if 1 in h else None
                    if meta and meta.get("totalPages"):
                        pages, basis = min(cap, int(meta["totalPages"])), "MEASURED"
                    break
        row["publishers"][pub] = {"plan_line": line, "pages": pages, "basis": basis}
        per_pub[pub]["pages"] += pages
        per_pub[pub]["measured" if basis == "MEASURED" else "default"] += 1
    names.append(row)

grand = sum(v["pages"] for v in per_pub.values())
n_lines = sum(len(r["publishers"]) for r in names)
doc = {"to_id": "AMGT_HARVST.TO-HVST-aa-5.pre-run-listing-page-print-190-names", "floor": "2026-01-01",
       "names": len(names), "plan_lines": n_lines, "per_publisher_totals": per_pub,
       "planned_listing_pages_ceiling": grand, "publisher_hosts_refused": PUB_BLOCKED,
       "hosts_resolved": sorted(set(HOSTS)), "rows": names}
OUT.write_text(json.dumps(doc, indent=1), encoding="utf-8")
print("PLAN LINES: %d = %d names x %d publishers (denominator 190 x 5 = 950)" % (n_lines, len(names), len(PUBS)))
for p in PUBS:
    v = per_pub[p]
    print("%-8s pages=%5d  basis MEASURED=%d DEFAULT=%d" % (p, v["pages"], v["measured"], v["default"]))
print("hosts resolved: %s" % sorted(set(HOSTS)))
print("PLANNED LISTING PAGES CEILING: %d" % grand)
print("NETWORK CALLS TO PUBLISHERS: %d" % len(PUB_BLOCKED))
