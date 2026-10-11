"""c7_tags.py -- MX-c-7 AC3 instrument (round-8 analysis E2): the catalog's retire tags, the folds, E-13's guidance.

Reads the working tree only, offline. Prints one line per check and a summary; exit 0 only when every check holds:
  FWD18   C1-C8/W1-W6 answered by a SERVED need's `retires`, read from the emitted catalog: expect 3 of 14 (C2 W5 W6)
  C3      C3 carried by E-4, E-5 and E-9 (any status): expect 3 of 3
  E25     E-25's retires no longer claim C1
  FOLDS   references to the need-local word folds (_YTD / _AMP_WORD) in opal_discover: expect 0
  GUIDE   discover on an unknown model name reaches E-13 first, and that match carries the five served model codes
Usage: python c7_tags.py <gateway dir>
"""
import json
import os
import re
import sys

import yaml

gw = sys.argv[1]
cat = yaml.safe_load(open(os.path.join(gw, "app", "refs", "DATA_CATALOG.yaml"), encoding="utf-8"))
needs = {n["id"]: n for n in (cat.get("needs") or [])}
tags = {"C%d" % i for i in range(1, 9)} | {"W%d" % i for i in range(1, 7)}
served = set()
for n in needs.values():
    if n.get("status") == "SERVED":
        served |= set(n.get("retires") or []) & tags
ok = []
fwd18 = len(served)
ok.append(fwd18 == 3 and served == {"C2", "W5", "W6"})
print("FWD18 served %d of 14 (%s)" % (fwd18, " ".join(sorted(served))))
c3 = sum(1 for i in ("E-4", "E-5", "E-9") if "C3" in (needs.get(i, {}).get("retires") or []))
ok.append(c3 == 3)
print("C3 carried by E-4/E-5/E-9: %d of 3" % c3)
e25 = "C1" in (needs.get("E-25", {}).get("retires") or [])
ok.append(not e25)
print("E25 claims C1: %s" % e25)
src = open(os.path.join(gw, "app", "integrations", "opal_discover", "integration.py"), encoding="utf-8").read()
folds = len(re.findall(r"\b_YTD\b|\b_AMP_WORD\b", src))
ok.append(folds == 0)
print("FOLDS references: %d" % folds)
sys.path.insert(0, gw)
os.chdir(gw)
from app.graphql_plumbing import catalog_gate as g  # noqa: E402
from app.integrations.opal_discover import integration as od  # noqa: E402
ms = od.discover("how did the growth model do against its benchmark last quarter", g.OPAL_INTERNAL).get("matches", [])
first = ms[0] if ms else {}
fid = (first.get("need") or {}).get("id")
blob = json.dumps(first)
codes = [c for c in ("UST", "ST", "INT", "LT", "ULT") if re.search(r"\b%s\b" % c, blob)]
ok.append(fid == "E-13" and len(codes) == 5)
print("GUIDE first=%s five model codes in the match: %d of 5" % (fid, len(codes)))
print("E2 catalog checks held %d of %d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
