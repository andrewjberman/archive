#!/usr/bin/env bash
# OPLGTW OG-mg-1 AC2 (Phase B): both grant writes landed, read back LIVE, and the ledger closed.
#  - ledger nfra-oplgtw-r30-grant-writes CLOSED at HEAD, sentinel gone;
#  - LIVE read of gateway-access-state-table (POLICY# partitions, strongly consistent, fully paginated; identities reduced
#    to role labels in-process, never printed): Andrew's principal_profile is active and its grant in force carries
#    calendar_months 13; the Bloomberg principal's profile is active and its grant in force has the SAME scope (mirror);
#    the one pre-existing active profile (Alyssa's) is unchanged in revision.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"; slug=nfra-oplgtw-r30-grant-writes
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
live=$(timeout 100 python - "$(native "$W/MG1_BEFORE.json")" <<'EOF'
import json, sys
try:
    import boto3
    from boto3.dynamodb.types import TypeDeserializer
    TD = TypeDeserializer()
    c = boto3.client("dynamodb", region_name="us-east-1")
    kw = {"TableName": "gateway-access-state-table", "ConsistentRead": True,
          "FilterExpression": "begins_with(pk,:p)", "ExpressionAttributeValues": {":p": {"S": "POLICY#"}}}
    items = []
    while True:
        r = c.scan(**kw); items += r["Items"]
        if "LastEvaluatedKey" not in r: break
        kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
except Exception as e:
    print("live read FAILED %s" % type(e).__name__); raise SystemExit(0)
val = lambda i, k: (list(i[k].values())[0] if k in i else None)
prof = {}
for i in items:
    if val(i, "record_type") == "principal_profile" and val(i, "email"):
        em = val(i, "email").lower()
        role = "andrew" if em.startswith("andrew") else "bbg" if em.startswith("opalbloomberg") else "alyssa" if em.startswith("alyssa") else "other"
        prof[role] = i
def grant(role):
    p = prof.get(role)
    if not p: return None
    pk, gr = val(p, "pk"), str(val(p, "grant_revision"))
    for i in items:
        if val(i, "pk") == pk and val(i, "record_type") == "data_entitlement" and str(val(i, "revision")) == gr:
            s = TD.deserialize(i["scope"]) if "scope" in i else None
            return json.loads(s) if isinstance(s, str) else s
    return None
def cm(sc):
    # calendar_months sits under the scope's dates map (Z-S174: the first draft read the top level of a typed map)
    d = (sc or {}).get("dates") if isinstance(sc, dict) else None
    return str((d or {}).get("calendar_months")) if isinstance(d, dict) else str((sc or {}).get("calendar_months"))
def strip(sc):
    return {k: v for k, v in (sc or {}).items() if k not in ("tid", "oid", "email", "principal", "subject")}
ga, gb = grant("andrew"), grant("bbg")
a_ok = bool(prof.get("andrew")) and val(prof["andrew"], "status") == "active" and isinstance(ga, dict) and cm(ga) == "13"
b_ok = bool(prof.get("bbg")) and val(prof["bbg"], "status") == "active" and isinstance(gb, dict)
mirror = a_ok and b_ok and strip(ga) == strip(gb)
try:
    before = {r["role"]: r for r in json.load(open(sys.argv[1], encoding="utf-8")).get("principals", [])}
    al_before = (before.get("alyssa") or {}).get("profile_revision")
except Exception:
    al_before = None
al_now = str(val(prof["alyssa"], "revision")) if prof.get("alyssa") else None
al_ok = al_before is not None and str(al_before) == al_now
print("policy items %d; andrew active+13mo: %s; bbg active: %s; bbg scope == andrew scope: %s; alyssa unchanged: %s"
      % (len(items), "yes" if a_ok else "no", "yes" if b_ok else "no", "yes" if mirror else "no", "yes" if al_ok else "no"))
print("OK" if (a_ok and b_ok and mirror and al_ok) else "NO")
EOF
)
live=$(printf '%s' "$live" | tr -d '\r')
echo "$slug: status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
printf '%s\n' "$live" | sed '$d'
[ "$closed" = yes ] && [ "$sent" = 0 ] && [ "$(printf '%s\n' "$live" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
