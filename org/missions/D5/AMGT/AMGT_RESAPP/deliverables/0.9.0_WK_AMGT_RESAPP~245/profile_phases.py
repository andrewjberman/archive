"""AMGT-aw-1 -- a fresh-process local profile of the cold first request, per route, before and after the cut.

profile_phases.py <before|after> <route> [repeats]   (repo root as cwd, PYTHONPATH=<repo root>)
  route: trending | breakout | chatter
  `before` turns the stored-name read off (`_refdata_name` answers None), which is exactly the path the code took
  before this cell: every unnamed row reads its model block. `after` runs the code as it stands.
Each repeat is a NEW python process; one request; the AMGT_PHASE lines and the wall total are printed as JSON.
"""

import json
import re
import subprocess
import sys

ROUTES = {
    "trending": ("/lead-panel/rankings/trending/price", None),
    "breakout": ("/lead-panel/rankings/breakout/price", None),
    "chatter": ("/lead-panel/timeseries/collected/chatter", {"days": "30"}),
}

CHILD = """
import json, sys, time
t0 = time.monotonic()
from lib.research.api import scoped_amgt
if sys.argv[1] == "before":
    scoped_amgt._refdata_name = lambda key: None
import botocore.client
counts = {"model_block": 0, "refdata": 0, "other": 0}
orig = botocore.client.BaseClient._make_api_call
def counted(self, op, params):
    if op == "GetObject":
        k = str(params.get("Key", ""))
        counts["model_block" if k.startswith("derived/model_block/") else "refdata" if "/refdata/" in k else "other"] += 1
    return orig(self, op, params)
botocore.client.BaseClient._make_api_call = counted
path, q = json.loads(sys.argv[2])
init_ms = (time.monotonic() - t0) * 1000
t1 = time.monotonic()
r = scoped_amgt.handler({"rawPath": "/api/scoped/amgt" + path, "requestContext": {"http": {"method": "GET"}},
                         "headers": {"x-firm-id": "opal"}, "queryStringParameters": q})
print("TOTAL_MS", round((time.monotonic() - t1) * 1000), "INIT_MS", round(init_ms), "STATUS", r["statusCode"],
      "GETS", json.dumps(counts))
"""


def one(mode, route):
    path, q = ROUTES[route]
    p = subprocess.run([sys.executable, "-c", CHILD, mode, json.dumps([path, q])], capture_output=True, timeout=900)
    out = p.stdout.decode("utf-8", errors="replace")
    phases = {}
    for m in re.finditer(r"AMGT_PHASE route=\S+ phase=(.+?) ms=(\d+)", out):
        phases[m.group(1)] = phases.get(m.group(1), 0) + int(m.group(2))
    t = re.search(r"TOTAL_MS (\d+) INIT_MS (\d+) STATUS (\d+) GETS (\{.*\})", out)
    return {"phases": phases, "total_ms": int(t.group(1)), "init_ms": int(t.group(2)), "status": int(t.group(3)),
            "gets": json.loads(t.group(4))} if t else {"error": (out + p.stderr.decode("utf-8", errors="replace"))[-600:]}


def main():
    mode, route = sys.argv[1], sys.argv[2]
    repeats = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    print(json.dumps({"mode": mode, "route": route, "runs": [one(mode, route) for _ in range(repeats)]}))


if __name__ == "__main__":
    main()
