"""AMGT_CORPUS round 24, CRPS-z-2 -- TSM's same-currency anchor: the worker's stored-source census, and the discriminator's served
reason for TSM CURR_ENTP_VAL read live (S3 raw reads only). The issuer's file.

  -> 'z2 sources_searched N anchor <source|none> reason_states_limit True|False fx_invented False|True census_file True|False'
"""
import importlib.util
import json
import os
import subprocess

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
RES = os.path.join(TOP, "integrations", "bloomberg", "research")
CENSUS = os.path.join(TOP, "org/missions/D5/AMGT/AMGT_CORPUS/deliverables/0.9.0_WK_AMGT_CORPUS~2/TSM_ANCHOR_SOURCES_ROUND24.json")
spec = importlib.util.spec_from_file_location("bum_z2", os.path.join(RES, "build_unit_map.py"))
bum = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bum)
r = bum.discriminate_facts([("TSM US Equity", "CURR_ENTP_VAL")])[0]
reason = str(r.get("reason") or "")
has = os.path.exists(CENSUS)
c = json.load(open(CENSUS, encoding="utf-8")) if has else {}
srcs = c.get("sources") or []
anchor = c.get("anchor")
name = (anchor or {}).get("source") or "none"
if r.get("state") == "RESOLVED":
    ok = bool(anchor) and bool((r.get("evidence") or {}))
    invented = not bool((anchor or {}).get("source_key"))
else:
    ok = "no same-currency anchor stored" in reason
    invented = False
print("z2 sources_searched %d anchor %s reason_states_limit %s fx_invented %s census_file %s" % (
    len(srcs), name, ok, invented, has))
