"""AMGT_CORPUS round 47, CRPS-aw-10 -- locate the master template in the synced research library. Issuer's file. READ-ONLY.

  python aw10_locate.py            (from the repository root of the site-Z checkout)

Prints, whole, and returns 0 only when exactly ONE file in the library has the master's name:
  template_locate root <library root> source <how the root was derived>
  template_locate matches <n> of files_walked <w>
  template_locate match <full path> size <bytes> mtime <UTC ISO>          (one line per match)
  template_locate expected_size 383839 size_equal <True|False|None>
The library root comes from `lib.research.corpus.library.library_root()` (never typed). The walk follows no link and opens no file.
Exit 0: one match. Exit 3: none or more than one (the executor writes nothing and reports).
"""
import datetime
import os
import sys

from lib.research.corpus import library, team_sheet

EXPECTED_SIZE = 383839  # bytes, SharePoint item 01L6LHKFRTYYYRWCI37VGLHJQPCL3KMJXN, read by Graph 2026-10-11


def main():
    root = library.library_root()
    print("template_locate root %s source %s" % (root, library.library_root_source()))
    hits = []
    walked = 0
    for d, _dirs, files in os.walk(root, followlinks=False):
        for f in files:
            walked += 1
            if f == team_sheet.MASTER_NAME:
                p = os.path.join(d, f)
                st = os.stat(p)
                mt = datetime.datetime.fromtimestamp(st.st_mtime, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                hits.append((p, st.st_size, mt))
    print("template_locate matches %d of files_walked %d" % (len(hits), walked))
    for p, size, mt in hits:
        print("template_locate match %s size %d mtime %s" % (p, size, mt))
    eq = (hits[0][1] == EXPECTED_SIZE) if len(hits) == 1 else None
    print("template_locate expected_size %d size_equal %s" % (EXPECTED_SIZE, eq))
    return 0 if len(hits) == 1 else 3


if __name__ == "__main__":
    sys.exit(main())
