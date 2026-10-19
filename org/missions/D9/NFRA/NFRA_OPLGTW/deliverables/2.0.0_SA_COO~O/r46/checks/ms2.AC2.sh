#!/usr/bin/env bash
# OPLGTW OG-ms-2 AC2 (Phase B): master 08403355 is in Alyssa's LIVE grant at its full current account set, nothing else changed.
#  - ledger nfra-oplgtw-ms2-alyssa-master-0840 CLOSED at HEAD, sentinel gone;
#  - LIVE strongly consistent read of the POLICY# partitions: Alyssa active, a NEWER grant revision than W/MS2_BEFORE.json, three masters,
#    the new master's account count equal to the recorded current count, the two other masters' account sets hashing as before,
#    the scope without masters and accounts hashing as before; Andrew's grant revision unchanged (W/MG2_BEFORE.json);
#  - W/MS2_READBACK_DECIDE.json: decide() on her live grant admits the four read tools and refuses schwab_prepare_download for 08403355.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"; slug=nfra-oplgtw-ms2-alyssa-master-0840
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
live=$(timeout 100 python - "$(native "$W/MS2_BEFORE.json")" "$(native "$W/MG2_BEFORE.json")" "$(native "$W/MS2_READBACK_DECIDE.json")" <<'EOF'
import hashlib, json, sys
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
    print("live read FAILED %s" % type(e).__name__); print("NO"); raise SystemExit(0)
val = lambda i, k: (list(i[k].values())[0] if k in i else None)
prof = {}
for i in items:
    if val(i, "record_type") == "principal_profile" and val(i, "email") and val(i, "status") == "active":
        em = val(i, "email").lower()
        role = "andrew" if em.startswith("andrew") else "alyssa" if em.startswith("alyssa") else "other"
        if role in ("andrew", "alyssa"): prof[role] = i
def grant(role):
    p = prof.get(role)
    if not p: return None, None
    pk, gr = val(p, "pk"), str(val(p, "grant_revision"))
    for i in items:
        if val(i, "pk") == pk and val(i, "record_type") == "data_entitlement" and str(val(i, "revision")) == gr:
            s = TD.deserialize(i["scope"]) if "scope" in i else None
            return int(gr), (json.loads(s) if isinstance(s, str) else s)
    return None, None
def load(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return {}
before = (load(sys.argv[1]).get("principal") or {})
mg2 = {r.get("role"): r for r in load(sys.argv[2]).get("principals", [])}
num = lambda o: int(o) if o == int(o) else float(o)
rev, sc = grant("alyssa"); sc = sc or {}
acc = sc.get("accounts") or {}
M = "08403355"
newer = rev is not None and before.get("grant_revision") is not None and rev > int(before["grant_revision"])
three = len(sc.get("masters") or []) == 3 and M in (sc.get("masters") or [])
newok = M in acc and len(acc[M]) == before.get("new_master_accounts_current")
oldh = {m: hashlib.sha256("\n".join(sorted(acc.get(m, []))).encode()).hexdigest() for m in (before.get("accounts_sha256") or {})}
oldok = bool(oldh) and oldh == before.get("accounts_sha256")
rest = {k: v for k, v in sc.items() if k not in ("masters", "accounts")}
resth = hashlib.sha256(json.dumps(rest, sort_keys=True, separators=(",", ":"), default=num).encode()).hexdigest()
restok = resth == before.get("scope_sans_masters_accounts_sha256")
arev, _ = grant("andrew")
andok = arev is not None and (mg2.get("andrew") or {}).get("grant_revision") is not None and arev == int(mg2["andrew"]["grant_revision"])
tools = ("schwab_get_access", "schwab_list_files", "schwab_describe_dataset", "schwab_query")
p = (load(sys.argv[3]).get("alyssa") or {})
dec = all((p.get("admit") or {}).get(t) is True for t in tools) and (p.get("refuse") or {}).get("schwab_prepare_download") is True and p.get("tree") == "deployed" and len(str(p.get("code_sha") or "")) >= 10
Y = lambda x: "yes" if x else "no"
print("alyssa: active %s; newer grant revision %s; masters 3 %s; new master count == current %s; other masters' accounts unchanged %s; rest of scope unchanged %s" % (Y("alyssa" in prof), Y(newer), Y(three), Y(newok), Y(oldok), Y(restok)))
print("andrew: grant revision unchanged %s" % Y(andok))
print("decide() on Alyssa's live grant admits 4 read tools and refuses prepare_download on the new master: %s" % Y(dec))
print("OK" if all(("alyssa" in prof, newer, three, newok, oldok, restok, andok, dec)) else "NO")
EOF
)
live=$(printf '%s' "$live" | tr -d '\r')
echo "$slug: status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
printf '%s\n' "$live" | sed '$d'
[ "$closed" = yes ] && [ "$sent" = 0 ] && [ "$(printf '%s\n' "$live" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
