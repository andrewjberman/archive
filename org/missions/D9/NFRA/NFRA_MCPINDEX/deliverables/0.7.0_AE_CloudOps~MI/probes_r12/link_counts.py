"""link_counts.py <gateway dir> -- MX-r-12 PHASE A, amendment A1.

Prints MC Portal's per-tool catalog link counts as the breakdown page reads them: imports THAT gateway
tree's own app.admin_gateway_breakdown and calls _catalog_read_tool_rows(), so each tree is measured by
its OWN reader against its OWN DATA_CATALOG.yaml. Read-only, no network, MOCK_GRAPH=1.

Output: one `TOOL <name> <count>` line per tool, sorted, then `TOTALS tools=<n> links=<n>`.
"""
from __future__ import annotations

import os
import sys

gw = os.path.abspath(sys.argv[1])
os.environ.setdefault("MOCK_GRAPH", "1")
sys.path.insert(0, gw)
os.chdir(gw)

from app import admin_gateway_breakdown as agb  # noqa: E402

rows = agb._catalog_read_tool_rows()
tools = sorted(rows)
total = 0
for t in tools:
    n = len(rows[t])
    total += n
    print("TOOL %s %d" % (t, n))
print("TOTALS tools=%d links=%d" % (len(tools), total))
print("READER %s" % os.path.relpath(agb.__file__, gw).replace(os.sep, "/"))
print("CATALOG %s" % os.path.relpath(agb.CATALOG_YAML, gw).replace(os.sep, "/"))
