#!/usr/bin/env bash
# OPLGTW OG-ap-24 AC1 (round-37 GRANTS-BATCH, PHASE A): the vendor-roles .tf equals what the generator derives from the merged adapters; structure of the grant; the plan reads no destroy.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS"
TF=infra/aws/terraform/opal-gateway/client_vendor_roles_iam.tf
[ -f "$TF" ] && [ -f "$W/gr_grant_gen.py" ] && [ -f "$W/GR_PLAN.txt" ] || { echo "client_vendor_roles_iam.tf, gr_grant_gen.py or GR_PLAN.txt absent"; echo "RESULT: FAIL"; exit 1; }
timeout 100 python "$W/gr_grant_gen.py" --check > /tmp/gr_check.out 2>&1; gc=$?
res=$(python - "$TF" "$W/GR_PLAN.txt" <<'PYEOF'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
code = "\n".join(l for l in t.splitlines() if not l.lstrip().startswith("#"))
roles = len(re.findall(r'resource\s+"aws_iam_role"', code))
wild = 1 if re.search(r'Resource\s*=\s*(\[\s*)?"\*"', code) else 0
pd = 1 if re.search(r's3:(Put|Delete)', code) else 0
princ = set(re.findall(r'AWS"?\s*[:=]\s*"?(arn:aws:iam::[0-9]+:role/[A-Za-z0-9_.+=,@/-]+|[A-Za-z0-9_.-]*gateway[A-Za-z0-9_.-]*)', code))
other = [p for p in princ if "opal-gateway-role" not in p and "aws_iam_role.gw" not in p]
plan = open(sys.argv[2], encoding="utf-8").read()
m = re.search(r"(\d+) to add, (\d+) to change, (\d+) to destroy", plan)
print("generator --check exit %%GC%% (want 0); roles in the .tf %d (want 5); wildcard resource %d (want 0); put or delete in actions %d (want 0); trust principals other than the gateway role %d (want 0); plan: %s" % (roles, wild, pd, len(other), m.group(0) if m else "NONE"))
ok = roles == 5 and wild == 0 and pd == 0 and not other and m and m.group(3) == "0"
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r' | sed "s/%GC%/$gc/")
printf '%s\n' "$res" | sed '$d'
[ "$gc" = 0 ] && [ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
