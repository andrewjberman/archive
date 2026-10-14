#!/usr/bin/env bash
# OPLGTW OG-mg-1 AC1 (round-37, the r30 grant writes, Phase A): the before-record and the ask exist and are complete.
#  - W/MG1_BEFORE.json names BOTH principals by role ("andrew", "bbg"), each with pk_hash and its current profile/grant
#    state (null when none), and the store's denominator (POLICY# items scanned, principal_profile records);
#  - W/NEVER_WIDEN_ASK_OG-mg-1.md names both records to write, the 13-month window, the mirror, the rollback (revoke), and
#    holds no email address.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
python - "$(native "$W/MG1_BEFORE.json")" "$(native "$W/NEVER_WIDEN_ASK_OG-mg-1.md")" <<'EOF'
import json, os, re, sys
ok = True
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    rows = {r.get("role"): r for r in d.get("principals", []) if isinstance(r, dict)}
    roles_ok = {"andrew", "bbg"} <= set(rows) and all(rows[k].get("pk_hash") and "profile" in rows[k] for k in ("andrew", "bbg"))
    den = d.get("denominator", {})
    den_ok = isinstance(den.get("policy_items_scanned"), int) and isinstance(den.get("principal_profiles"), int)
    print("before-record: roles andrew+bbg with pk_hash and state: %s; denominator printed: %s" % ("yes" if roles_ok else "no", "yes" if den_ok else "no"))
    ok = roles_ok and den_ok
except Exception as e:
    print("before-record: absent or unreadable (%s)" % type(e).__name__); ok = False
try:
    t = open(sys.argv[2], encoding="utf-8").read()
    need = ["Andrew", "Bloomberg", "13", "mirror", "rollback", "revoke"]
    n = sum(1 for k in need if k.lower() in t.lower())
    emails = len(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", t))
    print("ask items: %d of %d; email addresses in the ask: %d (want 0)" % (n, len(need), emails))
    ok = ok and n == len(need) and emails == 0
except Exception:
    print("ask items: 0 of 6 (absent)"); ok = False
print("RESULT: " + ("PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
EOF
