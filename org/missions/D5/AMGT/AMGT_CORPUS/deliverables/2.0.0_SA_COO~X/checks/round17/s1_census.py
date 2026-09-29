"""AMGT_CORPUS round 17, CRPS-s-1 -- grade the worker's model-block census file (read-only; the issuer's file).

  -> 's1 census names N present P absent A rows_valid V hitachi <state>'
  -> 's1 producer writer <path> invoked_by_n K population_source_named <True|False> admits_new_registrations <True|False> evidence_n E'
"""
import json
import os
import sys

PATH = "org/missions/D5/AMGT/AMGT_CORPUS/deliverables/0.9.0_WK_AMGT_CORPUS~1/MODEL_BLOCK_CENSUS_ROUND17.json"
if not os.path.exists(PATH):
    print("s1 census MISSING %s" % PATH)
    sys.exit(0)
d = json.load(open(PATH, encoding="utf-8"))
rows = d.get("rows") or []
need = ("security_key", "folder", "model_block", "latest_stamp", "evidence")
valid = [r for r in rows if all(k in r for k in need) and r.get("model_block") in ("present", "absent")
         and ((r["model_block"] == "present") == bool(r.get("latest_stamp")))]
present = sum(1 for r in valid if r["model_block"] == "present")
absent = sum(1 for r in valid if r["model_block"] == "absent")
hit = [r for r in rows if r.get("security_key") == "6501_JP_Equity"]
print("s1 census names %d present %d absent %d rows_valid %d hitachi %s" % (
    d.get("denominator", -1), present, absent, len(valid), hit[0].get("model_block") if hit else "NO-ROW"))
p = d.get("producer") or {}
print("s1 producer writer %s invoked_by_n %d population_source_named %s admits_new_registrations %s evidence_n %d" % (
    p.get("writer") or "NONE", len(p.get("invoked_by") or []), bool(p.get("population_source")),
    p.get("admits_new_registrations"), len(p.get("evidence") or [])))
