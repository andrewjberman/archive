#!/usr/bin/env bash
# OPLGTW OG-ec-2 AC2 (round-37 G2-ECLIPSE, PHASE B): the fix is deployed from the repo's bytes and the Eclipse silver guard reads PASS.
#  - ledger nfra-oplgtw-eclipse-converter is CLOSED at HEAD, its sentinel gone;
#  - W/EC2_PROOF.json: deployed code sha256 equals the repo's, the sweep was driven by the applier (not waited for), the guard reads PASS with expected = landed, missing 0, alien 0,
#    the Eclipse silver freshness in trading days is stated and is at most 1.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS"
slug=nfra-oplgtw-eclipse-converter; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$W/EC2_PROOF.json" ] || { echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent"; echo "EC2_PROOF.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$W/EC2_PROOF.json")" "$(native "$W/EC2_PLAN.json")" <<'PYEOF'
import json, sys
p = json.load(open(sys.argv[1], encoding="utf-8")); plan = json.load(open(sys.argv[2], encoding="utf-8"))
eq = p.get("deployed_code_sha256") == plan.get("repo_code_sha256") and bool(p.get("deployed_code_sha256"))
driven = p.get("sweep_driven_by_applier") is True
g = p.get("guard") or {}
guard = g.get("verdict") == "PASS" and g.get("expected") == g.get("landed") and g.get("missing") == 0 and g.get("alien") == 0
td = p.get("freshness_td")
fresh = isinstance(td, int) and 0 <= td <= 1
print("deployed code equals the repo's: %s; sweep driven by the applier: %s; guard %s (expected %s landed %s missing %s alien %s); Eclipse silver freshness %s trading day(s)" % (
    "yes" if eq else "no", "yes" if driven else "no", g.get("verdict"), g.get("expected"), g.get("landed"), g.get("missing"), g.get("alien"), td))
sys.exit(0 if eq and driven and guard and fresh else 1)
PYEOF
); rc=$?
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent"
printf '%s\n' "$res" | tr -d '\r'
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
