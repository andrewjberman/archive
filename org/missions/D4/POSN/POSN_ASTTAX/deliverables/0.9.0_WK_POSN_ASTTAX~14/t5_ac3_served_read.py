"""T5-AC3/AC5 -- read the LIVE SERVED artifacts: clause (a) served label, clause (b) LABEL-GROUPED
weight, clause (d) subtotals vs grand total. Members of the retag set located BY TICKER.

No write of any kind. Reads only the bytes downloaded from S3 in the previous step.
"""
import json
import os
import collections

D = ".scratch/served"
MEMBERS = ["DBC", "GLD", "GSG", "IAU", "SLV", "USO", "VIXY", "VXX", "UVXY", "QBER", "PDBC"]
TARGET = {"DBC": "Commodities", "GLD": "Commodities", "GSG": "Commodities", "IAU": "Commodities",
          "SLV": "Commodities", "USO": "Commodities", "VIXY": "Structured", "VXX": "Structured",
          "UVXY": "Structured", "QBER": "Structured", "PDBC": "Commodities"}


def walk(o, path=""):
    if isinstance(o, dict):
        yield path, o
        for k, v in o.items():
            for r in walk(v, path + "/" + str(k)):
                yield r
    elif isinstance(o, list):
        for i, v in enumerate(o):
            for r in walk(v, path + "[%d]" % i):
                yield r


for fn in sorted(os.listdir(D)):
    p = os.path.join(D, fn)
    print("\n" + "=" * 100)
    print("ARTIFACT %s  (%d bytes on disk)" % (fn, os.path.getsize(p)))
    try:
        doc = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print("  NOT JSON: %s" % e)
        continue

    # 1. every dict that carries an asset_class / assetClass key
    holders = [(pa, o) for pa, o in walk(doc)
               if isinstance(o, dict) and ("asset_class" in o or "assetClass" in o)]
    print("  rows carrying an asset_class/assetClass key: %d" % len(holders))
    vals = collections.Counter((o.get("asset_class") or o.get("assetClass")) for _, o in holders)
    print("  SERVED asset_class VALUE census (denominator %d rows):" % len(holders))
    for v, n in sorted(vals.items(), key=lambda kv: (-kv[1], str(kv[0]))):
        print("      %-26r %4d" % (v, n))

    # 2. retag-set members present, by ticker
    present = []
    for pa, o in holders:
        t = o.get("ticker") or o.get("symbol") or o.get("Ticker")
        if t in MEMBERS:
            present.append((t, pa, o.get("asset_class") or o.get("assetClass"),
                            o.get("sub_asset_class") or o.get("subAssetClass"),
                            o.get("weight"), o.get("weight_pct"), o.get("allocation")))
    print("  RETAG-SET MEMBERS PRESENT (of %d checked): %d" % (len(MEMBERS), len(present)))
    for t, pa, ac, sac, w, wp, al in sorted(present):
        print("      %-6s served asset_class=%-14r sub=%-14r weight=%-10s weight_pct=%-8s at %s"
              % (t, ac, sac, w, wp, pa[:88]))

    # 3. LABEL-GROUPED weight: group the row weights by their served label
    grp = collections.defaultdict(float)
    cnt = collections.Counter()
    for pa, o in holders:
        lab = o.get("asset_class") or o.get("assetClass")
        w = o.get("weight", o.get("weight_pct", o.get("value")))
        if isinstance(w, (int, float)):
            grp[lab] += float(w)
            cnt[lab] += 1
    if grp:
        print("  LABEL-GROUPED weight over the rows above (clause (b) grain):")
        tot = 0.0
        for lab in sorted(grp, key=lambda k: str(k)):
            print("      %-26r rows=%-4d sum(weight)=%.6f" % (lab, cnt[lab], grp[lab]))
            tot += grp[lab]
        print("      GRAND TOTAL of the label groups: %.6f" % tot)

    # 4. any 'allocation' dict (the NEGATIVE CONTROL column)
    for pa, o in walk(doc):
        if isinstance(o, dict) and pa.endswith("/allocation"):
            print("  ALLOCATION DICT (negative control) at %s: %s" % (pa[:70], json.dumps(o)[:260]))
