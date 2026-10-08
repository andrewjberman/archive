"""ETFS_RIVALS round 26 -- CTO half C1 (msg 31514): gold_canonical_shape and gold_trade_schedule run locally at the pin on
live inputs, their rows against the SERVED objects of the same dates.

    python upstream_stages_local.py <code root> <start> <end> <out dir>

Overlay sink: reads live S3, writes only under <out dir>/layer. Stage 1: build-canonical-shape, mode replay, report dates
start..end. Stage 2: build-trade-schedule, mode replay, same range, reading the canonical objects stage 1 just wrote
(the overlay lists local objects beside live ones, and each reader takes the newest). For each date the locally written
object is compared with the newest SERVED object of that date: same row keys, and every column equal except the ones
that name the build (revision, produced_at, batch, input manifest, source uris)."""
import collections
import io
import json
import pathlib
import sys
import time

import pandas as pd

ROOT = pathlib.Path(sys.argv[1]).resolve()
LO, HI, OUT = sys.argv[2], sys.argv[3], pathlib.Path(sys.argv[4]).resolve()
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))
from rivalfunds import gold_canonical_shape as g1mod, gold_trade_schedule as g5mod, homes, revision, sinks  # noqa: E402


class OverlaySink:
    kind = "overlay"

    def __init__(self, local_root):
        self.live, self.local = sinks.S3Sink(), sinks.LocalSink(str(local_root))

    def get(self, uri):
        return self.local.get(uri) if self.local.exists(uri) else self.live.get(uri)

    def exists(self, uri):
        return self.local.exists(uri) or self.live.exists(uri)

    def list(self, prefix_uri):
        return sorted(set(self.live.list(prefix_uri)) | set(self.local.list(prefix_uri)))

    def put(self, uri, data, content_type=None):
        return self.local.put(uri, data, content_type)


OUT.mkdir(parents=True, exist_ok=True)
s = OverlaySink(OUT / "layer")
live = sinks.S3Sink()
BUILD = ("revision", "produced_at", "batch_id", "input_manifest", "producer_version", "source_uri", "silver_uri", "g1_revision",
         "canonical_revision", "claim_revision", "run_id")
rec = {"code_root": str(ROOT), "range": [LO, HI], "stages": {}}


def norm(v):
    return None if pd.isna(v) else v


def compare(name, prefix_fn, keycols_try):
    res = {}
    local_objs = [u for u in s.local.list(prefix_fn("")) if u.endswith(".parquet")]
    by = collections.defaultdict(list)
    for u in local_objs:
        by[u.split("date=")[1][:10]].append(u)
    tot = collections.Counter()
    for d, us in sorted(by.items()):
        served = [u for u in live.list(prefix_fn(d)) if u.endswith(".parquet")]
        if not served:
            res[d] = {"served": None}
            tot["dates with no served object"] += 1
            continue
        a = pd.read_parquet(io.BytesIO(s.local.get(revision.newest(us))))
        b = pd.read_parquet(io.BytesIO(live.get(revision.newest(served))))
        cols = [c for c in b.columns if c in a.columns and c not in BUILD]
        only = {"only_local": sorted(set(a.columns) - set(b.columns)), "only_served": sorted(set(b.columns) - set(a.columns))}
        key = next((k for k in keycols_try if all(c in a.columns and c in b.columns for c in k)
                    and not a.duplicated(list(k)).any() and not b.duplicated(list(k)).any()), None)
        if key is None:  # no unique key: compare as sorted multisets of the compared columns
            sa = a[cols].astype(str).sort_values(cols).reset_index(drop=True)
            sb = b[cols].astype(str).sort_values(cols).reset_index(drop=True)
            same = len(sa) == len(sb) and bool((sa.values == sb.values).all())
            res[d] = {"rows_local": len(a), "rows_served": len(b), "key": None, "equal": bool(same), **only}
            tot["dates equal" if same else "dates DIFFERENT"] += 1
            continue
        ai, bi = a.set_index(list(key)), b.set_index(list(key))
        common = ai.index.intersection(bi.index)
        diff = collections.Counter()
        for c in [c for c in cols if c not in key]:
            x, y = ai.loc[common, c], bi.loc[common, c]
            ne = ~((x.astype(str) == y.astype(str)) | (x.isna() & y.isna()))
            if int(ne.sum()):
                diff[c] = int(ne.sum())
        same = len(ai) == len(bi) == len(common) and not diff
        res[d] = {"rows_local": len(a), "rows_served": len(b), "key": list(key), "only_local_keys": int(len(ai.index.difference(bi.index))),
                  "only_served_keys": int(len(bi.index.difference(ai.index))), "columns_compared": len(cols), "differing_columns": dict(diff),
                  "equal": bool(same), **only}
        tot["dates equal" if same else "dates DIFFERENT"] += 1
    print(f"{name}: {dict(tot)}")
    for d, r in sorted(res.items()):
        print("   ", d, {k: v for k, v in r.items() if k not in ("only_local", "only_served") or v})
    return {"totals": dict(tot), "dates": res}


t = time.time()
r1 = g1mod.handler_entry({"mode": "replay", "start": LO, "end": HI, "batch_id": "r26-c1-local", "sink": s})
print("build-canonical-shape:", r1.get("status"), "outputs", len(r1.get("outputs") or []), f"{time.time() - t:.0f}s", "| detail:", str(r1.get("detail"))[:300])
rec["stages"]["canonical_shape"] = {"status": r1.get("status"), "outputs": len(r1.get("outputs") or []), "detail": str(r1.get("detail"))[:600],
                                    "compare": compare("canonical_shape", homes.canonical_shape, (("fund_id", "report_date", "raw_identifier", "security_id"),
                                                                                                   ("fund_ticker", "report_date", "raw_identifier")))}
t = time.time()
r2 = g5mod.handler_entry({"mode": "replay", "start": LO, "end": HI, "batch_id": "r26-c1-local", "canonical_batch_id": "r26-c1-local", "sink": s})
print("build-trade-schedule:", r2.get("status"), "outputs", len(r2.get("outputs") or []), f"{time.time() - t:.0f}s", "| detail:", str(r2.get("detail"))[:300])
rec["stages"]["trade_schedule"] = {"status": r2.get("status"), "outputs": len(r2.get("outputs") or []), "detail": str(r2.get("detail"))[:600],
                                   "compare": compare("trade_schedule", homes.trade_schedule, (("fund_ticker", "security_key", "window_start", "window_end", "action"),))}
json.dump(rec, open(OUT / "upstream_stages_local.json", "w", encoding="utf-8"), indent=1, default=str)
