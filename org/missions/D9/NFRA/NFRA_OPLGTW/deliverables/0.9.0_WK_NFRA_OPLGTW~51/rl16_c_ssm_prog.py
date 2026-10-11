"""OG-rl-16 PHASE C host program (adapted from the ~43 r29 / ~48 tl1 host programs; the field set is this order's).
Run by rl16_ssm_prog.py as a SEPARATE process (env -i, the installed venv, cwd /opt/opal-gateway; never the running service).
argv[1] = mode label, argv[2] = the served release sha (the EC2_MANIFEST deployed_commit, passed in as the r29 template does).
Reads the INSTALLED code in /opt/opal-gateway: the installed tool list, SAFE_TOOLS / write_class, ONE call through the installed
module's own entry copy_site_file_to_s3 with quarter 2026Q9 (graph_call and s3_client are COUNTING STAND-INS, so even a regression
could neither read SharePoint nor write S3), the host .env (a VALUE compare inside the process; only booleans leave it; no .env
value is ever printed), and the installed botocore's S3 PutObject input shape.
Prints booleans, counts and the body; never a value, a token or a credential."""
import asyncio
import hashlib
import json
import os
import re
import subprocess
import sys

GW = "/opt/opal-gateway"
served = sys.argv[2] if len(sys.argv) > 2 else ""
sys.path.insert(0, GW)
WANT_ROOT = "s3://opal-data-assets/smartx/49financial/bronze/fee_statement/"
TOOL = "copy_site_file_to_s3"

pid = subprocess.check_output(["systemctl", "show", "opal-gateway", "-p", "MainPID", "--value"]).decode().strip()
enabled = ""
for kv in open("/proc/%s/environ" % pid, "rb").read().split(bytes([0])):
    if kv.startswith(b"ENABLED_INTEGRATIONS="):
        enabled = kv.split(b"=", 1)[1].decode("utf-8", "replace")
os.environ["ENABLED_INTEGRATIONS"] = enabled
os.environ["MOCK_GRAPH"] = "1"

from mcp.server.fastmcp import FastMCP  # noqa: E402
from app import tools, integrations, destructive_ops  # noqa: E402

integrations.register_enabled(tools.mcp, enabled.split())
names = sorted(t.name for t in asyncio.run(FastMCP.list_tools(tools.mcp)))
installed_code = os.path.dirname(os.path.abspath(tools.__file__)) == GW + "/app"
tool_listed = TOOL in names
tool_safe = TOOL in destructive_ops.SAFE_TOOLS
tool_write_class = destructive_ops.write_class(TOOL)
holders = sum(1 for n in names if destructive_ops.write_class(n) == "write_files")

# the .env: parse in memory, compare the one value, test the other key's presence; nothing leaves the process but booleans
env = {}
for ln in open(GW + "/.env", encoding="utf-8", errors="replace"):
    ln = ln.strip()
    if not ln or ln.startswith("#") or "=" not in ln:
        continue
    k, v = ln.split("=", 1)
    k = re.sub(r"^export\s+", "", k.strip())
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    env[k] = v
fee_root_equals_address = env.get("ADVI_FEE_STATEMENT_S3_ROOT") == WANT_ROOT
market_update_root_present = "ADVI_MARKET_UPDATE_S3_ROOT" in env
# the process's own environment must carry the root for the installed module's destination_root (it reads os.environ); the
# refusal on a bad quarter comes BEFORE that, and we do not export any .env value into this process.

# ONE call through the installed module's own entry, quarter 2026Q9, with counting stand-ins
from app.integrations.advi_billing import site_to_s3  # noqa: E402

calls = {"graph": 0, "s3": 0}


def _graph(*a, **k):
    calls["graph"] += 1
    raise RuntimeError("stand-in graph_call reached")


class _S3:
    def __getattr__(self, name):
        def _f(*a, **k):
            calls["s3"] += 1
            raise RuntimeError("stand-in s3 reached")
        return _f


try:
    site_to_s3.copy_site_file_to_s3("stand-in-token", "stand-in-site", "stand-in-item", "2026Q9", graph_call=_graph, s3_client=_S3())
    refused = False
except site_to_s3.SiteToS3Refused:
    refused = True
except Exception:  # noqa: BLE001 -- anything else is NOT a refusal
    refused = False
bad_quarter_refused = refused and calls["graph"] == 0 and calls["s3"] == 0
objects_written = calls["s3"]   # a stand-in s3 call is counted; the stand-in can write nothing

import botocore.session  # noqa: E402

members = botocore.session.get_session().get_service_model("s3").operation_model("PutObject").input_shape.members
put_ok = "IfNoneMatch" in members

body = {"served_release": served, "installed_code": installed_code, "tool_listed": tool_listed, "tool_safe": tool_safe,
        "tool_write_class": tool_write_class, "bad_quarter_refused": bad_quarter_refused, "objects_written": objects_written,
        "fee_root_equals_address": fee_root_equals_address, "market_update_root_present": market_update_root_present,
        "put_object_accepts_if_none_match": put_ok, "write_files_holders": holders}
s = json.dumps(body, sort_keys=True)
print("RL16C_AUX tools=%d graph_calls=%d s3_calls=%d tools_py_md5=%s destructive_ops_md5=%s"
      % (len(names), calls["graph"], calls["s3"], hashlib.md5(open(GW + "/app/tools.py", "rb").read()).hexdigest(),
         hashlib.md5(open(GW + "/app/destructive_ops.py", "rb").read()).hexdigest()))
print("E2_BODY " + s)
print("E2_DIGEST " + hashlib.sha256(s.encode("utf-8")).hexdigest())
