"""Signature closure over a BUILT Lambda zip, WITH the attribute-call limb (IRPT_BCKEND IB-pr-416, worker 0.9.0_WK_IRPT_BCKEND~278).

Copied from org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/signature_closure.py (row IRPT_ANLREQ-D2-S16; the
original is untouched). It reads the zip's own bytes, never the repo.

Usage: python signature_closure_attr.py <zip>

LIMB 1 (the original, unchanged): for every call `f(...)` where `f` is bound by `from <packaged module> import f` (a function, or a
class -> its __init__), the call's keywords must be parameters of the packaged callee (or the callee takes **kwargs), and its
positional count must fit (or the callee takes *args). Calls with *a / **kw unpacking are counted as skipped_unpack.

LIMB 2 (new, IB-pr-416): every call `m.f(...)` / `m.Cls(...)` where `m` is bound by `import <packaged module> [as m]` (or
`from <pkg> import <packaged module> [as m]`) and `f` / `Cls` is a top-level function or class of that packaged module is checked the same
way. A `**name` unpack is resolved STATICALLY when `name` is a local bound to a dict literal in the same function and every other use of
`name` is a constant-key subscript store (`name["k"] = v`), or the unpack is itself a dict literal / a conditional of dict literals: its
possible keys are then checked as keywords. This is what sees the irpt-performance-adapter split `Enforcer(**render)` with
render["load_report_owner"] set under a condition. An unpack that cannot be resolved statically (a parameter, a call result, a dict that is
`.update()`d or stored under a non-constant key) is counted in attr_skipped_unpack. Positional `*a` unpacking is skipped the same way.
NOT SEEN by either limb: calls through a variable (`f = m.Cls; f(...)`), a callee reached by getattr, and a class that inherits
its __init__ (no own __init__ -> no signature to read).

Last line: "signature_closure calls=<n> checked=<k> skipped_unpack=<u> mismatched=<m> attr_skipped_unpack=<u> attr_checked=<k>
attr_mismatched=<m>" (it ENDS with attr_checked and attr_mismatched); exit 1 when either mismatch count is > 0.
"""
import ast
import sys
import zipfile


def sig_of(node, drop_self):
    a = node.args
    posonly = [x.arg for x in a.posonlyargs]
    named = [x.arg for x in a.args]
    if drop_self:
        if posonly:
            posonly = posonly[1:]
        elif named:
            named = named[1:]
    return {"pos": len(posonly) + len(named), "kw": set(named) | {x.arg for x in a.kwonlyargs},
            "varargs": a.vararg is not None, "varkw": a.kwarg is not None}


def defs_of(tree):
    out = {}
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out[n.name] = sig_of(n, False)
        elif isinstance(n, ast.ClassDef):
            init = [b for b in n.body if isinstance(b, ast.FunctionDef) and b.name == "__init__"]
            if init:
                out[n.name] = sig_of(init[0], True)
            elif not n.bases and not any(isinstance(b, ast.Assign) or isinstance(b, ast.AnnAssign) for b in n.body):
                out[n.name] = {"pos": 0, "kw": set(), "varargs": False, "varkw": False}
    return out


def _const_keys(d):
    """Keys of a dict literal when every key is a string constant, else None."""
    keys = []
    for k in d.keys:
        if isinstance(k, ast.Constant) and isinstance(k.value, str):
            keys.append(k.value)
        else:
            return None
    return keys


def _enclosing(parents, node):
    while node in parents:
        node = parents[node]
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Module)):
            return node
    return None


def _walk_scope(scope):
    """Nodes of a function/module body, not descending into nested defs/classes' bodies."""
    stack = list(ast.iter_child_nodes(scope))
    while stack:
        n = stack.pop()
        yield n
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            continue
        stack.extend(ast.iter_child_nodes(n))


def local_dict_keys(scope, name):
    """Possible keys of local `name` (a dict literal plus constant-key subscript stores), or None when not statically known."""
    keys, bound = set(), 0
    for n in _walk_scope(scope):
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    ks = _const_keys(n.value) if isinstance(n.value, ast.Dict) else None
                    if ks is None:
                        return None
                    keys.update(ks)
                    bound += 1
                elif isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) and t.value.id == name:
                    sl = t.slice
                    if isinstance(sl, ast.Constant) and isinstance(sl.value, str):
                        keys.add(sl.value)
                    else:
                        return None
        elif isinstance(n, (ast.AugAssign, ast.AnnAssign)):
            t = n.target
            if (isinstance(t, ast.Name) and t.id == name) or \
                    (isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) and t.value.id == name):
                return None
        elif isinstance(n, ast.Delete):
            for t in n.targets:
                if (isinstance(t, ast.Name) and t.id == name) or \
                        (isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) and t.value.id == name):
                    return None
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) \
                and n.func.value.id == name and n.func.attr in ("update", "setdefault", "pop", "popitem", "clear", "__setitem__"):
            return None
        elif isinstance(n, (ast.For, ast.comprehension)):
            t = n.target
            if isinstance(t, ast.Name) and t.id == name:
                return None
    return keys if bound else None


