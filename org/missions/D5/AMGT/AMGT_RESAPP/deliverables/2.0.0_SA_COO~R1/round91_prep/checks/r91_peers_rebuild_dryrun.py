"""Round 91 read: what a peers rebuild against the CURRENT scanner would change. Read-only: nothing is written."""
import collections
import json
import sys
import time

import boto3

from lib.research.identity import crosswalk
from lib.research.peers import csc as csc_module
from lib.research.peers import engine
from lib.research.peers import universe as universe_module

t0 = time.time()
s3 = boto3.client("s3", region_name="us-east-1")
doc = universe_module.build_candidate_universe(refresh=True)
print("fresh universe: vintages", doc.get("vintages") or doc.get("scanner_vintages") or {k: doc[k] for k in doc if "vintage" in k.lower()} )
csc_map = csc_module.build_csc_map(factor_metadata=universe_module.fetch_factor_metadata(),
                                   row_value_codes=doc.get("row_value_codes"))
union, union_source = crosswalk.load_identity_universe(client=s3)
current, _i, _a = crosswalk.load_crosswalk()
keyed = [n for n in current["records"] if n.get("resolution") == "MEASURED" and n.get("security_key")]
widened = engine.build_widened_identity_index(union)
print("keyed names", len(keyed), "elapsed", round(time.time() - t0))

def latest_stored(key):
    prefix = "peers/v1/%s/" % crosswalk.slash_safe_key(key)
    r = s3.list_objects_v2(Bucket="opal-data-harvest", Prefix=prefix)
    objs = sorted(o["Key"] for o in r.get("Contents", []))
    if not objs:
        return None, None
    k = objs[-1]
    return k, json.loads(s3.get_object(Bucket="opal-data-harvest", Key=k)["Body"].read())

rows = []
for i, n in enumerate(keyed):
    key = n["security_key"]
    new = engine.peers(key, as_of="2026-10-11", universe_document=doc, csc_map=csc_map, widened_identity_index=widened)
    okey, old = latest_stored(key)
    nm = [m["ticker"] for m in new["members"]]
    om = [m["ticker"] for m in (old or {}).get("members", [])]
    caps = sorted({m.get("cap_vintage") for m in new["members"] if m.get("cap_vintage")})
    rows.append({"key": key, "old_key": okey, "old_basis": (old or {}).get("basis"), "new_basis": new["basis"],
                 "new_members": nm, "old_members": om,
                 "old_n": len(om), "new_n": len(nm), "same_set": set(nm) == set(om), "same_order": nm == om,
                 "new_cap_vintages": caps, "old_as_of": (old or {}).get("as_of")})
    if i % 40 == 0:
        print("..", i, "elapsed", round(time.time() - t0))
flat = [{"security_key": r["key"], "basis": r["new_basis"], "members": []} for r in rows]
json.dump(rows, open(sys.argv[1], "w"))
c = collections.Counter()
for r in rows:
    c["old_%s" % r["old_basis"]] += 1
    c["new_%s" % r["new_basis"]] += 1
    c["same_set" if r["same_set"] else "changed_set"] += 1
    if r["old_basis"] == "derived" and r["new_basis"] != "derived":
        c["REGRESSION_derived_to_absent"] += 1
print(dict(c))
vint = collections.Counter(v for r in rows for v in r["new_cap_vintages"])
print("new member cap_vintage values:", dict(vint))
print("elapsed", round(time.time() - t0))
