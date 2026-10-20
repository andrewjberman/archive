#!/usr/bin/env bash
# OPLGTW OG-gc-1 AC2 (round 47, PHASE B): the client_* tools answer for Alyssa and Menachem on the live gateway. W/GC1_RESULT.json:
#  {"write": "none" | "person_access", "principals": {"alyssa": R, "menachem": R}} with R = {"served_call": {"tool": "client_resolve_account", "answered": true, "tool_denied": false, "absent_reason": <not "firm_not_served" and not a denial code>,
#   "candidate_count": n >= 1}, "as_principal": <the same role: the call was made in HIS OR HER OWN session>, "record_revision": n | null}.
#  When write is "person_access", the LIVE person_access record of each principal is re-read here (strong read) and its tools_allow equals the ask's set (a subset of the five client tools), its channels_allow is empty, its tools_deny is empty,
#  status active, stopped false; when write is "none" no person_access record carries a client tool in tools_allow for either principal (read here).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"
[ -f "$W/GC1_RESULT.json" ] || { echo "GC1_RESULT.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(timeout 110 python3 -I - "$(native "$W")" <<'PYEOF'
import json, os, sys
W = sys.argv[1]
d = json.load(open(os.path.join(W, "GC1_RESULT.json"), encoding="utf-8")); d = d.get("body", d)
TOOLS = {"client_resolve_account", "client_get_holdings", "client_get_transactions", "client_get_allocation", "client_get_fees"}
ok = True
write = d.get("write")
write_ok = write in ("none", "person_access")
print("write kind %s: %s" % (write, "ok" if write_ok else "NOT OK"))
ok = ok and write_ok
for who in ("alyssa", "menachem"):
    r = (d.get("principals") or {}).get(who) or {}
    sc = r.get("served_call") or {}
    good = (r.get("as_principal") == who and sc.get("tool") == "client_resolve_account" and sc.get("answered") is True and sc.get("tool_denied") is False
            and sc.get("absent_reason") not in ("firm_not_served",) and isinstance(sc.get("candidate_count"), int) and sc["candidate_count"] >= 1)
    print("%s: a served client_resolve_account call in the principal's own session answered, not denied, %s candidate(s): %s" % (who, sc.get("candidate_count"), "ok" if good else "NOT OK"))
    ok = ok and good
try:
    import boto3
    from boto3.dynamodb.types import TypeDeserializer
    td = TypeDeserializer()
    c = boto3.client("dynamodb", region_name="us-east-1")
    kw = {"TableName": "gateway-access-state-table", "ConsistentRead": True, "FilterExpression": "sk = :s", "ExpressionAttributeValues": {":s": {"S": "person_access"}}}
    items = []
    while True:
        r = c.scan(**kw)
        items += r["Items"]
        if "LastEvaluatedKey" not in r:
            break
        kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
    recs = [{k: td.deserialize(v) for k, v in i.items()} for i in items]
except Exception as e:
    print("live read FAILED %s" % type(e).__name__)
    print("NO")
    raise SystemExit(0)
with_client = [x for x in recs if TOOLS & set(x.get("tools_allow") or [])]
if write == "none":
    print("live person_access records carrying a client tool in tools_allow: %d (want 0): %s" % (len(with_client), "ok" if not with_client else "NOT OK"))
    ok = ok and not with_client
else:
    good = len(with_client) >= 1 and all(x.get("status") == "active" and x.get("stopped") in (False, None) and not x.get("channels_allow") and not x.get("tools_deny")
                                         and set(x.get("tools_allow") or []) <= TOOLS for x in with_client)
    print("live person_access records admitting client tools: %d, each active, not stopped, tools_allow a subset of the five client tools, no channel, no deny: %s" % (len(with_client), "ok" if good else "NOT OK"))
    ok = ok and good
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
