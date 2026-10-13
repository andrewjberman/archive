"""FB-k-2 read-only summariser: reads a saved `aws lambda list-functions --output json` file and
prints, per function, only what the inventory needs: name, runtime, role name, last-modified, the
environment variable NAMES, and a value only for bucket/region/table/queue-shaped keys whose value is
a bucket name (opal-data-*), a region, or a plain resource name. Secret-shaped keys are never printed
as values. Usage: python -I planinv_lambda_summary.py <list-functions.json> [--match REGEX]
"""
import json
import re
import sys

ARGS = sys.argv[1:]
if not ARGS:
    sys.exit("usage: planinv_lambda_summary.py <list-functions.json> [--match REGEX]")
path = ARGS[0]
match = re.compile(ARGS[ARGS.index("--match") + 1]) if "--match" in ARGS else None

SECRETISH = re.compile(r"SECRET|TOKEN|PASS|KEY|CRED|JWT|PRIVATE|COOKIE|AUTH", re.I)
VALUEKEY = re.compile(r"BUCKET|REGION|TABLE|QUEUE|TOPIC|PREFIX|FIRM|SCOPE|HOME|DEST|SOURCE|TARGET", re.I)
BUCKETISH = re.compile(r"^opal-data-[a-z0-9-]+$|^opal-[a-z0-9-]+$|^us-east-1$")

with open(path, encoding="utf-8") as fh:
    funcs = json.load(fh)["Functions"]

scanned = 0
shown = 0
legacy_env = 0
for f in sorted(funcs, key=lambda x: x["FunctionName"]):
    scanned += 1
    name = f["FunctionName"]
    env = (f.get("Environment") or {}).get("Variables", {}) or {}
    if match is None:
        continue
    if not (match.search(name) or any(match.search(k) for k in env) or match.search(f.get("Role", ""))
            or any("opal-data-" in str(v) for v in env.values())):
        continue
    shown += 1
    vals = []
    hits_legacy = False
    for k in sorted(env):
        v = str(env[k])
        if "opal-data-inf" in v or "opal-data-bd" in v or "opal-data-cot" in v:
            hits_legacy = True
        if VALUEKEY.search(k) and not SECRETISH.search(k) and BUCKETISH.match(v):
            vals.append("%s=%s" % (k, v))
        elif "opal-data-" in v and not SECRETISH.search(k):
            vals.append("%s=<bucket-shaped>" % k)
    legacy_env += 1 if hits_legacy else 0
    print("FN %s | runtime=%s | role=%s | modified=%s | env_names=%s" % (
        name, f.get("Runtime", "-"), f.get("Role", "").split("/")[-1], f.get("LastModified", "-")[:19],
        ",".join(sorted(env.keys())) or "none"))
    if vals:
        print("   values: " + "; ".join(vals))
    if hits_legacy:
        print("   LEGACY-IN-ENV: env value names an opal-data-inf/bd/cot bucket")

print("SUMMARY scanned=%d matched=%d env_legacy=%d" % (scanned, shown, legacy_env))
