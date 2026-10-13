#!/usr/bin/env bash
# OPLGTW OG-hv-1 AC2 (round-37 R4, FWD-21): the asset-manager principal census and the release ask.
#  - W/HV1_PRINCIPALS.json names the IDENTITY store admission reads (PRD v2.8; never the grant store) and carries both
#    denominators (identity-store principals >= 1, audit-lake principals over 30 days >= 1),
#    at least one principal row, an asset_manager field (true/false/"unknown") with its source on EVERY row, and no
#    plaintext email anywhere in the file (an '@' followed by a domain counts; the email_domain field holds no '@');
#  - W/NEVER_WIDEN_ASK_OG-hv-1.md names its seven required items (v2.8: the role's S3 read named as a widening): diff by file, the two tools, the widening to the 24
#    prefixes for Opal principals only, the IAM grant with the builder's policy name, both branches, and the rollback.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~64"
res=$(python - "$(native "$W/HV1_PRINCIPALS.json")" "$(native "$W/NEVER_WIDEN_ASK_OG-hv-1.md")" <<'EOF'
import json, re, sys
ok = True
try:
    raw = open(sys.argv[1], encoding="utf-8").read(); d = json.loads(raw)
    den = d.get("denominator", {}); g = den.get("identity_store_principals"); st = str(d.get("identity_store", "")); a = den.get("audit_lake_principals_30d")
    rows = d.get("principals", [])
    am = all(isinstance(r, dict) and r.get("asset_manager") in (True, False, "unknown") and r.get("asset_manager_source")
             for r in rows) and len(rows) > 0
    emails = len(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw))
    print("census: identity_store %s; identity_store_principals %s, audit_lake_principals_30d %s; principals %d; asset_manager field on every row: %s; plaintext emails %d"
          % ("named" if st and "grant" not in st.lower() else "NOT-NAMED", g, a, len(rows), "yes" if am else "no", emails))
    ok = bool(st) and "grant" not in st.lower() and isinstance(g, int) and g >= 1 and isinstance(a, int) and a >= 1 and am and emails == 0
except Exception as e:
    print("census: absent or unreadable (%s)" % type(e).__name__); ok = False
try:
    t = open(sys.argv[2], encoding="utf-8").read().lower()
    need = ["harvest_list", "harvest_read", "24", "gateway-global-harvest-read-policy", "refused", "rollback", "widening"]
    n = sum(1 for k in need if k in t)
    print("ask sections: %d of 7" % n); ok = ok and n == 7
except Exception:
    print("ask sections: 0 of 7 (absent)"); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
