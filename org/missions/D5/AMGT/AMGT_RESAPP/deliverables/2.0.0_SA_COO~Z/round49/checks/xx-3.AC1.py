"""AMGT_RESAPP round 49, AMGT-xx-3 AC1 -- OFFICERS FROM THE PROXY STATEMENT WHEN THE ANNUAL REPORT'S OFFICER SECTION POINTS ELSEWHERE
(DSGN FWD-7), proven on the walked no-officer name: INTU_US_Equity, whose 10-K (accession 0000896878-26-000037) Item 10 lists no
officers and refers to the proxy.

`lib.research.management.proxy_officers.officers_from_proxy(security_key)` returns
  {"status": "SERVED" | "UNRESOLVED-SOURCE", "officers": [{"name", "role", ...}], "source": {"form": "DEF 14A", "accession",
   "url", "filing_date", "retrieved_at", "document_sha256"}, "reason"}
SERVED here means: form DEF 14A, an accession, at least three officers, each with a name that is not a title and a role.
usage: python <this>   (from the repo root; reads EDGAR through lib/research/filings/fetch.py)"""
import os
import re
import sys

sys.path.insert(0, os.getcwd())
TITLE = re.compile(r"^(chief|executive|officer|president|vice|senior|general|counsel|secretary|treasurer|director|chair)", re.I)


def main():
    try:
        from lib.research.management import proxy_officers as po
    except ImportError as exc:
        print("no lib.research.management.proxy_officers (%s)" % exc)
        print("OFFICERS FROM THE PROXY ON THE WALKED NAME: NO")
        return 1
    r = po.officers_from_proxy("INTU_US_Equity") or {}
    src = r.get("source") or {}
    officers = r.get("officers") or []
    bad = [o for o in officers if not o.get("name") or not o.get("role") or TITLE.match(str(o.get("name")))]
    print("status %s, form %s, accession %s, officers %d, malformed %d" % (
        r.get("status"), src.get("form"), src.get("accession"), len(officers), len(bad)))
    for o in officers[:6]:
        print("  %s -- %s" % (o.get("name"), o.get("role")))
    ok = (r.get("status") == "SERVED" and src.get("form") == "DEF 14A" and src.get("accession")
          and len(officers) >= 3 and not bad)
    print("OFFICERS FROM THE PROXY ON THE WALKED NAME: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
