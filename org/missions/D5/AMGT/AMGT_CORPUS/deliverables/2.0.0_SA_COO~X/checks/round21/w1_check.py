"""AMGT_CORPUS round 21, CRPS-w-1 -- the pack_shape census through the dossier's own function, over the 96 security keys of
the round-17 census, with four named controls measured by the issuer at the cut (the fold's A/B picks: IMB docx, ADBE pdf,
AZN pdf; 6501 has no report). Read-only (S3 reads); the issuer's file.

  -> 'w1 pack_shape folders F pdf P docx D mixed M none N errors E sum_ok S control IMB_LN_Equity <v> ADBE_US_Equity <v>
      AZN_LN_Equity <v> 6501_JP_Equity <v>'
"""
import json
import sys

from lib.research.corpus import dossier
from lib.research.harvest import store

CENSUS = "org/missions/D5/AMGT/AMGT_CORPUS/deliverables/0.9.0_WK_AMGT_CORPUS~1/MODEL_BLOCK_CENSUS_ROUND17.json"
CONTROLS = ["IMB_LN_Equity", "ADBE_US_Equity", "AZN_LN_Equity", "6501_JP_Equity"]

keys = [r["security_key"] for r in json.load(open(CENSUS, encoding="utf-8"))["rows"]]
client = store._default_client()
counts = {"pdf": 0, "docx": 0, "mixed": 0, "none": 0}
errors = 0
seen = {}
for k in keys:
    try:
        f = dossier.pack_shape(k, client=client)
        v = f.get("value")
        label = "none" if v is None else v
        if label not in counts or (v is None and not f.get("absent")):
            errors += 1
            continue
        counts[label] += 1
        seen[k] = label
    except Exception as exc:  # noqa: BLE001 -- a raise is counted, never hidden
        errors += 1
        print("ERR %s %s" % (k, type(exc).__name__), file=sys.stderr)
ctrl = " ".join("%s %s" % (k, seen.get(k, "ERR")) for k in CONTROLS)
print("w1 pack_shape folders %d pdf %d docx %d mixed %d none %d errors %d sum_ok %s control %s" % (
    len(keys), counts["pdf"], counts["docx"], counts["mixed"], counts["none"], errors,
    sum(counts.values()) == len(keys), ctrl))
