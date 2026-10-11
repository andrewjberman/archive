"""ADVI_FIRMBKTS round 4 check for cell FB-g-24 (the opal_name module exposes a scope's canonical CLASS PREFIXES, rendered by
the builder, so a grant on a served class's directory is generated, never typed; the CTO's act-0 CTO half ADDENDUM 1),
issuer 2.0.0_SA_COO~B1.

--arms module [--root <tree>] [--base <ref>]  (5 arms)
  M1 generated_locals.tf carries a `class_prefix` local (scope long form -> a map from each REGISTERED destination class's
     legacy prefix to its canonical directory prefix, ending /) and main.tf declares an output `class_prefix` keyed on
     var.scope (null for no scope).
  M2 each entry equals the producers' seam's canonical destination of the class's legacy prefix (the directory of
     destination(legacy_prefix + "x")) and sits under that scope's platinum prefix; every registered class is present
     (the count of classes is printed).
  M3 `terraform test` passes in the module folder (PASS with a printed note where terraform is absent).
  M4 DORMANT: against the base, generated_locals.tf and main.tf keep every base line in order (mark lines excepted) and no
     other module file changes.
  M5 the committed generated_locals.tf is the builder's output, and `lib/opal_naming.py validate` exits 0.
Plain ASCII output; the last line carries the arm count. Never edit this file.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

MOD = "infra/aws/terraform/modules/opal_name"
GL = MOD + "/generated_locals.tf"
MAIN = MOD + "/main.tf"


def _git(root, *a):
    return subprocess.run(["git", "-C", root] + list(a), capture_output=True, text=True, encoding="utf-8",
                          errors="replace")


def _root(arg):
    if arg:
        return arg
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _base(root, arg):
    if arg:
        return arg
    wl = _git(root, "worktree", "list", "--porcelain").stdout.split("\n")
    primary = next((ln.split()[1] for ln in wl if ln.startswith("HEAD ")), "")
    return _git(root, "merge-base", "HEAD", primary).stdout.strip()


def _kept(old_lines, new_lines):
    i = 0
    for ln in new_lines:
        if i < len(old_lines) and ln == old_lines[i]:
            i += 1
    return i


def _map(text, name):
    m = re.search(r"%s\s*=\s*\{(.*?)\n\s*\}" % name, text, re.S)
    return dict(re.findall(r'"([^"]+)"\s*=\s*"([^"]*)"', m.group(1))) if m else {}


def _class_map(text):
    """The nested map of the class_prefix local: {scope: {legacy_prefix: canonical_dir}}."""
    start = re.search(r"^\s*class_prefix\s*=\s*\{", text, re.M)
    if not start:
        return {}
    depth, i, body = 1, start.end(), []
    while i < len(text) and depth:
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        if depth:
            body.append(ch)
        i += 1
    out = {}
    for sm in re.finditer(r'"([^"]+)"\s*=\s*\{(.*?)\}', "".join(body), re.S):
        out[sm.group(1)] = dict(re.findall(r'"([^"]+)"\s*=\s*"([^"]*)"', sm.group(2)))
    return out


def module(root, base):
    res = []
    gl = open(os.path.join(root, *GL.split("/")), encoding="utf-8").read()
    mn = open(os.path.join(root, *MAIN.split("/")), encoding="utf-8").read()
    has_local = re.search(r"^\s*class_prefix\s*=", gl, re.M) is not None
    has_out = re.search(r'output\s+"class_prefix"\s*\{', mn) is not None and "var.scope" in mn
    print("  local class_prefix=%s output class_prefix=%s" % (has_local, has_out))
    res.append(("M1 the module carries the class_prefix local and output", has_local and has_out))

    sys.path.insert(0, os.path.join(root, "lib"))
    sys.path.insert(0, os.path.join(root, "data", "black_diamond", "scripts", "gold"))
    import opal_naming  # noqa: E402
    from lib import platinum_dest as pd  # noqa: E402
    reg = opal_naming._registry()
    classes = reg["platinum_destinations"]["platinum_destinations"]
    expect = {}
    for c in classes:
        d = pd.destination(c["legacy_prefix"] + "x", "canonical")[1]
        expect.setdefault(c["scope"], {})[c["legacy_prefix"]] = d[:-1]
    got = _class_map(gl)
    pref = _map(gl, "platinum_prefix")
    ok2 = bool(expect) and got == expect and all(
        v.startswith(pref.get(sc, "\0")) and v.endswith("/") for sc, cm in got.items() for v in cm.values())
    print("  classes=%d got=%s" % (sum(len(v) for v in got.values()), "equal" if got == expect else got))
    res.append(("M2 every registered class maps to its canonical directory under the scope's platinum prefix", ok2))

    tf = shutil.which("terraform")
    if tf:
        modp = os.path.join(root, *MOD.split("/"))
        subprocess.run([tf, "init", "-backend=false", "-input=false", "-no-color"], cwd=modp, capture_output=True,
                       text=True, timeout=110)
        r = subprocess.run([tf, "test", "-no-color"], cwd=modp, capture_output=True, text=True, timeout=110)
        print("  terraform test rc=%d: %s" % (r.returncode, (r.stdout.strip().splitlines() or [""])[-1][:100]))
        ok3 = r.returncode == 0
    else:
        print("  terraform not on PATH: test arm skipped")
        ok3 = True
    res.append(("M3 terraform test passes in the module folder", ok3))

    ok4 = True
    for f in (GL, MAIN):
        old = [ln for ln in _git(root, "show", "%s:%s" % (base, f)).stdout.splitlines()
               if "GENERATED by lib/opal_naming.py" not in ln]
        new = [ln for ln in open(os.path.join(root, *f.split("/")), encoding="utf-8").read().splitlines()
               if "GENERATED by lib/opal_naming.py" not in ln]
        k = _kept(old, new)
        print("  %s: base lines kept in order %d of %d" % (f, k, len(old)))
        ok4 = ok4 and k == len(old)
    changed = _git(root, "diff", "--name-only", base, "HEAD", "--", MOD).stdout.split()
    changed += _git(root, "diff", "--name-only", "HEAD", "--", MOD).stdout.split()
    others = sorted({c for c in changed if c not in (GL, MAIN)})
    print("  other module files changed: %s" % others)
    res.append(("M4 dormant: the base's lines are all kept in order and no other module file changes",
                ok4 and not others))

    code = ("import sys; sys.path.insert(0,'lib'); import opal_naming as n; n.generate(sys.argv[1], ['%s']); "
            "print('done')" % GL)
    with tempfile.TemporaryDirectory() as td:
        g = subprocess.run([sys.executable, "-c", code, td], cwd=root, capture_output=True, text=True, timeout=120)
        gp = os.path.join(td, *GL.split("/"))
        gen = open(gp, encoding="utf-8").read() if os.path.isfile(gp) else None
    val = subprocess.run([sys.executable, "lib/opal_naming.py", "validate"], cwd=root, capture_output=True,
                         text=True, timeout=100)
    print("  generate rc=%d in sync=%s; validate rc=%d" % (g.returncode, gen == gl, val.returncode))
    res.append(("M5 the committed generated_locals.tf is the builder's output and validate exits 0",
                g.returncode == 0 and gen == gl and val.returncode == 0))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("module",), required=True)
    ap.add_argument("--root")
    ap.add_argument("--base")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        res = module(root, _base(root, a.base))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: %s (%s: %s)" % (MOD, type(e).__name__, str(e)[:160]))
        res = [("the module readable at the tree and the base", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 MODULE CLASSES: %d of 5 arms" % n)
    sys.exit(0 if n == 5 else 1)


if __name__ == "__main__":
    main()
