"""Reach read of a BUILT investor-reporting zip (CTO half IB-pr-416 AMENDMENT 1, condition 8).

Question: from the function's entry module, which packaged functions are reachable, and how many call sites among them call
`artifacts.put`, `retention.reserve`, or a repository `get` naming ANALYSIS_COMMENTARY?

Method (static, over-approximating): parse every .py member with ast. Roots are every function and method defined in the entry
module (default `entry.py`), plus that module's top-level statements. A call `f(...)` or `x.f(...)` reaches EVERY packaged
function or method named `f` (and a class named `f` reaches all its methods' names only when called). The walk therefore reaches
at least what the runtime can; a count of 0 is a sound 0 for this method, a count above 0 may be an over-reach and is listed
site by site for a reader to judge.

Usage: python reach_read_416.py <zip> [entry_module.py]
Last line: reach_read routes=<r> modules=<m> defs=<d> reached=<n> put=<a> reserve=<b> commentary_get=<c> commentary_refs=<e>
ASCII only. No network call.
"""
import ast
import sys
import zipfile

FAMILY = "ANALYSIS_COMMENTARY"


def src(node):
    try:
        return ast.unparse(node)
    except Exception:
        return ""


def main():
    zpath = sys.argv[1]
    entry_mod = sys.argv[2] if len(sys.argv) > 2 else "entry.py"
    zf = zipfile.ZipFile(zpath)
    trees = {}
    skipped = []
    for name in zf.namelist():
        if not name.endswith(".py"):
            continue
        try:
            trees[name] = ast.parse(zf.read(name).decode("utf-8"))
        except SyntaxError as exc:
            skipped.append("%s (%s)" % (name, exc.msg))
    if entry_mod not in trees:
        print("ERROR: %s not in the zip" % entry_mod)
        print("reach_read ERROR")
        sys.exit(2)

    defs = {}       # simple name -> list of (module, qualname, node)
    classes = {}    # class name -> list of (module, node)
    all_defs = []
    for mod, tree in trees.items():
        stack = [(tree, "")]
        while stack:
            node, prefix = stack.pop()
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    q = prefix + child.name
                    defs.setdefault(child.name, []).append((mod, q, child))
                    all_defs.append((mod, q))
                    stack.append((child, q + "."))
                elif isinstance(child, ast.ClassDef):
                    classes.setdefault(child.name, []).append((mod, child))
                    stack.append((child, prefix + child.name + "."))
                else:
                    stack.append((child, prefix))

    def calls_in(node):
        out = []
        for n in ast.walk(node):
            if isinstance(n, ast.Call):
                out.append(n)
        return out

    def callee_name(call):
        f = call.func
        if isinstance(f, ast.Name):
            return f.id
        if isinstance(f, ast.Attribute):
            return f.attr
        return None

    reached = {}
    queue = []

    def reach(mod, q, node):
        key = (mod, q)
        if key not in reached:
            reached[key] = node
            queue.append((mod, q, node))

    entry_tree = trees[entry_mod]
    # roots: the entry module's own body (top-level calls) and every def in it
    queue.append((entry_mod, "<module>", entry_tree))
    reached[(entry_mod, "<module>")] = entry_tree
    for name, lst in defs.items():
        for mod, q, node in lst:
            if mod == entry_mod:
                reach(mod, q, node)

    while queue:
        mod, q, node = queue.pop()
        for call in calls_in(node):
            nm = callee_name(call)
            if nm is None:
                continue
            for m2, q2, n2 in defs.get(nm, []):
                reach(m2, q2, n2)
            for m2, cnode in classes.get(nm, []):
                for child in cnode.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name in (
                            "__init__", "__post_init__", "__call__", "__new__"):
                        reach(m2, cnode.name + "." + child.name, child)

    routes = []
    for n in ast.walk(entry_tree):
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ("OPERATION", "OPERATIONS") for t in n.targets):
            routes.append(src(n.value))

    put_sites, reserve_sites, get_sites, ref_sites = [], [], [], []
    seen_calls = set()
    for (mod, q), node in sorted(reached.items()):
        if q == "<module>":
            continue
        for call in calls_in(node):
            ident = (mod, call.lineno, call.col_offset)
            if ident in seen_calls:
                continue
            f = call.func
            if not isinstance(f, ast.Attribute):
                continue
            recv = src(f.value)
            text = src(call)
            if f.attr == "put" and "artifact" in recv.lower():
                seen_calls.add(ident)
                put_sites.append("%s:%d in %s: %s" % (mod, call.lineno, q, text[:150]))
            elif f.attr == "reserve":
                seen_calls.add(ident)
                reserve_sites.append("%s:%d in %s: %s" % (mod, call.lineno, q, text[:150]))
            elif f.attr == "get" and FAMILY in text:
                seen_calls.add(ident)
                get_sites.append("%s:%d in %s: %s" % (mod, call.lineno, q, text[:150]))
        for n in ast.walk(node):
            if (isinstance(n, ast.Name) and n.id == FAMILY) or (isinstance(n, ast.Attribute) and n.attr == FAMILY) or (
                    isinstance(n, ast.Constant) and n.value == FAMILY):
                ref_sites.append("%s:%d in %s" % (mod, getattr(n, "lineno", 0), q))
    ref_sites = sorted(set(ref_sites))

    print("zip: %s" % zpath)
    print("entry module: %s; routes (OPERATION constants): %s" % (entry_mod, routes or "none declared by constant"))
    print("DENOMINATOR: %d .py modules parsed (%d skipped: %s); %d function/method defs packaged; %d reached from the entry" % (
        len(trees), len(skipped), skipped or "none", len(all_defs), len([k for k in reached if k[1] != "<module>"])))
    for label, sites in (("artifacts.put", put_sites), ("reserve", reserve_sites), ("get naming " + FAMILY, get_sites),
                         ("any reference to " + FAMILY, ref_sites)):
        print("%s call sites in reached code: %d" % (label, len(sites)))
        for s in sites:
            print("    " + s)
    print("reach_read routes=%d modules=%d defs=%d reached=%d put=%d reserve=%d commentary_get=%d commentary_refs=%d" % (
        len(routes), len(trees), len(all_defs), len([k for k in reached if k[1] != "<module>"]), len(put_sites),
        len(reserve_sites), len(get_sites), len(ref_sites)))


if __name__ == "__main__":
    main()
