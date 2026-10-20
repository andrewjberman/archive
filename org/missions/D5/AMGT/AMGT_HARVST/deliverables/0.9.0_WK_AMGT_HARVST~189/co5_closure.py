"""HVST-co-5: the import closure of lib.research.harvest.gold_refresh (the gold chatter rebuild driver), measured per
package. Method as HVST-cn-4 (cn4_closure.py, deliverables 0.9.0_WK_AMGT_HARVST~181): the real import runs in a clean
child process under a builtins.__import__ hook that records, for every module newly loaded, the module whose import
statement loaded it. Sizes are the installed size of each third-party distribution. Changes nothing outside the
child's scratch file. Run from the repo root of the worktree:
    python -u <this file> > <this file's folder>/co5_closure.out
"""
import ast
import importlib.metadata as im
import io
import os
import subprocess
import sys

MIB = 1024 * 1024
LIMIT_BYTES = 250 * MIB
DRIVER = "lib.research.harvest.gold_refresh"
POSITIVE = "lib.research.harvest.store"
NEGATIVE = "json"

CHILD = r'''
import builtins, sys
root, target, out = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, root)
_orig = builtins.__import__
importer_of = {}
def _hook(name, globals=None, locals=None, fromlist=(), level=0):
    try:
        caller = sys._getframe(1).f_globals.get("__name__", "?")
    except Exception:
        caller = "?"
    before = set(sys.modules)
    try:
        return _orig(name, globals, locals, fromlist, level)
    finally:
        for k in list(sys.modules):
            if k not in before and k not in importer_of:
                importer_of[k] = caller
builtins.__import__ = _hook
err = None
try:
    exec("import " + target, {"__name__": "__closure_driver__"})
except BaseException as e:
    err = type(e).__name__ + ": " + str(e)[:300]
mods = []
for k, caller in importer_of.items():
    f = getattr(sys.modules.get(k), "__file__", None)
    mods.append([k, f, caller])
import json  # imported only after the measured import, so the json control is not pre-loaded
with open(out, "w", encoding="utf-8") as fh:
    json.dump({"target": target, "error": err, "modules": mods}, fh)
'''

STDLIB = set(sys.stdlib_module_names)


def is_third(top):
    return top not in STDLIB and not top.startswith("_") and top != "lib"


def run_child(root, target):
    scratch = os.path.join(root, ".scratch")
    os.makedirs(scratch, exist_ok=True)
    out = os.path.join(scratch, "co5_" + target.replace(".", "_") + ".json")
    if os.path.exists(out):
        os.remove(out)
    p = subprocess.run(
        [sys.executable, "-u", "-W", "ignore", "-c", CHILD, root, target, out],
        cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if p.returncode != 0 or not os.path.exists(out):
        return None, "child rc=%s stderr_tail=%s" % (p.returncode, p.stderr[-600:].replace("\n", " | "))
    import json
    with open(out, encoding="utf-8") as fh:
        data = json.load(fh)
    if data.get("error"):
        return None, "import error: " + data["error"]
    return data, ""


def static_tops(path):
    """Third-party top-level names imported at module top level (tl) and only inside functions (lz)."""
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read(), filename=path)
    tl, lz = set(), set()

    def names_of(node):
        if isinstance(node, ast.Import):
            return [a.name.split(".")[0] for a in node.names]
        if isinstance(node, ast.ImportFrom):
            if node.level or not node.module:
                return []
            return [node.module.split(".")[0]]
        return []

    def visit(node, in_func):
        for child in ast.iter_child_nodes(node):
            f = in_func or isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))
            if isinstance(child, (ast.Import, ast.ImportFrom)):
                for t in names_of(child):
                    if is_third(t):
                        (lz if f else tl).add(t)
            visit(child, f)

    visit(tree, False)
    lz -= tl
    return tl, lz


def first_lib(top, importer_of):
    """Walk the recorded importer chain from a package upward to the first lib module."""
    seen = set()
    cur = importer_of.get(top)
    while cur and cur not in seen:
        seen.add(cur)
        if cur == "lib" or cur.startswith("lib."):
            return cur
        cur = importer_of.get(cur.split(".")[0])
    return "NONE"


