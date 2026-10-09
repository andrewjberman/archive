"""WS2-a AC1 -- price_series.series(..., actions=<frame>) adjusts a security's closes for stored splits, so a split leaves a
continuous curve; a big move with no action on file is a gap, never drawn. Pure: frames only, no S3, no vendor.

Run from the repository root:  python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~V1/ws2/checks/ws2-a.AC1.py
Last line: `AC1 RESULT: PASS 0 failures` or `AC1 RESULT: FAIL <n> (<arms>)`.
"""
import datetime as dt
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 9))
sys.path[:0] = [ROOT, os.path.join(ROOT, "data", "etfs", "scripts")]

import pandas as pd  # noqa: E402

from rivalfunds import gold_canonical_shape as g1mod  # noqa: E402
from rivalfunds import price_series  # noqa: E402

K = "TKOMY_US_Equity"
START, END = dt.date(2026, 10, 1), dt.date(2026, 10, 7)
CLOSES = [("2026-10-01", 50.5), ("2026-10-02", 49.93), ("2026-10-05", 49.59), ("2026-10-06", 50.5), ("2026-10-07", 3.33)]
fails = []


def check(arm, ok, detail):
    print(("OK   " if ok else "FAIL ") + f"({arm}) {detail}", flush=True)
    if not ok:
        fails.append(arm)


def g4(rows):
    return pd.DataFrame([{"security_id": K, "date": d, "px_close": p, "currency": "USD"} for d, p in rows],
                        columns=["security_id", "date", "px_close", "currency"])


def g1():
    return pd.DataFrame([], columns=[f.name for f in g1mod.SCHEMA])


def act(rows):
    """The stored gold corporate_actions shape: security_id in Bloomberg form (spaces), ratio = new shares per old share."""
    return pd.DataFrame([{"security_id": s, "event_type": e, "ratio": r, "ex_date": x, "claim": c, "source_url": u}
                         for s, e, r, x, c, u in rows],
                        columns=["security_id", "event_type", "ratio", "ex_date", "claim", "source_url"])


def run(closes, actions):
    try:
        return price_series.series(g4(closes), g1(), [K], START, END, actions=actions)[K]
    except Exception as e:  # noqa: BLE001 -- a missing keyword at the base is the expected FAIL
        return {"error": f"{type(e).__name__}: {e}"}


split = act([("TKOMY US Equity", "split", 15.0, "2026-10-07", "MEASURED", None)])

# (a) the split adjusts every close before its ex-date by its ratio; the curve is continuous
out = run(CLOSES, split)
pts = [p for p in out.get("points", []) if p[1] is not None]
vals = [p[1] for p in pts]
cont = len(vals) == 5 and max(vals) / min(vals) < 1.2
check("a", cont and abs(vals[0] - 50.5 / 15) < 0.01 and abs(vals[-1] - 3.33) < 1e-9,
      f"adjusted points {[(p[0], round(p[1], 4)) for p in pts] or out.get('error')}")

# (b) the series records what adjusted it
adj = out.get("adjustment")
check("b", isinstance(adj, list) and len(adj) == 1 and float(adj[0].get("ratio")) == 15.0
      and str(adj[0].get("ex_date"))[:10] == "2026-10-07" and adj[0].get("event_type") == "split",
      f"adjustment {adj!r}")

# (c) control: no actions -> the unadjusted closes, and an empty adjustment list; the 93% drop is then a gap, not drawn
ctl = run(CLOSES, None)
cpts = [p for p in ctl.get("points", []) if p[1] is not None]
check("c", ctl.get("adjustment") == [] and [p[0] for p in cpts] == [d for d, _ in CLOSES[:4]]
      and any(g.get("start") == "2026-10-07" for g in ctl.get("gaps", [])),
      f"no-action points {[(p[0], p[1]) for p in cpts] or ctl.get('error')}; gaps {ctl.get('gaps')}")

# (d) a cash dividend and a split dated after the window adjust nothing
other = act([("TKOMY US Equity", "cash_div", 0.5, "2026-10-02", "MEASURED", None),
             ("TKOMY US Equity", "split", 2.0, "2026-10-20", "MEASURED", None)])
flat = [(d, p * 1.0) for d, p in CLOSES[:4]]
o2 = run(flat, other)
check("d", [p[1] for p in o2.get("points", []) if p[1] is not None] == [p for _, p in flat] and o2.get("adjustment") == [],
      f"points {o2.get('points') or o2.get('error')}; adjustment {o2.get('adjustment')}")

# (e) an inferred row (WS2-b's shape: claim INFERRED, a source_url) adjusts the same way and carries its source
inf = act([("TKOMY US Equity", "split", 15.0, "2026-10-07", "INFERRED", "https://example.test/tokio-split")])
o3 = run(CLOSES, inf)
a3 = o3.get("adjustment") or [{}]
check("e", len([p for p in o3.get("points", []) if p[1] is not None]) == 5 and a3[0].get("claim") == "INFERRED"
      and a3[0].get("source_url") == "https://example.test/tokio-split", f"adjustment {o3.get('adjustment') or o3.get('error')}")

print("AC1 RESULT: PASS 0 failures" if not fails else f"AC1 RESULT: FAIL {len(fails)} ({', '.join(fails)})")
