"""OG-rl-8 Phase A: READ-ONLY census of the ATTRIBUTE NAMES (never values) of gateway-access-state-table records, grouped by (namespace/kind, sort-key head).
Confirms where a refresh-family record carries tid/oid/email before the population is built (LG1_ADMIT_SET.md section 2 step 1).  usage: python r20_attr_census.py"""
import collections
import boto3

ddb = boto3.client("dynamodb", region_name="us-east-1")
items = []
for page in ddb.get_paginator("scan").paginate(TableName="gateway-access-state-table", ConsistentRead=True):   # Scan only: no write verb is reachable from this client use
    items += page.get("Items", [])
print("items", len(items))
shape = collections.Counter()
for it in items:
    pk, sk = it["pk"]["S"], it["sk"]["S"]
    kind = "/".join(pk.split("#")[:2]) if pk.startswith("RUNTIME#") else ("POLICY#EMAILDENY" if pk.startswith("POLICY#EMAILDENY#") else "POLICY#<principal>")
    shape[(kind if not kind.startswith("RUNTIME/probe") else "RUNTIME/probe", sk.split("#")[0], tuple(sorted(it.keys())))] += 1
for k, v in sorted(shape.items(), key=lambda x: -x[1]):
    print(v, k)
# for the refresh family: which attribute holds a principal/email-bearing structure
rf = [it for it in items if it["sk"]["S"] == "oauth_refresh_family"]
t = collections.Counter()
for it in rf:
    for name, val in it.items():
        t[(name, next(iter(val.keys())))] += 1
print("refresh-family attribute name/type counts:", dict(t))
