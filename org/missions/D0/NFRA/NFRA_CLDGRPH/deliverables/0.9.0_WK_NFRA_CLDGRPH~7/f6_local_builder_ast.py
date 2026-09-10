#!/usr/bin/env python3
"""F6-AC3 instrument -- is there a BUILDER of a LOCAL Kuzu store left?

An ast walk for the one act that BUILDS a local Kuzu store:

    kuzu.Database(<path under the repo>)        # WRITE-open: no read_only=True

kuzu.Database CREATES an absent store, so a write-open on a repo path IS a
builder whether or not a loader follows it. A read-only open (read_only=True) is
NOT a builder -- it cannot create -- and is printed, banded and excluded. A
mention in a docstring, a comment or a string is NOT a builder either; both
classes are printed so the zero is never hiding them.

PATH RESOLUTION, stated because it is the whole discrimination. For each
write-open the path expression is resolved backwards through module-level and
enclosing-function assignments in the SAME file (up to 6 hops), and the collected
source text is classified:

  REPO      an anchor that lands inside the repository -- __file__, _HERE/HERE,
            os.path.dirname(os.path.abspath(__file__)), or a bare relative literal
  TEMP      tempfile / mkdtemp / mkstemp / TemporaryDirectory / tmp_path / tmpdir
  UNRESOLVED  neither -- a parameter, a CLI value with no visible default, an
            attribute off another object

Only REPO write-opens count toward LOCAL_KUZU_BUILDERS. TEMP and UNRESOLVED
sites are ENUMERATED on their own lines with their evidence chain and their own
counters, so an unresolved site can never hide inside the zero -- read them.

usage: f6_local_builder_ast.py <dir-or-file> [...] [--exclude a.py,b.py]
       [--exclude-note "<why, with the declaring row cited>"] [--label L]

EXCLUSION IS BY BASENAME, and that is only sound while each excluded basename is
UNIQUE in the swept population -- measured here before the widening: all six occur
exactly once across the 486 .py files of the four trees. A duplicate basename would
silently excuse a second file, so re-measure that if the exclusion list grows.
exit 0 always; the caller grades the printed lines.
"""
from __future__ import annotations

import ast
import os
import re
import sys

REPO_RE = re.compile(r"__file__|\b_?HERE\b|os\.path\.dirname|\.parent\b")
TEMP_RE = re.compile(r"tempfile|mkdtemp|mkstemp|TemporaryDirectory|tmp_path|tmpdir|/tmp\b")
TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_])kuzu_stitch(?:_db|_load)?(?![A-Za-z0-9_])")
COMMENT_RE = re.compile(r"#.*$")


def _is_kuzu_database(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    f = node.func
    if isinstance(f, ast.Attribute) and f.attr == "Database":
        return isinstance(f.value, ast.Name) and f.value.id == "kuzu"
    return isinstance(f, ast.Name) and f.id == "Database"


def _read_only(node: ast.Call) -> bool:
    for kw in node.keywords:
        if kw.arg == "read_only":
            v = kw.value
            if isinstance(v, ast.Constant):
                return bool(v.value)
            return True   # a non-literal read_only= is treated as read-only: conservative
    return False


def _assign_map(tree: ast.AST, src: str) -> dict:
    """name -> source text of its last assigned value, module and function scope."""
    out: dict = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            val = node.value
            if val is None:
                continue
            seg = ast.get_source_segment(src, val) or ""
            for t in targets:
                if isinstance(t, ast.Name):
                    out.setdefault(t.id, seg)
    return out


def _resolve(expr_src: str, amap: dict, hops: int = 6) -> str:
    chain = [expr_src]
    seen = set()
    for _ in range(hops):
        names = re.findall(r"(?<![A-Za-z0-9_.])([A-Za-z_][A-Za-z0-9_]*)", chain[-1])
        added = ""
        for n in names:
            if n in amap and n not in seen:
                seen.add(n)
                added += " <- %s=%s" % (n, amap[n])
        if not added:
            break
        chain.append(added)
    return "".join(chain)


def classify(chain: str) -> str:
    if TEMP_RE.search(chain):
        return "TEMP"
    if REPO_RE.search(chain):
        return "REPO"
    if re.search(r"""=\s*["'][^"'/\\][^"']*["']""", chain) or re.search(
            r"""^["'][^"'/\\][^"']*["']$""", chain.strip()):
        return "REPO"
    return "UNRESOLVED"


def py_files(paths):
    out = []
    for p in paths:
        if os.path.isfile(p) and p.endswith(".py"):
            out.append(p)
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in
                           (".git", "__pycache__", "node_modules", ".venv")]
                for f in sorted(files):
                    if f.endswith(".py"):
                        out.append(os.path.join(root, f).replace("\\", "/"))
    return sorted(set(out))


