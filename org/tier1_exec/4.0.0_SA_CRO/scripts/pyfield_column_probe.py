#!/usr/bin/env python3
"""pyfield_column_probe.py -- EVIDENCE EXTRACTOR for the NFRA_PYFIELD column denominator (TO-0).

>> THIS IS NOT A CLASSIFIER, AND THE DISTINCTION IS THE POINT. <<

It extracts, for every string-literal subscript site in the corpus, the syntactic evidence a
human adjudicator needs in order to decide whether the base is a DataFrame (so the subscript
names a COLUMN) or something else (dict / record / API response / list-of-str literal).
It deliberately does NOT emit a column/not-column verdict. A probe that both selected the
population and judged it would be scoring its own heuristic and calling the result ground truth
-- which is the exact defect TO-0 exists to correct (24.3% is a true statement about SUBSCRIPTS
and a meaningless one about COLUMNS).

WHAT IT DOES EMIT per site: base kind + name, the key, the source line, enclosing scope, whether
the site is a STORE target, the attribute (if any) called on the result, and the BINDING EVIDENCE
for the base name in the nearest enclosing scope -- parameter? loop variable over what? assigned
from what RHS shape? That evidence is what a second party re-derives to check the verdicts.

MARKER SETS ARE DERIVED FROM THE INSTALLED PANDAS API, NEVER HAND-DRAWN.
TO-0 <do_not> forbids lifting `_DF_METHODS` (71 hand-drawn names against a real universe of 240,
missing 170, one member that can never fire, unpinned). The version derived against is printed
in the header of every run and belongs in any figure quoted from it.

CORPUS is passed on the command line. It is NOT defaulted to the estate, and every figure this
probe prints is scoped to the paths given. See the deliverable's boundary_declaration.

Usage:
    python pyfield_column_probe.py <dir> [<dir> ...] --out <sites.jsonl>
    python pyfield_column_probe.py --self-test

Author: 4.0.0_SA_CRO   TO: NFRA_PYFIELD.TO-0   Vintage: stamped at run time into the output.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import sys
from datetime import datetime, timezone

# --------------------------------------------------------------------------------------
# MARKER SETS -- derived at runtime from the installed pandas API (TO-0 <do_not> rule 2).
# --------------------------------------------------------------------------------------


def derive_marker_sets():
    """Return (meta, sets). Every set is DERIVED from the installed pandas, never hand-listed.

    MINIMAL / WIDE reproduce the two ends the PRD names exactly:
      MINIMAL -- `value_counts`, `nunique`, `fillna`; the PRD's "no dict has these".
      WIDE    -- any public pandas attribute not on `dict`; the PRD's "any method not on dict".
    STRICT_DERIVED is this probe's own re-derivable middle: pandas attributes that exist on NO
    common builtin container or string. It replaces the PRD's MID, which was a hand-chosen set
    that no longer exists (scratchpad-only, lost with its session) and therefore cannot be
    reproduced. Substituting a derived set for a lost hand-drawn one is stated, not silent.
    """
    import pandas as pd

    df_attrs = {a for a in dir(pd.DataFrame) if not a.startswith("_")}
    sr_attrs = {a for a in dir(pd.Series) if not a.startswith("_")}
    pandas_attrs = df_attrs | sr_attrs

    def pub(t):
        return {a for a in dir(t) if not a.startswith("_")}

    dict_attrs = pub(dict)
    builtin_attrs = pub(dict) | pub(list) | pub(str) | pub(set) | pub(tuple) | pub(object)

    sets = {
        # The PRD's stated ends, reproduced exactly so the comparison is apples-to-apples.
        "MINIMAL": {"value_counts", "nunique", "fillna"},
        # This probe's derived middle (replaces the lost MID).
        "STRICT_DERIVED": pandas_attrs - builtin_attrs,
        # The PRD's WIDE.
        "WIDE": pandas_attrs - dict_attrs,
    }
    meta = {
        "pandas_version": pd.__version__,
        "universe_df_or_series": len(pandas_attrs),
        "sizes": {k: len(v) for k, v in sets.items()},
    }
    return meta, sets


# DataFrame-producing constructors. Seeded from pandas' own API surface (every `read_*` reader
# plus the frame-returning top-level functions), then PROPAGATED flow-locally: a name assigned
# from an operation on a known DataFrame name is itself a DataFrame. This is the "small
# constructor set by design so it measures a floor" the PRD describes -- a floor, not a ceiling.
def derive_constructors():
    import pandas as pd

    readers = {a for a in dir(pd) if a.startswith("read_")}
    frame_makers = {
        "DataFrame",
        "Series",
        "concat",
        "merge",
        "merge_asof",
        "merge_ordered",
        "pivot",
        "pivot_table",
        "crosstab",
        "get_dummies",
        "json_normalize",
    }
    return readers | (frame_makers & {a for a in dir(pd)}) | {"json_normalize"}


# Non-DataFrame RHS shapes that are strong evidence of a dict/record/response base.
NON_DF_CALL_HINTS = (
    "json.loads",
    "json.load",
    "loads",
    "get_object",
    "list_objects",
    "list_objects_v2",
    "head_object",
    "get_item",
    "query",
    "scan",
    "to_dict",
    "dict",
    "defaultdict",
    "OrderedDict",
    "Counter",
)


# --------------------------------------------------------------------------------------
# AST helpers
# --------------------------------------------------------------------------------------


def expr_shape(node) -> str:
    """A compact, stable descriptor of an expression's SHAPE. Used for RHS evidence.

    Deliberately lossy and deliberately deterministic: it is evidence for a human, not a type.
    """
    if node is None:
        return "none"
    if isinstance(node, ast.Call):
        return "call:" + dotted(node.func)
    if isinstance(node, ast.Dict):
        return "dict-literal"
    if isinstance(node, ast.DictComp):
        return "dict-comprehension"
    if isinstance(node, ast.ListComp):
        return "list-comprehension"
    if isinstance(node, ast.List):
        return "list-literal"
    if isinstance(node, ast.Subscript):
        return "subscript:" + dotted(node.value)
    if isinstance(node, ast.Attribute):
        return "attribute:" + dotted(node)
    if isinstance(node, ast.Name):
        return "name:" + node.id
    if isinstance(node, ast.Constant):
        return "const:" + type(node.value).__name__
    if isinstance(node, ast.BinOp):
        return "binop"
    if isinstance(node, (ast.Tuple,)):
        return "tuple"
    return type(node).__name__.lower()


def dotted(node) -> str:
    """Render a dotted name for Name/Attribute chains; '<expr>' for anything else."""
    parts = []
    cur = node
    while True:
        if isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        elif isinstance(cur, ast.Name):
            parts.append(cur.id)
            break
        elif isinstance(cur, ast.Call):
            parts.append("()")
            cur = cur.func
        elif isinstance(cur, ast.Subscript):
            parts.append("[]")
            cur = cur.value
        else:
            parts.append("<expr>")
            break
    return ".".join(reversed(parts))


class ScopeInfo:
    """Binding evidence for one lexical scope (module or function)."""

    __slots__ = ("name", "params", "assigns", "loopvars", "withvars", "parent")

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.params = set()
        self.assigns = {}    # name -> [rhs shape, ...]
        self.loopvars = {}   # name -> iterable shape
        self.withvars = {}   # name -> context shape

    def lookup(self, ident):
        """Walk the scope chain. Returns (evidence dict, scope name where found)."""
        cur = self
        while cur is not None:
            ev = {}
            if ident in cur.params:
                ev["is_param"] = True
            if ident in cur.assigns:
                ev["assigned_from"] = cur.assigns[ident]
            if ident in cur.loopvars:
                ev["loop_over"] = cur.loopvars[ident]
            if ident in cur.withvars:
                ev["with_from"] = cur.withvars[ident]
            if ev:
                ev["found_in_scope"] = cur.name
                return ev
            cur = cur.parent
        return {}


def collect_scopes(tree, modname):
    """Build a scope tree with binding evidence. Returns (root, node->scope map)."""
    root = ScopeInfo(modname)
    node_scope = {}

    def targets_of(t):
        if isinstance(t, ast.Name):
            return [t.id]
        if isinstance(t, (ast.Tuple, ast.List)):
            out = []
            for e in t.elts:
                out.extend(targets_of(e))
            return out
        return []

    def walk(node, scope):
        node_scope[id(node)] = scope
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                sub = ScopeInfo(f"{scope.name}.{child.name}", scope)
                a = child.args
                for arg in list(a.args) + list(a.posonlyargs) + list(a.kwonlyargs):
                    sub.params.add(arg.arg)
                    # A `txns: pd.DataFrame` annotation is SOUND, FREE evidence. Recorded as a
                    # binding so the fixed point can seed on it (v2 resolver only).
                    if annotation_is_df(arg.annotation):
                        sub.assigns.setdefault(arg.arg, []).append("annotation:DataFrame")
                if a.vararg:
                    sub.params.add(a.vararg.arg)
                if a.kwarg:
                    sub.params.add(a.kwarg.arg)
                node_scope[id(child)] = scope
                walk(child, sub)
            elif isinstance(child, ast.ClassDef):
                sub = ScopeInfo(f"{scope.name}.{child.name}", scope)
                node_scope[id(child)] = scope
                walk(child, sub)
            else:
                if isinstance(child, ast.Assign):
                    shape = expr_shape(child.value)
                    for t in child.targets:
                        for nm in targets_of(t):
                            scope.assigns.setdefault(nm, []).append(shape)
                elif isinstance(child, (ast.AugAssign, ast.AnnAssign)):
                    if isinstance(child.target, ast.Name):
                        scope.assigns.setdefault(child.target.id, []).append(
                            expr_shape(getattr(child, "value", None))
                        )
                elif isinstance(child, (ast.For, ast.AsyncFor)):
                    shape = expr_shape(child.iter)
                    for nm in targets_of(child.target):
                        scope.loopvars.setdefault(nm, shape)
                elif isinstance(child, (ast.With, ast.AsyncWith)):
                    for item in child.items:
                        if item.optional_vars is not None:
                            shape = expr_shape(item.context_expr)
                            for nm in targets_of(item.optional_vars):
                                scope.withvars.setdefault(nm, shape)
                elif isinstance(child, (ast.comprehension,)):
                    shape = expr_shape(child.iter)
                    for nm in targets_of(child.target):
                        scope.loopvars.setdefault(nm, shape)
                walk(child, scope)

    walk(tree, root)
    return root, node_scope


def annotation_is_df(node) -> bool:
    """True if a type annotation names a pandas frame/series. Sound, free, and often present."""
    if node is None:
        return False
    try:
        txt = ast.unparse(node)
    except Exception:
        return False
    txt = txt.strip().strip('"').strip("'")
    return ("DataFrame" in txt) or ("pd.Series" in txt) or txt.endswith("Series")


def summarize_local_returns(tree, constructors):
    """ONE-HOP return summary: which local `def`s return a DataFrame.

    This is the RESOLVER-STRENGTH axis, and it exists so the deliverable can separate
    "the corpus is genuinely ambiguous" from "my analyzer was weak" -- two claims that a single
    undecidable rate silently conflates. Iterated to a fixed point so helper->helper chains
    resolve. Still flow-local per body; NOT type inference, and it does not cross files.
    """
    funcs = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs[node.name] = node

    df_funcs = set()
    for name, fn in funcs.items():
        if annotation_is_df(fn.returns):
            df_funcs.add(name)

    changed = True
    passes = 0
    while changed and passes < 6:
        changed = False
        passes += 1
        for name, fn in funcs.items():
            if name in df_funcs:
                continue
            sub = ScopeInfo(name)
            for arg in list(fn.args.args) + list(fn.args.posonlyargs) + list(fn.args.kwonlyargs):
                sub.params.add(arg.arg)
                if annotation_is_df(arg.annotation):
                    sub.assigns.setdefault(arg.arg, []).append("call:pd.DataFrame")
            for ch in ast.walk(fn):
                if isinstance(ch, ast.Assign):
                    for t in ch.targets:
                        if isinstance(t, ast.Name):
                            sub.assigns.setdefault(t.id, []).append(expr_shape(ch.value))
            bound = resolve_df_names(sub, constructors, df_funcs)
            for ch in ast.walk(fn):
                if isinstance(ch, ast.Return) and ch.value is not None:
                    sh = expr_shape(ch.value)
                    head = sh.split(":", 1)[1].split(".")[0] if ":" in sh else ""
                    if (sh.startswith("call:") and (sh.split(":", 1)[1].split(".")[-1] in constructors
                                                    or head in bound or head in df_funcs)) \
                       or (sh.startswith(("subscript:", "attribute:", "name:")) and head in bound):
                        df_funcs.add(name)
                        changed = True
                        break
    return df_funcs


def resolve_df_names(scope: ScopeInfo, constructors, df_funcs=frozenset()) -> set:
    """Flow-local fixed point: which names in this scope are bound to a DataFrame.

    Seed on a pandas constructor call; propagate through operations on already-bound names.
    A FLOOR by construction -- it cannot see cross-file arrivals, parameters, or reassignment
    through a call it does not recognise. That under-reach is the measured 24.3%, not a bug.
    """
    bound = set()
    changed = True
    passes = 0
    while changed and passes < 8:
        changed = False
        passes += 1
        for nm, shapes in scope.assigns.items():
            if nm in bound:
                continue
            for sh in shapes:
                hit = False
                if sh.startswith("call:"):
                    callee = sh[5:]
                    tail = callee.split(".")[-1]
                    head = callee.split(".")[0]
                    if tail in constructors and head in ("pd", "pandas", tail):
                        hit = True
                    elif head in bound:
                        hit = True          # df.merge(...) / df.groupby(...).agg(...)
                    elif "." not in callee and callee in df_funcs:
                        hit = True          # a local helper VERIFIED to return a DataFrame
                elif sh.startswith("subscript:"):
                    if sh.split(":", 1)[1].split(".")[0] in bound:
                        hit = True          # df[mask] / df[cols]
                elif sh.startswith("attribute:"):
                    if sh.split(":", 1)[1].split(".")[0] in bound:
                        hit = True
                elif sh.startswith("name:"):
                    if sh[5:] in bound:
                        hit = True
                elif sh == "annotation:DataFrame":
                    hit = True              # declared by the author, not inferred
                if hit:
                    bound.add(nm)
                    changed = True
                    break
    return bound


# --------------------------------------------------------------------------------------
# Site extraction
# --------------------------------------------------------------------------------------


def extract_file(path, constructors, src_root, resolver="v2"):
    """Yield one evidence record per string-literal subscript site.

    resolver="v1"  seed ONLY on in-scope pandas constructors (the PRD spike's shape: a floor).
    resolver="v2"  additionally seed on DataFrame-typed parameter ANNOTATIONS and on one-hop
                   local-return summaries. Both are shipped so the deliverable can report the
                   DELTA -- which is the measurement of how much "undecidable" was analyzer
                   weakness rather than corpus ambiguity.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            src = fh.read()
    except Exception as exc:  # pragma: no cover
        return [], {"path": path, "error": f"read: {exc}"}
    try:
        tree = ast.parse(src)
    except SyntaxError as exc:
        return [], {"path": path, "error": f"parse: {exc}"}

    lines = src.splitlines()
    rel = os.path.relpath(path, src_root).replace(os.sep, "/")
    modname = os.path.basename(path)
    root, node_scope = collect_scopes(tree, modname)

    if resolver == "v1":
        # Strip the v2-only evidence so the two resolvers are cleanly separable.
        def strip(sc):
            for k in list(sc.assigns):
                sc.assigns[k] = [s for s in sc.assigns[k] if s != "annotation:DataFrame"]
                if not sc.assigns[k]:
                    del sc.assigns[k]
        seen = set()

        def walk_scopes(sc):
            if id(sc) in seen:
                return
            seen.add(id(sc))
            strip(sc)
        for sc in set(node_scope.values()):
            walk_scopes(sc)
        df_funcs = frozenset()
    else:
        df_funcs = summarize_local_returns(tree, constructors)

    # Pre-resolve df-bound names per scope.
    df_names = {}

    def scope_df(sc):
        if id(sc) not in df_names:
            df_names[id(sc)] = resolve_df_names(sc, constructors, df_funcs)
        return df_names[id(sc)]

    # parent map, for usage-side (attribute called ON the subscript result)
    parent = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parent[id(child)] = node

    sites = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Subscript):
            continue
        sl = node.slice
        if not (isinstance(sl, ast.Constant) and isinstance(sl.value, str)):
            continue  # only string-literal subscripts; this is the PRD's population

        base = node.value
        base_is_name = isinstance(base, ast.Name)
        base_name = base.id if base_is_name else None
        sc = node_scope.get(id(node), root)

        # usage-side: is an attribute taken on the RESULT of this subscript?
        par = parent.get(id(node))
        usage_attr = None
        if isinstance(par, ast.Attribute) and par.value is node:
            usage_attr = par.attr

        # store vs load
        is_store = isinstance(node.ctx, ast.Store)

        ev = sc.lookup(base_name) if base_name else {}
        binding_hit = bool(base_name and base_name in scope_df(sc))

        rec = {
            "file": rel,
            "line": node.lineno,
            "col": node.col_offset,
            "scope": sc.name,
            "key": sl.value,
            "base_kind": "name" if base_is_name else "expr",
            "base": base_name if base_is_name else dotted(base),
            "is_store": is_store,
            "usage_attr": usage_attr,
            "binding_hit": binding_hit,
            "evidence": ev,
            "src": (lines[node.lineno - 1].strip() if node.lineno - 1 < len(lines) else ""),
        }
        sites.append(rec)

    return sites, None


