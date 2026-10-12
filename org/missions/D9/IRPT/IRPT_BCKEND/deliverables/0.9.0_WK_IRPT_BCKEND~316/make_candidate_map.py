"""IB-pr-460 candidate source map writer (from IB-pr-456's; ASCII). From the worktree root:
    python <this file> <pin> <out_map_json> <out_repins_json> [<map_ref>]
Reads infra/aws/lambda/ci/lambda-source-map.json AT <map_ref> (default <pin>) and writes the SAME map (every function, every key verbatim)
except that, in every function, ONLY the staged_from rows whose repo_path is commentary_draft_store.py are re-pinned to <pin> with sha256
recomputed from `git show <pin>:<repo_path>`. In the real map NO row pins commentary_draft_store.py: it is a NATIVE member of the
function's source_dir (reports/), which the builder reads from the worktree, i.e. from <pin>. So the expected result is 0 rows re-pinned
and a candidate map byte-equal to the real map's serialization at <map_ref>; the output states both facts. lambda-source-map.json is NOT
edited. <out_repins_json> is the small committed diff (here: empty, with the evidence that the member is native)."""
import hashlib
import json
import subprocess
import sys

pin, out_map, out_repins = sys.argv[1], sys.argv[2], sys.argv[3]
REF = sys.argv[4] if len(sys.argv) > 4 else pin
FULL = subprocess.run(["git", "rev-parse", pin], capture_output=True, check=True).stdout.decode().strip()
STORE = "infra/aws/lambda/investor-reporting/reports/commentary_draft_store.py"
FN = "irpt-commentary-draft-store-lambda"
raw = subprocess.run(["git", "show", REF + ":infra/aws/lambda/ci/lambda-source-map.json"], capture_output=True, check=True).stdout.decode("utf-8")
smap = json.loads(raw)
repins = []
for fn, e in smap["functions"].items():
    for s in e.get("staged_from") or []:
        if s["repo_path"] != STORE:
            continue
        r = subprocess.run(["git", "show", "%s:%s" % (FULL, s["repo_path"])], capture_output=True)
        if r.returncode:
            sys.exit("ERROR: %s is not at %s" % (s["repo_path"], FULL[:10]))
        sha = hashlib.sha256(r.stdout).hexdigest()
        repins.append({"function": fn, "packaged_as": s["packaged_as"], "repo_path": s["repo_path"], "old_pin": s["pin"], "new_pin": FULL,
                       "old_sha256_prefix": s["sha256"][:12], "new_sha256_prefix": sha[:12], "bytes_changed": s["sha256"] != sha})
        s["pin"], s["sha256"] = FULL, sha
e = smap["functions"][FN]
native = {"function": FN, "store_in_files": "commentary_draft_store.py" in e["files"],
          "store_in_staged_from": any(s["repo_path"] == STORE or s["packaged_as"] == "commentary_draft_store.py" for s in e.get("staged_from") or []),
          "source_dir": e["source_dir"], "read_from": "the worktree at the pin (native member of source_dir)"}
text = json.dumps(smap, indent=2) + "\n"
with open(out_map, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
with open(out_repins, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps({"pin": FULL, "map_ref": REF, "rows_repinned": len(repins), "repins": repins, "store_member": native,
                        "candidate_map_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}, indent=1) + "\n")
print("rows re-pinned: %d" % len(repins))
print("native member of source_dir: %s" % json.dumps(native))
