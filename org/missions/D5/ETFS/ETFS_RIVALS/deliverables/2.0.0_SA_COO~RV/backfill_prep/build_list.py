"""Backfill security list (read-only): every Bloomberg request security any universe fund reported in G1 over the 365 calendar
days to the as-of day, formerly-held keys included (CTO ruling msg 30817 term 1), then a DRY RUN of market-range (no vendor
call, nothing written)."""
import collections
import datetime as dt
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
END = dt.date.fromisoformat(sys.argv[2])
OUT = pathlib.Path(sys.argv[3])
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))
from rivalfunds import bbg_budget, enrichment_bloomberg as eb, gold_holding_contribution as hc, homes, sinks  # noqa: E402

s = sinks.S3Sink()
lo = END - dt.timedelta(days=365)
uris = hc._newest_by_date(s, homes.canonical_shape(""), str(lo), str(END))
dates = sorted(uris) if isinstance(uris, dict) else None
print("G1 partitions in window:", len(uris), "| first/last:", (dates[0], dates[-1]) if dates else type(uris).__name__)
seen = collections.Counter()
last_seen = {}
fail = 0
for d in (dates or []):
    try:
        secs = eb._g1_market_securities(s, str(d)[:10])
    except Exception as e:  # noqa: BLE001
        fail += 1
        if fail <= 3:
            print("  read failed", d, type(e).__name__, str(e)[:120])
        continue
    for x in secs:
        seen[x] += 1
        last_seen[x] = str(d)[:10]
allsecs = sorted(seen)
today = eb._g1_market_securities(s, dates[-1].isoformat() if hasattr(dates[-1], "isoformat") else str(dates[-1])[:10]) if dates else []
former = [x for x in allsecs if x not in set(today)]
print("distinct request securities over the window:", len(allsecs), "| in the newest G1 day:", len(today), "| formerly held:", len(former),
      "| G1 days unreadable:", fail)
print("identifier-keyed requests:", sum(1 for x in allsecs if eb._is_id_request(x)))
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "securities_365d.txt").write_text("\n".join(allsecs) + "\n", encoding="utf-8")
(OUT / "securities_365d.json").write_text(json.dumps({"window": [str(lo), str(END)], "count": len(allsecs), "formerly_held": former,
                                                     "last_seen": last_seen}, indent=1), encoding="utf-8")
print("budget remaining today:", bbg_budget.remaining())
r = eb.handler_entry({"mode": "market-range", "start": str(lo), "end": str(END), "securities": allsecs, "batch_id": "dryrun-plan",
                      "sink": s, "max_points": 10**9, "dry_run": True})
print("dry run:", json.dumps({k: r.get(k) for k in ("status", "detail", "plan")}, default=str)[:900])
