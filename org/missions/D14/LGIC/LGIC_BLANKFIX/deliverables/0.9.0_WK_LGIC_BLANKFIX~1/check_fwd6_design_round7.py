#!/usr/bin/env python3
"""check_fwd6_design_round7 -- the repaired FWD-6 design (BF-v-3): its seven parts, its paths, and an owner for every HOLE text.

    python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~1/check_fwd6_design_round7.py

It makes every check check_fwd6_design.py makes (it calls that file's own functions; that file is left as it is):
  1. the `## ` headings outside fenced blocks are exactly the seven required, in order;
  2. every inline backticked repository path in FWD6_DESIGN_round6.md (beside this file) exists.
And the round-7 check, read from the code and never from a typed list:
  3. it parses lib/opal_naming_rootcheck.py with `ast` and enumerates every HOLE text:
       - each `return "HOLE", <text>` (the card line, the stray brace, the grader's raise, the cadence rebuild, the
         no-canonical verdict, and the frame `partial form ...; could not fill`);
       - each `why.append(<text>)` in the function that returns the frame (the blank it could not fill);
       - the text of the collision (`_collisions`, which run_items turns into `decided[i] = (..., "HOLE", detail)`);
       - the reason strings `_ruling_of` returns, which `decide` appends to a card or raised HOLE (`ruling_unread`);
     every other use of the string "HOLE" is counted and not listed (a count key, a kind test, the kind tuple);
  4. for each text it derives a NEEDLE (the longest literal run between %-formats, 60 characters at most, or the expression
     `ans['raised']` when the text is the value of a variable) and requires, in the design's "owed" table (the rows whose
     first cell is H<number>), a row whose second cell is that needle in backticks and whose last cell names an owner: a
     serial of the form N.N.N_XX_NAME, or the words "the creator". A row whose needle matches no text counts as stale
     and fails the run.
Last line, printed once:
  FWD6-DESIGN ok=<bool> headings=<n> paths=<n> missing=<n> hole_texts=<n> owned=<n> unowned=<n>
Python 3.9; ASCII only; standard library only.
"""
import ast
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(HERE, "check_fwd6_design.py")
RELPATH = "lib/opal_naming_rootcheck.py"
OWNER_RE = re.compile(r"\b\d\.\d\.\d_[A-Z]{2,3}_[A-Za-z0-9_]+|\bthe creator\b")


def load_old():
    spec = importlib.util.spec_from_file_location("check_fwd6_design_r6", OLD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def lit(node, consts):
    """The literal text of an expression: strings joined, a %-format's left side, a module constant resolved; else ''."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return consts.get(node.id, "")
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
        return lit(node.left, consts)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return lit(node.left, consts) + lit(node.right, consts)
    if isinstance(node, ast.IfExp):
        return lit(node.body, consts)
    return ""


def needle_of(node, consts):
    """(needle, how). The longest literal run between %-formats (60 characters at most), else a variable's expression."""
    segs = [t.strip(" ;,:()") for t in re.split(r"%[sr]", lit(node, consts))]
    best = max(segs, key=len) if segs else ""
    if len(best) >= 8:
        return best[:60].strip(), "literal"
    for sub in ast.walk(node):
        if isinstance(sub, ast.Subscript):
            return ast.unparse(sub), "expression"
    return best, "short"


def is_str(c, v):
    return isinstance(c, ast.Constant) and c.value == v


def hole_sites(tree):
    """[(function, line, needle, kind)] in file order; plus the count of other uses of the string HOLE."""
    consts = {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            if isinstance(n.value, ast.Constant) and isinstance(n.value.value, str):
                consts[n.targets[0].id] = n.value.value
    funcs = dict((n.name, n) for n in tree.body if isinstance(n, ast.FunctionDef))
    sites, yielders = [], set()

    def add(fn, node, expr, kind):
        nd, how = needle_of(expr, consts)
        sites.append((fn, node.lineno, nd, kind + "/" + how))

    for fn_name, fn in funcs.items():
        for node in ast.walk(fn):
            if isinstance(node, ast.Return) and isinstance(node.value, ast.Tuple) and len(node.value.elts) == 2 \
                    and is_str(node.value.elts[0], "HOLE"):
                yielders.add(id(node.value.elts[0]))
                add(fn_name, node, node.value.elts[1], "return")
                for sub in ast.walk(fn):  # the blanks the frame could not fill
                    if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute) and sub.func.attr == "append" \
                            and isinstance(sub.func.value, ast.Name) and sub.func.value.id == "why" and sub.args:
                        if not any(s[1] == sub.lineno for s in sites):
                            add(fn_name, sub, sub.args[0], "why")
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Tuple) \
                    and any(is_str(e, "HOLE") for e in node.value.elts):
                for e in node.value.elts:
                    if is_str(e, "HOLE"):
                        yielders.add(id(e))
                if "_collisions" not in funcs:
                    raise SystemExit("FWD6-DESIGN ok=False (no _collisions in %s)" % RELPATH)
                for sub in ast.walk(funcs["_collisions"]):
                    if isinstance(sub, ast.Assign) and isinstance(sub.targets[0], ast.Subscript):
                        add("_collisions", sub, sub.value, "assign")
    if "_ruling_of" not in funcs:
        raise SystemExit("FWD6-DESIGN ok=False (no _ruling_of in %s)" % RELPATH)
    for sub in ast.walk(funcs["_ruling_of"]):
        if isinstance(sub, ast.Return) and isinstance(sub.value, ast.Tuple) and len(sub.value.elts) == 2 \
                and isinstance(sub.value.elts[0], ast.Constant) and sub.value.elts[0].value is None and not (isinstance(sub.value.elts[1], ast.Constant)
                                                              and sub.value.elts[1].value is None):
            add("_ruling_of", sub, sub.value.elts[1], "suffix")
    others = sum(1 for n in ast.walk(tree) if is_str(n, "HOLE") and id(n) not in yielders)
    sites.sort(key=lambda s: s[1])
    return sites, others


