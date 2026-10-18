# -*- coding: utf-8 -*-
"""HVST-cm-3 read-only spot check of the writer basis.

For each WRITER line of cm3_writers.out, read the enclosing function of the cited line from the SHARED checkout
(C:/Dev/ajb_workspace, read only) and report whether that function calls slash_safe_key (by name or attribute).
Usage: python -B cm3_basis_check.py <path to cm3_writers.out>
"""
import ast
import re
import sys

SHARED = "C:/Dev/ajb_workspace"
WRITER_RE = re.compile(r"^WRITER (\S+) (\S+):(\d+) (\S+) spelling=(\S+)")


def writer_lines(path):
    with open(path, encoding="utf-8", newline="") as fh:
        for ln in fh.read().split("\n"):
            m = WRITER_RE.match(ln)
            if m:
                yield m.group(1), m.group(2), int(m.group(3)), m.group(4), m.group(5)


def enclosing(tree, fn, line):
    node = None
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == fn and n.lineno <= line <= n.end_lineno:
            node = n
    return node


def slash_calls(node):
    lines = []
    for c in ast.walk(node):
        if isinstance(c, ast.Call):
            f = c.func
            name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else "")
            if name.endswith("slash_safe_key"):
                lines.append(c.lineno)
    return sorted(set(lines))


def main():
    for prefix, rel, line, fn, spelling in writer_lines(sys.argv[1]):
        if not rel.endswith(".py"):
            print("NONPY %s %s:%d %s spelling=%s" % (prefix, rel, line, fn, spelling))
            continue
        with open(SHARED + "/" + rel, encoding="utf-8", errors="replace") as fh:
            tree = ast.parse(fh.read())
        node = enclosing(tree, fn, line)
        span = (node.lineno, node.end_lineno) if node is not None else None
        calls = slash_calls(node) if node is not None else []
        hit = ("slash_safe_key@" + ",".join(str(x) for x in calls)) if calls else "NO-slash_safe_key-call"
        print("%s %s %s:%d %s fn_span=%s %s" % (spelling, prefix, rel, line, fn, span, hit))


if __name__ == "__main__":
    main()
