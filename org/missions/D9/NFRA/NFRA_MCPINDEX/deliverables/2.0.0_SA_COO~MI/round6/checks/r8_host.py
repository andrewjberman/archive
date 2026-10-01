"""r8_host.py -- runs ON the gateway host (shipped via SSM by r8.AC2.sh) under /opt/opal-gateway/.venv/bin/python.
Loads /opt/opal-gateway/.env the way systemd's EnvironmentFile does (KEY=VALUE per line, split at the first '='),
NEVER through a shell -- the file's values are unquoted, and a shell source echoes values in its errors. Prints only
the next tools discover names for two asks; no env value is printed."""
import os
import sys

ROOT = "/opt/opal-gateway"
with open(os.path.join(ROOT, ".env"), encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v)
sys.path.insert(0, ROOT)
os.chdir(ROOT)
from app.graphql_plumbing import catalog_gate as g  # noqa: E402
from app.integrations.opal_discover import integration as od  # noqa: E402


def names(q):
    return [((m.get("next_tool") or {}).get("name")) for m in od.discover(q, g.OPAL_INTERNAL).get("matches", [])]


print("bd=" + ",".join(map(str, names("what fees did Black Diamond charge"))))
print("etf=" + ",".join(map(str, names("ETF positioning"))))
