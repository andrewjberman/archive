"""reach_read.py -- which packaged code can a Lambda zip's declared routes reach, and does any of it write?

CTO half of IB-pr-416, AMENDMENT 1, condition 8: before an apply, print from the BUILT zip the handlers reachable from
the function's declared routes and the count of call sites among them that call `artifacts.put`, `retention.reserve`,
or an `ArtifactRepository.get` on `ANALYSIS_COMMENTARY`. A count above 0 is a STOP.

Usage:  python reach_read.py <zip> [--roots mod1,mod2,...] [--json <out>]

METHOD (static, reads only the zip's own bytes; nothing is imported or run):
  1. Every top-level `.py` member is parsed. Every function, method and nested function is a node `module:qualname`.
  2. ROOTS are every node of the root modules (default: entry, status_installed, handler). These modules hold the route
     table, every route's handler closure and the composition that builds the readers, so every declared route's
     handler is a root. The route count is read from the zip (string keys "GET /..." / "POST /..." in the root modules).
  3. EDGES are by NAME and over-approximate on purpose: a node reaches every packaged function, method or class
     `__init__` whose name equals any name it calls OR merely references (a callback passed as a value counts).
     A receiver is never resolved, so `x.put(...)` reaches EVERY packaged `put`.
  4. TARGETS, counted over call sites inside reachable nodes:
       put      a call `.put(...)` that the same over-approximation can bind to a `put` defined in repository.py
       reserve  a call `.reserve(...)`
       get_ac   a call `.get(...)` with an argument that is, or is a module constant equal to, "ANALYSIS_COMMENTARY"
     and, as the definition-side control, whether repository.py's `put` methods and retention.py's `reserve` are
     themselves reachable nodes.

WHAT A RESULT MEANS: the walk over-approximates, so a 0 is sound within the zip's top-level modules (a member under a
sub-directory is listed as NOT WALKED and voids the 0 if it is importable). A count above 0 is a STOP to be read, not
proof that a route writes. Dynamic dispatch through `getattr` with a computed name is invisible to this read.
"""
import ast
import json
import sys
import zipfile

FAMILY = "ANALYSIS_COMMENTARY"
DEFAULT_ROOTS = ("entry", "status_installed", "handler")


class Node:
    def __init__(self, module, qualname, name, tree):
        self.module, self.qualname, self.name, self.tree = module, qualname, name, tree
        self.key = module + ":" + qualname


