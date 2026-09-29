"""uu-4 step 2 -- THE CLOSURE DIFF against the deployed BUILD INPUT, and the four stop limbs the
halves let me grade before the upload (limb 5 is graded on OUTPUT, pre/post apply, not here).

Both halves' limbs, verbatim:
 (1) the closure diff names a file beyond lib/research/api/case_rule.py (ADDED),
     lib/research/api/scoped_amgt.py, lib/research/print/render_pack.py
 (2) build_pack changed
 (3) in scoped_amgt.py, any function beyond _model_cases (and the new import) changed
 (4) in render_pack.py, any function beyond _model_case_line changed

Every verdict carries a denominator on BOTH sides, and every identity verdict carries a PLANTED
MUTATION control that must FIRE -- because "nothing changed" and "an extractor that found nothing"
read identically.
usage: python step2_closure_diff.py <deployed.zip> <fresh.zip>
"""
import ast
import hashlib
import sys
import zipfile

ALLOWED = {
    "lib/research/api/case_rule.py": "added",
    "lib/research/api/scoped_amgt.py": "changed",
    "lib/research/print/render_pack.py": "changed",
}
LIMB3_FN = "_model_cases"
LIMB4_FN = "_model_case_line"
LIMB2_FN = "build_pack"


def members(path):
    with zipfile.ZipFile(path) as z:
        return {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}


def source(path, arc):
    with zipfile.ZipFile(path) as z:
        return z.read(arc).decode("utf-8")


def defs(src):
    """arcname-independent map: qualified function name -> sha256 of its source segment."""
    tree = ast.parse(src)
    out = {}

    def walk(node, prefix):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = prefix + child.name
                seg = ast.get_source_segment(src, child) or ""
                out[name] = hashlib.sha256(seg.encode("utf-8")).hexdigest()
                walk(child, name + ".")
            elif isinstance(child, ast.ClassDef):
                walk(child, prefix + child.name + ".")

    walk(tree, "")
    return out


