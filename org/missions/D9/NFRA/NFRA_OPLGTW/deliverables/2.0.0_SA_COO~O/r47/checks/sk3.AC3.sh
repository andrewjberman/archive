#!/usr/bin/env bash
# OPLGTW OG-sk-3 AC3: the bucket-side fact. W/SK3_BUCKET_POLICY.json (W = deliverables/0.9.0_WK_NFRA_OPLGTW~179/):
#  {"body": {"bucket": "opal-data-49financial", "owner_file": "<repo-relative .tf that creates the bucket>", "policy_file": "<repo-relative .tf holding the bucket policy, or null when none is declared>",
#            "policy_denies_unlisted_principals": <bool|null>, "names_gateway_catalog_role": <bool|null>, "identity_policy_alone_suffices": <bool>, "needs_change": <bool>, "reason": "<one or two sentences>"}}
#  Read here, not taken from the record: owner_file exists, is a .tf and holds the bucket name; policy_file is null or exists, is a .tf and holds the bucket name; needs_change is true exactly when the policy denies unlisted principals and does not name the catalog role;
#  needs_change true is a finding for the issuer (a BLOCKING row), not a failure of the check.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W=org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~179
[ -f "$W/SK3_BUCKET_POLICY.json" ] || { echo "SK3_BUCKET_POLICY.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python3 -I - "$(native "$W")" <<'PYEOF'
import json, os, sys
W = sys.argv[1]
d = json.load(open(os.path.join(W, "SK3_BUCKET_POLICY.json"), encoding="utf-8")); d = d.get("body", d)
ok = True


def holds(path):
    try:
        return path.endswith(".tf") and "opal-data-49financial" in open(path, encoding="utf-8", errors="replace").read()
    except Exception:
        return False


def say(label, cond):
    global ok
    ok = ok and bool(cond)
    print("%s: %s" % (label, "ok" if cond else "NOT OK"))


say("bucket named opal-data-49financial; owner_file %s is a .tf that holds the bucket name (read here)" % d.get("owner_file"), d.get("bucket") == "opal-data-49financial" and holds(d.get("owner_file") or ""))
pf = d.get("policy_file")
say("policy_file %s is null or a .tf that holds the bucket name (read here)" % pf, pf is None or holds(pf))
den, nam, nc = d.get("policy_denies_unlisted_principals"), d.get("names_gateway_catalog_role"), d.get("needs_change")
consistent = isinstance(nc, bool) and isinstance(d.get("identity_policy_alone_suffices"), bool) and ((nc is True) == (den is True and nam is False)) and (pf is not None or (den is None and nam is None and nc is False))
say("needs_change %s is consistent with denies_unlisted %s and names_catalog_role %s (a missing policy file means no denial and no change)" % (nc, den, nam), consistent)
say("reason stated", isinstance(d.get("reason"), str) and len(d["reason"]) >= 30)
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
