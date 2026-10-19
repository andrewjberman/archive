"""host_breakdown.py <gateway dir>: the SERVED /gateway page's own data, read ON the gateway host (round 22, FWD-23/24/25 denominator).

Run IN-PROCESS under the gateway's own venv against its deployed code: it calls app.admin_gateway_breakdown._compute(), the function behind GET
/api/admin/gateway/breakdown that the /gateway page renders (channels of every kind, the tools under each, each tool's catalog `indexes`, the
(vendor, firm) segments of opal-data-assets and opal-data-bd, and the holders). READ-ONLY: _compute() writes nothing; the audit sink is stubbed.
Prints one marker line, then base64(gzip(JSON)) of the body, so the SSM output cap (24000 chars) does not truncate it.
"""
import base64
import gzip
import json
import os
import sys

gw = os.path.abspath(sys.argv[1])
sys.path.insert(0, gw)
os.chdir(gw)
with open(os.path.join(gw, ".env"), encoding="utf-8", errors="replace") as fh:
    for line in fh:
        line = line.rstrip("\n")
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            v = v.strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]    # systemd's EnvironmentFile strips one pair of surrounding quotes; a bare split would leave '"ycharts' and 'blackdiamond"'
            os.environ.setdefault(k.strip(), v)
from app import audit  # noqa: E402
from app import admin_gateway_breakdown as bd  # noqa: E402

audit.log_call = lambda *a, **k: None
# The served process registers the ENABLED_INTEGRATIONS onto the shared `mcp` at app/server.py import (line ~91), BEFORE the page's data is
# computed. A fresh process that imports only admin_gateway_breakdown sees the native tools alone (round 22's first read: 103 tools, no
# integration channel -- an undercount). Register them the same way the service does, from the same env, before _compute().
from app import integrations, tools as gw_tools  # noqa: E402
from app.config import get_config  # noqa: E402
_enabled = list(get_config().ENABLED_INTEGRATIONS)
_report = integrations.register_enabled(gw_tools.mcp, _enabled)
print("INTEGRATIONS_ENABLED %s" % ",".join(_enabled))
print("INTEGRATIONS_REGISTERED %s" % ",".join("%s:%d" % (k, len(v.get("tools", []))) for k, v in sorted(_report.items())))
body = bd._compute()
raw = json.dumps(body, separators=(",", ":"), default=str).encode("utf-8")
print("BREAKDOWN_B64GZ")
print(base64.b64encode(gzip.compress(raw)).decode("ascii"))
print("BREAKDOWN_BYTES %d" % len(raw))
