"""Build the Lambda's flat scratch tree from lambda-source-map.json staged_from pins (git show, read-only on the repo).

Usage: python -I build_tree.py <scratch_root> <worktree_root>
Writes <scratch_root>/lambda_flat/<packaged_as> for every staged_from entry, checks each sha256 against the map,
computes the door import closure (roots uploads.py and upload_entry.py) and writes <scratch_root>/tools/tree_manifest.json.
"""
import ast
import hashlib
import json
import os
import subprocess
import sys

SCR, WT = sys.argv[1], sys.argv[2]
FLAT = os.path.join(SCR, "lambda_flat")
mp = json.load(open(os.path.join(WT, "infra/aws/lambda/ci/lambda-source-map.json"), encoding="utf-8"))
fn = mp["functions"]["irpt-ycharts-generate"]
staged = fn["staged_from"]
by_packaged = {m["packaged_as"]: m for m in staged}
problems, members = [], {}
for m in staged:
    got = subprocess.run(["git", "-C", WT, "show", m["pin"] + ":" + m["repo_path"]], capture_output=True)
    if got.returncode != 0 or not got.stdout:
        problems.append("git show failed %s:%s rc=%s" % (m["pin"], m["repo_path"], got.returncode))
        continue
    sha = hashlib.sha256(got.stdout).hexdigest()
    dest = os.path.join(FLAT, m["packaged_as"])
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "wb").write(got.stdout)
    members[m["packaged_as"]] = {"repo_path": m["repo_path"], "pin": m["pin"], "sha256": sha,
                                 "map_sha256": m["sha256"], "sha_matches_map": sha == m["sha256"]}
    if sha != m["sha256"]:
        problems.append("sha mismatch %s" % m["packaged_as"])

flat_mods = {p[:-3]: p for p in members if p.endswith(".py") and "/" not in p}


def imports(path):
    tree = ast.parse(open(path, encoding="utf-8", errors="replace").read())
    top = set(id(n) for n in tree.body)
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            mods = [node.module]
        else:
            continue
        for mod in mods:
            found.append((mod.split(".")[0], node.lineno, id(node) in top))
    return found


def walk_closure(roots, flat_names, staged_members, flat_dir):
    """Import closure of the roots over the staged flat names; a name not staged is simply not followed here
    (door_unstaged.py is the check that lists the non-stdlib, non-staged imports of the closure)."""
    closure = {}
    queue = list(roots)
    while queue:
        name_file = queue.pop()
        if name_file in closure:
            continue
        closure[name_file] = staged_members[name_file]
        for mod, _line, _top in imports(os.path.join(flat_dir, name_file)):
            if mod in flat_names:
                queue.append(flat_names[mod])
    return closure


ROOTS = ["uploads.py", "upload_entry.py"]
closure = walk_closure(ROOTS, flat_mods, members, FLAT)
manifest = {"scratch_flat": FLAT, "staged_members": len(members), "problems": problems,
            "door_roots": ROOTS, "door_closure": sorted(closure), "door_closure_pins": {k: v["pin"] for k, v in closure.items()},
            "members": members}
open(os.path.join(SCR, "tools", "tree_manifest.json"), "w", encoding="utf-8").write(json.dumps(manifest, indent=1, sort_keys=True))
print("staged written %d; sha matches map %d; problems %d" % (len(members), sum(1 for v in members.values() if v["sha_matches_map"]), len(problems)))
print("door closure %d members: %s" % (len(closure), ", ".join(sorted(closure))))