def _own_walk(fn):
    """Yield the AST nodes of one function body WITHOUT descending into nested defs (they are their own nodes)."""
    stack = list(ast.iter_child_nodes(fn))
    while stack:
        cur = stack.pop()
        yield cur
        if isinstance(cur, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            if isinstance(cur, ast.Lambda):
                stack.extend(ast.iter_child_nodes(cur))
            continue
        stack.extend(ast.iter_child_nodes(cur))


def collect(module, tree):
    nodes, classes = [], {}

    def visit(body, prefix, in_class):
        for item in body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                qual = prefix + item.name
                nodes.append(Node(module, qual, item.name, item))
                visit(item.body, qual + ".", None)
            elif isinstance(item, ast.ClassDef):
                classes[item.name] = prefix + item.name
                visit(item.body, prefix + item.name + ".", item.name)
            elif hasattr(item, "body") and not isinstance(item, ast.Lambda):
                for field in ("body", "orelse", "finalbody", "handlers"):
                    sub = getattr(item, field, None)
                    if isinstance(sub, list):
                        visit([s for s in sub if isinstance(s, ast.AST)], prefix, in_class)
    visit(tree.body, "", None)
    return nodes, classes


def names_used(fn):
    used = set()
    for cur in _own_walk(fn):
        if isinstance(cur, ast.Name):
            used.add(cur.id)
        elif isinstance(cur, ast.Attribute):
            used.add(cur.attr)
    # a nested def is reached by its parent (it is defined there to be used there or returned)
    for cur in ast.iter_child_nodes(fn):
        pass
    return used


def nested_defs(fn):
    out = []
    stack = list(ast.iter_child_nodes(fn))
    while stack:
        cur = stack.pop()
        if isinstance(cur, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.append(cur.name)
            continue
        if isinstance(cur, ast.ClassDef):
            continue
        stack.extend(ast.iter_child_nodes(cur))
    return out


def module_constants(tree):
    out = {}
    for item in tree.body:
        if isinstance(item, ast.Assign) and isinstance(item.value, ast.Constant) and isinstance(item.value.value, str):
            for target in item.targets:
                if isinstance(target, ast.Name):
                    out[target.id] = item.value.value
    return out


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    zpath = argv[1]
    roots = DEFAULT_ROOTS
    out_json = None
    rest = argv[2:]
    while rest:
        flag = rest.pop(0)
        if flag == "--roots":
            roots = tuple(part for part in rest.pop(0).split(",") if part)
        elif flag == "--json":
            out_json = rest.pop(0)
        else:
            print("ERROR: unknown argument " + flag)
            return 2

    modules, not_walked, parse_errors = {}, [], []
    with zipfile.ZipFile(zpath) as zf:
        members = zf.namelist()
        for member in members:
            if not member.endswith(".py"):
                continue
            if "/" in member:
                not_walked.append(member)
                continue
            try:
                modules[member[:-3]] = ast.parse(zf.read(member).decode("utf-8"), member)
            except (SyntaxError, UnicodeDecodeError) as exc:
                parse_errors.append(member + ": " + type(exc).__name__)

    all_nodes, by_name, constants = [], {}, {}
    for module, tree in sorted(modules.items()):
        nodes, classes = collect(module, tree)
        constants[module] = module_constants(tree)
        for node in nodes:
            all_nodes.append(node)
            by_name.setdefault(node.name, []).append(node)
        for cname, cqual in classes.items():
            for node in nodes:
                if node.qualname == cqual + ".__init__":
                    by_name.setdefault(cname, []).append(node)

    missing_roots = [m for m in roots if m not in modules]
    route_keys = set()
    for module in roots:
        tree = modules.get(module)
        if tree is None:
            continue
        for cur in ast.walk(tree):
            if isinstance(cur, ast.Constant) and isinstance(cur.value, str) and \
                    cur.value.split(" ")[0] in ("GET", "POST", "PUT", "DELETE", "PATCH") and " /" in cur.value:
                route_keys.add(cur.value)

    by_key = {node.key: node for node in all_nodes}
    reached = set()
    frontier = [node for node in all_nodes if node.module in roots]
    while frontier:
        node = frontier.pop()
        if node.key in reached:
            continue
        reached.add(node.key)
        wanted = names_used(node.tree)
        for name in wanted:
            for callee in by_name.get(name, ()):
                if callee.key not in reached:
                    frontier.append(callee)
        for name in nested_defs(node.tree):
            key = node.module + ":" + node.qualname + "." + name
            if key in by_key and key not in reached:
                frontier.append(by_key[key])

    def is_family(arg, module):
        if isinstance(arg, ast.Constant) and arg.value == FAMILY:
            return True
        if isinstance(arg, ast.Name) and constants.get(module, {}).get(arg.id) == FAMILY:
            return True
        if isinstance(arg, ast.Attribute) and any(table.get(arg.attr) == FAMILY for table in constants.values()):
            return True
        return False

    repo_put_defs = [n for n in by_name.get("put", ()) if n.module == "repository"]
    sites = {"put": [], "reserve": [], "get_ac": []}
    put_other = []
    for key in sorted(reached):
        node = by_key[key]
        for cur in _own_walk(node.tree):
            if not (isinstance(cur, ast.Call) and isinstance(cur.func, ast.Attribute)):
                continue
            receiver = ast.unparse(cur.func.value)
            where = "%s.py:%d in %s  receiver=%s" % (node.module, cur.lineno, node.qualname, receiver)
            if cur.func.attr == "put":
                (sites["put"] if repo_put_defs else put_other).append(where)
            elif cur.func.attr == "reserve":
                sites["reserve"].append(where)
            elif cur.func.attr == "get":
                args = list(cur.args) + [kw.value for kw in cur.keywords]
                if any(is_family(arg, node.module) for arg in args):
                    sites["get_ac"].append(where)

    defs = {
        "repository.put defs": sorted(n.key for n in repo_put_defs),
        "repository.put defs reached": sorted(n.key for n in repo_put_defs if n.key in reached),
        "retention.reserve defs reached": sorted(
            n.key for n in by_name.get("reserve", ()) if n.module == "retention" and n.key in reached),
    }
    count = len(sites["put"]) + len(sites["reserve"]) + len(sites["get_ac"])
    result = {
        "zip": zpath, "root_modules": list(roots), "missing_root_modules": missing_roots,
        "routes_read": sorted(route_keys), "modules_walked": len(modules), "members_not_walked": not_walked,
        "parse_errors": parse_errors, "nodes_total": len(all_nodes), "nodes_reached": len(reached),
        "reached_by_module": {}, "sites": sites, "definition_control": defs, "count": count,
    }
    for key in reached:
        module = key.split(":")[0]
        result["reached_by_module"][module] = result["reached_by_module"].get(module, 0) + 1
    if out_json:
        with open(out_json, "w", encoding="utf-8") as handle:
            json.dump(result, handle, indent=1, sort_keys=True)

    print("ROUTES READ (%d):" % len(route_keys))
    for route in sorted(route_keys):
        print("  " + route)
    print("MODULES walked=%d  not_walked(sub-directory)=%d  parse_errors=%d  missing_roots=%s"
          % (len(modules), len(not_walked), len(parse_errors), missing_roots or "none"))
    print("REACHED BY MODULE: " + ", ".join(
        "%s=%d" % item for item in sorted(result["reached_by_module"].items())))
    for kind in ("put", "reserve", "get_ac"):
        print("SITES %s (%d):" % (kind, len(sites[kind])))
        for where in sites[kind]:
            print("  " + where)
    for label, keys in sorted(defs.items()):
        print("%s: %s" % (label, keys or "none"))
    verdict = "STOP" if (count or parse_errors or missing_roots) else "PROCEED"
    print("reach_read routes=%d handlers_walked=%d of %d put=%d reserve=%d get_ac=%d count=%d verdict=%s"
          % (len(route_keys), len(reached), len(all_nodes), len(sites["put"]), len(sites["reserve"]),
             len(sites["get_ac"]), count, verdict))
    return 1 if verdict == "STOP" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
