"""AMGT_RESAPP round 49, AMGT-xx-3 AC2 -- THE CENSUS: over the identified research-library names, how many whose annual report's
officer section points elsewhere GAIN officers from the proxy, with every denominator printed.

`lib.research.management.proxy_officers.census()` returns a dict with integer keys `identified` (names with a security_key),
`pointer` (names whose persisted officer section is UNRESOLVED-SOURCE with `section_refers_to` set), `gained` (pointer names
whose proxy read is SERVED) and `rows` (one per pointer name: security_key, status, officer count, reason). Printed as
  census: identified I; officer section points elsewhere P; gain officers from the proxy G of P
PASS when 0 < G <= P <= I and every pointer row that did not gain carries a reason.
usage: python <this>   (from the repo root)"""
import os
import sys

sys.path.insert(0, os.getcwd())


def main():
    try:
        from lib.research.management import proxy_officers as po
    except ImportError as exc:
        print("no lib.research.management.proxy_officers (%s)" % exc)
        print("THE CENSUS PRINTS ITS DENOMINATORS: NO")
        return 1
    c = po.census() or {}
    i, p, g, rows = c.get("identified"), c.get("pointer"), c.get("gained"), c.get("rows") or []
    print("census: identified %s; officer section points elsewhere %s; gain officers from the proxy %s of %s" % (i, p, g, p))
    silent = [r for r in rows if r.get("status") != "SERVED" and not r.get("reason")]
    for r in rows:
        print("  %s %s officers=%s %s" % (r.get("security_key"), r.get("status"), r.get("officers"), (r.get("reason") or "")[:90]))
    ok = all(isinstance(x, int) for x in (i, p, g)) and 0 < g <= p <= i and len(rows) == p and not silent
    print("THE CENSUS PRINTS ITS DENOMINATORS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
