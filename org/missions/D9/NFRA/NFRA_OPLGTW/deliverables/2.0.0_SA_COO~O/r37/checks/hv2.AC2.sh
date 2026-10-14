#!/usr/bin/env bash
# OPLGTW OG-hv-2 AC2 (PHASE B, landed and served):
#  - ledgers nfra-oplgtw-harvest-read-grant and nfra-oplgtw-gateway-release-hv are CLOSED at HEAD, sentinels gone;
#  - EC2_MANIFEST deployed_commit equals the release, and runbook 7.2 names it (rb.AC2);
#  - W/HV2_IAM_SIM.json: the role is allowed on a packs/ key and a wsj/harvest/ key, implicitDeny on an unlisted prefix;
#  - W/HV2_SERVED.json, read on the host through the INSTALLED code: both tools listed; an Opal principal reads one real
#    packs/ input_ledger.json; a non-Opal principal is refused on packs/ and wsj/harvest/; an off-list prefix is refused;
#    zero S3 calls on a refusal; and (PRD v2.8) the SAME unprofiled standard-tier Opal principal is refused one
#    schwab_* tool and blackdiamond_list_fees (the research-only arm).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
closed=0; sent=0
for slug in nfra-oplgtw-harvest-read-grant nfra-oplgtw-gateway-release-hv; do
  e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
  [ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=$((closed+1))
  sent=$((sent + $(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)))
done
rel=NONE; [ -f "$W/hv2_release.json" ] && rel=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha','NONE'))" "$(native "$W/hv2_release.json")" | tr -d '\r')
dep=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'].get('deployed_commit','NONE'))" | tr -d '\r')
# Normalise both commits to full hashes before comparing (a short release_sha read as FAIL on a correct deploy;
# found by 0.7.0_AE_CloudOps~Z msg 33988).
full() { git rev-parse --verify --quiet "$1^{commit}" 2>&1 | tr -d '' | grep -E "^[0-9a-f]{40}$" || printf '%s' "$1"; }
[ "$rel" != NONE ] && rel=$(full "$rel"); [ "$dep" != NONE ] && dep=$(full "$dep")
rb=FAIL; bash org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/round2/checks/rb.AC2.sh >/dev/null 2>&1 && rb=PASS
res=$(python - "$(native "$W/HV2_IAM_SIM.json")" "$(native "$W/HV2_SERVED.json")" <<'EOF'
import json, sys
try:
    s = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception:
    s = {}
print("simulate packs=%s wsj_harvest=%s control_unlisted=%s" % (s.get("packs"), s.get("wsj_harvest"), s.get("control_unlisted")))
sim_ok = s.get("packs") == "allowed" and s.get("wsj_harvest") == "allowed" and s.get("control_unlisted") == "implicitDeny"
try:
    b = json.load(open(sys.argv[2], encoding="utf-8")).get("body", {})
except Exception:
    b = {}
tl = b.get("tools_listed")
srv = (isinstance(tl, list) and {"harvest_list", "harvest_read"} <= set(tl) and b.get("opal_packs_read") is True
       and b.get("non_opal_refused_packs") is True and b.get("non_opal_refused_wsj") is True
       and b.get("off_prefix_refused") is True and b.get("s3_calls_on_refusal") == 0
       and b.get("research_only_schwab_refused") is True and b.get("research_only_bd_refused") is True)
print("served fields: %s" % ("yes" if srv else "no"))
print("OK" if sim_ok and srv else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r')
echo "ledgers CLOSED $closed of 2; sentinels at HEAD $sent"
echo "manifest deployed_commit=${dep:0:10}; release_sha=${rel:0:10}; equal=$([ "$dep" = "$rel" ] && echo yes || echo no); rb.AC2 $rb"
printf '%s\n' "$res" | sed '$d'
[ "$closed" = 2 ] && [ "$sent" = 0 ] && [ "$rel" != NONE ] && [ "$dep" = "$rel" ] && [ "$rb" = PASS ] && [ "$(printf '%s\n' "$res" | tail -1)" = OK ] \
  && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