def owed_rows(text):
    """{needle: [owner cell, ...]} over the table rows whose first cell is H<number>, and the row count."""
    rows, n = {}, 0
    for ln in text.splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 4 or not re.match(r"^H\d+[a-z]?$", cells[0]):
            continue
        m = re.match(r"^`(.+)`$", cells[1])
        if not m:
            continue
        n += 1
        rows.setdefault(m.group(1), []).append(cells[-1])
    return rows, n


def main():
    old = load_old()
    root = old.repo_root(HERE)
    with open(old.DOC, "rb") as fh:
        text = fh.read().decode("utf-8")
    prose, heads = old.split_doc(text)
    toks = old.path_tokens(prose, set(os.listdir(root)))
    missing = sorted(set(t for t in toks if not os.path.exists(os.path.join(root, *t.split("/")))))
    heads_ok = heads == old.HEADINGS
    for m in missing:
        print("MISSING: " + m)
    if not heads_ok:
        print("HEADINGS WANTED: %r" % (old.HEADINGS,))
        print("HEADINGS FOUND:  %r" % (heads,))
    with open(os.path.join(root, *RELPATH.split("/")), "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8"))
    sites, others = hole_sites(tree)
    rows, nrows = owed_rows(text)
    owned, unowned, short = 0, 0, 0
    for fn, line, nd, kind in sites:
        cells = rows.get(nd, [])
        ok = bool(cells) and all(OWNER_RE.search(c) for c in cells)
        owned += 1 if ok else 0
        unowned += 0 if ok else 1
        short += 1 if kind.endswith("/short") else 0
        print("HOLE-TEXT %-12s %-10s %s %s -> %s" % (fn + ":" + str(line), kind, "OWNED  " if ok else "UNOWNED", nd,
                                                    "; ".join(OWNER_RE.search(c).group(0) for c in cells if OWNER_RE.search(c))))
    needles = set(s[2] for s in sites)
    stale = sorted(k for k in rows if k not in needles)
    for k in stale:
        print("STALE ROW: %s" % k)
    print("HOLE-TEXT other uses of the string HOLE (not texts): %d; table rows: %d; texts: %d" % (others, nrows, len(sites)))
    ok = heads_ok and not missing and len(toks) > 0 and unowned == 0 and not stale and short == 0 and len(sites) > 0
    print("FWD6-DESIGN ok=%s headings=%d paths=%d missing=%d hole_texts=%d owned=%d unowned=%d"
          % (ok, len(heads), len(set(toks)), len(missing), len(sites), owned, unowned))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
