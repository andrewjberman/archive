import hashlib
import json
import subprocess
import sys
PIN = sys.argv[1]
names = sys.argv[2].split(",")
m = json.load(open("C:/dev/wk-irpt-bckend-268/infra/aws/lambda/ci/lambda-source-map.json", encoding="utf-8"))
e = m["functions"]["irpt-status"]
delta = []
for s in e["staged_from"]:
    if s["packaged_as"] in names:
        blob = subprocess.run(["git", "show", "%s:%s" % (PIN, s["repo_path"])], capture_output=True, cwd="C:/dev/wk-irpt-bckend-268").stdout
        new = hashlib.sha256(blob).hexdigest()
        delta.append({"packaged_as": s["packaged_as"], "repo_path": s["repo_path"], "pin_before": s["pin"], "sha256_before": s["sha256"],
                      "pin_after": PIN, "sha256_after": new, "unchanged_bytes": new == s["sha256"]})
        s["pin"], s["sha256"] = PIN, new
assert len(delta) == len(names), (len(delta), names)
json.dump(m, open(sys.argv[3], "w", encoding="utf-8"), indent=2)
json.dump(delta, open(sys.argv[3] + ".delta.json", "w"), indent=1)
for d in delta:
    print(d["packaged_as"], d["pin_before"][:10], "->", PIN[:10], "same-bytes" if d["unchanged_bytes"] else "MOVES")
