#!/usr/bin/env python3
"""F5-AC3's AST census: does anything on comp-debt's REACHABILITY path OPEN a local Kuzu store?

An AST walk, not a text scan, because a text scan cannot tell a live call from the docstring that
RECORDS its retirement -- and this file's whole point is that the retirement is documented in prose
that still contains the words. The walk looks for three shapes:

    import kuzu / from kuzu import ...          an import of the engine at all
    kuzu.Database(...) / kuzu.Connection(...)   an open, however it is spelled
    <anything>(..., read_only=True)             the open's signature, for a re-aliased import

THE POPULATION IS DECLARED: comp_debt.py plus projection_client.py -- the two files the REACHABILITY
leg executes. canon_motif_scorer is deliberately NOT in it: that is a different family and it uses
the kuzu LIBRARY legitimately, so including it would make this census fail for a reason that has
nothing to do with this cell.

A PLANTED file is walked by the SAME function on every run: if the walker cannot find an open in a
file written to contain one, its 0 over the real files means nothing.
"""
import argparse
import ast
import io
import json
import os
import sys

PLANT = '''"""A planted probe -- not part of the tool. It exists so a 0 above means something."""
import kuzu

STITCH_DB = "kuzu_stitch_db"


def open_it(path):
    return kuzu.Connection(kuzu.Database(path, read_only=True))
'''


def opens_in(path: str) -> list:
    """Every local-store OPEN or kuzu import in one file, as (line, shape)."""
    try:
        tree = ast.parse(io.open(path, encoding="utf-8", errors="replace").read(), filename=path)
    except SyntaxError as exc:
        return [(getattr(exc, "lineno", 0), "UNPARSEABLE: %s" % exc)]
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name == "kuzu" or a.name.startswith("kuzu."):
                    hits.append((node.lineno, "import %s" % a.name))
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] == "kuzu":
                hits.append((node.lineno, "from %s import ..." % node.module))
        elif isinstance(node, ast.Call):
            f = node.func
            name = ""
            if isinstance(f, ast.Attribute):
                name = "%s.%s" % (getattr(f.value, "id", "?"), f.attr)
            elif isinstance(f, ast.Name):
                name = f.id
            if name in ("kuzu.Database", "kuzu.Connection"):
                hits.append((node.lineno, "%s(...)" % name))
            elif any(k.arg == "read_only" for k in node.keywords or []):
                hits.append((node.lineno, "%s(..., read_only=...)" % (name or "<call>")))
    return sorted(hits)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", nargs="+", required=True)
    ap.add_argument("--plant-dir", required=True)
    a = ap.parse_args()

    per_file = {}
    for p in a.files:
        per_file[p] = opens_in(p)
    dirty = {p: h for p, h in per_file.items() if h}

    os.makedirs(a.plant_dir, exist_ok=True)
    planted = os.path.join(a.plant_dir, "f5_planted_open_probe.py")
    io.open(planted, "w", encoding="utf-8", newline="\n").write(PLANT)
    plant_hits = opens_in(planted)

    out = {
        "files_walked": len(per_file),
        "files_with_a_local_open": len(dirty),
        "per_file": {p: [{"line": ln, "shape": sh} for ln, sh in h] for p, h in per_file.items()},
        "control_planted_file": planted,
        "control_hits": [{"line": ln, "shape": sh} for ln, sh in plant_hits],
        "control_fired": bool(plant_hits),
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
