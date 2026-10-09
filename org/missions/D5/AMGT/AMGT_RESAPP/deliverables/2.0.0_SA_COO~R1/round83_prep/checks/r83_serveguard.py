"""AMGT_RESAPP round-83 PREP -- the serve-path guard for the passage-map repair (AMGT-hh-1).

  python r83_serveguard.py [--base <commit>]

`lib/research/api/scoped_amgt.py` (the live opal-amgt-scoped-api function) imports
`lib.research.filings.passages.clean_location`, and `drafting_build.py` / `ceo_search.py` import `Locator` and
`cjk_share`. The round-83 repair moves `build_passage_map` only. This check compares, by AST, every top-level
definition of `passages.py` that a module OTHER than analyze/translate/document imports, between the base commit and the
working tree:
    G1 clean_location, Locator, cjk_share are each present and byte-identical (ast.dump) to the base.
Verdict: R83 SERVEGUARD: YES|NO (exit 0|1). At the base it reads YES (nothing moved).
"""
from __future__ import annotations

import argparse
import ast
import subprocess
import sys

PATH = "lib/research/filings/passages.py"
GUARDED = ("clean_location", "Locator", "cjk_share")
BASE = "051e5b9200"


def defs(src):
    out = {}
    for node in ast.parse(src).body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            out[node.name] = ast.dump(node, include_attributes=False)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=BASE)
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    base_src = subprocess.run(["git", "-C", root, "show", "%s:%s" % (a.base, PATH)], capture_output=True, text=True,
                              encoding="utf-8")
    if base_src.returncode != 0 or not base_src.stdout:
        print("FAIL G0 the base copy of %s at %s did not read: %s" % (PATH, a.base, base_src.stderr.strip()))
        print("R83 SERVEGUARD: NO")
        return 1
    with open("%s/%s" % (root, PATH), encoding="utf-8") as fh:
        now_src = fh.read()
    old, new = defs(base_src.stdout), defs(now_src)
    good = 0
    for name in GUARDED:
        if name not in old:
            print("FAIL G1 %s is not defined at the base %s (the guard list is wrong)" % (name, a.base))
            continue
        same = new.get(name) == old[name]
        print("%s G1 %s %s" % ("PASS" if same else "FAIL", name,
                               "unchanged from %s" % a.base if same else "CHANGED or missing (a serve-path move)"))
        good += same
    moved = sorted(n for n in set(old) | set(new) if old.get(n) != new.get(n))
    print("   definitions moved since %s: %d %s" % (a.base, len(moved), moved))
    ok = good == len(GUARDED)
    print("R83 SERVEGUARD: %s %d of %d" % ("YES" if ok else "NO", good, len(GUARDED)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
