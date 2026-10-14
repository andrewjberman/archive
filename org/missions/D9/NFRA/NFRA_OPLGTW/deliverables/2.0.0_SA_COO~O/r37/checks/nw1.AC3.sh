#!/usr/bin/env bash
# OPLGTW OG-nw-1 AC2b (round-37 FWD22-W6, FWD-22 G6, PHASE A): the grant file and the ask.
#  - infra/aws/terraform/opal-gateway/news_read_iam.tf: ONE aws_iam_role_policy; the only actions dynamodb:Query and dynamodb:GetItem;
#    no Scan, no wildcard action, no bare '*' resource; at least three table ARNs;
#  - W/NEVER_WIDEN_ASK_OG-nw-1.md names its seven items.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~82"
res=$(python - "$(native "infra/aws/terraform/opal-gateway/news_read_iam.tf")" "$(native "$W/NEVER_WIDEN_ASK_OG-nw-1.md")" <<'EOF'
import re, sys
ok = True
try:
    t = open(sys.argv[1], encoding="utf-8").read()
    pol = len(re.findall(r'resource\s+"aws_iam_role_policy"', t))
    acts = set(re.findall(r'"(dynamodb:[A-Za-z*]+|[a-z0-9]+:\*|\*)"', t))
    arns = set(re.findall(r'arn:aws:dynamodb:[^"\s]+', t))
    bare = len(re.findall(r'Resource\s*=\s*"\*"', t))
    print("grant: policies %d (want 1); actions %s (want only Query and GetItem); dynamodb ARNs %d (want >= 3); bare * resources %d (want 0)" % (pol, sorted(acts), len(arns), bare))
    ok = pol == 1 and acts == {"dynamodb:Query", "dynamodb:GetItem"} and len(arns) >= 3 and bare == 0
except Exception as e:
    print("grant file absent or unreadable (%s)" % type(e).__name__); ok = False
try:
    a = open(sys.argv[2], encoding="utf-8").read().lower()
    need = ["diff", "tools", "widening", "grant", "both branches", "rollback", "triggers"]
    n = sum(1 for k in need if k in a)
    print("ask sections: %d of 7" % n); ok = ok and n == 7
except Exception:
    print("ask sections: 0 of 7 (absent)"); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
