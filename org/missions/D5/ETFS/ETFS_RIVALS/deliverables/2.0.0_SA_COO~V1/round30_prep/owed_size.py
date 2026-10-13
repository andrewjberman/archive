"""Read-only sizing of the Rival Funds owed history. S3 GETs/LISTs only; no Bloomberg, no writes."""
import datetime as dt
import json
import re
import sys
sys.path.insert(0, "C:/dev/ajb_workspace")
from data.etfs.scripts.rivalfunds import history_owed as ho, gold_holding_contribution as hc, homes
from data.etfs.scripts.rivalfunds.sinks import S3Sink

DAY = "2026-10-13"
s = S3Sink()
tc = hc._tc()
asof = tc.prev_trading_day(dt.date.fromisoformat(DAY))
print("page day", DAY, "as-of", asof)

df = ho.owed(s, DAY, 365)
print("OWED close-only (current 365-day class):", ho.summary(df))
print("columns", list(df.columns), "sample funds values:", df["funds"].head(3).tolist())

# fund membership
def fset(x):
    return {t.strip() for t in str(x).replace(";", ",").replace("|", ",").split(",") if t.strip()}
df["fs"] = df["funds"].map(fset)
all_funds = sorted(set().union(*df["fs"]))
print("funds in owed set:", len(all_funds), all_funds)
only_ctrl = df["fs"].map(lambda f: f and f <= {"ACWI", "IWM"})
print("units whose only holders are ACWI/IWM:", int(only_ctrl.sum()), "securities:", df[only_ctrl]["security_id"].nunique())
keep = df[~only_ctrl]
print("after Z4:", ho.summary(keep))

# held-day subset: (security, next trading day after a report that holds it)
lo = asof - dt.timedelta(days=365)
tdays = [x for x in tc.trading_days_between(lo - dt.timedelta(days=10), asof + dt.timedelta(days=5))]
nxt_of = {tdays[i]: tdays[i + 1] for i in range(len(tdays) - 1)}
g1 = hc._read(s, hc._newest_by_date(s, homes.canonical_shape(""), (lo - dt.timedelta(days=7)).isoformat(), DAY),
              ("fund_ticker", "report_date", "security_id", "raw_identifier", "security_name"))
print("G1 rows read:", len(g1), "funds:", sorted(g1["fund_ticker"].unique()))
g1["rd"] = g1["report_date"].map(lambda x: dt.date.fromisoformat(str(x)[:10]))
held = g1[g1["security_id"].notna()].drop_duplicates(["security_id", "rd", "fund_ticker"])
pairs, by_fund = set(), {}
for sid, rd, f in zip(held["security_id"], held["rd"], held["fund_ticker"]):
    n = nxt_of.get(rd)
    if n and lo <= n <= asof:
        pairs.add((str(sid), n.isoformat()))
        by_fund.setdefault(f, set()).add((str(sid), n.isoformat()))
need = set(zip(keep["security_id"].astype(str), keep["date"].astype(str)))
print("RANKINGS need: held return-days", len(pairs), "of which owed:", len(pairs & need), "securities", len({p[0] for p in pairs}))
print("per fund held return-days (owed):", {f: len(v & need) for f, v in sorted(by_fund.items())})
print("sum of per-fund (a pair held by 2 funds counts twice):", sum(len(v & need) for v in by_fund.values()))
# dialogs: the securities the published page opens a dialog for -> chart need = their full owed history
try:
    html = s.get(homes.page(DAY, "index.html")).decode("utf-8", "replace")
    dk = set(re.findall(r'data-sec-dialog="([^"]*)"', html))
    print("published page", DAY, "bytes", len(html), "security dialogs", len(dk))
    pk = hc.parsekey_map(hc.g4_window(s, (lo).isoformat(), DAY, ("security_id", "date", "security_parsekey"))[0])
    alias, _ = hc.identity_maps(g1, pk)
    g1["key"] = list(hc.row_keys(g1, alias, pk))
    ids = set(g1[g1["key"].astype(str).isin({d.replace("&amp;", "&") for d in dk})]["security_id"].astype(str))
    chart = keep[keep["security_id"].astype(str).isin(ids)]
    print("dialog keys matched to securities:", len(ids), "; owed units for those securities (full 365d):", len(chart))
except Exception as e:
    print("dialog read failed:", type(e).__name__, e)
H = pairs & need
C = set(zip(chart["security_id"].astype(str), chart["date"].astype(str))) if "chart" in dir() else set()
U = H | C
print("UNION held-owed + chart-owed (units):", len(U), "| H only", len(H - C), "| C only", len(C - H), "| both", len(H & C))
for lab, n in (("R30", 30), ("R90", 90), ("R365", 365)):
    cut = (asof - dt.timedelta(days=n)).isoformat()
    h = {x for x in H if x[1] >= cut}
    c = {x for x in C if x[1] >= cut}
    u = h | c
    print(lab, "earliest", cut, "held-owed", len(h), "chart-owed", len(c), "union", len(u), "securities", len({x[0] for x in u}))
# the page's own top-N: is any fund-level price/return read? (no) ; count of held securities per fund
print("fund-level units (13 funds x owed dates):", 13 * len({d for _, d in need}))
json.dump({"owed_units": int(len(keep)), "H": len(H), "C": len(C), "U": len(U)}, open("owed_size_out.json", "w"))
