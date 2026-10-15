"""IB-pr-597 candidate source map writer (method from deliverables/0.9.0_WK_IRPT_BCKEND~312/make_candidate_map.py and
the IB-pr-585 writer in deliverables/0.9.0_WK_IRPT_BCKEND~427/make_candidate_map_perf.py; ASCII). From the worktree root:
    python make_candidate_map_perf.py <base_commit> <out_map_json> <out_repins_json> [<map_ref>]
Reads infra/aws/lambda/ci/lambda-source-map.json AT <map_ref> (default HEAD) and writes the SAME map (every function, every key
verbatim) except that, in function irpt-holdings-performance-lambda ONLY, the staged_from rows whose repo_path is one of the two
split-adjust members (holdings_performance.py, sources.json) are re-pinned to <base_commit> with sha256 recomputed from
`git show <base_commit>:<repo_path>`. lambda-source-map.json is NOT edited."""
import hashlib
import json
import subprocess
import sys

base, out_map, out_repins = sys.argv[1], sys.argv[2], sys.argv[3]
REF = sys.argv[4] if len(sys.argv) > 4 else "HEAD"
FN = "irpt-holdings-performance-lambda"
MEMBERS = {
    "data/assets/scripts/gold/irpt_holdings_performance/holdings_performance.py",
    "data/assets/scripts/gold/irpt_holdings_performance/sources.json",
}
FULL = subprocess.run(["git", "rev-parse", "--verify", base + "^{commit}"],
                      capture_output=True, check=True).stdout.decode().strip()
raw = subprocess.run(["git", "show", REF + ":infra/aws/lambda/ci/lambda-source-map.json"],
                     capture_output=True, check=True).stdout.decode("utf-8")
smap = json.loads(raw)
repins = []
for s in smap["functions"][FN].get("staged_from") or []:
    if s["repo_path"] not in MEMBERS:
        continue
    r = subprocess.run(["git", "show", "%s:%s" % (FULL, s["repo_path"])], capture_output=True)
    if r.returncode:
        sys.exit("ERROR: %s is not at %s" % (s["repo_path"], FULL[:10]))
    sha = hashlib.sha256(r.stdout).hexdigest()
    repins.append({"function": FN, "packaged_as": s["packaged_as"], "repo_path": s["repo_path"],
                   "old_pin": s["pin"], "new_pin": FULL,
                   "old_sha256_prefix": s["sha256"][:12], "new_sha256_prefix": sha[:12],
                   "bytes_changed": s["sha256"] != sha})
    s["pin"], s["sha256"] = FULL, sha
with open(out_map, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(smap, indent=2) + "\n")
with open(out_repins, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps({"base_commit": FULL, "map_ref": REF, "rows_repinned": len(repins),
                        "repins": repins}, indent=1) + "\n")
print("rows re-pinned: %d" % len(repins))
for x in repins:
    print(x["function"], x["packaged_as"].rsplit("/", 1)[-1], x["old_pin"][:10], "->", FULL[:10],
          "bytes_changed=%s" % x["bytes_changed"])
