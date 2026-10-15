"""RIV-ya-1 drain act (issuer): the chart reader at HEAD equals the chart reader at the base, over the LIVE store, for every held security.
READ-ONLY: S3 GETs and LISTs only; no writes, no vendor call.

    python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round31/ya1_live_delta.py [N_REPORT_DATES] [BASE_COMMIT]

Reads the live `canonical_shape` of the last N report dates (default 60) for the keys, then runs `price_series.series` over the last 365
days twice over the SAME frames: the module as committed at BASE_COMMIT (default 1af8b0dba8, the round-31 issuance, before ya-1) and the module at
HEAD. The only key excused is `precedence_dropped` (new at HEAD; it must read 0 for every key). Prints the denominators (keys, days, G1 rows, G4
rows, action rows, inferred rows) and ONE verdict line: DELTA=0 or DELTA!=0. The G5 half of the same read is `round30_prep/xe3_live_delta.py`.
"""
import datetime as dt
import importlib.util
import subprocess
import sys

import pandas as pd

sys.path.insert(0, "C:/dev/ajb_workspace")
sys.path.insert(0, "C:/dev/ajb_workspace/data/etfs/scripts")
from rivalfunds import gold_holding_contribution as hc  # noqa: E402
from rivalfunds import homes, price_series, sinks  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
BASE = sys.argv[2] if len(sys.argv) > 2 else "1af8b0dba8"

src = subprocess.run(["git", "-C", "C:/dev/ajb_workspace", "show", f"{BASE}:data/etfs/scripts/rivalfunds/price_series.py"],
                     capture_output=True, text=True, encoding="utf-8").stdout
assert "precedence_drop" not in src and "def series" in src, "BASE is not the pre-ya-1 module"
spec = importlib.util.spec_from_loader("rivalfunds.price_series_base", loader=None, origin="base")
base = importlib.util.module_from_spec(spec)
base.__package__ = "rivalfunds"
exec(compile(src, "price_series_base.py", "exec"), base.__dict__)

s = sinks.get_sink("s3")
end = dt.date.today()
start = end - dt.timedelta(days=365)
lo, hi = start.isoformat(), end.isoformat()
g1_uris = hc._newest_by_date(s, homes.canonical_shape(""), lo, hi)
dates = sorted(g1_uris)[-N:]
g1 = hc._read(s, {d: g1_uris[d] for d in dates}, hc.G1_COLUMNS)
keys = sorted({str(k) for k in g1["security_id"].dropna() if str(k).strip()})
g4, _ = hc.g4_window(s, lo, hi, price_series._G4_COLUMNS)
actions = price_series._actions(s, lo, hi)
n_inf = int((actions["claim"] == "INFERRED").sum()) if len(actions) and "claim" in actions.columns else 0
print(f"denominators: report dates {len(dates)} ({dates[0]}..{dates[-1]}), keys {len(keys)}, days {start}..{end}, "
      f"G1 rows {len(g1)}, G4 rows {len(g4)}, action rows {len(actions)} (INFERRED {n_inf})")
old = base.series(g4, g1, keys, start, end, actions=actions)
new = price_series.series(g4, g1, keys, start, end, actions=actions)
diff = []
for k in keys:
    a, b = dict(old[k]), dict(new[k])
    if b.pop("precedence_dropped") != 0:
        diff.append((k, "precedence_dropped != 0"))
    if a != b:
        diff.append((k, "series differs"))
print("keys compared:", len(keys), "| keys with a difference:", len(diff), diff[:5])
print("VERDICT: DELTA=0" if not diff else "VERDICT: DELTA!=0")
_ = pd
