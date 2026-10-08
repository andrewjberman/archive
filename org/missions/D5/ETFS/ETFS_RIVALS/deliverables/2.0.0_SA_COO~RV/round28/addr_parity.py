"""Compare every literal address()/name() call of the rivalfunds package at two pins.

Usage: python addr_parity.py <repo> <pinA> <pinB>
Each pin's lib/opal_naming.py + infra/logic/registry + org/standards are extracted with git archive into a temp dir,
imported in a fresh subprocess, and the harvested calls are evaluated. Prints the denominator and every difference.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import io
import tarfile

repo, pin_a, pin_b = sys.argv[1:4]
src_dir = os.path.join(repo, "data", "etfs", "scripts", "rivalfunds")

CALL = re.compile(r'\b(address|name)\(((?:\s*(?:f?"[^"]*"|\*?[A-Z0-9_]+)\s*,?)+)\)')
ARG = re.compile(r'(f?)"([^"]*)"|(\*?[A-Z0-9_]+)')
calls = set()
consts = {}
for root, dirs, files in os.walk(src_dir):
    if "tests" in root.split(os.sep):
        continue
    for f in files:
        if not f.endswith(".py"):
            continue
        text = open(os.path.join(root, f), encoding="utf-8").read()
        for m in re.finditer(r'^([A-Z0-9_]+)\s*=\s*(\(.*?\)|"[^"]*")\s*$', text, re.M):
            consts.setdefault(m.group(1), m.group(2))
        for m in CALL.finditer(text):
            calls.add((m.group(1), m.group(2)))


def resolve(argtext):
    out = []
    for fm, s, ident in ARG.findall(argtext):
        if ident:
            star = ident.startswith("*")
            key = ident.lstrip("*")
            v = consts.get(key)
            if v is None:
                return None
            if v.startswith("("):
                vals = re.findall(r'"([^"]*)"', v)
                out.extend(vals if star else [tuple(vals)])
            else:
                out.append(v.strip('"'))
        else:
            if fm:
                s = re.sub(r"\{[^}]*\}", "X", s)
                s = s.replace("date=X", "date=2026-10-09")
            out.append(s)
    return out


resolved = []
for kind, argtext in sorted(calls):
    args = resolve(argtext)
    if args is None or any(isinstance(a, tuple) for a in args):
        continue
    resolved.append((kind, args))

RUNNER = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
from lib import opal_naming as on
calls = json.loads(open(sys.argv[2]).read())
res = []
for kind, args in calls:
    try:
        res.append(["OK", getattr(on, kind)(*args)])
    except BaseException as e:
        res.append(["ERR", type(e).__name__ + ": " + str(e)[:160]])
print(json.dumps(res))
'''


def run(pin, calls_path, runner_path):
    d = tempfile.mkdtemp(prefix="addr_" + pin[:8] + "_")
    tar = subprocess.run(["git", "-C", repo, "archive", pin, "lib/opal_naming.py", "lib/__init__.py",
                          "infra/logic/registry", "org/standards"], capture_output=True)
    if tar.returncode != 0:
        tar = subprocess.run(["git", "-C", repo, "archive", pin, "lib/opal_naming.py", "infra/logic/registry",
                              "org/standards"], capture_output=True)
    if tar.returncode != 0:
        sys.exit("git archive failed at %s: %s" % (pin, tar.stderr.decode(errors="replace")))
    tarfile.open(fileobj=io.BytesIO(tar.stdout)).extractall(d)
    if not os.path.exists(os.path.join(d, "lib", "__init__.py")):
        open(os.path.join(d, "lib", "__init__.py"), "w").close()
    p = subprocess.run([sys.executable, "-I", runner_path, d, calls_path], capture_output=True, text=True,
                       encoding="utf-8", cwd=d)
    if p.returncode != 0:
        sys.exit("runner failed at %s: %s" % (pin, p.stderr[-800:]))
    return json.loads(p.stdout.strip().splitlines()[-1])


tmp = tempfile.mkdtemp(prefix="addr_par_")
cp = os.path.join(tmp, "calls.json")
rp = os.path.join(tmp, "runner.py")
open(cp, "w").write(json.dumps(resolved))
open(rp, "w").write(RUNNER)
ra = run(pin_a, cp, rp)
rb = run(pin_b, cp, rp)
print("harvested calls: %d distinct literal call sites, %d resolved to literal args" % (len(calls), len(resolved)))
print("pin A %s: OK %d, ERR %d" % (pin_a, sum(r[0] == "OK" for r in ra), sum(r[0] == "ERR" for r in ra)))
print("pin B %s: OK %d, ERR %d" % (pin_b, sum(r[0] == "OK" for r in rb), sum(r[0] == "ERR" for r in rb)))
diff = 0
for (kind, args), a, b in zip(resolved, ra, rb):
    if a != b:
        diff += 1
        print("DIFF", kind, args, "\n  A:", a, "\n  B:", b)
print("differences: %d of %d" % (diff, len(resolved)))
for (kind, args), b in zip(resolved, rb):
    if b[0] == "OK":
        print("  sample", kind, args, "->", b[1])
        break
