"""IB-pr-456 live configuration read (AWS READ ONLY: lambda get-function-configuration through .tools/aws; ASCII). From the worktree root:
    python <this file> <out_json> <fn> [<fn> ...]
Records handler, runtime, memory, timeout, the role NAME (not the ARN), the layer NAMES and versions (not the ARNs), and the environment variable NAMES
(never the values). No account id is written."""
import json
import subprocess
import sys

out, fns = sys.argv[1], sys.argv[2:]
rows = []
for fn in fns:
    r = subprocess.run(["bash", ".tools/aws", "lambda", "get-function-configuration", "--function-name", fn, "--output", "json"], capture_output=True, timeout=120)
    if r.returncode:
        raise SystemExit("aws failed for %s: %s" % (fn, r.stderr.decode("utf-8", "replace")[-200:]))
    c = json.loads(r.stdout.decode("utf-8"))
    layers = []
    for ly in c.get("Layers", []):
        parts = ly["Arn"].split(":")
        layers.append("%s:%s" % (parts[6], parts[7]) if len(parts) > 7 else "?")
    rows.append({"function": fn, "handler": c["Handler"], "runtime": c["Runtime"], "memory": c["MemorySize"], "timeout": c["Timeout"], "role_name": c["Role"].split("/")[-1],
                 "layers": layers, "environment_variable_names": sorted((c.get("Environment") or {}).get("Variables", {})), "code_sha256": c["CodeSha256"],
                 "last_modified": c["LastModified"], "package_type": c.get("PackageType")})
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps({"live_configuration": rows}, indent=1) + "\n")
for x in rows:
    print(x["function"], x["handler"], x["runtime"], x["memory"], x["timeout"], x["role_name"], x["layers"], len(x["environment_variable_names"]))
