#!/usr/bin/env python3
"""E3-AC2 instrument -- the reader walk over a SCOPE of .py files.

WHAT IT ANSWERS: does any CODE in the scope name `kuzu_db` or `kuzu_ac7` as a
PATH or as the argument of an open, i.e. is anything still able to READ the
residual local stores. It is an ast walk, not a text grep, so:

  - a COMMENT can never be a hit (comments are not in the ast at all);
  - a DOCSTRING is excluded EXPLICITLY (module/class/function head Constant);
  - a PROSE string constant that merely mentions the token (a help text, a tool
    description) is counted and PRINTED under PROSE_MENTIONS, never as a reader
    -- dropping it silently would be the same defect this project keeps finding;
  - the BUILDER is excluded BY NAME, printed, never inferred.

TOKEN BOUNDARY: `(?<![A-Za-z0-9_])(kuzu_db|kuzu_ac7)(?![A-Za-z0-9_])`. The left
boundary is load-bearing: `scratch_kuzu_db` (org/modules/graph/tsgraph_spike)
is a DIFFERENT artifact and a `kuzu_db\\b` regex matches inside it. The loose
count is reported beside the strict one as NEAR_MISS so the exclusion is visible.

Exit code is 0 whatever it finds; the caller grades the printed lines.
"""
from __future__ import annotations

import ast
import os
import re
import sys

TOKEN_STRICT = re.compile(r"(?<![A-Za-z0-9_])(kuzu_db|kuzu_ac7)(?![A-Za-z0-9_])")
TOKEN_LOOSE = re.compile(r"(kuzu_db|kuzu_ac7)")
# loose-but-NOT-strict: a token GLUED to a longer identifier, i.e. a DIFFERENT
# artifact (scratch_kuzu_db). Named per file so the boundary's exclusions are
# auditable from the criterion's own output rather than from prose beside it.
TOKEN_GLUED = re.compile(r"[A-Za-z0-9_](kuzu_db|kuzu_ac7)|(kuzu_db|kuzu_ac7)[A-Za-z0-9_]")
OPEN_FUNCS = {"open", "Database", "connect", "join", "Path", "read_text",
              "read_bytes", "rmtree", "remove", "exists", "isdir", "isfile",
              "stat", "getsize", "getmtime", "listdir", "scandir"}
PATH_ATTR = re.compile(r"(?i)(_?DB(_PATH)?|_PATH|_DIR|_FILE)$")


def _docstring_nodes(tree: ast.AST) -> set:
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


def _call_name(node: ast.Call) -> str:
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return ""


def _path_shaped(s: str) -> bool:
    """A PATH is a token with no whitespace whose segments include the token."""
    if not s or len(s) > 300 or any(c.isspace() for c in s):
        return False
    segs = re.split(r"[/\\]", s)
    for seg in segs:
        if TOKEN_STRICT.search(seg) and len(seg) <= 40:
            return True
    return False


def walk_file(path: str):
    """Returns (readers, prose, docstring_hits, builder_hits_unused, loose_hits, parse_ok)."""
    try:
        src = open(path, encoding="utf-8", errors="replace").read()
    except OSError as ex:
        return None, "READ-FAILED: %r" % (ex,)
    loose = len(TOKEN_LOOSE.findall(src))
    glued = len(TOKEN_GLUED.findall(src))
    try:
        tree = ast.parse(src)
    except SyntaxError as ex:
        return None, "PARSE-FAILED: %s" % (ex,)
    docs = _docstring_nodes(tree)
    readers, prose, docstrings = [], [], []
    # parent map: which Call (if any) an expression sits directly inside, and
    # which assignment target name it is bound to.
    parent_call = {}
    parent_assign = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            for arg in list(node.args) + [kw.value for kw in node.keywords]:
                parent_call[id(arg)] = _call_name(node)
                for sub in ast.walk(arg):
                    parent_call.setdefault(id(sub), _call_name(node))
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            names = [t.id for t in targets if isinstance(t, ast.Name)]
            if names and node.value is not None:
                for sub in ast.walk(node.value):
                    parent_assign.setdefault(id(sub), names[0])
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        if not TOKEN_STRICT.search(node.value):
            continue
        line = getattr(node, "lineno", 0)
        excerpt = node.value.strip().replace("\n", " ")[:110]
        if id(node) in docs:
            docstrings.append((line, excerpt))
            continue
        call = parent_call.get(id(node), "")
        assign = parent_assign.get(id(node), "")
        why = []
        if _path_shaped(node.value):
            why.append("PATH-SHAPED")
        if call in OPEN_FUNCS:
            why.append("ARG-OF:%s" % call)
        if assign and PATH_ATTR.search(assign):
            why.append("BOUND-TO:%s" % assign)
        if why:
            readers.append((line, "+".join(why), excerpt))
        else:
            prose.append((line, excerpt))
    return (readers, prose, docstrings, loose, glued), None


