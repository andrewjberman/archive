"""IB-pr-482 candidate source map writer. From the worktree root:
    python <this file> <pin> <out_json>
Reads infra/aws/lambda/ci/lambda-source-map.json at HEAD and writes a map holding ONLY irpt-performance-adapter, every key verbatim, in which
ONLY the staged_from row of holdings_gold.py is re-pinned to <pin> (sha256 recomputed from `git show <pin>:<repo_path>`). Every other member
keeps the pin and sha256 it has. lambda-source-map.json itself is NOT edited. ASCII only.
"""
import hashlib
import json
import subprocess
import sys

pin, out = sys.argv[1], sys.argv[2]
FULL = subprocess.run(["git", "rev-parse", pin], capture_output=True, check=True).stdout.decode().strip()
FN = "irpt-performance-adapter"
MEMBER = "holdings_gold.py"
smap = json.loads(subprocess.run(["git", "show", "HEAD:infra/aws/lambda/ci/lambda-source-map.json"], capture_output=True, check=True).stdout.decode("utf-8"))
doc = {k: v for k, v in smap.items() if k != "functions"}
doc["_note_IB_pr_482"] = "CANDIDATE (IRPT_BCKEND IB-pr-482, worker ~337): irpt-performance-adapter only; the holdings_gold.py row re-pinned to %s. Not the source map." % FULL
e = json.loads(json.dumps(smap["functions"][FN]))
repins = []
for s in e["staged_from"]:
    if s["packaged_as"] != MEMBER:
        continue
    r = subprocess.run(["git", "show", "%s:%s" % (FULL, s["repo_path"])], capture_output=True)
    if r.returncode:
        sys.exit("ERROR: %s is not at %s" % (s["repo_path"], FULL[:10]))
    sha = hashlib.sha256(r.stdout).hexdigest()
    repins.append({"member": MEMBER, "repo_path": s["repo_path"], "old_pin": s["pin"], "new_pin": FULL, "old_sha256": s["sha256"], "new_sha256": sha})
    s["pin"], s["sha256"] = FULL, sha
doc["functions"] = {FN: e}
doc["_repins_IB_pr_482"] = repins
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(doc, indent=2) + "\n")
print(json.dumps(repins, indent=1))
