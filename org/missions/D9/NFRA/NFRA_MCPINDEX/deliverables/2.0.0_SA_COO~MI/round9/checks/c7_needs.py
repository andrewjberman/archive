"""c7_needs.py -- MX-c-7 AC1 instrument (PRD v0.8 FWD-19, contract 4).

Grades the EMITTED runtime catalog's `needs:` list for the operations lead's six entries:
  E-30 trade reconciliation, E-31 billing        -- each mirrors its reader's census verdict:
        census SERVED -> status SERVED, op_class read, tool == the reader module's TOOL constant;
        census GAP    -> status GAP, tool null, owner == the census owner;
  E-32 post model update rec, E-33 high cash account alert FA, E-34 assets transfer alert FA,
  E-35 restricted account alert FA                -- status GAP, owner 'unowned', tool null, op_class read.
Also: E-1..E-29 still present (none lost), no duplicate id, and every one of the six carries a retires_none reason
(they retire none of Alyssa's C1-C8 / W1-W6). Prints every violation, then one summary line. Offline, read-only.
Usage: python c7_needs.py <DATA_CATALOG.yaml> <census_trade_rec.json> <census_billing.json> <gateway dir>
"""
import json
import os
import re
import sys

import yaml

cat = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
cens = {"E-30": (sys.argv[2], "ops_trade_rec"), "E-31": (sys.argv[3], "ops_billing")}
gw = sys.argv[4]
needs = [n for n in (cat.get("needs") or []) if isinstance(n, dict)]
by = {}
for n in needs:
    by.setdefault(str(n.get("id")), []).append(n)
bad = []
dups = sorted(i for i, v in by.items() if len(v) > 1)
if dups:
    bad.append("duplicate ids %s" % dups)
old = {"E-%d" % i for i in range(1, 30)}
if not old <= set(by):
    bad.append("lost earlier entries %s" % sorted(old - set(by)))


def tool_of(pkg):
    p = os.path.join(gw, "app", "integrations", pkg, "integration.py")
    if not os.path.exists(p):
        return None
    m = re.search(r'^TOOL\s*=\s*["\']([^"\']+)["\']', open(p, encoding="utf-8").read(), re.M)
    return m.group(1) if m else None


for i in ("E-30", "E-31"):
    n = (by.get(i) or [{}])[0]
    try:
        c = json.load(open(cens[i][0], encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        bad.append("%s census unreadable (%s)" % (i, type(exc).__name__))
        continue
    if c.get("verdict") == "SERVED":
        t = tool_of(cens[i][1])
        if n.get("status") != "SERVED" or n.get("op_class") != "read" or not t or n.get("tool") != t:
            bad.append("%s census SERVED but entry status=%r op_class=%r tool=%r (module TOOL %r)"
                       % (i, n.get("status"), n.get("op_class"), n.get("tool"), t))
    elif c.get("verdict") == "GAP":
        if n.get("status") != "GAP" or n.get("tool") not in (None, "") or n.get("owner") != c.get("owner"):
            bad.append("%s census GAP (owner %r) but entry status=%r tool=%r owner=%r"
                       % (i, c.get("owner"), n.get("status"), n.get("tool"), n.get("owner")))
    else:
        bad.append("%s census verdict %r" % (i, c.get("verdict")))
for i in ("E-32", "E-33", "E-34", "E-35"):
    n = (by.get(i) or [{}])[0]
    if (n.get("status"), n.get("owner"), n.get("tool") or None, n.get("op_class")) != ("GAP", "unowned", None, "read"):
        bad.append("%s status=%r owner=%r tool=%r op_class=%r (want GAP/unowned/null/read)"
                   % (i, n.get("status"), n.get("owner"), n.get("tool"), n.get("op_class")))
six = ["E-%d" % k for k in range(30, 36)]
for i in six:
    n = (by.get(i) or [{}])[0]
    if not n:
        bad.append("%s absent" % i)
    elif not str(n.get("retires_none") or "").strip():
        bad.append("%s states no retires_none reason" % i)
for b in bad:
    print("VIOLATION: " + b)
print("ops lead entries present %d of 6; earlier entries kept %d of 29; duplicates %d; violations %d"
      % (sum(1 for i in six if by.get(i)), len(old & set(by)), len(dups), len(bad)))
sys.exit(0 if not bad else 1)
