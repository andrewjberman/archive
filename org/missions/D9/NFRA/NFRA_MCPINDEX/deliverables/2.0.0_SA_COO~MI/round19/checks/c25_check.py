"""c25_check.py -- grades MX-c-25 (the gold book catalog entry drops its stale `open_items` line: the gateway role CAN read gold/book), from the repo root.

  python c25_check.py ac1   against BASE_REF the catalog entries differ in exactly ONE file, workflows/atom_decomposition/catalog_entries/opal_data_etfs_gold_book.yaml;
                            in it exactly the stale open_items item (the one naming `implicitDeny` on gold/book) is gone, no line is added, and the other open_items item is byte-equal
  python c25_check.py ac2   the entry still validates: validate_catalog_v02.py prints OK for opal_data_etfs_gold_book and no FAIL line anywhere

The tree is the worktree (or C25_ROOT, a planted tree). Exit 0 PASS, 1 FAIL, 9 no run.
"""
import os
import subprocess
import sys

import yaml

BASE_REF = "0afc0f3a19"
ROOT = os.environ.get("C25_ROOT") or "."
ENT = "workflows/atom_decomposition/catalog_entries"
ONE = ENT + "/opal_data_etfs_gold_book.yaml"
STALE = "implicitDeny"


def git(*args):
    r = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        print("ERROR: git %s rc %d: %s" % (" ".join(args), r.returncode, r.stderr[-200:]))
        sys.exit(9)
    return r.stdout.replace("\r", "")


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok  " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def ac1():
    files = [ln for ln in git("diff", "--name-only", BASE_REF, "--", ENT).splitlines() if ln.strip()]
    print("DENOMINATOR catalog entry files differing from %s: %d (%s)" % (BASE_REF, len(files), ", ".join(files) or "none"))
    res = [("exactly one entry file differs, the gold book one", files == [ONE])]
    base = yaml.safe_load(git("show", "%s:%s" % (BASE_REF, ONE)))
    now = yaml.safe_load(open(os.path.join(ROOT, ONE), encoding="utf-8"))
    bo, no = base.get("open_items") or [], now.get("open_items") or []
    gone = [x for x in bo if STALE in str(x) and "gold/book" in str(x)]
    kept = [x for x in bo if x not in gone]
    print("DENOMINATOR open_items at base %d (stale %d); now %d" % (len(bo), len(gone), len(no)))
    res.append(("the base holds exactly one stale item naming %s on gold/book" % STALE, len(gone) == 1))
    res.append(("the stale item is gone and the other items are byte-equal and in order", no == kept and len(no) == len(bo) - 1))
    other = [k for k in base if k != "open_items" and base[k] != now.get(k)] + [k for k in now if k not in base]
    res.append(("no other field of the entry changed (%d changed)" % len(other), not other))
    added = [ln for ln in git("diff", "-U0", BASE_REF, "--", ONE).splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    res.append(("no line is added (%d added)" % len(added), not added))
    return report(res)


def ac2():
    r = subprocess.run([sys.executable, "workflows/atom_decomposition/validate_catalog_v02.py"], cwd=ROOT, capture_output=True, text=True, timeout=250)
    out = (r.stdout or "").replace("\r", "")
    ok_line = [ln for ln in out.splitlines() if "opal_data_etfs_gold_book" in ln and ln.strip().startswith("OK")]
    bad = [ln for ln in out.splitlines() if ln.strip().startswith(("FAIL", "ERROR"))]
    print("DENOMINATOR validator rc %d; gold book OK lines %d; FAIL lines %d" % (r.returncode, len(ok_line), len(bad)))
    return report([("the gold book entry validates", len(ok_line) == 1), ("no FAIL line and rc 0", not bad and r.returncode == 0)])


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac1", "ac2"):
        print(__doc__)
        return 9
    return {"ac1": ac1, "ac2": ac2}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
