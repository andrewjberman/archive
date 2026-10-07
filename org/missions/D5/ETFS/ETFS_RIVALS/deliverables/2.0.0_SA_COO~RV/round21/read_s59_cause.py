"""ETFS_RIVALS round 21 -- read R3 of ROUND_ANALYSIS.round20 (2.0.0_SA_COO~RV): why 11 of 393 dialog month strips disagree
with their fund-security's trade markers (row ETFS_RIVALS-Z-S59). Read-only: live S3 through get/list, the round-19 real
run's local layer for the page and chart objects; nothing written but the out json.

    python read_s59_cause.py <code root> <page day> <real-run layer root> <out json>

For each disagreeing strip it prints the strip's traded year-months, the markers' year-months, and the fund's G5
trade_schedule rows for the security in the months where the two differ: action, window_start, window_end, est_notional,
est_notional_base, security_id and security_key. The strip is drawn from gold buying_trend (built from G5 by security
key and est_notional_base); the markers from the same G5 rows by the chart key and est_notional."""
import collections
import datetime as dt
import glob
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
DAY, LAYER, OUT = sys.argv[2], sys.argv[3].rstrip("/\\"), sys.argv[4]
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))
from rivalfunds import gold_holding_contribution as hc, homes, sinks  # noqa: E402

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
base = LAYER + "/opal-data-etfs/rivalfunds/etfs/"
html = open(base + f"platinum/page/date={DAY}/index.html", encoding="utf-8").read()
objs = {}
for f in glob.glob(base + f"platinum/page/date={DAY}/charts/*.json"):
    o = json.load(open(f, encoding="utf-8"))
    objs[o["fund"]] = o["securities"]

bad = []
for seg in html.split('data-sec-dialog="')[1:]:
    key = seg.split('"', 1)[0]
    for sec in re.split(r"(?=<section data-fund=)", seg)[1:]:
        fm = re.match(r"<section data-fund=[\"']?([A-Za-z0-9_]+)", sec)
        st = re.search(r"data-month-chart>(.*?)</div>", sec)
        if not fm or not st or "data-chart-fund" not in sec:
            continue
        fund = fm.group(1)
        got = re.findall(r"<i class=(\w) data-m=(\w{3})>", st.group(1))
        y, mo = int(DAY[:4]), int(DAY[5:7])
        yms = []
        for _ in got:
            yms.append(f"{y:04d}-{mo:02d}")
            y, mo = (y - 1, 12) if mo == 1 else (y, mo - 1)
        yms.reverse()
        traded = {ym for ym, (k, _n) in zip(yms, got) if k in ("u", "d")}
        mk = (objs.get(fund, {}).get(key) or {}).get("markers") or []
        mkm = {x["end"][:7] for x in mk} & set(yms)
        if traded != mkm:
            bad.append({"fund": fund, "key": key, "strip_only": sorted(traded - mkm), "markers_only": sorted(mkm - traded),
                        "strip_months": yms})
print("disagreeing strips:", len(bad))

s = sinks.S3Sink()
lo = (dt.date.fromisoformat(DAY) - dt.timedelta(days=400)).isoformat()
g5u = hc._newest_by_date(s, homes.trade_schedule(""), lo, DAY)
g5 = hc._read(s, g5u)
print("G5 partitions read:", len(g5u), "| rows:", len(g5), "| columns:", [c for c in g5.columns][:30])
fc = "fund_ticker" if "fund_ticker" in g5.columns else "fund_id"
g5["_we"] = g5["window_end"].astype(str).str[:10]
cls = collections.Counter()
for b in bad:
    sub = g5[(g5[fc].astype(str) == b["fund"])]
    kcols = [c for c in ("security_key", "security_id") if c in sub.columns]
    hit = sub[sub[kcols].astype(str).apply(lambda col: col == b["key"]).any(axis=1)]
    months = set(b["strip_only"]) | set(b["markers_only"])
    rows = hit[hit["_we"].str[:7].isin(months)]
    b["g5_rows_under_the_key_in_those_months"] = int(len(rows))
    keep = [c for c in ("action", "window_start", "window_end", "est_notional", "est_notional_base", "security_id", "security_key",
                        "window_trading_days", "status") if c in rows.columns]
    b["rows"] = json.loads(rows[keep].astype(str).head(8).to_json(orient="records"))
    # other keys the same fund trades in those months whose name could be the same security (same security_id or key prefix)
    if "security_key" in sub.columns and "security_id" in sub.columns:
        ids = set(hit["security_id"].astype(str)) | set(hit["security_key"].astype(str))
        alt = sub[(sub["security_id"].astype(str).isin(ids) | sub["security_key"].astype(str).isin(ids))
                  & ~(sub[kcols].astype(str).apply(lambda col: col == b["key"]).any(axis=1))]
        b["rows_under_another_key_same_ids"] = int(len(alt))
    acts = collections.Counter(rows["action"].astype(str)) if "action" in rows.columns else {}
    nulls = int(rows["est_notional"].isna().sum()) if "est_notional" in rows.columns else None
    nulls_b = int(rows["est_notional_base"].isna().sum()) if "est_notional_base" in rows.columns else None
    b["actions"], b["est_notional_null"], b["est_notional_base_null"] = dict(acts), nulls, nulls_b
    sig = ("strip_only" if b["strip_only"] else "") + ("+markers_only" if b["markers_only"] else "")
    sig += " | no G5 row under the key" if not len(rows) else (" | est_notional null" if nulls else " | rows present")
    cls[sig] += 1
    print(json.dumps({k: b[k] for k in ("fund", "key", "strip_only", "markers_only", "g5_rows_under_the_key_in_those_months", "actions",
                                        "est_notional_null", "est_notional_base_null", "rows_under_another_key_same_ids") if k in b}))
    for r in b["rows"][:4]:
        print("     ", json.dumps(r))
print("signature distribution:", dict(cls))
json.dump({"day": DAY, "disagreeing": bad, "signatures": dict(cls)}, open(OUT, "w", encoding="utf-8"), indent=1)
