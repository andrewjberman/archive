"""ETFS_RIVALS round 22 -- the read 1.0.0_SA_CTO~Z msg 31137 asks for (2.0.0_SA_COO~RV): per fund, the markers in the
chart objects against the trades in gold trade_schedule (G5) for the same window. The earlier run is not the ruler; G5 is.

    python markers_vs_trade_schedule.py <code root> <page day> <after layer root> <before layer root> <out json>

Read-only: live G5 and G4 through get/list; the real runs' chart objects from their local layers.
Ruler, built here and not taken from the publisher: a G5 row counts when its fund is the object's fund, its window_end
lies in [asof - 365 days, page day], its action is one the marker builder draws, its est_notional is neither null nor
zero, and its key -- the recorded security_key, or the Bloomberg key G4's security_parsekey gives for it -- is a key of
that fund's chart object. Markers are compared as TRADES: the sum of each marker's n_trades.
Also names the markers the round-22 run holds and the pre-fold run did not, by security and date."""
import collections
import datetime as dt
import glob
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
DAY, AFTER, BEFORE, OUT = sys.argv[2], sys.argv[3].rstrip("/\\"), sys.argv[4].rstrip("/\\"), sys.argv[5]
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))
from rivalfunds import gold_holding_contribution as hc, homes, price_series as ps, sinks, trade_markers as tm  # noqa: E402

PAGE = "/opal-data-etfs/rivalfunds/etfs/platinum/page/date=" + DAY + "/charts/*.json"


def load(root):
    out = {}
    for f in sorted(glob.glob(root + PAGE)):
        o = json.load(open(f, encoding="utf-8"))
        out[o["fund"]] = o
    return out


a, b = load(AFTER), load(BEFORE)
asof = sorted({o["asof"] for o in a.values()})
assert len(asof) == 1, asof
lo = (dt.date.fromisoformat(asof[0]) - dt.timedelta(days=365)).isoformat()
s = sinks.S3Sink()
g5 = hc._read(s, hc._newest_by_date(s, homes.trade_schedule(""), lo, DAY))
g4 = hc._read(s, hc._newest_by_date(s, ps._G4_PREFIX, lo, DAY), ("security_id", "date", "security_parsekey"))
pk = hc.parsekey_map(g4)
buy = {x for x in ("entry", "add")}
sell = {x for x in ("trim", "exit")}
drawn = buy | sell
print("marker builder's own action sets, if it names them:", {n: getattr(tm, n) for n in dir(tm) if n.isupper() and "ACTION" in n})
fc = "fund_ticker" if "fund_ticker" in g5.columns else "fund_id"
g5 = g5.assign(_we=g5["window_end"].astype(str).str[:10], _act=g5["action"].astype(str))
g5 = g5[(g5["_we"] >= lo) & (g5["_we"] <= DAY) & g5["_act"].isin(drawn)]
g5 = g5[g5["est_notional"].notna() & (g5["est_notional"].astype(float) != 0.0)]
print(f"window {lo} .. {DAY} (asof {asof[0]}) | G5 rows that can be a marker: {len(g5)} | parsekey pairs: {len(pk)}")

rec = {"day": DAY, "asof": asof[0], "window": [lo, DAY], "funds": {}}
print(f"{'fund':<6} {'G5 trades':>9} {'markers':>8} {'as trades':>9} {'equal':>6}  off-page G5 trades")
eq = 0
for f in sorted(a):
    keys = set(a[f]["securities"])
    rows = g5[g5[fc].astype(str) == f]
    k1 = rows["security_key"].astype(str)
    mapped = k1.where(k1.isin(keys), k1.str.upper().map(pk).fillna(k1))
    on = int(mapped.isin(keys).sum())
    off = int(len(rows) - on)
    mk = [m for v in a[f]["securities"].values() for m in v.get("markers") or []]
    trades = sum(int(m.get("n_trades") or 1) for m in mk)
    ok = on == trades
    eq += ok
    rec["funds"][f] = {"g5_trades_on_the_page_keys": on, "markers": len(mk), "markers_as_trades": trades, "equal": bool(ok),
                       "g5_trades_under_no_page_key": off}
    print(f"{f:<6} {on:>9} {len(mk):>8} {trades:>9} {ok!s:>6}  {off}")
rec["funds_equal"] = f"{eq} of {len(a)}"
print("funds whose markers (as trades) equal the trade schedule:", rec["funds_equal"])


def sig(m):
    return (m["side"], m["start"], m["end"], round(float(m["usd"]), 2))


gained = []
for f in sorted(a):
    sb = collections.Counter(sig(m) for v in (b.get(f, {}).get("securities") or {}).values() for m in v.get("markers") or [] if float(m["usd"]) != 0.0)
    for k, v in a[f]["securities"].items():
        for m in v.get("markers") or []:
            if m["end"] > asof[0]:
                continue
            if sb[sig(m)] > 0:
                sb[sig(m)] -= 1
            else:
                gained.append({"fund": f, "key": k, "name": v.get("name"), "side": m["side"], "start": m["start"], "end": m["end"],
                               "usd": round(float(m["usd"]), 2), "n_trades": m.get("n_trades")})
rec["gained_against_the_pre_fold_run"] = gained
print("markers in this run and not in the pre-fold run (page-day ones aside):", len(gained))
for g in gained:
    print(f"  {g['fund']} {g['key']:<18} {g['side']:<4} {g['start']} -> {g['end']}  ${g['usd']:,.0f}  {g['name']}")
json.dump(rec, open(OUT, "w", encoding="utf-8"), indent=1)
