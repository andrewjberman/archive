"""ETFS_RIVALS round 21 -- read R5 of ROUND_ANALYSIS.round20 (2.0.0_SA_COO~RV): a dollar security's Bloomberg close against
the price its holders' reports imply, on the same day (CVO row C-S55: SUNB, close 77.39 against an implied 63.49).
Read-only: live S3 through get/list; the real run's chart objects only for the list of dollar keys.

    python read_r5_close_vs_implied.py <code root> <as-of day> <real-run layer root> <page day> <out json>

For every chart key stored as USD: the G4 close of the as-of day and the holding-implied price of the same day (the
package's own price_series._market / _implied), the ratio, and how many differ by more than 3 percent. For the worst, and
for any key containing SUNB, the G1 rows behind the implied price: fund, raw identifier, security_id, security_bloomberg,
name, quantity, market value."""
import collections
import datetime as dt
import glob
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
ASOF, LAYER, PAGE_DAY, OUT = sys.argv[2], sys.argv[3].rstrip("/\\"), sys.argv[4], sys.argv[5]
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))
from rivalfunds import gold_holding_contribution as hc, homes, price_series as ps, sinks  # noqa: E402

keys = {}
for f in glob.glob(LAYER + f"/opal-data-etfs/rivalfunds/etfs/platinum/page/date={PAGE_DAY}/charts/*.json"):
    o = json.load(open(f, encoding="utf-8"))
    for k, v in o["securities"].items():
        if v.get("currency") == "USD":
            keys.setdefault(k, set()).add(o["fund"])
print("distinct chart keys stored as USD:", len(keys))

s = sinks.S3Sink()
lo = (dt.date.fromisoformat(ASOF) - dt.timedelta(days=7)).isoformat()
g4 = hc._read(s, hc._newest_by_date(s, ps._G4_PREFIX, lo, ASOF))
g1 = hc._read(s, hc._newest_by_date(s, homes.canonical_shape(""), ASOF, ASOF))
wanted = set(keys)
mkt = ps._market(g4, wanted)
imp = ps._implied(g1, g4, wanted)
both = [(k, mkt[(k, ASOF)], imp[(k, ASOF)]) for k in sorted(wanted) if (k, ASOF) in mkt and (k, ASOF) in imp]
print(f"as-of {ASOF}: keys with a close {sum(1 for k in wanted if (k, ASOF) in mkt)} | with an implied price "
      f"{sum(1 for k in wanted if (k, ASOF) in imp)} | with both {len(both)}")
rows = sorted(((k, m, i, i / m - 1.0) for k, m, i in both), key=lambda r: -abs(r[3]))
bands = collections.Counter("over 3 percent" if abs(r[3]) > 0.03 else ("1 to 3 percent" if abs(r[3]) > 0.01 else "within 1 percent")
                            for r in rows)
print("implied against close:", dict(bands))
rec = {"asof": ASOF, "usd_keys": len(keys), "with_both": len(both), "bands": dict(bands), "worst": [], "sunb": []}
cols = [c for c in ("fund_ticker", "report_date", "raw_identifier", "security_id", "security_bloomberg", "security_name", "quantity",
                    "market_value", "resolution_status") if c in g1.columns]


def behind(key: str):
    out = []
    for r in g1.itertuples():
        try:
            ks = hc.row_keys(r._asdict() if hasattr(r, "_asdict") else dict(r))
        except Exception:  # noqa: BLE001
            ks = ()
        if key in (ks if isinstance(ks, (list, tuple, set)) else (ks,)):
            out.append({c: str(getattr(r, c)) for c in cols})
    return out


for k, m, i, d in rows[:8]:
    print(f"  {k}: close {m:.2f} implied {i:.2f} ({d:+.1%}) funds {sorted(keys[k])}")
    rec["worst"].append({"key": k, "close": m, "implied": i, "diff": d, "funds": sorted(keys[k])})
for k, m, i, d in rows:
    if "SUNB" in k.upper() or abs(d) > 0.03:
        b = behind(k)
        g4r = g4[g4["security_id"].astype(str).str.upper().isin({k.upper(), k.replace("_", " ").upper()})]
        g4c = [c for c in ("security_id", "security_parsekey", "date", "px_close", "currency") if c in g4r.columns]
        entry = {"key": k, "close": m, "implied": i, "diff": d, "g1_rows": b, "g4_rows": json.loads(g4r[g4c].astype(str).tail(2).to_json(orient="records"))}
        (rec["sunb"] if "SUNB" in k.upper() else rec.setdefault("over_3_percent", [])).append(entry)
        print(f"  -- {k}: G1 rows behind the implied price: {json.dumps(b)[:700]}")
        print(f"     G4 rows: {json.dumps(entry['g4_rows'])[:300]}")
json.dump(rec, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