def unpack_keys(expr, scope):
    """Possible keyword names of a `**expr` unpack, or None when unknown."""
    if isinstance(expr, ast.Dict):
        if any(k is None for k in expr.keys):
            return None
        return set(_const_keys(expr) or []) if _const_keys(expr) is not None else None
    if isinstance(expr, ast.IfExp):
        a, b = unpack_keys(expr.body, scope), unpack_keys(expr.orelse, scope)
        return None if a is None or b is None else a | b
    if isinstance(expr, ast.Name) and scope is not None:
        return local_dict_keys(scope, expr.id)
    return None


def check_call(n, s, scope):
    """(status, unknown_keywords, too_many) for a call node n against callee signature s.
    status: 'skip' (unresolvable unpack), or 'checked'."""
    if any(isinstance(a, ast.Starred) for a in n.args):
        return "skip", [], False
    kws = set()
    for k in n.keywords:
        if k.arg is None:
            ks = unpack_keys(k.value, scope)
            if ks is None:
                return "skip", [], False
            kws |= ks
        else:
            kws.add(k.arg)
    unknown = sorted(k for k in kws if k not in s["kw"]) if not s["varkw"] else []
    too_many = len(n.args) > s["pos"] and not s["varargs"]
    return "checked", unknown, too_many


def main():
    z = zipfile.ZipFile(sys.argv[1])
    mods = {}
    for name in z.namelist():
        if name.endswith(".py"):
            mod = name[:-3].replace("/", ".")
            if mod.endswith(".__init__"):
                mod = mod[: -len(".__init__")]
            try:
                mods[mod] = ast.parse(z.read(name).decode("utf-8"), name)
            except SyntaxError as e:
                print("ERROR: %s does not parse: %s" % (name, e))
                sys.exit(1)
    defs = {m: defs_of(t) for m, t in mods.items()}
    calls = checked = skipped = 0
    attr_calls = attr_checked = attr_skipped = 0
    bad, attr_bad = [], []
    for mod, tree in mods.items():
        bound, aliases = {}, {}
        parents = {c: p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
                if n.module in defs:
                    for al in n.names:
                        if al.name in defs[n.module]:
                            bound[al.asname or al.name] = (n.module, al.name)
                for al in n.names:                              # from pkg import module as m
                    full = n.module + "." + al.name
                    if full in defs:
                        aliases[al.asname or al.name] = full
            elif isinstance(n, ast.Import):
                for al in n.names:
                    if al.name in defs:
                        aliases[al.asname or al.name] = al.name
        for n in ast.walk(tree):
            if not isinstance(n, ast.Call):
                continue
            if isinstance(n.func, ast.Name) and n.func.id in bound:
                # LIMB 1 -- the original behaviour (any unpack is skipped), unchanged
                calls += 1
                if any(isinstance(a, ast.Starred) for a in n.args) or any(k.arg is None for k in n.keywords):
                    skipped += 1
                    continue
                checked += 1
                src, fname = bound[n.func.id]
                s = defs[src][fname]
                unknown = sorted(k.arg for k in n.keywords if k.arg not in s["kw"]) if not s["varkw"] else []
                too_many = len(n.args) > s["pos"] and not s["varargs"]
                if unknown or too_many:
                    bad.append("%s:%d calls %s.%s -- unknown keyword(s) %s%s" % (
                        mod, n.lineno, src, fname, unknown,
                        "; %d positional > %d" % (len(n.args), s["pos"]) if too_many else ""))
            elif isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) and n.func.value.id in aliases \
                    and n.func.attr in defs[aliases[n.func.value.id]]:
                # LIMB 2 -- module.f(...) / module.Cls(...)
                attr_calls += 1
                src, fname = aliases[n.func.value.id], n.func.attr
                s = defs[src][fname]
                status, unknown, too_many = check_call(n, s, _enclosing(parents, n))
                if status == "skip":
                    attr_skipped += 1
                    continue
                attr_checked += 1
                if unknown or too_many:
                    attr_bad.append("%s:%d calls %s.%s -- unknown keyword(s) %s%s" % (
                        mod, n.lineno, src, fname, unknown,
                        "; %d positional > %d" % (len(n.args), s["pos"]) if too_many else ""))
    for b in bad:
        print("MISMATCH: " + b)
    for b in attr_bad:
        print("ATTR_MISMATCH: " + b)
    print("signature_closure calls=%d checked=%d skipped_unpack=%d mismatched=%d attr_skipped_unpack=%d attr_checked=%d attr_mismatched=%d"
          % (calls, checked, skipped, len(bad), attr_skipped, attr_checked, len(attr_bad)))
    sys.exit(1 if (bad or attr_bad) else 0)


if __name__ == "__main__":
    main()
