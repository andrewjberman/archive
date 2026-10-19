"""IRPT_ANLREQ price-page inventory of the COMPARISON and MULTI maps (issuer 2.0.0_SA_COO~G2, 2026-10-19). MEASUREMENT ONLY.

    python price_pages_inventory_maps.py        (run from the repository root; needs pypdf, which the producer's tests need)

For each map it runs the SHIPPED Opal producer over the REAL map with the round-57 checker's fixtures (three tickers, a 10-year monthly
price history, SPY and BIL served), pricing off then on, and prints: element counts by (method, status, reason); how many elements pricing
moves; and the vendor-call elements split into price-based calls (returns, risk_stats, key_stats, level_series, standardized_returns,
scatter) and the rest, with the price-based ones split by the portfolio_* side and the comparison_* side. key_stats also carries
non-price rows (Net Expense Ratio, Cash Net Allocation), so the price-based count is an upper bound. ASCII only.
"""
import collections
import json
import sys

sys.path.insert(0, "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks")
import ar_price_checks as pc  # noqa: E402

MAPS = "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps/"
PRICE = ("returns", "risk_stats", "key_stats", "level_series", "standardized_returns", "scatter")


def report(name):
    mp = json.load(open(MAPS + name, encoding="utf-8"))
    out = {}
    for pricing in (False, True):
        rec, _sec = pc.run(pricing, MAPS + name)
        out[pricing] = {e["id"]: (str(e["method"])[:14], e["status"], e.get("reason")) for e in rec["elements"]}
    counts = collections.Counter(out[True].values())
    print("== %s: %d map elements, %d with the producer's three classified" % (name, len(mp["elements"]), len(out[True])))
    for key, n in sorted(counts.items(), key=lambda kv: -kv[1])[:8]:
        print("  %4d  %s" % (n, key))
    moved = [i for i in out[False] if out[False][i] != out[True][i]]
    print("  moved by turning pricing on: %d" % len(moved))
    own = [i for i, v in out[True].items() if v[0] in ("OWN_SERIES", "OPAL_HELD")]
    print("  Opal-wired elements (OWN_SERIES or OPAL_HELD): %d" % len(own))
    vendor = [e for e in mp["elements"] if isinstance(e.get("source"), dict) and e["source"].get("call") and not e["source"].get("computed")]
    price = [e for e in vendor if any(t in e["source"]["call"] for t in PRICE)]
    side = collections.Counter("comparison_*" if e["source"]["call"].startswith("comparison_") else "portfolio_*" for e in price)
    print("  vendor-call elements: %d; price-based calls (upper bound): %d; by side: %s" % (len(vendor), len(price), dict(side)))
    print("  price-based by call: %s" % dict(collections.Counter(e["source"]["call"] for e in price).most_common()))
    print("  price-based by kind: %s; by page: %s" % (dict(collections.Counter(e["kind"] for e in price)),
                                                     dict(sorted(collections.Counter(e["page"] for e in price).items()))))


def main():
    for name in ("comparison_map.json", "multi_map.json"):
        report(name)


if __name__ == "__main__":
    main()
