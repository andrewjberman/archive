"""host_refused.py <gateway dir> <tools.json>: the INSTALLED entitlement and tier decisions, called in-process on the gateway host (round 23, R23.7 step 3, REFUSED-CORRECT).

Run under the gateway's own venv through ap38_guard.py. For every tool name in <tools.json> ({"tools": [{"tool", "channel"}]}) and for each of the three tiers it
calls the same functions the served path calls, with an explicit UNPROFILED Access (no profile record), so NO access-store read happens and nothing is written:
  native tool (app/tools.py, goes through _run):  data_entitlement.decide -> guard.enforce -> entitlements.is_entitled(write_class)
  integration tool (run_integration_tool):        data_entitlement.decide -> guard.enforce_min_tier(spec.min_tier)
The first layer that denies is recorded with its code. The audit sink is stubbed. Prints a marker line then base64(gzip(JSON)).
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
                v = v[1:-1]
            os.environ.setdefault(k.strip(), v)
from app import audit  # noqa: E402

audit.log_call = lambda *a, **k: None
from app import integrations, tools as gw_tools  # noqa: E402
from app.config import get_config  # noqa: E402
from app import data_entitlement as de, guard, destructive_ops, entitlements  # noqa: E402
from app.integrations import registry  # noqa: E402
from app.tier import Tier  # noqa: E402

integrations.register_enabled(gw_tools.mcp, list(get_config().ENABLED_INTEGRATIONS))
doc = json.load(open(sys.argv[2], encoding="utf-8"))
UNPROFILED = de.Access(False, None, None, frozenset())
EMAIL = "tier-probe@opalinvest.com"
rows = []
for t in doc["tools"]:
    tool = t["tool"]
    spec = registry._ACTIVE_BY_TOOL.get(tool)
    path = "integration" if spec is not None else "native"
    tag = None
    wclass = None
    if spec is None:
        tag = guard.classify(tool)
        wclass = destructive_ops.write_class(tool)
    mutating = (spec is not None and not spec.read_only) or (spec is None and tag["class"] is not guard.OpClass.SAFE)
    per_tier = {}
    for tier in (Tier.READ_ONLY, Tier.STANDARD_EMPLOYEE, Tier.MASTER_ADMIN):
        verdict = {"admitted": True, "layer": None, "code": None}
        den = de.decide(tool, UNPROFILED, tier)
        if den is not None:
            verdict = {"admitted": False, "layer": "data_entitlement", "code": den.get("code")}
        elif spec is not None:
            try:
                guard.enforce_min_tier(tool, tier, spec.min_tier)
            except guard.GuardDenied as gd:
                verdict = {"admitted": False, "layer": "min_tier", "code": gd.code}
        else:
            try:
                guard.enforce(tool, EMAIL, tier)
            except guard.GuardDenied as gd:
                verdict = {"admitted": False, "layer": "guard", "code": gd.code}
            else:
                if wclass is not None and not entitlements.is_entitled(tier, wclass):
                    verdict = {"admitted": False, "layer": "write_class", "code": "write_class_denied"}
        per_tier[tier.value] = verdict
    rows.append({"tool": tool, "channel": t.get("channel"), "path": path, "mutating": bool(mutating),
                 "write_class": wclass, "min_tier": (spec.min_tier if spec is not None else None), "tiers": per_tier})
body = {"schema": "gateway_tier_decisions/1", "claim": "measured", "guard": "decide+enforce+enforce_min_tier+is_entitled, unprofiled Access, no store read",
        "tools": rows}
raw = json.dumps(body, separators=(",", ":"), default=str).encode("utf-8")
print("TIERS_B64GZ")
print(base64.b64encode(gzip.compress(raw)).decode("ascii"))
print("TIERS_BYTES %d TOOLS %d" % (len(raw), len(rows)))