def module_level(src):
    """sha of the module-level statements that are NOT function/class defs (imports live here)."""
    tree = ast.parse(src)
    stmts = [ast.dump(n) for n in tree.body
             if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
    return hashlib.sha256("\n".join(stmts).encode("utf-8")).hexdigest(), len(stmts)


def fn_diff(old_src, new_src):
    a, b = defs(old_src), defs(new_src)
    changed = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    return changed, sorted(set(b) - set(a)), sorted(set(a) - set(b)), len(a), len(b)


def control_fires(src, fn, label):
    """Plant a mutation INSIDE fn and assert the extractor reports exactly that function changed."""
    base = defs(src)
    if fn not in base:
        print("    CONTROL %s: *** function %s not found -- extractor is aimed at the wrong object ***" % (label, fn))
        return False
    tree = ast.parse(src)
    target = None
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == fn.split(".")[-1]:
            target = node
            break
    lines = src.splitlines(True)
    ins = target.body[0].lineno - 1
    indent = " " * (target.body[0].col_offset)
    mutated = "".join(lines[:ins]) + indent + "_planted_control_marker = 1\n" + "".join(lines[ins:])
    mut = defs(mutated)
    fired = fn in mut and mut[fn] != base[fn]
    others = [k for k in set(base) & set(mut) if base[k] != mut[k] and k != fn]
    print("    CONTROL %s: planted a statement inside %s -> extractor %s%s"
          % (label, fn, "FIRED" if fired else "*** DID NOT FIRE ***",
             (" (and reported %d other function(s) moved: %s)" % (len(others), others)) if others else ""))
    return fired


dep_path, fresh_path = sys.argv[1], sys.argv[2]
dep, fresh = members(dep_path), members(fresh_path)

added = sorted(set(fresh) - set(dep))
removed = sorted(set(dep) - set(fresh))
changed = sorted(k for k in set(dep) & set(fresh) if dep[k] != fresh[k])
same = sorted(k for k in set(dep) & set(fresh) if dep[k] == fresh[k])

print("CLOSURE DIFF -- denominator printed on BOTH sides")
print("  deployed artifact : %d members (%s)" % (len(dep), dep_path))
print("  fresh artifact    : %d members (%s)" % (len(fresh), fresh_path))
print("  added %d | removed %d | CHANGED %d | same %d   (sums to %d of %d fresh)"
      % (len(added), len(removed), len(changed), len(same), len(added) + len(changed) + len(same), len(fresh)))
for a in added:
    print("    ADDED   %s" % a)
for r in removed:
    print("    REMOVED %s" % r)
for c in changed:
    print("    CHANGED %s  (%s -> %s)" % (c, dep[c][:16], fresh[c][:16]))

verdicts = {}

# ---- LIMB 1 -------------------------------------------------------------------------------------
moved = set(added) | set(removed) | set(changed)
beyond = sorted(moved - set(ALLOWED))
print("\nLIMB 1 -- no file beyond the three the halves name")
print("  moved set (%d): %s" % (len(moved), sorted(moved)))
print("  the halves allow: %s" % sorted(ALLOWED))
print("  BEYOND the allowed set (%d): %s" % (len(beyond), beyond))
wrong_dir = [a for a in added if ALLOWED.get(a) != "added"] + [c for c in changed if ALLOWED.get(c) != "changed"]
print("  moved in a direction the halves did not name (%d): %s" % (len(wrong_dir), wrong_dir))
verdicts["limb1"] = not beyond and not removed and not wrong_dir
print("  LIMB 1: %s" % ("CLEAR" if verdicts["limb1"] else "*** HIT -- STOP ***"))

# ---- LIMB 2: build_pack ------------------------------------------------------------------------
print("\nLIMB 2 -- build_pack (the pdf path) did not change")
rp_old, rp_new = source(dep_path, "lib/research/print/render_pack.py"), source(fresh_path, "lib/research/print/render_pack.py")
d_old, d_new = defs(rp_old), defs(rp_new)
bp_same = d_old.get(LIMB2_FN) == d_new.get(LIMB2_FN) and LIMB2_FN in d_old
print("  build_pack present in both: %s | deployed %s | fresh %s"
      % (LIMB2_FN in d_old and LIMB2_FN in d_new, (d_old.get(LIMB2_FN) or "ABSENT")[:16], (d_new.get(LIMB2_FN) or "ABSENT")[:16]))
c2 = control_fires(rp_new, LIMB2_FN, "limb2")
verdicts["limb2"] = bp_same and c2
print("  LIMB 2: %s" % ("CLEAR (byte-identical, on a controlled extractor)" if verdicts["limb2"] else "*** HIT -- STOP ***"))

# ---- LIMB 3: scoped_amgt.py ---------------------------------------------------------------------
print("\nLIMB 3 -- in scoped_amgt.py only %s (and the new import) moved" % LIMB3_FN)
sa_old, sa_new = source(dep_path, "lib/research/api/scoped_amgt.py"), source(fresh_path, "lib/research/api/scoped_amgt.py")
ch3, add3, rem3, n3o, n3n = fn_diff(sa_old, sa_new)
ml_o, nso = module_level(sa_old)
ml_n, nsn = module_level(sa_new)
print("  functions: deployed %d, fresh %d | CHANGED %d %s | added %s | removed %s" % (n3o, n3n, len(ch3), ch3, add3, rem3))
print("  module-level statements: deployed %d, fresh %d -> %s"
      % (nso, nsn, "IDENTICAL" if ml_o == ml_n else "MOVED (the halves license the new import)"))
extra3 = [c for c in ch3 if c != LIMB3_FN] + add3 + rem3
print("  beyond %s (%d): %s" % (LIMB3_FN, len(extra3), extra3))
c3 = control_fires(sa_new, LIMB3_FN, "limb3")
verdicts["limb3"] = not extra3 and LIMB3_FN in ch3 and c3
print("  LIMB 3: %s" % ("CLEAR" if verdicts["limb3"] else "*** HIT -- STOP ***"))

# ---- LIMB 4: render_pack.py ---------------------------------------------------------------------
print("\nLIMB 4 -- in render_pack.py only %s moved" % LIMB4_FN)
ch4, add4, rem4, n4o, n4n = fn_diff(rp_old, rp_new)
ml4o, ns4o = module_level(rp_old)
ml4n, ns4n = module_level(rp_new)
print("  functions: deployed %d, fresh %d | CHANGED %d %s | added %s | removed %s" % (n4o, n4n, len(ch4), ch4, add4, rem4))
print("  module-level statements: deployed %d, fresh %d -> %s" % (ns4o, ns4n, "IDENTICAL" if ml4o == ml4n else "MOVED"))
extra4 = [c for c in ch4 if c != LIMB4_FN] + add4 + rem4
print("  beyond %s (%d): %s" % (LIMB4_FN, len(extra4), extra4))
c4 = control_fires(rp_new, LIMB4_FN, "limb4")
verdicts["limb4"] = not extra4 and LIMB4_FN in ch4 and c4
print("  LIMB 4: %s" % ("CLEAR" if verdicts["limb4"] else "*** HIT -- STOP ***"))

print("\n==== VERDICT ON THE FOUR LIMBS GRADED HERE ====")
for k in ("limb1", "limb2", "limb3", "limb4"):
    print("  %s: %s" % (k, "CLEAR" if verdicts[k] else "HIT"))
print("  limb5: graded on OUTPUT (served /print pdf) pre vs post apply -- NOT here")
ok = all(verdicts.values())
print("\n%s" % ("ALL FOUR CLEAR -- the upload may proceed" if ok else "*** A LIMB WAS HIT -- REFUSE, print, stop, report ***"))
sys.exit(0 if ok else 1)
