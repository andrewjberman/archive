"""tools_census.py <extracted-artifact-dir> <out.json>: in-process tool census (MOCK_GRAPH=1), the 7 live ids. No network, no host env."""

import json
import os
import sys

root = os.path.abspath(sys.argv[1])
os.chdir(root)
sys.path.insert(0, root)
os.environ.update(
    {"MOCK_GRAPH": "1", "IDENTITY_PROVIDER": "alb_oidc", "ENABLED_INTEGRATIONS": ""}
)
from app import integrations  # noqa: E402
from app.tools import mcp  # noqa: E402

native = sorted(t.name for t in mcp._tool_manager.list_tools())
ids = "ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond".split()
rep = integrations.register_enabled(mcp, ids)
allnames = sorted(t.name for t in mcp._tool_manager.list_tools())
json.dump(
    {
        "ids": ids,
        "native": len(native),
        "integration": len(allnames) - len(native),
        "total": len(allnames),
        "all": allnames,
    },
    open(sys.argv[2], "w"),
    indent=1,
)
print(
    root,
    "ids=%d native=%d integration=%d total=%d"
    % (len(ids), len(native), len(allnames) - len(native), len(allnames)),
)
