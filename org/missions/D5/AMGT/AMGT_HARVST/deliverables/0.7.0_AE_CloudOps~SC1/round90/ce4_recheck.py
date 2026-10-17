"""HVST-ce-4: READ-ONLY re-check of the 18 names whose printed branch checks were lost (8035_JP .. NKE). Writes nothing."""
from __future__ import annotations

import importlib.util

spec = importlib.util.spec_from_file_location("ce4_run", r"C:\dev\ajb_workspace\org\missions\D5\AMGT\AMGT_HARVST\deliverables\0.7.0_AE_CloudOps~SC1\round90\ce4_run.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
cen = m.census()
allnames = m.names()
first18 = allnames[:allnames.index("NOW_US_Equity")]
first18 = [n for n in first18 if n not in ("UNH_US_Equity", "KMB_US_Equity")]
bad = 0
for n in first18:
    doc = m.continuation.build(n)
    ok = m.check_branch(n, doc, cen)
    counts = m.scan("RECHECK " + n, doc)
    if not ok or counts != [0, 0]:
        bad += 1
print("RECHECK SUMMARY names=%d branch_B_or_mexico=%d" % (len(first18), bad))
