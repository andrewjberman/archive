"""link_counts_real_host.py -- runs ON the gateway host under its own venv. READ-ONLY, no network, no write.

The CONTROL for the A1 link-count comparison: takes the LIVE side by IMPORTING the real installed
app.admin_gateway_breakdown and calling _catalog_read_tool_rows(), so the off-host ast-exec mechanism can be
checked against the module's own answer on the one side where both are available. Prints per-tool counts and
totals only -- no row ids, no env values.
"""

import os
import sys

ROOT = "/opt/opal-gateway"
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from app import admin_gateway_breakdown as agb  # noqa: E402

rows = agb._catalog_read_tool_rows()
counts = {t: len(ids) for t, ids in rows.items()}
print("---REAL reader=%s catalog=%s" % (agb.__file__, agb.CATALOG_YAML))
for t in sorted(counts):
    print("REAL TOOL %s %d" % (t, counts[t]))
print("---REAL TOTALS tools=%d links=%d" % (len(counts), sum(counts.values())))
