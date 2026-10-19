#!/usr/bin/env bash
# OPLGTW OG-mg-2 AC2 (Phase B): the two grants are re-activated at the current account sets, READ BACK LIVE.
#  - ledger nfra-oplgtw-mg2-schwab-full-accounts CLOSED at HEAD, sentinel gone;
#  - LIVE strongly consistent read of the POLICY# partitions: for andrew and alyssa the profile is active, the grant in force
#    is a NEWER revision than W/MG2_BEFORE.json, every master's account count equals the recorded current count, and the
#    scope without accounts hashes to the recorded value (nothing else changed);
#  - W/MG2_READBACK_DECIDE.json: decide() on Alyssa's LIVE grant admits the four read tools and refuses schwab_prepare_download.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1"; slug=nfra-oplgtw-mg2-schwab-full-accounts
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
live=$(timeout 100 python - "$(native "$W/MG2_BEFORE.json")" "$(native "$W/MG2_READBACK_DECIDE.json")" <<'EOF'
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
try:
    before = {r["role"]: r for r in json.load(open(sys.argv[1], encoding="utf-8")).get("principals", [])}
except Exception:
    before = {}
res = {}
import os
HELD = os.path.exists(sys.argv[1].replace("MG2_BEFORE.json", "MG2_ANDREW_HELD.md"))   # amendment A1: option (b), Andrew's activation held
for role in ("andrew", "alyssa"):
    rev, sc = grant(role); b = before.get(role) or {}
    if role == "andrew" and HELD:
        same = rev is not None and b.get("grant_revision") is not None and rev == int(b["grant_revision"])
        res[role] = same
        print("andrew: HELD by option (b); grant revision unchanged %s" % ("yes" if same else "no"))
        continue
    newer = rev is not None and b.get("grant_revision") is not None and rev > int(b["grant_revision"])
    acc = (sc or {}).get("accounts") or {}
    counts_ok = bool(acc) and {m: len(v) for m, v in acc.items()} == b.get("accounts_current")
    rest = {k: v for k, v in (sc or {}).items() if k != "accounts"}
    num = lambda o: int(o) if o == int(o) else float(o)
    h = hashlib.sha256(json.dumps(rest, sort_keys=True, separators=(",", ":"), default=num).encode()).hexdigest()
    res[role] = newer and counts_ok and h == b.get("scope_sans_accounts_sha256")
    print("%s: active %s; newer grant revision %s; per-master counts == current %s; rest of scope unchanged %s"
          % (role, "yes" if role in prof else "no", "yes" if newer else "no", "yes" if counts_ok else "no", "yes" if h == b.get("scope_sans_accounts_sha256") else "no"))
tools = ("schwab_get_access", "schwab_list_files", "schwab_describe_dataset", "schwab_query")
try:
    p = json.load(open(sys.argv[2], encoding="utf-8")).get("alyssa") or {}
    dec = all((p.get("admit") or {}).get(t) is True for t in tools) and (p.get("refuse") or {}).get("schwab_prepare_download") is True
except Exception:
    dec = False
print("decide() on Alyssa's live grant admits 4 read tools and refuses prepare_download: %s" % ("yes" if dec else "no"))
print("OK" if (all(res.values()) and len(res) == 2 and dec) else "NO")
EOF
)
live=$(printf '%s' "$live" | tr -d '\r')
echo "$slug: status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
printf '%s\n' "$live" | sed '$d'
[ "$closed" = yes ] && [ "$sent" = 0 ] && [ "$(printf '%s\n' "$live" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
