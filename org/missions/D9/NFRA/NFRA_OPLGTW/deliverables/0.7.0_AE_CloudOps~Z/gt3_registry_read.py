#!/usr/bin/env python
"""OG-ap-18 Phase B STEP 0: read the HOST's live MCP registry BY NAME. READ-ONLY.

Runs ON i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python, pulled from S3 (Rule 12). It
imports app.tools and lists the registry; it writes nothing, calls no AWS service and touches no store.

WHY BY NAME AND NOT BY COUNT. The CTO's STEP 0 condition is that the repo-side count (65) and the
host-side count (46) differ by an EXPLAINED and CONSTANT 19. Two counts differing by 19 is consistent
with any number of stories, including a tool silently missing from the host and a different one
silently extra. Only the NAMES can say which 19, so this prints the full sorted list and the caller does
the set algebra against the repo-side sets it computed from app/data_entitlement.py at the same ref.

It also prints the three repo-side sets AS THE HOST HAS THEM, so the comparison does not depend on my
checkout being the same bytes as the host: if the host's own data_entitlement disagrees with the repo at
the ref I think is live, that shows here rather than hiding behind a matching total.
"""
from __future__ import annotations

import json
import os
import sys
import traceback

ROOT = "/opt/opal-gateway"


def main() -> int:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    out = {}
    from app import tools

    try:
        names = [t.name for t in tools.mcp._tool_manager.list_tools()]
        out["instrument"] = "app.tools.mcp._tool_manager.list_tools()"
    except Exception:
        import asyncio
        names = [t.name for t in asyncio.run(tools.mcp.list_tools())]
        out["instrument"] = "asyncio.run(app.tools.mcp.list_tools())"
    out["live_registry_count"] = len(names)
    out["live_registry_names"] = sorted(names)
    out["duplicate_names"] = sorted({n for n in names if names.count(n) > 1})

    # the host's OWN copy of the classification sets, so a repo/host divergence cannot hide
    from app import data_entitlement as de
    out["host_side_sets"] = {
        "NATIVE_TOOLS": sorted(de.NATIVE_TOOLS),
        "INTEGRATION_TOOLS": sorted(de.INTEGRATION_TOOLS),
        "INDEX_TOOLS": sorted(de.INDEX_TOOLS),
    }
    out["host_side_counts"] = {k: len(v) for k, v in out["host_side_sets"].items()}
    union = set(de.NATIVE_TOOLS) | set(de.INTEGRATION_TOOLS) | set(de.INDEX_TOOLS)
    out["host_side_union_count"] = len(union)
    out["live_minus_union"] = sorted(set(names) - union)       # live tools no set classifies
    out["union_minus_live"] = sorted(union - set(names))       # classified tools not live
    out["enabled_integrations_names_only"] = sorted(
        (os.environ.get("ENABLED_INTEGRATIONS") or "").replace(",", " ").split())
    print("REGISTRY_READ_JSON")
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("REGISTRY_READ_JSON")
        print(json.dumps({"fatal": traceback.format_exc()[-1500:]}, indent=1))
        sys.exit(1)
