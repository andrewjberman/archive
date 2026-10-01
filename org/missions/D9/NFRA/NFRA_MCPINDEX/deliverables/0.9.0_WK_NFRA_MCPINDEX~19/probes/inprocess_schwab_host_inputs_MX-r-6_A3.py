"""MX-r-6 A3 in-process proof (read-only) -- run inside the DEPLOY-ONLY artifact, with the release's .env shape.

argv[1] = extracted artifact dir; argv[2] = the deploy-only tree's deploy-to-ec2.sh; argv[3] = 'with' | 'without' (negative control).
The process environment is the operator's own (AWS read credentials) plus ONLY the static KEY=value pairs of the
.env printf (REMOTE_DIR mapped to the extracted dir). No value of any secret is printed.
"""
import asyncio
import os
import re
import sys

root, script, mode = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(script, encoding="utf-8").read()
line = next(ln for ln in text.splitlines() if ln.startswith("printf 'MOCK_GRAPH=0"))
fmt = re.match(r"printf '(.*?)' ", line).group(1)
pairs = {}
for item in fmt.split("\\n"):
    if "=" in item:
        k, _, v = item.partition("=")
        if v != "%s":
            pairs[k] = v.replace("${REMOTE_DIR}", root)
if mode == "with":
    os.environ.update({k: v for k, v in pairs.items() if k.startswith(("NFRA_OPLGTW", "SCHWAB_"))})
    os.environ["ENABLED_INTEGRATIONS"] = pairs["ENABLED_INTEGRATIONS"]
for k in [k for k in os.environ if k.startswith("SCHWAB_") and mode == "without"]:
    del os.environ[k]
print("MODE", mode, "ENV KEYS SET:", sorted(k for k in os.environ if k.startswith(("NFRA_OPLGTW", "SCHWAB_"))))
print("CONTRACT PATH EXISTS:", os.path.isfile(os.environ.get("NFRA_OPLGTW_CONTRACT_PATH", "")))
sys.path.insert(0, root)
os.chdir(root)

from app.integrations.schwab import integration as si  # noqa: E402

# 1. the construction the first Schwab call performs
try:
    service = si.build_default_service()
    print("BUILD: OK", type(service).__name__)
except Exception as exc:  # noqa: BLE001
    print("BUILD: RAISED", type(exc).__name__, str(exc)[:160])
    service = None


# 2. the tools themselves (the OG-z-1 admission chokepoint needs a live principal: its seam is disclosed and replaced)
class _Mcp:
    def __init__(self):
        self.fns = {}

    def tool(self, name=None, **_kw):
        def deco(fn):
            self.fns[name or fn.__name__] = fn
            return fn
        return deco


si._admit = lambda tool: None
mcp = _Mcp()
integration = si.SchwabIntegration()
print("REGISTERED:", integration.register(mcp))


def code_of(result):
    sc = getattr(result, "structuredContent", None)
    if isinstance(sc, dict):
        e = sc.get("error")
        if isinstance(e, dict):
            return {k: e.get(k) for k in ("code", "reason", "where") if k in e}
        return {"error": str(e)[:120]}
    return [getattr(c, "text", "")[:160] for c in (getattr(result, "content", None) or [])]


for name, kwargs in (("schwab_get_access", {}),
                     ("schwab_list_files", {"master": "08242234", "dataset": "dim_position"})):
    try:
        res = asyncio.run(mcp.fns[name](**kwargs))
        print("TOOL", name, "isError=%s" % getattr(res, "isError", None), code_of(res))
    except Exception as exc:  # noqa: BLE001
        print("TOOL", name, "RAISED", type(exc).__name__, str(exc)[:160])