def main() -> int:
    args = sys.argv[1:]
    label = "SCOPE"
    if "--label" in args:
        i = args.index("--label")
        label = args[i + 1]
        args = args[:i] + args[i + 2:]
    builders = []
    if "--builder" in args:
        while "--builder" in args:
            i = args.index("--builder")
            builders.append(args[i + 1].replace("\\", "/"))
            args = args[:i] + args[i + 2:]
    scopes = args
    files = []
    for sc in scopes:
        if os.path.isfile(sc) and sc.endswith(".py"):
            files.append(sc)
            continue
        for root, _dirs, names in os.walk(sc):
            for n in sorted(names):
                if n.endswith(".py"):
                    files.append(os.path.join(root, n))
    files = sorted(set(f.replace("\\", "/") for f in files))
    readers, prose, docs, failed, loose_total = [], [], [], [], 0
    glued_files = []
    builder_hits = []
    for f in files:
        res, err = walk_file(f)
        if err:
            failed.append((f, err))
            continue
        r, p, d, loose, glued = res
        loose_total += loose
        if glued:
            glued_files.append((f, glued))
        for line, why, ex in r:
            if f in builders:
                builder_hits.append((f, line, why, ex))
            else:
                readers.append((f, line, why, ex))
        prose += [(f, line, ex) for line, ex in p]
        docs += [(f, line, ex) for line, ex in d]
    print("--- READER WALK [%s] ---" % label)
    print("SCOPES=%s" % " ".join(scopes))
    print("FILES_WALKED=%d" % len(files))
    print("PARSE_FAILURES=%d%s" % (len(failed),
          "" if not failed else " " + repr(failed)))
    for f in builders:
        print("BUILDER_DECLARED=%s" % f)
    for f, line, why, ex in builder_hits:
        print("  BUILDER_EXCLUDED %s:%d [%s] %s" % (f, line, why, ex))
    for f, line, why, ex in readers:
        print("  READER %s:%d [%s] %s" % (f, line, why, ex))
    for f, line, ex in prose:
        print("  PROSE_MENTION (not a reader) %s:%d %s" % (f, line, ex))
    for f, line, ex in docs:
        print("  DOCSTRING (not counted) %s:%d %s" % (f, line, ex))
    print("PROSE_MENTIONS=%d" % len(prose))
    print("DOCSTRING_MENTIONS=%d" % len(docs))
    print("BUILDER_HITS=%d" % len(builder_hits))
    print("NEAR_MISS_LOOSE_TOKEN_HITS=%d (loose regex over source text, incl."
          " scratch_kuzu_db and every comment/docstring -- printed so the"
          " strict boundary's exclusions are visible)" % loose_total)
    for f, n in glued_files:
        print("  NEAR_MISS_GLUED_TOKEN (a DIFFERENT artifact, excluded by the"
              " left word boundary) %s x%d" % (f, n))
    print("NEAR_MISS_GLUED_FILES=%d" % len(glued_files))
    print("READERS=%d of %d files" % (len(readers), len(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
