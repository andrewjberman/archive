#!/usr/bin/env python3
"""POSN_ASTTAX.TO-X1-1 / AT7-s-1 / X1-AC1 -- THE POSITIVE CONTROL.

The criterion's expect: "a scratch copy of the file with the tuple reduced to
two fields (or the SET clause given a fourth owned field) FAILS to import with
the assertion's message -- printed."

BOTH directions are run, because the assertion is an EQUALITY and each side can
break on its own:
  A. the guard NARROWER than the write  (tuple reduced to two fields)
  B. the guard WIDER   than the write   (SET clause given a fourth owned field)
plus C. the UNMUTATED bytes, which must import CLEANLY -- without C, "it
raised" would not distinguish a working assertion from a broken file.

SCRATCH COPIES ONLY. The working-tree file is never modified; no table of any
kind is opened; boto3 is never imported (the module only defines and asserts at
import, and this control never calls seed()).
"""
import importlib.util
import io
import os
import sys
import traceback

ROOT = os.getcwd()
REPO_PATH = "data/black_diamond/scripts/classification/seed_canonical_securities.py"
SCRATCH = os.path.join(ROOT, ".scratch")


def try_import(label, src, filename):
    path = os.path.join(SCRATCH, filename)
    io.open(path, "w", encoding="utf-8", newline="\n").write(src)
    name = "x1ac1_%s" % abs(hash(label))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    print("")
    print("-" * 100)
    print("  ARM: %s" % label)
    print("  scratch copy: %s (%d bytes)" % (path, len(src.encode("utf-8"))))
    try:
        spec.loader.exec_module(mod)
    except AssertionError as exc:
        print("  RESULT: AssertionError at import -- THE ASSERTION FIRED.")
        print("  ITS MESSAGE, verbatim:")
        for line in str(exc).splitlines():
            print("    %s" % line)
        tb = traceback.extract_tb(sys.exc_info()[2])[-1]
        print("  raised at %s:%d" % (os.path.basename(tb.filename), tb.lineno))
        return "FIRED"
    except Exception as exc:  # noqa: BLE001
        print("  RESULT: %s -- NOT the assertion: %s" % (type(exc).__name__, exc))
        return "OTHER:%s" % type(exc).__name__
    print("  RESULT: imported CLEANLY. owned=%r set=%r"
          % (mod.YANG_OWNED_FIELDS, mod.YANG_SET_FIELDS))
    return "CLEAN"


def main():
    src = io.open(os.path.join(ROOT, REPO_PATH), encoding="utf-8").read()
    print("=" * 100)
    print("X1-AC1 POSITIVE CONTROL -- CAN THE IMPORT-TIME ASSERTION ACTUALLY FIRE?")
    print("=" * 100)
    print("  subject: %s (%d bytes, working tree, UNMODIFIED by this control)"
          % (REPO_PATH, len(src.encode("utf-8"))))

    # ---- C: the unmutated bytes (the negative arm of the control) ----------
    c = try_import("C. UNMUTATED working-tree bytes -- must import CLEANLY",
                   src, "x1ac1_c_unmutated.py")

    # ---- A: the guard NARROWER than the write ------------------------------
    old_tuple = "YANG_OWNED_FIELDS = ('asset_class', 'sub_asset_class', 'name')"
    new_tuple = "YANG_OWNED_FIELDS = ('asset_class', 'sub_asset_class')"
    assert src.count(old_tuple) == 1, "tuple literal count %d" % src.count(old_tuple)
    a = try_import("A. TUPLE REDUCED to two fields (guard NARROWER than the write)",
                   src.replace(old_tuple, new_tuple), "x1ac1_a_narrow_tuple.py")

    # ---- B: the guard WIDER than the write ---------------------------------
    old_expr = "updated_by = :ub'"
    new_expr = "updated_by = :ub, management_style = :ms'"
    assert src.count(old_expr) == 1, "clause literal count %d" % src.count(old_expr)
    b = try_import("B. SET CLAUSE given a FOURTH owned field, management_style = :ms "
                   "(guard WIDER than the write)",
                   src.replace(old_expr, new_expr), "x1ac1_b_fourth_field.py")

    print("")
    print("=" * 100)
    print("  C unmutated        : %s   (expected CLEAN)" % c)
    print("  A narrower guard   : %s   (expected FIRED)" % a)
    print("  B wider  guard     : %s   (expected FIRED)" % b)
    ok = (c == "CLEAN" and a == "FIRED" and b == "FIRED")
    print("")
    if ok:
        print("  OK: the assertion DISCRIMINATES -- it fires on a divergence in EITHER")
        print("  direction and stays silent on the real bytes, 3 of 3 arms as expected.")
    else:
        print("  ERROR: the control does not discriminate. Report this, not the result.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
