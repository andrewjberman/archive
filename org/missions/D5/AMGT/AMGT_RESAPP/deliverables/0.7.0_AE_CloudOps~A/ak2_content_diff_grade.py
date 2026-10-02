"""AMGT-ak-2 -- grade the packaged CONTENT-DIFF as a SET, independently of the build
script's own summary line.

The CTO half's condition 1 says the content-diff must read CHANGED 3 with exactly three
named files. The build script PRINTS that summary itself, so reading it back is the tool
describing itself. This recomputes the diff from the two artifacts: the zip just built and
the artifact version the live function runs now. Set equality is checked BOTH WAYS -- a
file changed but not listed, and a file listed but unmoved, are different defects and
either one is a STOP.

  --built <zip>  --deployed <zip>  [--out <json>]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile

EXPECT_CHANGED = {
    "lib/research/api/scoped_amgt.py",
    "lib/research/api/monthly_chatter.py",
    "org/standards/NAMING_SCHEMA.json",
}
# A path that is not in either artifact. If this reads "packaged", the grader is broken.
FABRICATED = "lib/research/api/zzz_no_such_module_9999.py"


def members(path):
    with zipfile.ZipFile(path) as z:
        return {n: hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if not n.endswith("/")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--built", required=True)
    ap.add_argument("--deployed", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()

    new, old = members(a.built), members(a.deployed)
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    common = set(new) & set(old)
    changed = sorted(k for k in common if new[k] != old[k])
    identical = sorted(k for k in common if new[k] == old[k])

    print("INDEPENDENT CONTENT-DIFF (recomputed from both artifacts, not read off any summary line)")
    print("  packaged DENOMINATOR: built %d member(s), deployed %d member(s)" % (len(new), len(old)))
    print("  IDENTICAL %d  CHANGED %d  ADDED %d  REMOVED %d" % (len(identical), len(changed), len(added), len(removed)))
    for c in changed:
        print("    CHANGED  %s" % c)
    for c in added:
        print("    ADDED    %s" % c)
    for c in removed:
        print("    REMOVED  %s" % c)

    got = set(changed)
    extra = sorted(got - EXPECT_CHANGED)        # changed but NOT signed for -- a STOP
    missing = sorted(EXPECT_CHANGED - got)      # signed for but unmoved -- also a STOP
    print("  SET EQUALITY, BOTH WAYS, against the halves' three signed files:")
    print("    changed-but-not-signed : %d %s" % (len(extra), extra))
    print("    signed-but-unmoved     : %d %s" % (len(missing), missing))
    print("  CONTROL fabricated path %s: %s" % (FABRICATED, "packaged -- GRADER BROKEN"
                                                if FABRICATED in new else "not packaged (grader discriminates)"))

    verdict = (not extra) and (not missing) and (not added) and (not removed) and len(changed) == 3
    print("CONTENT-DIFF VERDICT: %s" % ("PASS -- exactly the three signed files moved"
                                        if verdict else "STOP -- the package diff is not the signed diff"))
    if a.out:
        json.dump({"built_members": len(new), "deployed_members": len(old),
                   "identical": len(identical), "changed": changed, "added": added, "removed": removed,
                   "changed_but_not_signed": extra, "signed_but_unmoved": missing,
                   "fabricated_control_packaged": FABRICATED in new, "verdict": verdict},
                  open(a.out, "w", encoding="utf-8"), indent=1, sort_keys=True)
    return 0 if verdict else 1


if __name__ == "__main__":
    raise SystemExit(main())
