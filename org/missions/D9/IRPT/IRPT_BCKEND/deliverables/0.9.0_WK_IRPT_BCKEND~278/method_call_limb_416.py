"""IB-pr-416 METHOD-call limb (TO AMENDMENT 2; CTO AMENDMENT 7 of the release-1 half: "the closure checks gain a METHOD-call arm").
    python method_call_limb_416.py <lambda_zip>
signature_closure.py reads name calls (f(...)) and signature_closure_attr.py reads module-attribute calls (module.f(...), module.Cls(...)).
Neither can see `obj.method(...)` where obj is a runtime object: the release-1 revision 5 split was exactly that
(`retention.reference(owner, family, logical_id, revision)` against a packaged RetentionPolicy.reference of three parameters).
This limb parses every packaged .py, collects every METHOD defined in a packaged class, and for each `<expr>.m(...)` call whose attribute name
`m` is defined as a method of a packaged class (and is not a method name of a builtin or stdlib container type, where the receiver could be
that type) checks the call's positional count and keywords against EVERY packaged method of that name: the call fits when ANY candidate accepts
it, and is MISMATCHED when none does. A call with a starred argument or a ** mapping is counted as skipped_unpack. A call whose receiver is a
packaged module or a stdlib import alias is the attribute limb's, not this one's.
Last line: "method_call checked=<k> skipped_unpack=<u> not_packaged_method=<n> mismatched=<m>"; exit 1 when m > 0. ASCII only. It reads the zip
and nothing else: no network, no AWS, no import of the packaged code.
"""
import ast
import sys
import zipfile

BUILTIN_METHODS = set()
for _t in (dict, list, set, frozenset, str, bytes, bytearray, tuple, int, float, bool, complex):
    BUILTIN_METHODS.update(n for n in dir(_t) if not n.startswith("__"))
BUILTIN_METHODS.update(["read", "write", "close", "seek", "tell", "flush", "readline", "readlines", "writelines", "send", "recv", "join",
                        "start", "stop", "run", "wait", "submit", "result", "shutdown", "map", "acquire", "release", "put", "get_nowait",
                        "isoformat", "strftime", "timestamp", "total_seconds", "hexdigest", "digest", "update", "encode", "decode",
                        "load", "loads", "dump", "dumps", "match", "fullmatch", "search", "findall", "sub", "group", "groups", "finditer",
                        "info", "warning", "error", "debug", "exception", "critical", "log", "setLevel", "addHandler", "getLogger"])


def params(fn):
    a = fn.args
    pos = [x.arg for x in a.posonlyargs + a.args]
    return {"pos": pos, "ndef": len(a.defaults), "kwonly": [x.arg for x in a.kwonlyargs],
            "kwonly_required": [x.arg for x, d in zip(a.kwonlyargs, a.kw_defaults) if d is None],
            "vararg": a.vararg is not None, "kwarg": a.kwarg is not None}


def kind(fn):
    names = {d.id if isinstance(d, ast.Name) else getattr(d, "attr", "") for d in fn.decorator_list}
    return "static" if "staticmethod" in names else ("class" if "classmethod" in names else "instance")


def accepts(p, npos, kws, drop_first):
    pos = p["pos"][1:] if drop_first and p["pos"] else list(p["pos"])
    required = len(pos) - min(p["ndef"], len(pos))
    if npos > len(pos) and not p["vararg"]:
        return False
    names = set(pos) | set(p["kwonly"])
    if not p["kwarg"] and any(k not in names for k in kws):
        return False
    bound = set(pos[:npos])
    if any(k in bound for k in kws):
        return False
    for i, n in enumerate(pos):
        if i >= npos and i < required and n not in kws:
            return False
    return all(n in kws for n in p["kwonly_required"])


def main():
    z = zipfile.ZipFile(sys.argv[1])
    trees = {}
    for n in z.namelist():
        if n.endswith(".py"):
            try:
                trees[n] = ast.parse(z.read(n).decode("utf-8"), n)
            except SyntaxError:
                pass
    packaged = {n[:-3].replace("/", ".") for n in trees}
    toplevel = {n[:-3].replace("/", "."): {x.name for x in t.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
                for n, t in trees.items()}
    methods = {}
    for n, t in trees.items():
        for cls in [x for x in ast.walk(t) if isinstance(x, ast.ClassDef)]:
            for f in cls.body:
                if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.setdefault(f.name, []).append((n, cls.name, kind(f), params(f)))
    checked = skipped = notpk = mism = 0
    for n, t in sorted(trees.items()):
        aliases = set()
        for x in ast.walk(t):
            if isinstance(x, ast.Import):
                aliases.update((a.asname or a.name).split(".")[0] for a in x.names)
            elif isinstance(x, ast.ImportFrom) and x.module and x.level == 0 and x.module in packaged:
                pass
        enclosing = {}
        for cls in [x for x in ast.walk(t) if isinstance(x, ast.ClassDef)]:
            for sub in ast.walk(cls):
                if isinstance(sub, ast.Call):
                    enclosing[id(sub)] = cls          # innermost class wins (ast.walk is breadth first, later = deeper)
        for c in [x for x in ast.walk(t) if isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute)]:
            m = c.func.attr
            root = c.func.value
            while isinstance(root, (ast.Attribute, ast.Call, ast.Subscript)):
                root = root.value if not isinstance(root, ast.Call) else root.func
            if isinstance(root, ast.Name) and root is c.func.value and (
                    root.id in aliases or (root.id in packaged and m in toplevel.get(root.id, ()))):
                continue                                        # a module attribute call: the attribute limb's
            if m not in methods or m in BUILTIN_METHODS or (m.startswith("__") and m.endswith("__")):
                notpk += 1
                continue
            if any(isinstance(a, ast.Starred) for a in c.args) or any(k.arg is None for k in c.keywords):
                skipped += 1
                continue
            if isinstance(c.func.value, ast.Name) and c.func.value.id == "self":
                own = enclosing.get(id(c))
                if own is None or not any(isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef)) and f.name == m for f in own.body):
                    notpk += 1                                  # self.<port>(...): an injected callable attribute, not a method of this class
                    continue
            checked += 1
            npos, kws = len(c.args), [k.arg for k in c.keywords]
            rv = c.func.value
            unbound_ok = (isinstance(rv, ast.Name) and rv.id[:1].isupper()) or (isinstance(rv, ast.Attribute) and rv.attr[:1].isupper())   # Class.method(obj, ...) / mod.Class.method(obj, ...)
            fit = False
            for (_, _, kd, p) in methods[m]:
                if accepts(p, npos, kws, drop_first=(kd != "static")) or (unbound_ok and accepts(p, npos, kws, drop_first=False)):
                    fit = True
                    break
            if not fit:
                mism += 1
                print("METHOD_MISMATCH: %s:%d calls .%s(%d positional, keywords %s) -- no packaged method of that name accepts it; candidates: %s" % (
                    n[:-3], c.lineno, m, npos, kws, "; ".join("%s.%s(%s)" % (cl, m, ",".join(p["pos"] + p["kwonly"])) for (_, cl, _, p) in methods[m])))
    print("method_call checked=%d skipped_unpack=%d not_packaged_method=%d mismatched=%d" % (checked, skipped, notpk, mism))
    sys.exit(1 if mism else 0)


if __name__ == "__main__":
    main()
