"""c10_discover.py -- MX-c-8 AC3 / MX-r-11 instrument (FWD-21 routing): the three discover reads, in-process.

Usage: python c10_discover.py <gateway dir>
Runs <gateway dir>'s opal_discover against its own catalog as the Opal-internal principal (offline in a worktree; on the
host under the deployed venv). Prints one DISCOVER line per subject:
  * the two harvest subjects: catalogued True AND at least one match on channel harvest_datasets;
  * the Schwab control ("Schwab account positions", the alignment report's own phrase): catalogued True, its three
    schwab_dim silver datasets still matched, and NO harvest_datasets match.
Read-only; no network (discover's freshness reads are lazy and not taken by a harvest_datasets row).
"""
import os
import sys

gw = os.path.abspath(sys.argv[1])
sys.path.insert(0, gw)
os.chdir(gw)
from app.graphql_plumbing import catalog_gate as g  # noqa: E402
from app.integrations.opal_discover import integration as od  # noqa: E402

ok = 0
for subject in ("harvested news articles and chatter", "security analysis research pack"):
    r = od.discover(subject, g.OPAL_INTERNAL)
    ms = r.get("matches", []) or []
    h = [m.get("dataset") for m in ms if m.get("channel") == "harvest_datasets"]
    good = r.get("catalogued") is True and len(h) >= 1
    ok += good
    print("DISCOVER %r catalogued=%s matches=%d harvest=%d first_harvest=%s %s"
          % (subject, r.get("catalogued"), len(ms), len(h), h[0] if h else "-", "OK" if good else "BAD"))
r = od.discover("Schwab account positions", g.OPAL_INTERNAL)
ms = r.get("matches", []) or []
ds = {m.get("dataset") for m in ms}
sch = len({"schwab_dim_position", "schwab_dim_balance", "schwab_dim_transaction"} & ds)
hv = sum(1 for m in ms if m.get("channel") == "harvest_datasets")
good = r.get("catalogued") is True and sch == 3 and hv == 0
ok += good
print("DISCOVER 'Schwab account positions' catalogued=%s matches=%d schwab_silver=%d of 3 harvest=%d %s"
      % (r.get("catalogued"), len(ms), sch, hv, "OK" if good else "BAD"))
print("discover reads good %d of 3" % ok)
sys.exit(0 if ok == 3 else 1)
