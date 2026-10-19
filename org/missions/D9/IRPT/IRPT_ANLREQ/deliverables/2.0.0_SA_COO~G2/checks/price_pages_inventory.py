"""IRPT_ANLREQ price-page inventory (issuer 2.0.0_SA_COO~G2, 2026-10-19). MEASUREMENT ONLY: it runs the shipped Opal producer over the REAL
overview map, with the repository's own test fixtures and made-up prices, once with pricing off and once with pricing on, and prints
each element's (method, status, reason) counts and the ids that still read NOT_IN_THIS_VERSION. It writes nothing outside memory.

    python price_pages_inventory.py        (run from the repository root; needs pypdf, which the producer's tests need)

The three tickers of the fixture are AAA, BBB, CCC; the benchmark proxy SPY and the risk-free proxy BIL are served here so the nine
OWN_SERIES price elements can read VALUE. ASCII only.
"""
import collections
import json
import sys

ROOT = "infra/aws/lambda/investor-reporting/ycharts/research/tests"
MAP = "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps/overview_map.json"


def load():
    sys.path.insert(0, ROOT)
    sys.path.insert(0, "lib")
    import test_opal_producer as tp
    import test_opal_producer_prices as tpp
    return tp, tpp


def run(tp, tpp, mp, pricing):
    over = {}
    if pricing:
        levels = tpp._levels
        readers = tpp._readers(estate={"AAA": levels("AAA"), "SPY": levels("AAA"), "BIL": levels("BBB")})
        over = {"pricing": True, "as_of": tpp.AS_OF, "price_readers": readers}
    return tpp.op.produce(tp.REQ, tp.FIRM, tp.make_stores(map=mp, **over))


def main():
    tp, tpp = load()
    mp = json.load(open(MAP, encoding="utf-8"))
    el = {e["id"]: e for e in mp["elements"]}
    print("MAP %s: %d elements, %d calls" % (MAP, len(el), len(mp.get("calls", []))))
    status = {}
    for pricing in (False, True):
        rec = run(tp, tpp, mp, pricing)
        counts = collections.Counter((str(e["method"])[:14], e["status"], e.get("reason")) for e in rec["elements"])
        print("== pricing=%s: %d elements" % (pricing, len(rec["elements"])))
        for key, n in sorted(counts.items(), key=lambda kv: -kv[1]):
            print("  %4d  %s" % (n, key))
        status[pricing] = {e["id"]: (e["method"], e["status"], e.get("reason")) for e in rec["elements"]}
    moved = [i for i in status[False] if status[False][i] != status[True][i]]
    print("== moved by turning pricing on: %d of %d" % (len(moved), len(el)))
    for i in moved:
        s = el[i].get("source") or {}
        print("  %-7s p%-2s %-6s %-46s %s -> %s" % (i, el[i].get("page"), el[i].get("kind"), str(el[i].get("label"))[:46],
                                                    status[False][i][1:], status[True][i][1:]))
    still = [i for i in status[True] if status[True][i][1] != "VALUE" and status[True][i][2] == "NOT_IN_THIS_VERSION"]
    groups = collections.defaultdict(list)
    for i in still:
        groups[status[True][i][0][:14]].append(i)
    print("== still NOT_IN_THIS_VERSION with pricing on: %d (denominator: %d elements)" % (len(still), len(el)))
    for method, ids in sorted(groups.items()):
        print("  %-14s %d" % (method, len(ids)))
    print("== VENDOR_SOURCED rows (call named by the map) that need a price series or a snapshot metric")
    for i in groups.get("VENDOR_SOURCED", []):
        s = el[i].get("source")
        print("  %-7s p%-2s %-6s %-46s call=%s" % (i, el[i].get("page"), el[i].get("kind"), str(el[i].get("label"))[:46],
                                                    s.get("call") if isinstance(s, dict) else s))
    print("== OPAL_HELD rows read NO_RULE whose group name is a risk or return statistic or a yield")
    for i in groups.get("OPAL_HELD", []):
        s = el[i].get("source") or {}
        g = str(s.get("group") or s.get("field") or "")
        if any(t in g for t in ("beta", "alpha", "yield", "return", "sharpe", "sortino", "drawdown", "volatil", "std")):
            print("  %-7s p%-2s %-6s %-46s group=%s" % (i, el[i].get("page"), el[i].get("kind"), str(el[i].get("label"))[:46], g[:40]))


if __name__ == "__main__":
    main()
