"""served_names_host.py -- runs ON the gateway host under its own venv and .env. READ-ONLY, no network.
Prints the DEPLOYED tree's SERVED tool names, one per line, by the same instrument c10_index.py uses:
app.integrations.register_enabled(mcp, ENABLED_INTEGRATIONS) then mcp._tool_manager.list_tools().
Importing the registry is load-bearing (row Z-S48): without register_enabled only the 43 native tools appear.
Never prints an env VALUE; ENABLED_INTEGRATIONS ids are not secret and are printed as the basis."""
import os
import sys

ROOT = "/opt/opal-gateway"
env = dict(os.environ)
with open(os.path.join(ROOT, ".env"), encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env.setdefault(k.strip(), v.strip('"'))
os.environ.update(env)
enabled = env.get("ENABLED_INTEGRATIONS", "").replace(",", " ").split()
sys.path.insert(0, ROOT)
os.chdir(ROOT)
from app import integrations as integ  # noqa: E402
from app import tools as gw_tools  # noqa: E402

native = sorted({t.name for t in gw_tools.mcp._tool_manager.list_tools()})
integ.register_enabled(gw_tools.mcp, enabled)
served = sorted({t.name for t in gw_tools.mcp._tool_manager.list_tools()})
print("---BASIS ids=%d %s" % (len(enabled), " ".join(enabled)))
print("---COUNTS native=%d served=%d integration=%d" % (len(native), len(served), len(served) - len(native)))
print("---SERVED")
for n in served:
    print(n)
