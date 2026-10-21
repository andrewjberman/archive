#!/usr/bin/env python
"""OG-rl-18 Phase A step 3(c): a READ-ONLY strong scan of the gateway access-state table's POLICY# records; counts only. `sentinel_grants_in_store` = the number of records whose scope.accounts holds the string `*`
(as a list member or as the whole value) for any master. No write, no account number or name is printed or stored.
usage: python rl18_sentinel_scan.py <out.json>"""
from __future__ import annotations

import datetime as dt
import io
import json
import sys

import boto3
from boto3.dynamodb.types import TypeDeserializer

TABLE = "gateway-access-state-table"
me = boto3.client("dynamodb", region_name="us-east-1")
td = TypeDeserializer()
items, kw, pages = [], {"TableName": TABLE, "ConsistentRead": True}, 0
resp = {"LastEvaluatedKey": True}
while "LastEvaluatedKey" in resp:
    resp = me.scan(**kw)
    pages += 1
    items += [{k: td.deserialize(v) for k, v in it.items()} for it in resp["Items"]]
    if "LastEvaluatedKey" in resp:
        kw["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
pol = [i for i in items if str(i.get("pk", "")).startswith("POLICY#")]
with_scope = [i for i in pol if isinstance(i.get("scope"), dict)]


def holds_star(v):
    if v == "*":
        return True
    if isinstance(v, (list, tuple, set, frozenset)):
        return any(x == "*" for x in v)
    return False


star = [i for i in with_scope if isinstance(i["scope"].get("accounts"), dict) and any(holds_star(v) for v in i["scope"]["accounts"].values())]
by_type = {}
for i in pol:
    by_type[str(i.get("record_type"))] = by_type.get(str(i.get("record_type")), 0) + 1
out = {"table": TABLE, "read_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "consistent_read": True, "scan_pages": pages, "items_scanned": len(items), "policy_records": len(pol),
       "policy_records_by_type": by_type, "records_with_a_scope": len(with_scope), "sentinel_grants_in_store": len(star)}
io.open(sys.argv[1], "w", encoding="utf-8", newline="\n").write(json.dumps(out, indent=1) + "\n")
print(json.dumps(out))
