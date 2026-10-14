#!/usr/bin/env bash
# OPLGTW OG-cl-0 AC1 (round-37 G1-TYPED, FWD-22 G2): the reader-role inventory has its denominator, every vendor row, and a status each.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~83"
res=$(python - "$(native "$W/G2_ROLES.json")" <<'EOF'
import json, re, sys
ok = True
try:
    raw = open(sys.argv[1], encoding="utf-8").read(); d = json.loads(raw)
    den = d.get("denominator", {}); sc, m = den.get("roles_scanned"), den.get("roles_with_s3_read_on_client_buckets")
    v = d.get("vendors", {})
    need = ["blackdiamond", "orion", "eclipse", "schwab", "commonwealth", "smartx", "taxsma"]
    good = sum(1 for k in need if isinstance(v.get(k), dict) and v[k].get("status") in ("EXISTING-FIT", "NEEDS-NARROWING", "MISSING") and str(v[k].get("why", "")).strip())
    roles = d.get("roles", [])
    rowok = all(isinstance(r, dict) and r.get("role") and "s3_reads" in r and r.get("one_firm") in (True, False, "unknown") for r in roles)
    leaks = len(re.findall(r"AKIA[0-9A-Z]{16}|aws_secret", raw))
    print("roles: scanned %s, with S3 read on client buckets %s, rows %d, well-formed %s; vendors with a status and a reason %d of 7; credentials in file %d; ask_inputs present %s"
          % (sc, m, len(roles), "yes" if rowok else "no", good, leaks, "yes" if d.get("ask_inputs") else "no"))
    ok = isinstance(sc, int) and sc >= 1 and isinstance(m, int) and m >= 0 and len(roles) == m and rowok and good == 7 and leaks == 0 and bool(d.get("ask_inputs"))
except Exception as e:
    print("roles: absent or unreadable (%s)" % type(e).__name__); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