def dist_size(dname, cache):
    if dname not in cache:
        d = im.distribution(dname)
        total, n = 0, 0
        for f in (d.files or []):
            try:
                p = f.locate()
            except Exception:
                continue
            if p.is_file():
                total += p.stat().st_size
                n += 1
        cache[dname] = (total, n, d.version)
    return cache[dname]


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n", write_through=True)
    root = os.getcwd()
    if not os.path.isfile(os.path.join(root, "lib", "research", "harvest", "gold_refresh.py")):
        print("ERROR: run from the repo root of the worktree (gold_refresh.py not under cwd)")
        return 2

    data, why = run_child(root, DRIVER)
    if data is None:
        print("ERROR: driver import did not measure: " + why)
        return 1
    mods = data["modules"]  # [name, file, importer] in load order
    importer_of = {n: imp for n, _f, imp in mods}
    lib_mods = sorted((n, f) for n, f, _i in mods if n.startswith("lib."))
    tops = sorted({n.split(".")[0] for n, _f, _i in mods if is_third(n.split(".")[0])})
    detail = ["CLOSURE-IMPORTED target=%s modules=%d lib_modules=%d third_party_tops=%d"
              % (DRIVER, len(mods), len(lib_mods), len(tops))]

    static_all = {}
    for n, f, _i in mods:
        if f and f.endswith(".py") and os.path.isfile(f):
            try:
                static_all[n] = static_tops(f)
            except SyntaxError as e:
                detail.append("NOTE static parse failed name=%s err=%s" % (n, e))

    pkg_dists = im.packages_distributions()
    dcache = {}
    rows = []
    for t in tops:
        dl = sorted(pkg_dists.get(t, []))
        if dl:
            dname = dl[0]
            size, nfiles, ver = dist_size(dname, dcache)
        else:
            dname, size, nfiles, ver = "NONE", 0, 0, "NONE"
            tfile = next((f for n, f, _i in mods if n == t), None)
            detail.append("NOTE no-distribution top=%s file=%s" % (t, tfile))
        rows.append((size, t, dname, ver, nfiles, first_lib(t, importer_of), importer_of.get(t, "NONE")))
    rows.sort(key=lambda r: (-r[0], r[1]))
    for size, t, dname, ver, nfiles, fl, via in rows:
        detail.append("PKG %s dist=%s version=%s mb=%.2f files=%d first_lib_importer=%s via=%s"
                      % (t, dname, ver, size / MIB, nfiles, fl, via))
    dist_bytes = {}
    for size, t, dname, ver, nfiles, fl, via in rows:
        if dname != "NONE":
            dist_bytes[dname] = size
    third_party_bytes = sum(dist_bytes.values())

    lib_code_bytes = 0
    for n, f in lib_mods:
        if f and f.endswith(".py") and os.path.isfile(f):
            lib_code_bytes += os.path.getsize(f)
        tl, lz = static_all.get(n, (set(), set()))
        detail.append("LIBIMPORT %s top=%s lazy=%s" % (n, ",".join(sorted(tl)) or "none", ",".join(sorted(lz)) or "none"))

    removable = []
    for t in tops:
        top_imp = [n for n, (tl, _lz) in static_all.items() if t in tl]
        lazy_imp = [n for n, (_tl, lz) in static_all.items() if t in lz]
        if lazy_imp and not top_imp:
            removable.append(t)

    total_bytes = lib_code_bytes + third_party_bytes
    verdict = "UNDER" if total_bytes <= LIMIT_BYTES else "OVER"
    biggest = sorted(dist_bytes.items(), key=lambda kv: (-kv[1], kv[0]))[:3]

    # Controls, printed FIRST.
    pos, pos_why = run_child(root, POSITIVE)
    if pos is None:
        print("CONTROL-POSITIVE target=%s pyarrow_in_closure=unmeasured reason=%s" % (POSITIVE, pos_why))
    else:
        has = any(n.split(".")[0] == "pyarrow" for n, _f, _i in pos["modules"])
        print("CONTROL-POSITIVE target=%s pyarrow_in_closure=%s" % (POSITIVE, "yes" if has else "no"))
    neg, neg_why = run_child(root, NEGATIVE)
    if neg is None:
        print("CONTROL-NEGATIVE target=%s third_party_tops=unmeasured reason=%s" % (NEGATIVE, neg_why))
    else:
        neg_tops = {n.split(".")[0] for n, _f, _i in neg["modules"] if is_third(n.split(".")[0])}
        print("NOTE control-negative json newly_loaded=%d" % len(neg["modules"]))
        print("CONTROL-NEGATIVE target=%s third_party_tops=%d" % (NEGATIVE, len(neg_tops)))

    print("GOLD-DRIVER-CLOSURE entry=%s lib_modules=%d third_party_pkgs=%d third_party_mb=%.2f lib_code_mb=%.2f "
          "total_mb=%.2f limit_unzipped_mb=250 verdict=%s biggest=%s removable_by_lazy=%s"
          % (DRIVER, len(lib_mods), len(dist_bytes), third_party_bytes / MIB, lib_code_bytes / MIB,
             total_bytes / MIB, verdict,
             ",".join("%s:%.2f" % (n, s / MIB) for n, s in biggest) or "none",
             ",".join(removable) or "none"))
    print("NOTE measured by the import hook in a child process; sizes are the installed distributions "
          "(cn4 method, unchanged)")
    for line in detail:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
