"""IB126 source-map pin read (worker 0.9.0_WK_IRPT_BCKEND~287, IRPT_BCKEND.TO-IB-pr-428). READ ONLY, LOCAL ONLY (git + files).

For each of the four functions: for every file that builds an answer or its envelope, what does
infra/aws/lambda/ci/lambda-source-map.json say pins it, and is that pinned blob the same bytes as the file at this tree's HEAD?
  STAGED  -> the file is a `staged_from` row: recorded `pin` commit and `sha256`; the pinned blob is read with `git show
             <pin>:<path>` and compared (a) with the recorded sha256 and (b) with HEAD's file.
  NATIVE  -> the file sits in the function's `source_dir` and is packaged from the tree at build time (no per-file pin); the
             function's `last_deployed_commit` is read and the file at that commit is compared with HEAD's file.
For _authz/served.py, when the pinned blob differs from HEAD, the text of `response_envelope` and of the three call sites is
compared between the two blobs, because that is the only part of served.py that builds the envelope.
The map's `last_deployed_commit` is a record, not proof of the deployed bytes (rule 22a): this reads the tree and the map only.

Usage: python ib126_pin_read.py <repo_root>   (writes ib126_source_map_pins.json beside this file)
"""
import ast
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
HERE = os.path.dirname(os.path.abspath(__file__))
IR = "infra/aws/lambda/investor-reporting/"
SM = json.load(open(os.path.join(ROOT, "infra/aws/lambda/ci/lambda-source-map.json"), encoding="utf-8"))["functions"]

FILES = {
    "irpt-directory-search": ["directory/entry.py", "_authz/served.py"],
    "irpt-status": ["ops/owned_requests.py", "ops/entry.py", "reports/status_installed.py", "_authz/served.py"],
    "irpt-ycharts-generate": ["intake/uploads.py", "intake/upload_entry.py", "reports/generate_installed.py",
                              "ycharts/generate/entry.py", "ycharts/generate/comparison_catalogue.py", "_authz/served.py"],
    "irpt-export-render": ["export/custody_read.py", "export/custody_persist.py", "export/entry.py", "_authz/served.py"],
}


def git_show(commit, path):
    out = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (commit, path)], capture_output=True)
    return out.stdout if out.returncode == 0 else None


def sha(b):
    return hashlib.sha256(b).hexdigest()


def func_text(blob, name):
    tree = ast.parse(blob.decode("utf-8"))
    lines = blob.decode("utf-8").splitlines()
    for node in ast.walk(tree):          # module-level functions and Entry's methods alike
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return "\n".join(lines[node.lineno - 1:node.end_lineno])
    return None


def main():
    head = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], capture_output=True).stdout.decode().strip()
    out = {"head": head, "functions": {}}
    for fn, paths in FILES.items():
        rec = SM[fn]
        last = rec["last_deployed_commit"]
        block = {"source_dir": rec["source_dir"], "last_deployed_commit": last, "last_deployed_at": rec["last_deployed_at"],
                 "files": {}}
        staged = rec.get("staged_from", [])
        in_files = {os.path.basename(f) for f in rec["files"]}
        for p in paths:
            full = IR + p
            cur = open(os.path.join(ROOT, full), "rb").read()
            hits = [e for e in staged if e["repo_path"] == full]
            if hits:
                e = hits[0]
                pinned = git_show(e["pin"], full)
                row = {"kind": "STAGED", "packaged_as": e["packaged_as"], "pin": e["pin"],
                       "recorded_sha256_matches_pinned_blob": (pinned is not None and sha(pinned) == e["sha256"]),
                       "pinned_blob_equals_head_file": (pinned is not None and pinned == cur)}
                if pinned is not None and pinned != cur and p.endswith("served.py"):
                    same = {}
                    for name in ("response_envelope", "_handle_owner_read", "_handle_prospect", "handle"):
                        a, b = func_text(pinned, name), func_text(cur, name)
                        same[name] = (a is not None and a == b)
                    row["served_py_functions_identical_between_pin_and_head"] = same
                    row["pin_to_head_diff_lines"] = subprocess.run(
                        ["git", "-C", ROOT, "diff", "--numstat", e["pin"], head, "--", full],
                        capture_output=True).stdout.decode().strip()
            else:
                old = git_show(last, full)
                row = {"kind": "NATIVE", "listed_in_function_files": os.path.basename(p) in in_files,
                       "file_at_last_deployed_commit_equals_head_file": (old is not None and old == cur),
                       "file_exists_at_last_deployed_commit": old is not None}
            block["files"][p] = row
        out["functions"][fn] = block
    with open(os.path.join(HERE, "ib126_source_map_pins.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    for fn, b in out["functions"].items():
        print("==", fn, "last_deployed_commit", b["last_deployed_commit"][:10], b["last_deployed_at"])
        for p, r in b["files"].items():
            print("   %-46s %s" % (p, {k: (v if not isinstance(v, str) or len(v) < 14 else v[:10]) for k, v in r.items()}))


if __name__ == "__main__":
    main()
