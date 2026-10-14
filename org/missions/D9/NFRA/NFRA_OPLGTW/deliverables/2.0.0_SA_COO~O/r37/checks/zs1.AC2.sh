#!/usr/bin/env bash
# OPLGTW OG-zs-1 AC2 (round-37 ZS114-EDGE-AUTH): the deploy closed and the bare path refuses an unauthenticated read.
#  - ledger nfra-oplgtw-edge-auth-json-tiered is CLOSED at HEAD and its sentinel is gone;
#  - A1/A2 (rows Z-S115, Z-S121): the WebACL conditions -- rules identical before and after with at most ONE UpdateWebACL (0 is safer than 1: nothing was sent), or no ACL change at all;
#  - THIS CHECK performs the live unauthenticated GETs: the bare /json-tiered/ path and its twin both answer 401 or 403;
#  - W/ZS1_PROOF.json: bare_unauth_status 401/403, twin_authed_status 200, a named twin_auth_source, and a scanner_authorizer sentence.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
closed=0; sent=0
for slug in nfra-oplgtw-edge-auth-json-tiered; do
  e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
  [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=$((closed+1))
  sent=$((sent + $(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)))
done
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent"
acl=$(python - "$(native "$W/ZS1_PROOF.json")" "$(native "$W/ZS1_ACL_BEFORE.json")" "$(native "$W/ZS1_ACL_AFTER.json")" <<'EOF'
import json, os, sys
ok = False
try:
    n = json.load(open(sys.argv[1], encoding="utf-8")).get("updatewebacl_calls")
except Exception:
    n = None
have = os.path.exists(sys.argv[2]) and os.path.exists(sys.argv[3])
if n in (0, 1) and have:
    try:
        b = json.load(open(sys.argv[2], encoding="utf-8")); a = json.load(open(sys.argv[3], encoding="utf-8"))
        same = bool(b.get("rules_sha256")) and b.get("rules_sha256") == a.get("rules_sha256") and len(b.get("rules", [])) == len(a.get("rules", [])) > 0
        print("WebACL rules %s, updatewebacl_calls %s" % ("identical before and after" if same else "DIFFER before and after", n)); ok = same
    except Exception as e:
        print("WebACL before/after files unreadable (%s), updatewebacl_calls %s" % (type(e).__name__, n))
elif n == 0 and not have:
    print("WebACL not changed by this apply, updatewebacl_calls 0"); ok = True
else:
    print("WebACL conditions not met (updatewebacl_calls %s)" % n)
print("OK" if ok else "NO")
EOF
)
acl=$(printf '%s' "$acl" | tr -d '\r'); printf '%s\n' "$acl" | sed '$d'
res=$(python - "$(native "$W/ZS1_PROOF.json")" <<'EOF'
import json, sys, urllib.error, urllib.request
BASE = "https://opalinvest.dev"
def status(path):
    try:
        r = urllib.request.urlopen(urllib.request.Request(BASE + path, method="GET"), timeout=30)
        return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return "ERR-" + type(e).__name__
bare = status("/json-tiered/market-overview/rsi-summary.json")
twin = status("/api/general/json-tiered/market-overview/rsi-summary.json")
print("live bare path unauthenticated: %s; twin unauthenticated: %s" % (bare, twin))
ok = bare in (401, 403) and twin in (401, 403)
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    pf = d.get("bare_unauth_status") in (401, 403) and d.get("twin_authed_status") == 200 and bool(str(d.get("twin_auth_source", "")).strip()) and bool(str(d.get("scanner_authorizer", "")).strip())
    print("proof file: bare %s, twin authenticated %s, scanner authorizer read %s" % (d.get("bare_unauth_status"), d.get("twin_authed_status"), "yes" if str(d.get("scanner_authorizer", "")).strip() else "no"))
    ok = ok and pf
except Exception as e:
    print("proof file: absent or unreadable (%s)" % type(e).__name__); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$(printf '%s\n' "$acl" | tail -1)" = OK ] && [ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
