"""AMGT_CORPUS round 33 CRPS-ai-2 gate / leg a -- the per-key diff of a field_map.json against the committed bytes at a ref.
Read-only. The issuer's file; run as a named script with python -u.

  python -u m33.py <map_path> [<ref>]   compare <map_path> with `git show <ref>:integrations/bloomberg/research/field_map.json`
                                        (ref defaults to HEAD)
  -> 'FIELD <mnemonic> unit <security> <old> -> <new>' per changed field-level unit label
  -> 'm33 fields_unit F unit_evidence E raw_stamp R derived_by D value_sampled S status_moves M other_keys O
      securities <sorted list> other_securities X'
The signed expectation is the dry run's, printed in NEVER_WIDEN_ROUND33_AI2_SERVED_ACT.md.
"""
import collections
import json
import subprocess
import sys

SECS = set(["HEI US Equity", "MELI US Equity", "PWR US Equity", "JD US Equity", "ORA FP Equity", "RWE GR Equity", "BP/ LN Equity",
        "AZN LN Equity", "RKT LN Equity", "TTE FP Equity", "ULVR LN Equity"])
REL = "integrations/bloomberg/research/field_map.json"

path = sys.argv[1]
ref = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
old_doc = json.loads(subprocess.run(["git", "show", "%s:%s" % (ref, REL)], capture_output=True, check=True).stdout)
new_doc = json.load(open(path, encoding="utf-8"))
b = {e["mnemonic"]: e for e in old_doc["fields"]}
a = {e["mnemonic"]: e for e in new_doc["fields"]}
c = collections.Counter()
touched = set()
for m in sorted(set(a) | set(b)):
    ou, nu = (b.get(m) or {}).get("unit"), (a.get(m) or {}).get("unit")
    if json.dumps(ou, sort_keys=True) != json.dumps(nu, sort_keys=True):
        c["fields_unit"] += 1
        if isinstance(ou, dict) and isinstance(nu, dict):
            for s in sorted(set(ou) | set(nu)):
                if ou.get(s) != nu.get(s):
                    touched.add(s)
                    print("FIELD %s unit %s %s -> %s" % (m, s, str(ou.get(s))[:40], str(nu.get(s))[:40]))
    for k in set(a.get(m) or {}) | set(b.get(m) or {}):
        if k in ("per_security_detail", "unit"):
            continue
        if json.dumps((a.get(m) or {}).get(k), sort_keys=True) != json.dumps((b.get(m) or {}).get(k), sort_keys=True):
            c["other_keys"] += 1
            print("FIELDKEY %s %s" % (m, k))
    bd = (b.get(m) or {}).get("per_security_detail") or {}
    ad = (a.get(m) or {}).get("per_security_detail") or {}
    for s in set(bd) | set(ad):
        o, n = bd.get(s) or {}, ad.get(s) or {}
        if json.dumps(o, sort_keys=True) == json.dumps(n, sort_keys=True):
            continue
        touched.add(s)
        for k in set(o) | set(n):
            if json.dumps(o.get(k), sort_keys=True) != json.dumps(n.get(k), sort_keys=True):
                if k in ("unit_status", "sign_status"):
                    c["status_moves"] += 1
                elif k in ("unit_evidence", "raw_stamp", "derived_by", "value_sampled"):
                    c[k] += 1
                else:
                    c["other_keys"] += 1
                    print("DETAILKEY %s %s %s" % (m, s, k))
print("m33 fields_unit %d unit_evidence %d raw_stamp %d derived_by %d value_sampled %d status_moves %d other_keys %d "
      "securities %s other_securities %d" % (c["fields_unit"], c["unit_evidence"], c["raw_stamp"], c["derived_by"],
                                             c["value_sampled"], c["status_moves"], c["other_keys"], sorted(touched),
                                             len(touched - SECS)))
