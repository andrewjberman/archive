"""IB-pr-416 candidate source map writer (TO AMENDMENT 2: ONE commit for the whole function). From the worktree root:
    python <this file> <pin> <out_json> [<map_ref>]
Reads infra/aws/lambda/ci/lambda-source-map.json AT <map_ref> (default HEAD) and writes a map holding ONLY the three functions
irpt-narrative, irpt-performance-adapter and irpt-status (every other key of each entry verbatim) in which EVERY staged_from row whose
repo_path is under infra/aws/lambda/investor-reporting/ or data/assets/scripts/gold/investor_reporting/ is re-pinned to <pin>, its sha256 recomputed from `git show <pin>:<repo_path>`.
No member-by-member choice: a sibling dragged out of step is the S60 / rev 4 / rev 5 failure. Rows OUTSIDE investor-reporting (lib/,
org/standards/, infra/logic/registry/, data/, _vendor, inf-pipeline) keep their pin and are listed under _kept_IB_pr_416. The function's
own source_dir files come from the worktree, which equals <pin> for the investor-reporting tree (the cell edits only its deliverables).
Every re-pin (function, member, old pin, new pin, old/new sha256 prefix) is written under _repins_IB_pr_416. lambda-source-map.json itself
is NOT edited (outside this order's grant): the candidate is what BAU_SOURCE_MAP_OVERRIDE and release-census.py --map read. ASCII only.
"""
import hashlib
import json
import subprocess
import sys

pin, out = sys.argv[1], sys.argv[2]
MAP_REF = sys.argv[3] if len(sys.argv) > 3 else "HEAD"
FULL = subprocess.run(["git", "rev-parse", pin], capture_output=True, check=True).stdout.decode().strip()
FUNCS = ["irpt-narrative", "irpt-performance-adapter", "irpt-status"]
IR = "infra/aws/lambda/investor-reporting/"
IR_PREFIX = (IR, "data/assets/scripts/gold/investor_reporting/")    # the lambda tree and the gold investor_reporting scripts it packages

smap = json.loads(subprocess.run(["git", "show", MAP_REF + ":infra/aws/lambda/ci/lambda-source-map.json"], capture_output=True,
                                 check=True).stdout.decode("utf-8"))
doc = {k: v for k, v in smap.items() if k != "functions"}
doc["_note_IB_pr_416"] = ("CANDIDATE (IRPT_BCKEND IB-pr-416, worker ~278): the three split functions only; every investor-reporting staged row "
                          "re-pinned to the ONE commit %s (source map read at %s). Not the source map; lambda-source-map.json is untouched." % (FULL, MAP_REF))
doc["functions"] = {}
doc["_repins_IB_pr_416"] = {}
doc["_kept_IB_pr_416"] = {}
moved = {}
for fn in FUNCS:
    e = json.loads(json.dumps(smap["functions"][fn]))
    moved[fn] = []
    for s in e["staged_from"]:
        if not s["repo_path"].startswith(IR_PREFIX):
            doc["_kept_IB_pr_416"].setdefault(fn, []).append({"member": s["packaged_as"], "repo_path": s["repo_path"], "pin": s["pin"]})
            continue
        r = subprocess.run(["git", "show", "%s:%s" % (FULL, s["repo_path"])], capture_output=True)
        if r.returncode:
            sys.exit("ERROR: %s is not at %s" % (s["repo_path"], FULL[:10]))
        sha = hashlib.sha256(r.stdout).hexdigest()
        if s["pin"] != FULL or s["sha256"] != sha:
            moved[fn].append(s["packaged_as"])
            doc["_repins_IB_pr_416"].setdefault(fn, []).append(
                {"member": s["packaged_as"], "repo_path": s["repo_path"], "old_pin": s["pin"], "new_pin": FULL,
                 "old_sha256_prefix": s["sha256"][:12], "new_sha256_prefix": sha[:12], "bytes_changed": s["sha256"] != sha})
        s["pin"], s["sha256"] = FULL, sha
    doc["functions"][fn] = e
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(doc, indent=2) + "\n")
for fn in FUNCS:
    print(fn, "re-pinned/changed rows: %d" % len(moved[fn]), moved[fn])
