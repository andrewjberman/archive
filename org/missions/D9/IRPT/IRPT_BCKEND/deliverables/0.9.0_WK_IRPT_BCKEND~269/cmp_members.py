"""IB-pr-406: member-by-member sha256 comparison of two extracted bundle trees.
Usage: python -I cmp_members.py <base_tree> <built_tree>   -> JSON: counts, members only in one side, changed members and their built sha256.
"""
import hashlib
import json
import os
import sys


def walk(root):
    out = {}
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            path = os.path.join(dirpath, name)
            with open(path, "rb") as fh:
                out[os.path.relpath(path, root).replace(os.sep, "/")] = hashlib.sha256(fh.read()).hexdigest()
    return out


def main():
    base, built = walk(sys.argv[1]), walk(sys.argv[2])
    changed = sorted(k for k in base.keys() & built.keys() if base[k] != built[k])
    print(json.dumps({"base_n": len(base), "built_n": len(built), "only_base": sorted(base.keys() - built.keys()),
                      "only_built": sorted(built.keys() - base.keys()), "changed": changed,
                      "built_sha": {k: built[k] for k in changed}}, indent=1))


if __name__ == "__main__":
    main()
