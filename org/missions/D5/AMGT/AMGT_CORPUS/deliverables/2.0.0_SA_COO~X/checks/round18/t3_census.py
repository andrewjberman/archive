"""AMGT_CORPUS round 18, CRPS-t-3 -- grade the worker's model-block READER census (read-only; the issuer's file).
  -> 't3 readers N rows_valid V all_valid <bool> key_forms <sorted forms> bp_absent K'
"""
import json
import os
import sys
P = "org/missions/D5/AMGT/AMGT_CORPUS/deliverables/0.9.0_WK_AMGT_CORPUS~3/MODEL_BLOCK_READERS_ROUND18.json"
if not os.path.exists(P):
    print("t3 census MISSING %s" % P)
    sys.exit(0)
d = json.load(open(P, encoding="utf-8"))
rows = d.get("readers") or []
need = ("reader", "key_form", "reads_bp", "evidence")
ok = [r for r in rows if all(k in r for k in need) and r["reads_bp"] in ("OK", "ABSENT", "NOT_APPLICABLE") and r["evidence"]]
print("t3 readers %d rows_valid %d all_valid %s key_forms %s bp_absent %d" % (
    d.get("denominator", -1), len(ok), len(ok) == len(rows) == d.get("denominator"),
    ",".join(sorted({r["key_form"] for r in ok})) or "none", sum(1 for r in ok if r["reads_bp"] == "ABSENT")))
