"""ETFS_RIVALS round 16 -- the CTO's term 4 (msg 30787): re-measure the round-15 real run after RIV-pc-1.

    python measure_currency.py <before charts dir> <after charts dir> <out json>

Reads two sets of per-fund chart objects for the same day. Prints and writes: fund-securities; how many carry both
source codes; the boundary jump (first market close over the last holding-implied price before it) above 3 or below
1/3, and above 1.05 or below 1/1.05; the count by stored currency of securities that still carry an implied point;
whether every USD security's points are identical before and after; and euro listings measured on both runs."""
import collections
import glob
import json
import os
import sys

BEFORE, AFTER, OUT = sys.argv[1], sys.argv[2], sys.argv[3]


def load(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, "*.json"))):
        o = json.load(open(f, encoding="utf-8"))
        for k, v in o["securities"].items():
            out[(o["fund"], k)] = v
    return out


def jump(v):
    pts = [p for p in v["points"] if p[1] is not None]
    m = [p for p in pts if p[2] == "m"]
    i = [p for p in pts if p[2] == "i"]
    if not (m and i):
        return None
    prev = [p for p in i if p[0] < m[0][0]]
    return m[0][1] / prev[-1][1] if prev else None


def measure(secs):
    both = wide = narrow = 0
    for v in secs.values():
        codes = {p[2] for p in v["points"] if p[1] is not None}
        if {"m", "i"} <= codes:
            both += 1
        r = jump(v)
        if r is not None:
            wide += r > 3 or r < 1 / 3
            narrow += r > 1.05 or r < 1 / 1.05
    return {"fund_securities": len(secs), "both_sources": both, "jump_over_3x": int(wide), "jump_over_5pct": int(narrow),
            "implied_only": sum(1 for v in secs.values() if {p[2] for p in v["points"] if p[1] is not None} == {"i"}),
            "market_only": sum(1 for v in secs.values() if {p[2] for p in v["points"] if p[1] is not None} == {"m"}),
            "no_price_at_all": sum(1 for v in secs.values() if not any(p[1] is not None for p in v["points"]))}


b, a = load(BEFORE), load(AFTER)
rec = {"before": measure(b), "after": measure(a), "same_keys": sorted(b) == sorted(a)}
ccy = collections.Counter(str(v.get("currency")) for v in a.values())
rec["after_by_currency"] = dict(ccy.most_common())
rec["after_implied_points_by_currency"] = dict(collections.Counter(
    str(v.get("currency")) for v in a.values() if any(p[2] == "i" for p in v["points"])).most_common())
usd = [k for k, v in a.items() if v.get("currency") == "USD"]
rec["usd_securities"] = len(usd)
rec["usd_points_identical_before_and_after"] = sum(1 for k in usd if k in b and b[k]["points"] == a[k]["points"])
us_listed = [k for k in a if "_US_" in k[1]]
rec["us_listed_keys"] = len(us_listed)
rec["us_listed_stored_usd"] = sum(1 for k in us_listed if a[k].get("currency") == "USD")
rec["us_listed_points_identical"] = sum(1 for k in us_listed if k in b and b[k]["points"] == a[k]["points"])
rec["us_listed_not_usd"] = sorted(f"{f}:{k}:{a[(f, k)].get('currency')}" for f, k in us_listed if a[(f, k)].get("currency") != "USD")[:40]
eur = [k for k, v in a.items() if v.get("currency") == "EUR"]
ratios = sorted(round(r, 3) for r in (jump(b[k]) for k in eur if k in b) if r is not None)
rec["eur_securities"] = len(eur)
rec["eur_before_boundary_ratio"] = {"n": len(ratios), "min": ratios[0] if ratios else None,
                                    "median": ratios[len(ratios) // 2] if ratios else None, "max": ratios[-1] if ratios else None,
                                    "over_5pct": sum(1 for r in ratios if r > 1.05 or r < 1 / 1.05)}
rec["eur_after_with_an_implied_point"] = sum(1 for k in eur if any(p[2] == "i" for p in a[k]["points"]))
json.dump(rec, open(OUT, "w", encoding="utf-8"), indent=2)
print(json.dumps(rec, indent=2))
