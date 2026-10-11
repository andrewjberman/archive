import datetime
import json

import boto3
D = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
m = json.load(open(D + "/mapping_v3.json", encoding="utf-8"))
s3 = boto3.client("s3")
out = {"generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "parents": []}
for g in m["regrids"]:
    b, p = g["bucket"], g["parent"]
    keys = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=b, Prefix=p):
        for o in page.get("Contents", []):
            keys.append([o["Key"], o["Size"]])
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out["parents"].append({"bucket": b, "parent": p, "listed_at": t, "count": len(keys), "keys": keys,
                           "v3_listed_objects": g["listed_objects"], "v3_listed_at": g["listed_at"]})
    print(b, p, "live", len(keys), "v3", g["listed_objects"], flush=True)
json.dump(out, open(".scratch/live_parents.json", "w", encoding="utf-8"))
print("parents", len(out["parents"]), "total objects", sum(x["count"] for x in out["parents"]))
