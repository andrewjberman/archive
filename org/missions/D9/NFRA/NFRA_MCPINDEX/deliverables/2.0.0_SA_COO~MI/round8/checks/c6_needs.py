"""c6_needs.py -- MX-c-6 AC1 instrument (FWD-12, FWD-15, FWD-17, FWD-18; PRD v0.7 contracts 1, 5, 6).

Reads the EMITTED runtime catalog (app/refs/DATA_CATALOG.yaml) and grades its top-level `needs:` list against the
brief's Part IV.A denominator (E-1..E-29). Prints every violation, then one summary line. Offline, read-only.
Usage: python c6_needs.py <path to DATA_CATALOG.yaml>
"""
import re
import sys

import yaml

cat = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
needs = cat.get("needs") or []
REQ = ("id", "need", "source", "status", "tool", "owner", "retires", "op_class")
STATUS = {"SERVED", "PARTIAL", "GAP", "DENIED", "UNMEASURED"}
UNOWNED = {"E-9", "E-10", "E-11", "E-12", "E-20", "E-26", "E-27", "E-28"}
WF = re.compile(r"^(C[1-8]|W[1-6])$")
want = {"E-%d" % i for i in range(1, 30)}
bad = []
ids = [str(n.get("id")) for n in needs if isinstance(n, dict)]
for n in needs:
    if not isinstance(n, dict):
        bad.append("non-mapping entry")
        continue
    i = str(n.get("id"))
    miss = [k for k in REQ if k not in n]
    if miss:
        bad.append("%s missing keys %s" % (i, miss))
    if n.get("status") not in STATUS:
        bad.append("%s status %r outside the enum" % (i, n.get("status")))
    if n.get("op_class") not in ("read", "write"):
        bad.append("%s op_class %r is not read|write" % (i, n.get("op_class")))
    if n.get("status") in ("GAP", "DENIED", "UNMEASURED") and not str(n.get("owner") or "").strip():
        bad.append("%s is %s with no owner (a project code or 'unowned')" % (i, n.get("status")))
    if n.get("status") == "PARTIAL" and str(n.get("tool") or "").startswith("ycharts_") and not n.get("live_error"):
        bad.append("%s is a PARTIAL vendor entry with no live_error" % i)
    r = n.get("retires") or []
    if any(not WF.match(str(x)) for x in r):
        bad.append("%s retires %r (each must be one of C1-C8 / W1-W6)" % (i, r))
    if not r and not str(n.get("retires_none") or "").strip():
        bad.append("%s retires nothing and states no retires_none reason" % i)
unowned = {str(n.get("id")) for n in needs if isinstance(n, dict) and str(n.get("owner")) == "unowned"}
for b in bad:
    print("VIOLATION: " + b)
print("needs entries %d of 29 (ids exact=%s, duplicates=%d); violations %d; unowned %d of 8 (exact=%s)"
      % (len(set(ids) & want), set(ids) == want, len(ids) - len(set(ids)), len(bad), len(unowned & UNOWNED),
         unowned == UNOWNED))
ok = set(ids) == want and len(ids) == 29 and not bad and unowned == UNOWNED
sys.exit(0 if ok else 1)
