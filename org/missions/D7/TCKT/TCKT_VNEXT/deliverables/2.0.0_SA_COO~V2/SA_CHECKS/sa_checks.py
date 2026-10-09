"""TCKT_VNEXT workstream SA (TV-r-1 seat arm) -- the issuer's mechanical check (2.0.0_SA_COO~V2).

  sa-census  SA-l1-AC1  the route census JSON is well formed and every row is grounded:
             - top level: {"denominator": {"roots_scanned": [...], "routes_found": N}, "candidate_tokens": [...], "rows": [...]}
             - every row: route, method, function, firm_source (path:line), and per candidate token a verdict in
               {ONE_FIRM, NO_FIRM, MORE_THAN_ONE, UNRESOLVED} plus "other_firm_refused" (true/false/null)
             - len(rows) == denominator.routes_found, and every firm_source path exists with that line in range
Prints SA-CENSUS-OK <N rows, per-token verdict counts> or SA-CENSUS-FAIL <reason>; exit 0/1. Run from the worktree root.
"""
import json
import sys
from pathlib import Path

CENSUS = Path("org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~6/SA_ROUTE_CENSUS.json")
VERDICTS = {"ONE_FIRM", "NO_FIRM", "MORE_THAN_ONE", "UNRESOLVED"}


def fail(msg):
    print("SA-CENSUS-FAIL " + msg)
    return 1


def main(argv):
    if not argv or argv[0] != "sa-census":
        print("usage: sa_checks.py sa-census")
        return 2
    if not CENSUS.exists():
        return fail("absent: %s" % CENSUS.as_posix())
    try:
        d = json.loads(CENSUS.read_text(encoding="utf-8"))
    except ValueError as e:
        return fail("not JSON: %s" % e)
    den = d.get("denominator") or {}
    tokens = d.get("candidate_tokens") or []
    rows = d.get("rows") or []
    if not den.get("roots_scanned") or not isinstance(den.get("routes_found"), int):
        return fail("denominator missing roots_scanned or routes_found")
    if not tokens:
        return fail("no candidate_tokens")
    if len(rows) != den["routes_found"] or not rows:
        return fail("rows %d != routes_found %s" % (len(rows), den.get("routes_found")))
    counts = {t.get("name", "?"): {v: 0 for v in VERDICTS} for t in tokens}
    for i, r in enumerate(rows):
        for k in ("route", "method", "function", "firm_source", "per_token"):
            if k not in r:
                return fail("row %d missing %s" % (i, k))
        src = str(r["firm_source"])
        if ":" not in src:
            return fail("row %d firm_source not path:line" % i)
        path, _, line = src.rpartition(":")
        p = Path(path)
        if not p.exists():
            return fail("row %d firm_source path absent: %s" % (i, path))
        try:
            n = int(line)
        except ValueError:
            return fail("row %d firm_source line not an int: %s" % (i, line))
        if n < 1 or n > len(p.read_text(encoding="utf-8", errors="replace").splitlines()):
            return fail("row %d firm_source line out of range: %s" % (i, src))
        for t in tokens:
            name = t.get("name", "?")
            v = (r["per_token"] or {}).get(name) or {}
            if v.get("verdict") not in VERDICTS:
                return fail("row %d token %s verdict %r" % (i, name, v.get("verdict")))
            if "other_firm_refused" not in v:
                return fail("row %d token %s missing other_firm_refused" % (i, name))
            counts[name][v["verdict"]] += 1
    summary = "; ".join("%s %s" % (k, ",".join("%s=%d" % (vv, c) for vv, c in sorted(v.items()) if c)) for k, v in counts.items())
    print("SA-CENSUS-OK rows=%d tokens=%d | %s" % (len(rows), len(tokens), summary))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
