"""IB-pr-456 candidate source map writer (from IB-pr-426's and IB-pr-416's; ASCII). From the worktree root:
    python <this file> <base_commit> <out_map_json> <out_repins_json> [<map_ref>]
Reads infra/aws/lambda/ci/lambda-source-map.json AT <map_ref> (default HEAD) and writes the SAME map (every function, every key verbatim)
except that, in each function the census found, ONLY the staged_from rows whose repo_path is one of the three changed members
(ycharts/generate/submission.py, ycharts/generate/acceptance.py, the AnalysisSubmissionRequest schema) are re-pinned to <base_commit>
with sha256 recomputed from `git show <base_commit>:<repo_path>`. A function whose copy of a member is NATIVE to its source_dir
(irpt-ycharts-generate's submission.py and acceptance.py) has no row to re-pin: the builder reads them from the worktree, which IS
<base_commit>. lambda-source-map.json is NOT edited. <out_repins_json> is the small diff (member, old/new pin, sha256 prefixes)."""
import hashlib
import json
import subprocess
import sys

base, out_map, out_repins = sys.argv[1], sys.argv[2], sys.argv[3]
REF = sys.argv[4] if len(sys.argv) > 4 else "HEAD"
FULL = subprocess.run(["git", "rev-parse", base], capture_output=True, check=True).stdout.decode().strip()
G = "infra/aws/lambda/investor-reporting/ycharts/generate/"
THREE = {G + "submission.py", G + "acceptance.py", "docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json"}
raw = subprocess.run(["git", "show", REF + ":infra/aws/lambda/ci/lambda-source-map.json"], capture_output=True, check=True).stdout.decode("utf-8")
smap = json.loads(raw)
repins = []
for fn, e in smap["functions"].items():
    for s in e.get("staged_from") or []:
        if s["repo_path"] not in THREE:
            continue
        r = subprocess.run(["git", "show", "%s:%s" % (FULL, s["repo_path"])], capture_output=True)
        if r.returncode:
            sys.exit("ERROR: %s is not at %s" % (s["repo_path"], FULL[:10]))
        sha = hashlib.sha256(r.stdout).hexdigest()
        repins.append({"function": fn, "packaged_as": s["packaged_as"], "repo_path": s["repo_path"], "old_pin": s["pin"], "new_pin": FULL,
                       "old_sha256_prefix": s["sha256"][:12], "new_sha256_prefix": sha[:12], "bytes_changed": s["sha256"] != sha})
        s["pin"], s["sha256"] = FULL, sha
with open(out_map, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(smap, indent=2) + "\n")
with open(out_repins, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps({"base_commit": FULL, "map_ref": REF, "rows_repinned": len(repins), "repins": repins}, indent=1) + "\n")
print("rows re-pinned: %d" % len(repins))
for x in repins:
    print(x["function"], x["packaged_as"], x["old_pin"][:10], "->", FULL[:10], "bytes_changed=%s" % x["bytes_changed"])
