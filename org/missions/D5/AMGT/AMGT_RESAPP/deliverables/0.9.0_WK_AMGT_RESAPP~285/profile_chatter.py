"""AMGT-ba-19 step 3: time each UNLABELLED span of the chatter handler locally, in a FRESH process, with time.perf_counter
around the handler's own calls. No file under lib/ is edited. Run: python profile_chatter.py [--full]

Spans (scoped_amgt.handler, route /api/scoped/amgt/lead-panel/timeseries/collected/chatter):
  S0 module import of scoped_amgt           -- Init, outside Duration (reference only)
  S1 routing + authorisation                -- _scheduled_action_response, _path, _firm_id, _method, _route_template, _query
  S2 request-time import of the chatter module chain -- `from lib.research.api import monthly_chatter, rolling_windows`
  S3 parse_days
  S4 the response serialisation (_response on a stub body of the served shape; the real one is the labelled `serialize` phase)
  --full: one end-to-end handler call after the spans (warm imports), printing the AMGT_PHASE lines it emits.
The local split is an INFERENCE about the deployed one (different CPU, memory share, disk, Python and package build).
"""
import json
import subprocess
import sys
import time

root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
sys.path.insert(0, root)
pc = time.perf_counter
out = {}

t = pc()
from lib.research.api import scoped_amgt  # noqa: E402

out["S0_import_scoped_amgt_ms"] = (pc() - t) * 1000
heavy_before = {m for m in ("pyarrow", "boto3", "numpy", "pandas") if m in sys.modules}

event = {"rawPath": "/api/scoped/amgt/lead-panel/timeseries/collected/chatter", "requestContext": {"http": {"method": "GET"}},
         "headers": {"x-firm-id": "opal"}, "queryStringParameters": {"days": "30"}}

t = pc()
scoped_amgt._scheduled_action_response(event)
path = scoped_amgt._path(event)
firm = scoped_amgt._firm_id(event)
rest = [s for s in path[len(scoped_amgt.ROUTE_PREFIX):].split("/") if s]
method = scoped_amgt._method(event)
scoped_amgt._route_template(rest, method)
query = scoped_amgt._query(event)
out["S1_routing_auth_ms"] = (pc() - t) * 1000

mods_before = set(sys.modules)
t = pc()
from lib.research.api import monthly_chatter, rolling_windows  # noqa: E402,F401

out["S2_request_time_import_ms"] = (pc() - t) * 1000
new = set(sys.modules) - mods_before
out["S2_new_modules"] = len(new)
out["S2_new_top_level"] = sorted({m.split(".")[0] for m in new})
out["S2_heavy_loaded_by_S2"] = sorted({m for m in ("pyarrow", "boto3", "numpy", "pandas") if m not in heavy_before and m in sys.modules})

t = pc()
rolling_windows.parse_days(query.get("days"))
out["S3_parse_days_ms"] = (pc() - t) * 1000

body = {"as_of": "2026-10-06", "rows": [{"security_key": "K%d" % i, "display_name": "N", "by_month": {"2026-09": {"collected": 1, "by_publisher": {"p": 1}}}}
                                         for i in range(1500)]}
t = pc()
scoped_amgt._response(200, body)
out["S4_response_stub_1500_rows_ms"] = (pc() - t) * 1000

if "--full" in sys.argv:
    t = pc()
    r = scoped_amgt.handler(event)
    out["FULL_handler_warm_imports_ms"] = (pc() - t) * 1000
    out["FULL_status"] = r.get("statusCode")
    out["FULL_body_bytes"] = len(r.get("body") or "")
print("PROFILE_JSON " + json.dumps(out))
