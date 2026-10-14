#!/usr/bin/env bash
# OPLGTW OG-zs-1 AC1 (round-37 ZS114-EDGE-AUTH): the traffic read, the Terraform change and the plan.
#  - W/ZS1_LOGREAD.json: window_days >= 7, a named source, non_portal_consumers == 0;
#  - infra/aws/terraform/portal-auth/cloudfront-distribution.tf at HEAD: behavior "/json-tiered/*" carries a viewer-request
#    association with local.auth_validator_edge_arn, and the twin "/api/general/json-tiered/*" still carries its three;
#  - W/ZS1_PLAN.txt reads "Plan: 0 to add, 1 to change, 0 to destroy".
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
res=$(python - "$(native "$W/ZS1_LOGREAD.json")" "$(native "$W/ZS1_PLAN.txt")" <<'EOF'
import json, re, subprocess, sys
ok = True
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    lr = isinstance(d.get("window_days"), int) and d["window_days"] >= 7 and bool(str(d.get("source", "")).strip()) and d.get("non_portal_consumers") == 0
    print("log read: window %s days, source %s, non-portal consumers %s" % (d.get("window_days"), "named" if str(d.get("source", "")).strip() else "NOT-NAMED", d.get("non_portal_consumers")))
    ok = ok and lr
except Exception as e:
    print("log read: absent or unreadable (%s)" % type(e).__name__); ok = False
tf = subprocess.run(["git", "show", "HEAD:infra/aws/terraform/portal-auth/cloudfront-distribution.tf"], capture_output=True).stdout.decode("utf-8", "replace")
def block(path):
    i = tf.find('path_pattern             = "%s"' % path)
    if i < 0:
        i = tf.find('path_pattern = "%s"' % path)
    if i < 0:
        return ""
    j = tf.find("ordered_cache_behavior", i + 10)
    k = tf.find("\n  # ", i + 10)
    ends = [x for x in (j, k) if x > 0]
    return tf[i:min(ends)] if ends else tf[i:]
b7, b6 = block("/json-tiered/*"), block("/api/general/json-tiered/*")
v = bool(re.search(r'event_type\s*=\s*"viewer-request"\s*\n\s*lambda_arn\s*=\s*local\.auth_validator_edge_arn', b7))
twin = len(re.findall(r"lambda_function_association", b6))
print("behavior /json-tiered/* carries auth-validator-edge viewer-request: %s; twin associations %d of 3" % ("yes" if v else "no", twin))
ok = ok and v and twin == 3
try:
    p = open(sys.argv[2], encoding="utf-8", errors="replace").read()
    m = re.search(r"Plan:\s*0 to add,\s*([12]) to change,\s*0 to destroy", p)
    pl = bool(m) and (m.group(1) == "1" or "aws_wafv2_web_acl.opal_cloudfront_protection" in p)
    print("plan 0 to add, %s to change, 0 to destroy: %s (a second change must be the named WebACL churn)" % (m.group(1) if m else "?", "yes" if pl else "no"))
    ok = ok and pl
except Exception:
    print("plan 0 to add, 1 to change, 0 to destroy: no (absent)"); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
