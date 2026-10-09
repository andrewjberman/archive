"""RIV-we-1's real-run read: CGIC's trade windows before and after the canonical rebuild, and a control fund's.

    python we1_windows_compare.py <code root> <layer dir> <snapshot json> before|after

`before` records, per fund, the (window_start, window_end, n trades) of the newest local trade_schedule object of every
date into <snapshot json>; `after` reads the same again and prints the difference per fund. Reads only the local layer.
"""
import io
import json
import pathlib
import sys

ROOT, LAYER, SNAP, MODE = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2], pathlib.Path(sys.argv[3]), sys.argv[4]
sys.path[:0] = [str(ROOT / "data" / "etfs" / "scripts"), str(ROOT)]
import pandas as pd  # noqa: E402

from rivalfunds import homes, revision, sinks  # noqa: E402

s = sinks.LocalSink(LAYER)
pre = homes.trade_schedule("")
by_date: dict = {}
for u in s.list(pre):
    if u.endswith(".parquet") and "date=" in u:
        by_date.setdefault(u.split("date=")[1][:10], []).append(u)
out: dict = {}
for d, us in sorted(by_date.items()):
    df = pd.read_parquet(io.BytesIO(s.get(revision.newest(us))))
    for fund, g in df.groupby(df["fund_ticker"].astype(str)):
        trades = g[~g["action"].astype(str).isin(["below_tolerance"])]
        out.setdefault(fund, {})[d] = sorted({(str(a)[:10], str(b)[:10]) for a, b in zip(trades["window_start"], trades["window_end"])}) \
            + [len(trades)]
if MODE == "before":
    SNAP.write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    print("before: funds", len(out), "dates", len(by_date))
else:
    before = json.loads(SNAP.read_text(encoding="utf-8"))
    for fund in sorted(set(before) | set(out)):
        a, b = before.get(fund, {}), out.get(fund, {})
        changed = sorted(d for d in set(a) | set(b) if json.dumps(a.get(d)) != json.dumps(json.loads(json.dumps(b.get(d)))))
        print(f"{fund}: {len(changed)} of {len(set(a) | set(b))} dates changed")
        if fund == "CGIC":
            for d in changed[-6:]:
                print("   ", d, "before", a.get(d), "after", b.get(d))
