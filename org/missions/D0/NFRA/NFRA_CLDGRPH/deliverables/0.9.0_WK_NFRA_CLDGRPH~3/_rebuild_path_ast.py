"""E4-AC4 instrument -- is there a local rebuild path to the PROJECTION?

An ast walk over the given files for CODE-band occurrences of the four tokens
that would BE such a path:

    kuzu_nessie_load    the canonical loader module
    ensure_fresh        the marker-oracle rebuild entrypoint
    CANONICAL_DB_PATH   the canonical store's path constant
    kuzu_nessie_db      the canonical store itself

CODE means: an import name, a Name id, an Attribute attr, a called function's
name, or a non-docstring string constant. It does NOT mean a comment (comments
are not in the ast at any point) or a docstring (excluded explicitly, and both
excluded classes are PRINTED so the zero is not hiding them).

DENOMINATOR: ast nodes walked, printed per file. A file that fails to parse is
printed as a PARSE FAILURE and never folded into the zero.

usage: _rebuild_path_ast.py <py> [<py> ...] [--label L]
exit 0 always; the caller grades the printed lines.
"""
from __future__ import annotations

import ast
import re
import sys

TOKENS = ("kuzu_nessie_load", "ensure_fresh", "CANONICAL_DB_PATH", "kuzu_nessie_db")
TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_])(%s)(?![A-Za-z0-9_])" % "|".join(TOKENS))
COMMENT_RE = re.compile(r"#.*$")


def _docstring_ids(tree: ast.AST) -> set:
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                             ast.AsyncFunctionDef)):
            body = getattr(node, "body", None)
            if body and isinstance(body[0], ast.Expr):
                v = body[0].value
                if isinstance(v, ast.Constant) and isinstance(v.value, str):
                    out.add(id(v))
    return out


def walk(path: str):
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    docs = _docstring_ids(tree)
    hits, doc_hits = [], []
    n_nodes = 0
    for node in ast.walk(tree):
        n_nodes += 1
        line = getattr(node, "lineno", 0)
        if isinstance(node, ast.Import):
            for a in node.names:
                if TOKEN_RE.search(a.name):
                    hits.append((line, "IMPORT", a.name))
        elif isinstance(node, ast.ImportFrom):
            if node.module and TOKEN_RE.search(node.module):
                hits.append((line, "IMPORT-FROM", node.module))
            for a in node.names:
                if TOKEN_RE.search(a.name):
                    hits.append((line, "IMPORT-FROM-NAME", a.name))
        elif isinstance(node, ast.Name):
            if TOKEN_RE.search(node.id):
                hits.append((line, "NAME", node.id))
        elif isinstance(node, ast.Attribute):
            if TOKEN_RE.search(node.attr):
                hits.append((line, "ATTRIBUTE", node.attr))
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if TOKEN_RE.search(node.value):
                where = doc_hits if id(node) in docs else hits
                where.append((line, "DOCSTRING" if id(node) in docs else "STRING",
                              node.value.strip().replace("\n", " ")[:90]))
    comment_hits = []
    for i, ln in enumerate(src.splitlines(), 1):
        m = COMMENT_RE.search(ln)
        if m and TOKEN_RE.search(m.group(0)):
            comment_hits.append((i, "COMMENT", m.group(0).strip()[:90]))
    return n_nodes, hits, doc_hits, comment_hits


def main() -> int:
    args = sys.argv[1:]
    label = "REAL"
    if "--label" in args:
        i = args.index("--label")
        label = args[i + 1]
        args = args[:i] + args[i + 2:]
    print("--- REBUILD-PATH WALK [%s] ---" % label)
    print("TOKENS (4): %s" % ", ".join(TOKENS))
    total_nodes, total_hits, failures = 0, [], []
    for p in args:
        try:
            n, hits, docs, comments = walk(p)
        except (OSError, SyntaxError) as ex:
            failures.append((p, str(ex)))
            continue
        total_nodes += n
        print("  FILE %s  ast_nodes=%d" % (p, n))
        for line, kind, txt in hits:
            print("    REBUILD-PATH %s:%d [%s] %s" % (p, line, kind, txt))
            total_hits.append((p, line, kind, txt))
        for line, kind, txt in docs:
            print("    DOCSTRING (excluded, printed) %s:%d %s" % (p, line, txt))
        for line, kind, txt in comments:
            print("    COMMENT (never in the ast, printed) %s:%d %s" % (p, line, txt))
    for p, ex in failures:
        print("  PARSE FAILURE %s: %s" % (p, ex))
    print("PARSE_FAILURES=%d" % len(failures))
    print("PROJECTION_REBUILD_PATHS=%d of %d" % (len(total_hits), total_nodes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
