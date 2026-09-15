"""CONTROL, not a criterion. Two reads over infra/aws/terraform.

(1) COVERAGE of the limb's Terraform reader against a DIFFERENT instrument: EN-t-1's census (its own tfscan.py), at the
census's own base fd9c9ca174 (file bytes read by git cat-file, not the worktree). Key = (file, line, tf type), restricted
to the limb's 30 types. Prints both denominators, the intersection, both one-sided sets, and the literal/expression split
(census value_claim 'measured' vs the limb's value is not None), and literal-value equality.

(2) THE ENFORCE EXPOSURE at this worktree's HEAD: every directory holding a tracked .tf file, run through the limb's own
run() and judge(); counts roots with >=1 REFUSE verdict, and the verdict totals.
"""
import collections
import importlib.machinery
import importlib.util
import json
import os
import re
import subprocess
import sys

BASE = "fd9c9ca174"


def load(path, name):
    loader = importlib.machinery.SourceFileLoader(name, path)
    spec = importlib.util.spec_from_loader(name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


nag = load(".tools/naming-apply-gate.py", "nag")
ng = load(".tools/naming-gate.py", "ng")
types = dict(ng.TF_NODE)
types.update(nag.NOT_GRADED_TYPES)
print("LIMB TYPES: %d" % len(types))

# ---- (1) coverage at the census base
ls = subprocess.run(["git", "ls-tree", "-r", "--name-only", BASE, "infra/aws/terraform"], capture_output=True, text=True, check=True)
files = [f for f in ls.stdout.splitlines() if f.endswith(".tf")]
p = subprocess.Popen(["git", "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
mine = {}
for f in files:
    p.stdin.write(("%s:%s\n" % (BASE, f)).encode())
    p.stdin.flush()
    hdr = p.stdout.readline().decode().split()
    size = int(hdr[2])
    body = p.stdout.read(size)
    p.stdout.read(1)
    text = body.decode("utf-8", errors="replace").replace("\r\n", "\n")
    rows, _mods = nag.read_tf(ng.scan, text, types)
    for r in rows:
        mine[(f, r["line"], r["tf_type"])] = r
p.stdin.close()
p.wait()
t = open("org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/TF_LABEL_CENSUS.md", encoding="utf-8").read()
d = json.loads(re.search(r"```json\n(.*?)\n```", t, re.S).group(1))
census = {(r["file"], r["line"], r["type"]): r for r in d["name_attributes"] if r["type"] in types}
both = set(mine) & set(census)
print("COVERAGE @%s: tracked .tf files read: %d  census rows (limb types): %d  limb rows: %d  both: %d  census-only: %d  limb-only: %d" % (
    BASE, len(files), len(census), len(mine), len(both), len(set(census) - set(mine)), len(set(mine) - set(census))))
for k in sorted(set(census) - set(mine))[:10]:
    print("  census-only: %s:%d %s %s=%r" % (k[0], k[1], k[2], census[k]["attribute"], census[k]["value"]))
for k in sorted(set(mine) - set(census))[:10]:
    print("  limb-only:   %s:%d %s %s expr=%r" % (k[0], k[1], k[2], mine[k]["attr"], mine[k]["expr"]))
split = collections.Counter()
diffval = []
for k in both:
    c_lit = census[k]["value_claim"].startswith("measured")
    m_lit = mine[k]["value"] is not None
    split[(c_lit, m_lit)] += 1
    if c_lit and m_lit and census[k]["value"] != mine[k]["value"]:
        diffval.append((k, census[k]["value"], mine[k]["value"]))
print("LITERAL SPLIT over both (census_literal, limb_literal): %s" % dict(split))
print("LITERAL VALUES THAT DIFFER: %d" % len(diffval))
for x in diffval[:5]:
    print("  %r" % (x,))

# ---- (2) enforce exposure at HEAD
ls = subprocess.run(["git", "ls-files", "infra/aws/terraform"], capture_output=True, text=True, check=True)
dirs = sorted({os.path.dirname(f) for f in ls.stdout.splitlines() if f.endswith(".tf")})
refused_roots, verdicts, graded_n, unres_n, mod_n = 0, collections.Counter(), 0, 0, 0
for dd in dirs:
    graded, unresolved, _n = nag.run(dd)
    graded_n += len(graded)
    unres_n += len(unresolved)
    mod_n += sum(1 for u in unresolved if u[2])
    for g in graded:
        verdicts[g[0] if g[0] != "REFUSE" else ("REFUSE-RAISE" if g[4] == nag.RAISE_CANON else "REFUSE-OOP-OR-ALIAS")] += 1
    if any(g[6] for g in graded):
        refused_roots += 1
print("EXPOSURE @HEAD: directories with a tracked .tf: %d  refused under ENFORCE: %d  name attributes: %d (graded %d, expressions %d, module-produced %d)" % (
    len(dirs), refused_roots, graded_n + unres_n, graded_n, unres_n, mod_n))
print("VERDICTS: %s" % dict(verdicts))
sys.exit(0)
