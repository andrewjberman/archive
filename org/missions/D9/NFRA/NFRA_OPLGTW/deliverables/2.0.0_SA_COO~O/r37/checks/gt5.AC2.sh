#!/usr/bin/env bash
# OPLGTW OG-gt-5 AC2 (round-37 G1-TYPED, FWD-22): the invoke grant file and the ask (PHASE A; the invoke itself is Phase B).
#  - infra/aws/terraform/opal-gateway/harvest_published_invoke_iam.tf: ONE aws_iam_role_policy, the only action
#    lambda:InvokeFunction, exactly one function ARN, no wildcard action and no lambda:* ;
#  - W/NEVER_WIDEN_ASK_OG-gt-5.md names its seven items.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~76"
res=$(python - "$(native "infra/aws/terraform/opal-gateway/harvest_published_invoke_iam.tf")" "$(native "$W/NEVER_WIDEN_ASK_OG-gt-5.md")" <<'EOF'
import re, sys
ok = True
try:
    t = open(sys.argv[1], encoding="utf-8").read()
    pol = len(re.findall(r'resource\s+"aws_iam_role_policy"', t))
    acts = set(re.findall(r'"(lambda:[A-Za-z*]+|[a-z0-9]+:\*|\*)"', t))
    arns = set(re.findall(r'arn:aws:lambda:[^"\s]+', t))
    wild = [a for a in acts if a.endswith("*")]
    print("grant: policies %d (want 1); actions %s (want only lambda:InvokeFunction); function ARNs %d (want 1); wildcard actions %d (want 0)" % (pol, sorted(acts), len(arns), len(wild)))
    ok = pol == 1 and acts == {"lambda:InvokeFunction"} and len(arns) == 1 and not wild
except Exception as e:
    print("grant file absent or unreadable (%s)" % type(e).__name__); ok = False
try:
    a = open(sys.argv[2], encoding="utf-8").read().lower()
    need = ["diff", "tool", "widening", "grant", "both branches", "rollback", "triggers"]
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
