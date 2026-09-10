#!/usr/bin/env python3
"""TO-CG-F-7 / CG-s-27 -- the SUBSTITUTE control for a dead one.

F7-AC4 is specified as "the control that can fail: the writer's new REQUIRED kwargs would
break a caller that was not updated". MEASURED, IT CANNOT: with the CG-s-27 kwargs stripped
back out of kuzu_incremental_refresh.py the AC4 invocation still reads `10 passed`, because
`test_kuzu_incremental_refresh.py` collects ZERO under pytest (it is a `main()`-style
self-test guarded by `if __name__ == "__main__"`, with no pytest-shaped test functions) and
all 10 collected tests come from `test_projection_worker.py`, which never calls the writer.
Filed as NFRA_CLDGRPH-W3-S16.

This is the discriminating instrument that does NOT need one: statically BIND every producer
call site's argument NAMES against `inspect.signature(_provenance.write_manifest)`. A caller
left behind fails the bind with the same TypeError the interpreter would raise at run time --
and no engine is opened, no store is created, no loader is run (this order's BOUNDS).

Run: python org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/f7_signature_bind.py
"""
from __future__ import annotations

import ast
import inspect
import os
import sys

ROOT = os.path.join("infra", "aws", "globgrph")
EXCLUDED = ("kuzu_load.py",)
SENTINEL = object()

sys.path.insert(0, os.path.join(os.getcwd(), ROOT))
import _provenance  # noqa: E402

SIG = inspect.signature(_provenance.write_manifest)


def call_sites(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            if not name.endswith(".py") or name in EXCLUDED:
                continue
            if os.path.basename(dirpath) == "tests" or name == "_provenance.py":
                continue
            p = os.path.join(dirpath, name)
            with open(p, encoding="utf-8") as fh:
                tree = ast.parse(fh.read(), filename=p)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and (
                        (isinstance(node.func, ast.Name) and node.func.id == "write_manifest")
                        or (isinstance(node.func, ast.Attribute)
                            and node.func.attr == "write_manifest")):
                    kws = [kw.arg for kw in node.keywords if kw.arg]
                    yield p.replace("\\", "/"), node.lineno, len(node.args), kws


def try_bind(n_pos, kwnames):
    try:
        SIG.bind(*([SENTINEL] * n_pos), **{k: SENTINEL for k in kwnames})
        return True, ""
    except TypeError as ex:
        return False, str(ex)


def main():
    print("=== CG-s-27 signature bind: every producer call site against the ONE writer ===")
    print("SIGNATURE: write_manifest%s" % (SIG,))
    print("")
    sites = list(call_sites(ROOT))
    ok = 0
    for path, line, n_pos, kws in sites:
        good, err = try_bind(n_pos, kws)
        print("  %-50s :%-5d %s" % (path, line, "BINDS" if good else "REFUSED: " + err))
        ok += 1 if good else 0
    print("")
    # THE CONTROL: the same bind with the CG-s-27 kwargs removed must be REFUSED at every
    # site. A bind that accepts a stripped caller is not measuring the requirement.
    stripped_refused = 0
    for path, line, n_pos, kws in sites:
        rest = [k for k in kws if k not in ("edge_count_semantics", "artifact_claim")]
        good, err = try_bind(n_pos, rest)
        print("  CONTROL %-42s :%-5d %s" % (path, line,
              "REFUSED (as it must): " + err if not good else "ACCEPTED -- DEAD CONTROL"))
        stripped_refused += 0 if good else 1
    print("")
    print("SITES_BINDING=%d of %d" % (ok, len(sites)))
    print("STRIPPED_CALLER_REFUSED=%d of %d" % (stripped_refused, len(sites)))
    print("BIND_CONTROL=%s" % ("FIRED" if (stripped_refused == len(sites) and sites) else "DEAD"))
    return 0 if (ok == len(sites) and stripped_refused == len(sites) and sites) else 1


if __name__ == "__main__":
    sys.exit(main())
