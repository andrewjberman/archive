#!/usr/bin/env python3
"""E4-AC2 instrument -- do comp-debt's STITCH refusals name the decision?

An ast read, not a text grep: it finds every `raise SystemExit(...)` in the
file, collects every string Constant inside the raised expression (the texts
are `"..." % args` BinOps and implicit concatenations, so a naive `.args[0]`
read would see only the first fragment), and grades the two that live inside
`_stitch_freshness` -- the absent-store refusal and the stale-store refusal.

WHY THE SCOPE IS THE FUNCTION AND NOT THE FILE: comp_debt.py raises a THIRD
SystemExit, the served-graph refusal in `freshness_assert`, which is the NESSIE
surface's and has nothing to do with the stitch home. It is printed as
OUT-OF-SCOPE-BY-NAME rather than silently dropped, so the 2-of-2 denominator is
visible as a choice.

usage: _refusal_ast.py <py> --home <TOKEN> [--cell CG-s-20] [--scope FUNC]
                       [--label L]
exit 0 always; the caller grades the printed lines.
"""
from __future__ import annotations

import ast
import sys


def _strings(node: ast.AST):
    out = []
    for sub in ast.walk(node):
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
            out.append(sub.value)
    return out


def main() -> int:
    args = sys.argv[1:]
    opts = {"--home": None, "--cell": "CG-s-20", "--scope": "_stitch_freshness",
            "--label": "REAL"}
    path = args[0]
    i = 1
    while i < len(args):
        if args[i] in opts:
            opts[args[i]] = args[i + 1]
            i += 2
        else:
            i += 1
    home = opts["--home"]
    cell = opts["--cell"]
    scope = opts["--scope"]
    print("--- REFUSAL READ [%s] %s ---" % (opts["--label"], path))
    print("SCOPE_FUNCTION=%s   HOME_TOKEN=%s   CELL_TOKEN=%s" % (scope, home, cell))
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except (OSError, SyntaxError) as ex:
        print("  UNREADABLE: %s" % ex)
        print("REFUSAL_TEXTS_NAME_HOME=0 of 0")
        return 0

    in_scope, out_scope = [], []
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for node in ast.walk(fn):
            if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) \
                    and getattr(node.exc.func, "id", "") == "SystemExit":
                text = " ".join(_strings(node.exc))
                (in_scope if fn.name == scope else out_scope).append(
                    (fn.name, node.lineno, text))

    for fn, line, text in out_scope:
        print("  OUT-OF-SCOPE-BY-NAME  %s():%d  %s..." % (fn, line, text[:70]))
    ok = 0
    for fn, line, text in in_scope:
        has_home = home in text
        has_cell = cell in text
        verdict = "NAMES-HOME" if (has_home and has_cell) else "DOES-NOT-NAME"
        if has_home and has_cell:
            ok += 1
        print("  %s  %s():%d  home=%s cell=%s  len=%d"
              % (verdict, fn, line, has_home, has_cell, len(text)))
        print("      %s" % text[:200].replace("\n", " "))
    print("REFUSAL_SITES_IN_SCOPE=%d" % len(in_scope))
    print("REFUSAL_TEXTS_NAME_HOME=%d of %d" % (ok, len(in_scope)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
