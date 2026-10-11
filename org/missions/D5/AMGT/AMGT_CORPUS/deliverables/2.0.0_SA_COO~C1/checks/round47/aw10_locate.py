"""AMGT_CORPUS round 47, CRPS-aw-10 -- locate the master template in the synced research library. Issuer's file. READ-ONLY.

  PYTHONPATH=. python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~C1/checks/round47/aw10_locate.py
  (from the repository root of the site-Z checkout; `PYTHONPATH=.` is REQUIRED: `python <path>` puts the script's directory, not the
  working directory, on sys.path, so `import lib.research` fails without it -- row AMGT_CORPUS-Z-S92, read by ~ZC 2026-10-11)

AMENDMENT 1 (issuer, 2026-10-11 ~18:2xZ): the SharePoint item sits in `Shared Documents/Asset Management/` (Graph listing of that folder,
read by the issuer), which is the PARENT of the library root `.../Asset Management/Research` that `library.library_root()` derives. The first
version walked only the root, so its 0 of 378 did not look where the item is. This version walks the root (every file, as before) AND lists the
files DIRECTLY inside the root's parent folder (no recursion there: the parent also holds the dashboard folders). It prints:
  template_locate root <library root> source <how the root was derived>
  template_locate parent <the root's parent> exists <True|False> files_directly_in_parent <n>
  template_locate matches <n> of files_walked <w> in_root <a> in_parent <b>
  template_locate match <full path> size <bytes> mtime <UTC ISO>          (one line per match)
  template_locate expected_size 383839 size_equal <True|False|None>
Exit 0: exactly ONE match across the root and the parent's direct files. Exit 3: none or more than one (the executor writes nothing and
reports). The walk follows no link and opens no file. The root comes from `library_root()` (never typed).
"""
import datetime
import os
import sys

from lib.research.corpus import library, team_sheet

EXPECTED_SIZE = 383839  # bytes, SharePoint item 01L6LHKFRTYYYRWCI37VGLHJQPCL3KMJXN, read by Graph 2026-10-11


def _stat_line(p):
    st = os.stat(p)
    mt = datetime.datetime.fromtimestamp(st.st_mtime, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return (p, st.st_size, mt)


def main():
    root = library.library_root()
    print("template_locate root %s source %s" % (root, library.library_root_source()))
    parent = os.path.dirname(os.path.normpath(root))
    parent_ok = os.path.isdir(parent)
    hits, walked = [], 0
    in_root = in_parent = 0
    for d, _dirs, files in os.walk(root, followlinks=False):
        for f in files:
            walked += 1
            if f == team_sheet.MASTER_NAME:
                hits.append(_stat_line(os.path.join(d, f)))
                in_root += 1
    parent_files = 0
    if parent_ok:
        for f in sorted(os.listdir(parent)):
            p = os.path.join(parent, f)
            if os.path.isfile(p) and not os.path.islink(p):
                parent_files += 1
                if f == team_sheet.MASTER_NAME:
                    hits.append(_stat_line(p))
                    in_parent += 1
    print("template_locate parent %s exists %s files_directly_in_parent %d" % (parent, parent_ok, parent_files))
    print("template_locate matches %d of files_walked %d in_root %d in_parent %d" % (len(hits), walked, in_root, in_parent))
    for p, size, mt in hits:
        print("template_locate match %s size %d mtime %s" % (p, size, mt))
    eq = (hits[0][1] == EXPECTED_SIZE) if len(hits) == 1 else None
    print("template_locate expected_size %d size_equal %s" % (EXPECTED_SIZE, eq))
    return 0 if len(hits) == 1 else 3


if __name__ == "__main__":
    sys.exit(main())
