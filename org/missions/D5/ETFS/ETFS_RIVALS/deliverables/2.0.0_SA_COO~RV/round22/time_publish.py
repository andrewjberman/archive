"""ETFS_RIVALS round 22 -- time and peak memory of each stage a republish runs, on this machine, for the deploy half.

    python time_publish.py <code root> <YYYY-MM-DD> <out dir>

Same read-only overlay as the real run (live inputs, local writes only). Prints seconds per call for gold
holding_contribution, gold buying_trend and publish-page (which builds the 13 chart objects), and the process's peak
working set. A Lambda at 1,024 MB is a different machine: the figures bound nothing, they size the question."""
import importlib.util
import json
import os
import pathlib
import sys
import time

ROOT = pathlib.Path(sys.argv[1]).resolve()
DAY = sys.argv[2]
OUT = pathlib.Path(sys.argv[3]).resolve()
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))
_spec = importlib.util.spec_from_file_location("r12_real_run", ROOT / "org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round12/real_run.py")
r12 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r12)

from rivalfunds import gold_buying_trend, gold_holding_contribution, publish_page  # noqa: E402


def peak_mb():
    try:
        import psutil
        m = psutil.Process().memory_info()
        return round(getattr(m, "peak_wset", m.rss) / 1e6)
    except Exception:  # noqa: BLE001
        return None


OUT.mkdir(parents=True, exist_ok=True)
s = r12.OverlaySink(OUT / "layer")
rec = {"day": DAY, "code_root": str(ROOT)}
for name, fn, ev in (("gold_holding_contribution", gold_holding_contribution.handler_entry, {"date": DAY, "sink": s}),
                     ("gold_buying_trend", gold_buying_trend.handler_entry, {"date": DAY, "sink": s})):
    t = time.time()
    r = fn(ev)
    rec[name] = {"status": r.get("status"), "seconds": round(time.time() - t, 1), "peak_mb_so_far": peak_mb()}
os.environ[publish_page.PRODUCE_ENV] = "0"
t = time.time()
r = publish_page.handler_entry({"date": DAY, "mode": "replay", "batch_id": "r22-timing", "sink": s})
rec["publish_page"] = {"status": r.get("status"), "seconds": round(time.time() - t, 1), "peak_mb_so_far": peak_mb()}
print(json.dumps(rec, indent=1))
(OUT / f"timing_{DAY}.json").write_text(json.dumps(rec, indent=1), encoding="utf-8")