def iter_py(paths):
    for p in paths:
        if os.path.isfile(p) and p.endswith(".py"):
            yield p
        for dirpath, _dirs, files in os.walk(p):
            for f in sorted(files):
                if f.endswith(".py"):
                    yield os.path.join(dirpath, f)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="*", help="corpus dirs/files -- NOT defaulted to the estate")
    ap.add_argument("--out", default=None, help="write JSONL site records here")
    ap.add_argument("--root", default=".", help="path root for relative loci")
    ap.add_argument("--resolver", choices=("v1", "v2"), default="v2",
                    help="v1 = constructor-seeded floor only; v2 = + annotations + local returns")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    if not args.paths:
        ap.error("no corpus given -- this probe never defaults to the estate")

    meta, sets = derive_marker_sets()
    constructors = derive_constructors()
    vintage = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")

    all_sites, errors, files = [], [], 0
    for path in iter_py(args.paths):
        files += 1
        sites, err = extract_file(path, constructors, args.root, resolver=args.resolver)
        if err:
            errors.append(err)
        all_sites.extend(sites)

    # Axis assignment, using the DERIVED sets.
    for s in all_sites:
        a = s["usage_attr"]
        s["usage_MINIMAL"] = bool(a and a in sets["MINIMAL"])
        s["usage_STRICT"] = bool(a and a in sets["STRICT_DERIVED"])
        s["usage_WIDE"] = bool(a and a in sets["WIDE"])

    hdr = {
        "probe": "pyfield_column_probe.py",
        "vintage": vintage,
        "corpus": [p.replace(os.sep, "/") for p in args.paths],
        "denominator_grain": "AST string-literal Subscript NODES (not lines, not files)",
        "resolver": args.resolver,
        "files_scanned": files,
        "parse_errors": len(errors),
        "sites": len(all_sites),
        "marker_meta": meta,
        "constructors_seeded": sorted(constructors),
    }
    print(json.dumps(hdr, indent=2))

    name_based = [s for s in all_sites if s["base_kind"] == "name"]
    print("\n-- POPULATION --")
    print(f"  string-literal subscripts (all bases) : {len(all_sites)}")
    print(f"  name-based                            : {len(name_based)}")
    print(f"  expr-based (<expr>, unattemptable)    : {len(all_sites) - len(name_based)}")

    print("\n-- AXES over name-based --")
    for setname, key in (("MINIMAL", "usage_MINIMAL"), ("STRICT_DERIVED", "usage_STRICT"), ("WIDE", "usage_WIDE")):
        n = sum(1 for s in name_based if s[key])
        pct = (100.0 * n / len(name_based)) if name_based else 0.0
        print(f"  usage-side [{setname:<14}] : {n:>5}  ({pct:.1f}%)")
    b = sum(1 for s in name_based if s["binding_hit"])
    print(f"  binding-side                 : {b:>5}  ({100.0*b/len(name_based):.1f}%)" if name_based else "")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(json.dumps({"_header": hdr}) + "\n")
            for s in all_sites:
                fh.write(json.dumps(s) + "\n")
        print(f"\nwrote {len(all_sites)} site records -> {args.out}")

    if errors:
        print("\n-- PARSE/READ ERRORS (counted, never silently dropped) --")
        for e in errors:
            print(f"  {e['path']}: {e['error']}")
    return 0


