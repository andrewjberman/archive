import datetime as dt
import json
import os
import re
import sys

ROOT = "C:/tmp/wk-mx19-49"
LIST = os.path.join(ROOT, "org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables", "0.9.0_WK_NFRA_MCPINDEX~49", "listings")
sys.path.insert(0, ROOT)
from lib import trading_calendar as tc  # noqa: E402

LINE = re.compile(r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})\s+(\d+) (.+)$")
DATED = re.compile(r"^(\d{4}-\d{2}-\d{2})\.parquet$")
NOW_UTC = dt.datetime(2026, 10, 16, 14, 0, 0)  # listing run 2026-10-16T13:59:45Z to 13:59:56Z
EXPECTED = tc.expected_last_trading_day(NOW_UTC)
summary = {"listing_utc_window": "2026-10-16T13:59:45Z..2026-10-16T13:59:56Z",
           "expected_t1_frontier": str(EXPECTED), "tables": {}}
for t in ["unrealized", "transactions", "allocations", "fees"]:
    lines = [ln.rstrip("\r") for ln in open(os.path.join(LIST, "silver_%s.txt" % t), encoding="utf-8") if ln.strip()]
    objs = 0
    total = 0
    dates = []
    nondated = []
    unparsed = []
    newest_lm = None
    for ln in lines:
        m = LINE.match(ln)
        if not m:
            unparsed.append(ln)
            continue
        objs += 1
        total += int(m.group(3))
        key = m.group(4)
        ts = dt.datetime.strptime(m.group(1) + " " + m.group(2), "%Y-%m-%d %H:%M:%S")
        if newest_lm is None or ts > newest_lm:
            newest_lm = ts
        name = key.split("/")[-1]
        d = DATED.match(name)
        if d and key == "silver/%s/%s" % (t, name):
            dates.append(d.group(1))
        else:
            nondated.append("%s %s" % (key, m.group(3)))
    newest = max(dates) if dates else None
    behind = tc.trading_days_behind(newest, EXPECTED) if newest else None
    summary["tables"][t] = {
        "objects": objs,
        "bytes": total,
        "dated_parts": len(dates),
        "newest_dated": newest,
        "trading_days_behind_t1": behind,
        "nondated_keys": nondated,
        "unparsed_lines": len(unparsed),
        "newest_last_modified_listing_local_EDT": str(newest_lm),
        "newest_last_modified_utc": str(newest_lm + dt.timedelta(hours=4)) if newest_lm else None,
    }
out = os.path.join(LIST, "summary.json")
with open(out, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(summary, fh, indent=2, sort_keys=True)
    fh.write("\n")
print(json.dumps(summary, indent=2, sort_keys=True))
