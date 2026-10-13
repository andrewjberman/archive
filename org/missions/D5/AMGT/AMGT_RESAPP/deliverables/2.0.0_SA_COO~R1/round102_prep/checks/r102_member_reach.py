"""AMGT_RESAPP round-102 PREP -- which of the build's DIFFERING members does the scoped handler actually LOAD?

  PYTHONPATH=<the pin's worktree> python r102_member_reach.py <member path> [<member path> ...]

READ-ONLY. Imports `lib.research.api.scoped_amgt` from the checkout it runs in, then drives the handler in-process (S3 reads on the live pool, no function invoke, no write) through every
ROUTE SHAPE the function serves with real subjects: the overlay, peers, coverage, thesis, ledger and versions leaves for two subjects, the ranked lists, the rank series, the collected
chatter series, the timeline, `/freshness` and its page view, `/lists`. Afterwards it prints, for each member path given, whether a module loaded from that file is in `sys.modules` (LOADED)
or not (NOT LOADED), and for non-module members (a data file) whether the file was opened by a loaded module is NOT knowable here, so it prints `DATA FILE: read by name, see the pair`.
Verdict line `R102 MEMBER REACH: <n> of <m> given members LOADED`. This is a LOWER bound on reachability (a route not driven here may load more); the pair says so. Exit 0. Writes nothing.
"""
import io
import contextlib
import os
import sys


def event(path):
    return {"rawPath": path, "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}


ROUTES = []
for sj in ("ASML_NA_Equity", "ADBE_US_Equity"):
    for leaf in ("overlay", "peers", "coverage", "thesis", "ledger", "versions"):
        ROUTES.append("/api/scoped/amgt/security/%s/%s" % (sj, leaf))
    ROUTES.append("/api/scoped/amgt/security/%s/timeline" % sj)
ROUTES += [
    "/api/scoped/amgt/lead-panel/rankings/TRENDING/PRICE",
    "/api/scoped/amgt/lead-panel/rankings/BREAKOUT/CHATTER",
    "/api/scoped/amgt/lead-panel/timeseries/TRENDING/PRICE",
    "/api/scoped/amgt/lead-panel/timeseries/collected/chatter",
    "/api/scoped/amgt/freshness",
    "/api/scoped/amgt/lists",
]


def main(argv):
    root = os.getcwd()
    from lib.research.api import scoped_amgt

    statuses = {}
    for path in ROUTES:
        ev = event(path)
        if path.endswith("/freshness"):
            ev["queryStringParameters"] = {"view": "page"}
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                resp = scoped_amgt.handler(ev)
            statuses[path] = resp.get("statusCode")
        except Exception as err:  # noqa: BLE001
            statuses[path] = "EXC %s" % type(err).__name__
    print("driven %d routes: statuses %s" % (len(ROUTES), sorted(set(str(v) for v in statuses.values()))))
    loaded = set()
    for mod in list(sys.modules.values()):
        f = getattr(mod, "__file__", None)
        if f:
            loaded.add(os.path.normcase(os.path.abspath(f)))
    n = 0
    for member in argv:
        full = os.path.normcase(os.path.abspath(os.path.join(root, member)))
        if member.endswith(".py"):
            hit = full in loaded
            n += 1 if hit else 0
            print("%-62s %s" % (member, "LOADED" if hit else "NOT LOADED"))
        else:
            print("%-62s DATA FILE: read by name, see the pair" % member)
    print("R102 MEMBER REACH: %d of %d given members LOADED" % (n, len(argv)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
