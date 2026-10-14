#!/usr/bin/env bash
# OPLGTW OG-ap-17 AC2 (Phase B, OG-bd-3 served):
# - ledger nfra-oplgtw-gateway-release-bd3 is CLOSED at HEAD with its sentinel gone;
# - EC2_MANIFEST deployed_commit equals the release, and runbook 7.2 names it (rb.AC2);
# - W/AP17_SERVED.json, read on the host through the INSTALLED code (in-process, synthetic principals): a PROFILED
#   master_admin is admitted blackdiamond_list_fees, a PROFILED standard principal is denied it, and the unprofiled
#   cases are bd-2's (master_admin admitted, standard denied); objects_written 0.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"; slug=nfra-oplgtw-gateway-release-bd3
entries=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${slug}_deploy_completion\.md$")
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
closed=no; [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=yes
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
rel=NONE; [ -f "$W/ap17_release.json" ] && rel=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha','NONE'))" "$(native "$W/ap17_release.json")" | tr -d '\r')
dep=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
# Normalise both commits to full hashes before comparing (a short release_sha read as FAIL on a correct deploy;
# found by 0.7.0_AE_CloudOps~Z msg 33988).
full() { git rev-parse --verify --quiet "$1^{commit}" 2>&1 | tr -d '' | grep -E "^[0-9a-f]{40}$" || printf '%s' "$1"; }
[ "$rel" != NONE ] && rel=$(full "$rel"); [ "$dep" != NONE ] && dep=$(full "$dep")
rb=FAIL; bash org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/round2/checks/rb.AC2.sh >/dev/null 2>&1 && rb=PASS
srv=$(python - "$(native "$W/AP17_SERVED.json")" <<'EOF'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8")); b = d.get("body", {})
except Exception:
    print("absent"); raise SystemExit(0)
ok = (b.get("installed_code") is True and b.get("bd_profiled_master_admin_admitted") is True
      and b.get("bd_profiled_standard_denied") is True and b.get("bd_unprofiled_master_admin_admitted") is True
      and b.get("bd_unprofiled_standard_denied") is True and b.get("objects_written") == 0
      and bool(d.get("ssm_command_id")))
print("yes" if ok else "no")
EOF
)
srv=$(printf '%s' "$srv" | tr -d '\r')
echo "$slug: entries at HEAD $entries; status CLOSED=$closed; sentinel at HEAD=$([ "$sent" = 0 ] && echo no || echo yes)"
echo "manifest deployed_commit=${dep:0:10}; release_sha=${rel:0:10}; equal=$([ "$dep" = "$rel" ] && echo yes || echo no); rb.AC2 $rb; served bd-3 fields: $srv"
[ "$entries" -ge 1 ] && [ "$closed" = yes ] && [ "$sent" = 0 ] && [ "$rel" != NONE ] && [ "$dep" = "$rel" ] && [ "$rb" = PASS ] && [ "$srv" = yes ] \
  && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
