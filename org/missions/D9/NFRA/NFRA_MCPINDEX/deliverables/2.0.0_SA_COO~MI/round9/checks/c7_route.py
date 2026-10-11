"""c7_route.py -- MX-c-7 AC2 instrument: the operations lead's words reach his entries on the first try (offline).

Runs the gateway's opal_discover in-process against the working tree's catalog, as the Opal-internal principal, and
prints each ask's FIRST match. A HIT is the expected need id first. Read-only; no network.
Usage: python c7_route.py <gateway dir>
"""
import os
import sys

gw = sys.argv[1]
sys.path.insert(0, gw)
os.chdir(gw)
from app.graphql_plumbing import catalog_gate as g  # noqa: E402
from app.integrations.opal_discover import integration as od  # noqa: E402

ASKS = [("trade reconciliation", "E-30"), ("did the custodian settle our trades", "E-30"),
        ("billing", "E-31"), ("which households have unpaid fees", "E-31"),
        ("post model update rec", "E-32"), ("high cash account alert", "E-33"),
        ("assets transfer alert", "E-34"), ("restricted account alert", "E-35"),
        # round-8 analysis E2: Alyssa's two phrasings reach their needs from catalog text, with no word fold
        ("statement", "E-9"), ("S&P YTD", "E-19")]
hit = 0
for ask, want in ASKS:
    ms = od.discover(ask, g.OPAL_INTERNAL).get("matches", [])
    first = ms[0] if ms else {}
    got = (first.get("need") or {}).get("id") or first.get("dataset") or "NOT_CATALOGUED"
    ok = got == want
    hit += ok
    print("ROUTE %-40s first=%s want=%s %s" % (ask, got, want, "HIT" if ok else "MISS"))
print("ops lead asks routed %d of %d on the first try" % (hit, len(ASKS)))
sys.exit(0 if hit == len(ASKS) else 1)
