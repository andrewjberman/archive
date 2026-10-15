#!/usr/bin/env python
"""OG-ap-20 Phase A, A1's addition: ENUMERATE THE SEAMS THE TAKEN MODULES IMPORT, BEFORE THE CUT.

A1 asks for this because of row Z-S137 one order ago: OG-ap-19's take-list omitted app/typed_scope.py,
a seam an EARLIER cell wrote that the taken modules were later built on, and the release could not
import without it. A take-list enumerates the files THIS release's cells wrote plus the hookup's; a
seam in neither set is invisible to it. This script is the cheap tell the row recommended, run at CUT
time rather than after a suite goes red.

WHAT IT DOES: reads each module the order's take-list names, AT box/sitez HEAD, by AST -- never by
import, because importing needs the gateway's dependencies and would run module-level code. It collects
every intra-package import (`from . import X`, `from .X import ...`, `import app.X`) and reports, for
each name, whether the RELEASE BASE already carries it. A name the base lacks and the take-list omits is
the Z-S137 class, and the point of running this now is that the answer arrives before the cut.

THE TRANSITIVE STEP MATTERS. typed_scope itself imported harvest_read and harvest_typed; had those been
absent too, taking typed_scope alone would have moved the failure one level down rather than fixing it.
So every newly-required seam is itself opened and its imports enumerated, to fixpoint.

Usage: python g5a_seams.py <base_sha> [--json <out>]
"""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys

GW = "infra/aws/ec2/opal-gateway"
# the order's take-list for OG-ap-20 step 4
TAKEN = ["app/etfs_ownership.py", "app/etfs_funds.py", "app/portal_mdpf.py"]
HOOKUP = ["app/tools.py", "app/destructive_ops.py", "app/data_entitlement.py"]


def show(ref: str, path: str):
    p = subprocess.run(["git", "show", "%s:%s/%s" % (ref, GW, path)], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        return None
    return p.stdout.decode("utf-8", "replace")


def resolve(ref: str, name: str):
    """(path, kind) for an intra-package name at `ref`, or (None, None).

    PYTHON RESOLVES A NAME TO A MODULE **OR A PACKAGE**, and checking only app/<name>.py makes this
    guard cry wolf on every package. Measured: the first run of this script reported app/integrations.py
    as a required-but-absent seam for all three taken modules, when `integrations` is the PACKAGE
    app/integrations/ -- present at the base all along. A guard that false-positives on a package is a
    guard that gets ignored, which is worse than not having it.
    """
    mod = "app/%s.py" % name
    if show(ref, mod) is not None:
        return mod, "module"
    pkg = "app/%s/__init__.py" % name
    if show(ref, pkg) is not None:
        return pkg, "package"
    return None, None


def intra_imports(src: str) -> set:
    """Every intra-package module name this source imports."""
    out = set()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                if node.module:
                    out.add(node.module.split(".")[0])
                else:
                    for a in node.names:            # from . import X, Y
                        out.add(a.name)
            elif node.module and node.module.startswith("app."):
                out.add(node.module.split(".")[1])
        elif isinstance(node, ast.Import):
            for a in node.names:
                if a.name.startswith("app."):
                    out.add(a.name.split(".")[1])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    trunk = subprocess.run(["git", "rev-parse", "box/sitez"], capture_output=True).stdout.decode().strip()

    out = {"base_sha": a.base, "trunk_sha": trunk, "take_list": TAKEN + HOOKUP,
           "modules": {}, "seams_required": {}, "missing_from_base_and_takelist": [], "absent_at_trunk": []}

    frontier, seen = list(TAKEN), set()
    while frontier:
        path = frontier.pop(0)
        if path in seen:
            continue
        seen.add(path)
        src = show(trunk, path)
        if src is None:
            out["absent_at_trunk"].append(path)
            continue
        try:
            imps = sorted(intra_imports(src))
        except SyntaxError as exc:
            out["modules"][path] = {"error": "SyntaxError: %s" % exc}
            continue
        rec = {"imports": imps, "per_import": {}}
        for name in imps:
            base_path, base_kind = resolve(a.base, name)
            trunk_path, trunk_kind = resolve(trunk, name)
            dep = trunk_path or base_path or "app/%s.py" % name
            at_base = base_path is not None
            at_trunk = trunk_path is not None
            in_take = dep in (TAKEN + HOOKUP)
            rec["per_import"][name] = {"path": dep, "kind": trunk_kind or base_kind,
                                       "at_base": at_base, "at_trunk": at_trunk,
                                       "in_take_list": in_take}
            if not at_base and not in_take:
                out["seams_required"].setdefault(dep, []).append(path)
                if at_trunk and (trunk_kind == "module"):
                    frontier.append(dep)            # follow a module; a package is a tree, not one file
        out["modules"][path] = rec

    out["missing_from_base_and_takelist"] = sorted(out["seams_required"])
    out["verdict"] = ("CLEAR -- every module the take-list names imports only things the base already carries "
                      "or the take-list includes"
                      if not out["seams_required"] else
                      "SEAM(S) REQUIRED -- %d name(s) the base lacks and the take-list omits: %s"
                      % (len(out["seams_required"]), sorted(out["seams_required"])))
    out["denominator"] = {"modules_opened": len(seen), "take_list_entries": len(TAKEN) + len(HOOKUP),
                          "distinct_intra_imports": len({n for m in out["modules"].values()
                                                         for n in m.get("imports", [])})}
    out["method"] = ("ast over box/sitez HEAD, intra-package imports only (from . import X, from .X import ..., "
                     "import app.X); each newly-required seam is itself opened and followed to fixpoint, because "
                     "taking one seam whose own dependency is also absent only moves the failure down a level")
    if a.json:
        with open(a.json, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(out, indent=1) + "\n")
        print("  WROTE %s" % a.json)
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
