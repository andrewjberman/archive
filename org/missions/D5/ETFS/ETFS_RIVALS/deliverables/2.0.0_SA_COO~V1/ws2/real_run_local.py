"""ETFS_RIVALS workstreams 2-3 -- the issuer's ONE REAL RUN, on live inputs with LOCAL writes only.

    python real_run_local.py <code root> <day> <out dir> [--no-search]

Overlay sink (round 26's): reads live S3, writes only under <out dir>/layer. Nothing is written to S3 and nothing deploys.
  1. build-trade-schedule, mode replay, over the 40 days before <day> (RIV-wd-1's rules on the real reports).
  2. The dramatic-move lookup (RIV-wb-1) over the market closes of the 30 days before <day>: each candidate is searched
     on the web (Bright Data SERP; BRIGHT_DATA_API_KEY and BD_SERP_ZONE from the environment) and a found action is
     written as an INFERRED corporate-action row, locally. `--no-search` skips the search.
  3. publish-page, mode replay, for <day>, reading everything through the overlay (RIV-wa-1, wc-1, wc-2 and the hookup).
The page and the audit page land under <out dir>/layer; their paths and a run record are printed and written to
<out dir>/real_run_local.json.
"""
import datetime as dt
import io
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(sys.argv[1]).resolve()
DAY, OUT = sys.argv[2], pathlib.Path(sys.argv[3]).resolve()
SEARCH = "--no-search" not in sys.argv
FRESH = "--fresh-canonical" in sys.argv
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))
import pandas as pd  # noqa: E402

from rivalfunds import dramatic_move, homes, publish_page, sinks  # noqa: E402
from rivalfunds import gold_trade_schedule as g5mod  # noqa: E402


class OverlaySink:
    kind = "overlay"

    def __init__(self, local_root):
        self.live, self.local = sinks.S3Sink(), sinks.LocalSink(str(local_root))

    def get(self, uri):
        return self.local.get(uri) if self.local.exists(uri) else self.live.get(uri)

    def exists(self, uri):
        return self.local.exists(uri) or self.live.exists(uri)

    def list(self, prefix_uri):
        live = set(self.live.list(prefix_uri))
        if FRESH and "/gold/canonical_shape/" in prefix_uri:  # --fresh-canonical: rebuild G1 from inputs, never reuse a served revision
            live = set()
        return sorted(live | set(self.local.list(prefix_uri)))

    def put(self, uri, data, content_type=None):
        return self.local.put(uri, data, content_type)


OUT.mkdir(parents=True, exist_ok=True)
s = OverlaySink(OUT / "layer")
d = dt.date.fromisoformat(DAY)
rec = {"code_root": str(ROOT), "day": DAY, "stages": {}}

t = time.time()
lo = (d - dt.timedelta(days=40)).isoformat()
if "--canonical" in sys.argv:  # RIV-we-1: rebuild canonical_shape first, so the trade windows read the claimed as-of dates
    from rivalfunds import gold_canonical_shape as g1mod
    r1 = g1mod.handler_entry({"mode": "replay", "start": lo, "end": DAY, "batch_id": f"ws2-g1-{int(time.time())}", "sink": s, "budget_s": 7200})
    rec["stages"]["canonical_shape"] = {"status": r1.get("status"), "outputs": len(r1.get("outputs") or []),
                                        "detail": str(r1.get("detail"))[:400], "seconds": round(time.time() - t)}
    print("build-canonical-shape:", rec["stages"]["canonical_shape"], flush=True)
    t = time.time()
r = g5mod.handler_entry({"mode": "replay", "start": lo, "end": DAY, "batch_id": f"ws2-g5-{int(time.time())}", "sink": s})
rec["stages"]["trade_schedule"] = {"status": r.get("status"), "outputs": len(r.get("outputs") or []),
                                   "detail": str(r.get("detail"))[:400], "seconds": round(time.time() - t)}
print("build-trade-schedule:", rec["stages"]["trade_schedule"], flush=True)

t = time.time()
g4_prefix = homes.address("rivalfunds", "etfs", "gold", "security_market", "date=")
ca_prefix = homes.address("rivalfunds", "etfs", "gold", "corporate_actions", "date=")
frames, acts = [], []
for k in range(0, 31):
    day = (d - dt.timedelta(days=k)).isoformat()
    for u in s.list(g4_prefix + day + "/"):
        if u.endswith(".parquet"):
            frames.append(pd.read_parquet(io.BytesIO(s.get(u))))
    for u in s.list(ca_prefix + day + "/"):
        if u.endswith(".parquet"):
            acts.append(pd.read_parquet(io.BytesIO(s.get(u))))
g4 = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
actions = pd.concat(acts, ignore_index=True) if acts else pd.DataFrame(columns=["security_id", "event_type", "ratio", "ex_date", "claim"])
cands = dramatic_move.detect(g4, actions) if len(g4) else []
found, written = [], None
for c in cands:
    err = None
    try:
        row = dramatic_move.lookup(c, search=dramatic_move.serp_search) if SEARCH else None
    except Exception as e:  # noqa: BLE001 -- a failed search is recorded per candidate, never read as "nothing found"
        row, err = None, f"{type(e).__name__}: {e}"
    found.append({"candidate": {k: str(v) for k, v in c.items()}, "row": row, "error": err})
rows = [f["row"] for f in found if f["row"]]
by_ex = {}
for row in rows:  # the row lives under its EX-DATE partition: the chart window ends at the as-of day, before the publish day
    by_ex.setdefault(str(row["ex_date"])[:10], []).append(row)
written = [dramatic_move.write_rows(s, rs, ex) for ex, rs in sorted(by_ex.items())] or None
rec["stages"]["dramatic_move"] = {"g4_rows": int(len(g4)), "candidates": len(cands), "found": len(rows), "written": written,
                                  "detail": found, "seconds": round(time.time() - t), "search": SEARCH}
print("dramatic-move:", {k: v for k, v in rec["stages"]["dramatic_move"].items() if k != "detail"}, flush=True)
for f in found:
    print("   ", f["candidate"].get("security_id"), f["candidate"].get("date"), f["candidate"].get("prior_close"), "->",
          f["candidate"].get("close"), "|", (f["row"] or {}).get("event_type"), (f["row"] or {}).get("ratio"),
          (f["row"] or {}).get("source_url"), flush=True)

t = time.time()
r = publish_page.handler_entry({"mode": "replay", "date": DAY, "batch_id": f"ws2-real-run-{int(time.time())}", "sink": s})
rec["stages"]["publish_page"] = {"status": r.get("status"), "outputs": r.get("outputs"), "detail": str(r.get("detail"))[:600],
                                 "seconds": round(time.time() - t)}
print("publish-page:", r.get("status"), "| detail:", str(r.get("detail"))[:300], flush=True)
for o in r.get("outputs") or []:
    print("   ", o, flush=True)
json.dump(rec, open(OUT / "real_run_local.json", "w", encoding="utf-8"), indent=1, default=str)