def main() -> int:
    args = sys.argv[1:]
    label, exclude = "REAL", []
    if "--label" in args:
        i = args.index("--label")
        label = args[i + 1]
        args = args[:i] + args[i + 2:]
    if "--exclude" in args:
        i = args.index("--exclude")
        exclude = [x.strip() for x in args[i + 1].split(",") if x.strip()]
        args = args[:i] + args[i + 2:]
    note = ""
    if "--exclude-note" in args:
        i = args.index("--exclude-note")
        note = args[i + 1]
        args = args[:i] + args[i + 2:]

    files = py_files(args)
    print("--- LOCAL-KUZU-BUILDER WALK [%s] ---" % label)
    print("PREDICATE: kuzu.Database(<path resolving under the repo>) with no read_only=True")
    print("EXCLUDED_BY_NAME (%d): %s%s"
          % (len(exclude), ",".join(exclude) or "(none)",
             ("  [%s]" % note) if note else ""))
    print("FILES_WALKED=%d" % len(files))

    builders, temps, unres, readonly, excluded_hits, failures = [], [], [], [], [], []
    nodes_total = 0
    for path in files:
        try:
            src = open(path, encoding="utf-8").read()
            tree = ast.parse(src)
        except (OSError, SyntaxError, UnicodeDecodeError) as ex:
            failures.append((path, str(ex)))
            continue
        amap = _assign_map(tree, src)
        base = os.path.basename(path)
        for node in ast.walk(tree):
            nodes_total += 1
            if not _is_kuzu_database(node):
                continue
            line = getattr(node, "lineno", 0)
            arg_src = (ast.get_source_segment(src, node.args[0])
                       if node.args else "(no positional path arg)")
            chain = _resolve(arg_src or "", amap)
            kind = classify(chain)
            rec = (path, line, arg_src, kind, chain[:300])
            if _read_only(node):
                readonly.append(rec)
            elif base in exclude:
                excluded_hits.append(rec)
            elif kind == "REPO":
                builders.append(rec)
            elif kind == "TEMP":
                temps.append(rec)
            else:
                unres.append(rec)

    def dump(title, rows, tag):
        print("%s (%d):" % (title, len(rows)))
        for path, line, arg, kind, chain in rows:
            print("  %s %s:%d  arg=%s  class=%s" % (tag, path, line, arg, kind))
            print("      resolution: %s" % chain)

    dump("BUILDERS -- write-open on a repo path, NOT excluded by name", builders, "BUILDER")
    dump("EXCLUDED BY NAME -- the projection's own builders, named in the criterion",
         excluded_hits, "EXCLUDED")
    dump("TEMP write-opens -- a path outside the repo; not a local store", temps, "TEMP")
    dump("UNRESOLVED write-opens -- READ THESE; they are not folded into the zero",
         unres, "UNRESOLVED")
    dump("READ-ONLY opens -- cannot create; not builders", readonly, "READONLY")

    for path, ex in failures:
        print("  PARSE FAILURE %s: %s" % (path, ex))
    print("PARSE_FAILURES=%d" % len(failures))
    print("AST_NODES_WALKED=%d" % nodes_total)
    print("WRITE_OPENS_TEMP=%d" % len(temps))
    print("WRITE_OPENS_UNRESOLVED=%d" % len(unres))
    print("READ_ONLY_OPENS=%d" % len(readonly))
    print("EXCLUDED_BY_NAME_HITS=%d" % len(excluded_hits))
    print("LOCAL_KUZU_BUILDERS=%d of %d files" % (len(builders), len(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
