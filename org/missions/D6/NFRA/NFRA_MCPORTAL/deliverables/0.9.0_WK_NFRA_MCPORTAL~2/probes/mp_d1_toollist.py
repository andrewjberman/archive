"""TO-MP-d-1 4a(iii): list the MCP tool names REGISTERED on the host's gateway, read-only.

Run on-box from /opt/opal-gateway as ec2-user through the service's own venv, with the service's own .env loaded
the way systemd's EnvironmentFile does (KEY=VALUE per line, no shell parsing). Prints keys never values: only the
tool names and their count. Imports app.server so every registration the running service performs at import
(native tools + ENABLED_INTEGRATIONS) is performed here too; the per-principal discovery filter is NOT applied --
this is the registered surface, not one caller's view. Same script before and after the act.
"""
import os
import sys

with open(".env", encoding="utf-8") as fh:
    for raw in fh:
        line = raw.rstrip("\r\n")
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v

sys.path.insert(0, os.getcwd())
from app import server  # noqa: E402,F401  -- performs the service's own registrations
from app.tools import mcp  # noqa: E402

names = sorted(t.name for t in mcp._tool_manager.list_tools())
print("TOOLCOUNT", len(names))
for n in names:
    print("TOOL", n)
