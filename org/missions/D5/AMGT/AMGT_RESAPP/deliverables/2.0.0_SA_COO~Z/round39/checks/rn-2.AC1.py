"""AMGT_RESAPP round 39, AMGT-rn-2 AC1 -- the producer STATES its semantics machine-readably: every present CSC
column whose relation begins "RECIPROCAL" carries `transform == "reciprocal"` and `units in {"fraction", "percent"}`
on the map entry build_csc_map() emits. Run from the repo root: python <this>. Exit 0 only when every such entry
carries both fields; the denominator is printed either way."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.getcwd())
from lib.research.peers import csc  # noqa: E402

m = csc.build_csc_map()
recip = [e for e in m["present"] if str(e.get("relation", "")).upper().startswith("RECIPROCAL")]
ok = 0
for e in recip:
    good = e.get("transform") == "reciprocal" and e.get("units") in ("fraction", "percent")
    ok += 1 if good else 0
    print("%s code=%s transform=%r units=%r -> %s" % (e["column"], e.get("code"), e.get("transform"), e.get("units"),
                                                       "OK" if good else "MISSING"))
print("RECIPROCAL entries carrying transform+units: %d of %d (present columns: %d)" % (ok, len(recip), len(m["present"])))
sys.exit(0 if recip and ok == len(recip) else 1)
