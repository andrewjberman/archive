"""AMGT_RESAPP round 77 -- AMGT-ba-27: the /freshness page carries the portal's dev-only mark (Andrew-direct 2026-10-07).

  python r77_ba27.py --crit AC1|AC2 --portal <portal dir>

Reads <portal dir>/src/App.tsx as text.
AC1 (build):
    C1 the nav entry whose path is '/freshness' carries `requiresDev: true` (and keeps `requiresTier: 'internal'`);
    C2 the route whose path is "/freshness" wraps the page in a ProtectedRoute carrying `requireDev` (and keeps `requireInternal`);
    C3 the page component is still mounted on that route (`<Freshness />`).
AC2 (control; it PASSES at the base):
    C1 Investor Reporting keeps its mark: its nav entry carries `requiresDev: true` and its route `requireDev`;
    C2 exactly ONE more nav entry and ONE more route carry the mark than at the base count this check states (the base
       counts are 1 nav entry and 2 routes), so no other page gained or lost it.
Verdict: R77 BA27 <CRIT> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

BASE_NAV = 1      # nav entries with requiresDev: true at portal DEV 659104f4 (Investor Reporting)
BASE_ROUTES = 2   # <Route ...> lines with requireDev at portal DEV 659104f4 (Investor Reporting, its print route)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"), required=True)
    ap.add_argument("--portal", required=True)
    a = ap.parse_args()
    text = open(os.path.join(a.portal, "src", "App.tsx"), encoding="utf-8").read()
    lines = text.splitlines()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    nav = [ln for ln in lines if re.search(r"path:\s*'/freshness'", ln)]
    route = [ln for ln in lines if re.search(r'<Route\s+path="/freshness"', ln)]
    nav_dev = [ln for ln in lines if "path:" in ln and re.search(r"requiresDev:\s*true", ln)]
    route_dev = [ln for ln in lines if "<Route" in ln and re.search(r"\brequireDev\b", ln)]
    print(f"   /freshness nav entries {len(nav)}; routes {len(route)}; nav entries with the mark {len(nav_dev)}; routes with the mark {len(route_dev)}")

    if a.crit == "AC1":
        clause("C1 the /freshness nav entry carries requiresDev: true and stays internal",
               len(nav) == 1 and re.search(r"requiresDev:\s*true", nav[0]) and "requiresTier: 'internal'" in nav[0],
               nav[0].strip()[:140] if nav else "no entry")
        clause("C2 the /freshness route carries requireDev and stays requireInternal",
               len(route) == 1 and re.search(r"\brequireDev\b", route[0]) and "requireInternal" in route[0],
               route[0].strip()[:160] if route else "no route")
        clause("C3 the page is still mounted on the route", len(route) == 1 and "<Freshness />" in route[0])
    else:
        ir_nav = [ln for ln in nav_dev if "'/investor-reporting'" in ln]
        ir_route = [ln for ln in route_dev if 'path="/investor-reporting"' in ln]
        clause("C1 Investor Reporting keeps its mark", len(ir_nav) == 1 and len(ir_route) == 1)
        fresh_nav = sum(1 for ln in nav_dev if "'/freshness'" in ln)
        fresh_route = sum(1 for ln in route_dev if 'path="/freshness"' in ln)
        clause("C2 no other page gained or lost the mark",
               len(nav_dev) - fresh_nav == BASE_NAV and len(route_dev) - fresh_route == BASE_ROUTES,
               f"nav {len(nav_dev)} (freshness {fresh_nav}); routes {len(route_dev)} (freshness {fresh_route})")
    yes = all(ok)
    print(f"R77 BA27 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
