"""IB-pr-416 candidate source map writer. From the worktree root:
    python <this file> <pin> <out_json> [<extra_json>]
<extra_json> is an optional JSON object {"<function>": ["<packaged_as>", ...]} of NON-shared staged rows to re-pin to <pin> as well
(the ones the signature closure proved must move with a shared one).
Reads infra/aws/lambda/ci/lambda-source-map.json AT HEAD and writes a map holding ONLY the three functions irpt-narrative,
irpt-performance-adapter and irpt-status (every other key of each entry verbatim) in which each staged_from row that names a SHARED
authorization module -- a path under investor-reporting/_authz, _scope, _ids, _keys, _render_identity, or data/firm_registry.json -- is
re-pinned to <pin> with its sha256 recomputed from `git show <pin>:<repo_path>`. <pin> is served.py's own staged pin (74a62fb46c), so the
tree is the one in which the packaged served.py is consistent: the S60 split is a PIN LAG (the callee rows lag the served.py row). Every
re-pin (function, member, old pin, new pin, old/new sha256 prefix) is written under the key _repins_IB_pr_416. Rows for function-local members (performance/, reports/, ycharts/, ops/, intake/, directory/), lib/, org/standards and
infra/logic/registry keep their pin and sha256. The lambda-source-map.json itself is NOT edited (outside this order's grant); the
candidate is what BAU_SOURCE_MAP_OVERRIDE and release-census.py --map read. ASCII only.
"""
import hashlib
import json
import subprocess
import sys

pin, out = sys.argv[1], sys.argv[2]
EXTRA = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
FULL = subprocess.run(["git", "rev-parse", pin], capture_output=True, check=True).stdout.decode().strip()
FUNCS = ["irpt-narrative", "irpt-performance-adapter", "irpt-status"]
IR = "infra/aws/lambda/investor-reporting/"
SHARED = tuple(IR + d + "/" for d in ("_authz", "_scope", "_ids", "_keys", "_render_identity")) + ("data/firm_registry.json",)

smap = json.loads(subprocess.run(["git", "show", "HEAD:infra/aws/lambda/ci/lambda-source-map.json"], capture_output=True,
                                 check=True).stdout.decode("utf-8"))
doc = {k: v for k, v in smap.items() if k != "functions"}
doc["_note_IB_pr_416"] = ("CANDIDATE (IRPT_BCKEND IB-pr-416, worker ~278): the three split functions only; shared authorization staged rows "
                          "re-pinned to %s (plus extra rows %s), served.py included (its row is already at that pin). Not the source map; lambda-source-map.json is untouched." % (FULL, json.dumps(EXTRA, sort_keys=True)))
doc["functions"] = {}
doc["_repins_IB_pr_416"] = {}
moved = {}
for fn in FUNCS:
    e = json.loads(json.dumps(smap["functions"][fn]))
    moved[fn] = []
    for s in e["staged_from"]:
        if not (s["repo_path"].startswith(SHARED) or s["packaged_as"] in EXTRA.get(fn, [])):
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
