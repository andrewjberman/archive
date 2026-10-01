"""host_probe_a1_tools.py -- runs ON the gateway host (SSM) under /opt/opal-gateway/.venv/bin/python as ec2-user.
READ-ONLY, in-process. The host .env is parsed in Python (KEY=VALUE split at the first '='), never shell-sourced
(row Z-S73). Prints: (1) the tool census with the host's own ENABLED_INTEGRATIONS; (2) A1 (MX-d-6): for the BD fees
ask and the 'Schwab positions' ask, the silver_datasets matches each of the 3 KNOWN_FIRMS receives (must be none) and
the silver next tools OPAL_INTERNAL receives (must include blackdiamond_list_fees and schwab_query).
No env value is printed; only tool names, dataset names and counts."""

import json
import os
import re
import sys

ROOT = "/opt/opal-gateway"
with open(os.path.join(ROOT, ".env"), encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v
sys.path.insert(0, ROOT)
os.chdir(ROOT)


def scrub(s):
    return re.sub(
        r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
        "<uuid>",
        str(s),
    )


from app import integrations  # noqa: E402
from app.tools import mcp  # noqa: E402

native = sorted(t.name for t in mcp._tool_manager.list_tools())
ids = os.environ["ENABLED_INTEGRATIONS"].split()
integrations.register_enabled(mcp, ids)
allnames = sorted(t.name for t in mcp._tool_manager.list_tools())
print(
    "---TOOLS",
    json.dumps(
        {
            "ids": ids,
            "native": len(native),
            "integration": len(allnames) - len(native),
            "total": len(allnames),
            "all": allnames,
        }
    ),
)

from app.graphql_plumbing import catalog_gate  # noqa: E402
from app.integrations.opal_discover import integration as od  # noqa: E402

asks = {
    "what fees did Black Diamond charge": "blackdiamond_list_fees",
    "Schwab positions": "schwab_query",
}
print("---KNOWN_FIRMS", len(catalog_gate.KNOWN_FIRMS), list(catalog_gate.KNOWN_FIRMS))
bad = 0
for ask, tool in asks.items():
    try:
        d = od.discover(ask, catalog_gate.OPAL_INTERNAL, "")
        tools = [
            (m.get("next_tool") or {}).get("name")
            for m in d.get("matches", [])
            if m.get("channel") == "silver_datasets"
        ]
        ok = tool in tools
        bad += 0 if ok else 1
        print("---A1 INTERNAL ask=%r silver_next_tools=%s want=%s %s" % (ask, tools, tool, "OK" if ok else "FAIL"))
    except Exception as e:
        bad += 1
        print("---A1 INTERNAL EXC", ask, type(e).__name__, scrub(e)[:200])
for firm in catalog_gate.KNOWN_FIRMS:
    for ask in asks:
        try:
            d = od.discover(ask, "firm", firm)
            silver = [m.get("dataset") for m in d.get("matches", []) if m.get("channel") == "silver_datasets"]
            ok = silver == []
            bad += 0 if ok else 1
            print(
                "---A1 FIRM %s ask=%r silver_matches=%d catalogued=%s %s"
                % (firm, ask, len(silver), d.get("catalogued"), "OK" if ok else "FAIL")
            )
        except Exception as e:
            bad += 1
            print("---A1 FIRM EXC", firm, ask, type(e).__name__, scrub(e)[:200])
print("---A1 VERDICT", "PASS" if bad == 0 else "FAIL", "failures=%d of %d legs" % (bad, 2 + 2 * len(catalog_gate.KNOWN_FIRMS)))