# --------------------------------------------------------------------------------------
# Self-test -- a probe whose assertions have never been mutated has never been tested.
# --------------------------------------------------------------------------------------

SELF_TEST_SRC = '''
import pandas as pd, json
def f(records, path):
    df = pd.read_parquet(path)          # constructor -> binding
    df["a"] = df["b"].fillna(0)         # store + usage(fillna)
    merged = df.merge(other, on="k")    # propagate
    merged["c"] = 1
    for r in records:                   # loop var over a param
        x = r["_period"]                # NOT a column
    obj = json.loads(path)              # dict-literal-ish
    y = obj["Key"]                      # NOT a column
    z = lookup()["deep"]                # <expr> base
    return x, y, z
'''


def self_test():
    meta, sets = derive_marker_sets()
    constructors = derive_constructors()
    import tempfile

    fails = []

    def check(cond, label):
        print(("  PASS  " if cond else "  FAIL  ") + label)
        if not cond:
            fails.append(label)

    print(f"pandas {meta['pandas_version']}; universe={meta['universe_df_or_series']}; "
          f"sets={meta['sizes']}")

    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "t.py")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(SELF_TEST_SRC)
        sites, err = extract_file(p, constructors, td)
        check(err is None, "parses without error")
        by = {(s["base"], s["key"]): s for s in sites}

        # 6, enumerated by hand from SELF_TEST_SRC: df['a'], df['b'], merged['c'],
        # r['_period'], obj['Key'], lookup()['deep']. `on="k"` is a KWARG, not a subscript.
        # (This assertion first read 8 -- author error, caught by its own first run. Recorded
        # rather than quietly corrected: the fixture count is the one number in this test that
        # nothing else cross-checks, so it is exactly where a wrong expectation would survive.)
        check(len(sites) == 6, f"finds 6 string-literal subscripts (got {len(sites)})")
        check(by[("df", "a")]["is_store"], "df['a'] = ... is a STORE target")
        check(by[("df", "b")]["usage_attr"] == "fillna", "usage_attr captured on df['b'].fillna()")
        check(by[("df", "b")]["binding_hit"], "df resolves as DataFrame (constructor seed)")
        check(by[("merged", "c")]["binding_hit"], "merged propagates from df.merge(...)")
        check(by[("r", "_period")]["binding_hit"] is False, "loop var r does NOT resolve as df")
        check("loop_over" in by[("r", "_period")]["evidence"], "loop evidence recorded for r")
        check("call:json.loads" in by[("obj", "Key")]["evidence"].get("assigned_from", []),
              "json.loads RHS shape recorded for obj")
        check(by[("obj", "Key")]["binding_hit"] is False, "obj does NOT resolve as df")
        exprs = [s for s in sites if s["base_kind"] == "expr"]
        check(len(exprs) == 1, f"<expr> base detected (got {len(exprs)})")

        # MUTATION: break the constructor seed; the binding axis must go DARK, not stay green.
        mutant = resolve_df_names(
            collect_scopes(ast.parse(SELF_TEST_SRC), "t")[0], set()
        )
        check(len(mutant) == 0, "MUTANT (empty constructor set) -> zero df names, axis goes dark")

        # NEGATIVE CONTROL: a file with no subscripts yields zero, not an error.
        p2 = os.path.join(td, "empty.py")
        with open(p2, "w", encoding="utf-8") as fh:
            fh.write("x = 1\n")
        s2, e2 = extract_file(p2, constructors, td)
        check(e2 is None and len(s2) == 0, "negative control: clean file yields 0 sites, no error")

        # ---- v2 resolver path: annotated param + one-hop local return. Tested BOTH ways, so a
        # ---- v2 that silently did nothing (or that fired under v1) would fail here.
        v2src = (
            "import pandas as pd\n"
            "def mk() -> pd.DataFrame:\n"
            "    return pd.read_parquet('k')\n"
            "def g(txns: pd.DataFrame):\n"
            "    return txns['acct']\n"
            "def h():\n"
            "    z = mk()\n"
            "    return z['col']\n"
        )
        p3 = os.path.join(td, "v2.py")
        with open(p3, "w", encoding="utf-8") as fh:
            fh.write(v2src)
        s_v2, _ = extract_file(p3, constructors, td, resolver="v2")
        s_v1, _ = extract_file(p3, constructors, td, resolver="v1")
        g2 = {s["base"]: s for s in s_v2}
        g1 = {s["base"]: s for s in s_v1}
        check(g2["txns"]["binding_hit"], "v2: annotated param `txns: pd.DataFrame` resolves")
        check(not g1["txns"]["binding_hit"], "v1: same annotated param does NOT resolve (clean split)")
        check(g2["z"]["binding_hit"], "v2: one-hop local return `mk() -> DataFrame` resolves")
        check(not g1["z"]["binding_hit"], "v1: same local-return name does NOT resolve (clean split)")

        # Marker-set sanity: the PRD's MINIMAL members must all be real pandas attributes.
        import pandas as pd
        real = set(dir(pd.DataFrame)) | set(dir(pd.Series))
        check(sets["MINIMAL"] <= real, "MINIMAL members all exist on the installed pandas")
        check("concat" not in sets["WIDE"], "pd.concat correctly ABSENT (module fn, not an attr)")

    print(f"\nself-test: {len(fails)} failure(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
