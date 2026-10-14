"""RIV-xe-3 drain act (issuer): the union reader read against the LIVE store equals today's G5 output (CTO msg 5577 arm (a), DELTA = 0),
BEFORE any deploy. READ-ONLY: S3 GETs and LISTs only; no writes, no vendor call.

    python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~V1/round30_prep/xe3_live_delta.py [N_REPORT_DATES]

Runs the pure G5 functions (`infer_trades`, `infer_recon`, `held_funds`) over the live `canonical_shape` of the last N report dates (default 60),
once with the actions the OLD rule keeps (per security only its latest pull) and once with the actions `gold_trade_schedule.load_actions`
returns at HEAD (the new union reader), and compares the frames. The only column excused is `corporate_actions_revision`, a lineage label that
names the pulls read. Prints the denominators (objects, rows, dates, funds, trade rows), the extra rows the union adds (with ex-dates), and ONE
verdict line: DELTA=0 or DELTA!=0.
"""
import io
import sys

import pandas as pd
import pyarrow.parquet as pq

sys.path.insert(0, "C:/dev/ajb_workspace")
from data.etfs.scripts.rivalfunds import gold_trade_schedule as g, homes, universe  # noqa: E402
from data.etfs.scripts.rivalfunds.sinks import S3Sink  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
LINEAGE = {"corporate_actions_revision"}

s = S3Sink()
prefix = homes.address("rivalfunds", "etfs", "gold", "corporate_actions", "date=")
uris = [u for u in s.list(prefix) if u.endswith(".parquet")]
raw = pd.concat([pq.read_table(io.BytesIO(s.get(u))).to_pandas() for u in uris], ignore_index=True)
print("corporate_actions objects", len(uris), "rows", len(raw), "securities", raw["security_id"].nunique())

key = raw["as_of"].astype(str) + "|" + raw["revision"].astype(str)
old_actions = raw[key == key.groupby(raw["security_id"]).transform("max")]
new_actions, label, _ = g.load_actions(s)
print("OLD rule rows", len(old_actions), "| NEW reader rows", len(new_actions))

K = ["security_id", "row_kind", "event_type", "ex_date"]
o = old_actions[K].astype(str).apply(tuple, axis=1)
extra = new_actions[~new_actions[K].astype(str).apply(tuple, axis=1).isin(set(o))]
print("rows the union adds beyond the old rule:", len(extra))
if len(extra):
    print(extra[["security_id", "row_kind", "event_type", "ex_date", "revision"]].head(30).to_string())
    ex = pd.to_datetime(extra["ex_date"], errors="coerce")
    print("extra ex_date range:", ex.min(), "to", ex.max())

avail = g._canonical_by_date(s)
dates = sorted(avail)[-N:]
in_universe = set(universe.funds())
frames = []
for d in dates:
    t = pq.read_table(io.BytesIO(s.get(avail[d]))).to_pandas()
    frames.append(t[t["fund_ticker"].isin(in_universe)])
canonical = pd.concat(frames, ignore_index=True)
parsekeys = g.load_parsekeys(s, canonical)
print("report dates", len(dates), dates[0], "to", dates[-1], "| canonical rows", len(canonical), "funds", canonical["fund_ticker"].nunique())


def _norm(df):
    df = df.drop(columns=[c for c in LINEAGE if c in df.columns], errors="ignore")
    return df.sort_values(list(df.columns), kind="mergesort").reset_index(drop=True).astype(str)


ok = True
for name, fn in (("infer_trades", g.infer_trades), ("infer_recon", g.infer_recon)):
    a = _norm(fn(canonical, old_actions, "L", parsekeys))   # ONE label for both: the label is lineage, never compared
    b = _norm(fn(canonical, new_actions, "L", parsekeys))
    same = a.shape == b.shape and a.equals(b)
    print(f"{name}: old {a.shape} new {b.shape} equal={same}")
    if not same and a.shape == b.shape:
        bad = [c for c in a.columns if not a[c].equals(b[c])]
        print("   differing columns:", bad)
        for c in bad[:3]:
            m = a[c] != b[c]
            print("   ", c, "old", a[c][m].head(3).tolist(), "new", b[c][m].head(3).tolist())
    ok = ok and same
ha = g.held_funds(canonical, old_actions, None, parsekeys)
hb = g.held_funds(canonical, new_actions, None, parsekeys)
print("held_funds: old", ha, "new", hb, "equal=", ha == hb)
ok = ok and ha == hb
print("VERDICT:", "DELTA=0" if ok else "DELTA!=0")
