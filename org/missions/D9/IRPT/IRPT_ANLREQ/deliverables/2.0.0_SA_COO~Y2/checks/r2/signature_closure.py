"""Signature closure over a BUILT Lambda zip (issuer 2.0.0_SA_COO~Y2, row IRPT_ANLREQ-D2-S16).

symbol_closure.py proves every imported NAME resolves inside the zip; it cannot see a call whose keywords or arity the
packaged callee does not accept (release 1 rev 4: status_installed.py passed additional_policy_revisions= to a packaged
composition.py that predates it, and every call raised TypeError). This reads the zip's own bytes, never the repo.

Usage: python signature_closure.py <zip>
For every call `f(...)` where `f` is bound by `from <packaged module> import f` (a function, or a class -> its __init__),
the call's keywords must be parameters of the packaged callee (or the callee takes **kwargs), and its positional count
must fit (or the callee takes *args). Calls with *a / **kw unpacking are counted as unknown and skipped, and the count
is printed. Last line: "signature_closure calls=<n> checked=<k> skipped_unpack=<u> mismatched=<m>"; exit 1 when m > 0.
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
    bad = []
    for mod, tree in mods.items():
        bound = {}
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom) and n.module and n.level == 0 and n.module in defs:
                for al in n.names:
                    if al.name in defs[n.module]:
                        bound[al.asname or al.name] = (n.module, al.name)
        for n in ast.walk(tree):
            if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in bound):
                continue
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
                    mod, n.lineno, src, fname, unknown, "; %d positional > %d" % (len(n.args), s["pos"]) if too_many else ""))
    for b in bad:
        print("MISMATCH: " + b)
    print("signature_closure calls=%d checked=%d skipped_unpack=%d mismatched=%d" % (calls, checked, skipped, len(bad)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
