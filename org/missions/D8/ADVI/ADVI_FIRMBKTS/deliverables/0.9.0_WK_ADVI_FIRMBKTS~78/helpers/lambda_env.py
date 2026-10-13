import json
import re
import sys

D = "C:/dev/wk-firmbkts-78-data"
funcs = {x["FunctionName"]: x for x in json.load(open(D + "/lambdas.json", encoding="utf-8"))["Functions"]}
want = sys.argv[1:]
SECRETISH = re.compile(r"SECRET|TOKEN|PASS|CRED|KEY|AUTH|SALT|PRIVATE", re.I)
VALUE_OK = re.compile(r"^(opal-data-[a-z0-9-]+|us-east-1|[a-z0-9][a-z0-9_.-]{0,62})$")
for name in want:
    f = funcs.get(name)
    if not f:
        print("NOFUNC %s" % name)
        continue
    env = (f.get("Environment") or {}).get("Variables") or {}
    parts = []
    for k in sorted(env):
        v = env[k]
        if SECRETISH.search(k):
            parts.append("%s=<redacted>" % k)
        elif VALUE_OK.match(v or "") and not re.fullmatch(r"\d{9,}", v or ""):
            parts.append("%s=%s" % (k, v))
        else:
            parts.append("%s=<set>" % k)
    print("FN %s runtime=%s mem=%s timeout=%s role=%s" % (name, f.get("Runtime"), f.get("MemorySize"), f.get("Timeout"), (f.get("Role") or "").split("/")[-1]))
    print("   env: " + "; ".join(parts))
